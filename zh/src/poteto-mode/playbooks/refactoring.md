### 重构

通过 [poteto-mode 的 Non-negotiables](../SKILL.md#non-negotiables) 解析 driver 技能。

**你拥有的是契约。结构在变，行为不变。** 与增加行为的 Feature、修正行为的 Bug fix 都不同。

如果清理过程中暴露出缺失的功能或真实的 bug，把它拆出去，先针对钉住的契约交付结构性改动。允许重新设计，但要指明并转回 Feature。大型或横切的结构工作属于 **figure-it-out** 技能。这个 playbook（流程清单）处理的是聚焦到中等规模的改动。

1. 先钉住行为契约。对受影响的子系统运行 **how** 技能来了解契约，然后写一个捕获当前行为的特征测试、快照或等价性工具，在任何结构移动之前完成。该区域没有覆盖就先写钉子再动结构。类型检查和 lint 不是钉子。
2. 按 **principle-model-the-domain** 指名代码缺失的结构。形状已经清晰且局部化的代码保持朴素。重塑必须删除分支或非法状态，而不是增加间接层。
3. 指名目标形状。说明如果今天重建，模块布局、类型和调用图应该是什么样（**principle-foundational-thinking**、**principle-redesign-from-first-principles**）。目标跨越函数边界时，先跑 **architect** 技能对形状做并行设计探索，再动手。
4. 先做减法再做加法。在引入新形状之前，删除死代码、合并单调用者的包装、去掉冗余校验器、清除孤儿引用（**principle-subtract-before-you-add**）。能到达目标形状的最小改动才交付（**principle-laziness-protocol**）。「可能有帮助」的投机性清理一律回退。
5. 以小的保持行为的步骤移动，每一步都让钉子保持绿色。API 重塑时，在同一波里迁移所有调用者并删除旧 API（**principle-migrate-callers-then-delete-legacy-apis**）。不做兼容垫片，不留新旧并行路径。每次重命名都对照真实文件抽查。重命名会悄悄漏掉字符串、行文和回引里的用法。把机械性编辑委派给一个子代理，使用你配置的 refactoring 模型（默认见 poteto-mode 的 Models 一节），并给出具体范围（文件路径、被移动的名字、要保住的行为）。按 Subagents 一节，为这份工作选子代理的推理等级。
6. 在真实产物上证明行为未变，而不是「编译过了」（**principle-prove-it-works**）。较大的重塑要跑一次等价性检查：一个 diff 新旧输出的脚本、一份对着新代码回放的已录制基线，或通过相关 driver 技能在匹配面上跑一次冒烟。
7. 确认这次改动值得保留。成功度量是降低读者负担（**principle-minimize-reader-load**）。如果 diff 没有在某处降低读者负担，回退它。
8. rebase 成小的有序提交。一条减法提交，然后是重塑，然后是任何后续清理。用 **sequence-verifiable-units** 原则技能整形，让每个保持行为的切片在下一切片之前保持绿色。执行 **Opening a PR**。

**汇报：** 变了的结构、你把它对照的钉子、等价性证明、读者负担的变化、交付了什么回退了什么。没有新行为。
