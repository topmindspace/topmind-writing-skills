#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""article_scaffold.py — 新建一篇长文的文章文件夹（单源结构）。

    python3 article_scaffold.py --title "文章标题" [--base 输出目录] [--tags AI,Agent] [--date 2026-10-18]
                                [--env 环境名] [--by 改稿人]

生成：
    <文章名>/
      <文章名>.md      唯一源稿（frontmatter 五个必填字段 + 可选 subtitle、多环境字段 + H1 标题）
      images/          正文配图，按出现顺序 01-xxx.png、02-xxx.png
      cover/           封面（cover-1500x600.png 等）
      骨架.md          动笔前的信息设计骨架：主要信息、读者、每节要点 / 形式 / 图表计划 / 字数（不发布）
      素材来源.md      每张图、每个数字的出处
      raw/             原始素材、截图、笔记（不发布）
      out/             派生产物（X长文.html、X发布稿.txt、公众号版 HTML），可随时重建
      参考/            其他环境写的同主题稿件和素材：参考-<环境>-<YYYYMMDD>.md，只作参考，永远不当源稿

多环境字段（可选，见 references/workspace.md「多环境协作」）：updated_at 写当前时间（ISO 8601，带时区），
updated_env / updated_by 用 --env / --by 填，不填就留空；每次改稿时更新这三项，新旧以 updated_at 为准。
subtitle 可以留空：填了的话 md2wechat 写进图片上传清单的「摘要」，md2x-html 在页顶预览里给出（都不进正文）。
刚建好的文件夹跑 check_article.py 应该只有 W5（封面还没做）。
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


def now_iso():
    """当前时间，ISO 8601 带时区（如 2026-10-18T17:00:00+08:00）。"""
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def frontmatter(title, date, tags, env="", by="", updated_at=None):
    tag_list = ", ".join(tags)
    return ("---\n"
            "title: %s\n"
            "subtitle: \n"
            "date: %s\n"
            "status: 草稿\n"
            "updated_at: %s\n"
            "updated_env: %s\n"
            "updated_by: %s\n"
            "tags: [%s]\n"
            "cover: cover/cover-1500x600.png\n"
            "---\n" % (title, date, updated_at or now_iso(), env, by, tag_list))


SKELETON_TPL = """# 骨架

动笔前先填，写完正文回头对一遍。判断方法见 references/information-design.md 第一、二节。不发布。

类型：记录 / 观点 / 教程 / 资讯 / 方法论 / 架构 / 对比 / 随笔（随笔可以整篇段落）
主要信息：（读者看完该知道什么，一两句）
读者：（谁、已经知道什么、为什么会看）
篇幅：约 ____ 字，__ 张图，__ 个表 / 列表

## 我的判断（必填）

3–5 条，每条写依据，以及读者大概会怎么反驳。全文的主线就是这几条判断，素材是给判断作证的。

| # | 判断 | 依据 | 读者会怎么反驳 |
|---|---|---|---|
| 1 | | | |

## 每节

「素材 / 判断」写这一节里两者的大致比例；一节全是素材，就是在罗列（脚本提示 I9）。

| 节 | 要点 | 形式 | 图表计划 | 素材 / 判断 | 字数 |
|---|---|---|---|---|---|
| 开头 | 结论 + 关键数字 | 段落 | — | 3 / 7 | 150 |
| | | | | | |
| 结尾 | | | | | |

## 自制图（方法论、架构、对比类至少 1 张）

| 图 | 讲什么 | 类型（架构 / 光谱 / 演进 / 流程） | 图源 |
|---|---|---|---|
| | | | raw/自制图源/xx.html |
"""


SOURCES_TPL = """# 素材来源

每张图、每个关键数字一行：用在哪、出处、取用日期。正文图片下方的「来源：」行从这里摘。

| 位置 | 内容 | 出处 | 日期 |
|---|---|---|---|
| images/01-xxx.png | | | |
"""


def scaffold(title, base, date=None, tags=None, env="", by=""):
    name = safe_name(title)
    if not name:
        raise ValueError("标题清洗后为空，换一个标题")
    root = os.path.join(base, name)
    if os.path.exists(root):
        raise FileExistsError("文件夹已存在，不覆盖：%s" % root)
    date = date or datetime.date.today().isoformat()
    tags = tags or []
    os.makedirs(root)
    for d in ("images", "cover", "raw", "out", "参考"):
        os.makedirs(os.path.join(root, d))
    md = os.path.join(root, name + ".md")
    with open(md, "w", encoding="utf-8") as f:
        f.write(frontmatter(name, date, tags, env, by))
        f.write("\n# %s\n\n" % name)
    with open(os.path.join(root, "骨架.md"), "w", encoding="utf-8") as f:
        f.write(SKELETON_TPL)
    with open(os.path.join(root, "素材来源.md"), "w", encoding="utf-8") as f:
        f.write(SOURCES_TPL)
    return root, md


def main():
    ap = argparse.ArgumentParser(description="新建长文文章文件夹（<文章名>/<文章名>.md 单源）")
    ap.add_argument("--title", required=True, help="文章标题，也是文件夹名和文件名")
    ap.add_argument("--base", default=".", help="在哪个目录下建（缺省当前目录）")
    ap.add_argument("--date", default=None, help="frontmatter date，缺省今天")
    ap.add_argument("--tags", default="", help="逗号分隔的标签")
    ap.add_argument("--env", default="", help="frontmatter updated_env：在哪个环境建的（如 主环境、本地），缺省留空")
    ap.add_argument("--by", default="", help="frontmatter updated_by：谁建的（如 agent、手动），缺省留空")
    args = ap.parse_args()
    tags = [t.strip() for t in re.split(r"[,，]", args.tags) if t.strip()]
    try:
        root, md = scaffold(args.title, args.base, args.date, tags, args.env, args.by)
    except (FileExistsError, ValueError) as e:
        print("错误：%s" % e, file=sys.stderr)
        return 1
    print("文章文件夹：%s" % root)
    print("源稿      ：%s" % md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
