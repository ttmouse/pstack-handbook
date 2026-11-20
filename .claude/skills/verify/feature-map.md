# 功能地图

页面有这些功能，用户这样到达，verify 这样验。改页面时对着这张表看，别漏。

| 功能 | 用户怎么到达 | 检查项 | 什么算过 |
|---|---|---|---|
| 章节目录 | 左侧导轨，或窄屏顶部栏展开 | `anchors` `toc-coverage` `chapter-nav` | 每条链接都有落点，目录与正文 h2 一一对应，点了会滚到章首且不被顶栏压住 |
| 窄屏抽屉 | 顶部栏点开，再点任一章节 | `phone-toc` | 打开后再点章节，抽屉自动收起 |
| 技能过滤 | 第 4 章输入框，输入关键词 | `filter` | 行数变少且不为零，Esc 复原到原行数 |
| 全文检索 | 导轨搜索框（窄屏在抽屉里） | `page-search` `page-search-phone` | 输入即出节级结果，点结果落到命中处且有 mark，Esc 复原章节列表，手机上点完抽屉收起 |
| 图放大 | 窄屏点任一插图 | `figure-zoom` | 窄屏切换放大态，宽屏不响应 |
| 插图绘制 | 任意章节的图 | `figures-drawn` | 每张 SVG 都有实际尺寸，不是空白 |
| 入场动效 | 滚到任意章节 | `reveal` `reduced-motion` | 滚到的内容可见；系统要求减少动效时直接可见 |
| 表格窄屏堆叠 | 窄屏看任意表格 | `table-stacking` | 每格都带 data-label，能单独成行 |
| 深浅配色 | 跟随系统 | `contrast` | 正文、标题、目录、图注都过 4.5:1 |
| 触控尺寸 | 手机上点目录和按钮 | `tap-targets` | 可点区域高度不小于 44px |
| 横向溢出 | 任意宽度 | `overflow` | 320 到 1440 五档都不横向滚动 |
| 资源自足 | 打开页面 | `no-errors` | 无脚本报错、无外链请求 |
| playbook 编号 | 第 3 章 | `playbook-numbers` | 01 起连续，不缺号 |
| 打印版式 | 系统打印或导出 PDF | `print-layout` | A4 下版心众数在 490–560px（37em@10.5pt=518），深浅系统色下图面都是浅色，导轨隐藏、reveal 全可见、无横向溢出 |
| 附录与页脚锚点 | 正文交叉引用点进附录 A–D；外链 `#colophon` 直达页脚 | `appendix-anchors` | 4 个附录锚点落点距视口顶 40–140px（scroll-margin 84），视口中点落在该节 offsetTop 区间内；页脚落点在视口内 |

这张表的功能名和 `scripts/verify.mjs` 的 FEATURES 检查项 ID 一一对应。改页面时对着这张表看，别漏；新增功能先补检查（先红后绿）再动页面。

`print-layout` 目前是 extra：`--feature print-layout` 或 `--extra` 才跑，进不进默认必过门槛待拍板。
