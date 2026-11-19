---
name: typescript-best-practices
description: TypeScript 最佳实践。读取或编辑任何 .ts 或 .tsx 文件时使用。
paths: ["**/*.ts", "**/*.tsx"]
---

# TypeScript 最佳实践

在 Muse 上，先读[平台映射](../poteto-mode/references/muse-tools.md)，包括其中按 skill 的备注，再执行本技能。

先应用 **type-system-discipline** 原则技能。

| 规则 | 要点 |
|------|------|
| 可辨识联合 | 用 `kind` 字面量判别字段建模变体，让非法状态无法被表示。不要用可选字段大杂烩。 |
| 品牌类型 | 给原始类型加上 `& { readonly __brand: "X" }` 品牌，防止混用。只在边界验证一次。品牌只能来自经过验证的类型守卫（`input is AgentId`），绝不来自 `as`。 |
| 建构式建模 | 把类型设计成非法值根本构造不出来。非空用 `[T, ...T[]]`，偶数长度用 `[T, T][]`，区间用 `start` 加 `duration`。不是运行时守卫，也不是对 refinement 类型的空想。 |
| 最简的全域类型 | 只要 `T[]` 上的每个操作都保持全域，就保留 `T[]`。只有当松散类型逼出 `!`、转型或"不该发生"的 throw 时，才收紧为 `NonEmpty<T>`。 |
| `unknown` 优先于 `any` | 外部数据一律 `unknown`。 |
| schema 先于手写守卫 | 在手写逐属性类型守卫之前，用仓库的运行时 schema 库从 schema 推导类型，比如 `z.infer`。 |
| 不用 `as` 转型 | 每个 `as` 都是一次等着发生的运行时崩溃。只在验证之后转型。 |
| 收窄优先级 | 判别字段 switch > `in` 运算符 > `typeof`/`instanceof` > 自定义类型守卫 > `as`。 |
| 类型守卫 | 必须真正验证声明。说谎的守卫比 `as` 更糟，因为 bug 藏在一个自称安全的名字背后。命名为 `isX` 或 `hasX`。 |
| 穷尽性 | 在 default 分支内联 `const _exhaustive: never = x;`，新增变体时编译器直接报错。 |
| `satisfies` 优先于 `as` | 验证值的同时不拓宽字面量类型。 |
| 边界验证 | 在数据入口解析成命名的领域类型。`Record<string, unknown>`（无论怎么写）止步于这次解析。边界内信任类型。参见 **boundary-discipline** 原则技能。 |
| schema 派生类型 | 在声明新 interface 之前，先用 `Pick`/`Omit`/`Parameters`/`ReturnType`/`Awaited`/`typeof`。 |
| 对象参数 | 传对象，不传位置参数，让参数顺序自解释。热路径（逐帧渲染、分词器、解析器）除外。 |
| 真实测试 | 能跑的不要 mock。优先用框架的真实测试原语，带泄漏/资源释放检查，在真实运行的构建里验证 UI。只 mock 本地跑不了的东西。 |
| 结构化遥测 | 优先用带足够上下文的结构化日志诊断，凭一个 id 就能调试。发布代码里不放 `console.log`。 |

示例见 `references/patterns.md`。
