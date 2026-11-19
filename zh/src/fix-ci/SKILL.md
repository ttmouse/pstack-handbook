---
name: fix-ci
description: 找出失败的 PR 检查，查看日志或外部检查链接，做聚焦的修复
---

# Fix CI

## Trigger

分支或 PR 的 CI 在挂，需要一条快速迭代到全绿的路径。

## Workflow

1. 定位当前 PR，查看 `gh pr checks --json name,bucket,state,workflow,link`。
2. 检查失败的 job，提取第一条可操作的错误。有 GitHub Actions 日志就用它；否则用检查链接定位失败的命令或服务。
3. 施加最小的安全修复。
4. 推送，复查 PR 检查集，重复直到全绿。

## Guardrails

- 一次只修一条可操作的失败。
- 先做最小、低风险的改动，再考虑更大范围的重构。
- 始终以 `gh pr checks` 作为 PR CI 整体状态的唯一事实来源。

## Output

- 最主要的失败 job 和根因错误
- 按迭代顺序列出施加的修复
- CI 当前状态和下一步动作
