# topmind-format · X 纯文本格式化

[English](./README.en.md) | 中文

把现成的文字排成 X 上好读的样子：**转段子**（每句一行、行间空一行，完全不用 emoji，分点不加符号）或**格式化成短文**（合理分段换行、列表改「·」「1）」或 emoji，标题 emoji 与人设点缀可选）。只动排版，不改字，自带原文保真校验；正文里的链接、来源行、配图行会拿出来另列，交付一段可直接复制的纯文本，链接和图片另发。

- 版本：**v0.1.4**（随 `@topmindspace/topmind-writing-skills@0.8.36` 发布）

## 安装

```bash
npx @topmindspace/topmind-writing-skills install topmind-format
```

## 用法

| 你说 | 结果 |
|---|---|
| 转段子 / 段子格式 | 每句一行，行与行之间空一行；去掉所有 emoji 和列表符号，分点一条一行 |
| 格式化 / 格式化成短文 | 分段、列表改「·」「1）」（`--bullets emoji` 改 🔹 / 1️⃣）；标题 emoji、人设点缀可选 |

```bash
python3 scripts/format_text.py 原文.txt --mode duanzi --split   # 段子体不接受 --open / --close / --title-emoji
python3 scripts/format_text.py 原文.txt --mode short --links-out 链接.txt   # 链接 / 来源行另存，另发
python3 scripts/format_text.py 原文.txt --mode short --bullets emoji --title-emoji 🆕   # emoji 可选
python3 scripts/lint_x_post.py 输出.txt
```

emoji 规则（只用于短文体）见 [references/emoji-system.md](./references/emoji-system.md)；X 排版规则见 [references/x-post-format.md](./references/x-post-format.md)。

## 边界

从零写段子 → `topmind-viral-posts`；从零写短文 → `topmind-briefs`；X 长文 → `topmind-x-article`；公众号排版 → `topmind-wechat-post`；发帖 → `topmind-x`（须用户确认）。

## 开发

```bash
python3 scripts/audit_skill.py
python3 scripts/package_skill.py --check
python3 scripts/negative_tests.py
```
