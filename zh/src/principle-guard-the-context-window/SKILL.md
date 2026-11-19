---
name: principle-guard-the-context-window
description: "上下文要满时应用：大输出、长文件、重复读取、扇出规划。把大宗内容路由给子代理；主线程只留摘要，不留原始负载。"
user-invocable: false
---

# Guard the Context Window

**为什么：** 上下文溢出会拖垮推理质量，产生压缩伪影，并让进展中断。

**模式：**
- **给阶段定大小，给范围设上限。** 限制每个阶段的文件数，设定轮次预算，把机制自身的开销算进去。
