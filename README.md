# topmind-writing-skills

[English](./README.en.md) | 中文

[![Release](https://img.shields.io/github/v/release/topmindspace/topmind-writing-skills?style=flat-square&color=blue)](https://github.com/topmindspace/topmind-writing-skills/releases)
[![npm](https://img.shields.io/npm/v/@topmindspace/topmind-writing-skills?style=flat-square)](https://www.npmjs.com/package/@topmindspace/topmind-writing-skills)
[![CI](https://img.shields.io/github/actions/workflow/status/topmindspace/topmind-writing-skills/ci.yml?style=flat-square&label=CI)](https://github.com/topmindspace/topmind-writing-skills/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

**让 AI 写出像人写的社交媒体内容。** 段子、快讯、长文、排版、改稿、封面、长图，八个技能装进你的 AI 助手（Claude Code、Cursor、Codex……），说一句「来条段子」「发个快讯」「改稿」就开工。

<p align="center">
  <img src="docs/assets/writing-cover.png" alt="topmind-writing-skills · 写作技能合集" width="960" />
</p>

```bash
npx @topmindspace/topmind-writing-skills install topmind-viral-posts   # 装一个
npx @topmindspace/topmind-writing-skills list                          # 看全部
```

## 它和「让 AI 随便写一条」有什么不一样

- **先定类型，再动笔**：段子有 14 种写法，短文有 9 种内容类型，每种的首行、结构、收尾都不一样。
- **一眼快餐**：X 正文只留事实、数字和亮点；查证过程、口径说明、链接、原图都另发，正文可以直接复制。
- **去 AI 味有脚本**：套话、播报腔、套路互动尾巴、编出来的亲历、标点腔，脚本逐条标出来，人来决定改不改。
- **长文先有判断**：骨架里必须先写「我的判断」，素材给判断作证，不写成资料汇编。
- **事实不动**：改稿只改表达，不改数字、引语和确定性；每处改动都说得出依据。

## 能写什么

| 类别 | 技能 | 一句话 | 你可以这样说 |
|---|---|---|---|
| 段子 | [`topmind-viral-posts`](./topmind-viral-posts/) | 一句一行、零 emoji 的 X 短帖，14 种写法 | 「来条段子」「不懂就问」「写个群聊体」 |
| 短文 | [`topmind-briefs`](./topmind-briefs/) | 一件事讲完就停：快讯、预告、新品、羊毛、榜单、论文、实测 | 「发个快讯」「来篇短的」「写条预告」 |
| 长文 · X | [`topmind-x-article`](./topmind-x-article/) | X Article：单源 Markdown → 一键复制 HTML + 图文预览 | 「写 X 长文」「出一键复制版」 |
| 长文 · 公众号 | [`topmind-wechat-post`](./topmind-wechat-post/) | 公众号长文：质量三关、图片内嵌排版、发布清单 | 「写公众号」「公众号排版」 |
| 格式化 | [`topmind-format`](./topmind-format/) | 现成文字只改排版不改字：转段子、格式化成短文、几个开头拼成品 | 「转段子」「排一下版」 |
| 改稿 | [`topmind-revise`](./topmind-revise/) | 结构 → 事实 → 逻辑 → 去 AI 味 → 保真审计；也能快审一条回复 | 「改稿」「去 AI 味」「看看这条回复」 |
| 封面 | [`topmind-cover`](./topmind-cover/) | X 和公众号封面：22 种风格、标题逐字核对 | 「做个封面」「头图」 |
| 长图 | [`topmind-poster`](./topmind-poster/) | HTML → 高清长图 / 海报 / 信息图，文字数字逐字正确 | 「出张长图」「做个榜单图」 |

> **短文** = X 纯文本帖，1000 字以内都行；**长文** = X Article 或公众号长文；**段子** = 一句一行、行间空一行的短帖。

## 段子：14 种写法

先想清楚**想让哪种人来评论**，再挑写法：

| 写法 | 一句话 | 典型开头 | 想要的评论 |
|---|---|---|---|
| A1 不懂就问 | 装傻式真疑问 | 难道没人…吗？ | 懂行的人来解释 |
| A2 扒料求证 | 线索 + 上次结果 + 猜测 | XX 要上新了？！ | 补线索、猜结果 |
| A3 故障求证 | 第一时间问挂没挂 | XX 挂了吗？ | 「我也是」+ 接梗 |
| A4 卧槽体 | 真实反应 + 换算反差 | 卧槽，算完我人傻了 | 震惊、转发 |
| A5 冷知识 | 我才知道 / 白干了 | 我才知道… | 「我也才知道」 |
| A6 群聊体 | 每家一句「xx：」 | 今日 XX 群： | 接梗、补一家 |
| A7 连续剧 | 同一主角的连续进展 | 栏目名 + Day N | 竞猜、出主意 |
| A8 算账 | 自己的数字换算成钱和时间 | 一个 XX 干掉我 N% 额度 | 晒自己的账 |
| A9 站边轻判断 | 承认一方 + 内行轻判断 | 确实…但… | 两边站队 |
| A10 荒诞自嘲 | 集体痛点写成荒诞画面 | 我以为…已经是极限了 | 共鸣、晒经历 |
| A11 产品反转 | 具体产品 + 场景 + 动作反转 | 一个生活场景 | 接梗 |
| A12 借热点 | 新事套旧梗 | X 版「某某」来了 | 接梗、站队 |
| B1 关系帖 | 互关、新人、打卡 | 真实进展 | 关注、打招呼 |
| B2 互助帖 | 求码、送码 | 真实需求 | 送码、求码 |

每种写法都有适用题材、钩子、结构、收尾、反例和原创示例，见 [patterns.md](./topmind-viral-posts/references/patterns.md)。

## 短文：9 种内容类型

| 类型 | 首行怎么写 | 收尾 |
|---|---|---|
| 快讯（首发） | 是什么 + 最狠的一个数，比读者认识的对手 | 「...」或不收 |
| 快讯（晚到） | 换角度：实测、算账、求证 | 「...」 |
| 预告 / 传闻 | 「要来了？！」，动词照口径 | 「？！」 |
| 新品 / 工具 | 真疑问或一句真心推荐 | 「...」 |
| 羊毛 / 优惠 | 一句话说能马上拿到什么 | 不收 |
| 榜单 / 数据 | 谁第一、领先多少 | 不收 |
| 论文 | 一句结论 | 不收 |
| 实测 | 结果一句（翻车、快、贵） | 自嘲或一个真问题 |
| 观点一句话 | 一句内行的轻判断 | 判断本身 |

首发窗口以分钟计，晚了就换角度；预告和正式发布分开写。细则见 [topmind-briefs](./topmind-briefs/SKILL.md)。

## 看看效果

示例全部原创，名称和数字是虚构的。

**段子 · A6 群聊体**

```text
今日模型群：

青鸟：新版本上线了，价格没动

Nova：我们也上线了，价格动了

小甲：你们上线前能不能先说一声

用户：我只想知道今天哪家不排队
```

**段子 · A11 产品反转**

```text
让某编辑器的 agent 帮我整理仓库

它扫了一遍

说有个文件三个月没人动过

建议删掉

我点了确认

然后它自己的配置文件就没了
```

**短文 · 快讯（首发）**

```text
某模型低调上线新版：编程评测 31 → 42，价格不变

网页、App、接口已全量切换，权重开源。

几项关键提升：

1）编程评测：31 → 42
2）推理评测：37 → 43
3）智能体评测：74 → 77，比某知名闭源模型高 3 分

单任务成本两毛钱出头...
```

链接、官方评测图、「分数是厂商自测」这类口径提醒，都另发给作者，不进正文。

**去 AI 味 · 改前 → 改后**

```text
重磅！某编辑器 3.0 发布，AI 编程迎来新纪元！

更新内容：
🔹 补全更快
🔹 支持本地模型
🔹 插件市场改版

这不仅是一次更新，更是开发方式的变革。
```

```text
某编辑器 3.0 发布，可以接本地模型了

更新内容：
· 补全更快
· 支持本地模型
· 插件市场改版
```

去掉了「重磅」和「新纪元」（播报腔）、「不仅…更是…」（递进套句）和升华收尾；首行换成读者最关心的那个变化。

更多示例：[段子](./topmind-viral-posts/examples/) · [短文](./topmind-briefs/examples/) · [格式化](./topmind-format/examples/) · [改稿](./topmind-revise/examples/) · [X 长文](./topmind-x-article/examples/) · [公众号](./topmind-wechat-post/examples/) · [长图](./topmind-poster/examples/) · [封面](./topmind-cover/assets/examples/)

## 长文：先有判断，再有素材

一篇长文一个文件夹，`article_scaffold.py` 一条命令建好：

```text
<文章名>/
├─ <文章名>.md    唯一源稿
├─ 骨架.md        主要信息、读者、我的判断（必填）、每节要点 / 形式 / 图表计划
├─ 素材来源.md    每张图、每个数字的出处（不发布）
├─ images/  cover/  raw/自制图源/
└─ out/           X 长文 HTML、公众号 HTML、预览.png（随时可重建）
```

- **我的判断**：3–5 条，每条写依据和读者会怎么反驳；一节很长却没有判断，脚本会提示「素材罗列」。
- **自制图**：方法论、架构、对比类文章至少一张，把自己的判断画出来。
- **图文预览**：交付前生成 `out/预览.png` 先看一遍；X 粘贴不了的表格可以自动转成图。

## 写法规则：原则优先

所有技能共用一套分层规则（唯一真源 `shared/references/`，每个技能自带副本，单独安装也能用）：

| 层 | 文件 | 管什么 |
|---|---|---|
| 写作原则 | `social-writing-principles.md` | 先想清楚传达什么、结论先行、每句有新信息、形式跟内容走、原图优先、站在读者那边 |
| 信息设计 | `information-design.md` | 先写骨架、内容 → 形式（列表 / 表格 / 图 / 段落）、篇幅和密度 |
| 措辞口吻 | `core-voice.md` | 十条措辞原则，V01–V40 是它们在标题、开头、数字、问句、回复、段子里的例子 |
| 审稿 | `de-ai-rules.md` + `topmind-revise` | 去 AI 味（长文模式 + 社交短帖 S01–S10）、改写边界、保真审计 |

人设是**还在学习的普通人**：讲自己看到、试过的，不站讲台，不确定就直说。

### 脚本只提示，人来判断

```bash
python3 scripts/lint_x_post.py X短文.txt --kind news   # 快讯
python3 scripts/lint_x_post.py 段子.txt --duanzi        # 段子
python3 scripts/de_ai_lint.py 文章.md --genre long      # 长文
```

| 级别 | 含义 | 要求 |
|---|---|---|
| E 错误 | Markdown 残留；正文里有 URL / 来源行 / 配图说明 | 必须清零 |
| W 警告 | AI 套话、套路互动尾巴、类比腔、英文模板句、标点腔、回复过长…… | 每条给结论：改，或写明保留理由 |
| H 提示 / I1–I9 | 语境词、首行偏长、口径词进了正文、播报模板；信息设计（长段、可转列表、素材罗列……） | 只供判断，不进 `--strict` |

作者有往期帖子数据时，`post_type_report.py` 可以统计自己哪些开头、收尾、类型表现更好，生成一份习惯摘要给改稿用；数据只留在作者本机。

## 怎么组合

| 你要做的事 | 组合 |
|---|---|
| 同一件事出快讯和段子 | `topmind-briefs` 出快讯，`topmind-viral-posts` 出段子，事实保持一致 |
| 写好的文字只要排版 | `topmind-format`；要改内容转 `topmind-revise` |
| X 长文 | `topmind-x-article` + `topmind-revise` + `topmind-cover` |
| 公众号长文 | `topmind-wechat-post` + `topmind-revise` + `topmind-cover` |
| 榜单长图 | 文案先由 `topmind-briefs` 写好，再交给 `topmind-poster` |

所有技能只起草、不代发；发布由你确认。

## 安装

**npm = 钉版本快照；GitHub = 跟仓库最新。**

```bash
npx @topmindspace/topmind-writing-skills install topmind-briefs --to ./.claude/skills
npx @topmindspace/topmind-writing-skills@latest install topmind-briefs   # 升级：旧版直接覆盖
npx @topmindspace/topmind-writing-skills install topmind-briefs --force   # 同版本重装 / 降级
npx @topmindspace/topmind-writing-skills uninstall topmind-briefs --to ./.claude/skills
npx github:topmindspace/topmind-writing-skills install topmind-briefs     # 跟仓库最新
```

- 默认探测 `./.agents` → `./.claude` → `./.cursor` → `./.codex` → `./.mimocode`，再到用户级目录；安装摘要会打印实际目标目录。
- 已装更旧的版本就覆盖；版本相同提示已是最新；要降级加 `--force`。
- 技能 id 不是独立 npm 包，不要 `npm install topmind-briefs`。

<details>
<summary>仓库结构与发布</summary>

```text
topmind-writing-skills/
├─ topmind-*/                    # 八个技能（SKILL.md + references + scripts + examples）
├─ shared/                       # 共享脚本与写作规则的唯一真源（manifest.json 声明分发目标）
├─ bin/topmind-writing-skills.js # CLI：list / install / uninstall
├─ evals/                        # 路由评测用例（不进 npm 包）
├─ docs/                         # 发布规范 · CI 说明
└─ scripts/                      # 仓库级门禁、同步、隐私扫描
```

- 改共享文件只改 `shared/`，再跑 `npm run sync:shared`；CI 校验各技能副本逐字节一致。
- SKILL.md frontmatter 只用 Agent Skills 规范字段，能通过 `skills-ref validate`。
- push main 后 GitHub 立即可见；打 tag `vX.Y.Z` 自动出 Release 并发布 npm。每个技能的版本号写在它自己的 `SKILL.md` 和 [CHANGELOG](./CHANGELOG.md) 里。
- 详见 [docs/PUBLISHING.md](./docs/PUBLISHING.md) · [docs/ci.md](./docs/ci.md)。

> 正式商务演示技能已独立成仓库：[`topmind-presentation`](https://github.com/topmindspace/topmind-presentation)。

</details>

## 许可证

MIT © TopMindspace — [LICENSE](./LICENSE)
