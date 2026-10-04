#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CSS 审计：本组技能无 CSS 资产；若未来加入 .css 文件，则做括号配平基础检查。"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
NAME = ROOT.name
errors: list[str] = []


def main() -> None:
    print(f"[audit_css] {NAME}")
    css_files = [p for p in ROOT.rglob("*.css") if ".git" not in p.parts and "dist" not in p.parts]
    if not css_files:
        print("  ✓ 无 CSS 资产，跳过")
        print(f"\n[audit_css] {NAME}: 通过")
        return
    for css in css_files:
        text = css.read_text(encoding="utf-8")
        balanced = text.count("{") == text.count("}")
        print(("  ✓ " if balanced else "  ✗ ") + f"{css.name} 括号配平")
        if not balanced:
            errors.append(css.name)
    if errors:
        print(f"\n[audit_css] {NAME}: {len(errors)} 项失败")
        sys.exit(1)
    print(f"\n[audit_css] {NAME}: 全部通过")


if __name__ == "__main__":
    main()
