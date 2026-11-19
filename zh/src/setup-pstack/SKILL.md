---
name: setup-pstack
description: 配置 pstack 每个角色使用哪个模型。检测可用模型并写入当前运行时的覆盖表。用于 /setup-pstack、「配置 pstack 模型」、修改 pstack 的模型选择，或开关 SessionStart hook。
---

# Setup pstack

在 Codex 上，先阅读[平台映射](../poteto-mode/references/codex-tools.md)（包括其中的各技能说明），再执行本技能。

在 GitHub Copilot 上，先阅读[平台映射](../poteto-mode/references/copilot-tools.md)（包括其中的各技能说明），再执行本技能。

在 Muse 上，先阅读[平台映射](../poteto-mode/references/muse-tools.md)（包括其中的各技能说明），再执行本技能。

在 Antigravity 上，先阅读[平台映射](../poteto-mode/references/agy-tools.md)（包括其中的各技能说明），再执行本技能。

写入当前运行时的按角色模型覆盖表。每个 pstack 技能都在正文里写明默认模型；覆盖表把这些默认值适配到你实际可用的模型。

在任何非 Claude Code 的运行时上，先读[其他运行时](references/runtimes.md)。它的表格给出覆盖表路径、加载方式和列出模型的方法，你那个运行时的章节说明哪些步骤不同。本文件其余部分描述 Claude Code。

在 Claude Code 上，配置目录是 `$CLAUDE_CONFIG_DIR`（设置时）或 `~/.claude`（否则）。本技能称它 `<config>`，用户覆盖表是 `<config>/pstack-models.md`。项目覆盖表是仓库根目录的 `.claude/pstack-models.md`（`git rev-parse --show-toplevel`；不在仓库内时为 Claude Code 启动所在目录），随仓库提交，并在该项目中取代用户覆盖表。session hook 只要发现它就会读取。模型各行的生效依赖第 6 步在其标题下写入的那一行，所以手写的项目表也需要这行。Claude Code 没有 Cursor `.mdc` 那样自动应用「规则」的机制，所以引入是显式的：用户在 `<config>/CLAUDE.md` 加一行，例如：

```text
@<config>/pstack-models.md
```

其中 `<config>` 写成解析后的路径，这样文件会作为每次会话的上下文加载。项目覆盖表则由仓库根目录 `CLAUDE.md` 里的 `@.claude/pstack-models.md` 加载。

## 步骤

### 1. 检测可用模型

枚举本会话中 `Agent` 工具的 `model` 参数接受的模型名。这是可靠来源。在 Claude Code 上它们是下面 [Models](#models) 列出的家族名，每个运行该家族的当前模型，完整的模型 ID 会被拒绝。默认面板也在那里列出。面板按跨家族多样性挑选。用户想额外提供任何 slug，请其确认或粘贴。绝不写入一个你没有确认过可用的真实 slug。别名 `inherit-parent` 和 `auto` 始终有效，即使不是检测到的 slug。两者都表示该角色运行在父会话的模型上，`Agent` 调用通过省略 `model` 来表达。

### 2. 装载当前状态

在 Claude Code 上，先问要配置用户覆盖表（对所有项目生效），还是项目覆盖表（只对本仓库、任何机器生效）。后续步骤都用选定的表。

默认的角色到模型映射是下面「写入覆盖表」步骤里展示的形状。当前运行时的表已存在时，读它，把其中的值当作当前选择；否则从默认值开始。角色不在这个形状里的行，比如 `how critics`、`architect runners`、`reflect tooling` 或 `why investigators`，来自已退役的角色，删掉。较旧的表可能写着 `claude-` 开头的完整模型 ID，`Agent` 工具不接受；每个都替换成它的家族名，即 `claude-` 后面那个词。

### 3. 映射并确认

展示每个角色及其当前模型，把任何不在检测集合中的真实 slug 标记为需要选择。同时列出第 2 步删除或改写的每一行。问是照单全收还是改某些角色，选项是检测到的模型加 `inherit-parent` 和 `auto`。优先用 `AskUserQuestion` 而不是自由输入。面板角色（arena runners、interrogate reviewers）的值是一个列表，每个条目各跑一个子代理，别名条目也计入，所以列表长度决定数量。`arena cross-judge pool` 也是列表，但 Arena 只跑一个 judge，只尝试与父会话不同家族的值，按列表顺序，所以按偏好排序。`inherit-parent` 或 `auto` 的值不做 judge。`swarm workers` 是每个 worker 的默认模型，除非竞速或对比给每个 arm 指定了别的模型。

然后问默认推理力度，即 `default effort` 行。可以是 `session`（沿用父会话的力度），或 [Models](#models) 里的某个档位。从那里列的默认值起步。所有不带后缀的角色值都按它运行。再问是否有角色要以别的档位运行。角色值可以在 slug 后带一个档位，如 `<slug> @xhigh`；面板条目各带各的，如 `<slug> @xhigh, <slug> @max`。每个档位作为派发的 effort 传入，所以选择不必改动会话就能生效。默认力度不加后缀。

### 4. 选择 session hook 是否路由任务

在 Claude Code 上，插件的 `SessionStart` hook 在启动、恢复、清除和压缩时注入 poteto-mode 强制要求。问是否保留 hook，默认是开。答案就是当前运行时表里的 `session hook` 行：`on` 或 `off`。没有表或没有该行时，hook 注入。该行在没有 pstack 路由 hook 的其他运行时上不起作用。

### 5. 校验

写入的每个真实 slug 必须在检测集合里。`inherit-parent` 和 `auto` 始终通过。校验 slug 时剥掉 `@<level>` 后缀，档位对照 [Models](#models) 的力度档位。`default effort` 的值是这些档位之一或 `session`。选定的真实 slug 或档位不可用时，停下来重新问。

### 6. 写入覆盖表

按下方的形状写当前运行时的表。整个文件覆盖写入，保证重跑幂等。项目表还要在标题下多加一行，让同时装载两张表的会话知道哪张算数：`This project's sheet. In this repository it replaces the user's pstack-models.md; ignore that sheet's lines.`

```markdown
# pstack model configuration

Per-role model overrides for pstack skills. Each pstack SKILL.md names its defaults in a Models section; the values here override those defaults. Delete a line to fall back to the skill default. A value of `inherit-parent` or `auto` runs that role on the parent session's model (the `Agent` call omits `model`); an alias entry in a panel list still counts toward that panel's fan-out. A model may carry a reasoning effort, as in `opus @xhigh` (levels: low, medium, high, xhigh, max); the role's subagent then runs at that level, each entry of a panel list on its own. `default effort` sets the level for a value without one; `session` uses the runtime's platform mapping to start from the parent session's effort. On Codex this requires active-turn metadata or an explicit effort choice. `session hook: off` stops the supported runtime's pstack routing hook from injecting the poteto-mode mandate; any other value, or no line, leaves it on.

feature, refactoring: sonnet
bug-fix: opus
perf-issue: opus
hillclimb: opus
judgment and prose: opus
strongest judgment: fable
arena runners: opus, fable, sonnet, haiku
arena cross-judge pool: opus, fable, sonnet, haiku
swarm workers: opus
interrogate reviewers: opus, fable, sonnet, haiku
thermos reviewers: opus
no-comments reviewer: opus

default effort: session
session hook: on
```

### 7. 接入

在 Claude Code 上，若 `<config>/CLAUDE.md` 尚未包含 `<config>/pstack-models.md`，追加一行 `@` 指向表的解析路径，如 `@~/.claude/pstack-models.md`，让模型各行在每次会话都加载。项目表则改在仓库根目录的 `CLAUDE.md` 追加 `@.claude/pstack-models.md`（如果没有），并提醒用户提交这两个文件。

### 8. 确认

告诉用户覆盖写到了哪里、模型各行如何加载、插件 hook 是否开启。重跑本技能会更新覆盖表。

### 9. 提议验证技能（可选）

检查项目是否有驱动真实应用拿证据的方法（项目 `verify` 或 `verify-*` 技能，或已有的 harness）。没有就提议一次：「想不想要一个项目本地的验证技能，让 agent 能像用户一样驱动应用、证明改动有效？我可以用 /create-verification-skill 生成一个。」同意就调用 [`/create-verification-skill`](../create-verification-skill/SKILL.md)。拒绝就继续，不纠缠。

### 10. 提议形式化验证技能（可选）

检查项目是否已有形式化验证技能（对着代码运行模型检查器、证明器或其他 verifier 的项目技能）。没有就提议一次：「想不想要一个形式化验证技能，让 agent 能证明你代码的某个关键性质在范围内的每种情况下都成立，而不只是测试触达的那些情况？我可以用 /create-formal-verification-skill 生成一个。」同意就调用 [`/create-formal-verification-skill`](../create-formal-verification-skill/SKILL.md)。拒绝就继续，不纠缠。

## Models

由 `plugins/pstack/models.json` 盖章生成（在彼处编辑，重跑 `tools/generate.mjs`）。

- 可用 Claude 模型: `opus`, `fable`, `sonnet`, `haiku`
- 默认面板: `opus`, `fable`, `sonnet`, `haiku`
- 推理力度档位: `low`, `medium`, `high`, `xhigh`, `max`
- 默认推理力度: `session`
- 单角色默认: `opus`
