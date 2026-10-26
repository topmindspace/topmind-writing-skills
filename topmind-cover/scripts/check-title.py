#!/usr/bin/env python3
"""封面标题生图风险检查：整张生成前先跑，挑出生图模型容易写错的标题。

用法：
  python3 scripts/check-title.py "标题" ["副标题" ...]
  python3 scripts/check-title.py --json "标题"

检查项（见 references/design-system.md 第九节「中文字生图规约」）：
  长度    主标题 > 8 字警告，> 12 字高风险（建议拆成主标题 + 副标题，或改走脚本叠字）
  形近字  于/干/千、未/末、己/已/巳、戊/戌/戍、拨/拔、侯/候、即/既、析/拆、免/兔、鸟/乌、
          辨/辩/辫、赢/嬴、茶/荼、崇/祟 等，模型常互换
  生僻字  不在 GB2312 一级常用字里（含二级字、繁体、扩展区）
  繁体    能在 Big5 编码但不在 GB2312 里的字，模型常把简体写成繁体，反之亦然
  符号    书名号、引号、全角标点、emoji：模型常漏写或画乱
退出码：0 低风险；1 有中风险；2 有高风险。
"""
import json
import sys

CONFUSABLE = {  # 只收实际高频出错的组合；常见大字（大、人、日、天…）模型基本不会写错，不报
    "于": "干千", "干": "于千", "千": "干于", "未": "末", "末": "未", "己": "已巳", "已": "己巳", "巳": "己已",
    "戊": "戌戍", "戌": "戊戍", "戍": "戊戌", "拨": "拔", "拔": "拨", "侯": "候", "候": "侯", "即": "既", "既": "即",
    "析": "拆", "拆": "析", "汩": "汨", "汨": "汩", "免": "兔", "兔": "免", "鸟": "乌", "乌": "鸟", "冶": "治",
    "治": "冶", "辨": "辩辫", "辩": "辨辫", "辫": "辨辩", "赢": "嬴羸", "茶": "荼", "荼": "茶", "崇": "祟", "祟": "崇",
}
PUNCT = set("《》「」『』“”‘’【】—…·")


def level(ch):
    try:
        b = ch.encode("gb2312")
    except UnicodeEncodeError:
        return 0
    if len(b) != 2: return -1
    return 1 if 0xB0 <= b[0] <= 0xD7 else 2 if 0xD8 <= b[0] <= 0xF7 else -1


def is_trad(ch):
    if level(ch) > 0: return False
    try:
        ch.encode("big5"); return True
    except UnicodeEncodeError:
        return False


def check(text, is_main=True):
    out = []
    han = [c for c in text if "\u4e00" <= c <= "\u9fff" or "\u3400" <= c <= "\u4dbf"]
    n = len(han)
    if is_main and n > 12: out.append(("高", f"主标题 {n} 个汉字，超过 12，模型很难全对：拆成主标题 + 副标题，或改走脚本叠字"))
    elif is_main and n > 8: out.append(("中", f"主标题 {n} 个汉字，建议 ≤ 8"))
    elif not is_main and n > 14: out.append(("中", f"副标题 {n} 个汉字，建议 ≤ 14"))
    for c in dict.fromkeys(han):
        if c in CONFUSABLE: out.append(("中", f"「{c}」易写成「{'」「'.join(CONFUSABLE[c])}」：出图后重点核对，或用后期排版保留原文"))
        if is_trad(c): out.append(("高", f"「{c}」是繁体字：保留作者语言选择，必要时用后期排版"))
        elif level(c) == 2: out.append(("中", f"「{c}」不是一级常用字，模型容易写错：核字，或用后期排版保留原字"))
        elif level(c) == 0: out.append(("高", f"「{c}」是生僻字（不在 GB2312）：核字，或改走脚本叠字保留原字"))
    sym = [c for c in text if c in PUNCT or ord(c) > 0x1F000]
    if sym: out.append(("中", f"含 {''.join(dict.fromkeys(sym))}：标点和 emoji 常被漏写或画乱，按作者意图保留并核对"))
    return out


def main():
    args = [a for a in sys.argv[1:] if a != "--json"]
    if not args:
        print("用法：check-title.py \"主标题\" [\"副标题\" ...]", file=sys.stderr); sys.exit(1)
    res = {t: check(t, i == 0) for i, t in enumerate(args)}
    worst = max([{"中": 1, "高": 2}[lv] for v in res.values() for lv, _ in v] or [0])
    if "--json" in sys.argv:
        print(json.dumps({"risk": ["低", "中", "高"][worst], "items": res}, ensure_ascii=False))
    else:
        for t, items in res.items():
            print(f"「{t}」：" + ("低风险" if not items else ""))
            for lv, msg in items: print(f"  [{lv}] {msg}")
        print("总体风险：" + ["低", "中", "高"][worst])
    sys.exit(worst)


if __name__ == "__main__":
    main()
