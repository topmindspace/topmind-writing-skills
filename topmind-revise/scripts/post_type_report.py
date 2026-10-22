#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""post_type_report.py — 用自己导出的帖子数据，看哪种开头、结尾、长度、类型更好（风格校准和周复盘用）。

    python3 post_type_report.py 帖子.jsonl                       # JSONL：每行一个 {"text": ..., "views": ...}
    python3 post_type_report.py 帖子.csv --text-col text --metric-col views
    python3 post_type_report.py 帖子.jsonl --config 词表.json     # 换成自己的分类词表
    python3 post_type_report.py 帖子.jsonl --json                # 机器可读输出
    python3 post_type_report.py 帖子.jsonl --samples-out 样本习惯.md   # 另存作者写作习惯（给 topmind-revise 的 samples 用）

输出：每个维度（开头 / 结尾 / 长度 / 类型 / 是否带图 / 是否带话题标签）下各类的条数、指标中位数、
相对全体中位数的倍数。倍数只看方向：类型是正则粗分，样本少时波动很大（少于 --min-n 条的类不显示倍数）。

词表是一个 JSON：{"opening": {"类名": "正则", ...}, "ending": {...}, "type": {...}}，缺的维度用内置默认；
某一类要「至少出现 N 次」时写成 {"regex": "正则", "min": N}（比如对话体要两行以上「xx：」）。
本脚本不带任何数据；数据和结论放在你自己的私有目录。只用 Python 标准库。
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

DEFAULT_LEXICON = {
    "opening": {
        "真疑问": r"^(?:难道|有没有人|是不是就我|一直没想明白|我就纳闷|到底|[^。\n]{0,20}[吗？?]\s*$)",
        "惊叹 / 情绪": r"^(?:卧槽|我靠|好家伙|救命|妈的|不是吧|离谱|绝了|太)",
        "判断语": r"^(?:说实话|我认为|我觉得|其实|本质上|说白了|真正的)",
        "求证 / 扒料": r"(?:？！|\?!|被扒|要上新|要来了|出现在|闪现)",
        "播报": r"^(?:重磅|突发|刚刚|官宣|正式发布)",
    },
    "ending": {
        "省略号": r"(?:\.\.\.|…)\s*$",
        "问句": r"[？?]\s*$",
        "感叹": r"[！!]\s*$",
        "句号": r"[。.]\s*$",
    },
    "type": {
        "故障求证": r"挂了|崩了|宕机|转圈|报错",
        "群聊 / 对话": {"regex": r"(?m)^[^\n：:]{1,8}[：:]\S", "min": 2},
        "连续剧": r"Day\s*\d+|第\s*\d+\s*天|番外",
        "算账 / 额度": r"额度|账单|token|订阅|多少钱|块钱|美元",
        "关系帖": r"互关|蓝V|破\s*\d+|就差\s*\d+|出摊|新人报到",
        "互助帖": r"邀请码|求码|送码",
    },
}
LEN_BUCKETS = [(0, 30, "≤30 字"), (31, 60, "31–60 字"), (61, 150, "61–150 字"), (151, 400, "151–400 字"), (401, 10**9, "400 字以上")]
HASHTAG_RE = re.compile(r"(?<![\w&#])#[\w\u4e00-\u9fff]{1,40}")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]")


def load_posts(path: str, text_col: str, metric_col: str, media_col: str | None):
    p = Path(path)
    rows = []
    if p.suffix.lower() == ".csv":
        with p.open(encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
    else:
        for ln in p.read_text(encoding="utf-8-sig").split("\n"):
            ln = ln.strip()
            if ln:
                rows.append(json.loads(ln))
    posts = []
    for r in rows:
        text = str(r.get(text_col) or "").strip()
        try:
            metric = float(r.get(metric_col) or 0)
        except (TypeError, ValueError):
            continue
        if not text:
            continue
        media = bool(r.get(media_col)) if media_col else None
        posts.append({"text": text, "metric": metric, "media": media})
    return posts


def matches(rx, text: str) -> bool:
    if isinstance(rx, dict):
        return len(re.findall(rx["regex"], text)) >= int(rx.get("min", 1))
    return bool(re.search(rx, text))


def body_lines(text: str):
    return [ln for ln in text.splitlines() if ln.strip() and not re.fullmatch(r"\s*(?:#\S+\s*)+", ln)]


def classify(posts, lexicon):
    dims: dict[str, dict[str, list[float]]] = {}

    def put(dim, cls, v):
        dims.setdefault(dim, {}).setdefault(cls, []).append(v)

    for p in posts:
        lines = body_lines(p["text"])
        if not lines:
            continue
        first, last = lines[0], lines[-1]
        v = p["metric"]
        hit = [k for k, rx in lexicon["opening"].items() if matches(rx, first)]
        put("开头", hit[0] if hit else "其他", v)
        hit = [k for k, rx in lexicon["ending"].items() if matches(rx, last)]
        put("结尾", hit[0] if hit else "无标点", v)
        n = sum(1 for ch in "".join(lines) if not ch.isspace())
        put("长度", next(lbl for lo, hi, lbl in LEN_BUCKETS if lo <= n <= hi), v)
        hit = [k for k, rx in lexicon["type"].items() if matches(rx, p["text"])]
        put("类型", hit[0] if hit else "其他", v)
        put("话题标签", "带" if HASHTAG_RE.search(p["text"]) else "不带", v)
        if p["media"] is not None:
            put("配图", "带图" if p["media"] else "纯文字", v)
    return dims


def report(dims, overall, min_n):
    out = {}
    for dim, classes in dims.items():
        rows = []
        for cls, vals in sorted(classes.items(), key=lambda kv: -statistics.median(kv[1])):
            med = statistics.median(vals)
            lift = round(med / overall, 2) if overall and len(vals) >= min_n else None
            rows.append({"类": cls, "条数": len(vals), "中位数": round(med, 1), "倍数": lift})
        out[dim] = rows
    return out


def habits(posts):
    """作者写作习惯（给 topmind-revise 的 samples 校准用）：句长、结尾符号、开头词、emoji 和话题标签比例。"""
    lines = [ln for p in posts for ln in body_lines(p["text"])]
    lens = [sum(1 for ch in ln if not ch.isspace()) for ln in lines] or [0]
    ends = {}
    for p in posts:
        bl = body_lines(p["text"])
        if bl:
            m = re.search(r"(\.\.\.|…|[？?！!。.])\s*$", bl[-1])
            key = m.group(1) if m else "无标点"
            ends[key] = ends.get(key, 0) + 1
    heads = {}
    for p in posts:
        bl = body_lines(p["text"])
        if bl:
            heads[bl[0][:2]] = heads.get(bl[0][:2], 0) + 1
    n = max(1, len(posts))
    return {
        "帖子数": len(posts),
        "每行字数中位数": statistics.median(lens),
        "结尾符号": dict(sorted(ends.items(), key=lambda kv: -kv[1])),
        "常见开头两字": dict(sorted(heads.items(), key=lambda kv: -kv[1])[:10]),
        "带 emoji 比例": round(sum(1 for p in posts if EMOJI_RE.search(p["text"])) / n, 2),
        "带话题标签比例": round(sum(1 for p in posts if HASHTAG_RE.search(p["text"])) / n, 2),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="帖子开头 / 结尾 / 长度 / 类型 → 指标中位数和倍数（只看方向）")
    ap.add_argument("data", help="JSONL 或 CSV")
    ap.add_argument("--text-col", default="text")
    ap.add_argument("--metric-col", default="views", help="指标列（浏览、互动……）")
    ap.add_argument("--media-col", default=None, help="可选：是否带图的列（非空即带图）")
    ap.add_argument("--config", help="分类词表 JSON（覆盖内置默认）")
    ap.add_argument("--min-n", type=int, default=5, help="少于这么多条的类不算倍数")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--samples-out", help="另存作者写作习惯（Markdown）")
    args = ap.parse_args(argv)
    lexicon = json.loads(json.dumps(DEFAULT_LEXICON))
    if args.config:
        try:
            user = json.loads(Path(args.config).read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            print(f"错误：读不了词表 {args.config}（{e}）", file=sys.stderr)
            return 2
        for k, v in user.items():
            lexicon[k] = v
    try:
        posts = load_posts(args.data, args.text_col, args.metric_col, args.media_col)
    except (OSError, ValueError) as e:
        print(f"错误：读不了数据 {args.data}（{e}）", file=sys.stderr)
        return 2
    if not posts:
        print("错误：没有可用的帖子（检查 --text-col / --metric-col）", file=sys.stderr)
        return 2
    overall = statistics.median(p["metric"] for p in posts)
    rep = report(classify(posts, lexicon), overall, args.min_n)
    hb = habits(posts)
    if args.samples_out:
        lines = ["# 作者写作习惯（样本校准）", "", f"样本：{hb['帖子数']} 条", ""]
        for k, v in hb.items():
            if k != "帖子数":
                lines.append(f"- {k}：{v}")
        Path(args.samples_out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps({"总条数": len(posts), "全体中位数": overall, "维度": rep, "习惯": hb}, ensure_ascii=False, indent=1))
        return 0
    print(f"共 {len(posts)} 条，全体中位数 {overall:g}（倍数 = 该类中位数 / 全体中位数，只看方向）")
    for dim, rows in rep.items():
        print(f"\n## {dim}")
        print("| 类 | 条数 | 中位数 | 倍数 |\n|---|---|---|---|")
        for r in rows:
            lift = "—" if r["倍数"] is None else f"{r['倍数']}×"
            print(f"| {r['类']} | {r['条数']} | {r['中位数']:g} | {lift} |")
    print("\n## 写作习惯")
    for k, v in hb.items():
        print(f"- {k}：{v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
