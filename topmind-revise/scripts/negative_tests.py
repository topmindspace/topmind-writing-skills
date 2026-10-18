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
import re
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
        # 按次数比：删掉一处「多半」、多引用一次数字都要看得见；「改前」这种短词不算引语
        cb, ca = t / "cnt_b.md", t / "cnt_a.md"
        cb.write_text("# t\n\n明年多半会涨，后年多半还涨，star 已经 39 万。\n", encoding="utf-8")
        ca.write_text("# t\n\n这一段里「改前」只是个标签。明年多半会涨，star 已经 39 万，比去年多 39 万。\n", encoding="utf-8")
        r = run(["scripts/revise_check.py", str(cb), str(ca), "--json"])
        fid = (json.loads(r.stdout or "{}") if r.returncode == 0 else {}).get("保真", {})
        check("revise_check：确定性词按次数比（多半 2→1）", any("多半（2→1）" in x for x in fid.get("确定性词", {}).get("次数变化", [])),
              json.dumps(fid, ensure_ascii=False)[:300])
        check("revise_check：数字按次数比（39万 1→2）", any(x.startswith("39万（1→2）") for x in fid.get("数字", {}).get("次数变化", [])),
              json.dumps(fid, ensure_ascii=False)[:300])
        check("revise_check：「改前」这种短词不算引语", not fid.get("引语", {}).get("新增"), json.dumps(fid, ensure_ascii=False)[:300])

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
        # --declare：改动表里依据是事实 / 逻辑 / 作者意见的段落不计入；依据是规则编号的照算
        def declare_file(basis: str) -> Path:
            f = t / f"declare_{basis[:2]}.md"
            rows = "\n".join(f"| 改前第 {i} 段 | {basis} | {pb[:18]}… | … |" for i, pb in enumerate(paras_b, 1))
            f.write_text("# 改稿报告\n\n## 改动表\n\n| 位置 | 依据 | 原文 | 改后 |\n|---|---|---|---|\n" + rows + "\n", encoding="utf-8")
            return f
        r = run(["scripts/revise_check.py", str(clean_b), str(clean_a), "--json", "--declare", str(declare_file("② 逻辑"))])
        o = (json.loads(r.stdout or "{}") if r.returncode == 0 else {}).get("过度改稿", {})
        check("revise_check --declare：登记为逻辑关的改动不计入过度改稿", o.get("over_edit") is False and len(o.get("declared", [])) == 5,
              json.dumps(o, ensure_ascii=False)[:300])
        r = run(["scripts/revise_check.py", str(clean_b), str(clean_a), "--json", "--declare", str(declare_file("⓪ 结构"))])
        o = (json.loads(r.stdout or "{}") if r.returncode == 0 else {}).get("过度改稿", {})
        check("revise_check --declare：登记为⓪结构复查的改动不计入过度改稿", o.get("over_edit") is False and len(o.get("declared", [])) == 5,
              json.dumps(o, ensure_ascii=False)[:300])
        r = run(["scripts/revise_check.py", str(clean_b), str(clean_a), "--json", "--declare", str(declare_file("Z17 假强调"))])
        o = (json.loads(r.stdout or "{}") if r.returncode == 0 else {}).get("过度改稿", {})
        check("revise_check --declare：依据是规则编号的改动照算", o.get("over_edit") is True, json.dumps(o, ensure_ascii=False)[:300])
        r = run(["scripts/revise_check.py", str(clean_b), str(clean_a), "--declare", str(t / "nope.md")])
        check("revise_check --declare 读不到文件退出码=2 且无 Traceback", r.returncode == 2 and no_tb(r), f"rc={r.returncode}")
        # 报告骨架：改动表预填、剩余 H 也列进「保留未改的命中」、带人工检查清单
        hb, ha = t / "h_b.md", t / "h_a.md"
        hb.write_text("# t\n\n这是一段普通的介绍，讲本地存储。\n\n第二段保持不变，讲插件。\n", encoding="utf-8")
        ha.write_text("# t\n\n这是真正的本地存储，一段普通的介绍。\n\n第二段保持不变，讲插件。\n", encoding="utf-8")
        rp2 = t / "report2.md"
        run(["scripts/revise_check.py", str(hb), str(ha), "--report", str(rp2)])
        txt = rp2.read_text(encoding="utf-8") if rp2.is_file() else ""
        check("revise_check --report：改动表按 diff 预填", "| 改前第" in txt and "真正的本地存储" in txt, txt[:300])
        check("revise_check --report：剩余 H 列进保留未改的命中", "[H1]" in txt and "（一句判断）" in txt, txt[:500])
        check("revise_check --report：带人工检查清单", "## 人工检查" in txt and "- [ ]" in txt)
        lb, la = t / "long_b.md", t / "long_a.md"
        para = "某笔记工具这周发了新版，把同步改成了可选项，默认只存本地，用户自己决定要不要上云。"
        lb.write_text("# t\n\n" + "\n\n".join([para] * 5) + "\n", encoding="utf-8")
        la.write_text("# t\n\n" + para + "\n\n- 同步：可选\n- 存储：本地\n", encoding="utf-8")
        rp3 = t / "report3.md"
        r = run(["scripts/revise_check.py", str(lb), str(la), "--report", str(rp3)])
        t3 = rp3.read_text(encoding="utf-8") if rp3.is_file() else ""
        check("revise_check：长文给出改前 / 改后信息设计提示数（I，只提示）",
              "信息设计提示" in r.stdout and re.search(r"改前 [1-9]\d* 条 → 改后 0 条", t3) is not None, r.stdout[-300:] + t3[:200])
        check("revise_check --report：带信息设计诊断（⓪ 结构）且在改动表之前",
              "## 信息设计诊断" in txt and txt.find("## 信息设计诊断") < txt.find("## 改动表"), txt[:400])

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
        # 草稿期占位截图：W4 不报错；改成定稿就是 E3
        art2 = Path(td) / "占位"
        art2.mkdir()
        fm = "---\ntitle: 占位\ndate: 2026-10-18\nstatus: {st}\ntags: [a]\ncover: cover/c.png\n---\n\n# 占位\n\n正文。\n\n![对练截图](images/01-对练截图.png)\n"
        (art2 / "占位.md").write_text(fm.format(st="草稿"), encoding="utf-8")
        r = run(["scripts/check_article.py", str(art2)])
        check("check_article 草稿期占位截图只给 W4", r.returncode == 0 and "W4" in r.stdout and "E3" not in r.stdout, r.stdout[-200:])
        (art2 / "占位.md").write_text(fm.format(st="定稿"), encoding="utf-8")
        r = run(["scripts/check_article.py", str(art2)])
        check("check_article 定稿时缺图仍是 E3", r.returncode == 1 and "E3" in r.stdout, r.stdout[-200:])
        (art2 / "占位.md").write_text(fm.format(st="草稿").replace("01-对练截图", "01-架构"), encoding="utf-8")
        r = run(["scripts/check_article.py", str(art2)])
        check("check_article 普通图片缺失仍是 E3（不是占位）", r.returncode == 1 and "E3" in r.stdout, r.stdout[-200:])

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
