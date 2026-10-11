#!/usr/bin/env python3
"""md → X 长文可粘贴纯文本。

把 Markdown 原稿转成可直接粘贴进 X Article 编辑器的纯文本：
标题/正文保留，排版标记剥离，图片转为 [图N] 占位。

用法：
    python3 md2x.py <输入.md> --out <输出/X发布稿.txt>

规则见 references/x-format.md。
"""
import argparse
import re
import sys
from pathlib import Path

# --- 行内规则 ---------------------------------------------------------------

# markdown 转义：反斜杠 + ASCII 标点 → 标点本身（先占位保护，避免被 emphasis 误配对）
_UNESCAPE_RE = re.compile(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\\\]^_`{|}~])")
_PUA0, _PUA1 = "\ue000", "\ue001"

HR_RE = re.compile(r"^(\*(\s*\*){2,}|-(\s*-){2,}|_(\s*_){2,})\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
SETEXT_RE = re.compile(r"^=+\s*$")
TABLE_SEP_RE = re.compile(r"^:?-+:?$")
# 引用式定义：[label]: url "可选 title"（行首至多 3 空格）
REFDEF_RE = re.compile(r"^\s{0,3}\[([^\]]+)\]:\s*(\S+)(?:\s+[\"'(].*[\"')])?\s*$")


def _protect_escapes(s):
    """把反斜杠转义换成私有用区占位符，返回 (新串, 还原表)。"""
    store = []

    def repl(m):
        store.append(m.group(1))
        return f"{_PUA0}{len(store) - 1}{_PUA1}"

    return _UNESCAPE_RE.sub(repl, s), store


def _restore_escapes(s, store):
    def repl(m):
        return store[int(m.group(1))]

    return re.sub(f"{_PUA0}(\\d+){_PUA1}", repl, s)


def _parse_paren(s, j):
    """s[j] == '(' 时，找与之匹配的 ')'（括号可嵌套）。

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


def _split_url_title(inner):
    """把 `(url "title")` 括号内文本拆出 url（title 丢弃）。"""
    inner = inner.strip()
    m = re.match(r"^(\S+?)(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?$", inner)
    return m.group(1) if m else inner


def _replace_images(s, images, defs):
    """![alt](url) / ![alt][ref] → [图N]（alt 记入 images）。"""
    res = []
    i, n = 0, len(s)
    while i < n:
        if s.startswith("![", i):
            k = s.find("]", i + 2)
            if k == -1 or "]" in s[i + 2:k]:
                res.append(s[i])
                i += 1
                continue
            alt = s[i + 2:k]
            j = k + 1
            if j < n and s[j] == "(":
                parsed = _parse_paren(s, j)
                if not parsed:
                    res.append(s[i])
                    i += 1
                    continue
                j = parsed[1]  # url 允许为空；图片占位不依赖 url
            elif j < n and s[j] == "[":
                k2 = s.find("]", j + 1)
                if k2 == -1:
                    res.append(s[i])
                    i += 1
                    continue
                label = s[j + 1:k2] or alt  # [alt][] 省略式：label 取 alt
                if label.strip().lower() not in defs:
                    res.append(s[i])
                    i += 1
                    continue
                j = k2 + 1
            else:
                res.append(s[i])
                i += 1
                continue
            images.append(alt.strip())
            res.append(f"[图{len(images)}]")
            i = j
        else:
            res.append(s[i])
            i += 1
    return "".join(res)


def _replace_links(s, defs):
    """[文字](url) / [文字][ref] / [文字][] / [文字] → 文字（url）。"""
    # 1) 行内式：url 括号可嵌套
    res = []
    i, n = 0, len(s)
    while i < n:
        if s[i] == "[" and not (i > 0 and s[i - 1] == "!"):
            k = s.find("](", i + 1)
            if k != -1 and "]" not in s[i + 1:k]:
                parsed = _parse_paren(s, k + 1)
                if parsed:
                    url = _split_url_title(parsed[0])
                    if url:
                        res.append(f"{s[i + 1:k]}（{url}）")
                        i = parsed[1]
                        continue
        res.append(s[i])
        i += 1
    s = "".join(res)

    # 2) 引用式 [文字][label] / [文字][]（(?<!\!) 避免误伤残留的坏图片写法）
    def _ref(m):
        label = (m.group(2) or m.group(1)).strip().lower()
        url = defs.get(label)
        return f"{m.group(1)}（{url}）" if url else m.group(0)

    s = _INLINE_REF2_RE.sub(_ref, s)

    # 3) 快捷引用 [文字]（仅当 label 有定义时才转，避免误伤普通方括号）
    def _shortcut(m):
        url = defs.get(m.group(1).strip().lower())
        return f"{m.group(1)}（{url}）" if url else m.group(0)

    return _INLINE_REF1_RE.sub(_shortcut, s)


# _inline() 的行内模式：预编译在模块级，避免每行重复走 re 缓存查找
_INLINE_BI_RE = re.compile(r"\*\*\*(.+?)\*\*\*")   # 粗斜体
_INLINE_B_RE = re.compile(r"\*\*(.+?)\*\*")         # 加粗
_INLINE_BU_RE = re.compile(r"__(.+?)__")
_INLINE_I_RE = re.compile(r"\*(.+?)\*")            # 斜体
_INLINE_CODE_RE = re.compile(r"`(.+?)`")           # 行内代码
_INLINE_DEL_RE = re.compile(r"~~(.+?)~~")           # 删除线
_INLINE_TASK0_RE = re.compile(r"^(\s*)- \[ \]\s+")
_INLINE_TASK1_RE = re.compile(r"^(\s*)- \[x\]\s+", re.I)
_INLINE_REF2_RE = re.compile(r"(?<!\!)\[([^\]]+)\]\[([^\]]*)\]")
_INLINE_REF1_RE = re.compile(r"(?<!\!)\[([^\]]+)\]")


def _inline(s, defs):
    """行内标记剥离（用于正文行、标题文本、表格单元格）。"""
    s = _INLINE_BI_RE.sub(r"\1", s)  # 粗斜体
    s = _INLINE_B_RE.sub(r"\1", s)    # 加粗
    s = _INLINE_BU_RE.sub(r"\1", s)
    s = _INLINE_I_RE.sub(r"\1", s)    # 斜体
    s = _INLINE_CODE_RE.sub(r"\1", s)  # 行内代码
    s = _INLINE_DEL_RE.sub(r"\1", s)  # 删除线
    s = _replace_links(s, defs)       # 链接（行内式/引用式）
    s = _INLINE_TASK0_RE.sub(r"\1- ", s)  # 任务列表
    s = _INLINE_TASK1_RE.sub(r"\1- ", s)
    return s


def _strip_frontmatter(md):
    """去掉文首 frontmatter 块。块内非空行必须都含 ':'，否则视为正文（如文首分割线）。"""
    m = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(\r?\n|$)", md, flags=re.S)
    if m and all(not ln.strip() or ":" in ln for ln in m.group(1).splitlines()):
        return md[m.end():]
    return md


def convert(md: str):
    images = []
    defs = {}
    out_lines = []
    in_code = False
    fence_len = 0

    md, esc_store = _protect_escapes(md)
    md = _strip_frontmatter(md)

    # 先收集引用式定义（[label]: url），定义行不进正文
    body = []
    for raw in md.splitlines():
        m = REFDEF_RE.match(raw)
        if m:
            defs[m.group(1).strip().lower()] = m.group(2)
        else:
            body.append(raw)

    for raw in body:
        line = raw.rstrip()

        # 代码块：先处理围栏，块内行原样缩进（分割线规则不进代码块）。
        # 围栏反引号数 >= 3：```` 开栏只能由 >= 4 反引号闭合（CommonMark），
        # 否则 markdown 示例里的内层 ``` 会把外层栏提前"闭合"，造成静默错排。
        stripped = line.strip()
        if stripped.startswith("```"):
            k = 0
            while k < len(stripped) and stripped[k] == "`":
                k += 1
            if not in_code:
                in_code = True
                fence_len = k
            elif k >= fence_len and not stripped[k:].strip():
                in_code = False
                fence_len = 0
            else:
                # 栏内误写的短栏 / 带信息串的栏是代码内容，不是闭合栏
                out_lines.append("    " + line)
            continue
        if in_code:
            out_lines.append("    " + line)
            continue

        # 图片占位（行内式/引用式）
        line = _replace_images(line, images, defs)

        # 引用：剥掉所有层级的 >（放标题识别之前，引用内标题也能转）
        line = re.sub(r"^(>\s?)+", "", line)

        # 标题 → 纯文本行（标题内行文标记同样剥离）
        m = HEADING_RE.match(line)
        if m:
            out_lines.append("")
            out_lines.append(_inline(m.group(2).strip(), defs))
            out_lines.append("")
            continue

        # Setext 一级标题：上一行是正文则转为标题
        if SETEXT_RE.match(line):
            if out_lines and out_lines[-1].strip():
                text = out_lines.pop()
                out_lines.append("")
                out_lines.append(text)
                out_lines.append("")
            else:
                out_lines.append("")
            continue

        # 分割线（* * * / - - - / _ _ _ 允许空格）→ 空行
        if HR_RE.match(line):
            out_lines.append("")
            continue

        # 表格行 → "项：值" 列表（单元格内行文标记同样剥离）
        if "|" in line and line.strip().startswith("|"):
            raw_cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(TABLE_SEP_RE.match(c) for c in raw_cells):
                continue
            cells = [_inline(c, defs) for c in raw_cells]
            label = cells[0]
            rest = "，".join(c for c in cells[1:] if c)
            out_lines.append(f"{label}：{rest}" if rest else label)
            continue

        out_lines.append(_inline(line, defs))

    # 压缩 3+ 空行为 2 个；去首尾空行（只 strip 换行，保留首行缩进——文档可能以代码块开头）
    text = "\n".join(out_lines)
    text = re.sub(r"\n{3,}", "\n\n", text).lstrip("\n").rstrip() + "\n"

    # 文末附图注清单
    if images:
        text += "\n—— 配图清单 ——\n"
        for i, alt in enumerate(images, 1):
            text += f"[图{i}] {alt or '（未写图注）'}\n"

    return _restore_escapes(text, esc_store), images


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="输入 Markdown")
    ap.add_argument("--out", required=True, help="输出 X发布稿.txt")
    args = ap.parse_args()

    inp = Path(args.input)
    if not inp.is_file():
        if inp.is_dir():
            sys.exit(f"错误：输入是目录不是文件 {inp}")
        sys.exit(f"错误：找不到输入文件 {inp}")
    try:
        md = inp.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        sys.exit(f"错误：输入文件不是有效的 UTF-8 编码 {inp}")
    except OSError as e:
        sys.exit(f"错误：无法读取输入文件 {inp}（{e}）")
    text, images = convert(md)

    out = Path(args.out)
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    except OSError as e:
        sys.exit(f"错误：无法写入输出文件 {out}（{e}）")

    chars = len(text.replace("\n", ""))
    print(f"OK {out}")
    print(f"正文约 {chars} 字，配图 {len(images)} 张")


if __name__ == "__main__":
    main()
