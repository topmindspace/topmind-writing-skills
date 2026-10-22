#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_article.py — 检查文章文件夹结构（<文章名>/<文章名>.md 单源）。

    python3 check_article.py <文章名>/<文章名>.md [--json]
    python3 check_article.py <文章名>/                      # 传文件夹也行
    python3 check_article.py 30-短文/<日期-主题>/公众号短文.md   # 短文文件夹也行（见下面「短文文件夹」）

短文文件夹：文件名是「公众号短文.md」，或路径里有「30-短文/」时按短文检查——
    不要求文件名 = 标题（E2 只比 H1 和 frontmatter title），不要求封面和 tags；
    没有 frontmatter 或缺 title / date / status 只报 W7，不报 E1。

E 级（必须清零，有任何一条退出码 1）：
    E1 frontmatter 缺字段（title / date / status / tags / cover 五个都要有）
    E2 H1 标题、frontmatter title、文件名三者不一致
    E3 正文引用的本地图片不存在（草稿期的占位截图例外，见 W4；定稿 / 已发布时照样是 E3）
    E4 images/ 下图片编号与正文出现顺序不一致（后出现的图序号反而更小或重复），或没有序号前缀
    E5 出现 Obsidian 写法 ![[ ]]、callout（> [!note]）或 ::: 容器——源稿要能被任何 Markdown 工具读
    E6 定稿 / 已发布的稿子里还有占位图（文件名带「待补 / 占位 / placeholder」）
    E7 定稿 / 已发布的稿子，frontmatter cover 指向的封面不存在（或 cover 留空）
W 级（逐条给结论）：
    W1 images/ 里有图没被正文引用
    W2 远程图片（发布前应下载到 images/）
    W3 顺序正确，但编号不连续或带插入后缀（11a、11b），建议重编号
    W4 草稿期的占位截图：图片还没放进来（文件名带「待补 / 占位 / placeholder / 截图」，或在 素材来源.md 里登记过），
       或放的是占位图；status 改成定稿前要补上
    W5 草稿期封面还没做：cover 指向的文件不存在或 cover 留空（定稿时升级成 E7）
    W6 subtitle（可选）写了但和标题一样，或超过 40 字
    H1 updated_at 写了但没有时区（如 2026-10-18T17:00:00，应写成 +08:00 或 Z 结尾）；
       多环境字段 updated_at / updated_env / updated_by 都是可选的，缺了不报
    W7 短文文件夹缺 frontmatter 或缺 title / date / status（建议补上，方便归档和多环境协作）
    W18 自制图没标清楚：图注（alt）或紧跟的「来源：」行要写「自制」和数据来源
        （与 de_ai_lint / lint_x_post 的 W18 同一口径）
"""
import argparse
import json
import os
import re
import sys

REQUIRED = ("title", "date", "status", "tags", "cover")
OPTIONAL = ("subtitle", "updated_at", "updated_env", "updated_by")  # 可选字段：留空或不写都行
TZ_RE = re.compile(r"(Z|[+-]\d{2}:?\d{2})$", re.I)
SUBTITLE_MAX = 40
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
IMG_EXT = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")
SELFMADE_RE = re.compile(r"自制|self[- ]?made", re.I)
SOURCE_HINT_RE = re.compile(r"数据|来源|据|source|data", re.I)
SOURCE_LINE_RE = re.compile(r"^来源[：:]")
PLACEHOLDER_NAME_RE = re.compile(r"待补|占位|placeholder", re.I)
SCREENSHOT_NAME_RE = re.compile(r"截图|screenshot", re.I)
FINAL_STATUS = ("定稿", "已发布")
SHORT_STEMS = ("公众号短文", "X短文")
SHORT_REQUIRED = ("title", "date", "status")


def is_short_article(md_path):
    stem = os.path.splitext(os.path.basename(md_path))[0]
    parts = os.path.normpath(md_path).split(os.sep)
    return stem in SHORT_STEMS or "30-短文" in parts


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
    errors, warns, hints = [], [], []
    md_path = os.path.abspath(md_path)
    root = os.path.dirname(md_path)
    stem = os.path.splitext(os.path.basename(md_path))[0]
    with open(md_path, encoding="utf-8-sig") as f:
        text = f.read()
    lines = text.split("\n")

    short = is_short_article(md_path)
    fm, body_start = parse_frontmatter(lines)
    if fm is None:
        if short:
            warns.append((1, "W7", "短文没有 frontmatter：建议补 title / date / status，方便归档和多环境协作"))
        else:
            errors.append((1, "E1", "缺 frontmatter（需要 title / date / status / tags / cover）"))
        fm = {}
    else:
        missing = [k for k in (SHORT_REQUIRED if short else REQUIRED) if k not in fm]
        if missing and short:
            warns.append((1, "W7", "短文 frontmatter 缺字段：%s" % "、".join(missing)))
        elif missing:
            errors.append((1, "E1", "frontmatter 缺字段：%s" % "、".join(missing)))
        ua = fm.get("updated_at", "")
        if ua and not TZ_RE.search(ua):
            ua_line = next((i + 1 for i, ln in enumerate(lines[:body_start]) if ln.startswith("updated_at:")), 1)
            hints.append((ua_line, "H1", "updated_at 没有时区：%s；写成 ISO 8601 带时区（如 +08:00 或 Z 结尾），"
                                        "多环境协作时新旧以它为准" % ua))

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
    names = {"H1": h1, "frontmatter title": title} if short else {"H1": h1, "frontmatter title": title, "文件名": stem}
    present = {k: v for k, v in names.items() if v}
    if len(set(present.values())) > 1:
        errors.append((h1_line or 1, "E2", "标题不一致：%s" % "；".join(
            "%s=%s" % (k, v) for k, v in present.items())))

    final = fm.get("status", "") in FINAL_STATUS and not short
    if "cover" in fm and (fm.get("cover") or not short):
        cv = fm.get("cover", "")
        if not cv:
            (errors if final else warns).append(
                (1, "E7" if final else "W5", "cover 留空：封面做好后填 cover/cover-1500x600.png 这类相对路径"))
        elif not re.match(r"https?://", cv) and not os.path.isfile(os.path.normpath(os.path.join(root, cv))):
            if final:
                errors.append((1, "E7", "定稿的封面不存在：%s" % cv))
            else:
                warns.append((1, "W5", "封面还没做：%s（草稿期只提醒；定稿前用 topmind-cover 出图）" % cv))
    sub = fm.get("subtitle", "")
    if sub:
        if title and sub == title:
            warns.append((1, "W6", "subtitle 和 title 一样，留空或换成概括结构的一句（core-voice V02）"))
        elif len(sub) > SUBTITLE_MAX:
            warns.append((1, "W6", "subtitle 有 %d 字，超过 %d 字；副标题概括结构就够（core-voice V02）" % (len(sub), SUBTITLE_MAX)))
    sources_txt = ""
    sp = os.path.join(root, "素材来源.md")
    if os.path.isfile(sp):
        with open(sp, encoding="utf-8-sig") as f:
            sources_txt = f.read()
    used = []
    ordering = []  # 参与编号顺序检查的图（含草稿期还没放进来的占位截图）
    for no, alt, src in refs:
        if re.match(r"https?://", src):
            warns.append((no, "W2", "远程图片，发布前下载到 images/：%s" % src))
            continue
        p = os.path.normpath(os.path.join(root, src))
        base = os.path.basename(src)
        is_placeholder = bool(PLACEHOLDER_NAME_RE.search(base))
        if not os.path.isfile(p):
            planned = is_placeholder or SCREENSHOT_NAME_RE.search(base) or (base in sources_txt)
            if planned and not final:
                warns.append((no, "W4", "占位截图还没放进来：%s（草稿期只提醒；改成定稿前要补上）" % src))
                ordering.append((no, p))
            else:
                errors.append((no, "E3", "图片不存在：%s" % src))
            continue
        if is_placeholder:
            if final:
                errors.append((no, "E6", "定稿里还有占位图：%s" % src))
            else:
                warns.append((no, "W4", "这张还是占位图：%s（改成定稿前替换）" % src))
        used.append((no, p))
        ordering.append((no, p))

    img_dir = os.path.join(root, "images")
    in_images = [(no, p) for no, p in ordering
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
            "warnings": [dict(line=l, code=c, msg=m) for l, c, m in warns],
            "hints": [dict(line=l, code=c, msg=m) for l, c, m in hints]}


def resolve(path):
    if os.path.isdir(path):
        name = os.path.basename(os.path.normpath(path))
        cand = os.path.join(path, name + ".md")
        if os.path.isfile(cand):
            return cand
        cand = os.path.join(path, "公众号短文.md")
        if os.path.isfile(cand):
            return cand
        skip = {"素材来源.md", "骨架.md", "交付说明.md", "README.md"}
        mds = [f for f in os.listdir(path) if f.endswith(".md") and f not in skip]
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
        for it in r["hints"]:
            print("  [%s] 第 %d 行：%s" % (it["code"], it["line"], it["msg"]))
        print("E %d / W %d%s%s" % (len(r["errors"]), len(r["warnings"]),
                                   " / H %d" % len(r["hints"]) if r["hints"] else "",
                                 "" if r["errors"] else "  ✓ 结构通过"))
    return 1 if r["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
