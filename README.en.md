# topmind-writing-skills

**[中文](./README.md)** | English

> Chinese is the default (`README.md`); this file is the English parallel.

[![Release](https://img.shields.io/github/v/release/topmindspace/topmind-writing-skills?style=flat-square&color=blue)](https://github.com/topmindspace/topmind-writing-skills/releases)
[![npm](https://img.shields.io/npm/v/@topmindspace/topmind-writing-skills?style=flat-square)](https://www.npmjs.com/package/@topmindspace/topmind-writing-skills)
[![CI](https://img.shields.io/github/actions/workflow/status/topmindspace/topmind-writing-skills/ci.yml?style=flat-square&label=CI)](https://github.com/topmindspace/topmind-writing-skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

**TopMindSpace writing skills**: WeChat articles, X long-form, short briefs, viral short posts, formatting, revision, covers and long images — eight skills, one repo. Principles first: decide what you want to say and which form reads best, then worry about wording. Scripts hint; people decide.

<p align="center">
  <img src="docs/assets/writing-cover.png" alt="topmind-writing-skills · writing skills collection" width="960" />
</p>

```bash
npx @topmindspace/topmind-writing-skills list
npx @topmindspace/topmind-writing-skills install topmind-briefs
```

## Skills

> Terms: **short post (短文)** = a plain-text X post, up to about 1000 Chinese characters (no 280-character limit); **long-form (长文)** = an X Article or a WeChat article; **duanzi (段子)** = a one-sentence-per-line short-post style.

| Skill | Version | What it does |
|---|---|---|
| [`topmind-wechat-post`](./topmind-wechat-post/) | **0.3.18** | WeChat long-form: single-source article folder, three quality gates (revise by default), inline typography on request (images embedded), publish checklist and status sync |
| [`topmind-x-article`](./topmind-x-article/) | **0.4.24** | X long-form: single-source Markdown (revise by default) → on-request one-click-copy HTML / plain-text fallback + cover + checklist |
| [`topmind-briefs`](./topmind-briefs/) | **0.2.26** | Short briefs (X + WeChat): one topic, stop when done; sources → original images → content → layout; one copy-ready plain-text X block, links and images sent separately |
| [`topmind-viral-posts`](./topmind-viral-posts/) | **0.3.18** | X viral short posts: 18 templates + hook × body × closer combinations; duanzi layout with no emoji |
| [`topmind-format`](./topmind-format/) | **0.1.11** | X plain-text formatter: to duanzi / to short post; layout only, words unchanged, with a fidelity check |
| [`topmind-revise`](./topmind-revise/) | **0.1.3** | Revision and quality check: ⓪ structure → facts → logic → de-AI → fidelity audit; four modes; every change maps to a rule code |
| [`topmind-cover`](./topmind-cover/) | **0.4.15** | Cover art (X 1500×600 / WeChat 900×383): 22 styles, seven-layer scene recipe, whole-image generation + title proofing |
| [`topmind-poster`](./topmind-poster/) | **0.1.8** | HTML+CSS → high-res long image / poster / infographic: headless Chrome 2× + auto-trim; one image per section |

Installer [`@topmindspace/topmind-writing-skills`](https://www.npmjs.com/package/@topmindspace/topmind-writing-skills) is **0.8.47** (whole-repo, same-tag releases).

## Writing philosophy: principles first

Social posts exist to get information and a point of view across: clear, simple, easy to read; use images, tables and lists instead of long paragraphs wherever the content allows. All writing skills share one layered rule set (single source `shared/references/`, copied into each skill so standalone installs work):

| Layer | Files | Covers |
|---|---|---|
| 0 · Principles | `social-writing-principles.md` | 8 principles: know what to say, conclusion first, every sentence adds something, form follows content, everyday words, originals and data over paraphrase, the reader's side, honest and measured |
| 1 · Information design | `information-design.md` | Skeleton first, content → form table (list / table / image / paragraph), length and density, spotting padding, what the I1–I8 hints mean |
| 2 · Voice | `core-voice.md` | Ten wording principles; V01–V33 are worked examples for titles, openings, numbers, quotes, replies, jokes |
| 3 · Review | `topmind-revise` + `de-ai-rules.md` | ⓪ structure → facts → logic → cut → de-AI → layout → fidelity audit; the de-AI rules are for reviewing finished drafts, not for drafting |

Practices shared by every skill:

- **Principles are written as why + how to judge + example**: examples show the thinking, not a word list. Only real hard constraints (platform limits, facts, compliance) stay strict, labeled 「硬约束」 (hard constraint).
- **Persona: an ordinary person who is still learning** — not an expert, not a lecturer; a little self-mockery is fine; say so when unsure.
- **Originals first** (`image-sourcing.md`): find official / original-post / third-party images before writing and log sources in `素材来源.md`; self-made charts are a fallback, labeled 自制 with the data source.
- **Scripts hint**: E errors must be zero; each W warning needs a decision; H hints and I1–I8 information-design hints are advisory and never part of `--strict`.
- **Revise only what is wrong**: keep rewrite boundaries (wording only, never facts or certainty); reordering sections needs `depth=structure`.

### The long-form article folder

One article, one folder, one source file; `article_scaffold.py` (or wechat-post's `new-article.py`) creates it:

```text
<title>/
├─ <title>.md     the only source (readable in Obsidian; HTML comments with writing notes never reach derived output)
├─ 骨架.md        skeleton: main message, reader, per-section points / form / chart plan / length
├─ 素材来源.md    source for every image and number
├─ images/  cover/
├─ raw/           originals, screenshots, notes (not published)
├─ out/           derived output: X HTML, plain text, WeChat HTML (rebuild any time)
└─ 参考/          same-topic drafts and assets from other environments (reference only, never the source)
```

Multi-environment work (optional): the source frontmatter carries `updated_at` (ISO 8601 with time zone), `updated_env` and `updated_by`; `updated_at` decides which copy is newer. When both sides changed and the order is unclear, nothing is overwritten — the older copy goes into `参考/`. See `workspace.md`. Legacy `公众号稿.md` packages stay readable.

## Which skill, and how they combine

| Task | Skill | Typical combination |
|---|---|---|
| A data-driven brief (numbers, rankings, launches) | `topmind-briefs` | → `topmind-format` for layout; no original image → ask, then `topmind-cover` 16:9 |
| Engagement jokes, follower posts | `topmind-viral-posts` | → `topmind-format` to re-lay duanzi |
| Existing text, layout only | `topmind-format` | words unchanged; rewriting → `topmind-revise` |
| Edit, tighten, de-AI, quality check | `topmind-revise` | standalone, or called by the long-form skills |
| Thousands-of-words X article | `topmind-x-article` | + `topmind-revise` + `topmind-cover` (5:2) |
| WeChat long-form & layout | `topmind-wechat-post` | + `topmind-revise` + `topmind-cover`; 300–800-character pieces → briefs |
| Long images, posters, infographics | `topmind-poster` | copy written first by briefs / wechat-post |

## Skill highlights

### topmind-wechat-post · WeChat long-form

- Single-source article folder; review and rewrite through `topmind-revise` by default; typography output goes to `out/` with base64-embedded images.
- Hand-written heading numbers are kept as written; Python stdlib only.

### topmind-x-article · X long-form

- Delivers only `<title>.md` by default; for X, derives one-click-copy HTML (images embedded in `![]()` order, 「来源：」 lines as captions) or a plain-text fallback (`md2x.py`: images → `[图N]`, tables → "item: value", lists → 「·」 / 「1）」).
- Publishing is a manual paste; fetch the post back afterwards to verify.

### topmind-briefs · Short briefs

- No HTML by default: verify first-hand sources → find the original post and images → write → lay out.
- The X version is one copy-ready plain-text block (emoji optional, 0–2 hashtags); links (with source and publish time) and images are sent separately; the WeChat version is about 300–800 characters. Draft only.

### topmind-viral-posts · X viral short posts

- 18 templates (advice, self-mockery, hot news, little-known facts, contrast, self-Q&A, …) + hook × body × closer combinations; all examples are original.
- Duanzi layout: one sentence per line, blank lines between, no emoji; 1–3 hashtags on the last line, classification tags listed separately.

### topmind-format · X plain-text formatter

- **To duanzi**: one sentence per line with blank lines, emoji and bullets removed; **to short post**: paragraphing, lists as 「·」 / 「1）」 or emoji.
- `format_text.py` changes layout only and checks fidelity; links, source lines and image notes are pulled out to be sent separately.

### topmind-revise · Revision and quality check

- Four modes: audit (report only), revise (back up, then write back), embed (called by long-form skills; returns only the final draft), quick (titles, short posts, one-liners, replies).
- `revise_check.py` diffs numbers, quotes, proper nouns and hedging words, and reports the share of clean paragraphs that were rewritten anyway.

### topmind-cover · Cover art

- Theme → seven-layer scene recipe → 2–3 style combos → layered prompt → seven-item score; whole-image generation with character proofing by default, `title-engine.py` overlay as a fallback.
- `crop-cover.py` crops both platform sizes; style index in [`cover-styles.md`](./topmind-cover/references/cover-styles.md).

<p align="center">
  <img src="https://github.com/topmindspace/topmind-writing-skills/raw/main/topmind-cover/assets/examples/overview.png" alt="topmind-cover · 22 cover-style overview" width="960" />
</p>

### topmind-poster · HTML → high-res long image

- HTML+CSS layout → headless Chrome 2× screenshot → auto-trim, all in `render_poster.py`; layout recipes in [`layout-recipes.md`](./topmind-poster/references/layout-recipes.md).
- Why not an image model: rankings carry text and numbers that must be exact, and generation mangles them. Covers have no dense text and go through `topmind-cover`.

> The business presentation skill lives in its own repo: [`topmind-presentation`](https://github.com/topmindspace/topmind-presentation).

## Shared X plain-text rules

Used by every skill that outputs X text (`shared/references/`):

| Doc | Covers |
|---|---|
| `x-delivery-contract.md` | Short-post workflow (sources → original post/images → content → layout); one copy-ready plain-text body, hashtags last; links and images sent separately |
| `x-post-format.md` | No Markdown, bullet sets, spacing, sources, images, WeChat → X |
| `emoji-system.md` | Emoji system (short posts only, optional): 0–2 persona motifs, 0–1 title emoji, one bullet set per post |
| `x-layout-patterns.md` | Layout patterns: conclusion on the first line, list lead-ins, 【headings】 |

Three output levels of `lint_x_post.py` / `de_ai_lint.py`:

| Level | Meaning | Required |
|---|---|---|
| E error | Markdown leftovers (E1–E9); URLs / source lines / image notes in the body (E10–E12) | must be zero |
| W warning | AI-sounding phrases, long first line, long paragraphs, structural patterns, punctuation tics, unlabeled self-made images, … | each needs a decision: fix, or note why it stays |
| H hint / I1–I8 | context words, parallel closers, emoji density; information design (long runs of prose, list / table candidates, opening that doesn't deliver, …) | advisory, never in `--strict` |

Pick the genre with `--genre long|short|duanzi|reply|title`; hide hints with `--no-hints`.

## Original examples

All examples are written by us (fictional or neutral topics; no third-party text or images): [viral-posts](./topmind-viral-posts/examples/) · [briefs](./topmind-briefs/examples/) · [format](./topmind-format/examples/) · [revise](./topmind-revise/examples/) · [x-article](./topmind-x-article/examples/) · [wechat-post](./topmind-wechat-post/examples/) · [poster](./topmind-poster/examples/) · [cover](./topmind-cover/assets/examples/).

## Install

**npm = pinned snapshot; GitHub = repo HEAD.**

```bash
npx @topmindspace/topmind-writing-skills install topmind-briefs --to ./.claude/skills
npx @topmindspace/topmind-writing-skills@latest install topmind-briefs   # upgrade: an older install is overwritten
npx @topmindspace/topmind-writing-skills install topmind-briefs --force   # reinstall same version / downgrade
npx @topmindspace/topmind-writing-skills@0.8.4 install topmind-briefs     # pin a version
npx @topmindspace/topmind-writing-skills uninstall topmind-briefs --to ./.claude/skills
npx github:topmindspace/topmind-writing-skills install topmind-briefs     # track HEAD
```

- Default probe order: `./.agents` → `./.claude` → `./.cursor` → `./.codex` → `./.mimocode`, then user-level `~/.claude`, etc.; the install summary prints the actual target.
- An older install is overwritten (`Upgraded <skill> <old> -> <new>`); the same version prints `Already up to date`; a newer installed version is never downgraded without `--force`.
- Do not `npm install topmind-briefs`: skill ids are not standalone packages. The old `tms-skills` package is no longer updated, and its `^2` (2.0.0–2.1.1) is deprecated.

## Repo layout

```text
topmind-writing-skills/
├─ topmind-*/                    # eight skills (SKILL.md + references + scripts + examples)
├─ shared/                       # single source for shared scripts and writing rules (manifest.json lists targets)
├─ bin/topmind-writing-skills.js # CLI: list / install / uninstall
├─ evals/                        # routing eval cases (not shipped to npm)
├─ docs/                         # publishing guide · CI notes
├─ scripts/                      # repo gates, sync, privacy scan
└─ package.json · CHANGELOG.md · LICENSE
```

- Edit shared files only in `shared/`, then run `npm run sync:shared`; CI checks that every skill copy is byte-identical.
- SKILL.md frontmatter keeps only Agent Skills spec keys at the top level (`name` / `description` / `license` / `metadata`), so `skills-ref validate` passes.
- The npm package ships only `overview.png` from the cover examples; per-style samples are on GitHub and in the Release zip.

## Release & CI

| Action | GitHub | npm |
|---|:---:|:---:|
| push main | live | unchanged |
| tag `vX.Y.Z` | Release + zip | auto publish |

```bash
npm run check && npm run audit && npm run privacy
```

See [docs/PUBLISHING.md](./docs/PUBLISHING.md) · [docs/ci.md](./docs/ci.md).

## License

MIT © TopMindspace — [LICENSE](./LICENSE)
