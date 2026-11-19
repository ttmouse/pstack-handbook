---
name: thermos
description: "并行启动两个 thermo-nuclear 评审子代理，然后综合它们的发现。用于 thermos、双 thermo 评审，或 bug/安全与代码质量合并的分支审计。"
---

# Thermos

在 Codex 上，先读[平台映射](../poteto-mode/references/codex-tools.md)，包括其中按 skill 的备注，再执行本技能。

在 GitHub Copilot 上，先读[平台映射](../poteto-mode/references/copilot-tools.md)，包括其中按 skill 的备注，再执行本技能。

在 Muse 上，先读[平台映射](../poteto-mode/references/muse-tools.md)，包括其中按 skill 的备注，再执行本技能。

在 Antigravity 上，先读[平台映射](../poteto-mode/references/agy-tools.md)，包括其中按 skill 的备注，再执行本技能。

把两轮 thermo 评审作为异步后台子代理并行跑起来，然后综合它们的结果。

## 工作流

1. 从用户请求、PR、当前分支或相关改动文件确定评审范围。
2. 收集 diff 和必要的文件/上下文摘录，让评审者无需猜测就能评估改动。
3. 在同一条消息里派出两个子代理，`run_in_background: true`：
   - `subagent_type: "pstack:thermo-nuclear-review-subagent"`，负责 bug、破坏性变更、安全、devex 回退、feature-flag 泄漏和其他分支审计风险。
   - `subagent_type: "pstack:thermo-nuclear-code-quality-review-subagent"`，负责可维护性、结构、文件尺寸增长、意大利面、抽象和代码库健康度风险。

   两个调用的 `model` 都设为 `pstack-models.md` 里 `thermos reviewers` 行的值；表或那一行缺失时用[模型](#模型)里的默认值。值为 `auto` 或 `inherit-parent` 时不设 `model`。如果 `Agent` 工具拒绝某个 slug，用默认值并说明。如果它拒绝默认值，用错误信息里同族最接近的有效 slug。按 **poteto-mode** 技能的 Subagents 一节，为每个子代理选适合任务的推理强度。
4. 给两个子代理传同一份限定范围的 diff/文件上下文，要求它们返回按优先级排列的发现，附文件引用和证据。
5. 两个都完成后综合结果，发现优先，跨评审者去重。重叠的发现权重更高，分歧用自己的判断解决，摘要保持简短。

如果各后台子代理的摘要已经对用户可见，不要整体复述。给出统一的结论、信号最强的发现，以及仍然存在的不确定性。

## 模型

角色默认值，来自 `plugins/pstack/models.json`（在那里编辑，重跑 `tools/generate.mjs`）。`pstack-models.md` 覆盖表里匹配的角色行会在运行时覆盖这里的每一项；`/setup-pstack` 负责写入，并列出每个运行时的表路径。

- thermos reviewers: `opus`

## 推理强度

覆盖表里的角色值可以在模型后面带推理强度，比如 `opus @xhigh`。Claude Code 上的级别：`low`、`medium`、`high`、`xhigh`、`max`。哪些可用取决于模型。不带 `@` 的值取表的 `default effort` 行（一个级别或 `session`），表里没有该行时取 `session`。在 Claude Code 上，`session` 不设置强度。在其他运行时上，`session` 按平台映射执行。读模型前先剥掉后缀：`inherit-parent` 或 `auto` 在每一层都仍然省略 `model`，模型名照常作为 `model` 传入。强度放在派发的 effort 字段里，`subagent_type` 用你本来要用的那个。在 Claude Code 的 `Agent` 调用上是 `effort`，在 Codex 的 `spawn_agent` 上是 `reasoning_effort`。在 Muse 上是 Workflow 子任务的 `effort`；`subagent_spawn` 派发沿用会话的强度。
