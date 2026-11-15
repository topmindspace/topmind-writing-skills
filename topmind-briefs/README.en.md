# topmind-briefs

English | [中文](./README.md)

Write high-signal short posts for X and WeChat (typically 300–800 Chinese characters): actionable tips, prompt deliveries, release briefs, benchmarks, paper takeaways, and hands-on opinions. Chinese is the default language; current user instructions and author samples take priority. See [SKILL.md](./SKILL.md) for the full workflow.

## Key Capabilities

- **Angle by Post Type**:
  - **Tips & Prompt Delivery**: Lead with the concrete result or contrast number, include the copyable command/prompt, and state clear negative boundaries ("when NOT to use").
  - **Product & Industry News**: Strip PR filler and purchase disclaimers; translate technical specs into everyday sensory scale.
  - **Security & Breaking Events**: Open with the reader's immediate question, clarify the exact blast radius in one sentence, and list actionable steps with compact `1）2）` numbering.
- **Peer Stance & Honest Attribution**: Write like a knowledgeable colleague rather than a lecturer. Never fabricate first-person experience; keep verification logs outside the copyable text block.
- **Extensible Knowledge Pack**: Includes cards like `brief-value-first`, `brief-news-to-post`, `voice-peer-stance`, and `de-ai-mechanisms` (see [knowledge/README.md](./knowledge/README.md) and [references/knowledge-library.md](./references/knowledge-library.md)).

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-briefs
```

See [examples/README.md](./examples/README.md) and [references/examples.md](./references/examples.md) for before/after examples, and [platform-cover-specs.md](./references/platform-cover-specs.md) for cross-platform cover dimensions.

## Tools

```bash
python3 scripts/lint_x_post.py X短文.txt --kind news
python3 scripts/de_ai_lint.py 公众号短文.md
```

Lint checks formatting residue and offers non-blocking contextual hints. This skill drafts content only and does not publish externally. MIT License. See the [collection](https://github.com/topmindspace/topmind-writing-skills).
