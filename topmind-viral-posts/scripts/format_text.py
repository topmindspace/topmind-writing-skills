#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""format_text.py — 把一段文字格式化成 X 段子体或短文体，只动排版，不改字。

用法：
    python3 format_text.py 原文.txt --mode duanzi              # 段子体：每句一行，行与行之间空一行；完全不用 emoji，分点只去掉符号
    python3 format_text.py 原文.txt --mode duanzi --split      # 同上，并按句末标点（。！？!?）拆句
    python3 format_text.py 原文.txt --mode short               # 短文体：合并多余空行，Markdown 列表 → 「·」/「1）」纯文本列表
    python3 format_text.py 原文.txt --mode short --bullets emoji   # Markdown 列表 → 🔹 / 1️⃣ emoji 列表（emoji 不强制，可选）
    python3 format_text.py 原文.txt --mode short --title-emoji 🆕 --open 🐔 --close 🌱   # 点缀只用于短文体，可选
    python3 format_text.py 原文.txt --mode short --links-out 链接.txt   # 另存从正文里拿出来的链接 / 来源行 / 配图行
    python3 format_text.py 原文.txt --mode duanzi --out 段子.txt
    cat 原文.txt | python3 format_text.py - --mode duanzi
    python3 format_text.py 原文.txt --mode short --variants 开头备选.txt   # 多个开头 → 拼成多条完整成品，每条之间一行 ---

--variants：开头备选文件里每个开头之间用单独一行 --- 隔开。原文第一段（第一个空行之前）被逐个替换成备选开头，
其余部分不动，输出几条完整成品（第一条是原文自己的开头），条与条之间一行 ---（lint_x_post.py 会按 --- 分条检查）。

规则见 references/emoji-system.md 与 references/x-post-format.md。
交付规约（x-delivery-contract.md）：正文是一段可直接复制的纯文本，链接、原图、配图另发。
所以两种模式都会把 URL、来源行（来源：/ 出处：/ 原帖：…）、配图行（配图：/ [图1]…）从正文里拿出来，
打印到标准错误的「另发」清单里（或用 --links-out 写进文件），正文里不留。
每次输出前做「原文保真」校验：去掉空白、列表符号、emoji 和上述拿出来的链接 / 来源 / 配图行后，与原文逐字一致；不一致即报错（退出码 1）。
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

UL_RE = re.compile(r"^(\s*)[-*+]\s+(\S.*)$")
OL_RE = re.compile(r"^(\s*)(\d{1,2})[.)、]\s*(\S.*)$")
SENT_RE = re.compile(r"(?<=[。！？!?…])(?=[^。！？!?…」”’）)\s])")
EMOJI_RE = re.compile(r"[\U0001F100-\U0001F2FF\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\u2190-\u21FF\u25AA\u25AB\u2022\u20E3\uFE0F\u2460-\u2473]")
QUOTE_RE = re.compile(r"^\s*>\s?")  # Markdown 引用标记：X 不渲染，去掉标记、保留文字

KEYCAPS = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]


def skeleton(text: str) -> str:
    """保真比对用：去空白、emoji、Markdown 列表标记与序号标记。"""
    out = []
    for ln in text.splitlines():
        ln = QUOTE_RE.sub("", ln)
        m = UL_RE.match(ln)
        if m:
            ln = m.group(2)
        else:
            o = OL_RE.match(ln)
            if o:
                ln = o.group(3)
        out.append(ln)
    s = "".join(re.sub(r"^\s*(?:[0-9]\uFE0F?\u20E3|\U0001F51F|\d{1,2}）|·)", "", ln) for ln in out)
    s = EMOJI_RE.sub("", s)
    return re.sub(r"\s+", "", s)


BULLET_RE = re.compile(r"^\s*(?:[0-9]\uFE0F?\u20E3|\U0001F51F|[\u2460-\u2473]|\d{1,2}）|[🔹🔸▫▪•·✅❌📌➡→])")
URL_RE = re.compile(r"https?://\S+")
SOURCE_LINE_RE = re.compile(r"^\s*(?:来源|信源|信息来源|出处|原帖|原文|原文链接|链接|参考|via|source)\s*[:：]", re.I)
IMAGE_LINE_RE = re.compile(r"^\s*(?:(?:配图|原图|图注|图片|插图)\s*[:：]|\[(?:图|图片|配图|视频)[^\]]*\]|【配图[^】]*】)")


def split_links(text: str) -> tuple[str, list[str]]:
    """把来源行、配图行整行拿出；其余行里的 URL 摘出来。返回 (正文, 另发清单)。"""
    body, extra = [], []
    for ln in text.splitlines():
        if SOURCE_LINE_RE.match(ln) or IMAGE_LINE_RE.match(ln):
            extra.append(ln.strip())
            continue
        urls = URL_RE.findall(ln)
        if urls:
            extra += urls
            ln = URL_RE.sub("", ln).rstrip()
            ln = re.sub(r"[ \t]{2,}", " ", ln)
            if not ln.strip() or re.fullmatch(r"\s*[:：（(）)\-—]*\s*", ln):
                continue
        body.append(ln)
    return "\n".join(body) + "\n", extra


def strip_emoji(s: str) -> str:
    """段子体用：去掉 emoji 及其变体选择符、零宽连接符，再收拾多余空格。"""
    s = EMOJI_RE.sub("", s).replace("\u200d", "")
    return re.sub(r"[ \t]{2,}", " ", s).strip()


def to_bullet(ln: str, style: str = "plain") -> str | None:
    """Markdown 列表行 → X 纯文本列表行；不是列表行返回 None。
    plain：无序「· 」、有序「1）」；emoji：一级 🔹 / 1️⃣，二级缩进 ▫️。"""
    m = UL_RE.match(ln)
    if m:
        lvl = 1 if len(m.group(1).expandtabs(2)) else 0
        if style == "plain":
            return ("  " * lvl) + "· " + m.group(2)
        return ("  ▫️ " if lvl else "🔹 ") + m.group(2)
    o = OL_RE.match(ln)
    if o:
        n = int(o.group(2))
        lvl = 1 if len(o.group(1).expandtabs(2)) else 0
        if style == "plain":
            return ("  " * lvl) + f"{n}）" + o.group(3)
        return ("  " * lvl) + (KEYCAPS[n] if n < len(KEYCAPS) else f"{n}）") + " " + o.group(3)
    return None


def duanzi(text: str, split: bool) -> list[str]:
    """段子体：一句一行、行间空一行，完全不用 emoji。
    分点条目去掉列表符号（Markdown 标记与 emoji 符号都去掉），一条一行、靠行间空行区分；--split 不拆列表条目。
    原文里的 emoji（含人设点缀、情绪表情）一并去掉。"""
    lines: list[str] = []
    for raw in text.splitlines():
        raw = QUOTE_RE.sub("", raw)
        if not raw.strip():
            continue
        m, o = UL_RE.match(raw.rstrip()), OL_RE.match(raw.rstrip())
        if m or o or BULLET_RE.match(raw):
            item = m.group(2) if m else (o.group(3) if o else BULLET_RE.sub("", raw, count=1))
            lines.append(strip_emoji(item))
        elif split:
            lines += [strip_emoji(p) for p in SENT_RE.split(raw.strip()) if strip_emoji(p)]
        else:
            lines.append(strip_emoji(raw))
    lines = [ln for ln in lines if ln]
    out: list[str] = []
    for ln in lines:
        out += [ln, ""]
    return out[:-1]


def short(text: str, style: str = "plain") -> list[str]:
    out: list[str] = []
    blank = False
    for raw in text.splitlines():
        ln = QUOTE_RE.sub("", raw).rstrip()
        if not ln.strip():
            if out and not blank:
                out.append("")
            blank = True
            continue
        blank = False
        b = to_bullet(ln, style)
        ln = b if b is not None else ln.strip()
        out.append(ln)
    while out and not out[-1]:
        out.pop()
    return out


def decorate(lines: list[str], title_emoji: str | None, open_e: str | None, close_e: str | None) -> list[str]:
    if not lines:
        return lines
    if title_emoji:
        lines[0] = f"{title_emoji} {lines[0]}"
    if open_e:
        lines[0] = f"{lines[0]} {open_e}"
    if close_e:
        idx = len(lines) - 1
        # 话题标签行之前的最后一句
        while idx > 0 and (lines[idx].startswith("#") or not lines[idx].strip()):
            idx -= 1
        if re.match(r"^\s*(?:🔹|▫️|•|·|▪|✅|❌|📌|[0-9]\uFE0F?\u20E3|🔟|\d{1,2}）)", lines[idx]):
            lines[idx + 1:idx + 1] = ["", close_e]  # 列表项里不放人设点缀，单独成行
        else:
            lines[idx] = f"{lines[idx]} {close_e}"
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(description="X 段子体 / 短文体格式化（只动排版，不改字）")
    ap.add_argument("src", help="原文文件，- 表示标准输入")
    ap.add_argument("--mode", choices=["duanzi", "short"], required=True)
    ap.add_argument("--split", action="store_true", help="段子体：按句末标点拆句")
    ap.add_argument("--title-emoji", help="短文体：标题 emoji（须与标题关键词对应）")
    ap.add_argument("--open", dest="open_e", help="开头人设点缀，如 🐔 🐱")
    ap.add_argument("--close", dest="close_e", help="结尾人设点缀，如 🌱 🌸")
    ap.add_argument("--bullets", choices=["plain", "emoji"], default="plain", help="短文体 Markdown 列表改写方式：plain（· / 1），默认）或 emoji（🔹 / 1️⃣）")
    ap.add_argument("--links-out", help="把从正文拿出的链接 / 来源行 / 配图行写进这个文件（另发用）")
    ap.add_argument("--out", help="输出文件；省略则打印到标准输出")
    ap.add_argument("--variants", help="开头备选文件（每个开头之间一行 ---）：拼成多条完整成品，每条之间一行 ---")
    args = ap.parse_args()

    try:
        text = sys.stdin.read() if args.src == "-" else Path(args.src).read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as e:
        print(f"错误：无法读取 {args.src}（{e}）", file=sys.stderr)
        return 2
    if not text.strip():
        print("错误：原文为空", file=sys.stderr)
        return 2

    if args.mode == "duanzi" and (args.title_emoji or args.open_e or args.close_e):
        print("错误：段子体完全不用 emoji，不接受 --title-emoji / --open / --close（点缀只用于 --mode short）", file=sys.stderr)
        return 2
    body, extra = split_links(text)
    bodies = [body]
    if args.variants:
        try:
            vt = Path(args.variants).read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError) as e:
            print(f"错误：无法读取 {args.variants}（{e}）", file=sys.stderr)
            return 2
        heads = [v.strip("\n") for v in re.split(r"(?m)^\s*---\s*$", vt) if v.strip()]
        parts = re.split(r"\n\s*\n", body.strip("\n"), maxsplit=1)
        rest = parts[1] if len(parts) > 1 else ""
        bodies += [h + ("\n\n" + rest if rest else "") + "\n" for h in heads]
    outs = []
    for b in bodies:
        lines = duanzi(b, args.split) if args.mode == "duanzi" else short(b, args.bullets)
        lines = decorate(lines, args.title_emoji, args.open_e, args.close_e)
        res = "\n".join(lines) + "\n"
        if skeleton(res) != skeleton(b):
            print("错误：原文保真校验未通过（格式化改动了文字）", file=sys.stderr)
            return 1
        outs.append(res)
    result = "\n---\n\n".join(o.rstrip("\n") + "\n" for o in outs) if len(outs) > 1 else outs[0]
    if extra:
        if args.links_out:
            Path(args.links_out).write_text("\n".join(extra) + "\n", encoding="utf-8")
        print("另发（不放进正文）：\n" + "\n".join(extra), file=sys.stderr)
    if args.out:
        Path(args.out).write_text(result, encoding="utf-8")
        print(f"已写出 {args.out}（原文保真校验通过）", file=sys.stderr)
    else:
        sys.stdout.write(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
