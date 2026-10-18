---
name: topmind-wechat-post
description: "管一篇公众号文章从选题/底稿到发布清单的完整生命周期：单源文章文件夹 <文章名>/<文章名>.md、审校改写、质量三关（默认组合 topmind-revise：事实/逻辑/去AI味，含改稿保真溯源审计）、状态同步；用户要公众号版时再按需出微信内联 HTML 与发布清单到 out/。不代发。Use when 写公众号、写公众号文章、公众号长文、公众号排版、微信排版、公众号定稿、发公众号、公众号交付包、公众号发布清单、wechat、mp format。Do NOT use for 公众号短文与快讯（300–800 字，→ topmind-briefs）、X 帖子与段子（→ topmind-viral-posts；派生的 X 短帖交付一段可复制纯文本，链接、原图另发）、X 纯文本格式化与转段子（→ topmind-format）、X 长文（→ topmind-x-article）、封面与头图（→ topmind-cover）、长图与海报（→ topmind-poster）、只改错别字、小红书/知乎、纯网页发布、单独改稿与去 AI 味（→ topmind-revise）、通用长文写作（→ topmind-write）。"
license: MIT
metadata:
  version: "0.3.16"
  action_category: "write"
  triggers: "公众号, 写公众号, 微信排版, 公众号排版, 公众号稿, 公众号长文, 排版这篇文章, 定稿, 发公众号, 公众号交付, wechat, mp format, 写公众号文章, 公众号排版定稿, 公众号发布清单"
  author: "TopMindSpace"
  homepage: "https://github.com/topmindspace/topmind-writing-skills#readme"
  updated: "2026-10-18"
---

# topmind-wechat-post · 公众号创作技能

**公众号专用写作技能**。管一篇公众号文章从选题/底稿到发布清单的完整生命周期。

```
选题/底稿 → 建文章文件夹 → 创作 → 质量三关（topmind-revise）→ 定稿(frontmatter status)
          →（按需）排版到 out/ → 发布清单 →（可选）回推 notes
```

默认交付一份 `<文章名>/<文章名>.md`（含 images/、cover/、素材来源.md），Obsidian 里直接能看；
用户说「公众号排版 / 公众号版」时才跑 `md2wechat.py`，产物进 `out/`。

> 用户明确说公众号 / 微信排版时进本技能；通用长文写作不在本技能范围内。
> 篇幅在 300–800 字的公众号短文走 `topmind-briefs`（双平台短文），本技能管长文与完整交付包。
> 同一选题要出 X 版时，从同一份 `<文章名>.md` 派生（→ `topmind-x-article`，按需进 `out/`）；X 纯文本稿的列表改成「·」「1）」（emoji 可选，不强制）
>（X 纯文本不渲染 Markdown 列表，规则见 [references/x-post-format.md](references/x-post-format.md)），
> 只允许排版差异，内容一致；源稿本身继续用 Markdown 列表。
> 派生的 X 短帖按 **[references/x-delivery-contract.md](references/x-delivery-contract.md)（必读必守）** 交付：正文是一段可直接复制的纯文本，**不含 URL 和来源行**；长文里的文内链接和原图挪到另发的链接 / 图片消息。公众号长文本身可以有文内链接，不受此限。

## 先读：写作原则与信息设计

本技能建立在两份共享文件上，动笔前先读：

- [references/social-writing-principles.md](references/social-writing-principles.md)：8 条社交媒体写作原则（先想清楚、结论先行、每句都有新信息、形式跟内容走、简单清楚、原图优先、站在读者那边、真实有分寸）
- [references/information-design.md](references/information-design.md)：内容 → 形式决策表、篇幅和密度、去啰嗦的判断法
- 措辞和口吻在这两层之上，见 [references/core-voice.md](references/core-voice.md)

长文：先写骨架（每节要点 + 形式 + 图表计划 + 字数），再写正文。

## 语言：默认中文

- **默认中文**：标题、正文、配图文案一律用中文写作，这是默认行为，不需要用户每次声明。
- **英文是例外**：只有用户**明确说**"写英文文章"时才用英文。用户消息里夹杂英文词、
  给英文参考素材、引用英文原文，都不算"要求写英文"。
- 官方产品名、模型名、论文标题保留英文；引语正文写「人名：中文意思」，英文原文记进素材来源，
  不在正文里原文加括注（`references/core-voice.md` V13）。

## 脚本（真源）

| 脚本 | 用途 |
|------|------|
| `scripts/new-article.py` | 建文章文件夹：默认调用 `article_scaffold.py` 建新结构；`--legacy` 建旧交付包 |
| `scripts/article_scaffold.py` | （共享脚本）新建 `<文章名>/<文章名>.md` + images/cover/raw/out + 骨架.md + 素材来源.md；已存在就报错，不覆盖 |
| `scripts/check_article.py` | （共享脚本）文章文件夹体检：五项 frontmatter、H1 = title = 文件名、图片存在且编号跟出现顺序一致、无容器 / callout / `![[ ]]`；草稿期占位截图只给 W4、定稿才算错；E 级退出码 1 |
| `scripts/sync-status.py` | 状态 ⇄ 字数（新结构只改 frontmatter；旧交付包保留 `-released` 改名） |
| `scripts/sync-mapping.py` | 映射一致性（frontmatter + 目录 + 可选 notes + topic 总表），新旧结构都认 |
| `scripts/push-to-topstream.py` | 可选回推：公众号稿降级为纯 Markdown notes |
| `scripts/lint-wechat.py` | 排版体检 + 自动修复（中英文间距、段长、AI 腔…）；源稿出现 `:::` 报错（旧交付包 `公众号稿.md` 只告警） |
| `scripts/md2wechat.py` | Markdown → 全内联 HTML 到 `out/`；**必加 `--embed-images`**；手写小标题序号原样保留 |
| `scripts/de_ai_lint.py` | 去 AI 味检查（公众号稿默认用它）：W 警告（W9、W14–W21）+ H 提示（语境词等，只供判断）；规则见 `references/de-ai-rules.md` |
| `scripts/lint_x_post.py` | 派生 X 版时的 X 稿检查：无 Markdown 列表/标题/加粗，正文无 URL / 来源行 / 配图说明；去 AI 味部分复用 `de_ai_lint.py`（`--md` 等同 `de_ai_lint.py`） |
| `scripts/count_words.py` | 统一口径字数（改前 / 改后、单段最长） |
| `scripts/revise_check.py` | 改稿保真比对（数字、引语、专名、确定性词）+ 过度改稿检查 |
| `scripts/info_design_hints.py` | （共享脚本）信息设计提示 I1–I8，只供判断；`lint-wechat.py`、`de_ai_lint.py` 也会附带显示 |
| `scripts/scan_ai_flavor.py` | 中文去 AI 味打分入口：默认跑随包 `scan_ai_flavor_builtin.py`（词面分）；`$TOPMIND_AI_SCAN` 指向外部扫描脚本时转发过去；`--which` 查实际执行哪份 |
| `scripts/audit-provenance.py` | （共享脚本）**改稿保真审计**：双向逐段溯源（本稿→源稿 / 源稿→本稿），抓悄悄扩写与被落下的段。有源稿时定稿必跑 |
| `scripts/wechat_paths.py` | 路径解析模块（被上面脚本导入）：不写死个人路径、类别编号与年份 |

```bash
# 路径解析：CLI --base / --workspace → env TOPMIND_WECHAT_BASE / TOPMIND_WORKSPACE；解析不到就报错
export TOPMIND_WORKSPACE=/path/to/workspace   # 推荐
python3 scripts/new-article.py --title "文章名"                 # → <专题>/文章名/文章名.md
python3 scripts/check_article.py <专题>/文章名/
python3 scripts/lint-wechat.py --input <专题>/文章名/文章名.md --fix
python3 scripts/scan_ai_flavor.py <专题>/文章名/文章名.md      # 总分 ≥85；先跑 de_ai_lint.py 逐句定位
python3 scripts/md2wechat.py --input <专题>/文章名/文章名.md --embed-images   # 按需 → out/
python3 scripts/sync-status.py --set 定稿 <专题>/文章名 --apply  # 只改 frontmatter，目录名不变
```

细节见 [`references/workflow.md`](references/workflow.md) · [`references/known-pits.md`](references/known-pits.md)。

## 路径默认

| 用途 | 解析 |
|------|------|
| 文章文件夹的上级（专题目录） | `--base` → `TOPMIND_WECHAT_BASE` → 工作区里按**名称**发现的「长文」类别（兼容旧名「创作」「专题」）+ `{当年}-公众号`；`TOPMIND_WECHAT_CATEGORY` / `TOPMIND_WECHAT_TOPIC` 可覆盖；都解析不到就报错 |
| 工作区 | `--workspace` → `TOPMIND_WORKSPACE` |
| 底稿/回推 | `--topstream` → `TOPSTREAM_ROOT` → 可选；没有则跳过 notes 校验（`push-to-topstream.py` 必须给） |
| 终稿交付 | 可 `save-output` 拷贝到 role:delivery 类别（以 `topmind.yaml` 实际目录为准，如 `88-输出/`），文章文件夹仍留在长文类专题 |

编号和年份都不写死：工作区类别以 `topmind.yaml` 与磁盘实际目录名为准（当前模板为 `00-收件箱 / 10-动态 / 20-长文 / 30-短文 / 40-小说 / 60-参考素材 / 70-已发布 / 88-输出 / 99-归档`，以后改编号也不影响脚本）。

## 三条路径

### forward（底稿 → 公众号）

```
底稿 notes/*.md → 审校改写 → 质量三关 → 定稿 → 排版 → 发布
```

`new-article.py --title "文章名" --direction forward --source-file notes/xxx.md`

### reverse（选题原创）

```
选题包 → 调研素材 → 多轮改稿 → 三关 → 定稿 → 排版 → 发布 →（可选）push-to-topstream
```

`new-article.py --title "文章名"`（reverse 是默认；要对接 topstream 时加 `--source-file`，会写入可选字段 `target_file: pending`）

### 站外拉取（转载整合 / 在线精选站）

源不在本工作区、也不在 topstream `notes/` 时，**仍落 `reverse` + `target_file: pending`**。  
**不要用 `forward`**：它要求 `source_file` 以 `notes/` 开头且文件真实存在，站外源必然过不了 `sync-mapping.py`。

```bash
python3 scripts/new-article.py --title "<标题>" --direction reverse
```

取源注意（RSC 载荷、图片 hash 映射、`md5` 去重、截图裁切）见 `references/workflow.md`「站外拉取取源注意」；差异与口径写进文章文件夹的 `素材来源.md`。

**回推纪律**：notes 保持纯 Markdown（源稿本来就不用 `:::` 容器；旧交付包里的容器 / 徽章 / `==高亮==` 回推时去掉）；回推**务必带 `--assets`**（否则 GitHub 上 `images/` 死链）。命令串见 `references/workflow.md`「收尾」。

## 文章文件夹与状态

```text
<文章名>/                        # 文件夹名 = 文章名，不随状态改
├── <文章名>.md                  # 唯一源稿，唯一改稿入口
├── images/                      # 01-xxx.png、02-xxx.png…，按正文出现顺序编号
├── cover/                       # 封面
├── 素材来源.md                  # 私有：图源、承重事实来源、未核实条目
├── raw/                         # 原始素材（不发布）；改稿备份放 raw/备份-<时间戳>/
└── out/                         # 按需生成，可随时重建，不手改
    ├── <文章名>-公众号版.html   # 浏览器打开 → 复制正文 → 粘贴后台
    ├── 图片上传清单.md  images/
    └── 改稿报告.md              # topmind-revise 的完整报告
```

**frontmatter（固定五项 + 可选字段）**

```yaml
title: 文章名           # = H1 = 文件名（check_article.py 校验）
date: 2026-10-18
status: 草稿            # 草稿 | 定稿 | 已发布
tags: [AI, Agent]
cover: cover/cover-1500x600.png   # 草稿期封面还没做 → check_article W5；定稿时 → E7
subtitle: 从一个插件被下架说起    # 可选：副标题，md2wechat 写进图片上传清单的「摘要」，正文不重复；留空即可
# 以下为可选字段：对接 topstream 时才写，有就维护，没有不报错
direction: reverse      # forward | reverse
source_file: ""         # forward 填 notes/xxx.md
target_file: pending    # reverse：pending | notes/xxx.md
word_count: 0           # 纯中文字数，sync-status 维护
```

**交付**：发布/分享时直接用 `out/` 里的 HTML 原文件原样呈现，
不临时重新生成版本；`<文章名>.md` 是唯一改稿入口，改稿后重建 `out/` 再交付。

状态**不要手改目录名**，用脚本改 frontmatter：

```bash
python3 scripts/sync-status.py --set 定稿 <专题>/<文章名> --apply
```

**旧交付包（只读兼容，不自动迁移）**：`YYYY-MM-DD-<短名>[-released]/公众号稿.md` 照旧能
lint、排版、同步状态（`-released` 改名逻辑只对旧包生效）；`new-article.py --legacy` 仍能建旧包。

## 质量三关（定稿前必过）

写稿前先填文章文件夹里的 `骨架.md`：主要信息、读者、每节要点 / 形式 / 图表计划 / 字数（方法见 [`references/information-design.md`](references/information-design.md) 第一、二节）。形式在骨架里定下来，写的时候才不会默认写成段落；写完回头对一遍骨架。再找图、记来源（[`references/image-sourcing.md`](references/image-sourcing.md)，信源清单放文章文件夹的 `素材来源.md`，不进本仓库）。**默认组合 `topmind-revise`**：三关由它执行（`mode=embed genre=long sources=<文章名>/素材来源.md`），它把终稿和三行摘要回给本技能、完整报告落 `out/改稿报告.md`；没装就按 [`references/revision-workflow.md`](references/revision-workflow.md) 手动走：⓪ 结构 → 事实 → 逻辑 → 删冗余 → 去 AI 味 → 核心经验对照（[`references/core-voice.md`](references/core-voice.md)）→ 排版 → 保真审计 → 过度改稿检查，每轮先备份、报改前 / 改后字数（`scripts/count_words.py`）。

### 关 1 · 事实

- 承重数字回**一手来源**；厂商口径与媒体报道分开写，媒体报道点名具体媒体（「据 XX 报道」），不写泛泛的「据报道」  
- 查不到一手来源的传闻**删**  
- 改稿续写：正文已有数字**回源重核**（上一轮文本最不可信）  
- 多口径（主轮/复跑）显式拆开；表格从数据源生成，禁止手抄  
- 外部工具改过的稿：**先核数字再动文字**；「比值对但绝对值错」= 全段重核  
- **有源稿时（`reverse` / 站外拉取）跑一次双向溯源审计**，不靠记忆判断改了几处：

  ```bash
  python3 scripts/audit-provenance.py --draft <文章名>/<文章名>.md --source <文章名>/raw/源稿-*.md
  ```

  正向查「本稿有、源稿找不到」（扩写藏在这里），反向查「源稿有、本稿落下」。**退出码 1 不是失败，是「有待判定项」**：每一项要么归入已声明的修正/增补，要么就是不该有的改动；逐条在 `素材来源.md` 里声明后即收口。源稿里后加的块（勘误等）用 `--skip '^>\s*\[!'` 排除。细节见 `references/workflow.md`。

  ⚠️ **适用范围**：本脚本按**段落**比对，只在「源稿与派生稿同构」时有效（如 X 长文 → 公众号稿）。若派生稿把**表格改写成句子、数据清单改写成图**，相似度会整体塌到阈值下、失去判别力（实测一篇多源综述：正向 39/39 段全部判为待判定）。此时改用**数字级回源核对**——把正文每个承重数字逐个对回底本，再把结果写进 `素材来源.md` 替代逐段判定。

### 关 2 · 逻辑

- 单边结论旁配反方证据  
- 结构前后一致；同一事实多处同值  

### 关 3 · 文字（去 AI 味）

**必过**：按 [`references/de-ai-rules.md`](references/de-ai-rules.md) 逐条过，先守改写边界（只改表达，不改事实和确定性）。

```bash
python3 scripts/de_ai_lint.py <文章名>.md --genre long   # W 每条有结论（改掉或写保留理由）；H 只供判断
python3 scripts/scan_ai_flavor.py <文章名>.md           # 总分 ≥85（人话）
python3 scripts/revise_check.py <备份>/<文章名>.md <文章名>.md   # 改稿后：数字 / 引语没被改坏，没命中的段落没被大改
```

- 配了外部扫描器（`$TOPMIND_AI_SCAN`）且它输出「作者姿态分」时，姿态分同样 ≥85；`--which` 确认实际执行哪份，定稿门禁要外部扫描器时加 `--require-external`
- 清单 / 词表 / 说明书类文体容易误判，脚本提示「疑似清单文档」时先确认文体

- 删套话/黑话/工程圈行话；降调段末加粗金句  
- **满分 ≠ 有人味**：再查「段末金句癖 / 节奏过分整齐 / 没有场景与我 / 报告体标注」  
- **口语化 ≠ 有人味**：删社交垫词（元叙述、空转过渡、姿态句）  
- 判据：**这句话删掉之后，读者少知道了什么？**  

详见 [`references/writing-quality.md`](references/writing-quality.md)。

## 排版要点（写稿时）

- 开头用具体事实，接地气、好懂（`references/core-voice.md` V05），不硬凑对仗收句；单段 2–3 句、≤110 字；列表项 ≤70 字  
- 二级标题要序号就手写「一、」「二、」，`md2wechat.py` 原样保留、不再自动编号（都没写时才按主题自动编号；`--auto-number` 恢复旧行为）  
- **源稿不用 `:::` 容器、callout、`![[ ]]`**：金句、数据、提示用普通段落、加粗或引用写；`lint-wechat.py` 对新源稿里的 `:::` 报错（旧交付包只告警，md2wechat 仍能渲染）  
- 图片写 `![说明](images/01-xxx.png)`，出处写在下一行「来源：……」，排版时渲染成图注  
- 评测稿：**图承担数据，正文只解读**；健康密度 **300–450 字/图**  
- 个股用词红线：禁用 买入/推荐/目标价…；文末投资声明  

更多：[`references/typography-rules.md`](references/typography-rules.md) · [`references/wechat-constraints.md`](references/wechat-constraints.md)。

## 排版与导出（必读）

用户要公众号版时才跑（产物缺省进 `<文章名>/out/`，`--slug` 缺省文件名，`--asset-root` 缺省文章文件夹）：

```bash
python3 scripts/md2wechat.py --input <文章名>/<文章名>.md --embed-images \
  [--theme assets/themes/minimal-ink.json]
# 旧交付包：--input <包>/公众号稿.md --out-dir <包> --slug <slug> --asset-root <素材根>
```

1. **永远 `--embed-images`**，否则粘贴丢图（相对路径被序列化成 file://）  
2. **图片 basename 一致（硬约束）**：正文引用名 = `images/` 目标名；禁止两套同名图共处  
3. 合规自检出现 `✗` 改生成器，不要手改 HTML  
4. **配图位置**：图片必须紧跟它证明的那段文字
   （最多隔一段）；改稿移动段落时图片行一起搬。构建后必跑：嵌入图数量=文档图数量、
   嵌入图顺序=文档出现顺序（逐张解码与源文件比对）；每张图前后 6 行做主题关键词
   邻近检查，不通过则人工核对。
5. **双版一致性校验**：同一选题出 X 版后，
   必跑 X 内嵌图序列 vs 公众号内嵌图序列的逐字节/逐像素比对（X 去掉封面后应完全一致）。
   两版都直接读同一份 `<文章名>.md` 的 `![]()`，禁止手工拼 `--images`
   （曾因文件名排序 ≠ 文档顺序，导致 X 版从某一节起整段配图错位）；`check_article.py` 校验编号跟出现顺序一致。

已知问题清单：[`references/known-pits.md`](references/known-pits.md)。

## 主题

| 文件 | 风格 | 适用 |
|------|------|------|
| `assets/themes/md3-business-blue.json`（默认） | MD3 商务蓝：Material Design 3 设计语言，大圆角，tonal 配色 | 通用 / 商务 / AI 技术 |
| `assets/themes/minimal-ink.json` | 黑白灰 + 砖红 | 深度研析 / 观点 / 随笔 |
| `assets/themes/tech-blue.json` | 科技蓝 | AI/技术 |
| `assets/themes/newsprint.json` | 报纸衬线 | 人文评论 |
| `assets/themes/graphite.json` | 石墨克制 | 严肃报告 |
| `assets/themes/amber-review.json` | 琥珀评测 | 产品评测 |

`md2wechat.py --list-themes` 看全部；`--theme genre:评测` 可按题材自动选。  
渲染规格见 [`references/element-spec.md`](references/element-spec.md) · 主题映射见 [`references/theme-map.md`](references/theme-map.md)。

**平台红线速查**（详见 [`references/wechat-constraints.md`](references/wechat-constraints.md)）：禁 `div`/`pre`/`h1`/`figure`/`thead`/flex/float/gradient/shadow；表格 `table-layout` 不写 fixed；列数 ≥4 转卡片。

## 与 Desktop「公众号创作」

topmind Desktop 的「公众号创作」插件是本技能的可视化工作流伴面（若有）：包列表 → 改稿 → 三关 → 预览 → 导出。导出时它优先调用本技能的 `scripts/md2wechat.py`，脚本语义以本技能为准。本技能已取代 topmind-skills 包里旧的 `topmind-wechat`（4.15.2 起删除）。

## 外部依赖

无必需的外部技能。去 AI 味规则与检查随包自带（`references/core-voice.md`、`references/de-ai-rules.md`、`scripts/de_ai_lint.py`、`scripts/scan_ai_flavor.py`）；推荐同时安装 `topmind-revise` 执行质量三关，没装时按随包的 `references/revision-workflow.md` 手动走；
想接入自己的扫描脚本时设 `$TOPMIND_AI_SCAN=/path/to/script.py`，参数与退出码原样转发。

## When NOT to use

- 只想改几个句子 → 直接编辑  
- 小红书 / 知乎 / 掘金 → 平台约束不同  
- 公众号短文、快讯、数据榜单（300–800 字，X + 公众号双版）→ `topmind-briefs`  
- X 帖子、段子、涨粉帖 → `topmind-viral-posts`；X 长文 → `topmind-x-article`  
- 单独出长图、海报、信息图 → `topmind-poster`  
- 通用长文写作与交付 → `topmind-write`（topmind-skills 包）
- 封面配图、头图 → `topmind-cover`
- 只改稿、去 AI 味、质检，不排版 → `topmind-revise`（没装就按 `references/de-ai-rules.md` 改写，跑 `scripts/de_ai_lint.py` 核对）

## 历史案例

具体项目里沉淀下来的做法（带日期）见 [`references/case-notes.md`](references/case-notes.md)，按需读取；本页只保留通用规则。

## 写作原则

写作原则见 [references/social-writing-principles.md](references/social-writing-principles.md)（第 0 层）和 [references/information-design.md](references/information-design.md)（第 1 层）；研究类选题按 [references/research-mode.md](references/research-mode.md)；目录和交付规约见 [references/workspace.md](references/workspace.md)。触发本技能时默认执行。
