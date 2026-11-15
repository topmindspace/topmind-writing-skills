# topmind-cover

English | [中文](./README.md)

Design high-impact article covers, social image-post covers, and video thumbnails for WeChat, X (Articles & Posts), Xiaohongshu, and Douyin. Built around modern visual trends—Swiss editorial typography, Bento modular cards, highlighted source-evidence collages, tactile macro materials, and hand-drawn whiteboard breakdowns—while keeping prompts concise so AI image models can perform at their best.

Chinese is the default language; user instructions and brand assets take priority. See [SKILL.md](./SKILL.md) for the full workflow.

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-cover
```

A scoped knowledge pack ships with this skill. See [knowledge-library.md](./references/knowledge-library.md) and the [card directory](./knowledge/README.md).

## Key References & Specimens

- [Cover Styles (cover-styles.md)](./references/cover-styles.md): 5 modern cover trends and 22 visual starting points
- [Cover Prompts (cover-prompts.md)](./references/cover-prompts.md): Concise, art-director-level prompts for both native text-rendering models and negative-space + deterministic overlay workflows
- [Composition Patterns (cover-patterns.md)](./references/cover-patterns.md) & [Medium Combos (cover-combos.md)](./references/cover-combos.md): 16 focal-point structures and 24 cross-medium palettes
- [Platform Cover Specs (platform-cover-specs.md)](./references/platform-cover-specs.md): Exact aspect ratios, resolutions, and safe-zone strategies across WeChat, X, Xiaohongshu, and Douyin
- [Interactive Layout Atlas (creative-atlas.html)](./assets/examples/creative-atlas.html) & [Sample Guide](./assets/examples/README.md)

## Cropping & Typography Tools

Run from this skill directory (requires Pillow; `title-engine.py` also requires NumPy):

```bash
# Default: X Article (1500×600) + WeChat wide cover (900×383)
python3 scripts/crop-cover.py master.png --out-dir output

# WeChat wide (900×383) + square share card (900×900) cropped independently from source
python3 scripts/crop-cover.py original.png --preset wechat --anchor center --out-dir output

# X post (1200×675) / Xiaohongshu & Douyin 3:4 portrait (1080×1440)
python3 scripts/crop-cover.py master.png --preset x-post --out-dir output
python3 scripts/crop-cover.py portrait.png --preset xiaohongshu --out-dir output

# Landscape pair (16:9 1920×1080 master -> exports 1920×1080 + central 4:3 1080×810)
python3 scripts/crop-cover.py landscape-16x9.png --preset landscape-pair --out-dir output

# Vertical pair (9:16 1080×1920 master -> exports 1080×1920 + central 3:4 1080×1440)
python3 scripts/crop-cover.py vertical-9x16.png --preset vertical-pair --out-dir output
```

Use `python3 scripts/title-engine.py --list-fonts` to inspect local fonts. Proofread every character, verify thumbnail legibility near 300 px wide, and label conceptual feature illustrations honestly (`功能示意，不是实拍`).

Deliver the requested image files; these skills do not publish externally. MIT License. See the [collection](https://github.com/topmindspace/topmind-writing-skills).
