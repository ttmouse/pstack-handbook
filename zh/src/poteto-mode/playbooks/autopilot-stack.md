### Autopilot-stack

跑 Autopilot-full playbook，但不合并。

1. **用本步替换步骤 5：验证完就停。** 每个 PR 在当前 head 上验证通过且 CI 绿之后停下，把 PR 交给操作者。交接之后，没有操作者的放行任何人都不得 push。每个 loop tick 的提示词都会点名这个文件，所以每个 tick 都能看到这条禁合并规则。
2. **只有 PR 依赖于另一个 PR 时才 stack。** 这是对步骤 3 的唯一例外。把 PR 的 base 设为另一个 PR 的分支而不是 trunk，按 `playbooks/opening-a-pr.md`。以「每个 PR rebase 到其父 PR 的分支、stack 根 rebase 到 trunk」取代步骤 2 的 rebase 到 trunk。下方 PR 的新 head 会重新 stack 上方的 PR，而 restack 后 `git patch-id` 不变的 PR 保留其裁决。任何 restack 之前，遵循 [Merge and restack safety](../references/merge-safety.md)：捕获受影响的链及其远端 head，取消该链的 auto-merge 请求和队列成员资格，核实取消成功，再用 `--force-with-lease=refs/heads/<branch>:<captured-remote-head>` push。记录每份裁决的 head SHA、base SHA、base 分支和 patch-id；一份裁决可能不再适用于新 base 的 PR，要重新送回验证。

**汇报：** 逐个列出每个 PR 及其裁决，取代 Autopilot-full 中「哪些已 merge-ready 等操作者点击」的部分。
