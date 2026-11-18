这本是 TypeScript 的类型纪律速查表，处理任何 `.ts` / `.tsx` 文件时自动生效，核心思想是「把非法状态建造成无法表示」。

拆解里面的黑话：

- **判别式 union**：用 `kind` 字面量字段建模变体，替代可选字段拼凑的对象。
- **branded types**：给 ID 这类基本类型打品牌标记，编译期就防止两种 ID 混用，品牌必须来自验证型 type guard 而不是 `as`。
- **narrowing 层级**：判别式 switch 优于 `in` 优于 `typeof` 优于 type guard，`as` 是最后手段——每个 `as` 都是一次排队的运行时崩溃。
- **穷尽检查**：switch 的 default 臂写 `const _exhaustive: never = x`，新增变体时编译器直接报错。

什么时候用它：读写 TS 代码、评审类型设计、纠结一个值该不该用 `any`。什么时候别用：它是规则表不是教程，想学原理去读 type-system-discipline 原则技能。
