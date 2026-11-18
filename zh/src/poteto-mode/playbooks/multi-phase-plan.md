### 多阶段或多 PR 计划

通过 [poteto-mode 的 Non-negotiables](../SKILL.md#non-negotiables) 解析 driver skill。

**你拥有计划，不拥有代码。计划是一张 checklist，owner 逐框执行、操作者从证据审计。** 计划就是交付物。不要实现。

1. 当改动只有一两个文件、且路子显然时，跳过计划。说出来，然后停。
2. 写之前先用原型敲定开放问题。每个问题跑一遍 `playbooks/prototype.md`。保留分支、SHA 和截图给附录 A。只有任何运行都定不下来的产品或偏好抉择才问操作者。给出选项（**never-block-on-the-human** 原则 skill）。
3. 在子代理里探索，用 `subagent_type: "pstack:poteto-agent"` 并按 Subagents 一节指定显式模型（**guard-the-context-window** 原则 skill）。按 Subagents 一节为每个子代理挑选与任务匹配的推理档位。每个返回文件指针、约定、测试命令和入口点。不要内联转储。
4. 把下面的骨架复制进计划文件并填满每个占位符。除非操作者点名了路径，把文件写到 agent store（`~/.claude/orchestrate/<slug>/docs/`）之下。每个标题、每个子块都按给出的顺序保留。每个 PR 一节。一个 PR 是一个带自己证据的改动（**sequence-verifiable-units** 原则 skill）。在 **How to read this** 里点名执行 playbook（流程清单）。当一个 PR 构建在另一个 PR 之上时选 `playbooks/autopilot-stack.md`，当每个 PR 都独立成立时选 `playbooks/autopilot-full.md`。常设程序走 `playbooks/orchestrate.md`。执行 playbook 拥有基底选择、拓扑改动和合并权。不要把它的 rebase 步骤抄进计划。
5. 全文在 `/technical-writing` 下写作，然后 `/unslop`。正文是单一的 Diátaxis 模式：how-to。附录承载解释与参考。每个标题陈述任务或发现。不用长破折号。句中不用冒号。
6. 从已安装插件运行 `node skills/poteto-mode/scripts/check-plan.mjs <plan.md>` 并修掉它打印的每一行（**encode-lessons-in-structure** 原则 skill）。
7. 交回。贴出计划路径和脚本的输出，然后停。执行在操作者显式 go 之后开始，按计划点名的执行 playbook 进行。

**验证。** 只有测试不算充分的验证。一个 PR 只有当它的 unit、live、perf 框全部勾上才算验证过（**prove-it-works** 原则 skill）。这句话就是验证规则。每个验证块都以它开头。live 块是强制的。十条 lane 跑在配置的 `swarm workers` 模型上、位于 PR head，通过 driver skill 驱动真实表面，按 **swarm** skill。每条 lane 是一个框，含一个具体场景、它保存的截图、和它的通过谓词。其中一条 lane 是 **Regression lane against trunk。** 它在 trunk 和 head 上运行同一个承重场景。如果 trunk 没有这个 feature，这条 lane 记录这个事实，并对 diff 新增的行为加上用户等待的终态做闸门，而不是凭空造一个 trunk 结果。perf 闸门是双边的。trunk 和 head 都必须产出那个命名的指标。如果 trunk 缺这个 feature，还要把 diff 新增的工作单独隔离出来，为那份工作加绝对预算，再加上用户等待的端到端终态。不要在不像的场景之间宣称比值。perf 块点名指标、交错探测、先测的 trunk 基线、以及带失败数字的规则。改变交互的 PR 是 review-gated 的。操作者在合并之前于聊天里用截图和一段视频 review 它。不改变任何交互的 PR 写 `**Review gate.** None. <PR id> is not review-gated.`，且其下没有任何框。

**Driver skill。** 通过 Non-negotiables 选择它，并把解析出的 skill 路径或精确命令放进每条 live lane 的启动配方里。原生移动端用仓库里现成的模拟器驱动 skill。触及两个表面的 PR 在两个表面上都配 lane。没有 driver skill 的表面是附录 C 里的一个风险，它的 live 块仍要点名每条 lane 如何驱动它。

````markdown
# <Program> plan

<十行以内。改了什么、为谁、这个程序执行的规则是什么、以及按序的 PR id。>

## How to read this

一个框是一个工作单元。每个框都点名验证它的证据。嵌套的框是上方框的子步骤。只有当证据存在时才勾框——一个文件、一行日志、一张截图、一次测试运行、或一个 SHA。正文是 how-to。附录做解释和记录。

程序从已安装插件运行 `skills/poteto-mode/playbooks/<execution playbook>.md`。<谁来合并，哪些 PR id 是操作者的条目、会在 merge-ready 处停下。>

只有测试不算充分的验证。一个 PR 只有当它的 unit、live、perf 框全部勾上才算验证过。

## Program checklist

### Arm the program

- [ ] 向操作者陈述协议和本计划，然后停。只在操作者显式 go 之后开始执行。
- [ ] 得到操作者的 go 后，把这段原文写进程序 store 在 `~/.claude/orchestrate/<slug>/` 下的 `notes.md`，并在你的 todolist 里复述。"<计划路径、按序的 PR id、验证规则、谁合并、以及完成条件。>"
- [ ] 程序启动时从已安装插件读这些。每个 tick 都重读。
  - [ ] `skills/poteto-mode/playbooks/<execution playbook>.md`
  - [ ] `skills/swarm/SKILL.md`
  - [ ] `<driver skill path>`
  - [ ] `skills/poteto-mode/playbooks/opening-a-pr.md`
  - [ ] `skills/<程序用到的其他每个叶子 skill>/SKILL.md`
- [ ] 把每小时的审计 tick 武装成动态模式下的真实 `/loop`，它自己调度唤醒而不是阻塞在 sleep 上。绝不把节奏留给记忆。
- [ ] 逐字使用这个 tick 提示词。"从已安装插件重读执行 playbook，以及程序 store 里 `notes.md` 的目标。对照两者审计这次运作并在本 tick 内修复漂移。探测每条活跃 lane，只凭副作用判断进展。立即收兵卡死的 lane 并派出它的接替者。然后，仅当审计发现了此前没有状态消息报告过的被跟踪变化时——例如开了一个 PR、一个 code-ready head、一轮启动或收尾、一个裁决、一次合并、一个卡死代理及所采取的动作、一个新增或清除的阻塞、或一个只有操作者能做的决定——才在聊天里向操作者发一条简短的状态消息。点名每一个这样的变化，别的什么都不说。不要重复表格、已合并列表、或没变化的阻塞。如果审计什么都没发现，本轮就以无回复文本结束。无论哪种情况，都在你的决策轨迹里记下这个 tick 的行。行里写明报告了哪些条目，或 none。"
- [ ] 操作者 hold 或 stand-down 时，立刻向每个 owner 发送零写入指令。

### Spawn owners

- [ ] 每个 PR 派一个 owner，带执行 playbook 点名的完整生命周期。
- [ ] 遵循这个依赖图。只有当父级合并之后才启动被依赖的工作，或在执行 playbook 允许堆叠时基于父分支。
  - [ ] <PR id> 和 <PR id> 互相独立且最先。两者都从 `main` 切出。
  - [ ] <PR id> 在 <PR id> 之后。
- [ ] 守住文件边界。<PR id 或类别> 只触碰 `<glob>`。
- [ ] 守住 review 闸门。<PR id> 们改变交互。它们等待操作者在聊天里用截图和一段视频 review 之后才能合并。

### PR mechanics, for every PR

- [ ] 解析一次 forge。默认 `gh`；如果 `command -v origin` 成功且 Origin 能解析这个仓库，所有 PR 操作都用 `origin pr`。记录任何向 `gh` 的降级。绝不要求 `gt`。
- [ ] 按 **Opening a PR**，以 ready 状态开 PR，绝不开 draft。运行自带内置 PR 工具时用它，否则按解析出的 forge 用 `origin pr create --status open --base <base-branch>` 或 `gh pr create --base <base-branch>`。堆叠中的子 PR 以其父分支为目标。
- [ ] 在面向 PR 的 push 之前跑一次仓库的 lint 和 typecheck。带 hooks push。
- [ ] 每次提交前跑 `/deslop`，review 前跑 `/no-comments`。
- [ ] 按 `../references/bugbot-triage.md` 分诊每条 review 机器人和安全审查的评论。
- [ ] 在 code-ready 上报与 babysit 之前，以及 merge prep 之后再次，记录拓扑 owner 在执行 playbook 下准备好的 base 和 head SHA。

### Verdict and merge, for every PR

- [ ] 完整 swarm 只跑一次，在 code-ready head 上。只有新行为、重新设计、或大量新 diff 才再跑一次完整 swarm。rebase、合并冲突解决、或小修只需在新 head 上配一个 verifier，纯措辞改动则不需要。按 `skills/swarm/SKILL.md` 跑每次完整 swarm。一条闸门 lane。来自 PR **Verify, live** 块的十条 live lane。来自其 **Verify, perf** 块的 perf lane。两条或以上的审计 lane，各有各的焦点，读 diff 和凭据且不信任 PR 正文。根节点在裁决之前审计 merge-ready 报告里的凭据。
- [ ] 用执行 playbook 的阻塞规则评判每一条发现。没有发现阻塞时裁决为 clean。在标注了 `Regression lane against trunk.` 的 lane 里出现的 trunk 行为上的失败，记在 trunk 头上，不阻塞 PR。新 head 获得新裁决，但在 `playbooks/shipping.md` 的 patch-id 规则下仍然有效的结果除外。
- [ ] <来自执行 playbook 的合并或交接规则，带 `playbooks/shipping.md` 的 patch-id 规则。>

### Boot recipe, for every live lane

每条 live lane 在 PR head 上自己的工作树里运行。通过这个启动配方里记录的 skill 路径或精确命令驱动。

- [ ] `git fetch origin <head-branch> && git checkout <head SHA>`。
- [ ] <启动 backend 和表面。等待就绪。>
- [ ] <只通过 driver skill 的命令投递输入。点名只读的诊断。>
- [ ] 把每张截图保存到 `/tmp/swarm-<pr-id>/worker-<n>/<slug>.png`，并在报告里返回这些路径。

## <以动词短语表述的任务> (<PR id>)

**Depends on.** <PR id，或 None。>

**Files.**

- [ ] 编辑 `<path>`。
- [ ] 创建 `<path>`。
- [ ] 删除 `<path>`。

**Build.**

- [ ] <一个改动。点名符号和文件。>

**You see.**

- [ ] <一个可观察的结果，带精确的日志行或屏幕状态。>

**Verify, unit.** 只有测试不算充分的验证。一个 PR 只有当它的 unit、live、perf 框全部勾上才算验证过。

- [ ] <测试文件及它新增的用例。> 运行 `<command>`。

**Verify, live.** 只有测试不算充分的验证。一个 PR 只有当它的 unit、live、perf 框全部勾上才算验证过。十条 lane 跑在配置的 `swarm workers` 模型上、位于 PR head，按启动配方。

- [ ] Lane 1. Regression lane against trunk。在 trunk 和 head 上运行<同一个承重场景>。如果 trunk 缺这个 feature，记录这一点，并对<diff 新增的行为加上用户等待的终态>做闸门。保存 `<slug>.png`。<谓词>成立时通过。
- [ ] Lane 2. <场景。> 保存 `<slug>.png`。<谓词>成立时通过。
- [ ] Lane 3. <场景。> 保存 `<slug>.png`。<谓词>成立时通过。
- [ ] Lane 4. <场景。> 保存 `<slug>.png`。<谓词>成立时通过。
- [ ] Lane 5. <场景。> 保存 `<slug>.png`。<谓词>成立时通过。
- [ ] Lane 6. <场景。> 保存 `<slug>.png`。<谓词>成立时通过。
- [ ] Lane 7. <场景。> 保存 `<slug>.png`。<谓词>成立时通过。
- [ ] Lane 8. <场景。> 保存 `<slug>.png`。<谓词>成立时通过。
- [ ] Lane 9. <场景。> 保存 `<slug>.png`。<谓词>成立时通过。
- [ ] Lane 10. <场景。> 保存 `<slug>.png`。<谓词>成立时通过。

**Verify, perf.** 只有测试不算充分的验证。一个 PR 只有当它的 unit、live、perf 框全部勾上才算验证过。

- [ ] Metric. <在 trunk 和 head 两端测的是什么。如果 trunk 缺这个 feature，还要点名 diff 新增的工作和用户等待的端到端终态。>
- [ ] Probe. <命令或过程，在 trunk 和 head 上交错运行。两端都必须产出指标。>
- [ ] Baseline. 先记录 trunk 的 <值>。
- [ ] Rule. <head 对 trunk，带失败的那个数字。如果场景不像，为 diff 新增的工作和用户可见的终态加绝对预算，而不是给出无效的比值。>

**Review gate.** 操作者在合并前 review。

- [ ] 把 lane <n> 的截图复制到 `<media path>/<pr-id>-review-<slug>.png`。
- [ ] 在一条 lane 的工作树里录制一段 30 到 60 秒的改动视频。保存为 `<media path>/<pr-id>-review.mp4`。
- [ ] 在聊天里贴出截图和视频。停在 merge-ready。等待操作者的点击。

**Merge.**

- [ ] 根节点在精确的 head SHA 上给出 clean 裁决。
- [ ] Bugbot 分诊完成。
- [ ] Base 和裁决在执行 playbook 和 `playbooks/shipping.md` 的 patch-id 规则下都是最新的。
- [ ] <owner squash-merge 自己的 PR，或根节点把它追加到 base 分支堆叠、由操作者自底向上落地。>

## Close the program

- [ ] 上面的每个框都带着自己的证据勾上。
- [ ] 用执行 playbook 点名的报告回复操作者。

## Appendix A. Prototype evidence

<每个被原型回答了的开放问题，带分支、SHA 和工件链接。每个仍未被证明的问题。>

## Appendix B. Alternatives rejected

<每个被权衡过的方法，以及它为什么输了。>

## Appendix C. Risks

<每个风险，落在哪个 PR 里，owner 盯着什么。>

## Appendix D. Links and reading list

<编辑之前要读的文档。哪些 PR 会得到 `skills/how/SKILL.md` 和 `skills/interrogate/SKILL.md`。按 `skills/show-me-your-work/SKILL.md` 的轨迹。>
````

**回复：** 计划路径、各 PR id 及其依赖与 review-gated 集合、原型证明了什么、什么仍未被证明，以及检查脚本的输出。
