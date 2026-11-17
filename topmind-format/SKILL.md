---
name: topmind-format
description: "把已有文字排成适合 X 的纯文本，按语义段落空行或紧凑列表呈现，严格保留原文措辞、事实、语序与表达性标点符号。支持短文、段子和多个已有开头的完整稿拼接。改写润色用 topmind-revise，从零写作用 topmind-briefs 或 topmind-viral-posts。"
license: MIT
metadata:
  version: "0.1.17"
  action_category: "write"
  triggers: "转段子, 改成段子, 段子格式, 格式化, 格式化一下, 格式化成短文, 排一下版, 整理格式, 加空行, 分行, 加 emoji, X 排版, 几个开头, 备选开头, 拼成成品, format"
  author: "TopMindSpace"
  homepage: "https://github.com/topmindspace/topmind-writing-skills#readme"
  updated: "2026-11-17"
---

# topmind-format · X 纯文本保真排版

用户已有现成文字，本技能**只调整段落空行、分行节拍与列表呈现，清理 Markdown 渲染残留**。严格保留原文的事实、措辞、语序、表达性标点（如 `？？？`、`！！！`、`！！？`、`……`）和有语义作用的符号（如 `✅ / ❌`、箭头、数字）。若用户同时要求润色或去 AI 味，再组合 `topmind-revise`。

## 一、版式选项与 X 排版习惯

| 版式模式 | 适用内容 | 排版做法 |
|---|---|---|
| **短文 `short`** | 干货要点、快讯、观察说明 | **按语义段落空行**（一个完整意思一段，不句句空行）；并列项优先用紧凑 `1）2）` 或 `·` |
| **段子 `duanzi`** | 口语吐槽、群聊拟人、动作反转 | 按说话呼吸与节拍分行，包袱独立成行 |
| **原样微调** | 作者已有明确分段习惯 | 仅清理误带的 `**粗体**`、`## 标题` 等 Markdown 符号与多余空行 |

样张见 [creative-practice.md](references/creative-practice.md)；更多版式细节见 [x-layout-patterns.md](references/x-layout-patterns.md) 与 [x-post-format.md](references/x-post-format.md)。需要检索排版保真经验卡时见 [knowledge-library.md](references/knowledge-library.md)。

## 二、操作与保真原则

1. **清理残留，不动字句**：将 Markdown 的 `**`、`##`、代码围栏转为适合 X 普通帖直读的纯文本；没有并列内容时不把普通句子硬拆成列表。
2. **保留情绪标点与符号语义**：作者原文里的 `？？？`、`！！！`、`！！？`、`……` 以及 `✅ / ❌` 承载语气和正反判断，排版时原样保留，绝不自作主张改成单个句号或删改。
3. **链接与来源按意图安排**：默认保留原文链接，或按 X 短帖习惯将来源链接移至代码块外另列（使用 `--separate-links`）。必要归因词（「据某媒体报道」「厂商自测」）留在正文。

```bash
python3 scripts/format_text.py 原文.txt --mode short --out 短文.txt
python3 scripts/format_text.py 原文.txt --mode duanzi --split --out 段子.txt
# 用户要把链接和来源另列时
python3 scripts/format_text.py 原文.txt --mode short --separate-links --links-out 链接.txt
# 作者给多个开头（用 --- 分隔）需要拼成多版完整成品时
python3 scripts/format_text.py 原文.txt --mode short --variants 开头备选.txt
```

`lint_x_post.py` 可用于检查是否有漏网的 Markdown 符号残留；所有风格提示（W/H）均不产生改字授权，也不阻断交付。

## 三、交付

每份完成稿独立放在一个可复制纯文本代码块内；挪出代码块外的链接或说明附在块外（见 [x-delivery-contract.md](references/x-delivery-contract.md) 与 [emoji-system.md](references/emoji-system.md)）。本技能不执行对外发布。
