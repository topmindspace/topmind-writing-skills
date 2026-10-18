#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""article_scaffold.py — 新建一篇长文的文章文件夹（单源结构）。

    python3 article_scaffold.py --title "文章标题" [--base 输出目录] [--tags AI,Agent] [--date 2026-10-18]

生成：
    <文章名>/
      <文章名>.md      唯一源稿（frontmatter 五个字段 + H1 标题）
      images/          正文配图，按出现顺序 01-xxx.png、02-xxx.png
      cover/           封面（cover-1500x600.png 等）
      素材来源.md      每张图、每个数字的出处
      raw/             原始素材、截图、笔记（不发布）
      out/             派生产物（X长文.html、X发布稿.txt、公众号版 HTML），可随时重建

文件夹已存在就报错退出，绝不覆盖。文件名里的 / \\ : * ? " < > | 换成「-」，最长 80 字。
"""
import argparse
import datetime
import os
import re
import sys

UNSAFE_RE = re.compile(r'[/\\:*?"<>|\x00-\x1f]')
MAX_NAME = 80


def safe_name(title):
    name = UNSAFE_RE.sub("-", title.strip())
    name = re.sub(r"\s+", " ", name).strip(" .-")
    return name[:MAX_NAME].rstrip(" .-")


def frontmatter(title, date, tags):
    tag_list = ", ".join(tags)
    return ("---\n"
            "title: %s\n"
            "date: %s\n"
            "status: 草稿\n"
            "tags: [%s]\n"
            "cover: cover/cover-1500x600.png\n"
            "---\n" % (title, date, tag_list))


SOURCES_TPL = """# 素材来源

每张图、每个关键数字一行：用在哪、出处、取用日期。正文图片下方的「来源：」行从这里摘。

| 位置 | 内容 | 出处 | 日期 |
|---|---|---|---|
| images/01-xxx.png | | | |
"""


def scaffold(title, base, date=None, tags=None):
    name = safe_name(title)
    if not name:
        raise ValueError("标题清洗后为空，换一个标题")
    root = os.path.join(base, name)
    if os.path.exists(root):
        raise FileExistsError("文件夹已存在，不覆盖：%s" % root)
    date = date or datetime.date.today().isoformat()
    tags = tags or []
    os.makedirs(root)
    for d in ("images", "cover", "raw", "out"):
        os.makedirs(os.path.join(root, d))
    md = os.path.join(root, name + ".md")
    with open(md, "w", encoding="utf-8") as f:
        f.write(frontmatter(name, date, tags))
        f.write("\n# %s\n\n" % name)
    with open(os.path.join(root, "素材来源.md"), "w", encoding="utf-8") as f:
        f.write(SOURCES_TPL)
    return root, md


def main():
    ap = argparse.ArgumentParser(description="新建长文文章文件夹（<文章名>/<文章名>.md 单源）")
    ap.add_argument("--title", required=True, help="文章标题，也是文件夹名和文件名")
    ap.add_argument("--base", default=".", help="在哪个目录下建（缺省当前目录）")
    ap.add_argument("--date", default=None, help="frontmatter date，缺省今天")
    ap.add_argument("--tags", default="", help="逗号分隔的标签")
    args = ap.parse_args()
    tags = [t.strip() for t in re.split(r"[,，]", args.tags) if t.strip()]
    try:
        root, md = scaffold(args.title, args.base, args.date, tags)
    except (FileExistsError, ValueError) as e:
        print("错误：%s" % e, file=sys.stderr)
        return 1
    print("文章文件夹：%s" % root)
    print("源稿      ：%s" % md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
