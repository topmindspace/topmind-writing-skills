# topmind-format · X Plain-Text Formatter

**[中文](./README.md)** | English

Lays out existing text for X: **duanzi mode** (one sentence per line, a blank line between every line, no emoji at all, bullets without symbols) or **short-post mode** (paragraphing; lists become 「·」/「1）」 or, optionally, emoji bullets; title emoji and motifs are optional). Layout only — the words are never changed; a fidelity check enforces it. Links, source lines and image notes are pulled out of the body so it stays one copy-ready plain-text block; links and images are sent separately.

- Version: **v0.1.6** (ships with `@topmindspace/topmind-writing-skills@0.8.41`)

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-format
```

## Usage

```bash
python3 scripts/format_text.py input.txt --mode duanzi --split   # duanzi rejects --open / --close / --title-emoji
python3 scripts/format_text.py input.txt --mode short --links-out links.txt   # links / source lines saved to send separately
python3 scripts/format_text.py input.txt --mode short --bullets emoji --title-emoji 🆕   # emoji optional
python3 scripts/lint_x_post.py output.txt
```

Emoji rules (short posts only): [references/emoji-system.md](./references/emoji-system.md). X layout rules: [references/x-post-format.md](./references/x-post-format.md).

## Scope

Writing jokes from scratch → `topmind-viral-posts`; writing briefs → `topmind-briefs`; X long-form → `topmind-x-article`; WeChat layout → `topmind-wechat-post`; posting → `topmind-x` (needs user confirmation).

## Development

```bash
python3 scripts/audit_skill.py
python3 scripts/package_skill.py --check
python3 scripts/negative_tests.py
```

## Original examples

Sample outputs written by us (fictional or neutral topics, no third-party text) are in [`examples/`](./examples/).
