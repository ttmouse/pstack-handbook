---
name: no-comments
description: "派出 comment-sicko 子代理，修复被接受的发现，并为声称的约束提供编码方案。"
---

# No comments

在 Codex 上，先读[平台映射](../poteto-mode/references/codex-tools.md)（包括其中的每技能注记），再执行本技能。

在 GitHub Copilot 上，先读[平台映射](../poteto-mode/references/copilot-tools.md)（包括其中的每技能注记），再执行本技能。

在 Muse 上，先读[平台映射](../poteto-mode/references/muse-tools.md)（包括其中的每技能注记），再执行本技能。

在 Antigravity 上，先读[平台映射](../poteto-mode/references/agy-tools.md)（包括其中的每技能注记），再执行本技能。

派出 comment-sicko。对被接受的发现采取行动。

尊重 comment-sicko 的新鲜视角。

## 范围

使用调用方给的文件或 diff。否则使用当前分支相对基线分支（默认 `main`）的 diff，包含工作树。

## 步骤

1. 用 `subagent_type: "pstack:comment-sicko"` 派出 `Agent`。传入范围。按 **poteto-mode** 技能的 Subagents 一节，为每项工作选合适的子代理推理强度。不要复述它的规则。

   将 `model` 设为 `pstack-models.md` 中 `no-comments reviewer` 一行的值；若该表或该行缺失，用 [Models](#models) 的默认值。值为 `auto` 或 `inherit-parent` 时，不设 `model`。若 `Agent` 工具拒绝某个 slug，用默认值并说明。若它拒绝默认值，用错误信息里同家族最接近的有效 slug。
2. 检查它的报告和 diff。拒绝这些情况：对应用代码的编辑、越出范围、受异常保护的删除、误述 `MUST KILL` 理由、以及把留下的有意代码当有罪的标记。针对「我们自己的代码里的意外」的标记仍然可执行。不要恢复那些注释。一个 keep 只有在证明了它针对我们无法改变的东西之后才成立。审计被漏掉的、作用域内的 lint 和 TypeScript 抑制注释。涉及正确性或安全性的抑制注释仍然是可执行的 `MUST KILL`。只有在有确切例外和范围内证据时才恢复删除。在接受理由单薄的 `IMPORTANT` 或 `do not remove` 的 kill 或 keep 之前，先对它们的符号跑 `/how` 或 `/why`。如果 kill 含糊，不要恢复。如果 keep 被推翻或仍然含糊，删掉它。对一份被拒绝的报告，回滚并点名失败原因重跑一次。第二次仍被拒绝，标记为 open，并让 `/no-comments` 因该报告中被拒绝的发现而失败，而不是让整轮运行失败。

   一条 `HOLD` 如果点出了依赖、平台、厂商或协议的某条规则，并说明去哪里核实，就不算含糊的 keep。把它留在原处，并标记为 open。其他任何 `HOLD` 都是含糊的 keep。不要接受对陈述这类规则的注释的 kill，除非报告引用了反驳该规则或显示该规则约束的是别的东西的文档页或源文件。把那条注释按 `HOLD` 恢复，即使按其他规则含糊的 kill 本应保持删除。第二次被拒绝之后，回滚其中被拒绝的发现，并带着你接受的全部发现完成步骤 3 到 6。
3. 对琐碎的被接受标记直接修复：删除死路径、去掉参数、或改用真正的 API。如果任何修复需要形状设计，对被接受集合及周边代码跑一次 `/architect`。止步于草图。形状由 Architect 定，实现由步骤 4 做。
4. 在范围内实现最小的根因修复。移除每一个被点名的变通代码。如果根因在范围外，落地范围内最小的修复，其余标记为 open。**principle-fix-root-causes** 和 **principle-redesign-from-first-principles** 技能只指导意图。两者都不授权扩大围栏，也不授权修复围栏之外的实例。绝不贴上症状守卫。
5. 约束注释写着 `do not remove`、`do not change wording`、或 `talk to X before changing`。保留关于我们无法改变之物的 keep。提供范围内最便宜的类型、运行时、测试或 CI lint 方案。等待交互式批准。无人值守和 eval 模式需要调用方预先批准。批准则先编码再删除。否则删除，把约束标记为 open，并草拟范围外的工作。
6. 汇报：删除数量、恢复的注释、`HOLD` 注释、重跑情况、architect 草图、修复、编码提议、已落地的编码、未强制执行的约束、以及其他 open 工作。

## Models

角色默认值，盖戳自 `plugins/pstack/models.json`（要改就在那里改，然后重跑 `tools/generate.mjs`）。`pstack-models.md` 覆盖表中匹配的角色行会在运行时覆盖这里的默认值；`/setup-pstack` 负责写入，并按运行时列出其路径。

- no-comments reviewer: `opus`

## Reasoning effort

覆盖表中的角色值可以在模型后面带上推理强度，如 `opus @xhigh`。Claude Code 上的档位：`low`、`medium`、`high`、`xhigh`、`max`。哪些档位可用取决于模型。不带 `@` 的值取该表的 `default effort` 行（一个档位或 `session`），表里没有该行时取 `session`。在 Claude Code 上，`session` 不设置强度。在其他运行时上，`session` 按平台映射处理。读取模型前先剥掉后缀：`inherit-parent` 或 `auto` 在每一层都不传 `model`，模型名则作为 `model` 传入。把档位作为派发的 effort 字段传入，`subagent_type` 保持原样。在 Claude Code 的 `Agent` 调用上是 `effort`，在 Codex 的 `spawn_agent` 上是 `reasoning_effort`。在 Muse 上是 Workflow 子任务的 `effort`；`subagent_spawn` 派发保持会话的强度。
