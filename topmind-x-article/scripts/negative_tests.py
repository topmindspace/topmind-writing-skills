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

        # 9. 列表转 emoji 项目符号（X 纯文本不渲染 Markdown 列表），代码块内不动；--list-style keep 保留原符号
        (td / "lst.md").write_text(
            "# t\n\n- 一\n- 二\n  - 二点一\n    - 更深\n\n1. 步骤一\n2. 步骤二\n\n```\n- 代码里的\n```\n\n-5% 不是列表\n",
            encoding="utf-8")
        r = run([str(td / "lst.md"), "--out", str(td / "o9.txt")])
        out = (td / "o9.txt").read_text(encoding="utf-8") if (td / "o9.txt").exists() else ""
        check("列表默认 plain（「· 」「1）」，二级缩进两格）",
              r.returncode == 0 and "· 一" in out and "  · 二点一" in out and "  · 更深" in out
              and "1）步骤一" in out and "2）步骤二" in out and "🔹" not in out)
        r = run([str(td / "lst.md"), "--out", str(td / "o9e.txt"), "--list-style", "emoji"])
        oute = (td / "o9e.txt").read_text(encoding="utf-8") if (td / "o9e.txt").exists() else ""
        check("--list-style emoji 仍可用（两层缩进、序号 keycap）",
              r.returncode == 0 and "🔹 一" in oute and "  ▫️ 二点一" in oute and "  ▫️ 更深" in oute
              and "1️⃣ 步骤一" in oute and "2️⃣ 步骤二" in oute)
        check("代码块内的 - 不被改写、-5% 不被当列表",
              "    - 代码里的" in out and "-5% 不是列表" in out)
        r = run([str(td / "lst.md"), "--out", str(td / "o10.txt"), "--list-style", "keep"])
        out = (td / "o10.txt").read_text(encoding="utf-8") if (td / "o10.txt").exists() else ""
        check("--list-style keep 保留原符号", r.returncode == 0 and "- 一" in out and "1. 步骤一" in out)

        # 10. 文章文件夹结构：md2x / md2x-html 直接读 <文章名>.md，产物缺省进 out/
        import base64 as _b64
        png = _b64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk"
                             "+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==")
        art = td / "示例文章"
        for d in ("images", "cover", "out"):
            (art / d).mkdir(parents=True)
        (art / "images" / "01-first.png").write_bytes(png)
        (art / "images" / "02-second.png").write_bytes(png + b"\x00second")
        (art / "cover" / "cover-1500x600.png").write_bytes(png)
        (art / "示例文章.md").write_text(
            "---\ntitle: 示例文章\ndate: 2026-01-01\nstatus: 草稿\ntags: []\n"
            "cover: cover/cover-1500x600.png\n---\n\n# 示例文章\n\n开头。\n\n"
            "![第一张](images/01-first.png)\n\n来源：某官方文档\n\n中段。\n\n"
            "![第二张](images/02-second.png)\n\n```\n![代码里的](images/none.png)\n```\n",
            encoding="utf-8")
        html_script = ROOT / "scripts" / "md2x-html.py"
        r = subprocess.run([PY, str(html_script), str(art / "示例文章.md")],
                           capture_output=True, text=True, timeout=30)
        outp = art / "out" / "X长文.html"
        html = outp.read_text(encoding="utf-8") if outp.exists() else ""
        b1 = _b64.b64encode(png).decode()
        b2 = _b64.b64encode(png + b"\x00second").decode()
        check("md2x-html 直接读 ![]()，按文档顺序嵌图到 out/X长文.html",
              r.returncode == 0 and html.count('<figure class="ximg"') == 2
              and 0 <= html.find(b1) < html.find(b2), (r.stdout + r.stderr)[-300:])
        check("md2x-html「来源：」行成小号图注、代码块里的 ![]() 不动",
              '<p class="src">来源：某官方文档</p>' in html and "代码里的" in html)
        check("md2x-html 缺省读 frontmatter cover", "cover-1500x600" in html or html.count("data:image/png") == 3,
              str(html.count("data:image/png")))
        (art / "旧.md").write_text("# t\n\n[图1]\n", encoding="utf-8")
        r = subprocess.run([PY, str(html_script), str(art / "旧.md"), "--out", str(td / "x.html")],
                           capture_output=True, text=True, timeout=30)
        check("md2x-html 有 [图N] 却没给图片来源 → 干净报错",
              r.returncode != 0 and "--images-from" in r.stderr and "Traceback" not in r.stderr, r.stderr[-200:])
        r = run([str(art / "示例文章.md")])
        txt = art / "out" / "X发布稿.txt"
        check("md2x 缺省输出到 out/X发布稿.txt",
              r.returncode == 0 and txt.is_file() and "[图1]" in txt.read_text(encoding="utf-8"),
              (r.stdout + r.stderr)[-200:])
        r = subprocess.run([PY, str(ROOT / "scripts" / "check_article.py"), str(art)],
                           capture_output=True, text=True, timeout=30)
        check("check_article 示例文章结构通过", r.returncode == 0, r.stdout[-300:])

    if fails:
        print(f"\n[negative_tests] {len(fails)} 项失败")
        sys.exit(1)
    print("\n[negative_tests] 全部通过")


if __name__ == "__main__":
    main()
