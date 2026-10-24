# topmind-wechat-post · WeChat long-form

**[中文](./README.md)** | English

**The whole path of a WeChat article, from topic to publish checklist.** Single-source article folder, "my judgments" in the skeleton, three quality gates (facts / logic / de-AI, run by `topmind-revise`), WeChat layout with embedded images (paste and the images come along), a preview image before delivery, publish checklist and status sync.

- Version: **v0.3.20**

Say: "写公众号", "公众号排版", "公众号定稿", "出公众号发布清单".

Highlights:

- **Judgments first**: 3–5 required judgments with basis and likely pushback; method, architecture and comparison pieces get at least one diagram of your own.
- **Paste with images**: `md2wechat.py --embed-images` inlines images as base64; hand-written heading numbers are kept; 「·」 lists render one item per line.
- **Preview**: `--preview` renders `out/预览.png` at phone width.

One article = one folder `<title>/` with a single source `<title>.md`; WeChat HTML goes to `out/` only when needed. Legacy `YYYY-MM-DD-name/公众号稿.md` packages stay readable.

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-wechat-post
```

## Usage

```bash
export TOPMIND_WORKSPACE=/path/to/workspace   # recommended: finds the long-form category by name + {year}-公众号; or pass --base

# Create an article folder: <topic>/标题/标题.md + images/ cover/ raw/ out/ 参考/ + 骨架.md, 素材来源.md (--legacy --slug for the old layout)
python3 scripts/new-article.py --title "标题"
A=<topic>/标题

# Structure check: frontmatter, matching titles, images exist and are numbered in order, no ::: / callout / ![[ ]]
python3 scripts/check_article.py $A

# Typography lint + auto-fix (::: containers in new sources are errors)
python3 scripts/lint-wechat.py --input $A/标题.md --fix

# De-AI-flavor (run by topmind-revise when installed): every W needs a decision, H is advisory; score target ≥ 85
python3 scripts/de_ai_lint.py $A/标题.md --genre long
python3 scripts/scan_ai_flavor.py $A/标题.md

# On request: Markdown → fully inline HTML into $A/out/ (--embed-images is mandatory, or pasted images go missing)
python3 scripts/md2wechat.py --input $A/标题.md --embed-images --preview

# Status sync: frontmatter only, folder name unchanged
python3 scripts/sync-status.py --set 定稿 $A --apply
```

Scripts use Python stdlib only — zero dependencies.

## Minimal example

Input `demo.md`:

    # Title

    Opening hook paragraph.

    ## 一、Chapter One

    Body text with **emphasis**.

    ![diagram](images/a.png)

    来源：official project docs

```bash
# first drop a real image at images/a.png next to demo.md (missing files land in the
# checklist as "not embedded" and will be lost on paste)
mkdir -p images && cp /path/to/your-image.png images/a.png
python3 scripts/md2wechat.py --input demo.md --out-dir demo --slug demo --embed-images
```

Output `demo/demo-公众号版.html` (open in a browser → click "复制正文" → paste into the WeChat editor):

```html
<!-- hand-written "一、" is kept as written, no extra auto number (auto numbering only when no h2 has one; --auto-number restores the old behavior) -->
<h2 ...>一、Chapter One</h2>
<!-- a "来源：" line right after an image renders as a small gray caption -->
<!-- images inlined as base64, pasted along with the text -->
<img src="data:image/png;base64,iVBORw0KGgo..." ...>
```

Also generated: `demo/图片上传清单.md` — the upload checklist for images, mermaid diagrams, and reference links.

## md2wechat parameters

| Flag | Description |
|------|-------------|
| `--input` | Required: input md (`<title>.md` in the new layout) |
| `--out-dir` / `--slug` | Optional: default to `<input dir>/out` and the input file name |
| `--auto-number` | Strip hand-written h2 numbers and auto-number (old behavior); by default hand-written numbers are kept |
| `--embed-images` | Inline images as base64 (mandatory, or pasted images go missing) |
| `--theme` | Theme id / Chinese name / JSON path, or `genre:<topic>` for auto-pick; `--list-themes` shows all |
| `--link-mode` | Link rendering: `footnote` (default: superscript `[n]` + end-of-article "参考链接") / `inline` (label normal, URL gray: `文字（url）`) / `note` (whole block gray small text: `文字（url）`) |
| `--asset-root` | Asset root dir, resolves `../assets/`-style image paths in the draft (defaults to the input dir) |
| `--no-toc` | Skip the auto-inserted "本文看点" reading guide |
| `--signature` / `--author` / `--author-bio` | Closing signature: `auto` (default, skipped if the draft has one) / `on` / `off`, name and bio |
| `--no-pangu` | Disable automatic CJK/Latin spacing |
| `--render-mermaid` | Render mermaid to PNG when mmdc is available |

## Three paths

- **forward**: draft → WeChat article (review & rewrite)
- **reverse**: original topic → WeChat article → optional pushback
- **curated web**: online curated sources → handled as reverse

## Three quality gates

Facts (first-hand sources) / logic (structural consistency) / copy (de-AI-flavor ≥ 85).

## Related skills

- Cover art → `topmind-cover` (shared X long-form / WeChat cover)
- X long-form → `topmind-x-article` (Markdown draft → one-click X publish package)

## External dependencies

None required. De-AI rules and checks ship with the skill (`references/de-ai-rules.md`, `scripts/lint_x_post.py --md`, `scripts/scan_ai_flavor.py`). To plug in your own scanner, set `$TOPMIND_AI_SCAN=/path/to/script.py`; arguments and exit code are forwarded unchanged.

## Development

```bash
python3 scripts/package_skill.py --check
python3 scripts/negative_tests.py
```

## Original examples

Sample outputs written by us (fictional or neutral topics, no third-party text) are in [`examples/`](./examples/).
