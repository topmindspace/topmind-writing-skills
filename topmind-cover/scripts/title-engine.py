#!/usr/bin/env python3
"""title-engine：多层花式标题合成器（封面双路径的「脚本叠字」高级版）。

用法：
  python3 scripts/title-engine.py <场景图> <spec.json> --out <封面.png> [--size 2480x992] [--list-fonts]

场景图先按 --size 居中裁剪 + LANCZOS 缩放（不给则保持原尺寸），再按 spec["layers"] 顺序逐层绘制。
坐标：x / y 用 0–1 小数表示画面比例，或用整数像素；anchor 取 lt / mm / rb 等（左中右 l m r × 上中下 t m b）。

图层类型（type）：
  text      文字块。字段：text, font, size, sizes[逐字字号], char_colors[逐字颜色], tracking, vertical,
            arc{radius}, wave{amp,period}, fill(颜色 | {gradient:[c1,c2,...],angle} | {texture:"concrete|metal|gold|scene|<图片>"}),
            strokes[[宽,色],...] 多重描边（由外到内）, extrude{depth,dx,dy,color,color_end} 3D 挤出,
            long_shadow{length,angle,color}, shadow{dx,dy,blur,color}, glow{color,radius,strength} 霓虹外发光,
            inner_glow{color,radius}, glitch{offset,colors,slices}, sticker{border,color,shadow},
            plate{color,pad,radius} 色块底板, highlight{color,height,offset} 高亮笔, underline{color,width,offset},
            rotate 角度, shear 斜切, perspective[[x,y]*4] 四角目标点（相对文字块宽高的比例，顺序 左上 右上 右下 左下）, opacity
  deco      装饰元件。kind: star | sparkle | arrow | burst | circle | stamp | tape | dots | lines；
            字段 x,y,size,color,rotate，arrow 用 points[[x,y]...]，burst/stamp 可带 text
  occlude   前景遮挡（主体压字）：mask 取 "rembg"（需 pip install rembg）、"luma>阈值"、"luma<阈值"、
            "sat>阈值"、或 polygon[[x,y]...]；region[x0,y0,x1,y1] 限定作用范围；把场景主体重新贴回最上层
字体别名见 FONTS（全部简体 SC / 中文字库）；--list-fonts 打印本机可用情况。
"""
import argparse, json, math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops, ImageOps

HOME = os.path.expanduser("~/.fonts/tm")
NOTO = "/usr/share/fonts/opentype/noto"
FONTS = {  # 别名: (候选文件, ttc 索引, 可变字重)
    "hei": ([f"{HOME}/NotoSansSC-VF.ttf", f"{NOTO}/NotoSansCJK-Bold.ttc"], 2, "Bold"),
    "hei-black": ([f"{HOME}/NotoSansSC-VF.ttf", f"{NOTO}/NotoSansCJK-Bold.ttc"], 2, "Black"),
    "hei-medium": ([f"{HOME}/NotoSansSC-VF.ttf", f"{NOTO}/NotoSansCJK-Regular.ttc"], 2, "Medium"),
    "hei-light": ([f"{HOME}/NotoSansSC-VF.ttf", f"{NOTO}/NotoSansCJK-Regular.ttc"], 2, "Light"),
    "song": ([f"{HOME}/NotoSerifSC-VF.ttf", f"{NOTO}/NotoSerifCJK-Bold.ttc"], 2, "Bold"),
    "song-black": ([f"{HOME}/NotoSerifSC-VF.ttf", f"{NOTO}/NotoSerifCJK-Bold.ttc"], 2, "Black"),
    "song-regular": ([f"{HOME}/NotoSerifSC-VF.ttf", f"{NOTO}/NotoSerifCJK-Regular.ttc"], 2, "Regular"),
    "kuaile": ([f"{HOME}/ZCOOLKuaiLe-Regular.ttf"], 0, None),
    "huangyou": ([f"{HOME}/ZCOOLQingKeHuangYou-Regular.ttf"], 0, None),
    "xiaowei": ([f"{HOME}/ZCOOLXiaoWei-Regular.ttf"], 0, None),
    "maobi": ([f"{HOME}/MaShanZheng-Regular.ttf"], 0, None),
    "wenkai": ([f"{HOME}/LXGWWenKai-Bold.ttf"], 0, None),
}
_fc = {}


def fail(m):
    print("错误：" + m, file=sys.stderr); sys.exit(1)


def font(name, size):
    key = (name, int(size))
    if key in _fc: return _fc[key]
    if os.path.isfile(str(name)):
        f = ImageFont.truetype(name, int(size), index=0)
    else:
        if name not in FONTS: fail(f"未知字体别名 {name}，可用：{', '.join(FONTS)}")
        paths, idx, w = FONTS[name]
        p = next((p for p in paths if os.path.isfile(p)), None)
        if not p: fail(f"字体 {name} 未安装（见 references/typography-system.md 字体安装）")
        f = ImageFont.truetype(p, int(size), index=idx if p.endswith(".ttc") else 0)
        if w and p.endswith("VF.ttf"):
            try: f.set_variation_by_name(w)
            except Exception: pass
    _fc[key] = f
    return f


def color(c, a=None):
    if isinstance(c, (list, tuple)): return tuple(c)
    c = c.lstrip("#")
    if len(c) == 6: c += "FF"
    t = tuple(int(c[i:i + 2], 16) for i in (0, 2, 4, 6))
    return t if a is None else t[:3] + (int(a),)


def P(v, total):
    return int(v * total) if isinstance(v, float) and abs(v) <= 2 else int(v)


# ---------- 字形布局 ----------
def glyph_mask(spec):
    text = spec["text"]; base = spec.get("size", 120)
    sizes = spec.get("sizes") or [base] * len(text)
    fname = spec.get("font", "hei")
    fonts = spec.get("fonts") or [fname] * len(text)
    track = spec.get("tracking", 0.04)
    cells = []
    for i, ch in enumerate(text):
        s = sizes[i % len(sizes)]; f = font(fonts[i % len(fonts)], s)
        w = f.getlength(ch) if ch != " " else s * 0.3
        im = Image.new("L", (int(s * 2), int(s * 2)), 0)
        # 基线对齐：每个字画在格子里同一基线位置（anchor="ls"），标点、数字不会被垂直居中
        ImageDraw.Draw(im).text((int(s * 0.5), int(s * 1.4)), ch, font=f, fill=255, anchor="ls")
        cells.append((ch, s, w, im))
    maxs = max(c[1] for c in cells)
    pad = int(maxs * 2)
    vertical = spec.get("vertical"); arc = spec.get("arc"); wave = spec.get("wave")
    total = sum(c[2] for c in cells) + track * maxs * (len(cells) - 1)
    W = int((total if not vertical else maxs) + pad * 2)
    H = int((maxs if not vertical else sum(c[1] for c in cells) * (1 + track)) + pad * 2 + (maxs * 2 if arc else 0))
    mask = Image.new("L", (W, H), 0); idx = Image.new("L", (W, H), 0)
    base_y = pad + maxs * 0.88  # 共同基线
    cur = 0
    for i, (ch, s, w, im) in enumerate(cells):
        ang = 0
        if vertical:
            ox = pad + (maxs - w) / 2 - s * 0.5; oy = pad + cur + s * 0.88 - s * 1.4; cur += s * (1 + track)
            cx, cy = ox + s * 0.5 + w / 2, oy + s * 1.4 - s * 0.38
        else:
            ox = pad + cur - s * 0.5; oy = base_y - s * 1.4
            cx, cy = pad + cur + w / 2, base_y - s * 0.38
            cur += w + track * maxs
            dy = 0
            if wave:
                ph = 2 * math.pi * i / wave.get("period", 4) + wave.get("phase", 0)
                dy = wave.get("amp", 0.15) * maxs * math.sin(ph); ang = wave.get("tilt", 0) * math.cos(ph)
            if arc:
                R = arc["radius"] * maxs; th = (cx - pad - total / 2) / R
                dy = R - R * math.cos(th); ang = -math.degrees(th)
                nx = pad + total / 2 + R * math.sin(th); ox += nx - cx; cx = nx
            oy += dy; cy += dy
        ang += (spec.get("jitter", 0) * (random.Random(i * 7 + 3).random() - 0.5) * 2)
        g = im.rotate(ang, resample=Image.BICUBIC, center=(cx - ox, cy - oy)) if ang else im
        mask.paste(255, (int(ox), int(oy)), g)
        idx.paste(i + 1, (int(ox), int(oy)), g.point(lambda v: 255 if v > 127 else 0))
    bb = mask.getbbox() or (0, 0, 1, 1)
    m = int(maxs * 0.9)
    box = (max(bb[0] - m, 0), max(bb[1] - m, 0), min(bb[2] + m, W), min(bb[3] + m, H))
    return mask.crop(box), idx.crop(box), maxs, (bb[0] - box[0], bb[1] - box[1], bb[2] - box[0], bb[3] - box[1])


# ---------- 填充 ----------
def texture(kind, size, scene=None):
    W, H = size; rng = np.random.default_rng(7)
    if kind == "scene" and scene is not None:
        return scene.resize(size).convert("RGBA")
    if os.path.isfile(str(kind)):
        return Image.open(kind).convert("RGBA").resize(size)
    if kind == "concrete":
        n = rng.normal(0, 1, (H // 4 + 1, W // 4 + 1))
        base = Image.fromarray(np.uint8(np.clip(185 + n * 18, 0, 255))).resize(size, Image.BICUBIC)
        fine = Image.fromarray(np.uint8(np.clip(rng.normal(0, 14, (H, W)) + 128, 0, 255)))
        a = np.asarray(base, float) + (np.asarray(fine, float) - 128) * 0.8
        pits = rng.random((H, W)) > 0.996
        a[pits] -= 70
        g = Image.fromarray(np.uint8(np.clip(a, 0, 255))).filter(ImageFilter.GaussianBlur(0.6))
        return Image.merge("RGBA", (g, g.point(lambda v: v * 0.98), g.point(lambda v: v * 0.94), Image.new("L", size, 255)))
    if kind in ("metal", "gold"):
        y = np.linspace(0, 1, H)[:, None]
        band = 0.55 + 0.45 * np.cos(y * 6.2 + 0.6) * np.cos(y * 2.1)
        streak = rng.normal(0, 0.04, (1, W))
        v = np.clip(band + streak, 0, 1)
        if kind == "gold":
            rgb = np.stack([255 * (0.55 + 0.45 * v), 200 * (0.4 + 0.6 * v), 80 * (0.2 + 0.8 * v)], -1)
        else:
            rgb = np.repeat((90 + 165 * v)[..., None], 3, -1)
        rgb = np.broadcast_to(rgb, (H, W, 3))
        return Image.fromarray(np.uint8(rgb)).convert("RGBA")
    fail(f"未知纹理 {kind}")


def gradient(cols, angle, size):
    W, H = size; a = math.radians(angle)
    yy, xx = np.mgrid[0:H, 0:W]
    t = (xx * math.cos(a) + yy * math.sin(a)); t = (t - t.min()) / max(t.max() - t.min(), 1)
    cs = [np.array(color(c), float) for c in cols]
    seg = t * (len(cs) - 1); i = np.clip(seg.astype(int), 0, len(cs) - 2); f = (seg - i)[..., None]
    out = np.zeros((H, W, 4))
    for k in range(len(cs) - 1):
        sel = (i == k)[..., None]
        out = np.where(sel, cs[k] * (1 - f) + cs[k + 1] * f, out)
    return Image.fromarray(np.uint8(out), "RGBA")


def fill_img(fill, size, scene, idx=None, char_colors=None):
    if isinstance(fill, dict) and "gradient" in fill:
        im = gradient(fill["gradient"], fill.get("angle", 90), size)
    elif isinstance(fill, dict) and "texture" in fill:
        im = texture(fill["texture"], size, scene)
        if fill.get("tint"):
            im = Image.blend(im, Image.new("RGBA", size, color(fill["tint"])), fill.get("tint_amount", 0.35))
    else:
        im = Image.new("RGBA", size, color(fill or "#FFFFFF"))
    if char_colors and idx is not None:
        a = np.asarray(idx)
        arr = np.array(im)
        for i, c in enumerate(char_colors):
            if c: arr[a == i + 1] = color(c)
        # 抗锯齿边缘：按最近字的颜色扩张
        im = Image.fromarray(arr)
    return im


def dilate(m, r):
    if r <= 0: return m
    return m.filter(ImageFilter.MaxFilter(int(r) * 2 + 1)) if r < 6 else m.filter(ImageFilter.GaussianBlur(r / 2)).point(lambda v: 255 if v > 20 else 0).filter(ImageFilter.GaussianBlur(0.8))


def solid(mask, c):
    im = Image.new("RGBA", mask.size, color(c)); a = ImageChops.multiply(im.getchannel("A"), mask); im.putalpha(a); return im


# ---------- 文字图层 ----------
def render_text(spec, scene):
    mask, idx, S, bb = glyph_mask(spec)
    W, H = mask.size
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    over = lambda im: out.alpha_composite(im)
    if spec.get("plate"):
        p = spec["plate"]; pad = P(p.get("pad", 0.18), S)
        d = ImageDraw.Draw(out)
        d.rounded_rectangle((bb[0] - pad, bb[1] - pad * 0.6, bb[2] + pad, bb[3] + pad * 0.6), P(p.get("radius", 0.15), S), fill=color(p["color"]))
    if spec.get("highlight"):
        h = spec["highlight"]; d = ImageDraw.Draw(out); hh = P(h.get("height", 0.38), S); off = P(h.get("offset", 0.05), S)
        y1 = bb[3] + off; d.polygon([(bb[0] - S * 0.08, y1 - hh), (bb[2] + S * 0.1, y1 - hh - S * 0.06), (bb[2] + S * 0.06, y1), (bb[0] - S * 0.04, y1 + S * 0.04)], fill=color(h["color"]))
    if spec.get("long_shadow"):
        ls = spec["long_shadow"]; L = P(ls.get("length", 0.5), S); a = math.radians(ls.get("angle", 45))
        acc = Image.new("L", (W, H), 0)
        for k in range(1, L, 2):
            acc = ImageChops.lighter(acc, ImageChops.offset(mask, int(k * math.cos(a)), int(k * math.sin(a))))
        over(solid(acc, ls.get("color", "#00000055")))
    if spec.get("shadow"):
        sh = spec["shadow"]; m = ImageChops.offset(dilate(mask, sum(s[0] for s in spec.get("strokes", [])) or 0), P(sh.get("dx", 0.04), S), P(sh.get("dy", 0.06), S))
        over(solid(m.filter(ImageFilter.GaussianBlur(P(sh.get("blur", 0.05), S))), sh.get("color", "#00000088")))
    if spec.get("glow"):
        g = spec["glow"]; r = P(g.get("radius", 0.18), S)
        for k, rr in enumerate([r, r // 2, r // 4 + 1]):
            gm = mask.filter(ImageFilter.GaussianBlur(rr)).point(lambda v: min(255, v * g.get("strength", 2.2)))
            over(solid(gm, g["color"]))
    if spec.get("sticker"):
        st = spec["sticker"]; b = P(st.get("border", 0.12), S); sm = dilate(mask, b)
        if st.get("shadow", True):
            over(solid(ImageChops.offset(sm, int(b * 0.5), int(b * 0.8)).filter(ImageFilter.GaussianBlur(b * 0.6)), "#00000066"))
        over(solid(sm, st.get("color", "#FFFFFF")))
    if spec.get("extrude"):
        ex = spec["extrude"]; dep = P(ex.get("depth", 0.18), S); dx, dy = ex.get("dx", 0.6), ex.get("dy", 1.0)
        c0, c1 = np.array(color(ex.get("color", "#333333")), float), np.array(color(ex.get("color_end", ex.get("color", "#111111"))), float)
        base = dilate(mask, spec.get("strokes", [[0]])[0][0] if spec.get("strokes") else 0)
        for k in range(dep, 0, -1):
            c = tuple(int(v) for v in c1 + (c0 - c1) * (1 - k / dep))
            over(solid(ImageChops.offset(base, int(k * dx), int(k * dy)), c))
    strokes = spec.get("strokes") or []
    tot = sum(s[0] for s in strokes)
    for w, c in strokes:
        over(solid(dilate(mask, P(tot, S) if isinstance(tot, float) else tot), c)); tot -= w
    fill = fill_img(spec.get("fill", "#FFFFFF"), (W, H), scene, idx, spec.get("char_colors"))
    face = fill.copy(); face.putalpha(ImageChops.multiply(fill.getchannel("A"), mask))
    if spec.get("bevel"):
        sh = ImageChops.subtract(mask, ImageChops.offset(mask, 3, 3)).filter(ImageFilter.GaussianBlur(1.5))
        hl = solid(sh, "#FFFFFF99"); face.alpha_composite(hl)
    if spec.get("glitch"):
        gl = spec["glitch"]; o = P(gl.get("offset", 0.04), S); cs = gl.get("colors", ["#FF2BD6", "#00F0FF"])
        over(solid(ImageChops.offset(mask, -o, 0), cs[0] + "CC" if len(cs[0]) == 7 else cs[0]))
        over(solid(ImageChops.offset(mask, o, 0), cs[1] + "CC" if len(cs[1]) == 7 else cs[1]))
    over(face)
    if spec.get("inner_glow"):
        ig = spec["inner_glow"]; edge = ImageChops.subtract(mask, mask.filter(ImageFilter.MinFilter(5))).filter(ImageFilter.GaussianBlur(P(ig.get("radius", 0.04), S)))
        over(solid(ImageChops.multiply(edge, mask), ig.get("color", "#FFFFFF")))
    if spec.get("glitch") and spec["glitch"].get("slices", 0):
        rng = random.Random(5); arr = np.array(out)
        for _ in range(spec["glitch"]["slices"]):
            y = rng.randrange(0, H - 4); h = rng.randrange(2, max(3, S // 10)); sx = rng.randrange(-S // 6, S // 6)
            arr[y:y + h] = np.roll(arr[y:y + h], sx, axis=1)
        out = Image.fromarray(arr)
    if spec.get("underline"):
        u = spec["underline"]; d = ImageDraw.Draw(out); y = bb[3] + P(u.get("offset", 0.12), S)
        d.line([(bb[0], y), (bb[2], y - S * 0.04)], fill=color(u["color"]), width=P(u.get("width", 0.07), S))
    return transform(out, spec), S


def transform(im, spec):
    if spec.get("shear"):
        k = spec["shear"]; W, H = im.size; extra = int(abs(k) * H)
        im = im.transform((W + extra, H), Image.AFFINE, (1, k, -extra if k > 0 else 0, 0, 1, 0), Image.BICUBIC)
    if spec.get("perspective"):
        import cv2
        bb = im.getbbox(); im = im.crop(bb); W, H = im.size
        pts = np.float32(spec["perspective"]) * np.float32([W, H])
        mnx, mny = pts.min(0); pts -= [mnx, mny]
        OW, OH = int(pts[:, 0].max()) + 2, int(pts[:, 1].max()) + 2
        M = cv2.getPerspectiveTransform(np.float32([[0, 0], [W, 0], [W, H], [0, H]]), pts)
        im = Image.fromarray(cv2.warpPerspective(np.array(im), M, (OW, OH), flags=cv2.INTER_CUBIC))
    if spec.get("rotate"):
        im = im.rotate(spec["rotate"], resample=Image.BICUBIC, expand=True)
    if spec.get("opacity") is not None:
        im.putalpha(im.getchannel("A").point(lambda v: int(v * spec["opacity"])))
    bb = im.getbbox()
    return im.crop(bb) if bb else im


# ---------- 装饰 ----------
def star_pts(cx, cy, r, n=5, inner=0.45, rot=-90):
    return [(cx + (r if i % 2 == 0 else r * inner) * math.cos(math.radians(rot + i * 180 / n)),
             cy + (r if i % 2 == 0 else r * inner) * math.sin(math.radians(rot + i * 180 / n))) for i in range(2 * n)]


def render_deco(d, cw, ch):
    s = P(d.get("size", 0.08), ch); col = color(d.get("color", "#FFD400")); oc = color(d.get("outline", "#141414"))
    k = d["kind"]; ow = max(2, s // 14)
    im = Image.new("RGBA", (s * 4, s * 4), (0, 0, 0, 0)); g = ImageDraw.Draw(im); c = s * 2
    if k == "star":
        g.polygon(star_pts(c, c, s), fill=col, outline=oc, width=ow)
    elif k == "sparkle":
        g.polygon(star_pts(c, c, s, 4, 0.18, -90), fill=col)
    elif k == "burst":
        g.polygon(star_pts(c, c, s * 1.5, d.get("points", 12), 0.72, -90), fill=col, outline=oc, width=ow)
        if d.get("text"):
            f = font(d.get("font", "huangyou"), int(s * d.get("text_scale", 0.62)))
            g.text((c, c), d["text"], font=f, fill=color(d.get("text_color", "#141414")), anchor="mm")
    elif k == "circle":
        for j in range(2):
            g.arc((c - s * 1.6 + j * 4, c - s + j * 3, c + s * 1.6 - j * 3, c + s - j * 2), 10 + j * 30, 350 + j * 15, fill=col, width=ow * 2)
    elif k == "stamp":
        g.rounded_rectangle((c - s, c - s, c + s, c + s), s // 6, outline=col, width=ow * 2)
        t = d.get("text", "精选"); f = font(d.get("font", "maobi"), int(s * (1.4 if len(t) <= 1 else 0.85 if len(t) <= 2 else 0.6)))
        if len(t) == 4:
            for i, chh in enumerate(t):
                g.text((c + (s * 0.45 if i < 2 else -s * 0.45), c + (-s * 0.45 if i % 2 == 0 else s * 0.45)), chh, font=f, fill=col, anchor="mm")
        else:
            g.text((c, c), t, font=f, fill=col, anchor="mm")
        a = np.array(im); rng = np.random.default_rng(3); holes = rng.random(a.shape[:2]) > 0.93; a[holes, 3] = a[holes, 3] // 3; im = Image.fromarray(a)
    elif k == "tape":
        g.rectangle((c - s * 1.5, c - s * 0.35, c + s * 1.5, c + s * 0.35), fill=col[:3] + (190,))
    elif k == "dots":
        for i in range(5):
            for j in range(3): g.ellipse((c - s + i * s * 0.45, c - s * 0.5 + j * s * 0.45, c - s + i * s * 0.45 + s * 0.15, c - s * 0.5 + j * s * 0.45 + s * 0.15), fill=col)
    elif k == "lines":
        for i in range(3):
            a = math.radians(-60 + i * 30); g.line((c + s * 0.4 * math.cos(a), c + s * 0.4 * math.sin(a), c + s * 1.3 * math.cos(a), c + s * 1.3 * math.sin(a)), fill=col, width=ow * 2)
    if k == "arrow":
        pts = [(P(x, cw), P(y, ch)) for x, y in d["points"]]
        lay = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); g = ImageDraw.Draw(lay)
        # 手绘曲线：二次贝塞尔
        (x0, y0), (x1, y1), (x2, y2) = pts[0], pts[1], pts[-1]
        curve = [((1 - t) ** 2 * x0 + 2 * (1 - t) * t * x1 + t * t * x2, (1 - t) ** 2 * y0 + 2 * (1 - t) * t * y1 + t * t * y2) for t in np.linspace(0, 1, 40)]
        g.line(curve, fill=col, width=d.get("width", max(4, ch // 120)), joint="curve")
        ang = math.atan2(y2 - curve[-4][1], x2 - curve[-4][0]); L = ch // 28
        for da in (2.6, -2.6):
            g.line([(x2, y2), (x2 + L * math.cos(ang + da), y2 + L * math.sin(ang + da))], fill=col, width=d.get("width", max(4, ch // 120)))
        return lay, (0, 0)
    if d.get("rotate"): im = im.rotate(d["rotate"], resample=Image.BICUBIC)
    return im, (P(d["x"], cw) - c, P(d["y"], ch) - c)


def place(canvas, im, x, y, anchor):
    W, H = canvas.size; w, h = im.size; x, y = P(x, W), P(y, H)
    ax = {"l": 0, "m": 0.5, "r": 1}[anchor[0]]; ay = {"t": 0, "m": 0.5, "b": 1}[anchor[1]]
    pos = (int(x - w * ax), int(y - h * ay)); canvas.alpha_composite(im, pos); return pos


def subject_mask(base, o):
    W, H = base.size; m = o.get("mask", "rembg")
    if isinstance(m, list) or o.get("polygon"):
        pm = Image.new("L", (W, H), 0); ImageDraw.Draw(pm).polygon([(P(x, W), P(y, H)) for x, y in (o.get("polygon") or m)], fill=255); out = pm
    elif m == "rembg":
        try:
            from rembg import remove, new_session
        except ImportError:
            fail("occlude 用 rembg 需要先 pip install rembg；或改用 luma/sat 阈值或 polygon")
        out = remove(base.convert("RGB"), only_mask=True, session=new_session(o.get("model", "u2net")))
    else:
        kind, thr = m[:-len(m.split(m[3])[-1]) - 1], float(m.split(m[3])[-1])
        hsv = base.convert("HSV"); ch = {"luma": base.convert("L"), "sat": hsv.getchannel("S")}[m[:4].strip("<>")]
        out = ch.point(lambda v: 255 if (v > thr if m[4] == ">" else v < thr) else 0)
    if o.get("region"):
        r = o["region"]; rm = Image.new("L", (W, H), 0); ImageDraw.Draw(rm).rectangle((P(r[0], W), P(r[1], H), P(r[2], W), P(r[3], H)), fill=255)
        out = ImageChops.multiply(out, rm)
    return out.filter(ImageFilter.GaussianBlur(o.get("feather", 1.2)))


def fit(im, size):
    W, H = size; iw, ih = im.size
    if iw / ih > W / H: nw = int(ih * W / H); x0 = (iw - nw) // 2; im = im.crop((x0, 0, x0 + nw, ih))
    else: nh = int(iw * H / W); y0 = (ih - nh) // 2; im = im.crop((0, y0, iw, y0 + nh))
    return im.resize(size, Image.LANCZOS)


HEAVY = ("extrude", "long_shadow", "glow", "inner_glow", "glitch", "bevel")
SHAPES = ("rotate", "shear", "perspective", "arc", "wave")
ROLE_MIN = {"main": 0.20, "sub": 0.09, "label": 0.06, "ornament": 0.045}  # 占画面高比例，见 references/design-system.md
CONTRAST_MIN = {"main": 3.0, "sub": 4.5, "label": 4.5, "ornament": 3.0}
SAFE_X, SAFE_Y = 0.05, 0.07


def role_of(l):
    if l.get("role"): return l["role"]
    sz = float(l.get("size", 0.2))
    return "main" if sz >= 0.2 else "sub" if sz >= 0.09 else "label"


def combo_check(spec):
    """静态检查：层级、字号下限、字体数量、特效克制、非水平处理须写理由、装饰数量。"""
    layers = spec.get("layers", [])
    texts = [l for l in layers if l.get("type", "text") == "text"]
    probs = []
    if not texts: return ["没有文字图层"]
    roles = [role_of(l) for l in texts]
    for l, r in zip(texts, roles):
        if r not in ROLE_MIN: probs.append(f"「{l.get('text')}」role 只能是 main / sub / label / ornament"); continue
        sizes = [float(x) for x in (l.get("sizes") or [l.get("size", 0.2)])]
        if min(sizes) < ROLE_MIN[r] - 1e-9:
            probs.append(f"「{l.get('text')}」({r}) 字号 {min(sizes):.3f} 低于下限 {ROLE_MIN[r]}（画面高比例）")
    if "main" not in roles: probs.append("缺主标题（role=main 或字号 ≥0.20）")
    if roles.count("ornament") > 1: probs.append("英文 / 装饰小字行最多 1 行")
    mains = [float(l.get("size", 0.2)) for l, r in zip(texts, roles) if r == "main"]
    subs = [float(l.get("size", 0.2)) for l, r in zip(texts, roles) if r == "sub"]
    if mains and subs and min(mains) / max(subs) < 1.6:
        probs.append(f"主标题与副标题字号比 {min(mains) / max(subs):.2f} < 1.6，层级不清")
    fonts = {l.get("font", "hei") for l in texts} | {f for l in texts for f in l.get("fonts", [])}
    if len(fonts) > 3: probs.append(f"字体 {len(fonts)} 种，超过 3 种（一主一辅，最多再加一种标签字体）")
    heavy = [l.get("text") for l in texts if any(l.get(k) for k in HEAVY)]
    if len(heavy) > 1: probs.append(f"重特效用在了 {len(heavy)} 个字块（{'、'.join(heavy)}），只能用在一个重点词上")
    shaped = [l for l in texts if any(l.get(k) for k in SHAPES)]
    for l in shaped:
        if not l.get("reason"): probs.append(f"「{l.get('text')}」做了旋转 / 斜切 / 透视 / 弧形，但没写 reason")
        if abs(float(l.get("rotate", 0))) > 12: probs.append(f"「{l.get('text')}」旋转 {l.get('rotate')}° 超过 12°")
    if len(shaped) > 2: probs.append("非水平处理超过 2 个字块，画面会乱")
    decos = [l for l in layers if l.get("type") == "deco"]
    if len(decos) > 2: probs.append(f"装饰元件 {len(decos)} 个，上限 2 个")
    return probs


def rel_lum(rgb):
    c = np.asarray(rgb, float) / 255
    c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def ratio(a, b):
    hi, lo = max(a, b), min(a, b); return (hi + 0.05) / (lo + 0.05)


def qa_layer(scene, im, pos, L, W, H):
    """渲染后检查：安全区 + 对比度。
    有底板 / 贴纸时比「字色 vs 底板色」；否则比「字（或描边外缘）vs 字下方场景」，取较大者（WCAG G18：描边可保对比）。"""
    role = role_of(L); probs = []
    x, y = pos; w, h = im.size
    if x < W * SAFE_X - 1 or y < H * SAFE_Y - 1 or x + w > W * (1 - SAFE_X) + 1 or y + h > H * (1 - SAFE_Y) + 1:
        probs.append(f"超出安全区（左右 {SAFE_X:.0%}、上下 {SAFE_Y:.0%}）")
    a = np.asarray(im.getchannel("A")); solid_ = a > 230
    if solid_.sum() < 20: return probs, None
    rgb = np.asarray(im.convert("RGB"))
    fill = L.get("fill", "#FFFFFF")
    cc = [c for c in (L.get("char_colors") or []) if c]
    fills = [rel_lum(np.array(color(c)[:3])) for c in ([fill] if isinstance(fill, str) else []) + cc]
    if not fills or not isinstance(fill, str):
        fi = np.asarray(fill_img(fill, (128, 128), scene).convert("RGB"))
        fills += [float(np.percentile(rel_lum(fi.reshape(-1, 3)), 20)), float(np.percentile(rel_lum(fi.reshape(-1, 3)), 80))]
    back = L.get("plate", {}).get("color") or L.get("sticker", {}).get("color") if (L.get("plate") or L.get("sticker")) else None
    if back:
        bl = [float(rel_lum(np.array(color(back)[:3])))]
    else:
        x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
        under = np.asarray(scene.convert("RGB").crop((x0, y0, x1, y1)))
        m = solid_[y0 - y:y1 - y, x0 - x:x1 - x]
        lum = rel_lum(under[m]) if m.sum() else rel_lum(under.reshape(-1, 3))
        bl = [float(np.percentile(lum, 10)), float(np.percentile(lum, 90))]  # 最差位置：最暗和最亮处都要过
    edge = solid_ & (np.asarray(Image.fromarray(np.uint8((~solid_) * 255)).filter(ImageFilter.MaxFilter(5))) > 0)
    el = float(np.median(rel_lum(rgb[edge]))) if L.get("strokes") and edge.sum() else None
    def worst(fl): return min(ratio(fl, b) for b in bl)
    cr = min(worst(f) for f in fills)
    if el is not None:
        cr = max(cr, worst(el))
        sw = sum(float(w_) * (H if float(w_) < 1 else 1) for w_, _ in L.get("strokes", []))
        if sw >= 2:  # 描边够粗时，字与描边的对比也算（WCAG G18 描边法）
            cr = max(cr, min(ratio(f, el) for f in fills))
    if cr < CONTRAST_MIN.get(role, 3.0):
        probs.append(f"对比度 {cr:.2f}:1 < {CONTRAST_MIN.get(role, 3.0)}:1")
    return probs, cr


def main():
    ap = argparse.ArgumentParser(description="多层花式标题合成")
    ap.add_argument("background", nargs="?"); ap.add_argument("spec", nargs="?")
    ap.add_argument("--out"); ap.add_argument("--size"); ap.add_argument("--list-fonts", action="store_true")
    ap.add_argument("--check", action="store_true", help="只显示静态设计建议，不出图；--strict 可将模板建议作为门禁")
    ap.add_argument("--strict", action="store_true", help="主动启用模板门禁：--check 有建议时退出 1；出图有设计建议时退出 2")
    a = ap.parse_args()
    if a.list_fonts:
        for k, (ps, _, w) in FONTS.items():
            p = next((p for p in ps if os.path.isfile(p)), None); print(f"{k:14s} {'OK ' + os.path.basename(p) if p else '缺失'} {w or ''}")
        return
    if a.check:
        path = a.spec or a.background
        if not path or not os.path.isfile(path): fail("--check 需要 spec.json")
        try: sp = json.load(open(path, encoding="utf-8"))
        except Exception as e: fail(f"spec 不是合法 JSON：{e}")
        if not isinstance(sp, dict) or not isinstance(sp.get("layers"), list) or not sp["layers"]:
            fail("spec 需要非空 layers 列表")
        if any(not isinstance(layer, dict) for layer in sp["layers"]):
            fail("layers 中每项需要是图层对象")
        probs = combo_check(sp)
        for m in probs: print("设计建议：" + m)
        print("设计检查（静态）：" + ("通过" if not probs else f"{len(probs)} 项建议，结合实际图判断")); sys.exit(1 if a.strict and probs else 0)
    if not (a.background and a.spec and a.out): fail("需要 <场景图> <spec.json> --out <输出>")
    if not os.path.isfile(a.background): fail(f"找不到场景图：{a.background}")
    try: spec = json.load(open(a.spec, encoding="utf-8"))
    except Exception as e: fail(f"spec 读取失败：{e}")
    if not isinstance(spec, dict) or not isinstance(spec.get("layers"), list) or not spec["layers"]: fail("spec 需要非空 layers 列表")
    if any(not isinstance(layer, dict) for layer in spec["layers"]): fail("layers 中每项需要是图层对象")
    base = Image.open(a.background).convert("RGBA")
    if a.size or spec.get("size"):
        w, h = map(int, (a.size or spec["size"]).lower().split("x")); base = fit(base, (w, h))
    W, H = base.size; canvas = base.copy(); scene = base.copy(); qa = []
    static = combo_check(spec)
    for L in spec["layers"]:
        t = L.get("type", "text")
        canvas_before = canvas.copy()
        if t == "text":
            L0 = L; L = dict(L); L["size"] = P(L.get("size", 0.2), H)
            if "sizes" in L: L["sizes"] = [P(s, H) for s in L["sizes"]]
            for k in ("strokes",):
                if k in L: L[k] = [[P(w_, H) if isinstance(w_, float) else w_, c] for w_, c in L[k]]
            im, _ = render_text(L, scene); pos = place(canvas, im, L.get("x", 0.06), L.get("y", 0.3), L.get("anchor", "lm"))
            role = role_of(L0)
            pr, cr = qa_layer(canvas_before, im, pos, L0, W, H)
            qa.append((L0.get("text"), role, cr, pr))
        elif t == "deco":
            im, pos = render_deco(L, W, H); canvas.alpha_composite(im, (int(pos[0]), int(pos[1]))) if im.size != (W, H) else canvas.alpha_composite(im)
        elif t == "occlude":
            m = subject_mask(base, L); canvas.paste(base, (0, 0), m)
        else:
            fail(f"未知图层类型 {t}")
    canvas.convert("RGB").save(a.out)
    print(f"已输出：{a.out}（{W}×{H}，{len(spec['layers'])} 层）")
    bad = list(static)
    for text, role, cr, pr in qa:
        print(f"  [{role}] {text}：对比度 {cr:.2f}:1" if cr else f"  [{role}] {text}")
        bad += [f"「{text}」{p}" for p in pr]
    for m in bad: print("设计建议：" + m)
    print("设计检查：" + ("通过" if not bad else f"{len(bad)} 项不达标"))
    if bad and a.strict: sys.exit(2)


if __name__ == "__main__":
    main()
