### Refactoring

通过 [poteto-mode 的 Non-negotiables](../SKILL.md#non-negotiables) 解析 driver skill。

**契约归你。结构变，行为不变。** 与添加行为的 Feature、纠正行为的 Bug fix 相区别。

清理过程中发现缺失的功能或真 bug，就把它拆出去，先按钉住的契约发布结构性改动。允许重新设计，但要明说出来并路由到 Feature。大型或横切的结构工作属于 **figure-it-out** 技能；本 playbook 管聚焦到中等规模。

1. 先钉住行为契约。追溯受影响子系统以弄清契约，然后在任何结构移动之前，写一个特征测试、快照或等价性台架来捕获当前行为。该区域没有覆盖就先写钉子再动结构。类型检查和 lint 不是钉子。
2. 按 **principle-model-the-domain** 说出代码缺的那层结构。形状已经清楚且局部化时，无聊的代码就保留。重塑必须删掉分支或非法状态，而不是加间接层。
3. 说出目标形状。说明如果今天从零建，模块布局、类型、调用图应该是什么样（**principle-foundational-thinking**、**principle-redesign-from-first-principles**）。目标跨越函数边界时，移动之前先跑 **architect** 技能定形态。
4. 先减后加。引入新形状之前，先删死代码、折叠单调用方的包装、去掉冗余校验器、移除孤儿引用（**principle-subtract-before-you-add**）。到达目标形状的最小改动才发布（**principle-laziness-protocol**）。「也许有用」的投机清理要回滚。
5. 以小步行为保持的方式移动，每步钉子保持绿。API 重塑时，同一波迁移所有调用方并删除旧 API（**principle-migrate-callers-then-delete-legacy-apis**）。不留兼容垫片，不留新旧并行路径。每次重命名都对照实际文件抽查。重命名会静默漏掉字符串、散文、回引里的用法。机械编辑委托给子代理，使用你配置的 refactoring 模型（默认见 poteto-mode 的 Models 一节），并给一个具体范围（文件路径、被移动的名字、要保持的行为）。按 poteto-mode 的 Subagents 一节为每个子代理选合适的推理档位。
6. 在真实产物上证明行为不变，而不是「编译过了」（**principle-prove-it-works**）。较大的重塑跑一次等价性检查：diff 新旧输出的脚本、对着新代码回放录制好的基线、或通过相关 driver skill 在匹配界面上的一次冒烟。
7. 确认这个改动值得保留。成功度量是读者负担的降低（**principle-minimize-reader-load**）。diff 没有在某个地方降低读者负担，就回滚。
8. rebase 成少量有序提交：一个纯删减提交，然后是重塑，然后是后续清理。用 **sequence-verifiable-units** 原则技能塑形，让每个行为保持切片在下一步之前保持绿。走 **Opening a PR** 流程。

**汇报：** 变了什么结构、钉住它的钉子、等价性证明、读者负担的 delta、发布与回滚了什么。没有新行为。
