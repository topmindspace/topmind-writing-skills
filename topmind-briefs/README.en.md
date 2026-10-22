# topmind-briefs · Briefs (X + WeChat)

English | [中文](./README.md)

**One thing, then stop.** News, previews, launches, deals, rankings, papers, hands-on results and one-line takes: nine content types, each with its own opening and ending. The X version is one block of plain text you can paste straight in, facts and highlight at a glance; links, original images and caliber notes are delivered separately. The WeChat version is 300–800 characters of Markdown. Writes in Chinese by default.

- Version: **v0.2.27**

```bash
npx @topmindspace/topmind-writing-skills install topmind-briefs
```

Say: "发个快讯", "来篇短的", "写条预告", "有个羊毛帮我发一条", "这个榜单换第一了", "公众号和 X 各一版".

## Nine content types

| Type | For | Opening | Ending |
|---|---|---|---|
| News (first) | Just announced | What + the sharpest number, vs a rival readers know | "..." or none |
| News (late) | Window has passed | New angle: hands-on, math, verification | "..." |
| Preview / rumor | Teasers, gray rollouts, docs | "Coming?!", verbs match the caliber | "?!" |
| Launch / tool | Something useful and new | Genuine question or a sincere pick | "..." |
| Deal | Limited-time, free | What you can grab now | none |
| Ranking / data | Rank changes, benchmarks | Who's first, by how much | none |
| Paper | New method or result | One-line conclusion | none |
| Hands-on | You ran it | The result (broke, fast, pricey) | Self-roast or a real question |
| One-line take | Persona-building know-how | An insider's light judgment | The judgment |

## Example (original, fictional)

```text
某模型低调上线新版：编程评测 31 → 42，价格不变

网页、App、接口已全量切换，权重开源。

几项关键提升：

1）编程评测：31 → 42
2）推理评测：37 → 43
3）智能体评测：74 → 77，比某知名闭源模型高 3 分

单任务成本两毛钱出头...
```

Delivered separately: the source line, `[图1]` the official chart, and the caliber note "scores are vendor-reported". More in [references/examples.md](./references/examples.md) and [`examples/`](./examples/).

## Key practices

- **Glanceable**: the X body keeps facts, key numbers and the highlight; verification notes go into the caliber note.
- **Match the caliber**: a preview is not a launch; a gray rollout is not an announcement.
- **Timing**: the first-post window is minutes; if late, change the angle.
- **One event, several posts**: performance in one, price in another.
- **Images** only when the image is the information; no original → ask first.
- **Hashtags**: none by default, at most 2.

## Delivery and checks

Order: body (plain text) → links (source｜time｜URL) → images (1–2 originals) → caliber note → (optional) WeChat Markdown.

```bash
python3 scripts/lint_x_post.py X短文.txt --kind news
python3 scripts/check_article.py <brief-folder>/
python3 scripts/format_text.py X短文.txt --mode short --out X短文.txt
```

HTML only on request: `md2x-html.py` (X one-click copy), `md2wechat.py --embed-images --no-toc --preview` (WeChat layout + preview image).

## When not to use

Duanzi → `topmind-viral-posts`; layout only → `topmind-format`; long-form → `topmind-x-article` / `topmind-wechat-post`; long images → `topmind-poster`; covers → `topmind-cover`; posting → `topmind-x` (with your confirmation).

All samples are self-written; no third-party text is included.
