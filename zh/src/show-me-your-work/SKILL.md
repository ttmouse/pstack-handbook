---
name: show-me-your-work
description: "为长时间运行或无人值守的工作保留一条可审查的决策轨迹：一份 TSV 日志，每个决定一行（做了什么、为什么、证据、结果）。默认留在本地；当审查者需要轨迹才能信任结果时才提交。用于 /show-me-your-work、自主或多阶段运行，或人离开一段时间后要审查的工作。"
---

# Show me your work

在 Codex 上，先阅读[平台映射](../poteto-mode/references/codex-tools.md)（包括其中的各技能说明），再执行本技能。

在 GitHub Copilot 上，先阅读[平台映射](../poteto-mode/references/copilot-tools.md)（包括其中的各技能说明），再执行本技能。

在 Muse 上，先阅读[平台映射](../poteto-mode/references/muse-tools.md)（包括其中的各技能说明），再执行本技能。

在 Antigravity 上，先阅读[平台映射](../poteto-mode/references/agy-tools.md)（包括其中的各技能说明），再执行本技能。

只保留一份正本日志。

## 格式

单个 TSV 文件，每个决定一行。单元格保持单行。证据是指针，不是散文。

复制 `references/decision-log-template.tsv`（表头行）来开一份干净的日志。各列：

- **ts.** ISO8601 时间戳。
- **phase.** 阶段或工作流。
- **decision.** 选了什么或做了什么，一行。
- **why.** 用大白话讲的理由。如果是某个原则驱动的，平实说出来，不要贴术语标签。
- **evidence.** 能证明它的链接或路径：commit SHA、PR 号、`file:line`，或产物、trace、截图的路径。绝不写成一段话。
- **result.** 结果或判定状态：`tests green`、`reverted`、`pixel-diff 0`、`INCONCLUSIVE`、`open`。

一个例子，写得直白，让审查者一眼读完。

```
ts	phase	decision	why	evidence	result
2026-05-24T09:02:00Z	frame	counted the work first, about 100 components and roughly 75 hours	wanted to know the size before starting a long run	commit 3a9f1c2	found 5 things to sort out before starting
2026-05-24T09:40:00Z	harness	took screenshots of the old version before changing anything	so we can compare old against new and catch any visual change	scripts/snapshot.sh, baseline/	saved 120 reference screenshots
2026-05-24T11:15:00Z	widget	moved the widget styles over without changing how it looks	keep the change small and the result identical	commit 7c21e0a, pixel-diff 0	looks identical, tests pass
2026-05-24T12:30:00Z	widget	threw out a helper's work because its screenshots were blank	checked the real files instead of trusting its summary	worktree reset	reverted, tightened the instructions for next time
```

## 记一行

每条都按你向同事汇报的做法写：大白话、具体的动作，不用 AI 腔和抽象术语（**unslop** 技能同样适用于日志文本）。

用助手脚本 `scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>`。它会盖 `ts` 时间戳、首次使用时写表头、清理多余的制表符和换行，并对以 `=`、`+`、`-`、`@` 或 `"` 开头的单元格加单引号前缀。直接 `printf` 追加一行也行，但单元格内容来自生成文本或用户输入时，注意那些同样的字节。

记决策点和检查点，不记每个动作：一个岔路口的选择、一个单元完成及其验证结果、一次转向或回滚及其触发、一个浮出的阻塞、一个修复的闸门。循环运行每轮迭代一行。琐碎和自明的事跳过。

一次运行是一个 agent 对话，包括它的后续轮次和对它的任何摘要。一次拾起、一个接替的 agent、一个新聊天，都开启新的运行。运行往已有行的日志里追加时，它的第一行 phase 为 `start`；在另一次运行的 `start` 行之后，它自己的第一行也是 `start`。所以一次运行在后续轮次回到某份日志时，先读日志的最后几行，确认此后是否有别的运行写过。`start` 行要点名它之前这段 `ts` 范围内、本次运行没有写的那些行，其 evidence 要能指认本次运行，比如它的 agent id。phase `start` 不作他用。

## 日志放哪

默认日志是工作产物，不提交。放在工作目录的 `decisions.tsv`，多个工作并行时放 `.audit/<task-slug>.tsv`，并留在 git 之外。

只有当工作足够重大、审查者需要轨迹才能信任结果时才提交。

## 规则

- 只追加。错误的判断用一行新的去取代它。绝不编辑或删除历史。
- 优先用提交过的脚本产出的证据，而不是手工的一次性产物（**encode-lessons-in-structure** 原则技能）。

## 对照转写审计日志

运行结束、交回之前，检查日志说的是否是真话。在 Claude Code 的每项目转写目录 `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/<encoded-cwd>/` 下读本次运行的转写，`node <plugin>/skills/reflect/scripts/claude-project-dir.mjs` 会打印该目录。不要在 `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/` 下全局 glob——那会读到无关的私人聊天。把本次运行的各行对照实际发生的事逐段走查。每段从本次运行的某个 `start` 行开始（本次运行创建日志时则从第一行开始），到另一个运行的下一条 `start` 行结束：

- 核对每行都对应一个真实的决定或动作。
- 核对每行的 evidence 能解析、且展示的正是该行声称的东西。
- 塑造了工作却没有记录的岔路、转向或被放弃的方案是缺口，补上。

纠正的是日志，不是故事。审计绝不编辑或删除任何一行，哪怕是编造的。某行既不是真实决定也不是真实动作，或它的声称或证据有误时，追加一行取代它，写上实际发生的事和一个能解析的指针。本审计不检查本次运行各段之外的行；但本次运行自身的工作若显示其中某行有误，像任何错误判断一样取代它。

## 轨迹的跨模型审查

交回之前，用一个与干活模型不同家族的模型启动一个子代理。自我审查不能替代这一步。子代理读审计轨迹和本次运行的转写，然后标出用户该注意什么。不是重做工作，是扫描次优或有风险的地方。按 **poteto-mode** 技能的 Subagents 章节，为每个子代理按任务选择推理力度。

- 记录了但证据薄弱或缺失的决定。
- 被跳过、或在转写中没有证明就声称完成的验证步骤。
- 事后看有风险的选择（过早、范围蔓延、遮掩症状）。
- 用户随手扫一遍会漏掉的缺口。

产生了轨迹的运行，每次回复末尾都要有「Attention」一节。第一行单独给出审查者的模型（`reviewed by <model>`），然后逐条列出标记，指向具体的行或时刻。「No flags」是有效值；模型名不是。

## 阅读轨迹

从头读到尾，顺着证据指针抽查。GitHub 会把提交的 TSV 渲染成表格；终端里用 `column -s$'\t' -t decisions.tsv` 查看。

## 组合本技能

其他技能把审计轨迹路由到这里，而不是各自发明一套。按名字引用它，把格式交给它管。不要复述各列。
