---
name: fix-ci
description: 找出失败的 PR 检查，检查日志或外部检查链接，应用聚焦的修复
---

# Fix CI

## 触发

分支或 PR 的 CI 失败，需要一条快速迭代到全绿的路径。

## 工作流

1. 解析活跃 PR，检查 `gh pr checks --json name,bucket,state,workflow,link`。
2. 检查失败的 job，提取第一个可行动的错误。有 GitHub Actions 日志时用日志；否则用检查链接定位失败的命令或服务。
3. 应用最小的安全修复。
4. 推送，复查 PR 检查集，重复直到全绿。

## 护栏

- 一次只修一个可行动的失败。
- 在更大重构之前，优先最小、低风险的改动。
- 以 `gh pr checks` 作为 PR 整体 CI 状态的唯一事实来源。

## 输出

- 主要失败的 job 和根因错误
- 按迭代顺序应用的修复
- 当前 CI 状态和下一步动作
