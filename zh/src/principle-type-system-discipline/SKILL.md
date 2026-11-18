---
name: principle-type-system-discipline
description: "适用于设计类型、审查函数签名，或在任何静态类型语言里写代码时。让非法状态不可表示，给语义原语加品牌类型，在边界解析外部数据，穷尽变体，从权威 schema 派生。"
user-invocable: false
---

# Type System Discipline

让编译器拒绝不可能的状态、不匹配的原语和未处理的变体。优先用「把错误和特殊情况定义到不存在」的方式，而不是增殖处理分支。TypeScript 语法见 `typescript-best-practices` 技能。

- **给语义原语加品牌类型（brand）。** `UserId` 和 `OrderId` 底层都是字符串，但不应该可以互换。给每个自己的类型，比如 TypeScript 里的 branded intersection，其他语言里的 newtype。在创建时校验一次，下游信任类型。如果两个参数共享同一个原语类型但含义不同，就给他们加品牌。
- **外部数据在解析之前没有类型。** RPC 载荷、JSON、IPC 消息、CLI 参数、配置文件、环境变量、数据库行。在每个边界放一个解析函数，把非结构化输入变成类型化模型。校验放在哪里由 **boundary-discipline** 原则技能决定。
- **从权威 schema 派生类型。** 当一个 protocol buffer、OpenAPI spec、GraphQL schema、数据库迁移、design-token 文件或另一个文件拥有某个形状时，从它派生，而不是手工写一个平行类型。见 **encode-lessons-in-structure** 原则技能。
