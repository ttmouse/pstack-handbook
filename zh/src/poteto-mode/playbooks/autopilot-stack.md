### Autopilot-stack

运行 Autopilot-full playbook（流程清单），但不合并。

1. **以第 5 步的位置替换为：停在 verified。** 当每个 PR 在其当前 head 上已验证且全绿时停下，然后把 PR 们交给操作者。交接之后，任何人不得在未经操作者 go 的情况下 push。每个 loop tick 的提示词都点名这个文件，所以每个 tick 都能看到禁止合并的规则。
2. **只有当一个 PR 构建在另一个 PR 之上时才堆叠它。** 这是对第 3 步的唯一例外。让这个 PR 基于另一个 PR 的分支而非 trunk，按 `playbooks/opening-a-pr.md` 的 **Size and stacks**。以第 2 步的 rebase 到 trunk 替换为：每个 PR rebase 到其父 PR 的分支，堆叠的根 PR rebase 到 trunk。下层 PR 出现新 head 时，重新堆叠位于其上的 PR，而 restack 后 `git patch-id` 不变的 PR 保留其裁决。在任何 restack 之前，遵循 [Merge and restack safety](../references/merge-safety.md)：捕获受影响的链及其远端 head，取消该链的 auto-merge 请求和队列成员资格，核实取消成功，然后用 `--force-with-lease=refs/heads/<branch>:<captured-remote-head>` push。记录每个裁决的 head SHA、base SHA、base 分支和 patch-id，并把裁决可能不再适用于新基底的 PR 送回验证。

**回复：** 列出每个 PR 及其裁决，以此替换"哪些已 merge-ready 等待操作者点击"。
