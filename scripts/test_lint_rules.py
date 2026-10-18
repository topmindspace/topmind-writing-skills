#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""去 AI 味规则回归测试（CI 与 Release 都跑）。

三组样例，全部是通用虚构示例：
  SHOULD_PASS   不应报 W 的写法（作者在合适场景里会用的强势词、口语收尾、梗、「其实是…」等）；允许出 H 提示。
  SHOULD_WARN   应报指定 W 编号的套话。
  SHOULD_HINT   应报指定 H 编号、但不应报任何 W 的写法。
任何一句误报或漏报，退出码 1。新增规则先在这里加样例。
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True  # 同目录模块不写 __pycache__（技能包里不留缓存）
sys.path.insert(0, str(ROOT / "shared" / "scripts"))
import de_ai_lint as D  # noqa: E402

# (文体, 文本)；文体为 long 时按 Markdown 处理
SHOULD_PASS = [
    ("long", "总结来说，离线能力会是笔记应用接下来的分水岭。拭目以待吧。"),
    ("long", "毫无疑问，比拼已经从参数转到了生态，预计明年会有平台站队。归根结底，谁都不想丢掉入口。"),
    ("long", "说白了，谁离用户近，谁就有话语权。"),
    ("long", "大家抢着做 agent，其实是在抢入口。"),
    ("long", "平台不是真不让进，是怕位置被占。"),
    ("long", "明年大平台大概率会站队。"),
    ("long", "照现在的速度，明年大平台多半要站队。"),
    ("long", "某项目的 star 已经超过 12 万，比上一个榜首多出 3 万。"),
    ("long", "放在一起看就明白了：老牌框架攒了五年才 8 万。"),
    ("long", "某创始人：也许我们该自己做一个竞争对手。"),
    ("long", "文中配图和排版都是用某工具做的，想试的直接把仓库地址丢给你的 agent。"),
    ("long", "# 笔记工具，真正的本地优先来了\n\n## 二、现在：大厂纷纷跟进\n\n过去半年发了 8 款。"),
    ("long", "![某项目时间线](images/01-timeline.png)\n\n来源：某项目官方仓库，截至 10 月 15 日"),
    ("long", "![自制，数据：某官方 2026-09](images/02-chart.png)"),
    ("long", "这只小火箭太猛了，某项目半年涨到 12 万 star。"),
    ("long", "两边都在提速。"),
    ("long", "测试还在进行中，结果下周出。\n\n可能是 A，也可能是 B。"),
    ("long", "据某媒体报道，出货量 6 月回升 12%。"),
    ("long", "经过 5 轮实测，某插件又升级了，这次主要调启动速度。"),
    ("title", "做了一年笔记工具，发现真正缺的是记录习惯"),
    ("title", "某商店下架某插件，作者要自己做一个？"),
    ("title", "本地优先笔记工具"),
    ("title", "某系列第二篇：它凭什么越用越懂你"),
    ("summary", "一文读懂某某的过去、现在与未来。"),
    ("short", "某编辑器 3.0 要收费了？！\n\n官方更新日志里出现了订阅入口。\n\n#AI #智能体"),
    ("short", "开源史上最快，某项目 30 天 star 破 10 万。\n\n#AI #开源"),
    ("short", "重磅：某模型开源，权重和代码都放出来了。"),
    ("short", "终端直接执行：npx some-cli install"),
    ("short", "把仓库地址丢给你的 agent，让它帮你装好。"),
    ("short", "某技能又升级了：\n\n· 长文默认 Markdown\n· 新增改稿技能\n· 去 AI 味规则重写"),
    ("reply", "某框架（小火箭🚀）更新了！！"),
    ("reply", "这小火箭是真能涨啊🚀"),
    ("reply", "站某厂，顶住"),
    ("reply", "能理解，谁都不想把入口让出去"),
    ("reply", "这股热度能撑到年底吗"),
    ("duanzi", "我让某 agent 帮我整理这个月的开销\n\n它问我要不要取消三个用不上的订阅\n\n结果第一个取消的就是它自己"),
    ("duanzi", "老板：你这周产出呢\n\n我：agent 在跑"),
    ("duanzi", "两家又同一天发布新模型\n\n最开心的是做评测的博主"),
]

SHOULD_WARN = [
    ("short", "为什么？答案很简单：它更快。", "W15"),
    ("long", "这才是 AI 的意义。", "W15"),
    ("long", "话不多说，直接上图。", "W15"),
    ("long", "我们对数据进行了深入分析。", "W15"),
    ("long", "专家指出这很重要。", "W15"),
    ("long", "未来可期。", "W15"),
    ("long", "希望对你有帮助。", "W15"),
    ("long", "本质上，这是一场平台之间的较量。", "W15"),
    ("long", "这背后其实是一场深层博弈。", "W15"),
    ("long", "在当今这个时代，工具层出不穷。", "W9"),
    ("long", "它不仅更快，更稳定。", "W9"),
    ("long", "这不是一次升级，而是一场变革。", "W9"),
    ("long", "综上所述，值得一试。", "W9"),
    ("short", "更快、更强、更智能的新版本", "W9"),
    ("long", "这次更新是颠覆性的。", "W9"),
    ("long", "一句话总结：快。", "W9"),
    ("long", "It's not just a model, but a platform.", "W16"),
    ("long", "说完现在，再看看明年会怎么走。", "W20"),
    ("long", "先看时间线。", "W20"),
    ("long", "如图所示，增长很快。", "W21"),
    ("short", "老板说：你这周产出呢", "W19"),
    ("duanzi", "我妈说：那我找谁", "W19"),
    ("short", "太快了！！！", "W17"),
    ("short", "第一行\n\n真的吗？？", "W17"),
    ("long", "这一段写得太长了，" * 14, "W14"),
    ("long", "![自制流量图](images/01-x.png)", "W18"),
]

SHOULD_HINT = [
    ("long", "我认为明年会二选一。", "H3"),
    ("long", "这个项目约 30 万用户。", "H4"),
    ("long", "某项目的 star 数达到 392,000。", "H4"),
    ("long", "开发者在狂奔，平台在刹车。", "H5"),
    ("long", "![某项目 star](images/01.png)\n\n来源：GitHub，star 增长曲线", "H6"),
    ("short", "某平台被拦了。\n\n某平台暂未回应。", "H8"),
    ("title", "你还在手动整理笔记吗？", "H9"),
    ("long", "毫无疑问，这是今年最重要的更新。", "H1"),
    ("long", "这是里程碑式的成就。", "H1"),
    ("short", "某更新上线\n\n#AI #编程 #工具", "H11"),
    ("short", "某更新上线\n\n🔹 一\n🔹 二\n🔹 三\n🔹 四\n🔹 五", "H7"),
    ("long", "某创始人说：也许该自己做。", "H12"),
    ("long", "第一句。第二句。第三句。第四句。", "H10"),
    ("reply", "更新了！！", "H2"),
]

fails: list[str] = []


def run(genre: str, text: str):
    g = "short" if genre == "summary" else genre
    return D.analyze(text, g, markdown=(g == "long"))


def main() -> int:
    for genre, text in SHOULD_PASS:
        w, _h = run(genre, text)
        if w:
            fails.append(f"误报 W（{genre}）：{text[:30]!r} → {[c for _, c, _ in w]}")
    for genre, text, code in SHOULD_WARN:
        w, _h = run(genre, text)
        if code not in {c for _, c, _ in w}:
            fails.append(f"漏报 {code}（{genre}）：{text[:30]!r} → {[c for _, c, _ in w]}")
    for genre, text, code in SHOULD_HINT:
        w, h = run(genre, text)
        if code not in {c for _, c, _ in h}:
            fails.append(f"漏报 {code}（{genre}）：{text[:30]!r} → {[c for _, c, _ in h]}")
        if w:
            fails.append(f"提示样例误报 W（{genre}）：{text[:30]!r} → {[c for _, c, _ in w]}")
    # CLI：H 不计入 --strict；--no-hints 关掉提示；lint_x_post 与 de_ai_lint 一致
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "s.txt"
        f.write_text("某项目更新了！！\n\n毫无疑问，这次值得一试。\n\n#AI #智能体\n", encoding="utf-8")
        for script in ("de_ai_lint.py", "lint_x_post.py"):
            r = subprocess.run([sys.executable, str(ROOT / "shared/scripts" / script), str(f), "--strict"],
                               capture_output=True, text=True)
            if r.returncode != 0 or "提示" not in r.stdout:
                fails.append(f"{script} --strict：H 提示不应导致失败 rc={r.returncode} {r.stdout[-200:]}")
            r = subprocess.run([sys.executable, str(ROOT / "shared/scripts" / script), str(f), "--no-hints"],
                               capture_output=True, text=True)
            if "[H" in r.stdout:
                fails.append(f"{script} --no-hints 仍打印提示")
        r = subprocess.run([sys.executable, str(ROOT / "shared/scripts/de_ai_lint.py"), str(f), "--json"],
                           capture_output=True, text=True)
        if '"hints"' not in r.stdout:
            fails.append("de_ai_lint --json 输出缺 hints")
    total = len(SHOULD_PASS) + len(SHOULD_WARN) + len(SHOULD_HINT)
    if fails:
        print("\n".join("  ✗ " + x for x in fails))
        print(f"[test_lint_rules] {len(fails)} 项失败（共 {total} 条样例）")
        return 1
    print(f"[test_lint_rules] 全部通过：不应报 {len(SHOULD_PASS)} 条、应报 W {len(SHOULD_WARN)} 条、应报 H {len(SHOULD_HINT)} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())
