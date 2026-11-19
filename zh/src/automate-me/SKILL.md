---
name: automate-me
description: "用于 \"automate me\"、\"create/update/refresh my -mode skill\"、\"turn/capture my preferences or working style into a skill\"，或想让代理照着用户的工作方式干活时。通过 plugin-dev:skill-development + unslop 起草或修订个人 -mode 技能，可选地从最近的会话记录里挖掘新鲜证据。"
---

# Automate me

在 Codex 上，遵循本技能前先读[平台映射](../poteto-mode/references/codex-tools.md)，包括其中按技能给出的说明。

在 GitHub Copilot 上，遵循本技能前先读[平台映射](../poteto-mode/references/copilot-tools.md)，包括其中按技能给出的说明。

在 Muse 上，遵循本技能前先读[平台映射](../poteto-mode/references/muse-tools.md)，包括其中按技能给出的说明。

在 Antigravity 上，遵循本技能前先读[平台映射](../poteto-mode/references/agy-tools.md)，包括其中按技能给出的说明。

这是一条引导式流程，把用户的工作习惯变成代理会遵循的技能。产出是一个为该用户量身定制的 `-mode` 技能（如 `jay-mode`、`priya-mode`）。

本技能编排另外三个技能：一次内联挖掘（见步骤 1）、**plugin-dev:skill-development** 技能（写技能）和 **unslop** 技能（文字纪律）。它只负责排序，不替代它们。

## Flow

### 0. Check for an existing skill

递归查找 `.claude/skills/**/*-mode/SKILL.md` 和 `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/*-mode/SKILL.md`，匹配用户的 handle。Mode 技能可以放在个人类目目录（`.claude/skills/<handle>/`），不一定在顶层。如果已存在一个，用 `AskUserQuestion` 确认意图（除非用户已经说了 "update my skill" 之类的话）：

- 更新现有技能（重复运行时的默认选项）
- 从零重写（少见，动手前先问为什么）

Update 模式会改变后续流程：
- 步骤 1 只挖掘该技能上次编辑之后的历史（`git log -1 --format=%cI <path>`）。
- 步骤 2 问的是改了什么、缺了什么，而不是从零开始采集。
- 步骤 4 直接在现有文件上编辑。用户没有推翻过的章节原样保留；有新证据的章节才修订；只有真正的新规则才新增章节。

### 1. Mine their history

先定位当前工作区的会话记录，再分发任务。Claude Code 把它们存放在 `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/<encoded-cwd>/*.jsonl`。运行 `node <plugin>/skills/reflect/scripts/claude-project-dir.mjs` 来打印本次会话的目录，不要手拼 `<encoded-cwd>`。只用这个路径。不要跨 `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/` 做 glob——那会跨越工作区边界，读到无关项目里的私人聊天。

在这个范围内调查近期的代理对话，找反复出现的模式。把历史切片，并行跑多个子代理（比如最近 2-4 周切成 3 片，保证每片素材够用）。每个子代理的推理强度按活儿来定，依据 **poteto-mode** 技能的 Subagents 一节。每个切片挖掘子代理从父级提供的工作区范围内的路径读取会话记录，寻找下面的信号，并返回一份简短的结构化模式清单，附证据指针。值得挖掘的默认信号：

- 回复偏好（长度、语气、格式、"讲简单点"之类的纠正）
- 委派习惯（子代理、模型、专门工作流、并行度）
- 验证姿态（"完成"意味着什么、单元测试还是实际复现、用不用 reviewer）
- 代码和文字纪律（风格、引用的原则、lint/格式化工具）
- 流程惯例（工作树、提交、PR、评审/合并工具）
- 元偏好（任务中途修技能、主动提新技能）

提升某个信号前先跨切片交叉核对。两个以上切片都出现的模式是高置信度的。孤例信号很弱，通常直接丢弃。

### 2. Ask the user directly

挖掘会漏掉还没显形过的意图。用 `AskUserQuestion` 工具（结构化多选），别让用户从零打字。

形式：一到两个问题，每个 4-6 个选项，类目问题用 `allow_multiple: true`。先问宽的（"哪些方面最重要？"），再就选中的方面用具体选项追问。结构化轮次结束后，再问一个自由聊天式问题，兜住选项漏掉的东西。

别一次甩 20 个问题。

### 3. Cluster findings

把汇总的信号分组进章节。常见的组（只挂用得上的）：

- **Response style**：长度、语气、格式。
- **Autonomy**：不问就做多少事、MCP 工具使用。
- **Understand first**：界定范围或调查改动时用哪些技能。
- **Subagents**：默认用法、并行度、模型配任务、专门工作流。
- **Prose / code discipline**：原则、lint 工具、风格指南。
- **Review and verify**：复现姿态、验证技能、实测工具。
- **Process**：git 工作树、提交、PR、评审/合并工具。
- **Skills**：写技能的习惯、先修技能、提新技能。

**poteto-mode** 技能展示了这个形状。读它来把握粒度，但不要抄内容。用户的规则不等于 poteto-mode 的规则。

### 4. Draft the skill

用 **plugin-dev:skill-development** 技能来写。放置位置：

- 路径：已存在的 mode 技能保留其类目。新建 mode 时，若仓库已为该 handle 建立了个人类目，用 `.claude/skills/<handle>/<handle>-mode/SKILL.md`；否则默认放在项目的 `.claude/skills/<handle>-mode/SKILL.md`（用户偏好个人技能的话放 `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/<handle>-mode/`）。
- Handle：用户的名字或自选标识。
- Frontmatter `description`：触发条件是用户名字 + `/<handle>-mode` + "work in their style"，不要写 "write code"、"review PR" 这类泛化关键词。
- Frontmatter 格式：遵循 `plugin-dev:skill-development` 的 YAML 规则。`description` 保持单个 YAML 标量。标点或换行需要时，加引号或用 `description: >-` 加缩进续行。
- Frontmatter `disable-model-invocation: true` 为默认。只有用户明确想让 mode 在每一轮都生效时才去掉。

### 5. Iterate on prose

对每一行都套用 **unslop** 技能和 `plugin-dev:skill-development` 的写作准则。

把草稿给用户看，收反馈。预期多轮迭代。砍要狠。mode 技能不是手册。

### 6. Land it

在 main 之外的工作树里干活。提交并开 PR，不要直接推 main。

## Guardrails

- **不要对单次对话过拟合。** 说过一次又被另一次推翻的偏好是噪音。先攒到多个实例再成文。
- **不要耍聪明。** 给代理读者复述其他技能的内容、编造比喻、写"诗意"文字，全是零收益的成本。保持可操作性。
- **引用，不要内联。** 用户依赖的其他技能以路径引用出现，不要贴摘录。用户在别处维护的原则文档同理。
- **章节保持最少。** 只有当用户在某方面有具体的、非默认的规则时才加一节。"Communicate clearly" 不算一节；"Short paragraphs. Tables when comparing options. Bullets only when items are genuinely parallel." 算。
- **命名保持通用。** 祈使句里用 "the user" 或 "the human"，不要写作者的名字。
- **不要强求对称。** 用户没有值得写下的流程规则，就整个跳过 Process 一节。

## Evaluation

`-mode` 技能是主观产出。`plugin-dev:skill-development` 式的 test/iterate 基准循环在这里没用。和用户一起感受一下：读起来像不像本人？漏了什么？然后交付。

只有当触发准确度在实践中真的成了问题时，才跑描述优化循环。

## When not to use

- 用户要的是任务专用技能（不是工作习惯）：单独用 `plugin-dev:skill-development`，不需要挖掘。
- 用户想记录的是一条窄工作流（如"我怎么写 commit message"）。那是普通技能，不是 mode 技能。
