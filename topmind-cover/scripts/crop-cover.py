#!/usr/bin/env python3
"""按本包预设等比裁切封面；预设不是平台强制上传规格。

用法：
    python3 crop-cover.py <主图路径> --out-dir <包>/images/

产出：
    <out-dir>/00-封面.png          1500x600  (X / 公众号共用主文件)
    <out-dir>/00-封面-公众号.png   900x383   (公众号封面大图，中央裁剪)

其他预设（各输出直接从原图裁切）：
    python3 crop-cover.py <16:9 主图> --preset x-post --out-dir <目录>
    python3 crop-cover.py <竖版主图> --preset xiaohongshu --out-dir <目录>
    python3 crop-cover.py <竖版主图> --preset douyin --out-dir <目录>
    python3 crop-cover.py <原图> --preset wechat --anchor left --out-dir <目录>

横版与竖版通常需分别构图；脚本不判断裁切是否损伤标题或主体。
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
                    help="本包导出预设：article 双横图（默认）；x-post 16:9；"
                         "xiaohongshu / douyin 3:4；wechat 宽图与方图。不是平台硬性要求")
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
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        sys.exit(f"错误：无法创建输出目录 {out_dir}（{e}）")

    try:
        for name, (tw, th) in targets.items():
            out = ImageOps.fit(img, (tw, th), method=Image.Resampling.LANCZOS,
                               centering=ANCHORS[args.anchor])
            dest = out_dir / name
            out.save(dest)
            print(f"OK {dest} ({tw}x{th})")
    except OSError as e:
        sys.exit(f"错误：写入封面图失败（{e}）")


if __name__ == "__main__":
    main()
