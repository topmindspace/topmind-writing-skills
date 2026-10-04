#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""技能入口审计：SKILL.md 结构完整性（任一不过 → 退出码 1）。"""
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
    print(f"[audit_skill] {NAME}")
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")

    m = re.search(r"^triggers:\s*\n((?:  - .+\n?)+)", text, re.M)
    triggers = re.findall(r"^  - (.+)$", m.group(1), re.M) if m else []
    check(len(triggers) >= 1, f"triggers ≥1（实 {len(triggers)}）")

    check("When NOT to use" in text or "何时不用" in text, "含 When NOT to use / 何时不用")

    has_workflow = bool(re.search(r"工作流|Workflow|用法|Usage", text))
    check(has_workflow, "含工作流/用法说明")

    fm = re.match(r"^---\r?\n([\s\S]*?)\r?\n---", text)
    desc = ""
    if fm:
        dm = re.search(r'^description:\s*"([^"]*)"\s*$', fm.group(1), re.M)
        if dm:
            desc = dm.group(1).strip()
        else:
            dm = re.search(r"^description:\s*>\-\s*\n((?:[ \t]+.*\n?)+)", fm.group(1), re.M)
            if dm:
                desc = " ".join(l.strip() for l in dm.group(1).splitlines())
    check("Use when" in desc or "用" in desc, "description 含使用场景")
    check("Do NOT use" in desc or "不用" in desc, "description 含不适用场景")
    check(len(desc) <= 1024, f"description ≤1024（实 {len(desc)}）")

    if errors:
        print(f"\n[audit_skill] {NAME}: {len(errors)} 项失败")
        sys.exit(1)
    print(f"\n[audit_skill] {NAME}: 全部通过")


if __name__ == "__main__":
    main()
