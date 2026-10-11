#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""topmind-cover 异常输入测试：crop-cover.py 错误路径干净（任一失败 → 退出码 1）。"""
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
CROP = ROOT / "scripts" / "crop-cover.py"
PY = sys.executable
fails: list[str] = []


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([PY, str(CROP), *args], capture_output=True, text=True, timeout=60)


def check(name: str, cond: bool, detail: str = "") -> None:
    print(("  ✓ " if cond else "  ✗ ") + name + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        fails.append(name)


def main() -> None:
    print("[negative_tests] topmind-cover")
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)

        # 1. 缺失输入 → 非零退出，无 Traceback
        r = run([str(td / "nope.png"), "--out-dir", str(td / "o1")])
        check("缺失输入干净报错", r.returncode != 0 and "Traceback" not in r.stderr, r.stderr[:100])

        # 2. 非图片文件 → 非零退出，无 Traceback
        (td / "notimg.txt").write_text("hello", encoding="utf-8")
        r = run([str(td / "notimg.txt"), "--out-dir", str(td / "o2")])
        check("非图片干净报错", r.returncode != 0 and "Traceback" not in r.stderr, r.stderr[:100])

        # 3. 正常图片产出双尺寸
        try:
            from PIL import Image
            img = Image.new("RGB", (1600, 900), (20, 30, 60))
            img.save(td / "ok.png")
            r = run([str(td / "ok.png"), "--out-dir", str(td / "o3")])
            got_a = (td / "o3" / "00-封面.png").exists()
            got_b = (td / "o3" / "00-封面-公众号.png").exists()
            check("正常图片产出双尺寸", r.returncode == 0 and got_a and got_b, r.stderr[:100])
            if got_a:
                w, h = Image.open(td / "o3" / "00-封面.png").size
                check("主图 1500×600", (w, h) == (1500, 600), f"实 {w}×{h}")
            if got_b:
                w, h = Image.open(td / "o3" / "00-封面-公众号.png").size
                check("公众号图 900×383", (w, h) == (900, 383), f"实 {w}×{h}")
        except ImportError:
            print("  - 跳过图片生成测试（无 Pillow）")

    if fails:
        print(f"\n[negative_tests] {len(fails)} 项失败")
        sys.exit(1)
    print("\n[negative_tests] 全部通过")


if __name__ == "__main__":
    main()
