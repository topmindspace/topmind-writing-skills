# topmind-format · X 纯文本零改字保真排版

[English](./README.en.md) | 中文

将已有文字排成适合 X 阅读的纯文本：**100% 保留原文措辞、事实、语序、链接与表达性标点**，只调整段落空行、列表呈现与说话节拍，清理 Markdown 格式残留。

## 核心特点

- **零改字铁律**：不删改原文一字一句、不丢弃原有链接与来源归因；需要润色或去 AI 味时交由 `topmind-revise`。
- **三种排版模式**：
  - **短文 `short`**：按**语义段落空行**（一个完整意思一段，不搞句句空行），并列项转为紧凑 `1）2）` 或 `·`。
  - **段子 `duanzi`**：按口语呼吸与叙事节拍分行，让包袱与反转独立成行。
  - **多开头拼接 `--variants`**：当作者写了多个备选开头时，自动与正文拼成多份完整可复制成品。
- **保留情绪标点与符号语义**：原文中的 `？？？`、`！！！`、`！！？`、`……` 以及 `✅ / ❌`、emoji 默认完整保留。

## 安装与使用

```bash
npx @topmindspace/topmind-writing-skills install topmind-format
```

完整规则见 [SKILL.md](./SKILL.md)，零改字保真排版前后对照见 [examples/README.md](./examples/README.md)，按需知识包见 [knowledge/README.md](./knowledge/README.md)。

## 常用脚本

```bash
python3 scripts/format_text.py 原文.txt --mode short --out 短文.txt
python3 scripts/format_text.py 原文.txt --mode duanzi --split --out 段子.txt
```

仅在用户明确要求时才使用 `--separate-links` 或 `--strip-emoji`。只负责文本排版，由用户完成对外发布。

MIT License。仓库维护与合集说明见 [topmind-writing-skills](https://github.com/topmindspace/topmind-writing-skills)。
