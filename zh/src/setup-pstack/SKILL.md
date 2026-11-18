---
name: setup-pstack
description: 配置 pstack 每个角色使用哪些模型。检测可用模型，写入当前宿主的覆盖表。用于 /setup-pstack、「配置 pstack 模型」、更改 pstack 的模型选择，或开关 SessionStart hook。
---

# Setup pstack

在 Codex 上，先读[平台映射](../poteto-mode/references/codex-tools.md)（含其逐技能备注），再执行本技能。

在 GitHub Copilot 上，先读[平台映射](../poteto-mode/references/copilot-tools.md)（含其逐技能备注），再执行本技能。

在 Muse 上，先读[平台映射](../poteto-mode/references/muse-tools.md)（含其逐技能备注），再执行本技能。

在 Antigravity 上，先读[平台映射](../poteto-mode/references/agy-tools.md)（含其逐技能备注），再执行本技能。

在 Grok Build 上，先读[平台映射](../poteto-mode/references/grok.md)，并跳过第 4 步、第 3 步的 effort 提问和第 5 步的 effort 校验；配置表里省略 effort 和 `session hook` 行及后缀。Grok 不暴露 effort 控制，`session hook` 行也不控制 Grok 的路由提示。

在 GitHub Copilot 上，按 [Copilot 安装步骤](copilot.md) 替代第 1、3、4、7 步和第 6 步的标题。

在 OMP 上，按 [OMP 安装](../poteto-mode/references/omp-tools.md#model-names) 执行，替代第 1 至 8 步。OMP 使用原生模型角色和 agent 覆盖；其全局 pstack 配置表只控制 session hook。询问主会话路由对所有 OMP profile 是开还是关。在 `~/.omp/pstack-models.md` 里，把所有 `session hook:` 行替换为一行精确的 `session hook: on` 或 `session hook: off`，保留其他行和现有编码。确认是全局作用域，然后重启会话以清除先前上下文。

在 Kimi Code CLI 上，跳过第 4 步、第 3 步的 effort 提问和第 5 步的 effort 校验；配置表里省略 effort 和 `session hook` 行及后缀。第 8 步里，说明路由由插件的启用状态控制，而不是汇报 hook 设置。见 [Kimi 模型名](../poteto-mode/references/kimi-tools.md#model-names)。

在其他宿主上，读下方的[其他宿主](#other-runtimes)了解配置表位置和加载方式；步骤相同。

写入当前宿主的逐角色模型覆盖表，路径见[其他宿主](#other-runtimes)。每个 pstack 技能都在行内写明默认模型；覆盖表把这些默认适配到你实际可用的模型。

Claude Code 没有 Cursor `.mdc` 那种自动应用的「规则」机制。Claude Code 配置目录在设置了 `$CLAUDE_CONFIG_DIR` 时取该变量，否则取 `~/.claude`。本技能称它为 `<config>`。引入是显式的：用户在 `<config>/CLAUDE.md`（或其项目 `CLAUDE.md`）里加一行，例如：

```text
@<config>/pstack-models.md
```

`<config>` 写成解析后的路径，这样该文件会作为上下文加载进每个会话。

Codex 主目录在设置了 `$CODEX_HOME` 时取该变量，否则取 `~/.codex`。本技能称它为 `<codex-home>`。

## Steps（步骤）

### 1. 检测可用模型

枚举本次会话 `Agent` 工具的 `model` 参数接受哪些模型名。这是可靠的来源。在 Claude Code 上它们是下方 [Models](#models) 列出的家族名，每个跑该家族的当前模型，完整模型 ID 会被拒绝。默认面板也列在那里。面板按跨家族多样性挑选。让用户确认或粘贴他们希望可用的其他 slug。绝不写入一个你没有确认可用的真实 slug。别名 `inherit-parent` 和 `auto` 永远有效，即使它们不是检测到的 slug。两者都表示该角色跑在父会话的模型上，`Agent` 调用以省略 `model` 来表达。

### 2. 加载当前状态

默认的角色到模型映射就是下方「写入覆盖表」步骤展示的规则形状。如果当前宿主的配置表已存在，读它，把它的值当作当前选择。否则从这些默认开始。一行若其角色不在该形状里，如 `how critics`，来自已退役的角色。删掉它。较旧的表可能写 `claude-` 开头的完整模型 ID，`Agent` 工具会拒绝。逐个替换为家族名，即 `claude-` 后面的那个词。

### 3. 映射并确认

展示每个角色及其当前模型，把任何不在检测集合里的真实 slug 标为待选择。同时列出第 2 步删除或改写的每一行。问是照单接受还是改特定角色，选项为检测到的模型加 `inherit-parent` 和 `auto`。优先用 `AskUserQuestion`，而非自由文本。面板类角色（arena runners、architect runners、interrogate reviewers）的值是一个列表，每个条目跑一个子代理，别名条目也算，所以列表长度就是数量。`arena cross-judge pool` 也是列表，但 Arena 只跑一个评审者。它只尝试家族不同于父模型的值，按列表顺序，所以按偏好排序。`inherit-parent` 或 `auto` 的值绝不评审。`swarm workers` 是每个 worker 的默认模型，除非竞速或对比按臂指定了别的模型。

然后问默认推理强度，即 `default effort` 行。它是 `session`（保持父会话的强度），或 [Models](#models) 里的一个级别。从那里列出的默认开始。每个不带后缀的角色值都按它运行。然后问是否有角色要在别的级别运行。在 Claude Code 上角色值可以在 slug 后带一个，如 `<slug> @xhigh`；面板条目各自带，如 `<slug> @xhigh, <slug> @max`。每个级别作为派发的 effort 传入，所以这个选择无需改动会话即生效。默认强度就不带后缀。

在 Codex 上，说明 `session` 需要当前线程的 active-turn 元数据，部分宿主不暴露。平台映射的 helper 会读它；不可用时，派发前必须显式选择强度。对这类宿主提供一个固定默认级别，而不是承诺自动继承。

### 4. 选择 session hook 是否路由任务

在 Claude Code 和 Codex 上，插件的 `SessionStart` hook 在启动、resume、clear 和 compact 时注入 poteto-mode 强制项。Codex 要求用户先经 `/hooks` 信任插件 hook 才会运行。在 Pi 上，pstack 扩展在每次 agent 启动时把同一强制项加进系统提示词。在 Muse 上，用户用 `muse plugins approve pstack` 批准插件的 hook 后，原生插件的 `SessionStart` hook 注入该强制项。在 OpenCode 2 上，原生插件把该强制项加进根会话的模型请求。询问是否保留该 hook。默认是开。答案就是当前宿主配置表里的 `session hook` 行：`on` 或 `off`。没有配置表或没有该行时，hook 注入。该行在没有 pstack 路由 hook 的其他宿主上是惰性的。

### 5. 校验

写入的每个真实 slug 必须在检测集合里。`inherit-parent` 和 `auto` 永远通过。校验 slug 时去掉所有 `@<level>` 后缀，级别对照 [Models](#models) 的 effort 级别。`default effort` 的值是这些级别之一或 `session`。在 Codex 上，级别改为你的 Codex 模型接受的 `reasoning_effort` 值。选中的真实 slug 或级别不可用时，停下来重新问。

### 6. 写入覆盖表

按下面的形状写当前宿主的配置表。整个文件覆盖写入，保证重跑幂等。

```markdown
# pstack model configuration

Per-role model overrides for pstack skills. Each pstack SKILL.md names its defaults in a Models section; the values here override those defaults. Delete a line to fall back to the skill default. A value of `inherit-parent` or `auto` runs that role on the parent session's model (the `Agent` call omits `model`); an alias entry in a panel list still counts toward that panel's fan-out. A model may carry a reasoning effort, as in `opus @xhigh` (levels: low, medium, high, xhigh, max); the role's subagent then runs at that level, each entry of a panel list on its own. `default effort` sets the level for a value without one; `session` uses the runtime's platform mapping to start from the parent session's effort. On Codex this requires active-turn metadata or an explicit effort choice. `session hook: off` stops the supported runtime's pstack routing hook from injecting the poteto-mode mandate; any other value, or no line, leaves it on.

feature, refactoring: sonnet
bug-fix: opus
perf-issue: opus
hillclimb: opus
judgment and prose: opus
strongest judgment: fable
how explorer: opus
how explainer: opus
why investigators: opus
why synthesizer: opus
reflect tooling: opus
reflect judgment, divergent, synthesizer: opus
arena runners: opus, fable, sonnet, haiku
arena cross-judge pool: opus, fable, sonnet, haiku
swarm workers: opus
architect runners: opus, fable, sonnet, haiku
interrogate reviewers: opus, fable, sonnet, haiku
thermos reviewers: opus
no-comments reviewer: opus

default effort: session
session hook: on
```

### 7. 接入

在 Claude Code 上，若 `<config>/CLAUDE.md` 尚未 include `<config>/pstack-models.md`，追加一行 `@` 指向配置表解析后的路径，如 `@~/.claude/pstack-models.md`，让模型行在每个会话加载。用户偏好项目级时，把 include 加进项目的 `CLAUDE.md`。

在 Codex 上，把模型行和 `default effort` 行粘贴进 `<codex-home>/AGENTS.md`；Codex 没有 `@` include。不要把 `session hook` 行粘进去：插件 hook 直接从 `<codex-home>/pstack-models.md` 读它。

在 Muse 上，无需 include 行：插件 hook 直接读配置表并在会话开始注入其角色行。它在用户批准插件 hook 之后才运行，所以 hook 还没跑过时要提 `muse plugins approve pstack`。

### 8. 确认

告诉用户覆盖写到了哪里、模型行如何加载、插件 hook 是否开启。重跑本技能会更新覆盖表。

### 9. 提议一个验证技能（可选）

检查项目是否已有驱动真实应用取证的途径（项目级 `verify` 或 `verify-*` 技能，或既有 harness）。没有则提议一次：「要不要一个项目级验证技能，让代理像用户一样驱动应用并证明变更有效？我可以用 /create-verification-skill 生成一个。」同意则调用 [`/create-verification-skill`](../create-verification-skill/SKILL.md)。拒绝则不再推销，继续。

### 10. 提议一个形式化验证技能（可选）

检查项目是否已有形式化验证技能（跑模型检查器、证明或其他 verifier 的项目技能）。没有则提议一次：「要不要一个形式化验证技能，让代理能证明你代码的关键性质在范围内每一种情况下都成立，而不只是测试覆盖到的那些？我可以用 /create-formal-verification-skill 生成一个。」同意则调用 [`/create-formal-verification-skill`](../create-formal-verification-skill/SKILL.md)。拒绝则不再推销，继续。

## 其他宿主

角色行处处相同。不同的是配置表路径、宿主如何加载它、以及你如何列出模型。用宿主自己的工具检测模型，绝不写入一个你没见过被列出的 slug。子代理调用没有模型参数的宿主也照样得到配置表，作为用户选择的记录，并在它能应用之处应用。`session hook` 行适用于 Claude Code、Codex、GitHub Copilot、Muse、MiniMax Code、Antigravity、OMP 和 OpenCode 2 插件，以及 pstack Pi 扩展。

| 宿主 | 配置表 | 加载 | 列出模型 | 状态 |
| --- | --- | --- | --- | --- |
| Claude Code | `<config>/pstack-models.md` | `<config>/CLAUDE.md` 里的 `@<config>/pstack-models.md` | `Agent` 工具的 model 参数 | 实测验证 |
| Codex | `<codex-home>/pstack-models.md` | 模型行：粘贴进 `<codex-home>/AGENTS.md`；hook 设置：由插件读取 | 你配置的 Codex 模型，见 [codex-tools.md](../poteto-mode/references/codex-tools.md#model-names) | hook 契约已测试；发现已验证 |
| Pi | Pi agent 目录里的 `pstack-models.md`，即 `$PI_CODING_AGENT_DIR` 或 `~/.pi/agent` | 由 pstack Pi 扩展读取，模型行和 hook 设置都读；无 include 行 | `pi --list-models`，见 [pi-tools.md](../poteto-mode/references/pi-tools.md#model-names) 及其 `setup-pstack` 备注 | 扩展契约离线已测试；实测结果见仓库的 `docs/pi-equivalence.md` |
| GitHub Copilot（CLI 与应用） | `${COPILOT_HOME:-~/.copilot}/pstack-models.md` | 插件 hook 检查它并在会话开始注入角色行；仅装技能的安装用 `view` 读它 | `task` 工具的 `model` 枚举，见 [copilot-tools.md](../poteto-mode/references/copilot-tools.md#model-names) | hook 契约已测试；CLI 安装已冒烟测试 |
| Muse | `${XDG_CONFIG_HOME:-~/.config}/muse/pstack-models.md` | 插件 hook 读它并在会话开始注入角色行（hook 获批后）；无 include 行 | 模型目录（`muse model-profile show <model>` 列出每一个），见 [muse-tools.md](../poteto-mode/references/muse-tools.md#model-names) | hook 契约已测试；插件安装已验证 |
| MiniMax Code | `~/.minimax/pstack-models.md`，即使 `MINIMAX_DATA_DIR` 移动了 MiniMax 的数据目录也如此，因为 MiniMax Code 对 hook 和它的 `bash` 工具隐瞒该变量 | 模型行：角色模型技能之前由 agent 读取，或粘贴进 MiniMax Code 数据目录的 `AGENTS.md`；hook 设置：由插件读取 | `mcode provider list` 或 `model` 斜杠命令，见 [minimax-tools.md](../poteto-mode/references/minimax-tools.md#model-names) | hook 契约已测试；插件加载在 0.7.4 上冒烟测试通过；无实测会话 |
| Kimi Code CLI | `<KIMI_CODE_HOME>/pstack-models.md`，未设置则为 `~/.kimi-code/pstack-models.md` | 角色模型技能之前由 agent 读取；无 hook 设置 | 配置了子代理模型池时的 `Agent` 工具 model 参数，见 [kimi-tools.md](../poteto-mode/references/kimi-tools.md#model-names) | 安装与合成 provider 的上下文投递在 macOS Kimi 2.4.1 上核查过；模型合规未测试 |
| Antigravity (`agy`) | `~/.gemini/config/pstack-models.md` | 模型行：角色模型技能之前由 agent 读取，或粘贴进 `~/.gemini/config/AGENTS.md`；hook 设置：由插件的 `SessionStart` hook 读取 | `invoke_subagent` 的 `Model` 枚举（`inherit`、`flash_lite`、`flash`、`pro`），见 [agy-tools.md](../poteto-mode/references/agy-tools.md#model-names) | 在 macOS 上用 `agy` 1.5.0 测试：插件安装、hook 开关、完整技能读取和一次实测子代理回复；Windows 未测试 |
| OMP | `~/.omp/pstack-models.md`（跨 profile 全局；仅 hook） | 由 OMP 插件读取用于路由 | `omp models --kind chat`；模型角色使用 OMP 配置，见 [omp-tools.md](../poteto-mode/references/omp-tools.md#model-names) | 在 OMP 18.16.0 上用合成 provider 核查了安装、技能访问和路由开关；模型合规未测试 |
| Grok Build | `${GROK_HOME:-~/.grok}/pstack-models.md` | 角色模型技能之前由 agent 读取；`session hook` 行不控制 Grok 路由提示 | 会话模型选择器；见 [grok.md](../poteto-mode/references/grok.md#model-names) | 合成 provider 的插件与技能加载已测试 |
| OpenCode 2 | `${XDG_CONFIG_HOME:-~/.config}/opencode/pstack-models.md` | 把路径加进 `opencode.jsonc` 的 `instructions` 数组；插件直接读 hook 设置 | 会话里的 `models` 命令；见 [opencode-tools.md](../poteto-mode/references/opencode-tools.md#model-names) | 在 2.2.5 上用回环 provider 测试了原生技能激活与路由 |
| Gemini CLI | `~/.gemini/pstack-models.md` | `~/.gemini/GEMINI.md` 里的 `@~/.gemini/pstack-models.md` | 会话里的 `model` 斜杠命令 | 来自已发布文档，无实测会话 |
| Prime Agent | 无文档化的配置表路径；模型由 Prime 的配置决定 | | | 无实测会话 |

## Models（模型）

从 `plugins/pstack/models.json` 盖章生成（在那里改，重跑 `tools/generate.mjs`）。

- 可用 Claude 模型：`opus`、`fable`、`sonnet`、`haiku`
- 默认面板：`opus`、`fable`、`sonnet`、`haiku`
- 推理强度级别：`low`、`medium`、`high`、`xhigh`、`max`
- 默认推理强度：`session`
- 单角色默认值：`opus`
