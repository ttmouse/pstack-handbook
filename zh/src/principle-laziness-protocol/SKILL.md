---
name: principle-laziness-protocol
description: "重构、评估 diff 大小，或想加抽象、加分层、加信号穿线时应用。倾向删除，倾向解决问题的最小改动。"
user-invocable: false
---

# Laziness Protocol

- **合并决策。** 不要在多个地方重复同一个选择。把它放到唯一的事实来源后面，把结果作为一个简单标志传出去。
- **最小化 diff。** 做解决问题的最小改动。更少的行胜过「优雅」的样板。
