#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""样式资产审计：主题/风格资源有效性（任一不过 → 退出码 1）。

本组技能无 CSS 样式表：若存在 assets/themes/*.json 则校验 JSON 可解析；
references 风格文档非空（已由 audit_docs 覆盖，此处做存在性断言）。
"""
from __future__ import annotations

import json
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
    print(f"[audit_styles] {NAME}")
    themes = sorted((ROOT / "assets" / "themes").glob("*.json")) if (ROOT / "assets" / "themes").is_dir() else []
    if themes:
        for t in themes:
            try:
                json.loads(t.read_text(encoding="utf-8"))
                check(True, f"assets/themes/{t.name} JSON 可解析")
            except (OSError, json.JSONDecodeError) as e:
                check(False, f"assets/themes/{t.name} 解析失败: {e}")
    else:
        check(True, "无主题 JSON 资产（本技能不依赖主题文件）")

    refdir = ROOT / "references"
    has_style_doc = refdir.is_dir() and any(refdir.glob("*.md"))
    check(has_style_doc, "references 风格/格式文档存在")

    if errors:
        print(f"\n[audit_styles] {NAME}: {len(errors)} 项失败")
        sys.exit(1)
    print(f"\n[audit_styles] {NAME}: 全部通过")


if __name__ == "__main__":
    main()
