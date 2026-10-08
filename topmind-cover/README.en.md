# topmind-cover · Cover Art Generation

**[中文](./README.md)** | English

A reusable skill for generating cover art for X long-form posts and WeChat articles. Goal: **striking, eye-catching, theme-focused**.

- Version: **v0.4.2** (ships with `@topmindspace/topmind-writing-skills@0.8.22`)

## Style gallery

<p align="center">
  <img src="https://github.com/topmindspace/topmind-writing-skills/raw/main/topmind-cover/assets/examples/overview.png" alt="topmind-cover · 19 cover-style overview" width="960" />
</p>

22 styles (clean white / background blur / paper collage / news flash / giant-type manifesto / tutorial steps / minimalist / editorial magazine / 3D cute-toy / anime desk / diorama book / academic print / gallery grid / dark SaaS / cinematic flow / hardcore 3D type / viral dry-goods / brand launch / fun IP, light-first ordering): use cases, palette stories, abstract design principles, and Chinese+English prompt recipes in [`references/cover-styles.md`](./references/cover-styles.md); full-size per-style shots in [`assets/examples/`](./assets/examples/). Prefer writing your own prompts and sending them straight to an image model (bypassing the skill)? See [`references/cover-prompts.md`](./references/cover-prompts.md) — a copy-paste prompt compendium plus cross-platform viral-cover research.

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-cover
```

## Usage

0. **Pick a style**: choose 1 of 22 styles from `references/cover-styles.md` by topic (light-first) → check the example image to confirm the visual language.
1. **Refine the title**: lock the title copy first (usually ≤ 10 chars) using that style's title rules; rewrite until it lands — no drawing yet.
2. **Composition brief**: one-sentence brief (theme / audience / mood / visual metaphor / palette direction) before composing the prompt.
3. Input: article title + 3 theme keywords + platform (x / wechat / both, default both).
4. Generate with the agent's image-generation capability (landscape 5:2, 8% margin on all sides).
5. **Impact self-check** (required): pass every item in the [impact self-check list](./SKILL.md#冲击力自检清单); on failure, tweak the prompt and regenerate, max 3 attempts.
6. Crop and save:

```bash
python3 scripts/crop-cover.py <main-image> --out-dir <package>/images/
# produces 00-封面.png (1500x600) + 00-封面-公众号.png (900x383, center crop)
```

## Sizes

| Platform | Size | Aspect |
|----------|------|--------|
| X Article cover | 1500x600 | 5:2 (master image) |
| WeChat cover large image | 900×383 | 2.35:1 (center crop) |

## Design rules

One image, one theme; subject fills 40%+ of the frame; big title ≤ 10 chars, high contrast; avoid clutter, tiny dense text, and competing subjects. **Safe-zone rule**: title text and key subject must stay inside the central vertical 60% safe zone.

## Development

```bash
python3 scripts/package_skill.py --check
python3 scripts/negative_tests.py
```
