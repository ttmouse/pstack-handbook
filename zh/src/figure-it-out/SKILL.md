---
name: figure-it-out
description: "没有更窄的 playbook 适用时，设计一份可审计的 playbook：大型迁移、雄心勃勃的多部分改动，或人类离开一段时间后回来评审的工作。按任务伸缩严格度，跑假设循环，记录决策。用于 /figure-it-out 或 'figure it out'。"
---

# Figure it out

任务对不上任何 playbook 时，自己设计一个。写任何代码之前的交付物就是工作流本身：一串按任务伸缩严格度的阶段，跑一遍科学方法，留下一份人类离开后回来还能审计的决策轨迹。

## Start

开一个 todolist，第一项是读 **poteto-mode** 技能的 Principles 一节。然后把下面的阶段加为 todo。

## Phase A: Frame

先落实事实，再承诺。说不出下面这些就不要开跑：

- 完成的定义，写成一个可证伪的谓词（**prove-it-works** 原则技能）。
- 量化的范围：粗略的单位和工作量，加上落实事实时暴露的阻塞项。
- 严格度级别，偏高取。单向门和高爆炸半径的多给，可逆的低风险步骤少给。严格度是门禁和产物，不是"更努力"。

承诺一次长跑之前，先呈现界定和取舍。可逆的工作直接推进（**never-block-on-the-human** 原则技能），但一次数小时的运行值得设置一个检查点。

## Phase B: Design the workflow

分解成原子的、可独立落地的单元。按风险最大的未知排最前。脚手架和验证先于功能（**foundational-thinking** 原则技能）。

- 先建验证测试台再干活，基线从改动前状态采集，让检查读出来是"旧值 vs 新值"。
- 单向门的设计决策，跑 **architect** 技能（它会跑 **arena**）。形状已经具体的机械活跳过。给已定稿的设计再跑一轮 arena 是过度工程（**laziness-protocol** 原则技能）。
- 决定哪些部分分发。只在接缝处并行，每个 worker 给自己的工作树或分支（**separate-before-serializing-shared-state** 原则技能）。不要过度分发。每个子代理的推理强度按活儿来定，依据 **poteto-mode** 技能的 Subagents 一节。
- 把设计好的阶段清单写下来。人类评审的就是这份清单。

然后执行设计。把它的步骤作为具体条目插进 todolist 的 Phase C 和 Phase D 条目之间。每一步都在 Phase C 的循环纪律下运行，并把 Phase D 的日志穿插进去——每落地一步记一行——而不是把整条轨迹留到最后。

## Phase C: Run the loop

每个单元都是一次实验。陈述假设，做最小的改动，对照谓词在真实产物上测量，有进步就保留，没有就回滚。套用 **sequence-verifiable-units** 原则技能：每个单元先验证再开始下一个，不把检查攒到最后一起做。

- 靠检查产物验证，绝不靠自我汇报。某个东西过得太容易时，先怀疑观察方法，再怀疑系统。
- 委派出去的活配一个裁判。worker 想骗过门禁，就重置并加固契约。门禁本身错了，就在独立的改动里修门禁，而不是绕开它。
- 结论只有 VERIFIED、NOT VERIFIED 或 INCONCLUSIVE。INCONCLUSIVE 不是通过。不隐藏否定结果。

## Phase D: Keep the audit trail

用 **show-me-your-work** 技能记录这次运行。figure-it-out 的活通常够大，值得把轨迹提交进去，让评审者在 PR 里就能读到。轨迹加 diff，才是人类回来之后能信任这份工作的东西。

## Phase E: Verify and hand back

对照 Phase A 的谓词在真实产品上核查整体，不只是测试台。任何反复出现的纠正，编码成门禁、lint 规则、检查或脚本（**encode-lessons-in-structure** 原则技能）。

**Reply:** 你设计的 playbook、严格度级别及理由、决策轨迹路径、对照谓词已验证什么、还有什么未决。
