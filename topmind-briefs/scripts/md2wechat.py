#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""md2wechat v2 — Markdown -> WeChat MP inline-style HTML.

Zero dependency (stdlib only). WeChat's rich text editor strips <style> blocks
and class attributes, so every style in the output is inlined.

Supported beyond CommonMark:
  - code syntax highlighting (inline span colors, no <style>)
  - ::: container blocks (note/tip/warn/danger/pull/dialogue/stat)
  - [!badge] inline tags, ==highlight==
  - footnote link mode (external links -> end-of-article index)
  - CJK "pangu" spacing between Han and Latin/digits
  - four heading-2 style variants

Usage:
    python3 md2wechat.py --input 稿.md --out-dir 交付包 --slug foo \
        --asset-root /path/to/repo [--theme theme.json] [--link-mode footnote] \
        [--embed-images]

Outputs:
    <out-dir>/<slug>-公众号版.html   full page, copy body section into WeChat
    <out-dir>/images/*               local image assets
    <out-dir>/diagrams/*             extracted mermaid sources (+ png if rendered)
    <out-dir>/图片上传清单.md         manual upload checklist

--embed-images: 把正文 <img> 的本地路径换成 base64 data URI。
公众号后台拿到相对路径或本地/内网地址时无法取图，粘贴过去图片会整段消失；
base64 内嵌后图片字节随剪贴板一起过去，粘贴即带图。images/ 仍照常导出，
作为「后台显示占位符时手动补传」的兜底。
"""

import argparse
import base64
import html
import json
import os
import re
import shutil
import subprocess
import sys

# ---------------------------------------------------------------- theme

DEFAULT_THEME = {
    "id": "md3-business-blue",
    "name": "MD3 商务蓝",
    "genre": ["通用", "商务", "AI/技术", "教程", "评测"],
    "accent": "#0B57D0",
    # accent 的浅化与淡化变体：下划线与浅底高亮都必须与主色同源，
    # 否则主题一换就会露出上一套主题的色（历史 bug：tech-blue 继承砖红 mark_bg）。
    "accent_light": "#7CACF8",
    "accent_soft": "#E8F0FE",
    "accent_container": "#D3E3FD",
    "text": "#1F1F1F",
    "text_strong": "#0B1F3A",
    "text_muted": "#5F6368",
    "text_light": "#80868B",
    "surface": "#F8FAFD",
    "surface_container": "#EDF2FA",
    "border": "#C4C7C5",
    "code_bg": "#1A1C1E",
    "code_text": "#E3E2E6",
    "c_note": "#7CACF8",
    "c_tip": "#146C2E",
    "c_warn": "#B06000",
    "c_danger": "#B3261E",
    "mark_bg": "#E8F0FE",
    "radius": "16px",
    "radius_small": "8px",
    "font_size": "16px",
    "line_height": "1.75",
    "para_gap": "24px",
    # 公众号只认 left / center / right，justify 会被判为非标准值
    "align": "left",
    "h2_style": "number",
    "toc": True,
    "toc_max": 5,
    "toc_min_h2": 4,
    "toc_min_chars": 2000,
    "table_max_cols": 3,
    "code_scheme": "mono",
    "img_border": "#E8F0FE",
    "font_stack": (
        "-apple-system,BlinkMacSystemFont,'Helvetica Neue',"
        "'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif"
    ),
    "mono_stack": "Menlo,Monaco,Consolas,'Courier New',monospace",
}

# Material Palenight derived, desaturated to survive on #2C2C2C
HIGHLIGHT = {
    "comment": "#6B7A8F",
    "string": "#C3E88D",
    "number": "#F78C6C",
    "keyword": "#C792EA",
    "builtin": "#FFCB6B",
    "func": "#82AAFF",
    "variable": "#FFCB6B",
    "op": "#89DDFF",
    "key": "#82AAFF",
    "punct": "#89DDFF",
    "flag": "#FFCB6B",
    "tag": "#F07178",
    "attr": "#FFCB6B",
    "add": "#C3E88D",
    "del": "#E58B7F",
    "meta": "#6B7A8F",
}

# ordered rules: earlier patterns win
LANG_RULES = {
    "python": [
        ("comment", r"#[^\n]*"),
        ("string", r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\''),
        ("keyword", r"\b(?:def|class|if|elif|else|for|while|return|import|from|as|try|except|finally|with|lambda|yield|pass|break|continue|in|is|not|and|or|None|True|False|self|async|await|raise|assert|global|del|match|case)\b"),
        ("builtin", r"\b(?:print|len|range|int|str|float|list|dict|set|tuple|open|enumerate|zip|map|filter|sum|min|max|abs|sorted|type|isinstance|super|getattr|setattr|hasattr)\b"),
        ("func", r"\b[A-Za-z_]\w*(?=\s*\()"),
        ("number", r"\b\d+\.?\d*\b"),
        ("op", r"[=+\-*/%<>!&|^~]+"),
    ],
    "js": [
        ("comment", r"//[^\n]*|/\*[\s\S]*?\*/"),
        ("string", r"`(?:\\.|[^`\\])*`|\"(?:\\.|[^\"\\\n])*\"|'(?:\\.|[^'\\\n])*'"),
        ("keyword", r"\b(?:const|let|var|function|return|if|else|for|while|class|extends|new|await|async|import|export|from|default|try|catch|finally|throw|typeof|instanceof|this|super|null|undefined|true|false|switch|case|break|continue|delete|in|of|yield|static|get|set)\b"),
        ("builtin", r"\b(?:console|JSON|Math|Object|Array|String|Number|Boolean|Promise|window|document|require|module|exports|process)\b"),
        ("func", r"\b[A-Za-z_$]\w*(?=\s*\()"),
        ("number", r"\b\d+\.?\d*\b"),
        ("op", r"[=+\-*/%<>!&|^~?:]+"),
    ],
    "json": [
        ("key", r'"(?:\\.|[^"\\])*"(?=\s*:)'),
        ("string", r'"(?:\\.|[^"\\])*"'),
        ("keyword", r"\b(?:true|false|null)\b"),
        ("number", r"-?\b\d+\.?\d*(?:[eE][+-]?\d+)?\b"),
        ("punct", r"[{}\[\],:]"),
    ],
    "bash": [
        ("comment", r"#[^\n]*"),
        ("string", r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''),
        ("variable", r"\$\w+|\$\{[^}]*\}"),
        ("keyword", r"\b(?:if|then|else|fi|for|in|do|done|while|case|esac|function|return|export|local|source)\b"),
        ("builtin", r"\b(?:npm|npx|node|python3?|pip3?|git|docker|curl|wget|vercel|mmdc|openssl|mkdir|cp|mv|rm|ls|cat|grep|sed|awk|trash|open|echo|cd|sudo|chmod|kill|ps|top)\b"),
        ("flag", r"(?<=\s)-{1,2}[\w-]+"),
        ("op", r"[|&;<>]+"),
    ],
    "yaml": [
        ("comment", r"#[^\n]*"),
        ("key", r"^\s*[\w.\-/]+(?=\s*:)"),
        ("string", r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''),
        ("keyword", r"\b(?:true|false|null|yes|no|on|off)\b"),
        ("number", r"\b\d+\.?\d*\b"),
        ("punct", r"[-:]"),
    ],
    "sql": [
        ("comment", r"--[^\n]*"),
        ("string", r"'(?:\\.|[^'\\])*'"),
        ("keyword", r"\b(?:SELECT|FROM|WHERE|INSERT|INTO|VALUES|UPDATE|SET|DELETE|CREATE|TABLE|ALTER|DROP|JOIN|LEFT|RIGHT|INNER|OUTER|ON|GROUP|BY|ORDER|LIMIT|OFFSET|AS|AND|OR|NOT|NULL|IS|IN|LIKE|COUNT|SUM|AVG|MAX|MIN|DISTINCT|INDEX|PRIMARY|KEY|DEFAULT|CASCADE|WITH|UNION|HAVING)\b"),
        ("number", r"\b\d+\.?\d*\b"),
        ("op", r"[=<>!*/+\-]+"),
    ],
    "diff": [
        ("meta", r"^@@[^\n]*|^---[^\n]*|^\+\+\+[^\n]*"),
        ("add", r"^\+[^\n]*"),
        ("del", r"^-[^\n]*"),
    ],
    "html": [
        ("comment", r"<!--[\s\S]*?-->"),
        ("string", r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''),
        ("tag", r"</?[A-Za-z][\w:.-]*|/?>"),
        ("attr", r"[\w:.-]+(?=\s*=)"),
        ("punct", r"[=]"),
    ],
    "css": [
        ("comment", r"/\*[\s\S]*?\*/"),
        ("keyword", r"@[\w-]+"),
        ("string", r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''),
        ("key", r"[\w-]+(?=\s*:)"),
        ("number", r"-?\b\d+\.?\d*(?:px|em|rem|%|vh|vw|s|ms)?\b|#[0-9a-fA-F]{3,8}"),
        ("punct", r"[{}\[\],;:]"),
    ],
}

LANG_ALIASES = {
    "javascript": "js", "jsx": "js", "typescript": "js", "ts": "js", "tsx": "js",
    "py": "python", "sh": "bash", "shell": "bash", "zsh": "bash", "console": "bash",
    "yml": "yaml", "xml": "html", "vue": "html", "scss": "css", "less": "css",
    "http": "json", "diff": "diff", "patch": "diff",
}


def build_code_scheme(theme):
    """按主题生成代码高亮色板。

    默认 mono：只用「主色 + 明暗层级」，不引入第二套色彩语言。
    历史问题：代码块固定用 Material Palenight 的 16 色（天蓝/蓝/绿/橙/紫），
    与砖红主题毫无关系，一篇文章里出现两套色板，读者会觉得是另一个号。
    """
    if theme.get("code_scheme") == "palenight":
        return dict(HIGHLIGHT)
    base = theme.get("code_text", "#E8E8E8")
    bg = theme.get("code_bg", "#2C2C2C")
    acc = mix_hex(theme.get("accent", "#A6524A"), "#FFFFFF", 0.34)
    dim = mix_hex(base, bg, 0.46)
    mid = mix_hex(base, bg, 0.20)
    return {
        "comment": dim, "meta": dim,
        "string": mid, "number": mid,
        "keyword": acc, "tag": acc, "del": acc,
        "builtin": base, "func": base, "variable": base,
        "op": mid, "key": mid, "punct": mid, "flag": mid,
        "attr": mid, "add": mid,
    }


def highlight(code, lang, scheme=None):
    """Inline-span syntax highlighting (no <style>, no class)."""
    key = LANG_ALIASES.get(lang, lang)
    rules = LANG_RULES.get(key)
    if not rules:
        return html.escape(code, quote=False)
    palette = scheme or CTX.get("hl_scheme") or HIGHLIGHT
    pattern = _HL_PATTERN_CACHE.get(key)
    if pattern is None:
        # (?m) 不能写进单个分支：拼成 alternation 后它就不在表达式开头了，
        # Python 会报 "global flags not at the start"（历史 crash：```yaml / ```diff
        # 代码块直接 Traceback）。MULTILINE 在编译期统一加，分支里只留 ^。
        pattern = re.compile("|".join("(?P<%s>%s)" % (name, pat) for name, pat in rules), re.S | re.M)
        _HL_PATTERN_CACHE[key] = pattern
    out = []
    pos = 0
    for m in pattern.finditer(code):
        if m.start() > pos:
            out.append(html.escape(code[pos:m.start()], quote=False))
        color = palette.get(m.lastgroup)
        text = html.escape(m.group(), quote=False)
        out.append('<span style="color:%s;">%s</span>' % (color, text) if color else text)
        pos = m.end()
    out.append(html.escape(code[pos:], quote=False))
    return "".join(out)


THEME_DIR = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "assets", "themes"))


def list_themes():
    """列出 assets/themes/ 下所有可用主题（按题材分主题的清单来源）。"""
    out = []
    if not os.path.isdir(THEME_DIR):
        return out
    for fn in sorted(os.listdir(THEME_DIR)):
        if not fn.endswith(".json"):
            continue
        path = os.path.join(THEME_DIR, fn)
        try:
            with open(path, encoding="utf-8") as fh:
                d = json.load(fh)
        except Exception:
            continue
        out.append({
            "file": path, "stem": fn[:-5],
            "id": d.get("id", fn[:-5]), "name": d.get("name", fn[:-5]),
            "genre": d.get("genre", []), "accent": d.get("accent", ""),
            "h2_style": d.get("h2_style", ""),
        })
    return out


def resolve_theme(spec):
    """把 --theme 的值解析成主题文件路径。

    支持三种写法，降低「按题材换主题」的使用门槛：
      1. 空串            -> 用 DEFAULT_THEME（不读文件）
      2. 主题名 / 标识   -> 在 assets/themes/ 里按 id、文件名、中文名匹配
      3. 文件路径        -> 直接读
    另有 "genre:题材" 语法按题材自动选主题（方案 B 的入口）。
    """
    if not spec:
        return None
    if os.path.exists(spec):
        return spec
    themes = list_themes()
    if spec.startswith("genre:"):
        want = spec.split(":", 1)[1].strip()
        for t in themes:
            if want in t["genre"]:
                return t["file"]
        raise SystemExit("没有主题声明题材「%s」。各主题题材见 references/theme-map.md" % want)
    low = spec.strip().lower()
    for t in themes:
        if low in (t["id"].lower(), t["stem"].lower(), t["name"].lower()):
            return t["file"]
    raise SystemExit("未知主题：%s\n可用主题：%s" % (
        spec, "、".join("%s(%s)" % (t["name"], t["id"]) for t in themes) or "（无）"))


def load_theme(spec):
    base = dict(DEFAULT_THEME)
    path = resolve_theme(spec)
    if not path:
        return base
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as e:
        # ValueError 覆盖 json.JSONDecodeError：坏掉的主题文件给干净报错，不抛 Traceback
        sys.exit("错误：主题文件无法解析 %s（%s）" % (path, e))
    accent = data.get("accent", base["accent"])
    # 主色派生字段必须按「本主题」的主色重算，不能继承默认主题的值：
    # 默认主题的 accent_light / mark_bg 是砖红系，继承过来会让蓝色或灰色主题里
    # 冒出砖红下划线和砖红高亮底——这正是 tech-blue 等主题当年从没被启用的原因。
    data.setdefault("accent_light", mix_hex(accent, "#FFFFFF", 0.62))
    data.setdefault("accent_soft", mix_hex(accent, "#FFFFFF", 0.92))
    data.setdefault("mark_bg", data["accent_soft"])
    theme = dict(base)
    theme.update(data)
    theme.setdefault("id", os.path.basename(path)[:-5])
    return theme


def mix_hex(a, b, ratio):
    """把 a 往 b 混 ratio 比例（0=全 a，1=全 b）。主题色派生用，避免手填出错。"""
    a = a.lstrip("#")
    b = b.lstrip("#")
    if len(a) != 6 or len(b) != 6:
        return "#" + a
    out = []
    for i in (0, 2, 4):
        va, vb = int(a[i:i + 2], 16), int(b[i:i + 2], 16)
        out.append("%02X" % int(round(va + (vb - va) * ratio)))
    return "#" + "".join(out)


# ---------------------------------------------------------------- inline

# shared render state, set once per convert() run
CTX = {
    "theme": DEFAULT_THEME,
    "link_mode": "footnote",
    "footnotes": [],
    "use_pangu": True,
}

CODE_TOKEN = "\x00C%d\x00"
HAN = r"\u4e00-\u9fff\u3400-\u4dbf"
HAN_RE = re.compile("[%s]" % HAN)
PANGU_A = re.compile(r"([%s])([A-Za-z0-9])" % HAN)
PANGU_B = re.compile(r"([A-Za-z0-9])([%s])" % HAN)

# render_inline() 的行内模式：预编译在模块级，避免每行重复走 re 缓存查找
# （666k 行级调用 × 10 个模式时，re.sub 的字符串模式查找是可观开销）。
INLINE_CODE_RE = re.compile(r"`([^`]+)`")


def _parse_paren(s, j):
    """s[j] == '(' 时找与之匹配的 ')'（括号可嵌套：URL 里允许出现平衡括号，如维基链接）。

    返回 (括号内文本, 右括号之后的位置)；括号不平衡返回 None。
    """
    depth = 0
    k, n = j, len(s)
    while k < n:
        c = s[k]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return s[j + 1:k], k + 1
        k += 1
    return None


# `(url)` / `(url "title")` / `(url 'title')` / `(url (title))` → url（title 丢弃）。
_URL_TITLE_RE = re.compile(r'^(\S+?)(?:\s+(?:"[^"]*"|\'[^\']*\'|\([^()]*\)))?\s*$')


def _split_url_title(inner):
    """把链接/图片括号内的 `url "title"` 拆出 url（title 丢弃）。

    裸 url 不得含空白：含裸空白时返回 ""（调用方保留原文，
    与旧正则 `[^)\\s]+` 的行为一致，不静默吞掉）。
    """
    m = _URL_TITLE_RE.match(inner.strip())
    return m.group(1) if m else ""


def _scan_md_links(text, img, repl):
    """扫描替换行内图片/链接，url 括号支持嵌套、可带 "title"。

    img=True 扫 ![alt](src)，False 扫 [label](url)；repl(文本, url) -> 替换串。
    括号不平衡、url 为空、url 含裸空白时保留原文（旧正则同样认不出这些写法，
    保留原文比截断 URL 更安全——历史 bug：`![a](img(1).png)` 被截成 `img(1`，
    文件明明存在却被记成缺失；`[维基](…/猫_(动物))` 的 URL 被截断、正文多个 `)`）。
    """
    open_tok = "![" if img else "["
    skip = len(open_tok)
    res = []
    i, n = 0, len(text)
    while i < n:
        if text.startswith(open_tok, i):
            k = text.find("]", i + skip)
            if k != -1 and k + 1 < n and text[k + 1] == "(":
                parsed = _parse_paren(text, k + 1)
                if parsed:
                    url = _split_url_title(parsed[0])
                    if url:
                        res.append(repl(text[i + skip:k], url))
                        i = parsed[1]
                        continue
        res.append(text[i])
        i += 1
    return "".join(res)
INLINE_BADGE_RE = re.compile(r"\[!([^\]]+)\]")
INLINE_HL_RE = re.compile(r"==([^=]+)==")
INLINE_UNDER_RE = re.compile(r"\+\+([^+]+)\+\+")
INLINE_U_RE = re.compile(r"&lt;u&gt;(.+?)&lt;/u&gt;")
INLINE_MARK_RE = re.compile(r"~~([^~]+)~~")
INLINE_STRONG_RE = re.compile(r"\*\*([^*]+)\*\*")
INLINE_EM_RE = re.compile(r"(?<![*\w])\*([^*\n]+)\*(?!\*)")

# highlight() 的语言联合模式缓存：同一语言的多段代码块只编译一次
_HL_PATTERN_CACHE = {}


def pangu(text):
    text = PANGU_A.sub(r"\1 \2", text)
    text = PANGU_B.sub(r"\1 \2", text)
    return text


def esc(text):
    return html.escape(text, quote=False)


def render_inline(raw):
    """Escape + markdown inline -> HTML with inline styles.

    Reads shared state from CTX so links/footnotes resolve across all
    block types (paragraphs, tables, lists, containers) uniformly.
    """
    theme = CTX["theme"]
    link_mode = CTX["link_mode"]
    footnotes = CTX["footnotes"]
    use_pangu = CTX["use_pangu"]
    spans = []

    def stash(code):
        spans.append(code)
        return CODE_TOKEN % (len(spans) - 1)

    text = esc(raw)
    text = INLINE_CODE_RE.sub(lambda m: stash(m.group(1)), text)

    if use_pangu:
        text = pangu(text)

    strong = 'font-weight:600;color:%s;' % theme["text_strong"]
    em = 'font-style:normal;color:%s;' % theme["text_muted"]

    # images（行内图与独立成行图共用同一括号语义）
    def img_repl(alt, src):
        # 行内图片同样走图片管线：本地文件解析 → 复制到 images/ → 登记清单，
        # 否则 --embed-images 找不到文件、清单漏项、计数为 0（历史 bug：
        # 段落里的 ![alt](x.png) 被原样保留相对路径，粘贴到公众号后整图消失）。
        resolver = CTX.get("img_resolve")
        if resolver and not re.match(r"^(https?:|data:|//)", src):
            src = resolver(html.unescape(src))
        caption = ' alt="%s"' % alt if alt else ""
        return ('<img src="%s"%s style="max-width:100%%;height:auto;'
                'border-radius:3px;vertical-align:middle;">') % (src, caption)

    text = _scan_md_links(text, True, img_repl)

    # links
    def link_repl(label, url):
        # 入口处已 esc()：先还原，插入点与脚注登记处再按需转义。
        # 否则脚注列表里 URL 的 & 会被 esc 两次、显示成 &amp;（历史 bug）。
        label, url = html.unescape(label), html.unescape(url)
        if link_mode == "footnote" and footnotes is not None:
            # url→序号字典：原写法每次链接都扫全表两次（O(n²)），长文链接多时明显变慢
            fidx = CTX.get("footnote_idx")
            if fidx is not None and url in fidx:
                idx = fidx[url]
            elif fidx is not None:
                footnotes.append({"url": url, "label": label})
                idx = len(footnotes)
                fidx[url] = idx
            else:  # 外部直接调 render_inline 且未初始化索引时，走原来的线性查找
                if url not in [f["url"] for f in footnotes]:
                    footnotes.append({"url": url, "label": label})
                idx = [f["url"] for f in footnotes].index(url) + 1
            return ('%s<sup style="font-size:11px;color:%s;'
                    'padding-left:1px;">[%d]</sup>'
                    % (esc(label), theme["accent"], idx))
        if link_mode == "inline":
            return ('%s<span style="font-size:13px;color:%s;">（%s）</span>'
                    % (esc(label), theme["text_light"], esc(url)))
        return ('<span style="font-size:13px;color:%s;word-break:break-all;">'
                '%s（%s）</span>' % (theme["text_light"], esc(label), esc(url)))

    text = _scan_md_links(text, False, link_repl)

    # badges: [!文本]
    # 不用 display:inline-block：公众号对非常规 display 值支持不稳定，
    # 徽章是纯行内元素，padding 足够撑开视觉。
    text = INLINE_BADGE_RE.sub(
        r'<span style="font-size:11px;line-height:1.6;'
        r'color:' + theme["accent"] + r';background:' + theme["accent_soft"] + r';'
        r'padding:1px 6px;border-radius:2px;margin:0 2px;'
        r'font-weight:600;">\1</span>',
        text,
    )

    # ==高亮== before bold so inner markup still works
    text = INLINE_HL_RE.sub(
        r'<strong style="font-weight:600;color:' + theme["text_strong"] + r';'
        r'background:' + theme["accent_soft"] + r';padding:1px 3px;'
        r'border-radius:2px;">\1</strong>',
        text,
    )

    # ++下划线++ / <u>下划线</u>：标记层（正文关键词标记），出现频率最高、
    # 权重介于加粗与高亮之间。esc() 已把 <u> 转义，故这里匹配实体。
    underline = ('<span style="border-bottom:2px solid %s;font-weight:600;'
                 'color:%s;">\\1</span>'
                 % (theme["accent_light"], theme["text_strong"]))
    text = INLINE_UNDER_RE.sub(underline, text)
    text = INLINE_U_RE.sub(underline, text)

    # ~~荧光笔~~：半高亮。用纯色浅底，不用 linear-gradient
    # （渐变在公众号会被静默丢弃，退化成无底）。
    text = INLINE_MARK_RE.sub(
        r'<span style="background:%s;font-weight:600;color:%s;">\1</span>'
        % (theme["accent_soft"], theme["text_strong"]),
        text,
    )

    text = INLINE_STRONG_RE.sub(r'<strong style="%s">\1</strong>' % strong, text)
    text = INLINE_EM_RE.sub(r'<em style="%s">\1</em>' % em, text)

    for idx, code in enumerate(spans):
        text = text.replace(
            CODE_TOKEN % idx,
            '<code style="background:%s;color:%s;padding:2px 5px;'
            'border-radius:3px;font-size:14px;font-family:%s;word-break:break-all;">%s</code>'
            % (theme["surface"], theme["accent"], theme["mono_stack"], code),
        )
    return text


# ---------------------------------------------------------------- blocks

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
# 围栏反引号数 >= 3：```` 开栏只能由 >= 4 反引号闭合（CommonMark），
# 否则 markdown 示例代码里的内层 ``` 会把外层栏提前"闭合"，造成静默错排。
FENCE_RE = re.compile(r"^(`{3,})(\w*)\s*$")
HR_RE = re.compile(r"^(-{3,}|\*{3,}|_{3,})\s*$")


def match_img_only(line):
    """独立成行图片：![alt](src) 独占一行（src 括号可嵌套、可带 title）。

    返回 (alt, src)，不是独立成行图片返回 None。
    与行内图片共用同一括号语义（_parse_paren + _split_url_title）。
    """
    if not line.startswith("!["):
        return None
    k = line.find("]", 2)
    if k == -1:
        return None
    j = k + 1
    if j >= len(line) or line[j] != "(":
        return None
    parsed = _parse_paren(line, j)
    if not parsed:
        return None
    src = _split_url_title(parsed[0])
    if not src or line[parsed[1]:].strip():
        return None
    return line[2:k], src
CAPTION_RE = re.compile(r"^\*(.+)\*\s*$")
TABLE_SEP_RE = re.compile(r"^\|?[\s:|-]+\|[\s:|-]*$")
CONTAINER_RE = re.compile(r"^:::+\s*(\w+)?\s*(.*)$")

CN_NUM = "一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾"

# 标题里手写的中文/阿拉伯序号。序号应由排版层生成（可换样式、可加引用），
# 写进标题文本后就变成了不可编程的字符串。这里统一剥离后重新编号。
# 注意：\d{1,2}[、.．](?!\d) 带负向断言，避免把「3.4× 成本」这类
# 以数字开头的标题误剥成「4× 成本」。
HAND_NUM_RE = re.compile(
    r"^(?:第\s*[" + CN_NUM + r"]{1,3}\s*[、.．]?\s*"
    r"|[" + CN_NUM + r"]{1,3}\s*[、.．]\s*"
    r"|\d{1,2}\s*[、.．](?!\d)\s*"
    r"|0\d\s+)"
)

# 末章若是收束类（总结/结语/小结…），编号改用 ∞ 而不是顺延的数字——
# 数字编号暗示「还有下一节」，收束章用数字会和读者预期打架。
# 只在 h2_style 含 number 时生效（其它样式本来就不输出编号）。
SUMMARY_H2_RE = re.compile(
    r"^(?:总结|结语|小结|尾声|后记|写在最后|写在后面|收尾|结尾|余论|结语与展望)"
)


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_list_item(line):
    return bool(re.match(r"^\s*([-*+]|\d+[.)])\s+", line))


def list_meta(line):
    m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", line)
    indent = len(m.group(1).replace("\t", "    ")) // 2
    return indent, m.group(2), m.group(3)


def para_style(theme):
    return ("margin:0 0 %s;line-height:%s;letter-spacing:0.5px;"
            "text-align:%s;word-break:break-word;"
            % (theme["para_gap"], theme["line_height"], theme["align"]))


def render_heading(level, text, theme, index=None):
    accent = theme["accent"]
    if level == 1:
        # 正文大标题不用 <h1>：微信对 h1 有「标题」语义映射，粘贴后字号/样式易被
        # 后台覆盖。改用 <p> + 内联样式，等价且稳（20px/700/居中）。
        return ('<p style="font-size:20px;font-weight:700;color:%s;'
                'text-align:center;margin:0 0 18px;line-height:1.5;'
                'letter-spacing:0.5px;">%s</p>'
                % (theme["text_strong"], render_inline(HAND_NUM_RE.sub("", text).strip() or text)))

    if level == 2:
        style = theme.get("h2_style", "number")
        # 先剥离手写序号，再按主题样式决定是否由排版层补编号
        plain = HAND_NUM_RE.sub("", text).strip() or text.strip()
        t = render_inline(plain)
        num = ""
        if "number" in style and index:
            # index 既可以是序号（int，渲染成 01/02），也可以是 ∞ 这类标记（str）
            label = ("%02d" % index) if isinstance(index, int) else str(index)
            num = ('<span style="color:%s;font-weight:700;margin-right:8px;'
                   'font-family:%s;">%s</span>'
                   % (accent, theme["mono_stack"], label))

        if style == "center":
            return ('<h2 style="font-size:18px;font-weight:700;color:%s;'
                    'text-align:center;margin:36px 0 18px;padding:12px 0;'
                    'line-height:1.5;border-top:1px solid %s;'
                    'border-bottom:1px solid %s;letter-spacing:1px;">%s%s</h2>'
                    % (theme["text_strong"], theme["border"], theme["border"],
                       num, t))
        if style == "underline":
            return ('<h2 style="font-size:18px;font-weight:700;color:%s;'
                    'margin:34px 0 16px;line-height:1.5;display:inline-block;'
                    'border-bottom:2px solid %s;padding-bottom:4px;">%s%s</h2>'
                    % (theme["text_strong"], accent, num, t))
        if style == "plain":
            return ('<h2 style="font-size:18px;font-weight:700;color:%s;'
                    'margin:34px 0 16px;line-height:1.5;'
                    'letter-spacing:0.5px;">%s%s</h2>'
                    % (theme["text_strong"], num, t))
        # number / bar：都走左竖条；number 额外带 01/02 编号
        return ('<h2 style="font-size:18px;font-weight:700;color:%s;'
                'margin:34px 0 16px;padding-left:11px;line-height:1.5;'
                'border-bottom:2px solid %s;padding-bottom:8px;">%s%s</h2>'
                % (theme["text_strong"], accent, num, t))

    if level == 3:
        t = render_inline(HAND_NUM_RE.sub("", text).strip() or text)
        return ('<h3 style="font-size:16px;font-weight:600;color:%s;'
                'margin:26px 0 12px;line-height:1.5;">%s</h3>'
                % (theme["text_strong"], t))
    t = render_inline(text)
    return ('<h4 style="font-size:15px;font-weight:600;color:%s;'
            'margin:22px 0 10px;line-height:1.5;">%s</h4>' % (theme["text"], t))


def render_code(code, lang, theme):
    body = highlight(code.rstrip("\n"), (lang or "").lower())
    # 语言标签用 <section> 不用 <div>：公众号新版编辑器底层是 ProseMirror，
    # 白名单里没有 div，div 包裹的块连同背景/内边距会被整段吞掉。
    label = ('<section style="font-size:11px;color:%s;padding:0 0 8px;'
             'letter-spacing:1px;font-weight:600;font-family:%s;">%s</section>'
             % (theme["accent"], theme["mono_stack"], esc(lang.upper()))
             if lang else "")
    # 不用 <pre>：公众号端 pre 不自动换行，窄屏会横向溢出。
    # 改用 section + pre-wrap + break-all，长行自动折行；缩进与换行由代码自身
    # 提供，HTML 源码里不在该 section 内插入任何格式化换行。
    return ('<section style="margin:0 0 %s;background:%s;border-radius:%s;'
            'padding:16px;">%s<section style="margin:0;'
            'white-space:pre-wrap;word-break:break-all;color:%s;font-size:13.5px;'
            'line-height:1.65;font-family:%s;">%s</section></section>'
            % (theme["para_gap"], theme["code_bg"], theme["radius"], label,
               theme["code_text"], theme["mono_stack"], body))


def render_quote(lines, theme):
    texts = []
    buf = []
    for line in lines:
        if not line.strip():
            if buf:
                texts.append(render_inline(" ".join(buf)))
                buf = []
            continue
        buf.append(line.strip())
    if buf:
        texts.append(render_inline(" ".join(buf)))
    parts = []
    for k, x in enumerate(texts):
        gap = "0" if k == len(texts) - 1 else "10px"
        parts.append('<p style="margin:0 0 %s;line-height:1.75;text-align:%s;'
                     'word-break:break-word;">%s</p>'
                     % (gap, theme["align"] or "left", x))
    # 用 <section> 而非 <blockquote>：公众号对 blockquote 有原生「引用」样式，
    # 可能覆盖我们设置的颜色与边框。section 样式完全自控。
    # MD3：无衬条（无 border-left/border-top），纯背景色调 + 大圆角区分层级。
    return ('<section style="margin:0 0 %s;padding:14px 16px;'
            'background:%s;border-radius:%s;'
            'color:%s;font-size:15px;">%s</section>'
            % (theme["para_gap"], theme["surface"],
               theme["radius"], theme["text"], "".join(parts)))


def render_paragraph(text, theme, tight=False, align=None):
    style = para_style(theme)
    if tight:
        style = style.replace("margin:0 0 %s;" % theme["para_gap"], "margin:0 0 10px;")
    if align:
        style += "text-align:%s;" % align
    return '<p style="%s">%s</p>' % (style, render_inline(text))


def render_list(items, theme, ordered, depth=0):
    tag = "ol" if ordered else "ul"
    style = ("margin:0 0 20px;padding-left:%dpx;line-height:%s;"
             % (26 if depth == 0 else 22, theme["line_height"]))
    if ordered:
        style += "list-style-type:decimal;"
    else:
        style += "list-style-type:disc;color:%s;" % theme["accent"]
    out = ["<%s style=\"%s\">" % (tag, style)]
    for item in items:
        line = '<li style="margin-bottom:9px;color:%s;">' % theme["text"]
        line += '<span style="color:%s;">%s</span>' % (theme["text"], item["text"])
        if item["children"]:
            line += render_list(item["children"], theme,
                                bool(item["children_ordered"]), depth + 1)
        line += "</li>"
        out.append(line)
    out.append("</%s>" % tag)
    return "".join(out)


def build_list(lines, theme, start=0):
    items = []
    root = {"indent": -1, "children": items, "ordered": False, "children_ordered": None}
    stack = [root]
    i = start
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            if i + 1 < len(lines) and is_list_item(lines[i + 1]):
                i += 1
                continue
            break
        if not is_list_item(line):
            if line.startswith("    ") or line.startswith("\t"):
                if items:
                    items[-1]["text"] += " " + line.strip()
                i += 1
                continue
            break
        indent, marker, content = list_meta(line)
        node = {
            "text": render_inline(content),
            "children": [],
            "children_ordered": None,
            "indent": indent,
            "ordered": not marker.startswith(("-", "*", "+")),
        }
        while stack and stack[-1]["indent"] >= indent:
            stack.pop()
        if not stack:
            stack = [root]
        parent = stack[-1]
        if parent["children_ordered"] is None:
            parent["children_ordered"] = node["ordered"]
        parent["children"].append(node)
        stack.append(node)
        i += 1

    ordered = bool(re.match(r"^\s*(\d+[.)])\s+", lines[start]))
    return render_list(items, theme, ordered), i


def render_table(rows, theme):
    """表格分流渲染。

    列数 <= table_max_cols：保留 <table>，但不加 table-layout:fixed，
    让列宽按内容自适应（fixed 会把各列均分，5 列在 677px 正文宽里每列仅 135px，
    中文被压成竖条）。
    列数更多：转卡片化，每行一张卡（首列作标题，其余「列名 + 值」成对），
    彻底摆脱横向溢出。公众号端列数 > 4 必然溢出，这是唯一稳的解法。

    另外：<thead>/<tbody>/<colgroup> 在公众号里不被支持，一律不输出。
    """
    cols = max(len(r) for r in rows)
    if cols > int(theme.get("table_max_cols", 3)):
        return render_table_cards(rows[0], rows[1:], theme)

    head = rows[0]
    # MD3 浅色表：表头浅蓝底 + 蓝色文字，无网格线；
    # 表头用一条蓝色底部分隔线强调，行与行之间用浅色底部分隔线。
    hcells = "".join(
        '<th style="background:%s;border-bottom:2px solid %s;padding:10px 12px;'
        'text-align:left;font-weight:600;color:%s;font-size:14px;'
        'line-height:1.55;word-break:break-word;">%s</th>'
        % (theme["accent_soft"], theme["accent"], theme["accent"],
           render_inline(c))
        for c in head
    )
    body_rows = "".join(
        "<tr>%s</tr>" % "".join(
            '<td style="border-bottom:1px solid %s;padding:10px 12px;color:%s;'
            'font-size:14px;line-height:1.6;word-break:break-word;">%s</td>'
            % (theme["border"], theme["text"], render_inline(c))
            for c in row
        )
        for row in rows[1:]
    )
    return ('<section style="margin:0 0 %s;">'
            '<table style="border-collapse:collapse;width:100%%;font-size:14px;">'
            '<tr>%s</tr>%s</table></section>'
            % (theme["para_gap"], hcells, body_rows))


def render_table_cards(head, body, theme):
    cards = []
    for row in body:
        if not row:
            continue
        title = render_inline(row[0]) if row else ""
        metas = []
        for k in range(1, len(row)):
            name = head[k] if k < len(head) else ""
            metas.append(
                '<p style="margin:0 0 6px;line-height:1.6;">'
                '<span style="font-size:12.5px;color:%s;">%s</span>'
                '<span style="font-size:14px;font-weight:600;color:%s;'
                'margin-left:8px;">%s</span></p>'
                % (theme["text_light"], render_inline(name),
                   theme["text_strong"], render_inline(row[k])))
        cards.append(
            '<section style="margin:0 0 12px;padding:13px 15px;background:%s;'
            'border-radius:%s;">'
            '<p style="margin:0 0 9px;font-size:15px;font-weight:600;color:%s;'
            'line-height:1.5;word-break:break-word;">%s</p>%s</section>'
            % (theme["surface"], theme["radius"],
               theme["accent"], title, "".join(metas)))
    return ('<section style="margin:0 0 %s;">%s</section>'
            % (theme["para_gap"], "".join(cards)))


def render_hr(theme):
    # 宽度用百分比：公众号端 px 固定值在不同屏宽下表现不一致。
    # 不用 display:inline-block：audit_inline 会把它判为 WARN，而这是生成器
    # 自己的输出、用户无从修复——自检永远带一条洗不掉的 WARN 等于没有自检。
    # 块级 section + margin:0 auto 居中，视觉与原来完全一致。
    return ('<section style="margin:32px 0;">'
            '<section style="width:12%%;height:2px;background:%s;'
            'margin:0 auto;"></section></section>' % theme["accent"])


def render_figure(src, caption, theme, alt=""):
    cap = ""
    if caption:
        cap = ('<p style="font-size:13px;color:%s;text-align:center;'
               'margin:9px 0 %s;line-height:1.6;">%s</p>'
               % (theme["text_light"], theme["para_gap"], render_inline(caption)))
    border = ""  # MD3 优雅：图片无边框，只保留圆角
    altattr = ' alt="%s"' % esc(alt) if alt else ""
    # 图片一律 max-width:100%，绝不用 width:100%：正文容器约 677px，
    # width:100% 会把 400px 的小截图强行拉满变糊，竖图更糟。
    # max-width 让大图缩到容器宽、小图保持原尺寸并居中。
    # 不用 <figure>：微信粘贴时可能剥离包裹导致图注错位，改 section + p。
    return ('<section style="margin:0 0 %s;">'
            '<p style="margin:0;text-align:center;">'
            '<img src="%s"%s style="max-width:100%%;height:auto;display:block;'
            '%sborder-radius:%s;margin:0 auto;"></p>%s</section>'
            % ("9px" if caption else theme["para_gap"], src, altattr, border,
               theme["radius"], cap))


# ---------------------------------------------------------------- containers

CONTAINER_KINDS = {
    "note": "note", "info": "note", "memo": "note",
    "tip": "tip", "success": "tip", "ok": "tip",
    "warn": "warn", "warning": "warn",
    "danger": "danger", "error": "danger",
    "pull": "pull", "quote": "pull", "golden": "pull",
    "dialogue": "dialogue", "chat": "dialogue", "talk": "dialogue",
    "stat": "stat", "data": "stat", "metric": "stat",
}

DEFAULT_LABELS = {
    "note": "说明", "tip": "提示", "warn": "注意", "danger": "警告",
}


def render_container(kind, label, inner_lines, theme):
    kind = CONTAINER_KINDS.get(kind, "note")
    text = "\n".join(inner_lines)

    if kind == "pull":
        # 金句块用 <section> 不用 <div>（div 会被公众号整段吞掉）。
        # MD3：无上下衬线，tonal 卡片（surface_container 比正文卡片深一阶）承载。
        return ('<section style="margin:28px 0;padding:20px 18px;'
                'background:%s;border-radius:%s;">'
                '<p style="margin:0;font-size:17px;line-height:1.85;color:%s;'
                'text-align:center;font-weight:600;letter-spacing:0.5px;'
                'word-break:break-word;">%s</p></section>'
                % (theme.get("surface_container", theme["surface"]),
                   theme["radius"],
                   theme["text_strong"], render_inline(text.strip())))

    if kind == "dialogue":
        rows = []
        for line in inner_lines:
            if not line.strip():
                continue
            m = re.match(r"^\s*(.{1,12}?)\s*[:：]\s*(.+)$", line)
            if m:
                name, say = m.group(1), m.group(2)
                rows.append(
                    '<p style="margin:0 0 6px;font-size:13px;color:%s;">%s</p>'
                    '<p style="margin:0 0 14px;padding:11px 14px;background:%s;'
                    'border-radius:%s;font-size:15px;line-height:1.72;'
                    'color:%s;">%s</p>'
                    % (theme["text_light"], render_inline(name),
                       theme["surface"], theme["radius"], theme["text"],
                       render_inline(say)))
            else:
                rows.append('<p style="margin:0 0 14px;padding:11px 14px;'
                            'background:%s;border-radius:%s;font-size:15px;'
                            'line-height:1.72;color:%s;">%s</p>'
                            % (theme["surface"], theme["radius"], theme["text"],
                               render_inline(line.strip())))
        return '<section style="margin:0 0 %s;">%s</section>' % (
            theme["para_gap"], "".join(rows))

    if kind == "stat":
        rows = []
        for line in inner_lines:
            if not line.strip() or "|" not in line:
                continue
            value, desc = line.split("|", 1)
            rows.append(
                '<p style="margin:0 0 14px;line-height:1.3;">'
                '<span style="font-size:26px;font-weight:700;color:%s;'
                'margin-right:10px;">%s</span>'
                '<span style="font-size:13px;color:%s;">%s</span></p>'
                % (theme["accent"], esc(value.strip()),
                   theme["text_light"], esc(desc.strip())))
        return '<section style="margin:0 0 %s;padding:16px 18px;' \
               'background:%s;border-radius:%s;">%s</section>' % (
                   theme["para_gap"], theme["surface"], theme["radius"],
                   "".join(rows))

    color = {"note": theme["c_note"], "tip": theme["c_tip"],
             "warn": theme["c_warn"], "danger": theme["c_danger"]}[kind]
    label_html = ""
    if label:
        # 标签用 <section> 不用 <div>
        label_html = ('<section style="font-size:12px;font-weight:600;color:%s;'
                      'letter-spacing:1px;margin-bottom:6px;">%s</section>'
                      % (color, esc(label)))
    body = []
    buf = []
    for line in inner_lines:
        if not line.strip():
            if buf:
                body.append(render_paragraph(" ".join(buf), theme, tight=True))
                buf = []
            continue
        buf.append(line.strip())
    if buf:
        body.append(render_paragraph(" ".join(buf), theme, tight=True))
    # MD3  tonal 卡片：无衬条，靠背景色调 + 大圆角区分层级；
    # 种类用标签文字颜色区分（note 蓝 / tip 绿 / warn 橙 / danger 红）。
    return ('<section style="margin:0 0 %s;padding:14px 16px;background:%s;'
            'border-radius:%s;">%s%s</section>'
            % (theme["para_gap"], theme["surface"], theme["radius"],
               label_html, "".join(body)))


# ---------------------------------------------------------------- images

def resolve_image(src, md_path, out_dir, assets, asset_root):
    if re.match(r"^https?://", src):
        assets.append({"src": src, "local": None, "remote": True})
        return src
    abs_path = os.path.normpath(os.path.join(os.path.dirname(md_path), src))
    if not os.path.exists(abs_path) and asset_root:
        rel = re.sub(r"^(\.\./)+", "", src)
        candidate = os.path.normpath(os.path.join(asset_root, rel))
        if os.path.exists(candidate):
            abs_path = candidate
    if not os.path.exists(abs_path):
        # 本地文件缺失：登记缺失记录再返回原 src（HTML 保留占位 <img>，
        # embed 会跳过并提示"未内嵌"，上传清单与计数也不会漏掉这一项）
        assets.append({"src": src, "local": None, "remote": False,
                       "missing": True})
        return src
    img_dir = os.path.join(out_dir, "images")
    try:
        os.makedirs(img_dir, exist_ok=True)
    except OSError as e:
        sys.exit("错误：无法创建图片目录 %s（%s）" % (img_dir, e))
    base = os.path.basename(abs_path)
    target = os.path.join(img_dir, base)
    n = 1
    while os.path.exists(target) and not os.path.samefile(abs_path, target):
        stem, ext = os.path.splitext(base)
        target = os.path.join(img_dir, "%s-%d%s" % (stem, n, ext))
        n += 1
    if not os.path.exists(target):
        try:
            shutil.copy2(abs_path, target)
        except OSError as e:
            sys.exit("错误：复制图片失败 %s → %s（%s）" % (abs_path, target, e))
    rel = os.path.relpath(target, out_dir)
    assets.append({"src": src, "local": rel, "remote": False,
                   "basename": os.path.basename(target),
                   "size": os.path.getsize(abs_path)})
    return rel


def handle_mermaid(code, out_dir, diagrams, theme, render):
    os.makedirs(os.path.join(out_dir, "diagrams"), exist_ok=True)
    idx = len(diagrams) + 1
    mmd = os.path.join(out_dir, "diagrams", "diagram-%02d.mmd" % idx)
    with open(mmd, "w", encoding="utf-8") as fh:
        fh.write(code)
    png = os.path.join(out_dir, "diagrams", "diagram-%02d.png" % idx)
    rel_png = os.path.relpath(png, out_dir)
    ok = False
    if render and shutil.which("mmdc"):
        try:
            subprocess.run(
                ["mmdc", "-i", mmd, "-o", png, "-b", "white", "-w", "1080"],
                check=True, capture_output=True, timeout=180,
            )
            ok = os.path.exists(png)
        except Exception:
            ok = False
    diagrams.append({"index": idx, "mmd": os.path.relpath(mmd, out_dir),
                     "png": rel_png if ok else None})
    if ok:
        return render_figure(rel_png, None, theme)
    note = ("［此处为流程图 %02d，公众号不支持 mermaid。请渲染 diagrams/%s 为图片后手动插入］"
            % (idx, os.path.basename(mmd)))
    return ('<section style="margin:0 0 %s;padding:14px 16px;'
            'background:%s;color:%s;'
            'font-size:14px;line-height:1.7;border-radius:%s;">%s</section>'
            % (theme["para_gap"], theme["surface"],
               theme["text_muted"], theme["radius"], esc(note)))


# ---------------------------------------------------------------- parser

def strip_frontmatter(lines):
    if lines and lines[0].strip() == "---":
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                return lines[idx + 1:]
    return lines


def convert_blocks(lines, md_path, out_dir, theme, ctx):
    out = []
    i = 0
    n = len(lines)
    h2_index = 0
    h2_titles = []
    toc_at = None  # 导读落点：首个正文段落之后

    # 预扫描：末章是否为收束类，决定它的编号用数字还是 ∞
    h2_texts = [HAND_NUM_RE.sub("", l.strip()[3:]).strip() or l.strip()[3:].strip()
                for l in lines if l.strip().startswith("## ")]
    h2_total = len(h2_texts)
    last_is_summary = bool(h2_total) and bool(SUMMARY_H2_RE.match(h2_texts[-1]))

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        m = FENCE_RE.match(stripped)
        if m:
            open_len = len(m.group(1))
            lang = m.group(2)
            i += 1
            buf = []
            while i < n:
                s2 = lines[i].strip()
                k = 0
                while k < len(s2) and s2[k] == "`":
                    k += 1
                # 闭合栏：反引号数 >= 开栏数且后面无其它字符（闭合栏可比开栏长）。
                # 带信息串的 ```python 不是闭合栏，是栏内代码——旧写法按
                # startswith("```") 判闭合，会把栏提前关掉。
                if k >= open_len and not s2[k:].strip():
                    break
                buf.append(lines[i])
                i += 1
            i += 1
            code = "\n".join(buf)
            if lang.lower() == "mermaid":
                out.append(handle_mermaid(code, out_dir, ctx["diagrams"], theme,
                                          ctx["render_mermaid"]))
            else:
                out.append(render_code(code, lang, theme))
            continue

        if HR_RE.match(stripped) and not is_list_item(line):
            out.append(render_hr(theme))
            i += 1
            continue

        m = HEADING_RE.match(stripped)
        if m:
            level = len(m.group(1))
            marker = h2_index
            if level == 2:
                h2_index += 1
                h2_titles.append(HAND_NUM_RE.sub("", m.group(2)).strip()
                                 or m.group(2).strip())
                marker = ("∞" if (last_is_summary and h2_index == h2_total)
                          else h2_index)
            out.append(render_heading(level, m.group(2).strip(), theme, marker))
            i += 1
            continue

        m = CONTAINER_RE.match(stripped)
        if m:
            kind = (m.group(1) or "note").lower()
            label = m.group(2).strip()
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith(":::"):
                buf.append(lines[i])
                i += 1
            if kind in ("toc", "目录", "导读"):
                out.append(TOC_TOKEN)
                i += 1
                continue
            if kind in ("sign", "signature", "签名"):
                out.append(SIGN_TOKEN)
                i += 1
                continue
            i += 1
            out.append(render_container(kind, label or DEFAULT_LABELS.get(
                CONTAINER_KINDS.get(kind, "note"), ""), buf, theme))
            continue

        if stripped.startswith("|") and i + 1 < n and TABLE_SEP_RE.match(lines[i + 1].strip()):
            rows = [split_row(stripped)]
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i].strip()))
                i += 1
            out.append(render_table(rows, theme))
            continue

        if stripped.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append(render_quote(buf, theme))
            continue

        if is_list_item(line):
            block_html, i = build_list(lines, theme, i)
            out.append(block_html)
            continue

        m = match_img_only(stripped)
        if m:
            caption = None
            if i + 1 < n:
                cm = CAPTION_RE.match(lines[i + 1].strip())
                if cm:
                    caption = cm.group(1)
                    i += 1
            src = resolve_image(m[1], md_path, out_dir,
                                ctx["assets"], ctx["asset_root"])
            out.append(render_figure(src, caption, theme, alt=m[0]))
            i += 1
            continue

        buf = [stripped]
        i += 1
        while i < n:
            cur = lines[i].strip()
            if (not cur or HEADING_RE.match(cur) or HR_RE.match(cur)
                    or CONTAINER_RE.match(cur) or cur.startswith(">")
                    or cur.startswith("|") or is_list_item(lines[i])
                    or match_img_only(cur) or FENCE_RE.match(cur)):
                break
            buf.append(cur)
            i += 1
        out.append(render_paragraph(" ".join(buf), theme))
        if toc_at is None:
            toc_at = len(out)

    # 自动导读：显式 ::: toc 优先。触发条件是「章节够多」或「正文够长」任一成立——
    # 只按字数会漏掉「1152 字 / 6 节」这类章节密集的短稿，只按章节数会漏掉
    # 「3 节 / 3000 字」这类长段落稿。
    if not any(x == TOC_TOKEN for x in out) and ctx.get("toc"):
        n_h2 = len(h2_titles)
        n_han = ctx.get("han_chars", 0)
        by_h2 = n_h2 >= int(theme.get("toc_min_h2", 4))
        by_len = n_h2 >= 3 and n_han >= int(theme.get("toc_min_chars", 2000))
        if by_h2 or by_len:
            out.insert(toc_at if toc_at is not None else 0, TOC_TOKEN)

    html = "".join(out)
    html = html.replace(TOC_TOKEN, render_toc(h2_titles, theme))
    return html


def convert(md_text, md_path, out_dir, theme, link_mode="footnote",
            render_mermaid=False, asset_root=None, use_pangu=True,
            toc=True, sign_mode="auto", author="", author_bio=""):
    lines = strip_frontmatter(md_text.split("\n"))
    han_chars = sum(len(HAN_RE.findall(l)) for l in lines)
    ctx = {"assets": [], "diagrams": [], "footnotes": [],
           "render_mermaid": render_mermaid, "asset_root": asset_root,
           "toc": bool(toc), "han_chars": han_chars,
           "sign_mode": sign_mode, "author": author, "author_bio": author_bio}
    CTX["theme"] = theme
    CTX["link_mode"] = link_mode
    CTX["footnotes"] = ctx["footnotes"]
    CTX["footnote_idx"] = {}
    CTX["use_pangu"] = use_pangu
    CTX["hl_scheme"] = build_code_scheme(theme)
    # 行内图片解析器：render_inline 里的 ![alt](src) 通过它走 resolve_image，
    # 与独立成行的图片共享「复制到 images/ + 登记清单」管线。
    abs_md = os.path.abspath(md_path)
    CTX["img_resolve"] = lambda s: resolve_image(
        s, abs_md, out_dir, ctx["assets"], ctx.get("asset_root"))

    body = convert_blocks(lines, md_path, out_dir, theme, ctx)

    # 尾部签名区。auto：稿件末尾已自带签名/CTA 就不重复生成（避免出现两处签名）。
    sign_html = render_signature(theme, author, author_bio)
    if SIGN_TOKEN in body:
        body = body.replace(SIGN_TOKEN, sign_html)
    elif sign_mode == "on":
        body += sign_html
    elif sign_mode == "auto" and not md_tail_has_signature(lines):
        body += sign_html

    if link_mode == "footnote" and ctx["footnotes"]:
        body += render_footnotes(ctx["footnotes"], theme)
    return body, ctx["assets"], ctx["diagrams"], ctx["footnotes"]


def render_footnotes(footnotes, theme):
    items = "".join(
        '<p style="margin:0 0 8px;font-size:13px;line-height:1.7;color:%s;'
        'word-break:break-all;">[%d] %s — %s</p>'
        % (theme["text_muted"], idx, esc(f["label"]), esc(f["url"]))
        for idx, f in enumerate(footnotes, 1)
    )
    # 标题用 <section> 不用 <div>
    return ('<section style="margin:34px 0 %s;padding:16px 18px;'
            'background:%s;border-radius:%s;">'
            '<section style="font-size:13px;font-weight:600;color:%s;'
            'letter-spacing:1px;margin-bottom:10px;">参考链接</section>%s</section>'
            % (theme["para_gap"], theme["surface"], theme["radius"],
               theme["text_strong"], items))


# ---------------------------------------------------------------- toc / signature

SIGN_RE = re.compile(
    r"点赞|在看|三连|点个关注|欢迎关注|关注「|扫码|分享给|我是[^。，,]{0,20}[，,]")

# 流式解析时还不知道全文有哪些 H2，先用占位符标记落点，收尾时统一替换
TOC_TOKEN = "\x01TOC\x01"
SIGN_TOKEN = "\x01SIGN\x01"


def md_tail_has_signature(lines, window=8):
    """稿件末尾是否已自带签名/CTA。自带则不再追加，避免出现两处签名区。"""
    tail = [l.strip() for l in lines if l.strip()][-window:]
    return any(SIGN_RE.search(l) for l in tail)


def render_toc(titles, theme):
    """前言导读。展示精选看点而非全量目录：超出 toc_max 时截断并注明总节数，
    不假装全文只有这几节。"""
    if not titles:
        return ""
    cap = int(theme.get("toc_max", 5))
    shown = titles[:cap]
    # 导读的标记必须跟正文标题一致：
    #  - 标题带编号（h2_style 含 number）→ 导读也用编号；末章收束类用 ∞，避免「导读 04 / 正文 ∞」
    #  - 标题不带编号（center/underline/plain）→ 导读只用中性圆点，不要凭空造出 01/02
    numbered = "number" in theme.get("h2_style", "number")
    last_summary = bool(titles) and bool(SUMMARY_H2_RE.match(titles[-1]))

    def label(k):
        if not numbered:
            return "·"
        return "∞" if (last_summary and k == len(titles)) else "%02d" % k

    rows = "".join(
        '<p style="margin:0 0 7px;font-size:14px;line-height:1.6;color:%s;'
        'word-break:break-word;">'
        '<span style="color:%s;font-weight:700;margin-right:8px;'
        'font-family:%s;">%s</span>%s</p>'
        % (theme["text"], theme["accent"], theme["mono_stack"], label(k),
           render_inline(t))
        for k, t in enumerate(shown, 1))
    more = ""
    if len(titles) > len(shown):
        more = ('<p style="margin:9px 0 0;font-size:12.5px;color:%s;">'
                '……共 %d 节</p>' % (theme["text_light"], len(titles)))
    return ('<section style="margin:0 0 26px;padding:15px 17px;background:%s;'
            'border-radius:%s;">'
            '<p style="margin:0 0 10px;font-size:12.5px;font-weight:600;'
            'color:%s;letter-spacing:1px;">本文看点</p>%s%s</section>'
            % (theme["surface"], theme["radius"],
               theme["accent"], rows, more))


def render_signature(theme, author="", bio=""):
    """尾部签名区。2026-10-01 起默认不再渲染"自我介绍"行（我是{{作者名}}，{{一句话简介}}）；
    只保留三连 CTA。author/bio 参数保留仅为兼容旧调用，不再使用。"""
    return ('<section style="margin:34px 0 0;padding:16px 18px;background:%s;'
            'border-radius:%s;">'
            '<p style="margin:0;font-size:14px;line-height:1.75;color:%s;'
            'word-break:break-word;">如果你觉得今天这篇有收获，欢迎'
            '<span style="font-weight:600;color:%s;">点赞、在看、转发</span>'
            '三连，我们下篇见。</p></section>'
            % (theme["surface"], theme["radius"],
               theme["text"], theme["accent"]))


# ---------------------------------------------------------------- embed

MIME_BY_EXT = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".svg": "image/svg+xml",
}


def embed_images_inline(body, out_dir):
    """把正文里指向本地文件的 <img src> 换成 base64 data URI。

    公众号后台会丢相对路径与本地地址：粘贴过去的 <img> 没有可抓取的 URL，
    整张图直接消失（连占位符都没有）。内嵌成 data URI 后，图片字节跟着
    剪贴板一起过去。远程 http(s) 图与已经是 data: 的图不动。
    返回 (新正文, 统计)。
    """
    stats = {"count": 0, "bytes": 0, "skipped": []}

    def repl(m):
        src = m.group(1)
        if re.match(r"^(https?:|data:|//)", src):
            return m.group(0)
        path = os.path.normpath(os.path.join(out_dir, src))
        mime = MIME_BY_EXT.get(os.path.splitext(path)[1].lower())
        if not mime or not os.path.exists(path):
            stats["skipped"].append(src)
            return m.group(0)
        with open(path, "rb") as fh:
            raw = fh.read()
        stats["count"] += 1
        stats["bytes"] += len(raw)
        return 'src="data:%s;base64,%s"' % (
            mime, base64.b64encode(raw).decode("ascii"))

    return re.sub(r'src="([^"]+)"', repl, body), stats


# ---------------------------------------------------------------- page

PAGE_TPL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
/* 仅本地预览用：公众号会剥离 style 标签，正文内联样式保持百分比宽度 */
body>div,body>article{{max-width:677px!important;margin-left:auto!important;
margin-right:auto!important;box-sizing:border-box;}}
</style>
</head>
<body style="margin:0;padding:24px 12px 64px;background:#EDEDED;font-family:{font_stack};">

<div style="max-width:100%;margin:0 auto 18px;padding:13px 18px;background:#FFF8E6;
border:1px solid #F0D9A8;border-radius:8px;font-size:13px;line-height:1.7;color:#7A5C1E;">
{notice}
</div>

<div style="max-width:100%;margin:0 auto 14px;display:flex;align-items:center;gap:10px;
flex-wrap:wrap;">
<button onclick="copyBody()" style="padding:9px 20px;font-size:14px;color:#fff;
background:{accent};border:none;border-radius:6px;cursor:pointer;">复制正文</button>
<span id="wx-tip" style="font-size:13px;color:#4A7A3A;"></span>
<span style="margin-left:auto;font-size:12px;color:#888;">{title}</span>
</div>

<div style="max-width:100%;margin:0 auto;padding:0 0 8px;font-size:12px;
color:#999;text-align:center;">↓ 正文开始 ↓</div>

<article id="wx-body" style="max-width:100%;margin:0 auto;padding:26px 20px 32px;
background:#FFFFFF;border:1px dashed #C9C9C9;border-radius:8px;
font-size:{font_size};color:{text};line-height:{line_height};
font-family:{font_stack};">
{body}
</article>

<script>
function copyBody() {{
  var node = document.getElementById('wx-body');
  var sel = window.getSelection();
  var range = document.createRange();
  range.selectNodeContents(node);
  sel.removeAllRanges();
  sel.addRange(range);
  try {{
    document.execCommand('copy');
    document.getElementById('wx-tip').textContent = '已复制，去公众号后台粘贴';
  }} catch (e) {{
    document.getElementById('wx-tip').textContent = '复制失败，请手动全选';
  }}
  sel.removeAllRanges();
}}
</script>
</body>
</html>
"""


def build_notice(embedded, n_images):
    """页顶「发布前须知」文案。内嵌模式与手动上传模式的说明不同。"""
    code = ('<code style="background:#F5F5F5;padding:1px 4px;border-radius:3px;">%s</code>')
    head = ("<strong>发布前须知</strong>：上方为操作提示，<strong>不要一起复制</strong>。"
            "请点「复制正文」或全选下方虚线框内容，粘贴到公众号后台编辑器。")
    if embedded:
        tail = ("<br>本页 %d 张图已 base64 内嵌，粘贴时会跟着一起过去，正常情况下"
                "无需再手动插图。若后台某张图显示为占位符，按 %s 的顺序，"
                "从 %s 手动补传这一张。"
                % (n_images, code % "图片上传清单.md", code % "images/"))
    else:
        tail = ("<br>图片需手动上传：本页图片仅供本地预览 —— 按 %s 的顺序"
                "逐张插入素材库。" % (code % "图片上传清单.md"))
    return head + tail


# audit_inline 的值级检查：原来是 8 次全正文 re.search（re.I 下每次都扫完整 MB 级
# body，大正文里 audit_inline 能占近一半耗时）。合并为一次单遍扫描：命中哪个分支
# 报哪条，收集命中的分支序号后按原列表顺序输出——与原来逐条 search 的结果完全一致。
_AUDIT_VALUE_PATTERNS = [
    ("linear-gradient", "ERROR", "linear-gradient（渐变被静默丢弃，退化成无背景。改纯色）"),
    ("box-shadow", "ERROR", "box-shadow（阴影被丢弃）"),
    ("rgba\\(|hsla\\(", "ERROR", "rgba()/hsla() 颜色（透明度不被支持，改纯色十六进制）"),
    ("var\\(--", "ERROR", "CSS 变量（不支持，值必须写死）"),
    ("@media|@keyframes", "ERROR", "@media/@keyframes（媒体查询与动画不被支持）"),
    ("\\sclass=", "ERROR", "class 属性（公众号会剥离，样式必须内联）"),
    ("\\sid=", "WARN", "id 属性（正文里无意义，可能被剥离）"),
    ("<img[^>]*width=\"", "WARN", "<img> 上的 width 属性（公众号不保证保留，宽度用内联 style）"),
]
_AUDIT_VALUE_RE = re.compile(
    "|".join("(?P<g%d>%s)" % (i, pat)
             for i, (pat, _lv, _msg) in enumerate(_AUDIT_VALUE_PATTERNS)),
    re.I,
)


def audit_inline(body):
    """正文的平台合规自检，返回 [(级别, 说明)]，空列表即通过。

    级别含义：
      ERROR —— 公众号会静默丢弃该样式或整段吞掉该标签，产物必然与预览不一致
      WARN  —— 转换后仍可读，但存在降级风险或移动端体验问题

    红线依据见 references/wechat-constraints.md，本函数是该文档的可执行版本。
    """
    issues = []

    def add(level, msg):
        issues.append((level, msg))

    # ---- 标签级：会被剥离或不被支持
    TAGS = [
        ("<div", "ERROR", "<div> 标签（新版编辑器白名单无 div，包裹的块连同背景/内边距会被整段吞掉，是「粘贴后样式全丢」的头号元凶。改 <section>）"),
        ("<figure", "ERROR", "<figure> 标签（粘贴时可能剥离包裹导致图注错位。用 <section>+<p>）"),
        ("<figcaption", "ERROR", "<figcaption> 标签（同上，图注改用独立 <p>）"),
        ("<pre", "ERROR", "<pre> 标签（公众号端不自动换行，窄屏横向溢出。用 <section>+pre-wrap）"),
        ("<thead", "ERROR", "<thead> 不被支持（去掉分组标签，表头行直接作为首个 <tr>）"),
        ("<tbody", "ERROR", "<tbody> 不被支持（同上）"),
        ("<colgroup", "ERROR", "<colgroup> 不被支持"),
        ("<h1", "ERROR", "<h1> 标签（微信按标题语义覆盖字号，正文大标题用 <p> + 内联样式）"),
        ("<iframe", "ERROR", "<iframe> 会被剥离（视频只能用公众号自带组件）"),
        ("<video", "ERROR", "<video> 会被剥离"),
        ("<script", "ERROR", "<script> 会被剥离"),
        ("<style", "ERROR", "<style> 会被剥离，样式必须内联"),
    ]
    for tag, lv, msg in TAGS:
        if tag in body:
            add(lv, msg)

    # ---- 属性/值级
    for m in re.finditer(r'style="([^"]*)"', body):
        decls = [d.strip() for d in m.group(1).split(";") if d.strip()]
        for decl in decls:
            prop, _, val = decl.partition(":")
            prop, val = prop.strip().lower(), val.strip()
            low = val.lower()
            if prop == "text-align" and val not in ("left", "center", "right"):
                add("ERROR", "text-align:%s 非标准值（只允许 left/center/right）" % val)
            elif prop in ("width", "max-width", "min-width") and "px" in low:
                add("ERROR", "%s:%s 固定像素宽度（不同屏宽下表现不一致，改百分比）" % (prop, val))
            elif prop == "white-space" and low in ("pre", "nowrap"):
                add("ERROR", "white-space:%s 不换行（窄屏溢出；折行用 pre-wrap）" % val)
            elif prop in ("position", "float", "transform", "opacity"):
                add("ERROR", "%s:%s 定位/透明属性（公众号会吞掉，元素错位）" % (prop, val))
            elif prop == "display" and low in ("flex", "grid"):
                add("ERROR", "display:%s（布局属性被吞，内容堆叠。用 <section>+padding 模拟）" % val)
            elif prop.startswith("-"):
                add("ERROR", "%s 私有属性（公众号不支持）" % prop)
            elif prop == "table-layout" and low == "fixed":
                add("WARN", "table-layout:fixed（各列宽度均分，小屏下中文被压成竖条；除非逐列显式设宽，否则去掉）")
            elif prop == "display" and low == "inline-block":
                add("WARN", "display:inline-block（非常规 display 值，公众号支持不稳定）")
            elif prop == "border-radius":
                add("WARN", "border-radius（圆角可能被丢弃，降级为直角；属可接受的优雅降级，勿依赖圆角做视觉区分）")

    hit = set()
    for m in _AUDIT_VALUE_RE.finditer(body):
        for i in range(len(_AUDIT_VALUE_PATTERNS)):
            if m.group("g%d" % i) is not None:
                hit.add(i)
                break
    for i in sorted(hit):
        _pat, lv, msg = _AUDIT_VALUE_PATTERNS[i]
        add(lv, msg)

    # ---- 图片宽度：小图被拉伸是高频问题
    for m in re.finditer(r'<img[^>]*style="([^"]*)"', body):
        st = m.group(1)
        if re.search(r"(?<!max-)(?<!min-)\bwidth:\s*100%", st) and "max-width" not in st:
            add("WARN", "图片用 width:100%（小图会被强行拉满变糊，改 max-width:100%;height:auto）")
            break

    # 去重（保留首次出现的级别）
    seen, out = {}, []
    for lv, msg in issues:
        if msg not in seen:
            seen[msg] = lv
            out.append((lv, msg))
    # ERROR 在前
    out.sort(key=lambda x: 0 if x[0] == "ERROR" else 1)
    return out


def atomic_write(path, text):
    """原子写文件：先写临时文件再 rename，写一半失败（磁盘满/断电）时
    不会留下半截产物——要么是旧文件，要么是没有文件，绝不残缺。"""
    tmp = path + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def write_manifest(out_dir, slug, title, assets, diagrams, theme, footnotes,
                   embedded=False):
    lines = ["# 图片上传清单 · %s" % title, ""]
    if embedded:
        lines.append("> 本页图片已 base64 内嵌，正常情况下粘贴到后台即带图。"
                     "若有图显示为占位符，再按此顺序逐张上传到素材库替换。")
    else:
        lines.append("> 公众号不会抓取本地图片，请在后台编辑器按此顺序逐张上传到素材库并插入正文。")
    lines.append("")
    if assets:
        lines.append("## 正文图片（按出现顺序）")
        lines.append("")
        lines.append("| 序号 | 文件名 | 体积 | 原 Markdown 引用 |")
        lines.append("|---|---|---|---|")
        for idx, a in enumerate(assets, 1):
            size = ""
            if a.get("size"):
                kb = a["size"] / 1024
                size = "%.0f KB" % kb if kb < 1024 else "%.1f MB" % (kb / 1024)
            if a.get("remote"):
                lines.append("| %d | %s（远程） | %s | `%s` |" % (idx, a["src"], size, a["src"]))
            elif a.get("missing"):
                lines.append("| %d | ⚠ 本地文件缺失：`%s` | — | `%s` |"
                             % (idx, a["src"], a["src"]))
            else:
                lines.append("| %d | `%s` | %s | `%s` |"
                             % (idx, a.get("basename") or "", size, a["src"]))
        lines.append("")
        lines.append("图片目录：`images/`（公众号单图建议 < 2 MB，宽度 1080 px 左右）")
        lines.append("")
    else:
        lines.append("## 正文图片")
        lines.append("")
        lines.append("_无_")
        lines.append("")
    lines.append("## 图表（mermaid）")
    lines.append("")
    if diagrams:
        lines.append("| 序号 | 源文件 | 已渲染 PNG |")
        lines.append("|---|---|---|")
        for d in diagrams:
            lines.append("| %d | `%s` | %s |" % (d["index"], d["mmd"],
                                                 ("`%s`" % d["png"]) if d["png"] else "未渲染"))
        lines.append("")
        lines.append("渲染：`mmdc -i diagrams/xx.mmd -o diagrams/xx.png -b white -w 1080`")
    else:
        lines.append("_无_")
    if footnotes:
        lines.append("")
        lines.append("## 参考链接（正文上标序号对应）")
        lines.append("")
        for idx, f in enumerate(footnotes, 1):
            lines.append("%d. %s — %s" % (idx, f["label"], f["url"]))
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("主题：%s · 点缀色 `%s` · 标题样式 `%s` · 代码色板 `%s`"
                 % (theme["name"], theme["accent"],
                    theme.get("h2_style", "number"),
                    theme.get("code_scheme", "mono")))
    path = os.path.join(out_dir, "图片上传清单.md")
    atomic_write(path, "\n".join(lines))
    return path


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    # 不设 required=True：--list-themes 需要能在不带输入文件时单独运行。
    # 必填校验放在下面手动做。
    ap.add_argument("--input", default="")
    ap.add_argument("--out-dir", default="")
    ap.add_argument("--slug", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--theme", default="",
                    help="主题：可传标识（tech-blue）、中文名（科技蓝）、JSON 路径，"
                         "或 genre:题材 按题材自动选（如 genre:评测）。留空用默认主题")
    ap.add_argument("--list-themes", action="store_true", help="列出所有可用主题后退出")
    ap.add_argument("--link-mode", default="footnote",
                    choices=["footnote", "note", "inline"])
    ap.add_argument("--asset-root", default="",
                    help="源仓库根目录，用于解析稿中 ../assets/ 形式的图片路径")
    ap.add_argument("--no-pangu", action="store_true", help="关闭中英文自动加空格")
    ap.add_argument("--render-mermaid", action="store_true")
    ap.add_argument("--embed-images", action="store_true",
                    help="把正文图片转成 base64 内嵌，粘贴到公众号时带图（推荐）")
    ap.add_argument("--no-toc", action="store_true",
                    help="不自动插入前言导读（默认 H2 >=4 个，或 H2 >=3 且正文 >=2000 中文字时插入）")
    ap.add_argument("--signature", default="auto", choices=["auto", "on", "off"],
                    help="尾部签名区：auto=稿件末尾已有签名则不重复生成（默认）")
    ap.add_argument("--author", default="", help="签名区署名；留空写 {{作者名}} 占位")
    ap.add_argument("--author-bio", default="", help="签名区一句话简介")
    args = ap.parse_args()

    if args.list_themes:
        for t in list_themes():
            print("%-14s %-10s %-9s %s" % (t["id"], t["name"], t["accent"],
                                           "、".join(t["genre"]) or "（未声明题材）"))
        return

    missing = [n for n, v in (("--input", args.input), ("--out-dir", args.out_dir),
                              ("--slug", args.slug)) if not v]
    if missing:
        sys.exit("缺少必填参数：%s" % "、".join(missing))

    if os.path.isdir(args.input):
        sys.exit("错误：输入是目录不是文件 %s" % args.input)
    if not os.path.isfile(args.input):
        sys.exit("错误：找不到输入文件 %s" % args.input)

    theme = load_theme(args.theme)
    try:
        with open(args.input, encoding="utf-8") as fh:
            md_text = fh.read()
    except UnicodeDecodeError:
        sys.exit("错误：输入文件不是有效的 UTF-8 编码 %s" % args.input)
    except OSError as e:
        sys.exit("错误：无法读取输入文件 %s（%s）" % (args.input, e))

    try:
        os.makedirs(args.out_dir, exist_ok=True)
    except OSError as e:
        sys.exit("错误：无法创建输出目录 %s（%s）" % (args.out_dir, e))
    body, assets, diagrams, footnotes = convert(
        md_text, os.path.abspath(args.input), args.out_dir, theme,
        args.link_mode, args.render_mermaid, args.asset_root or None,
        not args.no_pangu,
        toc=not args.no_toc, sign_mode=args.signature,
        author=args.author, author_bio=args.author_bio,
    )

    title = args.title
    if not title and md_text.startswith("---"):
        end = md_text.find("\n---", 3)
        fm = md_text[3:end] if end > 0 else ""
        m = re.search(r"^title:\s*(.+)$", fm, re.M)
        if m:
            title = m.group(1).strip().strip("\"'")
    if not title:
        for line in md_text.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip()
                break
    title = title or args.slug

    embed_stats = None
    if args.embed_images:
        body, embed_stats = embed_images_inline(body, args.out_dir)

    page = PAGE_TPL.format(
        title=esc(title), body=body, accent=theme["accent"],
        text=theme["text"], font_size=theme["font_size"],
        line_height=theme["line_height"], font_stack=theme["font_stack"],
        notice=build_notice(embed_stats is not None,
                            embed_stats["count"] if embed_stats else len(assets)),
    )
    html_path = os.path.join(args.out_dir, "%s-公众号版.html" % args.slug)
    atomic_write(html_path, page)

    manifest = write_manifest(args.out_dir, args.slug, title, assets, diagrams,
                              theme, footnotes, embed_stats is not None)

    plain = re.sub(r"<[^>]+>", "", body)
    print("HTML     : %s" % html_path)
    audit = audit_inline(body)
    errors = [m for lv, m in audit if lv == "ERROR"]
    warns = [m for lv, m in audit if lv == "WARN"]
    if errors or warns:
        print("合规自检 : %s（ERROR %d / WARN %d）"
              % ("✗ 未通过" if errors else "△ 通过但有提示", len(errors), len(warns)))
        for m in errors:
            print("   [ERROR] %s" % m)
        for m in warns[:8]:
            print("   [WARN ] %s" % m)
        if len(warns) > 8:
            print("   …… 另有 %d 条 WARN" % (len(warns) - 8))
    else:
        print("合规自检 : ✓ 无告警（标签/属性/宽度/对齐 全部通过）")
    print("清单     : %s" % manifest)
    if embed_stats:
        print("图片内嵌 : ✓ %d 张 / %.0f KB（base64 后约 %.1f MB）"
              % (embed_stats["count"], embed_stats["bytes"] / 1024,
                 embed_stats["bytes"] * 4 / 3 / 1024 / 1024))
        if embed_stats["skipped"]:
            print("           未内嵌：%s" % "、".join(embed_stats["skipped"]))
    print("主题     : %s（%s） / 标题样式 %s / 代码色板 %s"
          % (theme["name"], theme.get("id", "-"), theme.get("h2_style", "number"),
             theme.get("code_scheme", "mono")))
    print("图片     : %d 张（%d 远程）" % (len(assets), sum(1 for a in assets if a.get("remote"))))
    print("图表     : %d 个 mermaid" % len(diagrams))
    print("脚注     : %d 条" % len(footnotes))
    print("正文字数 : %d" % len(plain))


if __name__ == "__main__":
    sys.exit(main())
