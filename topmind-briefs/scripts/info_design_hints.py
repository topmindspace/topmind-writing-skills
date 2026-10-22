#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""info_design_hints.py — 信息设计提示（I1–I9，只提示，不判卷）。

    python3 info_design_hints.py 稿子.md [--budget 2000] [--type essay] [--json]

判断方法见 references/information-design.md。提示的是「这里的内容形状可能更适合列表 / 表格 / 图」
「这一段可能在重复」，不是错误：永远不进 --strict，退出码只在读不到文件时为 2，其余为 0。

  I1 连续纯文字块过多（≥4 段，中间没有图、表、列表、小标题）
  I2 图、表、列表太少（长文每 800 字不到一个）
  I3 一句里并列项多（「、」串起 3 项以上较长的项、分号串 3 段以上、连续几段用「第一 / 首先」开头），可以转列表
  I4 连着几组「改前 / 改后」「A：/ B：」对照，可以转表格
  I5 相邻段落重复表达（8 字以上相同片段），或一节首句复读小标题
  I6 首段太长（超过 120 字），或首段没有交底（没有数字、以问句收住）
  I7 某一节（##）超过 400 字却全是段落
  I8 超出骨架里写的篇幅预算 30% 以上（读同目录 骨架.md 的「篇幅：约 N 字」，或 --budget）
  I9 某一节（##）超过 400 字，却一句判断都没有（大概率 / 预计 / 意味着 / 我的判断 / 说白了…）：素材罗列

frontmatter 写 `type: essay`（随笔、故事）时不提示 I1、I2、I7。
"""
import argparse
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

CODES = {
    "I1": "连续纯文字", "I2": "图表列表少", "I3": "并列项可转列表", "I4": "对照可转表格",
    "I5": "重复表达", "I6": "首段没交底", "I7": "长节全是段落", "I8": "超篇幅预算",
    "I9": "素材罗列",
}
ESSAY_EXEMPT = {"I1", "I2", "I7"}

RUN_MAX = 3            # 连续纯文字块的参考上限
CHARS_PER_ELEMENT = 800
LEAD_MAX = 120
SECTION_MIN = 400
REPEAT_MIN = 8
BUDGET_OVER = 0.30
# I9：判断句的标志词。一节里一个都没有，多半是在罗列素材（方法论、架构、对比类长文要有自己的判断）
JUDGE_RE = re.compile(r"大概率|预计|意味着|我的判断|我判断|我认为|我觉得|说白了|其实是|关键是|换句话说|所以|因此|应该|不如|值得|建议|更适合|看起来|多半|未必|恐怕|结论")
I9_EXEMPT_RE = re.compile(r"参考|来源|附录|延伸阅读|致谢|术语|名词")

_SYMBOLS_RE = re.compile(r"[\s*\-#>\[\]()`|]")
_URL_RE = re.compile(r"\]\([^)]*\)|https?://\S+")
LIST_RE = re.compile(r"^\s*(?:[-*+]\s|\d+[.)、）]\s?|[·•]\s?|[（(]?\d+[）)]\s?)")
ORDINAL_RE = re.compile(r"^(?:第[一二三四五六七八九十\d]+[，、,：:]|首先|其次|再次|最后|其一|其二|其三)")
PAIR_RE = re.compile(r"^(?:改前|改后|原文|原句|原稿|改成|修改后|之前|之后|[ABＡＢ][：:]|方案\s*[ABＡＢ])")
BOLD_HEAD_RE = re.compile(r"^\*\*[^*]{1,30}\*\*$")   # 单独一行的加粗短语当小标题（路标）
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
DIGIT_RE = re.compile(r"\d|[一二三四五六七八九十百千万亿两]+(?:个|次|倍|年|月|天|小时|分钟|字|篇|张|轮|成|%)")


def vlen(text: str) -> int:
    return len(_SYMBOLS_RE.sub("", _URL_RE.sub("]", text)))


def split_frontmatter(lines):
    meta, start = {}, 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                for ln in lines[1:i]:
                    if ":" in ln:
                        k, v = ln.split(":", 1)
                        meta[k.strip()] = v.strip()
                start = i + 1
                break
    return meta, start


def blocks_of(lines, start):
    """切成块：(类型, 起始行号, 文本)。类型：text / heading / image / list / table / quote / code / caption。"""
    out, cur, cur_no, fence, comment = [], [], 0, False, False

    def flush():
        nonlocal cur
        if cur:
            out.append(classify(cur, cur_no))
            cur = []

    for i in range(start, len(lines)):
        ln, no = lines[i], i + 1
        s = ln.strip()
        if comment:
            if "-->" in s:
                comment = False
            continue
        if s.startswith("<!--"):
            flush()
            if "-->" not in s:
                comment = True
            continue
        if s.startswith(("```", "~~~")):
            if not fence:
                flush()
                out.append(("code", no, ""))
            fence = not fence
            continue
        if fence:
            continue
        if not s:
            flush()
            continue
        if s.startswith("#") or BOLD_HEAD_RE.match(s):
            flush()
            out.append(("heading", no, s))
            continue
        if not cur:
            cur_no = no
        cur.append(s)
    flush()
    return out


def classify(buf, no):
    first = buf[0]
    text = "\n".join(buf)
    if first.startswith("!["):
        return ("image", no, text)
    if first.startswith("|"):
        return ("table", no, text)
    if first.startswith(">"):
        return ("quote", no, text)
    if first.startswith(("来源：", "来源:", "图：", "注：")) and len(buf) == 1:
        return ("caption", no, text)
    if sum(1 for b in buf if LIST_RE.match(b)) >= max(2, len(buf) // 2 + 1):
        return ("list", no, text)
    if len(buf) >= 3 and sum(1 for b in buf if vlen(b) <= 40) == len(buf):
        return ("list", no, text)   # 短行分行写，读起来就是列表
    return ("text", no, text)


ELEMENTS = {"image", "table", "list", "code", "quote"}


def units(text):
    """并列项长度：一个汉字算 1，一个英文词 / 数字算 1（「Mac、Windows、Linux」是短项，不提示）。"""
    return len(CJK_RE.findall(text)) + len(re.findall(r"[A-Za-z0-9][A-Za-z0-9.+_-]*", text))


def _clauses(text):
    return [c for c in re.split(r"[。！？!?\n]", text) if c.strip()]


def _strip_heading(h):
    h = re.sub(r"^#+\s*", "", h)
    h = re.sub(r"^[一二三四五六七八九十\d]+[、.．]\s*", "", h)
    return re.sub(r"[\s：:，,？?！!「」“”]", "", h)


def _norm(text):
    return re.sub(r"[\s，。、；：！？,.;:!?「」“”‘’()（）*`#>\-]", "", text)


def analyze(text, essay=False, budget=None):
    lines = text.splitlines()
    meta, start = split_frontmatter(lines)
    if meta.get("type", "").strip().lower() == "essay":
        essay = True
    blocks = blocks_of(lines, start)
    hits = []
    body = [b for b in blocks if b[0] != "heading" or not b[2].startswith("# ")]
    texts = [b for b in body if b[0] == "text"]
    total = sum(vlen(b[2]) for b in body if b[0] in ("text", "list", "table", "quote", "caption"))

    # I1 连续纯文字
    run = []
    for b in body + [("end", 0, "")]:
        if b[0] == "text":
            run.append(b)
            continue
        if b[0] == "caption":
            continue
        if len(run) > RUN_MAX:
            hits.append((run[0][1], "I1", f"连续 {len(run)} 段纯文字（第 {run[0][1]}–{run[-1][1]} 行）：中间能不能插一张图，或把并列 / 对照的内容转成列表、表格"))
        run = []

    # I2 图表列表少
    elements = sum(1 for b in body if b[0] in ELEMENTS)
    if total >= CHARS_PER_ELEMENT * 2 and total / max(1, elements) > CHARS_PER_ELEMENT:
        hits.append((body[0][1] if body else 1, "I2", f"全文约 {total} 字，图 / 表 / 列表 {elements} 个（参考：每 500–800 字一个）：哪些段落其实是数据、步骤或对比"))

    # I3 并列项
    ord_run = []
    for b in body + [("end", 0, "")]:
        if b[0] == "text" and ORDINAL_RE.match(b[2]):
            ord_run.append(b)
        else:
            if len(ord_run) >= 2:
                hits.append((ord_run[0][1], "I3", f"连续 {len(ord_run)} 段用「第一 / 首先」类开头：这是一个列表"))
            ord_run = []
    for b in texts:
        done = False
        for c in _clauses(b[2]):
            semis = [x for x in re.split(r"[；;]", c) if vlen(x) >= 4]
            if len(semis) >= 3:
                hits.append((b[1], "I3", f"一句里用分号串了 {len(semis)} 段：可以拆成列表"))
                done = True
                break
            for part in re.split(r"[，,：:]", c):
                items = part.split("、")
                if len(items) >= 3 and min(units(x) for x in items[:-1]) >= 4 and units(items[-1]) >= 2:
                    hits.append((b[1], "I3", f"「{part[:20]}…」并列了 {len(items)} 项、每项都不短：可以转成列表"))
                    done = True
                    break
            if done:
                break

    # I4 对照
    pair_lines = []
    for b in texts + [b for b in body if b[0] == "quote"]:
        for k, ln in enumerate(b[2].split("\n")):
            if PAIR_RE.match(re.sub(r"^[>\s*]+", "", ln)):
                pair_lines.append(b[1] + k)
    if len(pair_lines) >= 4:
        hits.append((pair_lines[0], "I4", f"正文里有 {len(pair_lines)} 行「改前 / 改后」「A：/ B：」式对照：两组以上可以做成两列表格"))

    # I5 重复：相邻（3 段内）段落有 8 字以上相同片段；一节首句复读小标题
    norm = [(b[1], _norm(b[2])) for b in texts if not PAIR_RE.match(b[2])]   # 对照行本来就相似，归 I4
    seen = set()
    for i in range(len(norm)):
        for j in range(i + 1, min(i + 3, len(norm))):
            a, c = norm[i][1], norm[j][1]
            m = SequenceMatcher(None, a, c, autojunk=False).find_longest_match(0, len(a), 0, len(c))
            frag = a[m.a:m.a + m.size]
            if m.size >= REPEAT_MIN and len(CJK_RE.findall(frag)) >= 6 and norm[j][0] not in seen:
                seen.add(norm[j][0])
                hits.append((norm[j][0], "I5", f"和第 {norm[i][0]} 行重复「{frag[:16]}」：同一个意思说一遍就够"))
    for k, b in enumerate(body):
        if b[0] == "heading" and b[2].startswith("##"):
            core = _strip_heading(b[2])
            nxt = next((x for x in body[k + 1:] if x[0] != "caption"), None)
            if nxt and nxt[0] == "text" and len(core) >= 4:
                first = _norm(_clauses(nxt[2])[0]) if _clauses(nxt[2]) else ""
                m = SequenceMatcher(None, core, first, autojunk=False).find_longest_match(0, len(core), 0, len(first))
                if m.size >= max(4, int(len(core) * 0.8)):
                    hits.append((nxt[1], "I5", f"首句复读小标题「{core[:12]}」：小标题已经说了，首句直接给新信息"))

    # I6 首段
    lead = next((b for b in body if b[0] in ("text", "list", "table", "image")), None)
    if lead and lead[0] == "text":
        n = vlen(lead[2])
        if n > LEAD_MAX:
            hits.append((lead[1], "I6", f"首段 {n} 字：开头一两句先交底（结论或最关键的事实），细节往后放"))
        elif not DIGIT_RE.search(lead[2]) and re.search(r"[？?]\s*$|[…]+\s*$", lead[2].strip()):
            hits.append((lead[1], "I6", "首段没有数字也没有结论、以问句或省略号收住：读者看完开头还不知道这篇要说什么"))

    # I7 长节全是段落
    sec, sec_no, sec_title = [], None, ""
    for b in body + [("heading", 0, "## end")]:
        if b[0] == "heading" and b[2].startswith("## "):
            if sec_no and sec:
                chars = sum(vlen(x[2]) for x in sec if x[0] == "text")
                if chars > SECTION_MIN and not any(x[0] in ELEMENTS for x in sec):
                    hits.append((sec_no, "I7", f"这一节约 {chars} 字，全是段落：至少放一张图、一个列表或表格，或拆成两节"))
                all_chars = sum(vlen(str(x[2])) for x in sec)
                if (all_chars > SECTION_MIN and not I9_EXEMPT_RE.search(sec_title)
                        and not any(JUDGE_RE.search(str(x[2])) for x in sec)):
                    hits.append((sec_no, "I9", f"这一节约 {all_chars} 字，没有一句判断：素材之外，写一句你怎么看（骨架「我的判断」）"))
            sec, sec_no, sec_title = [], b[1], b[2]
        elif sec_no:
            sec.append(b)

    # I8 篇幅预算
    if budget and total > budget * (1 + BUDGET_OVER):
        hits.append((body[0][1] if body else 1, "I8", f"全文约 {total} 字，骨架预算 {budget} 字，超出 {total / budget - 1:.0%}：回头对一下哪一节写跑了"))

    if essay:
        hits = [h for h in hits if h[1] not in ESSAY_EXEMPT]
    return sorted(hits, key=lambda h: (h[0], h[1]))


def read_budget(md_path: Path):
    sk = md_path.parent / "骨架.md"
    if not sk.is_file():
        return None
    m = re.search(r"篇幅[：:]\s*约?\s*(\d{3,6})\s*字", sk.read_text(encoding="utf-8", errors="replace"))
    return int(m.group(1)) if m else None


def check_file(path, essay=False, budget=None):
    p = Path(path)
    text = p.read_text(encoding="utf-8-sig")
    return analyze(text, essay=essay, budget=budget or read_budget(p))


def main(argv=None):
    ap = argparse.ArgumentParser(description="信息设计提示 I1–I9（只提示，不进 --strict）")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--budget", type=int, help="篇幅预算（字）；缺省读同目录 骨架.md")
    ap.add_argument("--type", choices=["essay"], help="随笔 / 故事：不提示 I1、I2、I7")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    report = []
    for f in args.files:
        try:
            hits = check_file(f, essay=args.type == "essay", budget=args.budget)
        except (OSError, UnicodeDecodeError) as e:
            print(f"错误：无法读取 {f}（{e}）", file=sys.stderr)
            return 2
        report.append({"file": f, "hints": [{"line": n, "code": c, "msg": m} for n, c, m in hits]})
        if not args.json:
            for n, c, m in hits:
                print(f"{f}:{n}: [{c}] 信息设计：{m}")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    else:
        total = sum(len(r["hints"]) for r in report)
        print(f"info_design_hints：{total} 条提示（只供判断，不是错误；方法见 information-design.md）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
