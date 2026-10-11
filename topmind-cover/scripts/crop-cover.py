#!/usr/bin/env python3
"""封面图裁剪：从 5:2 主图中央裁出公众号 2.35:1 版，并统一落盘命名。

用法：
    python3 crop-cover.py <主图路径> --out-dir <包>/images/

产出：
    <out-dir>/00-封面.png          1500x600  (X / 公众号共用主文件)
    <out-dir>/00-封面-公众号.png   900x383   (公众号封面大图，中央裁剪)
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("需要 Pillow：pip install pillow")

TARGETS = {
    "00-封面.png": (1500, 600),
    "00-封面-公众号.png": (900, 383),
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", help="5:2 主图路径")
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    src = Path(args.src)
    out_dir = Path(args.out_dir)
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        sys.exit(f"错误：无法创建输出目录 {out_dir}（{e}）")

    if not src.is_file():
        sys.exit(f"错误：找不到输入图片 {src}")
    try:
        img = Image.open(src).convert("RGB")
    except Exception as e:
        sys.exit(f"错误：无法读取图片 {src}（{e}）")
    w, h = img.size

    # 先按 5:2 中央裁一块基准
    base_ratio = 5 / 2
    if w / h > base_ratio:
        cw, ch = int(h * base_ratio), h
    else:
        cw, ch = w, int(w / base_ratio)
    x0, y0 = (w - cw) // 2, (h - ch) // 2
    base = img.crop((x0, y0, x0 + cw, y0 + ch))

    try:
        for name, (tw, th) in TARGETS.items():
            ratio = tw / th
            bw, bh = base.size
            if bw / bh > ratio:
                cw2, ch2 = int(bh * ratio), bh
            else:
                cw2, ch2 = bw, int(bw / ratio)
            x1, y1 = (bw - cw2) // 2, (bh - ch2) // 2
            out = base.crop((x1, y1, x1 + cw2, y1 + ch2)).resize((tw, th), Image.LANCZOS)
            dest = out_dir / name
            out.save(dest)
            print(f"OK {dest} ({tw}x{th})")
    except OSError as e:
        sys.exit(f"错误：写入封面图失败（{e}）")


if __name__ == "__main__":
    main()
