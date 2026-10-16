#!/usr/bin/env python3
"""Overlay a multi-line title onto a cover background (path B of the dual path).

Usage:
  python3 scripts/overlay-title.py <background.png> <spec.json> --out <cover.png> [--font <font file>]

spec.json fields (all optional except lines):
  lines        list of {"text", "size", "color", "underline", "stroke", "stroke_color"}
               or plain strings; each line can override the global values
  x, y         top-left of the title block in pixels (default: 7% of width, 22% of height)
  align        "left" (default) or "center" (centered on the image)
  color        default text color (default "#1E1E1E")
  stroke       outline width in px (default 0); stroke_color (default "#FFFFFF")
  shadow       true for a hard drop shadow; shadow_color, shadow_offset (default 6)
  line_gap     extra pixels between lines (default 12)
  chips        list of short strings drawn as rounded pills under the title
  chip_bg, chip_color, chip_size   pill colors and text size (defaults "#1E1E1E", "#FFFFFF", 30)
  underline    a line's "underline" color draws a hand-marker bar under that line

The output keeps the background's size. Text is drawn exactly as given; check it before publishing.
"""
import argparse
import json
import os
import sys

FONT_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "C:/Windows/Fonts/msyhbd.ttc",
    "C:/Windows/Fonts/msyh.ttc",
]


def fail(msg):
    print("错误：" + msg, file=sys.stderr)
    sys.exit(1)


def find_font(explicit):
    if explicit:
        if not os.path.isfile(explicit):
            fail("找不到字体文件：%s" % explicit)
        return explicit
    for path in FONT_CANDIDATES:
        if os.path.isfile(path):
            return path
    fail("没找到中文字体，请用 --font 指定一个 .ttf/.ttc/.otf 文件")


def main():
    ap = argparse.ArgumentParser(description="在封面底图上叠加多行标题")
    ap.add_argument("background")
    ap.add_argument("spec")
    ap.add_argument("--out", required=True)
    ap.add_argument("--font")
    args = ap.parse_args()

    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        fail("需要 Pillow：pip install Pillow")

    if not os.path.isfile(args.background):
        fail("找不到底图：%s" % args.background)
    if not os.path.isfile(args.spec):
        fail("找不到 spec 文件：%s" % args.spec)
    try:
        with open(args.spec, encoding="utf-8") as f:
            spec = json.load(f)
    except (ValueError, OSError) as e:
        fail("spec 不是合法 JSON：%s" % e)
    if not isinstance(spec, dict) or not spec.get("lines"):
        fail("spec 里必须有非空的 lines 列表")
    try:
        img = Image.open(args.background).convert("RGBA")
    except Exception:
        fail("底图不是可读取的图片：%s" % args.background)

    font_path = find_font(args.font)
    W, H = img.size
    draw = ImageDraw.Draw(img)

    def font(size):
        try:
            index = 2 if "CJK" in os.path.basename(font_path) and font_path.endswith(".ttc") else 0
            return ImageFont.truetype(font_path, int(size), index=index)
        except Exception:
            fail("字体无法加载：%s" % font_path)

    color = spec.get("color", "#1E1E1E")
    stroke = int(spec.get("stroke", 0))
    stroke_color = spec.get("stroke_color", "#FFFFFF")
    shadow = bool(spec.get("shadow", False))
    shadow_color = spec.get("shadow_color", "#00000088")
    off = int(spec.get("shadow_offset", 6))
    gap = int(spec.get("line_gap", 12))
    align = spec.get("align", "left")
    x0 = int(spec.get("x", W * 0.07))
    y = int(spec.get("y", H * 0.22))

    try:
        for raw in spec["lines"]:
            line = {"text": raw} if isinstance(raw, str) else dict(raw)
            text = str(line.get("text", ""))
            if not text:
                continue
            f = font(line.get("size", H * 0.16))
            sw = int(line.get("stroke", stroke))
            l, t, r, b = draw.textbbox((0, 0), text, font=f, stroke_width=sw)
            w, h = r - l, b - t
            x = (W - w) // 2 if align == "center" else x0
            if line.get("underline"):
                bar_h = max(8, h // 5)
                draw.rounded_rectangle([x - 6, y + h - bar_h // 2 - t, x + w + 6, y + h + bar_h // 2 - t],
                                       radius=bar_h // 2, fill=line["underline"])
            if shadow:
                draw.text((x - l + off, y - t + off), text, font=f, fill=shadow_color,
                          stroke_width=sw, stroke_fill=shadow_color)
            draw.text((x - l, y - t), text, font=f, fill=line.get("color", color),
                      stroke_width=sw, stroke_fill=line.get("stroke_color", stroke_color))
            y += h + gap

        chips = spec.get("chips") or []
        if chips:
            cf = font(spec.get("chip_size", 30))
            cx, y = x0, y + gap * 2
            for chip in chips:
                l, t, r, b = draw.textbbox((0, 0), str(chip), font=cf)
                pw, ph = (r - l) + 36, (b - t) + 20
                if align == "center" and cx == x0:
                    total = sum(draw.textbbox((0, 0), str(c), font=cf)[2] + 52 for c in chips)
                    cx = (W - total) // 2
                draw.rounded_rectangle([cx, y, cx + pw, y + ph], radius=ph // 2,
                                       fill=spec.get("chip_bg", "#1E1E1E"))
                draw.text((cx + 18 - l, y + 10 - t), str(chip), font=cf, fill=spec.get("chip_color", "#FFFFFF"))
                cx += pw + 16
    except ValueError as e:
        fail("颜色或数值写法不对：%s" % e)

    out_dir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_dir, exist_ok=True)
    img.convert("RGB").save(args.out)
    print("已输出：%s（%d×%d）" % (args.out, W, H))


if __name__ == "__main__":
    main()
