---
name: technical-writing
description: "分层技术写作标准：Diátaxis 结构、Google 开发者风格句子、STE 指令规则、Global English 句法。用于 /technical-writing，或撰写和评审文档、RFC、readme、PR 描述、commit message。"
---

# 技术写作

让疲惫的工程师第一遍就能读懂。四层全部应用。

三条规则凌驾于各层之上：

- **砍掉每个不干活的词。**句子去掉一个词还能活，这个词就去掉。「In order to」就是「to」。「It is important to note that」什么都不是。
- **用短的日常词。**「Use」，不是「utilize」。「Help」，不是「facilitate」。「Do」，不是「perform」。长词必须用精确性来换取它的长度。
- **当一条规则让句子变糟时，换个方式修句子，或者别动它。**一条每条规则都遵守、读起来却像机器写的句子，就是失败。

代码库就是词表。写真实的符号、文件、flag 或命令名，不要写同义词或对它的描述。

不要发明行话。用开发者会脱口而出的词：「move」「delete」「a budget that only decreases」，而不是「evacuate」「ratchet」「endgame」。文档第一次提到某个命名模式时说明它的含义，就是可以接受的。在你回复中把新的违规词及其替换作为对 `unslop` 的 abstract-metaphor 规则的补充提案提出，附 diff。不要编辑那个技能。

## 变换节奏

一份文档可以遵守所有层、读起来仍像机器写的：每句都短促，没有任何观点，没有任何具体的东西。

- 刻意混合句子长度。短句落定一个要点。长句承载一个事实连同它的条件或后果。
- 一句一个想法不等于每句一个长度。拆开承载两个想法的句子。保留承载一个想法的长句。
- 在模式允许的地方带上观点。Explanation 权衡取舍，所以说出你怎么看，而不是罗列正反两面。Reference 保持干燥。
- 具体胜过空洞。不是「schema changes can cause issues」，而是「a column rename fails the build」。

## 先选模式（Diátaxis）

一份文档，一个模式。两个问题决定它：内容是服务行动（做）还是理解（想），以及它服务学习还是工作？

- 行动 + 学习：**tutorial**。
- 行动 + 工作：**how-to**。
- 理解 + 工作：**reference**。
- 理解 + 学习：**explanation**。

这个罗盘可以用于整份文档，也可以用于一句话。

**Tutorial：在做中学。**学习者的成功是你的职责，不是他们的。开篇说学习者将做出什么，而不是他们将「学到」什么。每一步都产出可见结果，早点且频繁。告诉他们应当看到什么：预期输出、prompt 变化、日志行。解释压缩到一个从句加一个链接。保持具体。以「我们」的口吻、用命令写：「First, do x. Now, do y.」

**How-to：通往目标的步骤。**解决一个人拥有的问题，而不是机器能执行的操作。假定读者胜任，跳过教学。只有行动：不旁逸、不铺垫、不为完整而完整。这些用链接代替。允许分岔和判断：「If you want x, do y.」以任务命名指南：「How to calibrate the radar array」，而不是「Radar array calibration」。

**Reference：供查阅的事实。**只描述。不指令、不劝说、无观点。干燥、完整、确定。不含糊地陈述事实、选项、限制和错误。镜像被描述物的结构，让代码和文档可以一起导航。材料放在读者期望的位置。尽量从代码生成。

**Explanation：理解与缘由。**一个有边界的话题，离开产品也能读。每个标题都应容忍前面隐含一个「About…」。锚定一个真实的「为什么」问题。给出上下文：设计决策、历史、约束、备选方案。观点只允许出现在这里，别处不允许。

不要混模式：tutorial 里不放 reference 表格，reference 里不放 tutorial 式手把手，how-to 里不争论。拆开并链接。

## 对着读者写句子（Google developer style）

- 以「you」对读者说话，用现在时。「Will」只用于真正发生在将来的事。
- 说清谁做什么：「the compiler checks」，不是「is checked」。只有当施动者未知或无关紧要时被动才可接受。
- 指令写成命令：「Click Submit.」事实平铺直叙。绝不用「should be done」。
- 条件放在指令前面：「To delete the document, click Delete.」
- 常见情形在前。例外在后。
- 声音像一位懂行的朋友。不用流行词、不用比喻、指令里不用「please」，操作步骤里绝不用「simply」「easy」「quickly」。如果它真的简单，读者就不会在这里。
- 不预告（「we will soon support...」），连续的句子不以同一短语开头。
- 用说明去向的词做链接：页面标题或简短描述。绝不用「click here」。能用一句页内上下文，就不用一个页外链接。
- 标题承载要点，而不只是话题（「Pick the mode first」，不是「Modes」）。Sentence case。任务标题是光杆动词短语（「Create an instance」）。概念标题是名词短语。每页一个 h1，不跳级。
- 序列用编号列表，其余用圆点。用一个完整的句子引入列表。各项保持平行结构。
- 代码放代码字体。UI 元素加粗。用串行逗号。去掉「etc.」，直接说明列表不完整。

## 让陈述一次只承载一件事（STE 规则）

- 一句一条指令。其他地方一句一个想法。
- 超过约 20 词的指令、超过约 25 词的其他句子拆开。
- 警告或条件放在它守护的步骤之前：「If hot oil touches your skin, injuries can occur.」
- 保留「the」和「a」：「Remove backup file」有两种读法。「Remove the backup file」只有一种。
- 每个词只给一个含义、一个岗位，然后保持不变。如果「check」表示检查，就不要再拿它表示约束。
- 每个动作选一个词并用到底：用「start」，而不是这里「start」那里「initiate」。
- 把操作步骤写成直接命令，绝不用叙述，绝不用被动：「Install the component」，不是「the component must be installed」。
- 尽量避免「-ing」词。

## 不给任何句子留下两种读法（Global English）

- 「only」「not」这类词紧贴它们修饰的词：「only fails on growth」和「fails only on growth」含义不同。
- 拆开长名词串：「the proto import budget check script」变成「the script that checks the proto-import budget」。
- 让每个「it」「they」「this」都指向一个明显的东西。拿不准就重复名词。绝不用「this」或「which」指代整个从句。
- 不要丢动词：「Phase 1 moves the converters and Phase 2 the runtime」让 Phase 2 没了动词。给它补一个。
- 保留显示结构的小词，比如「Ensure that the switch is off」里的「that」。绝不为省词数牺牲清晰。
- 在并列中重复冠词以避免误读：当它们是两个东西时写「the client and the host」，不写「the client and host」。
- 当一句话能有两种分组时，说清「and」或「or」连接哪些部分。「Both...and」「either...or」「if...then」是免费消歧器。
- 用句号，不用分号。破折号换成新句子。
- 括号里的文字要么是完整的语法单元，要么自成一句。绝不用「(s)」构成复数。
- 不用斜杠：写「a, b, or both」，不写「a/b」或「and/or」。
- 每个东西在任何地方只用一个名字。一份文档对同一个东西说「the gate」「the ratchet」「the budget check」，等于教了三样东西。没变的东西不要翻新措辞。
- 跳过习语、口语、拉丁缩写和隐喻。

## 语气与仓库细节

- 对本技能触及的每份文档应用 **unslop** 技能。那个技能拥有 slop 模式目录：AI 词汇、填充词、对冲、格式特征。
- PR 描述和 commit message 也是写作。除 Diátaxis 外的每一层都适用于它们。PR 正文是一份评审者一分钟能读完的简报。不要粘贴 swarm 日志、SHA 列表或指标表格。链接它们。
- 产品 UI 文案不是文档。那些走你们产品的文案规范。
- 代码片段用 tab 缩进。写真实路径。让每个计数或树形断言在落地的提交上为真，并附上重新生成它的命令。

## 实战示例

修改前：

> Configuration of the proto import ratchet budget script parameters is performed via budget.json. Note that it's important to remember that running with --write, which updates the committed budget to reflect the current count, should only be done when lowering it. If exceeded, CI fails.
>
> 译文：proto 导入预算脚本的参数配置通过 budget.json 进行。注意，使用 `--write` 运行会把提交过的预算更新为当前计数，这一点很重要：只有在下调预算时才应该这么做。超出预算时 CI 会失败。

修改后：

> `budget.mjs` reads the committed budget from `budget.json` and counts the files that import protos. If the count exceeds the budget, CI fails. Run `budget.mjs --write` only to lower the budget.
>
> 译文：`budget.mjs` 从 `budget.json` 读取已提交的预算，统计导入 proto 的文件数。超过预算时 CI 失败。`budget.mjs --write` 只用于下调预算。
