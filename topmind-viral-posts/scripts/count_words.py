#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""count_words.py — 改稿前后统一口径的字数统计。

口径：去掉 frontmatter、标题行（#）、图片行（![…](…)）、代码围栏，再去掉空白和 Markdown 符号后的字符数。
同时报单段最长字数（长文段落建议 110 字内）和段落数。

用法：
    python3 count_words.py 稿子.md               # 打印「字数 N｜段落 M｜单段最长 K」
    python3 count_words.py 改前.md 改后.md       # 打印改前 → 改后
    python3 count_words.py 稿子.md --json
只用 Python 标准库。退出码：读文件失败 → 2，其余 → 0。
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

SYMBOLS_RE = re.compile(r"[\s*\-#>\[\]()`|]")
URL_RE = re.compile(r"\]\([^)]*\)|https?://\S+")


def body_lines(text: str) -> list[str]:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                lines = lines[i + 1:]
                break
    out, fence = [], False
    for ln in lines:
        if ln.lstrip().startswith(("```", "~~~")):
            fence = not fence
            continue
        if fence or ln.lstrip().startswith(("![", "#")):
            out.append("")
            continue
        out.append(ln)
    return out


def count_text(text: str) -> dict:
    lines = body_lines(text)
    paras, cur = [], []
    for ln in lines + [""]:
        if ln.strip():
            cur.append(ln)
        elif cur:
            paras.append(" ".join(cur))
            cur = []
    lens = [len(SYMBOLS_RE.sub("", URL_RE.sub("]", p))) for p in paras]
    return {"chars": sum(lens), "paragraphs": len(paras), "longest_paragraph": max(lens) if lens else 0}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="改稿字数统计（统一口径）")
    ap.add_argument("files", nargs="+", help="一个文件；或两个文件（改前、改后）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    res = []
    for f in a.files[:2]:
        try:
            res.append(count_text(Path(f).read_text(encoding="utf-8-sig")))
        except (OSError, UnicodeDecodeError) as e:
            print(f"错误：无法读取 {f}（{e}）", file=sys.stderr)
            return 2
    if a.json:
        print(json.dumps(res if len(res) > 1 else res[0], ensure_ascii=False))
    elif len(res) == 1:
        r = res[0]
        print(f"字数 {r['chars']}｜段落 {r['paragraphs']}｜单段最长 {r['longest_paragraph']}")
    else:
        b, c = res
        pct = (c["chars"] - b["chars"]) * 100 / max(1, b["chars"])
        print(f"字数：改前 {b['chars']} → 改后 {c['chars']}（{pct:+.0f}%）｜单段最长 {b['longest_paragraph']} → {c['longest_paragraph']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
