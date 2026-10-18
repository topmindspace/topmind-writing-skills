#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_article.py — 检查文章文件夹结构（<文章名>/<文章名>.md 单源）。

    python3 check_article.py <文章名>/<文章名>.md [--json]
    python3 check_article.py <文章名>/                      # 传文件夹也行

E 级（必须清零，有任何一条退出码 1）：
    E1 frontmatter 缺字段（title / date / status / tags / cover 五个都要有）
    E2 H1 标题、frontmatter title、文件名三者不一致
    E3 正文引用的本地图片不存在
    E4 images/ 下图片编号与正文出现顺序不一致（后出现的图序号反而更小或重复），或没有序号前缀
    E5 出现 Obsidian 写法 ![[ ]]、callout（> [!note]）或 ::: 容器——源稿要能被任何 Markdown 工具读
W 级（逐条给结论）：
    W1 images/ 里有图没被正文引用
    W2 远程图片（发布前应下载到 images/）
    W3 顺序正确，但编号不连续或带插入后缀（11a、11b），建议重编号
    W18 自制图没标清楚：图注（alt）或紧跟的「来源：」行要写「自制」和数据来源
        （与 de_ai_lint / lint_x_post 的 W18 同一口径）
"""
import argparse
import json
import os
import re
import sys

REQUIRED = ("title", "date", "status", "tags", "cover")
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
IMG_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")
SELFMADE_RE = re.compile(r"自制|self[- ]?made", re.I)
SOURCE_HINT_RE = re.compile(r"数据|来源|据|source|data", re.I)
SOURCE_LINE_RE = re.compile(r"^来源[：:]")


def parse_frontmatter(lines):
    if not lines or lines[0].strip() != "---":
        return None, 0
    fm = {}
    for i, ln in enumerate(lines[1:], 1):
        if ln.strip() == "---":
            return fm, i + 1
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", ln)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip("\"'")
    return fm, 0


def check(md_path):
    errors, warns = [], []
    md_path = os.path.abspath(md_path)
    root = os.path.dirname(md_path)
    stem = os.path.splitext(os.path.basename(md_path))[0]
    with open(md_path, encoding="utf-8-sig") as f:
        text = f.read()
    lines = text.split("\n")

    fm, body_start = parse_frontmatter(lines)
    if fm is None:
        errors.append((1, "E1", "缺 frontmatter（需要 title / date / status / tags / cover）"))
        fm = {}
    else:
        missing = [k for k in REQUIRED if k not in fm]
        if missing:
            errors.append((1, "E1", "frontmatter 缺字段：%s" % "、".join(missing)))

    h1, h1_line = None, 0
    fence = False
    comment = False  # <!-- … --> 里的写作提示不检查
    refs = []  # (line, alt, src)
    for no, ln in enumerate(lines, 1):
        if no <= body_start:
            continue
        st = ln.strip()
        if st.startswith("```") or st.startswith("~~~"):
            fence = not fence
            continue
        if fence:
            continue
        if comment:
            comment = "-->" not in st
            continue
        if st.startswith("<!--"):
            comment = "-->" not in st
            continue
        if h1 is None and re.match(r"^#\s+\S", st):
            h1, h1_line = st[1:].strip(), no
        if "![[" in st:
            errors.append((no, "E5", "Obsidian 图片写法 ![[ ]]，改成 ![说明](images/xx.png)"))
        if re.match(r"^>\s*\[!\w+\]", st):
            errors.append((no, "E5", "callout（> [!note]）只有部分编辑器认，改成普通段落或引用"))
        if st.startswith(":::"):
            errors.append((no, "E5", "::: 容器只有部分工具认，源稿里不用"))
        for m in IMG_RE.finditer(ln):
            refs.append((no, m.group(1), m.group(2)))
            alt, src = m.group(1), m.group(2)
            if SELFMADE_RE.search(alt + " " + src):
                # 紧跟（或隔一个空行）的「来源：」行也算图注
                nxt = ""
                for k in (no, no + 1):
                    if k < len(lines) and lines[k].strip():
                        nxt = lines[k].strip() if SOURCE_LINE_RE.match(lines[k].strip()) else ""
                        break
                label = alt + " " + nxt
                if not (SELFMADE_RE.search(label) and (SOURCE_HINT_RE.search(alt) or nxt)):
                    warns.append((no, "W18", "自制图没标清楚：图注或下一行「来源：」写「自制」和数据来源，"
                                             "例如「来源：自制，数据：xx 官方」"))

    title = fm.get("title")
    if h1 is None:
        errors.append((1, "E2", "缺 H1 标题（# 文章名）"))
    names = {"H1": h1, "frontmatter title": title, "文件名": stem}
    present = {k: v for k, v in names.items() if v}
    if len(set(present.values())) > 1:
        errors.append((h1_line or 1, "E2", "标题不一致：%s" % "；".join(
            "%s=%s" % (k, v) for k, v in present.items())))

    used = []
    for no, alt, src in refs:
        if re.match(r"https?://", src):
            warns.append((no, "W2", "远程图片，发布前下载到 images/：%s" % src))
            continue
        p = os.path.normpath(os.path.join(root, src))
        if not os.path.isfile(p):
            errors.append((no, "E3", "图片不存在：%s" % src))
            continue
        used.append((no, p))

    img_dir = os.path.join(root, "images")
    in_images = [(no, p) for no, p in used
                 if os.path.dirname(p) == img_dir]
    seen = []
    for no, p in in_images:
        if p not in seen:
            seen.append(p)
    prev_key, gaps = None, []
    for idx, p in enumerate(seen, 1):
        base = os.path.basename(p)
        no = next(n for n, q in in_images if q == p)
        m = re.match(r"^(\d+)([a-z]?)(?=[-_.\s]|$)", base, re.I)
        if not m:
            errors.append((no, "E4", "images/ 里的图没有序号前缀：%s（按出现顺序命名为 %02d-xxx）" % (base, idx)))
            continue
        key = (int(m.group(1)), m.group(2).lower())
        if prev_key is not None and key <= prev_key:
            errors.append((no, "E4", "images/ 编号与出现顺序不一致：第 %d 张是 %s，序号没有比上一张大"
                           % (idx, base)))
        elif int(m.group(1)) != idx or m.group(2):
            gaps.append(base)
        prev_key = key
    if gaps:
        warns.append((0, "W3", "图片顺序正确，但编号不连续或带插入后缀（如 11a）：%s 等 %d 张；方便时按 01、02… 重编号"
                      % (gaps[0], len(gaps))))

    if os.path.isdir(img_dir):
        used_set = {p for _, p in used}
        for f in sorted(os.listdir(img_dir)):
            fp = os.path.join(img_dir, f)
            if f.lower().endswith(IMG_EXT) and fp not in used_set:
                warns.append((0, "W1", "images/ 里没被正文引用：%s" % f))

    return {"file": md_path, "errors": [dict(line=l, code=c, msg=m) for l, c, m in errors],
            "warnings": [dict(line=l, code=c, msg=m) for l, c, m in warns]}


def resolve(path):
    if os.path.isdir(path):
        name = os.path.basename(os.path.normpath(path))
        cand = os.path.join(path, name + ".md")
        if os.path.isfile(cand):
            return cand
        mds = [f for f in os.listdir(path) if f.endswith(".md") and f != "素材来源.md"]
        if len(mds) == 1:
            return os.path.join(path, mds[0])
        raise FileNotFoundError("文件夹里找不到 <文章名>.md：%s" % path)
    if not os.path.isfile(path):
        raise FileNotFoundError("找不到文件：%s" % path)
    return path


def main():
    ap = argparse.ArgumentParser(description="检查文章文件夹结构")
    ap.add_argument("path", help="<文章名>.md 或文章文件夹")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        md = resolve(args.path)
    except FileNotFoundError as e:
        print("错误：%s" % e, file=sys.stderr)
        return 2
    r = check(md)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print("文章：%s" % r["file"])
        for it in r["errors"]:
            print("  [%s] 第 %d 行：%s" % (it["code"], it["line"], it["msg"]))
        for it in r["warnings"]:
            loc = "第 %d 行：" % it["line"] if it["line"] else ""
            print("  [%s] %s%s" % (it["code"], loc, it["msg"]))
        print("E %d / W %d%s" % (len(r["errors"]), len(r["warnings"]),
                                 "" if r["errors"] else "  ✓ 结构通过"))
    return 1 if r["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
