---
name: architect
description: "先勾出类型、签名和模块结构，再让实现去填充，过程中保持人在环上。用于 /architect、'architect this'、'design this'，或任何直接动手写代码会锁死错误形状的非平凡工作。"
---

# Architect

在 Codex 上，遵循本技能前先读[平台映射](../poteto-mode/references/codex-tools.md)，包括其中按技能给出的说明。

在 GitHub Copilot 上，遵循本技能前先读[平台映射](../poteto-mode/references/copilot-tools.md)，包括其中按技能给出的说明。

在 Muse 上，遵循本技能前先读[平台映射](../poteto-mode/references/muse-tools.md)，包括其中按技能给出的说明。

在 Antigravity 上，遵循本技能前先读[平台映射](../poteto-mode/references/agy-tools.md)，包括其中按技能给出的说明。

写代码之前，先梳理这次改动涉及的每个系统，然后为它勾出两种不同的形状（类型、签名、模块边界），选出那个每份状态只有一个所有者、每件事只有一种做法、调用方需要知道的东西最少的形状。如果变通手段开始重复出现，就重新设计，而不是继续打补丁。

设计规模大或有争议时，改跑 **arena** 技能，不要一个人勾草图。

在关闭每个实现单元、或把它的契约交给下一个 worker 之前，对照已保存的草图和理由检查有哪些被接受的偏离。一旦所有者或评审流程接受了某个变更，就更新草图中受影响的部分，并记录是谁接受的。未被接受的变更和未解决的分歧保持可见，绝不要为了给已实现的东西找理由而改动草图。
