---
name: create-verification-skill
description: "生成一个项目本地的验证技能，用用户的方式驱动你的应用——任意语言、框架、平台。用于 /create-verification-skill、\"make a control skill for this repo\"、\"make a driver skill for this repo\"，或项目没有脚本能证明 UI/CLI/服务行为时。"
---

# Create a verification skill

在 Codex 上，遵循本技能前先读[平台映射](../poteto-mode/references/codex-tools.md)，包括其中按技能给出的说明。

在 GitHub Copilot 上，遵循本技能前先读[平台映射](../poteto-mode/references/copilot-tools.md)，包括其中按技能给出的说明。

在 Muse 上，遵循本技能前先读[平台映射](../poteto-mode/references/muse-tools.md)，包括其中按技能给出的说明。

在 Antigravity 上，遵循本技能前先读[平台映射](../poteto-mode/references/agy-tools.md)，包括其中按技能给出的说明。

每个认真的项目都需要一种脚本化方式来驱动真实应用并证明行为：启动它、像用户一样操作一个功能、采集证据。本技能把它生成为一个项目本地技能（`.claude/skills/verify/`），为该仓库量身定制。命名为 `verify`。在仓库根目录，这个名字的项目技能会顶替 Claude Code 内置的 `/verify`——后者只有用户能调用——于是所有提到驱动技能的 playbook 都能调用项目这份（[Claude Code 2.1.200 或更高](https://code.claude.com/docs/en/skills#run-and-verify-your-app)）。在 monorepo 里，写到被改动的那个 package 目录。生成器的输出是写给下一个代理的，不是写给人的：它会在任务中途被冷启动阅读，而那个代理从没见过这个应用。

## 1. Interview the repo, not the user

以下从代码库里回答，只有观察不到的才问用户：

- **Surface：** 用户实际接触的是什么？Web UI、CLI/TUI、桌面应用、API、移动应用、库？一个仓库可以有多个；挑主要的，其余记下来。
- **Run：** 应用本地怎么启动？优先用仓库自己文档里的 dev 命令（package scripts、Makefile、README quickstart）。记下端口、环境变量、种子数据、认证。
- **Drive：** 代理怎么以编程方式与它交互？先找现成的测试设施——Playwright/Cypress 用例、expect 脚本、PTY 辅助、可直接 curl 的端点、调试端口。找不到再选通用配方：web 和 Electron 用浏览器/CDP，CLI/TUI 用 tmux/PTY 测试设施，服务用纯 HTTP。
- **Observe：** 能采集什么证据？截图、终端转写、响应体、日志、退出码、数据库状态。
- **Isolate：** 两个实例能否并行跑（端口、数据目录、profile）？不能的话在生成的技能里写明：拒绝双重驱动共享实例，好过弄坏用户的会话。

如果 checkout 现状编译不过或起不来，先生成之前修好它（或精确报告）；对着一个坏掉的基线写技能，只会教出错误的步骤。当一个无关的缺失资源阻塞启动（API 从不服务的静态目录、一个示例配置），生成的技能可以创建它，明确标记为验证脚手架，并在清理时移除。

## 2. Generate the skill

写 `.claude/skills/verify/SKILL.md`，带 YAML frontmatter（`name: verify`，`description` 点明应用、surface 和使用时机——没有 frontmatter 技能永远不会注册，加了 `disable-model-invocation` 模型就无法调用它），加上以下章节，每节都落在访谈的实际发现上（不留占位符）：

- **Launch：** 为验证启动应用的精确命令，以及怎么判断就绪（一行日志、一个提示符）。启动必须能从空数据目录到达可用状态，包括迁移和种子数据。就绪 = 可用，不只是"进程有响应"——数据库健康检查通过时，它的初始化脚本可能还在跑。包含清理（teardown）。短命的 CLI 或 TUI 没有需要保活的服务：启动意味着构建二进制（或装依赖）一次，然后每次驱动都在自己隔离的 PTY 或 tmux 会话里进行。
- **Doctor：** 一条只读检查，回答"这个实例值得驱动吗？"——进程在跑、版本/构建正确、端口是我们的、认证有效。任何时候看起来不对劲，代理都先跑它。
- **Drive：** 测试设施配方，用这个仓库真实的选择器/命令，不是示例。优先稳定的句柄（ARIA 标签、data 属性、提示符字符串、路由路径），而不是坐标和 tab 顺序。
- **Evidence：** 证明要采集什么、放到哪里。写明证明标准：走真实的用户路径，不是内部 setter 或测试专用端点；同时采集动作和产生的状态，不只是最终画面；可见结果之外还要核实副作用（写入的文件、插入的行、发出的消息）；只在生产边界本就隔离了外部系统的地方才用 mock。安全路径是 dry-run 或测试模式时，靠观察（文件、网络、git refs）核实它到底跳过了什么，而不是信它的名字：有些 dry-run 仍然碰网络或开浏览器。
- **Cleanup：** 怎么拆除这次运行创建的实例。绝不按进程名杀；只杀你启动的。清理移除实例和临时状态，绝不移除证据：证明产物要在拆除后存活，放在技能里指定的位置。
- **Helpers：** 技能附带的任何脚本都要可执行，且调用方式写在技能正文里。读者需要逆向工程才能用的辅助脚本不是辅助脚本。

## 3. Seed the feature map

创建 `.claude/skills/verify/features/README.md`，加上每个你能识别的用户可见功能一个文件（起步瞄准前 3-5 个，从路由、命令、菜单或文档来）。形状遵循 [`references/feature-map-example/`](references/feature-map-example/)：一个 README 索引，每个功能一个文件。每个文件从用户视角回答：这个功能是什么、怎么到达它、怎么用测试设施驱动它、什么可观察的终态证明它能用。四个 H2 是 `Sub-features`、`How to get to it (user POV)`、`Driving it with <harness>`、`Gotchas`。如果种子数据缺某个旅程需要的前置条件，该旅程就报告失败，原因写进那个功能的 `Gotchas`。绝不为了让它通过而削弱旅程。功能地图是仓库持续维护的验证来源；只驱动一个顺手入口的证明，当地图上还列着其他入口时，就是不完整的。

## 4. Prove the generated skill before handing it over

把它的说明端到端跑一遍：launch、doctor、驱动 ONE 个地图上的功能（一个就够；地图存在的意义就是让后续运行覆盖其余）、采集证据、清理。清理之后确认证据还在指定位置——吃掉证明的清理算失败。修掉失败的部分，每次失败的迭代之后也要跑生成的清理，让坏掉的尝试不留下进程和端口。从没执行过的生成技能是草稿，不是交付物。如果你是在替身（容器代替新装 VM、本地栈代替远程栈）上完成的证明，列出替身做了而真实目标不会做的每个搭建步骤。这些步骤在真实目标上跑到之前都算未验证。

## 5. Offer the maintenance loop

应用变化后要保持地图不失真，指引用户去 `/maintain-verification-skill`。只在对方问起时才建议节奏。
