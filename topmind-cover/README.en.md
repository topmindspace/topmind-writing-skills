# topmind-cover · Cover Art Generation

**[中文](./README.md)** | English

A reusable skill for generating cover art for X long-form posts and WeChat articles. Goal: **striking, eye-catching, theme-focused**.

- Version: **v0.4.9** (ships with `@topmindspace/topmind-writing-skills@0.8.37`)

## Style gallery

<p align="center">
  <img src="https://github.com/topmindspace/topmind-writing-skills/raw/main/topmind-cover/assets/examples/overview.png" alt="topmind-cover · 22 cover-style overview" width="960" />
</p>

22 styles (clean white / background blur / paper collage / news flash / giant-type manifesto / tutorial steps / minimalist / editorial magazine / 3D cute-toy / anime desk / diorama book / academic print / gallery grid / dark SaaS / cinematic flow / hardcore 3D type / viral dry-goods / brand launch / fun IP / orange warm / sketch cartoon / cyber neon, light-first ordering): use cases, palette stories, abstract design principles, and Chinese+English prompt recipes in [`references/cover-styles.md`](./references/cover-styles.md); full-size per-style shots in [`assets/examples/`](./assets/examples/). Prefer writing your own prompts and sending them straight to an image model (bypassing the skill)? See [`references/cover-prompts.md`](./references/cover-prompts.md) — a copy-paste prompt compendium plus cross-platform viral-cover research.

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-cover
```

## Usage

0. **Pick a style combo**: choose a main style (1 of 22, light-first) from `references/cover-styles.md`, then a secondary style from section 4 of [`references/scene-builder.md`](./references/scene-builder.md); check the example image.
1. **Refine the title**: lock the title copy first (usually ≤ 10 chars, split into 2–3 lines with size contrast) using that style's title rules; no drawing yet.
2. **Seven-layer scene recipe**: theme → metaphor / conflict → hero (optionally the TopMind chick / cat / plant IP) → an action that interacts with the title → 2–4 props → ≥3 background layers → light. No recognizable real people.
3. **2–3 options by default**: option card `Option A | metaphor | style: main + secondary | layout: L1–L10 | palette`, differing in at least three of the four; never repeat the main style on consecutive covers.
4. **Compose and generate**: fill every slot of the layered CN/EN template in `scene-builder.md`; pick 1 main + 1 secondary title treatment from the 24 in `typography-system.md`, plus chips / buttons / corner badges. For long titles or misrendered text use path B: generate the scene with a clean title area, then overlay the title with `scripts/overlay-title.py`.
5. **Score and self-check** (required): six-dimension score (richness / topic fit / title treatment / depth / readability / texture) must total ≥ 20 with no item ≤ 2, then pass the [impact self-check list](./SKILL.md#冲击力自检清单); otherwise revise and regenerate (max 3), then switch options.
6. Crop and save:

```bash
python3 scripts/crop-cover.py <main-image> --out-dir <package>/images/
# produces 00-封面.png (1500x600) + 00-封面-公众号.png (900x383, center crop)

# X short-post cover: generate a separate 16:9 master
python3 scripts/crop-cover.py <16:9-image> --preset x-post --out-dir <dir>
# produces 00-封面-X短文.png (1200x675)

# Path B: scene background + scripted title overlay (line sizes, keyword color, stroke, shadow, marker underline, chips)
python3 scripts/overlay-title.py <background> <spec.json> --out <cover> [--font <font>]
```

## Sizes

| Platform | Size | Aspect |
|----------|------|--------|
| X Article cover | 1500x600 | 5:2 (master image) |
| WeChat cover large image | 900×383 | 2.35:1 (center crop) |
| X short-post cover | 1200×675 | 16:9 (generated separately) |

## Design rules

One image, one theme; subject fills 40%+ of the frame; big title ≤ 10 chars, high contrast; avoid clutter, tiny dense text, and competing subjects. **Safe-zone rule**: title text and key subject must stay inside the central vertical 60% safe zone.

## Development

```bash
python3 scripts/package_skill.py --check
python3 scripts/negative_tests.py
```
