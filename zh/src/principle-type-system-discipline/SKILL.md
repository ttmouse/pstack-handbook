---
name: principle-type-system-discipline
description: "适用于设计类型、审查函数签名，或用任何静态类型语言写代码时。让非法状态无法被表示，给语义化的原始类型加品牌，在边界解析外部数据，穷尽所有变体，从权威 schema 派生类型。"
user-invocable: false
---

# Type System Discipline

让编译器拒绝不可能的状态、错配的原始类型和未处理的变体。

- **给语义化的原始类型加品牌（brand）。** 两个参数类型相同但含义不同时，给各自定义独立类型，在创建处验证一次。
- **外部数据在解析前是无类型的。** JSON、RPC 载荷、CLI 参数、配置、环境变量、数据库行，都要经过边界处的解析函数，由它返回带类型的模型。
- **从权威 schema 派生类型。** 某个形状由 schema 文件负责时，从它派生类型，不要手工再写一份平行的。

TypeScript 语法细节见 **typescript-best-practices** 技能。
