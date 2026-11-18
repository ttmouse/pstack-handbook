---
name: how
description: "用于「X 是怎么工作的」、改动前的代码走读，以及位置/归属/分层问题（「这个应该放哪」「哪个包拥有这个」「这是不是正确的层」）。解释子系统架构、运行时流程、上手心智模型。动机问题用 why。"
---

# How

在 Codex 上，先读[平台映射](../poteto-mode/references/codex-tools.md)（包括其中的每技能注记），再执行本技能。

在 GitHub Copilot 上，先读[平台映射](../poteto-mode/references/copilot-tools.md)（包括其中的每技能注记），再执行本技能。

在 Muse 上，先读[平台映射](../poteto-mode/references/muse-tools.md)（包括其中的每技能注记），再执行本技能。

在 Antigravity 上，先读[平台映射](../poteto-mode/references/agy-tools.md)（包括其中的每技能注记），再执行本技能。

探索代码库来回答「X 是怎么工作的」类问题。产出达到资深工程师上手一个子系统水准的架构解释，足以建立可用的心智模型，又不至于读起来像带注释的源码。

每次派出都是 `Agent` 子代理，`subagent_type: "general-purpose"`、`readonly: true`。Explorer 用 `pstack-models.md` 的 `how explorer` 行（默认见 [Models](#models)），每个 explainer 用 `how explainer` 行（默认见 [Models](#models)）。把 `model` 设为该行的值，表或该行缺失时用默认值。值为 `auto` 或 `inherit-parent` 时不设 `model`。若 `Agent` 工具拒绝某个 slug，用默认值并说明。若它拒绝默认值，用错误信息里同家族最接近的有效 slug。按 **poteto-mode** 技能的 Subagents 一节，为每项工作选子代理推理强度。

## 1. 评估复杂度

范围模糊时，陈述你的理解并开始探索。用户可以纠正方向。

- **简单**（单个模块、小工具、如「函数 X 怎么工作」的窄问题）：不用 explorer。派一个 explainer，一次性探索并解释，用 `references/explainer-prompt.md` 构建、去掉 explorer-findings 一节。跳到第 4 步。
- **复杂**（横跨多个文件或服务的子系统、横切功能、完整架构概览）：到第 2 步。

拿不准时走简单路径。

## 2. 探索（仅复杂）

把问题分解为 2 到 4 个角度，每个是子系统的一个不同切片。在一条消息里派出全部 explorer，各自填好 `references/explorer-prompt.md` 和自己的角度。

## 3. 综合（仅复杂）

全部 explorer 返回后，派一个 explainer，填好 `references/explainer-prompt.md` 和所有 explorer 的发现。

## 4. 呈现

呈现 explainer 的输出。为了清晰或补充对话上下文做轻度编辑没问题。不要大幅重写。

## 输出格式

解释使用 `references/explainer-prompt.md` 定义的章节，不适用的删掉：Overview、Key Concepts、How It Works、Where Things Live、Gotchas。

## Models

角色默认值，盖戳自 `plugins/pstack/models.json`（要改就在那里改，然后重跑 `tools/generate.mjs`）。`pstack-models.md` 覆盖表中匹配的角色行会在运行时覆盖这里的默认值；`/setup-pstack` 负责写入，并按运行时列出其路径。

- how explorer: `opus`
- how explainer: `opus`

## Reasoning effort

覆盖表中的角色值可以在模型后面带上推理强度，如 `opus @xhigh`。Claude Code 上的档位：`low`、`medium`、`high`、`xhigh`、`max`。哪些档位可用取决于模型。不带 `@` 的值取该表的 `default effort` 行（一个档位或 `session`），表里没有该行时取 `session`。在 Claude Code 上，`session` 不设置强度。在其他运行时上，`session` 按平台映射处理。读取模型前先剥掉后缀：`inherit-parent` 或 `auto` 在每一层都不传 `model`，模型名则作为 `model` 传入。把档位作为派发的 effort 字段传入，`subagent_type` 保持原样。在 Claude Code 的 `Agent` 调用上是 `effort`，在 Codex 的 `spawn_agent` 上是 `reasoning_effort`。在 Muse 上是 Workflow 子任务的 `effort`；`subagent_spawn` 派发保持会话的强度。
