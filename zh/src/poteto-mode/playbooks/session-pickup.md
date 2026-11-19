### Session pickup

**续接点归你。读前一条轨迹，不要重做它。**

1. 先按 [Resume storage](../references/resume-storage.md) 读项目检查点。读成功就直接拿到笔记和产物，不需要上一个会话给路径。指针缺失时，通过 Claude Code 每项目 transcript 目录下的本地 transcript 定位前一条轨迹：`${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/<encoded-cwd>/*.jsonl`（`node <plugin>/skills/reflect/scripts/claude-project-dir.mjs` 打印本会话的目录，其中就有在同一目录启动的更早会话；对在别处启动的那个，传入它的启动目录：`node <plugin>/skills/reflect/scripts/claude-project-dir.mjs "<start directory>"`。不要对 `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/projects/` 下其他目录做 glob——那会越过工作区边界，读到无关项目的私人聊天），或者通过一个云端代理 URL、一个已 push 的分支。检查点不可用或不完整时，需要诊断，而不是静默回退。走 transcript 回退时，先读元数据概览和最后几条消息，再回扫决策点。长 transcript 放到子代理里解析，还原后的时间线留在主线程（**principle-guard-the-context-window** 技能）。按 poteto-mode 的 Subagents 一节为每个子代理选合适的推理档位。
2. 重建运行状态。分支和工作树、什么已经落地（对照 base 跑 `git log`、`git diff`）、开着的 todo、已做的决策。用前一条轨迹恢复进度。涉及人类裁决的主张，在确切范围重要时，找到本人可归因的原话，附来源指针和发言人。代理摘要不是原始裁决；同一条摘要在多份笔记里的复本也只是同一条证据链。
3. 分清已完成与待办。把已发布的对照已计划的比较，指出续接点；不要重跑先前的 repro，不要重做已完成的工作。影响剩余工作的主张要复核，但不重复已完成的调查。读续接笔记链接的产物，包括被要求的问题或清单。
4. 在真实产物上对照原始目标验证继承来的主张（**principle-prove-it-works** 技能）。先前一次通过的自述不是证明。
5. 把剩余工作路由到匹配的 playbook 并选定裁决：继续执行、发布一份已完成的建议、批准或推翻先前的结论、或对失败的运行做事后复盘。Pickup playbook 到此为止。路由到的 playbook 接管其余。

**汇报：** 前一个代理停在哪、继承了什么 vs 重做了什么（理想情况是零重做）、续接点、以及结果。
