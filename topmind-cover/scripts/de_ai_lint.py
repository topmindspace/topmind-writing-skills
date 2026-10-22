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
    python3 de_ai_lint.py 快讯.txt --genre short --kind news   # 快讯：首行超 30 字报 W10
    python3 de_ai_lint.py 关系帖.txt --genre duanzi --kind ops # 关系帖：允许行动号召（W22 豁免）
    python3 de_ai_lint.py X短文.txt --genre short --sources 素材来源.md   # 标题动词和口径对照（H20）

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
KINDS = ("post", "news", "ops")  # post：一般帖；news：快讯（首行规则更严）；ops：关系帖（互关 / 打卡，允许行动号召）

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
    # 总结腔：先收窄再揭晓（「理由就一条：」「原因只有一个，」「说到底就一句：」）→ 直接说理由（core-voice V08）
    r"(?:理由|原因)(?:就|只有|就只有)(?:一条|一个|一点)(?=[：:，,。])", r"只有一个(?:原因|理由)(?=[：:，,。])", r"就一句[：:]",
]
AI_RE = re.compile("|".join(AI_PHRASES))
NOT_BUT_RE = re.compile(r"不是.{1,12}而是")

# --- H1：语境词（只提示） ------------------------------------------------------
CONTEXT_WORDS = [
    (r"一文(?:读懂|看懂)", "摘要里可以用；标题里确认是概括式用法", "V04"),
    (r"毫无疑问|不可否认", "后面要接判断和依据，空着就删", "V08"),
    (r"归根结底", "后面那句有实质内容就留", "V08"),
    (r"真正的", "看场景可用；「真正的 X 从来不是」才是套话", "原则 8"),
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
    r"\d[\d.]*\s*(?:万|亿|千|百)?\s*(?:个|人|元|美元|次|款|家|倍|%|颗|star|星)?\s*左右|较[^，。！？\n]{1,12}高出"
)                                                                                          # H4
# 「约 / 大约 + 数字」：只在像新闻稿的地方提示——带万 / 亿 / 千这类量级，或同一句里在做对比。
# 作者自述的大概数（「试了约 50 个提示词」「大概跑了 3 个小时」）不报。
ABOUT_NUM_RE = re.compile(r"(?:大约|约)\s*\d[\d.,]*(?:\s*(?:万|亿|千))?(?:\s*%)?")
ABOUT_MAG_RE = re.compile(r"\d\s*(?:万|亿|千)")
COMPARE_RE = re.compile(r"比|多出|高出|低于|超过|领先|落后|较|相比|翻了")
# 只讨论某个词本身：「」“” 里的内容不参与词面 / 句式检查（改写边界：讨论这个词本身的句子不动）
MENTION_RE = re.compile(r"「[^」\n]{1,40}」|“[^”\n]{1,40}”")
# 示例行：「改前：」「原文：」「反例：」「A：」…开头的行是在展示别人的写法，不参与检查（W14 段长照查）
EXAMPLE_LINE_RE = re.compile(r"^\s*(?:·\s*)?(?:改前|原文|修改前|反例|原句|AI 版|❌|✗|[A-D])\s*[：:]")
# H5 补充：段末两个等长短分句、都以人称 / 主体开头（「它写稿，我挑刺。」）
SHORT_PAIR_RE = re.compile(r"(?:^|[。！？；])\s*([\u4e00-\u9fff]{2,6})[，,]\s*([\u4e00-\u9fff]{2,6})[。！]?\s*$")
PAIR_SUBJECT_RE = re.compile(r"^(?:我们|你们|他们|她们|它们|我|你|他|她|它|人|用户|平台|厂商|开发者|作者|读者|机器|模型)")
# H13：小标题格式（V06「序号、阶段：概括」）
H2_RE = re.compile(r"^\s{0,3}##\s+(.+?)\s*#*\s*$")
HAND_NUM_RE = re.compile(r"^(?:[一二三四五六七八九十]+、|\d{1,2}[.、])")
HEADING_PUNCT_RE = re.compile(r"[：:，,？?！!；;]")
HEADING_EXEMPT_RE = re.compile(r"参考|来源|附录|延伸阅读|致谢|写在最后|后记|FAQ", re.I)
# H14：同一说法两种写法（中英混排有空格 / 没空格，如「去AI味」和「去 AI 味」）
MIXED_TERM_RE = re.compile(r"[\u4e00-\u9fff]{1,4} ?[A-Za-z][A-Za-z0-9+.-]{0,15} ?[\u4e00-\u9fff]{1,4}")
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

# --- 社交短帖模式（de-ai-rules 第五节 S01–S10；core-voice V34–V40） -------------------------
# H9 白名单：真疑问（懂行的人能给出具体答案），开头用不算说教（V34）
GENUINE_Q_RE = re.compile(r"难道(?:就)?没(?:有)?人|难道只有我|有没有人|是不是(?:就|只有)我|一直没(?:想明白|搞懂|弄懂)|我就纳闷|到底(?:是|靠|怎么|为什么|为啥|哪)")
# W22 套路互动钩子结尾（S06）
HOOK_END_RE = re.compile(
    r"(?:你|你们|大家)(?:会|还会)?(?:换|选|用)(?:吗|哪个|哪家)|(?:你|你们|大家)(?:怎么|如何)看|(?:你|你们|大家)觉得呢"
    r"|评论区(?:聊聊|说说|见|告诉我|留言|扣\d)|欢迎(?:留言|讨论|评论)|你(?:们)?站哪(?:边|队)|你(?:们)?还知道哪些|你(?:们)?(?:遇到过|有过)吗"
)
# W24 类比腔（S02）
ANALOGY_RE = re.compile(r"跟[^，。！？\n]{1,16}(?:一个|是一个|同一个|一样的)道理|说白了|就好比|好比说|同理[，,]|^[^=\n]{1,16}\s=\s[^=\n]{1,16}$")
# H16 编经历提示（S05）
OWN_EXP_RE = re.compile(r"我的(?:做法|土办法|习惯|经验)是?|我(?:一般|平时|通常|每次)(?:都|会|是)|我之前(?:也)?(?:试过|用过|做过|踩过)")
# H17 X 短文里的口径词 / 查证过程（V39）
CALIBER_RE = re.compile(r"官方称|据官方|官方口径|厂商口径|按图估读|据悉|据了解|据我查|经核实")
# H18 中文帖里没必要的英文小词（V38）
EN_SMALL_RE = re.compile(r"\b(?:credits?|quota|changelog|reset|rollout|waitlist|deprecated|onboarding|release notes?)\b", re.I)
# H19 播报模板（S07）：警报 emoji + 重磅 / 突发
ALARM_EMOJI_RE = re.compile("[\U0001F6A8\U0001F4E2\U0001F4E3\u203C\u26A0]")
BREAKING_RE = re.compile(r"重磅|突发|炸裂|刚刚")
# W25 英文网文模板（S10）
EN_TEMPLATE_RE = re.compile(r"\bbingo card\b|^\s*step\s*1\b|\bapparently\b|\byour move\b|\bnot complaining\b|\blet that sink in\b|\bthis is the way\b|\bhot take\s*:|\bunpopular opinion\s*:", re.I)
# H4 豁免：引述别人的话（「人名：」开头、「说 / 称 / 回应…」开头）
REPORTED_RE = re.compile(r"^\s*(?:[\u4e00-\u9fffA-Za-z0-9·]{1,12}[：:]|(?:说|称|表示|回应|透露|宣称|承认))")
# H20 口径和标题动词
RELEASE_VERB_RE = re.compile(r"正式发布|发布了|上线了|全量|(?<![要快])来了|官宣")
PREVIEW_SRC_RE = re.compile(r"预告|传闻|灰度|未官宣|还没官宣|内测|泄露|文档里出现")
REPLY_HINT_MAX = 25
REPLY_WARN_MAX = 40
HOOK_MAX_CJK = 30

LONG_PARA_MAX = 110
HASHTAG_ONLY_RE = re.compile(r"^\s*(?:#[\w\u4e00-\u9fff]{1,40}\s*)+$")
# 字数口径与 count_words.py 一致：去掉空白、Markdown 符号和链接地址后的字符数
_CW_SYMBOLS_RE = re.compile(r"[\s*\-#>\[\]()`|]")
_CW_URL_RE = re.compile(r"\]\([^)]*\)|https?://\S+")


def visible_len(text: str) -> int:
    return len(_CW_SYMBOLS_RE.sub("", _CW_URL_RE.sub("]", text)))
MAX_PER_RULE = 3
SHORT_TAGS_MAX = 2
DECOR_HINT_MAX = 3

HINT_CODES = {
    "H1": "语境词", "H2": "可接受的连用标点", "H3": "「我认为」式观点句", "H4": "新闻式精确",
    "H5": "对仗收句", "H6": "来源行描述图", "H7": "emoji 过密", "H8": "无效信息",
    "H9": "标题反问说教", "H10": "段落句子多", "H11": "话题标签多", "H12": "「人名说：」",
    "H13": "小标题格式", "H14": "同一说法两种写法",
    "H15": "回复偏长", "H16": "编经历提示", "H17": "口径词进了正文", "H18": "夹英文小词",
    "H19": "播报模板", "H20": "标题动词和口径对不上", "H21": "首行偏长",
}


def mask_mentions(lines: list[str]) -> list[str]:
    """把「」“”里讨论的词换成占位、把示例行清空，只用于词面 / 句式检查；行号不变。"""
    out = []
    for ln in lines:
        if EXAMPLE_LINE_RE.match(ln):
            out.append("")
            continue
        out.append(MENTION_RE.sub(lambda m: "「" + "某" * 2 + "」", ln))
    return out


def heading_hits(raw: list[str], start: int):
    """H13：二级小标题有的手写序号、有的没有；或一个小标题里标点叠在一起（V06）。"""
    heads = []
    in_fence = False
    for off, ln in enumerate(raw):
        if FENCE_RE.match(ln):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = H2_RE.match(ln)
        if m and not HEADING_EXEMPT_RE.search(m.group(1)):
            heads.append((start + off, m.group(1).strip()))
    out = []
    if len(heads) >= 2:
        numbered = [h for h in heads if HAND_NUM_RE.match(h[1])]
        if numbered and len(numbered) < len(heads):
            miss = next(h for h in heads if not HAND_NUM_RE.match(h[1]))
            out.append((miss[0], "H13", f"小标题「{miss[1][:16]}」没有序号，其他小标题有：序号要么都写、要么都不写（core-voice V06）"))
    for no, h in heads:
        body = HAND_NUM_RE.sub("", h)
        if len(HEADING_PUNCT_RE.findall(body)) >= 2:
            out.append((no, "H13", f"小标题「{h[:16]}」标点偏多：「序号、阶段：概括」，一个冒号或不加（core-voice V06）"))
    return out[:MAX_PER_RULE]


def term_variant_hits(raw: list[str], start: int):
    """H14：同一个中英混排说法，有的地方带空格、有的不带（标题和正文最常见）。"""
    seen: dict[str, dict[str, int]] = {}
    in_fence = False
    for off, ln in enumerate(raw):
        if FENCE_RE.match(ln):
            in_fence = not in_fence
            continue
        if in_fence or MD_IMG_RE.match(ln):
            continue
        t = re.sub(r"\]\([^)]*\)|https?://\S+|`[^`]*`", " ", ln)
        t = re.sub(r"^\s*(?:title|subtitle)\s*:\s*", "", t)
        for m in MIXED_TERM_RE.finditer(t):
            core = re.search(r"[A-Za-z][A-Za-z0-9+.-]*", m.group(0)).group(0)
            seg = m.group(0)
            i = seg.index(core)
            left, right = seg[:i], seg[i + len(core):]
            key = (left.rstrip()[-1:] + core + right.lstrip()[:1])
            form = ("_" if left.endswith(" ") else "") + core + ("_" if right.startswith(" ") else "")
            seen.setdefault(key, {}).setdefault(form, start + off)
    out = []
    for key, forms in seen.items():
        spaced = [f for f in forms if f.startswith("_") or f.endswith("_")]
        tight = [f for f in forms if not (f.startswith("_") or f.endswith("_"))]
        if spaced and tight:
            no = min(forms.values())
            out.append((no, "H14", f"「{key}」有带空格和不带空格两种写法：全文统一一种（标题受文件名限制时，正文跟标题走或在报告里说明）"))
    return out[:MAX_PER_RULE]


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


def punct_split(lines: list[str], start: int, long_mode: bool, genre: str | None = None):
    """W17 与 H2。返回 (warns, hints)。

    「？！」首行、末行各可用一次（未完全核实的热点，V22）；短文 / 段子 / 回复里的「！！」「！！！」和感叹号偏多
    只提示（H2），长文照报 W17。破折号在所有文体都按 W17 查。
    """
    text = "\n".join(ln for ln in lines if not FENCE_RE.match(ln))
    warns, hints = [], []
    first = _first_body_index(lines)
    last = next((i for i in range(len(lines) - 1, -1, -1) if lines[i].strip() and not HASHTAG_ONLY_RE.match(lines[i])), -1)
    qe_used: set[int] = set()
    soft = not long_mode
    for off, ln in enumerate(lines):
        for m in PUNCT_RUN_RE.finditer(ln):
            run = m.group(0)
            if QE_RE.match(run) and off in (first, last) and off not in qe_used:
                qe_used.add(off)
                continue
            if soft and re.fullmatch(r"[！!]{2,3}", run):
                hints.append((start + off, "H2", f"「{run}」：转发点评、惊讶语气可以用一处，别处换成句号或「...」"))
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
            hints.append((start, "H2", f"感叹号 {bangs} 个：短文一般 {BANG_SHORT_MAX} 个以内，语气尽量靠事实"))
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
        # 新结构里出处写在图片下一行（可隔一个空行）的「来源：」，也算图注
        nxt = ""
        for k in (off + 1, off + 2):
            if k < len(lines) and lines[k].strip():
                nxt = lines[k].strip() if re.match(r"^来源[：:]", lines[k].strip()) else ""
                break
        label = alt + " " + nxt
        if SELFMADE_HINT_RE.search(alt + " " + path) and not (SELFMADE_HINT_RE.search(label) and (SOURCE_HINT_RE.search(alt) or nxt)):
            out.append((start + off, "W18", "自制图没标清楚：图注（alt）或下一行「来源：」里写「自制」和数据来源，例如「来源：自制，数据：xx 官方」"))
    return out


def long_para_hits(lines: list[str], start: int):
    out = []
    for off, ln in enumerate(lines):
        s = ln.strip()
        if s and not s.startswith("·"):
            n = visible_len(ln)
            if n > LONG_PARA_MAX:
                out.append((start + off, "W14", f"这一段约 {n} 字，超过 {LONG_PARA_MAX} 字：拆成短段，或改成「概要 + 列表」，能用图说明的就删字"))
    return out


def voice_hits(lines: list[str], start: int, genre: str, raw: list[str] | None = None, kind: str = "post"):
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
        ma = ABOUT_NUM_RE.search(body)
        if ma and not (ABOUT_MAG_RE.search(ma.group(0)) or COMPARE_RE.search(body)):
            ma = None
        if (m or ma) and REPORTED_RE.match(body):
            m = ma = None
        if m or ma:
            frag = (m or ma).group(0).strip()
            add(hints, no, "H4", f"「{frag}」：不是新闻稿，数字不必写「约 / 左右」，对比给对象和定语（core-voice V12）")
        elif CJK_RE.search(body) and THOUSANDS_RE.search(body):
            add(hints, no, "H4", f"千分位「{THOUSANDS_RE.search(body).group(0)}」：中文正文写「12 万」这类（core-voice V12）")
        m = PARALLEL_CLOSE_RE.search(body)
        if m and m.group(1) != m.group(3):
            add(hints, no, "H5", f"对仗收句「{m.group(0).strip()[:24]}」：事实列完就够，要收就用平实概括（core-voice V05）")
        else:
            sp = SHORT_PAIR_RE.search(body)
            if (sp and len(sp.group(1)) == len(sp.group(2)) and sp.group(1)[0] != sp.group(2)[0]
                    and PAIR_SUBJECT_RE.match(sp.group(1)) and PAIR_SUBJECT_RE.match(sp.group(2))):
                add(hints, no, "H5", f"短对仗收句「{sp.group(1)}，{sp.group(2)}」：收尾换成平实说法或生活化类比（core-voice V05 / V10）")
        m = FILLER_INFO_RE.search(body)
        if m and genre != "long":
            add(hints, no, "H8", f"「{m.group(0)}」：不增加信息量，删掉（core-voice V22）")
        elif m and m.group(0).startswith("据"):
            add(hints, no, "H8", f"「{m.group(0)}」：点名具体媒体，或不写（core-voice V22）")
        if (genre == "title" or off == first) and TITLE_PREACH_RE.search(body) and not GENUINE_Q_RE.search(body):
            add(hints, no, "H9", "标题 / 首行反问说教：写清讲什么，不反问读者（core-voice V01）")
        if is_long and not body.strip().startswith("·") and len(SENT_END_RE.findall(body)) > 3:
            add(hints, no, "H10", "一段超过 3 句：一段 2–3 句，手机上不超过 5 行（core-voice V17）")
        if genre in ("reply", "duanzi"):
            m = ANALOGY_RE.search(body)
            if m:
                add(warns, no, "W24", f"类比腔「{m.group(0).strip()[:16]}」：换成自己的做法或一个具体场景（de-ai-rules S02）")
        if genre in ("reply", "short", "duanzi"):
            m = OWN_EXP_RE.search(body)
            if m:
                add(hints, no, "H16", f"「{m.group(0)}」：确认这段经历作者真有；没有就删掉，或在交付说明里提示作者自己讲（de-ai-rules S05）")
            if CJK_RE.search(body):
                m = EN_SMALL_RE.search(body)
                if m:
                    add(hints, no, "H18", f"中文帖夹英文小词「{m.group(0)}」：换成中文说法（core-voice V38）")
        if genre == "short":
            m = CALIBER_RE.search(body)
            if m:
                add(hints, no, "H17", f"「{m.group(0)}」：X 短文正文不写查证过程和口径，挪进交付说明的口径提醒（core-voice V39）")
        if genre in ("reply", "short") and not CJK_RE.search(body):
            m = EN_TEMPLATE_RE.search(body)
            if m:
                add(warns, no, "W25", f"英文网文模板「{m.group(0).strip()}」：换成 3–6 个词的普通说法（de-ai-rules S10）")
    if raw:
        for off, ln in enumerate(raw):
            if SOURCE_DESC_RE.match(ln):
                add(hints, start + off, "H6", "来源行只写出处和时间，不描述图的内容（core-voice V14）")
    if genre == "short":
        tags = HASHTAG_RE.findall("\n".join(lines))
        if len(tags) > SHORT_TAGS_MAX:
            add(hints, start, "H11", f"话题标签 {len(tags)} 个：段子和短文默认不带，要带最多两个，宽泛词 + 主题词（core-voice V27）")
    if genre in ("short", "reply"):
        items = [ln for ln in lines if LIST_EMOJI_RE.match(ln)]
        decor = sum(len(EMOJI_RE.findall(ln)) for ln in lines if not LIST_EMOJI_RE.match(ln))
        if len(items) > 4:
            add(hints, start, "H7", f"emoji 列表 {len(items)} 条：行多改用「·」或「1）」（core-voice V25）")
        elif decor > DECOR_HINT_MAX:
            add(hints, start, "H7", f"点缀 emoji {decor} 个：避免满屏 emoji（core-voice V26）")
    body_lines = [(off, ln) for off, ln in enumerate(lines) if ln.strip() and not HASHTAG_ONLY_RE.match(ln)]
    if body_lines and genre in ("short", "duanzi") and kind != "ops":
        off, ln = body_lines[-1]
        m = HOOK_END_RE.search(ln)
        if m:
            add(warns, start + off, "W22", f"套路互动钩子结尾「{m.group(0)}」：删掉；要问就问自己真拿不准的（core-voice V34，de-ai-rules S06）")
    if genre == "duanzi":
        for (o1, _), (o2, _) in zip(body_lines, body_lines[1:]):
            if o2 == o1 + 1:
                add(warns, start + o2, "W23", "段子体行间没空行：一句一行，行与行之间空一行")
                break
    if genre == "reply":
        n = sum(1 for ch in "".join(ln for _, ln in body_lines) if not ch.isspace())
        if CJK_RE.search("".join(ln for _, ln in body_lines)):
            if n > REPLY_WARN_MAX:
                add(warns, start, "W26", f"回复约 {n} 字，超过 {REPLY_WARN_MAX} 字：回复是聊天，不是点评，留态度和你自己的东西（core-voice V37）")
            elif n > REPLY_HINT_MAX:
                add(hints, start, "H15", f"回复约 {n} 字：中文回复默认 {REPLY_HINT_MAX} 字以内（core-voice V37）")
    if genre == "short" and body_lines:
        alarm = any(ALARM_EMOJI_RE.search(ln) for _, ln in body_lines)
        breaking = any(BREAKING_RE.search(ln) for _, ln in body_lines[:2])
        emoji_items = sum(1 for _, ln in body_lines if LIST_EMOJI_RE.match(ln))
        if alarm and breaking and emoji_items >= 2:
            add(hints, start, "H19", "播报模板（警报 emoji + 重磅 / 突发 + emoji 分点）：第一句给个人反应或最狠的一个数（de-ai-rules S07）")
    return warns, hints


def first_line_hits(lines: list[str], start: int, genre: str, kind: str = "post"):
    """W10 / H21 首行长度：快讯（--kind news）首行约 30 字内（W10）；其他短帖首行偏长只提示（H21）。"""
    first = _first_body_index(lines)
    if first < 0 or genre not in ("short", "duanzi"):
        return [], []
    ln = lines[first]
    n = sum(1 for ch in ln if not ch.isspace())
    weight = sum(2 if CJK_RE.match(ch) else 1 for ch in ln if not ch.isspace())
    if weight <= HOOK_MAX_CJK * 2:
        return [], []
    if genre == "short" and kind == "news":
        return [(start + first, "W10", f"快讯首行约 {n} 字：写「是什么 + 最狠的一个数」，约 {HOOK_MAX_CJK} 字内（core-voice V05）")], []
    return [], [(start + first, "H21", f"首行约 {n} 字：观点、吐槽、真疑问可以长一点；读一遍，能更短就更短（core-voice V05）")]


def sources_hits(lines: list[str], start: int, sources_text: str):
    """H20：标题 / 首行写了「来了 / 发布 / 上线」，素材来源却标着预告、传闻、灰度（core-voice V40）。"""
    first = _first_body_index(lines)
    if first < 0 or not sources_text:
        return []
    head = lines[first]
    m = RELEASE_VERB_RE.search(head)
    p = PREVIEW_SRC_RE.search(sources_text)
    if m and p and not re.search(r"[？?]", head):
        return [(start + first, "H20", f"标题 / 首行写「{m.group(0)}」，素材来源里标着「{p.group(0)}」：动词跟着口径走（core-voice V40）")]
    return []


def analyze(text: str, genre: str = "long", markdown: bool | None = None, start: int = 1,
            kind: str = "post", sources_text: str = ""):
    """对一段文字跑全部去 AI 味检查。返回 (warns, hints)，元素为 (行号, 代码, 说明)。"""
    raw = text.splitlines()
    if markdown is None:
        markdown = genre == "long"
    lines = md_to_plain(raw) if markdown else raw
    masked = mask_mentions(lines)
    long_mode = genre == "long"
    warns = phrase_hits(masked, start) + struct_hits(masked, start)
    pw, ph = punct_split(lines, start, long_mode, genre)
    warns += pw
    hints = list(ph)
    fw, fh = first_line_hits(lines, start, genre, kind)
    warns += fw
    hints += fh
    hints += sources_hits(lines, start, sources_text)
    if long_mode:
        warns += long_para_hits(lines, start)
    if markdown:
        warns += image_label_hits(raw, start)
    vw, vh = voice_hits(masked, start, genre, raw if markdown else None, kind)
    warns += vw
    hints += vh
    if markdown:
        hints += heading_hits(raw, start) + term_variant_hits(raw, start)
    return sorted(warns), sorted(hints, key=lambda h: (h[0], int(h[1][1:])))


def design_hints(path: str) -> list:
    """信息设计提示 I1–I9（info_design_hints.py）；同目录没有这个脚本时返回空。永远不计入 --strict。"""
    sys.dont_write_bytecode = True  # 技能包里不留 __pycache__
    try:
        here = str(Path(__file__).resolve().parent)
        if here not in sys.path:
            sys.path.insert(0, here)
        import info_design_hints as IDH
        return IDH.check_file(path)
    except (ImportError, OSError, UnicodeDecodeError):
        return []


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
    ap.add_argument("--no-design", action="store_true", help="不打印 I 级信息设计提示（长文 Markdown 才有）")
    ap.add_argument("--kind", choices=KINDS, default="post", help="帖子用途：post（默认）/ news（快讯，首行超 30 字报 W10）/ ops（关系帖，允许行动号召）")
    ap.add_argument("--sources", help="素材来源文件（如 素材来源.md）：标题动词和口径对照（H20）")
    args = ap.parse_args(argv)
    report, total_w, total_h, total_i = [], 0, 0, 0
    for f in args.files:
        try:
            text = sys.stdin.read() if f == "-" else Path(f).read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError) as e:
            print(f"错误：无法读取 {f}（{e}）", file=sys.stderr)
            return 2
        genre = args.genre or _guess_genre(f)
        md = (not args.plain) and (f.lower().endswith((".md", ".markdown")) or genre == "long")
        src_text = ""
        if args.sources:
            try:
                src_text = Path(args.sources).read_text(encoding="utf-8-sig")
            except (OSError, UnicodeDecodeError) as e:
                print(f"错误：无法读取 {args.sources}（{e}）", file=sys.stderr)
                return 2
        warns, hints = analyze(text, genre, md, kind=args.kind, sources_text=src_text)
        if args.no_hints:
            hints = []
        design = [] if (args.no_design or not md or genre != "long" or f == "-") else design_hints(f)
        total_w += len(warns)
        total_h += len(hints)
        total_i += len(design)
        report.append({"file": f, "genre": genre,
                       "warnings": [{"line": n, "code": c, "msg": m} for n, c, m in warns],
                       "hints": [{"line": n, "code": c, "msg": m} for n, c, m in hints],
                       "design": [{"line": n, "code": c, "msg": m} for n, c, m in design]})
        if not args.json:
            for n, c, m in warns:
                print(f"{f}:{n}: [{c}] 警告：{m}")
            for n, c, m in hints:
                print(f"{f}:{n}: [{c}] 提示：{m}")
            for n, c, m in design:
                print(f"{f}:{n}: [{c}] 信息设计：{m}")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    else:
        failed = args.strict and total_w
        tail = f"；信息设计提示 {total_i}（I，只供判断，见 information-design.md）" if total_i else ""
        print(f"de_ai_lint：{'未通过' if failed else '通过'}（警告 {total_w}，提示 {total_h}；提示只供判断，不要求改{tail}）")
    return 1 if (args.strict and total_w) else 0


if __name__ == "__main__":
    sys.exit(main())
