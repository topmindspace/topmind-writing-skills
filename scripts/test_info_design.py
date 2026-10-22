#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""信息设计提示（I1–I9）回归测试：test_lint_rules.py 会调用，CI 与 Release 都跑。

两组样例，全部是通用虚构示例：
  SHOULD_REPORT      应报指定 I 编号。
  SHOULD_NOT_REPORT  不应报指定的 I 编号（None 表示一条 I 都不应报）。
另查：I 提示永远不让 de_ai_lint --strict 失败；--no-design 关掉；--json 有 design 字段。
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "shared" / "scripts"))
import info_design_hints as I  # noqa: E402

FM = "---\ntitle: 示例\n---\n\n# 示例\n\n"
P40 = "某笔记工具这周发了新版，把同步改成了可选项，默认只存本地，用户自己决定要不要上云。"
P150 = ("某笔记工具这周发了新版，把同步改成了可选项，默认只存本地。" * 5)[:150]
LEAD = "某笔记工具 3.0 把同步改成了可选，默认只存本地。\n\n"


def doc(*paras, fm=FM):
    return fm + "\n\n".join(paras) + "\n"


SHOULD_REPORT = [
    ("I1", doc(LEAD.strip(), P40, P40.replace("这周", "上周"), P40.replace("新版", "测试版"), P40.replace("本地", "硬盘"))),
    ("I2", doc(LEAD.strip(), *[f"## {n}、第 {n} 节\n\n" + P150 + "\n\n" + P150.replace("某", "这款") for n in "一二三四五六"])),
    ("I3", doc(LEAD.strip(), "新版支持离线编辑、本地端到端加密、多设备自动同步、插件市场一键安装。")),
    ("I3", doc(LEAD.strip(), "离线编辑默认打开；同步改成手动开启；插件市场换了审核规则；导出支持三种格式。")),
    ("I3", doc(LEAD.strip(), "第一，同步变成了可选项。", "第二，插件要重新审核。", "第三，导出多了两种格式。")),
    ("I4", doc(LEAD.strip(), "改前：它让效率提升了数倍。", "改后：同样的笔记，整理时间从 20 分钟降到 5 分钟。",
               "改前：这是一次革命性的更新。", "改后：这次更新把同步改成了可选。")),
    ("I5", doc(LEAD.strip(), "## 二、离线能力成了标配", "离线能力成了标配，三家主流工具都默认只存本地。")),
    ("I5", doc(LEAD.strip(), "这次更新最大的变化是同步改成了可选项，默认只存本地。",
               "换句话说，同步改成了可选项，默认只存本地，用户自己决定。")),
    ("I6", doc(P150 + "这是一段很长的开头。")),
    ("I6", doc("你有没有想过，笔记到底该放在哪里？", P40)),
    ("I7", doc(LEAD.strip(), "## 二、现在", P150, P150.replace("某", "这款"), P150.replace("新版", "测试版"))),
    ("I9", doc(LEAD.strip(), "## 二、三家的做法\n\n" + P150 + "\n\n" + P150.replace("某", "另一款") + "\n\n" + P150.replace("某", "第三款"))),
]
BUDGET_CASE = doc(LEAD.strip(), "![图](images/01.png)", P150, "- 一\n- 二", P150.replace("某", "这款"), "| a | b |\n|---|---|\n| 1 | 2 |",
                  P150.replace("新版", "测试版"), "![图](images/02.png)", P150.replace("本地", "硬盘"))

GOOD = doc(
    "某笔记工具 3.0 把同步改成了可选，默认只存本地。三个变化：",
    "- 同步：默认关闭，手动开启\n- 插件：重新审核，首批 120 个\n- 导出：新增 PDF 和 HTML",
    "## 二、和竞品比",
    "| 工具 | 默认存储 | 价格 |\n|---|---|---|\n| A | 本地 | 免费 |\n| B | 云端 | 按月付 |",
    "放在一起看，本地优先已经从小众选择变成了默认选项。",
    "![某工具设置页](images/01-settings.png)",
    "来源：某工具官方更新日志，截至 10 月 15 日",
    "## 三、明年会怎样",
    "照现在的速度，明年多半每个主流工具都会给一个「只存本地」的开关。",
)
SHOULD_NOT_REPORT = [
    (None, GOOD),
    ({"I1", "I2", "I7"}, doc(P40, P40.replace("这周", "上周"), P40.replace("新版", "测试版"), P40.replace("本地", "硬盘"),
                             P40.replace("用户", "我"), fm="---\ntitle: 随笔\ntype: essay\n---\n\n# 随笔\n\n")),
    ({"I3"}, doc(LEAD.strip(), "支持 Mac、Windows、Linux。")),
    ({"I3"}, doc(LEAD.strip(), "离线、加密、同步，三样都有。")),
    ({"I4"}, doc(LEAD.strip(), "| 改前 | 改后 |\n|---|---|\n| 效率提升数倍 | 20 分钟降到 5 分钟 |\n| 革命性更新 | 同步改成可选 |")),
    ({"I5"}, doc(LEAD.strip(), "## 二、离线能力成了标配", "三家主流工具这个月都改了默认设置。")),
    ({"I1"}, doc(LEAD.strip(), P40, P40.replace("这周", "上周"), "![图](images/01.png)", P40.replace("新版", "测试版"), P40)),
    ({"I6"}, doc("某笔记工具 3.0 发布：同步改成可选，默认只存本地。", P40)),
]


def codes(text, budget=None):
    return {c for _, c, _ in I.analyze(text, budget=budget)}


def main() -> int:
    fails = []
    for want, text in SHOULD_REPORT:
        got = codes(text)
        if want not in got:
            fails.append(f"漏报 {want}：{text[len(FM):len(FM) + 40]!r} → {sorted(got)}")
    if "I8" not in codes(BUDGET_CASE, budget=400):
        fails.append("漏报 I8：预算 400 字的稿子写了 700 多字")
    if "I8" in codes(BUDGET_CASE, budget=700):
        fails.append("误报 I8：在预算 30% 以内")
    judged = doc(LEAD.strip(), "## 二、三家的做法\n\n" + P150 + "\n\n" + P150.replace("某", "另一款") + "\n\n大概率明年三家都会默认只存本地。")
    if "I9" in codes(judged):
        fails.append("误报 I9：这一节有判断句")
    for banned, text in SHOULD_NOT_REPORT:
        got = codes(text)
        bad = got if banned is None else got & banned
        if bad:
            fails.append(f"误报 {sorted(bad)}：{text[len(FM):len(FM) + 40]!r}")
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "a.md"
        f.write_text(SHOULD_REPORT[0][1], encoding="utf-8")
        lint = str(ROOT / "shared/scripts/de_ai_lint.py")
        r = subprocess.run([sys.executable, lint, str(f), "--strict"], capture_output=True, text=True)
        if r.returncode != 0 or "[I1]" not in r.stdout:
            fails.append(f"de_ai_lint --strict：I 提示应打印且不导致失败 rc={r.returncode} {r.stdout[-200:]}")
        r = subprocess.run([sys.executable, lint, str(f), "--no-design"], capture_output=True, text=True)
        if "[I" in r.stdout:
            fails.append("de_ai_lint --no-design 仍打印 I 提示")
        r = subprocess.run([sys.executable, lint, str(f), "--json"], capture_output=True, text=True)
        if '"design"' not in r.stdout:
            fails.append("de_ai_lint --json 输出缺 design")
        r = subprocess.run([sys.executable, str(ROOT / "shared/scripts/info_design_hints.py"), str(f)], capture_output=True, text=True)
        if r.returncode != 0:
            fails.append(f"info_design_hints 有提示时退出码应为 0：rc={r.returncode}")
        (Path(td) / "骨架.md").write_text("# 骨架\n\n篇幅：约 100 字\n", encoding="utf-8")
        if I.read_budget(f) != 100:
            fails.append("read_budget 没读到同目录 骨架.md 的篇幅")
    total = len(SHOULD_REPORT) + len(SHOULD_NOT_REPORT) + 2
    if fails:
        print("\n".join("  ✗ " + x for x in fails))
        print(f"[test_info_design] {len(fails)} 项失败（共 {total} 条样例）")
        return 1
    print(f"[test_info_design] 全部通过：应报 {len(SHOULD_REPORT) + 1} 条、不应报 {len(SHOULD_NOT_REPORT) + 1} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())
