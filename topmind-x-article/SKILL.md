---
name: topmind-x-article
description: "X 长文（Article）发布：默认组合 topmind-revise 改稿，交付单源 <文章名>/<文章名>.md（Obsidian 直接看）；要发 X 时再按需派生 out/X长文.html（富文本一键复制+配图内嵌）与 out/X发布稿.txt（纯文本兜底；长文可保留文内链接，派生 X 短帖时链接、原图另发）+ 封面图 + 发布清单，由用户人工点发布。Use when X 长文、发 X 文章、写 X 文章、X article、长文发 X、写 X 长文、X 文章排版、推特长文、twitter 长文、Twitter Article。Do NOT use for 短推文、短帖、快讯与段子写稿（→ topmind-viral-posts 或 topmind-briefs）、现成文字格式化与转段子（→ topmind-format）、把短帖发出去（→ topmind-x，须用户确认）、公众号文章（→ topmind-wechat-post）、只要封面或头图（→ topmind-cover）、单独改稿、去 AI 味与质检（→ topmind-revise）。"
license: MIT
metadata:
  version: "0.4.22"
  action_category: "write"
  triggers: "X 长文, 发 X 文章, 写 X 文章, X article, 长文发 X, X 发长文, X 文章排版, 转纯文本, X 纯文本, X发布稿, 发 article, 一键复制, 写 X 长文, X 长文发布, 推特长文, twitter 长文, Twitter Article"
  author: "TopMindSpace"
  homepage: "https://github.com/topmindspace/topmind-writing-skills#readme"
  updated: "2026-10-18"
---

# topmind-x-article · X 长文

一篇长文只有一份源稿 `<文章名>/<文章名>.md`。默认交付这份 Markdown（含 images/、cover/、素材来源.md），
Obsidian 里直接能看；用户要发 X 时，再从它派生发布包到 `out/`。

```
<文章名>.md ─(默认)→ topmind-revise 改稿 → check_article.py 体检 → 交付 Markdown
            ─(按需)→ md2x-html.py → out/X长文.html（一键复制全文+配图）
            ─(按需)→ md2x.py      → out/X发布稿.txt（纯文本兜底）
            ─(按需)→ topmind-cover → cover/cover-1500x600.png → 发布清单 → 人工粘贴发布
```

## 先读：写作原则与信息设计

本技能建立在两份共享文件上，动笔前先读：

- [references/social-writing-principles.md](references/social-writing-principles.md)：8 条社交媒体写作原则（先想清楚、结论先行、每句都有新信息、形式跟内容走、简单清楚、原图优先、站在读者那边、真实有分寸）
- [references/information-design.md](references/information-design.md)：内容 → 形式决策表、篇幅和密度、去啰嗦的判断法
- 措辞和口吻在这两层之上，见 [references/core-voice.md](references/core-voice.md)

长文：先写骨架（每节要点 + 形式 + 图表计划 + 字数），再写正文；X 不渲染表格，派生时转分行或做成图。

## 语言：默认中文

- **默认中文**：标题、正文、配图文案一律用中文写作，这是默认行为，不需要用户每次声明。
- **英文是例外**：只有用户**明确说**"写英文文章/帖子"时才用英文。用户消息里夹杂英文词、
  给英文参考素材、引用英文原文，都不算"要求写英文"。
- 官方产品名、模型名、论文标题保留英文；引语正文写「人名：中文意思」，英文原文记进素材来源，
  不在正文里原文加括注（`references/core-voice.md` V13）。

## 工作流

0. **建文件夹、写稿、改稿（默认组合 topmind-revise，先于任何转换）**：
   - 新文章先建文件夹：`python3 scripts/article_scaffold.py --title "文章名" [--base 目录]`，
     得到 `<文章名>/<文章名>.md` + `images/ cover/ raw/ out/` + `骨架.md` + `素材来源.md`；已存在就报错，不覆盖。
   - **先写骨架**：填 `骨架.md`（主要信息、读者、每节要点 / 形式 / 图表计划 / 字数，方法见 `references/information-design.md` 第一、二节）。并列要点、步骤、对照、数据先在骨架里定成列表 / 表格 / 图，写完正文回头对一遍。X 长文不渲染 Markdown 表格的场景按决策表最后一列处理。
   - **先找图再写字**：按 `references/image-sourcing.md` 找官方 / 原帖 / 第三方原图，按出现顺序存成
     `images/01-xxx.png`、`02-xxx.png`，正文直接写 `![说明](images/01-xxx.png)`，出处写在图片下一行
     「来源：……」，同时记进私有 `素材来源.md`（不进本仓库）。自制图只作兜底，只用于有出处的数据，图注或「来源：」行写「自制」和数据来源（W18）。
   - 小标题想要序号就手写「一、」「二、」，不用 `:::` 容器、callout、`![[ ]]`。
   - **改稿交给 `topmind-revise`**（`mode=embed genre=long sources=<文章名>/素材来源.md`）：
     它按 core-voice 改写、跑 `de_ai_lint.py` / `revise_check.py` / `count_words.py`，把终稿和三行摘要
     （字数前后、未核实条数、保留的提示）回给本技能，完整报告落 `out/改稿报告.md`。
     没装 revise 时按随包 `references/revision-workflow.md` 手动走：⓪ 结构 → 逻辑与事实 → 删冗余 → 去 AI 味 → 排版，
     `python3 scripts/de_ai_lint.py <文章名>.md --genre long` 的 W 每条有结论（改掉或写保留理由），H 只供判断。
   - 体检：`python3 scripts/check_article.py <文章名>/` E 级清零（五项 frontmatter、H1 = title = 文件名、
     图片存在且编号跟出现顺序一致、无容器和 wikilink）。草稿期封面还没做只给 W5、占位截图只给 W4，
     `status` 改成定稿后这两项升级成 E7 / E3。frontmatter 可以加可选的 `subtitle`（副标题，md2x-html 只在页顶预览里给出，不进复制内容）。
   - **到这里就是默认交付**：一份 `<文章名>.md`。用户没说要 X 版，就不生成 HTML。
1. **按需：转 HTML**（用户说「出 X 版 / 一键复制 / X 长文 HTML」时）：
   ```bash
   python3 scripts/md2x-html.py <文章名>/<文章名>.md
   # → <文章名>/out/X长文.html；封面缺省读 frontmatter 的 cover
   ```
   直接读源稿里的 `![]()`，按文档顺序嵌图，不需要再派生 `X长文.md`，也不手工拼 `--images`。
   单文件 HTML：内联样式 + 配图 base64 内嵌。浏览器打开后点页顶
   「一键复制全文」，富文本（含格式）进剪贴板，去 X 文章编辑器粘贴。
   转换规则见 `references/x-html-format.md`。
   - `#` 首个标题**不进剪贴板**：手动填入 X 标题栏（工具栏有三步话术提示）。
   - 每张配图自动编号 `[图N]`。「一键复制全文」只带文字和格式，配图位置换成 `[图N]` 占位段
     （X 不认 data-URI 随文粘贴，几 MB base64 还会拖垮剪贴板）；粘贴后在每个 `[图N]` 处
     点该图下「复制图片」→ Cmd/Ctrl+V，或「下载图片」后上传，再删掉占位。
   - 图片下一行的「来源：」渲染成小号灰字图注，随正文一起复制。
   - 复制按顺序降级：copy 事件 + `execCommand('copy')`（同步，file:// 与聊天附件预览等
     iframe 里也能用）→ `navigator.clipboard.write(ClipboardItem)` → `writeText` →
     自动全选正文并提示按 Cmd/Ctrl+C。每一步都有 toast，不会静默失败。
     点击图片弹出 lightbox 放大看原图（右键可另存/截图，不拦截右键菜单）。
   - 每个 ``` 提示词块渲染为引用块（X 可识别）+ 右上角「复制提示词」按钮，
     一键复制该块纯文本。**复制分双通道**：作者侧用 HTML 里的按钮（发布前取用文本）；
     读者侧一键复制只能来自 X 原生代码块，需在编辑器里 Insert → Code 手动逐块转换
     （X 原生代码块带 native copy button；粘贴 `<pre>` 会被 X 丢弃，走不过去）。
     详见 `references/x-html-format.md`「提示词的复制链路（双通道）」。
   - 封面只在页顶预览 + 提供下载；**封面始终在 X 编辑器单独上传**（X 有独立封面入口）。
2. **按需：转纯文本**（兜底）：`python3 scripts/md2x.py <文章名>/<文章名>.md` → `out/X发布稿.txt`，
   规则见 `references/x-format.md`。HTML 复制异常时的备用入口。
   **列表**：纯文本不渲染 Markdown 列表，`md2x.py` 默认把 `- ` / `1. ` 转成「· 」/「1）」
   （二级缩进两格，最多两层）；`--list-style emoji` 可选 🔹 / ▫️ / 1️⃣，`keep` 保留原符号。
   规则见 `references/x-post-format.md`；交付规约见 **`references/x-delivery-contract.md`（必读必守）**：长文是规约里写明的例外——`X长文.html` / `X发布稿.txt` 里合理的文内链接照常保留（lint 用 `--long`，不查 E10–E12）；但信源清单、封面、说明仍另列，不糅进稿子。从长文再派生 X 短帖时按短文规则：一段可复制纯文本，链接、原图另发。转完可跑 `python3 scripts/lint_x_post.py out/X发布稿.txt --long` 自检。
   转完**通读一遍**：X 不渲染 markdown，标记剥离后断句、emphasis 全靠文字本身，
   读不顺就回源稿改。
   注意区分两条链路：`X长文.html` 走 X Article 编辑器的富文本，**原生列表保留**（以 `references/x-html-format.md` 为准）；
   只有 `X发布稿.txt` 这种纯文本兜底稿，以及短帖（→ `topmind-viral-posts` / `topmind-briefs`）才需要把列表改成纯文本写法。
3. **封面图**：调 `topmind-cover`，平台选 `x`，得 1500×600 主图，放进 `cover/`，frontmatter 的 `cover` 指向它。
4. **发布清单**：按 `references/publish-checklist.md` 逐项过。
5. **发布**：用户在 X Article 编辑器粘贴全文、上传封面与配图（按 `[图N]` 编号），
   人工点发布。**API 不发长文**（topmind-x 的 xurl 只覆盖短推文）。
6. **收尾**：frontmatter 的 `status` 改「已发布」；记录发布时间与链接；全文抓回核对一遍（标题、数字、图序）。

## 目录约定

```
<文章名>/
├── <文章名>.md        # 唯一源稿：改稿永远只改它
├── images/            # 01-xxx.png、02-xxx.png…，按正文出现顺序编号
├── cover/             # cover-1500x600.png 等（topmind-cover 产出，X 编辑器单独上传）
├── 素材来源.md        # 私有：图源、承重事实来源、未核实条目
├── raw/               # 原始下载、截图、笔记（不发布）
└── out/               # 按需生成，可随时重建，不手改
    ├── X长文.html     # 首选复制入口：浏览器打开，一键复制全文
    ├── X发布稿.txt    # 纯文本兜底入口
    └── 改稿报告.md    # topmind-revise 的完整报告
```

旧结构（`公众号稿.md` + 派生 `X长文.md` + `[图N]`）只读兼容：
`python3 scripts/md2x-html.py X长文.md --out X长文.html --images-from 公众号稿.md` 仍可用，不自动迁移。

## 派生规则（历次配图错位与重号的结论）

- **单源**：只改 `<文章名>.md`，改完重新派生 `out/`；`out/` 里的文件不手改，不另存一份 X 稿。
- **图跟着文字走**：图片行紧跟它证明的那段文字（最多隔一段）；改稿移动段落时，图片行一起搬。
- **编号 = 出现顺序**：`images/` 文件名编号与正文出现顺序一致，`check_article.py` 不一致就报 E4。
  曾因按文件名排序手工传 `--images`（文件名顺序 ≠ 文档顺序）导致从某张图起整段错位一格；
  现在 `md2x-html.py` 直接按文档顺序读 `![]()`，不再允许手工排序。
- **序号不叠加**：小标题手写「一、」时原样保留，派生时不再加序号（曾出现「一、一、」重号）。
- **构建后必查**：HTML 体积（有图时 MB 级）、data-URI 数量 = 图片数（+1 封面）、无 `:::` 残留；
  抽查每张图前后几行是否出现该图主题词，章节题图只查节标题相关性。
- **封面不占编号**：正文图按 `[图1]…[图N]` 编号，封面单独上传；`X发布稿.txt` 的 `[图N]` 与 HTML 一致。

## 实战沉淀

- **事实（硬约束）**：承重事实（数字、排名、发布日期、融资额）逐条回一手来源
  （官方公告/模型卡/论文/财报）；厂商给的数字标"厂商口径"或"官方口径"；
  媒体转引标"据 XX 报道"（点名媒体，不写泛泛的「据报道」）；查不到一手来源的传闻删；
  未来判断用「预计」「大概率」「现在看起来」，附一条支撑事实，不写「我认为」，与事实段落切割，不混写。改稿续写时正文已有数字回源重核（上一轮文本最不可信）。
- **文字**：去 AI 味、精炼、不编造；看图即得的简单事实不再展开复述；
  多用第三方客观素材，观点可以撞、表达必须原创。
- **交付**：发布/分享时直接用交付的 HTML 原文件原样呈现，不临时重新生成版本。
- **长文改稿**：用户嫌稿子长、AI 味重时，交给 `topmind-revise`（`mode=revise genre=long`）；没装时按 `references/revision-workflow.md`、`references/information-design.md`（结构和篇幅）和 `references/image-sourcing.md`（图先于字）整改，场景写法以 `references/core-voice.md` 为准：
  公式化标签改平实说法（「三个词」→「简单总结」、「五个分支」→「主要 5 个方向」、「三件事」→「有三大特征」）；
  过去一句话 + 图、现在汇总加分析、未来写判断（「预计」「大概率」）+ 一条支撑事实；原图（官方截图、原始 X 帖、官方文书、第三方数据图）先于文字，
  自制图只用于有出处的数据；一段 2–3 句、不超过约 110 字。每张图的来源 URL 记在本地私有信源清单，不进公开仓库。
- 补充信息（邀请码、链接、勘误）**不挤正文**，发在发布后首条评论并置顶
- 标题 ≤140 字符，写清讲什么（core-voice V01）；开头用具体事实，接地气、好懂（V05）；配图逐张按 `[图N]` 顺序上传，传完对照清单点一遍
- 事实修正只改源稿再重新派生，不回头改已发原文（除非勘误）
- 提示词密集型文章（如 N 条直出提示词），发布时建议把提示词引用块逐块转为
  X 原生代码块（Insert → Code → 粘贴 → 删原块，每块约 10 秒）：这是 X 平台唯一可靠的
  读者侧一键复制链路（原生代码块带 native copy button，已实测确认）
- X 编辑器不认剪贴板里的 data-URI 图片：**全文复制只带文字和格式，图片一律按 `[图N]` 手动补**，
  不要承诺一键带图
- **复制按钮失效（实踩）**：旧版只用 `navigator.clipboard.write`，在 file:// 未授权、
  聊天附件预览（沙箱 iframe、无 clipboard-write）里被拒，`writeText` 降级同样被拒 → 只弹"复制失败"；
  旧版还把 6.4MB base64 塞进 text/html。现已改为 execCommand 同步优先 + 图片占位，
  改动后用无头 Chrome 在 file://、http、两种沙箱 iframe 下回读剪贴板验证
- **图片手动补位**：每张图下有「复制图片」按钮，
  把 PNG 以 `image/png` 写进剪贴板，X 编辑器支持直接粘贴图片
  （X 认图片粘贴，不认 data-URI 随文粘贴）。流程：点「复制图片」→
  去 X 编辑器对应位置 Ctrl/Cmd+V。失败时回退到「下载图片」再上传。
  封面同理有「复制封面图」按钮

## When NOT to use

- 短推文 / 短帖 / 快讯 / 段子写稿 → `topmind-viral-posts`（引流互动型）或 `topmind-briefs`（信息密度型）
- 把短帖发出去 → `topmind-x`（发帖连接器，须用户确认）
- 公众号 → `topmind-wechat-post`
- 只要封面、头图 → `topmind-cover`
- 只想存档不发布 → `topmind-capture`
- 写稿（只有发布需求、无原稿时）→ 先走写作技能再回本技能

## 外部依赖

以下技能**不在本仓库**（由宿主智能体环境另行提供）；缺失时对应路由能力不可用，
本技能核心流程（原稿转文本、封面、发布清单）不受影响：

- `topmind-x`（topmind-skills 包）：短推文发帖连接器，须用户确认后才发；xurl 只覆盖短推文，不发长文。
- `topmind-capture`：「只想存档不发布」时的收录路由。

## 写作原则

写作原则见 [references/social-writing-principles.md](references/social-writing-principles.md)（第 0 层）和 [references/information-design.md](references/information-design.md)（第 1 层）；研究类选题按 [references/research-mode.md](references/research-mode.md)；目录和交付规约见 [references/workspace.md](references/workspace.md)。触发本技能时默认执行。
