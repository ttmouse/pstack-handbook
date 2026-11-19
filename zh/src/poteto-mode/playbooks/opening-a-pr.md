### Opening a PR

在其他每本 playbook 的结尾被调用。

从 trunk 之外的一个 git 工作树出发，不把无关工作混进来。rebase 成少量可落地的提交。提交前对 diff 跑 `/deslop`。在任何从工作树发起的 commit、merge、deploy 之前，列出所有活着的 agent，停掉每一个持有这棵树的——包括不是你启动的孙辈。确认每个都已停止，然后跑 `git status`，读一遍即将发布的树。

标题：`type(scope): subject`，有承载改动的真实符号就写上。正文：一份一分钟简报，40 行以内，按顺序用这些 `##` 标题，空的可省：`## Why`、`## What changed`、`## Scope`、`## Tradeoffs`（只写评审人否则会追问的被拒方案）、`## Blast Radius`、`## Verification`。

后续工作按 base 分支 stack。直接开 ready 状态的 PR，通过本次运行的 PR 工具，`draft: false`。没有这个工具就用 `gh pr create` 不带 `--draft`，或 Origin 的 CLI 能解析仓库时用 `origin pr create --status open`。开 PR 不等于开始 babysit。
