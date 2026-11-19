---
name: swarm
description: "扇出 N 个并行 worker，收割结果，返回一份报告。用于 /swarm、'swarm this'，或并行覆盖、竞速、闯关和探索。"
---

# Swarm

在 Codex 上，先读[平台映射](../poteto-mode/references/codex-tools.md)，包括其中按 skill 的备注，再执行本技能。

在 GitHub Copilot 上，先读[平台映射](../poteto-mode/references/copilot-tools.md)，包括其中按 skill 的备注，再执行本技能。

在 Muse 上，先读[平台映射](../poteto-mode/references/muse-tools.md)，包括其中按 skill 的备注，再执行本技能。

在 Antigravity 上，先读[平台映射](../poteto-mode/references/agy-tools.md)，包括其中按 skill 的备注，再执行本技能。

## 开始

在启动任何东西之前，先开一个 todolist，每个阶段一条。

1. 定框
2. 扇出
3. 聚合
4. 报告

## 阶段 A：定框

1. 说清完成判据，以及 swarm 必须返回的产物或报告。
2. 选形状。切成多个分片，或让 N 个 worker 在相同简报上竞速，或两者混合。竞速或混合形状要在派出前声明 `first pass`、`rank all` 或 `best-of`。
3. 从 `pstack-models.md` 的 `swarm workers` 行选 worker 模型。如果表或那一行缺失，用[模型](#模型)里的默认值。值为 `auto` 或 `inherit-parent` 时省略 `model`，让 worker 跑在父模型上。如果 `Agent` 工具拒绝某个 slug，用默认值并说明。如果它拒绝默认值，用错误信息里同族最接近的有效 slug。模型竞速时，每条臂的模型要提前点名。按 **poteto-mode** 技能的 Subagents 一节，为每个子代理选适合任务的推理强度。
4. 每个 worker 写文件时给它独立的可写输出。worker 验证或测量 commit 时，简报里写明确切的 SHA。测量类简报还要写方法（样本数、一个样本是什么、顺序）。worker 把两者都记进结果。

## 阶段 B：扇出

在一条消息里派出全部 N 个 worker，`subagent_type: "general-purpose"`，`run_in_background: true`，模型用步骤 3 选的值，`auto` 或 `inherit-parent` 时不设。Claude Code 的子代理都跑在本机，所以隔离来自阶段 A 分配的工作树或输出目录，不来自远程环境。

当 worker 必须从非默认分支开始时，在它自己的工作树里检出该分支，并在简报里写明工作树路径。

每份简报都独立成立。包含目标、范围、确切的分片或竞速臂、如何验证、报告什么。报告用 `PASS`、`ISSUES` 或 `BLOCKED`，附证据。能证明缺陷的 worker 报 `ISSUES`，列出它能证明的每一个问题，不只第一个。

如果有 worker 掉线，用 N-1 继续，并记一笔。

## 阶段 C：聚合

读最终结果。丢弃一个没有记录简报所要求的 SHA 和方法的结果，并重新派出该 worker 一次。第二次还不合格，记一个缺口。缺口不算通过。覆盖型任务，每个必需分片都要有结果。竞速型任务，按提前声明的选择规则执行：first pass、rank all 或 best-of。不要粘贴 worker 的原始输出。

## 阶段 D：报告

在对话里返回一份合并报告：结果表格、问题一句话摘要、缺口和掉线记录，用了竞速时附竞速规则。

## 模型

角色默认值，来自 `plugins/pstack/models.json`（在那里编辑，重跑 `tools/generate.mjs`）。`pstack-models.md` 覆盖表里匹配的角色行会在运行时覆盖这里的每一项；`/setup-pstack` 负责写入，并列出每个运行时的表路径。

- swarm workers: `opus`

## 推理强度

覆盖表里的角色值可以在模型后面带推理强度，比如 `opus @xhigh`。Claude Code 上的级别：`low`、`medium`、`high`、`xhigh`、`max`。哪些可用取决于模型。不带 `@` 的值取表的 `default effort` 行（一个级别或 `session`），表里没有该行时取 `session`。在 Claude Code 上，`session` 不设置强度。在其他运行时上，`session` 按平台映射执行。读模型前先剥掉后缀：`inherit-parent` 或 `auto` 在每一层都仍然省略 `model`，模型名照常作为 `model` 传入。强度放在派发的 effort 字段里，`subagent_type` 用你本来要用的那个。在 Claude Code 的 `Agent` 调用上是 `effort`，在 Codex 的 `spawn_agent` 上是 `reasoning_effort`。在 Muse 上是 Workflow 子任务的 `effort`；`subagent_spawn` 派发沿用会话的强度。
