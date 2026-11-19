本页译文已从 0.9.129 全量同步到 **0.9.142**（2026-11-19 发布）。对你学习影响最大的变化：

**技能大幅瘦身（0.9.140）**

- **how / why / reflect** 各自缩成一个短文件：how 现在只派一个只读子代理然后呈现答案；why 直接从代码背后的 commit 和 PR 讨论里找答案；reflect 自己读会话记录、不再派评审子代理。原来的参考提示词和多来源流程全部删除。
- **architect** 从五阶段流程缩成一页简报：穷举改动触碰的每个系统、画两种形状、选「每份状态只有一个主人」的那种；大设计或争议设计直接交给 arena 跑。
- **14 条原则**和 unslop、technical-writing 正文变短，但规则本身一条没删。
- **poteto-mode** 总管也精简了：不再把任务路由给 how，触发清单缩到 13 行，Comments 一节删除（no-comments 仍然在评审前运行）。

**结构变化**

- **新增 worker.md**（总管目录下）：把操作员规则带给每个被派起的子代理，每次开工提示的第一行就指向它。本页总管分组里已收录。
- **Orchestrate playbook 被删除**：程序级（跨天、多 PR）的工作改路由到 figure-it-out。因此本页 playbook 编号 **17 空缺**，其余编号保持与学习手册一致。
- **Babysit、Opening a PR、Multi-phase plan 三本清单砍到几条规则**；Multi-phase plan 不再运行 check-plan.mjs 脚本。
- **角色收缩**：how explorer、how explainer、why investigators、why synthesizer、reflect 系列、architect runners 七个模型角色删除，setup-pstack 下次运行会自动从模型表清掉对应行。xhigh 以上强度必须在模型表显式指定；「第二意见」和 show-me-your-work 的评审者改用异族模型。

**新增运行时支持（0.9.130）**：Kimi Code CLI、Grok Build、OMP、OpenCode 2 都有了原生插件，各自的工具映射在 poteto-mode 的 references 里。

**工程修复（0.9.131–0.9.142，不影响学习内容）**：worktree 审计多处修复（远程领先/落后计数、子模块、压缩的 Codex 会话记录）、check-playbooks 支持 YAML 引号和无编号步骤的基清单、watch-pr 不再把等待审批的 fork CI 误判为「没有 CI」、OMP 上验证技能写到 .omp/skills/。

术语与本页开头「翻译说明」一致：playbook、技能名、命令、路径保留英文。各文档右侧的「解读」按 0.9.142 内容撰写；learn 手册（英文页）仍基于 0.9.129，读到与本页不一致处，以本页新译文为准。
