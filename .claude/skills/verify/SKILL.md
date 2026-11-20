---
name: verify
description: 用真实浏览器驱动 pstack 手册，验证改动有没有坏。改完页面、合并前、或要复现一条报障时用。入口命令是 tools/check.sh（diagrams → build → verify 一条命令），退出码 0 通过，1 失败，2 用法错误。
---

# verify

这份手册是单文件静态页，没有测试框架。这里用 Playwright 真开 Chrome，把每个功能按用户会走的路径驱动一遍，量出来再判。

## 跑

```bash
tools/check.sh                                             # diagrams → build → verify 一条命令，退出码即结论
node .claude/skills/verify/scripts/verify.mjs              # 只跑浏览器验证（18 项 + extra，约 25s）
node .claude/skills/verify/scripts/verify.mjs --feature contrast
node .claude/skills/verify/scripts/verify.mjs --json       # 给脚本用（带通道与耗时）
node .claude/skills/verify/scripts/verify.mjs --out .audit/verify   # 每项留一张截图
node .claude/skills/verify/scripts/verify.mjs --channel launch      # 不依赖常驻 Chrome，用自带 chromium 无头新开
node .claude/skills/verify/scripts/verify.mjs --extra                # 加跑 extra 项（打印版式）
```

退出码就是结论。0 通过，1 有失败，2 参数错。别读文字判断，读退出码。

通道是实测定的（2026-11-20，记录在 `.audit/probe/`）：主通道 `cdp` 连本机常驻 headless Chrome（`http://127.0.0.1:9333`，可用 `VERIFY_CDP` 换端口），不在线会自动拉起（`--headless=new --user-data-dir=/tmp/cdp-d`）。选它是因为保真度——自带 chromium 的无头壳动画时序和真 Chrome 不一致，`reveal` 在那条通道 3/3 稳定误报，真 Chrome 3/3 通过。`--channel launch`（自带 chromium，快约 5s）留给本机没有 Chrome 或常驻实例起不来的场合。两条通道都是无头，有人在前台干活也不抢屏；远程会话用 headed `channel:'chrome'` 会无限卡死，别再用。

依赖只有 python3 和 playwright。playwright 按 Node 的向上解析找，仓库住在 `~/projects` 下时直接命中 `~/node_modules`；clone 到别处跑 verify 报 `Cannot find playwright`，就在那个 clone 里 `npm i playwright`（diagrams/build 不受影响，干净 clone 重建产物字节一致）。

门槛待拍板：`print-layout` 现在是 extra（`--extra` 或 `--feature print-layout` 才跑），要不要进默认必过套件等拍板；拍进就删掉 verify.mjs 里它的 `extra: true` 一行。

## 判据

每项检查写在 `scripts/verify.mjs` 的 `FEATURES` 表里，一条一项。每条给四样：怎么到达、在哪个视口、做什么动作、什么算过。失败时 detail 要写清差多少，不是写「失败」。

现在的覆盖面在 `feature-map.md`，功能名和检查项 ID 一一对应。

## 加一项

用户能看到的行为，就配一条检查。顺序是：先写检查，看它失败，再改页面。没失败的检查先别急着写，先想它是真能坏还是只换个说法描述现状。

阈值要写成数字。版面类写像素，可读性写对比度比值，交互类写状态变化。

## 边界

它验的是页面自己的行为。构建产物对不对由 `tools/build.py` 管，那套检查（断链、外链、标签配对）别在这里重复。

改完页面跑一次，跟上次比。有一条从 PASS 变 FAIL，就是这一改弄坏的。
