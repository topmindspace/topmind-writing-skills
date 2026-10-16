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
                return subprocess.run([sys.executable, str(ENGINE), "--check", str(f)], capture_output=True, text=True)
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
            r = chk([main, {"type": "text", "role": "sub", "text": "副标题", "size": 0.1}])
            check("引擎：合规层级通过", r.returncode == 0, r.stdout[:120])
            for sp in sorted((ROOT / "assets" / "title-specs").glob("*.json")):
                r = subprocess.run([sys.executable, str(ENGINE), "--check", str(sp)], capture_output=True, text=True)
                check(f"引擎：示例 spec {sp.name} 达标", r.returncode == 0, r.stdout[-120:])

    # 6. check-title：形近字 / 超长 / 繁体 / 生僻字被标出，常用短标题通过
    CT = ROOT / "scripts" / "check-title.py"
    def ct(*a):
        return subprocess.run([sys.executable, str(CT), *a], capture_output=True, text=True)
    r = ct("大于一切"); check("标题检查：「于」被标为形近字", r.returncode == 1 and "干" in r.stdout, r.stdout[:120])
    r = ct("一二三四五六七八九十一二三"); check("标题检查：超过 12 字为高风险", r.returncode == 2, r.stdout[:120])
    r = ct("鍵盤"); check("标题检查：繁体为高风险", r.returncode == 2 and "繁体" in r.stdout, r.stdout[:120])
    r = ct("硬核架构", "从单体到分布式"); check("标题检查：常用短标题低风险", r.returncode == 0, r.stdout[:120])
    r = ct(); check("标题检查：缺参数干净报错", r.returncode == 1 and "Traceback" not in r.stderr, r.stderr[:80])

    # 7. cover-patterns：范式 12–20 个，每个都有英文模板，通用尾句含简体原文约束
    pat = (ROOT / "references" / "cover-patterns.md").read_text(encoding="utf-8")
    import re as _re
    n = len(_re.findall(r"^## X\d+ ", pat, _re.M))
    check("范式库：12–20 个范式", 12 <= n <= 20, f"实 {n}")
    check("范式库：模板含 {title} 与简体原文约束", "{title}" in pat and "Simplified Chinese characters exactly as given" in pat)

    # 8. cover-combos：≥20 个命名组合，每个有模板；不得含第三方网址或来源站名
    cb = (ROOT / "references" / "cover-combos.md").read_text(encoding="utf-8")
    nc = len(_re.findall(r"^### C\d+ ", cb, _re.M))
    check("组合库：至少 20 个命名组合", nc >= 20, f"实 {nc}")
    check("组合库：每个组合都有英文模板", cb.count("```text") >= nc and "central horizontal band" in cb)
    check("组合库：不含第三方网址", "http" not in cb)

    # 9. 不得出现参考来源：第三方站点名、创作者账号、来源 / 灵感致谢、资料网址清单
    import re as _re2
    base = ROOT.parent if (ROOT.parent / "shared").is_dir() else ROOT
    bad = _re2.compile(r"xarticles|x\.com/(?!i/)[A-Za-z0-9_]+/(?:status|article)|inspired by|learned from|灵感来自|参考帖|参考了|借鉴自|调研来源|^## 来源\s*$|^出处：|公开封面合集|uisdc|nngroup|huashu|alchaincyf|noahduck", _re2.I | _re2.M)
    hits = []
    for f in base.rglob("*"):
        if f.suffix not in (".md", ".json", ".txt") or "node_modules" in f.parts or f.name == "CHANGELOG.md" or f.name.startswith("LICENSE"):
            continue
        for m in bad.finditer(f.read_text(encoding="utf-8", errors="ignore")):
            hits.append(f"{f.relative_to(base)}: {m.group(0)}")
    check("全仓：不出现参考来源、站点名、账号或致谢语", not hits, "; ".join(hits[:5]))

    if fails:
        print(f"\n[negative_tests] {len(fails)} 项失败")
        sys.exit(1)
    print("\n[negative_tests] 全部通过")


if __name__ == "__main__":
    main()
