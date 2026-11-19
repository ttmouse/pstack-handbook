---
name: arena
description: "对同一任务并行生成 N 个候选，选出一个基底，再把落选者最强的部分嫁接进去。用于 /arena、'arena this'、'throw it in the arena'，或任何一次尝试就可能锁死错误形状的非平凡产物。"
---

# Arena

在 Codex 上，遵循本技能前先读[平台映射](../poteto-mode/references/codex-tools.md)，包括其中按技能给出的说明。

在 GitHub Copilot 上，遵循本技能前先读[平台映射](../poteto-mode/references/copilot-tools.md)，包括其中按技能给出的说明。

在 Muse 上，遵循本技能前先读[平台映射](../poteto-mode/references/muse-tools.md)，包括其中按技能给出的说明。

在 Antigravity 上，遵循本技能前先读[平台映射](../poteto-mode/references/agy-tools.md)，包括其中按技能给出的说明。

在启动任何东西之前，先开一个 todolist，每个阶段一条（Frame、Fan out、Cross-judge、Pick、Graft、Verify）。

## Phase A: Frame

每个候选拿到的 prompt 完全相同，所以 prompt 就是契约。

1. 说明每个候选要产出什么产物。
2. 推导评分标准：3-6 条具体的、可打分的标准，描述*这个*任务上的成功长什么样。它是 Phase D 里选择者的工具。候选只看得到任务本身。
3. 从 `pstack-models.md` 的 `arena runners` 一行挑选 runner，没有这一行时按 [Models](#models) 选。`auto` 或 `inherit-parent` 条目就是父模型，此时省略 `model` 并生成 `general-purpose`。如果 `Agent` 工具拒绝了某个 slug，就用同家族最近的合法 slug，或者直接放弃该席位，但至少保留两个 runner，并说明这一点。家族按模型名划分，如 Opus、Fable、Sonnet。要有多个设计方向就多派几个；当产出受生成能力制约、对判断不敏感时，可以重复使用同一个模型。每个子代理的推理强度按 **poteto-mode** 技能的 Subagents 一节来定。
4. 给每个候选分配独立的输出位置（尽量用 git 工作树，否则用 `/tmp/arena-<slug>/candidate-<n>/`），依据 **separate-before-serializing-shared-state** 原则技能。

## Phase B: Fan out

在一条消息里以 `run_in_background: true` 生成全部 N 个子代理，每个都带上任务、共享背景材料的路径、自己的输出路径，以及产出要求：产物 + 一段简短理由，说明考虑过哪些备选、拒绝了什么。

如果某个候选没有产出，就按 N-1 继续，并记下这次掉队。

## Phase C: Cross-judge

Phase B 的候选全部完成后，从 `pstack-models.md` 的 `arena cross-judge pool` 一行生成一个只读裁判，没有这一行时按 [Models](#models) 选。裁判绝不能来自父模型的家族——家族的划分见 Phase A 第 3 步——所以用另一个家族的第一个条目。`auto` 或 `inherit-parent` 条目就是父模型。如果不知道父模型是什么，就用第一个真实 slug，并说明家族检查没有执行。如果 `Agent` 工具拒绝了某个 slug，就用同家族最近的合法 slug，不行再换下一个条目，实在不行就跳过裁判，并说明这一点。在你于 Phase D 阅读的同时，裁判按路径标签给每个候选逐条对照评分标准打分，并推荐一个基底。

## Phase D: Pick a base

选定之前把每个候选从头到尾读完。逐条对照评分标准打分，不靠整体感觉，并且与 Phase C 的裁判结果对照。对基底判断一致，就确认选择。不一致说明你们中有一个有偏差，或评分标准写得含糊。决定前把两份理由都读一遍。

选那个未来维护者最容易在不破坏不变量的前提下扩展的基底。两个感觉打平时，选边界更干净或 API 更小的那个，依据 Laziness Protocol。

## Phase E: Graft

把每个落选候选再过一遍，找值得移植进基底的东西——通常每个候选一到两处，不是大部分。每个嫁接都手工融入，依据 **redesign-from-first-principles** 原则技能，让结果在同一个心智模型下保持连贯。不要机械粘贴。

如果候选们收敛到同一个形状，这是强烈的一致信号。记下它，直接交付共识形状，不需要嫁接。如果严重发散，说明 Phase A 的界定不够充分。重新框定再跑一轮，而不是对发散取平均。

## Phase F: Verify

像对待任何其他产出一样验证合成产物，依据 **prove-it-works** 原则技能。如果验证发现了 arena 漏掉的问题，要么是 Phase A 错了（重新框定再跑），要么是某个候选发现了它而你漏掉了嫁接（回到 Phase E）。不要掩盖。

## Outputs

一份合成产物，附带一段简短的合成说明：基底是什么、为什么选它、裁判的结论或 Phase C 跳过了裁判、每个嫁接来自哪个候选、拒绝了什么及原因、收敛或掉队情况，以及验证结果。

## Models

各角色默认值，从 `plugins/pstack/models.json` 盖章生成（在那儿改，重跑 `tools/generate.mjs`）。运行时若 `pstack-models.md` 覆盖表里有对应的角色行，则以该行为准；`/setup-pstack` 负责写出这张表，并按运行时列出其路径。

- arena runners: `opus`, `fable`, `sonnet`, `haiku`
- arena cross-judge pool: `opus`, `fable`, `sonnet`, `haiku`

## Reasoning effort

覆盖表里的角色值可以在模型后面带推理强度，如 `opus @xhigh`。Claude Code 上的级别有：`low`, `medium`, `high`, `xhigh`, `max`。哪些可用取决于模型。不带 `@` 的值取覆盖表的 `default effort` 行（一个级别或 `session`），覆盖表没有该行时取 `session`。在 Claude Code 上，`session` 不设置任何强度。在其他运行时上，`session` 按平台映射处理。读模型之前先剥掉后缀：`inherit-parent` 或 `auto` 在所有级别下仍然省略 `model`，模型名照常作为 `model` 传入。把级别放进派发的 effort 字段，`subagent_type` 保持你本来要用的那个。Claude Code 的 `Agent` 调用上是 `effort`，Codex 的 `spawn_agent` 上是 `reasoning_effort`。在 Muse 上是 Workflow 子任务的 `effort`；`subagent_spawn` 派发保持会话的强度。
