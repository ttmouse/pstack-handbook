---
name: architect
description: "写代码之前先勾画类型、签名和模块结构，然后留在循环里让实现填充。用于 /architect、「architect this」、「design this」，或任何直接跳进代码会锁死错误形状的非平凡工作。"
---

# Architect

在 Codex 上，遵循本技能之前先读[平台映射](../poteto-mode/references/codex-tools.md)，包括其按技能的说明。

在 GitHub Copilot 上，遵循本技能之前先读[平台映射](../poteto-mode/references/copilot-tools.md)，包括其按技能的说明。

在 Muse 上，遵循本技能之前先读[平台映射](../poteto-mode/references/muse-tools.md)，包括其按技能的说明。

在 Antigravity 上，遵循本技能之前先读[平台映射](../poteto-mode/references/agy-tools.md)，包括其按技能的说明。

先勾画类型、函数签名、类形状和模块边界，函数体写 `not implemented`，配以伪代码。跨多个模型视角综合，然后对照选定的草图填代码。

## 启动

开始之前打开一个 todolist，每个阶段一条。

1. Ground
2. Sketch
3. Agree
4. Implement
5. Scrap

## 阶段 A：夯实问题

对新代码触及的每个系统建立真实的心理模型。对相关子系统运行 **how** 技能。点名一个文件不等于夯实。产出 `how` 所规定的架构解释。如果设计重新定义所有权或分层，也对现有形态运行 **why** 技能，让缘由变成约束，而不是猜测。

只有当工作真的是没有任何周边系统要集成的全新绿地时，才跳过阶段 A。

## 阶段 B：Sketch

用 design-sketch 任务和阶段 A 的夯实产物运行 **arena** 技能。把 `references/runner-prompt.md` 作为每个 runner 的提示词。

runner 从 `pstack-models.md` 的 `architect runners` 行取，替代 `arena runners` 行。表或该行缺失时，用 [Models](#models) 的默认值。别名和被拒绝条目遵循 **arena** 技能阶段 A 的 runner 规则。

做两次设计。综合之前要求至少两个结构上不同的候选，即使第一个看起来已经够用。这是 **exhaust-the-design-space** 原则技能的具体化。是整个形状的备选，不是一个形状内部的点状修补。

综合之前，用 [`references/design-red-flags.md`](references/design-red-flags.md) 筛查每个候选。假定下一个贡献者是一个只看它打开过的文件、复制最近的示例、取能编译的最短路径的代理。优先这样的设计：从某一个文件看合理的改动，对整个仓库也合理。

在接口深度上比较可行候选。优先用更小、更简单的公共表面隐藏更多复杂度的设计。一个丰富的接口可以通过集中能力来保持调用链短，而不是把能力散落到各层。

Arena 返回一个综合后的设计包。它的综合决定填进 rationale 的「Synthesis decision」一节。

## 阶段 C：Agree（可选）

默认：用综合后的设计直接进入实现。没有人工检查点。

当调用方明确要求时选择检查点：「/architect with checkpoint」、「stop and show me before implementing」或类似说法。然后呈现综合设计，暂停等待签字。

无论哪种方式，综合都可以作为独立提交交付，即 **foundational-thinking** 原则技能的「scaffold first」模式。填充期间计划内、范围内的破坏是可以的，依据 **outcome-oriented-execution** 原则技能。要在实现之前对设计做对抗性施压，就对综合后的草图运行 **interrogate** 技能。

如果人类对形状提出异议（在检查点或事后），把它当作阶段 A 的证据。在写更多代码之前重新夯实并重跑阶段 B。

## 阶段 D：对照草图实现

把 `not implemented` 函数体换成代码，伪代码换成逻辑。综合后的草图就是契约。对它的偏离是要浮出的信号，不是要静默吸收的摩擦。如果某个函数需要一个草图没预料到的参数，追问：是草图错了，是需求漏了，还是实现越界了。

在每个实现单元收尾或把它的契约交给下一个 worker 之前，把已接受的偏离与保存的行为契约、接口和职责分配比对。一旦合适的所有者或评审流程接受了一个变更，更新现有草图和 rationale 中受影响的部分，并在那里记录接受来源。从抛出错误改为返回拒绝的变更，必须在下一个单元开始之前更新结果契约。

对不影响共享契约的局部偏离，记录决策和设计为何仍然成立；局部变量改名不需要重写架构。保持未接受的变更和未解决的分歧可见。当下一个 worker 会收到矛盾指令时，不要宣称该单元已对齐；也不要仅仅为了给已实现的东西辩护而编辑规格。使用既有设计产物，而不是每个单元一份平行记录。重复的结构性偏离仍然触发阶段 E。

## 阶段 E：架构错误时推倒

如果实现不断产生草图吸收不了的摩擦，扔掉草图。不要往错误的设计上打补丁，依据 **redesign-from-first-principles** 和 **fix-root-causes** 原则技能。

信号是一个*模式*，不是单例。特征：

- 同一种形状的 workaround 在无关代码中反复出现。
- 多个不相关的边界情况都需要特例分支。
- 类型需要逃生舱口（`any`、转型、实际上总是被设置的可选字段）才能编译。
- 「我们需要一把锁」的条件反射，而草图说过状态不是共享的。
- 调用方必须知道抽象的内部规则才能使用它。
- 实现中出现两个以上同形状的独立阶段 D 偏离。

用判断。几个边界情况不足以判一个架构死刑。有些问题本身确实复杂。数据中的复杂度不是设计中的复杂度。

推倒时：

1. 对已建成的部分重跑 **how** 技能。
2. 重新设计，就像新约束从第一天就在，依据 redesign-from-first-principles。
3. 先做减法再加东西，依据 **subtract-before-you-add** 原则技能。新草图在长大之前应当比旧草图更小。
4. 回到阶段 B 重跑 arena。

## 产出

先写调用方的用法，类型草图从它推导。小改动用一个含新类型和签名的文件。更大的工作是模块地图加类型定义。rationale 随附，按 `references/rationale-template.md` 成形，包括用法草图和综合决定。

## Models

角色默认值，盖自 `plugins/pstack/models.json`（在那儿改，重跑 `tools/generate.mjs`）。`pstack-models.md` 覆盖表中匹配的角色行在运行时覆盖这些值；`/setup-pstack` 写它，并按运行时列出路径。

- architect runners: `opus`, `fable`, `sonnet`, `haiku`

## Reasoning effort

覆盖表中的角色值可以在模型后面带推理等级，如 `opus @xhigh`。Claude Code 上的等级：`low`、`medium`、`high`、`xhigh`、`max`。哪些可用取决于模型。不带 `@` 的值取表的 `default effort` 行——一个等级或 `session`；表里没有该行时取 `session`。在 Claude Code 上，`session` 不设置等级。其他运行时，`session` 按平台映射处理。读模型之前先去掉后缀：`inherit-parent` 或 `auto` 在任何层级都不传 `model`，模型名则作为 `model` 传入。把等级作为派遣的 effort 字段传入，`subagent_type` 保持原样。即 Claude Code 的 `Agent` 调用上是 `effort`，Codex 的 `spawn_agent` 上是 `reasoning_effort`。在 Muse 上，它是 Workflow 子任务的 `effort`；`subagent_spawn` 派遣保持会话的等级。
