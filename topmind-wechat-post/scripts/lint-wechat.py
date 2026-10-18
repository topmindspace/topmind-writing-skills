#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lint-wechat v2 — 公众号排版体检。

Checks a Markdown draft against WeChat MP readability constraints and
Chinese typography conventions. Zero dependency.

Usage:
    python3 lint-wechat.py --input 稿.md --asset-root /path/to/repo
    python3 lint-wechat.py --input 稿.md --fix      # auto-fix CJK spacing
    python3 lint-wechat.py --input 公众号稿.md --legacy   # 旧交付包：::: 容器只告警不报错

源稿里的 ::: 容器默认报错：长文是单源 Markdown，要能被任何编辑器和派生脚本读，
「金句/数据/提示」用普通段落、加粗或引用写。旧交付包加 --legacy 只读兼容。
"""

import argparse
import os
import re
import sys

sys.dont_write_bytecode = True  # 同目录模块不写 __pycache__
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import count_words as CW  # noqa: E402  字数口径与 count_words / de_ai_lint W14 一致

FENCE_RE = re.compile(r"^```(\w*)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)")
LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)")
CONTAINER_RE = re.compile(r"^:::+\s*(\w+)?")
CJK = re.compile(r"[\u4e00-\u9fff]")

# 与 md2wechat.py 的 CONTAINER_KINDS 保持一致，外加 toc/sign 两个结构容器。
# 拼错容器名会被静默降级成 note，这里显式报出来。
KNOWN_CONTAINERS = {
    "note", "info", "memo", "tip", "success", "ok",
    "warn", "warning", "danger", "error",
    "pull", "quote", "golden", "dialogue", "chat", "talk",
    "stat", "data", "metric",
    "toc", "目录", "导读", "sign", "signature", "签名",
}
HAN = r"\u4e00-\u9fff\u3400-\u4dbf"
PANGU_A = re.compile(r"([%s])([A-Za-z0-9])" % HAN)
PANGU_B = re.compile(r"([A-Za-z0-9])([%s])" % HAN)

# AI 腔 / 八股表达
AI_TONE = [
    (r"综上所述|总而言之|值得(注意|一提|记录|关注|单独)|不难看出|众所周知|显而易见", "八股过渡词"),
    (r"随着[^，。]{0,8}的发展|在当今[^，。]{0,6}(时代|社会)", "时代背景式开场"),
    (r"不仅仅?是[^，。]{0,12}，?更是", "「不仅是…更是」排比"),
    (r"不是[^，。]{1,12}，不是[^，。]{1,12}，而是", "三段式排比"),
    # 注意：不收「口径」（数据校验语境的官方口径/社区口径）与「对齐」（alignment），属专业用法
    (r"赋能|抓手|打法|颗粒度|底层逻辑|组合拳|护城河|生态位|闭环|沉淀(?![物池])|赛道|倒逼|复盘|卡位|生态化反", "互联网黑话"),
    (r"本质上|事实上|意味着|由此可见|换句话说|换言之|殊途同归|更进一步说", "AI 高频连接词"),
    (r"^(#|##|###)?\s*\*\*[^\*]{8,60}\*\*[：:]", "标题式加粗金句"),
    (r"(极其|非常|大大|十分|特别)(轻巧|优秀|出色|明显|强大)", "副词堆叠"),
]

# 段末加粗金句：整段被加粗且以句号结尾（AI 体典型收尾）
AI_BOLD_PUNCHLINE = re.compile(r"[。！？]\s*\*\*[^\n\*]{10,120}\*\*[。！？]?\s*$")

MAX_IMG_MB = 2.0
MAX_IMG_HARD_MB = 5.0


MD_LINK_RE = re.compile(r"!?\[([^\]]*)\]\([^)\s]*\)")
BARE_URL_RE = re.compile(r"https?://[^\s)\]|>]+")


def visual_len(text):
    """读者实际看到的视觉长度。

    关键点：URL 不算字数。链接只留显示文字——否则一个 60 字符的 URL 会把
    一个 40 字的清单项撑成「100 字超标」，链接速查章节会整片误报。
    """
    plain = MD_LINK_RE.sub(r"\1", text)
    plain = BARE_URL_RE.sub("", plain)
    plain = re.sub(r"[*_`>#|]", "", plain)
    cjk = len(CJK.findall(plain))
    latin = len(plain) - cjk
    return int(cjk + latin * 0.6)


def strip_frontmatter(lines):
    if lines and lines[0].strip() == "---":
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                return lines[idx + 1:], idx + 1
    return lines, 0


# ------------------------------------------------------------------ fix

PROTECT = [
    (re.compile(r"`[^`]+`"), "\x01"),                       # inline code
    (re.compile(r"\]\([^)\s]+\)"), "\x02"),                 # link/image targets
    (re.compile(r"https?://[^\s)\]]+"), "\x03"),            # bare urls
]


def pangu_line(line):
    slots = []

    def stash(m):
        slots.append(m.group(0))
        return "\x00%d\x00" % (len(slots) - 1)

    for pattern, _ in PROTECT:
        line = pattern.sub(stash, line)
    line = PANGU_A.sub(r"\1 \2", line)
    line = PANGU_B.sub(r"\1 \2", line)
    for idx, text in enumerate(slots):
        line = line.replace("\x00%d\x00" % idx, text)
    return line


def pangu_scan(line):
    """盘古之白检测：**必须先屏蔽与 pangu_line 相同的保护段**。

    否则图片/链接目标里的中文会被误报：文件名出现 `Argon官方` 这类中英混排片段时，
    会被当成缺空格命中 PANGU_B，而 --fix 保护的正是这一段、根本不会改它 ——
    告警永远清不掉，用户会以为正文不合规。检测与修复必须用同一套屏蔽规则。
    """
    masked = line
    for pattern, _ in PROTECT:
        masked = pattern.sub("\x00", masked)
    return bool(PANGU_A.search(masked) or PANGU_B.search(masked))


def fix_cjk(path, dry_run=False):
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    _, fm_end = strip_frontmatter(lines)

    in_fence = False
    changed = []
    for idx, line in enumerate(lines):
        if FENCE_RE.match(line.strip()):
            in_fence = not in_fence
            continue
        if in_fence or idx <= fm_end:
            continue
        new = pangu_line(line)
        if new != line:
            changed.append((idx + 1, line, new))
            lines[idx] = new

    if not dry_run and changed:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
    return changed


# ------------------------------------------------------------------ lint

def lint(path, max_para, max_item, asset_root=None, legacy=False):
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    # fm_off：frontmatter 占掉的行数。所有报出的行号必须加回它，
    # 否则行号比编辑器里看到的小，无法与 lint_x_post.py --md 等工具的定位对照。
    lines, fm_off = strip_frontmatter(raw.split("\n"))

    errors, warns, info = [], [], []
    base = os.path.dirname(os.path.abspath(path))

    in_fence = False
    para_buf, para_start = [], 0
    prev_level = 0
    consecutive = 0
    total_chars = 0
    strong_chars = 0
    h1_count = 0
    cjk_missing = 0
    headings = []
    # 单源长文是纯 Markdown：不建议、也不统计 ++下划线++ 这类扩展标记的覆盖率。
    # 已有的 ++x++ / <u> / ~~x~~ / ==x== 只做兼容读取（md2wechat 照常渲染），计入强调占比。
    body_paras = 0      # 正文段落数（真正的段落，不含标题/列表/引用/表格/代码）
    bold_count = 0      # 加粗处数（只在摘要里显示，不设上限）

    # 「全部链接速查」这类章节是纯链接清单，条目长是天然的，不参与长度检查
    LINK_DUMP_RE = re.compile(r"(全部链接|链接速查|参考链接|参考资料|延伸阅读)")
    in_link_dump = False
    in_container = False

    def flush_para(end_line):
        nonlocal para_buf, para_start, body_paras
        if not para_buf:
            return
        if in_link_dump:
            para_buf = []
            return
        text = " ".join(para_buf).strip()
        body_paras += 1
        length = CW.count_text(text)["longest_paragraph"]
        if length > max_para * 1.8:
            errors.append("L%d 段落过长（%d 字，约 %d 行手机屏）：%s…"
                          % (para_start + 1 + fm_off, length,
                             round(length / 28, 1), text[:28]))
        elif length > max_para:
            warns.append("L%d 段落偏长（%d 字），建议拆成两段：%s…"
                         % (para_start + 1 + fm_off, length, text[:28]))
        para_buf = []

    for idx, line in enumerate(lines):
        stripped = line.strip()

        if FENCE_RE.match(stripped):
            in_fence = not in_fence
            flush_para(idx)
            continue
        if in_fence:
            continue

        cm = CONTAINER_RE.match(stripped)
        if cm:
            flush_para(idx)
            kind = (cm.group(1) or "").strip().lower()
            if kind and not legacy:
                errors.append("L%d 源稿里用了 `::: %s` 容器：单源长文不用容器，改成普通段落、加粗或引用"
                              "（旧交付包加 --legacy 只告警）" % (idx + 1 + fm_off, kind))
            if kind:
                if kind not in KNOWN_CONTAINERS:
                    warns.append("L%d 未知容器 `::: %s`（会被当成 note 渲染）："
                                 "可用 %s"
                                 % (idx + 1 + fm_off, kind,
                                    "、".join(sorted(c for c in KNOWN_CONTAINERS if c.isascii()))))
                in_container = True
            else:
                in_container = False
            continue

        # 容器体内的数据行（如 ::: stat 的三行）是组件内容，不是正文段落。
        # 不排除的话段落数和强调占比的分母会虚高。
        if in_container:
            total_chars += visual_len(stripped)
            continue

        # 分隔线同样不是正文段落：一份 8 条 --- 的稿子会平白多出 8 个分母
        if re.match(r"^(-{3,}|\*{3,}|_{3,})\s*$", stripped):
            flush_para(idx)
            continue

        m = HEADING_RE.match(stripped)
        if m:
            flush_para(idx)
            level = len(m.group(1))
            title = m.group(2).strip()
            if level == 1:
                h1_count += 1
            else:
                headings.append((level, title))
            if level <= 2:
                in_link_dump = bool(LINK_DUMP_RE.search(title))
            if prev_level and level > prev_level + 1:
                warns.append("L%d 标题跳级 h%d → h%d：%s"
                             % (idx + 1 + fm_off, prev_level, level, stripped[:30]))
            prev_level = level
            consecutive += 1
            if consecutive > 2:
                warns.append("L%d 连续 %d 个标题无正文，建议合并或补过渡段"
                             % (idx + 1 + fm_off, consecutive))
            continue
        consecutive = 0

        total_chars += visual_len(stripped)
        # 强调总量 = 加粗 + 兼容读取的扩展标记（++x++ / ~~x~~ / ==x== / <u>）。
        bold = re.findall(r"\*\*([^*]+)\*\*", stripped)
        marked = (re.findall(r"\+\+([^+]+)\+\+", stripped)
                  + re.findall(r"~~([^~]+)~~", stripped)
                  + re.findall(r"==([^=]+)==", stripped)
                  + re.findall(r"<u>(.*?)</u>", stripped))
        bold_count += len(bold)
        strong_chars += sum(len(re.findall(r"[*\u4e00-\u9fffA-Za-z0-9]", s))
                            for s in bold + marked)

        if pangu_scan(stripped):
            cjk_missing += 1

        if not stripped:
            flush_para(idx)
            continue

        if re.match(r"^\s*([-*+]|\d+[.)])\s+", line) and not line[:1].isspace():
            flush_para(idx)
            item = re.sub(r"^\s*([-*+]|\d+[.)])\s+", "", line)
            length = visual_len(item)
            j = idx + 1
            while j < len(lines) and lines[j].strip() and lines[j][:1].isspace():
                length += visual_len(lines[j].strip())
                j += 1
            if length > max_item and not in_link_dump:
                warns.append("L%d 列表项偏长（%d 字，含续行），建议拆成多项或改成段落：%s…"
                             % (idx + 1 + fm_off, length, item[:26]))
            continue

        if stripped.startswith(">") or stripped.startswith("|"):
            flush_para(idx)
            continue

        if re.match(r"^!\[[^\]]*\]\([^)]+\)\s*$", stripped):
            flush_para(idx)
            continue

        if not para_buf:
            para_start = idx
        para_buf.append(stripped)

    flush_para(len(lines))

    if h1_count > 1:
        warns.append("正文有 %d 个 H1，公众号标题在后台单独填写，正文应只保留 1 个主标题"
                     % h1_count)

    if cjk_missing:
        warns.append("中英文/数字之间缺空格（盘古之白）约 %d 处，用 --fix 自动修复"
                     % cjk_missing)

    # 不再检查「标记覆盖率」和「加粗 ≤5 处」：那是旧的 ++下划线++ 两层强调体系，
    # 和单源纯 Markdown 冲突。重点过多只看下面的强调占比。
    density = strong_chars / max(1, total_chars)
    if density > 0.2:
        warns.append("强调占比 %.0f%%（建议 < 20%%），重点过多会被稀释" % (density * 100))

    punch = 0
    for para in re.split(r"\n\s*\n", raw):
        if AI_BOLD_PUNCHLINE.search(para.strip()):
            punch += 1
    if punch:
        warns.append("段末加粗金句 %d 处，建议降调为普通陈述句" % punch)

    for pattern, label in AI_TONE:
        locs = []
        for m in re.finditer(pattern, raw, re.M):
            locs.append(raw.count("\n", 0, m.start()) + 1)
        if len(locs) >= 2:
            shown = "、".join("L%d" % n for n in locs[:6])
            warns.append("AI 腔 / 八股表达「%s」%d 处（%s%s），建议改写"
                         % (label, len(locs), shown,
                            "…" if len(locs) > 6 else ""))

    text_all = "\n".join(lines)
    for alt, src in IMG_RE.findall(text_all):
        if re.match(r"^https?://", src):
            info.append("远程图片，粘贴时微信通常会自动抓取，失败需手动上传：%s" % src)
        else:
            found = os.path.exists(os.path.join(base, src))
            if not found and asset_root:
                found = os.path.exists(
                    os.path.join(asset_root, re.sub(r"^(\.\./)+", "", src)))
            if not found:
                errors.append("本地图片不存在（可用 --asset-root 指定源仓库）：%s" % src)
            else:
                p = src if os.path.isabs(src) else os.path.join(base, src)
                if not os.path.exists(p) and asset_root:
                    p = os.path.join(asset_root, re.sub(r"^(\.\./)+", "", src))
                mb = os.path.getsize(p) / 1024 / 1024
                if mb > MAX_IMG_HARD_MB:
                    errors.append("图片过大 %.1f MB（公众号建议 < %.0f MB）：%s"
                                  % (mb, MAX_IMG_MB, os.path.basename(src)))
                elif mb > MAX_IMG_MB:
                    warns.append("图片 %.1f MB 偏大，建议压到 %.0f MB 内：%s"
                                 % (mb, MAX_IMG_MB, os.path.basename(src)))

    links = LINK_RE.findall(text_all)
    if links:
        info.append("外链 %d 处，默认转文末「参考链接」脚注（公众号正文不支持可点外链）"
                    % len(links))

    if "```mermaid" in text_all:
        info.append("含 mermaid 流程图，公众号不支持，需渲染成图片后手动插入")
    if re.search(r"\$\$.+?\$\$|\\\((?:.+?)\\\)|\\\[(?:.+?)\\\]|\\[a-zA-Z]{2,}\{", text_all):
        warns.append("疑似 LaTeX 公式，公众号不支持，需转成图片")

    return (errors, warns, info, total_chars, strong_chars, headings,
            body_paras, bold_count)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--max-para", type=int, default=110)
    ap.add_argument("--max-item", type=int, default=70)
    ap.add_argument("--asset-root", default="")
    ap.add_argument("--fix", action="store_true", help="自动修复中英文之间的空格")
    ap.add_argument("--warn-only", action="store_true")
    ap.add_argument("--legacy", action="store_true",
                    help="旧交付包（公众号稿.md）只读兼容：::: 容器不报错")
    args = ap.parse_args()

    if args.fix:
        changed = fix_cjk(args.input)
        if changed:
            print("已修复中英文间距 %d 行：" % len(changed))
            for num, old, new in changed[:8]:
                print("  L%d  %s" % (num, old.strip()[:52]))
                print("   →  %s" % new.strip()[:52])
            if len(changed) > 8:
                print("  … 其余 %d 行" % (len(changed) - 8))
        else:
            print("中英文间距无需修复")
        print("")

    (errors, warns, info, total, strong, headings,
     body_paras, bold_count) = lint(
        args.input, args.max_para, args.max_item, args.asset_root or None,
        legacy=args.legacy or os.path.basename(args.input) == "公众号稿.md")

    first_para = ""
    with open(args.input, encoding="utf-8") as fh:
        body, _ = strip_frontmatter(fh.read().split("\n"))
    for line in body:
        s = line.strip()
        if s and not s.startswith(("#", ">", "|", "-", "*", "!", ":")) and not s.startswith("---"):
            first_para = re.sub(r"[*_`]", "", s)
            break

    print("体检：%s" % os.path.basename(args.input))
    with open(args.input, encoding="utf-8") as fh:
        words = CW.count_text(fh.read())["chars"]
    print("  字数 %d · 正文 %d 段 · 加粗 %d 处 · 预计阅读 %d 分钟"
          % (words, body_paras, bold_count, max(1, round(words / 400))))
    print("")
    if errors:
        print("错误 %d：" % len(errors))
        for e in errors:
            print("  ✗ %s" % e)
        print("")
    if warns:
        print("警告 %d：" % len(warns))
        for w in warns:
            print("  ! %s" % w)
        print("")
    if info:
        print("提示 %d：" % len(info))
        for i in info:
            print("  · %s" % i)
        print("")
    try:
        import info_design_hints as IDH  # 同目录的共享脚本；I 提示只供判断，不影响退出码
        design = IDH.check_file(args.input)
    except (ImportError, OSError, UnicodeDecodeError):
        design = []
    if design:
        print("信息设计提示 %d（只供判断，见 references/information-design.md）：" % len(design))
        for n, c, m in design:
            print("  · [%s] L%d %s" % (c, n, m))
        print("")
    if not errors and not warns:
        print("  ✓ 未发现排版问题")

    print("发布信息（公众号后台手动填）：")
    if first_para:
        print("  摘要候选：%s…" % first_para[:54])
    if headings:
        print("  章节：%s" % " / ".join(h[1][:12] for h in headings if h[0] == 2))

    if errors and not args.warn_only:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
