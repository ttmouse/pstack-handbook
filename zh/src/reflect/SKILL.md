---
name: reflect
description: 在活跃会话记录上生成三个并行评审子代理，提炼可沉淀的经验，并把每条路由到一个现有技能的具体修改上。用户说 reflect 时使用。
---

# Reflect

在 Codex 上，先读[平台映射](../poteto-mode/references/codex-tools.md)（包括其中的逐技能说明），再执行本技能。

在 GitHub Copilot 上，先读[平台映射](../poteto-mode/references/copilot-tools.md)（包括其中的逐技能说明），再执行本技能。

在 Muse 上，先读[平台映射](../poteto-mode/references/muse-tools.md)（包括其中的逐技能说明），再执行本技能。

在 Antigravity 上，先读[平台映射](../poteto-mode/references/agy-tools.md)（包括其中的逐技能说明），再执行本技能。

从当前对话里挖掘可沉淀的经验，然后把它们路由进技能修改。

用户说「reflect」或「/reflect」时调用。对话琐碎、跑题、或已被父代理正确遵循的现有技能覆盖时跳过。一次性的事不是经验。

## 1. 定位活跃会话记录

扇出之前，在 Claude Code 的按项目会话记录目录 `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/<encoded-cwd>/` 里找到本次对话的转录。不要跨 `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/` 做 glob。那会跨过工作区边界，读到无关项目的私人聊天。

在已安装插件下跑 `skills/reflect/scripts/find-transcript.mjs`，带 projects 目录和对话开头用户提示的一个片段。它旁边的 `claude-project-dir.mjs` 打印本次会话的 projects 目录，不管 shell 之后挪到哪：

```bash
dir=$(node <plugin>/skills/reflect/scripts/claude-project-dir.mjs) && node <plugin>/skills/reflect/scripts/find-transcript.mjs "$dir" "<opening prompt fragment>"
```

它覆盖三种布局（扁平的 `<id>.jsonl`、嵌套的 `<id>/<id>.jsonl`、子代理的 `<parent>/subagents/<child>.jsonl`），按最新优先，打印第一条开头键入提示携带该片段的路径。不要手工重新实现这个扫描：转录的第一行是会话元数据，不是消息；以 `/clear` 或 `!` shell 命令开头的会话会把那条命令的包装和输出作为 `user` 记录记在提示之前；文件能跑到几个兆，所以 finder 会流式读取每个候选并在第一条键入的 `user` 记录处停止。如果这行退出码为 1，写一份紧凑的会话摘要传进去。摘要按对话顺序一行一条列出：用户的提示和纠正、工具调用及其结果、触碰过的文件。它不下诊断、不给结论、不说原因。评审者评判的是会话，不是你对它的结论。

## 2. 并行生成三个评审者

一条消息，三个 `Agent` 调用，`subagent_type: "general-purpose"`。评审者需要 MCP 访问来查转录引用的工单、聊天线程和可观测性 trace，所以选一个保留 MCP 访问的 subagent_type。提示词禁止写文件。父代理执行修改。

每个评审者和合成者在 `pstack-models.md` 里各对应一行角色，[Models](#models) 里各有一个默认值。`model` 设为那行的值，表或那行缺失时用默认值。值为 `auto` 或 `inherit-parent` 时把 `model` 留空。`Agent` 工具拒绝某个 slug，就用默认值并说出来。拒绝默认值的话，用错误信息里同家族最接近的合法 slug。按 **poteto-mode** 技能的 Subagents 小节，为工作选择每个子代理的推理强度。

| 视角 | 角色行 | 提示词模板 |
|---|---|---|
| Judgment | `reflect judgment, divergent, synthesizer` | `references/judgment-reviewer.md` |
| Tooling | `reflect tooling` | `references/tooling-reviewer.md` |
| Divergent | `reflect judgment, divergent, synthesizer` | `references/divergent-reviewer.md` |

每个模板逐字传递，在标记处替换转录路径或摘要。转录路径旁边什么都不加，长转录也不要加重点提示。评审者在 `Agent` 响应正文里返回发现。

## 3. 合成

一个 `Agent` 调用，`subagent_type: "general-purpose"`，`model` 取自 `reflect judgment, divergent, synthesizer` 行（默认见 [Models](#models)）。它通过 MCP 抽查引用，所以选一个保留 MCP 访问的 subagent_type。逐字传递 `references/synthesizer.md`，在标记处内联每个评审者的完整输出。它返回一份 Accepted / Rejected / Backlog 列表。

## 4. 结构化强制检查

把任何一条用 lint 规则、脚本、元数据 flag 或运行时检查能更可靠强制执行的 Accepted 项移到 Backlog。见 **encode-lessons-in-structure** 原则技能。

## 5. 应用

展示合成器的完整 Accepted / Rejected / Backlog 输出，等明确批准后才执行任何 Accepted 修改。用户挑子集，也可能改路由。技能改动影响组织里每个未来的代理。不要自动执行。

每条 Backlog 项不等审批就归档到你们团队的 devex 或 backlog 跟踪器。只有 Accepted 列表等审批。

绝不编辑 `plugins/cache/` 下的技能。批准前，展示它的目的地：`.claude/skills/<skill>/` 或 `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/<skill>/`。批准后，把技能文件夹复制到那里并编辑副本。绝不开 PR 或 push。

严格按每条批准行的 Routing 执行：

- 琐碎的现有技能修改（一行 bullet、一句收紧的话、一个过时事实的更正）：父代理直接做。
- 实质性的现有技能修改（新小节、新模式表、超过约 10 行）：交给 **plugin-dev:skill-development** 技能，跑它的 draft / test / iterate 闭环。
- `tune description: <skill path>`（技能存在但该触发时没触发）：交给 `plugin-dev:skill-development`，跑它的 description 优化闭环。
- `new skill via plugin-dev:skill-development: <kebab-name>`：把创建交给 `plugin-dev:skill-development`。不要临时发明形状。

如果你的环境带 SKILL.md 校验器，在宣布完成前对每个触碰过的技能跑一遍它。

## 6. 给用户总结

短列表，无前言：

- 已应用的修改：`<skill path>`。改了什么，每条一行。
- 新建的技能：`<skill path>`。每条一行（少见）。
- 已归档到 devex 跟踪器的 Backlog：`<issue title>`（`<tags>`）。每条一行。
- 已丢弃：每条被拒发现一行 + 合成器给的理由。

## Models

角色默认值，从 `plugins/pstack/models.json` 戳出（在那儿改，重跑 `tools/generate.mjs`）。`pstack-models.md` 覆盖表里匹配的角色行在运行时覆盖每一项；`/setup-pstack` 写它并按宿主列出其路径。

- reflect tooling: `opus`
- reflect judgment, divergent, synthesizer: `opus`

## Reasoning effort（推理强度）

覆盖表里的角色值可以在模型后面带推理强度，比如 `opus @xhigh`。Claude Code 上的等级：`low`、`medium`、`high`、`xhigh`、`max`。哪些可用取决于模型。不带 `@` 的值取表的 `default effort` 行——一个等级或 `session`；表没有该行时取 `session`。在 Claude Code 上，`session` 不设置强度。其他宿主上，`session` 按平台映射走。读模型前先剥掉后缀：`inherit-parent` 或 `auto` 在每个等级上仍然省略 `model`，模型名照常作为 `model` 传入。等级作为派发的 effort 字段传入，`subagent_type` 照常用你本来要用的。即 Claude Code 的 `Agent` 调用上是 `effort`，Codex 的 `spawn_agent` 上是 `reasoning_effort`。在 Muse 上是 Workflow 子代理上的 `effort`；`subagent_spawn` 派发保持会话的强度。
