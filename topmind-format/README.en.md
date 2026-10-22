# topmind-format · X plain-text formatting

English | [中文](./README.md)

**Layout only, not a single character changed.** Turns existing text into something readable on X: duanzi layout, brief layout, or several alternative openings stitched into full posts. A fidelity check fails if any character changes; links, source lines and image notes are pulled out to be delivered separately.

- Version: **v0.1.12**

```bash
npx @topmindspace/topmind-writing-skills install topmind-format
```

Say: "转段子", "排一下版", "格式化成短文", "加空行", "我想了几个开头，帮我拼成完整的帖子".

## Three modes

| You say | Result |
|---|---|
| Duanzi | One sentence per line, blank line between; all emoji and bullet symbols removed |
| Brief | Sensible paragraphs; lists become 「·」「1）」 (or 🔹 / 1️⃣); Markdown quote markers removed |
| Stitch openings | Each opening replaces the first paragraph; each result is fidelity-checked |

## Example (original, in Chinese)

```text
今天把周报写完了，

结果发现写的是上周的。

白干两小时，谁懂？
```

## Scripts

```bash
python3 scripts/format_text.py in.txt --mode duanzi --split
python3 scripts/format_text.py in.txt --mode short --links-out links.txt
python3 scripts/format_text.py in.txt --mode duanzi --variants openings.txt   # alternatives separated by ---
python3 scripts/lint_x_post.py out.txt
```

The de-AI lint still runs, but this skill never rewrites: hits go into the change notes for you to decide; rewrites go to `topmind-revise`.

## When not to use

Write a duanzi from scratch → `topmind-viral-posts`; a brief → `topmind-briefs`; X long-form → `topmind-x-article`; WeChat layout → `topmind-wechat-post`; posting → `topmind-x` (with your confirmation).

More in [`examples/`](./examples/); all self-written.
