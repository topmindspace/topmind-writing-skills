# topmind-poster

English | [中文](./README.md)

Build high-signal one-pager summary cards, benchmark rankings, architecture diagrams, and multi-page long images using editable HTML/CSS, and render crisp high-resolution PNGs. Chinese is the default language; see [SKILL.md](./SKILL.md) for the full workflow.

## Key Capabilities

- **Three Things in One Image**: Present the **key change (numbers/comparison), factual boundary (conditions/when not to use), and concrete recommendation** in a single scannable visual.
- **Visual Separation of Evidence vs. Advice**: Place objective evidence (source parameters, paper tables, benchmark data) and subjective author recommendations in visually distinct zones.
- **Balanced Density & Honest Citations**:
  - Maintain mobile-readable typography (`>= 22px` body text) without overcrowded disclaimers or empty pseudo-minimalism.
  - Embed real source screenshots with highlighted lines rather than fabricating fake paper/official pages in HTML; label conceptual demos honestly (`功能示意，不是实拍`).

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-poster
```

See [layout-recipes.md](./references/layout-recipes.md) for proven CSS tokens and grid recipes, and [examples/README.md](./examples/README.md) for a ready-to-render HTML/CSS benchmark poster.

## Tools

```bash
python3 scripts/render_poster.py poster.html -o poster.png
```

Inspect the rendered PNG for typography, cropping, and data accuracy. This skill outputs images and HTML sources only and does not publish externally. MIT License. See the [collection](https://github.com/topmindspace/topmind-writing-skills).
