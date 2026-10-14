---
name: topmind-format
description: "X 纯文本格式化：用户贴一段现成文字，只改排版、不改字。转段子 → 每句一行、行与行之间空一行，完全不用 emoji（去掉点缀与列表符号，分点一条一行）；格式化成短文 → 合理分段换行，列表改 emoji 项目符号，按 TopMind emoji 体系加标题 emoji 与鸡/猫/植物人设点缀。保留原文事实与措辞，自带保真校验脚本；交付遵守 X 交付规约：正文单独成块可直接复制，信源、原图、说明另列；短文分点用 emoji 列表符号、段子零 emoji；没有原图时询问是否配图。只交付不代发。Use when 转段子、改成段子格式、段子格式、格式化、格式化一下、格式化成短文、排一下版、整理格式、加空行、分行、加 emoji、X 排版、format。Do NOT use for 从零写段子、涨粉帖（→ topmind-viral-posts）、从零写干货短文、快讯（→ topmind-briefs）、X 长文（→ topmind-x-article）、公众号排版与公众号 HTML（→ topmind-wechat-post）、封面（→ topmind-cover）、把帖子发出去（→ topmind-x，须用户确认）。"
license: MIT
metadata:
  version: "0.1.3"
  action_category: "write"
  triggers: "转段子, 改成段子, 段子格式, 格式化, 格式化一下, 格式化成短文, 排一下版, 整理格式, 加空行, 分行, 加 emoji, X 排版, format"
  author: "TopMindSpace"
  homepage: "https://github.com/topmindspace/topmind-writing-skills#readme"
  updated: "2026-10-14"
---

# topmind-format · X 纯文本格式化

用户已经有文字，只想让它在 X 上好读。本技能**只动排版**：换行、空行、列表符号、emoji 点缀（emoji 只用于短文体）；
不改字、不增删事实、不调换顺序。要改写内容时，转给 `topmind-viral-posts`（段子）或 `topmind-briefs`（短文）。

## 何时不用

- 从零写段子、涨粉帖、互关帖 → `topmind-viral-posts`
- 从零写干货短文、快讯、榜单速报 → `topmind-briefs`
- X 长文、发 X 文章 → `topmind-x-article`
- 公众号排版、公众号 HTML → `topmind-wechat-post`
- 要改写措辞、压缩字数、换钩子（不只是排版）→ 按体裁转 `topmind-viral-posts` / `topmind-briefs`
- 发帖 → `topmind-x`（须用户确认）

> **必读必守**：[references/x-delivery-contract.md](references/x-delivery-contract.md)——**短文体**分点必须用 emoji 列表符号；**段子体完全不用 emoji**，分点不加符号、一条一行；两种都禁用 `- ` `1. `；格式化结果单独一个 `text` 块、只放可发布内容；信源、原图、改动说明块外另列。

## 两种模式

| 用户说 | 模式 | 做什么 |
|---|---|---|
| 转段子、段子格式、改成段子 | 段子体 `duanzi` | 每句一行，**行与行之间都空一行**；**完全不用 emoji**：去掉人设点缀、表情和列表符号，分点条目一条一行、行间空行 |
| 格式化、格式化成短文、排一下版 | 短文体 `short` | 合理分段（一段 1–3 行），列表改 emoji 项目符号，标题行首加 0–1 个与关键词对应的 emoji，开头/结尾 0–2 个人设点缀 |

只说「格式化」又看不出体裁时：原文有列表、数据、来源链接 → 短文体；原文是口语短句、吐槽、互关 → 段子体。还拿不准就给两版让用户挑。

## 工作流

1. **读原文**：确认是用户自己的文字或用户给的文字；记下原文里的数字、链接、话题标签、表情，后面逐一核对。
2. **断句**（版式规律见 [references/x-layout-patterns.md](references/x-layout-patterns.md)）：
   - 段子体：一句一行。长句在逗号处断开时，只断在意思完整的地方（例：「X 创作者收益里，」/「付费蓝V用户的互动权重会高很多。」），不在词中间断。原文的分点（`- ` `1.` `🔹` 等）去掉符号，条目一条一行、行间空行；原文自带的 emoji 一并去掉（保真校验不计 emoji）。
   - 短文体：标题一行；正文一段 1–3 行；并列信息改成列表（列表前的「xx：」引导语单独一行；条目超过一行时条目之间空一行）；原文已有【小标题】的保留并单独成行；链接、来源行、话题标签各自单独成行。
3. **加 emoji（只用于短文体）**：段子体一个都不加。短文体只用 TopMind 体系，唯一出处 [references/emoji-system.md](references/emoji-system.md)（本技能不另立规则）：
   - 人设点缀（🐔 🐱 为主角，🌱 🌿 🌸 等为配角）只放开头一行或结尾一行，同一帖最多 2 个；
   - 标题 emoji 必须对上标题关键词（发布 🆕、数据 📊、教程 🛠️ …），对不上就不放；
   - 列表符号一帖一套（🔹 / ▫️ / 1️⃣ / ✅❌），规则见 [references/x-post-format.md](references/x-post-format.md)；
   - 短文体里原文自带的表情保留，不重复叠加；严肃内容（事故、争议、处罚）不加人设点缀。
4. **跑脚本**（可选但推荐）：

   ```bash
   python3 scripts/format_text.py 原文.txt --mode duanzi --split --out 段子.txt
   python3 scripts/format_text.py 原文.txt --mode short --title-emoji 🆕 --open 🐔 --out 短文.txt
   python3 scripts/lint_x_post.py 短文.txt
   python3 scripts/lint_x_post.py 段子.txt --duanzi
   ```

   `format_text.py` 输出前做原文保真校验（去掉空白、列表符号与 emoji 后逐字比对），改动了字就报错；
   短文体把 Markdown 列表改成 emoji 列表；段子体去掉所有 emoji 与列表符号（条目间空一行，`--split` 不拆列表条目），并拒绝 `--open` / `--close` / `--title-emoji`。
   `lint_x_post.py` 检查 Markdown 残留、符号混用、表情数量、正文混入的说明（W12）、段子里的 emoji（`--duanzi`，W13）；段子体的单个行间空行不报错。
5. **交付**（按 [references/x-delivery-contract.md](references/x-delivery-contract.md)）：格式化结果单独一个 `text` 块；块外依次列信源（原文自带链接，没有就写「用户提供，未附来源」）、原图（用户给了就列 1–2 张，没有就写「未找到原图」并问要不要配图）、改动说明（做了哪些排版改动、加了哪些 emoji、发现的疑似错字）。多条帖子每条一块。

## 铁律

- **不改字**：错别字、口头禅、粗口、标点都保留；看到明显错字或事实可疑处，在交付说明里提一句，由用户决定改不改。
- **不加事实**：不补数据、不补来源、不加话题标签；原文缺来源时，在交付说明里提醒「这条有数据但没来源」。
- **不用 Markdown**：X 稿里没有 `- ` 列表、`#` 标题、`**加粗**`、`> 引用`、`~~删除线~~`、代码围栏；话题标签保留在最后一行。交付前跑 `lint_x_post.py`，错误清零。
- **只交付不代发**：发帖走 `topmind-x`，须用户确认。

## 和其他技能怎么配合

| 场景 | 组合 |
|---|---|
| 写完段子再统一排版 | `topmind-viral-posts` 出稿 → 本技能段子体（viral-posts 的段子默认已是段子体，需要重排时再用） |
| 写完短文再统一排版 | `topmind-briefs` 出 X 版 → 本技能短文体 |
| 公众号稿转 X 稿 | `topmind-wechat-post` 或 `topmind-briefs` 的公众号稿 → 本技能短文体（Markdown 列表自动改 emoji） |
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
