---
name: principle-guard-the-context-window
description: "适用于上下文正在被填满时：大输出、长文件、重复读取、扇出规划。把大批量路由给子代理；在主线程里保留摘要，而不是原始载荷。"
user-invocable: false
---

# Guard the Context Window

**为什么：** 上下文溢出会降低推理质量、产生压缩伪影，并让进展停摆。

**模式：**
- **为阶段定尺寸并给范围封顶。** 限制每个阶段的文件数，设置回合预算，把机制的成本计入。
