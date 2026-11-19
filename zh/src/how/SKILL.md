---
name: how
description: "用于「X 是怎么工作的」、改代码前的代码走读，以及归属 / 分层 / 放置类问题（「这段该放哪」「哪个包负责这个」「这层对不对」）。解释子系统架构、运行时流程、上手心智模型。想了解动机用 why。"
---

# How

在 Codex 上，先阅读[平台映射](../poteto-mode/references/codex-tools.md)（包括其中的各技能说明），再执行本技能。

在 GitHub Copilot 上，先阅读[平台映射](../poteto-mode/references/copilot-tools.md)（包括其中的各技能说明），再执行本技能。

在 Muse 上，先阅读[平台映射](../poteto-mode/references/muse-tools.md)（包括其中的各技能说明），再执行本技能。

在 Antigravity 上，先阅读[平台映射](../poteto-mode/references/agy-tools.md)（包括其中的各技能说明），再执行本技能。

探索代码库，回答「X 是怎么工作的」这类问题。

如果范围不明确，先说明你的理解，再去探索。用户可以随时纠正方向。

## 1. 解释

启动一个 `Agent` 子代理，`subagent_type: "general-purpose"`、`readonly: true`，让它一次性完成探索和解释。把用户的问题和下面这段说明交给它：

> 你在为一位资深工程师写架构讲解。探索代码库，写出一篇让不熟悉这块的资深工程师读完就能建立扎实心智模型的解释。他理解架构后应该能有信心直接上手。你拥有代码库的只读权限。

## 2. 呈现

把子代理的产出呈现出来。为了清晰或补充对话上下文做轻量修改没问题，但不要大幅重写。
