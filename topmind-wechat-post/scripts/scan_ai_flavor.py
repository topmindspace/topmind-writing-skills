#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scan_ai_flavor.py — 中文去 AI 味打分入口。

默认运行随包的 `scan_ai_flavor_builtin.py`（词面分）。设置了 `$TOPMIND_AI_SCAN`
（指向你自己的扫描脚本）时，把参数原样转发过去，退出码取被调脚本的退出码；
外部脚本可以额外给出「作者姿态分」等维度。没有外部脚本时在 stderr 说明
「本次只有词面分、没有作者姿态分」，不会悄悄少一个维度。

规则表见 references/de-ai-rules.md；逐句结构检查用 `lint_x_post.py <稿>.md --md`。

## 开关（入口自有，不透传）

- `--which`             打印实际执行的脚本路径
- `--require-external`  没配置外部扫描脚本（或路径不存在）时退出 3，不回落
                        （`--require-canonical` 为旧名，等价）

其余参数原样透传（`<file>` / `--json` / `-o` / `-` 管道）。
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILTIN = os.path.join(HERE, "scan_ai_flavor_builtin.py")
ENV = "TOPMIND_AI_SCAN"


def resolve():
    """返回外部扫描脚本绝对路径；没配置或路径不存在返回 None。"""
    env = os.environ.get(ENV)
    if not env:
        return None
    p = os.path.abspath(os.path.expanduser(env))
    if not os.path.isfile(p) or os.path.realpath(p) == os.path.realpath(__file__):
        return None
    return p


FALLBACK_NOTE = (
    "⚠ 未配置外部扫描脚本（$%s），本次用随包内置实现：只有词面分，没有「作者姿态分」。\n"
    "  需要更多维度时：export %s=/path/to/your_scan.py；定稿门禁可加 --require-external 强制要求。\n"
) % (ENV, ENV)


def main():
    args = sys.argv[1:]
    require = any(a in ("--require-external", "--require-canonical") for a in args)
    args = [a for a in args if a not in ("--require-external", "--require-canonical")]
    target = resolve()

    if args and args[0] == "--which":
        if target:
            print(target)
            return 0
        print("%s（内置实现，无作者姿态分）" % BUILTIN)
        return 3 if require else 0

    if not target:
        if require:
            env = os.environ.get(ENV)
            sys.stderr.write("✗ --require-external：%s\n" % (
                "$%s 指向的文件不存在：%s" % (ENV, env) if env else "没有设置 $%s" % ENV))
            return 3
        sys.stderr.write(FALLBACK_NOTE)
        target = BUILTIN

    os.execv(sys.executable, [sys.executable, target] + args)
    return 0  # 不会到达


if __name__ == "__main__":
    sys.exit(main())
