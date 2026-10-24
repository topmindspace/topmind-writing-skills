# topmind-viral-posts · X duanzi

English | [中文](./README.md)

**One sentence per line, zero emoji, read in three seconds.** 12 topical patterns plus 2 relationship patterns, each with topics, hook, structure, ending, counter-examples and original samples. Decide who you want in the replies, then pick a pattern. The skill writes in Chinese by default.

- Version: **v0.3.20**

```bash
npx @topmindspace/topmind-writing-skills install topmind-viral-posts
```

Say: "来条段子", "不懂就问", "写个群聊体", "来条卧槽体", "蹭一下这个热点", "写条互关帖".

## 14 patterns

| Pattern | In one line | Typical opening | Replies you want |
|---|---|---|---|
| A1 Genuine question | Play dumb, ask what you really don't know | "Doesn't anyone use…?" | Experts explaining |
| A2 Leak check | Clue + last time + a guess | "XX is about to ship?!" | More clues, guesses |
| A3 Outage check | Ask "is it down?" right away | "Is XX down?" | "Me too" + jokes |
| A4 Whoa | Real reaction + a converted number | "Whoa, I did the math" | Shock, reposts |
| A5 TIL | "I only just learned…" | "TIL…" | "Me neither" |
| A6 Group chat | One line per company, "xx:" | "Today in the XX group:" | Riffs, one more company |
| A7 Series | Same protagonist, Day N | Column name + Day N | Bets, advice |
| A8 Do the math | Your own numbers in money and time | "One XX ate N% of my quota" | Their own bills |
| A9 Light take | Grant one side, add an insider take | "True, but…" | Taking sides |
| A10 Absurd self-roast | A shared pain as an absurd scene | "I thought … was the limit" | Relating, stories |
| A11 Product twist | Real product + scene + action twist | A daily-life scene | Riffs |
| A12 Trend remix | A familiar meme on new news | "The X edition of…" | Riffs, sides |
| B1 Relationship | Follow-backs, newcomers, check-ins, milestones | Real progress | Follows, hellos |
| B2 Mutual help | Asking for or giving invite codes | A real need | Codes |

Full breakdown in [references/patterns.md](./references/patterns.md), including a mapping from the old type list.

## Examples (original, in Chinese)

**A4 Whoa**

```text
卧槽，算完我人傻了

某公司一个新机房要放 20 万张卡

按一张卡一台电脑算，差不多是一个小县城每家一台

我这边还在为一个月 20 块的订阅犹豫...
```

**A11 Product twist**

```text
让某编辑器的 agent 帮我整理仓库

它扫了一遍

说有个文件三个月没人动过

建议删掉

我点了确认

然后它自己的配置文件就没了
```

More in [`examples/`](./examples/).

## Key practices

- **Duanzi layout**: one sentence per line, a blank line between lines, no emoji, no bullet symbols.
- **Endings**: "..." for a pause, a question the author genuinely can't answer, or an action twist; no boilerplate "what do you think?" bait. Delete-the-tail test: if the post is better without the last half-line, cut it.
- **Hashtags**: none by default on topical posts, at most 2; relationship and mutual-help posts take 1–3. Internal tags (type, replies wanted, platform, tone) go in the delivery notes.
- **Images by pattern**: most patterns are text-only; leak, outage and math posts take one screenshot when it is the evidence; relationship posts use your own profile or dashboard. No original image → ask first, then `topmind-cover`.
- **Posts with facts**: verify sources first; links and images are delivered separately, no verification notes in the body.
- **Replies and quote posts**: pick up the other person's point, then add one thing of your own; two versions in different tones.

## Checks

```bash
python3 scripts/lint_x_post.py duanzi.txt --duanzi   # emoji in a duanzi → W13
python3 scripts/lint_x_post.py ops.txt --kind ops     # relationship / mutual-help posts
```

E errors must be zero; each W warning needs a decision; H hints are for judgment only.

## When not to use

News, rankings and launches → `topmind-briefs`; X long-form → `topmind-x-article`; layout only → `topmind-format`; posting → `topmind-x` (with your confirmation).

All samples are self-written with fictional names and numbers; no third-party text is included.
