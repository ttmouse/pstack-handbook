---
name: why
description: "用于「X 为什么这样运作」「我们为什么选了 Y」、设计缘由、回退、复盘或需要数据支撑的阈值。发现可用的 MCP 并对每个证据类别（源码控制、工单系统、长文档、实时聊天、基础设施可观测性、错误追踪、产品分析仓库）并行查询，然后返回带引用的决策与权衡解读。运行时行为用 how。"
---

# Why

在 Codex 上，遵循本技能之前先读[平台映射](../poteto-mode/references/codex-tools.md)，包括其按技能的说明。

在 GitHub Copilot 上，遵循本技能之前先读[平台映射](../poteto-mode/references/copilot-tools.md)，包括其按技能的说明。

在 Muse 上，遵循本技能之前先读[平台映射](../poteto-mode/references/muse-tools.md)，包括其按技能的说明。

在 Antigravity 上，遵循本技能之前先读[平台映射](../poteto-mode/references/agy-tools.md)，包括其按技能的说明。

调查代码背后的动机与意图。配套的 `how` 技能回答代码做什么、怎么运作。`why` 回答是什么力量塑造了它的形态。

下文每个 spawn 都对应 `pstack-models.md` 里的一个角色行，默认值见 [Models](#models)。把 `model` 设为那一行的值；若表或行缺失，用默认值。值为 `auto` 或 `inherit-parent` 时，不要设置 `model`。如果 `Agent` 工具拒绝某个 slug，用默认值并说明。如果它拒绝默认值，用错误信息里同一家族最接近的有效 slug。按 **poteto-mode** 技能的 Subagents 一节，为每个子代理按任务选择推理等级。

每个 spawn 都是 `general-purpose` 且 `readonly: false`（agent 模式）。**不要用 readonly/Ask 模式。**它会剥离 MCP 访问，使基于 MCP 的调查者和综合者的引用抽查失效。调查者仍然不应写任何东西。

## 运行姿态

以**审慎、谨慎、精确的调查者**身份运作。对自己知道的和推断的诚实区分。完整信心框架和措辞指南见 `references/epistemics.md`。综合者必须遵循它。

## 第 1 步：理解目标和问题

**目标**通常是一段代码、一个模式、一个功能，或一个有名的设计决策。**问题**通常是设计缘由、权衡、一个有驱动力的边界情况、外部约束、死代码，或宽泛的历史梳理。

如果目标模糊（「我们为什么这样做？」且没有明确所指），从会话上下文做出最佳猜测（打开的文件、最近的编辑、光标位置、刚讨论的内容）。简要陈述你的理解，以便猜偏时用户可以纠正，然后继续。

## 第 2 步：建立代码锚点

spawn 调查者之前，先在线程内构建种子上下文：文件路径和行范围、关键符号（函数、类、常量）、触及目标最近的几次提交、来自合并提交的 PR 编号（subject 里的 `(#1234)` 模式），以及任何关联的工单 ID。跑 `git blame -L <start>,<end> <file>` 拿最后触改的提交，`git log --follow -p -- <file>` 拿穿透重命名的完整历史补丁，`git log --oneline -20 -- <file>` 拿带 PR 编号的近期提交，`git log -1 --format=%B <commit>` 提取 PR 编号。然后对任何有实质内容的提交拉取 PR 正文和讨论：`gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews`。这个锚点发给每个调查者和综合者。

## 第 3 步：并行 spawn 调查者

**默认做完整的并行调查。**目标是完整的覆盖地图，不是最小覆盖。记录空结果，不要跳过搜索。

### 发现

spawn 调查者之前，列出 Claude Code 环境中可用的 MCP。用系统提示顶部的工具列表（每个 MCP 都是一个前缀为 `mcp__<server>__<name>` 的工具）。否则读插件/项目里的 `.mcp.json`，或运行 `claude mcp list`。

把每个可用的 MCP 映射到一个证据类别：

1. 源码控制历史
2. 工单系统
3. 长文档
4. 实时团队聊天
5. 基础设施可观测性
6. 错误/异常追踪
7. 产品分析仓库

源码控制通过 git 和 `gh` 永远可用。其余六类，依据 MCP 名称、服务器说明、工具名和资源描述符分类。如果某个 MCP 能匹配多个类别，选与其主要证据匹配的那个。含糊的情况记入覆盖地图。

对每个有匹配 MCP 的类别各 spawn 一个调查者，全部放在同一条消息里以便并发运行，每个只拥有一个工具或 MCP。不要让一个代理覆盖多个 MCP。`model`：`why investigators` 行，默认值见 [Models](#models)。

每个调查者的提示词是填好的 `references/investigator-prompt.md`，外加：

- 所选 MCP 对应的类别 playbook `references/sources/<source>.md`，从 `references/source-playbook.md` 的示例改编
- `references/sources/incident-postmortem.md` **如果目标代码看起来是防御性的**（空值检查、重试逻辑、超时处理、限流、feature flag、出口守卫、OOM 处理）
- 代码锚点和用户的原始问题

### 调查者名册，每个可用证据类别一个

下面每个类别都独占地适合浮出一种形状的「为什么」，列在「Best at」之后。用它来预期回报、在某类别返回空时指名缺口，以及——仅在罕见的可证明无关的情形——为跳过提供理由。

1. **源码控制**（git 历史、`gh` 查 PR、代码注释、测试）。必 spawn，唯一有保证的来源。Best at *评审期间记录下来的实现时缘由*。
2. **工单系统**（如 Linear、Jira、GitHub Issues、Plane、Shortcut MCP）。Best at *产品或业务的强制因素*。当「为什么」在工程之外时最强。
3. **长文档**（如 Notion、Confluence、Google Docs、Coda MCP）。Best at *代码成形之前写下的长篇设计缘由*。
4. **实时团队聊天**（如 Slack、Discord、Microsoft Teams、Mattermost MCP）。Best at *从未落进文档的实时讨论*。当源码控制、工单和文档的书面痕迹很薄时尤其重要。
5. **基础设施可观测性**（如 Datadog、New Relic、Honeycomb、Grafana、Splunk MCP）。Best at *催生代码的基础设施与运行时现实*。当目标是对基础设施数据（超时、重试、限流、熔断）的反应时最强。
6. **错误/异常追踪**（如 Sentry、Rollbar、Bugsnag、Airbrake MCP）。Best at *催生防御性或纠正性代码的具体异常与错误轨迹*。对 catch 块、空值守卫、类型检查、重试和其他防御最强。
7. **产品分析仓库**（如 Databricks、Snowflake、BigQuery、ClickHouse、dbt、Redshift MCP）。Best at *塑造代码的产品与数据现实*。对 feature flag 门控的代码、实验驱动的发布、数据迁移，以及「这个数字哪来的」类问题最强。

### 什么时候可以跳过调查者

只有在**明确、书面、进入最终 Sources Consulted 的理由**下才可以。两个有效理由：

- **本环境没有该类别可用的 MCP。**把它标记为缺口，而不是选择：「Real-time team chat skipped. No matching MCP available, so the conversational record was not searchable.」
- **来源可证明无关**，而不只是「大概无关」。门槛很高：「Error / exception tracking skipped. Target is a build-time script with no runtime code path.」

如果你的范围评估表明目标是一个单提交的琐碎改动、PR 描述已包含完整答案，你可以在**确认所有七个可用类别搜索都多余之后**在线直接作答。明确说出来。这应当罕见。

## 第 4 步：综合

spawn 一个综合者。`model`：`why synthesizer` 行，默认值见 [Models](#models)。它拿到：

1. 调查者的发现，包括空结果和任何带理由跳过的类别
2. 代码锚点
3. 用户的原始问题
4. `references/epistemics.md` 中的认识论框架
5. `references/synthesizer-prompt.md` 的综合者提示模板

## 第 5 步：呈现

把综合者的输出呈现给用户。可以为清晰度做轻度编辑，或补充会话中的上下文，但**不要改写信心措辞**。

## 输出格式

结构即 `references/synthesizer-prompt.md` 中的：The Question、The Code in Question、What We Found、What We Can Reasonably Infer、Competing Hypotheses、What We Don't Know、Sources Consulted、Confidence Summary。可按需调整，但保持信心区分完好，Sources Consulted 保持每个调查者一行，包括返回空和被跳过的，并写明原因。

在 Sources Consulted 之后，如果用户的 `why` 问题是要改动这段代码的前奏，把沿革发现转成用于规划改动的 Preserve / Change / Avoid / Risk 约束集。

## 要避免的常见失败模式

- **近因偏误**。假定最近的提交是权威的。当前形态往往是更早许多决策的累积。往回追。

## Models

角色默认值，盖自 `plugins/pstack/models.json`（在那儿改，重跑 `tools/generate.mjs`）。`pstack-models.md` 覆盖表中匹配的角色行在运行时覆盖这些值；`/setup-pstack` 写它，并按运行时列出路径。

- why investigators: `opus`
- why synthesizer: `opus`

## Reasoning effort

覆盖表中的角色值可以在模型后面带推理等级，如 `opus @xhigh`。Claude Code 上的等级：`low`、`medium`、`high`、`xhigh`、`max`。哪些可用取决于模型。不带 `@` 的值取表的 `default effort` 行——一个等级或 `session`；表里没有该行时取 `session`。在 Claude Code 上，`session` 不设置等级。其他运行时，`session` 按平台映射处理。读模型之前先去掉后缀：`inherit-parent` 或 `auto` 在任何层级都不传 `model`，模型名则作为 `model` 传入。把等级作为派遣的 effort 字段传入，`subagent_type` 保持原样。即 Claude Code 的 `Agent` 调用上是 `effort`，Codex 的 `spawn_agent` 上是 `reasoning_effort`。在 Muse 上，它是 Workflow 子任务的 `effort`；`subagent_spawn` 派遣保持会话的等级。
