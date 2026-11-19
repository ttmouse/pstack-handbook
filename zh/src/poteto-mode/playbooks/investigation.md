### Investigation

**答案归你。计划、路由、成文。**

调查请求是只读的。产出是一份带引用的解释或建议，不是代码改动。

1. 追溯问题涉及的代码。动机类问题再走 **why** 技能。
2. 吞吐检查点保持一行：`throughput checkpoint: n/a, read-only investigation`。
3. 产出成文（Overview / Key Concepts / How It Works / Where Things Live / Gotchas），如果请求是在多个方案之间做决策，则给一份带取舍表的建议。
4. 回复套用 **unslop** 技能。

不走 PR、不走 babysit、不走 `architect`，除非调查是为了代码改动铺路。是的话，交还给用户并改路由到 Bug fix 或 Feature。

**汇报：** 调查产出本身。「我们确定吗？」类回答要给出你的真实判断和理由。前提错了就顶回去（见 Autonomy）。
