# topmind-wechat-post

English | [中文](./README.md)

Write, structure, and format WeChat Official Account articles from a topic or draft. Supports tool/plugin recommendation structures, hands-on product reviews, technical deep dives, and narrative essays, exporting WeChat-compatible inline HTML, mobile previews, and image upload lists. Chinese is the default language; see [SKILL.md](./SKILL.md) for the full workflow.

## Key Capabilities

- **Genre-Fit Article Structures**:
  - **Tool / Plugin Recommendations**: Name the tool in the title, front-load the pain point and install command, list core capabilities, and pair subheadings with concise examples and real screenshots.
  - **Hands-on Product & Model Reviews**: Preserve the author's specific evaluation dimensions and honest pros/cons without flattening into generic neutrality.
  - **Technical & Mechanism Deep Dives**: Separate source-code/experimental parameters from live production behavior while keeping a warm peer voice.
- **Evidence-First Visuals**: Visually separate objective evidence from author recommendations; highlight real source screenshots with surrounding context rather than fabricating fake pages; label conceptual covers honestly (`功能示意，不是实拍`).
- **WeChat Inline HTML Engine**: Ships with 6 curated themes (`md3-business-blue`, `minimal-ink`, `tech-blue`, `amber-review`, `graphite`, `newsprint`), base64 image embedding, and ProseMirror compatibility checks.

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-wechat-post
```

See [examples/README.md](./examples/README.md) for sample articles and [platform-cover-specs.md](./references/platform-cover-specs.md) for WeChat cover dimensions (`900×383` and `900×900`).

## Tools

```bash
python3 scripts/md2wechat.py --input 文章.md --embed-images --preview
python3 scripts/check_article.py <文章目录>
```

This skill generates drafts and publishing packages only and does not publish externally. MIT License. See the [collection](https://github.com/topmindspace/topmind-writing-skills).
