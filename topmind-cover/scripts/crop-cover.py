#!/usr/bin/env python3
"""按主流平台预设等比裁切封面（绝不拉伸变形，自动保护原图不被覆盖）。

用法：
    python3 crop-cover.py <主图路径> --out-dir <包>/images/

默认产出（article）：
    <out-dir>/00-封面.png          1500x600  (X Article / 通用长文头图，5:2)
    <out-dir>/00-封面-公众号.png   900x383   (公众号宽封面，约 2.35:1)

其他预设（各输出直接从原图独立裁切）：
    python3 crop-cover.py <16:9 主图> --preset x-post --out-dir <目录>
    python3 crop-cover.py <中央 4:3 已构图的 16:9 母图> --preset landscape-pair --out-dir <目录>
    python3 crop-cover.py <中央 3:4 已构图的 9:16 母图> --preset vertical-pair --out-dir <目录>
    python3 crop-cover.py <竖版主图> --preset xiaohongshu --out-dir <目录>
    python3 crop-cover.py <竖版主图> --preset douyin --out-dir <目录>
    python3 crop-cover.py <原图> --preset wechat --anchor left --out-dir <目录>

横版与竖版通常需分别构图；裁切后请实际检查标题与主体完整性。
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("需要 Pillow：pip install pillow")

PRESETS = {
    "article": {
        "00-封面.png": (1500, 600),
        "00-封面-公众号.png": (900, 383),
    },
    "x-post": {
        "00-封面-X短文.png": (1200, 675),
    },
    "landscape-pair": {
        "00-封面-横版-4x3.png": (1080, 810),
        "00-封面-横版-16x9.png": (1920, 1080),
    },
    "vertical-pair": {
        "00-封面-竖版-3x4.png": (1080, 1440),
        "00-封面-竖版-9x16.png": (1080, 1920),
    },
    "xiaohongshu": {"00-封面-小红书.png": (1080, 1440)},
    "douyin": {"00-封面-抖音图文.png": (1080, 1440)},
    "wechat": {
        "00-封面-公众号.png": (900, 383),
        "00-封面-公众号方图.png": (900, 900),
    },
}

ANCHORS = {
    "center": (0.5, 0.5),
    "left": (0.0, 0.5),
    "right": (1.0, 0.5),
    "top": (0.5, 0.0),
    "bottom": (0.5, 1.0),
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", help="原图路径；建议按目标画幅先完成构图")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--preset", choices=sorted(PRESETS), default="article",
                    help="导出预设：article 双横图（默认）；x-post 16:9；"
                         "landscape-pair 中央 4:3 与完整 16:9；"
                         "vertical-pair 中央 3:4 与完整 9:16；"
                         "xiaohongshu / douyin 3:4；wechat 宽图与方图。")
    ap.add_argument("--anchor", choices=sorted(ANCHORS), default="center",
                    help="裁切保留方向，默认 center；请实际检查每张输出")
    args = ap.parse_args()

    src = Path(args.src)
    out_dir = Path(args.out_dir)
    if not src.is_file():
        sys.exit(f"错误：找不到输入图片 {src}")
    targets = PRESETS[args.preset]
    try:
        for name in targets:
            dest = out_dir / name
            if dest.resolve() == src.resolve() or (dest.exists() and dest.samefile(src)):
                sys.exit("错误：输出会覆盖输入原图，请更换输出目录或原图文件名")
    except OSError as e:
        sys.exit(f"错误：无法核对输出路径（{e}）")
    try:
        with Image.open(src) as opened:
            img = ImageOps.exif_transpose(opened).convert("RGB")
    except Exception as e:
        sys.exit(f"错误：无法读取图片 {src}（{e}）")
    if args.preset == "landscape-pair":
        if args.anchor != "center":
            sys.exit("错误：横版双尺寸预设只使用中央 4:3，请用 --anchor center")
        if img.width * 9 != img.height * 16:
            sys.exit("错误：横版双尺寸预设需要已完成构图的 16:9 母图，请保留完整背景再叠字")
    if args.preset == "vertical-pair":
        if args.anchor != "center":
            sys.exit("错误：竖版双尺寸预设只使用中央 3:4，请用 --anchor center")
        if img.width * 16 != img.height * 9:
            sys.exit("错误：竖版双尺寸预设需要已完成构图的 9:16 母图，请保留完整背景再叠字")
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        sys.exit(f"错误：无法创建输出目录 {out_dir}（{e}）")

    try:
        for name, (tw, th) in targets.items():
            if args.preset == "landscape-pair" and tw * 3 == th * 4:
                width = img.height * 4 // 3
                left = (img.width - width) // 2
                out = img.crop((left, 0, left + width, img.height)).resize((tw, th), Image.Resampling.LANCZOS)
            elif args.preset == "vertical-pair" and tw * 4 == th * 3:
                height = img.width * 4 // 3
                top = (img.height - height) // 2
                out = img.crop((0, top, img.width, top + height)).resize((tw, th), Image.Resampling.LANCZOS)
            else:
                out = ImageOps.fit(img, (tw, th), method=Image.Resampling.LANCZOS,
                                   centering=ANCHORS[args.anchor])
            dest = out_dir / name
            out.save(dest)
            print(f"OK {dest} ({tw}x{th})")
    except OSError as e:
        sys.exit(f"错误：写入封面图失败（{e}）")


if __name__ == "__main__":
    main()
