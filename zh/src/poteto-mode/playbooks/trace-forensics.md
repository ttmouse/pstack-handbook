### Trace forensics

**从产物出发的诊断归你。**

与 **Runtime forensics** 相区别：那本给活进程插桩，而这里捕获已经存在。产物是一份固定的数据集——读它，不要重跑它。工具保持通用：cpuprofile 和 `.json.gz` 用 DevTools 或 trace 解析器，spindump 用文本编辑器，heapsnapshot 用你的堆分析工具。

1. 识别格式，用对的工具加载。大型产物的解析放到子代理里（**principle-guard-the-context-window** 技能），还原后的发现留在主线程。按 poteto-mode 的 Subagents 一节为每个子代理选合适的推理档位。
2. 把原始产物转成可查询的形态。把 trace 或堆快照导入 sqlite，每个样本、帧、节点一行。先到达可查询的形态，再去读。
3. 收窄到原因。查询占时最多的帧，沿调用树走到热路径。泄漏就沿泄漏对象的引用链追到 GC root。spindump 就找到卡在 CPU 上或被阻塞的线程及其等待原因。
4. 归因到源码。用产物自带的符号把热帧映射到文件、符号、行号。没有源码映射的帧还不构成诊断。把符号解析出来，或者明说产物不带符号。
5. 有一组成对的捕获时，diff 前后两个产物来确认。没有就把发现标注为该产物所能支撑的最强假设，而不是已确认的原因。
6. 交回一份带引用的诊断，没被要求就不修。原因明确后路由到 Bug fix 或 Perf issue。吞吐检查点保持一行：`throughput checkpoint: n/a, read-only forensics`。

**汇报：** 产物和格式、还原后的发现、源码位置、产物路径、以及成对捕获是否确认了它。
