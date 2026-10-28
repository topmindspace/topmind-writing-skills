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
npx @topmindspace/topmind-writing-skills install all      # 首次安装整套
npx @topmindspace/topmind-writing-skills@latest update    # 以后只更新已装技能
```

装好后直接对 AI 说「改这篇」「写条快讯」「给这篇做封面」。只想装一个，用 `install topmind-revise` 等技能 ID；`list` 查看全部。Desktop 和 Obsidian 已内置经过验证的写作快照，应用内更新从各自“关于与更新”进入，不需要再运行上面的 npx 命令。

宿主默认绑定活跃笔记，允许显式换稿。当前稿件、少量全局记忆和所选技能分层加载；其余资源按需读取，压缩不重置已完成操作和预算。

## 在 Desktop 与 Obsidian 中使用

默认内置 [topmind-writing-skills](https://github.com/topmindspace/topmind-writing-skills) 的版本化快照：改稿、只排版、短文、互动短帖、公众号、X 长文、封面与长图。写作仓独立迭代和发布，宿主内置经过验证的版本。

打开 Markdown，Desktop 从文章工具栏「写作」、应用、状态栏或命令面板进入；Obsidian 从 Ribbon、工作台、笔记/编辑器菜单或命令面板进入。选择动作先展示用途、目标和结果模式，明确开始后才发送 AI。源稿继续在主编辑器修改；选择格式和主题后生成预览，可复制正文或导出到源稿旁的 `out/`。旧 `公众号稿.md` 和文章目录可直接使用，不会被批量改名。

内置 HTML/文本排版无需 Python，预览与复制同源；源稿或图片改变后需要重新生成。扩展容器、图表源码、缺图和平台表格粘贴限制会显示诊断。封面生图、PNG 和外部发布依赖实际工具，复制不等于已发布。审校不使用“AI 味分数”作为定稿门槛。

“关于与更新”分别展示 Desktop、核心技能、独立写作包和集成组件。写作资源可独立更新；编译进宿主的排版代码随宿主升级。受管包按身份隔离，覆盖本地定制会被阻止，失败保留旧版。Desktop 支持标准更新器下载后显式重启；签名、平台或渠道不支持时保留手动下载。

## 加选项，让经验帮助创作

- **看过再借鉴**：实际阅读参考作品和可见样张，迁移角度、组织、节奏与设计关系。
- **按需探索**：方向未定时试几种真的不同的写法；明确要一稿就交完成稿，不固定多稿与审批回合。
- **偏好是选项**：口吻、长度、emoji、开头结尾和视觉风格跟任务与作者走，模板可以拆、混合或不用。
- **事实边界清楚**：正文保留必要归因、近似值和不确定性；隐私、授权、文件恢复与输出完整性仍明确核对。
- **工具帮助判断**：lint 提示回到语境，词面分数不作定稿门槛；真实质量通过作者或读者使用验证。

完整方法与同素材样张见 [创作实践](./shared/references/creative-practice.md)，整改范围与验证见 [审查报告](./docs/creative-skills-audit.md)。

## 能写什么

| 类别 | 技能 | 用途 | 你可以这样说 |
|---|---|---|---|
| 段子 | [`topmind-viral-posts`](./topmind-viral-posts/) | X 段子与互动短帖，14 类参考写法 | 「来条段子」「不懂就问」「写个群聊体」 |
| 短文 | [`topmind-briefs`](./topmind-briefs/) | 一件事讲完就停：快讯、预告、新品、羊毛、榜单、论文、实测 | 「发个快讯」「来篇短的」「写条预告」 |
| 长文 · X | [`topmind-x-article`](./topmind-x-article/) | X Article：单源 Markdown → 一键复制 HTML + 图文预览 | 「写 X 长文」「出一键复制版」 |
| 长文 · 公众号 | [`topmind-wechat-post`](./topmind-wechat-post/) | 公众号长文：质量三关、图片内嵌排版、发布清单 | 「写公众号」「公众号排版」 |
| 格式化 | [`topmind-format`](./topmind-format/) | 现成文字只改排版不改字：转段子、格式化成短文、几个开头拼成品 | 「转段子」「排一下版」 |
| 改稿 | [`topmind-revise`](./topmind-revise/) | 结构 → 事实 → 逻辑 → 去 AI 味 → 保真审计；也能快审一条回复 | 「改稿」「去 AI 味」「看看这条回复」 |
| 封面 | [`topmind-cover`](./topmind-cover/) | 小红书、抖音图文、公众号与 X 封面：平台适配、核字与多比例裁切 | 「做个封面」「头图」 |
| 长图 | [`topmind-poster`](./topmind-poster/) | HTML → 高清长图 / 海报 / 信息图，文字数字逐字正确 | 「出张长图」「做个榜单图」 |

**短文** = X 纯文本帖，1000 字以内都行；**长文** = X Article 或公众号长文；**段子** = 以观察、反差或幽默推进的短帖，排版按节奏选择。

## 创作方向与按需知识包

实施与验证见 [整改执行记录](./docs/creative-system.md)。

8 个技能共同使用“方向—具体例子—适用条件—反例 / 例外”的知识组织方式。事实、排版与工具协议继续核对；字体、场景、篇幅、修辞与风格由任务选择，不用统一审美门槛。

首批 37 张知识卡（35 张原创教学示例、2 条本次有记录的技术 / 视觉经验）随每个技能独立分发；先查摘要，再读相关卡片。可以补充指定私有包，经验先存为候选，不自动改写长期规则或把一次选择当普遍规律。用法与维护见 [知识包说明](./docs/knowledge-packs.md)。

```bash
npm run knowledge:search -- "字体 场景 优雅" --skill topmind-cover --limit 3
npm run knowledge:check
```

封面参考提供 22 个可变风格入口、16 类构图关系、24 个组合方向和 12 份完整提示词；[创作图册](./topmind-cover/assets/examples/creative-atlas.html) 有 8 组可见排版样张，可切换横竖布局。它们提供方法，不限定可创作范围，也不承诺流量效果。

## 多平台封面与图文

[平台参考](./shared/references/platform-cover-specs.md) 记录公开来源、核验日期和未实测项：小红书图文可从 3:4 起步，抖音普通图文与商城内容分别核对，公众号普通文章宽图 / 方图与图片消息分开处理。尺寸是本包导出预设，当前发布入口与用户要求优先。

`topmind-cover` 支持 `article`、`x-post`、`xiaohongshu`、`douyin` 和 `wechat` 预设；`wechat` 另给宽图与方图，裁切方向可调整。横竖版需要时分别构图，不用固定安全区或缺少证据的点击率约束设计。密集内容页用 `topmind-poster`，跨平台不自动扩展发布权限。

## 段子：14 种写法

先想清楚**想让哪种人来评论**，再挑写法：

| 写法 | 特点 | 典型开头 | 想要的评论 |
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
| 羊毛 / 优惠 | 直说能马上拿到什么 | 不收 |
| 榜单 / 数据 | 谁第一、领先多少 | 不收 |
| 论文 | 一句结论 | 不收 |
| 实测 | 结果一句（翻车、快、贵） | 自嘲或一个真问题 |
| 观点一句话 | 一句内行的轻判断 | 判断本身 |

以下是方向示例，不限定标点或收尾；时效已过时可补新角度，预告与发布保留状态差别。细则见 [topmind-briefs](./topmind-briefs/SKILL.md)。

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

正文保留“分数是厂商自测”等影响理解的归因与限定；详细来源、原图可另列，有用的链接也可随文。

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

## 长文：结构按内容选择

一篇长文一个文件夹，`article_scaffold.py` 一条命令建好：

```text
<文章名>/
├─ <文章名>.md    唯一源稿
├─ 骨架.md        主要信息、读者、主线与依据（按需）、每节要点 / 形式 / 图表计划
├─ 素材来源.md    每张图、每个数字的出处（不发布）
├─ images/  cover/  raw/自制图源/
└─ out/           X 长文 HTML、公众号 HTML、预览.png（随时可重建）
```

- **主线**：观点稿可列判断与反例，故事可列场景，教程可列任务与步骤，不凑固定数量。
- **配图**：原图、自制结构图和纯文字按理解价值选择，不设图片配额。
- **图文预览**：交付前生成 `out/预览.png` 先看一遍；X 粘贴不了的表格可以自动转成图。

## 写法规则：原则优先

所有技能共用一套分层规则（唯一真源 `shared/references/`，每个技能自带副本，单独安装也能用）：

| 层 | 文件 | 管什么 |
|---|---|---|
| 写作原则 | `social-writing-principles.md` | 先想清楚传达什么、结论先行、每句有新信息、形式跟内容走、原图优先、站在读者那边 |
| 信息设计 | `information-design.md` | 先写骨架、内容 → 形式（列表 / 表格 / 图 / 段落）、篇幅和密度 |
| 措辞口吻 | `core-voice.md` | V01–V40 是标题、开头、数字、问句、回复、段子的场景选项 |
| 审稿 | `de-ai-rules.md` + `topmind-revise` | 去 AI 味（长文模式 + 社交短帖 S01–S10）、改写边界、保真审计 |

声音跟当前任务、作者样本、读者与体裁走，不把所有作者固定成同一种人设。

### 脚本只提示，人来判断

在对应技能目录里运行（如 `topmind-briefs/`、`topmind-revise/`）：

```bash
python3 scripts/lint_x_post.py X短文.txt --kind news   # 快讯
python3 scripts/lint_x_post.py 段子.txt --duanzi        # 段子
python3 scripts/de_ai_lint.py 文章.md --genre long      # 长文
```

| 级别 | 含义 | 要求 |
|---|---|---|
| E 格式问题 | 误带标记、图片占位；链接分离只在 `--separate-links` 启用 | 核对实际格式；特殊代码和引用按语义处理 |
| W 编辑提示 | 句式、长度、标点、文字列表、正文链接等现象 | 按语境取用，可保留，无需逐条报告 |
| H 提示 / I1–I9 | 语境词、首行偏长、归因与限定、播报模板；信息设计（长段、可转列表、素材罗列……） | 只供判断，不进 `--strict` |

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
npx @topmindspace/topmind-writing-skills install all --to ./.claude/skills
npx @topmindspace/topmind-writing-skills status --to ./.claude/skills
npx @topmindspace/topmind-writing-skills@latest update --to ./.claude/skills
npx @topmindspace/topmind-writing-skills install topmind-briefs --to ./.claude/skills
npx @topmindspace/topmind-writing-skills install topmind-briefs --force --to ./.claude/skills
npx @topmindspace/topmind-writing-skills uninstall topmind-briefs --to ./.claude/skills
npx github:topmindspace/topmind-writing-skills update --to ./.claude/skills
```

- `install all` 首次安装整套；`update` 默认只更新已装的技能，不会擅自加装新技能；`status` 显示当前包快照与安装目录的差异。三者都支持 `--to` 指定实际目录。
- 不写 `--to` 时先找唯一的 TopMind 安装，再找唯一的技能目录或宿主配置；若同时存在多个候选，会列出目录并要求明确选择。没有宿主配置时使用当前项目的 `./.agents/skills`。结果会打印实际目录。
- 更新先复制到临时目录，完整后才替换；失败保留旧版。受管安装发现本地改动会停止，需明确 `--force`；强制替换时保留旧副本。升级早期未带安装记录的副本也会自动留备份。软链接或非同名技能目录不会被覆盖。
- 同版本不重复复制；已装版本比包新时拒绝降级，除非显式 `--force`。升级后重新打开 AI 会话，让宿主重新发现技能。
- 技能 id 不是独立 npm 包，不要 `npm install topmind-briefs`。

### 从本地仓库升级

本地未发布改动要从当前仓库安装，`@latest` 只包含 npm 已发布版本。先核实目标目录；已有跨工具软链接时更新其共享实际目录，保留链接关系。Codex 独立安装可在仓库根目录运行：

```bash
node bin/topmind-writing-skills.js status --to "$HOME/.codex/skills"
node bin/topmind-writing-skills.js update --to "$HOME/.codex/skills"
```

首次安装改用 `install all`；修改过技能内容而未改版本号时，用 `install <id> --force --to <实际目录>` 明确重装。CLI 只复制单个技能目录内的独立资源，不写入目标根目录的 `shared/`。

若 Codex 技能链接到其他共享目录，将 `--to` 换为核实后的实际目录；检查每项安装输出。安装了新技能或更新入口后，重开会话让宿主重新发现；同版本未发布内容需要明确加 `--force` 才会重装。

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

正式商务演示用 [`topmind-presentation`](https://github.com/topmindspace/topmind-presentation)，单独安装。

</details>

## 许可证

MIT © TopMindspace — [LICENSE](./LICENSE)
