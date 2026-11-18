---
name: swarm
description: "扇出 N 个并行 worker，收干它们，返回一份报告。用于 /swarm、'swarm this'，或并行覆盖、竞速、gauntlet 和探索。"
---

# Swarm

在 Codex 上，先读[平台映射](../poteto-mode/references/codex-tools.md)（包括其中的每技能注记），再执行本技能。

在 GitHub Copilot 上，先读[平台映射](../poteto-mode/references/copilot-tools.md)（包括其中的每技能注记），再执行本技能。

在 Muse 上，先读[平台映射](../poteto-mode/references/muse-tools.md)（包括其中的每技能注记），再执行本技能。

在 Antigravity 上，先读[平台映射](../poteto-mode/references/agy-tools.md)（包括其中的每技能注记），再执行本技能。

## 开始

在启动任何东西之前，开一个 todolist，每个阶段一条。

1. Frame
2. Fan out
3. Aggregate
4. Report

## 阶段 A：Frame

1. 陈述完成谓词，以及 swarm 必须返回的工件或报告。
2. 选择形状。切分成片，或在相同简报上竞速 N 个 worker，或两者混合。对竞速或混合形状，在派出之前声明 `first pass`、`rank all` 或 `best-of`。
3. 从 `pstack-models.md` 的 `swarm workers` 行选 worker 模型。表或该行缺失时，用 [Models](#models) 的默认值。`auto` 或 `inherit-parent` 时不传 `model`，worker 跑在父模型上。若 `Agent` 工具拒绝某个 slug，用默认值并说明。若它拒绝默认值，用错误信息里同家族最接近的有效 slug。模型竞速时，事先点名每臂的模型。按 **poteto-mode** 技能的 Subagents 一节，为每项工作选子代理推理强度。
4. 给每个会写输出的 worker 它自己可写的输出。worker 验证或测量提交时，每份简报点名确切的 SHA。测量简报还要点名方法（样本数、一个样本是什么、顺序）。worker 在结果里记录这两者。

## 阶段 B：Fan out

在一条消息里派出全部 N 个 worker，`subagent_type: "general-purpose"`、`run_in_background: true`、用步骤 3 的模型（`auto` 或 `inherit-parent` 时不设）。Claude Code 子代理都在本机运行，所以隔离来自阶段 A 分配的 worktree 或输出目录，而不是远程环境。

worker 必须从非默认分支开始时，在它自己的工作树里检出该分支，并在简报里写明工作树路径。

每份简报独立成立。包含目标、范围、确切的切片或竞速臂、如何验证、报告什么。报告用 `PASS`、`ISSUES` 或 `BLOCKED` 加证据。能证明缺陷的 worker 报 `ISSUES`，并列出它能证明的每一个问题，不只第一个。

某个 worker 掉线，用 N-1 继续，并注明。

## 阶段 C：Aggregate

读取最终结果。丢弃没有记录简报所点名的 SHA 和方法的结果，并把该 worker 重派一次。第二次仍缺，记为一个 gap。gap 不算 pass。覆盖任务里，每个必需切片都要有结果。竞速任务里，套用事先声明的选择规则。用 first pass、rank all 或 best-of。不要粘贴 worker 的原始转储。

## 阶段 D：Report

返回一份合并的会话内报告，含结果表、问题单行、gap 或掉线、以及若使用了竞速规则则写明该规则。

## Models

角色默认值，盖戳自 `plugins/pstack/models.json`（要改就在那里改，然后重跑 `tools/generate.mjs`）。`pstack-models.md` 覆盖表中匹配的角色行会在运行时覆盖这里的默认值；`/setup-pstack` 负责写入，并按运行时列出其路径。

- swarm workers: `opus`

## Reasoning effort

覆盖表中的角色值可以在模型后面带上推理强度，如 `opus @xhigh`。Claude Code 上的档位：`low`、`medium`、`high`、`xhigh`、`max`。哪些档位可用取决于模型。不带 `@` 的值取该表的 `default effort` 行（一个档位或 `session`），表里没有该行时取 `session`。在 Claude Code 上，`session` 不设置强度。在其他运行时上，`session` 按平台映射处理。读取模型前先剥掉后缀：`inherit-parent` 或 `auto` 在每一层都不传 `model`，模型名则作为 `model` 传入。把档位作为派发的 effort 字段传入，`subagent_type` 保持原样。在 Claude Code 的 `Agent` 调用上是 `effort`，在 Codex 的 `spawn_agent` 上是 `reasoning_effort`。在 Muse 上是 Workflow 子任务的 `effort`；`subagent_spawn` 派发保持会话的强度。
