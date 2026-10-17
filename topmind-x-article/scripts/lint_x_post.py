#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lint_x_post.py — X 纯文本帖检查：不含 Markdown 列表/标题/加粗，正文不含链接、来源行和配图说明。

X 的普通帖子不渲染 Markdown。本脚本检查 X 稿，并可把常见 Markdown 写法改成 X 写法。
公众号稿不在检查范围内（公众号稿继续用 Markdown 列表）。规则见 references/x-post-format.md。

用法：
    python3 lint_x_post.py X稿.txt                 # 检查（一个文件里多条帖子用单独一行 --- 分隔）
    python3 lint_x_post.py X稿.txt --fix --out X稿.fixed.txt   # 自动改写后输出到新文件（列表改 🔹 / 1️⃣）
    python3 lint_x_post.py X稿.txt --fix --style plain --out X稿.fixed.txt   # 列表改「·」/「1）」
    python3 lint_x_post.py X发布稿.txt --long      # 长文兜底稿：不查话题标签位置和字数
    python3 lint_x_post.py 段子.txt --duanzi       # 段子体：出现任何 emoji（含列表符号、人设点缀）记 W13
    python3 lint_x_post.py 公众号稿.md --md        # Markdown 稿只查去 AI 味 / 长段落 / 自制图标注
    cat X稿.txt | python3 lint_x_post.py -         # 从标准输入读取

交付规约（x-delivery-contract.md）：X 短文 / 段子的正文是一段可直接复制的纯文本，链接、原图、配图另发。
因此普通帖（非 --long）里：
  E10 正文出现 URL（含来源链接）——链接另发一条；
  E11 正文出现来源行（来源： / 信源： / 出处： / 原帖： / 原文： / 链接： / via: / source:）——另发；
  E12 正文出现配图说明（配图： / 原图： / 图注： / [图1] 占位）——图片另发；
  E8 代码围栏 ```（多半是把交付代码块的围栏一起复制进来了）；E9 删除线 ~~文字~~；--fix 会去掉 E8/E9 符号。
--long（x-article 的 X发布稿.txt 长文兜底稿）允许文内链接，不查 E10–E12。
警告（不影响退出码，--strict 时算失败）：点缀表情过多（W8）、疑似 AI 套话（W9，含排比、「不仅…更…」、空泛形容等）、
首行过长不像钩子（W10）、超过约 1000 字（W7，短文上限，更长的写成 X Article）、连续多个空行（W11）、正文里混入其他非发布内容（W12：说明 / 内部标签 / 帖序号等）、
段子体出现 emoji（W13，需 --duanzi）、长文单段超过约 110 字（W14，需 --long）。
W9 同时查公式化计数标签（「xx三个词」「xx一句话」「xx五个分支」「三件事」），短文、长文都查。
去 AI 味结构检查（规则表 references/de-ai-rules.md，短文、长文、--md 都查）：
  W15 中文结构套话（设问自答、揭晓式冒号、升华收尾、抽象拔高、铺垫过渡、进行+动词、对冲叠加、无出处权威、空洞期许、客服腔）；
  W16 英文结构套话（not X but Y、not just…but、signpost opener、wrap-up filler、transition stack、inflated vocab、role inflation、hedge stack、chatbot residue、in today's…）；
  W17 标点腔（破折号 / 感叹号过多、！！ ？！ 连用）；W18 自制图图注没写「自制」和数据来源（--long / --md 的 ![]() 行）。
  --md：Markdown 稿（公众号稿.md）只查内容类警告，不查 Markdown 语法。
短文分点不强制 emoji：🔹 / 1️⃣ 等 emoji 符号，或「1）」「·」「【小标题】」等纯文本方式都可以；只禁止会被当成 Markdown 的 - * + 1.。

退出码：有错误 → 1；加 --strict 时警告也算失败；其余 → 0。
只用 Python 标准库。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# --- 错误：X 不渲染的 Markdown 语法 -----------------------------------------
UL_RE = re.compile(r"^(\s*)([-*+])\s+(?:\[[ xX]\]\s+)?(\S.*)$")
OL_RE = re.compile(r"^(\s*)(\d{1,3})[.)]\s+(\S.*)$")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+\S")
BOLD_RE = re.compile(r"\*\*[^*\n]+\*\*|(?<![\w_])__[^_\n]+__(?![\w_])")
QUOTE_RE = re.compile(r"^\s*>\s?\S")
LINK_RE = re.compile(r"\[([^\]\n]+)\]\(([^)\s]+)\)")
TABLE_RE = re.compile(r"^\s*\|.*\|\s*$")
CODE_RE = re.compile(r"`[^`\n]+`")
SEP_RE = re.compile(r"^\s*(-{3,}|={3,}|\*{3,})\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
STRIKE_RE = re.compile(r"~~[^~\n]+~~")
# 正文块里不该出现的交付附注（行首）。话题标签属于正文；来源行、链接、配图说明不属于正文（E10–E12）
SOURCE_LINE_RE = re.compile(r"^\s*(?:来源|信源|信息来源|出处|原帖|原文|原文链接|链接|参考|via|source)\s*[:：]", re.I)
IMAGE_LINE_RE = re.compile(r"^\s*(?:(?:配图|原图|图注|图片|插图)\s*[:：]|\[(?:图|图片|配图|视频)[^\]]*\]|【配图[^】]*】)")
NONPUB_RE = re.compile(
    r"^\s*(?:【(?:帖|X ?版|公众号版|信息来源|说明)[^】]*】|[①②③④]\s*(?:正文|原帖|信源|原图)"
    r"|(?:说明|备注|注|标签|内部标签|分类|备选|备选标签|提示词|prompt|发布时间)\s*[:：])",
    re.I,
)
MAX_BLANK_RUN = 1  # 段间只空一行；连续 2 个以上空行记 W11

# --- 项目符号识别（emoji / 纯文本符号 / 序号）----------------------------------
KEYCAP = r"[0-9]\uFE0F?\u20E3"
CIRCLED = r"[\u2460-\u2473]"
SYMBOL = (
    r"(?:[\u00B7\u2022\u25AA\u25AB\u25E6\u2023\u2192\u25B6\u25B8]"
    r"|[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\u2190-\u21FF])\uFE0F?"
)
PLAIN_NUM = r"\d{1,2}）"  # 全角「1）」是纯文本序号，X 不当 Markdown
BULLET_RE = re.compile(r"^(\s*)(%s|%s|%s|%s|\U0001F51F)\s*(\S.*)?$" % (KEYCAP, CIRCLED, PLAIN_NUM, SYMBOL))
HASHTAG_RE = re.compile(r"(?<![\w&#])#(?!\d+(?![\w\u4e00-\u9fff]))[\w\u4e00-\u9fff]{1,40}")  # #2 这类名次不是话题标签
HASHTAG_TAIL_RE = re.compile(r"(?:\s*#(?!\d+(?![\w\u4e00-\u9fff]))[\w\u4e00-\u9fff]{1,40})+\s*$")
PLACEHOLDER_RE = re.compile(r"^\s*\[(?:图|视频|图片|配图)[^\]]*\]\s*$")  # 配图占位行不计字数
URL_RE = re.compile(r"https?://\S+")

KEYCAPS = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
CIRCLED_NUMS = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳"

CONTRAST_PAIR = {"✅", "❌"}
MAX_ITEMS = 7
MAX_LEVELS = 2
MAX_TAGS = 3
CHAR_LIMIT = 1000  # 短文（X 纯文本帖）约 1000 字内；更长的写成长文（X Article）
MAX_DECOR_EMOJI = 4  # 列表符号之外的点缀表情上限（规则建议 1–3 个）

# --- 去 AI 味：常见套话（只警告，不报错；规则见 writing-principles.md「去 AI 味」）--
AI_PHRASES = [
    "综上所述", "总而言之", "值得注意的是", "值得一提的是", "不难发现", "毋庸置疑",
    "让我们一起", "首先，", "其次，", "最后，", "在当今", "随着.{1,12}的发展",
    "颠覆性", "革命性", "一文读懂", "一文看懂", "建议收藏", "干货满满", "赋能",
    "不是.{1,12}而是", "真正的", "从来不是", "一句话总结", "划重点",
    "总的来说", "总体而言", "总体来看", "不仅.{1,16}更", "不仅.{1,16}还", "毫无疑问", "不可否认", "众所周知",
    "重磅", "炸裂", "震撼", "惊艳", "里程碑式", "划时代", "全方位", "一站式", "无缝", "深度赋能",
    "让我们拭目以待", "拭目以待", "未来已来", "这或许就是", "开启.{1,8}新篇章", "新纪元",
    r"更[^\s、，。]{1,3}、更[^\s、，。]{1,3}、更[^\s、，。]{1,3}",
    "进行了一个", "做出了.{0,4}改进",
    # 公式化计数标签：「xx三个词」「xx一句话」「xx五个分支」「三件事」→ 改成「简单总结」「主要 5 个方向」「有三大特征」
    r"[一二三四五六七八九十两0-9]+\s*个(?:词|关键词|字|分支)", "一句话", r"[二三四五六七八九十两]件事",
]
LONG_PARA_MAX = 110  # 长文单段字数上限（不含列表行），超过就拆短或改成列表
HOOK_MAX_WEIGHT = 60  # 首行（钩子）加权字数上限，约 30 个汉字
AI_RE = re.compile("|".join(AI_PHRASES))
EMOJI_RE = re.compile(r"[\U0001F100-\U0001F2FF\U0001F300-\U0001FAFF\u2600-\u27BF]")

# --- 去 AI 味：结构模式（逐行查，只警告；规则表见 references/de-ai-rules.md） ---------
# W15 中文结构套话。每条都是「句式」而不是单个词，正则刻意收窄，宁可漏报也不误报正常写法。
ZH_STRUCT = [
    ("设问自答", r"[？?]\s*(?:答案(?:是|很简单)|很简单[，,：:]|原因(?:很简单|在于)[，,：:]?)"),
    ("揭晓式冒号", r"(?:^|[。！？\s])(?:答案|真相|秘诀)(?:是|就是|其实是)?[：:]\s*\S"),
    ("升华收尾", r"^(?:而)?这(?:或许|也许)?(?:才|就)是[^，。！？\n]{0,14}(?:意义|本质|答案|未来|关键|力量|魅力|价值|真谛)[。！!]?\s*$"),
    ("抽象拔高", r"归根结底|本质上[，,]|某种(?:程度|意义)上|在一定程度上|不言而喻|显而易见的是"),
    ("铺垫过渡", r"(?:废)?话不多说|接下来[，,]?(?:就)?让我们|下面(?:我们)?(?:就)?来(?:看看|聊聊|拆解|盘点)|让我们(?:一起)?来(?:看看|聊聊)"),
    ("进行+动词", r"进行(?:了)?(?:一次|一番|一系列|深入的?|全面的?|有效的?)?(?:分析|研究|讨论|优化|处理|测试|评估|探索|沟通|调整|改进|对比|梳理|总结|介绍|说明|解读)"),
    ("对冲叠加", r"(?:或许|也许)[^。！？\n]{0,6}(?:可能|或许|也许)|可能[^。！？\n也]{0,6}(?:或许|也许)"),
    ("无出处权威", r"(?:专家|业内人士|分析人士|有研究|研究人员|权威人士)(?:普遍)?(?:指出|认为|表示|发现)"),
    ("空洞期许", r"未来可期|让我们(?:共同|一起)(?:期待|见证)|一起见证|值得每一个人"),
    ("客服腔", r"希望(?:这篇|本文|以上|这些)?(?:内容)?(?:能)?对(?:你|您|大家)有(?:所)?帮助|欢迎(?:在评论区)?(?:留言)?交流讨论"),
]
ZH_STRUCT_RE = [(name, re.compile(rx)) for name, rx in ZH_STRUCT]
AUTHORITY_SOURCED_RE = re.compile(r"\d|据|《|https?://|「|“")  # 同一行带数字 / 出处 / 引号的不算无出处
# W16 英文结构套话（英文稿、中英混排都查；只匹配整词，大小写不敏感）
EN_STRUCT = [
    ("not X but Y", r"\b(?:it'?s|this is|that'?s)\s+not\s+(?:just\s+|only\s+)?(?:about\s+)?[\w\s'-]{1,30}[,;—–-]+\s*(?:it'?s|but)\b"),
    ("not just X, but", r"\bnot\s+(?:just|only|merely)\b[^.!?\n]{1,40}\bbut\s+(?:also\s+)?"),
    ("isn't just", r"\b(?:isn'?t|aren'?t|wasn'?t)\s+just\b"),
    ("signpost opener", r"\b(?:here'?s the thing|let'?s dive in|let'?s break (?:it|this) down|buckle up|without further ado|in this (?:post|article), (?:we|i)'?ll)\b"),
    ("wrap-up filler", r"\b(?:in conclusion|in summary|to sum (?:it )?up|all in all|at the end of the day|the bottom line is)\b"),
    ("transition stack", r"(?:^|[.!?]\s+)(?:moreover|furthermore|additionally|consequently),"),
    ("inflated vocab", r"\b(?:delve|delves|delving|tapestry|testament to|pivotal|underscores?|fostering|vibrant|nestled|game[- ]changer|ever[- ]evolving|fast[- ]paced world|seamless(?:ly)?|unparalleled|groundbreaking|revolutioni[sz]e)\b"),
    ("role inflation", r"\b(?:plays? a (?:crucial|pivotal|vital|key) role|serves as a|stands as a|marks a (?:significant|major) (?:shift|milestone))\b"),
    ("hedge stack", r"\b(?:it is|it'?s) (?:important|worth) (?:to note|noting)\b|\bit'?s worth mentioning\b"),
    ("chatbot residue", r"\b(?:i hope this helps|great question|certainly!|as an ai\b|feel free to (?:ask|reach out)|happy to help)"),
    ("in today's", r"\bin today'?s (?:\w+[- ])?(?:world|landscape|era|age)\b"),
]
EN_STRUCT_RE = [(name, re.compile(rx, re.I)) for name, rx in EN_STRUCT]
# W17 标点腔：破折号、感叹号堆叠，连用标点
DASH_RE = re.compile(r"——|—")
BANG_RE = re.compile(r"[！!](?!=)")
PUNCT_RUN_RE = re.compile(r"[！!？?]{2,}")
DASH_SHORT_MAX = 2       # 短文破折号最多 2 处
BANG_SHORT_MAX = 2       # 短文感叹号最多 2 个
DENSITY_PER_K = 3        # 长文：每 1000 字超过 3 处破折号 / 感叹号才报
# W18 自制图标注（--md / --long 的 Markdown 图片行）：自制图 alt 里要写「自制」和数据来源
MD_IMG_RE = re.compile(r"^\s*!\[([^\]]*)\]\(([^)\s]+)[^)]*\)\s*$")
SELFMADE_HINT_RE = re.compile(r"自制|self[- ]?made", re.I)
SOURCE_HINT_RE = re.compile(r"数据|来源|据|source|data", re.I)


def struct_hits(lines: list[str], start: int):
    """逐行查 W15 / W16，返回 [(行号, 代码, 说明)]；同一条规则在一篇里最多报 3 处。"""
    out, seen = [], {}
    in_fence = False
    for off, ln in enumerate(lines):
        if FENCE_RE.match(ln):
            in_fence = not in_fence
            continue
        if in_fence or not ln.strip() or URL_RE.fullmatch(ln.strip()):
            continue
        body = URL_RE.sub("", ln)
        for name, rx in ZH_STRUCT_RE:
            m = rx.search(body)
            if not m:
                continue
            if name == "无出处权威" and AUTHORITY_SOURCED_RE.search(body):
                continue
            seen[name] = seen.get(name, 0) + 1
            if seen[name] <= 3:
                out.append((start + off, "W15", f"中文结构套话「{name}」：{m.group(0).strip()[:24]}；按 de-ai-rules.md 改写"))
        for name, rx in EN_STRUCT_RE:
            m = rx.search(body)
            if not m:
                continue
            seen[name] = seen.get(name, 0) + 1
            if seen[name] <= 3:
                out.append((start + off, "W16", f"英文结构套话「{name}」：{m.group(0).strip()[:32]}；按 de-ai-rules.md 改写"))
    return out


def punct_hits(lines: list[str], start: int, long_mode: bool):
    text = "\n".join(ln for ln in lines if not FENCE_RE.match(ln))
    out = []
    for off, ln in enumerate(lines):
        m = PUNCT_RUN_RE.search(ln)
        if m:
            out.append((start + off, "W17", f"标点连用「{m.group(0)}」：一个就够"))
            break
    n_chars = max(1, sum(1 for ch in text if not ch.isspace()))
    dashes, bangs = len(DASH_RE.findall(text)), len(BANG_RE.findall(text))
    if long_mode:
        lim = max(3, DENSITY_PER_K * n_chars / 1000)
        if dashes > lim:
            out.append((start, "W17", f"破折号 {dashes} 处（约 {n_chars} 字）：多数改成逗号、句号或冒号"))
        if bangs > lim:
            out.append((start, "W17", f"感叹号 {bangs} 个（约 {n_chars} 字）：语气靠事实，不靠感叹号"))
    else:
        if dashes > DASH_SHORT_MAX:
            out.append((start, "W17", f"破折号 {dashes} 处：短文最多 {DASH_SHORT_MAX} 处，其余改成逗号、句号或冒号"))
        if bangs > BANG_SHORT_MAX:
            out.append((start, "W17", f"感叹号 {bangs} 个：短文最多 {BANG_SHORT_MAX} 个"))
    return out


def image_label_hits(lines: list[str], start: int):
    out = []
    for off, ln in enumerate(lines):
        m = MD_IMG_RE.match(ln)
        if not m:
            continue
        alt, path = m.group(1), m.group(2)
        if SELFMADE_HINT_RE.search(alt + " " + path) and not (SELFMADE_HINT_RE.search(alt) and SOURCE_HINT_RE.search(alt)):
            out.append((start + off, "W18", "自制图没标清楚：图注（alt）里写「自制」和数据来源，例如「自制，数据：xx 官方」"))
    return out


def md_to_plain(lines: list[str]) -> list[str]:
    """--md：把 Markdown 稿（公众号稿）转成逐行对应的纯文本，只为跑内容检查；行号不变。"""
    out, in_fm, in_fence = [], False, False
    for i, ln in enumerate(lines):
        if i == 0 and ln.strip() == "---":
            in_fm = True
            out.append("")
            continue
        if in_fm:
            if ln.strip() == "---":
                in_fm = False
            out.append("")
            continue
        if FENCE_RE.match(ln):
            in_fence = not in_fence
            out.append("")
            continue
        if in_fence or TABLE_RE.match(ln) or SEP_RE.match(ln) or HEADING_RE.match(ln) or MD_IMG_RE.match(ln):
            out.append("")
            continue
        t = QUOTE_RE.sub("", ln) if QUOTE_RE.match(ln) else ln
        t = re.sub(r"^(\s*)(?:[-*+]|\d{1,3}[.)])\s+", r"\1· ", t)
        t = BOLD_RE.sub(lambda m: m.group(0).strip("*_"), t)
        t = LINK_RE.sub(lambda m: m.group(1), t)
        t = CODE_RE.sub(lambda m: m.group(0).strip("`"), t)
        out.append(t)
    return out


def _is_wide(ch: str) -> bool:
    o = ord(ch)
    return (
        0x1100 <= o <= 0x115F or 0x2E80 <= o <= 0xA4CF or 0xAC00 <= o <= 0xD7A3
        or 0xF900 <= o <= 0xFAFF or 0xFE30 <= o <= 0xFE6F or 0xFF00 <= o <= 0xFF60
        or 0xFFE0 <= o <= 0xFFE6 or 0x1F300 <= o <= 0x1FAFF or 0x2600 <= o <= 0x27BF
    )


def x_weight(text: str) -> int:
    """近似 X 的加权字数：中日韩与 emoji 记 2，其余记 1，链接固定记 23。"""
    text = URL_RE.sub("", text) + "u" * 23 * len(URL_RE.findall(text))
    return sum(0 if ch in "\uFE0F\u200D" else (2 if _is_wide(ch) else 1) for ch in text)


def indent_width(prefix: str) -> int:
    return len(prefix.replace("\t", "    ").replace("\u3000", "  "))


def split_posts(text: str, long_mode: bool):
    """返回 [(起始行号, [行...])]。长文模式整份当一篇。"""
    lines = text.splitlines()
    if long_mode:
        return [(1, lines)]
    posts, cur, start = [], [], 1
    for i, ln in enumerate(lines, 1):
        if SEP_RE.match(ln):
            posts.append((start, cur))
            cur, start = [], i + 1
        else:
            cur.append(ln)
    posts.append((start, cur))
    return [p for p in posts if any(x.strip() for x in p[1])]


def keycap_for(n: int) -> str:
    if 0 <= n <= 9:
        return KEYCAPS[n]
    if n == 10:
        return "🔟"
    if 11 <= n <= 20:
        return CIRCLED_NUMS[n - 1]
    return f"{n}）"


DUANZI_EMOJI_RE = re.compile(
    r"[\U0001F100-\U0001F2FF\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\u25AA\u25AB\u2022\u20E3\u2460-\u2473]"
)


def lint_post(start: int, lines: list[str], long_mode: bool, duanzi: bool = False):
    """返回 (errors, warnings)，元素为 (行号, 代码, 说明)。"""
    errs, warns = [], []
    in_fence = False
    bullets = []  # (行号, 缩进宽度, 符号)
    blank_run = 0
    for off, ln in enumerate(lines):
        no = start + off
        if not ln.strip():
            blank_run += 1
            if blank_run == MAX_BLANK_RUN + 1:
                warns.append((no, "W11", "连续多个空行：段与段之间只空一行"))
        else:
            blank_run = 0
        if FENCE_RE.match(ln):
            if not long_mode:
                errs.append((no, "E8", "代码围栏（``` / ~~~）：X 不渲染，复制正文时不要带上代码块围栏"))
                continue
            in_fence = not in_fence
            continue
        if duanzi and DUANZI_EMOJI_RE.search(ln):
            warns.append((no, "W13", "段子体不用 emoji（含人设点缀和列表符号）：分点一条一行、靠行间空行区分"))
        if not long_mode:
            if URL_RE.search(ln):
                errs.append((no, "E10", "正文里有 URL：X 短文 / 段子的链接（含来源链接）另发一条，不和正文混在一起"))
            if SOURCE_LINE_RE.match(ln):
                errs.append((no, "E11", "正文里有来源行：来源 / 原帖链接另发，正文只放可发布的纯文本"))
            if IMAGE_LINE_RE.match(ln):
                errs.append((no, "E12", "正文里有配图说明或图片占位：原图 / 配图另发"))
            elif NONPUB_RE.match(ln):
                warns.append((no, "W12", "正文里混入非发布内容（说明 / 内部标签 / 帖序号等）：另列，不放进可复制正文"))
        if STRIKE_RE.search(ln):
            errs.append((no, "E9", "Markdown 删除线（~~）：X 不渲染，去掉波浪线"))
        if in_fence or (long_mode and indent_width(ln[: len(ln) - len(ln.lstrip())]) >= 4 and ln.strip()):
            continue
        if UL_RE.match(ln) and not SEP_RE.match(ln):
            errs.append((no, "E1", "Markdown 无序列表（- * +）：X 不渲染，改用「·」「1）」或 🔹 等符号"))
        elif OL_RE.match(ln):
            errs.append((no, "E2", "Markdown 有序列表（1. / 1)）：改用全角「1）」、① ② ③ 或 1️⃣ 2️⃣ 3️⃣"))
        if HEADING_RE.match(ln):
            errs.append((no, "E3", "Markdown 标题（#）：X 不渲染，改成普通文字行"))
        if BOLD_RE.search(ln):
            errs.append((no, "E4", "Markdown 加粗（**）：X 不渲染，去掉星号"))
        if QUOTE_RE.match(ln):
            errs.append((no, "E5", "Markdown 引用（>）：去掉 >，引文用「」"))
        if LINK_RE.search(ln):
            errs.append((no, "E6", "Markdown 链接 [文字](url)：改成「文字 url」或直接贴 url"))
        if TABLE_RE.match(ln):
            errs.append((no, "E7", "Markdown 表格：拆成“项：值”的列表行"))
        if CODE_RE.search(ln):
            warns.append((no, "W1", "行内反引号：X 不渲染，会原样显示反引号"))
        m = BULLET_RE.match(ln)
        is_title = not any(x.strip() for x in lines[:off])  # 首行的标题 emoji 不算列表项
        if m and m.group(3) and not is_title:
            bullets.append((no, indent_width(m.group(1)), m.group(2).replace("\uFE0F", "")))

    # 按连续的列表块分别检查（空行或正文行隔开的是不同的列表）
    blocks, cur = [], []
    def _gap_has_text(a: int, b: int) -> bool:
        # 两个列表项之间只有空行（段子体行间空行）仍算同一个列表
        return any(lines[k - start].strip() for k in range(a + 1, b))

    def _family(sym: str) -> str:
        return "num" if (sym.endswith("\u20e3") or re.fullmatch(CIRCLED + "|\U0001F51F|" + PLAIN_NUM, sym)) else sym

    for item in bullets:
        gap = cur and item[0] - cur[-1][0] > 1
        # 空行隔开、符号体系不同的，算两个列表（如先「1）」再「·」）
        if gap and (_gap_has_text(cur[-1][0], item[0]) or _family(item[2]) != _family(cur[-1][2])):
            blocks.append(cur)
            cur = []
        cur.append(item)
    if cur:
        blocks.append(cur)
    for blk in blocks:
        widths = sorted({w for _, w, _ in blk})
        if len(widths) > MAX_LEVELS:
            warns.append((blk[0][0], "W2", f"列表缩进超过 {MAX_LEVELS} 层（出现 {len(widths)} 种缩进）"))
        for w in widths:
            kinds = {s for _, ww, s in blk if ww == w}
            numbered = all(k.endswith("\u20e3") or re.fullmatch(CIRCLED + "|\U0001F51F|" + PLAIN_NUM, k) for k in kinds)
            if len(kinds) > 1 and not numbered and not kinds <= CONTRAST_PAIR:
                warns.append((blk[0][0], "W3", "同一层级混用了多种项目符号：" + " ".join(sorted(kinds))))
        top = [no for no, w, _ in blk if w == widths[0]]
        if len(top) > MAX_ITEMS:
            warns.append((top[0], "W4", f"一个列表有 {len(top)} 条，超过 {MAX_ITEMS} 条，建议精简或拆成两帖"))

    if not long_mode:
        body = [ln for ln in lines if ln.strip()]
        if body:
            last = body[-1]
            tail = HASHTAG_TAIL_RE.sub("", last)
            rest = "\n".join(body[:-1] + [tail])
            mid = HASHTAG_RE.findall(rest)
            if mid:
                warns.append((start, "W5", "话题标签应放在最后一行，正文中间出现了：" + " ".join(mid[:3])))
            tags = HASHTAG_RE.findall("\n".join(lines))
            if len(tags) > MAX_TAGS:
                warns.append((start, "W6", f"话题标签 {len(tags)} 个，建议不超过 {MAX_TAGS} 个"))
        text_all = "\n".join(lines)
        decor = 0
        for ln in lines:
            bm = BULLET_RE.match(ln)
            rest_ln = (bm.group(3) or "") if bm else ln
            decor += len(EMOJI_RE.findall(rest_ln))
        if decor > MAX_DECOR_EMOJI:
            warns.append((start, "W8", f"点缀表情 {decor} 个（列表符号不计），建议 1–3 个，避免杂乱"))
        first = next((ln for ln in lines if ln.strip()), "")
        if x_weight(first) > HOOK_MAX_WEIGHT:
            warns.append((start, "W10", f"首行加权字数约 {x_weight(first)}，超过 {HOOK_MAX_WEIGHT}（约 30 个汉字）：首行做钩子，先给结论或最扎眼的数字"))
        n = sum(1 for ch in URL_RE.sub("", "\n".join(ln for ln in lines if not PLACEHOLDER_RE.match(ln))) if not ch.isspace())
        if n > CHAR_LIMIT:
            warns.append((start, "W7", f"约 {n} 字，超过短文的 {CHAR_LIMIT} 字左右；这么长的内容写成长文（X Article）"))
    hits = sorted({m.group(0) for m in AI_RE.finditer("\n".join(lines))})
    if hits:
        warns.append((start, "W9", "疑似 AI 套话：" + " / ".join(hits[:4]) + "；改成平实说法或删掉"))
    if long_mode:
        for off, ln in enumerate(lines):
            if ln.strip() and not BULLET_RE.match(ln):
                n = sum(1 for ch in URL_RE.sub("", ln) if not ch.isspace())
                if n > LONG_PARA_MAX:
                    warns.append((start + off, "W14", f"这一段约 {n} 字，超过 {LONG_PARA_MAX} 字：拆成短段，或改成「概要 + 列表」，能用图说明的就删字"))
    warns.extend(struct_hits(lines, start))
    warns.extend(punct_hits(lines, start, long_mode))
    if long_mode:
        warns.extend(image_label_hits(lines, start))
    return errs, warns


def fix_lines(lines: list[str], long_mode: bool, style: str = "emoji") -> list[str]:
    """把 Markdown 列表/标题/加粗/引用/链接改成 X 纯文本写法；表格与其他情况不自动处理。"""
    out, in_fence = [], False
    counters: dict[int, int] = {}
    for ln in lines:
        if FENCE_RE.match(ln):
            if not long_mode:
                continue  # 普通帖：去掉误带的代码块围栏
            in_fence = not in_fence
            out.append(ln)
            continue
        if in_fence or (long_mode and indent_width(ln[: len(ln) - len(ln.lstrip())]) >= 4 and ln.strip()):
            out.append(ln)
            continue
        if SEP_RE.match(ln):
            out.append(ln)
            continue
        s = ln
        m = UL_RE.match(s)
        o = OL_RE.match(s) if not m else None
        if m:
            level = 0 if indent_width(m.group(1)) == 0 else 1
            if style == "plain":
                s = ("  " * level) + "· " + m.group(3)
            else:
                s = ("  " * level) + ("🔹 " if level == 0 else "▫️ ") + m.group(3)
        elif o:
            w = indent_width(o.group(1))
            level = 0 if w == 0 else 1
            counters[level] = counters.get(level, 0) + 1
            mark = f"{int(o.group(2))}）" if style == "plain" else keycap_for(int(o.group(2))) + " "
            s = ("  " * level) + mark + o.group(3)
        else:
            if not ln.strip():
                counters.clear()
            s = re.sub(r"^\s{0,3}#{1,6}\s+", "", s)
            s = re.sub(r"^\s*>\s?", "", s)
        s = re.sub(r"\*\*([^*\n]+)\*\*", r"\1", s)
        s = re.sub(r"(?<![\w_])__([^_\n]+)__(?![\w_])", r"\1", s)
        s = STRIKE_RE.sub(lambda mm: mm.group(0)[2:-2], s)
        s = LINK_RE.sub(lambda mm: f"{mm.group(1)} {mm.group(2)}", s)
        s = CODE_RE.sub(lambda mm: mm.group(0).strip("`"), s)
        out.append(s)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="X 纯文本帖检查：无 Markdown 列表/标题/加粗，正文不含链接/来源行/配图说明")
    ap.add_argument("files", nargs="+", help="X 稿文件，- 表示标准输入")
    ap.add_argument("--long", action="store_true", help="长文兜底稿模式（X发布稿.txt）：整份当一篇，不查话题标签位置和字数")
    ap.add_argument("--fix", action="store_true", help="自动改写 Markdown 写法为 X 写法（需 --out；只处理单个文件）")
    ap.add_argument("--out", help="--fix 的输出文件")
    ap.add_argument("--style", choices=["emoji", "plain"], default="emoji", help="--fix 的列表写法：emoji（🔹 / 1️⃣，默认）或 plain（· / 1））")
    ap.add_argument("--duanzi", action="store_true", help="段子体模式：出现任何 emoji（含列表符号、人设点缀）记 W13")
    ap.add_argument("--strict", action="store_true", help="警告也算失败")
    ap.add_argument("--md", action="store_true", help="Markdown 稿（公众号稿 / X长文.md）只查内容：去 AI 味（W9、W15–W17）、长段落（W14）、自制图标注（W18）；不查 Markdown 语法")
    args = ap.parse_args()

    if args.fix:
        if len(args.files) != 1 or not args.out:
            print("错误：--fix 需要恰好一个输入文件，并用 --out 指定输出文件", file=sys.stderr)
            return 2
        src = args.files[0]
        text = sys.stdin.read() if src == "-" else Path(src).read_text(encoding="utf-8-sig")
        fixed = "\n".join(fix_lines(text.splitlines(), args.long, args.style)) + "\n"
        Path(args.out).write_text(fixed, encoding="utf-8")
        print(f"已写出 {args.out}")
        args.files = [args.out]

    total_e = total_w = 0
    for f in args.files:
        try:
            text = sys.stdin.read() if f == "-" else Path(f).read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError) as e:
            print(f"错误：无法读取 {f}（{e}）", file=sys.stderr)
            return 2
        if args.md:
            raw = text.splitlines()
            plain = md_to_plain(raw)
            errs, warns = lint_post(1, plain, True, False)
            errs = []  # Markdown 语法在公众号稿里是合法的，只保留内容类警告
            warns = [w for w in warns if w[1] in ("W9", "W14", "W15", "W16", "W17")] + image_label_hits(raw, 1)
            for no, code, msg in sorted(warns):
                print(f"{f}:{no}: [{code}] 警告：{msg}")
            total_w += len(warns)
            continue
        for idx, (start, lines) in enumerate(split_posts(text, args.long), 1):
            errs, warns = lint_post(start, lines, args.long, args.duanzi)
            label = "" if args.long else f"#帖{idx} "
            for no, code, msg in errs:
                print(f"{f}:{no}: {label}[{code}] 错误：{msg}")
            for no, code, msg in warns:
                print(f"{f}:{no}: {label}[{code}] 警告：{msg}")
            total_e += len(errs)
            total_w += len(warns)
    status = "通过" if not total_e and not (args.strict and total_w) else "未通过"
    print(f"lint_x_post：{status}（错误 {total_e}，警告 {total_w}）")
    return 1 if total_e or (args.strict and total_w) else 0


if __name__ == "__main__":
    sys.exit(main())
