#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""topmind-poster 异常输入测试：工具链在坏输入下干净失败、不崩溃（任一失败 → 退出码 1）。

覆盖：
  1. render_poster.py 对不存在的输入文件干净失败（不抛未捕获 Traceback）
  2. render_poster.py 对不存在的浏览器路径干净失败
  3. audit_skill.py 在 frontmatter 损坏的 SKILL.md 上退出码 1（不崩溃）
  4. package_skill.py --check 在缺 README.md 的技能目录上退出码 1（不崩溃）
  5. scripts/*.py 全部可编译
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
PY = sys.executable
fails: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    print(("  ✓ " if cond else "  ✗ ") + name + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        fails.append(name)


def run_quiet(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run([PY, *args], capture_output=True, text=True, timeout=120, cwd=str(cwd))


def main() -> None:
    print("[negative_tests] topmind-poster")

    # 1. 不存在的输入文件 → 干净失败（rc=0 但明确提示未渲染，或 rc=1；都不许有 Traceback）
    r = run_quiet(
        ["scripts/render_poster.py", "no-such-file.html", "-o", "out.png"],
        ROOT,
    )
    check(
        "render_poster 对缺失输入不抛 Traceback",
        "Traceback" not in (r.stderr or ""),
        (r.stderr or "")[-200:],
    )
    check(
        "render_poster 对缺失输入给出提示",
        "找不到" in (r.stdout or "") or "1/" in (r.stdout or ""),
        (r.stdout or "")[-200:],
    )

    # 2. 不存在的浏览器路径 → 干净失败
    r = run_quiet(
        ["scripts/render_poster.py", str(ROOT / "SKILL.md"), "-o", "out.png",
         "--chrome", "/no/such/chrome"],
        ROOT,
    )
    check(
        "render_poster 对坏浏览器路径不抛 Traceback",
        "Traceback" not in (r.stderr or ""),
        (r.stderr or "")[-200:],
    )
    check(
        "render_poster 对坏浏览器路径退出码=1",
        r.returncode == 1,
        f"rc={r.returncode}",
    )

    # 3. 参数互斥校验：多输入缺 --out-dir
    r = run_quiet(
        ["scripts/render_poster.py", "a.html", "b.html"],
        ROOT,
    )
    check(
        "render_poster 多输入缺 --out-dir 时退出码=1",
        r.returncode == 1,
        f"rc={r.returncode}",
    )

    # 4. frontmatter 损坏 → audit_skill 退出 1 且不崩溃
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        shutil.copytree(ROOT, t / "skill", ignore=shutil.ignore_patterns("dist", "__pycache__"))
        sk = t / "skill" / "SKILL.md"
        sk.write_text("no frontmatter here\n# broken\n", encoding="utf-8")
        r = run_quiet(["scripts/audit_skill.py"], t / "skill")
        check("audit_skill 在坏 frontmatter 上退出码=1", r.returncode == 1, f"rc={r.returncode}")
        check(
            "audit_skill 在坏 frontmatter 上无未捕获 Traceback",
            "Traceback" not in (r.stderr or ""),
            (r.stderr or "")[-200:],
        )

    # 5. 缺 README.md → package_skill --check 退出 1 且不崩溃
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        shutil.copytree(ROOT, t / "skill", ignore=shutil.ignore_patterns("dist", "__pycache__"))
        (t / "skill" / "README.md").unlink()
        (t / "skill" / "README.en.md").unlink(missing_ok=True)
        r = run_quiet(["scripts/package_skill.py", "--check"], t / "skill")
        check("package_skill --check 在缺 README.md 时退出码=1", r.returncode == 1, f"rc={r.returncode}")
        check(
            "package_skill --check 在缺 README.md 时无未捕获 Traceback",
            "Traceback" not in (r.stderr or ""),
            (r.stderr or "")[-200:],
        )

    # 6. scripts/*.py 可编译（只验语法，不写 .pyc）
    for py in sorted((ROOT / "scripts").glob("*.py")):
        try:
            compile(py.read_text(encoding="utf-8"), str(py), "exec")
            check(f"可编译: scripts/{py.name}", True)
        except SyntaxError as e:
            check(f"可编译: scripts/{py.name}", False, str(e))

    if fails:
        print(f"\n[negative_tests] topmind-poster: {len(fails)} 项失败")
        sys.exit(1)
    print("\n[negative_tests] topmind-poster: 全部通过")


if __name__ == "__main__":
    main()
