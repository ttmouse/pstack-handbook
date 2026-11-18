---
name: thermos
description: "并行启动两个 thermo-nuclear 审查子代理，然后综合它们的发现。用于 thermos、double thermo review，或合并 bug/安全与代码质量的分支审计。"
---

# Thermos

在 Codex 上，先读[平台映射](../poteto-mode/references/codex-tools.md)（包括其中的每技能注记），再执行本技能。

在 GitHub Copilot 上，先读[平台映射](../poteto-mode/references/copilot-tools.md)（包括其中的每技能注记），再执行本技能。

在 Muse 上，先读[平台映射](../poteto-mode/references/muse-tools.md)（包括其中的每技能注记），再执行本技能。

在 Antigravity 上，先读[平台映射](../poteto-mode/references/agy-tools.md)（包括其中的每技能注记），再执行本技能。

把两个 thermo 审查环节作为异步后台子代理并行运行，然后综合它们的结果。

## 工作流

1. 从用户请求、PR、当前分支或相关改动文件确定审查范围。
2. 收集 diff 以及审查者评估该改动所需的文件/上下文摘录，避免猜测。
3. 在同一条消息里以 `run_in_background: true` 启动两个子代理：
   - `subagent_type: "pstack:thermo-nuclear-review-subagent"`：管 bug、破坏、安全、devex 回归、feature-flag 泄漏和其他分支审计风险。
   - `subagent_type: "pstack:thermo-nuclear-code-quality-review-subagent"`：管可维护性、结构、文件体积增长、spaghetti、抽象和代码库健康风险。

   把两者的 `model` 都设为 `pstack-models.md` 中 `thermos reviewers` 行的值；表或该行缺失时用 [Models](#models) 的默认值。值为 `auto` 或 `inherit-parent` 时不设 `model`。若 `Agent` 工具拒绝某个 slug，用默认值并说明。若它拒绝默认值，用错误信息里同家族最接近的有效 slug。按 **poteto-mode** 技能的 Subagents 一节，为每项工作选子代理推理强度。
4. 给每个子代理相同的、划定范围的 diff/文件上下文，要求它返回带文件引用和证据、按优先级排序的发现。
5. 两者完成后，综合结果：发现优先，跨审查者去重。重叠的发现权重更高，分歧用自己的判断解决，摘要保持简短。

如果各个后台摘要已经对用户可见，不要整段复述。呈现统一结论、信号最强的发现、以及任何剩余的不确定性。

## Models

角色默认值，盖戳自 `plugins/pstack/models.json`（要改就在那里改，然后重跑 `tools/generate.mjs`）。`pstack-models.md` 覆盖表中匹配的角色行会在运行时覆盖这里的默认值；`/setup-pstack` 负责写入，并按运行时列出其路径。

- thermos reviewers: `opus`

## Reasoning effort

覆盖表中的角色值可以在模型后面带上推理强度，如 `opus @xhigh`。Claude Code 上的档位：`low`、`medium`、`high`、`xhigh`、`max`。哪些档位可用取决于模型。不带 `@` 的值取该表的 `default effort` 行（一个档位或 `session`），表里没有该行时取 `session`。在 Claude Code 上，`session` 不设置强度。在其他运行时上，`session` 按平台映射处理。读取模型前先剥掉后缀：`inherit-parent` 或 `auto` 在每一层都不传 `model`，模型名则作为 `model` 传入。把档位作为派发的 effort 字段传入，`subagent_type` 保持原样。在 Claude Code 的 `Agent` 调用上是 `effort`，在 Codex 的 `spawn_agent` 上是 `reasoning_effort`。在 Muse 上是 Workflow 子任务的 `effort`；`subagent_spawn` 派发保持会话的强度。
