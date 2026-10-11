#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sync-mapping.py — 校验「frontmatter ⇄ 目录名 ⇄ topstream 文件 ⇄ 派生视图」映射一致性。

frontmatter 是映射唯一真源，topic.md 与 topstream `docs/公众号映射.md` 是派生视图。
派生视图靠手改，容易与真源漂移。本脚本只读校验，报告差异，不改文件。

Usage:
    python3 sync-mapping.py                          # 校验全部包（dry-run）
    python3 sync-mapping.py --topstream <path>       # 额外校验 notes 文件是否存在
    python3 sync-mapping.py --check-topic <topic.md> # 校验 topic.md 总表是否与磁盘一致
    python3 sync-mapping.py --apply                  # 刷新 word_count（仅这一项可自动修）
"""

import argparse
import os
import re
import sys

from wechat_paths import require_base, resolve_topstream  # 同目录模块：路径解析不写死个人路径/编号/年份

VALID_STATUSES = ("草稿", "定稿", "已发布")
FINAL_STATUSES = ("定稿", "已发布")
RELEASED_SUFFIX = "-released"
DIR_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-([\u4e00-\u9fffA-Za-z0-9][\u4e00-\u9fffA-Za-z0-9-]*?)(-released)?$")


def split_fm(text):
    if not text.startswith("---\n"):
        return None, text
    i = text.find("\n---", 3)
    if i < 0:
        return None, text
    return text[4:i], text[i + 4:].lstrip("\n")


def get_field(fm, key):
    m = re.search(r"^%s:\s*(.*)$" % re.escape(key), fm, re.M)
    if not m:
        return None
    v = m.group(1).strip()
    if v in ("", '""', "''"):
        return ""
    return v.strip('"').strip("'")


def cjk_count(body):
    return len(re.findall(r"[\u4e00-\u9fff]", body))


def collect(base):
    """返回 [(dirname, pkg_path, fm, body)]"""
    out = []
    if not os.path.isdir(base):
        return out
    for name in sorted(os.listdir(base)):
        pkg = os.path.join(base, name)
        draft = os.path.join(pkg, "公众号稿.md")
        if not os.path.isdir(pkg) or not os.path.exists(draft):
            continue
        text = open(draft, encoding="utf-8").read()
        fm, body = split_fm(text)
        out.append((name, pkg, fm, body))
    return out


def check(base, topstream, check_topic):
    rows = collect(base)
    if not rows:
        print("✗ 专题下没有交付包：%s" % base)
        return 1

    errors, warns = [], []

    for name, pkg, fm, body in rows:
        tag = "[" + name + "]"
        if fm is None:
            errors.append("%s 无 frontmatter" % tag)
            continue

        direction = get_field(fm, "direction") or ""
        status = get_field(fm, "status") or "草稿"
        source_file = get_field(fm, "source_file") or ""
        target_file = get_field(fm, "target_file") or ""
        wc = get_field(fm, "word_count")

        # 字段完备性
        if direction not in ("forward", "reverse"):
            errors.append("%s direction 非法：%r（应为 forward/reverse）" % (tag, direction))
        if status not in VALID_STATUSES:
            errors.append("%s status 非法：%r" % (tag, status))

        if direction == "forward" and not source_file:
            errors.append("%s 是 forward 但缺 source_file（应填 notes/xxx.md）" % tag)
        if direction == "reverse" and target_file == "":
            errors.append("%s 是 reverse 但 target_file 为空（应为 pending 或 notes/xxx.md）" % tag)
        if direction == "forward" and source_file and not source_file.startswith("notes/"):
            warns.append("%s source_file 应以 notes/ 开头：%s" % (tag, source_file))

        # 目录名与状态
        m = DIR_RE.match(name)
        if not m:
            errors.append("%s 目录名不符合 YYYY-MM-DD-<短名>[-released]：%s" % (tag, name))
        else:
            has_sfx = name.endswith(RELEASED_SUFFIX)
            if status in FINAL_STATUSES and not has_sfx:
                errors.append("%s status=%s 但目录缺 -released 后缀（用 sync-status.py --set 修）"
                              % (tag, status))
            if status == "草稿" and has_sfx:
                errors.append("%s status=草稿 但目录带 -released 后缀" % tag)

        # 字数是否落盘最新
        cn = cjk_count(body)
        if wc and wc.isdigit() and int(wc) != cn:
            warns.append("%s word_count=%s 与实际中文字 %d 不一致（sync-status.py --apply 刷新）"
                         % (tag, wc, cn))

        # topstream 文件存在性
        if topstream:
            for field, rel in (("source_file", source_file), ("target_file", target_file)):
                if rel and rel not in ("pending", "") and rel.startswith("notes/"):
                    p = os.path.join(topstream, rel)
                    if not os.path.exists(p):
                        errors.append("%s %s 指向不存在的文件：%s" % (tag, field, rel))

    # 派生视图漂移：topic.md 总表里的目录名应与磁盘集合一致
    if check_topic:
        if not os.path.exists(check_topic):
            errors.append("topic.md 不存在：%s" % check_topic)
        else:
            topic = open(check_topic, encoding="utf-8").read()
            listed = set()
            for x in re.findall(r"`(\d{4}-\d{2}-\d{2}-[^`]+?/)`", topic):
                m = DIR_RE.match(x.rstrip("/"))
                if m:
                    listed.add(m.group(0))
            on_disk = set(n for n, _, _, _ in rows)          # 文章包（含 公众号稿.md）
            on_disk_all = set(n for n in os.listdir(base)
                              if os.path.isdir(os.path.join(base, n)))  # 含策划包等
            missing_in_topic = on_disk - listed
            stale_in_topic = listed - on_disk_all
            if missing_in_topic:
                warns.append("磁盘有但 topic.md 总表未列出：%s" % "、".join(sorted(missing_in_topic)))
            if stale_in_topic:
                warns.append("topic.md 总表列了但磁盘不存在：%s" % "、".join(sorted(stale_in_topic)))

    # 输出
    print("映射校验：%s" % base)
    print("-" * 80)
    for name, pkg, fm, body in rows:
        if fm is None:
            continue
        d = get_field(fm, "direction")
        s = get_field(fm, "status")
        sf = get_field(fm, "source_file") or "-"
        tf = get_field(fm, "target_file") or "-"
        print("%-40s %-8s %-4s src=%-28s tgt=%s" % (name, d, s, sf[:28], tf[:28]))
    print("-" * 80)
    if errors:
        print("错误 %d：" % len(errors))
        for e in errors:
            print("  ✗ %s" % e)
        print("")
    if warns:
        print("警告 %d：" % len(warns))
        for w in warns:
            print("  ! %s" % w)
        print("")
    if not errors and not warns:
        print("✓ 映射一致，无差异")
    return 1 if errors else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=None, help="交付包根（专题目录）；缺省按 wechat_paths.py 规则解析")
    ap.add_argument("--workspace", default=None, help="topmind 工作区根（缺省读 TOPMIND_WORKSPACE）")
    ap.add_argument("--topstream", default=None,
        help="topstream 仓库路径（默认 TOPSTREAM_ROOT；都没有则跳过 notes 校验）")
    ap.add_argument("--check-topic", default=None,
        help="topic.md 路径，校验总表是否与磁盘一致（默认 <base>/topic.md）")
    ap.add_argument("--no-topstream", action="store_true", help="不校验 topstream")
    ap.add_argument("--no-topic", action="store_true", help="不校验 topic.md")
    args = ap.parse_args()
    args.base = require_base(args.base, args.workspace)

    topstream = None if args.no_topstream else resolve_topstream(args.topstream)
    check_topic = None if args.no_topic else (args.check_topic or os.path.join(args.base, "topic.md"))
    return check(args.base, topstream, check_topic)


if __name__ == "__main__":
    sys.exit(main())
