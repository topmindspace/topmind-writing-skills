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

    # 1b. 共享版式文档随包自带（emoji 体系唯一真源 + 版式规律）
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
            r = run_quiet([str(fmt), str(md), "--mode", "short"], t)
            check("短文体默认：Markdown 列表 → 「·」/「1）」纯文本列表，不强加 emoji",
                  r.returncode == 0 and "· 更快" in r.stdout and "1）先装" in r.stdout
                  and "🔹" not in r.stdout and r.stdout.startswith("三处变化") and "\n\n\n" not in r.stdout, r.stdout[-200:])
            r = run_quiet([str(fmt), str(md), "--mode", "short", "--bullets", "emoji", "--title-emoji", "🆕"], t)
            check("短文体 --bullets emoji：列表 → 🔹 / 1️⃣，标题 emoji 在行首",
                  r.returncode == 0 and "🔹 更快" in r.stdout and "1️⃣ 先装" in r.stdout
                  and r.stdout.startswith("🆕 三处变化"), r.stdout[-200:])
            lk = t / "lk.txt"
            lk.write_text("新版发布\n补全更快了。\n来源：官方日志 https://example.com/log\n详情见官网 https://example.com\n[图1] 截图\n#AI\n", encoding="utf-8")
            r = run_quiet([str(fmt), str(lk), "--mode", "short", "--links-out", str(t / "links.txt")], t)
            links = (t / "links.txt").read_text(encoding="utf-8") if (t / "links.txt").exists() else ""
            check("链接 / 来源行 / 配图行拿出正文、另存另发",
                  r.returncode == 0 and "http" not in r.stdout and "来源：" not in r.stdout and "[图1]" not in r.stdout
                  and "https://example.com/log" in links and "https://example.com" in links and "[图1]" in links, r.stdout + links)
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
            src2 = t / "src2.txt"
            src2.write_text("新版发布\n\n来源：官方 https://example.com/a\n\n配图：官方截图\n\n#AI\n", encoding="utf-8")
            r = run_quiet([str(lint), str(src2)], t)
            out2 = r.stdout + r.stderr
            check("lint：正文有 URL / 来源行 / 配图说明报 E10 / E11 / E12（退出码 1）",
                  r.returncode == 1 and "E10" in out2 and "E11" in out2 and "E12" in out2, out2[-300:])
            r = run_quiet([str(lint), str(src2), "--long"], t)
            check("lint --long：长文允许文内链接，不报 E10–E12", "E10" not in (r.stdout + r.stderr) and "E11" not in (r.stdout + r.stderr), (r.stdout + r.stderr)[-200:])
            plain = t / "plain.txt"
            plain.write_text("某编辑器 3.0：补全延迟压到 200ms 以内\n\n这次改了三处：\n\n1）补全更快\n2）多文件修改\n3）免费 50 次\n\n· 适合小脚本\n· 大仓库待测\n\n#AI编程\n", encoding="utf-8")
            r = run_quiet([str(lint), str(plain), "--strict"], t)
            check("lint：零 emoji、「1）」「·」列表的短文完全通过", r.returncode == 0, (r.stdout + r.stderr)[-300:])
            ai = t / "ai.txt"
            ai.write_text("总的来说，这次更新不仅更快，更稳定，堪称更快、更强、更智能的重磅升级\n\n#AI\n", encoding="utf-8")
            r = run_quiet([str(lint), str(ai)], t)
            check("lint：AI 套话报 W9、首行过长报 W10", "W9" in r.stdout and "W10" in r.stdout, r.stdout[-300:])
            lg = t / "long.txt"
            lg.write_text("长文标题\n\n理想的 agent 就三件事，用三个词概括。\n\n" + "这一段写得太长了，" * 14 + "\n\n- 列表项不算段落\n", encoding="utf-8")
            r = run_quiet([str(lint), str(lg), "--long"], t)
            check("lint --long：公式化计数标签报 W9、单段过长报 W14", "W9" in r.stdout and "三件事" in r.stdout and "W14" in r.stdout, r.stdout[-300:])
            st = t / "struct.txt"
            st.write_text("新模型发布了\n\n为什么？答案很简单：它进行了深入分析。\n\n专家指出这很重要。\n\n这才是 AI 的意义。\n", encoding="utf-8")
            r = run_quiet([str(lint), str(st)], t)
            check("lint：设问自答 / 进行+动词 / 无出处权威 / 升华收尾报 W15",
                  r.stdout.count("W15") >= 4 and "设问自答" in r.stdout and "进行+动词" in r.stdout and "无出处权威" in r.stdout and "升华收尾" in r.stdout, r.stdout[-400:])
            en = t / "en.txt"
            en.write_text("New release\n\nIt's not just a model, but a platform. Let's dive in.\n\nMoreover, it plays a pivotal role. I hope this helps!\n", encoding="utf-8")
            r = run_quiet([str(lint), str(en)], t)
            check("lint：英文 not-just-but / signpost / transition / role inflation / chatbot residue 报 W16",
                  r.stdout.count("W16") >= 4 and "chatbot residue" in r.stdout, r.stdout[-400:])
            pu = t / "punct.txt"
            pu.write_text("太快了！！\n\n一——二——三——四\n\n好！好！\n", encoding="utf-8")
            r = run_quiet([str(lint), str(pu)], t)
            check("lint：标点连用、破折号 / 感叹号过多报 W17", r.stdout.count("W17") >= 3, r.stdout[-300:])
            okx = t / "legit.txt"
            okx.write_text("测试还在进行中，结果下周出。\n\n这就是我用的配置。\n\n据 IDC 报告，分析人士认为出货量 6 月回升 12%。\n\n可能是 A，也可能是 B。\n\n是不是该换了？我也说不准。\n\n这个 API 很稳，文档写得清楚。\n\nThe launch is not ready yet. We delayed it by two weeks.\n", encoding="utf-8")
            r = run_quiet([str(lint), str(okx), "--strict"], t)
            check("lint：正常写法不误报 W15 / W16 / W17（进行中、这就是…配置、有出处的分析人士、也可能、是不是）",
                  r.returncode == 0 and not any(c in r.stdout for c in ("W15", "W16", "W17")), r.stdout[-400:])
            md = t / "post.md"
            md.write_text("---\ntitle: t\n---\n# 标题\n\n**加粗**和 [链接](https://a.example) 都合法。\n\n- 列表也合法\n\n![自制流量图](images/01-x.png)\n\n![自制，数据：官方 2026-09](images/02-y.png)\n\n总的来说，未来可期。\n", encoding="utf-8")
            r = run_quiet([str(lint), str(md), "--md"], t)
            check("lint --md：Markdown 语法不报错，套话报 W9 / W15，缺数据来源的自制图报 W18（只报 1 张）",
                  r.returncode == 0 and "E1" not in r.stdout and "E4" not in r.stdout and "W9" in r.stdout and "W15" in r.stdout and r.stdout.count("W18") == 1, r.stdout[-400:])
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

    # 短文没有 280 字限制：约 900 字的纯文本不触发 W7；超过约 1000 字才提示写成长文（X Article）
    import tempfile as _tf
    LINT = ROOT / "scripts" / "lint_x_post.py"
    with _tf.TemporaryDirectory() as _d:
        f9 = Path(_d) / "s.txt"; f9.write_text("一段很长的短文\n\n" + "这是正文内容。" * 128 + "\n", encoding="utf-8")
        r = subprocess.run([sys.executable, str(LINT), str(f9)], capture_output=True, text=True)
        check("短文约 900 字不报 W7", "W7" not in r.stdout, r.stdout[:120])
        f9.write_text("一段很长的短文\n\n" + "这是正文内容。" * 160 + "\n", encoding="utf-8")
        r = subprocess.run([sys.executable, str(LINT), str(f9)], capture_output=True, text=True)
        check("超过约 1000 字提示写成 X Article", "W7" in r.stdout and "X Article" in r.stdout, r.stdout[:120])

    if fails:
        print(f"\n[negative_tests] topmind-format: {len(fails)} 项失败")
        sys.exit(1)
    print("\n[negative_tests] topmind-format: 全部通过")


if __name__ == "__main__":
    main()
