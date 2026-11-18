---
name: interrogate
description: "用于 'interrogate'、'adversarial review'、'multi-model review'、'challenge this'、'stress test this code'、'find blind spots' 或 'tear this apart'。对手尝试破坏一个改动或设计，只有被运行证明的发现才能留下。"
---

# Interrogate

在 Codex 上，先读[平台映射](../poteto-mode/references/codex-tools.md)（包括其中的每技能注记），再执行本技能。

在 GitHub Copilot 上，先读[平台映射](../poteto-mode/references/copilot-tools.md)（包括其中的每技能注记），再执行本技能。

在 Muse 上，先读[平台映射](../poteto-mode/references/muse-tools.md)（包括其中的每技能注记），再执行本技能。

在 Antigravity 上，先读[平台映射](../poteto-mode/references/agy-tools.md)（包括其中的每技能注记），再执行本技能。

对手尝试破坏一个改动或一个设计。发现只有被运行证明才能留下。报告发现。不应用修复。

## Frame

范围是用户点名的。否则是分支相对其与基线分支 merge base 的 diff，包含工作树。用 **in-your-own-words** 技能陈述意图，依据是用户的消息、提交和 PR 描述。意图不清时问用户。

## Fan out

运行 **arena** 技能的 Phase A 步骤 3 和 4 以及 Phase B，改动四处：读 `interrogate reviewers` 行替代 `arena runners`。把范围的未提交改动复制进每个工作树。每个对手以 `general-purpose` 派出。替代 arena 的任务和理由，给每个对手范围、意图和这份简报：

> 破坏这个改动。每个发现都要用一次对真实代码的运行来证明，比如一个失败的测试、一个复现脚本、或展示错误行为的命令输出。对设计或方案，跑一个原型或在当前树上探测。复现留在你自己的工作树里。报告每个发现时给出标题、确切命令、它打印的输出、以及意图要求的输出。略去你没有运行过的任何东西。那包括风格、命名、结构，以及需要未来改动才能成立的风险。「没有发现」是有效结果。

## Verify

按 arena 的 Phase F 验证每个发现，重跑它的命令。输出展示了失败、且失败破坏意图的发现保留。其余丢弃。合并共享同一根因的发现。

跳过 arena 的 Phase C、D、E。对手找到的失败各不相同，所以结论保留每一个已验证的发现，而不是某一个对手的清单。

## 输出

- **Intent**：复述。
- **Findings**：每个已验证发现给出命令、其输出、它如何破坏意图、以及发现它的对手。没有一个存活时写「no verified findings」。
- **Dropped**：每个对手被丢弃发现的数量及原因。

## Models

角色默认值，盖戳自 `plugins/pstack/models.json`（要改就在那里改，然后重跑 `tools/generate.mjs`）。`pstack-models.md` 覆盖表中匹配的角色行会在运行时覆盖这里的默认值；`/setup-pstack` 负责写入，并按运行时列出其路径。

- interrogate reviewers: `opus`, `fable`, `sonnet`, `haiku`

## Reasoning effort

覆盖表中的角色值可以在模型后面带上推理强度，如 `opus @xhigh`。Claude Code 上的档位：`low`、`medium`、`high`、`xhigh`、`max`。哪些档位可用取决于模型。不带 `@` 的值取该表的 `default effort` 行（一个档位或 `session`），表里没有该行时取 `session`。在 Claude Code 上，`session` 不设置强度。在其他运行时上，`session` 按平台映射处理。读取模型前先剥掉后缀：`inherit-parent` 或 `auto` 在每一层都不传 `model`，模型名则作为 `model` 传入。把档位作为派发的 effort 字段传入，`subagent_type` 保持原样。在 Claude Code 的 `Agent` 调用上是 `effort`，在 Codex 的 `spawn_agent` 上是 `reasoning_effort`。在 Muse 上是 Workflow 子任务的 `effort`；`subagent_spawn` 派发保持会话的强度。
