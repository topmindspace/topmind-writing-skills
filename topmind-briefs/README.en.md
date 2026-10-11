# topmind-briefs · Short-form briefs (WeChat + X)

**[中文](./README.md)** | English

One topic, one chart, then stop. Data-driven short posts: rankings, paper explainers,
product launches — one X post or short thread, ~300–800 Chinese characters on WeChat,
one-click-copy HTML for both.

- Version: **v0.2.13** (ships with `@topmindspace/topmind-writing-skills@0.8.30`)

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-briefs
```

## Usage

Run from this skill's directory:

```bash
# X version (image order derived from the WeChat draft; never hand-order --images)
python3 scripts/md2x-html.py brief-x.md --out brief-x.html --images-from brief-wechat.md

# WeChat version (images inlined as base64; writes <slug>-公众号版.html + 图片上传清单.md)
python3 scripts/md2wechat.py --input brief-wechat.md --out-dir out --slug brief --embed-images --no-toc
```

Both scripts ship with this skill (Python standard library only), so a standalone
install of briefs can render HTML. They are byte-identical copies of the same-named
scripts in `topmind-x-article` / `topmind-wechat-post`; inside the repo,
`scripts/negative_tests.py` checks they stay in sync. See [SKILL.md](./SKILL.md)
for the full workflow.

## X formatting and hashtags

X does not render Markdown, so the X version never uses `- ` lists, `#` headings or `**bold**`. Lists use emoji bullets
(🔹 items, ▫️ sub-items, 1️⃣ steps, ✅/❌ contrasts); one style per post, one item per line, at most two levels.
The WeChat draft keeps Markdown lists; the X draft is derived from it and only the layout may differ.
Each X version ends with 0–2 suggested hashtags on their own last line (none on the WeChat version). See
[references/x-post-format.md](./references/x-post-format.md) and [references/platform-specs.md](./references/platform-specs.md).

```bash
# Check the X version: no Markdown list/heading/bold, hashtags on the last line; add --fix --out to rewrite
python3 scripts/lint_x_post.py brief-x.md
```

## Content types

- Data rankings / ranking alerts / paper explainers / mechanism explainers
  (four types calibrated against real posts, see SKILL.md)
- Operating rules: draft only, never auto-post; every number needs a source;
  vendor numbers labeled as vendor claims; no rewriting others' work

## When NOT to use

X long-form → `topmind-x-article`; WeChat long-form → `topmind-wechat-post`;
engagement-style short posts and jokes → `topmind-viral-posts`; standalone long images/posters → `topmind-poster`;
covers and header images → `topmind-cover`; posting → `topmind-x` (only after the user confirms).
