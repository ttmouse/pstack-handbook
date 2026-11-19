### Multi-phase or multi-PR plan

通过 [poteto-mode 的 Non-negotiables](../SKILL.md#non-negotiables) 解析 driver skill。

**计划归你，代码不归你。计划是一份 owner 逐框执行、操作者凭证据审计的 checklist。** 计划就是交付物。不要实施。

1. 改动只有一两个文件且做法显然时，跳过计划。说明并停止。
2. 写之前先用原型解决悬而未决的问题，按 `playbooks/prototype.md`。只有任何运行都无法裁决的产品或偏好取舍才问操作者。
3. 写计划文件。开头写清楚改什么、按落地顺序排列的 PR id、以及依赖图——哪些 PR 相互独立且从 trunk 分叉、哪些等谁、各自可触碰哪些文件。然后每个 PR 一节。一个 PR 就是一个自带证据的改动（**sequence-verifiable-units** 原则技能）。每节都有 checkbox：它依赖什么、它编辑哪些文件、它构建的那一个改动、你看到的结果、以及它的验证。
4. 只有测试不算充分的验证。一个 PR 只有 unit、live、perf 三个框全勾上才算验证过。每个 live 框都通过 driver skill 在真实界面上驱动，在自己的工作树里，配一个具体场景和一个通过谓词。perf 框写明指标、探针、先测好的 trunk 基线、以及判失败的数字。改变交互的 PR，合并前要等操作者评审。
5. 交回计划路径并停止。执行要等操作者明确放行才启动。

**汇报：** 计划路径、各 PR id 及其依赖关系、需要评审放行的集合、以及仍处于未证明状态的部分。
