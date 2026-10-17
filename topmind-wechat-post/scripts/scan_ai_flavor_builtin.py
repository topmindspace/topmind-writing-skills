#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scan_ai_flavor_builtin.py — 中文去 AI 味打分（随包内置实现）。

给一篇 Markdown / 纯文本稿打 0–100 分（越高越像人写的），并列出命中位置。
规则与 `lint_x_post.py` 同源（W9 套话词、W15 中文结构套话、W16 英文结构套话、W17 标点腔），
另加几条只适合整篇看的结构信号：长段落（W14）、段落长度过分整齐、段首加粗标签重复、段末金句。
规则表见 references/de-ai-rules.md。只给词面与结构分，不给「作者姿态分」。

用法：
  python3 scan_ai_flavor.py <file>            # Markdown 报告
  python3 scan_ai_flavor.py --json <file>     # JSON
  python3 scan_ai_flavor.py -o report.md <file>
  cat article.md | python3 scan_ai_flavor.py -

只用 Python 标准库。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True  # 不在技能目录里留 __pycache__
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lint_x_post as L  # noqa: E402  同目录、同一份规则

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

PENALTY = {"W9": 4, "W15": 5, "W16": 4, "W17": 3, "W14": 2}
LEAD_LABEL_RE = re.compile(r"^\s*(?:[-*+]\s+)?\*\*([^*]{1,12})[：:]\*\*")
TAIL_QUIP_RE = re.compile(r"^[^，。！？\n]{2,16}[。！]$")  # 段末单独一行的短句金句


def scan_text(text: str) -> dict:
    raw = text.splitlines()
    plain = L.md_to_plain(raw)
    hits = []
    for no, ln in enumerate(plain, 1):
        if not ln.strip():
            continue
        for m in L.AI_RE.finditer(ln):
            hits.append({"line": no, "code": "W9", "name": "套话词", "text": m.group(0)})
    for no, code, msg in L.struct_hits(plain, 1):
        hits.append({"line": no, "code": code, "name": msg.split("：")[0], "text": msg.split("：", 1)[-1].split("；")[0]})
    for no, code, msg in L.punct_hits(plain, 1, True):
        hits.append({"line": no, "code": code, "name": "标点腔", "text": msg.split("：")[0]})

    for no, ln in enumerate(plain, 1):
        if ln.strip() and not ln.lstrip().startswith("·"):
            n = sum(1 for ch in L.URL_RE.sub("", ln) if not ch.isspace())
            if n > L.LONG_PARA_MAX:
                hits.append({"line": no, "code": "W14", "name": "长段落", "text": f"约 {n} 字"})
    body = "\n".join(plain)
    chars = sum(1 for ch in body if not ch.isspace())
    paras = [p for p in re.split(r"\n\s*\n", body) if p.strip()]
    structural, notes = 0, []
    lens = [sum(1 for ch in p if not ch.isspace()) for p in paras if not p.lstrip().startswith("·")]
    if len(lens) >= 8 and statistics.mean(lens) > 0:
        cv = statistics.pstdev(lens) / statistics.mean(lens)
        if cv < 0.25:
            structural += 6
            notes.append(f"段落长度过分整齐（变异系数 {cv:.2f}）：长短交错")
    labels = Counter(m.group(1) for m in (LEAD_LABEL_RE.match(x) for x in raw) if m)
    rep = [k for k, v in labels.items() if v >= 3]
    if rep:
        structural += 4
        notes.append("段首加粗标签重复：" + "、".join(rep))
    quips = 0
    for p in paras:
        lines = [x for x in p.splitlines() if x.strip()]
        if len(lines) >= 2 and TAIL_QUIP_RE.match(lines[-1].strip()):
            quips += 1
    if quips >= 3:
        structural += min(8, quips * 2)
        notes.append(f"段末金句 {quips} 处：最后一句多半可以删")

    scale = min(1.0, max(0.4, (1000 / max(chars, 1)) ** 0.5))  # 长文按篇幅放宽，但不无限稀释
    lexical = round(sum(PENALTY.get(h["code"], 2) for h in hits) * scale)
    score = max(0, min(100, 100 - lexical - structural))
    return {"score": score, "level": grade(score), "chars": chars, "lexical": lexical,
            "structural": structural, "notes": notes, "hits": hits}


def grade(score: int) -> str:
    if score >= 85:
        return "人话"
    if score >= 70:
        return "轻微 AI 味"
    if score >= 50:
        return "明显 AI 味"
    return "重度 AI 味"


def render_markdown(r: dict, source: str) -> str:
    md = ["## 去 AI 味扫描", "", f"- 文件：`{source}`", f"- **总分：{r['score']} / 100（{r['level']}）**",
          f"- 字数：{r['chars']}；句式扣分 -{r['lexical']}；结构扣分 -{r['structural']}", ""]
    if r["notes"]:
        md += ["### 结构信号"] + [f"- {n}" for n in r["notes"]] + [""]
    md.append("### 命中位置")
    if not r["hits"]:
        md.append("无命中")
    else:
        md += ["| 行 | 代码 | 类型 | 命中 |", "|---|---|---|---|"]
        for h in r["hits"][:40]:
            md.append(f"| {h['line']} | {h['code']} | {h['name']} | {h['text'][:30]} |")
        if len(r["hits"]) > 40:
            md.append(f"\n（还有 {len(r['hits']) - 40} 处未显示）")
    md += ["", "改法见 references/de-ai-rules.md；只改表达，不改事实和确定性。"]
    return "\n".join(md)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="中文去 AI 味打分（内置实现）")
    ap.add_argument("input", help="输入文件，- 表示标准输入")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("-o", "--output", help="输出文件（默认 stdout）")
    a = ap.parse_args(argv)
    if a.input == "-":
        text, source = sys.stdin.read(), "<stdin>"
    else:
        p = Path(a.input)
        if not p.is_file():
            print(f"文件不存在：{a.input}", file=sys.stderr)
            return 1
        text, source = p.read_text(encoding="utf-8-sig"), str(p)
    r = scan_text(text)
    out = json.dumps(r, ensure_ascii=False, indent=2) if a.json else render_markdown(r, source)
    if a.output:
        Path(a.output).write_text(out, encoding="utf-8")
        print(f"已写入 {a.output}（{r['score']} 分 / {r['level']}）")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
