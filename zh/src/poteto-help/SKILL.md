---
name: poteto-help
description: 引导用户完成 pstack 配置、/poteto-mode，以及为任务挑选技能、playbook 或原则。带着问题输入 /poteto-help。
---

# Poteto help

回答用户关于 pstack 的问题，递给他一条可以直接发送的提示词，并附上答案出处的文件链接。对求助类问题，不要动手做活。用户问的是「怎么做」，而一次 pstack 运行要花真金白银的 token，所以把提示词留给他自己发。

要求干活的消息（比如「用 pstack 修这个 bug」）不是求助问题。读 [`poteto-mode`](../poteto-mode/SKILL.md)，在它之下完成工作。

本文件把问题映射到拥有答案的已安装技能、playbook 和平台映射。回答前先读对应的来源。那些来源的指示优先于本映射和任何上游指南——上游指南描述的是 Cursor，与这个移植版可能不同。本地链接指向已安装插件内部，所以给用户的是文件的公开副本：`https://github.com/michael-denyer/pstack-claude/blob/main/plugins/pstack/` 加上相对插件根目录的路径。

## 搞清他要什么

从消息和对话推断需求。点名了具体情境的（比如「哪个技能审查 PR？」）直接跳到对应章节。仍不清楚就问一道选择题，选项如下，然后只回答他选的那节：

- 完成配置
- 用 `/poteto-mode` 开始一个任务
- 为一个情境挑技能
- 修一次跑坏的运行
- 把 pstack 变成自己的

核查会改变答案的状态，只在确实改变时才提：

- 模型或路由问题：先确认运行时和安装类型，再读 [`setup-pstack`](../setup-pstack/references/runtimes.md) 拿覆盖表位置和该运行时的加载方式。说默认值还是覆盖值生效之前，先核查配置。
- 没有项目 `verify` 或 `verify-*` 技能或其他应用 harness，意味着 agent 没有脚本化的方式驱动应用。问题涉及证明改动有效时，提 `/create-verification-skill`。
- 项目没有形式化验证技能，意味着测试触达之外没有任何性质被检查。问题涉及竞态、不变量或其他测试很少覆盖的情形时，提 `/create-formal-verification-skill`。已有形式化验证技能、且它覆盖的代码在它记录的最近同步提交之后变过时，问题涉及那部分代码就提 `/maintain-formal-verification-skill`。

模型覆盖表缺失且这件事要紧时，问用户是否现在就为每个角色挑模型和默认力度。要紧的情形：用户是新手、问题是配置或成本相关、或答案取决于哪些模型在跑。每次聊天至多问一次。需求本身也不清楚时，两个问题合并着问。给两个选择：

- 现在：给他 `/setup-pstack` 让他输入，同时照常回答他的问题。
- 以后：照常回答，并加一句说明每个角色保持默认模型，直到他运行 `/setup-pstack`。

## 完成配置

1. 确认用户的运行时，以及他要原生插件/包安装还是仅技能安装。读 [README](https://github.com/michael-denyer/pstack-claude/blob/main/README.md#install) 或[共享安装参考](https://github.com/michael-denyer/pstack-claude/blob/main/docs/reference.md#shared-skills-installation) 的对应章节，然后给出匹配的安装命令。
2. 解释模型选择、力度、覆盖表加载或自动路由之前，先读 [`/setup-pstack`](../setup-pstack/SKILL.md)，包括它的[其他运行时](../setup-pstack/references/runtimes.md)表格。对自带路由 hook 或扩展的运行时，用它在当前运行时覆盖表里的持久 `session hook: off` 设置关闭路由。写完模型表之后，它会各提议一次为项目生成验证技能和形式化验证技能，除非项目已有。
3. 按 [`references/prompting.md`](references/prompting.md)，给一条带目标和成败判据的首任务提示词。调用语法用[斜杠命令参考](https://github.com/michael-denyer/pstack-claude/blob/main/docs/reference.md#slash-commands)里当前运行时的写法。

给出运行时专属的指令或改造配方之前，适用时先读 [Codex 映射](../poteto-mode/references/codex-tools.md)或 [Pi 映射](../poteto-mode/references/pi-tools.md)。它们的路由章节覆盖 hook 信任、扩展加载和仅技能安装。其他运行时用[运行时支持参考](https://github.com/michael-denyer/pstack-claude/blob/main/docs/reference.md#runtime-support)。

用户担心成本时，讲清 token 花在哪、怎么少花。pstack 的额外开销在子代理和评审面板。重跑 `/setup-pstack`，选更低的力度或更便宜的模型。角色设为 `auto` 或 `inherit-parent` 时跑在聊天的模型上，聊天本身用便宜模型时这更省。面板列表越短，子代理越少——每个条目一个。把 `/poteto-mode` 留给需要严谨的工作。

## 用 `/poteto-mode` 开始任务

`/poteto-mode` 把任务匹配到一个 playbook，把 playbook 的步骤复制进 todo 列表，并在步骤需要时调用其他技能。一条好提示词写明目标和完成判据。不需要列技能——手写的步骤序列往往漏掉或打乱 playbook 本会保住的顺序。帮用户措辞前先读 [`references/prompting.md`](references/prompting.md)。

后续任务是否自动路由，用[完成配置](#完成配置)下的配置与运行时来源判断。承诺自动路由之前先核查本次安装确实开启。没开自动路由时，每个新任务都要显式调用 `poteto-mode`。聊天中途说「new task」会让模式重新匹配一个新的 playbook。子代理默认值读 [poteto-mode 的 Subagents 章节](../poteto-mode/SKILL.md#subagents)和当前运行时的映射。

## 挑技能

默认答案是 `/poteto-mode`，它在步骤需要时运行其余大多数技能。用户想要比 playbook 更多或更少的东西时，直接点名技能。推荐之前先读那个技能，并给一条示例提示词。

| 用户想要 | 技能 |
|---|---|
| 用严谨的方式做任何非平凡任务 | [`/poteto-mode`](../poteto-mode/SKILL.md) |
| 在 agent 开工前确认它理解了目标和问题 | [`/in-your-own-words`](../in-your-own-words/SKILL.md) |
| 发送前把提示词改得更深而不是更大：顶尖高手会补什么、最原始的素材和方法、外加一道外部核验。返回提示词本身，不执行任务 | [`/sharpen`](../sharpen/SKILL.md) |
| 了解代码现在怎么工作，或新代码该放哪 | [`/how`](../how/SKILL.md) |
| 了解代码为什么长这样，或一个数字从哪来 | [`/why`](../why/SKILL.md) |
| 平实地理解一次变更或一个子系统 | [`/teach`](../teach/SKILL.md) |
| 回顾自己近期在某个主题上的工作 | [`/recall`](../recall/SKILL.md) |
| 补上自上一条消息以来这次聊天里的变化，用大白话和少量配图，每条等拍板的事项都列出、只凭回复就能决定 | [`/ketchup`](../ketchup/SKILL.md) |
| 像 `/ketchup` 一样补课，但是一段带字幕的幻灯片短视频，待决事项以文字放在视频下方 | [`/ketchup-video`](../ketchup-video/SKILL.md) |
| 了解一个小 diff 可能波及自身之外什么 | [`/blast-radius`](../blast-radius/SKILL.md) |
| 在跨越函数边界的代码之前定下类型和模块形状 | [`/architect`](../architect/SKILL.md) |
| 对同一份任务书拿多个尝试，合并出最好的一个 | [`/arena`](../arena/SKILL.md) |
| 对切片并行检查，或让 worker 竞速 | [`/swarm`](../swarm/SKILL.md) |
| 让不同模型评审一个 diff 并设法击穿它 | [`/interrogate`](../interrogate/SKILL.md) |
| 存在廉价本地测试时以测试先行的方式修 bug | [`/tdd`](../tdd/SKILL.md) |
| 对 `.ts` 或 `.tsx` 工作应用 TypeScript 规则 | [`/typescript-best-practices`](../typescript-best-practices/SKILL.md) |
| 评审前清理注释，用的评审者不是写注释的人 | [`/no-comments`](../no-comments/SKILL.md) |
| 清除散文里的 AI 腔 | [`/unslop`](../unslop/SKILL.md) |
| 按标准写文档、RFC、README、PR 描述或提交信息 | [`/technical-writing`](../technical-writing/SKILL.md) |
| 用大白话把上一条回复再讲一遍 | [`/bro`](../bro/SKILL.md) |
| 给 agent 一套脚本化驱动应用、证明行为的方法 | [`/create-verification-skill`](../create-verification-skill/SKILL.md) |
| 把验证技能和功能地图重新对齐到应用 | [`/maintain-verification-skill`](../maintain-verification-skill/SKILL.md) |
| 形式化验证竞态、不变量或其他测试很少触达的性质 | [`/create-formal-verification-skill`](../create-formal-verification-skill/SKILL.md) |
| 覆盖的代码变了之后把形式化验证重新对齐，并判断失败是漂移还是 bug | [`/maintain-formal-verification-skill`](../maintain-formal-verification-skill/SKILL.md) |
| 把用户看到的界面行为展示成由 TLA+ 模型核查的图表，并给出到达每种违规状态的最短路径 | [`/statechart`](../statechart/SKILL.md) |
| 在报告或依据某个性能数字行动之前先审查它 | [`/benchmark-checklist`](../benchmark-checklist/SKILL.md) |
| 跑一次大型或横切的变更，或离开一阵后接手待审的工作 | [`/figure-it-out`](../figure-it-out/SKILL.md) |
| 运行期间保留决策日志，事后复盘 | [`/show-me-your-work`](../show-me-your-work/SKILL.md) |
| 为每个角色挑模型和默认力度 | [`/setup-pstack`](../setup-pstack/SKILL.md) |
| 把用户自己的工作习惯变成个人模式技能 | [`/automate-me`](../automate-me/SKILL.md) |
| 把一次完成任务带来的教训变成技能修改 | [`/reflect`](../reflect/SKILL.md) |
| 阻止 agent 在这个仓库里重复同样的错误 | [`/correct`](../correct/SKILL.md) |
| 在 pstack 里找到方向 | `/poteto-help` |

本目录旁边的某个技能目录不在表里时，读它的 frontmatter，按 description 路由。`principle-*` 目录见下文的「原则」。

近似情况：

- `/how` 讲代码做什么。`/why` 讲原因。`/teach` 运行其中一个或两者，并把结果讲得平实。
- `/arena` 给每个 worker 同一份任务书，合并最好的部分。`/swarm` 把工作切成切片或竞速，返回一份报告。
- `/interrogate` 审查 diff 本身。`/blast-radius` 找 diff 之外的破坏面，并证明让变更成立的那一个关键事实。
- `/recall` 跨近期对话重建上下文。`/ketchup` 只覆盖本次聊天自用户上一条消息以来的变化。恢复某一次具体的对话或分支是 Session pickup playbook。
- `/figure-it-out` 设计一次严谨的运行。Autonomous run playbook 把一个任务驱动到完成判据。

不在 pstack 里：

- Cursor 的驱动技能没有移植。poteto-mode 的 Non-negotiables 中的驱动策略点名了 Claude Code 的等价物：`run` 技能和项目 `verify` 技能。
- `/loop` 是 Claude Code 自带技能，**plugin-dev:skill-development** 技能是 Claude Code 的技能编写指南。
- pstack 没有 orchestrate 技能。斜杠菜单里出现 orchestrate 命令，是别的插件提供的。

## Playbook 和原则

playbook 是 `/poteto-mode` 内部的步骤清单，不是技能，所以没有斜杠命令。在 `/poteto-mode` 里，描述任务就会选中一个，这些短语直接点名：

- 「babysit this pr」或「check on pr 123」跑 Babysit。它把 PR 推到可合并状态就停。除非用户要求 merge、land 或 ship，否则不合并。
- 「land the stack」跑 Shipping。
- 「take over this branch」跑 Session pickup。
- 「pause safely」跑 Pause safely。
- 「full autopilot on this queue」跑 [Autopilot-full](../poteto-mode/playbooks/autopilot-full.md)。「stack them, don't ship」跑 [Autopilot-stack](../poteto-mode/playbooks/autopilot-stack.md)。解释无人值守会跑什么之前，先读所选 playbook 的合并规则。
- 「run the eval playbook」跑 Eval。

没有 `/poteto-mode` 时，像「babysit this pr」这样的短语可能启动 pstack 的独立 [`/babysit`](../babysit/SKILL.md) 技能。[Playbooks 章节](../poteto-mode/SKILL.md#playbooks)列出全部 playbook 及适用时机。这个移植版的 PR 工作流读 [Babysit](../poteto-mode/playbooks/babysit.md) 或 [Shipping](../poteto-mode/playbooks/shipping.md)。

pstack 没有规划技能。Claude Code 的 plan mode 可以与它并行使用。跨阶段或跨堆叠 PR 的工作，让 `/poteto-mode` 出计划会跑 [Multi-phase plan playbook](../poteto-mode/playbooks/multi-phase-plan.md)，它只写计划不实现。设计问题先由 Prototype playbook 或 `/architect` 用代码定下来。

原则是单条规则的技能，`/poteto-mode` 会读取并在回复里引用。用户很少直接调用，而是用名字来引导，比如「apply prove it works. show me the real output.」在 Claude Code 上 `principle-*` 叶子隐藏在斜杠菜单之外，`/poteto-mode` 按路径读取；其他运行时可能列在技能选择器里。[Principles 索引](../poteto-mode/SKILL.md#principles)列出全部。

## 修一次跑坏的运行

| 症状 | 修法 |
|---|---|
| 模式跑了几轮后不再生效 | 通过「完成配置」下的来源核查当前运行时的路由配置。没开自动路由时，每个任务显式调用 `poteto-mode`。 |
| 一个问题被当成了上个任务的下一步 | 说「new task」，或说明这一轮不需要模式。 |
| 新选的模型没生效 | 读 [setup-pstack](../setup-pstack/references/runtimes.md) 和当前运行时的映射，再核查它的表位置和加载方式。 |
| 运行比预期的贵 | 看「完成配置」下的成本段落。 |
| 一个技能没有自动加载 | 读它的 description 和当前运行时的技能加载说明。需要时显式调用；`/poteto-mode` 不会跑每一个技能。 |
| 并行 agent 互相覆盖 | 给每个 agent 自己的工作树。 |
| 一夜的运行有动静但什么都没完成 | 读 [Autonomous run](../poteto-mode/playbooks/autonomous-run.md) 和当前运行时的唤醒机制。队列场景读上面选定的 Autopilot playbook。给运行一个能过能不过的判据。 |
| 回复拿绿色构建当成功 | 让它拿出真实的命令、流程、存储的值或 profile。这就是 prove-it-works 原则。 |

对跑偏的运行，[`references/prompting.md`](references/prompting.md) 有一行式的纠偏话术，[`references/recipes.md`](references/recipes.md) 有可改造的提示词。

## 把 pstack 变成自己的

- [`/automate-me`](../automate-me/SKILL.md) 从用户自己的历史起草一个个人模式技能，与 `/poteto-mode` 并用。
- 会话之后跑 [`/reflect`](../reflect/SKILL.md)，把教训变成用户批准的技能修改。
- `/poteto-mode write a skill for <workflow>` 跑 authoring playbook。eval playbook 对技能改动做盲测。
- 行为不端的技能在它自己的 PR 里修，不要混进出问题的那次功能工作。

## 回复

答案先行。代码块里给至多一条示例提示词，合适时从 [`references/recipes.md`](references/recipes.md) 改造，然后附上对应文件的链接。保持简短，除非用户要整张地图。
