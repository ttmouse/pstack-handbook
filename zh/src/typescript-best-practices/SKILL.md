---
name: typescript-best-practices
description: TypeScript 最佳实践。读取或编辑任何 .ts 或 .tsx 文件时使用。
paths: ["**/*.ts", "**/*.tsx"]
---

# TypeScript best practices

在 Muse 上，先读[平台映射](../poteto-mode/references/muse-tools.md)（包括其中的每技能注记），再执行本技能。

先应用 **type-system-discipline** 原则技能。

| 规则 | 摘要 |
|------|---------|
| Discriminated unions | 用 `kind` 字面量判别式建模变体，让不可能的状态无法被表示。不要用可选字段袋。 |
| Branded types | 用 `& { readonly __brand: "X" }` 给基本类型打品牌，让它们无法被混用。在边界验证一次。品牌来自验证型 type guard（`input is AgentId`），绝不用 `as`。 |
| Constructive modeling | 把形状建造成非法值无法被构造出来。非空用 `[T, ...T[]]`，偶数长度用 `[T, T][]`，区间用 `start` 加 `duration`。这不是运行时守卫，也不是对 refinement types 的空想。 |
| Simplest total type | 只要 `T[]` 上的每个操作保持全函数，就保留 `T[]`。只有当宽松类型逼出 `!`、cast 或「不应该发生」的 throw 时，才加强为 `NonEmpty<T>`。 |
| `unknown` over `any` | 外部数据是 `unknown`。 |
| Schemas before guards | 在手写逐属性 type guard 之前，用仓库的运行时 schema 库并从 schema 推导类型，比如 `z.infer`。 |
| No `as` casts | 每个 `as` 都是一次等待发生的运行时崩溃。只在验证之后 cast。 |
| Narrowing hierarchy | 判别式 switch > `in` 运算符 > `typeof`/`instanceof` > 用户定义 type guard > `as`。 |
| Type guards | 必须证实其声称。撒谎的 guard 比 `as` 更糟，因为 bug 躲在一个自称安全的名字后面。命名为 `isX` 或 `hasX`。 |
| Exhaustiveness | 在 default 臂里写内联的 `const _exhaustive: never = x;`，这样新增变体时编译器报错。 |
| `satisfies` over `as` | 验证值的同时不拓宽字面量类型。 |
| Boundary validation | 在数据进入的地方 parse，parse 进命名的领域类型。`Record<string, unknown>`（无论怎么写）止于这次 parse。类型在内部可信。见 **boundary-discipline** 原则技能。 |
| Schema-derived types | 在声明新 interface 之前，先想到 `Pick`/`Omit`/`Parameters`/`ReturnType`/`Awaited`/`typeof`。 |
| Object args | 传对象而非按位置传参，让参数顺序自文档化。热路径（逐帧渲染、分词器、解析器）除外。 |
| Real tests | 能跑的不要 mock。优先用框架真实的测试原语加泄漏/释放检查，并在运行中的构建里验证 UI。只 mock 本地跑不了的。 |
| Structured telemetry | 优先用结构化日志诊断，上下文足够从一个 id 调试。发布代码里没有 `console.log`。 |

示例见 `references/patterns.md`。
