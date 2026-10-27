#!/usr/bin/env python3
"""标题核字线索，不预测生图成功率，也不要求改短标题或改语言。

默认只提示并返回 0；--strict 主动启用旧式提示级别退出码 1/2。
缺少输入仍失败。旧 JSON risk 字段保留兼容，只表示启发式核对级别。
"""
import json
import sys

CONFUSABLE = {  # 启发式形近字表；不是任何模型的错误率统计
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
    if is_main and n > 12: out.append(("高", f"主标题 {n} 个汉字：可按画幅分行或后期叠字，保留完整意思；长度不代表模型准确率"))
    elif is_main and n > 8: out.append(("中", f"主标题 {n} 个汉字：检查断行、字距与缩略图，按当前任务保留文案"))
    elif not is_main and n > 14: out.append(("中", f"副标题 {n} 个汉字：核对其阅读任务与字号，不设统一上限"))
    for c in dict.fromkeys(han):
        if c in CONFUSABLE: out.append(("中", f"「{c}」易写成「{'」「'.join(CONFUSABLE[c])}」：出图后重点核对，或用后期排版保留原文"))
        if is_trad(c): out.append(("高", f"「{c}」可能超出当前检查表的简体字范围：保留作者语言，核对实际字体覆盖；这不是错误判定"))
        elif level(c) == 2: out.append(("中", f"「{c}」位于旧编码表的另一分区：仅作核字线索，不推断罕见程度或模型表现"))
        elif level(c) == 0: out.append(("高", f"「{c}」不在本检查表的 GB2312 范围：核对字库覆盖并保留原字，不据此判定生僻或不合格"))
    sym = [c for c in text if c in PUNCT or ord(c) > 0x1F000]
    if sym: out.append(("中", f"含 {''.join(dict.fromkeys(sym))}：按作者意图保留标点与 emoji，并在成图核对"))
    return out


def main():
    args = [a for a in sys.argv[1:] if a not in {"--json", "--strict"}]
    if not args:
        print("用法：check-title.py \"主标题\" [\"副标题\" ...]", file=sys.stderr); sys.exit(1)
    res = {t: check(t, i == 0) for i, t in enumerate(args)}
    worst = max([{"中": 1, "高": 2}[lv] for v in res.values() for lv, _ in v] or [0])
    if "--json" in sys.argv:
        print(json.dumps({"advisory": True, "risk": ["低", "中", "高"][worst], "items": res}, ensure_ascii=False))
    else:
        for t, items in res.items():
            print(f"「{t}」：" + ("未发现启发式提示" if not items else ""))
            for lv, msg in items: print(f"  [{lv}] {msg}")
        print("核对级别（非准确率预测）：" + ["常规", "留意", "重点核对"][worst])
    sys.exit(worst if "--strict" in sys.argv else 0)


if __name__ == "__main__":
    main()
