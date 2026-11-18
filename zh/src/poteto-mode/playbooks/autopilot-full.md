### Autopilot-full

通过 [poteto-mode 的 Non-negotiables](../SKILL.md#non-negotiables) 解析 driver skill。

**你拥有裁决权，绝不拥有 PR。每个 PR 由唯一一个 owner 从构建一路带到 merge-ready，且在你的 swarm——它从未写过这些代码——证明将要落地的代码、并且操作者点了合并之前，什么都不会合并。**

一个裁决覆盖一个 patch，一次绿色 CI 覆盖一个 head。第 4 步运行一次完整 swarm，且只在出现重大改动时再运行。`playbooks/shipping.md` 的 patch-id 规则可以让一个 lane 的结果继续有效，而每个新 head 都需要自己的绿色 CI。

1. **操作者的闸门优先。** 授权只覆盖队列里的条目，所以操作者声明归自己的条目以及队列之外的 PR 在 merge-ready 处停下。要求陈述计划的请求不是放行指令。得到操作者的 go 之后，把完整的程序目标写进程序 store 在 `~/.claude/orchestrate/<slug>/` 下的 `notes.md`，并在你的 todolist 里复述一遍，让它在队列完成之前跨轮次持续有效。在第一个 owner 启动之前，告诉操作者这个程序的规模：owner 数量、第一轮的 verifier lane 数，以及第 4 步里每个 PR 最多两次 fix-forward 的上限。超过三个 owner 的程序要等操作者对这个规模的 go，除非操作者的请求已经点明了这个规模。
2. **每个 PR 派一个 owner，并把它的工作放在接替者能找到的地方。** 为整个程序解析一次 forge。GitHub CLI（`gh`）是默认值。如果 `command -v origin` 成功且 Origin 能解析这个仓库，所有 PR 操作都用 `origin pr`。否则留在 `gh` 上并记录这次降级。绝不要求 Graphite（`gt`）。每个 owner 是一个在自家工作树里运行的后台子代理，它负责构建、按 `playbooks/opening-a-pr.md` 开 PR、在真实工件上证明改动、按 `playbooks/babysit.md` 把它盯到全绿，并在第 4、5 步放行后在 merge-ready 处交出 PR。没有 owner 执行合并。

   尽早开 PR，让 CI 和机器人与开发工作并行。代码只有在跑过 slop-strip（**deslop** skill，`/deslop`）和 `/no-comments` 一轮之后才算就绪，所以完整 swarm 跑在完成的代码上。然后在自证之前 rebase 到当前 trunk 并上报 code-ready head，让验证跑在 patch 将要落地的基底上。之后每次后续 head 都要上报，自证、CI、babysit 全部完成后上报 merge-ready。修复轮次保持在那个基底上，除非 trunk 冲突、破坏 CI、或落地了对同一批文件的已知并发改动，因为每次 rebase 都会重启 CI。在 code-ready push 之前、以及在需要 verifier 的后续 push 之前，对被触及路径运行仓库的检查。

   假设 owner 的会话会死。启动后不久就 push，并按 **show-me-your-work** skill 在程序 store 的 `~/.claude/orchestrate/<slug>/` 下开启一条决策轨迹，然后每完成一个单元就先 push 再开始下一个。谁派生了子代理，谁就在这个 store 里记录它的 id、状态，以及从同类过去运行中得出的一条 stuck-after 时长，这样根节点就能在父节点死掉时探测它。只 force-push 你自己的分支，`--force-with-lease` 钉在你最后一次 push 或接手时的 SHA 上；遇到任何不是你做的 push，停下来向根节点上报。
3. **让 owner 们并行地基于 trunk 运行，绝不堆叠**，这样每个 PR 各自独立落地。
4. **Swarm 验证一次。** 完整 swarm 只跑一次，在 code-ready head 上。只有新行为、重新设计、或大量新 diff 才再跑一次完整 swarm。rebase、合并冲突解决、或小修只需在新 head 上配一个 verifier，纯措辞改动则不需要。按 **swarm** skill 在 code-ready SHA 上扇出互相独立的 verifier。它们重跑各道闸门、通过 driver skill 在真实表面上活体验证承重行为、并审计 diff。没有活体 lane，或在你审计 merge-ready 报告的凭据之前，裁决都不算干净，因为没有哪条 lane 信任一个它自己没检查过的主张。

   只有能展示出来的问题才能挡住一个 PR：head 上的一次失败运行，或被这个 PR 改错的一行文档。PR 的基底——无论是 trunk 还是堆叠里位于它下面的那个 PR——本来就有的问题不挡，除非这个 PR 复制了它或新触达了它。只有用户会碰到的 bug、失败的闸门、或被改错的已发布文档才挡，其余全部进 follow-up。

   给每条 review lane 的简报都要求报告这个 diff 破坏了什么，而不是它触及的文件里所有错误的东西；除非操作者要求，否则不要发起任何 mutation 或 fuzz 攻势。每个 PR 两次 fix-forward 是上限。当一条阻塞性发现撑过了第二次，停止那个 PR 上的工作，连同发现和证据一起上报它被阻塞，让操作者选择再来一轮、缩小 PR 范围、或关闭它。
5. **操作者只合并你验证过、且在它将落地的 trunk 上测试过的东西。** 绿色 CI 本身永远不构成合并授权，你的干净裁决是操作者点击的前置条件，永远不是它的替代品。一旦 swarm 的 lane 开始跑，merge prep 就 rebase 到当前 trunk、上报新 head、并等待绿色 CI。

   在交接之前，fetch trunk 并问它带来的改动是否可能影响这个 patch，因为为每一次 trunk 变动都 rebase 是没有尽头的。当代码从未在将要落地的形态上被测过时——例如冲突、双方都改了同一个文件、或改变了这个 PR 跑哪些检查——rebase 并等待 CI。双方都改了 lockfile 时，如果一次冻结安装（frozen install）在合并结果上通过、且这个 PR 改动的包在那里解析出的结果与 head 上一致，就不需要 rebase，因为这次安装测的就是将要落地的 lockfile，而安装失败则意味着必须由 rebase 来修复它。当 trunk 改动了 patch 的某个调用方、或 patch 依赖的东西（例如它调用的代码或某个依赖版本）时，在合并结果上运行这个 patch 的检查并在通过后交接。否则直接交接。如果 trunk 会在 merge prep 之后强推第三次 rebase，暂停并向根节点上报，由根节点来排序相撞的工作。

   owner 带着裁决和钉住的 head SHA 向操作者呈现 merge-ready 的 PR，然后返回，一个新的 owner 按 poteto-mode 的 Subagents 一节接手下一个条目。如果 trunk 在操作者合并之前又动了，`playbooks/shipping.md` 的 patch-id 规则决定是否重新验证。
6. **运行根节点这一层。** 任何放宽闸门的东西——比如提高预算或加一条 allowlist——都需要一个 verifier 的证明，然后再加上你新签署的会签（countersign），因为 owner 正是那个想要绿色的人。在授权覆盖审批的情况下，那次会签就是审批本身，owner 对它的记录指向你的会签，供某条 lane 去核查。被禁用或软失败的检查一定会被移出来，因为它不再守护任何用例。绝不给予或绕过 forge 强制要求的审批，因为没有会签能覆盖它。

   得到操作者的 go 后，把每小时的审计 tick 武装成一个动态模式下的真实 `/loop`，它自己调度唤醒而不是阻塞在 sleep 上，并保持到没有任何被委托的工作为止，因为长运行会漂移、代理会无声地卡死。每个 tick 都从已安装插件下的磁盘重读本 playbook，以及 store 里 `notes.md` 中的目标，并修复漂移——例如一个未上报的 head 或一个未登记的代理——方式是让它的 owner 把它记录下来，因为漂移是记录的缺口，不是停摆。它探测每一个代理，直到叶子 lane，并按副作用来判断每一个，因为状态文本和摘要能藏住一个卡死的孩子。一个代理在出错、无法启动轮次、或超过它的 stuck-after 时长仍无新动静时即为卡死，因此一个在第一个 tick 时既没 push 也没写轨迹行的 owner 也是卡死。在等你或操作者的那一个不算卡死，所以去回答它。立刻替换卡死的代理，不等它的 stop 落地。某个 tick 为操作者改变了什么，就以 **ketchup** skill 收尾向他们汇报；什么都没变的 tick 保持安静。
7. **操作者叫停时立即收兵。** 一道 hold 以零写入指令的形式到达每个 owner。每个人报告自己当前的状态，并保持各自的简报，直到操作者释放它们。

**回复：** 按 **ketchup** skill 向操作者汇报，覆盖每个 PR 的状态和裁决、哪些已 merge-ready 等待操作者点击、会签及其理由、仍开着的操作者闸门、以及被搁置的 follow-up，附上每个 PR 和轨迹的链接。
