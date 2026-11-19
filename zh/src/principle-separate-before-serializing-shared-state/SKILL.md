---
name: principle-separate-before-serializing-shared-state
description: "适用于并发执行方可能写同一个文件、分支、键或状态对象的时候。先消除共享；只有当单一共享写入点确实是必要不变量时，才做结构上的串行化。"
user-invocable: false
---

# Separate Before Serializing Shared State

当并发执行方可能写同一个文件、分支、键或对象时，先问一句：它们是真需要一个共享对象，还是在各自发布互不相关的事实？默认给每个执行方自己的文件、键、分支或状态目录，只在读取状态的地方做合并。两个 worker 各写一个字段到同一个 `state.json`，仍然是共享修改。

只有当「单一共享写入点」确实是必要不变量时，才用结构化的方式串行化访问（锁文件、单一写入者、顺序阶段、compare-and-swap）。指令说明不是并发控制，「我们需要加个锁」是一种坏味道，要先回头检查共享本身是否必要。
