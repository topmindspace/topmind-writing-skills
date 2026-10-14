#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""topmind-format 异常输入测试：技能工具链在坏输入下干净失败、不崩溃（任一失败 → 退出码 1）。

覆盖：
  1. 工作流引用的跨技能脚本存在（md2x-html.py / md2wechat.py 缺失即失败，不静默）
  2. audit_skill.py 在 frontmatter 损坏的 SKILL.md 上退出码 1（不抛未捕获异常）
  3. package_skill.py --check 在缺 README.md 的技能目录上退出码 1（不抛未捕获异常）
  4. format_text.py：段子体行间空行、短文体 emoji 列表、保真校验、坏输入干净报错
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
    print("[negative_tests] topmind-format")

    # 1. 自包含：SKILL.md / references 不引用技能目录外的路径（单独安装也能用）
    outside = []
    for md in [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md"))]:
        if md.is_file() and "](../" in md.read_text(encoding="utf-8"):
            outside.append(md.relative_to(ROOT).as_posix())
    check("不引用技能目录外的相对路径", not outside, "、".join(outside))

    # 1b. 共享版式文档随包自带（emoji 体系唯一真源 + 参考帖版式规律）
    for ref in ("emoji-system.md", "x-post-format.md", "x-layout-patterns.md", "x-delivery-contract.md"):
        check(f"共享文档随包自带: references/{ref}", (ROOT / "references" / ref).is_file())

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

    # 3b. X 稿检查脚本随包自带：Markdown 列表 → 失败；emoji 列表 → 通过；--fix 后通过；公众号稿不受影响
    lint = ROOT / "scripts" / "lint_x_post.py"
    check("X 稿检查脚本随包自带: scripts/lint_x_post.py", lint.is_file())
    if lint.is_file():
        with tempfile.TemporaryDirectory() as td:
            t = Path(td)
            bad = t / "bad.txt"
            bad.write_text("三个变化：\n\n- 响应更快\n- 价格更低\n1. 先装\n## 标题\n**加粗**\n\n#话题\n", encoding="utf-8")
            good = t / "good.txt"
            good.write_text("三个变化：\n\n🔹 响应更快\n🔹 价格更低\n  ▫️ 细节\n\n1️⃣ 先装\n2️⃣ 再用\n\n#话题\n", encoding="utf-8")
            r = run_quiet([str(lint), str(bad)], t)
            check("lint_x_post 对 Markdown 列表/标题/加粗退出码=1", r.returncode == 1, f"rc={r.returncode}")
            r = run_quiet([str(lint), str(good)], t)
            check("lint_x_post 对 emoji 列表退出码=0", r.returncode == 0, r.stdout[-200:])
            r = run_quiet([str(lint), str(bad), "--fix", "--out", str(t / "fixed.txt")], t)
            fixed = (t / "fixed.txt").read_text(encoding="utf-8") if (t / "fixed.txt").exists() else ""
            check("lint_x_post --fix 后无 Markdown 列表且检查通过",
                  r.returncode == 0 and "🔹 响应更快" in fixed and "1️⃣ 先装" in fixed and "**" not in fixed, r.stdout[-200:])
            resid = t / "resid.txt"
            resid.write_text("```text\n标题\n\n\n~~旧价~~ 新价\n```\n", encoding="utf-8")
            r = run_quiet([str(lint), str(resid)], t)
            check("lint_x_post 对代码围栏/删除线残留报 E8/E9、连续空行报 W11",
                  r.returncode == 1 and "[E8]" in r.stdout and "[E9]" in r.stdout and "[W11]" in r.stdout, r.stdout[-300:])
            r = run_quiet([str(lint), str(resid), "--fix", "--out", str(t / "resid.fixed.txt")], t)
            rf = (t / "resid.fixed.txt").read_text(encoding="utf-8") if (t / "resid.fixed.txt").exists() else ""
            check("lint_x_post --fix 去掉围栏与删除线", "```" not in rf and "~~" not in rf and "旧价 新价" in rf, rf[-200:])
            mix = t / "mix.txt"
            mix.write_text("三步：\n\n🔹 回评论\n\n🔹 发原创\n\n#日拱一卒\n\n配图：不配\n标签：类型=打卡\n", encoding="utf-8")
            r = run_quiet([str(lint), str(mix)], t)
            check("lint_x_post 对正文混入配图/标签报 W12，段子体行间空行列表不报 W11/W3",
                  "[W12]" in r.stdout and "[W11]" not in r.stdout and "[W3]" not in r.stdout, r.stdout[-300:])
            r = run_quiet([str(lint), str(t / "nope.txt")], t)
            check("lint_x_post 缺失文件干净报错", r.returncode == 2 and "Traceback" not in (r.stderr or ""))

    # 3c. 格式化脚本：只动排版，不改字
    fmt = ROOT / "scripts" / "format_text.py"
    check("格式化脚本随包自带: scripts/format_text.py", fmt.is_file())
    if fmt.is_file():
        with tempfile.TemporaryDirectory() as td:
            t = Path(td)
            src = t / "in.txt"
            src.write_text("说个冷知识：\n收益看互动权重。哪怕10万浏览，收益也可能很低。\n蓝V互关，评论区报到！！\n", encoding="utf-8")
            r = run_quiet([str(fmt), str(src), "--mode", "duanzi", "--split", "--open", "🐱", "--close", "🌱"], t)
            check("段子体：拒绝 --open/--close 点缀（退出码=2）", r.returncode == 2 and "Traceback" not in (r.stderr or ""))
            src.write_text("说个冷知识 🐱：\n收益看互动权重。哪怕10万浏览，收益也可能很低。\n蓝V互关，评论区报到！！😂\n", encoding="utf-8")
            r = run_quiet([str(fmt), str(src), "--mode", "duanzi", "--split"], t)
            out = r.stdout
            lines = out.rstrip("\n").split("\n")
            check("段子体：退出码=0", r.returncode == 0, r.stderr[-200:])
            check("段子体：每行之间都隔一个空行",
                  len(lines) >= 5 and all((ln == "") == (i % 2 == 1) for i, ln in enumerate(lines)), repr(out[:200]))
            check("段子体：原文 emoji 全部去掉", "🐱" not in out and "😂" not in out, repr(out[:200]))
            md = t / "md.txt"
            md.write_text("三处变化\n\n\n- 更快\n- 更省\n1. 先装\n\n#AI\n", encoding="utf-8")
            r = run_quiet([str(fmt), str(md), "--mode", "short", "--title-emoji", "🆕"], t)
            check("短文体：Markdown 列表 → emoji 列表，标题 emoji 在行首",
                  r.returncode == 0 and "🔹 更快" in r.stdout and "1️⃣ 先装" in r.stdout
                  and r.stdout.startswith("🆕 三处变化") and "\n\n\n" not in r.stdout, r.stdout[-200:])
            dl = t / "dl.txt"
            dl.write_text("这周就三步：\n- 早上回评论\n- 中午发原创。真的有用！\n1. 睡前回访\n", encoding="utf-8")
            r = run_quiet([str(fmt), str(dl), "--mode", "duanzi", "--split"], t)
            check("段子体：列表去符号不加 emoji，条目行间空行且不拆句",
                  r.returncode == 0 and "\n\n早上回评论\n\n中午发原创。真的有用！\n\n睡前回访" in r.stdout
                  and "- " not in r.stdout and "🔹" not in r.stdout and "1️⃣" not in r.stdout, r.stdout[-200:])
            dz = t / "dz.txt"
            dz.write_text("今天打卡\n\n🔹 回评论\n\n冲 🐔\n", encoding="utf-8")
            r = run_quiet([str(lint), str(dz), "--duanzi"], t)
            check("lint --duanzi：段子出现 emoji 报 W13", "W13" in (r.stdout + r.stderr), (r.stdout + r.stderr)[-200:])
            dz.write_text("今天打卡\n\n回评论\n\n冲\n", encoding="utf-8")
            r = run_quiet([str(lint), str(dz), "--duanzi"], t)
            check("lint --duanzi：零 emoji 段子不报 W13", "W13" not in (r.stdout + r.stderr), (r.stdout + r.stderr)[-200:])
            r = run_quiet([str(fmt), str(t / "nope.txt"), "--mode", "short"], t)
            check("format_text 缺失文件干净报错", r.returncode == 2 and "Traceback" not in (r.stderr or ""))
            empty = t / "empty.txt"
            empty.write_text("  \n", encoding="utf-8")
            r = run_quiet([str(fmt), str(empty), "--mode", "duanzi"], t)
            check("format_text 空输入干净报错", r.returncode == 2 and "Traceback" not in (r.stderr or ""))

    # 4. scripts/*.py 可编译（用内置 compile 只验语法，不写 .pyc，避免污染工作区）
    for py in sorted((ROOT / "scripts").glob("*.py")):
        try:
            compile(py.read_text(encoding="utf-8"), str(py), "exec")
            check(f"可编译: scripts/{py.name}", True)
        except SyntaxError as e:
            check(f"可编译: scripts/{py.name}", False, str(e))

    if fails:
        print(f"\n[negative_tests] topmind-format: {len(fails)} 项失败")
        sys.exit(1)
    print("\n[negative_tests] topmind-format: 全部通过")


if __name__ == "__main__":
    main()
