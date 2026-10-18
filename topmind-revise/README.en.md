# topmind-revise · Revision and quality check

English | [中文](./README.md)

Makes a draft shorter, more accurate and closer to the author's own voice, and proves the facts survived the edit. Works for long-form articles, short posts, one-liners, replies and titles. Use it on its own, or let `topmind-wechat-post` and `topmind-x-article` call it by default when they write long-form pieces.

- Version: **v0.1.0** (ships with `@topmindspace/topmind-writing-skills@0.8.44`)

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-revise
```

## Modes

| Mode | What it does |
|---|---|
| audit | Runs the checks and writes a revision report; the draft is untouched |
| revise | Backs up first, edits, writes back, and attaches the report |
| embed | Called by the long-form skills; returns the final draft plus a three-line summary |
| quick | Titles, short posts, replies and summaries: one rewrite, at most two alternatives |

Pipeline: facts → logic → cut redundancy → de-AI → voice check → layout → fidelity check → over-edit check.

```bash
python3 scripts/de_ai_lint.py draft.md                    # W warnings + H hints
python3 scripts/count_words.py before.md after.md
python3 scripts/revise_check.py before.md after.md --report report.md
```

## Rule layers

- `references/core-voice.md`: scenario rules (titles, openings, endings, numbers, quotes, source lines, lists, emoji).
- `references/de-ai-rules.md`: rewrite boundaries plus structural patterns; the linter reports W (warnings, each needs a decision) and H (hints only).
- `references/revision-workflow.md`: the full checklist this skill executes.

## Guarding against over-editing

Every change must map to a rule code or an author note; paragraphs with no hits stay as they are; `revise_check.py` flags the run when more than 30% of clean paragraphs were rewritten.

## Not for

Writing from scratch (use the writing skills), layout-only formatting (`topmind-format`), covers and images (`topmind-cover` / `topmind-poster`), or publishing.
