---
name: topmind-format
description: "把已有文字排成适合 X 的纯文本，保留措辞、事实、顺序与有表达作用的符号。支持短文、段子和多个已有开头的完整稿拼接。改写用 topmind-revise，从零写作用 topmind-briefs 或 topmind-viral-posts。"
license: MIT
metadata:
  version: "0.1.15"
  action_category: "write"
  triggers: "转段子, 改成段子, 段子格式, 格式化, 格式化一下, 格式化成短文, 排一下版, 整理格式, 加空行, 分行, 加 emoji, X 排版, 几个开头, 备选开头, 拼成成品, format"
  author: "TopMindSpace"
  homepage: "https://github.com/topmindspace/topmind-writing-skills#readme"
  updated: "2026-10-27"
---

# topmind-format · X 纯文本排版

用户已有文字，只调整换行、空行和列表等呈现。保留事实、措辞、顺序、标点和有表达作用的 emoji；疑似错字可另提建议。用户同时要求润色时可组合 `topmind-revise`，按已授权范围完成。

## 按需借鉴与积累

需要新方向、完整例子或相关经验时，用 [知识使用与增补](references/knowledge-library.md) 检索排版节奏、符号语义与保真对照；先读摘要，再选相关卡片。可以混合、改造或采用库外思路，简单任务直接完成。知识不替代当前用户要求；新反馈先作为有范围的候选，不自动改长期规则。

## 版式选项

| 版式 | 适用 | 做法 |
|---|---|---|
| 短文 `short` | 要点、数据、说明 | 语义分段，列表可用 ·、1）、emoji 或原符号 |
| 段子 `duanzi` | 口语、对话、反转 | 每个节拍独立一行，留白决定停顿 |
| 原样微调 | 作者风格明确 | 只修挤在一起或过多的空行 |

根据文本直接选合适版式。只有版式比较本身有价值时才给两版。样张见 [creative-practice.md](references/creative-practice.md)；更多排列见 [x-layout-patterns.md](references/x-layout-patterns.md)。

普通帖通常原样显示 Markdown 标记。可将加粗、标题、链接语法变成可读纯文本；`-`、`1.` 本身也能充当文字列表，不必为统一符号反复改稿。代码、数学式、引用里的符号按语义保留。

## 操作与保真

先读原文，按语义切行，再逐项核对数字、专名、引语、URL 与表情。来源可另列，也可按用户意图留正文；必要归因和限定留在正文，不因“排版”删掉。

随包脚本适合常用版式；用户要保留特殊结构时直接编辑并对照原文。

```bash
python3 scripts/format_text.py 原文.txt --mode duanzi --split --out 段子.txt
python3 scripts/format_text.py 原文.txt --mode short --out 短文.txt
python3 scripts/format_text.py 原文.txt --mode short --bullets emoji --out 短文.txt
# 用户要把链接和来源另列时
python3 scripts/format_text.py 原文.txt --mode short --separate-links --links-out 链接.txt
# 用户明确要纯文字、去表情时
python3 scripts/format_text.py 原文.txt --mode duanzi --strip-emoji
```

默认保留原文表情和链接；`--strip-emoji`、`--separate-links` 是可选转换。脚本的逐字校验有适用范围：它忽略空白、列表标记和 emoji，不能替代语义核对，尤其注意 ✅ / ❌ 等表达正反含义的符号。

作者给多个开头时可用 `--variants 开头备选.txt`（开头用 `---` 分隔）拼完整成品；不凭空改写开头。`lint_x_post.py` 可以找格式残留；风格警告不产生改字授权。这里只排版时无需额外研究、找图或走完整改稿报告。

## 交付

一个完成稿一个可复制块；有挪动的链接、图注或明确问题，在块外简述。沿用作者想要的链接、表情和标签安排。仅在交付契约明确要求链接分离时使用检查器 `--separate-links`。

参考：[交付建议](references/x-delivery-contract.md)、[emoji 选项](references/emoji-system.md)、[排版经验](references/x-post-format.md)。本技能不执行发布。

从零写作分别用 `topmind-briefs` / `topmind-viral-posts`；公众号和 X 长文导出用 `topmind-wechat-post` / `topmind-x-article`。
