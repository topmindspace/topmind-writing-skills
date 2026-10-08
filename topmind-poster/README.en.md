# topmind-poster · HTML → High-Res Long Image PNG

**[中文](./README.md)** | English

Rankings, infographics, monthly-report long images, posters — plus the "one image per section" workflow for splitting a long article into N shareable images. Text is 100% controllable, diffable, and iterable.

- Version: **v0.1.1** (ships with `@topmindspace/topmind-writing-skills@0.8.24`)

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-poster
```

## Why not an image generation model

Rankings and infographics carry dense precise text, numbers and brand names. Image models mangle characters, blur glyphs and invent figures. **These images must go through "HTML layout → headless browser screenshot"**. Covers are the exception — they have no dense text, so they use the generative route in `topmind-cover`.

## What it does

| Scenario | Output |
|---|---|
| Rankings / tiers / infographics | One vertical long image (1080 or 1180 wide, 2× retina) |
| Monthly / weekly report long image | Same, may contain chart cards |
| N images for one long article | Section images: one image per section, each shareable alone |
| Existing HTML | Export high-res PNG directly, auto-trimmed bottom whitespace |

## Usage

One command does it all:

```bash
python3 scripts/render_poster.py poster.html -o poster.png
```

The script runs three steps: headless Chrome 2× screenshot → scan the bottom by background color → crop the whitespace. Batch mode for section images:

```bash
python3 scripts/render_poster.py build/*.html --out-dir images/ --width 1180
```

Manual workflow, parameter semantics and 7 battle-tested pitfalls (sandbox flags, invisible bar fills, background sampling point, PNG resampling getting *larger*, …) live in [SKILL.md](./SKILL.md). Layout recipes are in [references/layout-recipes.md](./references/layout-recipes.md).

## Requirements

- Headless browser: Chrome / Chromium / Edge (`--chrome`, or `CHROME_PATH`)
- `Pillow` (for cropping): `python3 -m pip install --user Pillow`

## Boundaries

- **Not** article covers → `topmind-cover`
- **Not** multi-page decks / PPTX → `topmind-presentation`
- **Not** pure data-chart SVG → `svg-infographic-kit`
- **Not** article body layout → `topmind-wechat-post` / `topmind-x-article`

This skill owns the rendering step: they write the article, this skill turns a section of it into a standalone shareable image.
