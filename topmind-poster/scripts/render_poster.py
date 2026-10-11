#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTML → 高清 PNG（无头 Chrome 截图 + 自动裁掉底部空白）。

用法:
    python3 scripts/render_poster.py poster.html -o poster.png
    python3 scripts/render_poster.py p1.html p2.html p3.html --out-dir images/
    python3 scripts/render_poster.py poster.html -o poster.png --width 1080

参数:
    -o / --out          单个输入时的输出文件
    --out-dir           多个输入时的输出目录（输出名 = 输入名 .png）
    --width             画布宽度 CSS px（默认 1180）。**应与 HTML 里 body 的 width 一致**
    --scale             设备像素比（默认 2，即输出 2× 高清）
    --height            截图窗口高度（默认 8000）。内容触底会自动翻倍重试
    --tail              底部保留的尾巴像素（1× 计，默认 44）
    --chrome            指定 Chrome / Chromium 可执行文件路径

退出码: 0 全部成功 / 1 有失败。
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CHROME_CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
)


def find_chrome(explicit):
    """定位可执行的无头浏览器。"""
    if explicit:
        if not Path(explicit).is_file():
            raise SystemExit("[render_poster] 指定的浏览器不存在: %s" % explicit)
        return explicit
    env = os.environ.get("CHROME_PATH")
    if env and Path(env).is_file():
        return env
    for c in CHROME_CANDIDATES:
        if Path(c).is_file():
            return c
    for name in ("google-chrome", "chromium", "chromium-browser", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    raise SystemExit(
        "[render_poster] 未找到无头浏览器。用 --chrome <路径> 指定，或设 CHROME_PATH。"
    )


def screenshot(chrome, html, raw, width, height, scale):
    """调无头 Chrome 截整页。

    --no-sandbox / --disable-gpu-sandbox 在 macOS 沙箱下是必须的，
    否则报 `sandbox initialization failed` 后直接不出图（见 SKILL.md 坑 1）。
    """
    cmd = [
        chrome,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--disable-gpu-sandbox",
        "--hide-scrollbars",
        "--force-device-scale-factor=%d" % scale,
        "--window-size=%d,%d" % (width, height),
        "--screenshot=%s" % raw,
        html.resolve().as_uri(),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if not Path(raw).is_file():
        tail = (r.stderr or r.stdout or "")[-500:]
        raise SystemExit("[render_poster] 截图失败，未产出文件。\n%s" % tail)


def scan_bottom(im):
    """扫出内容底边 y。基准色从窗口底部取，不是左上角（见 SKILL.md 坑 5）。"""
    w, h = im.size
    rgb = im.convert("RGB")
    bg = rgb.getpixel((5, h - 6))
    px = rgb.load()
    for y in range(h - 1, -1, -1):
        if any(px[x, y] != bg for x in range(0, w, 7)):
            return y
    return -1


def render_one(chrome, src, dst, args):
    """截图 + 扫底 + 裁切。返回 (成功?, 尺寸, 内容底边)。"""
    from PIL import Image

    height = args.height
    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / "raw.png"
        last = -1
        for attempt in range(3):
            screenshot(chrome, src, raw, args.width, height, args.scale)
            im = Image.open(raw).convert("RGB")
            last = scan_bottom(im)
            if last < 0:
                raise SystemExit(
                    "[render_poster] 扫底失败：整幅都是背景色。"
                    "可能是页面用了整页平铺纹理（见 SKILL.md 坑 5），或 HTML 没渲染出内容。"
                )
            if last < im.size[1] - 8 or attempt == 2:
                break
            height *= 2
            print("  · 内容触底，窗口高度加倍到 %d 重试" % height)

        w, h = im.size
        bottom = min(h, last + 1 + args.tail * args.scale)
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.crop((0, 0, w, bottom)).save(dst)
    return True, (w, bottom), last


def main():
    ap = argparse.ArgumentParser(description="HTML → 高清 PNG（截图 + 自动裁白）")
    ap.add_argument("inputs", nargs="+", help="HTML 文件")
    ap.add_argument("-o", "--out", help="单个输入时的输出 PNG")
    ap.add_argument("--out-dir", help="多个输入时的输出目录")
    ap.add_argument("--width", type=int, default=1180, help="画布宽度 CSS px（默认 1180）")
    ap.add_argument("--scale", type=int, default=2, help="设备像素比（默认 2）")
    ap.add_argument("--height", type=int, default=8000, help="截图窗口高度（默认 8000）")
    ap.add_argument("--tail", type=int, default=44, help="底部保留尾巴 px（1× 计，默认 44）")
    ap.add_argument("--chrome", help="Chrome / Chromium 可执行文件路径")
    args = ap.parse_args()

    srcs = [Path(p) for p in args.inputs]
    if len(srcs) > 1 and not args.out_dir:
        raise SystemExit("[render_poster] 多个输入时必须给 --out-dir")
    if len(srcs) == 1 and not args.out and not args.out_dir:
        raise SystemExit("[render_poster] 请给 -o 或 --out-dir")

    chrome = find_chrome(args.chrome)
    ok = 0
    for s in srcs:
        dst = Path(args.out_dir) / (s.stem + ".png") if args.out_dir else Path(args.out)
        if not s.is_file():
            print("  ✗ 找不到 %s" % s)
            continue
        print("[render_poster] %s → %s" % (s.name, dst.name))
        _, size, last = render_one(chrome, s, dst, args)
        print("  ✓ %s  %d×%d  (内容底边 %dpx)" % (dst, size[0], size[1], last))
        ok += 1

    print("\n[render_poster] %d/%d 张成功" % (ok, len(srcs)))
    if ok != len(srcs):
        sys.exit(1)


if __name__ == "__main__":
    main()
