---
name: show-me-your-work
description: "为长时间运行或无人值守的工作保留一条可审查的决策轨迹：一个 TSV 日志，每个决策一行（做了什么、为什么、证据、结果）。默认本地保存；当评审者需要轨迹来信任结果时才提交它。用于 /show-me-your-work、自主或多阶段运行、或人离开后回头审查的工作。"
---

# Show me your work

在 GitHub Copilot 上，先读[平台映射](../poteto-mode/references/copilot-tools.md)（包括其中的逐技能说明），再执行本技能。

在 Muse 上，先读[平台映射](../poteto-mode/references/muse-tools.md)（包括其中的逐技能说明），再执行本技能。

在 Antigravity 上，先读[平台映射](../poteto-mode/references/agy-tools.md)（包括其中的逐技能说明），再执行本技能。

只保留一份正本日志。

## 格式

单个 TSV 文件，每个决策一行。单元格保持单行。证据是指针，不是散文。

复制 `references/decision-log-template.tsv`（表头行）来开一份干净的日志。各列：

- **ts.** ISO8601 时间戳。
- **phase.** 阶段或工作流。
- **decision.** 选择了或做了什么，一行。
- **why.** 用平实的话说理由。如果是某个原则驱动了它，直说，不用术语标签。
- **evidence.** 一条证明它的链接或路径：commit SHA、PR 号、`file:line`、或一个产物、trace、截图路径。绝不是一段话。
- **result.** 结果或谓词状态：`tests green`、`reverted`、`pixel-diff 0`、`INCONCLUSIVE`、`open`。

一个示例，写得平实让评审者一眼读完。

```
ts	phase	decision	why	evidence	result
2026-05-24T09:02:00Z	frame	counted the work first, about 100 components and roughly 75 hours	wanted to know the size before starting a long run	commit 3a9f1c2	found 5 things to sort out before starting
2026-05-24T09:40:00Z	harness	took screenshots of the old version before changing anything	so we can compare old against new and catch any visual change	scripts/snapshot.sh, baseline/	saved 120 reference screenshots
2026-05-24T11:15:00Z	widget	moved the widget styles over without changing how it looks	keep the change small and the result identical	commit 7c21e0a, pixel-diff 0	looks identical, tests pass
2026-05-24T12:30:00Z	widget	threw out a helper's work because its screenshots were blank	checked the real files instead of trusting its summary	worktree reset	reverted, tightened the instructions for next time
```

## 记一行

每条都按你会怎么跟队友讲你做了什么来写。平实的话、具体的动作、不用 AI 腔和抽象术语（**unslop** 技能同样适用于日志文字）。

用辅助脚本 `scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>`。它会打 `ts` 时间戳、首次使用时写表头、剥掉多余的 tab/换行、给以 `=`、`+`、`-`、`@` 或 `"` 开头的单元格加单引号前缀。裸 `printf` 追加一行也行，但单元格来自生成文本或用户提供的文本时，当心同样那些字节。

记决策点和检查点，不是每个动作：一次分叉的选择、一个单元完成及其验证结果、一次转向或回退及其触发点、一个浮出的阻塞、一个修好的闸门。循环运行每次迭代一行。琐碎和自明的跳过。

一次运行（run）指一个代理对话，包括它后续的轮次和任何对它的总结。一次接续、一个替换代理、或一个新聊天，都开启新的一次运行。当一次运行往已有行的日志里追加时，它的第一行 phase 为 `start`，它在另一次运行的 `start` 行之后的第一行也是。于是一次运行在后续轮次回到一份日志时，先读日志最后几行，看看是否有另一次运行在它之后写过。`start` 行写明它之前那段非本次运行所写的行的 `ts` 范围，其 evidence 写明本次运行，比如它的代理 id。phase `start` 不用于任何其他用途。

## 放在哪

默认日志是工作产物，不提交。放在工作目录的 `decisions.tsv`，多个工作并行时放 `.audit/<task-slug>.tsv`，并排除在 git 之外。

只有当工作足够重要、评审者需要轨迹才能信任结果时才提交它。

## 规则

- 只追加。错误的决定用新的一行取代它。绝不编辑或删除历史。
- 优先用已提交脚本产出的证据，而不是手工的一次性产物（**encode-lessons-in-structure** 原则技能）。

## 对照会话记录审计日志

运行结束、交回之前，检查日志说的是不是实话。在 Claude Code 的按项目会话记录目录 `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/<encoded-cwd>/` 下读本次运行的转录，`node <plugin>/skills/reflect/scripts/claude-project-dir.mjs` 会打印这个路径。不要跨 `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/` 做 glob。那会读到无关的私人聊天。拿本次运行的各行对照实际发生的事。其中每一段都起始于本次运行的一个 `start` 行——或本次运行创建了日志时的第一行——终止于另一次运行的下一个 `start` 行：

- 检查每一行都对应一个真实的决策或动作。
- 检查每行的证据能解析并展示了该行声称的东西。
- 某个塑造了工作的分叉、转向或被放弃的方案没有记录，就是缺口。补上它。

纠正日志，不是纠正故事。审计绝不编辑或删除一行，哪怕是编造的一行。当某行记录的既不是真实决策也不是真实动作，或它的主张或证据是错的，加一行取代它，写明实际发生了什么和一条能解析的指针。本次审计不检查本次运行的段落之外的行。如果本次运行自身的工作显示其中某行是错的，像任何错误决定一样取代它。

## 轨迹的跨模型评审

交回之前，在与干活者不同的模型家族上生成一个子代理。自我评审不是替代品。子代理读审计轨迹和本次运行的转录，然后标出用户应该注意什么。不是重做工作，是扫一遍找次优或有风险的东西。按 **poteto-mode** 技能的 Subagents 小节，为工作选择每个子代理的推理强度。

- 证据薄弱或缺失的已记录决策。
- 转录里被跳过或无凭据声称的验证步骤。
- 事后看有风险的选择（过早、范围蔓延、糊弄症状）。
- 用户随手略读会漏掉的缺口。

产出了轨迹的运行，其每次回复都以一个「Attention」小节结尾。先单独一行写评审者的模型（`reviewed by <model>`），再逐条列出标记并指向具体的行或时刻。「No flags」是合法取值。模型名不是。

## 审阅轨迹

从头到尾读，跟着证据指针走，抽查。GitHub 会把已提交的 TSV 渲染成表格。`column -s$'\t' -t decisions.tsv` 在终端里渲染它。

## 组合本技能

其他技能把它们的审计轨迹路由到这里，而不是各自发明一套。按名字引用它，把格式交给它管。不要复述那些列。
