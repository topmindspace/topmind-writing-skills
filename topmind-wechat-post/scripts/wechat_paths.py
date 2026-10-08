#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wechat_paths.py — 公众号交付包与 topstream 的路径解析（new-article / sync-* / push-to-topstream 共用）。

不写死任何个人路径、类别编号或年份。解析顺序（命中即用）：

交付包根（base）
  1. CLI `--base <专题目录>`
  2. 环境变量 `TOPMIND_WECHAT_BASE`（兼容旧名 `TOPMIND_WECHAT_PACKAGE_ROOT`）
  3. 工作区发现：CLI `--workspace` → 环境变量 `TOPMIND_WORKSPACE`
     - 类别目录按**名称**找，不按编号：`TOPMIND_WECHAT_CATEGORY`（完整目录名）优先，
       否则依次找名为「长文」「创作」「专题」的类别（形如 `NN-长文` / `NN 长文` / `长文`）
     - 专题目录：`TOPMIND_WECHAT_TOPIC`，否则 `{当年}-公众号`（年份取运行当天，不写死）
     - 先用已存在的 `<类别>/<专题>`；都不存在时用第一个已存在的类别 + 专题名（由调用方决定是否创建）
  4. 以上都没有 → 返回 None，调用方报错并提示传 `--base` 或设 `TOPMIND_WORKSPACE`

topstream（可选）
  CLI `--topstream` → 环境变量 `TOPSTREAM_ROOT`（兼容 `TOPMIND_TOPSTREAM`）→ None（跳过 notes 相关校验）
"""
from __future__ import annotations

import datetime
import os
import re

# 公众号交付包所在类别的候选名称（按优先级）。只认名称，编号随工作区模板变化。
CATEGORY_NAMES = ("长文", "创作", "专题")

_CAT_RE = re.compile(r"^(?:\d+[- ]?)?(.+)$")


def _abs(p):
    return os.path.abspath(os.path.expanduser(p))


def default_topic(today=None):
    env = os.environ.get("TOPMIND_WECHAT_TOPIC")
    if env:
        return env.strip()
    year = (today or datetime.date.today()).year
    return "%d-公众号" % year


def find_category_dirs(workspace):
    """返回工作区里按 CATEGORY_NAMES 优先级排列的类别目录（绝对路径）。"""
    explicit = os.environ.get("TOPMIND_WECHAT_CATEGORY")
    if explicit:
        p = os.path.join(workspace, explicit.strip())
        return [p] if os.path.isdir(p) else []
    try:
        entries = sorted(e for e in os.listdir(workspace)
                         if os.path.isdir(os.path.join(workspace, e)))
    except OSError:
        return []
    out = []
    for name in CATEGORY_NAMES:
        for e in entries:
            m = _CAT_RE.match(e)
            if m and m.group(1).strip() == name:
                out.append(os.path.join(workspace, e))
    return out


def resolve_workspace(cli_workspace=None):
    ws = cli_workspace or os.environ.get("TOPMIND_WORKSPACE")
    return _abs(ws) if ws else None


def resolve_base(cli_base=None, cli_workspace=None, today=None):
    """交付包根；解析不到返回 None。"""
    if cli_base:
        return _abs(cli_base)
    env = os.environ.get("TOPMIND_WECHAT_BASE") or os.environ.get("TOPMIND_WECHAT_PACKAGE_ROOT")
    if env:
        return _abs(env)
    ws = resolve_workspace(cli_workspace)
    if not ws:
        return None
    topic = default_topic(today)
    cats = find_category_dirs(ws)
    for cat in cats:
        p = os.path.join(cat, topic)
        if os.path.isdir(p):
            return p
    if cats:
        return os.path.join(cats[0], topic)
    return None


def resolve_topstream(cli_topstream=None):
    if cli_topstream:
        return _abs(cli_topstream)
    env = os.environ.get("TOPSTREAM_ROOT") or os.environ.get("TOPMIND_TOPSTREAM")
    return _abs(env) if env else None


MISSING_BASE = (
    "✗ 找不到公众号交付包根目录。\n"
    "  传 --base <专题目录>，或设置环境变量：\n"
    "    export TOPMIND_WECHAT_BASE=/path/to/<类别>/<年份>-公众号\n"
    "    export TOPMIND_WORKSPACE=/path/to/topmind-workspace   # 按名称发现「长文/创作/专题」类别\n"
    "  可选：TOPMIND_WECHAT_CATEGORY=<类别目录名>、TOPMIND_WECHAT_TOPIC=<专题目录名>"
)


def require_base(cli_base=None, cli_workspace=None):
    base = resolve_base(cli_base, cli_workspace)
    if not base:
        raise SystemExit(MISSING_BASE)
    return base
