---
name: get-pr-comments
description: 拉取并总结当前 PR 的评审意见
---

# Get PR comments

## Trigger

需要对当前 PR 的反馈做一份精炼、可执行的总结。

## Workflow

1. 定位当前分支对应的 PR。
2. 拉取评审意见和讨论留言。
3. 按严重程度和可操作性分组。
4. 返回一份精炼的行动清单。

## Output

- 分组后的反馈总结
- 按优先级排序的行动清单
- 仍需澄清的待决问题
