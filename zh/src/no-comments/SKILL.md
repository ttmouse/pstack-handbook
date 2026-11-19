---
name: no-comments
description: "启动 comment-sicko 子代理，修复已采纳的发现，并为声称的约束提供编码方案。"
---

# No comments

在 Codex 上，先阅读[平台映射](../poteto-mode/references/codex-tools.md)（包括其中的各技能说明），再执行本技能。

在 GitHub Copilot 上，先阅读[平台映射](../poteto-mode/references/copilot-tools.md)（包括其中的各技能说明），再执行本技能。

在 Muse 上，先阅读[平台映射](../poteto-mode/references/muse-tools.md)（包括其中的各技能说明），再执行本技能。

在 Antigravity 上，先阅读[平台映射](../poteto-mode/references/agy-tools.md)（包括其中的各技能说明），再执行本技能。

启动 comment-sicko，对已采纳的发现采取行动。

尊重 comment-sicko 的新鲜视角。

## 范围

用调用方给的文件或 diff；否则用当前分支（默认 `main`）的 diff，含工作树。

## 步骤

1. 以 `subagent_type: "pstack:comment-sicko"` 启动 `Agent`，传入范围。按 **poteto-mode** 技能的 Subagents 章节，为每个子代理按任务选择推理力度。不要复述它的规则。

   `model` 设为 `pstack-models.md` 里 `no-comments reviewer` 那一行，表或该行缺失时用 [Models](#models) 的默认值。值为 `auto` 或 `inherit-parent` 时保持 `model` 不设。`Agent` 工具拒绝某个 slug 时，改用默认值并说明；拒绝默认值时，用错误信息里同一家族最接近的有效 slug。
2. 检查它的报告和 diff。拒绝：对应用代码的编辑、越出范围、异常保护式的删除、陈述失实的 `MUST KILL` 理由，以及把我们有意保留的代码当作罪证的标记。针对我们代码中意外情况的 flag 重塑后仍然有效。不要恢复那些注释。一条保留要成立，必须证明它针对的是我们无法改变的东西。审计漏掉的范围化 lint 和 TypeScript 抑制。正确性或安全类的抑制仍然是有效的 `MUST KILL`。只有异常精确且范围得到证明时才恢复删除。对理由单薄的 `IMPORTANT` 或 `do not remove` 的 kill/keep，先追溯其符号或对它跑 `/why`。kill 含糊时不恢复。keep 被驳倒或仍含糊就删掉。拒绝一次的报告：回滚，点明失败原因重跑一次；再被拒绝则报告为 open，`/no-comments` 对该报告中被拒的发现判失败，不对整轮判失败。

   `HOLD` 若点名了某个依赖、平台、供应商或协议的规则，并给出核对位置，就不算含糊的 keep：保持原位，报告为 open。其他任何 `HOLD` 都是含糊的 keep。拒绝这类规则的 kill，除非报告引用了驳倒该规则的文档页或源文件，或表明该规则约束的是别的东西。这类注释要作为 `HOLD` 恢复，即便含糊的 kill 本应保持删除。第二次被拒后，回滚其被拒的发现，然后用所有你已接受的发现完成第 3 到 6 步。
3. 琐碎的已接受标记直接修：删掉死路径、去掉参数、改用真实 API。任何修复需要造型时，对已接受的发现集合及周围代码跑一次 `/architect`，到草图为止。造型归 architect，实现归第 4 步。
4. 在范围内实现最小的根因修复。移除每一个被点名的 workaround。根因在范围外时，落在范围内最小的修复，其余报告为 open。**principle-fix-root-causes** 和 **principle-redesign-from-first-principles** 技能只指导意图，都不授权扩大围栏或修复围栏之外的实例。绝不打症状补丁。
5. 约束注释写着 `do not remove`、`do not change wording` 或 `talk to X before changing`。关于我们无法改变之物的保留才留下。提供范围内最便宜的类型、运行时、测试或 CI lint。等待交互式批准。无人值守和 eval 需要调用方预先批准。批准了就编码再删除；否则直接删除，约束报告为 open，并草图化范围外的工作。
6. 报告：删除数量、恢复的注释、`HOLD` 注释、重跑、architect 草图、修复、编码提议、已完成的编码、未强制的约束，以及其他未决工作。

## Models

各角色默认值，由 `plugins/pstack/models.json` 盖章生成（在彼处编辑，重跑 `tools/generate.mjs`）。`pstack-models.md` 覆盖表里匹配的角色行会在运行时覆盖各项；`/setup-pstack` 负责写入该表，并按运行时列出其路径。

- no-comments reviewer: `opus`

## Reasoning effort

覆盖表里的角色值可以在模型后面带上推理力度，如 `opus @xhigh`。Claude Code 上的档位：`low`、`medium`、`high`、`xhigh`、`max`。哪些档位可用取决于模型。不带 `@` 的值取表里的 `default effort` 行（一个档位或 `session`），表里没有该行时取 `session`。在 Claude Code 上，`session` 不设置力度。在其他运行时上，`session` 遵循平台映射。读取模型前先剥掉后缀：`inherit-parent` 或 `auto` 在每一层仍然省略 `model`，而模型名作为 `model` 传入。档位作为派发的 effort 字段传入，`subagent_type` 保持原样。Claude Code 的 `Agent` 调用上是 `effort`，Codex 的 `spawn_agent` 上是 `reasoning_effort`。在 Muse 上，它是 Workflow 子任务的 `effort`；`subagent_spawn` 派发保持会话的力度。
