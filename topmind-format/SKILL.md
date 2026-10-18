---
name: topmind-format
description: "X 纯文本格式化：用户贴一段现成文字，只改排版、不改字。转段子 → 每句一行、行与行之间空一行，完全不用 emoji（去掉点缀与列表符号，分点一条一行）；格式化成短文 → 合理分段换行、合理列表（「·」「1）」或 emoji，emoji 不强制，用就按 TopMind 体系）。保留原文事实与措辞，自带保真校验脚本；交付一段可直接复制的纯文本，原文里的链接（含来源）、原图、配图拿出来另发，不混进正文；没有原图时询问是否配图。只交付不代发。Use when 转段子、改成段子格式、段子格式、格式化、格式化一下、格式化成短文、排一下版、整理格式、加空行、分行、加 emoji、X 排版、format。Do NOT use for 从零写段子、涨粉帖（→ topmind-viral-posts）、从零写干货短文、快讯（→ topmind-briefs）、X 长文（→ topmind-x-article）、公众号排版与公众号 HTML（→ topmind-wechat-post）、封面（→ topmind-cover）、改写措辞、去 AI 味改稿与质检（→ topmind-revise）、把帖子发出去（→ topmind-x，须用户确认）。"
license: MIT
metadata:
  version: "0.1.11"
  action_category: "write"
  triggers: "转段子, 改成段子, 段子格式, 格式化, 格式化一下, 格式化成短文, 排一下版, 整理格式, 加空行, 分行, 加 emoji, X 排版, format"
  author: "TopMindSpace"
  homepage: "https://github.com/topmindspace/topmind-writing-skills#readme"
  updated: "2026-10-18"
---

# topmind-format · X 纯文本格式化

用户已经有文字，只想让它在 X 上好读。本技能**只动排版**：换行、空行、列表符号、emoji 点缀（emoji 只用于短文体）；
不改字、不增删事实、不调换顺序。要改写现成内容时，转给 `topmind-revise`；从零重写时转 `topmind-viral-posts`（段子）或 `topmind-briefs`（短文）。

## 先读：写作原则与信息设计

本技能建立在两份共享文件上，动笔前先读：

- [references/social-writing-principles.md](references/social-writing-principles.md)：8 条社交媒体写作原则（先想清楚、结论先行、每句都有新信息、形式跟内容走、简单清楚、原图优先、站在读者那边、真实有分寸）
- [references/information-design.md](references/information-design.md)：内容 → 形式决策表、篇幅和密度、去啰嗦的判断法
- 措辞和口吻在这两层之上，见 [references/core-voice.md](references/core-voice.md)

排版：按决策表提示哪里可以转列表或表格，不改字。

## 何时不用

- 从零写段子、涨粉帖、互关帖 → `topmind-viral-posts`
- 从零写干货短文、快讯、榜单速报 → `topmind-briefs`
- X 长文、发 X 文章 → `topmind-x-article`
- 公众号排版、公众号 HTML → `topmind-wechat-post`
- 要改写措辞、压缩字数、去 AI 味（不只是排版）→ `topmind-revise`；从零重写 → `topmind-viral-posts` / `topmind-briefs`
- 发帖 → `topmind-x`（须用户确认）

> **必读（交付格式是硬约束）**：[references/x-delivery-contract.md](references/x-delivery-contract.md)——**短文体**分点默认「·」，行多用「1）」，短列表才用 emoji，较长短文用【小标题】；**段子体完全不用 emoji**，分点不加符号、一条一行；两种都禁用 `- ` `1. `；格式化结果是一段可直接复制的纯文本，**不含 URL、来源行、配图说明**；链接一条、图片一条另发，改动说明最后另列。

## 两种模式

| 用户说 | 模式 | 做什么 |
|---|---|---|
| 转段子、段子格式、改成段子 | 段子体 `duanzi` | 每句一行，**行与行之间都空一行**；**完全不用 emoji**：去掉人设点缀、表情和列表符号，分点条目一条一行、行间空行 |
| 格式化、格式化成短文、排一下版 | 短文体 `short` | 合理分段（一段 1–3 行），Markdown 列表默认改「·」「1）」（短列表按需改 emoji）；标题 emoji 0–1、人设点缀 0–2 都是可选的 |

只说「格式化」又看不出体裁时：原文有列表、数据、来源 → 短文体；原文是口语短句、吐槽、互关 → 段子体。还拿不准就给两版让用户挑。

## 工作流

1. **读原文**：确认是用户自己的文字或用户给的文字；记下原文里的数字、话题标签、表情，后面逐一核对；原文里的 URL、来源行、配图说明挑出来，放进另发的链接 / 图片消息（这是挪位置，不算改字）。
2. **断句**（版式规律见 [references/x-layout-patterns.md](references/x-layout-patterns.md)）：
   - 段子体：一句一行。长句在逗号处断开时，只断在意思完整的地方（例：「X 创作者收益里，」/「付费蓝V用户的互动权重会高很多。」），不在词中间断。原文的分点（`- ` `1.` `🔹` 等）去掉符号，条目一条一行、行间空行；原文自带的 emoji 一并去掉（保真校验不计 emoji）。
   - 短文体：标题一行；正文一段 1–3 行；并列信息改成列表（列表前的「xx：」引导语单独一行；条目超过一行时条目之间空一行）；原文已有【小标题】的保留并单独成行；话题标签在最后一行；链接、来源行不留在正文里。
3. **emoji（只在短文体、而且可选）**：段子体一个都不加。短文体不加也可以；要加只用 TopMind 体系，唯一出处 [references/emoji-system.md](references/emoji-system.md)（本技能不另立规则）：
   - 人设点缀（🐔 🐱 为主角，🌱 🌿 🌸 等为配角）只放开头一行或结尾一行，同一帖最多 2 个；
   - 标题 emoji 必须对上标题关键词（发布 🆕、数据 📊、教程 🛠️ …），对不上就不放；
   - 列表符号一帖一套：默认纯文本「·」「1）」，短列表（3–4 条）才用 emoji 🔹 / 1️⃣ / ✅❌，规则见 [references/x-post-format.md](references/x-post-format.md)；
   - 短文体里原文自带的表情保留，不重复叠加；严肃内容（事故、争议、处罚）不加人设点缀。
4. **跑脚本**（可选但推荐）：

   ```bash
   python3 scripts/format_text.py 原文.txt --mode duanzi --split --out 段子.txt
   python3 scripts/format_text.py 原文.txt --mode short --links-out 链接.txt --out 短文.txt
   python3 scripts/format_text.py 原文.txt --mode short --bullets emoji --title-emoji 🆕 --out 短文.txt   # 选用 emoji 时
   python3 scripts/lint_x_post.py 短文.txt
   python3 scripts/lint_x_post.py 段子.txt --duanzi
   ```

   `format_text.py` 先把 URL、来源行、配图行拿出正文（打印到标准错误的「另发」清单，`--links-out` 另存），再做原文保真校验（去掉空白、列表符号与 emoji 后逐字比对），改动了字就报错；
   短文体把 Markdown 列表改成「·」「1）」（`--bullets emoji` 改 🔹 / 1️⃣）；段子体去掉所有 emoji 与列表符号（条目间空一行，`--split` 不拆列表条目），并拒绝 `--open` / `--close` / `--title-emoji`。
   `lint_x_post.py` 检查 Markdown 残留、符号混用、表情数量、正文里的 URL / 来源行 / 配图说明（E10–E12）、混入的说明（W12）、AI 套话（W9）、中英文结构套话（W15 / W16）、标点腔（W17）、「人名说：」/ 过渡句 / 复述图片（W19–W21）、段子里的 emoji（`--duanzi`，W13），另给 H 级提示（语境词、话题标签过多等）；段子体的单个行间空行不报错。
   **去 AI 味检查必跑，但本技能不改字**：W 警告的命中按 [references/de-ai-rules.md](references/de-ai-rules.md) 写进改动说明，交给用户决定；H 提示只是语境判断（场景规则见 [references/core-voice.md](references/core-voice.md)），不写进「建议改」。用户明确要求改写时，建议转 `topmind-revise`（只改表达，不改事实）。
   **可转列表 / 表格的地方只报告**：`python3 scripts/info_design_hints.py 原文.md` 给出 I3（并列项可转列表）、I4（对照可转表格）、I1（连续纯文字）等提示，判断方法见 [references/information-design.md](references/information-design.md)。短文体里原文已经是并列分点的照常转「·」「1）」；原文是一段话但内容像列表的，不替用户拆，在改动说明里写「第 N 段可以拆成列表」，由用户决定。
5. **交付**（按 [references/x-delivery-contract.md](references/x-delivery-contract.md)）：正文一条（格式化结果，一个独立 `text` 块）→ 链接一条（原文里拿出来的 URL / 来源行，没有就写「用户提供，未附来源」）→ 图片一条（用户给了就列 1–2 张，没有就写「未找到原图」并问要不要配图）→ 改动说明（排版改动、加了哪些 emoji、挪出了哪些链接、发现的疑似错字）。多条帖子每条一块。

## 边界（硬约束：不改字）

- **不改字**：错别字、口头禅、粗口、标点都保留；看到明显错字或事实可疑处，在交付说明里提一句，由用户决定改不改。
- **不加事实**：不补数据、不补来源、不加话题标签；原文缺来源时，在交付说明里提醒「这条有数据但没来源」。
- **不用 Markdown**：X 稿里没有 `- ` 列表、`#` 标题、`**加粗**`、`> 引用`、`~~删除线~~`、代码围栏；话题标签保留在最后一行。交付前跑 `lint_x_post.py`，错误清零。
- **只交付不代发**：发帖走 `topmind-x`，须用户确认。

## 和其他技能怎么配合

| 场景 | 组合 |
|---|---|
| 写完段子再统一排版 | `topmind-viral-posts` 出稿 → 本技能段子体（viral-posts 的段子默认已是段子体，需要重排时再用） |
| 写完短文再统一排版 | `topmind-briefs` 出 X 版 → 本技能短文体 |
| 公众号稿转 X 稿 | `topmind-wechat-post` 或 `topmind-briefs` 的公众号稿 → 本技能短文体（Markdown 列表自动改「·」「1）」，文内链接挪到另发的链接消息） |
| 格式化后要配图 | 先找原图；没有原图先问用户，同意后走 `topmind-cover` 的「X 短文封面」 |

## 示例（原创演示）

输入：

```text
就差96个破3000了，兄弟们今天能不能帮我冲一下？关注我的评论区留言，我挨个回！
```

段子体输出：

```text
就差96个破3000了，

兄弟们今天能不能帮我冲一下？

关注我的评论区留言，我挨个回！
```

带分点的段子体（输入有 `- ` 列表）：

```text
这周发帖就三步：

早上回评论

中午发原创

睡前回访新关注
```
