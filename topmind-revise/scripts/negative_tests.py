#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""topmind-revise 异常输入测试：工具链在坏输入下干净失败、不崩溃，规则不误报（任一失败 → 退出码 1）。

覆盖：
  1. 自包含：不引用技能目录外的相对路径；共享规则与脚本随包自带
  2. audit_skill.py 在坏 frontmatter 上退出码 1；package_skill.py --check 在缺 README 时退出码 1
  3. de_ai_lint.py：强信号报 W、语境词只报 H、--strict 不被 H 卡住、读不到文件退出码 2
  4. revise_check.py：数字 / 引语变化被发现、--strict 退出码 1、过度改稿比例、坏输入退出码 2
  5. count_words.py：去掉标题和图片后计数
  6. examples：改前有 W、改后 0 W
  7. scripts/*.py 全部可编译
"""
from __future__ import annotations

import json
import py_compile
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


def run(args: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess:
    return subprocess.run([PY, *args], capture_output=True, text=True, timeout=60, cwd=str(cwd))


def no_tb(r: subprocess.CompletedProcess) -> bool:
    return "Traceback" not in (r.stderr or "") + (r.stdout or "")


def main() -> None:
    print("[negative_tests] topmind-revise")

    # 1. 自包含
    outside = [md.relative_to(ROOT).as_posix() for md in [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md"))]
               if md.is_file() and "](../" in md.read_text(encoding="utf-8")]
    check("不引用技能目录外的相对路径", not outside, "、".join(outside))
    for ref in ("core-voice.md", "de-ai-rules.md", "revision-workflow.md", "image-sourcing.md",
                "fact-check.md", "report-template.md", "examples.md"):
        check(f"规则随包自带: references/{ref}", (ROOT / "references" / ref).is_file())
    for sc in ("de_ai_lint.py", "lint_x_post.py", "count_words.py", "revise_check.py", "audit-provenance.py",
               "check_article.py"):
        check(f"脚本随包自带: scripts/{sc}", (ROOT / "scripts" / sc).is_file())

    # 2. 坏 frontmatter / 缺 README
    with tempfile.TemporaryDirectory() as td:
        sk = Path(td) / "skill"
        shutil.copytree(ROOT, sk, ignore=shutil.ignore_patterns("dist", "__pycache__"))
        (sk / "SKILL.md").write_text("no frontmatter\n", encoding="utf-8")
        r = run(["scripts/audit_skill.py"], sk)
        check("audit_skill 在坏 frontmatter 上退出码=1 且无 Traceback", r.returncode == 1 and no_tb(r), f"rc={r.returncode}")
    with tempfile.TemporaryDirectory() as td:
        sk = Path(td) / "skill"
        shutil.copytree(ROOT, sk, ignore=shutil.ignore_patterns("dist", "__pycache__"))
        (sk / "README.md").unlink()
        r = run(["scripts/package_skill.py", "--check"], sk)
        check("package_skill --check 在缺 README 时退出码=1 且无 Traceback", r.returncode == 1 and no_tb(r), f"rc={r.returncode}")

    with tempfile.TemporaryDirectory() as td:
        t = Path(td)

        # 3. de_ai_lint
        bad = t / "bad.md"
        bad.write_text("# 标题\n\n值得注意的是，这不仅是一次升级，更是一场变革。\n\n如图所示，速度快了一倍。\n", encoding="utf-8")
        r = run(["scripts/de_ai_lint.py", str(bad), "--json"])
        data = json.loads(r.stdout or "[]") if r.returncode == 0 else []
        codes = {w.get("code") for item in data for w in item.get("warnings", [])}
        check("de_ai_lint：强信号报 W9", "W9" in codes, r.stdout[-300:] + r.stderr[-300:])
        check("de_ai_lint：复述图片报 W21", "W21" in codes, str(codes))
        ctx = t / "ctx.md"
        ctx.write_text("# 标题\n\n真正的难点不在模型，在数据清洗。\n", encoding="utf-8")
        r = run(["scripts/de_ai_lint.py", str(ctx), "--strict"])
        check("de_ai_lint：语境词只给 H，--strict 不失败", r.returncode == 0 and "[H1]" in r.stdout, r.stdout[-300:])
        r = run(["scripts/de_ai_lint.py", str(ctx), "--no-hints"])
        check("de_ai_lint：--no-hints 不打印提示", "[H" not in r.stdout, r.stdout[-200:])
        r = run(["scripts/de_ai_lint.py", str(t / "missing.md")])
        check("de_ai_lint：读不到文件退出码=2 且无 Traceback", r.returncode == 2 and no_tb(r), f"rc={r.returncode}")

        # 4. revise_check
        before = t / "before.md"
        after = t / "after.md"
        before.write_text("# 标题\n\n某框架三个月涨到 6 万星标，作者说「这个功能我们不会做」。\n\n可能下个月发布 2.0。\n", encoding="utf-8")
        after.write_text("# 标题\n\n某框架三个月涨到 8 万星标，作者说「这个功能不做」。\n\n下个月发布 2.0。\n", encoding="utf-8")
        r = run(["scripts/revise_check.py", str(before), str(after), "--json"])
        rep = json.loads(r.stdout or "{}") if r.returncode == 0 else {}
        fid = rep.get("保真", {})
        check("revise_check：发现数字变化", "6万" in "".join(fid.get("数字", {}).get("消失", [])), json.dumps(fid, ensure_ascii=False)[:300])
        check("revise_check：发现引语变化", bool(fid.get("引语", {}).get("消失")), json.dumps(fid, ensure_ascii=False)[:300])
        check("revise_check：发现确定性词消失", "可能" in fid.get("确定性词", {}).get("消失", []), json.dumps(fid, ensure_ascii=False)[:300])
        r = run(["scripts/revise_check.py", str(before), str(after), "--strict"])
        check("revise_check --strict：数字 / 引语变化 → 退出码 1", r.returncode == 1, f"rc={r.returncode}")
        r = run(["scripts/revise_check.py", str(before), str(before), "--strict"])
        check("revise_check --strict：原样 → 退出码 0", r.returncode == 0, f"rc={r.returncode} {r.stdout[-200:]}")
        rp = t / "report.md"
        r = run(["scripts/revise_check.py", str(before), str(after), "--report", str(rp)])
        check("revise_check --report 写出报告骨架", rp.is_file() and "## 未核实条目" in rp.read_text(encoding="utf-8"))
        r = run(["scripts/revise_check.py", str(before), str(t / "missing.md")])
        check("revise_check：读不到文件退出码=2 且无 Traceback", r.returncode == 2 and no_tb(r), f"rc={r.returncode}")

        # 过度改稿：干净段落被大面积改写
        clean_b = t / "clean_b.md"
        clean_a = t / "clean_a.md"
        paras_b = [f"第{i}段讲的是版本 {i} 的变化，启动快了一些，内存少了一点。" for i in range(1, 6)]
        paras_a = [f"第{i}段讲版本 {i} 的变化：启动快了一些，内存也少了一点。" for i in range(1, 6)]
        clean_b.write_text("\n\n".join(paras_b) + "\n", encoding="utf-8")
        clean_a.write_text("\n\n".join(paras_a) + "\n", encoding="utf-8")
        r = run(["scripts/revise_check.py", str(clean_b), str(clean_a), "--json"])
        rep = json.loads(r.stdout or "{}") if r.returncode == 0 else {}
        check("revise_check：没命中的段落被大面积改写 → 提示过度改稿", rep.get("过度改稿", {}).get("over_edit") is True,
              json.dumps(rep.get("过度改稿"), ensure_ascii=False))

        # 5. count_words
        cw = t / "cw.md"
        cw.write_text("---\ntitle: x\n---\n# 标题不算\n\n一二三四五。\n\n![图](a.png)\n\n六七八。\n", encoding="utf-8")
        r = run(["scripts/count_words.py", str(cw), "--json"])
        cnt = json.loads(r.stdout or "{}") if r.returncode == 0 else {}
        check("count_words：去掉 frontmatter / 标题 / 图片后计数", cnt.get("paragraphs") == 2 and cnt.get("chars", 0) >= 8, r.stdout)

    # 6. examples
    ex = ROOT / "examples"
    r = run(["scripts/de_ai_lint.py", str(ex / "01-长文-改前.md"), "--strict"])
    check("examples：改前有 W（--strict 退出码 1）", r.returncode == 1, f"rc={r.returncode}")
    r = run(["scripts/de_ai_lint.py", str(ex / "01-长文-改后.md"), "--strict"])
    check("examples：改后 0 W", r.returncode == 0, r.stdout[-300:])
    r = run(["scripts/lint_x_post.py", str(ex / "02-短文-改后.txt"), "--strict"])
    check("examples：短文改后通过 lint_x_post --strict", r.returncode == 0, r.stdout[-300:])

    # 6b. check_article：缺 frontmatter 字段 → E1，退出 1，无 Traceback
    with tempfile.TemporaryDirectory() as td:
        art = Path(td) / "某文"
        art.mkdir()
        (art / "某文.md").write_text("---\ntitle: 某文\n---\n\n# 某文\n\n正文。\n", encoding="utf-8")
        r = run(["scripts/check_article.py", str(art / "某文.md")])
        check("check_article 缺字段报 E1 并退出 1", r.returncode == 1 and "E1" in r.stdout and no_tb(r), r.stdout[-200:])

    # 7. 可编译
    for f in sorted((ROOT / "scripts").glob("*.py")):
        try:
            py_compile.compile(str(f), doraise=True, cfile=str(Path(tempfile.gettempdir()) / (f.stem + ".pyc")))
            ok = True
        except py_compile.PyCompileError:
            ok = False
        check(f"可编译: scripts/{f.name}", ok)

    if fails:
        print(f"\n[negative_tests] {len(fails)} 项失败")
        sys.exit(1)
    print("\n[negative_tests] 全部通过")


if __name__ == "__main__":
    main()
