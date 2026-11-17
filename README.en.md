# topmind-writing-skills

English | [中文](./README.md)

[![Release](https://img.shields.io/github/v/release/topmindspace/topmind-writing-skills?style=flat-square&color=blue)](https://github.com/topmindspace/topmind-writing-skills/releases)
[![npm](https://img.shields.io/npm/v/@topmindspace/topmind-writing-skills?style=flat-square)](https://www.npmjs.com/package/@topmindspace/topmind-writing-skills)
[![CI](https://img.shields.io/github/actions/workflow/status/topmindspace/topmind-writing-skills/ci.yml?style=flat-square&label=CI)](https://github.com/topmindspace/topmind-writing-skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

**Social-media writing that sounds like a person wrote it.** Punchy one-liners, quick news posts, long-form articles, formatting, revision, covers and long images: eight skills for your AI assistant (Claude Code, Cursor, Codex…). Say "write a duanzi", "post a quick news brief" or "revise this" and it gets to work. The skills write in Chinese by default.

<p align="center">
  <img src="docs/assets/writing-cover.png" alt="topmind-writing-skills" width="960" />
</p>

```bash
npx @topmindspace/topmind-writing-skills install all      # first-time setup
npx @topmindspace/topmind-writing-skills@latest update    # later, update installed skills
```

Then tell your AI assistant "revise this", "write a quick brief", or "make a cover for this article". To install just one skill, use `install topmind-revise` or another ID from `list`. Desktop and Obsidian already include a reviewed writing snapshot; update it through each app's About & Updates screen rather than these npx commands.

Hosts start with the active note and allow explicit source changes. Drafts, a small read-only memory window and the selected skill are loaded in layers; other resources are retrieved as needed. Compaction does not reset completed work or budgets.

## Desktop and Obsidian integration

A reviewed release snapshot of [topmind-writing-skills](https://github.com/topmindspace/topmind-writing-skills) is bundled by default: revision, formatting, briefs, social posts, WeChat, X Articles, covers and posters. The writing repository keeps its own release cadence and version.

Open a Markdown document and choose **Writing & delivery** from the article toolbar or Apps/status/commands in Desktop, or the ribbon, workbench and note/editor menus in Obsidian. Selecting an action shows task setup; AI starts explicitly. Edit the source in the main editor, choose a delivery format and theme, then preview, copy or export beside it in `out/`. Existing article folders and WeChat drafts work in place.

Formatting preserves the draft’s wording, order and expressive marks. Review gives actionable feedback, and edits follow the author’s requested scope. When the user wants a copy-ready draft, deliver it separately from checks and publishing steps. Hosts load only the references they need for the task.

Built-in HTML/text typography requires no Python. Preview and copy use the same output; changed sources or images require regeneration. Diagnostics identify missing images, diagram source, extended containers and table paste limitations. AI images, PNG rendering and publishing require their respective tools. Copying does not publish; wording scores do not decide editorial quality.

The host pack also renders from source bytes, extracts local text from clipboard HTML, and evaluates a length rule set. The length entry accepts only caller-supplied JSON. This package does not ship or enable production platform rules. Fields, dates and reports are in [the length rule-set contract](docs/length-ruleset-v1.md). A Unicode code-point ceiling is not X weighted length and is not the target editor's final check. JavaScript and Python renderer differences are in [the capability matrix](docs/renderer-capability-matrix.md).

About & updates tracks the application, core skills, independent writing pack and integrations separately. Writing resources can update independently; compiled renderer code follows the host release. Managed packs are isolated, local modifications block replacement and failed installs preserve the previous version. Supported Desktop installs can download an update and explicitly restart; manual downloads remain available when signing or the installation channel prevents automatic updates.

## More choices, concrete references

- Read actual references and visible specimens, then adapt their methods to the current material.
- Explore a few distinct directions when useful; deliver one finished result for a clear one-result request.
- Treat voice, length, emoji, openings and visual style as choices. Current user intent and author samples guide them.
- Preserve necessary attribution, approximation and uncertainty in public copy. Facts, privacy, authorization and usable output remain concrete boundaries.
- Linters offer context-sensitive signals, not a style score to maximize. Writing quality still needs real author or reader evaluation.

See the [practice and specimens](./shared/references/creative-practice.md) and [audit](./docs/creative-skills-audit.md).

## What it writes

| Category | Skill | What it does | Say |
|---|---|---|---|
| Duanzi | [`topmind-viral-posts`](./topmind-viral-posts/) | X tech humor, contrast observations, genuine questions & sharp replies; 12 creative angles | "来条段子", "不懂就问", "写个群聊体" |
| Briefs | [`topmind-briefs`](./topmind-briefs/) | High-signal briefs: prompt tips, news rewrites, launches, deals, rankings, papers, hands-on | "发个快讯", "来篇短的", "写条技巧帖" |
| Long-form · X | [`topmind-x-article`](./topmind-x-article/) | X Article: single-source Markdown → one-click copy HTML + preview image | "写 X 长文", "出一键复制版" |
| Long-form · WeChat | [`topmind-wechat-post`](./topmind-wechat-post/) | WeChat articles: three quality gates, inline-image layout, publish checklist | "写公众号", "公众号排版" |
| Formatting | [`topmind-format`](./topmind-format/) | Re-layout without changing a word; stitch alternative openings into full posts | "转段子", "排一下版" |
| Revision | [`topmind-revise`](./topmind-revise/) | Structure → facts → logic → de-AI → fidelity audit; quick review for replies | "改稿", "去 AI 味", "看看这条回复" |
| Covers | [`topmind-cover`](./topmind-cover/) | Xiaohongshu, Douyin, WeChat and X covers, including video thumbnails and paired crops | "做个封面" |
| Long images | [`topmind-poster`](./topmind-poster/) | HTML → hi-res long image / poster / infographic with exact text and numbers | "出张长图" |

## Creative directions and on-demand knowledge

See the [implementation and verification record](./docs/creative-system.md).

All eight skills share scoped directions, complete examples and exceptions. Facts, formatting and tool contracts remain intact; typography, scenes, length and rhetoric are choices guided by the task.

A 45-card knowledge pack (covering the 8 de-AI mechanisms, peer stance & sensory translation, value-first takeaways & negative boundaries, news-to-post rewrites, play-dumb question patterns, learning from author edits, plugin/review structures, and visual evidence partitioning) ships with every standalone skill. Search summaries, then read selected cards, or easily add new strategy cards via `scripts/knowledge.py add`. See [knowledge packs](./docs/knowledge-packs.md).

```bash
npm run knowledge:search -- "typography scene editorial" --skill topmind-cover --limit 3
npm run knowledge:check
```

Cover resources include 22 adaptable style entries, 16 composition relationships, 24 combinations and 12 complete prompts. The [visual atlas](./topmind-cover/assets/examples/creative-atlas.html) offers eight actual layout studies with landscape / portrait switching. These resources support exploration without promising engagement or defining the full creative space.

## Covers across platforms

The [platform cover reference](./shared/references/platform-cover-specs.md) provides a practical size and safe-zone lookup across platforms: WeChat article wide covers (`900×383`, 2.35:1) and square share cards (`900×900`, 1:1) cropped independently from the source, Xiaohongshu & WeChat image-notes at `1080×1440` (3:4), X Article headers at `1500×600` (5:2), and X single-image posts at `1200×675` (16:9).

In `topmind-cover`, `landscape-pair` exports a centered 4:3 cover (`1080×810`) and full 16:9 master (`1920×1080`), while `vertical-pair` exports a centered 3:4 cover (`1080×1440`) and full 9:16 vertical master (`1080×1920`). Cover prompts support both native text-rendering models and negative-space + deterministic script overlay (`title-engine.py`), with honest `功能示意，不是实拍` labeling for conceptual UI illustrations.

## Duanzi & Conversational Posts: 12 Creative Angles

Decide **what makes readers pause and reply**, then pick an angle:

| Angle | What it is | Typical opening | Replies you want |
|---|---|---|---|
| A1 Genuine question | Peer stance + real pain point + 70% whitespace | "Folks using XX, do you all…?" | Peers sharing their setup |
| A2 Leak check | Clue + last time + a guess | "XX is about to ship?!" | More clues, guesses |
| A3 Outage check | Ask "is it down?" right away | "Is XX down?" | "Me too" + jokes |
| A4 Shock math | Pause at an anomaly + daily-life scale conversion | "Wait, is this per day???" | Shock, reposts |
| A5 TIL | "Just realized / wasted my quota" | "Just realized XX charges per…" | "Me neither" |
| A6 Group chat / Scene | One line per company or sharp action contrast | "Today in the XX group:" | Riffs, one more company |
| A7 Series | Same protagonist, Day N | Column name + Day N | Bets, advice |
| A8 Quota detective | Real numbers converted into cost and time | "Ran 30M tokens this morning…" | Their own bills |
| A9 Light take | Attitude-first framing + concrete updates | "Its real positioning is basically…" | Taking sides |
| A10 Absurd self-roast | Shared friction as an absurd action scene | "I thought … was the limit" | Relating, stories |
| A11 Product twist | Specific tool + task + literal-obedience twist | "Asked the coding agent to…" | Riffs |
| A12 Trend remix | A familiar meme on new news | "The Double-11 of models is here" | Riffs, sides |

Each angle has topics, mechanism, failure counter-examples, and samples in [patterns.md](./topmind-viral-posts/references/patterns.md).

## Briefs: 9 content types

| Type | Opening | Ending |
|---|---|---|
| News (first) | What + the single sharpest number, vs a rival readers know | "..." or none |
| News (late) | New angle: hands-on, math, verification | "..." |
| Preview / rumor | "Coming?!", verbs match the caliber | "?!" |
| Launch / tool | Genuine question or one sincere pick | "..." |
| Deal | What you can grab right now | none |
| Ranking / data | Who's first, by how much | none |
| Paper | One-line conclusion | none |
| Hands-on | The result (broke, fast, pricey) | Self-roast or a real question |
| One-line take | An insider's light judgment | The judgment |

These are optional directions, not fixed openings or endings. Keep preview and launch states distinct; add a fresh angle when useful. See [topmind-briefs](./topmind-briefs/SKILL.md).

## Examples

All samples are original; names and numbers are fictional. They are in Chinese, as the skills write.

**Duanzi · A6 group chat**

```text
今日模型群：

青鸟：新版本上线了，价格没动

Nova：我们也上线了，价格动了

小甲：你们上线前能不能先说一声

用户：我只想知道今天哪家不排队
```

**Brief · news (first)**

```text
某模型低调上线新版：编程评测 31 → 42，价格不变

网页、App、接口已全量切换，权重开源。

几项关键提升：

1）编程评测：31 → 42
2）推理评测：37 → 43
3）智能体评测：74 → 77，比某知名闭源模型高 3 分

单任务成本两毛钱出头...
```

Keep necessary vendor attribution and uncertainty in the copy. Detailed sources and charts can be listed separately; useful links may stay in the body.

**De-AI · before → after**

```text
重磅！某编辑器 3.0 发布，AI 编程迎来新纪元！

更新内容：
🔹 补全更快
🔹 支持本地模型
🔹 插件市场改版

这不仅是一次更新，更是开发方式的变革。
```

```text
某编辑器 3.0 发布，可以接本地模型了

更新内容：
· 补全更快
· 支持本地模型
· 插件市场改版
```

Removed the newsreader hype, the "not just X but Y" construction and the uplifting closer; the first line now carries the change readers care about.

More: [duanzi](./topmind-viral-posts/examples/) · [briefs](./topmind-briefs/examples/) · [format](./topmind-format/examples/) · [revise](./topmind-revise/examples/) · [X article](./topmind-x-article/examples/) · [WeChat](./topmind-wechat-post/examples/) · [poster](./topmind-poster/examples/) · [cover](./topmind-cover/assets/examples/)

## Long-form: choose a structure that fits

One folder per article, created by `article_scaffold.py`:

```text
<title>/
├─ <title>.md     the only source
├─ 骨架.md        message, reader, main thread and evidence (optional), per-section form and figures
├─ 素材来源.md    where every image and number came from (not published)
├─ images/  cover/  raw/自制图源/
└─ out/           X HTML, WeChat HTML, 预览.png (rebuildable)
```

- **Main thread**: claims and counterexamples for opinion, scenes for stories, tasks and steps for tutorials; no fixed number of judgments.
- **Diagrams**: originals and custom diagrams are options when they improve understanding; no figure quota.
- **Preview**: render `out/预览.png` before delivery; tables X can't paste can become images.

## Rules: principles first

All skills share layered rules (single source `shared/references/`, copied into each skill so it works standalone):

| Layer | File | Covers |
|---|---|---|
| Principles | `social-writing-principles.md` | Know the message, lead with it, new info every line, form follows content, originals first, reader's side |
| Information design | `information-design.md` | Skeleton first, content → form (list / table / figure / paragraph), length and density |
| Voice | `core-voice.md` | Contextual V01–V40 options for titles, openings, numbers, questions, replies and humor |
| Review | `de-ai-rules.md` + `topmind-revise` | De-AI patterns (long-form + social S01–S10), rewrite boundaries, fidelity audit |

The voice follows the current request, author samples, audience and genre; it is not one fixed persona.

### Scripts hint, people decide

Run these inside the skill folder (for example `topmind-briefs/` or `topmind-revise/`):

```bash
python3 scripts/lint_x_post.py X短文.txt --kind news   # news brief
python3 scripts/lint_x_post.py 段子.txt --duanzi        # duanzi
python3 scripts/de_ai_lint.py article.md --genre long  # long-form
```

| Level | Meaning | Required |
|---|---|---|
| E format issue | Likely marker leftovers and image placeholders; URL/source enforcement only with `--separate-links` | Check actual formatting and semantic exceptions |
| W editorial signal | Patterns, length, literal lists and inline links | Use context; valid choices need no written justification |
| H hint / I1–I9 | Context words, long first line, caliber notes in the body, newsreader template; information design (long runs, list candidates, material dumps…) | For judgment only, never in `--strict` |

If you have your own post data, `post_type_report.py` shows which openings, endings and types work for you and writes a habits summary for revision; the data stays on your machine.

## Combining skills

| Task | Combination |
|---|---|
| A news brief and a duanzi on the same event | `topmind-briefs` + `topmind-viral-posts`, same facts |
| Existing text, layout only | `topmind-format`; content changes go to `topmind-revise` |
| X long-form | `topmind-x-article` + `topmind-revise` + `topmind-cover` |
| WeChat long-form | `topmind-wechat-post` + `topmind-revise` + `topmind-cover` |
| Ranking long image | Copy from `topmind-briefs`, image from `topmind-poster` |

Every skill drafts only; you publish.

## Install

**npm = pinned snapshot; GitHub = latest.**

```bash
npx @topmindspace/topmind-writing-skills install all --to ./.claude/skills
npx @topmindspace/topmind-writing-skills status --to ./.claude/skills
npx @topmindspace/topmind-writing-skills@latest update --to ./.claude/skills
npx @topmindspace/topmind-writing-skills install topmind-briefs --to ./.claude/skills
npx @topmindspace/topmind-writing-skills install topmind-briefs --force --to ./.claude/skills
npx @topmindspace/topmind-writing-skills uninstall topmind-briefs --to ./.claude/skills
npx github:topmindspace/topmind-writing-skills update --to ./.claude/skills
```

- `install all` installs the full set once; `update` changes only already installed skills, and `status` compares the package snapshot with a destination. All accept `--to`.
- Without `--to`, the CLI selects a single existing TopMind installation, skills directory, or host configuration. If several match, it lists them and asks for `--to`. With no host configured, it uses `./.agents/skills` in the current project. Output always names the destination.
- Replacements are staged first; failures keep the old copy. Local edits to a managed skill stop automatic updates until `--force` is explicit, which retains the previous copy. Upgrading an older untracked installation also retains a backup. Symlinks and unrelated directories are never replaced.
- Equal versions are left alone; downgrading a newer installed version needs `--force`. Reopen the AI session after updating so the host discovers new skills.
- Skill ids are not npm packages; don't `npm install topmind-briefs`.

### Upgrade from a local checkout

Install local, unpublished changes from the checkout; `@latest` contains only the published npm snapshot. Verify the target first. If tools share skills through symlinks, update the resolved shared directory and preserve those links. For a standalone Codex installation, run from the repository root:

```bash
node bin/topmind-writing-skills.js status --to "$HOME/.codex/skills"
node bin/topmind-writing-skills.js update --to "$HOME/.codex/skills"
```

Use `install all` for the first install. Replace `--to` with the verified shared destination when appropriate. Unpublished changes with the same skill version require `install <id> --force --to <actual-dir>`. The CLI copies each skill's self-contained resources and never writes to a destination's root `shared/` directory.

<details>
<summary>Repository layout and releases</summary>

```text
topmind-writing-skills/
├─ topmind-*/                    # eight skills (SKILL.md + references + scripts + examples)
├─ shared/                       # single source for shared scripts and rules (manifest.json)
├─ bin/topmind-writing-skills.js # CLI: list / install / uninstall
├─ evals/                        # routing evals (not in the npm package)
├─ docs/                         # publishing · CI
└─ scripts/                      # repo gates, sync, privacy scan
```

- Edit shared files only in `shared/`, then `npm run sync:shared`; CI checks byte-equal copies.
- SKILL.md frontmatter uses Agent Skills spec fields only and passes `skills-ref validate`.
- Pushing main is visible on GitHub immediately; a `vX.Y.Z` tag creates a Release and publishes to npm. Each skill's version lives in its own `SKILL.md` and the [CHANGELOG](./CHANGELOG.md).
- See [docs/PUBLISHING.md](./docs/PUBLISHING.md) · [docs/ci.md](./docs/ci.md).

For business presentations, install [`topmind-presentation`](https://github.com/topmindspace/topmind-presentation) separately.

</details>

## License

MIT © TopMindspace — [LICENSE](./LICENSE)
