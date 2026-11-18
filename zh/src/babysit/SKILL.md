---
name: babysit
description: 看护一个已打开的 PR——修复失败的 CI，处理简单的审查评论，把它推进到可合并状态。Cursor 内置 /babysit 的 Claude Code 对应物。在打开 PR 之后、用户希望代理不用反复提示就把它带到合并时使用。
---

# Babysit a PR

在 Codex 上，先读[平台映射](../poteto-mode/references/codex-tools.md)（包括其中的每技能注记），再执行本技能。

在 GitHub Copilot 上，先读[平台映射](../poteto-mode/references/copilot-tools.md)（包括其中的每技能注记），再执行本技能。

在 Muse 上，先读[平台映射](../poteto-mode/references/muse-tools.md)（包括其中的每技能注记），再执行本技能。

在 Antigravity 上，先读[平台映射](../poteto-mode/references/agy-tools.md)（包括其中的每技能注记），再执行本技能。

Cursor 内置 `/babysit` 的 Claude Code 对应物。实现是一个循环：`gh` CLI 加 Claude Code `loop` 技能做节奏控制。

在 poteto-mode 里，**Babysit** playbook（流程清单）（[`../poteto-mode/playbooks/babysit.md`](../poteto-mode/playbooks/babysit.md)）取代本技能：它负责模式声明、merge frontier、stack 安全和 `watch-pr` watcher。本技能仍是 poteto-mode 运行之外单个 PR 的独立 `/babysit` 入口。

## 何时使用

- 有一个已打开的 PR，用户明确要求保持它绿色，且你并不在 poteto-mode 运行之内（那种情况由 playbook 负责）。
- 用户直接调用 `/babysit`。
- 打开 PR 的子代理不 babysit——返回父代理，由父代理决定。

## 步骤

1. **获取 PR 状态。**

   ```bash
   gh pr view <number> --json number,title,state,mergeable,reviewDecision,statusCheckRollup,mergeStateStatus,comments,reviews
   ```

2. **按优先级排序分诊。**
   - 合并冲突（`mergeStateStatus == DIRTY`）：运行 **fix-merge-conflicts** 技能。只有分支是你的且未共享时才 force-push。
   - 失败的检查（`statusCheckRollup` 中 `conclusion: FAILURE` 的条目）：运行 **fix-ci** 技能。给失败找根因；修底层的代码或测试；提交；推送。
   - 审查评论：运行 **get-pr-comments** 技能拿摘要，只对你真正认同的反馈采取行动。当一条评论只有一个机械答案——重命名、guard clause、格式小问题——就做这个编辑，并在 commit message 里引用该评论。当它取决于判断取舍，或你看不清对方在问什么，不要猜：留着不动，回复你本来会怎么做。
   - 审查机器人评论（Bugbot 等自动化）：行动前先分类为 fix/dismiss/ask，依据 [`bugbot-triage.md`](../poteto-mode/references/bugbot-triage.md)。对安全、数据和高严重性发现默认 ask。

3. **循环。** 用 Claude Code `loop` 技能控制复查节奏。按你在盯的东西选间隔：
   - 活跃 CI 运行：轮询 `gh pr checks --watch`（它会阻塞到检查完成，不需要单独的循环间隔）。
   - 等审查者：20–30 分钟一次心跳。
   - 空闲但想抓新评论：每小时一次。

4. **何时停止。**
   - 构建绿色、每条评论已解决、分支干净合并 → 宣布就绪。
   - 你已经跑了三轮 fix → push → recheck 还不完全绿 → 停下，总结还坏着什么，把控制权交回。
   - 下一个修复需要做设计选择 → 暂停，用 `AskUserQuestion` 提给用户。

5. **汇报。** 总结已应用的修复、已处理的评论、搁置的评论（带原因）、PR 当前状态。每条提交用 SHA 引用。

## 硬规则

- 不在别人可能已拉取的分支上重写历史。如果 rebase 或 force-push 看起来必要，先和用户确认。
- 不为了让测试通过而改测试的期望值。只有行为真的变了、且断言是钉在旧行为上时，才改断言。
- 绝不跳过 hooks（`--no-verify`）。
- 绝不通过把失败检查标记为非必需来绕过它。
- 只有全部检查绿色且没有未解决的审查评论时才 `gh pr ready`。

## 交叉引用

- 打开 PR 不会自动开始 babysit；在 poteto-mode 里 Babysit playbook 负责该请求，且只在被要求时开始。
- diff 有争议时，打开前先跑 `interrogate`；打开后由 babysit 接手。
- 你在这里写的任何文字（PR 评论、commit message、状态报告）都过 `unslop`。

## Provenance

这是 Cursor `/babysit` 的 Claude Code 对应物，不是移植——Cursor 的实现是闭源的。本技能独立撰写，有自己的行文和结构；工作流参考了 Cursor 公开的 `/babysit` 行为。与其他 PR 工具的重叠只有它运行的 `gh` CLI 命令，那是功能调用而非抄来的文字。
