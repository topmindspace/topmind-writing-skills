# topmind-x-article · One-Click X Long-Form Publishing

**[中文](./README.md)** | English

Turn a Markdown draft into a "copy → paste → publish" X long-form (Article) package.

- Version: **v0.4.10** (ships with `@topmindspace/topmind-writing-skills@0.8.27`)

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-x-article
```

## Usage

```bash
# 1. Draft → one-click-copy HTML (preferred)
python3 scripts/md2x-html.py <draft>.md --out <package>/X长文.html \
  --images-from 公众号稿.md [--cover cover-1500x600.png]
# --images-from derives image order from the WeChat draft in document order
# (required when the X draft is derived from it);
# never hand-assemble --images (filename sort order != document order —
# this once misplaced a whole section's images).
# Open X长文.html in a browser → click the top 「一键复制全文」 button → paste into the X Article editor body
# (the first # heading is excluded from the clipboard — fill it into X's title field by hand;
#  upload the cover separately via X's dedicated cover entry)

# 2. Plain-text fallback (when HTML copying misbehaves)
python3 scripts/md2x.py <draft>.md --out <package>/X发布稿.txt

# 3. Cover: generate a 1200×675 cover with topmind-cover

# 4. Follow references/publish-checklist.md item by item
```

## Conversion rules

The HTML path follows `references/x-html-format.md`: rich-text paste into the X editor
(headings/bold/links/lists/quote blocks preserved); ` ``` ` prompt blocks render as quote
blocks with a 「复制提示词」 copy button; GFM tables become lists (X drops `<table>` on paste);
the first `#` heading is excluded from the clipboard; images are base64-inlined and numbered
`[图N]`, with per-image 「下载图片」 download buttons as fallback upload.

Prompt copying is dual-channel: the author side uses the 「复制提示词」 button in the HTML
(to grab the text before publishing); the reader-side one-click copy can only come from X
native code blocks (convert each block by hand via Insert → Code — native code blocks carry a
native copy button, while pasted `<pre>` is discarded by X).

The plain-text fallback follows `references/x-format.md`: headings → plain text lines,
horizontal rules → blank lines, emphasis markers removed, links → `text（url）`, images →
`[图N]` (image list appended at the end), tables → "label：value" lists, blockquotes unquoted.

Read the result through once by hand after converting.

## Minimal example

Input (10 lines of markdown):

```markdown
# Manus 2.0 发布了

**从零重建**的 Agent，新增了 Cue 个人助手。

![发布会现场](cover.png)

| Token 消耗 | -23.2% |
| 耗时 | -28.2% |

详见[官方博客](https://manus.im/blog)。
```

`python3 scripts/md2x.py draft.md --out X发布稿.txt` produces:

```
Manus 2.0 发布了

从零重建的 Agent，新增了 Cue 个人助手。

[图1]

Token 消耗：-23.2%
耗时：-28.2%

详见官方博客（https://manus.im/blog）。

—— 配图清单 ——
[图1] 发布会现场
```

Copy the whole `X发布稿.txt` → paste into the X Article editor → upload images in `[图N]` order → publish.

## Publishing

X long-form posts are currently published by hand-pasting into the X Article editor; the API does not publish long-form. After publishing, do per the checklist: pin a first comment with the extra info, fetch the full text back for verification.

## External dependencies

The following skills are **not in this repo** (provided separately by the host agent environment). Missing ones disable the corresponding routed capability; the core flow (draft → text, cover, publish checklist) is unaffected:

- `topmind-x` (topmind-skills pack): short-post connector, posts only after the user confirms; its xurl covers short posts, not long-form. Short-post drafting goes to `topmind-viral-posts` / `topmind-briefs`.
- `topmind-capture`: the "archive only, don't publish" routing path.

## Development

```bash
python3 scripts/package_skill.py --check   # pre-publish check
python3 scripts/negative_tests.py          # bad-input tests
```
