#!/usr/bin/env node
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import path from 'node:path';
import fs from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../../../..');
const PAGE = 'file://' + path.join(ROOT, 'index.html');

const VIEWPORTS = { phone: 390, narrow: 320, tablet: 768, laptop: 1180, wide: 1440 };

const ok = (detail) => ({ ok: true, detail });
const fail = (detail) => ({ ok: false, detail });

/* ---- 通道：cdp 连本机常驻 headless Chrome（不在就拉起一个），launch 用自带 chromium 无头新开 ---- */
const CDP_URL = process.env.VERIFY_CDP || 'http://127.0.0.1:9333';
const CHROME_BIN = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

const cdpAlive = async () => {
  try {
    const res = await fetch(CDP_URL + '/json/version', { signal: AbortSignal.timeout(1500) });
    return res.ok;
  } catch {
    return false;
  }
};

const ensureCdp = async () => {
  if (await cdpAlive()) return;
  if (!fs.existsSync(CHROME_BIN)) {
    console.error(`CDP ${CDP_URL} 不在线，且没找到 ${CHROME_BIN}。有人在机器前可用：--channel launch`);
    process.exit(2);
  }
  const child = spawn(
    CHROME_BIN,
    [
      '--headless=new',
      `--remote-debugging-port=${new URL(CDP_URL).port}`,
      '--remote-allow-origins=*',
      '--user-data-dir=/tmp/cdp-d',
      '--hide-scrollbars',
      'about:blank',
    ],
    { detached: true, stdio: 'ignore' },
  );
  child.unref();
  for (let waited = 0; waited < 20000; waited += 400) {
    if (await cdpAlive()) return;
    await new Promise((resolve) => setTimeout(resolve, 400));
  }
  console.error(`CDP ${CDP_URL} 拉起超时，20 秒内 /json/version 没响应`);
  process.exit(2);
};

const openBrowser = async (channel) => {
  if (channel === 'cdp') {
    await ensureCdp();
    return chromium.connectOverCDP(CDP_URL);
  }
  try {
    return await chromium.launch({ headless: true });
  } catch (err) {
    console.error(`自带 chromium 启动失败：${err.message.split('\n')[0]}\n先跑 npx playwright install chromium`);
    process.exit(2);
  }
};

export const runSuite = async (picked, browser, shots) => {
  const results = [];
  for (const feature of picked) {
    const ctx = await browser.newContext({
      viewport: { width: VIEWPORTS[feature.viewport], height: 900 },
      colorScheme: feature.scheme || 'light',
      ...(feature.context || {}),
    });
    const page = await ctx.newPage();
    const errors = [];
    page.on('console', (m) => m.type() === 'error' && errors.push(m.text()));
    page.on('pageerror', (e) => errors.push(e.message));
    await page.goto(PAGE, { waitUntil: 'load' });
    await page.evaluate(() => {
      window.__verifyErrors = [];
      window.addEventListener('error', (e) => window.__verifyErrors.push(e.message));
    });
    await page.waitForTimeout(300);

    let result;
    try {
      result = await feature.run(page, browser);
    } catch (err) {
      result = fail(`抛错 ${err.message.split('\n')[0]}`);
    }
    if (errors.length && feature.id !== 'no-errors') result.detail += `；控制台: ${errors[0]}`;

    if (shots) {
      fs.mkdirSync(shots, { recursive: true });
      const file = path.join(shots, `${feature.id}.png`);
      await page.screenshot({ path: file, fullPage: false });
      result.shot = file;
    }
    results.push({ id: feature.id, name: feature.name, ...result });
    await ctx.close();
  }
  return results;
};

const settle = async (page, timeout = 4000) => {
  const started = Date.now();
  let last = -1;
  while (Date.now() - started < timeout) {
    const y = await page.evaluate(() => window.scrollY);
    if (y === last) return Date.now() - started;
    last = y;
    await page.waitForTimeout(80);
  }
  return -1;
};

const FEATURES = [
  {
    id: 'anchors',
    name: '目录锚点都能落地',
    viewport: 'laptop',
    async run(p) {
      const broken = await p.evaluate(() => {
        const ids = new Set([...document.querySelectorAll('[id]')].map((el) => el.id));
        return [...document.querySelectorAll('.rail-list a[href^="#"]')]
          .map((a) => a.getAttribute('href').slice(1))
          .filter((id) => !ids.has(id));
      });
      return broken.length ? fail(`断链 ${broken.join(', ')}`) : ok('全部命中');
    },
  },
  {
    id: 'overflow',
    name: '任何宽度都不横向溢出',
    viewport: 'phone',
    async run(p, browser) {
      const bad = [];
      for (const [name, width] of Object.entries(VIEWPORTS)) {
        const page = await browser.newPage({ viewport: { width, height: 900 } });
        await page.goto(PAGE, { waitUntil: 'load' });
        const over = await page.evaluate(
          () => document.documentElement.scrollWidth - window.innerWidth,
        );
        if (over > 1) bad.push(`${name}(${width}) 溢出 ${over}px`);
        await page.close();
      }
      return bad.length ? fail(bad.join('; ')) : ok(`${Object.keys(VIEWPORTS).length} 档宽度都没溢出`);
    },
  },
  {
    id: 'chapter-nav',
    name: '点目录跳到对应章，章节标题不被顶栏压住',
    viewport: 'laptop',
    async run(p) {
      await p.click('.rail-list a[href="#principles"]');
      const scrolled = await settle(p);
      if (scrolled < 0) return fail('点击后滚动 4 秒仍未停止');
      const top = await p.evaluate(
        () => document.getElementById('principles').getBoundingClientRect().top,
      );
      const active = await p.evaluate(
        () => document.querySelector('.rail-list a.on')?.getAttribute('href'),
      );
      const bar = await p.evaluate(() => {
        const rail = document.querySelector('.rail');
        return rail ? rail.getBoundingClientRect().width : 0;
      });
      if (top < 0) return fail(`目标章落到视口上方 ${Math.round(-top)}px`);
      if (top > 200) return fail(`目标章离顶部 ${Math.round(top)}px，跳转没到位`);
      if (active !== '#principles') return fail(`目录高亮停在 ${active}`);
      return ok(`落点 ${Math.round(top)}px，高亮正确，侧栏宽 ${Math.round(bar)}px`);
    },
  },
  {
    id: 'phone-toc',
    name: '手机上点章节，抽屉自动收起',
    viewport: 'phone',
    async run(p) {
      await p.click('#tocToggle + label, label[for="tocToggle"]').catch(() => {});
      await p.evaluate(() => {
        document.getElementById('tocToggle').checked = true;
      });
      await p.waitForTimeout(200);
      const open = await p.evaluate(() => document.getElementById('tocToggle').checked);
      await p.click('.rail-list a[href="#principles"]');
      await p.waitForTimeout(300);
      const closed = await p.evaluate(() => !document.getElementById('tocToggle').checked);
      if (!open) return fail('抽屉没打开，检查 label 关联');
      if (!closed) return fail('点章节后抽屉没收起');
      return ok('打开后点章节即收起');
    },
  },
  {
    id: 'filter',
    name: '技能过滤框能筛行，Esc 能清空',
    viewport: 'laptop',
    async run(p) {
      const total = await p.locator('table.filterable tr').count();
      await p.fill('#filter', '验证');
      await p.waitForTimeout(150);
      const shown = await p.locator('table.filterable tr:visible').count();
      if (shown <= 1) return fail(`过滤后只剩 ${shown} 行，等于没筛到`);
      if (shown >= total) return fail(`过滤后仍是 ${shown} 行，等于没生效`);
      await p.press('#filter', 'Escape');
      await p.waitForTimeout(150);
      const restored = await p.locator('table.filterable tr:visible').count();
      if (restored !== total) return fail(`Esc 后 ${restored} 行，原本 ${total} 行`);
      return ok(`筛到 ${shown}/${total} 行，Esc 复原`);
    },
  },
  {
    id: 'figure-zoom',
    name: '手机上点图放大，宽屏不放大',
    viewport: 'phone',
    async run(p, browser) {
      const fig = p.locator('figure.devfig').first();
      await fig.scrollIntoViewIfNeeded();
      await fig.click();
      await p.waitForTimeout(200);
      const zoomed = await fig.evaluate((el) => el.classList.contains('zoom'));
      const wide = await browser.newPage({ viewport: { width: 1180, height: 900 } });
      await wide.goto(PAGE, { waitUntil: 'load' });
      const wideZoom = await wide.evaluate(() => {
        const f = document.querySelector('figure.devfig');
        f?.click();
        return f?.classList.contains('zoom');
      });
      await wide.close();
      if (!zoomed) return fail('手机上点图没有放大');
      if (wideZoom) return fail('宽屏也放大了，应该只在窄屏生效');
      return ok('手机上放大，宽屏不受影响');
    },
  },
  {
    id: 'figures-drawn',
    name: '每张图都画出来了',
    viewport: 'laptop',
    async run(p) {
      const bad = await p.evaluate(() =>
        [...document.querySelectorAll('figure.devfig svg')]
          .map((svg, i) => ({ i, r: svg.getBoundingClientRect() }))
          .filter(({ r }) => r.width < 200 || r.height < 100)
          .map(({ i, r }) => `#${i + 1} ${Math.round(r.width)}x${Math.round(r.height)}`),
      );
      const count = await p.locator('figure.devfig').count();
      return bad.length ? fail(`尺寸异常 ${bad.join(', ')}`) : ok(`${count} 张全部有尺寸`);
    },
  },
  {
    id: 'reveal',
    name: '滚到的正文真的显示出来',
    viewport: 'laptop',
    async run(p) {
      await p.evaluate(() => window.scrollTo(0, document.body.scrollHeight * 0.5));
      await p.waitForTimeout(1200);
      const hidden = await p.evaluate(
        () =>
          [...document.querySelectorAll('[data-rv]')].filter(
            (el) =>
              el.getBoundingClientRect().top < window.innerHeight * 0.7 &&
              el.getBoundingClientRect().bottom > 0 &&
              Number(getComputedStyle(el).opacity) < 0.5,
          ).length,
      );
      return hidden ? fail(`视口内还有 ${hidden} 个元素是透明的`) : ok('入场动画后无残留隐藏');
    },
  },
  {
    id: 'no-errors',
    name: '没有脚本报错、外链请求和加载失败',
    viewport: 'phone',
    async run(p) {
      const errors = await p.evaluate(() => window.__verifyErrors || []);
      const external = await p.evaluate(() =>
        performance
          .getEntriesByType('resource')
          .map((e) => e.name)
          .filter((n) => /^https?:/.test(n)),
      );
      if (errors.length) return fail(`报错 ${errors.join(' | ')}`);
      if (external.length) return fail(`外链 ${external.join(', ')}`);
      return ok('无报错、无外链');
    },
  },
  {
    id: 'contrast',
    name: '深浅两套配色下正文都读得清',
    viewport: 'laptop',
    async run(p, browser) {
      const measure = async (scheme) => {
        const page = await browser.newPage({ viewport: { width: 1180, height: 900 }, colorScheme: scheme });
        await page.goto(PAGE, { waitUntil: 'load' });
        const bad = await page.evaluate(() => {
          const lum = (c) => {
            const [r, g, b] = c.map((v) => {
              v /= 255;
              return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4;
            });
            return 0.2126 * r + 0.7152 * g + 0.0722 * b;
          };
          const parse = (s) => {
            const m = s.match(/[\d.]+/g)?.map(Number) || [0, 0, 0];
            return { rgb: m.slice(0, 3), a: m.length > 3 ? m[3] : 1 };
          };
          const bgOf = (el) => {
            let n = el;
            while (n) {
              const c = parse(getComputedStyle(n).backgroundColor);
              if (c.a > 0.5) return c.rgb;
              n = n.parentElement;
            }
            return [255, 255, 255];
          };
          const ratio = (a, b) => {
            const [l1, l2] = [lum(a), lum(b)].sort((x, y) => y - x);
            return (l1 + 0.05) / (l2 + 0.05);
          };
          const probes = [
            ['正文', 'main p'],
            ['二级标题', 'main > h2 > .ttl'],
            ['目录项', '.rail-list a'],
            ['图注', 'figcaption'],
          ];
          return probes.flatMap(([label, sel]) => {
            const el = document.querySelector(sel);
            if (!el) return [];
            const fg = parse(getComputedStyle(el).color);
            const r = ratio(fg.rgb, bgOf(el));
            return r < 4.5 ? [`${label} ${r.toFixed(2)}:1`] : [];
          });
        });
        await page.close();
        return bad.map((b) => `${scheme} ${b}`);
      };
      const bad = [...(await measure('light')), ...(await measure('dark'))];
      return bad.length ? fail(bad.join('; ')) : ok('正文与目录项都过 4.5:1');
    },
  },
  {
    id: 'tap-targets',
    name: '手机上的可点区域够大',
    viewport: 'phone',
    async run(p) {
      const small = await p.evaluate(() =>
        [...document.querySelectorAll('.rail-list a, #filter, .cover .go')]
          .map((el) => ({ el, r: el.getBoundingClientRect() }))
          .filter(({ r }) => r.height > 0 && r.height < 44)
          .map(({ el, r }) => `${(el.textContent || el.id).trim().slice(0, 12)} ${Math.round(r.height)}px`),
      );
      return small.length ? fail(`小于 44px: ${small.slice(0, 5).join(', ')}`) : ok('都过 44px');
    },
  },
  {
    id: 'reduced-motion',
    name: '系统要求减少动效时不播入场动画',
    viewport: 'laptop',
    context: { reducedMotion: 'reduce' },
    async run(p) {
      await p.waitForTimeout(150);
      const hidden = await p.evaluate(
        () =>
          [...document.querySelectorAll('[data-rv]')].filter(
            (el) => Number(getComputedStyle(el).opacity) < 0.5,
          ).length,
      );
      return hidden ? fail(`减少动效下仍有 ${hidden} 个元素是透明的，等于内容被藏住`) : ok('直接可见');
    },
  },
  {
    id: 'toc-coverage',
    name: '目录和正文章节一一对应',
    viewport: 'laptop',
    async run(p) {
      const { heads, links } = await p.evaluate(() => ({
        heads: [...document.querySelectorAll('main > h2[id]')].map((h) => h.id),
        links: [...document.querySelectorAll('.rail-list a[href^="#"]')].map((a) =>
          a.getAttribute('href').slice(1),
        ),
      }));
      const missingInToc = heads.filter((h) => !links.includes(h));
      const dangling = links.filter((l) => !heads.includes(l));
      if (missingInToc.length) return fail(`章节不在目录里 ${missingInToc.join(', ')}`);
      if (dangling.length) return fail(`目录指向不存在的章节 ${dangling.join(', ')}`);
      return ok(`${heads.length} 章两边一致`);
    },
  },
  {
    id: 'table-stacking',
    name: '窄屏表格每格都带表头标签',
    viewport: 'phone',
    async run(p) {
      const unlabeled = await p.evaluate(() =>
        [...document.querySelectorAll('table tr')]
          .slice(1)
          .flatMap((row) => [...row.querySelectorAll('td')])
          .filter((td) => !td.dataset.label)
          .map((td) => td.textContent.trim().slice(0, 10)),
      );
      return unlabeled.length ? fail(`${unlabeled.length} 格缺标签，例如 ${unlabeled.slice(0, 3).join(' / ')}`) : ok('全部带 data-label');
    },
  },
  {
    id: 'playbook-numbers',
    name: 'playbook 编号连续且齐全',
    viewport: 'laptop',
    async run(p) {
      const nums = await p.$$eval('h4.pb .pbnum', (ns) => ns.map((n) => n.textContent.trim()));
      const want = Array.from({ length: nums.length }, (_, i) => String(i + 1).padStart(2, '0'));
      if (!nums.length) return fail('一个编号都没有');
      const gap = nums.find((n, i) => n !== want[i]);
      return gap ? fail(`编号断在 ${gap}，期望 ${want[nums.indexOf(gap)]}`) : ok(`${nums.length} 个，01 到 ${nums.at(-1)}`);
    },
  },
  {
    id: 'page-search',
    name: '导轨全文检索：出结果、跳转落点在命中处、Esc 复原',
    viewport: 'laptop',
    async run(p) {
      await p.fill('#search', '否决窗口');
      await p.waitForTimeout(150);
      const n = await p.locator('.rail-results a').count();
      if (n < 1) return fail(`结果 ${n} 条`);
      await p.click('.rail-results a:first-child');
      const scrolled = await settle(p);
      if (scrolled < 0) return fail('点击后滚动 4 秒仍未停止');
      const cnt = await p.evaluate(() => document.querySelectorAll('main mark').length);
      if (cnt < 1) return fail(`正文命中标记 ${cnt} 个`);
      const { top, vh } = await p.evaluate(() => ({
        top: document.querySelector('main mark').getBoundingClientRect().top,
        vh: window.innerHeight,
      }));
      if (top < 0 || top > vh) return fail(`落点 ${Math.round(top)}px 在视口外`);
      await p.press('#search', 'Escape');
      await p.waitForTimeout(150);
      const back = await p.evaluate(() => ({
        results: document.querySelector('.rail-results').hidden,
        list: document.querySelector('.rail-list').hidden,
        marks: document.querySelectorAll('main mark').length,
      }));
      if (!back.results) return fail('Esc 后结果列表没藏起');
      if (back.list) return fail('Esc 后章节列表没复原');
      if (back.marks > 0) return fail(`Esc 后正文还剩 ${back.marks} 个标记`);
      await p.fill('#search', 'zzz无此词xyz');
      await p.waitForTimeout(150);
      const none = await p.evaluate(() => ({
        none: document.querySelector('.rail-none').hidden,
        rows: document.querySelectorAll('.rail-results a').length,
      }));
      if (none.none) return fail('零命中没显示「没有匹配」');
      if (none.rows > 0) return fail(`零命中仍有 ${none.rows} 条结果`);
      return ok(`结果 ${n} 条，落点 ${Math.round(top)}px，Esc 复原，零命中有提示`);
    },
  },
  {
    id: 'page-search-phone',
    name: '手机抽屉里检索：点结果抽屉收起并落到命中处',
    viewport: 'phone',
    async run(p) {
      await p.evaluate(() => {
        document.getElementById('tocToggle').checked = true;
      });
      await p.waitForTimeout(200);
      await p.fill('#search', '费曼');
      await p.waitForTimeout(150);
      const n = await p.locator('.rail-results a').count();
      if (n < 1) return fail(`结果 ${n} 条`);
      await p.click('.rail-results a:first-child');
      const scrolled = await settle(p);
      if (scrolled < 0) return fail('点击后滚动 4 秒仍未停止');
      const closed = await p.evaluate(() => !document.getElementById('tocToggle').checked);
      if (!closed) return fail('点结果后抽屉没收起');
      const cnt = await p.evaluate(() => document.querySelectorAll('main mark').length);
      if (cnt < 1) return fail(`正文命中标记 ${cnt} 个`);
      const { top, vh } = await p.evaluate(() => ({
        top: document.querySelector('main mark').getBoundingClientRect().top,
        vh: window.innerHeight,
      }));
      if (top < 0 || top > vh * 1.5) return fail(`落点 ${Math.round(top)}px 超出 1.5 屏`);
      return ok(`结果 ${n} 条，抽屉收起，落点 ${Math.round(top)}px`);
    },
  },
  {
    id: 'print-layout',
    name: '打印版式：版心收在 37em，深色系统打印不出深底图',
    extra: true,
    viewport: 'laptop',
    async run(p, browser) {
      const measure = async (scheme) => {
        const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, colorScheme: scheme });
        await page.goto(PAGE, { waitUntil: 'load' });
        await page.emulateMedia({ media: 'print' });
        await page
          .waitForFunction(
            () => [...document.querySelectorAll('[data-rv]')].every((el) => Number(getComputedStyle(el).opacity) >= 0.99),
            { timeout: 3000 },
          )
          .catch(() => {});
        const m = await page.evaluate(() => {
          const widths = [...document.querySelectorAll('main p')].map((el) =>
            Math.round(el.getBoundingClientRect().width / 10) * 10,
          );
          const counts = {};
          widths.forEach((w) => { counts[w] = (counts[w] || 0) + 1; });
          const mode = Number(Object.entries(counts).sort((a, b) => b[1] - a[1])[0][0]);
          const probe = document.createElement('i');
          probe.style.backgroundColor = 'var(--panel)';
          document.body.appendChild(probe);
          const prgb = getComputedStyle(probe).backgroundColor.match(/\d+/g)?.map(Number) || [0, 0, 0];
          probe.remove();
          const fill = getComputedStyle(document.querySelector('figure.devfig svg rect')).fill;
          const frgb = fill.match(/\d+/g)?.map(Number) || [0, 0, 0];
          const rail = document.querySelector('.rail');
          const rvBad = [...document.querySelectorAll('[data-rv]')].filter(
            (el) => Number(getComputedStyle(el).opacity) < 0.99,
          ).length;
          const fig = document.querySelector('figure.devfig svg').getBoundingClientRect();
          return {
            mode,
            panelMaxCh: Math.max(...prgb),
            fillMaxCh: Math.max(...frgb),
            railW: Math.round(rail.getBoundingClientRect().width),
            rvBad,
            figW: Math.round(fig.width),
            figH: Math.round(fig.height),
            overflow: document.documentElement.scrollWidth - window.innerWidth,
          };
        });
        await page.close();
        const bad = [];
        if (m.mode < 490 || m.mode > 560) bad.push(`${scheme} 版心众数 ${m.mode}px，应在 490–560（37em@10.5pt=518）`);
        if (m.panelMaxCh < 200) bad.push(`${scheme} --panel 最亮通道 ${m.panelMaxCh}，深色变量会印出深底`);
        if (m.fillMaxCh < 200) bad.push(`${scheme} 图面填充最亮通道 ${m.fillMaxCh}，打印是深色`);
        if (m.railW !== 0) bad.push(`${scheme} 目录导轨没藏起，宽 ${m.railW}px`);
        if (m.rvBad > 0) bad.push(`${scheme} 打印态 ${m.rvBad} 个元素透明`);
        if (m.figW < 200 || m.figH < 100) bad.push(`${scheme} 图尺寸 ${m.figW}x${m.figH}`);
        if (m.overflow > 1) bad.push(`${scheme} 横向溢出 ${m.overflow}px`);
        return bad;
      };
      const bad = [...(await measure('light')), ...(await measure('dark'))];
      return bad.length ? fail(bad.join('；')) : ok('两套配色下版心都在 518px 一带、图面浅色、导轨隐藏、无溢出');
    },
  },
  {
    id: 'appendix-anchors',
    name: '附录与页脚锚点：落点在章首 84px 一带，页脚可直达',
    viewport: 'laptop',
    async run(p) {
      await p.evaluate(() => {
        document.documentElement.style.scrollBehavior = 'auto';
      });
      const bad = [];
      const lands = [];
      for (const id of ['cheat', 'files', 'glossary', 'flows']) {
        const link = p.locator(`a[href="#${id}"]`).first();
        await link.scrollIntoViewIfNeeded();
        await link.click();
        const scrolled = await settle(p);
        if (scrolled < 0) {
          bad.push(`#${id} 点击后滚动 4 秒未停`);
          continue;
        }
        const m = await p.evaluate((id) => {
          const h = document.getElementById(id);
          const heads = [...document.querySelectorAll('main > h2[id]')];
          const next = heads[heads.indexOf(h) + 1];
          return {
            top: Math.round(h.getBoundingClientRect().top),
            y: Math.round(window.scrollY),
            vh: window.innerHeight,
            from: Math.round(h.offsetTop),
            to: next ? Math.round(next.offsetTop) : document.body.scrollHeight,
          };
        }, id);
        if (m.top < 40 || m.top > 140) bad.push(`#${id} 落点 ${m.top}px，应在 40–140（scroll-margin 84）`);
        const mid = m.y + m.vh / 2;
        if (mid < m.from || mid >= m.to) bad.push(`#${id} 视口中点 ${Math.round(mid)} 不在本节 offsetTop 范围 ${m.from}–${m.to}，落进别节`);
        lands.push(m.top);
      }
      await p.evaluate(() => { location.hash = '#colophon'; });
      const scrolledF = await settle(p);
      if (scrolledF < 0) bad.push('#colophon 滚动 4 秒未停');
      const foot = await p.evaluate(() => {
        const f = document.getElementById('colophon');
        return { found: !!f, top: f ? Math.round(f.getBoundingClientRect().top) : -1, vh: window.innerHeight };
      });
      if (!foot.found) bad.push(`页脚没有 id=colophon，深链落不了地（落点还在页首，scrollY=${await p.evaluate(() => Math.round(window.scrollY))}）`);
      else if (foot.top < 0 || foot.top > foot.vh - 40) bad.push(`#colophon 落点 ${foot.top}px，超出视口 ${foot.vh}px`);
      return bad.length ? fail(bad.join('；')) : ok(`附录 4 锚点落点 ${lands.join('/')}px，页脚直达落点 ${foot.top}px`);
    },
  },
];

const argOf = (flag) => {
  const i = process.argv.indexOf(flag);
  return i > -1 ? process.argv[i + 1] : null;
};

const main = async () => {
  const only = argOf('--feature');
  const json = process.argv.includes('--json');
  const shots = argOf('--out');
  const extras = process.argv.includes('--extra');
  const channel = argOf('--channel') || process.env.VERIFY_CHANNEL || 'cdp';
  if (!['cdp', 'launch'].includes(channel)) {
    console.error(`unknown channel: ${channel}. known: cdp, launch`);
    process.exit(2);
  }
  const picked = only
    ? FEATURES.filter((f) => f.id === only)
    : FEATURES.filter((f) => extras || !f.extra);
  if (!picked.length) {
    console.error(`unknown feature: ${only}. known: ${FEATURES.map((f) => f.id).join(', ')}`);
    process.exit(2);
  }

  const started = Date.now();
  const browser = await openBrowser(channel);
  const results = await runSuite(picked, browser, shots);
  await browser.close();

  if (json) {
    console.log(JSON.stringify({ channel, ms: Date.now() - started, results }, null, 2));
  } else {
    for (const r of results) {
      console.log(`${r.ok ? 'PASS' : 'FAIL'}  ${r.id.padEnd(18)} ${r.name}\n      ${r.detail}`);
    }
    console.log(`\n[${channel}] ${results.filter((r) => r.ok).length}/${results.length} 通过，用时 ${((Date.now() - started) / 1000).toFixed(1)}s`);
  }
  process.exit(results.every((r) => r.ok) ? 0 : 1);
};

export { FEATURES, VIEWPORTS, PAGE, ok, fail, settle };

const isMain = process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href;
if (isMain) main();
