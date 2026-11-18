---
name: principle-redesign-from-first-principles
description: "适用于把一个新需求整合进现有设计时。"
user-invocable: false
---

# Redesign From First Principles

整合一个改动时，不要把它拴在现有设计上。重新设计，就当这个需求从一开始就是基础假设。

- 读所有受影响的文件，理解当前设计
- 问：「如果我们带着这个新需求从零开始写，我们会建什么？」
- 把改动传播到每一处引用：类型、文档、示例、理由章节
- 先想清楚整个重设计，然后增量交付

这是把改动整合进现有设计时保住选择余地（option value）的方法。
