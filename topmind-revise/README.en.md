# topmind-revise

English | [中文](./README.md)

Review or revise existing writing at the requested depth, from a short reply to a structural rewrite. Preserve author intent and verify factual changes; full reports are optional for tasks that need them. Chinese is the default language; current user instructions and author samples take priority. See [SKILL.md](./SKILL.md) for the capability, workflow and tools.

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-revise
```

A scoped knowledge pack ships with this skill. See [retrieval and contribution](./references/knowledge-library.md) and the [card directory](./knowledge/README.md). Read relevant summaries before selected cards; capture new local notes as candidates, without rewriting global preferences.

## How it works

Read actual references and relevant [specimens](./references/creative-practice.md). Explore distinct directions when that helps the task; deliver one complete result when the request is clear. Voice, length, emoji, structure and visual styles are choices rather than universal gates. Facts, attribution, privacy, authorization and usable output still matter.

## Tools

Run from this skill directory, using actual input paths:

```bash
python3 scripts/revise_check.py 改前.md 改后.md --report 改稿报告.md
```

Compare drafts for numbers, entities, quotations and certainty. Phrase diagnostics help locate possible issues; they do not determine authorship or replace editorial judgment.

Deliver the requested text or artifacts; these skills do not publish externally. MIT License. See the [collection](https://github.com/topmindspace/topmind-writing-skills) for installation options and maintenance.
