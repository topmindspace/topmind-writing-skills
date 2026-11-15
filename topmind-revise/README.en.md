# topmind-revise

English | [中文](./README.md)

Review, polish, condense, or rewrite existing drafts using the core diagnostic switch: **"Is this sentence completing a writing assignment, or talking to a friend?"** Strip AI task-speak and PR bloat while strictly preserving factual accuracy, author voice, and honest evaluation. Chinese is the default language; see [SKILL.md](./SKILL.md) for the full workflow.

## Key Capabilities

- **8 De-AI Mechanisms**: Eliminate over-explaining, meta-discourse filler, press-release intros, preachy endings, forced parallelism, lecturer tone, and spec-sheet dumping.
- **Voice & Honesty Preservation**: Temper unsupported absolute claims without washing out the author's personal warmth or honest product critiques. Never fabricate first-person ("I") experiences.
- **Learn from Author Edits**: Compare before/after revisions (`learn` mode), extract what bloat was cut and what anchor was added, tag the applicable scope, and extend the knowledge pack (`revise-learn-from-edits`, `de-ai-mechanisms`).
- **Factual & Provenance Verification**: Verify numbers, quotes, entities, and paragraph provenance with `revise_check.py` and `audit-provenance.py`.

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-revise
```

See [examples/README.md](./examples/README.md) for long-form and short-post revision comparisons, and [knowledge/README.md](./knowledge/README.md) for the bundled knowledge cards.

## Tools

```bash
python3 scripts/de_ai_lint.py 稿子.md
python3 scripts/revise_check.py 改前.md 改后.md --report 改稿报告.md
python3 scripts/audit-provenance.py --draft 改后.md --source 源稿.md
```

Diagnostic hints are non-blocking editorial aids. This skill does not publish externally. MIT License. See the [collection](https://github.com/topmindspace/topmind-writing-skills).
