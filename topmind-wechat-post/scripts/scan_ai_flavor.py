#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scan_ai_flavor.py — 中文去 AI 味扫描入口（转发器）。

优先调用 qu-aiwei-zh 的 canonical 检测脚本（含「E 类 · 作者姿态层」）；
找不到时回落到随包内置的 `scan_ai_flavor_builtin.py`，并在 stderr 明确提示
「本次只有词面分、没有作者姿态分」——单独安装本技能也能跑，但不会悄悄给出一个
少了一个维度的分数。

## canonical 查找顺序（命中即用，不写死个人路径）

1. `$QU_AIWEI_SCAN`                         显式指定脚本路径
2. 与本技能同级的已装技能：`<本技能所在 skills 目录>/qu-aiwei-zh/scripts/scan_ai_flavor.py`
3. `$QU_AIWEI_SKILLS_DIRS` 里的每个 skills 根目录（用系统路径分隔符分隔）
4. 常见宿主技能目录：`./.agents/skills`、`./.claude/skills`、`~/.agents/skills`、
   `~/.claude/skills`、`~/.codex/skills`、`~/.cursor/skills`

## 开关（转发器自有，不透传）

- `--which`              打印解析到的脚本路径（找不到时打印内置兜底路径并标注）
- `--require-canonical`  找不到 canonical 时退出 3，不回落（定稿门禁想要姿态分时用）

其余参数原样透传（`<file>` / `--json` / `-o` / `-` 管道），退出码取被调脚本的退出码。
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILTIN = os.path.join(HERE, "scan_ai_flavor_builtin.py")
REL = os.path.join("qu-aiwei-zh", "scripts", "scan_ai_flavor.py")


def _candidates():
    out = []
    env = os.environ.get("QU_AIWEI_SCAN")
    if env:
        out.append(env)
    # 本技能装在 <skills>/topmind-wechat-post/scripts/ 下 → 同级 <skills>/qu-aiwei-zh
    out.append(os.path.join(os.path.dirname(os.path.dirname(HERE)), REL))
    for root in (os.environ.get("QU_AIWEI_SKILLS_DIRS") or "").split(os.pathsep):
        if root.strip():
            out.append(os.path.join(root.strip(), REL))
    for root in (os.path.join(".", ".agents", "skills"), os.path.join(".", ".claude", "skills"),
                 os.path.join("~", ".agents", "skills"), os.path.join("~", ".claude", "skills"),
                 os.path.join("~", ".codex", "skills"), os.path.join("~", ".cursor", "skills")):
        out.append(os.path.join(root, REL))
    return [os.path.abspath(os.path.expanduser(c)) for c in out]


def resolve():
    """返回 canonical 脚本绝对路径；找不到返回 None。显式 $QU_AIWEI_SCAN 指错时不往下猜。"""
    env = os.environ.get("QU_AIWEI_SCAN")
    if env:
        p = os.path.abspath(os.path.expanduser(env))
        return p if os.path.isfile(p) else None
    for p in _candidates():
        if os.path.isfile(p) and os.path.realpath(p) != os.path.realpath(__file__):
            return p
    return None


FALLBACK_NOTE = (
    "⚠ 未找到 qu-aiwei-zh 的 canonical 检测脚本，本次用随包内置实现：只有词面分，"
    "没有「作者姿态分」（E 类）。\n"
    "  需要姿态分时：安装 qu-aiwei-zh 技能，或 export QU_AIWEI_SCAN=/path/to/scan_ai_flavor.py；"
    "定稿门禁可加 --require-canonical 强制要求。\n"
)


def main():
    args = sys.argv[1:]
    require = "--require-canonical" in args
    args = [a for a in args if a != "--require-canonical"]
    target = resolve()

    if args and args[0] == "--which":
        if target:
            print(target)
            return 0
        print("%s（内置兜底，无作者姿态分）" % BUILTIN)
        return 3 if require else 0

    if not target:
        if require:
            sys.stderr.write("✗ --require-canonical：找不到 qu-aiwei-zh canonical 脚本。\n已查找：\n")
            sys.stderr.write("".join("  %s\n" % p for p in _candidates()))
            return 3
        sys.stderr.write(FALLBACK_NOTE)
        target = BUILTIN

    os.execv(sys.executable, [sys.executable, target] + args)
    return 0  # 不会到达


if __name__ == "__main__":
    sys.exit(main())
