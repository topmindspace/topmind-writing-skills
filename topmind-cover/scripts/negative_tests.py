#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""topmind-cover 异常输入测试：crop-cover.py 与 overlay-title.py 错误路径干净、正常路径出图（任一失败 → 退出码 1）。"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
CROP = ROOT / "scripts" / "crop-cover.py"
OVERLAY = ROOT / "scripts" / "overlay-title.py"
PY = sys.executable
fails: list[str] = []


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([PY, str(CROP), *args], capture_output=True, text=True, timeout=60)


def run_overlay(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([PY, str(OVERLAY), *args], capture_output=True, text=True, timeout=60)


def check(name: str, cond: bool, detail: str = "") -> None:
    print(("  ✓ " if cond else "  ✗ ") + name + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        fails.append(name)


def main() -> None:
    print("[negative_tests] topmind-cover")
    crops = subprocess.run([PY, str(ROOT / "scripts" / "test_crop_cover.py")],
                           capture_output=True, text=True, timeout=60)
    check("多平台裁切行为回归", crops.returncode == 0, crops.stdout + crops.stderr)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)

        # 1. 缺失输入 → 非零退出，无 Traceback
        r = run([str(td / "nope.png"), "--out-dir", str(td / "o1")])
        check("缺失输入干净报错", r.returncode != 0 and "Traceback" not in r.stderr, r.stderr[:100])

        # 2. 非图片文件 → 非零退出，无 Traceback
        (td / "notimg.txt").write_text("hello", encoding="utf-8")
        r = run([str(td / "notimg.txt"), "--out-dir", str(td / "o2")])
        check("非图片干净报错", r.returncode != 0 and "Traceback" not in r.stderr, r.stderr[:100])

        # 3. 正常图片产出双尺寸
        try:
            from PIL import Image
            img = Image.new("RGB", (1600, 900), (20, 30, 60))
            img.save(td / "ok.png")
            r = run([str(td / "ok.png"), "--out-dir", str(td / "o3")])
            got_a = (td / "o3" / "00-封面.png").exists()
            got_b = (td / "o3" / "00-封面-公众号.png").exists()
            check("正常图片产出双尺寸", r.returncode == 0 and got_a and got_b, r.stderr[:100])
            if got_a:
                w, h = Image.open(td / "o3" / "00-封面.png").size
                check("主图 1500×600", (w, h) == (1500, 600), f"实 {w}×{h}")
            if got_b:
                w, h = Image.open(td / "o3" / "00-封面-公众号.png").size
                check("公众号图 900×383", (w, h) == (900, 383), f"实 {w}×{h}")
        except ImportError:
            print("  - 跳过图片生成测试（无 Pillow）")

        # 4. overlay-title：缺失底图 / 坏 spec → 干净报错
        (td / "spec_bad.json").write_text("{not json", encoding="utf-8")
        r = run_overlay([str(td / "nope.png"), str(td / "spec_bad.json"), "--out", str(td / "x.png")])
        check("叠字：缺失底图干净报错", r.returncode != 0 and "Traceback" not in r.stderr, r.stderr[:100])
        try:
            from PIL import Image
            Image.new("RGB", (1200, 675), (245, 240, 230)).save(td / "bg.png")
            r = run_overlay([str(td / "bg.png"), str(td / "spec_bad.json"), "--out", str(td / "x.png")])
            check("叠字：坏 JSON 干净报错", r.returncode != 0 and "Traceback" not in r.stderr, r.stderr[:100])
            (td / "spec_empty.json").write_text('{"lines": []}', encoding="utf-8")
            r = run_overlay([str(td / "bg.png"), str(td / "spec_empty.json"), "--out", str(td / "x.png")])
            check("叠字：空 lines 干净报错", r.returncode != 0 and "Traceback" not in r.stderr, r.stderr[:100])
            (td / "spec_ok.json").write_text(
                '{"lines": [{"text": "Local LLM", "size": 90}, {"text": "AT HOME", "size": 140, '
                '"color": "#D83A2E", "underline": "#F2C230"}], "stroke": 6, "shadow": true, "chips": ["a", "b"]}',
                encoding="utf-8")
            r = run_overlay([str(td / "bg.png"), str(td / "spec_ok.json"), "--out", str(td / "ok_overlay.png")])
            if r.returncode != 0 and "字体" in r.stderr:
                print("  - 跳过叠字出图测试（本机无可用字体）")
            else:
                ok = r.returncode == 0 and (td / "ok_overlay.png").exists()
                check("叠字：正常出图", ok, r.stderr[:100])
                if ok:
                    size = Image.open(td / "ok_overlay.png").size
                    check("叠字：尺寸与底图一致", size == (1200, 675), f"实 {size}")
        except ImportError:
            print("  - 跳过叠字测试（无 Pillow）")

    # 5. title-engine：坏输入干净报错；设计规范静态检查（字号下限、层级、克制）；示例 spec 全部达标
    ENGINE = ROOT / "scripts" / "title-engine.py"
    import importlib.util as _iu
    if not (_iu.find_spec("numpy") and _iu.find_spec("PIL")):
        print("  - 跳过 title-engine 测试（无 numpy / Pillow）")
    else:
        with tempfile.TemporaryDirectory() as t2:
            t2 = Path(t2)
            r = subprocess.run([sys.executable, str(ENGINE), str(t2 / "nope.png"), str(t2 / "x.json"), "--out", str(t2 / "o.png")], capture_output=True, text=True)
            check("引擎：缺场景图干净报错", r.returncode == 1 and "Traceback" not in r.stderr, r.stderr[:100])
            def chk(layers):
                f = t2 / "c.json"; f.write_text(json.dumps({"layers": layers}, ensure_ascii=False), encoding="utf-8")
                return subprocess.run([sys.executable, str(ENGINE), "--check", "--strict", str(f)], capture_output=True, text=True)
            main = {"type": "text", "role": "main", "text": "标题", "size": 0.3}
            r = chk([main, {"type": "text", "role": "label", "text": "小字", "size": 0.035}])
            check("引擎：标签字号低于 6% 被拦下", r.returncode == 1 and "低于下限" in r.stdout, r.stdout[:120])
            r = chk([main, {"type": "text", "role": "sub", "text": "副标题", "size": 0.25}])
            check("引擎：主副字号比 <1.6 被拦下", r.returncode == 1 and "层级不清" in r.stdout, r.stdout[:120])
            r = chk([dict(main, glow={"color": "#0F0"}), {"type": "text", "role": "sub", "text": "副", "size": 0.1, "extrude": {"depth": 0.1}}])
            check("引擎：重特效超过一个字块被拦下", r.returncode == 1 and "只能用在一个重点词" in r.stdout, r.stdout[:120])
            r = chk([dict(main, rotate=8)])
            check("引擎：旋转没写 reason 被拦下", r.returncode == 1 and "reason" in r.stdout, r.stdout[:120])
            r = chk([main] + [{"type": "deco", "kind": "star", "x": 0.5, "y": 0.5}] * 3)
            check("引擎：装饰超过 2 个被拦下", r.returncode == 1 and "上限 2 个" in r.stdout, r.stdout[:120])
            # 默认允许作者的风格选择；严格模板检查仅显式启用。
            custom = t2 / "custom.json"
            custom.write_text(json.dumps({"layers": [dict(main, rotate=18),
                {"type": "text", "role": "label", "text": "小字", "size": 0.035}]}), encoding="utf-8")
            relaxed = subprocess.run([sys.executable, str(ENGINE), "--check", str(custom)], capture_output=True, text=True)
            check("引擎：默认设计提示不卡住自定义排版", relaxed.returncode == 0 and "建议" in relaxed.stdout, relaxed.stdout[:160])
            empty = t2 / "empty.json"; empty.write_text('{"layers": []}', encoding="utf-8")
            invalid = subprocess.run([sys.executable, str(ENGINE), "--check", str(empty)], capture_output=True, text=True)
            check("引擎：空图层仍干净报错", invalid.returncode == 1 and "Traceback" not in invalid.stderr)
            r = chk([main, {"type": "text", "role": "sub", "text": "副标题", "size": 0.1}])
            check("引擎：合规层级通过", r.returncode == 0, r.stdout[:120])
            for sp in sorted((ROOT / "assets" / "title-specs").glob("*.json")):
                r = subprocess.run([sys.executable, str(ENGINE), "--check", str(sp)], capture_output=True, text=True)
                check(f"引擎：示例 spec {sp.name} 达标", r.returncode == 0, r.stdout[-120:])

    # 6. 标题核对默认是建议；显式 strict 可沿用旧提示级别，缺输入仍失败。
    CT = ROOT / "scripts" / "check-title.py"
    def ct(*a):
        return subprocess.run([sys.executable, str(CT), *a], capture_output=True, text=True)
    r = ct("大于一切"); check("标题：形近字提示不阻塞", r.returncode == 0 and "干" in r.stdout)
    r = ct("一二三四五六七八九十一二三"); check("标题：长标题保留原文", r.returncode == 0 and "长度不代表" in r.stdout)
    r = ct("鍵盤"); check("标题：作者语言不作为失败", r.returncode == 0 and "保留作者语言" in r.stdout)
    r = ct("--strict", "一二三四五六七八九十一二三"); check("标题：主动选择 strict 仍有退出级别", r.returncode == 2)
    r = ct(); check("标题：缺参数仍失败", r.returncode != 0 and "Traceback" not in r.stderr)

    # 知识目录、卡片与路径的真实完整性检查，替代固定配方数量 / 固定措辞测试。
    r = subprocess.run([PY, str(ROOT / "scripts" / "knowledge.py"), "validate"], capture_output=True, text=True)
    check("知识包：独立安装目录完整可读", r.returncode == 0, r.stdout + r.stderr)

    # 公开参考与署名可以保留；私人路径、密钥等由仓库 ci_privacy_scan.py 检查。
    # 不再把创作者账号、来源链接或致谢本身当作泄漏。

    if fails:
        print(f"\n[negative_tests] {len(fails)} 项失败")
        sys.exit(1)
    print("\n[negative_tests] 全部通过")


if __name__ == "__main__":
    main()
