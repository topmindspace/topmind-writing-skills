#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""revise_check.py — 改稿保真比对 + 过度改稿检查 + 报告骨架。

比较改前、改后两份稿子：
  1. 字数：改前 → 改后、单段最长（口径同 count_words.py）。
  2. 保真：数字、日期、引语（「」“”里的内容）、英文专名、确定性词（可能 / 预计 / 已经 / 据传…）
     改前有、改后没有的列为「消失」，改后新出现的列为「新增」。数字和引语的变化要逐条确认有依据。
  3. 去 AI 味：改前 / 改后各跑一遍 de_ai_lint，报 W / H 数量变化。
  4. 过度改稿：改前没有任何 W 命中的段落里，被改写（不是删除）的比例；超过 30% 提示「可能改过头」。

用法：
    python3 revise_check.py 改前.md 改后.md                     # 打印检查结果
    python3 revise_check.py 改前.md 改后.md --report 改稿报告.md   # 另外写出报告骨架（改动表留给人填）
    python3 revise_check.py 改前.txt 改后.txt --genre short --json
    python3 revise_check.py 改前.md 改后.md --strict              # 有数字 / 引语变化或过度改稿 → 退出码 1
只用 Python 标准库；依赖同目录的 de_ai_lint.py、count_words.py。退出码：读文件失败 → 2。
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.dont_write_bytecode = True  # 同目录模块不写 __pycache__（技能包里不留缓存）
sys.path.insert(0, str(Path(__file__).resolve().parent))
import count_words as CW  # noqa: E402
import de_ai_lint as D  # noqa: E402

NUM_RE = re.compile(r"\d+(?:[.,]\d+)*\s*(?:%|万|亿|千|倍|美元|元|个|款|家|次|天|年|月|日|小时|分钟|star)?")
QUOTE_RE = re.compile(r"「([^」\n]{2,80})」|“([^”\n]{2,80})”")
LATIN_RE = re.compile(r"\b[A-Z][A-Za-z0-9.+-]*(?:\s+[A-Z][A-Za-z0-9.+-]*)*\b")
CERTAINTY = ["可能", "也许", "或许", "预计", "大概率", "多半", "据传", "传言", "厂商口径", "官方称",
             "已经", "即将", "计划", "宣布", "推测", "未证实", "现在看起来"]
OVER_EDIT_RATIO = 0.30


def _norm(s: str) -> str:
    return re.sub(r"\s+", "", s)


def paragraphs(text: str) -> list[str]:
    out, cur = [], []
    for ln in CW.body_lines(text) + [""]:
        if ln.strip():
            cur.append(ln.strip())
        elif cur:
            out.append(" ".join(cur))
            cur = []
    return out


def tokens(text: str) -> dict[str, set[str]]:
    body = "\n".join(CW.body_lines(text))
    body = re.sub(r"\]\([^)]*\)|https?://\S+", "", body)
    return {
        "数字": {_norm(m.group(0)) for m in NUM_RE.finditer(body)},
        "引语": {m.group(1) or m.group(2) for m in QUOTE_RE.finditer(body)},
        "英文专名": {m.group(0) for m in LATIN_RE.finditer(body) if len(m.group(0)) > 1},
        "确定性词": {w for w in CERTAINTY if w in body},
    }


def over_edit(before: str, after: str, genre: str):
    bp, ap_ = paragraphs(before), paragraphs(after)
    md = genre == "long"
    unhit, modified, removed = 0, [], []
    for p in bp:
        w, _h = D.analyze(p, genre, markdown=md)
        best = max((difflib.SequenceMatcher(None, _norm(p), _norm(q)).ratio() for q in ap_), default=0.0)
        if w:
            continue
        unhit += 1
        if best >= 0.98:
            continue
        if best < 0.5:
            removed.append(p[:40])
        else:
            modified.append((round(best, 2), p[:40]))
    ratio = len(modified) / unhit if unhit else 0.0
    return {"unhit_paragraphs": unhit, "modified_without_hit": len(modified), "ratio": round(ratio, 2),
            "examples": modified[:5], "removed_without_hit": removed[:5], "over_edit": ratio > OVER_EDIT_RATIO}


def check(before: str, after: str, genre: str) -> dict:
    tb, ta = tokens(before), tokens(after)
    diff = {k: {"消失": sorted(tb[k] - ta[k]), "新增": sorted(ta[k] - tb[k])} for k in tb}
    md = genre == "long"
    wb, hb = D.analyze(before, genre, markdown=md)
    wa, ha = D.analyze(after, genre, markdown=md)
    return {
        "字数": {"改前": CW.count_text(before), "改后": CW.count_text(after)},
        "保真": diff,
        "去AI味": {"改前": {"W": len(wb), "H": len(hb)}, "改后": {"W": len(wa), "H": len(ha)},
                  "改后W明细": [f"L{n} [{c}] {m}" for n, c, m in wa]},
        "过度改稿": over_edit(before, after, genre),
    }


def render(r: dict) -> str:
    b, a = r["字数"]["改前"], r["字数"]["改后"]
    lines = [f"字数：改前 {b['chars']} → 改后 {a['chars']}｜单段最长 {b['longest_paragraph']} → {a['longest_paragraph']}"]
    for k, v in r["保真"].items():
        if v["消失"] or v["新增"]:
            lines.append(f"保真·{k}：消失 {v['消失'][:8]}｜新增 {v['新增'][:8]}")
    if not any(v["消失"] or v["新增"] for v in r["保真"].values()):
        lines.append("保真：数字、引语、英文专名、确定性词都没变")
    d = r["去AI味"]
    lines.append(f"去 AI 味：W {d['改前']['W']} → {d['改后']['W']}｜H {d['改前']['H']} → {d['改后']['H']}（H 只是提示）")
    o = r["过度改稿"]
    flag = "⚠ 可能改过头，逐段确认或恢复原文" if o["over_edit"] else "正常"
    lines.append(f"过度改稿：无命中段落 {o['unhit_paragraphs']} 段，其中被改写 {o['modified_without_hit']} 段（{o['ratio']:.0%}）→ {flag}")
    for ratio, ex in o["examples"]:
        lines.append(f"  · 相似度 {ratio}：{ex}…")
    return "\n".join(lines)


REPORT_TMPL = """# 改稿报告

## 字数

{counts}

## 改动表

| 位置 | 规则编号 / 作者意见 | 原文 | 改后 |
|---|---|---|---|
|  |  |  |  |

## 保留未改的命中（及理由）

{kept}

## 保真比对

{fidelity}

## 未核实条目

- （从素材来源.md 里列出仍未核实的事实；没有写「无」）

## 过度改稿检查

{over}
"""


def write_report(r: dict, path: Path) -> None:
    text = render(r).splitlines()
    kept = "\n".join(f"- {x}：（保留理由）" for x in r["去AI味"]["改后W明细"]) or "- 无"
    path.write_text(REPORT_TMPL.format(
        counts=text[0],
        kept=kept,
        fidelity="\n".join(f"- {x}" for x in text if x.startswith("保真")),
        over="\n".join(x for x in text if x.startswith("过度改稿") or x.startswith("  ·")),
    ), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="改稿保真比对 + 过度改稿检查")
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("--genre", choices=D.GENRES, help="文体；缺省 .md 当 long，其余当 short")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--report", help="写出改稿报告骨架（Markdown）")
    ap.add_argument("--strict", action="store_true", help="数字 / 引语有变化或过度改稿 → 退出码 1")
    a = ap.parse_args(argv)
    try:
        before = Path(a.before).read_text(encoding="utf-8-sig")
        after = Path(a.after).read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as e:
        print(f"错误：无法读取（{e}）", file=sys.stderr)
        return 2
    genre = a.genre or ("long" if a.before.lower().endswith(".md") else "short")
    r = check(before, after, genre)
    print(json.dumps(r, ensure_ascii=False, indent=1) if a.json else render(r))
    if a.report:
        write_report(r, Path(a.report))
        if not a.json:
            print(f"已写出报告骨架：{a.report}")
    bad = r["过度改稿"]["over_edit"] or any(r["保真"][k]["消失"] or r["保真"][k]["新增"] for k in ("数字", "引语"))
    return 1 if (a.strict and bad) else 0


if __name__ == "__main__":
    sys.exit(main())
