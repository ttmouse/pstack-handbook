### 会话接管

**你拥有的是恢复点。读前人的轨迹，不要重做它。**

1. 先按 [Resume storage](../references/resume-storage.md) 读项目检查点。一次成功的读取直接给出笔记和产物，不需要上个会话提供路径。指针缺失时，通过本地 transcript 找前人轨迹，位置在 Claude Code 的按项目 transcript 目录 `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/<encoded-cwd>/*.jsonl`（`node <plugin>/skills/reflect/scripts/claude-project-dir.mjs` 打印本会话的目录，里面存着在同一目录启动的更早会话。对起始于别处的会话，传入其起始目录：`node <plugin>/skills/reflect/scripts/claude-project-dir.mjs "<start directory>"`。不要在 `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/` 下的其他目录里 glob，那会越过工作区边界、读到无关项目的私人聊天），或一个云端代理 URL，或一个已推送的分支。检查点不可用或不完整需要诊断，而不是静默回退。走 transcript 回退时，先读元数据概览和最后的消息，再回扫决策点。长 transcript 在子代理里解析，把还原出的时间线留在主线程（**principle-guard-the-context-window** 技能）。按 Subagents 一节，为这份工作选子代理的推理等级。
2. 重建操作性状态。分支和工作树、什么已经落了（`git log`、对基线的 `git diff`）、打开的 todo、已做的决策。用前人轨迹恢复进度。对人类裁决的断言，遵循 [Claims about human decisions](../../why/references/epistemics.md#claims-about-human-decisions)。代理的总结不是原始裁决。
3. 对比已完成与待办。把已交付的对照计划过的比较，指名恢复点，不重跑前人的复现、不重做已完成的工作。对影响剩余工作的断言做复查，但不重复已完成的调查。读恢复笔记链接的产物，包括被要求保留的问题或清单。
4. 把剩余工作路由到匹配的 playbook（流程清单）并选定裁决：继续执行、交付一份已完成的推荐、批准或推翻先前结论，或对一次失败的运行做事后分析。接管 playbook 到此为止。被路由到的 playbook 负责其余部分。
5. 在真实产物上对照最初目标验证继承来的断言（**principle-prove-it-works** 技能）。先前的一次通过自报不是证明。

**汇报：** 前一个代理停在哪里、你继承了什么又重做了什么（理想情况是什么都没重做）、恢复点、以及结果。
