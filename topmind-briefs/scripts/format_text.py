#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""format_text.py — 把一段文字格式化成 X 段子体或短文体，只动排版，不改字。

用法：
    python3 format_text.py 原文.txt --mode duanzi              # 段子体：每句一行，行与行之间空一行
    python3 format_text.py 原文.txt --mode duanzi --split      # 同上，并按句末标点（。！？!?）拆句
    python3 format_text.py 原文.txt --mode short               # 短文体：合并多余空行，Markdown 列表 → emoji 列表
    python3 format_text.py 原文.txt --mode short --title-emoji 🆕 --open 🐔 --close 🌱
    python3 format_text.py 原文.txt --mode duanzi --out 段子.txt
    cat 原文.txt | python3 format_text.py - --mode duanzi

规则见 references/emoji-system.md 与 references/x-post-format.md。
每次输出前做「原文保真」校验：去掉空白、列表符号和新增的 emoji 后，与原文逐字一致；不一致即报错（退出码 1）。
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
KEYCAPS = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]


def skeleton(text: str) -> str:
    """保真比对用：去空白、emoji、Markdown 列表标记与序号标记。"""
    out = []
    for ln in text.splitlines():
        m = UL_RE.match(ln)
        if m:
            ln = m.group(2)
        else:
            o = OL_RE.match(ln)
            if o:
                ln = o.group(3)
        out.append(ln)
    s = "".join(re.sub(r"^\s*(?:[0-9]\uFE0F?\u20E3|\U0001F51F)", "", ln) for ln in out)
    s = EMOJI_RE.sub("", s)
    return re.sub(r"\s+", "", s)


def duanzi(text: str, split: bool) -> list[str]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if split:
        lines = [p.strip() for ln in lines for p in SENT_RE.split(ln) if p.strip()]
    out: list[str] = []
    for ln in lines:
        out += [ln, ""]
    return out[:-1]


def short(text: str) -> list[str]:
    out: list[str] = []
    blank = False
    for raw in text.splitlines():
        ln = raw.rstrip()
        if not ln.strip():
            if out and not blank:
                out.append("")
            blank = True
            continue
        blank = False
        m = UL_RE.match(ln)
        o = OL_RE.match(ln) if not m else None
        if m:
            lvl = 1 if len(m.group(1).expandtabs(2)) else 0
            ln = ("  ▫️ " if lvl else "🔹 ") + m.group(2)
        elif o:
            n = int(o.group(2))
            lvl = 1 if len(o.group(1).expandtabs(2)) else 0
            ln = ("  " * lvl) + (KEYCAPS[n] if n < len(KEYCAPS) else f"{n}.") + " " + o.group(3)
        else:
            ln = ln.strip()
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
        # 来源行、话题标签行之前的最后一句
        while idx > 0 and (lines[idx].startswith(("#", "来源", "出处", "http")) or not lines[idx].strip()):
            idx -= 1
        if re.match(r"^\s*(?:🔹|▫️|•|▪|✅|❌|📌|[0-9]\uFE0F?\u20E3|🔟)", lines[idx]):
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
    ap.add_argument("--out", help="输出文件；省略则打印到标准输出")
    args = ap.parse_args()

    try:
        text = sys.stdin.read() if args.src == "-" else Path(args.src).read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as e:
        print(f"错误：无法读取 {args.src}（{e}）", file=sys.stderr)
        return 2
    if not text.strip():
        print("错误：原文为空", file=sys.stderr)
        return 2

    lines = duanzi(text, args.split) if args.mode == "duanzi" else short(text)
    if args.mode == "duanzi" and args.title_emoji:
        print("提示：段子体没有标题行，已忽略 --title-emoji", file=sys.stderr)
        args.title_emoji = None
    lines = decorate(lines, args.title_emoji, args.open_e, args.close_e)
    result = "\n".join(lines) + "\n"

    if skeleton(result) != skeleton(text):
        print("错误：原文保真校验未通过（格式化改动了文字）", file=sys.stderr)
        return 1
    if args.out:
        Path(args.out).write_text(result, encoding="utf-8")
        print(f"已写出 {args.out}（原文保真校验通过）", file=sys.stderr)
    else:
        sys.stdout.write(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
