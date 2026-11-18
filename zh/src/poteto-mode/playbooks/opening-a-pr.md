### Opening a PR

在每个其他 playbook（流程清单）的末尾被调用。

**工作树。** 从 main 切出的 git 工作树里工作。子代理继承它。同一个分支上的多次 `Agent` 调用各自获得自己的工作树，或者在两次调用之间执行 `git fetch && git reset --hard origin/<branch>`。分支上有无关工作的脏状态：先 patch 掉，开新工作树，再应用回去。纠缠不清的工作树：从 main 重置，最小化地重做。在你从工作树里 commit、merge 或 deploy 之前，列出活跃代理，停掉每一个持有它的——包括那些你从未启动的孙代理。委托者的子代理不继承它的简报，所以一条只读指令到不了它们那里。确认每一次 stop，然后运行 `git status`，读一遍你即将发布的代码树。

**提交。** 放心地多提交。开 PR 之前 rebase 成小而有序的提交。每个提交都是一个未来的 PR：可落地、按顺序讲述故事。修复属于刚做的那个提交时用 amend。可以分开时用新提交。提交正文不复述标题。

**PR。** 提交前对 diff 跑 `/deslop`，review 前跑 `/no-comments`。每个 PR 标题、描述、提交正文都用 `/technical-writing` 写（除 Diátaxis 外的所有层级，并应用 STE 词汇规则：一个动作一个词，保留冠词，能用平实动词就不用 `-ing`），然后应用 `/unslop`。

**标题。** Conventional Commits 的 `type(scope): subject`，结尾没有句号。type 如 `feat`、`fix`、`docs`、`refactor`、`test`、`chore` 或 `perf`。scope 是领域，如 `pstack` 或 `poteto-mode`。subject 简短、祈使，且当某个真实符号承载了改动时点名它，例如 `fix(pstack): retarget opening-a-pr babysit trigger`。

**描述。** PR 正文是一份一分钟简报，不是实验记录本，读者是手里已有 diff 的 reviewer。它说清改动为什么存在、它刻意排除了什么、它可能破坏什么、你怎么证明了它有效。写短句、简单句，少放标识符，不要文字墙。正文会变成 squash 提交的正文，所以把那个提交控制在 40 行上下。使用 `##` 标题，不用加粗引导语，按这个顺序，没有内容可说的小节直接删掉：

- `## Why`：问题与方法，1-3 个短句。不放 SHA、rebase 家谱、或"基于 main"的开场白。
- `## What changed`：1-3 个短 bullet。只有当某个真实符号或路径承载改动时才点名它。重命名或重定向要提到两侧的名字。
- `## Scope`：必须有。1-3 个短条目，说它覆盖什么、刻意排除什么（一个 follow-up、一个已知缺口）。不放符号、路径、或逐文件的论述。
- `## Tradeoffs`：只写那些否则 reviewer 会追问的被拒备选方案。没有真正的选择时跳过。
- `## Blast Radius`：1-2 句，它触及谁或什么，以及为什么安全或有风险。如果 main 是红的，说明留它红的代价。
- `## Verification`：1-3 个 bullet，每个是一次真实的运行路径及其结果。性能：一个主数字带单位，`before → after`，其余给一个指向 arena 或 swarm 目录的链接。不放样本量方法论、swarm 逐 lane 的复述、或指标表格。

各小节之后，当视频或截图能证明一个主张时才附上。完整 SHA、swarm 或 arena lane 的复述、杠杆修正的长文、逐文件的 checklist、以及 "CLEAN" 裁决，放进一个链接的工件里，不放正文。

**Forge。** 在第一个 PR 操作之前解析 forge，并在 create、edit、view、watch、merge 中保持这个选择。GitHub CLI（`gh`）是默认值。如果 `command -v origin` 成功且 Origin 能解析这个仓库，优先用 `origin pr ...`。如果 Origin 缺席或无法解析这个仓库，留在 `gh` 上并记录这次降级。不要求 Graphite（`gt`）。

**内置 PR 工具。** 当运行环境提供了内置 PR 工具时，create、edit、retarget、mark ready 都走它，绝不走 forge CLI。CLI 建的 PR 会漏掉工具跟踪的内容。工具不覆盖的部分用解析出的 forge；运行环境没有这种工具时，所有 PR 操作都用 forge。

**规模与堆叠。** 五个窄的 PR 优于一个大 PR。堆叠是一条 base 分支链。根 PR 以 trunk 为目标。每个子分支 rebase 到其父分支的精确 tip，其 PR 以父分支为目标。父级合并后，按 `playbooks/shipping.md` 第 4 步把它的子级挪到 trunk 上。没有内置 PR 工具时，按解析出的 forge，用 `origin pr create --status open --base <parent-branch>` 或 `gh pr create --base <parent-branch>` 创建子 PR，用 `origin pr edit <pr> --base <parent-branch>` 或 `gh pr edit <pr> --base <parent-branch>` 重定向。只有独立工作才直接从 trunk 切分支。做大量堆叠工作之前先 rebase 到 trunk 上。

**就绪状态。** 每个 PR 都以 ready 状态打开，绝不开成 draft。内置 PR 工具可能默认 draft，所以通过它发起的每次创建都设 `draft: false`。用 Origin 时传 `--status open`。用 `gh` 时不传 `--draft`。如果一个 PR 仍被开成了 draft，通过 PR 工具标记 ready，或按解析出的 forge 运行 `origin pr ready <number>` 或 `gh pr ready <number>`。在引用 PR 状态之前先运行 `origin pr view <number>` 或 `gh pr view <number>`。

**Babysit。** 开 PR 不等于开始 babysit。贴出 URL，继续构建。先把阶段或整条堆叠做完。只有当整条堆叠已存在、用户又开口要求时，才单独跑一轮 babysit。每个新 PR 各配一个 babysit 会让构建停摆，还把检查次数花在后续波次会重启的提交上。反馈偏离了意图时顶回去。

开 PR 的子代理跑 `/deslop` 和 `/no-comments`，贴出 URL。它返回父级，不做 babysitting——除非它是 Autopilot-full 或 Autopilot-stack 的 owner。那个 owner 的简报派下了 babysit 循环，那正是 `playbooks/babysit.md` 在等的那个请求。owner 在自己的 code-ready 上报之后启动循环，上报 merge-ready，并豁免于本文件和 `playbooks/babysit.md` 中"整条堆叠建完才 babysit"的规则。
