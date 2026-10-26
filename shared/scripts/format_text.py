#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""X 文本格式化，默认保留文字、链接和有表达作用的表情。

--mode short 合并多余空行并转换常见 Markdown 列表；--mode duanzi 按节拍分行。
--split 可拆句；--strip-emoji 仅在需要去表情时使用；--separate-links 可将链接、
来源和图片说明另列（--links-out 保存）。--variants 拼接用户提供的备选开头。
逐字校验忽略空白、列表符号和 emoji，因此仍需人工核对符号语义。
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


def duanzi(text: str, split: bool, remove_emoji: bool = False) -> list[str]:
    """按节拍换行；默认保留表情和表达正反 / 方向的 emoji 符号。"""
    lines: list[str] = []
    clean = strip_emoji if remove_emoji else lambda value: value.strip()
    for raw in text.splitlines():
        raw = QUOTE_RE.sub("", raw)
        if not raw.strip():
            continue
        m, o = UL_RE.match(raw.rstrip()), OL_RE.match(raw.rstrip())
        if m or o or BULLET_RE.match(raw):
            # emoji 项目标记可能表达正反，保留；显式去表情时才删除。
            item = m.group(2) if m else (o.group(3) if o else raw)
            if remove_emoji:
                item = BULLET_RE.sub("", item, count=1)
            lines.append(clean(item))
        elif split:
            lines += [clean(part) for part in SENT_RE.split(raw.strip()) if clean(part)]
        else:
            lines.append(clean(raw))
    return "\n\n".join(line for line in lines if line).split("\n")


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
    ap.add_argument("--title-emoji", help="标题 emoji，按作者要求添加")
    ap.add_argument("--open", dest="open_e", help="开头人设点缀，如 🐔 🐱")
    ap.add_argument("--close", dest="close_e", help="结尾人设点缀，如 🌱 🌸")
    ap.add_argument("--bullets", choices=["plain", "emoji"], default="plain", help="短文体 Markdown 列表改写方式：plain（· / 1），默认）或 emoji（🔹 / 1️⃣）")
    ap.add_argument("--strip-emoji", action="store_true", help="明确需要纯文字时去掉 emoji；默认保留，注意核对符号含义")
    ap.add_argument("--separate-links", action="store_true", help="将链接、来源与图片说明移到另发清单；默认保留")
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

    body, extra = split_links(text) if args.separate_links else (text, [])
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
        lines = duanzi(b, args.split, args.strip_emoji) if args.mode == "duanzi" else short(b, args.bullets)
        if args.strip_emoji:
            lines = [strip_emoji(line) for line in lines]
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
