# topmind-viral-posts

English | [中文](./README.md)

Write conversational X posts, humor, replies, commentary and relationship updates. Use observations, questions, reversals or dialogue; author-requested emoji and rhythm are supported. Chinese is the default language; current user instructions and author samples take priority. See [SKILL.md](./SKILL.md) for the capability, workflow and tools.

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-viral-posts
```

## How it works

Read actual references and relevant [specimens](./references/creative-practice.md). Explore distinct directions when that helps the task; deliver one complete result when the request is clear. Voice, length, emoji, structure and visual styles are choices rather than universal gates. Facts, attribution, privacy, authorization and usable output still matter.

## Tools

Run from this skill directory, using actual input paths:

```bash
python3 scripts/lint_x_post.py 稿子.txt --duanzi
```

Style diagnostics are contextual suggestions, not a quality score. Platform conversion and directory requirements apply when using the corresponding tools. Check actual previews and disclose unverified steps.

Formatting preserves links and emoji by default. In skills that include `format_text.py`, `--separate-links` and `--strip-emoji` are explicit optional conversions. X lint only enforces link separation when `--separate-links` is requested.

Deliver the requested text or artifacts; these skills do not publish externally. MIT License. See the [collection](https://github.com/topmindspace/topmind-writing-skills) for installation options and maintenance.
