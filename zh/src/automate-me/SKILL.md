---
name: automate-me
description: "用于「automate me」「创建/更新/刷新我的 -mode 技能」「把我的偏好或工作方式变成一个技能」，或想让代理遵循用户的做法时。通过 plugin-dev:skill-development + unslop 起草或修订一个个人 -mode 技能，可选地从最近的会话记录拉取新鲜证据。"
---

# Automate me

在 Codex 上，先读[平台映射](../poteto-mode/references/codex-tools.md)（包括其中的逐技能说明），再执行本技能。

在 GitHub Copilot 上，先读[平台映射](../poteto-mode/references/copilot-tools.md)（包括其中的逐技能说明），再执行本技能。

在 Muse 上，先读[平台映射](../poteto-mode/references/muse-tools.md)（包括其中的逐技能说明），再执行本技能。

在 Antigravity 上，先读[平台映射](../poteto-mode/references/agy-tools.md)（包括其中的逐技能说明），再执行本技能。

一条引导式流程，把用户的工作约定变成一个代理会遵循的技能。产物是一个为该用户定制的 `-mode` 技能（比如 `jay-mode`、`priya-mode`）。

本技能编排另外三个：一个内联的挖掘环节（见第 1 步）、**plugin-dev:skill-development** 技能（撰写）、和 **unslop** 技能（文字纪律）。它只做排序，不替代它们。

## 流程

### 0. 检查已有技能

递归查找 `.claude/skills/**/*-mode/SKILL.md` 和 `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/*-mode/SKILL.md` 里匹配用户 handle 的。Mode 技能可以放在个人类目目录里（`.claude/skills/<handle>/`），不只在顶层。已有技能的话，用 `AskUserQuestion` 确认意图（除非对方已经说了「更新我的技能」之类）：

- 更新已有技能（重复运行时的默认）
- 从头重做（少见，做之前问为什么）

更新模式改变后续流程：

- 第 1 步只挖掘技能上次编辑之后的历史（`git log -1 --format=%cI <path>`）。
- 第 2 步问的是改了什么、缺了什么，不是从零采集什么。
- 第 4 步就地编辑已有文件。保留用户没有推翻的小节。用新证据修订有小节。只有真正的新规则才加新小节。

### 1. 挖掘他们的历史

扇出之前先定位活跃工作区的会话记录。Claude Code 把它们存在 `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/<encoded-cwd>/*.jsonl`。跑 `node <plugin>/skills/reflect/scripts/claude-project-dir.mjs` 打印本次会话的目录，不要手工拼 `<encoded-cwd>`。只用这个路径。不要跨 `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/` 做 glob。那会跨过工作区边界，读到无关项目的私人聊天。

在这个范围内调查最近的代理对话，找反复出现的模式。在历史切片上跑多个并行子代理（比如最近 2-4 周，切成 3 片让每片材料够用）。按 **poteto-mode** 技能的 Subagents 小节，为工作选择每个子代理的推理强度。每个切片挖掘子代理从父代理提供的工作区范围内的路径读会话记录，找下面的信号，并返回一份带证据指针的简短结构化模式列表。值得寻找的默认信号：

- 响应偏好（长度、语气、格式、「说人话」式纠正）
- 委派习惯（子代理、模型、专用工作流、并行度）
- 验证姿态（「完成」意味着什么、单元测试还是活体复现、评审者）
- 代码与文字纪律（风格、引用的原则、lint/format 工具）
- 流程约定（工作树、commit、PR、评审/合并工具）
- 元偏好（任务中途修技能、提议新技能）

提升一个信号之前跨切片交叉核对。2+ 个切片都看到的模式是高置信度。孤立信号很弱，通常被丢弃。

### 2. 直接问用户

挖掘会漏掉还没出现过的意图。用 `AskUserQuestion` 工具（结构化多选），不要让用户从零打字。

形状：一到两个问题，每个 4-6 个选项，类目问题用 `allow_multiple: true`。先问宽的（「哪些方面最重要？」），再对选中的方面追问具体选项。结构化几轮之后，一个自由聊天问题接住选项漏掉的东西。

不要一次抛 20 个问题。

### 3. 聚类发现

把合并后的信号分组成小节。常见的（只用用得上的）：

- **Response style**：长度、语气、格式。
- **Autonomy**：不问就做多少事、MCP 工具使用。
- **Understand first**：界定或调查一个改动时用哪些技能。
- **Subagents**：默认值、并行度、模型对任务、专用工作流。
- **Prose / code discipline**：原则、lint 工具、风格指南。
- **Review and verify**：复现姿态、验证技能、活体测试工具。
- **Process**：git 工作树、commit、PR、评审/合并工具。
- **Skills**：技能撰写习惯、先修技能、提议新技能。

**poteto-mode** 技能展示了这个形状。读它看粒度。不要抄它的内容。用户的规则和 poteto-mode 的不一样。

### 4. 起草技能

用 **plugin-dev:skill-development** 技能撰写。位置：

- 路径：保留已有 mode 技能的类目。新的 mode，仓库里已有该 handle 的成熟个人类目时用 `.claude/skills/<handle>/<handle>-mode/SKILL.md`。否则默认放项目里的 `.claude/skills/<handle>-mode/SKILL.md`（用户偏好个人技能的话放 `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/<handle>-mode/`）。
- Handle：用户的名或自选标识。
- Frontmatter `description`：按他们的名字 + `/<handle>-mode` + 「按他们的风格工作」触发，不按「写代码」「review PR」这类泛关键词触发。
- Frontmatter 格式：遵循 `plugin-dev:skill-development` 的 YAML 规则。`description` 保持单个 YAML 标量。标点或换行需要时加引号，或用 `description: >-` 带缩进续行。
- Frontmatter 默认 `disable-model-invocation: true`。只有用户明确希望自己的 mode 在每一轮都生效时才关掉。

### 5. 迭代文字

对每一行应用 **unslop** 技能和 `plugin-dev:skill-development` 的写作指南。

把草稿给用户看并收反馈。预期多轮迭代。狠砍。mode 技能不是手册。

### 6. 落地

在 main 之外的工作树上工作。commit 并开 PR。不要直接 push 到 main。

## 护栏

- **不要过拟合到一次对话。** 说了一次又在另一次被推翻的偏好是噪声。定成规则前要求多个实例。
- **不要耍聪明。** 复述其他技能的内容、发明隐喻、给代理读者写「诗意」文字，都是没有收益的成本。保持可操作。
- **引用，不内联。** 用户依赖的其他技能以路径引用出现，不要贴摘录。他们在别处维护的原则文档同理。
- **小节保持最少。** 只在用户有具体的、非默认的规则时才加小节。「沟通清晰」不是一个小节。「段落要短。比较选项时用表格。只有条目真正平行时才用 bullet。」是。
- **命名约定保持通用。** 祈使句里用「用户」或「人」，不用作者的名。
- **不要强求对称。** 用户没有值得写下的流程规则，就整个跳过 Process 小节。

## 评估

`-mode` 技能是主观产物。`plugin-dev:skill-development` 式的测试/迭代 benchmark 闭环在这里没用。和用户一起感受一下：读起来像他吗？漏了什么？然后发布。

只有技能的触发准确率在实践中成了问题时，才跑 description 优化闭环。

## 什么时候不用

- 用户要一个任务专属技能（不是工作约定）：单用 `plugin-dev:skill-development`，不需要挖掘。
- 用户要记录一个窄工作流（比如「我怎么写 commit message」）。那是普通技能，不是 mode 技能。
