# topmind-wechat-post · WeChat Article Authoring

**[中文](./README.md)** | English

Full lifecycle for WeChat articles: delivery package, review & rewrite, three quality gates, status sync, WeChat inline typography, and publish checklist.

- Version: **v0.3.1** (ships with `@topmindspace/topmind-writing-skills@0.8.23`)

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-wechat-post
```

## Usage

```bash
export TOPMIND_WORKSPACE=/path/to/workspace   # recommended: finds the long-form category by name + {year}-公众号; or pass --base

# Create a new delivery package
python3 scripts/new-article.py --slug demo --title "标题" --direction reverse

# Typography lint + auto-fix
python3 scripts/lint-wechat.py --input <package>/公众号稿.md --fix

# De-AI-flavor scan (target ≥ 85)
python3 scripts/scan_ai_flavor.py <package>/公众号稿.md

# Markdown → fully inline HTML (--embed-images is mandatory, or pasted images go missing)
python3 scripts/md2wechat.py --input <package>/公众号稿.md --out-dir <package> --slug demo --embed-images

# Status sync
python3 scripts/sync-status.py --set 定稿 <package> --apply
```

Scripts use Python stdlib only — zero dependencies.

## Minimal example

Input `demo.md`:

    # Title

    Opening hook paragraph.

    ## Chapter One

    Body text with **emphasis**.

    ![diagram](images/a.png)

```bash
# first drop a real image at images/a.png next to demo.md (missing files land in the
# checklist as "not embedded" and will be lost on paste)
mkdir -p images && cp /path/to/your-image.png images/a.png
python3 scripts/md2wechat.py --input demo.md --out-dir demo --slug demo --embed-images
```

Output `demo/demo-公众号版.html` (open in a browser → click "复制正文" → paste into the WeChat editor):

```html
<!-- h2 auto-numbered; closing chapters like "总结" get ∞ -->
<h2 ...><span ...>1</span>Chapter One</h2>
<!-- images inlined as base64, pasted along with the text -->
<img src="data:image/png;base64,iVBORw0KGgo..." ...>
```

Also generated: `demo/图片上传清单.md` — the upload checklist for images, mermaid diagrams, and reference links.

## md2wechat parameters

| Flag | Description |
|------|-------------|
| `--input` / `--out-dir` / `--slug` | Required: input md, output dir, filename slug |
| `--embed-images` | Inline images as base64 (mandatory, or pasted images go missing) |
| `--theme` | Theme id / Chinese name / JSON path, or `genre:<topic>` for auto-pick; `--list-themes` shows all |
| `--link-mode` | Link rendering: `footnote` (default: superscript `[n]` + end-of-article "参考链接") / `inline` (label normal, URL gray: `文字（url）`) / `note` (whole block gray small text: `文字（url）`) |
| `--asset-root` | Asset root dir, resolves `../assets/`-style image paths in the draft |
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

The following skills live **outside this repo** (usually provided by the user's local workbuddy environment). Missing ones degrade or disable the corresponding capability; all scripts in this repo still work fully:

- `humanizer-zh`: fidelity boundaries for Chinese de-AI-flavor; without it the "de-AI-flavor only, no typesetting" path is unavailable.
- `qu-aiwei-zh`: Chinese de-AI-flavor scan (canonical, includes the author-stance layer). `scripts/scan_ai_flavor.py` forwards to it when found and falls back to a bundled implementation (wording score only, with a warning) when not.

## Development

```bash
python3 scripts/package_skill.py --check
python3 scripts/negative_tests.py
```
