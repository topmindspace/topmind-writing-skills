# topmind-briefs · Short-form briefs (WeChat + X)

**[中文](./README.md)** | English

One topic, then stop. Data-driven short posts: rankings, paper explainers, product launches.
A brief is not a long-form article — **no HTML by default**: the X version is one copy-ready plain-text block
(sensible paragraphing, restrained emoji, source links); the WeChat version is ~300–800 Chinese characters of Markdown.
Original facts, images and quotes come first; a cover is optional when no original image exists. Every delivery lists
each source's name, publish time and link.

- Version: **v0.2.18** (ships with `@topmindspace/topmind-writing-skills@0.8.35`)

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-briefs
```

## Usage

```bash
python3 scripts/lint_x_post.py brief-x.txt                                  # check the X version
python3 scripts/format_text.py brief-x.txt --mode short --title-emoji 📊     # layout only, words unchanged
```

HTML only on explicit request (scripts ship with the skill; single source of truth is `shared/scripts/` in the repo):

```bash
python3 scripts/md2x-html.py brief-x.md --out brief-x.html --images-from brief-wechat.md
python3 scripts/md2wechat.py --input brief-wechat.md --out-dir out --slug brief --embed-images --no-toc
```

See [SKILL.md](./SKILL.md) for the workflow and [references/emoji-system.md](./references/emoji-system.md) for the emoji system.

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

Formatting existing text / converting to duanzi → `topmind-format`; X long-form → `topmind-x-article`; WeChat long-form → `topmind-wechat-post`;
engagement-style short posts and jokes → `topmind-viral-posts`; standalone long images/posters → `topmind-poster`;
covers and header images → `topmind-cover`; posting → `topmind-x` (only after the user confirms).
