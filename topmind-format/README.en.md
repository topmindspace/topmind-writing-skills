# topmind-format

English | [中文](./README.md)

Format existing text for X without rewriting its facts, wording or order. Preserve links and expressive symbols by default; separate links or strip emoji only when explicitly requested. Chinese is the default language; current user instructions and author samples take priority. See [SKILL.md](./SKILL.md) for the capability, workflow and tools.

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-format
```

A scoped knowledge pack ships with this skill. See [retrieval and contribution](./references/knowledge-library.md) and the [card directory](./knowledge/README.md). Read relevant summaries before selected cards; capture new local notes as candidates, without rewriting global preferences.

## How it works

Use the [practice reference](./references/creative-practice.md) to understand rhythm and expressive symbols. Adjust line breaks, spacing and permitted presentation symbols while preserving wording, facts and order. Use topmind-revise for rewriting.

## Tools

Run from this skill directory, using actual input paths:

```bash
python3 scripts/format_text.py 原文.txt --mode duanzi --out 排版稿.txt
```

Preserve links and expressive symbols. Use --separate-links or --strip-emoji only when requested. Check wording, facts and order after formatting.

Deliver the requested text or artifacts; these skills do not publish externally. MIT License. See the [collection](https://github.com/topmindspace/topmind-writing-skills) for installation options and maintenance.
