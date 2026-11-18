---
name: arena
description: "对同一任务生成 N 个并行候选，选一个底座，把败者最强的部分嫁接进去。用于 /arena、「arena this」「扔进竞技场」，或当对非平凡产物只试一次就会锁死错误形状时。"
---

# Arena

在 Codex 上，先读[平台映射](../poteto-mode/references/codex-tools.md)（包括其中的逐技能说明），再执行本技能。

在 GitHub Copilot 上，先读[平台映射](../poteto-mode/references/copilot-tools.md)（包括其中的逐技能说明），再执行本技能。

在 Muse 上，先读[平台映射](../poteto-mode/references/muse-tools.md)（包括其中的逐技能说明），再执行本技能。

在 Antigravity 上，先读[平台映射](../poteto-mode/references/agy-tools.md)（包括其中的逐技能说明），再执行本技能。

启动任何东西之前，先开一个 todolist，每个阶段一条（Frame、Fan out、Cross-judge、Pick、Graft、Verify）。

## 阶段 A：Frame（定框）

每个候选拿到同样的提示词，所以提示词就是契约。

1. 陈述每个候选要产出的产物。
2. 推导 rubric：针对*这个*任务成功长什么样，3-6 条具体可评分的标准。它是阶段 D 里选底座者的工具。候选只看到任务。
3. 选 runner。用 `pstack-models.md` 里的 `arena runners` 行。表或那行缺失的话，各按 [Models](#models) 里的默认跑一个。该行里的 `auto` 或 `inherit-parent` 条目意味着父模型，所以省略 `model`。如果 `Agent` 工具拒绝某个配置条目，让那个席位跑它所在家族的默认，并说出来。家族按模型名划分，比如 Opus、Fable、Sonnet。如果家族没有默认，或 `Agent` 工具拒绝那个默认，用错误信息里同家族最接近的合法 slug，都没有就放弃该席位并说出来。放弃的席位让 runner 少于两个时，加 runner 直到有两个，或该行只有一条时加到一个。加的 runner 用剩余某个 runner 的模型，或没有剩余时省略 `model` 让它跑在父模型上，并说出来。竞技场覆盖多个设计方向时多派 runner。工作是生成密集而非判断敏感时，同一个模型用 N 次。按 **poteto-mode** 技能的 Subagents 小节，为工作选择每个子代理的推理强度。
4. 给每个候选自己的输出位置（可能的话用 git 工作树，否则用 `/tmp/arena-<slug>/candidate-<n>/`），遵循 **separate-before-serializing-shared-state** 原则技能。

## 阶段 B：Fan out（扇出）

在一条消息里用 `run_in_background: true` 生成全部 N 个子代理，每个带任务、共享 grounding 的路径、自己的输出路径，以及产出该产物和一段简短理由的指令，理由要说明它考虑过哪些备选、拒绝了什么。

某个候选没有产出的话，用 N-1 继续，并记下掉队。

## 阶段 C：Cross-judge（交叉评审）

阶段 B 全部候选完成后，从 `pstack-models.md` 的 `arena cross-judge pool` 行选一个模型。表或那行缺失的话，从 [Models](#models) 的 runner 默认里选。生成一个只读的评审子代理。评审者绝不能来自父模型的家族，家族的定义见阶段 A 第 3 步。只试另一个家族的条目，按池顺序。`auto` 或 `inherit-parent` 条目是父模型，所以永远不评审。`Agent` 工具拒绝某条目的话，用错误信息里同模型最接近层级或速度的合法 slug，没有就移到下一条目。另一个家族的条目都跑不起来，再用同样方式试默认池里另一家族的条目。都不行，跳过评审，阶段 D 单独选底座，并说出来。如果你不知道父模型，按池顺序试池里的真实 slug，并说明家族检查没有跑。评审者看到 rubric 和以路径标签标示的候选，对每条标准打分，并带理由推荐一个底座。它与你在阶段 D 的阅读并行运行。候选还在写的时候别派它。

## 阶段 D：Pick（选底座）

选之前把每个候选从头到尾读完。逐条标准打分，不凭整体感觉，阶段 C 跑了交叉评审的话和它对比。底座上的一致确认你的选择。分歧意味着你们中有人有偏，或 rubric 含糊。决定前把两份理由都读了。

选那个未来的维护者最容易在不破坏不变量的前提下扩展的底座。两个感觉打平时，按 Laziness Protocol 优先更干净的边界或更小的 API。

## 阶段 E：Graft（嫁接）

把每个败选候选再走一遍，找值得移植进底座的东西，通常每个候选一两件，不是大部分。每个嫁接都手工并入，遵循 **redesign-from-first-principles** 原则技能，让结果在同一个心智模型下保持连贯。不要机械粘贴。

候选收敛到同一个形状，那就是强共识。记下它并发布共识形状。不需要嫁接。严重发散的话，阶段 A 说明不足。重新定框重跑，而不是对发散取平均。

## 阶段 F：Verify（验证）

像对待任何其他输出一样验证合成的产物，遵循 **prove-it-works** 原则技能。验证发现竞技场漏掉的问题，要么阶段 A 错了（重定框重跑），要么某个候选抓到了而你漏了嫁接（回到阶段 E）。不要糊过去。

## 输出

一个合成产物，旁边附一段简短的合成说明：底座及原因、交叉评审的结论或阶段 C 跳过了评审、每个嫁接及其来源候选、拒绝了什么及为什么、有无收敛或掉队、验证结果。

## Models

角色默认值，从 `plugins/pstack/models.json` 戳出（在那儿改，重跑 `tools/generate.mjs`）。`pstack-models.md` 覆盖表里匹配的角色行在运行时覆盖每一项；`/setup-pstack` 写它并按宿主列出其路径。

- arena runners: `opus`, `fable`, `sonnet`, `haiku`
- arena cross-judge pool: `opus`, `fable`, `sonnet`, `haiku`

## Reasoning effort（推理强度）

覆盖表里的角色值可以在模型后面带推理强度，比如 `opus @xhigh`。Claude Code 上的等级：`low`、`medium`、`high`、`xhigh`、`max`。哪些可用取决于模型。不带 `@` 的值取表的 `default effort` 行——一个等级或 `session`；表没有该行时取 `session`。在 Claude Code 上，`session` 不设置强度。其他宿主上，`session` 按平台映射走。读模型前先剥掉后缀：`inherit-parent` 或 `auto` 在每个等级上仍然省略 `model`，模型名照常作为 `model` 传入。等级作为派发的 effort 字段传入，`subagent_type` 照常用你本来要用的。即 Claude Code 的 `Agent` 调用上是 `effort`，Codex 的 `spawn_agent` 上是 `reasoning_effort`。在 Muse 上是 Workflow 子代理上的 `effort`；`subagent_spawn` 派发保持会话的强度。
