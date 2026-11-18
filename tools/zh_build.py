#!/usr/bin/env python3
"""Assemble the translated pstack documents (zh/src/**) into one self-contained
HTML page that reuses the handbook's CSS and page script.

Group order: 总管 (poteto-mode) → playbook (23, numbered by the same pinned
mapping as the handbook) → 技能 (43) → 原则 (24). Playbook sections reuse the
handbook's #pb-NN anchors so citations match the published handbook.
"""

import html as html_mod
import os
import re
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "zh" / "src"
OUT = ROOT / "zh" / "index.html"
HANDBOOK = ROOT / "index.html"

# filename stem -> pinned playbook number, mirroring PLAYBOOK_NUMBERS in build.py
PLAYBOOK_NUMBERS = {
    "investigation": 1, "bug-fix": 2, "perf-issue": 3, "hillclimb": 4,
    "runtime-forensics": 5, "trace-forensics": 6, "feature": 7,
    "refactoring": 8, "prototype": 9, "visual-parity": 10,
    "authoring-a-skill": 11, "eval": 12, "babysit": 13, "shipping": 14,
    "opening-a-pr": 15, "autonomous-run": 16, "orchestrate": 17,
    "autopilot-full": 18, "autopilot-stack": 19, "session-pickup": 20,
    "pause-safely": 21, "multi-phase-plan": 22, "worktree-cleanup": 23,
}

GROUPS = [
    ("总管", lambda p: p.name == "SKILL.md" and p.parent.name == "poteto-mode"),
    ("playbook（流程清单）", lambda p: p.parent.name == "playbooks"),
    ("技能", lambda p: p.name == "SKILL.md" and not p.parent.name.startswith("principle-")
        and p.parent.name != "poteto-mode"),
    ("原则", lambda p: p.name == "SKILL.md" and p.parent.name.startswith("principle-")),
]


def split_frontmatter(text):
    if text.startswith("---"):
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
        if m:
            return m.group(1), m.group(2)
    return "", text


def front_value(fm, key):
    m = re.search(rf"^{key}:\s*(.+?)$", fm, re.M)
    return m.group(1).strip().strip("\"'") if m else ""


def wrap_tables(fragment):
    """Wrap tables in .tw and stamp td data-labels from the header row, the
    same convention the handbook build uses for mobile stacking."""
    def fix_table(m):
        table = m.group(0)
        heads = re.findall(r"<th[^>]*>(.*?)</th>", table, re.S)
        plain = [re.sub(r"<[^>]+>", "", h).strip() for h in heads]
        # stamp data-label per td using its column index
        def stamp_row(row):
            body = row.group(1)
            counter = [-1]
            def repl(td):
                counter[0] += 1
                i = counter[0]
                label = plain[i] if i < len(plain) else ""
                open_tag, rest = td.group(1), td.group(2)
                if label and "data-label" not in open_tag:
                    open_tag = open_tag[:-1] + f' data-label="{html_mod.escape(label)}">'
                return open_tag + rest + "</td>"
            body = re.sub(r"(<td[^>]*>)(.*?)</td>", repl, body, flags=re.S)
            return "<tr>" + body + "</tr>"
        table = re.sub(r"<tr>(.*?)</tr>", stamp_row, table, flags=re.S)
        return '<div class="tw">' + table + "</div>"
    return re.sub(r"<table>.*?</table>", fix_table, fragment, flags=re.S)


def rewrite_links(frag, base_dir, slugmap):
    """Point markdown-relative links at in-page anchors; drop hrefs whose
    target is not part of this page."""
    def fix_href(m):
        href = m.group(1)
        target = os.path.normpath(os.path.join(base_dir, href))
        if target in slugmap:
            return f'href="#{slugmap[target]}"'
        return 'href="javascript:void(0)" style="text-decoration:none;color:inherit"'
    return re.sub(r'href="([^"]+)"', fix_href, frag)


def md_to_fragment(md_text, where=""):
    fm, body = split_frontmatter(md_text)
    frag = markdown.markdown(body, extensions=["tables", "fenced_code"])
    # prose like "principle-<title>" leaks raw tags past markdown; title/textarea/
    # style are RCDATA in the HTML parser and would swallow the rest of the page
    frag = re.sub(r"<(title|textarea|style)(?=[\s>/])", r"&lt;\1", frag, flags=re.I)
    frag = wrap_tables(frag)
    for tag in ("div", "table", "tr", "td", "th", "pre", "blockquote"):
        opens = len(re.findall(rf"<{tag}[ >]", frag))
        closes = frag.count(f"</{tag}>")
        if opens != closes:
            print(f"WARN unbalanced <{tag}> in {where}: {opens} open / {closes} close")
    return fm, frag


def collect_docs():
    docs = []  # (group, num_or_None, slug, title, md_path)
    all_md = sorted(SRC.rglob("*.md"))
    if not all_md:
        sys.exit("zh/src is empty — translations missing?")
    for group, pred in GROUPS:
        for p in all_md:
            rel = p.relative_to(SRC)
            if not pred(p):
                continue
            if p.parent.name == "playbooks":
                stem = p.stem
                num = PLAYBOOK_NUMBERS.get(stem)
                if num is None:
                    sys.exit(f"playbook {stem} has no pinned number — add it to PLAYBOOK_NUMBERS")
                docs.append((group, f"{num:02d}", f"pb-{num:02d}", stem, p))
            elif group == "总管":
                docs.append((group, "", "poteto-mode", "poteto-mode", p))
            elif group == "技能":
                docs.append((group, "", "sk-" + p.parent.name, p.parent.name, p))
            else:
                docs.append((group, "", p.parent.name, p.parent.name, p))
    # playbooks in pinned-number order, groups kept in collection order
    group_order = {g: i for i, (g, _) in enumerate(GROUPS)}
    docs.sort(key=lambda d: (group_order[d[0]], int(d[1]) if d[1] else 0))
    return docs


def build():
    page = HANDBOOK.read_text()
    style = re.search(r"<style>.*?</style>", page, re.S).group(0)
    style += """
<style>
/* zh-only: the rail holds 90 long English names, not 22 chapter labels */
:root{--rail:232px}
.rail-group{margin:14px 0 4px;padding:0 8px 0 0;font-size:12px;font-weight:600;
  letter-spacing:.06em;color:var(--muted);list-style:none}
.rail-group:first-child{margin-top:0}
.rail-list a{grid-template-columns:2.1em minmax(0,1fr);font-size:13px;padding:5px 8px 5px 0}
.rail-list .n:empty{visibility:hidden}
.rail-list a .t{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.rail-results .r-t{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
</style>"""
    boot = re.search(r'<script>document\.documentElement[^<]*</script>', page).group(0)
    script = re.search(r"<script>\n\(function\(\)\{.*?</script>", page, re.S).group(0)

    docs = collect_docs()
    counts = {}
    for g, *_ in docs:
        counts[g] = counts.get(g, 0) + 1

    rail_groups = "".join(
        f'<li class="rail-group">{html_mod.escape(g)} · {counts.get(g, 0)}</li>'
        for g, _ in GROUPS)

    slugmap = {os.path.normpath(str(p.relative_to(SRC))): slug
               for _, _, slug, _, p in docs}

    rail_items, sections = [], []
    last_group = None
    for group, num, slug, title, path in docs:
        if group != last_group:
            rail_items.append(f'<li class="rail-group">{html_mod.escape(group)} · {counts[group]}</li>')
            last_group = group
        n_span = f'<span class="n">{num}</span>' if num else '<span class="n"></span>'
        rail_items.append(f'<li><a href="#{slug}" title="{html_mod.escape(title, quote=True)}">'
                          f'{n_span}<span class="t">{html_mod.escape(title)}</span></a></li>')
        fm, frag = md_to_fragment(path.read_text(), where=title)
        frag = rewrite_links(frag, str(path.parent.relative_to(SRC)), slugmap)
        desc = front_value(fm, "description")
        desc_block = ""
        if desc:
            desc_block = (f'<div class="note"><b>description（路由依据，译文）。</b>'
                          f'{html_mod.escape(desc)}</div>')
        num_span = f'<span class="num">{num}</span>' if num else ""
        sections.append(
            f'<h2 id="{slug}">{num_span}<span class="ttl">{html_mod.escape(title)}</span></h2>\n'
            f"{desc_block}\n{frag}")

    total = len(docs)
    missing = [d for d in docs if not d[4].read_text().strip()]
    if missing:
        sys.exit(f"empty translations: {[str(d[4]) for d in missing]}")

    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#f6f5f2" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0c0d0f" media="(prefers-color-scheme: dark)">
<meta name="description" content="pstack 0.9.129 全部 playbook、技能与原则的纯中文全译，逐句对应用于学习。">
<title>pstack 原文全译</title>
{boot}
{style}
</head>
<body>
<input type="checkbox" id="tocToggle" class="toc-toggle">
<div class="shell">
<nav class="rail" aria-label="文档目录">
  <label class="rail-head" for="tocToggle">
    <span class="wordmark">pstack 原文全译</span>
    <span class="chev" aria-hidden="true"></span>
  </label>
  <div class="rail-search">
    <input id="search" placeholder="搜索全文" autocomplete="off">
    <ol class="rail-results" hidden></ol>
    <p class="rail-none" hidden>没有匹配</p>
  </div>
  <ol class="rail-list">
    {"".join(rail_items)}
  </ol>
</nav>
<main>

<header class="cover">
  <h1><span class="ln">pstack</span><span class="ln">原文全译</span></h1>
  <p class="lede">本机安装的 pstack 0.9.129 里全部 playbook、技能与原则的纯中文全译，逐句对应原文，供逐条学习。技能名、命令、路径、代码保留英文。</p>
  <div class="cover-foot">
    <a class="go" href="#readme">从翻译说明开始</a>
    <div class="stats">
      <div class="stat"><b>{total}</b><span>份文档</span></div>
      <div class="stat"><b>{counts.get("playbook（流程清单）", 0)}</b><span>本 playbook</span></div>
      <div class="stat"><b>{counts.get("技能", 0)}</b><span>个技能</span></div>
      <div class="stat"><b>{counts.get("原则", 0)}</b><span>条原则</span></div>
    </div>
  </div>
</header>

<h2 id="readme"><span class="num">0</span><span class="ttl">翻译说明</span></h2>
<p>来源：本机 <code>~/.claude/plugins/cache/pstack-claude/pstack/0.9.129/skills/</code>，逐文件全译，不摘要、不省略。术语约定：skill 译「技能」，principle 译「原则」，playbook、技能名、斜杠命令、文件路径、frontmatter、description、driver、verifier、watcher 保留英文，因为它们是你要原样敲进终端或核对文件时用到的字面量。每份文档开头的蓝框是它 frontmatter 里的 description 译文——那行字是路由的唯一依据，值得逐条读。翻译日期 2026-11-18，上游技能文本会随版本演进，数字以本机版本为准。</p>
{"".join(sections)}
</main>
</div>
<script>
{script.split("<script>", 1)[1]}
</body>
</html>
"""
    OUT.write_text(doc)
    print(f"docs     {total}")
    print(f"counts   {counts}")
    print(f"output   {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build()
