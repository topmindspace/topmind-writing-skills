#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""new-article.py — 一键创建公众号文章交付包。

创建 <base>/YYYY-MM-DD-<slug>/ 目录，内含：
  - 公众号稿.md   带 frontmatter 的文章骨架（含写作提示与容器语法示例）
  - images/       图片目录（可选，从 --images 拷贝）
  - diagrams/     mermaid 图表目录

Usage:
    python3 new-article.py --slug gpt-6-review --title "GPT-6 深度评测" \
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

from wechat_paths import require_base, resolve_topstream  # 同目录模块：路径解析不写死个人路径/编号/年份

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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True,
                    help="包名关键词（中文短名，可含英文/数字/连字符），如 个人免费基建全景、GrokBot多Agent调度")
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
    print("  稿件骨架 : 公众号稿.md（含容器语法示例，写作时删掉注释）")
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
