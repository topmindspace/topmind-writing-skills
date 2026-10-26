# topmind-format

English | [中文](./README.md)

Format existing text for X without rewriting its facts, wording or order. Preserve links and expressive symbols by default; separate links or strip emoji only when explicitly requested. Chinese is the default language; current user instructions and author samples take priority. See [SKILL.md](./SKILL.md) for the capability, workflow and tools.

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-format
```

## How it works

Read actual references and relevant [specimens](./references/creative-practice.md). Explore distinct directions when that helps the task; deliver one complete result when the request is clear. Voice, length, emoji, structure and visual styles are choices rather than universal gates. Facts, attribution, privacy, authorization and usable output still matter.

## Tools

Run from this skill directory, using actual input paths:

```bash
python3 scripts/format_text.py 原文.txt --mode duanzi --out 排版稿.txt
```

Style diagnostics are contextual suggestions, not a quality score. Platform conversion and directory requirements apply when using the corresponding tools. Check actual previews and disclose unverified steps.

Formatting preserves links and emoji by default. In skills that include `format_text.py`, `--separate-links` and `--strip-emoji` are explicit optional conversions. X lint only enforces link separation when `--separate-links` is requested.

Deliver the requested text or artifacts; these skills do not publish externally. MIT License. See the [collection](https://github.com/topmindspace/topmind-writing-skills) for installation options and maintenance.
