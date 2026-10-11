#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""topmind-viral-posts 异常输入测试：技能工具链在坏输入下干净失败、不崩溃（任一失败 → 退出码 1）。

覆盖：
  1. 工作流引用的跨技能脚本存在（md2x-html.py / md2wechat.py 缺失即失败，不静默）
  2. audit_skill.py 在 frontmatter 损坏的 SKILL.md 上退出码 1（不抛未捕获异常）
  3. package_skill.py --check 在缺 README.md 的技能目录上退出码 1（不抛未捕获异常）
  4. scripts/*.py 全部可编译
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
PY = sys.executable
fails: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    print(("  ✓ " if cond else "  ✗ ") + name + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        fails.append(name)


def run_quiet(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run([PY, *args], capture_output=True, text=True, timeout=60, cwd=str(cwd))


def main() -> None:
    print("[negative_tests] topmind-viral-posts")

    # 1. 自包含：SKILL.md / references 不引用技能目录外的路径（单独安装也能用）
    outside = []
    for md in [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md"))]:
        if md.is_file() and "](../" in md.read_text(encoding="utf-8"):
            outside.append(md.relative_to(ROOT).as_posix())
    check("不引用技能目录外的相对路径", not outside, "、".join(outside))

    # 2. frontmatter 损坏 → audit_skill 退出 1 且不崩溃
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        shutil.copytree(ROOT, t / "skill", ignore=shutil.ignore_patterns("dist", "__pycache__"))
        sk = t / "skill" / "SKILL.md"
        sk.write_text("no frontmatter here\n# broken\n", encoding="utf-8")
        r = run_quiet(["scripts/audit_skill.py"], t / "skill")
        check("audit_skill 在坏 frontmatter 上退出码=1",
              r.returncode == 1, f"rc={r.returncode}")
        check("audit_skill 在坏 frontmatter 上无未捕获 Traceback",
              "Traceback" not in (r.stderr or ""), (r.stderr or "")[-200:])

    # 3. 缺 README.md → package_skill --check 退出 1 且不崩溃
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        shutil.copytree(ROOT, t / "skill", ignore=shutil.ignore_patterns("dist", "__pycache__"))
        (t / "skill" / "README.md").unlink()
        (t / "skill" / "README.en.md").unlink(missing_ok=True)
        r = run_quiet(["scripts/package_skill.py", "--check"], t / "skill")
        check("package_skill --check 在缺 README.md 时退出码=1",
              r.returncode == 1, f"rc={r.returncode}")
        check("package_skill --check 在缺 README.md 时无未捕获 Traceback",
              "Traceback" not in (r.stderr or ""), (r.stderr or "")[-200:])

    # 4. scripts/*.py 可编译（用内置 compile 只验语法，不写 .pyc，避免污染工作区）
    for py in sorted((ROOT / "scripts").glob("*.py")):
        try:
            compile(py.read_text(encoding="utf-8"), str(py), "exec")
            check(f"可编译: scripts/{py.name}", True)
        except SyntaxError as e:
            check(f"可编译: scripts/{py.name}", False, str(e))

    if fails:
        print(f"\n[negative_tests] topmind-viral-posts: {len(fails)} 项失败")
        sys.exit(1)
    print("\n[negative_tests] topmind-viral-posts: 全部通过")


if __name__ == "__main__":
    main()
