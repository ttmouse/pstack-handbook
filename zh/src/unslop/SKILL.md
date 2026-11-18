---
name: unslop
description: 去除任何文字中的 AI 痕迹。
---

# Unslop

编辑文字，去掉 AI 模式。扫描下面的模式，然后重写。保持含义不变，并匹配预期的语气。

## 要检测和修复的模式

规则编号是稳定的 id，其他技能会引用它们。删掉一条规则会留下空号。

### 内容

3. **空洞的 -ing 短语。** "highlighting..."、"ensuring..."、"reflecting..."、"showcasing..."、"fostering..."。删除，或用真实来源展开。
5. **模糊的归因。** "Experts believe"、"Industry reports suggest"、"Some critics argue"。说出来源，否则删除。

### 语言

7. **AI 词汇。** Additionally, crucial, delve, enduring, enhance, fostering, garner, interplay, intricate, landscape（抽象义）, pivotal, showcase, tapestry（抽象义）, testament, underscore, vibrant。换成平实的词。
8. **花哨的说法代替 "is"。** "serves as"、"stands as"、"boasts"、"features"。直接说 "is" 或 "has"。
9. **"Not just X, but Y."** 直接陈述观点。
10. **三段式。** 不要把想法硬凑成三组。用自然的数量。
11. **同义词轮换。** 同一段落里 protagonist、main character、central figure、hero 轮着来。选定一个，重复使用。
12. **虚假的范围。** "from X to Y"，但 X 和 Y 并不在一个有意义的尺度上。直接列出主题。

### 风格

13. **破折号滥用。** 完全避免破折号。只用句号或逗号（不用括号、不用短破折号、不用连字符充当破折号）。如果一个思路需要分隔，就结束句子或用逗号。
14. **冒号滥用。** 冒号在列表或例子前没问题，不能当句中连接符。"If you're coming from traditional automation: instead of registering event handlers, you describe conditions" 里的冒号没有任何增益。改写让观点独立成立，不用对比框架。"Describing when the scheduler should fire works best as plain English." 同样的意思，不靠标点撑场。
15. **加粗滥用。** 不要给每个专有名词或缩写都加粗。
16. **行内小标题式列表。** 痕迹是加粗标签加冒号，且标签复述了整行内容："**Performance:** Performance improved..."。把它们改成散文。加粗引导语以句号结尾、点出条目名称、后面跟着真正的新细节（"**Schema in TypeScript.** Tables live in one file."）是允许的，不算痕迹。
17. **标题用 Title Case。** 用 sentence case。
18. **装饰性 emoji。** 从标题和列表项里删掉。
19. **弯引号。** 用直引号。

### 对话腔

20. **聊天机器人套话。** "I hope this helps!"、"Let me know if..."、"Of course!"、"Certainly!"、"Found the smoking gun!" 删除。
22. **谄媚语气。** "Great question! You're absolutely right!" 直接回应。

### 废话

23. **填充短语。** "In order to" 改成 "To"。"Due to the fact that" 改成 "Because"。删掉 "It is important to note that"。
24. **过度对冲。** "could potentially possibly be argued that it might" 改成 "may"。
25. **空泛的结论。** "The future looks bright." 写出具体的计划或事实。

### 行话

26. **抽象比喻名词。** Substrate（base）、wedge、wedge in（add）、vector（way、method）、locus、vantage、nexus、当作名词用的 primitive、当作比喻的 harness、当作 "API surface" 用的 surface、bedrock、当作比喻的 scaffolding、modality、paradigm、gold-plating（超出工作需要的部分）、当作比喻的 ratchet（这个机制的真名，或一个只会收紧的限制）、表示搬走代码的 evacuate（move out）、endgame（最后阶段）、north star、flywheel。这些词读起来很技术，但通常有一个更平实的具体词。选具体词。

### 平实表达

27. **说它做什么，不说它感觉如何。** "the database stays close at hand"、"SQL you can read"、"types that follow your schema" 都在命名一种感觉。修法是说出机制或一个数字："`.toSQL()` returns the exact string sent to the database"、"a column rename fails the build"。先问这句话想让读者做什么或知道什么，然后写出那个。如果无法把它复述为一条具体指令、事实或数字，删掉。再多查一步：如果这句话原封不动地出现在另一个项目的文档里也成立，那它对这个项目什么都没说。删掉。
28. **拆短或拆开密集的句子。** 如果读者必须回读才能解析一个句子，把它拆成两句或去掉从句。一句一个想法。
29. **主动语态。** 优先使用。抓住 "is/are/was/were + 过去分词"，说出动作执行者："queries are validated" 改成 "the compiler validates queries"，"the file is parsed by the loader" 改成 "the loader parses the file"。只有当执行者未知或真的无关紧要时，被动语态才可用。
30. **删掉副词，或换更强的动词。** "runs quickly" 改成 "is fast" 或给出数字，"significantly improves" 改成实测的差值。副词撑着一个弱动词，说明动词选错了。
31. **优先用平实的词。** "utilize" 和 "leverage" 改成 "use"，"facilitate" 改成 "help"，"numerous" 改成 "many"，"in the event that" 改成 "if"。花哨的同义词很少更清楚。
32. **做作的散文。** 在存在字面说法的地方用比喻或修饰：格言（"wire it or delete it"）、为效果而设的修辞性残句、拟人化的代码（"the plan holds it"）、比喻性动词（"rides along"、"stands on"）、套用的框架短语。"A dial worth turning" 改成 "a parameter worth varying"。说你想说的意思。比喻名词见规则 26。
33. **过度压缩。** 省略冠词、无动词残句、符号腔，以及迫使读者解码而不是阅读的缩写。"Parser rejects bad date → exit 2, no write" 改成 "The parser rejects a bad date, exits with code 2, and writes nothing."。写出带冠词和动词的完整句子，把箭头和缩写展开。
