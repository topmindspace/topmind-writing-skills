#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""de_ai_lint.py — 去 AI 味检查（规则表见 references/de-ai-rules.md，场景规则见 references/core-voice.md）。

三级输出：
  E  错误：只在 lint_x_post.py（X 格式）和 check_article.py（长文源稿结构）里出现，本脚本不出 E。
  W  警告：强信号（结构套话、图片复述、过渡句……）。交付前每条要有结论：改掉，或写明保留理由。
  H  提示：语境词和可能合理的写法（「毫无疑问」「重磅」「拭目以待」……）。只列出，按 core-voice 的场景判断，
     不要求改，不计入 --strict 失败。

用法：
    python3 de_ai_lint.py 稿子.md                    # .md 自动按 Markdown 处理，默认文体 long
    python3 de_ai_lint.py 短文.txt --genre short     # 文体：long / short / duanzi / reply / title
    python3 de_ai_lint.py 稿子.md --json             # 机器可读输出（revise_check.py 用）
    python3 de_ai_lint.py 稿子.md --no-hints         # 不打印 H 级提示
    python3 de_ai_lint.py 稿子.md --strict           # W 也算失败（H 永远不算）

lint_x_post.py 复用本文件的规则（import），原有警告编号 W9、W14–W18 不变。
退出码：--strict 且有 W → 1；读文件失败 → 2；其余 → 0。只用 Python 标准库。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

GENRES = ("long", "short", "duanzi", "reply", "title")

# --- 通用正则（lint_x_post.py 也用这些） ---------------------------------------
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+\S")
BOLD_RE = re.compile(r"\*\*[^*\n]+\*\*|(?<![\w_])__[^_\n]+__(?![\w_])")
QUOTE_RE = re.compile(r"^\s*>\s?\S")
LINK_RE = re.compile(r"\[([^\]\n]+)\]\(([^)\s]+)\)")
TABLE_RE = re.compile(r"^\s*\|.*\|\s*$")
CODE_RE = re.compile(r"`[^`\n]+`")
SEP_RE = re.compile(r"^\s*(-{3,}|={3,}|\*{3,})\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
URL_RE = re.compile(r"https?://\S+")
MD_IMG_RE = re.compile(r"^\s*!\[([^\]]*)\]\(([^)\s]+)[^)]*\)\s*$")
EMOJI_RE = re.compile(r"[\U0001F100-\U0001F2FF\U0001F300-\U0001FAFF\u2600-\u27BF]")
CJK_RE = re.compile(r"[\u4e00-\u9fff]")

# --- W9：套话词（强信号，见一次就看） -------------------------------------------
# 语境词（毫无疑问、归根结底、真正的、重磅、里程碑式、未来已来、拭目以待、一文读懂、总结来说……）
# 不在这里，在下面的 H1：作者在合适的场景里会用，脚本只提示。
AI_PHRASES = [
    "综上所述", "总而言之", "值得注意的是", "值得一提的是", "不难发现", "毋庸置疑",
    "让我们一起", "首先，", "其次，", "最后，", "在当今", "随着.{1,12}的发展",
    "颠覆性", "革命性", "建议收藏", "干货满满", "赋能",
    "不是.{1,12}而是", "从来不是", "一句话总结", "划重点",
    "总体而言", "总体来看", "不仅.{1,16}更", "不仅.{1,16}还", "众所周知",
    "炸裂", "震撼", "惊艳", "划时代", "全方位", "一站式", "无缝", "深度赋能",
    "让我们拭目以待", "这或许就是", "开启.{1,8}新篇章", "新纪元",
    r"更[^\s、，。]{1,3}、更[^\s、，。]{1,3}、更[^\s、，。]{1,3}",
    "进行了一个", "做出了.{0,4}改进",
    # 公式化计数标签：「xx三个词」「xx一句话」「xx五个分支」「三件事」→「简单总结」「主要 5 个方向」「有三大特征」
    r"[一二三四五六七八九十两0-9]+\s*个(?:词|关键词|字|分支)", "一句话", r"[二三四五六七八九十两]件事",
]
AI_RE = re.compile("|".join(AI_PHRASES))
NOT_BUT_RE = re.compile(r"不是.{1,12}而是")

# --- H1：语境词（只提示） ------------------------------------------------------
CONTEXT_WORDS = [
    (r"一文(?:读懂|看懂)", "摘要里可以用；标题里确认是概括式用法", "V04"),
    (r"毫无疑问|不可否认", "后面要接判断和依据，空着就删", "V08"),
    (r"归根结底", "后面那句有实质内容就留", "V08"),
    (r"真正的", "看场景可用；「真正的 X 从来不是」才是套话", "总原则 2"),
    (r"重磅|里程碑式?", "只给真重磅、真里程碑；平常更新用是小题大做", "V20"),
    (r"未来已来|(?<!让我们)拭目以待", "长文口语收尾可以，别和升华句叠用", "V10"),
    (r"总结来说|总的来说", "收尾用一次可以", "V10"),
]
CONTEXT_RE = [(re.compile(rx), tip, ref) for rx, tip, ref in CONTEXT_WORDS]

# --- W15 中文结构套话。每条都是「句式」，正则刻意收窄，宁可漏报也不误报 -----------------
ZH_STRUCT = [
    ("设问自答", r"[？?]\s*(?:答案(?:是|很简单)|很简单[，,：:]|原因(?:很简单|在于)[，,：:]?)"),
    ("揭晓式冒号", r"(?:^|[。！？\s])(?:答案|真相|秘诀)(?:是|就是|其实是)?[：:]\s*\S"),
    ("升华收尾", r"^(?:而)?这(?:或许|也许)?(?:才|就)是[^，。！？\n]{0,14}(?:意义|本质|答案|未来|关键|力量|魅力|价值|真谛)[。！!]?\s*$"),
    ("抽象拔高", r"本质上[，,]|某种(?:程度|意义)上|在一定程度上|不言而喻|显而易见的是|深层(?:次)?博弈"),
    ("铺垫过渡", r"(?:废)?话不多说|接下来[，,]?(?:就)?让我们|下面(?:我们)?(?:就)?来(?:看看|聊聊|拆解|盘点)|让我们(?:一起)?来(?:看看|聊聊)"),
    ("进行+动词", r"进行(?:了)?(?:一次|一番|一系列|深入的?|全面的?|有效的?)?(?:分析|研究|讨论|优化|处理|测试|评估|探索|沟通|调整|改进|对比|梳理|总结|介绍|说明|解读)"),
    ("对冲叠加", r"(?:或许|也许)[^。！？\n]{0,6}(?:可能|或许|也许)|可能[^。！？\n也]{0,6}(?:或许|也许)"),
    ("无出处权威", r"(?:专家|业内人士|分析人士|有研究|研究人员|权威人士)(?:普遍)?(?:指出|认为|表示|发现)"),
    ("空洞期许", r"未来可期|让我们(?:共同|一起)(?:期待|见证)|一起见证|值得每一个人"),
    ("客服腔", r"希望(?:这篇|本文|以上|这些)?(?:内容)?(?:能)?对(?:你|您|大家)有(?:所)?帮助|欢迎(?:在评论区)?(?:留言)?交流讨论"),
]
ZH_STRUCT_RE = [(name, re.compile(rx)) for name, rx in ZH_STRUCT]
AUTHORITY_SOURCED_RE = re.compile(r"\d|据|《|https?://|「|“")  # 同一行带数字 / 出处 / 引号的不算无出处

# --- W16 英文结构套话（整词，大小写不敏感） ---------------------------------------
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

# --- W17 标点腔 ------------------------------------------------------------------
DASH_RE = re.compile(r"——|—")
BANG_RE = re.compile(r"[！!](?!=)")
PUNCT_RUN_RE = re.compile(r"[！!？?]{2,}")
QE_RE = re.compile(r"^[？?][！!]$")          # 「？！」：未完全核实的热点首行 / 标题可用一次
DOUBLE_BANG_RE = re.compile(r"^[！!]{2}$")   # 「！！」：短文（转发点评）一处只提示
DASH_SHORT_MAX = 2
BANG_SHORT_MAX = 2
DENSITY_PER_K = 3

# --- W18 自制图标注 ----------------------------------------------------------------
SELFMADE_HINT_RE = re.compile(r"自制|self[- ]?made", re.I)
SOURCE_HINT_RE = re.compile(r"数据|来源|据|source|data", re.I)

# --- W19 / H12：「人名说：」式引语和对话 → 「人名：」 ---------------------------------
SAY_COLON_RE = re.compile(r"^\s*[\u4e00-\u9fffA-Za-z][\u4e00-\u9fffA-Za-z0-9 ·.]{0,9}说\s*[：:]")
# --- W20：小节过渡句、不言自明的引导语 ---------------------------------------------
TRANSITION_RE = re.compile(
    r"(?:说|聊|讲|看|回顾)完[^，。！？\n]{1,12}[，,]?\s*(?:我们)?再(?:来)?(?:看|聊|说)"
    r"|先(?:来)?看(?:一下|一看|看)?时间线|我们先来(?:看|聊|回顾)"
)
# --- W21：图片复述 -------------------------------------------------------------------
IMG_RETELL_RE = re.compile(r"如图所示|如下图|见下图|从图中(?:可以)?看(?:到|出)|(?:上|下)图(?:展示|显示|可以看到|中可以看到)")

# --- H 级（只提示） ---------------------------------------------------------------------
I_THINK_RE = re.compile(r"我(?:个人)?认为|我觉得|我的判断是?")                               # H3
NEWS_PRECISION_RE = re.compile(
    r"(?:大约|约)\s*\d|\d[\d.]*\s*(?:万|亿|千|百)?\s*(?:个|人|元|美元|次|款|家|倍|%|颗|star|星)?\s*左右|较[^，。！？\n]{1,12}高出"
)                                                                                          # H4
THOUSANDS_RE = re.compile(r"(?<![\d.,])\d{1,3}(?:,\d{3})+(?![\d,])")                       # H4（中文正文里的千分位）
PARALLEL_CLOSE_RE = re.compile(
    r"([\u4e00-\u9fff]{1,6})在([\u4e00-\u9fff]{1,8})[，,]\s*([\u4e00-\u9fff]{1,6})在([\u4e00-\u9fff]{1,8})[。！]?\s*$"
)                                                                                          # H5（「谁…谁就…」不报）
SOURCE_DESC_RE = re.compile(r"^\s*来源\s*[:：].*(?:曲线|趋势|走势|增长图|示意)")             # H6
FILLER_INFO_RE = re.compile(r"(?:暂|尚|还)未(?:作出|做出)?回应|截图为证|范围(?:还|尚)?不清楚|据(?:相关|媒体|外媒|网友)?报道")  # H8
TITLE_PREACH_RE = re.compile(r"你还在.{1,20}吗|难道.{1,20}[？?]|为什么你.{0,20}[？?]|你真的.{1,20}吗")  # H9
SENT_END_RE = re.compile(r"[。！？!?]")
HASHTAG_RE = re.compile(r"(?<![\w&#])#(?!\d+(?![\w\u4e00-\u9fff]))[\w\u4e00-\u9fff]{1,40}")
LIST_EMOJI_RE = re.compile(r"^\s*(?:[0-9]\uFE0F?\u20E3|[\U0001F300-\U0001FAFF\u2600-\u27BF]\uFE0F?)\s*\S")

LONG_PARA_MAX = 110
MAX_PER_RULE = 3
SHORT_TAGS_MAX = 2
DECOR_HINT_MAX = 3

HINT_CODES = {
    "H1": "语境词", "H2": "可接受的连用标点", "H3": "「我认为」式观点句", "H4": "新闻式精确",
    "H5": "对仗收句", "H6": "来源行描述图", "H7": "emoji 过密", "H8": "无效信息",
    "H9": "标题反问说教", "H10": "段落句子多", "H11": "话题标签多", "H12": "「人名说：」",
}


# =============================================================================
def md_to_plain(lines: list[str]) -> list[str]:
    """Markdown 稿转成逐行对应的纯文本，只为跑内容检查；行号不变。标题、图片、表格、代码行置空。"""
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


def _iter_body(lines: list[str]):
    in_fence = False
    for off, ln in enumerate(lines):
        if FENCE_RE.match(ln):
            in_fence = not in_fence
            continue
        if in_fence or not ln.strip() or URL_RE.fullmatch(ln.strip()):
            continue
        yield off, URL_RE.sub("", ln)


def phrase_hits(lines: list[str], start: int):
    """W9：返回 [(行号, 'W9', 说明)]（整篇汇总成一条，和旧版一致）。"""
    hits = sorted({m.group(0) for m in AI_RE.finditer("\n".join(lines))})
    if not hits:
        return []
    msg = "疑似 AI 套话：" + " / ".join(hits[:4]) + "；改成平实说法或删掉"
    if any(NOT_BUT_RE.fullmatch(h) for h in hits):
        msg += "（「不是…而是」优先改成「其实是…」）"
    return [(start, "W9", msg)]


def struct_hits(lines: list[str], start: int):
    """逐行查 W15 / W16，返回 [(行号, 代码, 说明)]；同一条规则在一篇里最多报 3 处。"""
    out, seen = [], {}
    for off, body in _iter_body(lines):
        for name, rx in ZH_STRUCT_RE:
            m = rx.search(body)
            if not m:
                continue
            if name == "无出处权威" and AUTHORITY_SOURCED_RE.search(body):
                continue
            seen[name] = seen.get(name, 0) + 1
            if seen[name] <= MAX_PER_RULE:
                out.append((start + off, "W15", f"中文结构套话「{name}」：{m.group(0).strip()[:24]}；按 de-ai-rules.md 改写"))
        for name, rx in EN_STRUCT_RE:
            m = rx.search(body)
            if not m:
                continue
            seen[name] = seen.get(name, 0) + 1
            if seen[name] <= MAX_PER_RULE:
                out.append((start + off, "W16", f"英文结构套话「{name}」：{m.group(0).strip()[:32]}；按 de-ai-rules.md 改写"))
    return out


def _first_body_index(lines: list[str]) -> int:
    return next((i for i, ln in enumerate(lines) if ln.strip()), -1)


def punct_split(lines: list[str], start: int, long_mode: bool):
    """W17 与 H2。「？！」在首行 / 标题出现一次不报；短文「！！」一处只提示。返回 (warns, hints)。"""
    text = "\n".join(ln for ln in lines if not FENCE_RE.match(ln))
    warns, hints = [], []
    first = _first_body_index(lines)
    qe_used = bang_used = False
    for off, ln in enumerate(lines):
        for m in PUNCT_RUN_RE.finditer(ln):
            run = m.group(0)
            if QE_RE.match(run) and off == first and not qe_used:
                qe_used = True
                continue
            if DOUBLE_BANG_RE.match(run) and not long_mode and not bang_used:
                bang_used = True
                hints.append((start + off, "H2", f"「{run}」：转发点评、惊讶语气可以用一处"))
                continue
            warns.append((start + off, "W17", f"标点连用「{run}」：一个就够"))
            break
        if any(w[1] == "W17" for w in warns):
            break
    n_chars = max(1, sum(1 for ch in text if not ch.isspace()))
    dashes = len(DASH_RE.findall(text))
    bangs = len(BANG_RE.findall(text))
    if long_mode:
        lim = max(3, DENSITY_PER_K * n_chars / 1000)
        if dashes > lim:
            warns.append((start, "W17", f"破折号 {dashes} 处（约 {n_chars} 字）：多数改成逗号、句号或冒号"))
        if bangs > lim:
            warns.append((start, "W17", f"感叹号 {bangs} 个（约 {n_chars} 字）：语气靠事实，不靠感叹号"))
    else:
        if dashes > DASH_SHORT_MAX:
            warns.append((start, "W17", f"破折号 {dashes} 处：短文最多 {DASH_SHORT_MAX} 处，其余改成逗号、句号或冒号"))
        if bangs > BANG_SHORT_MAX:
            warns.append((start, "W17", f"感叹号 {bangs} 个：短文最多 {BANG_SHORT_MAX} 个"))
    return warns, hints


def punct_hits(lines: list[str], start: int, long_mode: bool):
    """兼容旧接口：只返回 W17。"""
    return punct_split(lines, start, long_mode)[0]


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


def long_para_hits(lines: list[str], start: int):
    out = []
    for off, ln in enumerate(lines):
        s = ln.strip()
        if s and not s.startswith("·"):
            n = sum(1 for ch in URL_RE.sub("", ln) if not ch.isspace())
            if n > LONG_PARA_MAX:
                out.append((start + off, "W14", f"这一段约 {n} 字，超过 {LONG_PARA_MAX} 字：拆成短段，或改成「概要 + 列表」，能用图说明的就删字"))
    return out


def voice_hits(lines: list[str], start: int, genre: str, raw: list[str] | None = None):
    """新增的场景检查：W19–W21 与 H1–H12。返回 (warns, hints)。raw 是 Markdown 原文（有就用来查来源行）。"""
    warns, hints, seen = [], [], {}

    def add(bucket, no, code, msg):
        seen[code] = seen.get(code, 0) + 1
        if seen[code] <= MAX_PER_RULE:
            bucket.append((no, code, msg))

    is_long = genre == "long"
    first = _first_body_index(lines)
    for off, body in _iter_body(lines):
        no = start + off
        for rx, tip, ref in CONTEXT_RE:
            m = rx.search(body)
            if m:
                add(hints, no, "H1", f"语境词「{m.group(0)}」：{tip}（core-voice {ref}）")
        if SAY_COLON_RE.match(body):
            if genre in ("duanzi", "short", "reply"):
                add(warns, no, "W19", "「人名说：」改成「人名：」（core-voice V13）")
            else:
                add(hints, no, "H12", "引语可写成「人名：中文意思」（core-voice V13）")
        m = TRANSITION_RE.search(body)
        if m:
            add(warns, no, "W20", f"过渡句 / 引导语「{m.group(0)}」：小标题本身就是过渡，删掉（core-voice V07）")
        m = IMG_RETELL_RE.search(body)
        if m:
            add(warns, no, "W21", f"复述图片「{m.group(0)}」：图自己会说话，删掉或只点出图里看不出的（core-voice V15）")
        m = I_THINK_RE.search(body)
        if m and genre in ("long", "short"):
            add(hints, no, "H3", f"「{m.group(0)}」：观点句用「大概率」「预计」直接说（core-voice V08）")
        m = NEWS_PRECISION_RE.search(body)
        if m:
            add(hints, no, "H4", f"「{m.group(0).strip()}」：不是新闻稿，数字不必写「约 / 左右」，对比给对象和定语（core-voice V12）")
        elif CJK_RE.search(body) and THOUSANDS_RE.search(body):
            add(hints, no, "H4", f"千分位「{THOUSANDS_RE.search(body).group(0)}」：中文正文写「12 万」这类（core-voice V12）")
        m = PARALLEL_CLOSE_RE.search(body)
        if m and m.group(1) != m.group(3):
            add(hints, no, "H5", f"对仗收句「{m.group(0).strip()[:24]}」：事实列完就够，要收就用平实概括（core-voice V05）")
        m = FILLER_INFO_RE.search(body)
        if m and genre != "long":
            add(hints, no, "H8", f"「{m.group(0)}」：不增加信息量，删掉（core-voice V22）")
        elif m and m.group(0).startswith("据"):
            add(hints, no, "H8", f"「{m.group(0)}」：点名具体媒体，或不写（core-voice V22）")
        if (genre == "title" or off == first) and TITLE_PREACH_RE.search(body):
            add(hints, no, "H9", "标题 / 首行反问说教：写清讲什么，不反问读者（core-voice V01）")
        if is_long and not body.strip().startswith("·") and len(SENT_END_RE.findall(body)) > 3:
            add(hints, no, "H10", "一段超过 3 句：一段 2–3 句，手机上不超过 5 行（core-voice V17）")
    if raw:
        for off, ln in enumerate(raw):
            if SOURCE_DESC_RE.match(ln):
                add(hints, start + off, "H6", "来源行只写出处和时间，不描述图的内容（core-voice V14）")
    if genre == "short":
        tags = HASHTAG_RE.findall("\n".join(lines))
        if len(tags) > SHORT_TAGS_MAX:
            add(hints, start, "H11", f"话题标签 {len(tags)} 个：默认两个，宽泛词 + 主题词（core-voice V27）")
    if genre in ("short", "reply"):
        items = [ln for ln in lines if LIST_EMOJI_RE.match(ln)]
        decor = sum(len(EMOJI_RE.findall(ln)) for ln in lines if not LIST_EMOJI_RE.match(ln))
        if len(items) > 4:
            add(hints, start, "H7", f"emoji 列表 {len(items)} 条：行多改用「·」或「1）」（core-voice V25）")
        elif decor > DECOR_HINT_MAX:
            add(hints, start, "H7", f"点缀 emoji {decor} 个：避免满屏 emoji（core-voice V26）")
    return warns, hints


def analyze(text: str, genre: str = "long", markdown: bool | None = None, start: int = 1):
    """对一段文字跑全部去 AI 味检查。返回 (warns, hints)，元素为 (行号, 代码, 说明)。"""
    raw = text.splitlines()
    if markdown is None:
        markdown = genre == "long"
    lines = md_to_plain(raw) if markdown else raw
    long_mode = genre == "long"
    warns = phrase_hits(lines, start) + struct_hits(lines, start)
    pw, ph = punct_split(lines, start, long_mode)
    warns += pw
    hints = list(ph)
    if long_mode:
        warns += long_para_hits(lines, start)
    if markdown:
        warns += image_label_hits(raw, start)
    vw, vh = voice_hits(lines, start, genre, raw if markdown else None)
    warns += vw
    hints += vh
    return sorted(warns), sorted(hints, key=lambda h: (h[0], int(h[1][1:])))


def _guess_genre(path: str) -> str:
    return "long" if path.lower().endswith((".md", ".markdown")) else "short"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="去 AI 味检查：W 警告（强信号）+ H 提示（语境词，只提示）")
    ap.add_argument("files", nargs="+", help="稿子文件，- 表示标准输入")
    ap.add_argument("--genre", choices=GENRES, help="文体；缺省时 .md 当 long，其余当 short")
    ap.add_argument("--plain", action="store_true", help="按纯文本处理（不把 .md 当 Markdown）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--no-hints", action="store_true", help="不打印 H 级提示")
    ap.add_argument("--strict", action="store_true", help="W 也算失败（H 永远不算）")
    args = ap.parse_args(argv)
    report, total_w, total_h = [], 0, 0
    for f in args.files:
        try:
            text = sys.stdin.read() if f == "-" else Path(f).read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError) as e:
            print(f"错误：无法读取 {f}（{e}）", file=sys.stderr)
            return 2
        genre = args.genre or _guess_genre(f)
        md = (not args.plain) and (f.lower().endswith((".md", ".markdown")) or genre == "long")
        warns, hints = analyze(text, genre, md)
        if args.no_hints:
            hints = []
        total_w += len(warns)
        total_h += len(hints)
        report.append({"file": f, "genre": genre,
                       "warnings": [{"line": n, "code": c, "msg": m} for n, c, m in warns],
                       "hints": [{"line": n, "code": c, "msg": m} for n, c, m in hints]})
        if not args.json:
            for n, c, m in warns:
                print(f"{f}:{n}: [{c}] 警告：{m}")
            for n, c, m in hints:
                print(f"{f}:{n}: [{c}] 提示：{m}")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    else:
        failed = args.strict and total_w
        print(f"de_ai_lint：{'未通过' if failed else '通过'}（警告 {total_w}，提示 {total_h}；提示只供判断，不要求改）")
    return 1 if (args.strict and total_w) else 0


if __name__ == "__main__":
    sys.exit(main())
