#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文档审计：references 完整性与内部链接可达性（任一不过 → 退出码 1）。"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
NAME = ROOT.name
errors: list[str] = []


def check(cond: bool, msg: str) -> None:
    print(("  ✓ " if cond else "  ✗ ") + msg)
    if not cond:
        errors.append(msg)


def main() -> None:
    print(f"[audit_docs] {NAME}")
    md_files = [p for p in ROOT.rglob("*.md") if ".git" not in p.parts and "dist" not in p.parts]
    check(len(md_files) >= 2, f"md 文档 ≥2（实 {len(md_files)}，含 SKILL.md/README.md）")

    refdir = ROOT / "references"
    if refdir.is_dir():
        refs = sorted(refdir.glob("*.md"))
        check(len(refs) >= 1, f"references/*.md ≥1（实 {len(refs)}）")
        for md in refs:
            check(md.stat().st_size > 0, f"references/{md.name} 非空")

    for md in md_files:
        text = md.read_text(encoding="utf-8")
        rel = md.relative_to(ROOT).as_posix()
        for link in set(re.findall(r"\]\(([^)]+)\)", text)):
            if link.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = (md.parent / link.split("#")[0]).resolve()
            if link and not target.exists():
                # 允许指向脚本/资源等非 md 文件的相对链接缺失检查放宽到 md
                if target.suffix == ".md":
                    check(False, f"{rel} 悬空链接: {link}")
    check(True, "内部 md 链接可达")

    # 反引号代码引用中的路径可达（审计 轻微-15 门禁盲区：之前只查 [text](path) 形式，
    # `references/pan-style.md` 这类反引号引用曾漏网）。抓取反引号内的 references/*.md
    # 与 scripts/* 路径并校验存在；glob/占位符写法（* ? < > |）跳过。
    backtick_path_re = re.compile(r"(references|scripts)/([\w.\-/]+)")
    line_suffix_re = re.compile(r":\d+(?:-\d+)?$")
    backtick_bad = 0
    for md in md_files:
        text = md.read_text(encoding="utf-8")
        rel = md.relative_to(ROOT).as_posix()
        for span in set(re.findall(r"`([^`]+)`", text)):
            for kind, p in backtick_path_re.findall(span):
                p = line_suffix_re.sub("", p)
                if not p or any(c in p for c in "*?<>|"):
                    continue
                target = md.parent / kind / p
                if not target.exists():
                    target = ROOT / kind / p
                if not target.exists():
                    backtick_bad += 1
                    check(False, f"{rel} 反引号引用不可达: `{kind}/{p}`")
    check(backtick_bad == 0, f"反引号内 references/scripts 引用可达（扫描 {len(md_files)} 个 md 文件）")

    if errors:
        print(f"\n[audit_docs] {NAME}: {len(errors)} 项失败")
        sys.exit(1)
    print(f"\n[audit_docs] {NAME}: 全部通过")


if __name__ == "__main__":
    main()
