---
name: make-pr-easy-to-review
description: 为审查准备 PR：清理嘈杂的历史、改进 PR 描述、添加审查者指引，但不改变代码行为。用于 "make this easy to review"、"tidy this PR"、"clean up commits" 或 "annotate the diff"。
---

# Make PR Easy to Review

准备一个 PR，让审查者能快速理解意图、重要文件和风险。默认目标是在不改变行为的前提下提升可审查性。

## 工作流

1. 从用户提供的 URL 或当前分支解析目标 PR。
2. 检查提交、diff 大小、改动路径、生成文件和 PR 描述。
3. 识别可审查性问题：嘈杂的提交、过时的描述、无关改动、机械改动与逻辑改动混杂、缺测试、或审查入口不清晰。
4. 在重写历史或 force-push 之前先提出方案。
5. 应用安全的改进，然后验证树或 diff 仍与预期代码一致。

## 历史清理

只在用户要求或同意方案时重写历史。重写之前：

```bash
gh pr view <PR> --json title,headRefName,baseRefName,state,commits
git fetch origin <headRefName> <baseRefName>
ORIGINAL_TREE=$(git rev-parse origin/<headRefName>^{tree})
```

好的提交分组通常按依赖顺序：

1. Schema/存储或生成的 API 定义。
2. 核心逻辑。
3. 接线与集成。
4. UI 或表层行为。
5. 测试。

重写之后，验证内容一致性：

```bash
echo "Original tree: $ORIGINAL_TREE"
echo "Current tree:  $(git rev-parse HEAD^{tree})"
git diff origin/<headRefName> --stat
```

树被意外改变时不要推送。

## 审查者指引

当代码行为应保持不动时，优先用 PR 描述和审查备注：

- 加一段与实际 diff 相符的 TL;DR。
- 把核心文件与生成或机械文件分开。
- 点出有风险的行为改动、迁移顺序、发布计划和测试覆盖。
- 当 issue 追踪器、dashboard 或设计文档能解释意图时，附上链接。

## 护栏

- 绝不把有意义的行为改动藏进「清理」里。
- 不绕过 hooks，除非用户明确要求。
- PR 太大到靠备注无法变得可审查时，建议拆分，而不是围绕问题做抛光。
