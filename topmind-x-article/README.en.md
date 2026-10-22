# topmind-x-article · X long-form

**[中文](./README.md)** | English

**One Markdown source, one click into the X Article editor.** Skeleton and "my judgments" first, then the body; `topmind-revise` runs by default when the draft is done. For X, a one-click copy HTML is derived: images embedded in document order, "来源：" lines become captions, tables can become images, and a preview image is rendered so you check it before delivery.

- Version: **v0.4.25**

Say: "写 X 长文", "出一键复制版", "X 文章排版", "推特长文".

Highlights:

- **Skeleton first**: message, reader, my judgments (3–5, with basis and likely pushback), material-to-judgment ratio per section; a section that is all material gets a hint.
- **Own diagrams**: method, architecture and comparison pieces get at least one diagram of your view.
- **Tables as images**: `--tables-as-images` turns tables X can't paste into images, in order.
- **Preview**: `--preview` renders `out/预览.png` before delivery.

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-x-article
```

## Usage

```bash
# 0. Create the article folder (source + 骨架.md + 素材来源.md + images/ cover/ raw/ out/ 参考/) + structure check
#    fill 骨架.md before drafting; images as ![caption](images/01-xx.png), source on the next line "来源：…"
#    working across environments: --env / --by record updated_env / updated_by (see references/workspace.md)
python3 scripts/article_scaffold.py --title "My article"
python3 scripts/check_article.py "My article/"

# 1. On request: one-click-copy HTML (preferred) → My article/out/X长文.html
python3 scripts/md2x-html.py "My article/My article.md" --tables-as-images --preview   # preview: out/预览.png
# reads the source's ![]() lines and embeds images in document order; the cover defaults to frontmatter `cover`;
# never hand-assemble --images (filename sort order != document order —
# this once misplaced a whole section's images).
# Legacy layout: md2x-html.py X长文.md --out X长文.html --images-from 公众号稿.md
# Open X长文.html in a browser → click the top 「一键复制全文」 button → paste into the X Article editor body
# (the first # heading is excluded from the clipboard — fill it into X's title field by hand;
#  upload the cover separately via X's dedicated cover entry)

# 2. On request: plain-text fallback (when HTML copying misbehaves) → My article/out/X发布稿.txt
python3 scripts/md2x.py "My article/My article.md"

# 3. Cover: generate a 1500×600 cover with topmind-cover

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
Lists become "· " / "1）" by default (nested items indented two spaces, at most two levels), because
plain-text X posts do not render Markdown lists; `--list-style emoji` gives 🔹 / ▫️ / 1️⃣ and `--list-style keep` keeps the original markers (rules in `references/x-post-format.md`).
`python3 scripts/lint_x_post.py X发布稿.txt --long` is a quick self-check. The X Article HTML path pastes rich text, so native lists stay.

Read the result through once by hand after converting.

## Minimal example

Input (10 lines of markdown):

```markdown
# 晨光 3.0 发布了

**全新设计**的写作助手，新增了离线模式。

![发布会现场](cover.png)

| Token 消耗 | -20% |
| 耗时 | -30% |

详见[官方博客](https://example.com/blog)。
```

`python3 scripts/md2x.py draft.md --out X发布稿.txt` produces:

```
晨光 3.0 发布了

全新设计的写作助手，新增了离线模式。

[图1]

Token 消耗：-20%
耗时：-30%

详见官方博客（https://example.com/blog）。

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

## Original examples

Sample outputs written by us (fictional or neutral topics, no third-party text) are in [`examples/`](./examples/).
