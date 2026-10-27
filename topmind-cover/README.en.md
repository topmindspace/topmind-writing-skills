# topmind-cover

English | [中文](./README.md)

Design article covers and thumbnails using typography, photography, minimal layouts, scenes or original combinations. Inspect actual specimens, proofread text and verify the requested crops. Chinese is the default language; current user instructions and author samples take priority. See [SKILL.md](./SKILL.md) for the capability, workflow and tools.

Supports Xiaohongshu image notes, ordinary Douyin image posts, WeChat articles and X. Identify the publishing surface first. The [platform reference](./references/platform-cover-specs.md) records sources, verification dates and untested details; export presets are not universal upload requirements. WeChat image messages, Douyin commerce content and product images need their own checks.

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-cover
```

A scoped knowledge pack ships with this skill. See [retrieval and contribution](./references/knowledge-library.md) and the [card directory](./knowledge/README.md). Read relevant summaries before selected cards; capture new local notes as candidates, without rewriting global preferences.

## How it works

Read actual references and relevant [specimens](./references/creative-practice.md). Explore distinct directions when that helps the task; deliver one complete result when the request is clear. Voice, length, emoji, structure and visual styles are choices rather than universal gates. Facts, attribution, privacy, authorization and usable output still matter.


The [layout atlas](./assets/examples/creative-atlas.html) contains eight HTML/CSS studies with landscape and portrait views. The [sample directory](./assets/examples/README.md) explains PNGs, title specs and distribution differences.

## Tools

Run from this skill directory, using actual input paths:

```bash
python3 scripts/crop-cover.py 主图.png --out-dir 输出目录
python3 scripts/crop-cover.py portrait.png --preset xiaohongshu --out-dir output
python3 scripts/crop-cover.py portrait.png --preset douyin --out-dir output
python3 scripts/crop-cover.py original.png --preset wechat --anchor left --out-dir output
```

The default `article` preset keeps both landscape outputs (1500×600 and 900×383); `x-post` exports 1200×675; `xiaohongshu` / `douyin` export 1080×1440; `wechat` exports 900×383 and 900×900. These are package presets. Check the current editor and user specifications. Use `--anchor center|left|right|top|bottom` to adjust crop alignment. Every output is cropped proportionally from the original. Recompose when titles or subjects are cut; inspect every version. The script refuses to overwrite its source image.

Cropping requires Pillow; title tools also need NumPy. Typography and decoration suggestions support design decisions; malformed input still needs correction. Proofread and inspect every final crop.

Deliver the requested text or artifacts; these skills do not publish externally. MIT License. See the [collection](https://github.com/topmindspace/topmind-writing-skills) for installation options and maintenance.
