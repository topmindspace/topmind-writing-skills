# topmind-x-article

English | [中文](./README.md)

Write, structure, and export X Articles (long-form posts on X). Supports thesis-driven deep dives, tool/plugin walkthroughs, hands-on benchmarks, and cross-platform adaptation, exporting single-file copyable HTML, plain-text fallback, and publishing checklists. Chinese is the default language; see [SKILL.md](./SKILL.md) for the full workflow.

## Key Capabilities

- **Clear Long-Form Progression**:
  - **Argument & Mechanism Deep Dives (`x-argument`, `x-evidence`)**: Lead with the core thesis or contrast and advance section by section with concrete evidence.
  - **Tool Walkthroughs & Reviews (`wechat-plugin-and-review`)**: Keep full commands, links, and honest pros/cons inside the Article while adapting companion promo posts to short-post norms (`x-adapt`).
- **Single-Source Image Order & Dual-Channel Code Copy**:
  - `md2x-html.py` reads `![]()` in exact document order and generates `[图N]` placeholders so images never shift.
  - Provides one-click rich-text copy plus per-block prompt copy buttons for inserting native X Code blocks.

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-x-article
```

See [examples/README.md](./examples/README.md) for a complete sample X Article and [platform-cover-specs.md](./references/platform-cover-specs.md) for the `1500×600` (`5:2`) X Article banner spec.

## Tools

```bash
python3 scripts/md2x-html.py 文章.md --preview
python3 scripts/md2x.py 文章.md
python3 scripts/check_article.py <文章目录>
```

This skill generates drafts and export packages only and does not publish externally. MIT License. See the [collection](https://github.com/topmindspace/topmind-writing-skills).
