#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""revise_check.py — 改稿保真比对 + 过度改稿检查 + 报告骨架。

比较改前、改后两份稿子：
  1. 字数：改前 → 改后、单段最长（口径同 count_words.py）。
  2. 保真：数字、日期、引语（「」“”里像句子的内容）、英文专名、确定性词（可能 / 预计 / 已经 / 据传…）
     按出现次数比：改前有、改后没有的列为「消失」，改后新出现的列为「新增」，两边都有但次数变了的列为「次数变化」
     （删掉一处「多半」、多引用一次某个数字，都看得见）。数字和引语的变化要逐条确认有依据。
     「」里只有几个字、没有标点的（「改前」「一文读懂」）是在讨论某个词，不算引语。
  3. 去 AI 味：改前 / 改后各跑一遍 de_ai_lint，报 W / H 数量变化。
  4. 过度改稿：改前没有任何 W 命中的段落里，被改写（不是删除）的比例；超过 30% 提示「可能改过头」。
     事实关 / 逻辑关 / 作者意见的改动不算过度改稿：在改稿报告的改动表里登记（依据写「① 事实」「② 逻辑」
     「作者意见」），再用 --declare 改稿报告.md 跑一次，这些段落会单独列出、不计入比例。
  5. 报告骨架（--report）：改动表按段落 diff 预填「原文 / 改后」，依据一栏留给人填；
     「保留未改的命中」列出改后稿里全部 W 和 H（每条都要写理由或改掉），不会再出现「无」却有命中的情况。

用法：
    python3 revise_check.py 改前.md 改后.md                     # 打印检查结果
    python3 revise_check.py 改前.md 改后.md --report 改稿报告.md   # 另外写出报告骨架（改动表留给人填）
    python3 revise_check.py 改前.txt 改后.txt --genre short --json
    python3 revise_check.py 改前.md 改后.md --strict              # 有数字 / 引语变化或过度改稿 → 退出码 1
    python3 revise_check.py 改前.md 改后.md --declare out/改稿报告.md   # 改动表里登记的事实 / 逻辑 / 作者意见改动不计入过度改稿
只用 Python 标准库；依赖同目录的 de_ai_lint.py、count_words.py。退出码：读文件失败 → 2。
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from collections import Counter
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
QUOTE_PUNCT_RE = re.compile(r"[，。！？：；、,.!?:; ]")
QUOTE_MIN = 6  # 少于 6 个字且不带标点的「」内容当作「讨论这个词」，不算引语


def _is_quote(q: str) -> bool:
    return len(q) >= QUOTE_MIN or bool(QUOTE_PUNCT_RE.search(q))
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


def tokens(text: str) -> dict[str, Counter]:
    body = "\n".join(CW.body_lines(text))
    body = re.sub(r"\]\([^)]*\)|https?://\S+", "", body)
    return {
        "数字": Counter(_norm(m.group(0)) for m in NUM_RE.finditer(body)),
        "引语": Counter(q for q in (m.group(1) or m.group(2) for m in QUOTE_RE.finditer(body)) if _is_quote(q)),
        "英文专名": Counter(m.group(0) for m in LATIN_RE.finditer(body) if len(m.group(0)) > 1),
        "确定性词": Counter({w: body.count(w) for w in CERTAINTY if w in body}),
    }


def _diff(b: Counter, a: Counter) -> dict:
    return {"消失": sorted(k for k in b if k not in a),
            "新增": sorted(k for k in a if k not in b),
            "次数变化": sorted(f"{k}（{b[k]}→{a[k]}）" for k in b if k in a and a[k] != b[k])}


DECLARE_BASIS_RE = re.compile(r"⓪|①|②|结构|事实|逻辑|作者")


def declared_snippets(report_text: str) -> list[str]:
    """从改稿报告的改动表里取「依据」是事实 / 逻辑 / 作者意见的行的「原文」片段（去掉省略号和空白）。"""
    out = []
    for ln in report_text.splitlines():
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 4 or set(cells[0]) <= {"-", ":", " "} or cells[0] == "位置":
            continue
        if DECLARE_BASIS_RE.search(cells[1]):
            frag = _norm(re.sub(r"[…\.]{1,3}|「|」|`", "", cells[2]))
            if len(frag) >= 6:
                out.append(frag[:16])
    return out


def over_edit(before: str, after: str, genre: str, declared: list[str] | None = None):
    bp, ap_ = paragraphs(before), paragraphs(after)
    md = genre == "long"
    declared = declared or []
    unhit, modified, removed, exempt = 0, [], [], []
    for p in bp:
        w, _h = D.analyze(p, genre, markdown=md)
        best = max((difflib.SequenceMatcher(None, _norm(p), _norm(q)).ratio() for q in ap_), default=0.0)
        if w:
            continue
        if best < 0.98 and any(frag in _norm(p) for frag in declared):
            exempt.append(p[:40])
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
            "examples": modified[:5], "removed_without_hit": removed[:5], "declared": exempt,
            "over_edit": ratio > OVER_EDIT_RATIO}


def change_rows(before: str, after: str) -> list[tuple[str, str, str]]:
    """按段落 diff 预填改动表：(位置, 原文, 改后)。"""
    bp, ap_ = paragraphs(before), paragraphs(after)
    rows, matched = [], set()
    for i, p in enumerate(bp, 1):
        scores = [(difflib.SequenceMatcher(None, _norm(p), _norm(q)).ratio(), j) for j, q in enumerate(ap_)]
        best, j = max(scores, default=(0.0, -1))
        if best >= 0.98:
            matched.add(j)
            continue
        if best >= 0.5:
            matched.add(j)
            rows.append((f"改前第 {i} 段", p[:60], ap_[j][:60]))
        else:
            rows.append((f"改前第 {i} 段", p[:60], "（删除或拆分）"))
    for j, q in enumerate(ap_):
        if j not in matched and max((difflib.SequenceMatcher(None, _norm(q), _norm(p)).ratio() for p in bp), default=0) < 0.5:
            rows.append((f"改后第 {j + 1} 段", "（新增或拆分）", q[:60]))
    return rows


def check(before: str, after: str, genre: str, declared: list[str] | None = None) -> dict:
    tb, ta = tokens(before), tokens(after)
    diff = {k: _diff(tb[k], ta[k]) for k in tb}
    md = genre == "long"
    wb, hb = D.analyze(before, genre, markdown=md)
    wa, ha = D.analyze(after, genre, markdown=md)
    return {
        "字数": {"改前": CW.count_text(before), "改后": CW.count_text(after)},
        "保真": diff,
        "去AI味": {"改前": {"W": len(wb), "H": len(hb)}, "改后": {"W": len(wa), "H": len(ha)},
                  "改后W明细": [f"L{n} [{c}] {m}" for n, c, m in wa],
                  "改后H明细": [f"L{n} [{c}] {m}" for n, c, m in ha]},
        "过度改稿": over_edit(before, after, genre, declared),
        "改动": change_rows(before, after),
    }


def render(r: dict) -> str:
    b, a = r["字数"]["改前"], r["字数"]["改后"]
    lines = [f"字数：改前 {b['chars']} → 改后 {a['chars']}｜单段最长 {b['longest_paragraph']} → {a['longest_paragraph']}"]
    for k, v in r["保真"].items():
        if v["消失"] or v["新增"] or v["次数变化"]:
            lines.append(f"保真·{k}：消失 {v['消失'][:8]}｜新增 {v['新增'][:8]}｜次数变化 {v['次数变化'][:8]}")
    if not any(v["消失"] or v["新增"] or v["次数变化"] for v in r["保真"].values()):
        lines.append("保真：数字、引语、英文专名、确定性词都没变")
    d = r["去AI味"]
    lines.append(f"去 AI 味：W {d['改前']['W']} → {d['改后']['W']}｜H {d['改前']['H']} → {d['改后']['H']}（H 只是提示）")
    o = r["过度改稿"]
    flag = "⚠ 可能改过头，逐段确认或恢复原文" if o["over_edit"] else "正常"
    lines.append(f"过度改稿：无命中段落 {o['unhit_paragraphs']} 段，其中被改写 {o['modified_without_hit']} 段（{o['ratio']:.0%}）→ {flag}")
    for ratio, ex in o["examples"]:
        lines.append(f"  · 相似度 {ratio}：{ex}…")
    if o.get("declared"):
        lines.append(f"  已登记为结构 / 事实 / 逻辑 / 作者意见的改动 {len(o['declared'])} 段，不计入比例")
    dz = r.get("信息设计")
    if dz is not None:
        lines.append(f"信息设计提示（I，只供判断）：改前 {len(dz['改前'])} → 改后 {len(dz['改后'])}")
        for x in dz["改后"][:5]:
            lines.append(f"↳ {x}")
    return "\n".join(lines)


REPORT_TMPL = """# 改稿报告

- 技能：topmind-revise · 模式：（revise / embed，embed 写调用方）· 文体：（long / short …）
- 备份：（备份目录，长文默认 <文章文件夹>/raw/备份-<时间戳>/）

## 字数

{counts}

## 信息设计诊断（⓪ 结构）

先于措辞看结构（方法见 information-design.md）；随笔类整篇段落是正常的。

- 主要信息：（一两句；在不在开头）
- [ ] 每节要点能一句话说出
- [ ] 并列、步骤、对照、数据没有写成长段（该转列表 / 表格 / 图的已转或已列建议）
- [ ] 没有重复的段落和复读标题的首句
- [ ] 篇幅在预算内（有骨架.md 时对照）
- 结构改动：（light 默认只做低风险改动；重排章节写建议或注明 depth=structure）

脚本提示（info_design_hints.py，I1–I9，只供判断）：

{design}

## 改动表

依据填规则编号（Z / P / V / W / H）、「⓪ 结构」「① 事实」「② 逻辑」或「作者意见」；说不出依据的改动恢复原文。

| 位置 | 依据 | 原文 | 改后 |
|---|---|---|---|
{changes}

## 保留未改的命中（及理由）

改后稿里还剩的 W 和 H 全部列在这里：W 每条写保留理由（或回去改掉），H 写一句判断。

{kept}

## 人工检查（事实关 / 逻辑关）

- [ ] 承重数字、日期、排名、「第一」逐条对过素材来源
- [ ] 引语逐字照录，语气没有升级
- [ ] 作者自述 / 回忆类说法有记录支撑，或列进未核实条目
- [ ] 结论靠前；同一事实全文同值，同一事物一个叫法
- [ ] 导语、小结和后文对得上（没有「每个」「都」这类以偏概全）
- [ ] 对比有对象和定语

## 保真比对

{fidelity}

## 未核实条目

- （从素材来源.md 里列出仍未核实的事实；没有写「无」）

## 过度改稿检查

{over}
"""


def design_summary(before_path: str, after_path: str) -> dict:
    """改前 / 改后的信息设计提示（I1–I9，只提示）；同目录没有 info_design_hints.py 时为空。"""
    try:
        import info_design_hints as IDH
    except ImportError:
        return {"改前": [], "改后": []}
    budget = IDH.read_budget(Path(after_path))
    fmt = lambda hs: [f"[{c}] L{n} {m}" for n, c, m in hs]  # noqa: E731
    return {"改前": fmt(IDH.check_file(before_path, budget=budget)), "改后": fmt(IDH.check_file(after_path, budget=budget))}


def write_report(r: dict, path: Path) -> None:
    text = render(r).splitlines()
    d = r["去AI味"]
    kept = "\n".join([f"- {x}：（保留理由，或改掉）" for x in d["改后W明细"]]
                     + [f"- {x}：（一句判断）" for x in d.get("改后H明细", [])]) or "- 无（改后稿没有 W / H 命中）"
    cell = lambda t: t.replace("|", "／")  # noqa: E731
    changes = "\n".join(f"| {loc} |  | {cell(a)} | {cell(b)} |" for loc, a, b in r.get("改动", [])) or "| （无改动） |  |  |  |"
    dz = r.get("信息设计")
    if dz is None:
        design = "- （短文体不跑；长文 Markdown 才有 I 提示）"
    else:
        design = (f"- 改前 {len(dz['改前'])} 条 → 改后 {len(dz['改后'])} 条\n"
                  + ("\n".join(f"- {x}：（转了 / 不转的理由）" for x in dz["改后"]) or "- 改后稿没有 I 提示"))
    path.write_text(REPORT_TMPL.format(
        design=design,
        counts=text[0],
        changes=changes,
        kept=kept,
        fidelity="\n".join(f"- {x}" for x in text if x.startswith("保真")),
        over="\n".join(x for x in text if x.startswith("过度改稿") or x.startswith("  ")),
    ), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="改稿保真比对 + 过度改稿检查")
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("--genre", choices=D.GENRES, help="文体；缺省 .md 当 long，其余当 short")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--report", help="写出改稿报告骨架（Markdown）")
    ap.add_argument("--strict", action="store_true", help="数字 / 引语有变化或过度改稿 → 退出码 1")
    ap.add_argument("--declare", help="已填好的改稿报告：改动表里依据是事实 / 逻辑 / 作者意见的段落不计入过度改稿")
    a = ap.parse_args(argv)
    try:
        before = Path(a.before).read_text(encoding="utf-8-sig")
        after = Path(a.after).read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as e:
        print(f"错误：无法读取（{e}）", file=sys.stderr)
        return 2
    genre = a.genre or ("long" if a.before.lower().endswith(".md") else "short")
    declared = []
    if a.declare:
        try:
            declared = declared_snippets(Path(a.declare).read_text(encoding="utf-8-sig"))
        except (OSError, UnicodeDecodeError) as e:
            print(f"错误：无法读取 --declare（{e}）", file=sys.stderr)
            return 2
    r = check(before, after, genre, declared)
    if genre == "long":
        r["信息设计"] = design_summary(a.before, a.after)
    print(json.dumps(r, ensure_ascii=False, indent=1) if a.json else render(r))
    if a.report:
        write_report(r, Path(a.report))
        if not a.json:
            print(f"已写出报告骨架：{a.report}")
    bad = r["过度改稿"]["over_edit"] or any(r["保真"][k]["消失"] or r["保真"][k]["新增"] or r["保真"][k]["次数变化"]
                                         for k in ("数字", "引语"))
    return 1 if (a.strict and bad) else 0


if __name__ == "__main__":
    sys.exit(main())
