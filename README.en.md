# topmind-writing-skills

**[中文](./README.md)** | English

> Language note: **Chinese is the default** (`README.md`). This file is the full English parallel.

[![Release](https://img.shields.io/github/v/release/topmindspace/topmind-writing-skills?style=flat-square&color=blue)](https://github.com/topmindspace/topmind-writing-skills/releases)
[![npm](https://img.shields.io/npm/v/@topmindspace/topmind-writing-skills?style=flat-square)](https://www.npmjs.com/package/@topmindspace/topmind-writing-skills)
[![CI](https://img.shields.io/github/actions/workflow/status/topmindspace/topmind-writing-skills/ci.yml?style=flat-square&label=CI)](https://github.com/topmindspace/topmind-writing-skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

**TopMindSpace writing-skills collection** — WeChat articles, X long-form posts, short-form briefs, viral short posts, cover art, long-image rendering: six skills, one repo.

<p align="center">
  <img src="docs/assets/writing-cover.png" alt="topmind-writing-skills · writing skills collection" width="960" />
</p>

> The formal business presentation skill now lives on its own: [`topmind-presentation`](https://github.com/topmindspace/topmind-presentation) (repo `topmind-presentation`; the repo is the skill — clone and copy the root into your skills directory).

### topmind-wechat-post · WeChat article authoring

Full lifecycle for WeChat articles: delivery package, review & rewrite, three quality gates (facts / logic / de-AI-flavor), WeChat inline typography (images must be embedded), publish checklist and status sync. Python stdlib only — zero dependencies.

```bash
npx @topmindspace/topmind-writing-skills install topmind-wechat-post
```

### topmind-x-article · One-click X long-form publishing

Markdown draft → paste-ready plain text (`md2x.py` adapts to the X Article editor: images → `[图N]`, tables → "item: value" lists) + cover art + publish checklist. Publishing is done by hand-pasting; fetch the text back for verification after posting.

```bash
npx @topmindspace/topmind-writing-skills install topmind-x-article
```

### topmind-briefs · Short-form briefs

Short-form briefs for WeChat + X: one topic, one chart (data rankings / paper one-liners / product alerts / mechanism explainers). One X post or short thread, WeChat ~300–800 Chinese characters, 1 key visual. One-click-copy HTML for both, draft only — never auto-post.

```bash
npx @topmindspace/topmind-writing-skills install topmind-briefs
```

### topmind-cover · Cover art generation

Shared cover art for X long-form and WeChat: striking, eye-catching, theme-focused. **Pick a style → check the example → compose the prompt from the recipe**, then one-click crop to both platform sizes with `crop-cover.py` (X 1200×675, WeChat 900×383). 11-style index and recipes: [`references/cover-styles.md`](./topmind-cover/references/cover-styles.md).

```bash
npx @topmindspace/topmind-writing-skills install topmind-cover
```

<p align="center">
  <img src="https://github.com/topmindspace/topmind-writing-skills/raw/main/topmind-cover/assets/examples/overview.png" alt="topmind-cover · 19 cover-style overview" width="960" />
</p>

> Let ideas fly — make good thinking visible.

### topmind-poster · HTML → high-res long image

The **rendering step** for rankings, infographics, monthly-report long images and posters: HTML+CSS layout → headless Chrome 2× screenshot → auto-trimmed bottom whitespace. Includes the "one image per section" workflow (generator + renderer) that splits a long article into N individually shareable images. `render_poster.py` runs all three steps in one command; layout recipes (canvas / type scale / light & dark palettes / grid / progress bars) are in [`references/layout-recipes.md`](./topmind-poster/references/layout-recipes.md).

```bash
npx @topmindspace/topmind-writing-skills install topmind-poster
```

> Why not an image generation model: rankings carry dense text and numbers that must be character-exact, and generation mangles glyphs and invents figures. Covers are the exception (no dense text) and go through `topmind-cover`.

> **Rename note**: this repo was renamed from `tms-skills` to `topmind-writing-skills`;
> the npm package is `@topmindspace/topmind-writing-skills` and the old package is no longer updated.
> Also do not install the old package's `^2` (2.0.0–2.1.1 deprecated).

## Skills

| Skill | Version | What it does |
|-------|---------|--------------|
| [`topmind-wechat-post`](./topmind-wechat-post/) | **0.3.2** | WeChat article lifecycle: package, review, 3 quality gates, inline typography & publish checklist |
| [`topmind-x-article`](./topmind-x-article/) | **0.4.9** | X long-form one-click publish: Markdown → one-click-copy HTML (images/prompt copy, click-to-zoom images) / plain-text fallback + cover + checklist |
| [`topmind-cover`](./topmind-cover/) | **0.4.3** | Cover art for X / WeChat (X master 1500×600 / 5:2): striking, theme-focused; 22-style cover style library + 26 example images (incl. 3 alt samples) + 1 style overview |
| [`topmind-briefs`](./topmind-briefs/) | **0.2.9** | Short-form briefs (WeChat + X): one topic, one chart; data rankings / paper one-liners / product alerts / mechanism explainers; one-click-copy HTML for both |
| [`topmind-viral-posts`](./topmind-viral-posts/) | **0.3.3** | X viral short posts: 14 template types (incl. trending-news type); prefer original images (official/third-party), generate only when none exists |
| [`topmind-poster`](./topmind-poster/) | **0.1.2** | HTML+CSS → high-res long image / poster / infographic PNG: headless Chrome 2× screenshot + auto-trim; "one image per section" batch workflow (generator + renderer) |

Installer [`@topmindspace/topmind-writing-skills`](https://www.npmjs.com/package/@topmindspace/topmind-writing-skills) is **0.8.26** (whole-repo same-tag releases).

> SKILL.md frontmatter uses only Agent Skills spec keys at the top level (`name` / `description` / `license` / `metadata`); version, `action_category`, `triggers` and other custom keys live under `metadata` as strings, so `skills-ref validate` passes. Shared scripts and `writing-principles.md` have a single source in `shared/`; skill folders keep byte-identical copies (CI checks with `node scripts/sync_shared.js --check`). The npm package ships only `overview.png` from the cover examples; the per-style samples and `references/cover-study/` images stay on GitHub / in the Release zip.

## Install

**npm = pinned snapshot**; **GitHub = track repo HEAD**.

```bash
npx @topmindspace/topmind-writing-skills list
npx @topmindspace/topmind-writing-skills install topmind-briefs
npx @topmindspace/topmind-writing-skills install topmind-briefs --to ./.claude/skills
npx @topmindspace/topmind-writing-skills@0.8.4 install topmind-briefs   # pin
npx @topmindspace/topmind-writing-skills uninstall topmind-briefs --to ./.claude/skills
```

```bash
# track HEAD
npx github:topmindspace/topmind-writing-skills install topmind-briefs
```

Default probe order: `./.agents` → `./.claude` → `./.cursor` → `./.codex` → `./.mimocode`, then user-level `~/.claude`, etc. Or pass `--to`. When `--to` is omitted, the install summary explicitly prints the auto-detected target directory. Do not `npm install topmind-briefs` (skill id is not a standalone package).

`install` details: if a same-named skill already exists, the installed version is reported and overwriting is refused — pass `--force` to replace (or `uninstall` first). On success, a three-line summary is printed: where it was installed / installed skill version and installer version / next steps.

## Repo layout

```
topmind-writing-skills/
├─ topmind-briefs/                    # skill (SKILL.md + assets + references + scripts)
├─ topmind-viral-posts/               # skill (X viral short posts, one image each)
├─ topmind-poster/                    # skill (HTML → high-res long image / section images)
├─ topmind-cover/                     # skill
├─ topmind-wechat-post/               # skill
├─ topmind-x-article/                 # skill
├─ bin/topmind-writing-skills.js      # CLI: list / install / uninstall
├─ shared/                            # single source for shared scripts + writing principles (manifest.json lists targets)
├─ evals/                             # routing eval cases (not shipped to npm)
├─ docs/                              # publishing guide · CI notes (history archived in docs/archive)
├─ scripts/                           # repo gates / privacy scan
├─ package.json                       # @topmindspace/topmind-writing-skills
└─ LICENSE · CHANGELOG.md · README.md · README.en.md
```

## Release & CI

| Action | GitHub | npm |
|--------|:------:|:---:|
| push main | live | **unchanged** |
| tag `vX.Y.Z` | Release + zip | **auto publish** |

```bash
npm run check && npm run audit && npm run privacy
```

See [docs/PUBLISHING.md](./docs/PUBLISHING.md) · [docs/ci.md](./docs/ci.md).

## License

MIT © TopMindspace — [LICENSE](./LICENSE)
