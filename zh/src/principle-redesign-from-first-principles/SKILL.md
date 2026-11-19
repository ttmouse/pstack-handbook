---
name: principle-redesign-from-first-principles
description: "适用于把新需求融入现有设计的时候。"
user-invocable: false
---

# Redesign From First Principles

融入一项改动时，不要把它硬钉在现有设计上。重新设计，就当这个需求从一开始就是基础假设。

- 通读所有受影响的文件，理解当前设计
- 问自己：「如果我们带着这个新需求从零开始写，会造出什么？」
- 把改动传播到每一处引用：类型、文档、示例、设计理由章节
- 先想清楚整个重新设计，再增量交付

这是在向既有设计融入改动时，保住选择权（option value）的方法。
