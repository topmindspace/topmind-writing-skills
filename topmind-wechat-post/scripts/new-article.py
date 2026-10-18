#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""new-article.py — 一键创建长文文章文件夹（默认新结构）。

默认（新结构，单源）：调用 article_scaffold.py，创建 <base>/<文章名>/：
  - <文章名>.md   唯一源稿（frontmatter：title/date/status/tags/cover，可选 direction/source_file/target_file）
  - images/ cover/ raw/ out/ 与 素材来源.md
  公众号 HTML、X 长文 HTML、X 发布稿都从这一份源稿按需派生到 out/。

--legacy（旧结构，兼容老专题）：创建 <base>/YYYY-MM-DD-<slug>/ 交付包，内含公众号稿.md、images/、diagrams/。

Usage:
    python3 new-article.py --title "GPT-6 深度评测" [--base <专题目录>] [--tags AI,评测] [--images a.png b.png]
    python3 new-article.py --legacy --slug gpt-6-review --title "GPT-6 深度评测" \
        [--base <专题目录>] [--workspace <工作区>] [--date YYYY-MM-DD] [--images src1 src2 ...]

默认 base 见 wechat_paths.py：--base → TOPMIND_WECHAT_BASE → 工作区里按名称发现的
「长文/创作/专题」类别 + `{当年}-公众号`。解析不到就报错，不猜路径。
"""

import argparse
import datetime
import os
import re
import shutil
import sys

sys.dont_write_bytecode = True  # 同目录模块互相 import，不在技能目录里留 __pycache__

from wechat_paths import require_base, resolve_topstream  # 同目录模块：路径解析不写死个人路径/编号/年份
import article_scaffold  # 同目录模块（shared/scripts 副本）：新结构文章文件夹

BODY_HINTS = """
<!-- 骨架说明（写作时逐条删除）：
  1. 开头 3 句内给出一个具体事实、数字或场景，别写背景铺垫。
  2. 小标题用 ##；想要序号就直接写「一、」「二、」，排版脚本原样保留，不再自动编号。
  3. 正文段落不超过 110 字；重点句才加粗，加粗占比 < 20%。
  4. 图片写 ![说明](images/01-xxx.png)，按出现顺序编号；出处写在图片下一行「来源：……」。
  5. 不用 ::: 容器、callout、![[ ]]：源稿要能被任何 Markdown 工具读。
  6. 外链直接写 [文字](url)，生成公众号版时自动转文末脚注。
  7. 写完先跑 topmind-revise（三道门），再按需派生公众号 / X 版本到 out/。
-->
"""

SKELETON = """---
title: "{title}"
category: {category}
topic: {topic}
source_type: {source_type}
captured_at: {now}
status: 草稿
direction: {direction}
source_file: {source_file}
target_file: {target_file}
word_count: 0
tags: [公众号, 排版]
note_role: bundle
---

# {title}

<!-- 骨架说明（写作时逐条删除）：
  1. 开头：3 句内给出「反差钩子」——一个具体事实/数字/场景，别写背景铺垫。
  2. 小标题用 ##（h2），正文段落 ≤ 110 字（约 4 行手机屏）。
  3. 重点句才加粗，加粗占比 < 20%；关键数据可用 ::: stat 容器。
  4. 外链会被公众号拦截，直接写 [文字](url)，脚本自动转文末脚注。
  5. 中英文间距不用管，lint --fix 会自动补。
  6. 可用容器（::: 类型 然后空行，内容，空行，::: 收尾）：
       ::: note   补充说明（灰）
       ::: tip    小技巧（绿）
       ::: warn   注意事项（橙）
       ::: danger 常见坑（红）
       ::: pull   金句 / 核心观点（大字号居中）
       ::: dialogue  对话（A: B: 交替缩进）
       ::: stat   数据亮点（大数字）
       [!新特性] 这样的行内徽章  /  ==高亮重点==
-->

> 一句话导语：这篇文章解决什么问题、读者能带走什么。

## 为什么值得聊

## 核心内容

### 分论点一

### 分论点二

## 我的看法

::: pull
把最想让读者记住的一句话放在这里。
:::

## 小结

---

*本文首发于我的公众号，转载请注明出处。*
"""

# 目录名按专题规范：中文短名（可含英文/数字/连字符），如 个人免费基建全景、GrokBot多Agent调度
SLUG_RE = re.compile(r"^[\u4e00-\u9fffA-Za-z0-9][\u4e00-\u9fffA-Za-z0-9-]*$")


def new_layout(args):
    tags = [t.strip() for t in re.split(r"[,，]", args.tags) if t.strip()]
    try:
        root, md = article_scaffold.scaffold(args.title, args.base, args.date, tags)
    except (FileExistsError, ValueError) as e:
        print("✗ %s" % e)
        return 1
    text = open(md, encoding="utf-8").read()
    # 对接 topstream 时才写的可选字段，插在 frontmatter 结尾前
    if args.direction == "forward" or args.source_file:
        extra = "direction: %s\nsource_file: %s\ntarget_file: %s\n" % (
            args.direction, args.source_file or '""',
            '""' if args.direction == "forward" else "pending")
        head, sep, rest = text.partition("\n---\n")
        text = head + "\n" + extra.rstrip("\n") + sep + rest
    text = text.rstrip("\n") + "\n" + BODY_HINTS
    with open(md, "w", encoding="utf-8") as fh:
        fh.write(text)

    copied = 0
    for src in args.images:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(root, "images", os.path.basename(src)))
            copied += 1
        else:
            print("! 跳过不存在的图片：%s" % src)

    here = os.path.dirname(os.path.abspath(__file__))
    print("✓ 文章文件夹已创建：%s" % root)
    print("  源稿     : %s" % os.path.basename(md))
    if copied:
        print("  图片     : %d 张 → images/（按正文出现顺序改名 01-、02-…）" % copied)
    print("")
    print("下一步：")
    print("  1. 写完先过结构与改稿检查：")
    print("     python3 %s/check_article.py '%s'" % (here, md))
    print("     python3 %s/lint-wechat.py --input '%s' --fix" % (here, md))
    print("  2. 生成公众号 HTML（产物进 out/）：")
    print("     python3 %s/md2wechat.py --input '%s' --embed-images" % (here, md))
    print("  3. 定稿时改 frontmatter 的 status（目录名不变）：")
    print("     python3 %s/sync-status.py --set 定稿 '%s' --apply" % (here, root))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--legacy", action="store_true",
                    help="用旧结构 YYYY-MM-DD-<slug>/公众号稿.md（老专题兼容）；缺省用新结构 <文章名>/<文章名>.md")
    ap.add_argument("--slug", default="",
                    help="仅 --legacy：包名关键词（中文短名，可含英文/数字/连字符）")
    ap.add_argument("--tags", default="", help="新结构：逗号分隔的标签")
    ap.add_argument("--title", required=True, help="文章标题")
    ap.add_argument("--base", default=None, help="交付包根（专题目录）；缺省按 wechat_paths.py 规则解析")
    ap.add_argument("--workspace", default=None, help="topmind 工作区根（缺省读 TOPMIND_WORKSPACE）")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--direction", default="reverse", choices=("forward", "reverse"),
                    help="forward=源自 topstream 底稿；reverse=本工作区选题，定稿后回推 topstream")
    ap.add_argument("--source-file", default="",
                    help='forward 时填 topstream 的 notes/xxx.md')
    ap.add_argument("--images", nargs="*", default=[],
                    help="要拷入 images/ 的源图片路径")
    args = ap.parse_args()
    args.base = require_base(args.base, args.workspace)

    if not args.legacy:
        return new_layout(args)

    if not args.slug:
        print("✗ --legacy 需要 --slug")
        return 1
    if not SLUG_RE.match(args.slug):
        print("✗ 目录名只允许中文、英文字母、数字、连字符：%s" % args.slug)
        return 1

    pkg = os.path.join(args.base, "%s-%s" % (args.date, args.slug))
    if os.path.exists(pkg):
        print("✗ 目录已存在：%s" % pkg)
        return 1

    os.makedirs(os.path.join(pkg, "images"), exist_ok=True)
    os.makedirs(os.path.join(pkg, "diagrams"), exist_ok=True)

    draft = os.path.join(pkg, "公众号稿.md")
    if args.direction == "forward" and not args.source_file:
        print("⚠ forward 未给 --source-file，将留空 source_file（回补 notes/xxx.md）")
    src_file = args.source_file or '""'
    tgt_file = '""' if args.direction == "forward" else "pending"
    with open(draft, "w", encoding="utf-8") as fh:
        fh.write(SKELETON.format(
            title=args.title,
            source_type="user-original" if args.direction == "reverse" else "ai-derived",
            direction=args.direction,
            source_file=src_file,
            target_file=tgt_file,
            # category / topic 取交付包根的实际目录名（不写死编号与年份）
            category=os.path.basename(os.path.dirname(os.path.abspath(args.base))),
            topic=os.path.basename(os.path.abspath(args.base)),
            now=datetime.datetime.now().astimezone().isoformat(timespec="seconds")))

    copied = 0
    for src in args.images:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(pkg, "images", os.path.basename(src)))
            copied += 1
        else:
            print("! 跳过不存在的图片：%s" % src)

    print("✓ 交付包已创建：%s" % pkg)
    print("  稿件骨架 : 公众号稿.md（旧结构，含容器语法示例，写作时删掉注释）")
    if copied:
        print("  图片     : %d 张 → images/" % copied)
    print("")
    print("下一步：")
    print("  1. 写完稿后体检（可加 --fix 自动补中英文间距）：")
    print("     python3 %s/lint-wechat.py --input '%s' --fix" % (
        os.path.dirname(os.path.abspath(__file__)), draft))
    print("  2. 定稿时同步状态与目录名（加 --apply 生效）：")
    print("     python3 %s/sync-status.py --set 定稿 '%s' --apply" % (
        os.path.dirname(os.path.abspath(__file__)), os.path.basename(pkg)))
    print("  3. 生成公众号 HTML：")
    print("     python3 %s/md2wechat.py --input '%s' --out-dir '%s' --slug %s" % (
        os.path.dirname(os.path.abspath(__file__)), draft, pkg, args.slug))
    return 0


if __name__ == "__main__":
    sys.exit(main())
