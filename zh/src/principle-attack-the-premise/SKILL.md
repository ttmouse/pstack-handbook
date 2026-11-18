---
name: principle-attack-the-premise
description: "适用于两个或更多共享同一前提的修复在同一个闸门上失败时。先写下这个前提并直接检验它，再写下一个依赖它的修复。"
user-invocable: false
---

# Attack the Premise

当两个或更多共享同一前提的修复在同一个闸门上失败时，怀疑的是前提，而不是那些修复。

**为什么：** 每个失败的修复都是对它所依赖信念的反证。在同一个前提上做第三次修复，是把精力花在证据已经说明原因不在的地方。

**模式：**
- **把前提写下来。** 前提是每个失败的修复都依赖的那一句话。
- **在下一个修复之前先检验前提。** 找一个如果前提为假结果就会不同的观察，然后去做它。看失败是怎么分布的，而不只是看它们有多大。让这个检查可重跑，做法见 [Build the Lever](../principle-build-the-lever/SKILL.md)。
- **跟着证据走。** 如果证据与前提矛盾，原因在别处。找失败之间有什么前提没有预测到的共同点。如果证据确认了前提，就按 [Fix Root Causes](../principle-fix-root-causes/SKILL.md) 追问下一个「为什么」。之前的修复可能治的是后果而不是原因。
- **移除条件本身，而不是补偿它**，做法见 [Laziness Protocol](../principle-laziness-protocol/SKILL.md)。如果证据显示某一部分总是落在失败的一边，就改变把它放到那里的机制。一个事后清理的机制把原因留在原地，还在每次运行时增加工作量。

**停止条件：** 在前提被写下并检验之前，不要开始下一个修复。

本原则不同于 [Redesign from First Principles](../principle-redesign-from-first-principles/SKILL.md)，后者围绕新需求重建一个设计。本原则质疑的是当前设计所依赖的某个事实。
