---
name: principle-laziness-protocol
description: "适用于重构、评估 diff 大小，或忍不住想加抽象、分层或信号串接时。偏向删除，偏向能解决问题的最小改动。"
user-invocable: false
---

# Laziness Protocol

- **合并决策。** 不要在几个地方重复同一个选择。把它收进唯一的事实来源，把结果作为一个简单标志传递。
- **最小化 diff。** 做能解决问题的最小改动。更少的行胜过「优雅」的样板。
