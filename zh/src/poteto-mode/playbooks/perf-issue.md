### Perf issue

**测量故事归你。计划、评审、验证数字。** 每个修复都要挂在一次测量上，不要拿读源码代替测量。

1. 通过匹配的 driver skill 抓基线 trace。用 **benchmark-checklist** 技能审查基线，以及之后的每一个数字。
2. 追溯代码以落地假设。没跑过就不要宣称性能上限。
   按顺序试这些性能箴言，最便宜的在前：
   1. 不做它。结果没人用的工作直接停掉，而不是把它变便宜。
   2. 做它，但不做第二次。
   3. 少做它。
   4. 晚点做它。
   5. 趁没人看时做它。
   6. 并发做它。
   7. 更便宜地做它。

   某条箴言已经达标，就停。
3. 从 trace 出发计划修复。跨越函数边界就先 `architect`。把实现委托给子代理，使用你配置的 perf-issue 模型（默认见 poteto-mode 的 Models 一节）。按 poteto-mode 的 Subagents 一节为每个子代理选合适的推理档位。评审 diff。抓修复后的 trace。
   套用 **sequence-verifiable-units** 原则技能，每次尝试先验证再试下一个。
4. 解析并对比产物（JSON 转 sqlite，diff）。「不确定」或用错界面都不算通过，要标出来。
5. 在 PR 里引用测量。
6. 走 **Opening a PR** 流程。

要的是对一个指标的持续改进而非一次性修复时，改用 Hillclimb playbook（`playbooks/hillclimb.md`）。

**汇报：** 基线数字、修复后数字、delta、产物路径。
