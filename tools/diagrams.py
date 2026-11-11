#!/usr/bin/env python3
"""Generate the inline SVG diagrams for the pstack handbook.

Every figure is laid out by hand inside a 900-wide viewBox. Colors come from
the page's CSS variables, and text inherits the page font, so one SVG works in
light mode, dark mode and print without a second copy.

Two checks run while drawing: nothing may fall outside the viewBox, and no
label may be wider than the box that holds it. Both print a warning with the
figure name so a layout mistake fails loudly instead of silently overlapping.
"""
import html
import os

W = 900
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "figs")
PROBLEMS = []


def esc(s):
    return html.escape(s, quote=True)


def text_w(s, size):
    """Rough advance width: CJK is square, Latin about 0.56em."""
    return sum(size * (1.0 if ord(c) > 0x2E7F else 0.56) for c in s)


class Fig:
    def __init__(self, name, h, aria, caption):
        self.name, self.h, self.aria, self.caption = name, h, aria, caption
        self.parts = []

    # ---------- primitives ----------

    def check(self, what, x, y, w=0, h=0):
        if x < 0 or y < 0 or x + w > W or y + h > self.h:
            PROBLEMS.append(f"{self.name}: {what} out of bounds "
                            f"({x:.0f},{y:.0f},{w:.0f}x{h:.0f})")

    def line(self, x1, y1, x2, y2, dash=None, width=1.5, arrow=True):
        for x, y in ((x1, y1), (x2, y2)):
            self.check("line", x, y)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        a = f' marker-end="url(#{self.name}-arrow)"' if arrow else ""
        self.parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="var(--muted)" stroke-width="{width}"{d}{a}/>')

    def path(self, pts, dash=None, arrow=True):
        for x, y in pts:
            self.check("path", x, y)
        d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f}"
        for x, y in pts[1:]:
            d += f" L {x:.1f} {y:.1f}"
        da = f' stroke-dasharray="{dash}"' if dash else ""
        ar = f' marker-end="url(#{self.name}-arrow)"' if arrow else ""
        self.parts.append(
            f'<path d="{d}" fill="none" stroke="var(--muted)" stroke-width="1.5" '
            f'stroke-linejoin="round"{da}{ar}/>')

    def note(self, x, y, s, size=12, anchor="middle", color="var(--muted)",
             weight="400", rotate=None):
        if rotate is None:
            tw = text_w(s, size)
            x0 = {"middle": x - tw / 2, "start": x, "end": x - tw}[anchor]
            self.check("note", x0, y - size, tw, size)
        tr = f' transform="rotate({rotate} {x:.1f} {y:.1f})"' if rotate else ""
        self.parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
            f'font-size="{size}" font-weight="{weight}" fill="{color}"{tr}>{esc(s)}</text>')

    def box(self, cx, cy, title, sub=None, w=440, h=None, kind="box", dash=None,
            tsize=15, ssize=12.5, tcolor="var(--fg)"):
        h = h or (58 if sub else 40)
        x, y = cx - w / 2, cy - h / 2
        self.check("box", x, y, w, h)
        stroke = {"box": "var(--line)", "accent": "var(--accent)",
                  "ok": "var(--ok)", "bad": "var(--bad)",
                  "muted": "var(--muted)"}[kind]
        fill = "var(--panel)" if kind in ("ok", "bad", "muted") else "var(--panel2)"
        da = f' stroke-dasharray="6 5"' if dash else ""
        self.parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.4"{da}/>')
        tw = text_w(title, tsize)
        if tw > w - 28:
            PROBLEMS.append(f"{self.name}: title {title!r} needs {tw:.0f}px, box {w:.0f}px")
        ty = cy - 7 if sub else cy + 5
        self.parts.append(
            f'<text x="{cx:.1f}" y="{ty:.1f}" text-anchor="middle" font-size="{tsize}" '
            f'font-weight="600" fill="{tcolor}">{esc(title)}</text>')
        if sub:
            sw = text_w(sub, ssize)
            if sw > w - 20:
                PROBLEMS.append(f"{self.name}: sub {sub!r} needs {sw:.0f}px, box {w:.0f}px")
            self.parts.append(
                f'<text x="{cx:.1f}" y="{cy + 15:.1f}" text-anchor="middle" '
                f'font-size="{ssize}" fill="var(--muted)">{esc(sub)}</text>')

    def diamond(self, cx, cy, label, rx=92, ry=36):
        self.check("diamond", cx - rx, cy - ry, rx * 2, ry * 2)
        pts = f"{cx},{cy - ry} {cx + rx},{cy} {cx},{cy + ry} {cx - rx},{cy}"
        self.parts.append(
            f'<polygon points="{pts}" fill="var(--panel2)" stroke="var(--accent)" '
            f'stroke-width="1.4"/>')
        tw = text_w(label, 13)
        if tw > rx * 1.5:
            PROBLEMS.append(f"{self.name}: diamond label {label!r} too wide")
        self.parts.append(
            f'<text x="{cx}" y="{cy + 4.5:.1f}" text-anchor="middle" font-size="13" '
            f'font-weight="600" fill="var(--fg)">{esc(label)}</text>')

    def badge(self, cx, cy, s, kind="muted"):
        color = {"muted": "var(--muted)", "ok": "var(--ok)",
                 "bad": "var(--bad)", "accent": "var(--accent)"}[kind]
        w = text_w(s, 11) + 14
        self.check("badge", cx - w / 2, cy - 9, w, 18)
        self.parts.append(
            f'<rect x="{cx - w / 2:.1f}" y="{cy - 9:.1f}" width="{w:.1f}" height="18" '
            f'rx="9" fill="none" stroke="{color}" stroke-width="1"/>')
        self.parts.append(
            f'<text x="{cx:.1f}" y="{cy + 3.8:.1f}" text-anchor="middle" font-size="11" '
            f'fill="{color}">{esc(s)}</text>')

    # ---------- output ----------

    def render(self):
        head = (
            f'<svg viewBox="0 0 {W} {self.h}" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-label="{esc(self.aria)}">'
            f'<defs><marker id="{self.name}-arrow" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0.5 L10,5 L0,9.5 z" fill="var(--muted)"/></marker></defs>')
        body = "".join(self.parts)
        cap = (f'<figcaption>{self.caption}</figcaption>')
        return (f'<figure class="devfig"><div class="figscroll">{head}{body}</svg></div>'
                f'{cap}</figure>')


# --------------------------------------------------------------------------
# 1. 第 0.5 章：一个故事，六步
# --------------------------------------------------------------------------

def fig_story():
    f = Fig("story", 600,
            "一个缺陷从复现到提交的六个步骤，第五步不通过时回到第二步",
            "六步里最容易跳过的是第二步和第五步。整套流程只是把这两步固定下来。")
    cx, bw = 430, 470
    rows = [
        ("1 先让它重现出来", "点几下，确认真的会吞"),
        ("2 猜几个可能的原因", "没收到？收到了被忽略？没画出来？"),
        ("3 一个个排除，拿到运行时证据", "加一行日志，看按键到底进没进来"),
        ("4 找到原因，只改那一处", "不是顺手多改几处"),
        ("5 回到同一个地方再试一遍", "同一个入口，同样的连按速度"),
        ("6 交上去，写清是怎么回事", "改了什么、为什么、怎么验的"),
    ]
    ys = [60, 146, 232, 318, 404, 490]
    for (t, s), y in zip(rows, ys):
        f.box(cx, y, t, s, w=bw, kind="box")
    for y in ys[:-1]:
        f.line(cx, y + 29, cx, y + 57)
    # 失败回环：第 5 步不通，回到第 2 步继续排除
    f.path([(cx - bw / 2, 404), (120, 404), (120, 146), (cx - bw / 2 - 1, 146)], dash="6 5")
    f.note(104, 275, "不通就回头", size=12, rotate=-90)
    f.parts.append('<rect x="672" y="208" width="212" height="128" rx="10" fill="none" '
                   'stroke="var(--line)" stroke-dasharray="6 5"/>')
    f.note(686, 236, "最容易被跳过的两步", size=12.5, anchor="start", color="var(--accent2)")
    f.note(686, 264, "第 2 步 猜原因", size=12.5, anchor="start")
    f.note(686, 288, "第 5 步 回原地再试", size=12.5, anchor="start")
    f.note(686, 316, "跳了，结论就不可信", size=12, anchor="start")
    return f


# --------------------------------------------------------------------------
# 2. 第 1 章：四层结构
# --------------------------------------------------------------------------

def fig_layers():
    f = Fig("layers", 520,
            "四层结构：路由器调用流程清单，清单里的每一步由技能执行，原则由路由器按场景自选",
            "任务从上往下走，只有路由器和技能能直接叫；流程清单只能被路由器读，原则由它按场景自选。")
    cx, bw = 385, 430
    f.box(cx, 34, "你的任务", w=220, h=38, kind="accent")
    f.line(cx, 53, cx, 76)

    f.box(cx, 110, "路由器 poteto-mode", "判断类型，挑清单，抄步骤", w=bw, h=66)
    f.badge(548, 92, "能叫", "ok")

    f.line(cx, 143, cx, 192)
    f.note(cx + 78, 172, "选中一本", size=12, anchor="start")

    f.box(cx, 225, "流程清单 playbook × 23", "修缺陷六步、做功能五步", w=bw, h=66)
    f.badge(544, 207, "不能叫", "bad")

    f.line(cx, 258, cx, 307)
    f.note(cx + 90, 287, "每步翻译成技能调用", size=12, anchor="start")

    f.box(cx, 340, "技能 × 43 与子代理", "一个具体动作；重活派出去", w=bw, h=66)
    f.badge(548, 322, "能叫", "ok")

    f.line(cx, 373, cx, 415)

    f.box(cx, 450, "真实产物 + 证据", "截图、命令输出、断言结果", w=bw, h=58, kind="ok")

    f.parts.append('<rect x="660" y="88" width="230" height="274" rx="10" fill="none" '
                   'stroke="var(--muted)" stroke-dasharray="6 5"/>')
    f.note(775, 128, "原则 × 24", size=15, weight="600", color="var(--fg)")
    f.note(775, 158, "一句话约束", size=12.5)
    f.note(775, 190, "不单独执行", size=12.5)
    f.note(775, 224, "路由器按场景挑", size=12)
    f.path([(cx + bw / 2, 110), (660, 110)], dash="6 5", arrow=False)
    f.path([(cx + bw / 2, 340), (660, 340)], dash="6 5", arrow=False)
    return f


# --------------------------------------------------------------------------
# 3. 第 2 章：一次任务进来发生什么
# --------------------------------------------------------------------------

def fig_flow():
    f = Fig("flow", 720,
            "一次任务的处理流程：消息进入、判断类型、抄步骤、派活、验证、收尾，验证不通过回到对应步骤",
            "蓝色菱形是唯一的分叉点。验证不通过时回到对应步骤，而不是从头再来。")
    cx, bw = 400, 470
    f.box(cx, 54, "你的消息进主线程", "技能清单和启动指令已在上下文", w=bw, h=64)
    f.line(cx, 86, cx, 118)
    f.box(cx, 150, "判断任务类型", "命中一本流程清单", w=bw, h=64)
    f.line(cx, 182, cx, 214)
    f.box(cx, 246, "把步骤抄进待办", "这是最值得盯的地方", w=bw, h=64)
    f.line(cx, 278, cx, 310)
    f.box(cx, 342, "按步调技能，或派子代理", "重活出去，主线程只留判断", w=bw, h=64)
    f.line(cx, 374, cx, 416)

    f.diamond(cx, 452, "需要验证？")
    f.note(cx + 16, 440, "是", size=12, anchor="start")
    f.line(cx, 488, cx, 528)

    f.box(cx, 560, "跑验证", "真实产物、同一次运行", w=bw, h=64, kind="accent")
    f.line(cx, 592, cx, 626)

    f.box(cx, 660, "收尾", "按要求回报，说明跳过哪几步", w=bw, h=64)

    # 不通过：回到对应步骤
    f.path([(cx - bw / 2, 560), (88, 560), (88, 342), (cx - bw / 2 - 1, 342)], dash="6 5")
    f.note(72, 450, "不通过就回到对应步骤", size=12, rotate=-90)

    # 不需要验证：跳过验证，直接收尾
    f.path([(cx + 92, 452), (742, 452), (742, 660), (cx + bw / 2 + 1, 660)], dash="6 5")
    f.note(700, 442, "否", size=12, anchor="start")
    f.note(762, 560, "直接收尾", size=12, rotate=90)
    return f


# --------------------------------------------------------------------------
# 4. 第 3 章：修缺陷六步
# --------------------------------------------------------------------------

def fig_bugfix():
    f = Fig("bugfix", 620,
            "修缺陷六步：复现、二分排除、规划、同面验证、提交顺序、开 PR，验证失败回到规划",
            "两个回环：排除没收敛就再切一刀；同面验证不通过，修改方案而不是修改判据。")
    cx, bw = 400, 470
    rows = [
        (52, "1 自己复现", "在出问题的同一个面上驱动，能重现才继续"),
        (150, "2 二分排因", "列假设、取运行证据、排除，直到剩一个"),
        (248, "3 规划修复", "跨函数边界先做设计，再派实现"),
        (346, "4 回同一个面验证", "原来失败的操作现在要过，不是跑单测"),
        (444, "5 排列提交顺序", "失败的复现先进历史，修复在后"),
        (542, "6 开 PR", "写清坏在哪、根因、修复、怎么验"),
    ]
    for y, t, s in rows:
        kind = "accent" if y == 52 else "box"
        f.box(cx, y, t, s, w=bw, kind=kind)
    for y, _, _ in rows[:-1]:
        f.line(cx, y + 29, cx, y + 57)

    # 排除没收敛：自循环
    f.parts.append('<path d="M 635 150 C 700 150 700 128 637 128" fill="none" '
                   'stroke="var(--muted)" stroke-width="1.5" stroke-dasharray="6 5" '
                   f'marker-end="url(#{f.name}-arrow)"/>')
    f.note(700, 104, "再来一轮", size=12)

    # 验证不通过：回到规划
    f.path([(cx - bw / 2, 346), (86, 346), (86, 248), (cx - bw / 2 - 1, 248)], dash="6 5")
    f.note(70, 300, "不通过", size=12, rotate=-90)
    return f


# --------------------------------------------------------------------------
# 4b. 第 3 章：做功能八步
# --------------------------------------------------------------------------

def fig_feature():
    f = Fig("feature", 760,
            "做功能的八步流程：先懂、并行设计、写吞吐检查点、派实现、同面验证、重排提交、对抗争议、开 PR",
            "第三、四步是全套流程的分水岭：先想清楚怎么拆，再派活。第七步虚线框表示可以跳过。")
    cx, bw = 340, 430
    rows = [
        (50, "1 先懂再改", "用 how 把受影响的子系统读一遍", "box"),
        (142, "2 并行设计", "多个模型各出一版签名，交叉评审", "box"),
        (234, "3 写吞吐检查点", "四条待办，一项都不能删", "accent"),
        (326, "4 派实现", "文件、数据形状、成功标准，缺一不可", "box"),
        (418, "5 同面验证", "换界面或结论不确定都不算过", "box"),
        (510, "6 重排成小提交", "每段自证过，再下一段", "box"),
        (602, "7 有争议先对抗", "interrogate，小改动可跳过", "muted"),
        (694, "8 开 PR", "做了什么、为什么、检查点、未决", "ok"),
    ]
    for y, t, s, kind in rows:
        f.box(cx, y, t, s, w=bw, kind=kind, dash="6 5" if kind == "muted" else None)
    for y, _, _, _ in rows[:-1]:
        f.line(cx, y + 29, cx, y + 57)

    # 吞吐检查点的四问，贴在第三步右侧
    f.parts.append('<rect x="588" y="176" width="292" height="140" rx="10" fill="none" '
                   'stroke="var(--accent)" stroke-dasharray="6 5"/>')
    f.note(606, 200, "检查点四问", size=13, anchor="start",
           color="var(--accent2)", weight="600")
    for i, t in enumerate(("阻塞第一步", "独立工作面", "共享可变状态", "最小安全拆分")):
        f.note(606, 226 + i * 22, t, size=12.5, anchor="start")
    f.path([(cx + bw / 2, 234), (586, 234)], arrow=False, dash="6 5")
    return f

# --------------------------------------------------------------------------
# 2b. 第 2 章：上下文怎么省
# --------------------------------------------------------------------------

def fig_context():
    f = Fig("context", 440,
            "常驻式与按需式的上下文占用对比：整篇文件每次加载，或只加载描述、命中后再读正文",
            "左边每次都背整本书，右边平时只背目录。代价是目录必须写准。")
    f.note(200, 40, "常驻式（写进 CLAUDE.md）", size=13.5, color="var(--accent2)", weight="600")
    f.note(640, 40, "按需式（写成技能）", size=13.5, color="var(--accent2)", weight="600")

    f.parts.append('<rect x="60" y="66" width="280" height="238" rx="10" fill="var(--panel2)" '
                   'stroke="var(--line)"/>')
    f.note(200, 130, "整篇文件", size=15, weight="600", color="var(--fg)")
    f.note(200, 158, "每次会话全文加载", size=12.5)
    f.note(200, 200, "写五个技能就开始挤", size=12)
    f.note(200, 222, "写二十个必然撑爆", size=12)
    f.badge(200, 262, "每次都付", "bad")

    for i in range(6):
        f.parts.append(f'<rect x="500" y="{66 + i * 18}" width="280" height="9" rx="4" '
                       f'fill="var(--accent)" opacity="0.45"/>')
    f.note(640, 186, "43 条描述常驻，很薄", size=12.5)
    f.note(790, 82, "…", size=14, anchor="start")

    f.line(640, 200, 640, 226)
    f.parts.append('<rect x="500" y="230" width="280" height="74" rx="10" fill="var(--panel2)" '
                   'stroke="var(--accent)"/>')
    f.note(640, 258, "命中才读正文", size=14, weight="600", color="var(--fg)")
    f.note(640, 282, "读一次，答案留在结论里", size=12)
    f.badge(640, 322, "按需才付", "ok")

    f.note(450, 380, "省下来的不是字数，是判断质量：上下文越干净，后面的取舍越准。", size=12.5)
    f.note(450, 406, "代价只有一条：描述写不好，这个技能就等于不存在。", size=12.5,
           color="var(--accent2)")
    return f


# --------------------------------------------------------------------------
# 2c. 第 9 章：该不该走流程
# --------------------------------------------------------------------------

def fig_decide():
    f = Fig("decide", 500,
            "判断要不要走完整流程的三道门：改一行、能不能判定、要不要复现真实产物",
            "从上往下问，第一个命中的就停。判断不了就先当成要验证，多花的钱比返工便宜。")
    cx = 300
    f.diamond(cx, 80, "改一行、查事实、跑命令？", rx=150, ry=42)
    f.diamond(cx, 205, "完成标准能写成可判定的？", rx=150, ry=42)
    f.diamond(cx, 330, "要复现或验证真实产物？", rx=150, ry=42)
    f.box(cx, 448, "走完整流程", "poteto-mode 按类型选清单", w=340, h=62, kind="accent")

    exits = [
        (80, "直接做", "不走任何流程"),
        (205, "先定义完成标准", "流程救不了模糊目标"),
        (330, "单个技能够用", "how / why / teach"),
    ]
    for y, t, s in exits:
        f.line(cx + 150, y, 553, y)
        f.box(700, y, t, s, w=290, h=56, kind="muted")
        f.note(500, y - 10, "是" if y == 80 else "否", size=12)

    f.line(cx, 122, cx, 163)
    f.note(cx + 14, 148, "否", size=12, anchor="start")
    f.line(cx, 247, cx, 288)
    f.note(cx + 14, 273, "是", size=12, anchor="start")
    f.line(cx, 372, cx, 415)
    f.note(cx + 14, 398, "是", size=12, anchor="start")

    return f


# --------------------------------------------------------------------------
# 4c. 第 13 章：费曼循环
# --------------------------------------------------------------------------

def fig_feynman():
    f = Fig("feynman", 560,
            "费曼循环：选一个概念、讲给外行听、在卡住处停下、回读那一节，再讲一遍",
            "三个动作走一圈。卡住的那一句，就是你没真懂的地方。")
    f.note(60, 108, "选一个概念", size=13.5, anchor="start",
           color="var(--accent2)", weight="600")
    f.note(60, 132, "小到能一口气讲完", size=12, anchor="start")
    f.line(200, 120, 296, 120)

    f.box(450, 120, "讲给外行听", "不许用术语，不许跳过", w=300, h=64, kind="accent")
    f.box(680, 470, "在卡住的地方停下", "卡住就是知识缺口", w=300, h=64, kind="bad")
    f.box(220, 470, "回读那一节", "只补卡住的那一段", w=300, h=64)

    f.path([(540, 158), (646, 420)])
    f.note(612, 292, "讲不下去", size=12)
    f.path([(528, 470), (374, 470)])
    f.note(450, 458, "翻回去补", size=12)
    f.path([(352, 438), (404, 158)])
    f.note(336, 300, "再讲一遍", size=12, anchor="end")

    f.note(450, 330, "讲不通，就是没学会", size=14, color="var(--accent2)", weight="600")
    return f


# --------------------------------------------------------------------------
# 5b. 第 5 章：三条必记的原则落在哪
# --------------------------------------------------------------------------

def fig_principles():
    f = Fig("principles", 430,
            "三条最常救场的原则分别对应写之前、排查时、交付前，其余二十一条由 poteto-mode 按场景自选",
            "这三条对应三个最容易走偏的时刻。其余二十一条由 poteto-mode 按场景挑选，挑中的才读全文。")
    phases = [
        (180, "写之前", "laziness-protocol", "能删就删，最小改动"),
        (450, "排查时", "fix-root-causes", "追到第一次出错的地方"),
        (720, "交付前", "prove-it-works", "验真实产物，不验代理指标"),
    ]
    for cx, ph, name, desc in phases:
        f.box(cx, 70, ph, w=240, h=44, kind="muted")
        f.line(cx, 92, cx, 128)
        f.box(cx, 170, name, desc, w=240, h=76, kind="accent")
    f.line(300, 70, 328, 70)
    f.line(570, 70, 598, 70)

    f.parts.append('<rect x="60" y="252" width="780" height="92" rx="10" fill="var(--panel2)" '
                   'stroke="var(--line)" stroke-dasharray="6 5"/>')
    f.note(450, 284, "其余 21 条：设计取舍、边界与类型、并行与共享状态、上下文预算", size=13)
    f.note(450, 314, "索引写在 poteto-mode 正文里，它按场景自己挑，挑中的才读全文", size=12.5)
    return f


# --------------------------------------------------------------------------
# 5. 第 7 章：验证链路与两种失败来源
# --------------------------------------------------------------------------

def fig_verify():
    f = Fig("verify", 700,
            "验证链路：体检、单测门、驱动真实应用、取证、判定，不通过分产品不符与判据不成立两种",
            "判定失败只有两种原因：产品真的不符，或者你的标准本身不成立。先分清，再动手。")
    cx, bw = 380, 460
    f.box(cx, 48, "1 体检", "进程号、版本、是不是这次启动的", w=bw, kind="box")
    f.line(cx, 77, cx, 111)
    f.box(cx, 140, "2 单测门", "跑得快，先筛掉明显的", w=bw)
    f.line(cx, 169, cx, 203)
    f.box(cx, 232, "3 驱动真实应用", "用驱动工具，不靠手点和肉眼", w=bw)
    f.line(cx, 261, cx, 295)
    f.box(cx, 324, "4 取证", "截图、命令输出、含副作用的断言", w=bw)
    f.line(cx, 353, cx, 390)

    f.diamond(cx, 424, "判定")
    f.line(cx, 460, cx, 486)
    f.note(cx + 12, 476, "过", size=12, anchor="start")

    f.box(140, 520, "产品不符", "回去修，不要改判据", w=250, h=58, kind="bad")
    f.box(400, 520, "写状态文件", "判定 + 依据 + 证据路径", w=250, h=58, kind="ok")
    f.box(660, 520, "判据不成立", "改标准，再跑一次", w=250, h=58, kind="accent")

    f.path([(cx - 96, 424), (140, 424), (140, 490)])
    f.note(140, 410, "不过", size=12)
    f.path([(cx + 96, 424), (660, 424), (660, 490)])
    f.note(660, 410, "不过", size=12)

    f.line(400, 549, 400, 592)
    f.box(400, 626, "维护日志加一行", "这次验了什么、哪里容易误判", w=400, h=58)

    # 改完判据回到判定
    f.path([(785, 520), (856, 520), (856, 452), (404, 452)], dash="6 5")
    f.note(872, 486, "改完重跑", size=12, rotate=-90)
    return f


# --------------------------------------------------------------------------
# 6. 第 8 章：并行四问
# --------------------------------------------------------------------------

def fig_parallel():
    f = Fig("parallel", 700,
            "并行前要过的四道门：阻塞前置、文件不重叠、无共享写、单个更慢，任何一道不过就改变策略",
            "四道门从上往下过。任何一道不过，先改变策略，不要硬拆。")
    cx, bw = 330, 400
    gates = [
        (64, "第一步：有没有阻塞前置？", "必须做完才能开工的步骤", "先串行做完，再往下"),
        (184, "各路文件、服务完全不重叠？", "同一文件就是同一个写者", "先拆分目标，或串行"),
        (304, "有没有共享可变状态？", "两个代理写同一份数据", "只留一个写者"),
        (424, "单个工人会不会更快？", "小改动不值得拆", "就开一路，写下理由"),
    ]
    for y, t, s, exit_lbl in gates:
        f.box(cx, y, t, s, w=bw, h=64)
        f.line(cx + bw / 2, y, 566, y)
        f.box(720, y, exit_lbl, w=280, h=48, kind="muted")
        f.note(548, y - 8, "不满足", size=11)
    for y, _, _, _ in gates[:-1]:
        f.line(cx, y + 32, cx, y + 88, dash="6 5")
        f.note(cx + 14, y + 66, "满足", size=11, anchor="start")

    f.line(cx, 456, cx, 496)
    f.box(cx, 534, "开 N 路", "每路独立取证，最后只汇总差异", w=bw, h=64, kind="ok")
    f.note(330, 620, "上限不在你能开几路，而在你能验几路。", size=13,
           color="var(--accent2)")
    f.note(330, 646, "验不过来的那几路，等于没做。", size=12.5)
    return f


# --------------------------------------------------------------------------
# 7. 第 15 章：四级顺序
# --------------------------------------------------------------------------

def fig_levels():
    f = Fig("levels", 470,
            "把纠正变成结构的四级顺序，从改架构到口头提醒，效果依次递减",
            "从上往下，效果递减。你在第四级说过三遍的事，应该往上挪一级。")
    bars = [
        (30, 820, "第一级 改架构或数据结构 → 根除", "让这个错在类型或结构上写不出来", "ok"),
        (140, 720, "第二级 加检查规则或测试 → 拦住", "流水线里过不去，不靠人记", "accent"),
        (250, 620, "第三级 写进技能或规则文档 → 靠自觉", "它读到了才生效，读不到等于没写", "muted"),
        (360, 520, "第四级 评审时口头说一遍 → 没戏", "下次还会犯，你已经说过三遍了", "bad"),
    ]
    for y, w, t, s, kind in bars:
        f.box(40 + w / 2, y + 45, t, s, w=w, h=90, kind=kind)
    f.note(470, 24, "效果从强到弱", size=12.5)
    return f


# --------------------------------------------------------------------------
# 8. 第 15 章：成本怎么放大
# --------------------------------------------------------------------------

def fig_cost():
    f = Fig("cost", 420,
            "固定上下文成本随子代理线性放大，以及同一批任务加与不加流程的花费对比",
            "上：固定上下文按子代理数线性叠加。下：唯一一个公开的第三方对比，结果没有区别。")
    f.note(40, 40, "一 固定上下文怎么放大", size=13, anchor="start",
           color="var(--accent2)", weight="600")
    f.box(170, 100, "主线程 3,600 词", "每次进流程都读一遍", w=300, h=64)
    for i, x in enumerate((440, 560, 680)):
        f.box(x, 100, "子代理", "3,600 词", w=110, h=64, kind="muted")
        if i == 0:
            f.line(320, 100, 385, 100)
    f.note(450, 158, "每开一路子代理，固定部分就再叠一份", size=12, anchor="start")
    f.note(450, 182, "按三路算：4 × 3,600 词，这部分和任务难度无关", size=12, anchor="start")

    f.note(40, 226, "二 同一批任务的第三方实测（5 个小题，两边都 15/15 通过）", size=13,
           anchor="start", color="var(--accent2)", weight="600")
    f.note(170, 268, "不加流程", size=12.5, anchor="end")
    f.parts.append('<rect x="180" y="250" width="451" height="30" rx="6" fill="var(--panel2)" '
                   'stroke="var(--line)"/>')
    f.note(640, 270, "$2.44", size=12.5, anchor="start")

    f.note(170, 328, "加了流程", size=12.5, anchor="end")
    f.parts.append('<rect x="180" y="310" width="640" height="30" rx="6" fill="var(--accent)" '
                   'opacity="0.75"/>')
    f.note(828, 330, "$3.46", size=12.5, anchor="start")
    f.note(40, 386, "多花约四成，结果一样。简单任务上，这套流程是纯成本。", size=12.5,
           anchor="start")
    return f


# --------------------------------------------------------------------------
# 9. 第 16 章：两条环
# --------------------------------------------------------------------------

def fig_outerloop():
    f = Fig("outerloop", 620,
            "两条环：上排外循环决定做什么，下排内循环决定做完了；派活往下走，结果回流往上走",
            "上排没有任何插件提供，要自己搭。下排是这本手册第 1 到 13 章的全部内容。")
    xs = [112, 338, 564, 790]
    bw = 176
    top = [("信号流", "工单 语音 聊天"),
           ("队列", "先攒后看，找模式"),
           ("复现闸", "复现不了就不修"),
           ("一条主线", "其余明确判死")]
    bot = [("交接", "说清怎么验的"),
           ("验证", "真实产物"),
           ("实现", "最小改动"),
           ("认领", "一句话带背景")]
    top_y, bot_y = 118, 438

    f.note(40, 72, "外循环 · 决定做什么", size=14, anchor="start",
           color="var(--accent2)", weight="600")
    f.note(40, 536, "内循环 · 决定做完了", size=14, anchor="start",
           color="var(--accent2)", weight="600")

    for i, (t, s) in enumerate(top):
        f.box(xs[i], top_y, t, s, w=bw, kind="accent" if i == 3 else "box")
    for i, (t, s) in enumerate(bot):
        f.box(xs[i], bot_y, t, s, w=bw, kind="accent" if i == 3 else "box")

    for i in range(3):
        f.line(xs[i] + bw / 2, top_y, xs[i + 1] - bw / 2, top_y)
        f.line(xs[i + 1] - bw / 2, bot_y, xs[i] + bw / 2, bot_y)

    f.line(xs[3], top_y + 29, xs[3], bot_y - 29)
    f.note(xs[3] + 16, 268, "派活：目标 + 完成标准", size=12, rotate=90)
    f.line(xs[0], bot_y - 29, xs[0], top_y + 29)
    f.note(xs[0] - 16, 268, "结果与教训回流", size=12, rotate=-90)

    f.note(450, 236, "只装下排：工具很全，但不知道今天该干什么。", size=12.5,
           color="var(--bad)")
    f.note(450, 266, "只装上排：知道该做什么，但每件事都做不完。", size=12.5,
           color="var(--bad)")
    f.note(450, 574, "两排之间只传两样东西：一句带完成标准的话，和一条回流的教训。",
           size=12.5, color="var(--accent2)")
    return f


FIGS = [fig_story, fig_layers, fig_context, fig_flow, fig_bugfix, fig_feature,
        fig_principles, fig_verify, fig_parallel, fig_decide, fig_feynman,
        fig_levels, fig_cost, fig_outerloop]


def main():
    os.makedirs(OUT, exist_ok=True)
    for build in FIGS:
        fig = build()
        with open(os.path.join(OUT, fig.name + ".svg"), "w", encoding="utf-8") as fh:
            fh.write(fig.render())
        print(f"{fig.name:10s} {fig.h}px  {len(''.join(fig.parts))} chars")
    if PROBLEMS:
        print("\nLAYOUT PROBLEMS")
        for p in PROBLEMS:
            print("  " + p)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
