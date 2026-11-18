### 编写或修改一个 skill（技能）

**你拥有这个 skill 的声音。**

1. 使用 **plugin-dev:skill-development** skill（Claude Code 官方的 SKILL.md 编写指南）。
2. 验证这个 skill：frontmatter 含有 `name` 和 `description`，引用的文件存在，跨 skill 的链接都能解析。
3. 如果是结构性的，写测试用例。主观性的则跳过。
4. 运行 **Opening a PR**。

拿不准时，删。只保留能改变决策的文字。让它做那件事，跳过原因。只有当规则没有解释就会令人困惑时才解释。语气与篇幅匹配。按 **encode-lessons-in-structure** 原则 skill 指向结构性来源（类型、README、配置）。通过路径委托给其他 skill。不要复述。一个你反复遇到却没被沉淀的工作流 → 提议一个新 skill。

**回复：** skill 摘要、关键设计决策、验证备注。
