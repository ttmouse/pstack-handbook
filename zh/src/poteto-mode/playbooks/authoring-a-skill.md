### 编写或修改一个 skill

**skill 的语气由你负责。**

1. 使用 **plugin-dev:skill-development** 技能（Claude Code 官方的 SKILL.md 编写指南）。
2. 校验 skill：frontmatter 带 `name` 和 `description`，引用的文件存在，跨 skill 的链接能解析。
3. 结构性的写测试用例；主观性的跳过。
4. 走 **Opening a PR** 流程。

拿不准就删。只保留能改变决策的文字。叫它做这件事，跳过原因解释；只有不解释规则就会让人困惑时才解释。语气匹配规模。按 **encode-lessons-in-structure** 原则技能，把结构性的来源（类型、README、配置）指给读者。用路径委托给其他 skill。不要复述。某个工作流你反复遇到但没被沉淀 → 提议一个新 skill。

**汇报：** skill 摘要、关键设计决策、校验说明。
