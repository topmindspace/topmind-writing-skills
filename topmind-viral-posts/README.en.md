# topmind-viral-posts · X Viral Short Posts

**[中文](./README.md)** | English

Short, real, hooked — read in 3 seconds, impossible not to like/comment/follow. 14 post types summarised from common high-engagement writing patterns in the Chinese X community (all examples are original, written for this skill), each post paired with 1 image, a hashtag set and classification tags.

- Version: **v0.3.5** (ships with `@topmindspace/topmind-writing-skills@0.8.30`)

## Install

```bash
npx @topmindspace/topmind-writing-skills install topmind-viral-posts
```

## 14 Types

| Type | Hook | Image | Default tags (purpose · tone · hashtag) |
|---|---|---|---|
| Tips & advice | "Mistakes beginners make" | Slogan graphic / landscape | persona, growth · crisp · #新手指南 |
| Follow-for-follow | Direct ask + follow-back promise | Pet / portrait | follow-back · humble · #蓝V互关 #follow |
| Self-deprecating humor | Concrete numbers + contrast | Funny pet / fantasy | engagement, daily · self-mocking · #涨粉日记 |
| Interactive question | Either-or / soul question | Slogan graphic / landscape | engagement · curious · topic word |
| Daily check-in | Small wins + blessings | Landscape / pet | daily · warm · #日拱一卒 |
| Newcomer intro | Personification + ask for follows | Pet / portrait | follow-back, growth · humble · #新人报到 |
| Trending news | Real news + playful take | Official image / screenshot | news, traffic · restrained · event name |
| Hot take | Counter-intuitive claim | Slogan graphic | engagement, traffic · contrarian · #暴论 |
| Stats show-off | Concrete number + contrast/progress | Dashboard screenshot / chart | persona, growth · sincere · #数据复盘 |
| Sincere friending | "No follow-and-drop" trust signal | Lifestyle photo | follow-back · sincere · #真诚交友 |
| Relatable gripe | Platform pain point + self-mockery | Meme / pet | engagement, daily · self-mocking · #创作者日常 |
| Practical tip | Useful tip + why it works | Infographic | persona, traffic · crisp · #运营技巧 |
| Hard-won lesson | Beginner trap + vivid metaphor | Slogan graphic / landscape | persona · humble · #新手指南 |
| Execution checklist | Daily numbers + period | Checklist infographic | growth, persona · crisp · #执行清单 |

## Tags

Every post carries two kinds of tags:

- **Hashtags**: 1–3 per post, on the last line of the body; no synonym stacking, nothing that invites engagement farming or sensitive topics.
- **Classification tags**: type / purpose / platform / tone, listed in the "tags" item of the output, never in the post body.

See [references/tags-and-topics.md](./references/tags-and-topics.md) for the full vocabulary and rules.

## Plain-text formatting for X

X does not render Markdown, so X drafts never use `- ` lists, `#` headings or `**bold**`. Lists use emoji bullets (🔹 level one, ▫️ level two, 1️⃣ steps, ✅/❌ contrasts), at most two levels. When a WeChat draft is turned into an X draft, only the layout may change; the content stays the same. See [references/x-post-format.md](./references/x-post-format.md).

```bash
# Check an X draft: no Markdown list/heading/bold, hashtags on the last line; add --fix --out to rewrite
python3 scripts/lint_x_post.py x-draft.txt
```

## Images

Generated via `topmind-cover`, 5 image banks: portraits / pets (cats first) / landscapes / fantasy / slogan graphics. X single image 1200×675.

## Usage

See [SKILL.md](./SKILL.md) for workflow, [references/patterns.md](./references/patterns.md) for case breakdowns.
