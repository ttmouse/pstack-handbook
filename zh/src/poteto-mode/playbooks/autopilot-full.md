### Autopilot-full

通过 [poteto-mode 的 Non-negotiables](../SKILL.md#non-negotiables) 解析 driver skill。

**裁决归你，PR 归操作者。每个 PR 由唯一一个 owner 从构建一路带到 merge-ready，而在你的 swarm——它从不写代码——证明即将落地的代码、且操作者亲手点了合并之前，任何东西都不合并。**

一份裁决只覆盖一个补丁，一次绿 CI 只覆盖一个 head。步骤 4 全量跑一次 swarm，之后只有重大变更才重跑。`playbooks/shipping.md` 的 patch-id 规则可以让一条 lane 的结果继续有效，而每个新 head 都需要自己的绿 CI。

1. **操作者的闸门优先。** 授权只覆盖队列里的条目，所以操作者声明属于自己的条目和队列外的 PR 一律停在 merge-ready。要求陈述计划不等于放行。操作者放行后，把完整的程序目标写进程序仓库 `~/.claude/orchestrate/<slug>/` 下的 `notes.md`，并复述进你的 todolist，让它在跨轮次之间始终成立，直到队列清空。第一个 owner 启动前，向操作者报出程序规模：owner 数量、第一轮验证 lane 的数量、以及步骤 4 的「每个 PR 最多两次 fix-forward」上限。owner 超过三个的程序，要等操作者对这个规模的放行，除非操作者的请求里已经点明了规模。
2. **每个 PR 起一个 owner，并把它的工作放在接班人找得到的地方。** 整个程序只解析一次 forge。GitHub CLI（`gh`）是默认。如果 `command -v origin` 成功且 Origin 能解析该仓库，所有 PR 操作走 `origin pr`。否则留在 `gh` 并记录这个回退。绝不要求 Graphite（`gt`）。每个 owner 是一个后台子代理，跑在自己的工作树里：按 `playbooks/opening-a-pr.md` 开 PR、在真实产物上证明改动、按 `playbooks/babysit.md` 推到绿、在步骤 4 和 5 放行后把 PR 交接到 merge-ready。没有任何 owner 执行合并。playbook 里凡是说「报告一次 rebase」的地方，owner 自己 rebase 自己的分支，并用 `git push --force-with-lease` 发布。

   PR 要早开，让 CI 和机器人与开发并行。代码只有在跑完去 slop（**deslop** 技能，`/deslop`）和 `/no-comments` 清理之后才算就绪，所以完整 swarm 跑在成品代码上。然后在自证之前 rebase 到当前 trunk 并报告 code-ready head，让验证跑在补丁真正落地的基线上。之后每个 head 都要报告；自证、CI、babysit 都完成后报告 merge-ready。修复轮次继续留在该基线上，除非 trunk 有冲突、破坏了 CI、或落地了一个已知的对同文件的并发变更——因为每次 rebase 都会重启 CI。在 code-ready push 之前，以及任何后续需要验证器的 push 之前，先在已提交的 head 上对被触碰路径跑仓库的检查。

   按「owner 会话随时会死」来设防。启动后尽快 push，并按 **show-me-your-work** 技能在程序仓库 `~/.claude/orchestrate/<slug>/` 下开一条决策轨迹，然后每完成一个单元先 push 再开始下一个。谁起的子代理，谁就在该仓库里记录它的 id、状态、以及按同类过往运行得出的 stuck-after 运行时长，这样根节点在父代理死后还能探测它。只 force-push 自己的分支，且 `--force-with-lease` 钉在你最后一次 push 或接管的 SHA 上；遇到任何不是你做的 push，停下来向根节点报告。
3. **多个 owner 从 trunk 并行跑，绝不叠加**，让每个 PR 各自落地。
4. **Swarm 验证一次。** 全量 swarm 在 code-ready head 上跑一次。只有新行为、重新设计、或大幅新增 diff 才再跑一次全量。rebase、合并冲突解决、小修只需在新 head 上跑单个验证器；纯措辞变更什么都不用跑。按 **swarm** 技能在 code-ready SHA 上扇出相互独立的验证器。它们重跑各道闸门、通过 driver skill 在真实界面上活体验证承载性行为、并审计 diff。没有活体验证 lane，或者还没审计 merge-ready 报告的凭证，裁决就不算干净——因为没有任何 lane 信任一个自己没查过的断言。

   只为「你能展示出来的问题」挡 PR：head 上一次失败的运行，或 PR 弄错的一句文档。PR 基线上已有的问题——无论在 trunk 还是在 stack 里它下面的 PR——不挡，除非这个 PR 复制了它或新触达了它。只有用户会撞上的 bug、失败的闸门、或已发布的错误文档才挡，其他都进 follow-up。

   给每个评审 lane 的指令都是：报告这个 diff 破坏了什么，而不是它触碰的文件里所有错误的东西；除非操作者要求，不要发起 mutation 或 fuzz 攻势。每个 PR 的 fix-forward 上限是两次。当阻断性发现在第二次之后仍然成立，停止该 PR 的工作，带着发现和证据报告为 blocked，让操作者选择再来一轮、收窄 PR、或关闭它。
5. **操作者只合并你验证过、且在它将落地的 trunk 上测过的东西。** 绿 CI 单独永远不构成合并授权；你的干净裁决是操作者点击的前置条件，永远不是替代品。swarm 的 lane 启动后，合并准备阶段 rebase 到当前 trunk，报告新 head，等绿 CI。

   交接前，fetch trunk 并判断它的变更是否可能影响补丁——因为为 trunk 的每次移动都 rebase 是没有尽头的。当将要落地的代码从未被测过时——冲突、双方都改了同一文件、或改动了该 PR 跑哪些检查——rebase 并等 CI。双方都改了 lockfile 时，如果一次 frozen install 在合并结果上通过、且该 PR 改动的包解析结果与 head 一致，就不必 rebase：因为这次 install 测的就是将要落地的 lockfile，而 install 失败则必须通过 rebase 修复。当 trunk 改动了补丁的某个调用方、或补丁依赖的东西（它调用的代码、依赖版本），在合并结果上跑补丁的检查并通过后交接。否则直接交接。如果 trunk 会逼出第三次超出合并准备范围的 rebase，停下并向根节点报告，由根节点为冲突的工作排序。

   owner 携带裁决和钉住的 head SHA，把 merge-ready 的 PR 呈给操作者，然后返回，按 poteto-mode 的 Subagents 一节由新 owner 接下一个条目。如果操作者合并前 trunk 又动了，`playbooks/shipping.md` 的 patch-id 规则决定要不要重新验证。
6. **根层由你运行。** 任何放松闸门的事——提高预算、加 allowlist 条目——都需要一个验证器的证明，然后再加上你的新鲜会签，因为 owner 正是那个想看到绿色的人。在授权覆盖审批的情况下，这个会签就是那次审批，owner 对它的记录指向你的会签，供某条 lane 检查。被禁用或软失败的检查一定会被移除，因为它不再守护任何用例。绝不给予或绕过 forge 强制要求的审批，因为没有任何会签能覆盖它。

   操作者放行后，用真实 `/loop` 的动态模式布防一个每小时的审计 tick（它自己调度唤醒而不是阻塞在 sleep 上），直到没有遗留的委托工作才撤防，因为长任务会漂移、代理会无声卡死。每个 tick 从磁盘上已安装插件重读本 playbook、从仓库的 `notes.md` 重读目标，并修复漂移——比如一个未报告的 head 或一个未登记的代理——方式是让它的 owner 补上记录，因为漂移是记录缺口，不是停滞。它探测每个代理直到叶子 lane，并按副作用来判定每个代理，因为状态文本和摘要可能藏住一个卡死的孩子。一个代理报错、无法开始轮次、或超过其 stuck-after 运行时长仍无新东西，即为卡死；一个 owner 到第一个 tick 时既没 push 也没写轨迹行，同样算卡死。在等你或操作者的代理不算卡死——去回答它。卡死的代理立即替换，不等它的 stop 落地。给操作者带来了变化的 tick，结尾按 **ketchup** 技能向其同步；什么都没变的 tick 保持安静。
7. **操作者喊停就立刻停。** 一个 hold 以「零写入」命令的形式到达每个 owner。各自报告当前进度，并保持原任务直到操作者解除。

**汇报：** 按 **ketchup** 技能向操作者同步：每个 PR 的状态和裁决、哪些已 merge-ready 等操作者点击、会签及其理由、仍开着的操作者闸门、搁置的 follow-up，并附每个 PR 和决策轨迹的链接。
