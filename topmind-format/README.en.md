# topmind-format · X Plain-Text Formatter

**[中文](./README.md)** | English

Lays out existing text for X: **duanzi mode** (one sentence per line, a blank line between every line) or **short-post mode** (paragraphing, emoji bullets, a keyword-matched title emoji, and the account's chicken/cat/plant motif at the start or end). Layout only — the words are never changed; a fidelity check enforces it.

- Version: **v0.1.0** (ships with `@topmindspace/topmind-writing-skills@0.8.32`)

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-format
```

## Usage

```bash
python3 scripts/format_text.py input.txt --mode duanzi --split --open 🐱 --close 🌱
python3 scripts/format_text.py input.txt --mode short --title-emoji 🆕 --open 🐔
python3 scripts/lint_x_post.py output.txt
```

Emoji rules: [references/emoji-system.md](./references/emoji-system.md) (shared with topmind-briefs and topmind-viral-posts). X layout rules: [references/x-post-format.md](./references/x-post-format.md).

## Scope

Writing jokes from scratch → `topmind-viral-posts`; writing briefs → `topmind-briefs`; X long-form → `topmind-x-article`; WeChat layout → `topmind-wechat-post`; posting → `topmind-x` (needs user confirmation).

## Development

```bash
python3 scripts/audit_skill.py
python3 scripts/package_skill.py --check
python3 scripts/negative_tests.py
```
