# topmind-format · X 纯文本格式化

[English](./README.en.md) | 中文

把现成的文字排成 X 上好读的样子：**转段子**（每句一行、行间空一行）或**格式化成短文**（分段换行 + emoji 列表 + 标题 emoji + 鸡/猫/植物人设点缀）。只动排版，不改字，自带原文保真校验。

- 版本：**v0.1.2**（随 `@topmindspace/topmind-writing-skills@0.8.34` 发布）

## 安装

```bash
npx @topmindspace/topmind-writing-skills install topmind-format
```

## 用法

| 你说 | 结果 |
|---|---|
| 转段子 / 段子格式 | 每句一行，行与行之间空一行 |
| 格式化 / 格式化成短文 | 分段、列表改 🔹 / 1️⃣，标题 emoji 与关键词对应，开头结尾 0–2 个人设点缀 |

```bash
python3 scripts/format_text.py 原文.txt --mode duanzi --split --open 🐱 --close 🌱
python3 scripts/format_text.py 原文.txt --mode short --title-emoji 🆕 --open 🐔
python3 scripts/lint_x_post.py 输出.txt
```

emoji 规则见 [references/emoji-system.md](./references/emoji-system.md)（与 topmind-briefs、topmind-viral-posts 共用）；X 排版规则见 [references/x-post-format.md](./references/x-post-format.md)。

## 边界

从零写段子 → `topmind-viral-posts`；从零写短文 → `topmind-briefs`；X 长文 → `topmind-x-article`；公众号排版 → `topmind-wechat-post`；发帖 → `topmind-x`（须用户确认）。

## 开发

```bash
python3 scripts/audit_skill.py
python3 scripts/package_skill.py --check
python3 scripts/negative_tests.py
```
