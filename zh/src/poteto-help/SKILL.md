---
name: poteto-help
description: 引导用户完成 pstack 安装配置、/poteto-mode，以及为任务挑选合适的技能、playbook（流程清单）或原则。输入 /poteto-help 加一个问题。
---

# Poteto help

回答用户关于 pstack 的问题，递给他一条可以直接发送的提示词，并链接答案来源的文件。help 类问题不要动手做。用户问的是「怎么做」，而一次 pstack 运行要花真金白银的 token，所以把提示词留给他自己发。

要求干活的消息（如「用 pstack 修这个 bug」）不是 help 问题。读 [`poteto-mode`](../poteto-mode/SKILL.md)，在其之下干活。

本文件把问题映射到拥有答案的已安装技能、playbook 和平台映射。回答之前先读匹配的来源。该来源的指示优先于本映射和任何上游指南——上游指南描述的是 Cursor，可能与这个移植版不同。本地链接指向已安装插件内部，所以给用户该文件的公开副本：`https://github.com/michael-denyer/pstack-claude/blob/main/plugins/pstack/` 加上它相对插件根目录的路径。

## 搞清他们要什么

从消息和对话推断需求。点名了场景的（如「哪个技能评审 PR？」）直接跳到对应小节。需求仍不清楚时，问一个带下列选项的选择题，然后只回答他选的那节：

- 完成安装配置
- 用 `/poteto-mode` 开始一个任务
- 为场景挑一个技能
- 修复一次跑坏的运行
- 把 pstack 变成自己的

检查会改变答案的状态，只在相关时提：

- 模型或路由问题：先识别宿主和安装类型，然后读 [`setup-pstack`](../setup-pstack/SKILL.md#other-runtimes) 了解配置表位置和该宿主的加载方式。说清默认还是覆盖生效之前，先核对该配置。
- 没有项目级 `verify` 或 `verify-*` 技能或其他应用 harness，意味着代理没有脚本能驱动应用。当问题关于证明变更有效时，提 `/create-verification-skill`。
- 项目里没有形式化验证技能，意味着性质检查止步于测试覆盖之处。当问题关于竞态、不变量或其他测试很少命中的情形时，提 `/create-formal-verification-skill`。已有其一，且它覆盖的代码在它记录的 last in sync 提交之后改过，问题又涉及那段代码时，提 `/maintain-formal-verification-skill`。

模型配置表缺失且此事要紧时，问用户是否现在就为每个角色挑模型和默认强度。要紧的情形：用户是新手、问题关于安装或成本、或答案取决于哪些模型在跑。每次聊天至多问一次。需求也不清楚时，两个问题一起问。给两个选项：

- 现在：给他 `/setup-pstack` 去输入，同时回答他的问题。
- 稍后：回答他的问题，加一句说明每个角色在他运行 `/setup-pstack` 之前都保持默认模型。

## 完成安装配置

1. 识别用户的宿主，以及他想要原生插件/包还是仅装技能。读它在 [README](https://github.com/michael-denyer/pstack-claude/blob/main/README.md#install) 或[共享安装参考](https://github.com/michael-denyer/pstack-claude/blob/main/docs/reference.md#shared-skills-installation)里的小节，然后给出匹配的安装命令。
2. 在解释模型选择、effort、配置表加载或自动路由之前，先读 [`/setup-pstack`](../setup-pstack/SKILL.md)，包括其「其他宿主」表格。对内置路由 hook 或扩展，用当前宿主配置表里持久的 `session hook: off` 设置关闭路由。在模型配置表之后，它会各提议一次为本项目生成验证技能和形式化验证技能，除非项目已有。
3. 提议一条首个任务提示词：带目标和一个能通过或失败的判据，参照 [`references/prompting.md`](references/prompting.md)。调用语法用[斜杠命令参考](https://github.com/michael-denyer/pstack-claude/blob/main/docs/reference.md#slash-commands)里当前宿主的写法。

给出宿主专属指示或改造配方之前，适用时先读 [Codex 映射](../poteto-mode/references/codex-tools.md)或 [Pi 映射](../poteto-mode/references/pi-tools.md)。它们的路由小节覆盖 hook 信任、扩展加载和仅装技能的安装。其他宿主用[宿主支持参考](https://github.com/michael-denyer/pstack-claude/blob/main/docs/reference.md#runtime-support)。

如果担心成本，讲清 token 花在哪里、怎么少花。pstack 把额外 token 花在子代理和评审面板上。重跑 `/setup-pstack`，选更低的强度或更便宜的模型。角色设为 `auto` 或 `inherit-parent` 时跑在聊天的模型上，聊天跑在更便宜的模型上时就省钱。更短的面板列表跑更少的子代理，一个条目一个。`/poteto-mode` 留给需要严谨的工作。

## 用 `/poteto-mode` 开始一个任务

`/poteto-mode` 把任务匹配到一个 playbook（流程清单），把 playbook 的步骤抄进 todo list，并按步骤需要运行其他技能。被跳过的步骤以 `skip: <reason>` 留在清单里。好的提示词陈述目标以及如何判断完成。它不罗列技能，因为手写的序列容易丢掉或打乱 playbook 会保留的步骤。帮忙措辞前先读 [`references/prompting.md`](references/prompting.md)。

后续任务是否自动路由，用[完成安装配置](#get-set-up)下的安装与宿主来源判断。承诺自动路由之前先确认本次安装已启用。没有自动路由时，每个新任务手动调用 `poteto-mode`。聊天中途说「new task」会让模式匹配一份新 playbook。子代理默认值读 [poteto-mode 的 Subagents 小节](../poteto-mode/SKILL.md#subagents)和当前宿主的映射。

## 挑一个技能

默认答案是 `/poteto-mode`，它在步骤需要时运行其余大多数技能。用户想要比 playbook 给的更多或更少时，直接点名技能。推荐前先读那个技能，并给一个示例提示词。

| 用户想要 | 技能 |
|---|---|
| 严谨地做任何非平凡任务 | [`/poteto-mode`](../poteto-mode/SKILL.md) |
| 在开始前确认代理理解了目标和问题 | [`/in-your-own-words`](../in-your-own-words/SKILL.md) |
| 发送之前让提示词被改写得更深，而不是更大：顶尖从业者会补充什么、他的原料和方法、外加一次外部检查。它返回改写后的提示词，不代做任务 | [`/sharpen`](../sharpen/SKILL.md) |
| 了解代码现在怎么工作，或新代码该放哪 | [`/how`](../how/SKILL.md) |
| 了解代码为什么长这样，或某个数字从哪来 | [`/why`](../why/SKILL.md) |
| 平实易懂地讲清一个变更或子系统 | [`/teach`](../teach/SKILL.md) |
| 追赶自己在某主题上最近的工作 | [`/recall`](../recall/SKILL.md) |
| 追赶这条聊天里自己上一条消息之后的全部变化，平实语言加小图表，列出每一项等待他决定的事且只凭回复就能决定 | [`/ketchup`](../ketchup/SKILL.md) |
| 像 `/ketchup` 那样追赶，但产出是一段带字幕的幻灯片短视频，等待决策的事项以文字列在下面 | [`/ketchup-video`](../ketchup-video/SKILL.md) |
| 知道一个小 diff 可能在它之外弄坏什么 | [`/blast-radius`](../blast-radius/SKILL.md) |
| 在跨越函数边界的代码之前定下类型和模块形状 | [`/architect`](../architect/SKILL.md) |
| 同一份简报跑多个候选，合并成最好的一个 | [`/arena`](../arena/SKILL.md) |
| 对切片并行跑检查，或让 worker 竞速 | [`/swarm`](../swarm/SKILL.md) |
| 让不同模型评审一个 diff 并设法拆掉它 | [`/interrogate`](../interrogate/SKILL.md) |
| 存在便宜的本地测试时测试优先修 bug | [`/tdd`](../tdd/SKILL.md) |
| 对 `.ts` 或 `.tsx` 工作应用 TypeScript 规则 | [`/typescript-best-practices`](../typescript-best-practices/SKILL.md) |
| 评审前清除注释，用一位没写过它们的评审者 | [`/no-comments`](../no-comments/SKILL.md) |
| 清除散文里的 AI 腔 | [`/unslop`](../unslop/SKILL.md) |
| 按标准写文档、RFC、README、PR 描述或提交信息 | [`/technical-writing`](../technical-writing/SKILL.md) |
| 把上一条回复用平实的话再讲一遍 | [`/bro`](../bro/SKILL.md) |
| 给代理一条能驱动应用并证明行为的脚本化途径 | [`/create-verification-skill`](../create-verification-skill/SKILL.md) |
| 让验证技能及其功能地图与应用重新对齐 | [`/maintain-verification-skill`](../maintain-verification-skill/SKILL.md) |
| 形式化验证竞态、不变量或其他测试很少触达的性质 | [`/create-formal-verification-skill`](../create-formal-verification-skill/SKILL.md) |
| 在其覆盖的代码变更后让形式化验证重新对齐，并判断一次失败是漂移还是 bug | [`/maintain-formal-verification-skill`](../maintain-formal-verification-skill/SKILL.md) |
| 向 PM 或设计师展示用户所见，以经 TLA+ 模型核查的图表，并给出到每个违反规则状态的最短路径 | [`/statechart`](../statechart/SKILL.md) |
| 在汇报或使用某个性能数字之前先审它 | [`/benchmark-checklist`](../benchmark-checklist/SKILL.md) |
| 跑一次大型或横切的变更，或离开后回头再审的变更 | [`/figure-it-out`](../figure-it-out/SKILL.md) |
| 运行期间记决策日志，事后复查 | [`/show-me-your-work`](../show-me-your-work/SKILL.md) |
| 为每个角色挑模型和默认强度 | [`/setup-pstack`](../setup-pstack/SKILL.md) |
| 把自己的工作习惯变成一个个人模式技能 | [`/automate-me`](../automate-me/SKILL.md) |
| 把已完成任务的教训变成技能修改 | [`/reflect`](../reflect/SKILL.md) |
| 阻止代理在这个仓库里重复同样的错误 | [`/correct`](../correct/SKILL.md) |
| 在 pstack 里认路 | `/poteto-help` |

旁边的技能目录不在表里时，读它的 frontmatter，按 description 路由。`principle-*` 目录见下方原则部分。

容易混淆的：

- `/how` 解释代码做什么。`/why` 解释为什么。`/teach` 跑其中一个或两个，再把结果讲得平实。
- `/arena` 给每个 worker 同一份简报并合并最好的部分。`/swarm` 把工作切成切片或竞速，返回一份报告。
- `/architect` 定下设计后接着实现。加「with checkpoint」可以在它写代码前先审设计。
- `/interrogate` 评审 diff。`/blast-radius` 找 diff 之外的破坏，并证明那个让变更安全的唯一事实。
- `/recall` 跨最近聊天重建上下文。`/ketchup` 只覆盖这条聊天里用户上一条消息之后的内容。恢复某一条具体聊天或分支是 Session pickup playbook。
- `/figure-it-out` 设计单次严谨运行。Orchestrate playbook 运行跨越数天和许多 PR 的计划。Autonomous run playbook 把一个任务推到完成判据。

pstack 没有：

- Cursor 的 driver 技能没有移植版。poteto-mode 的 Non-negotiables 里的 driver 策略点名了 Claude Code 对应物：`run` 技能和项目 `verify` 技能。
- `/loop` 是 Claude Code 内置技能，**plugin-dev:skill-development** 技能是 Claude Code 的技能编写指南。
- pstack 没有 orchestrate 技能。Orchestrate 是 `/poteto-mode` 的 playbook。斜杠菜单里出现 orchestrate 命令，那是别的插件提供的。

## Playbook 与原则

Playbook 是 `/poteto-mode` 内部的步骤清单，不是技能，所以没有斜杠命令。在 `/poteto-mode` 里，描述任务即被匹配到一个；下面这些短语直接点名：

- "babysit this pr" 或 "check on pr 123" 运行 Babysit。它把 PR 推到 merge-ready 就停。除非用户要求 merge、land 或 ship，否则不合并。
- "land the stack" 运行 Shipping。
- "take over this branch" 运行 Session pickup。
- "pause safely" 运行 Pause safely。
- "full autopilot on this queue" 运行 [Autopilot-full](../poteto-mode/playbooks/autopilot-full.md)。"stack them, don't ship" 运行 [Autopilot-stack](../poteto-mode/playbooks/autopilot-stack.md)。解释哪些会无人值守运行之前，先读所选 playbook 的合并规则。
- "run the eval playbook" 运行 Eval。

没有 `/poteto-mode` 时，"babysit this pr" 这类短语可能启动的是 pstack 独立的 [`/babysit`](../babysit/SKILL.md) 技能。[Playbooks 小节](../poteto-mode/SKILL.md#playbooks)列出每个 playbook 及其适用时机。这个移植版的 PR 工作流读 [Babysit](../poteto-mode/playbooks/babysit.md) 或 [Shipping](../poteto-mode/playbooks/shipping.md)。

pstack 没有 planning 技能。Claude Code 的 plan mode 可以与之并存。跨阶段或堆叠 PR 的工作，向 `/poteto-mode` 要一个 plan 会运行[多阶段计划 playbook](../poteto-mode/playbooks/multi-phase-plan.md)，它写计划但不实现。设计问题，Prototype playbook 或 `/architect` 先在代码里裁决。

原则是单条规则的技能，`/poteto-mode` 会读取并在回复里引用。用户很少直接调用一个。他们用名字来引导，如「apply prove it works. show me the real output.」在 Claude Code 上 `principle-*` 叶子对斜杠菜单隐藏，`/poteto-mode` 按路径读取；其他宿主可能在技能选择器里列出它们。[Principles 索引](../poteto-mode/SKILL.md#principles)列出全部。

## 修复一次跑坏的运行

| 症状 | 修复 |
|---|---|
| 模式几轮之后不再生效 | 通过「完成安装配置」下的来源检查当前宿主的路由配置。没有自动路由时，每个任务手动调用 `poteto-mode`。 |
| 一个提问被当成上个任务的下一步 | 说「new task」，或说明这一轮不需要模式。 |
| 新的模型选择没有生效 | 读 [setup-pstack](../setup-pstack/SKILL.md#other-runtimes) 和当前宿主的映射，再核对其配置表位置与加载方式。 |
| 运行成本超出预期 | 见「完成安装配置」下的成本段落。 |
| 技能没有自己加载 | 读它的 description 和当前宿主的技能加载说明。需要时显式调用；`/poteto-mode` 不运行每个技能。 |
| 并行代理互相覆盖 | 给每个代理自己的工作树。 |
| 通宵运行推进了但什么都没完成 | 读 [Autonomous run](../poteto-mode/playbooks/autonomous-run.md) 和当前宿主的唤醒机制。队列任务读上面所选的 Autopilot playbook。给运行一个能通过或失败的判据。 |
| 回复凭一次绿色构建宣称成功 | 要真实的命令、流程、存储的值或 profile。这就是 prove-it-works 原则。 |

运行跑偏时，[`references/prompting.md`](references/prompting.md) 有一行的纠偏语，[`references/recipes.md`](references/recipes.md) 有可改造的提示词。

## 把 pstack 变成自己的

- [`/automate-me`](../automate-me/SKILL.md) 从用户自己的历史起草一个个人模式技能，与 `/poteto-mode` 并用。
- 会话之后 [`/reflect`](../reflect/SKILL.md) 把教训变成用户批准的技能修改。
- `/poteto-mode write a skill for <workflow>` 运行编写 playbook。评测 playbook 盲测一项技能变更。
- 行为不端的技能在它自己的 PR 里修，不要在出错的那个功能工作里顺手改。

## 回复

答案先行。至多给一个示例提示词，放在代码块里，[`references/recipes.md`](references/recipes.md) 里有合适的就改造它，然后给出该文件的链接。用户没要整张地图就保持简短。
