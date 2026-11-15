# topmind-format

English | [中文](./README.md)

Format existing text into clean, readable X plain text with **100% wording, fact, link, and expressive punctuation fidelity**. Adjust paragraph spacing, list symbols, and conversational pacing while stripping unintended Markdown syntax residue. Chinese is the default language; see [SKILL.md](./SKILL.md) for details.

## Key Capabilities

- **Zero-Rewrite Fidelity**: Never alter the author's wording, facts, order, or links. For rewriting or de-AI polishing, use `topmind-revise`.
- **Three Formatting Modes**:
  - **Short Post (`short`)**: Group sentences by semantic paragraph with clean `1）2）` or `·` lists.
  - **Punchy / Humor (`duanzi`)**: Break lines by spoken rhythm so the setup and punchline land cleanly.
  - **Lead Variants (`--variants`)**: Combine multiple author-written opening hooks with the body into complete copyable drafts.
- **Expressive Punctuation Preserved**: Keep `？？？`, `！！！`, `！！？`, `……`, `✅ / ❌`, and emoji intact by default.

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-format
```

See [examples/README.md](./examples/README.md) for side-by-side formatting examples and [knowledge/README.md](./knowledge/README.md) for formatting cards (`format-fidelity`, `format-layouts`).

## Tools

```bash
python3 scripts/format_text.py 原文.txt --mode short --out 短文.txt
python3 scripts/format_text.py 原文.txt --mode duanzi --split --out 段子.txt
```

Use `--separate-links` or `--strip-emoji` only when explicitly requested. This skill does not publish externally. MIT License. See the [collection](https://github.com/topmindspace/topmind-writing-skills).
