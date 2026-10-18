# topmind-writing-skills

**[中文](./README.md)** | English

> Language note: **Chinese is the default** (`README.md`). This file is the full English parallel.

[![Release](https://img.shields.io/github/v/release/topmindspace/topmind-writing-skills?style=flat-square&color=blue)](https://github.com/topmindspace/topmind-writing-skills/releases)
[![npm](https://img.shields.io/npm/v/@topmindspace/topmind-writing-skills?style=flat-square)](https://www.npmjs.com/package/@topmindspace/topmind-writing-skills)
[![CI](https://img.shields.io/github/actions/workflow/status/topmindspace/topmind-writing-skills/ci.yml?style=flat-square&label=CI)](https://github.com/topmindspace/topmind-writing-skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

**TopMindSpace writing-skills collection** — WeChat articles, X long-form posts, short-form briefs, viral short posts, revision and quality checks, cover art, long-image rendering: seven skills, one repo.

<p align="center">
  <img src="docs/assets/writing-cover.png" alt="topmind-writing-skills · writing skills collection" width="960" />
</p>

> The formal business presentation skill now lives on its own: [`topmind-presentation`](https://github.com/topmindspace/topmind-presentation) (repo `topmind-presentation`; the repo is the skill — clone and copy the root into your skills directory).

### topmind-wechat-post · WeChat article authoring

Full lifecycle for WeChat articles: single-source article folder (`<title>/<title>.md`), review & rewrite, three quality gates (run by topmind-revise by default: facts / logic / de-AI-flavor), WeChat inline typography on request (images must be embedded, output goes to `out/`), publish checklist and status sync. Hand-written heading numbers are kept as written; legacy `公众号稿.md` packages stay readable. Python stdlib only — zero dependencies.

```bash
npx @topmindspace/topmind-writing-skills install topmind-wechat-post
```

### topmind-x-article · One-click X long-form publishing

Delivers one `<title>.md` by default (after topmind-revise); when you want to post on X, derives into `out/` on request: one-click-copy HTML (rich text; reads the source's `![]()` lines and embeds images in order, "来源：" lines become captions) / plain-text fallback (`md2x.py`: images → `[图N]`, tables → "item: value" lists, lists → "·" / "1）" with emoji optional, because plain-text X does not render Markdown lists) + cover art + publish checklist. Publishing is done by hand-pasting; fetch the text back for verification after posting.

```bash
npx @topmindspace/topmind-writing-skills install topmind-x-article
```

### topmind-briefs · Short-form briefs

Short-form briefs for WeChat + X: one topic, one chart (data rankings / paper explainers / product alerts / mechanism explainers). A brief is not long-form: **no HTML by default**. Workflow: verify first-hand sources → find the original post and images → write (no AI tone, a real hook) → lay out (sensible paragraphs and lists). The X version is one copy-ready plain-text block (emoji optional, 0–2 hashtags); **links (with source and publish time), 1–2 original images and generated images are sent separately**; the WeChat version is ~300–800 Chinese characters of Markdown. Draft only — never auto-post.

```bash
npx @topmindspace/topmind-writing-skills install topmind-briefs
```

### topmind-viral-posts · X viral short posts

18 post types plus hook × body × closer combinations, summarised from common high-engagement writing patterns in the Chinese X community (all examples are original): **duanzi layout** (one sentence per line, a blank line between lines), conversational tone, an engagement hook; original images first; asks before generating one via `topmind-cover`. Hashtags (1–3) are part of the post body; classification tags (type / purpose / platform / tone) are listed separately. Duanzi posts use no emoji at all — no persona motif, no reaction emoji, no bullet symbols; bullets are plain lines separated by blank lines. Each post body is one copy-ready plain-text block; links, original images and generated images are sent separately.

```bash
npx @topmindspace/topmind-writing-skills install topmind-viral-posts
```

### topmind-format · X plain-text formatter

Paste existing text: **to duanzi** → one sentence per line with blank lines between, all emoji and bullet symbols removed; **to short post** → paragraphing, lists as 「·」/「1）」 or emoji; title emoji and persona motif optional. Layout only — words never change; `format_text.py` enforces fidelity and pulls links, source lines and image notes out of the body to be sent separately.

```bash
npx @topmindspace/topmind-writing-skills install topmind-format
```

### topmind-revise · Revision and quality check

Makes a draft shorter, more accurate and closer to the author's voice, and proves the facts survived. Four modes: audit (report only), revise (back up, then write back), embed (called by the WeChat / X long-form skills; returns only the final draft) and quick (titles, short posts, one-liners, replies). Pipeline: ⓪ structure review → facts → logic → cut redundancy → de-AI → voice check → layout → fidelity check → over-edit check; `revise_check.py` diffs numbers, quotes, proper nouns and hedging words, and reports the share of clean paragraphs that were rewritten anyway.

```bash
npx @topmindspace/topmind-writing-skills install topmind-revise
```

### Shared X plain-text rules (all skills that output X text)

Single source in `shared/references/`, distributed to each skill's `references/` via the manifest:

| Doc | Covers |
|---|---|
| `x-delivery-contract.md` (must read) | Short-post workflow: sources → original post/images → content → layout; emoji optional for short posts (bullets default to 「·」, 「1）」 for longer lists, emoji only for short lists, 【headings】 for longer posts), none at all in duanzi; never `- ` / `1. `; the X short-post / duanzi body is one copy-ready plain-text block (hashtags last); **links (including sources), original images and generated images are sent separately**; X long-form and WeChat articles may keep in-text links |
| `x-post-format.md` | No Markdown, bullet sets, spacing, sources, skeletons, images, WeChat → X |
| `emoji-system.md` | The TopMind emoji system (short posts only, optional): 0–2 persona motifs (🐔 🐱 🌱) at start/end; 0–1 keyword-matched title emoji; one bullet set per post |
| `x-layout-patterns.md` | Layout patterns in our own words |

Checks: `lint_x_post.py` reports three levels. **E errors** (E1–E9 Markdown leftovers; E10–E12 URLs / source lines / image notes in the body) must be zero. **W warnings** (W9 AI-sounding phrases, W10 first line too long, W12 notes / internal tags, W14 paragraph too long, W15 / W16 Chinese / English structural patterns, W17 punctuation tics, W18 self-made image without data source, W19 「name 说：」, W20 transition sentences, W21 retelling an image; W13 any emoji in a duanzi post with `--duanzi`) each need a decision. **H hints** (context words, news-style precision, parallel closing lines, emoji density, etc.) are advisory and never fail `--strict`. Pick the genre with `--genre long|short|duanzi|reply|title`; hide hints with `--no-hints`. The de-AI part shares one rule set with `de_ai_lint.py` (`de-ai-rules.md`).

### topmind-cover · Cover art generation

Shared cover art for X long-form and WeChat: striking, eye-catching, theme-focused. **Theme → seven-layer scene recipe → 2–3 style-combo options → layered prompt → seven-item score** (default: whole-image generation from 16 prompt patterns + character proofing and local fixes; fallback: scene + `title-engine.py` overlay), then one-click crop to both platform sizes with `crop-cover.py` (X 1500×600, WeChat 900×383). 22-style index and recipes: [`references/cover-styles.md`](./topmind-cover/references/cover-styles.md).

```bash
npx @topmindspace/topmind-writing-skills install topmind-cover
```

<p align="center">
  <img src="https://github.com/topmindspace/topmind-writing-skills/raw/main/topmind-cover/assets/examples/overview.png" alt="topmind-cover · 22 cover-style overview" width="960" />
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


## Writing philosophy: principles first

Social posts exist to get information and a point of view across: clear, simple, easy to read, with charts and lists instead of long paragraphs wherever the content allows. So these skills start with how to think, and only then with what to avoid. The writing skills share one layered rule set (`shared/references/`, copied into each skill so standalone installs work):

| Layer | Files | Covers |
|---|---|---|
| 0 · Principles | `social-writing-principles.md` | 8 principles: know what you want to say, lead with the conclusion, every sentence adds something new, form follows content, plain everyday words, originals and data over paraphrase, stand on the reader's side, honest and measured |
| 1 · Information design | `information-design.md` | Skeleton before prose, a content → form decision table (list / table / image / paragraph), length and density reference lines, ways to spot padding |
| 2 · Voice | `core-voice.md` | Ten wording principles; V01–V33 are worked examples for titles, openings, numbers, quotes, replies, jokes |
| Review · De-AI | `de-ai-rules.md` + `de_ai_lint.py` | Pattern table (Z / E / P) grouped by root cause; used for self-review and revision only, not while drafting |
| Execution | `topmind-revise` | ⓪ structure review → facts → logic → cut redundancy → de-AI → layout → fidelity check → over-edit check, with a revision report |

Also:

- **Principles are written as why + how to judge + example**: examples show the thinking, not a word list; concrete revision cases stay examples, never hard gates.
- **Originals first** (`image-sourcing.md`): find official / original-post / third-party images before writing and log sources in the private `素材来源.md` inside the article folder; self-made charts are a fallback and must be labeled 自制 with the data source.
- **Long-form starts with a skeleton**: `article_scaffold.py` creates `骨架.md` in the article folder (main message, reader, per-section points / form / chart plan / length), so the form is decided before drafting.
- **Scripts hint, people decide**: each W warning needs a decision (not a zero count); H hints and I1–I8 information-design hints are advisory and never part of `--strict`; the regression sets `scripts/test_lint_rules.py` and `scripts/test_info_design.py` keep normal writing from being flagged.
- **Revise only what is wrong**: rewrite boundaries first (change wording, never facts or certainty); by default only low-risk structural edits (parallel paragraphs → list, comparisons → table, remove repeats); reordering sections needs `depth=structure`.

## Original examples

Every skill ships sample outputs written by us (fictional or neutral topics; no third-party text or images):

| Skill | Examples |
|---|---|
| topmind-viral-posts (one-liners) | [`topmind-viral-posts/examples/`](./topmind-viral-posts/examples/) |
| topmind-briefs (short posts) | [`topmind-briefs/examples/`](./topmind-briefs/examples/) |
| topmind-format (formatting) | [`topmind-format/examples/`](./topmind-format/examples/) |
| topmind-revise (revision) | [`topmind-revise/examples/`](./topmind-revise/examples/) |
| topmind-x-article (X long-form) | [`topmind-x-article/examples/`](./topmind-x-article/examples/) |
| topmind-wechat-post (WeChat) | [`topmind-wechat-post/examples/`](./topmind-wechat-post/examples/) |
| topmind-poster (posters) | [`topmind-poster/examples/`](./topmind-poster/examples/) |
| topmind-cover (covers) | [`topmind-cover/assets/examples/`](./topmind-cover/assets/examples/) |

## Skills

> Terms: **short post (短文)** = a plain-text X post, anything up to about 1000 Chinese characters (no 280-character limit); **long-form (长文)** = an X Article; **duanzi (段子)** = a one-sentence-per-line short-post style.


| Skill | Version | What it does |
|-------|---------|--------------|
| [`topmind-wechat-post`](./topmind-wechat-post/) | **0.3.16** | WeChat article lifecycle: single-source article folder, review, 3 quality gates (revise by default), inline typography on request & publish checklist |
| [`topmind-x-article`](./topmind-x-article/) | **0.4.22** | X long-form: single-source Markdown (revise by default) → on-request one-click-copy HTML (images/prompt copy, click-to-zoom images) / plain-text fallback + cover + checklist |
| [`topmind-cover`](./topmind-cover/) | **0.4.13** | Cover art for X / WeChat (X master 1500×600 / 5:2): striking, theme-focused; 22-style cover style library + 16:9 X short-post cover scene + 24 title treatments + 7-layer scene recipe + 55 example images (22 styles × 2 sizes + 11 variant samples) + 1 style overview |
| [`topmind-briefs`](./topmind-briefs/) | **0.2.24** | Short-form briefs (WeChat + X): one topic, one chart; data rankings / paper explainers / product alerts / mechanism explainers; sources → images → content → layout; one copy-ready plain-text X block (no HTML by default, emoji optional, no AI tone), links / images sent separately; asks before generating any image |
| [`topmind-viral-posts`](./topmind-viral-posts/) | **0.3.16** | X viral short posts: 18 template types + combinations, duanzi layout (blank lines, no emoji, plain bullet lines), one copy-ready plain-text block per post with hashtags last, links / images sent separately, classification tags listed separately; asks before generating an image |
| [`topmind-format`](./topmind-format/) | **0.1.9** | X plain-text formatter: to duanzi (blank lines, no emoji) / to short post (paragraphing + sensible lists, emoji optional); layout only, words unchanged, with a fidelity check; one copy-ready plain-text body, links / images sent separately |
| [`topmind-revise`](./topmind-revise/) | **0.1.1** | Revision and quality check: edit, tighten, de-AI, three quality gates and fidelity audit; four modes (audit / revise / embed / quick); every change maps to a rule code, with an over-edit guard; the long-form skills use it by default |
| [`topmind-poster`](./topmind-poster/) | **0.1.6** | HTML+CSS → high-res long image / poster / infographic PNG: headless Chrome 2× screenshot + auto-trim; "one image per section" batch workflow (generator + renderer) |

Installer [`@topmindspace/topmind-writing-skills`](https://www.npmjs.com/package/@topmindspace/topmind-writing-skills) is **0.8.45** (whole-repo same-tag releases).

### Which skill, and how they combine

| Task | Skill | Typical combination |
|---|---|---|
| A data-driven brief (numbers, rankings, launches) | `topmind-briefs` | → `topmind-format` for layout; no original image → `topmind-cover` 16:9 |
| Engagement jokes, follower posts | `topmind-viral-posts` | → `topmind-format` to re-lay duanzi; pair with a briefs version for the same event |
| Existing text, layout only | `topmind-format` | words unchanged; rewriting → `topmind-revise` |
| Edit, tighten, de-AI, quality check | `topmind-revise` | standalone, or called by x-article / wechat-post after drafting |
| Thousands-of-words X article | `topmind-x-article` | + `topmind-revise` + `topmind-cover` (5:2); shorter than a post → briefs |
| WeChat long-form & layout | `topmind-wechat-post` | + `topmind-revise` + `topmind-cover`; 300–800-char briefs → briefs |
| Long images, posters, infographics | `topmind-poster` | copy written first by briefs / wechat-post |

> SKILL.md frontmatter uses only Agent Skills spec keys at the top level (`name` / `description` / `license` / `metadata`); version, `action_category`, `triggers` and other custom keys live under `metadata` as strings, so `skills-ref validate` passes. Shared scripts and references (`social-writing-principles.md`, `information-design.md`, `core-voice.md`, `de-ai-rules.md` and more) have a single source in `shared/`; skill folders keep byte-identical copies (CI checks with `node scripts/sync_shared.js --check`). The npm package ships only `overview.png` from the cover examples; the per-style samples stay on GitHub / in the Release zip.

## Install

**npm = pinned snapshot**; **GitHub = track repo HEAD**.

```bash
npx @topmindspace/topmind-writing-skills list
npx @topmindspace/topmind-writing-skills install topmind-briefs
npx @topmindspace/topmind-writing-skills install topmind-briefs --to ./.claude/skills
npx @topmindspace/topmind-writing-skills@latest install topmind-briefs   # upgrade: older install is overwritten, no --force needed
npx @topmindspace/topmind-writing-skills install topmind-briefs --force   # reinstall same version / downgrade
npx @topmindspace/topmind-writing-skills@0.8.4 install topmind-briefs   # pin (needs --force if a newer version is installed)
npx @topmindspace/topmind-writing-skills uninstall topmind-briefs --to ./.claude/skills
```

```bash
# track HEAD
npx github:topmindspace/topmind-writing-skills install topmind-briefs
```

Default probe order: `./.agents` → `./.claude` → `./.cursor` → `./.codex` → `./.mimocode`, then user-level `~/.claude`, etc. Or pass `--to`. When `--to` is omitted, the install summary explicitly prints the auto-detected target directory. Do not `npm install topmind-briefs` (skill id is not a standalone package).

`install` details: upgrades by default: if the installed version is older (or unreadable), it is overwritten in place (no backup) and `Upgraded <skill> <old> -> <new>` is printed; the same version prints `Already up to date` (`--force` reinstalls); an installed version newer than the package is refused unless `--force`. On success, a three-line summary is printed: where it was installed / installed skill version and installer version / next steps.

## Repo layout

```
topmind-writing-skills/
├─ topmind-briefs/                    # skill (SKILL.md + assets + references + scripts)
├─ topmind-viral-posts/               # skill (X viral short posts, duanzi layout)
├─ topmind-format/                    # skill (X plain-text formatter: duanzi / short post)
├─ topmind-revise/                    # skill (revision and quality check)
├─ topmind-poster/                    # skill (HTML → high-res long image / section images)
├─ topmind-cover/                     # skill
├─ topmind-wechat-post/               # skill
├─ topmind-x-article/                 # skill
├─ bin/topmind-writing-skills.js      # CLI: list / install / uninstall
├─ shared/                            # single source for shared scripts + writing principles (manifest.json lists targets)
├─ evals/                             # routing eval cases (not shipped to npm)
├─ docs/                              # publishing guide · CI notes
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
