---
name: make-pr-easy-to-review
description: 通过清理嘈杂的历史、改进 PR 描述、补充审查者指引来让 PR 便于审查，且不改变代码行为。用于「让这个 PR 好审查」「整理这个 PR」「清理提交」「给 diff 加注释」。
---

# Make PR Easy to Review

把 PR 准备到审查者能快速理解意图、关键文件和风险的程度。默认目标是在不改变行为的前提下提升可审查性。

## 工作流

1. 根据用户提供的 URL 或当前分支确定目标 PR。
2. 检查提交、diff 大小、改动路径、生成文件和 PR 描述。
3. 识别影响可审查性的问题：嘈杂的提交、过时的描述、无关改动、机械改动与逻辑改动混在一起、缺测试，或审查入口不清晰。
4. 重写历史或 force-push 之前，先提出方案。
5. 应用安全的改进，然后验证工作树或 diff 仍然与预期代码一致。

## 历史清理

只在用户要求或同意方案时才重写历史。重写之前：

```bash
gh pr view <PR> --json title,headRefName,baseRefName,state,commits
git fetch origin <headRefName> <baseRefName>
ORIGINAL_TREE=$(git rev-parse origin/<headRefName>^{tree})
```

好的提交分组通常按依赖顺序排：

1. Schema/存储或生成的 API 定义。
2. 核心逻辑。
3. 接线与集成。
4. UI 或表面行为。
5. 测试。

重写之后，验证内容一致性：

```bash
echo "Original tree: $ORIGINAL_TREE"
echo "Current tree:  $(git rev-parse HEAD^{tree})"
git diff origin/<headRefName> --stat
```

tree 意外变化时不要 push。

## 审查者指引

代码行为应当保持不变时，优先用 PR 描述和审查备注：

- 加一段与实际 diff 相符的 TL;DR。
- 把核心文件和生成文件、机械文件区分开。
- 点出高风险的行为改动、迁移顺序、上线计划和测试覆盖。
- 能解释意图的 issue 追踪、仪表盘或设计文档，附上链接。

## 护栏

- 绝不把实质性的行为改动藏在「清理」里。
- 不绕过 hooks，除非用户明确要求。
- 如果 PR 大到靠备注救不回来，建议拆分，而不是在问题周围抛光。
