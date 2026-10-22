# topmind-format · X 纯文本格式化

[English](./README.en.md) | 中文

**只改排版，一个字都不改。** 把现成的文字排成 X 上好读的样子：转段子、格式化成短文、把几个备选开头拼成几条完整成品。自带保真校验，改了字就报错；正文里的链接、来源行、配图行拿出来另发。

- 版本：**v0.1.12**

```bash
npx @topmindspace/topmind-writing-skills install topmind-format
```

你可以这样说：「转段子」「排一下版」「格式化成短文」「加空行」「我想了几个开头，帮我拼成完整的帖子」。

## 三种用法

| 你说 | 结果 |
|---|---|
| 转段子 | 每句一行，行与行之间空一行；去掉所有 emoji 和列表符号 |
| 格式化成短文 | 合理分段；列表改「·」「1）」（要 emoji 就改 🔹 / 1️⃣）；Markdown 引用去掉标记 |
| 几个开头拼成品 | 每个开头替换正文第一段，各自做保真校验，输出几条完整的帖子 |

## 示例（原创）

输入：

```text
今天把周报写完了，结果发现写的是上周的。白干两小时，谁懂？
```

段子体：

```text
今天把周报写完了，

结果发现写的是上周的。

白干两小时，谁懂？
```

再给一个备选开头「周报写了两小时，」，拼成第二条成品：

```text
周报写了两小时，

结果发现写的是上周的。

白干两小时，谁懂？
```

## 脚本

```bash
python3 scripts/format_text.py 原文.txt --mode duanzi --split
python3 scripts/format_text.py 原文.txt --mode short --links-out 链接.txt
python3 scripts/format_text.py 原文.txt --mode short --bullets emoji --title-emoji 🆕
python3 scripts/format_text.py 原文.txt --mode duanzi --variants 开头备选.txt   # 备选用 --- 隔开
python3 scripts/lint_x_post.py 输出.txt
```

去 AI 味检查照跑，但本技能不改字：命中写进改动说明，由你决定；要改内容转 `topmind-revise`。

## 何时不用

从零写段子 → `topmind-viral-posts`；从零写短文 → `topmind-briefs`；X 长文 → `topmind-x-article`；公众号排版 → `topmind-wechat-post`；发帖 → `topmind-x`（须你确认）。

更多示例见 [`examples/`](./examples/)，全部自己写，不收录任何第三方原文。
