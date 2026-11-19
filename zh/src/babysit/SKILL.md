---
name: babysit
description: 看护一个已打开的 PR——修 CI、处理简单直接的评审意见，把它推到可合并状态。Claude Code 版的 Cursor 内置 /babysit。在 PR 打开之后、用户想让代理无需反复提示就把 PR 护送到终点时使用。
---

# Babysit a PR

在 Codex 上，遵循本技能前先读[平台映射](../poteto-mode/references/codex-tools.md)，包括其中按技能给出的说明。

在 GitHub Copilot 上，遵循本技能前先读[平台映射](../poteto-mode/references/copilot-tools.md)，包括其中按技能给出的说明。

在 Muse 上，遵循本技能前先读[平台映射](../poteto-mode/references/muse-tools.md)，包括其中按技能给出的说明。

在 Antigravity 上，遵循本技能前先读[平台映射](../poteto-mode/references/agy-tools.md)，包括其中按技能给出的说明。

这是 Cursor 内置 `/babysit` 的 Claude Code 对应物。实现是一个循环，用 `gh` CLI 加 Claude Code 的 `loop` 技能来控制节奏。

在 poteto-mode 里，**Babysit** playbook（[`../poteto-mode/playbooks/babysit.md`](../poteto-mode/playbooks/babysit.md)）取代本技能：模式声明、合并前沿、堆栈安全和 `watch-pr` watcher 都归它管。本技能保留为 poteto-mode 运行之外单个 PR 的独立 `/babysit` 入口。

## When to use

- 有一个已打开的 PR，用户明确想让它保持绿，且你不在 poteto-mode 运行中（那种情况归 playbook 管）。
- 用户直接调用 `/babysit`。
- 打开 PR 的子代理不做 babysit——返回父级，让父级决定。

## Steps

1. **获取 PR 状态。**

   ```bash
   gh pr view <number> --json number,title,state,mergeable,reviewDecision,statusCheckRollup,mergeStateStatus,comments,reviews
   ```

2. **按优先级分诊。**
   - 合并冲突（`mergeStateStatus == DIRTY`）：跑 **fix-merge-conflicts** 技能。只有分支是你的且未共享时才 force-push。
   - 检查失败（`statusCheckRollup` 中 `conclusion: FAILURE` 的条目）：跑 **fix-ci** 技能。定位失败根因；修底层代码或测试；提交；推送。
   - 评审意见：跑 **get-pr-comments** 技能拿摘要，然后只对你真正认同的意见动手。当一条意见只有一个机械解法——改名、加守卫子句、格式小修——就改掉，并在 commit message 里引用该意见。当它取决于主观判断，或你搞不清对方在问什么，别猜：先放着，回复你本来会怎么做。
   - 评审机器人意见（Bugbot 等自动化）：动手前先分类为修复/驳回/提问，依据 [`bugbot-triage.md`](../poteto-mode/references/bugbot-triage.md)。涉及安全、数据和高严重性的发现，默认选择提问。

3. **循环。** 用 Claude Code 的 `loop` 技能控制复查节奏。按盯的东西选间隔：
   - CI 正在跑：轮询 `gh pr checks --watch`（它会阻塞到检查结束，不需要单独的循环间隔）。
   - 等评审人：20–30 分钟一次心跳。
   - 空闲但想抓新评论：每小时。

4. **何时停止。**
   - 构建绿了、每条意见都解决、分支可干净合并 → 宣告就绪。
   - 三轮 fix → push → recheck 跑完仍未全绿 → 停下，总结还坏着什么，把控制权交回。
   - 下一步修复会逼出一个设计抉择 → 暂停，用 `AskUserQuestion` 提给用户。

5. **汇报。** 总结修了什么、回应了哪些意见、搁置了哪些（附原因）、PR 当前状态。每条 commit 都给出 SHA。

## Hard rules

- 不改写别人可能已拉取的分支历史。如果 rebase 或 force-push 看起来必要，先跟用户确认。
- 不为了过测试而改测试的期望值。只有当行为真的变了、且断言原本钉死在旧行为上时，才改断言。
- 绝不跳过 hooks（`--no-verify`）。
- 绝不通过把检查标记为非必需来绕过失败的检查。
- 只在所有检查全绿且没有未解决的评审意见时才 `gh pr ready`。

## Cross-refs

- 打开 PR 不等于开始 babysit；在 poteto-mode 里归 Babysit playbook 管，且只在被要求时才开始。
- diff 有争议时，打开 PR 前先跑 `interrogate`；打开后由 babysit 接手。
- 在这里写的任何文字（PR 评论、commit message、状态汇报）都过一遍 `unslop`。

## Provenance

这是 Cursor `/babysit` 的 Claude Code 对应物，不是移植——Cursor 的实现是闭源的。本技能独立撰写，有自己的文字和结构；工作流参考了 Cursor 公开的 `/babysit` 行为。与其他 PR 工具的唯一重叠是它运行的 `gh` CLI 命令，那是功能性调用，不是抄来的文本。
