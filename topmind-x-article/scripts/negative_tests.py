#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""topmind-x-article 异常输入测试：md2x.py 在各种坏输入下不崩溃（任一失败 → 退出码 1）。"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
MD2X = ROOT / "scripts" / "md2x.py"
PY = sys.executable
fails: list[str] = []


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([PY, str(MD2X), *args], capture_output=True, text=True, timeout=30)


def check(name: str, cond: bool, detail: str = "") -> None:
    print(("  ✓ " if cond else "  ✗ ") + name + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        fails.append(name)


def main() -> None:
    print("[negative_tests] topmind-x-article")
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)

        # 1. 空文件
        (td / "empty.md").write_text("", encoding="utf-8")
        r = run([str(td / "empty.md"), "--out", str(td / "o1.txt")])
        check("空文件不崩溃", r.returncode == 0 and "Traceback" not in r.stderr)

        # 2. 只有 frontmatter
        (td / "fm.md").write_text("---\ntitle: t\n---\n", encoding="utf-8")
        r = run([str(td / "fm.md"), "--out", str(td / "o2.txt")])
        check("纯 frontmatter 不崩溃", r.returncode == 0 and "Traceback" not in r.stderr)

        # 3. 未闭合代码围栏
        (td / "fence.md").write_text("# t\n\n```python\nprint(1)\n", encoding="utf-8")
        r = run([str(td / "fence.md"), "--out", str(td / "o3.txt")])
        check("未闭合围栏不崩溃", r.returncode == 0 and "Traceback" not in r.stderr)

        # 4. 无分隔行的表格
        (td / "tbl.md").write_text("# t\n\n| a | b |\n| 1 | 2 |\n", encoding="utf-8")
        r = run([str(td / "tbl.md"), "--out", str(td / "o4.txt")])
        check("异常表格不崩溃", r.returncode == 0 and "Traceback" not in r.stderr)

        # 5. 不存在的输入 → 非零退出且无 Traceback
        r = run([str(td / "nope.md"), "--out", str(td / "o5.txt")])
        check("缺失输入干净报错", r.returncode != 0 and "Traceback" not in r.stderr)

        # 6. 正常输入产出配图清单
        (td / "ok.md").write_text("# t\n\n![a](x.png)\n", encoding="utf-8")
        r = run([str(td / "ok.md"), "--out", str(td / "o6.txt")])
        out = (td / "o6.txt").read_text(encoding="utf-8") if (td / "o6.txt").exists() else ""
        check("正常输入含配图清单", r.returncode == 0 and "[图1]" in out)

        # 7. 嵌套围栏：```` 开栏不被内层 ``` 提前闭合（内层栏是代码内容）
        (td / "nest.md").write_text(
            "# t\n\n````markdown\n外层\n```python\nprint(1)\n```\n结束\n````\n",
            encoding="utf-8")
        r = run([str(td / "nest.md"), "--out", str(td / "o7.txt")])
        out = (td / "o7.txt").read_text(encoding="utf-8") if (td / "o7.txt").exists() else ""
        check("嵌套围栏不提前闭合",
              r.returncode == 0 and "    ```python" in out and "print(1)" in out)

        # 8. 括号 URL 链接不断裂（与 md2wechat 对齐的守卫）
        (td / "paren.md").write_text(
            "# t\n\n[维基](https://zh.wikipedia.org/wiki/猫_(动物))\n", encoding="utf-8")
        r = run([str(td / "paren.md"), "--out", str(td / "o8.txt")])
        out = (td / "o8.txt").read_text(encoding="utf-8") if (td / "o8.txt").exists() else ""
        check("括号 URL 不截断",
              r.returncode == 0 and "猫_(动物)" in out)

    if fails:
        print(f"\n[negative_tests] {len(fails)} 项失败")
        sys.exit(1)
    print("\n[negative_tests] 全部通过")


if __name__ == "__main__":
    main()
