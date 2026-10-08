# topmind-briefs · Short-form briefs (WeChat + X)

**[中文](./README.md)** | English

One topic, one chart, then stop. Data-driven short posts: rankings, paper TL;DRs,
product launches — one X post or short thread, ~300–800 Chinese characters on WeChat,
one-click-copy HTML for both.

- Version: **v0.2.8** (ships with `@topmindspace/topmind-writing-skills@0.8.24`)

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

## Content types

- Data rankings / ranking alerts / paper explainers / mechanism explainers
  (four types calibrated against real posts, see SKILL.md)
- Operating rules: draft only, never auto-post; every number needs a source;
  vendor numbers labeled as vendor claims; no rewriting others' work

## When NOT to use

X long-form → `topmind-x-article`; WeChat long-form → `topmind-wechat-post`;
engagement-style short posts → `topmind-viral-posts`; posting → `topmind-x` (only after the user confirms).
