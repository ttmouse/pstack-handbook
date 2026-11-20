---
name: verify
description: 用真实浏览器驱动 pstack 手册，验证改动有没有坏。改完页面、合并前、或要复现一条报障时用。命令是 node .claude/skills/verify/scripts/verify.mjs，退出码 0 通过，1 失败，2 用法错误。
---

# verify

这份手册是单文件静态页，没有测试框架。这里用 Playwright 真开 Chrome，把每个功能按用户会走的路径驱动一遍，量出来再判。

## 跑

```bash
node .claude/skills/verify/scripts/verify.mjs              # 全部
node .claude/skills/verify/scripts/verify.mjs --feature contrast
node .claude/skills/verify/scripts/verify.mjs --json       # 给脚本用
node .claude/skills/verify/scripts/verify.mjs --out .audit/verify   # 每项留一张截图
```

退出码就是结论。0 通过，1 有失败，2 参数错。别读文字判断，读退出码。

## 判据

每项检查写在 `scripts/verify.mjs` 的 `FEATURES` 表里，一条一项。每条给四样：怎么到达、在哪个视口、做什么动作、什么算过。失败时 detail 要写清差多少，不是写「失败」。

现在的覆盖面在 `feature-map.md`，功能名和检查项 ID 一一对应。

## 加一项

用户能看到的行为，就配一条检查。顺序是：先写检查，看它失败，再改页面。没失败的检查先别急着写，先想它是真能坏还是只换个说法描述现状。

阈值要写成数字。版面类写像素，可读性写对比度比值，交互类写状态变化。

## 边界

它验的是页面自己的行为。构建产物对不对由 `tools/build.py` 管，那套检查（断链、外链、标签配对）别在这里重复。

改完页面跑一次，跟上次比。有一条从 PASS 变 FAIL，就是这一改弄坏的。
