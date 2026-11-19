---
name: interrogate
description: "用于「interrogate」「对抗性审查」「多模型评审」「challenge this」「压测这段代码」「找出盲点」「把这个拆解掉」。对抗方设法击穿一次变更或一个设计，只有被运行证实的问题才保留下来。"
---

# Interrogate

在 Codex 上，先阅读[平台映射](../poteto-mode/references/codex-tools.md)（包括其中的各技能说明），再执行本技能。

在 GitHub Copilot 上，先阅读[平台映射](../poteto-mode/references/copilot-tools.md)（包括其中的各技能说明），再执行本技能。

在 Muse 上，先阅读[平台映射](../poteto-mode/references/muse-tools.md)（包括其中的各技能说明），再执行本技能。

在 Antigravity 上，先阅读[平台映射](../poteto-mode/references/agy-tools.md)（包括其中的各技能说明），再执行本技能。

对抗方设法击穿一次变更或一个设计。一个问题只有被运行证实才算成立。只报告问题，不做修复。

## 定框

范围就是用户点名的对象；没点名，就是该分支与其基线分支的 merge base 到工作树之间的 diff。用 **in-your-own-words** 技能陈述意图，依据是用户消息、提交和 PR 描述。意图不明就问用户。

## 扇出

运行 **arena** 技能的 Phase A 第 3、4 步和 Phase B，变更数为四。把其中的 `arena runners` 换成读 `interrogate reviewers` 这一行。把范围内的未提交改动复制进每个工作树。每个对抗方都用 `general-purpose` 启动。不交给 arena 的任务和理由，而是给每个对抗方范围、意图和这段说明：

> 击穿这次变更。每个问题都要用一次针对真实代码的运行来证明，比如一个失败的测试、一个复现脚本，或一段显示错误行为的命令输出。对设计或方案，跑一个原型或在当前代码树上做探查。复现留在你自己的工作树里。每个问题都要给出标题、确切的命令、它打印的输出，以及意图所要求的输出。没跑过的不报。风格、命名、结构，以及要靠未来改动才能成立的风险都不算。零问题也是一个有效结果。

## 验证

按 arena Phase F 验证每个问题，重跑它的命令。输出显示失败、且失败确实破坏了意图的，保留；其余丢弃。共享同一根因的问题合并成一条。

跳过 arena 的 Phase C、D、E。各对抗方找到的失败各不相同，所以判定要保留所有经过验证的问题，而不是只留某一个对抗方的清单。

## 输出

- **意图**：复述。
- **问题**：每个已验证问题给出命令、输出、它如何破坏意图，以及哪些对抗方找到了它。一条都没剩下就说「没有已验证的问题」。
- **丢弃**：每个对抗方丢弃了几条、为什么。

## Models

各角色默认值，由 `plugins/pstack/models.json` 盖章生成（在彼处编辑，重跑 `tools/generate.mjs`）。`pstack-models.md` 覆盖表里匹配的角色行会在运行时覆盖各项；`/setup-pstack` 负责写入该表，并按运行时列出其路径。

- interrogate reviewers: `opus`, `fable`, `sonnet`, `haiku`

## Reasoning effort

覆盖表里的角色值可以在模型后面带上推理力度，如 `opus @xhigh`。Claude Code 上的档位：`low`、`medium`、`high`、`xhigh`、`max`。哪些档位可用取决于模型。不带 `@` 的值取表里的 `default effort` 行（一个档位或 `session`），表里没有该行时取 `session`。在 Claude Code 上，`session` 不设置力度。在其他运行时上，`session` 遵循平台映射。读取模型前先剥掉后缀：`inherit-parent` 或 `auto` 在每一层仍然省略 `model`，而模型名作为 `model` 传入。档位作为派发的 effort 字段传入，`subagent_type` 保持原样。Claude Code 的 `Agent` 调用上是 `effort`，Codex 的 `spawn_agent` 上是 `reasoning_effort`。在 Muse 上，它是 Workflow 子任务的 `effort`；`subagent_spawn` 派发保持会话的力度。
