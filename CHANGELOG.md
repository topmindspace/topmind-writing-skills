## [0.8.23] - 2026-10-08

> 根包 0.8.22 → **0.8.23**（patch）；各技能版本不变。0.8.22 已打 tag 但未生成 Release、未发布 npm，其全部内容随 0.8.23 一并发布（见下方 0.8.22 条目）。

> - 优化：**Release 打包不受运行时缓存影响**。`package_skill.py`（shared 真源 + 6 份副本）新增 `IGNORE_RES`，
>   `__pycache__/`、`*.pyc`、`*.pyo`、`.DS_Store` 在校验与打包时都直接跳过，不再判为「不应进包的文件」；
>   `scripts/_*`、`.env` 等仍按原规则拦截
> - 优化：`release.yml` 在 job 级设置 `PYTHONDONTWRITEBYTECODE=1`，负向测试运行脚本时不写字节码缓存，打包与 npm 包保持干净
> - 优化：CI `Skill package gates` 在负向测试之后追加「Release packaging check」，按 Release 同口径逐技能跑 `package_skill.py --check`，
>   打包问题在推送 main 时就能发现，不必等到打 tag

## [0.8.22] - 2026-10-08

> 根包 0.8.21 → **0.8.22**（patch）；技能各升 patch：topmind-wechat-post 0.3.0 → **0.3.1**、topmind-briefs 0.2.7 → **0.2.8**、
> topmind-x-article 0.4.7 → **0.4.8**、topmind-cover 0.4.1 → **0.4.2**、topmind-viral-posts 0.3.1 → **0.3.2**、topmind-poster 0.1.0 → **0.1.1**。

> - 特性支持：**公众号技能收为唯一真源**。topmind-skills 里的 `topmind-wechat` 并入 `topmind-wechat-post`（topmind-skills 4.15.2 起删除旧技能）：
>   - 新增 `scripts/audit-provenance.py`：改稿保真双向逐段溯源（本稿→源稿 / 源稿→本稿），有源稿时定稿必跑
>   - `scripts/scan_ai_flavor.py` 改为转发器：优先调用 qu-aiwei-zh 的 canonical 实现（含作者姿态分），
>     查找顺序 `$QU_AIWEI_SCAN` → 同级已装技能 → `$QU_AIWEI_SKILLS_DIRS` → 常见宿主技能目录，不写死个人路径；
>     找不到时回落内置 `scan_ai_flavor_builtin.py` 并在 stderr 提示缺姿态维度，`--require-canonical` 可强制要求
>   - `md2wechat.py` 两版逐段比对：本仓 1801 行版本已包含旧版全部能力，并多出括号 URL、嵌套围栏、行内图片管线、
>     原子写、坏输入干净报错等处理，保留本仓版本；旧版独有的左衬条样式、自我介绍签名行、minimal-ink 默认主题
>     是 2026-10-01/02 按用户要求去掉的，不恢复
>   - references 合入：`workflow.md` 补溯源审计步骤与 `word_count` 口径说明，`writing-quality.md` 补作者姿态分与清单文档误判说明
> - 优化：**去掉写死的路径、类别编号与年份**。新增 `scripts/wechat_paths.py`，`new-article / sync-status / sync-mapping / push-to-topstream`
>   共用：`--base` → `TOPMIND_WECHAT_BASE` → `--workspace` / `TOPMIND_WORKSPACE` 下按名称发现「长文」类别（兼容「创作」「专题」）
>   + `{当年}-公众号`；`TOPMIND_WECHAT_CATEGORY` / `TOPMIND_WECHAT_TOPIC` 可覆盖；解析不到就报错，不再回落 `~/TopWorkSpace/...`。
>   topstream 只认 `--topstream` / `TOPSTREAM_ROOT`；新建交付包的 frontmatter `category` / `topic` 取实际目录名
> - 优化：**共享文件单一真源**。新建 `shared/`（`audit_*.py`、`package_skill.py`、`md2wechat.py`、`md2x-html.py`、
>   `writing-principles.md`），`shared/manifest.json` 声明分发目标；`scripts/sync_shared.js` 同步副本，`--check` 在 CI、Release 与 `prepack` 里
>   校验逐字节一致。技能目录仍保留副本，单独安装照常可用
> - 特性支持：**frontmatter 符合 Agent Skills 规范**。6 个 SKILL.md 顶层只留 `name / description / license / metadata`，
>   `version / action_category / triggers / author / homepage / updated` 移入 `metadata`（字符串值），`triggers_cn` 并入
>   `metadata.triggers` 与 description 的 Use when；`agentskills validate` 6/6 通过，CI 新增校验步骤（skills-ref 0.1.1）。
>   `run_skill_gates.js`、安装器与 `audit_skill.py` 同时认 `metadata.version` / `metadata.triggers` 与旧的顶层写法
> - 优化：路由名称对齐。poster 的 `top-ppt-html` 改为 `topmind-presentation`；briefs 去掉未发布的 `topmind-x-posts`，
>   个人向/引流短帖改指 `topmind-viral-posts`；x-article 的短推文改指 viral-posts / briefs，发帖由 `topmind-x` 负责且须用户确认；
>   各技能 description 补齐互相的 Do NOT 边界（信息密度型 → briefs，引流互动型 → viral-posts）
> - 优化：**npm 包瘦身**。`package.json` `files` 排除 cover 单风格样张（`assets/examples/*.png`，保留 `overview.png`）与
>   `references/cover-study/*.png`；`npm pack --dry-run`：59.0 MB → 2.1 MB（解包 59.6 MB → 2.7 MB，179 → 121 个文件）。
>   完整样张仍在 git 仓库与 Release zip 中
> - 优化：wechat-post SKILL.md 里带日期的项目案例移到 `references/case-notes.md`，正文只留通用规则
> - 特性支持：新增 `evals/evals.json` 评测骨架（24 条，每个技能 3 条正例 + 1 条负例）与 `scripts/check_evals.js` 结构校验，尚未在真实宿主里执行
> - 其他：14 份 `docs/audit-2026-09-29*.md` 归档到 `docs/archive/audits/`；briefs 与 viral-posts 的负向测试不再依赖同级技能目录；
>   技能 package-lock.json 版本号与 package.json 对齐；README（中英）与 docs 的版本表、frontmatter 说明同步

## [0.8.21] - 2026-10-08

> 根包 0.8.20 → **0.8.21**（patch）；技能：topmind-briefs 0.2.6 → **0.2.7**（patch，交付脚本随包自带 + 篇幅口径统一）。

> - 优化 topmind-briefs 交付链路：`md2x-html.py`、`md2wechat.py` 随技能自带（`topmind-briefs/scripts/`），
>   单独安装 briefs 即可出 X 版与公众号版 HTML，不再依赖同级的 x-article / wechat-post 目录。
>   两个文件是上游真源的逐字节副本（与 `audit_*.py`、`writing-principles.md` 的全仓同步方式一致）
> - `negative_tests.py` 改为校验交付脚本随包存在，并在仓库内校验与上游逐字节一致，上游改动未同步时 CI 直接报出
> - SKILL.md / README（中英）/ platform-specs 的交付命令对齐脚本实际参数：`python3 scripts/...` 调用、
>   公众号版补 `--out-dir` / `--slug` / `--no-toc`，X 版统一用 `--images-from 公众号短文.md` 派生配图顺序
> - 公众号篇幅口径统一为 SKILL.md description 的「约 300–800 字」：style-guide 原「500 字内」改为同一口径；
>   README.en 的「words」改为「Chinese characters」；briefs `package.json` description 补全双平台口径
> - 版本同步：briefs SKILL.md / package.json / package-lock.json / README（中英）、根 README 技能表与安装器版本、
>   docs/PUBLISHING.md「当前线」按各技能现行版本更新
> - 实测（2026-10-08）：单独安装 briefs 后，用一篇真实公众号稿跑通双版 HTML，内嵌图数量、顺序与源图逐字节一致

## [0.8.20] - 2026-10-04

> 根包 0.8.19 → **0.8.20**（patch）；技能：新增 **topmind-poster 0.1.0**。

> - 新增 **topmind-poster**：HTML+CSS → 高清长图 / 海报 / 信息图 PNG（无头 Chrome 2× 截图 + 按背景色扫底自动裁白），
>   含「一段一图」分段图批量出图工作流（生成器 + 渲染器）
> - 新增 `scripts/render_poster.py`：一条命令跑完截图 → 扫底 → 裁切，支持批量、自动加大窗口重试、`--chrome` / `CHROME_PATH` 指定浏览器
> - 新增 `references/layout-recipes.md`：画布尺寸 / 字号层级 / 浅底深底配色 / 栅格 / 进度条 / 常用版式模板
> - 沉淀 7 个实测坑：macOS 沙箱下必须 `--no-sandbox`、柱状图填充整条消失（`<span>` 需 `display:block`）、
>   裁切基准色不能取左上角（顶部装饰层会污染）、PNG 重采样反而变大、`str.format()` 拼 CSS 报 KeyError 等
> - 定位说明：本技能只管**出图那一环**；封面走 `topmind-cover`，PPTX 走 `top-ppt-html`
> - README 技能表补齐 **topmind-viral-posts**（英文版此前缺）、校正各技能版本号与安装器版本

## [0.8.19] - 2026-10-03

> 根包 0.8.18 → **0.8.19**（patch）；技能：topmind-viral-posts 0.3.0 → **0.3.1**（patch，纯运营 7 型并入）。

> - topmind-viral-posts 新增 **8-14 型纯运营吸粉模板**（暴论型/数据晒单型/真诚交友型/吐槽共鸣型/干货技巧型/经验忠告型/执行清单型），基于 2026-10-03 用户提供的 10 张 X 爆款截图深度拆解
> - 新增 **Hashtag 矩阵**（#蓝V互关 #follow #真诚交友 #浇朋友 黄金组合）与 **黑话词典**（浇朋友/蓝朋友/出摊/串门/上岸）
> - 8-14 型为纯 X 运营/吸粉内容，不蹭新闻热点；双份真源合并，本地 skills/ 目录的 0.2.0 内容已并入正式仓库

## [0.8.18] - 2026-10-03

> 根包 0.8.17 → **0.8.18**（patch）；技能：topmind-wechat-post 0.3.1 → **0.3.2**（patch，衬条禁令铁律）。

> - design.md 设计要点新增 **禁止顶部/侧边衬条和颜色条铁律**（用户明确）：用浅色调色板区分区块，不用硬色条；MD3 真风格 = 浅色调色块 + 圆角 + 柔和阴影 + 标签药丸

## [0.8.17] - 2026-10-03

> 根包 0.8.16 → **0.8.17**（patch）；技能：topmind-wechat-post 0.3.0 → **0.3.1**（patch，MD3 卡片规范+去AI味补充）。

> - design.md 新增 **MD3 卡片规范**：禁止 matplotlib 做信息图，走 HTML+CSS → Playwright 截图 → PNG 路线；卡片不要衬条，表格式图表用浅色风格
> - writing-quality.md 事实关新增 **第三方图片核实三问**：数字是否过于整齐、时间是否对得上、总量是否对得上
> - writing-quality.md 文字关新增 **去AI味补充清单**（用户亲口）："不是…是…"对比句式、一句话总结、真正的、过度简洁、中立措辞

## [0.8.16] - 2026-10-03

> 根包 0.8.15 → **0.8.16**（patch）；技能：topmind-viral-posts 0.2.4 → **0.3.0**（minor，监控范围大扩张）。

> - 监控范围新增 5 类：AI 模型追踪（新模型/多模态/开源权重/部署教程）、
>   生图生视频（提示词/ComfyUI/模型对比）、工具技巧（ChatGPT/Claude/grok/豆包/Manus 等）、
>   优惠免费（云服务/AI 服务/订阅限免）、视觉灵感（热门奇特图片视频）。
> - 新增 4 种段子公式：新模型三行速报型、优惠实用型。

## [0.8.15] - 2026-10-03

> 根包 0.8.14 → **0.8.15**（patch）；技能：topmind-viral-posts 0.2.3 → **0.2.4**（patch，大 V 型公式）。

> - patterns.md 新增大 V 观点型两个子公式：观点摘抄+点评型、双方观点+站队型，附示例。

## [0.8.14] - 2026-10-03

> 根包 0.8.13 → **0.8.14**（patch）；技能：topmind-viral-posts 0.2.2 → **0.2.3**（patch，140 字铁律）。
>
> - 新增 **140 字生死线**铁律：X 时间线只显示前 280 字符（约 140 中文字），
>   钩子+核心事实+行动号召必须在前 140 字内；hashtag 放最后；
>   附字数检查方法与改写示例。

## [0.8.13] - 2026-10-03

> 根包 0.8.12 → **0.8.13**（patch）；技能：topmind-viral-posts 0.2.1 → **0.2.2**（patch，选题范围与时空锚点）。
>
> - 热点资讯型选题范围扩大：AI/科技/技能/工具/有趣科技/娱乐热点/社会新闻；
>   纯娱乐八卦选与科技圈/大众情绪相关的。
> - 新增时空锚点铁律：新闻资讯类正文必须带时间点或事件发生地点，
>   不许写"最近""某地"；附正反示例。

## [0.8.12] - 2026-10-03

> 根包 0.8.11 → **0.8.12**（patch）；技能：topmind-viral-posts 0.2.0 → **0.2.1**（patch，配图策略优化）。
>
> - 配图铁律重写：官方原图 > 第三方原图 > AI 生图；只有纯引流段子或无可用原图时才生图；
>   生图风格统一为清新优雅 / 商务美观 MD3 风（段子/短文/长文通用）。
> - 修复 SKILL.md 类型表新人报到型重复行。

## [0.8.11] - 2026-10-03

> 根包 0.8.10 → **0.8.11**（patch）；技能：topmind-viral-posts 0.1.0 → **0.2.0**（minor，新增第 7 类型）。
>
> - topmind-viral-posts 新增**热点资讯型**：AI/科技/技能/工具/八卦/传闻选题，
>   基于真实检索调研（至少 2 个独立来源交叉验证），段子/短文两种输出形态；
>   传闻标"未经证实"、厂商数据标"厂商口径"、推测与事实分开；
>   配图以官方原图/资讯截图优先，可多图（2-4 张）并注明来源。
> - README 技能表与类型说明同步更新。

## [0.8.10] - 2026-10-03

> 根包 0.8.9 → **0.8.10**（patch）；新增技能：topmind-viral-posts **0.1.0**。
>
> - 新增 topmind-viral-posts：X 引流段子/爆款短篇，基于中文区真实爆款帖提炼
>   6 大类型（干货忠告/互关求粉/自嘲幽默/互动提问/打卡日常/新人报到），
>   短句分行口语化带互动钩子；**每帖配 1 张图**（美女/宠物/风景/奇幻/标语
>   5 大图库，走 topmind-cover 出图，含配图公式）。
> - README：技能合集 4 → 5 个，技能一览表与仓库结构同步更新。

## [0.8.9] - 2026-10-02

> 根包 0.8.8 → **0.8.9**（patch；技能版本不变）。
>
> - 文档修正：writing-principles.md 第六节改为通用化表述——明确 topmind
>   目录规约（40-创作/88-发布）为默认值，可通过 `--base` /
>   `TOPMIND_WECHAT_BASE` / `TOPMIND_WORKSPACE` 覆盖；技能不强制依赖特定目录结构。

## [0.8.8] - 2026-10-02

> 根包 0.8.7 → **0.8.8**（patch）；技能：topmind-briefs 0.2.5 → **0.2.6**、
> topmind-x-article 0.4.6 → **0.4.7**（patch）、topmind-wechat-post 0.2.9 → **0.3.0**（minor，
> 新增工作区规约与交付标准章节）。
>
> - 全仓：writing-principles.md 新增第六/七/八节——工作区规约与交付标准
>   （40-创作/88-发布目录规约、云端备份、封面默认2版、双平台同步）、
>   研究深度要求（全面调研/多方综合/成稿核实）、表述偏好（无偏见、
>   涉中国厂商正面积极、敏感言论先讨论、信息汇总类图表优先）。

## [0.8.7] - 2026-10-02

> 根包 0.8.6 → **0.8.7**（patch）；技能：topmind-briefs 0.2.4 → **0.2.5**、
> topmind-x-article 0.4.5 → **0.4.6**、topmind-wechat-post 0.2.8 → **0.2.9**（patch）。
>
> - 全仓：writing-principles.md 第五节新增"很老"→"可以追溯很早之前"（用户亲口改稿）。

## [0.8.6] - 2026-10-02

> 根包 0.8.5 → **0.8.6**（patch）；技能：topmind-x-article 0.4.4 → **0.4.5**（patch）。
>
> - x-article：派生铁律补全容器转换（`::: pull/stat/tip` → X 兼容格式）。

## [0.8.5] - 2026-10-02

> 根包 0.8.4 → **0.8.5**（patch）；技能：topmind-wechat-post 0.2.7 → **0.2.8**（patch）。
>
> - wechat-post：图片去掉边框（MD3 优雅，只保留圆角）。

## [0.8.4] - 2026-10-02

> 根包 0.8.3 → **0.8.4**（patch）；技能：topmind-briefs 0.2.3 → **0.2.4**、
> topmind-x-article 0.4.3 → **0.4.4**、topmind-wechat-post 0.2.6 → **0.2.7**（patch）。
>
> - 全仓：writing-principles.md 编号修复（二点五 4→5→6），四处全量同步
>   （含第五节措辞偏好）。

## [0.8.3] - 2026-10-02

> 根包 0.8.2 → **0.8.3**（patch）；技能：topmind-wechat-post 0.2.5 → **0.2.6**、
> topmind-x-article 0.4.2 → **0.4.3**、topmind-cover 0.4.0 → **0.4.1**（均为 patch）。
>
> - wechat-post：`references/writing-principles.md` 新增第五节"措辞偏好"
>   （2026-10-02 用户亲手改稿确立：不用噱头式导语/"一句话"伪简洁/绝对化断言/
>   "我的判断"/"全文的题眼"/"同一份报告"/"坑"字/看不懂的梗；断言留余地、
>   简洁不取巧、评论腔删掉）；SKILL.md 实战沉淀追加 v2 措辞整改、PIL 结尾
>   总结插图做法、topmind-cover 封面流程
> - x-article：SKILL.md 新增"文本派生铁律"（`X长文.md` 由 `公众号稿.md` 去
>   frontmatter 派生，标题原样保留不重复加序号；曾出现"一、一、"重号 bug）
> - cover：风格转译器新增"清新震撼 → `white-clean`"映射；修正"19 选 1"→"22 选 1"
> - 文档卫生：根 README 技能一览表版本号全部对齐（wechat-post 0.2.0→0.2.6、
>   x-article 0.4.0→0.4.3、cover 0.3.4→0.4.1 且"11 风格"→"22 种风格"、
>   briefs 0.2.1→0.2.3、安装器 0.7.0→0.8.3）；各技能 README 中英文版版本号对齐；
>   `docs/PUBLISHING.md` 当前线更新

## [0.8.2] - 2026-10-02

> 根包 0.8.1 → **0.8.2**（patch）；技能：topmind-wechat-post 0.2.4 → **0.2.5**（patch）。
>
> - wechat-post：修 0.8.1 去衬条时遗留的 `%` 格式化参数错误（signature/toc/table_cards
>   三处多传 `theme["accent"]`，导致任何构建直接 TypeError 崩溃）；去衬条收尾：
>   callout 去左侧色条、金句去上下横线、mermaid 占位去顶条，全套 MD3 tonal 卡片
>   （无衬条，背景色调 + 大圆角区分层级）；标准表格表头去网格线，改 2px 蓝色底部分隔；
>   宽表转卡片标题改蓝色强调。
> - 全仓 writing-principles.md：卡片样式规则更新为"不用任何衬条"，表格浅色 + 蓝色强调。

## [0.8.1] - 2026-10-02

> 根包 0.8.0 → **0.8.1**（patch）；技能：topmind-wechat-post 0.2.3 → **0.2.4**（patch）。
>
> - wechat-post：卡片完全去衬条（无 border-left/border-top，纯背景+大圆角 MD3）；
>   表格改为浅色风格（表头浅蓝底+蓝色文字，单元格无边框线用底部分隔）。

## [0.8.0] - 2026-10-02

> 根包 0.7.9 → **0.8.0**（minor：cover 新增 3 种风格）；技能：topmind-cover 0.3.7 → **0.4.0**（minor）。
>
> - cover：新增 3 种风格（橙色暖阳 / 卡通素描 / 赛博霓虹），共 22 种；
>   新增 `references/typography-system.md`（字形/字号/高亮/衬条/装饰/透视）；
>   3 种新风格样张已生成，overview 更新为 22 风格版。

## [0.7.9] - 2026-10-02

> 根包 0.7.8 → **0.7.9**（patch）；技能：topmind-cover 0.3.6 → **0.3.7**、
> topmind-wechat-post 0.2.2 → **0.2.3**、topmind-x-article 0.4.1 → **0.4.2**、
> topmind-briefs 0.2.2 → **0.2.3**（patch）。
>
> - cover：MD3 设计基础（配色角色+字体层级+形状语言）；19 风格 MD3 化重生成；
>   设计哲学更新为"美观优雅的醒目"。
> - wechat-post：卡片去左侧条，改用横向线条（MD3 优雅）。
> - 全仓：writing-principles.md 新增"可视化优先"（表格>段落，列表>段落，图表>描述）。

## [0.7.8] - 2026-10-02

> 根包 0.7.7 → **0.7.8**（patch）；技能：topmind-cover 0.3.5 → **0.3.6**、
> topmind-wechat-post 0.2.1 → **0.2.2**、topmind-x-article 0.4.0 → **0.4.1**、
> topmind-briefs 0.2.1 → **0.2.2**（patch）。
>
> - cover：white-clean 4 版式总览图 + README 突出主风格。
> - 全仓：新增 `references/writing-principles.md`（精炼客观+素材优先+研究深度）；
>   briefs/x-article/wechat-post 三技能 SKILL.md 默认链接执行。

## [0.7.7] - 2026-10-02

> 根包 0.7.6 → **0.7.7**（patch）；技能：topmind-cover 0.3.4 → **0.3.5**、
> topmind-wechat-post 0.2.0 → **0.2.1**（patch）。
>
> - cover：修正倾斜滥用（条件触发+双行规范）、新增点题词高亮规范；
>   white-clean 新增 3 种版式示例（双行/左文右图/点题词高亮）。
> - wechat-post：默认主题切换为 MD3 商务蓝（#0B57D0，大圆角 16px，tonal 配色）。

## [0.7.6] - 2026-10-02

> 根包 0.7.5 → **0.7.6**（patch）；技能：topmind-cover 0.3.3 → **0.3.4**（patch）。
>
> - 新增"高级感设计系统"（字体/角度/景深/光影 4 维度）；SKILL.md 自检清单 11 项。
> - 19 风格示例图按高级感标准全量重生成；cover-prompts.md 新增第 6 章高级感增强指令。

## [0.7.5] - 2026-10-02

> 根包 0.7.4 → **0.7.5**（patch）；技能：topmind-cover 0.3.2 → **0.3.3**（patch）。
>
> - 19 风格示例图全量重生成（全新原创主题，与旧主题无重叠）。
> - 移除第三方参考图及"参考图复刻学习区"；技能内不再提及第三方来源。
> - cover-prompts.md：19 风格提示词安全区统一为 10%。

## [0.7.4] - 2026-10-01

> 根包 0.7.3 → **0.7.4**（patch）；技能：topmind-cover 0.3.1 → **0.3.2**（patch）。
>
> - cover 技能 11 → **19 种风格**：新增 chao-wan-3d / hard-core-type / dark-saas /
>   anime-desk / diorama-book / cinematic-flow / academic-print / gallery-grid
>  （完整配方 + 示例图）。
> - 新增 4 种构图骨架 + 文案排版密码章节；SKILL.md 加入风格转译器，安全区 5%→10%。
> - 两仓 cover 按新技能重生成（writing: chao-wan-3d / presentation: dark-saas）。

## [0.7.3] - 2026-10-01

> 根包 0.7.2 → **0.7.3**（patch）。white-clean 示例图按震撼升级包重生成
> （`assets/examples/white-clean.png` + 微信版中央裁剪）。

## [0.7.2] - 2026-10-01

> 根包 0.7.1 → **0.7.2**（patch）；技能：topmind-cover 0.3.0 → **0.3.1**（patch）。
>
> - topmind-cover 新增 **white-clean 震撼升级包**：前景压字（破框而出）、字体雕塑感、
>   纵深三层、体积光、对角线动能、撞色一处给足——白色清新从"好看"到"震撼"的 6 开关。
> - 两仓 README/落地页换上按 cover 技能配方新生成的白色清新 banner 封面（5:2）。

## [0.7.1] - 2026-10-01

> 根包 0.7.0 → **0.7.1**（patch）；技能：topmind-briefs 0.2.0 → **0.2.1**（patch，文档与去 AI 味优化）；
> topmind-cover / topmind-wechat-post / topmind-x-article 保持原版本（仅 repository.url 元数据变更）。
>
> 本轮为拆分与改名专版：
- 仓库由 `tms-skills` 改名为 **`topmind-writing-skills`**：
  npm 包 `@topmindspace/tms-skills` → `@topmindspace/topmind-writing-skills`，
  CLI `bin/tms-skills.js` → `bin/topmind-writing-skills.js`；
  根 `package.json` / 4 技能 `package.json` 的 `repository.url`、
  README 中英文 badge / 安装命令 / 技能表、PUBLISHING / ci.md、
  workflows、`ci_privacy_scan.py`、`ci_skill_gates.sh`（去掉 `--with-pptx` 分支）同步更新。
- **`top-ppt-html` 拆出为独立仓库 `topmind-presentation`**（技能改名 `topmind-presentation`）：
  技能文件、docs 下 ppt 专属页面（index/showcase/style-gallery、showcase/、site-assets/、
  industry-pptx-research.md）一并迁移；本仓删除 `top-ppt-html/` 目录；无引用 banner 图已删除。
- `topmind-cover/SKILL.md` 的报告封面指引改为走 `topmind-presentation`。
- 修 installer：`readSkillMeta` 支持 `>-` / `|` 块标量（`list` 对 briefs 曾显示 `>-…`）。
- deprecate 脚本指引文案指向新包名。

## [0.7.0] - 2026-10-01

> 根包 0.6.0 → **0.7.0**（minor，本轮是功能轮）；技能版本：topmind-x-article 0.3.0 → **0.4.0**、
> topmind-wechat-post 0.1.0 → **0.2.0**、topmind-briefs 0.1.0 → **0.2.0**；
> topmind-cover 保持 0.3.0、top-ppt-html 保持 0.2.1（无变更）。
> 注：0.6.0 发版时 x-article SKILL.md frontmatter 漏 bump（仍为 0.2.0），本轮一并纠正为 0.4.0。

### topmind-x-article 0.4.0（X 配图错位根治）

- `scripts/md2x-html.py` 新增 **`--images-from 公众号稿.md`**：从源 md 的 `![]()` 按文档顺序
  自动派生图片，**禁止手工拼 `--images` 顺序**。根因：旧构建按 `images/*` 文件名排序传入，
  而文件名数字顺序 ≠ 文档顺序（`14-kling`/`15-china-models` 建图顺序与文档相反；
  `21-codex`/`22-harness` 后加，排在 `16-openrouter` 之后），导致九月全景 X 版从第六节起整段配图错位
- 脚本内置校验：`[图N]` 必须连续编号且数量 = 图片数，否则直接报错退出（不静默生成错版）
- SKILL.md：工作流改用 `--images-from`；新增"错位症状 B"根因记录；补事实铁律/文字铁律/交付铁律；
  README 中英、references/x-html-format.md 同步

### topmind-wechat-post 0.2.0

- 签名区去掉"我是 {{作者名}}，{{一句话简介}}"自我介绍行，只保留三连 CTA（兼容旧参数）
- 新增**双版一致性校验**：同一选题出 X 版后，必跑 X 内嵌图序列 vs 公众号内嵌图序列逐字节比对
- 新增**交付铁律**：发布/分享用交付包 HTML 原文件原样呈现，不临时重生成；`公众号稿.md` 唯一改稿入口
- 三个写作技能统一**语言铁律**：默认中文写作，只有用户明确要求英文才用英文

### topmind-briefs 0.2.0

- 工作流改用 `--images-from 公众号短文.md` 派生图片顺序（同 x-article 根治方案）
- 构建后校验加：X 版内嵌图序列（无封面）与公众号版逐字节一致
- 新增交付铁律；语言铁律同步

### 文档与元数据

- 根 README 中英：技能表（x-article 0.4.0、wechat-post 0.2.0、briefs 0.2.0）、安装器版本 0.7.0、钉版本示例 `@0.7.0`
- 各技能 README 中英「同 tag」引用全部 → `@topmindspace/tms-skills@0.7.0`
- `docs/PUBLISHING.md`：当前线更新为 0.7.0

## [0.6.0] - 2026-09-30

> 根包 0.5.0 → **0.6.0**（minor，本轮是功能轮）；技能版本：topmind-cover 0.2.0 → **0.3.0**、
> topmind-x-article 0.2.0 → **0.3.0**、topmind-wechat-post 保持 0.1.0（无变更）、
> top-ppt-html 保持 0.2.1（无变更）。

### topmind-cover 0.3.0（X 封面主尺寸改为 5:2）

- X Article 封面主尺寸从 1200×675（16:9）改为 **1500×600（5:2）**：SKILL.md 尺寸表、
  流程步骤（横构图 5:2）、`scripts/crop-cover.py`、`scripts/negative_tests.py` 全量对齐
- topmind-x-article README 中英封面引用同步为 `cover-1500x600.png` / 1500×600
- `assets/examples/` 旧样张仍为 16:9 版，README 已明确标注"旧版、仅供风格参考"，不重制

### topmind-x-article 0.3.0（图片点击放大 lightbox）

- `scripts/md2x-html.py`：正文图与封面预览新增 lightbox——点击放大看原图，
  支持新标签页打开原图 / 下载原图，Esc / 点背景 / 关闭按钮退出；**不屏蔽右键**
  （`oncontextmenu` 未添加），放大后可右键另存或直接截图
- 加固：嵌套代码围栏（四反引号开栏）不会被内部三反引号提前关闭；未闭合围栏文末自动收尾；
  标题从 frontmatter 之后的首个一级标题提取；图片/封面缺失时干净报错
- 技能 README 中英补 lightbox 说明

### 文档与元数据

- 根 README 中英：技能表（x-article 0.3.0、cover 0.3.0 + 新描述）、安装器版本 0.6.0、钉版本示例 `@0.6.0`
- 四技能 README 中英「同 tag」引用全部 → `@topmindspace/tms-skills@0.6.0`
- `docs/PUBLISHING.md`：当前线（安装器 0.6.0、cover 0.3.0、x-article 0.3.0）与整仓同 tag 示例 v0.6.0

## [0.5.0] - 2026-09-29

> 根包 0.4.1 → **0.5.0**（minor，本轮是功能轮）；技能版本：topmind-x-article 0.1.0 → **0.2.0**、
> topmind-cover 保持 0.2.0（纯文档新增）、topmind-wechat-post 保持 0.1.0（纯文档）、top-ppt-html 保持 0.2.1（无变更）。

### topmind-x-article 0.2.0（新功能：HTML 一键复制发布链路）

- 新增 `scripts/md2x-html.py`：原稿 → 单文件 HTML（内联样式 + 配图 base64 内嵌 +
  页顶「一键复制全文」+ 每图 `[图N]` 编号/下载按钮 + 每提示词块「复制提示词」按钮 + 封面仅预览/下载）
- 按 X 编辑器真实语法重写（v3）：提示词块改 `<blockquote>`（X 不识别粘贴的 `<pre>` 为代码块，
  原生代码块只能走 Insert 菜单）；`#` 标题不进剪贴板（手动填 X 标题栏）；复制前 JS 自动剥离按钮/UI；
  GFM 表格转列表（X 粘贴丢弃 `<table>`）；新增有序列表、裸链接转超链接
- 提示词复制双通道文档：作者侧用 HTML「复制提示词」按钮（发布前取用文本）；
  读者侧一键复制必须转为 X 原生 Code 块（Insert → Code 手动逐块转换，原生代码块带 native copy button）
- README 中英重写用法（HTML 首选、txt 兜底）

### topmind-cover（文档，保持 0.2.0）

- 新增 `references/cover-prompts.md`（436 行）：11 风格可直接拷贝的中文提示词手册 +
  参考图复刻学习区（设计语言拆解 + 学习版提示词 + 原创红线）+ 外部调研
  （小红书六大高互动类型各 1 条、YouTube 高 CTR 范式、公众号/X 规则，8 个来源链接）+
  14 种内容类型场景组合推荐表 + 通用负面提示词中英 + 变量速查表

### topmind-wechat-post（文档，保持 0.1.0）

- `references/wechat-constraints.md`：已发布正文不可能保留 JS 复制按钮（JS 被剥离，
  第三方排版器的复制按钮只存在于其本地预览页）；代码围栏只负责高亮/折行/可读性，
  不得在正文中承诺「一键复制」；需复制即用走评论区置顶/附件/小程序文档等站外链路

### 文档与元数据

- 根 README 中英：技能表（x-article 0.2.0 + 新描述）、安装器版本 0.5.0、钉版本示例 `@0.5.0`
- 四技能 README 中英「同 tag」引用全部 → `@topmindspace/tms-skills@0.5.0`
- `docs/PUBLISHING.md`：当前线（安装器 0.5.0、x-article 0.2.0）与整仓同 tag 示例 v0.5.0

## [0.4.1] - 2026-09-29

> **本版备发**（tag v0.4.1 待打；npm 待发布；commit = 本轮审计报告落盘时的 `git log` 首条）。
> 根包 0.4.0 → **0.4.1**（patch）；技能版本：top-ppt-html 0.2.0 → **0.2.1**（修技能数据 bug 则 patch）、
> topmind-cover 保持 0.2.0（仅换样张图+描述文案，无功能变更）、topmind-wechat-post / topmind-x-article 保持 0.1.0。
> 本轮是第十三轮集成轮（A 文档抛光 + B 示例与描述 + C 新代码复审），改动最小、无新功能。
> 另含第十四轮集成轮（wechat-post/x-article 真 bug 修复 + installer 测试扩展）：**不 bump 版本**，全部并入 0.4.1。

### 安装器 bug 修复（高危 · Worker C 复审发现）

- `uninstall`/`install` 的 `assertDestOutsideSource` 守卫被符号链接绕过：`path.resolve` 不解析软链，
  `--to <软链指向包根>` 会跟随链接 `rmSync` 删掉包内技能源目录（已实测验证旧代码确会删源）
- 修复：`bin/tms-skills.js` 改用 `realpath` 归一化比对（`realOrResolved()`：dest 不存在时向上找最深存在祖先），+25/−4
- `scripts/test_installer_cli.js` 新增 case11/case12（uninstall/install 经软链指包根 → 拒绝、源目录完好），12 用例全过

### top-ppt-html 0.2.1（Worker C 复审发现 · 低危数据 bug）

- `assets/icons/index.json`：「组织」图标关键词含裸「架构」，会把「系统架构」类标题配上人物组织图 → 已收窄为「组织架构」

### 文档抛光（Worker A）

- topmind-cover/SKILL.md：冲击力自检清单 10→9（合并逐字正确项）、设计铁律去重
- impact-language.md：删除与 cover-styles.md 重复的「白色清新」章节（只在 cover-styles 保留，出处回指用户参考图）
- 根 README 中英：封面技能描述 8 种风格 → 11 种；top-ppt-html README 中英版本口径改为与 `@topmindspace/tms-skills@0.4.1` 同 tag

### 示例与描述（Worker B）

- `white-clean-alt.png`（white-clean-2）已重生成：标题「极简收纳全攻略」摆正、逐字正确；配套
  `white-clean-alt-wechat.png`（900×383）新增落盘并纳入 git；示例目录 README 计数同步为 26 张
- 4 处 description 更新（cover package.json + SKILL frontmatter 加「11 种风格模板」；ppt-html package.json + SKILL frontmatter 加「48 图标 + 弹性版式」）；overview alt 文案 8→11
- cover 安装文案复核：`list` 输出已准确，未动安装器

### 第十四轮集成（Worker A/B/C）——不 bump 版本，全部并入 0.4.1

- **topmind-wechat-post 修 6 真 bug**（`scripts/md2wechat.py`，Worker A 专审发现）：
  - yaml/diff 代码块高亮正则在分支内误用 `(?m)` → `re.error` 崩溃（编译期统一 `re.M|re.S`，分支内去掉）
  - URL 含平衡括号被截断 → 新增括号嵌套匹配扫描器替代旧正则
  - `[文字](url "title")` 带 title 链接认不出 → 链接解析支持 title
  - 脚注 URL 的 `&` 被转义两次 → 修正转义顺序
  - 坏主题 JSON 的 Traceback → 干净报错；目录当输入的报错文案修正
  - 嵌套围栏被提前闭合 → 围栏匹配支持嵌套
  - `scripts/negative_tests.py` 新增 6 个 case，15/15 绿
- **topmind-x-article 修嵌套围栏**（`scripts/md2x.py`，Worker A 专审发现）；
  `scripts/negative_tests.py` 新增 2 个 case，8/8 绿
- **installer 回归测试扩展**（Worker C）：`scripts/test_installer_cli.js` 新增 case13–22，
  覆盖 symlink 守卫纵深（realpath 归一化）与 installer 回归，72 断言全绿；`bin/` 未动，无真实绕过
- **分发体积与性能**（Worker B）：无真问题。0.4.1 tarball 解包 29.1MB（0.3.9 18.4MB，
  +10.7MB 系封面示例画廊预期增量）；top10 大文件全合法素材；48 图标 PNG 最大 27.4KB 无异常；
  install 耗时 0.3s 不需优化；`sync_npm_files.js --check` 通过
- 技能版本号保持：wechat-post / x-article 保持 0.1.0（纯 bug 修复按技能版本规则不 bump）；
  cover 保持 0.2.0、ppt-html 保持 0.2.1、根包保持 0.4.1

## [0.4.0] - 2026-09-29

> **本版备发**（tag v0.4.0 待打；npm 待发布；commit = 本轮审计报告落盘时的 `git log` 首条）。
> 根包 0.3.9 → **0.4.0**（minor，本轮是功能轮）；技能版本：top-ppt-html 0.1.19 → **0.2.0**、topmind-cover 0.1.0 → **0.2.0**、topmind-wechat-post / topmind-x-article 保持 0.1.0。
> 本轮是"对标业界+浅色封面+图标包版式"的功能轮（第十二轮）。

### 安装器（Worker A）

- 新增 `uninstall <id> [--to]` 命令：卸载已安装技能，`--to` 指向文件/缺目录时干净报错 exit 1
- `install` 已装版本感知：已装同版本拒绝安装并给出三行摘要（当前版本/来源/提示 uninstall 或覆盖），不再静默覆盖
- `scripts/test_installer_cli.js`：10 用例 38 断言，覆盖 install/uninstall/list/负向输入
- `--help` 更新、根 README.md/README.en.md 安装章节重写（`github:` 口径、钉版本示例同步 0.4.0）
- `.github/workflows/ci.yml` 新增 "Installer CLI tests" step

### topmind-cover 0.2.0（Worker B）

- 新增 3 个浅色风格：`white-clean`（排第一，标题冲击目标 1/3 字高）、`bg-blur`（背景虚化突出前景）、`paper-collage`（纸拼贴质感）
- `cover-styles.md` 11 风格重排为浅色优先；`impact-language.md` 补条目；SKILL.md 新增"直出/讨论"决策流
- 6 张新风格样张 + `overview.png` 重建；`references/ref-white-clean-1/2.png` 新增参考图

### top-ppt-html 0.2.0（Worker C）

- 内置原创图标包 `assets/icons/`：48 SVG + 48 PNG + `index.json` 映射，7 个默认图标兜底；`scripts/check_icons.py`（`--strict`）做图标一致性门禁；`references/icons.md` 文档化
- 3 种 layout variant：bento-grid / timeline / 2-col-feature（`references/layout-variants.md`）；`references/style-pack.md` 风格包文档化
- `validate_report.py` 新增内容覆盖率检查（<95% WARN）；随门禁修复 6 个真实丢字 bug
- `scripts/layout-constants.json` 加 adaptiveText 弹性文本规则；HTML/PPTX 弹性适配减少溢出截断

## [0.3.9] - 2026-09-29

> **本版备发**（tag v0.3.9 待打；npm 待发布；commit = 本轮审计报告落盘时的 `git log` 首条）。
> 注：0.3.7、0.3.8 未发布，全部内容已并入本版。
> 根包 0.3.8 → **0.3.9**（patch）；4 个技能 `version` 保持不动（top-ppt-html 0.1.19，其余 0.1.0）。
> 本轮是"新鲜眼睛"横扫（第十一轮）：只找前十轮没覆盖的盲区，改动最小。

### 代码异味横扫（第十一轮 Worker A）

- TODO 注释 6 命中 → 0 真遗留（均为有意为之：文档纪律说明/scaffold 指导注释/校验正则/示例代称）
- 死代码：全仓 Python + top-ppt-html JS 逐函数交叉 grep，零死函数；12 个 CLI 参数逐个验证全部在用
- 跨技能一致性修复：19 处错误信息半角冒号 `错误:` → 全角 `错误：`（多数派 47 处）；`validate_report.py` 加 `-h/--help` 早退（exit 0），与其他 argparse CLI 一致
- 重复逻辑（仅记录，不重构）：`esc()` HTML 转义三处逐字相同、`read_frontmatter()` 跨技能同构、`load_constants()` 各自实现——均为四技能同构门禁的有意设计

### 对抗输入测试（第十一轮 Worker B：5 真崩溃全部修复）

- `bin/tms-skills.js`：`--to` 指向已存在文件时 `mkdirSync` 抛未捕获堆栈 → try/catch 干净报错 exit 1
- `md2wechat.py`：`resolve_image` 的 `shutil.copy2`/`os.makedirs` 未捕获 OSError（磁盘满/目录当图片）→ 干净报错 exit 1
- `md2x.py`：输出写入 `mkdir`+`write_text` 未捕获 OSError → 干净报错 exit 1；目录当输入的报错文案修正（"找不到输入文件"→"输入是目录不是文件"）
- `crop-cover.py`：`out_dir.mkdir` 与渲染循环 `out.save` 未捕获 OSError（磁盘满→截断 PNG）→ 干净报错 exit 1
- 对抗矩阵：100KB 单行/emoji+零宽+混合换行/非法 UTF-8/空文件/纯标题/48MB 图片，其余全部干净通过

### 文档一致性（第十一轮 Worker C）

- 审计结论抽查 5 处全部为真（architecture 归一化/SKILL.md 13KB 预算/cover 触发词/ip-fun 原位垫色块补丁/footer 移出 content 标记）
- SKILL.md vs --help 漂移修复 1 处：wechat-post SKILL.md 注释声称 `--workspace` 参数，全仓无此参数 → 改为 `--base`
- README 示例 10/10 实跑通过（/tmp 干净目录，本地包安装）

## [0.3.8] - 2026-09-29

> **本版未发布**（未打 tag、未推 npm；0.3.8 全部内容已并入 0.3.9）。
> 根包 0.3.6 → **0.3.8**（patch）；4 个技能 `version` 保持不动（top-ppt-html 0.1.19，其余 0.1.0）。
> 本轮只动 top-ppt-html + 文档：渲染产出目检修复（A）+ PPTX 双引擎保真修复 11 bug（B）+ 文档修正（C）。

### 模板 footer 修复（第十轮 Worker A：渲染产出目检）

- `top-ppt-html/assets/templates/{presentation,research,architecture}.html`：`<footer>` 移出 `__TOPPPT_CONTENT_START__`/`__TOPPPT_CONTENT_END__` 标记之外——此前自动渲染取 content 区间时会连带删除页脚，目检确认已修复。

### PPTX 双引擎保真修复（第十轮 Worker B：PPTX 实检，11 bug 全部像素复验）

- `top-ppt-html/scripts/build_pptx.js` + `assets/pptx-export.js`（双端同规则）：
  - 图表数据标签小数位：按模型数值实际小数位（上限 2 位）生成 format code，修复小数标签被截断
  - hbar 条形图：类目轴自下而上绘制，反转数据使首项居顶；单系列颜色按数据点分配（跟随数据归属，与 A 通道一致）
  - streamgraph 退化：相邻 ribbon quad 沿走向微叠 0.02in，消除拼接处抗锯齿发丝缝
  - boxplot：min 标签默认移到须线帽下方，不再被组标签带压住叠印
  - marimekko：单元格归一化兼容裸数值或 `[标签,数值]` 对（裸数值沿用旧行为），修复 NaN 崩坏
  - pyramid：标题列宽按层内宽比例（labelFrac≈0.3）分配，顶层窄时改单框混排，修复窄层标题/说明叠印
  - KPI：第 4 个起的支撑指标不再静默截断——容量按最小允许行高计算、行高按全部指标自适应压缩，超容显式告警
  - donut 图例：百分比列 x（`donut.legendPctX` 5.3 → 10.8）右移，修复图例数值被圆环覆盖
  - table：内容高度逐格预估、超高全表收字号，字号触底仍装不下则显式告警（不再撑高行压脚注）
  - exhibit 徽标：纯编号自动补 `Exhibit ` 前缀（与 HTML 视觉一致），已带前缀的不重复
  - sankey/streamgraph note：note 与 footnote 均参与 `chartBottom` 结算，修复 note 重叠
- `top-ppt-html/scripts/layout-constants.json`：`donut.legendPctX` 5.3 → 10.8（单源），已由 `sync_runtime.py` 同步至 `pptx-export.js`、画廊、`templates/*.html`、示例的内联副本与 `__TOPPPT_RUNTIME_SHA__` 戳

### 文档修正（第十轮 Worker C）

- 根 README（中英）：当前线 0.2.x → 0.3.x；`topmind-cover` "17 张双尺寸" → "16 张双尺寸 + 1 张风格总览图"
- `docs/PUBLISHING.md`：`latest` 指向 0.3.1 → 0.3.6
- `topmind-wechat-post/README`（中英）：二级标题编号示例 `01` → `1`

## [0.3.7] - 2026-09-29

> **本版未发布**（未打 tag、未推 npm；0.3.7 全部内容已并入 0.3.8）。
> 根包 0.3.6 → **0.3.7**（patch）；4 个技能 `version` 保持不动（top-ppt-html 0.1.19，其余 0.1.0）。
> 本轮只动 topmind-cover：文字排印与装饰系统（第九轮）。

### 文字排印与装饰系统（第九轮）

- `topmind-cover/references/impact-language.md`：新增第七节"文字装饰系统"（+38 行）：6 种可靠装饰（关键词变色/字号对比/色块衬底/轻微阴影立体/手绘划线圈注箭头/小元素旋转≤8°）各给效果/风险/适用风格/提示词写法四列 + 8 风格各 2~3 种必用装饰指定 + 7 条装饰禁令（禁大标题透视/一句话超 3 色/三重叠加/竖排+旋转/色块吞字/装饰压笔画/装饰超量）
- `topmind-cover/references/cover-styles.md`（316→359 行）：8 风格提示词新增"文字特效"段（中英双语，全部含色号与量化参数，如"钩子词放大 1.5 倍""色块高 1.2 倍字高""投影偏移 1/10 字高"）；各风格"绝不"清单追加装饰禁令；news-flash 单色铁律放宽为"纯黑打底+爆点词朱红点睛"（仍 ≤3 色，与参考图布局/配色/文字结构全错开）；brand-launch 品牌词发光描边改为荧光绿块衬底
- `topmind-cover/SKILL.md`（114→116 行）：冲击力自检清单追加第 9/10 条——中文逐字正确（装饰未导致错字/乱码/笔画粘连）、装饰手法 ≤ 该风格指定数量（minimal 只许 1 种）；"必过 8 项"同步为"必过 10 项"
- 16 张样张全部重生成（标题沿用第八轮）：三重目检通过——中文逐字正确（装饰是错字重灾区，逐字核对）、每张 ≥2 种装饰生效且不乱（minimal 仅 1 种）、与 7 张参考图无实质相似；返工 1 次（magazine 首版比例错误）

## [0.3.6] - 2026-09-29

> **本版已发布**（commit 5dc0bb8，tag v0.3.6，GitHub Release + npm @0.3.6，latest 已切换）。
> 根包 0.3.5 → **0.3.6**（patch）；4 个技能 `version` 保持不动（top-ppt-html 0.1.19，其余 0.1.0）。
> 本轮只动 topmind-cover：冲击力升级（第八轮）。

### 冲击力升级（第八轮）

- 新增 `topmind-cover/references/impact-language.md`：从 7 张爆款参考图拆解的 20 条冲击力设计语言（字体/色彩/构图/信息层级/质感）+ 8 条保守陷阱；只沉淀抽象原则，不涉及任何参考图的具体版式
- `topmind-cover/references/cover-styles.md`：8 风格提示词配方全部重写为四要素结构（字体量级/配色系统/构图能量/质感细节），每风格新增标题文案提炼公式 + 5 条"绝不"清单；经红线自查（round5 差异审查表）无复现
- `topmind-cover/SKILL.md`：工作流新增"标题提炼 → 构图简报 → 生成 → 冲击力自检"（96→114 行）；新增 8 条目冲击力自检清单（3 秒测试/字高 ≥1/4/对比果断/记忆点/质感/逐字正确/中央 60% 安全区），不通过最多重生成 3 次
- 16 张样张全部重生成：8 个新标题（实测30款全翻车/快，就是慢/破晓 6.0：快四倍/从零到上线/21天爆单挑战/本周AI大事/慢食三餐/主编：流量是毒药）；双重目检（vs 参考图无实质相似、vs 旧 16 张全部明显更强）；中文逐字正确、无乱码
- README（中英）用法同步为 7 步 + 自检清单入口

## [0.3.5] - 2026-09-29

> **本版已发布**（commit 9ef7324，tag v0.3.5，GitHub Release + npm @0.3.5，latest 已切换）。
> 根包 0.3.4 → **0.3.5**（patch）；4 个技能 `version` 保持不动（top-ppt-html 0.1.19，其余 0.1.0）。
> 注：0.3.2、0.3.3、0.3.4 均未发布，全部内容已并入本版。

### 性能实测与优化（第七轮 Worker 4）

- **实测基线**（中等规模真实输入）：`md2x.py` 300KB/8814 行 0.33s；`md2wechat.py` 218KB/3219 行/
  80 图 0.42s（`--embed-images` 0.47s）；`crop-cover.py` 4000×2250 主图 1.79s；
  安装器 `install`/`list` 均 <0.5s（含 7.9MB 的 top-ppt-html）。
- **修 5 处 low-hanging fruit**（输出逐字节一致，已 diff 验证，无行为改动）：
  - `md2wechat.py audit_inline()`：8 次全正文 `re.search` 合并为一次预编译单遍扫描
    （原为大正文耗时的 ~47%，cProfile 实测）；
  - `md2wechat.py render_inline()`：10 个行内模式预编译到模块级
    （原每行 10 次 `re` 字符串模式缓存查找，666k 行调用时 667 万次）；
  - `md2wechat.py highlight()`：语言联合正则按语言缓存（原每代码块重编译一次）；
  - `md2wechat.py link_repl()`：脚注 url→序号改字典索引（原每链接两次全表扫描，O(n²)→O(n)）；
  - `md2x.py _inline()`：同理预编译全部行内模式。
- **实测提升**（交错对比，user CPU 时间）：md2wechat 11MB 输入 13.8s → 10.0s（-27%）；
  md2x 49MB 输入 62.5s → 42.2s（-32%）；300KB 输入 md2x 0.33s → 0.29s。
  crop-cover（PIL 解码/resize 主导）与安装器（node 启动 + 文件拷贝主导）无冗余工作，未改动。

### 可靠性矩阵（第七轮 Worker 4：三个技能 + 安装器）

- **修 2 个明确 bug**：
  - `md2x.py` / `md2wechat.py` 非法 UTF-8 输入原抛 `UnicodeDecodeError` Traceback，
    现干净报错（非零退出、无 Traceback）；读取期 `OSError`（如权限不足）同理。
  - `md2wechat.py` 交付物写入改原子写（临时文件 + `os.replace`）：磁盘满等中途失败时
    不再留下半截 HTML/清单（实测大文件写盘失败曾留下截断 HTML）。
- 矩阵其余项全部干净（非零退出、无 Traceback、无半截输出）：空文件、49MB 超大文件、
  特殊字符文件名（空格/引号/中文）、图片缺失（含 `--embed-images` 的"未内嵌"提示）、
  非图片/0 字节/缺失输入、缺 Pillow 干净提示、非法 skill id、装进技能源目录树被拒、
  未知命令/缺参数。
- 安装器经确认零网络调用（纯 `fs`/`path`），本地安装天然离线可用；断网仅影响
  `npx github:` 拉取，属 npm 侧报错，非本仓库代码路径。

### 发版准备 0.3.5

- 根 `package.json` 0.3.4 → **0.3.5**；9 处版本引用同步（根 README 中英钉版本示例、
  `docs/PUBLISHING.md` 当前线与版本策略、6 份技能 README 的"同 tag"行）；4 技能各自
  `version` 不动。
- 待办：`top-ppt-html/README{,.en}.md` 的 3 处 `@0.3.4` 引用由其审核 worker 同步
  （本轮未动 `top-ppt-html/` 目录）。

### 全门禁（第七轮 Worker 4，改完后跑）

- `ci_privacy_scan.py` PASS（200 文件）；`sync_npm_files.js --check` PASS；
  `ci_skill_gates.sh --with-pptx` 全绿；4 技能 `negative_tests.py` 全部通过；
  `run_skill_gates.js versions` PASS；`test_install_guards.js` 全部通过。

## [0.3.4] - 2026-09-29

> **本版备发中**（未 push、未打 tag、npm 无此版本）。
> 根包 0.3.3 → **0.3.4**（patch）；4 个技能 `version` 保持不动（top-ppt-html 0.1.19，其余 0.1.0）。
> 注：0.3.2、0.3.3 均未发布，全部内容已并入本版。

### top-ppt-html：全面审查 + 必要优化（第六轮）

- **渲染管线实跑**：虚构测试稿走完 render → hydrate_charts → data URI 内联 → validate --strict
  （95 PASS / 0 WARN / 0 FAIL）；故意注入 3 类缺陷（超大图片、布局溢出、空 alt）全部被抓；
  PPTX 11 slides 实跑，16:9、微软雅黑、中文原生文本、原生图表，strict 0 error / 0 warning；
  ELEMENT_OVERLAP / LAYOUT_FILL 门禁经真实 PPTX 注入验证有效。
- **build_pptx.js 修 6 处**：KPI 竖分隔线越过注释带、KPI/donut/image 页 `sec.points` 被丢弃、
  image 页图片底边越过注释带、cards 要点无脑 shrink 被 TEXT_OVERFLOW 抓、
  points 纯字符串/`{t,d}` 形态渲染为空或 `[object Object]`。
- **hydrate_charts.py**：空 labels/values、非数字 values、长度不一致原抛 Traceback，
  现干净报错（`ChartDataError`，带 section 定位），禁静默截断。
- **validate_report.py 修 2 处**：`alt=""` 视同缺失；图片体积按 data URI **解码后字节数**计量
  （原按标签字符串长度，属 bug；级别保持 WARN，strict 已拦截）。
- **SKILL.md/文档**：修 `（=?）` 编辑残留；README（中英）补 3 分钟最小示例；
  修 13 处死引用（错乱脚本路径、`docs/archive/…` 改 `../docs/archive/…` 等）；
  9 风格抽 3 套（品牌红/靛紫/光谱彩色）实跑渲染全部成功。
- 零用户可见行为改动。遗留候选：render_from_model 不同步 style/theme（需产品决策）、
  超长中文图表标签不截断、图片超限 WARN 不升级 FAIL、代码块页型缺失。

### 全仓横扫（第六轮）

- **修真 bug**：第五轮重写 `topmind-cover/references/cover-styles.md` 时把截断输出写进文件
  （ip-fun 尾部丢失、news-flash/minimal/magazine 三节整节丢失），已按审计文档+样张实物补齐。
- **docs/PUBLISHING.md**：补 HTTPS+PAT 推送方式（SSH 隧道被代理墙掐断后的实际走法；
  GitHub git 接口不认 Bearer 只认 Basic）、tag↔package.json 校验、NPM_TOKEN/E409 加固的文档记载。
- 三个新技能 README（中英）补版本号行；根 README.en 示例图体积与实测对齐（~8.9MB）。
- 四技能 description 触发边界复核：互不重叠、无真空（"X 长文封面"良性重叠已写清委托关系）。
- 隐私扫描 PASS（199 文件）；安装器四技能回归全过。

## [0.3.3] - 2026-09-29

> **本版未发布**（备发中：未 push、未打 tag、npm 无此版本）。
> 根包 0.3.2 → **0.3.3**（patch）；4 个技能 `version` 保持不动（top-ppt-html 0.1.19，其余 0.1.0）。
> 注：0.3.2 未发布，已并入本版。

### topmind-cover：6 张样张版式级重设计（差异化纠偏）

- 用户指出第四轮样张仍是"翻版"（版式结构照搬 7 张参考封面，只换文案形象）。
  本轮按**版式级标准**重做：只保留抽象原则（标题是视觉重心/信息分层/留白呼吸感），
  6 张重设计（gan-huo 居中构图+深炭灰暖橙、big-type 单行超大书法字+奶油亮底、
  brand-launch 深海军蓝+荧光绿、tutorial-steps 横向时间线+墨色题字、
  ip-fun 数字改右下角印章+橙黄暖色、news-flash 纯黑单色+纸纹+俯视静物大改），
  2 张保留微调（minimal「慢思考」、magazine「创造者访谈」）。
- 8 张主配色互不相同，且不与 7 张参考图主配色（浅蓝/黑红/粉紫/红白/蓝白）撞车；
  每张过双重目检（中文正确性 + 路人测试：描述画面后追问"像哪张参考图"，答不出才算过）。
- `references/cover-styles.md`：设计语言收紧为抽象原则，删除"左文右图""底部标签条"等
  具体版式描述；**原创铁律升级**：版式与配色也不得与第三方封面构成实质相似，
  只学原则不学版式。

### topmind-wechat-post / topmind-x-article：第二轮深审（质量）

- wechat-post：修 5 处文档与实现/规范打架（`---` 渲染文档落后于实现、主题表 genre 漏项、
  最小示例缺放图前置步骤、`--link-mode note` 档无文档、加粗密度两份规范打架按 lint 对齐）；
  零行为改动。遗留 3 个需改行为候选：缺图是否进合规自检、border-radius WARN 去噪、
  h2 序号剥离残留标点。
- x-article：文档×脚本 14/14 规则实测一致；补 x-format.md 4 处"脚本有行为、文档没写"缺口；
  SKILL.md 触发词补 `X 发长文`/`推特长文`/`twitter 长文`；README.en 表格标点精确化；
  零行为改动。遗留 4 个行为变化候选：无前导 `|` 表格、`~~~` 围栏、标题 140 字符检查
  （超长分段经评估不需要）。

## [0.3.2] - 2026-09-29

> **本版未发布**（未打 tag、未发 npm），全部内容已并入 0.3.3。以下为当时记录：

> 根包 0.3.1 → **0.3.2**（patch）；4 个技能 `version` 保持不动（top-ppt-html 0.1.19，其余 0.1.0）。
> 整仓同 tag 发版，技能 `version` 独立演进（见 docs/PUBLISHING.md）。

### topmind-cover：样张原创重制（纠偏）

- 上一版 16 张样张被指出"照搬参考封面"（文案与形象临摹第三方爆款图），本轮推倒重做：
  设计语言保留（巨型标题字/数字彩色突出/三层文字结构/中央 60% 安全区），
  **8 种风格全部换上原创标题与视觉**："7天玩转提示词"（纸飞机机器人）、"AI效率手册"
  （抽象光影几何）、"星尘 OS 3.0"（虚构品牌发布）、"从想法到产品"（步骤卡片）、
  "30天AI绘画挑战"（狐狸画家 IP）、"AI早报！"（报纸咖啡）、"慢思考"（银杏留白）、
  "创造者访谈"（杂志肖像）。
- `assets/examples/` 16 张（8 主图 + 8 公众号裁剪版）+ `overview.png` 全部重拼重检：
  中文逐字正确、无乱码、与参考图不构成临摹；`README.md` 声明样张为原创设计、
  标题/数字/品牌均为虚构演示。
- `references/cover-styles.md` 新增**原创铁律**：prompt 配方是设计语言，
  禁止照抄任何第三方封面的文案与形象；8 风格示例小节同步换为本轮原创标题。

### topmind-wechat-post：全面优化 + 4 处修复

- `scripts/md2wechat.py` 修复：**行内图片绕过图片管线**（现统一经管线解析、复制到
  `images/`、登记上传清单、可被 `--embed-images` 内嵌）；分隔线不再触发自家合规
  WARN（改用块级 `<section>` 居中，视觉一致）；标题手写序号剥离支持大写数字
  （壹贰叁肆伍陆柒捌玖拾）；图片 `title` 属性（`![a](x "t")`）不再导致整段源码泄漏。
- SKILL.md：主题表"适用"列与各主题 JSON 的 `genre` 声明对齐；补行内图片走图片管线
  说明；补 `--link-mode` 参数说明（默认脚注上标 / `inline` 括号注）。
- README（中/英）：新增 9 行"最小示例"（输入→输出片段）+ `md2wechat` 参数表。
- `negative_tests.py` 5→8 项，全过。

### topmind-x-article：全面优化 + 12 处转换 bug 修复

- `scripts/md2x.py` 修复 12 处：标题/引用/表格内行内标记残留、引用式链接与图片
  （`[文字][ref]`/`![alt][img]` 及定义行）、URL 含括号断裂、`\` 转义符残留、
  Setext 标题残留、带空格分割线（`* * *`）不识别、代码块内 `---` 误判分割线、
  文首 `---` 被 frontmatter 误吞、BOM 头、文档以代码块开头时首行缩进丢失。
- SKILL.md：description 补 `Do NOT use for 公众号（→ topmind-wechat-post）`，与短推文
  路由对称；`references/x-format.md` 转换规则表与脚本行为对齐。
- README（中/英）：转换规则更新 + 新增 10 行"最小示例"（输出经实测逐字一致）。

## [0.3.1] - 2026-09-29

> 根包 0.3.0 → **0.3.1**（patch）；4 个技能 `version` 保持不动（top-ppt-html 0.1.19，其余 0.1.0）。
> 整仓同 tag 发版，技能 `version` 独立演进（见 docs/PUBLISHING.md）。

### topmind-cover：风格库按爆款封面重沉淀 + 样张重制

- `references/cover-styles.md` 按 7 张爆款参考封面 + Manus 实战封面重沉淀为 **8 种风格**：
  爆款干货（`gan-huo`）/ 巨字宣言（`big-type`）/ 品牌发布（`brand-launch`）/
  教程步骤（`tutorial-steps`）/ IP 趣味（`ip-fun`）/ 资讯快报（`news-flash`）/
  极简留白（`minimal`，保留）/ 杂志编辑（`magazine`，保留），
  每种含适用场景、构图公式、配色 hex、标题写法规范（4~8 字、数字/关键词彩色突出）、
  中英 prompt 配方、避坑；删除旧 6 风格。
- `assets/examples/` 样张全部重制：**16 张**（8 风格 × 1200×675 主图 + 900×383 公众号中央裁剪版）
  + `overview.png`（8 宫格总览图），逐张目检（标题逐字准确、无乱码、中央 60% 安全区），
  7 次返工均为"底部元素超出安全区"；旧 12 张移除。
- 提炼规律：标题字巨大化（占画面高 22%~45%）、左文右图通用分区、三层文字结构
  （大标题 + 胶囊/笔刷副标题 + 底部标签条）、数字前置造冲击、背景极简浅色。
- 根 README（中/英）、cover README（中/英）、cover SKILL.md 嵌入总览图（GitHub 绝对 URL）
  + 8 风格一行式索引；用法"6 选 1"→"8 选 1"。

### bug 修复

- topmind-wechat-post `scripts/md2wechat.py`：本地图片文件缺失时未登记进"图片上传清单"
  （用户按清单补图会漏传）；现登记 `⚠ 本地文件缺失` 行并计入"图片 N 张"计数。
  HTML 仍保留断链占位（设计选择），清单已标注。

## [0.3.0] - 2026-09-29

> 根包 0.2.0 → **0.3.0**（minor，新功能）；4 个技能 `version` 保持不动（top-ppt-html 0.1.19，其余 0.1.0）。
> 整仓同 tag 发版，技能 `version` 独立演进（见 docs/PUBLISHING.md）。

### topmind-cover：封面风格库 + 12 张示例图（新功能）

- `references/cover-styles.md` 扩为 **6 种风格库**：震撼大字报（`big-poster`）/ 科技未来感（`tech-future`）/
  杂志编辑风（`magazine`）/ 极简留白（`minimal`）/ 国潮插画（`guochao`）/ 赛博故障艺术（`cyber-glitch`），
  每种含适用场景、配色 hex、字体建议、中英 prompt 配方、避坑。
- `assets/examples/` 新增 **12 张示例图**（6 风格 × 1200×675 主图 + 900×383 公众号中央裁剪版，共约 6.4MB），
  附 `assets/examples/README.md`（清单 + 安全区说明 + 复用声明），随 npm 包发布。
- SKILL.md 工作流新增"**步骤 0 选风格**"（三步必做：按题材 6 选 1 → 看示例图 → 按配方组 prompt）。
- 标题**中央垂直 60% 安全区**上升为设计铁律（风格库新增"安全区铁律"章节）：标题字与关键主体
  上下各预留 13%+，否则 900×383 中央裁剪会切掉标题。

### 最佳实践整改

- top-ppt-html / topmind-wechat-post 的 SKILL.md `description` 改**第三人称**（降误触发）；
  topmind-cover `description` 同步微调（"一次配齐"→"全流程覆盖"），`triggers` 新增 `缩略图` / `thumbnail`。
- topmind-wechat-post：站外取源坑与回推命令串收敛到 `references/workflow.md`，SKILL.md 只留索引；
  新增跨技能路由索引（封面配图 → topmind-cover，X 长文 → topmind-x-article）；
  二级标题序号由排版层自动生成（不再手写）。
- 各技能 README（中/英）与 SKILL.md 对齐：cover 新增风格库与示例图章节、用法改"步骤 0 选风格"；
  x-article 转换规则补"分隔线→空行"。

### bug 修复

- topmind-x-article `scripts/md2x.py`：`---` / `***` / `___` 分隔线转**空行**（原逻辑误当 frontmatter 吞掉）；
  `***粗斜体***` 先去三重星号再处理 `**` / `__` / `*`，不再残留星号。
- topmind-cover `scripts/crop-cover.py`：移除 `--slug` 悬空参数
  （用法与文档统一：`crop-cover.py <主图> --out-dir <包>/images/`）。

## [0.2.0] - 2026-09-29

### 新增三个写作/配图技能

- **topmind-wechat-post `0.1.0`**：公众号文章全生命周期技能（由 topmind-wechat 适配改名）。
  交付包 / 审校改写 / 质量三关（事实·逻辑·去 AI 味 ≥85）/ 状态同步 / 微信内联排版（`md2wechat --embed-images`）/ 发布清单。
  适配点：frontmatter 去 topmind-pack 专有键（`degradation`/`action_category`/`entrypoint`），
  跨 skill 引用改为通用表述，`writing-quality.md` 改用技能自带 `scan_ai_flavor.py`
  （原引用本机 `~/.workbuddy` 路径），`md2wechat.py` 缺失输入改干净报错（原 Traceback）。
- **topmind-x-article `0.1.0`**：X 长文一键发布。`md2x.py` 把 Markdown 转可直接粘贴进
  X Article 编辑器的纯文本（标题→纯文本行、加粗/斜体去标记、链接→`文字（url）`、
  图片→`[图N]`+文末配图清单、表格→"项：值"列表）；`references/publish-checklist.md`
  沉淀实战经验（首评置顶补信息、图序核对、发布后抓回核对）。缺失输入干净报错。
- **topmind-cover `0.1.0`**：文章封面配图，X / 公众号共用。设计铁律（震撼·醒目·主题突出：
  一图一主题、大标题 ≤10 字、四周 8% 留白）+ 5 套风格模板；
  `crop-cover.py` 从 16:9 主图中央裁出公众号 900×383 版（X 用 1200×675），落盘命名规范。
  缺失输入 / 非图片干净报错。
- 每个新技能带轻量 CI 门禁：`package_skill.py --check`（frontmatter/版本/引用完整性/禁用文件）、
  `audit_skill.py` / `audit_docs.py` / `audit_styles.py` / `audit_css.py`、`negative_tests.py`
  （异常输入不崩溃）。`ci_privacy_scan.py` 全仓通过。

## [0.1.19] - 2026-09-28

### 排版修复 · 大纲篇章化 · 参考资料去假 · 图标真导出 · PPTX 高保真增强

> 源起：2026-09-28 用户复盘五类问题（顶栏重叠 / 卡片不齐 / 大纲罗列页标题 / 参考资料占位 / PPTX 格式错乱），并要求「业界怎么解决的，不要闭门造车」。本次对照 Slidev `pptx-editable` / PptxGenJS / think-cell 混合通道模式系统整改。

#### A. HTML 排版硬伤
- **顶栏副标题压住右侧工具钮**：`.brand__txt` 此前无基础样式，flex `min-width:auto` 钉死整行文字宽，省略号永不触发。补 `min-width:0; overflow:hidden`，`.brand` / `.bar__in` / `.nav` 收缩链修复；≤1360px 自动收起副标题。
- **卡片高度不一致**：`.card` 改 flex 列 + 底对齐；`.g-quad` / `.g-half` / `.g-*--equal` 强制等高；`.g-half` 提升进 `engine.css` 并改 `align-items:stretch`（此前 research 专属且 `start` 违反「同构同高」契约）；纯卡片栅格不再误用 `.a-start`。

#### B. 大纲 = 章节大纲（3–7 章），不是页目录
- **结构契约**：`agenda` 条目 = 章（篇/section），每章 1+ 页；页标题逐页出现，章标题只在 Agenda 出现一次。预算 3–7 章（含参考资料 +1 仍 ≤8）。
- **生成器**：`render_from_model` / `scaffold_report` 按 eyebrow `NN ·` 章前缀归并，删掉「agenda 条数 ≠ 页数就按页强制重建」逻辑；锚点落该章第一页。
- **schema / 阈值**：`model-schema` 加 `agendaMax=7` / `agendaHint`；`layout-constants.contentQuality.agenda` 加 `chapterMin/Max`；`agendaComfortMax` 16→8。
- **文档**：`content-rules` §Agenda 重写；`SKILL` 铁律 4；`components-atoms` / `failure-modes` F20 / `layout-grammar` 阈值同步。
- **样张**：showcase 大纲 12 条页标题 → 9 章（`05 · 图表工艺` 下 3 页只占 1 条）。

#### C. 参考资料只列真实来源（宁缺毋假）
- **冒烟枪**：`render_from_model.py:738` 对每个 `[n]` 生成 `「来源名称，时间；口径。」`；scaffold 写「来源 N（替换为真实来源名称）」。
- **新规则**：只列 `model.refs` 真实来源；**无真实来源整节省略**（连导航 `#refs` 入口一并摘掉，避免悬空锚点）。硬拦占位串（`来源名称` / `替换为真实来源` / `某行业报告`）。
- **模板**：三份模式模板参考节改为注释掉的真实样例 + 「无真实来源则删整节」说明；`example.com` 假条目清除。
- **文档**：`content-rules` §五 规则 4 重写；`SKILL` 铁律 10；`layouts-research` / `.ref-link` 示例改真实机构名。

#### D. 图标真导出（SVG→PNG，不再用 accent 方块替代）
- **新模块**：`scripts/icon_lib.js`（20 语义图标单源）· `scripts/build_icon_assets.js`（sharp 栅格化）· `scripts/icon-assets.json`（PNG 缓存，gitignore）· `scripts/icon_raster.js`。
- **链路**：模型 `cards[].icon` / HTML `data-icon` → `extract_model` 回填 → `build_pptx` 嵌 PNG。`objectName: icon:*`，`validate_pptx` 单独计数 `icon_pictures`，**不进** `pictures=0` 内容图门禁。缺 sharp/资产回落 accent 方块。
- **schema**：`cards[].icon` 字段 + 取值说明（`icon_lib.js` 键）。

#### E. PPTX 高保真增强（对照业界混合通道）
- **发射前叠印断言**：`assertNoOverlap` / `rectsOverlap` 在 `addShape` 前自检组合布局（图表∩inline 数据表等），计入 `OVERLAP_PREEMIT`。
- **表格行高自适应**：`addTable` 超容量压到 hardFloor / 整体缩放；表头独立 `headRowH`；`fit:'shrink'`。
- **`regionOf('bar')` 双偏移纠正**：`chartX/chartW` 此前被当偏移再加 `mx`，柱图右移 0.6in 与标题/表格不齐——改与 donut/table/hbar 同口径对齐版心。双引擎同步。
- **图例收进图高**：waffle / marimekko / slope 图例带含在 `h` 内，与 inline 数据表留间隙（几何铁律②）。
- **文本自动收缩**：标题 / 卡片 / 结论条 / 页脚统一 `fit:'shrink'`（PowerPoint 字体度量 ≠ 浏览器）。

#### F. 文档与工程
- `icons.md` / `pptx-export.md` / `high-fidelity.md`（新增「已落地的高保真增强」对照表）/ `failure-modes` F20 / `tech-design`（图标单源登记）/ `package_skill`（三模块进必收）。
- 业界调研纪要：`docs/industry-pptx-research.md`（Slidev pptx-editable / PptxGenJS / think-cell / Marp / reveal.js 路线对比与取舍）。

#### 回归
- 技能审计 ✓ · 文档审计 ✓ · 研究 HTML 94/0/0 ✓ · 展示 HTML 85/2/0 ✓ · 两份 PPTX `errors:[] warnings:[]` ✓ · 打包校验 106 文件 ✓。

### 红线未动
反截断、图表多样性地板、Mode A craft、runtime SHA 同版本门禁、中文「演示文稿」术语、整仓 npm 发版、motion=none、结论条无「So what」标签、无左侧 accent 装饰轨、双单源 + sync_runtime、strict 0/0 交付。

## [0.1.18] - 2026-09-28

### PPTX 导出质量整改 · 双通道几何收敛 + 门禁盲区补齐

> 源起：2026-09-28 研究报告双通道交付复盘（HTML/PPTX），PPTX 有 4 类硬伤（含两处大面积文字叠印）、HTML 有 4 类空间利用问题、门禁全绿而效果不合格。本次按六类根因（R1–R7）系统整改。

#### A. 几何叠印硬伤（R1/R2 · PPTX 导出）
- **架构节点标题/注解叠印**：注解改为钳制在标题下边（原底对齐 `y=lh-0.5` 在 `lh≈0.59` 时与标题完全重合）；节点高不足降级单框混排。双引擎同步。
- **verdict/soWhat 同槽叠印**：共用 annotation 结论条槽位——渲染器互斥（verdict 优先）、`extract_model` WARN、`model-schema` 加 `mutualExclusionHint`。HTML 同步去重。
- **图例压来源行**：图例改落图区底部（`bodyBottom-0.28`），禁 `PH-0.62` 固定偏移。
- **`sec.note` 压 so-what 带**：`note` 与 `footnote` 合并到 `footnoteY=6.72`，禁用 `note.y=6.55` 绘制。
- **图表类目标签越出图区**：标签带含在图高 `h` 内（原画到 `y+h` 外）。
- **图片底边侵入注释带**：有图注时下界收到 `contentBottomWithNote`。

#### B. 列宽 / 槽位几何（R3）
- **三栏只占半幅（栏宽 1.69in）**：`regionOf('twocol')` 单栏宽被当总宽——改用版心全宽推导。双引擎同步。
- **KPI 支撑指标铺满整页**：A 通道 `regOf('kpi','metrics')` 缺分支——补 dividerX 右侧分栏。
- **halftable 图表越过 so-what**：`regOf('halftable')` 忽略 opts.top/bottom——传导 opts。

#### C. Agenda 分页与列序统一（R4）
- >8 条自动双列（列优先）；**>12 条自动分页**（Agenda I/II）；长标题截断全称沉 notes（`titleMaxChars=36`）。双引擎 + HTML 同步。

#### D. 门禁盲区补齐（R6）
- **新增 `ELEMENT_OVERLAP`**（元素两两重叠 ≥0.05in²）与 **`LAYOUT_FILL`**（版心填充率 <55%）。
- **Agenda 容量契约**：条数 ≤16、标题 ≤36 字、>8 条须双列。
- **图表还原度分级**（`charts.fidelityMap`）：low = area/radar/treemap/sankey/streamgraph/marimekko/boxplot/network；决策树标注 + 改判建议。
- **跨通道一致性**（`cross_verify`）：Agenda 阅读顺序、图片数量、图表数据标签。

#### E. 图标与图片正确使用
- **图标**：`render_from_model` 内置语义图标库 + `card_head()`；PPTX 保持 accent 方块路标。
- **图片**：`r_image` 支持真图渲染、占位同串、`fit=contain`、多图版式（grid/compare/wall）。

#### 文档同步
- `page-type-matrix` 容量契约 + 还原度；`failure-modes` F19/F20；`pptx-export` 几何铁律；`chart-decision-tree` 还原度列；`content-rules` / `components-atoms` / `modes` / `layouts-combo` 契约更新。
- Pages 源同步：`docs/showcase.html` / `docs/style-gallery.html` 与技能侧 assets 副本逐字节一致（meta → v0.1.18）。

### 红线未动
反截断、图表多样性地板、Mode A craft、runtime SHA 同版本门禁、中文「演示文稿」术语、整仓 npm 发版、motion=none、结论条无「So what」标签、无左侧 accent 装饰轨、大纲 >8 → 2col。

## [0.1.17] - 2026-09-26

### Release
- Republish of the **0.1.16 craft** (结论条去左轨 · anti-AI-flavor · Showcase 全页刷新). npm registry left `0.1.16` in a staged/conflict state (`E409 previously staged`); content identical to the `v0.1.16` GitHub Release / docs Pages source.

### 红线未动
反截断、图表多样性地板、Mode A craft、runtime SHA 同版本门禁、中文「演示文稿」术语、整仓 npm 发版、motion=none、结论条无「So what」标签、无左侧 accent 装饰轨。

## [0.1.16] - 2026-09-26

### Craft · 结论条去 AI 味：取消左侧 accent 装饰轨

#### 设计决策（硬原则）
- **结论条无 left rail**：用户明确拒绝结论条左侧色条为 AI-flavored chrome。`.sowhat` / PPTX `soWhatBar()` 改为 **MD3 tonal surface 满铺**（`accent-soft` + 细描边）+ 舒适字阶 / `line-height:1.65` / 内边距 `--sp-5`/`--sp-6`；**禁止**竖色条、霓虹边、装饰 chip 当强调。
- 写入 `design-system` §去 AI 味、`content-rules`、`components-atoms`、`SKILL`、`layout-constants.aiFlavor.visual.forbidConclusionLeftRail`。
- 同类收口 `.note` 同步去掉左轨，改 tonal 细描边；`.flagbar`（待核实）保留细强调（功能态，非结论装饰）。

#### 深度同步
- 引擎：`engine.css` · `build_pptx.js` · `pptx-export.js` · `style-gallery` 预览条。
- 样张 / 模板 / `docs/showcase.html`：全量 `sync_runtime`；Showcase 全页刷新（修 s1「要点一/二」占位 → 三主张卡；s2/s4 补结论条；「so-what」用户文案 →「结论条」；meta → v0.1.16）。
- 截图：`docs/showcase/topmind-showcase/*` + `assets/showcase/*` + theme-overview 重截。
- 版本对齐 **0.1.16**（根 + 技能 package / SKILL / README / PUBLISHING / CHANGELOG）。

### 红线未动
反截断、图表多样性地板、Mode A craft、runtime SHA 同版本门禁、中文「演示文稿」术语、整仓 npm 发版、motion=none、结论条无「So what」标签、大纲 >8 → 2col。

## [0.1.15] - 2026-09-26

### Release
- Republish of the **0.1.14 craft overhaul** (MD3 结论条 · 一屏/大纲自适应 · 克制图标). npm registry left `0.1.14` in a staged/conflict state (`E409 previously staged`); content identical to the `v0.1.14` GitHub Release / docs Pages source.

### 红线未动
反截断、图表多样性地板、Mode A craft、runtime SHA 同版本门禁、中文「演示文稿」术语、整仓 npm 发版、motion=none。

## [0.1.14] - 2026-09-26

### Craft overhaul · 三支柱：结论条 · 一屏高度/大纲自适应 · 克制图标

#### A. MD3 结论条（原 so-what）
- `.sowhat` 升为 MD3 tonal 衬条（`accent-soft` 底 + 左 4px accent 轨 + `--fw-title` / `fs-h3`）；**默认不显示「So what / SO WHAT」标签**（可选 `.sowhat--labeled`）。
- 与上方主内容呼吸间距 `clamp(28px,3.6vh,48px)`；`:has(>.sowhat)` 时 wrap 纵向 flex，结论条 `flex:none` 防挤压。
- CSS 迁入公共 `engine.css`（三模式共享）；research 模板去掉重复规则。
- PPTX `soWhatBar()` 双通道只画衬底+左轨+正文；`chartBottom` 相对 `soWhatY` 让位 0.12→0.20in。
- 门禁：`EXHIBIT_PAGE_MISSING_SOWHAT` 改检测结论条形状；文案「结论条」。

#### B. 一页一屏 · 大纲自适应
- 高度契约：`section.band` 一屏；主内容不得溢出或压进结论条/注释带；放不下走 `overflowRule`（重构→拆页→换形态→有限缩字），禁静默截断。
- 大纲：**>8 条须 `.agenda--2col`（两列/两排）**；>16 拆篇。阈值入 `contentQuality.agenda`；`validate_report` 只认 `<ol class="…agenda--2col">`（修 CSS 选择器误伤假通过）。
- Showcase 12 条大纲改双列；`layout-grammar` / `components-atoms` / SKILL 同步。

#### C. 图标原则（行业共识 · 非装饰）
- `icons.md` 增补 wayfinding / 同家族 / 有限密度 / 四正当位置 / 禁区（Agenda·表·图内）；Mode A 内容页必做。
- Showcase / 黄金样张落地 `card__ico` / `ul--ico`；`validate_report` 对「≥2 卡且无 `.card__ico`」发 WARN。

#### 发布
- 样张、模板、references、README、PUBLISHING、截图同步；版本对齐 **0.1.14**。

### 红线未动
反截断、图表多样性地板、Mode A craft、runtime SHA 同版本门禁、中文「演示文稿」术语、整仓 npm 发版、motion=none。

## [0.1.13] - 2026-09-26

### Changed
- Restored the spacious sparse cream/navy/gold banner (1280×360) with the install command as the bordered subtitle: `npx @topmindspace/tms-skills install top-ppt-html`.
- Restored the third-row product line: **TopMindspace Agent Skills · 让 idea 飞 · 正式场合演示文稿**.
- Aligned whole-repo package, skill metadata, and documentation versions to **0.1.13**.

## [0.1.12] - 2026-09-26

### Changed
- Regenerated `docs/assets/tms-skills-banner.png` (1280×360): includes core skill name **top-ppt-html**, formal keynote / presentation stage intent, tagline HTML + PPT.

## 0.1.11 — 2026-09-26

### Positioning · README slim · showcase narrative

- **差异化定位**：根 README / 技能 README（中英）开篇写清——市面 PPT 技能很多，为何还要 top-ppt-html；特色 **HTML + PPT 双交付**；为**演示报告 / 正式商务演示**而生；参考 **MD3** 信息密度与克制；日常 HTML 等同幻灯片，需要时再导出高保真可编辑 PPTX。
- **主题总览只留一张**：默认 `theme-overview.png`（演示·business-blue）；caption 链到 style-gallery / 研究·架构总览路径；正文不再三张并排占屏（落地页同步精简）。
- **Showcase 叙事**：改写「为什么是我们」与「双交付」两页；subtitle / meta → v0.1.11；版本折线含 0.1.11；`validate_report --strict` **0/0**（5 种图表保持）。
- **截图**：刷新 `docs/showcase/topmind-showcase/*` 与 `top-ppt-html/assets/showcase/`（含 positioning / charts / toolbar）。
- **SKILL.md**：开篇与 description 产品句对齐定位；等量删减冗余，体积仍 ≤13KB。
- **Live**：`docs/showcase.html` / Pages 源与 github.io `tms-skills/` 同步本版。
- 版本对齐 **0.1.11**（根 + 技能 package/lock / SKILL metadata / README / PUBLISHING）。

### 红线未动
反截断、图表多样性地板、Mode A craft、runtime SHA 同版本门禁、中文「演示文稿」术语、整仓 npm 发版、motion=none。

## 0.1.10 — 2026-09-26

### Showcase · header toolbar docs · bilingual README

- **产品 Showcase 加厚**：`2026-09-26-topmind-tms-skills-showcase` 扩为 Mode A · 12 内容页；**5 种图表**（`bar` / `donut` / `line` / `waterfall` / `hbar`）经 `render_from_model` + `hydrate_charts` 回填；含 **Header 工具栏专页**（控件 × 快捷键 × 行为表）；`validate_report --strict` **0/0**。
- **Header 工具栏文档**：`SKILL.md` 交付物表（T/P/H/F/B + 9 风格 + Esc/翻页 + `REPORT_MODEL` 同步）；根 README / 技能 README（中英）显著说明。
- **双语 README**：保持 **`README.md` = 中文默认**；新增 **`README.en.md`** 全量英文平行；`top-ppt-html/README.en.md` 用户向摘要；文首互链。
- **截图**：刷新 `docs/showcase/topmind-showcase/*` 与 `top-ppt-html/assets/showcase/`（含 `showcase-toolbar.png`）。
- **维护工具**：新增 `scripts/hydrate_charts.py`（核心图类型占位 SVG → 模型数据绘形，供样张重建）。
- **Live**：`docs/showcase.html` / Pages 源与 github.io `tms-skills/` 同步本版 showcase。
- 版本对齐 **0.1.10**（根 + 技能 package/lock / SKILL metadata / README / PUBLISHING）。

### 红线未动
反截断、图表多样性地板、Mode A craft、runtime SHA 同版本门禁、中文「演示文稿」术语、整仓 npm 发版、motion=none。

## 0.1.9 — 2026-09-26

### Docs · banner · theme overview · live showcase

- **主题总览大图**：根 README + `top-ppt-html/README.md` 嵌入三张 Gate 0 `theme-overview*.png`（演示 / 研究 / 架构），保留风格封面与 showcase 样张画廊。
- **Slim banner**：`docs/assets/tms-skills-banner.png` 裁为 **1280×360**；README 展示宽约 960。
- **Badge 行**：对齐 topmind 风格（Release / npm / CI / License）。
- **Live 链接**：指向 `https://topmindspace.github.io/tms-skills/`（落地页 / showcase.html / style-gallery.html）。
- **Pages 源**：`docs/index.html` + `docs/showcase.html` + `docs/style-gallery.html` + `docs/site-assets/`（启用 GitHub Pages → Deploy from branch `main` / `/docs` 即可上线同路径 URL）。
- 模板 / runtime：经 `sync_runtime.py` 校验，无「甲板」；`REPORT_MODEL` 与引擎 SHA 一致。
- 版本对齐 **0.1.9**（根 + 技能 package/lock / SKILL metadata / README / PUBLISHING）。

### 红线未动
反截断、图表多样性地板、Mode A craft、runtime SHA 同版本门禁、中文「演示文稿」术语、整仓 npm 发版。

## 0.1.8 — 2026-09-26

### Showcase · docs · release polish

- **产品 Showcase**：新增 Mode A 样张 `top-ppt-html/assets/examples/2026-09-26-topmind-tms-skills-showcase.html`（+ model）——介绍 TopMind / tms-skills / top-ppt-html（三模式·风格主题·质量门禁·Fast Mode）；`validate_report --strict` 与 `smoke_pptx` **0/0**。
- **截图**：刷新 `theme-overview*.png`；新增 `docs/showcase/`（showcase 全页 + 三黄金样张关键页）与精简 `top-ppt-html/assets/showcase/`（进技能包，供 README）。
- **README 吸引力**：根 README + 技能 README 增加 banner、风格/模式画廊、showcase 链接与安装钉版本 **0.1.8**。
- **Banner**：`docs/assets/tms-skills-banner.png`。
- **打包**：`package_skill` 纳入 `assets/showcase/*`；examples 最小数量仍 ≥3（黄金样张 + 可选 showcase）。
- **文档清理**：用户向 README 对齐当前产品面；PUBLISHING 版本线 → 0.1.8；`build_examples` 说明允许 showcase 并存。
- 版本对齐 **0.1.8**（根 + 技能 package/lock / SKILL metadata / README）。

### 红线未动
反截断、图表多样性地板、Mode A craft、runtime SHA 同版本门禁、中文「演示文稿」术语、整仓 npm 发版。

## 0.1.7 — 2026-09-26

### top-ppt-html · defect opt (D8/D9/D11/D13)

- **P0 D8**：`chartBottom(hasSoWhat, hasFootnote)` 不再 footnote 短路；`Math.min(soWhatY, footnoteY, contentBottomWithNote)` 与 flagY 让位同口径。双通道（`build_pptx.js` / `pptx-export.js`）对齐；flagBar 在 withNote 时底边不越过 `contentBottomWithNote`；Agenda 预留 0.25in 避免 severe 误伤。
- **P0 D9**：`annotation_band_overlap_check` 报告页内**全部**侵入者（去掉首条即 `break`）。
- **P1 D11**：有 so-what 时 `band_top = soWhatY`（6.05），捕获 (6.05, 6.40] 侵入；crush = 自带顶之上压下；注释自形状/窄 accent 条豁免保留。
- **P1 D13**：`ci_skill_gates.sh --with-pptx` 必跑 `smoke_pptx` × business-blue **与** research-mckinsey（覆盖 soWhat+footnote）；graphite-dark 可选。
- **CHROME_DRIFT**：页码只认 `N / M`，不再把年份/Exhibit 编号当页脚（research-mckinsey 假阳性清除）。
- **Fast Mode / 效率**：演讲/汇报线索→Mode A；明确跳过 vs 仍须（质检红线不降）；L0+L1 / `extract_snippet` 纪律不变。
- **门禁**：`test_feedback_gates` 锁定 D8/D9/D11/CHROME；research-mckinsey `--strict` **0/0**。
- 版本对齐 **0.1.7**（根 + 技能 package / SKILL metadata / README / PUBLISHING）。

### 红线未动
反截断、图表多样性地板、Mode A craft、runtime SHA 同版本门禁、中文「演示文稿」术语保持。

## 0.1.6 — 2026-09-25

### CI / Release 硬化
- **根因 A**：`validate_pptx` 的 `ANNOTATION_BAND_OVERLAP` 把全幅背景（底边 7.50in）误判为侵入注释带；改为排除 full-bleed 背景 / 全高装饰条 / chrome 区，同时保留对图例/主图压进 so-what 带的真阳性。
- **根因 A′**：`FONT_SIZE_NOT_SNAPPED` 未收录 `modeTypeScale` 的 **h2=17pt**；改为从 typeScale ∪ 全模式 modeTypeScale ∪ ladder 动态取允许集。
- **冒烟可读性**：`smoke_pptx.sh` 可靠传播 validate 退出码；失败时 stderr 先打错误码/页码短摘要。
- **根因 B**：Release `npm publish` 遇已发布/已 staged 的 **E409** 时改为 exit 0（幂等）；GitHub Release + 资产仍成功。
- **DRY**：`scripts/ci_skill_gates.sh` 为 CI/Release 共用门禁；Release 对齐 CI 的 fixture + `smoke_pptx`；CI concurrency cancel-in-progress；npm cache；python-pptx 仅 PPTX 步骤安装。
- 文档：新增 `docs/ci.md`；版本对齐 **0.1.6**。

### 红线未动
反截断、图表多样性地板、Mode A craft、runtime SHA 同版本门禁保持。

## 0.1.5 — 2026-09-25

### top-ppt-html · defect close-out

- **P0 D1**：环图右栏可见标题去掉作者约束「禁止叠在弧上」→ 读者向「构成明细」。
- **P0 D2**：`sync_runtime.py` 注入 `/* __TOPPPT_RUNTIME_SHA__:<16hex> */`（源 = `assets/pptx-export.js`）；`validate_report` 缺戳/漂移 FAIL；负例 N19。
- **P1 D3**：`cross_verify.NUMERIC_TOKEN` 增补 YB|ZB|EB|PB 与 kWh|Gbps。
- **P1 D4**：CI 轻量生成 `dist/regression` 样张 + `python-pptx`，使 N4/N5/N7 真正跑通（非全量 regression）。
- **P2**：package-lock 对齐 0.1.5；README/PUBLISHING 2.x 弃用改为事实陈述；`deprecate-npm-2x.sh` 精简为 `@2.x` one-shot + verify；双版本口径（包 semver vs schema `0.1`）写入 SKILL/tech-design。
- **术语**：全库「甲板」→ 演示文稿/样页等（保留英文 trigger `deck`）。

### Installer

- `@topmindspace/tms-skills` → **0.1.5**（整仓同 tag）。

## 0.1.4 — 2026-09-25

### top-ppt-html · craft + quality + docs + perf close-out

- **P0 效率 / agent 工作流**（usage-feedback）：
  - 默认交付 **仅 B 通道 PPTX**（`build_pptx.js`）；A 通道（`pptx-export.js` / `gen_channel_a.js`）限预览与 `cross_verify` / 回归。
  - `extract_snippet` 强制 + **整读大 L2 = FAIL / 不合格**（SKILL + playbook）；`audit_skill` 新增对应门禁。
  - `quality_gate` 对互不依赖子进程（HTML strict / PPTX strict / evals）**并行**执行。
  - Fast / 轻量路径强化 **HTML-first**；PPTX 显式 opt-in（用户要 PPT 或交付含 PPTX）。
  - **未削弱**红线：反截断、图表多样性（`minTypes.presentation=4` / registry）、Mode A 大气正式工艺、Gate 0 语义。
- **质量 / 规范**：对齐 SKILL frontmatter、双 `package.json`、README 钉版本、PUBLISHING、安装说明；跑通 check / audit / feedback gates。
- **docs 工艺改写**：定位强调优雅·美观·大气·演讲/正式场合；版式/排版/色彩/内容组织 + 质检与高保真导出；L0 仍瘦、L2 按需。
- **此前 #7（validator / engine）**：`shape_bounds` 读 `p:xfrm`、`TEXT_OVERFLOW_VERTICAL`、`ANNOTATION_BAND_OVERLAP`、`FONT_SIZE_NOT_SNAPPED`、多系列 vbar、streamgraph 图例内收、image caption `capYImg`——随本版一并发布。

### Installer

- `@topmindspace/tms-skills` → **0.1.4**（整仓同 tag）。

### Intentional leftovers

- 不引入 Claude-only `when_to_use` / 跨端风险 `allowed-tools`（同 0.1.3）。
- `skills-ref validate` 仍为可选，非发布硬依赖。
- layout-constants / model-schema 事实源版本线仍为 `0.1`（patch 记在 package / metadata）。

## 0.1.3 — 2026-09-24

### top-ppt-html · QA close-out + docs

- **P2-4 playbook 拆表**：意图→页型穷举 → `references/page-type-matrix.md`；图表决策表+七种误用 → `references/chart-decision-tree.md`。playbook 保留 Mode 契约 / V1–V4 / 组合 / **图表多样性摘要** / **反截断** / 路径·命令·L2 路由（体积 22KB→~17KB）。
- **版本对齐**：根 README / 技能 README / PUBLISHING / `metadata.version` / 双 `package.json` → **0.1.3**（消除残留 0.1.0 横幅）。
- **IMAGE_CAPTION**：配图页亦认 so-what/lead/figcaption；新增 WARN `IMAGE_NEAR_EMPTY`（近图过空）。
- **P2-2/P2-3**：不引入 Claude-only `when_to_use`、不写跨端风险 `allowed-tools`（`skills-ref validate` 已通过开放标准字段；扩展字段留给宿主实验）。
- **P2-5**：可选 `npx skills-ref@0.1.5 validate ./top-ppt-html`（不作为发布硬依赖；主门禁仍 `audit_skill`）。
- **docs**：根 README 安装表/钉版本/`@0.1.3`；技能 README 改为人类维护指南并指向 SKILL；package REQUIRED + MIN refs ≥25。

### Installer

- `@topmindspace/tms-skills` → **0.1.3**（整仓同 tag）。

### 此前 Unreleased（agent-compat，随 0.1.3 一并发布）

- **P0-1 Trigger eval**：`evals/trigger-queries.json` + `scripts/check_triggers.py`；`package_skill.py --check` 门禁。
- **P0-2 Mode A 读预算诚实**：L0+L1=2；Mode A/Fast 可加 L1.5（`default-surface` + `presentation-craft`）。
- **P0-3 反过读**：禁止整读清单 + 强制 `extract_snippet.py`。
- **P1 Frontmatter / 安装路径 / Fast 最小大纲 / 插画 brief**：license·compatibility·metadata；Cursor/Codex 路径；`illustration-layout.md`；`agents/openai.yaml`。


## 0.1.2 — 2026-09-24

### top-ppt-html · P2 cleanup（advanced 按需 · Mode A 次级骨架 · icons 压缩）

- **Advanced charts 按需**：默认读面 = `charts-discipline` + 核图 8；`charts-extended.md` **禁止预读**，仅意图命中 `extract_snippet.py --chart`。`charts.variety.preferCoreFirst` + validate WARN（A/B）；advanced **计入** `minTypes`（不降 `presentation=4`，不缩 registry）。
- **Mode A 骨架分层**：主力 P1–P4+P6/P10；次级 P7–P9/P11–P12（`layoutSystem.modeSkels` + layout-grammar / default-surface / recommend_layout 同口径）；画廊侧重主力。
- **icons.md 压缩**：语义表 + 禁区 + 尺寸档 + 高频 20 SVG（~8.7KB）；完整枚举 → `docs/archive/refs/icons-catalog.md`；package 仍 REQUIRED。
- **docs 对齐**：SKILL / playbook / presentation-craft / modes / charts 门面同步；Fast Mode + 长文溢出序保持不变。

### Installer

- 安装器 `@topmindspace/tms-skills` → **0.1.2**（随技能包内容更新）。



### top-ppt-html · Long-text / Quality round（反截断 + 门禁加深）

- **反截断政策**：Mode A / content-rules / presentation-craft「长文与信息承载」——溢出顺序固定为 重构→拆页/分章→换形态→有限 fontShrink；**禁止**静默截断 / 砍 so-what / 为疏朗删实质。单页字数改预警（presentation char 1800），不为「字多」单独 FAIL。
- **结构引导取代硬砍刀**：列表/卡片 `maxItemChars` 等改为引导 + prefer；checklist 同步。
- **layout-qa 加深**：`LAYOUT_QA_TRUNCATION` / `OVERFLOW_NO_SPLIT` / `HALF_EMPTY` / `ALIGN_RHYTHM`；presentation `--strict` 仍自动 layout-qa。负例 L4–L6。
- **recommend_layout**：高容量意图 → 多页序列（议程→主张→证据卡→明细），禁一页塞爆。
- **P1-3 charts facade**：纪律优先 → 核图 8 → extended 按需；**不降** `minTypes.presentation=4`。
- **P1-4 会场字号**：pptx-export venue 表（小会议室 / 默认 / 礼堂）。
- **P1-6 chrome**：跨页页脚 y 漂移 `CHROME_DRIFT` WARN + 文档说明。

### top-ppt-html · Presentation Craft（Mode A 工艺）

- **P0-1 图表多样性（用户明确保留）**：**不降** `minTypes.presentation`（仍为 **4**）；registry/advanced 图种保留。纪律改为「按内容选型拉开多样」+ 禁反模式（简单全幅 / 极偏 donut / 为过门禁硬上冷门图）；playbook §五 / layout-qa 同步。
- **P0-2 default-surface**：升为 Mode A / Fast 演示主读面（12 页型 + 8 核图 + V1–V4；P5–P12/advanced 按需）；SKILL L2 索引指向。
- **P0-3 layout-qa 默认**：`validate_report --strict` 在 presentation 下自动 `--layout-qa`；`quality_gate` 同口径；B/C 不强制。
- **P0-4 主张标题**：Mode A action/claim title（禁话题标签）写入 content-rules / modes；校验 WARN。
- **P0-5 `presentation-craft.md`**：中英术语一页纸清单（one idea / 3s / whitespace / CRAP / motion=none / WCAG…）；package REQUIRED。
- **P1**：fillTarget A 58–75% + intentional whitespace 豁免；`recommend_layout` 偏 V1–V4、降 donut 默认权重；Fast 路演/汇报/发布/演讲/demo→A；motion=none 铁律短句。

### top-ppt-html · Batch 3（瘦身）

- **归档 L2**：`industry-benchmark.md` / `design-system-engine.md` → `docs/archive/refs/`（生成路径不读）。
- **layoutSlots 单源**：删除 `scripts/layout_slots.json`；`lib_layout_regions.js` / `sync_runtime.py` 只读 `layout-constants.layoutSlots`。
- **示例**：`assets/examples/` 仅留 3 份黄金样张（每模式 1）；其余 → `docs/archive/examples/`；`build_examples.py` 瘦身为自检（全量脚本归档）。
- **主题 PNG**：`theme-overview*.png` 量化压缩约 −70%。
- **default-surface.md**：12 页型 + 8 图 + V1–V4 速查；playbook §五标注默认 8 核心图。
- **package**：MIN refs ≥20、examples ≥3；`recommend_layout.py` 入 REQUIRED；README 缩为安装+命令索引。

### top-ppt-html · Batch 2（布局选型 + layout-qa + PPTX 对齐）

- **recommend_layout.py**：`--mode A|B|C` + `--intent` / `--from-model` / `--stdin` → `{pageType,skel,chart,rationale,v?}`（V1–V4 / 极偏禁 donut / sizeByComplexity）。
- **validate_report.py --layout-qa**：缺 data-skel、连续同骨架、极偏 donut、演示简单全幅、V 契约；negative_tests 增 L1–L3。
- **cross_verify.py** 默认 SKIP，`--full-ab` 才跑；regression 同口径。
- **build_pptx.js** 尊重 `layoutPreset`（缺省由 pageToPreset 回填，写入备注）。
- **smoke_pptx.sh** + CI skill-gates 冒烟：extract_model → build_pptx → validate_pptx --strict。

# Changelog

## Unreleased

### top-ppt-html 0.1.1 — Batch 1（工作流单写 · Fast Mode）

- **模型单写统一**：playbook / SKILL / pptx-export 命令链均为 scaffold → 只填 `REPORT_MODEL` → `render_from_model --inplace` → `validate_report --strict`（禁 HTML/模型双写）。
- **`render_from_model.py` 纳入 package REQUIRED**；references 最小篇数注释对齐实有数量（≥24）。
- **Fast Mode**：触发词跳过 Gate 0 + 六项；默认 B/mckinsey/light 等；标准路径仍为硬门禁；`audit_skill` 适配豁免声明。
- **归档** `references/reform-plan.md` → `docs/archive/reform-plan.md`；硬门禁改指 `qualityGates` + `failure-modes`。
- 技能 `package.json` 版本对齐仓库叙事 `0.1.1`（LC 仍为 `0.1`）。

## 0.1.1 — 2026-09-24

### Fixes (P0 / P1)

- **Release 顺序与稳健性**：Privacy → 技能门禁 → Package → Collect → GitHub Release → **npm publish（已发布则跳过，避免 E409）** → 再 Prune。
- **Prune 策略**：只删旧 GitHub Release（保留 2 个）；**不再删除 git tags**。
- **多技能发现**：`scripts/discover_skills.js` + CI/Release 动态打包/门禁；`npm run sync:files` 同步 `package.json` `files`。
- **CLI**：校验 skill id；目标目录已存在时须 `--force`；文档口径与 README 对齐（npm 推荐 / GitHub 跟 HEAD）。
- **python3**：根与技能 `package.json`、workflows 统一 `python3`。
- **打包门禁**：`references/layout-grammar.md` 纳入 REQUIRED；去掉与 `theme-overview.png` 完全重复的 `theme-overview-presentation.png`。
- **Lockfile**：提交 `top-ppt-html/package-lock.json`；CI 优先 `npm ci --omit=dev`。
- **npm 2.x**：文档警告勿装 `^2`；提供 `scripts/deprecate-npm-2x.sh`（须维护者本地 npm 登录后执行）。

## 0.1.0 — 2026-09-24

首个公开版本。

### 安装

```bash
npx @topmindspace/tms-skills install top-ppt-html
# 或
npx github:topmindspace/tms-skills install top-ppt-html
```

### 包含

- 技能 **top-ppt-html**（品牌 TopPPT HTML）：单文件 HTML 报告 + 可编辑 16:9 PPTX
- 安装器 CLI **tms-skills**（`list` / `install`）
- 双通道分发：npm 钉版本 / GitHub 跟 HEAD
- tag 发版自动：GitHub Release + npm publish；**Release 只保留最近 2 个**

### 版本策略

- 安装器 `@topmindspace/tms-skills` 与技能 `top-ppt-html` **各自独立**按 semver 演进
- 默认 **patch / minor**；**major 仅用于**技能 id、CLI、注入标记等破坏性变更
- 改代码 ≠ 发 npm：必须 bump 版本并打 tag（或手工 publish）
