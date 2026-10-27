# topmind-wechat-post

English | [中文](./README.md)

Write or prepare WeChat articles from a topic or existing draft. Export inline HTML, previews and image-upload lists when requested; formatting-only tasks preserve the draft. Chinese is the default language; current user instructions and author samples take priority. See [SKILL.md](./SKILL.md) for the capability, workflow and tools.

For covers, image-post formats and cross-platform crops, read the [platform reference](./references/platform-cover-specs.md) as needed. Export presets are not mandatory upload specifications; verify actual platform previews.

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-wechat-post
```

A scoped knowledge pack ships with this skill. See [retrieval and contribution](./references/knowledge-library.md) and the [card directory](./knowledge/README.md). Read relevant summaries before selected cards; capture new local notes as candidates, without rewriting global preferences.

## How it works

Read actual references and relevant [specimens](./references/creative-practice.md). Explore distinct directions when that helps the task; deliver one complete result when the request is clear. Voice, length, emoji, structure and visual styles are choices rather than universal gates. Facts, attribution, privacy, authorization and usable output still matter.

## Tools

Run from this skill directory, using actual input paths:

```bash
python3 scripts/md2wechat.py --input 文章.md --embed-images --preview
```

For HTML export, check inline styles, image lists and image order. Previews need a browser and its dependencies; inspect the editor again after upload.

Deliver the requested text or artifacts; these skills do not publish externally. MIT License. See the [collection](https://github.com/topmindspace/topmind-writing-skills) for installation options and maintenance.
