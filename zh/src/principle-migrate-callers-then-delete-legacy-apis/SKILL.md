---
name: principle-migrate-callers-then-delete-legacy-apis
description: "适用于在旧调用方仍然存在时引入新的内部 API。在同一波里迁移调用方并删除旧 API，而不是保留兼容层。"
user-invocable: false
---

# Migrate Callers Then Delete Legacy APIs

- 把测试更新为断言新契约，删除那些只保护重构前实现细节的测试

**适用条件：**
- 没有外部用户依赖向后兼容
- 项目能吸收协调一致的破坏性变更
- 新 API 是某次简化或重构行动的一部分
