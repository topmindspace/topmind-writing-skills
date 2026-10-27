# 平台操作参考

按需查阅目录、脚本与导出细节。写法与质量判断见 SKILL.md 和共享经验；平台技术限制与审美选择分开处理。

## 封面与图文形态

普通文章宽封面、方形小图、正文头图与公众号图片消息分别处理，见 [平台封面参考](platform-cover-specs.md)。900×383 是本包预设，不是已核实的统一上传限制；宽图、方图、列表与分享预览按当前编辑器检查。

## 脚本（真源）


| 脚本 | 用途 |
|------|------|
| `scripts/new-article.py` | 建文章文件夹：默认调用 `article_scaffold.py` 建新结构；`--legacy` 建旧交付包 |
| `scripts/article_scaffold.py` | （共享脚本）新建 `<文章名>/<文章名>.md` + images/cover/raw/out/参考 + 骨架.md + 素材来源.md（frontmatter 带多环境字段，见 references/workspace.md 第 5 条）；已存在就报错，不覆盖 |
| `scripts/check_article.py` | （共享脚本）文章文件夹体检：五项 frontmatter、H1 = title = 文件名、图片存在且编号跟出现顺序一致、无容器 / callout / `![[ ]]`；草稿期占位截图只给 W4、定稿才算错；E 级退出码 1 |
| `scripts/sync-status.py` | 状态 ⇄ 字数（新结构只改 frontmatter；旧交付包保留 `-released` 改名） |
| `scripts/sync-mapping.py` | 映射一致性（frontmatter + 目录 + 可选 notes + topic 总表），新旧结构都认 |
| `scripts/push-to-topstream.py` | 可选回推：公众号稿降级为纯 Markdown notes |
| `scripts/lint-wechat.py` | 排版体检 + 自动修正（中英文间距、段长、AI 腔…）；源稿出现 `:::` 报错（旧交付包 `公众号稿.md` 只告警） |
| `scripts/md2wechat.py` | Markdown → 全内联 HTML 到 `out/`；需要内嵌图片时加 `--embed-images`，粘贴后带图需实测；手写小标题序号原样保留 |
| `scripts/de_ai_lint.py` | 去 AI 味检查（公众号稿默认用它）：W 警告（W9、W14–W21）+ H 提示（语境词等，只供判断）；规则见 `references/de-ai-rules.md` |
| `scripts/lint_x_post.py` | 派生 X 版时检查格式残留与图片占位；文字列表、正文链接和来源默认可保留，链接分离仅在显式选择时检查；去 AI 味部分复用 `de_ai_lint.py`（`--md` 等同 `de_ai_lint.py`） |
| `scripts/count_words.py` | 统一口径字数（改前 / 改后、单段最长） |
| `scripts/revise_check.py` | 改稿保真比对（数字、引语、专名、确定性词）+ 过度改稿检查 |
| `scripts/info_design_hints.py` | （共享脚本）信息设计提示 I1–I9，只供判断；`lint-wechat.py`、`de_ai_lint.py` 也会附带显示 |
| `scripts/scan_ai_flavor.py` | 中文去 AI 味打分入口：默认跑随包 `scan_ai_flavor_builtin.py`（词面分）；`$TOPMIND_AI_SCAN` 指向外部扫描脚本时转发过去；`--which` 查实际执行哪份 |
| `scripts/audit-provenance.py` | （共享脚本）**改稿保真审计**：双向逐段溯源（本稿→源稿 / 源稿→本稿），抓悄悄扩写与被落下的段。同构派生稿可用；全面重组时按主张与数字核对 |
| `scripts/wechat_paths.py` | 路径解析模块（被上面脚本导入）：不写死个人路径、类别编号与年份 |

```bash
# 路径解析：CLI --base / --workspace → env TOPMIND_WECHAT_BASE / TOPMIND_WORKSPACE；解析不到就报错
export TOPMIND_WORKSPACE=/path/to/workspace   # 推荐
python3 scripts/new-article.py --title "文章名"                 # → <专题>/文章名/文章名.md
python3 scripts/check_article.py <专题>/文章名/
python3 scripts/lint-wechat.py --input <专题>/文章名/文章名.md --fix
python3 scripts/scan_ai_flavor.py <专题>/文章名/文章名.md      # 诊断参考；不设定稿分数门槛
python3 scripts/md2wechat.py --input <专题>/文章名/文章名.md --embed-images   # 按需 → out/
python3 scripts/sync-status.py --set 定稿 <专题>/文章名 --apply  # 只改 frontmatter，目录名不变
```

细节见 [`references/workflow.md`](workflow.md) · [`references/known-pits.md`](known-pits.md)。

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

**回推规则**：notes 保持纯 Markdown（源稿本来就不用 `:::` 容器；旧交付包里的容器 / 徽章 / `==高亮==` 回推时去掉）；回推**务必带 `--assets`**（否则 GitHub 上 `images/` 死链）。命令串见 `references/workflow.md`「收尾」。

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

## 排版与导出（必读）

用户要公众号版时才跑（产物缺省进 `<文章名>/out/`，`--slug` 缺省文件名，`--asset-root` 缺省文章文件夹）：

```bash
python3 scripts/md2wechat.py --input <文章名>/<文章名>.md --embed-images --preview \
  [--theme assets/themes/minimal-ink.json]
# 旧交付包：--input <包>/公众号稿.md --out-dir <包> --slug <slug> --asset-root <素材根>
```

1. **永远 `--embed-images`**，否则粘贴丢图（相对路径被序列化成 file://）
   **图文预览（交付前必做）**：`--preview` 用无头 Chrome 把页面按手机宽度截成 `out/预览.png`；交付前自己先看一遍（图序、图注、列表、表格），交付说明里附上预览图。没有 Chrome 时脚本会提示，改用浏览器打开 HTML 自己看。
2. **图片 basename 一致（硬约束）**：正文引用名 = `images/` 目标名；禁止两套同名图共处
3. 合规自检出现 `✗` 改生成器，不要手改 HTML
4. **配图位置**：图片必须紧跟它证明的那段文字
   （最多隔一段）；改稿移动段落时图片行一起搬。构建后必跑：嵌入图数量=文档图数量、
   嵌入图顺序=文档出现顺序（逐张解码与源文件比对）；每张图前后 6 行做主题关键词
   邻近检查，不通过则人工核对。
5. **双版一致性校验**：同一选题出 X 版后，
   核对 X 与公众号内嵌图的内容、映射与顺序；有压缩、重采样或平台裁切时不要求字节或像素完全相同，实际内容差异需说明。
   两版都直接读同一份 `<文章名>.md` 的 `![]()`，禁止手工拼 `--images`
   （曾因文件名排序 ≠ 文档顺序，导致 X 版从某一节起整段配图错位）；`check_article.py` 校验编号跟出现顺序一致。

已知问题清单：[`references/known-pits.md`](known-pits.md)。

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
渲染规格见 [`references/element-spec.md`](element-spec.md) · 主题映射见 [`references/theme-map.md`](theme-map.md)。

**本包保守兼容策略**（平台行为变化时实际验证；详见 [`references/wechat-constraints.md`](wechat-constraints.md)）：禁 `div`/`pre`/`h1`/`figure`/`thead`/flex/float/gradient/shadow；表格 `table-layout` 不写 fixed；列数 ≥4 转卡片。

## 与 Desktop「公众号创作」

topmind Desktop 的「公众号创作」插件是本技能的可视化工作流伴面（若有）：包列表 → 改稿 → 三关 → 预览 → 导出。导出时它优先调用本技能的 `scripts/md2wechat.py`，脚本语义以本技能为准。本技能已取代 topmind-skills 包里旧的 `topmind-wechat`（4.15.2 起删除）。

## 外部依赖

无必需的外部技能。去 AI 味规则与检查随包自带（`references/core-voice.md`、`references/de-ai-rules.md`、`scripts/de_ai_lint.py`、`scripts/scan_ai_flavor.py`）；推荐同时安装 `topmind-revise` 执行质量三关，没装时按随包的 `references/revision-workflow.md` 手动走；
想接入自己的扫描脚本时设 `$TOPMIND_AI_SCAN=/path/to/script.py`，参数与退出码原样转发。
