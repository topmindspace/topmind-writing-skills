# 封面风格库（19 种）

> 想自己写提示词直接丢给 AI 生图（不走技能流程）？看 [`cover-prompts.md`](./cover-prompts.md)——
> 19 风格完整可拷贝提示词 + 全平台爆款封面流派调研。

> **原创铁律**：本库示例图均为原创，只演示抽象设计原则（标题是视觉重心、信息分层、留白呼吸感、数字与关键词强调），不临摹任何第三方封面；复用时版式与配色不得与第三方封面构成实质相似——只学原则，不学版式。

选风格先看题材，再看系列延续性。同一系列固定一个模板，只换主体与标题字。
选风格三步走：**先选风格 → 看 `assets/examples/` 对应示例图 → 按本库配方组 prompt**。

prompt 配方为中英双语模板：`{TITLE}` 为标题文字占位符（短标题 4~8 字）、其余占位符见各风格说明。尺寸固定 1500×600、横构图 5:2。标题字逐字写进 prompt；生成后第一件事就是检查标题字。

## 安全区铁律（所有风格通用）

900×383 公众号版是从 1500×600 主图**中央裁剪**（左右各裁约 3%）；
X 与公众号在手机端信息流里，左右边缘可能被平台图标/时间/转发按钮轻微遮挡：
**标题字与关键主体必须落在左右各 10% 安全边距之内**
（左右各预留 10% 不放标题字与关键主体），否则会被裁掉或遮挡。
垂直方向上下各预留 5%。
选风格、组 prompt、检查成图时都要先过这一条。

## 原创铁律（所有风格通用）

本库的 prompt 配方沉淀的是**抽象设计原则**——标题是视觉重心、信息分层、
留白与呼吸感、数字与关键词的强调手法——**不是任何具体版式**。
**版式与配色也不得与第三方封面构成实质相似：只学原则，不学版式。**
禁止照抄任何第三方封面的文案、形象、版式结构与配色组合——包括但不限于
标题文字、数字、品牌词、IP 形象、署名，以及"左文右图""底部标签条""两行撞色标题"
这类可辨识的构图公式。`assets/examples/` 中的 26 张风格示例图均为原创设计，
其标题/数字/品牌/署名（如"深蓝 OS 2.0""提示词避坑指南""读书打卡计划""@书山有路"）
均为虚构演示内容，仅用于演示设计原则。
用本库组 prompt 时，标题、形象、版式细节必须自己原创；
改图时只换主体与标题字，保留本风格的配色故事与设计原则。

---

## 9. gan-huo · 爆款干货

- **适用场景**：干货清单、评测、盘点、实测筛选类文章；"我替你试完了/筛完了"这类
  第一人称实测文的默认选择。示例图：`assets/examples/gan-huo.png`（原创："工具测评精选"）。
- **设计语言（抽象原则）**：
  - 标题是绝对视觉重心：居中大字，一眼即主题。
  - 信息分层三层：顶部眉题小字（给上下文）→ 中央大标题（给主题）→ 角落印章小数字（给数据点）。
  - 数字强调手法：数字不做彩色大字，收进印章/徽章做"小而精"的点睛。
  - 留白与呼吸感：深色底 + 大面积空旷，克制干练。
- **配色故事**：深炭灰 `#2B2B30` 做主色（沉稳、可信）；暖橙 `#FF8A3D` 只做细线点缀；
  朱红印章做一处跳色；标题米白高对比。
- **标题写法规范**：
  - 短标题 4~8 字，如"提示词避坑指南"；标题居中，字号约为画面高度 30%。
  - 顶部眉题小字交代筛选口径（如"12种写法 · 逐条实测"），字号约为标题的 30%。
  - 数据（如"18篇"）放右上角朱红印章内，白字，不放大。
- **标题文案提炼公式**：实测数字 + 翻车/打脸结果 + 省时间承诺。
  示例（虚构演示）："实测18篇：避开7个坑"。
- **prompt 配方**：
  ```
  中文：爆款干货风中文封面。字体量级：全图只有一个视觉重心——中央米白色超粗黑中文标题"{TITLE}"（逐字准确），标题字高占画面 1/3，与深底形成最大明度差；顶部小字眉题"{EYEBROW}"（筛选口径，如"18篇 · 逐条实测"）只做开场，字号约为标题的 1/3。配色系统：深炭灰 #2B2B30 全幅深底（沉稳可信，走极端明度）；暖橙 #FF8A3D 只做细线框点缀；朱红 #E6392B 方形印章（右上角，内写白色小字"{NUMBER}"）是全图唯一的跳色、唯一的记忆点。构图能量：一条纵向主阅读动线——眉题（为什么信）→ 大标题（这是什么）→ 印章（数据背书）；左下角一只小巧原创小形象（{CHARACTER}，占画面约15%）做动线落点，绝不遮挡标题。质感细节：深底必须加一层细腻胶片噪点颗粒 + 一道极淡的斜向光影，拒绝死平纯色的塑料感。文字特效：标题里挑钩子词做三处装饰，全句只用米白、朱红、暖橙三种颜色——①把一个钩子词（如“翻车”）换成朱红 #E6392B，其余字保持米白；②另一个钩子词下方垫一块朱红 #E6392B 实色矩形，色块高度为字高的 1.2 倍，米白字压在色块上、明暗对立（色块衬底的字不再换色）；③用暖橙 #FF8A3D 马克笔笔触把标题里的数字钩子（如“7”）圈起来，圈略大于字、不压笔画，只圈一处。除标题、眉题、印章、形象外无其他文字；所有文字与关键元素避开左右各 5% 的边缘区域，横构图5:2，尺寸1500×600。

  EN: High-impact Chinese viral-listicle cover. Type scale: exactly one visual anchor — a centered off-white extra-bold Chinese title "{TITLE}" (exact), glyph height 1/3 of the frame, maximum brightness contrast against the dark ground; a small top eyebrow "{EYEBROW}" (selection criteria, e.g. "18 posts, tested one by one") opens the read at ~1/3 of the title size. Color system: full-bleed deep charcoal #2B2B30 ground (steady, credible, extreme-dark value); warm-orange #FF8A3D hairline frame accents only; one vermilion #E6392B square seal at top-right with white micro-text "{NUMBER}" — the single hot-color accent and the single memorable element on the page. Composition energy: one vertical reading path — eyebrow (why trust) → giant title (what it is) → seal (data proof); a tiny original mascot ({CHARACTER}, ~15% of frame) sits bottom-left as the path's landing point, never covering the title. Texture: the dark ground must carry one layer of fine film grain plus one faint diagonal light sweep — flat lifeless solid color is forbidden. Text effects: decorate the hook words with exactly three treatments — only off-white, vermilion, and warm orange in the sentence: ① recolor one hook word (e.g. “翻车”) in vermilion #E6392B, keep the rest off-white; ② slide a solid vermilion #E6392B rectangle under another hook word, block height 1.2× glyph height, off-white type over it with opposing light-dark contrast (block-backed words are not recolored); ③ circle the title's number hook (e.g. “7”) with a warm-orange #FF8A3D marker stroke, the circle slightly larger than the glyphs, never touching strokes, only one circle. No other text. All text and key elements clear of the 5% edge margins on left and right. Landscape 5:2, 1500×600.
  ```
  占位符：`{EYEBROW}` 眉题（≤10 字）、`{NUMBER}` 印章内数字（如"18篇"，必须真实）、
  `{CHARACTER}` 原创小形象描述（如"纸飞机造型蓝色小机器人"），不得照抄任何现有 IP 形象。
- **绝不清单**：
  - 绝不小字标题：标题字高不足画面 1/4，整张作废。
  - 绝不把数字做成彩色大字抢标题：数字只进印章，标题里不再出现第二个数字钩子。
  - 绝不浅底：本风格必须是深底，浅底直接变味。
  - 绝不底部标签条/胶囊条：卖点只进眉题小字。
  - 绝不死平纯色底：无噪点无光影的"塑料底"一律重画。
  - 绝不透视/扭曲/弧形排大标题：中文必乱码，要动感用色块和圈注代替。
  - 绝不标题里超 3 种颜色：字色只许米白+朱红，暖橙圈注已是第三种，多一色就"吵"。
  - 绝不竖排+旋转组合：大标题永远水平；旋转只许右上印章≤8°。
  - 绝不色块吞字：色块高度≤1.3 倍字高，米白字压朱红块、明暗对立。
  - 绝不装饰压笔画：圈注只圈标题里一个数字钩子、不压笔画。
  - 绝不装饰超量：单图只用变色+色块+圈注 3 种，多一种即乱。

---

## 5. big-type · 巨字宣言

- **适用场景**：观点评论、深度长文、产品/版本发布宣言；"一句话立场"类文章的默认选择。
  示例图：`assets/examples/big-type.png`（原创："少即是多"）。
- **设计语言（抽象原则）**：
  - 标题即画面：单行超大，字形本身做文章（书法笔意 / 描边 / 烫金质感均可）。
  - 副标题是注解：陈述句，解释标题，不提问、不煽动。
  - 明亮底色反衬：用"亮"制造宣言的从容感，而非暗黑压迫感。
- **配色故事**：奶油底 `#FAF3E7`（温暖、纸感）；墨黑标题字；烫金 `#C9A227`
  只做笔画点缀，一处即够。
- **标题写法规范**：
  - 短标题 4~8 字，单行，横跨画面宽度约 80%，如"慢即是快"。
  - 副标题用陈述句（如"慢公司的效率哲学"），字号约为标题的 25%。
- **标题文案提炼公式**：反常识断言（4~6 字）+ 陈述句注解。
  示例（虚构演示）："少，才是多"。
- **prompt 配方**：
  ```
  中文：巨字宣言风中文封面。字体量级：标题即画面——单行超大墨黑中文标题"{TITLE}"（逐字准确），横跨画面约85%宽度，字高占画面 1/3~2/5；{TYPE_STYLE}（墨黑书法体配烫金 #C9A227 描边 / 空心描边字 / 竖排大字三选一），字形本身就是情绪；标题下方深灰色陈述句副标题"{SUBTITLE}"只做注解，字号约为标题的 1/4。配色系统：明亮奶油 #FAF3E7 全幅亮底（宣言的从容感，走极端明度）；墨黑标题字；烫金 #C9A227 只点缀一处笔画或一字，是全图唯一的强调。构图能量：一条横向主阅读动线——巨标题横扫全场（钩子与主题合一）→ 副标题收束落点；背景只留极淡的金色几何线条，全部给标题让路。质感细节：奶油底必须带细腻纸纹 + 书法笔锋的飞白质感，拒绝干净单调的平板底。文字特效：冲击力全在字形上，全句颜色不超过 3 种——①标题里的钩子词（如反常识断言词“暴跌”）字号放大到其余字的 1.5 倍，其余字保持原字号，不换行；②描边按 {TYPE_STYLE} 选型量化：“书法烫金”选型只给一处笔画或一字勾烫金 #C9A227 细描边（描边宽不超过笔画宽的 1/5，防笔画粘连）；“空心描边字”选型用 2px 深灰描边、字内留白；③字后方加一层同字形、浅墨灰色、向右下错位 4px 的字，只错位一层，制造轻微立体感；描边与立体已是两种效果，绝不再加阴影。除标题与副标题外无其他文字；所有文字避开左右各 5% 的边缘区域，横构图5:2，尺寸1500×600。

  EN: Giant-type manifesto Chinese cover. Type scale: the title IS the image — one single-line oversized ink-black Chinese title "{TITLE}" (exact), spanning ~85% of frame width, glyph height 1/3 to 2/5 of the frame; {TYPE_STYLE} (ink-black calligraphy with gold #C9A227 edge accents / outlined hollow type / vertical type) — the letterforms carry the emotion; a small dark-gray declarative subtitle "{SUBTITLE}" below only annotates, at ~1/4 of the title size. Color system: full-bleed bright cream #FAF3E7 ground (extreme-light value, the calm of a manifesto); ink-black title; gold #C9A227 accents exactly one stroke or one character — the single emphasis on the page. Composition energy: one horizontal reading path — the giant title sweeps the frame (hook and theme in one) → the subtitle lands the read; the background keeps only whisper-faint gold geometric lines, everything yields to the title. Texture: the cream ground must carry fine paper grain plus dry-brush flying-white texture in the calligraphy strokes — a clean flat ground is forbidden. Text effects: all impact lives in the letterforms — at most 3 colors in the line: ① enlarge the hook word (e.g. the contrarian claim word) to 1.5× the other glyphs, keep the rest at base size, no line break; ② quantify the outline per {TYPE_STYLE}: the “gold calligraphy” option outlines only one stroke or one glyph in a gold #C9A227 hairline (outline width ≤ 1/5 of stroke width, no stroke merging); the “hollow outline” option uses 2px dark-gray outline with empty interior; ③ add one same-glyph layer behind the type in light ink-gray, offset 4px down-right, a single offset only, for a subtle 3D lift; outline plus 3D is already two effects — never add a drop shadow. No other text. All text clear of the 5% edge margins on left and right. Landscape 5:2, 1500×600.
  ```
  占位符：`{TYPE_STYLE}` 字形处理三选一（书法烫金 / 描边空心 / 竖排），
  `{SUBTITLE}` 陈述句副标题（≤10 字，禁止问句）。
- **绝不清单**：
  - 绝不两行撞色标题：本风格只做单行（或竖排），两行撞色是别人的版式。
  - 绝不暗黑背景：本风格必须是亮底，暗底直接变味。
  - 绝不问句/煽动式副标题：副标题只能是陈述句注解。
  - 绝不标题字高不足 1/4：字一小，宣言感全失。
  - 绝不出现第二处烫金：强调色只给一处，多一处就"吵"。
  - 绝不透视变形大标题：要动感用轻微立体代替。
  - 绝不一句话超 3 种颜色（含描边色、立体层颜色）。
  - 绝不描边+阴影+立体三重叠加：本风格只用描边+轻微立体两种，绝不再加阴影。
  - 绝不竖排+旋转组合：竖排字形不叠加任何旋转；旋转只许印章/标签类小元素≤8°，单行大标题永远水平。
  - 绝不描边过粗：描边宽≤笔画宽 1/5，粗了笔画粘连。
  - 绝不装饰超量：字号对比+描边+轻微立体 3 种封顶。

---

## 10. brand-launch · 品牌发布

- **适用场景**：产品发布、版本更新、官方最佳实践/白皮书；有明确品牌主体的内容首选。
  示例图：`assets/examples/brand-launch.png`（原创虚构品牌"晨光 3.0"）。
- **设计语言（抽象原则）**：
  - 标题视觉重心居中置顶：品牌名就是标题，不藏不绕。
  - 氛围代替写实：用发光线条/光影做产品氛围，不画写实产品大图（防 AI 乱码也防呆板）。
  - 卖点信息分层：一排分隔符小字（"更快 · 更稳 · 更懂你"），轻量不做图标条。
- **配色故事**：深海军蓝 `#0A1F44` 做全幅主色（深邃、专业）；荧光绿 `#3DFF88`
  做唯一强调色（发光描边、细线、分隔符小字都用它）。
- **标题写法规范**：
  - 品牌词前置并上色："深蓝"用荧光绿发光描边，其余白字；短标题 4~8 字。
  - 标题下一条荧光绿细线收束视觉。
  - 底部一排分隔符小字卖点，格式 `更快 · 更稳 · 更懂你`，浅灰白小字。
- **标题文案提炼公式**：品牌词前置 + 版本号做钩子 + 卖点小字给承诺。
  示例（虚构演示）："曙光 5.0：快三倍"。
- **prompt 配方**：
  ```
  中文：品牌发布风中文封面。字体量级：品牌名就是标题——顶部居中大号白色粗黑中文标题"{TITLE}"（逐字准确），字高占画面 1/4~1/3，其中品牌词"{KEYWORDS}"做色块衬底（见"文字特效"段）、其余纯白，是全图唯一的视觉重心；标题下一条荧光绿细线收束视觉，紧跟一排浅灰白分隔符小字卖点"{SELLING_POINTS}"（如"更快 · 更稳 · 更懂你"）做背书。配色系统：深海军蓝 #0A1F44 全幅深底（深邃专业，走极端明度）；荧光绿 #3DFF88 是唯一的强调色（色块衬底、细线、卖点小字都用它，别处不再出现第二种颜色）。构图能量：一条纵向主阅读动线——品牌大标题（定调）→ 细线+卖点小字（背书）→ 中央下方荧光绿发光线条勾勒的抽象产品氛围（{PRODUCT}，线框/光影、无可读文字）做氛围落点；左上预留空白 logo 区。质感细节：深蓝底必须加一层细腻星尘噪点 + 中央一团柔和的荧光绿光晕渐变，拒绝死黑平板底。文字特效：贵气来自克制，全句只用纯白、荧光绿、深海军蓝三种颜色——①品牌词“{KEYWORDS}”下方垫一块荧光绿 #3DFF88 实色矩形，色块高度为字高的 1.2 倍，字换成深海军蓝 #0A1F44 粗体压在色块上、明暗对立（色块替代原荧光绿发光描边写法，不叠加）；②其余纯白标题字加一层向右下 45° 的柔和投影，投影偏移为字高的 1/10，黑色 30% 不透明度、柔和不脏；阴影不加在品牌词上，同一字不同时叠加描边和阴影。除标题、卖点小字外无其他文字；所有文字避开左右各 5% 的边缘区域，横构图5:2，尺寸1500×600。

  EN: Brand-launch Chinese cover. Type scale: the brand name IS the title — a large white extra-bold Chinese title "{TITLE}" (exact) centered at top, glyph height 1/4 to 1/3 of the frame; the brand term "{KEYWORDS}" glows in fluorescent-green outline, the rest pure white — the single visual anchor of the page; one thin fluorescent-green rule cinches the eye below the title, followed by one row of light-gray separator-style selling points "{SELLING_POINTS}" (e.g. "更快 · 更稳 · 更懂你") as proof. Color system: full-bleed deep navy #0A1F44 ground (deep, professional, extreme-dark value); fluorescent green #3DFF88 is the ONLY accent color (glowing outlines, hairlines, selling-point micro-text all use it — no second color anywhere). Composition energy: one vertical reading path — brand title (sets the tone) → rule plus selling points (proof) → an abstract product atmosphere drawn in glowing fluorescent-green lines ({PRODUCT}, wireframe and light, no readable text) lower-center as the atmospheric landing; empty logo area reserved top-left. Texture: the navy ground must carry fine stardust grain plus one soft fluorescent-green halo glow at center — a dead flat black ground is forbidden. Text effects: premium comes from restraint — only pure white, fluorescent green, and deep navy in the line: ① slide a solid fluorescent-green #3DFF88 rectangle under the brand term “{KEYWORDS}”, block height 1.2× glyph height, type set in deep-navy #0A1F44 bold over it with opposing light-dark contrast (the block replaces the glowing-outline treatment — never stacked); ② the remaining pure-white title glyphs get one soft drop shadow at 45° down-right, offset 1/10 of glyph height, black at 30% opacity, soft and clean; no shadow on the brand term — one glyph never carries outline and shadow together. No other text. All text clear of the 5% edge margins on left and right. Landscape 5:2, 1500×600.
  ```
  占位符：`{KEYWORDS}` 品牌词、`{PRODUCT}` 产品氛围描述、`{SELLING_POINTS}` 分隔符小字（≤12 字）；
  真实 logo 必须后期贴图，绝不用 AI 生成 logo。
- **绝不清单**：
  - 绝不渐变彩虹标题：强调色只用荧光绿一种，第二种颜色出现即杂。
  - 绝不写实产品大图/UI 截图：只要发光线框氛围，可读 UI 文字必出乱码。
  - 绝不图标式卖点条：卖点只用一排分隔符小字。
  - 绝不 AI 生成 logo：真实 logo 必须后期贴图。
  - 绝不死黑无光影的底：无星尘无光晕的平板深底一律重画。
  - 绝不透视变形大标题：要动感用轻微阴影代替。
  - 绝不一句话超 3 种颜色：本风格只有纯白、荧光绿、深海军蓝三种。
  - 绝不描边+阴影+立体三重叠加：品牌词用色块（无阴影），纯白字用阴影（无描边），同一字不同时叠加。
  - 绝不竖排+旋转组合：大标题永远水平；旋转只许小元素≤8°。
  - 绝不色块吞字：色块高度≤1.3 倍字高，深蓝字压荧光绿块、明暗对立。
  - 绝不装饰超量：色块+轻微阴影 2 种封顶。

---

## 6. tutorial-steps · 教程步骤

- **适用场景**：教程、上手指南、分步实操、保姆级攻略。
  示例图：`assets/examples/tutorial-steps.png`（原创："三步学会烘焙"）。
- **设计语言（抽象原则）**：
  - 标题做视觉锚：墨色书法题字，一字千钧，镇住画面。
  - 步骤沿横向时间线展开：一条线串起线框数字，数字是节奏点不是徽章。
  - 东方留白：大面积宣纸空，步骤区只占底部一条。
- **配色故事**：宣纸米 `#F2EDE0` 做底（温润）；墨黑书法标题；赭石 `#B5651D`
  只做时间线与线框数字。
- **标题写法规范**：
  - 大标题 4~8 字，墨色书法体，如"从想法到产品"，占画面高度约 25%。
  - 时间线：赭色水平细线 + 三个线框空心数字 `01 02 03`，每数字下一句极简短句（≤4 字）。
  - 右上角小字点睛（如"先懂逻辑，再动手"）。
- **标题文案提炼公式**："从A到B"动词句 + 步数做钩子。
  示例（虚构演示）："3步做出小程序"。
- **prompt 配方**：
  ```
  中文：教程步骤风中文封面。字体量级：标题做视觉锚——顶部中央墨色毛笔书法体大字标题"{TITLE}"（逐字准确），字高占画面约 1/3，一字千钧镇住全场；底部时间线上三个线框空心大数字"{N1}""{N2}""{N3}"是节奏钩子，字号约为标题的 1/2，每数字下方配极简短句"{S1}""{S2}""{S3}"（每句≤4字）；右上角小字点睛"{TIP}"（≤8字）只做注脚。配色系统：宣纸米 #F2EDE0 全幅底（温润，走极端浅明度）；墨黑书法标题；赭石 #B5651D 只给时间线细线与线框数字，是全图唯一的强调色。构图能量：一条"镇场→展开"动线——顶部书法大标题定调 → 右上点睛提示 → 底部横向时间线横向展开三步；大面积宣纸留白，步骤区只占底部一条。质感细节：宣纸底必须带淡墨晕染纹理 + 细腻纸纤维质感，拒绝死白平板底。文字特效：教程风靠“划重点”指路，全句只用墨黑、赭石两种颜色——①标题里的关键词（如动词“做出”）换成赭石 #B5651D，其余字保持墨黑；②在关键词下方画一条手绘感波浪下划线，赭石 #B5651D，线宽为笔画宽度的 1/2，略带抖动、不压笔画；装饰只用这 2 种，不再加箭头。除上述文字外无其他文字；所有文字避开左右各 5% 的边缘区域，文人气、克制，横构图5:2，尺寸1500×600。

  EN: Tutorial-steps Chinese cover. Type scale: the title is the visual anchor — a large ink-brush calligraphy title "{TITLE}" (exact) top-center, glyph height ~1/3 of the frame, one stroke worth a thousand words holding the whole page; on the bottom timeline, three large wireframe hollow numbers "{N1}" "{N2}" "{N3}" act as rhythm hooks at ~1/2 the title size, each with a minimal short phrase below ("{S1}" "{S2}" "{S3}", max 4 characters each); a small accent note "{TIP}" (max 8 characters) top-right as footnote only. Color system: full-bleed rice-paper beige #F2EDE0 ground (warm, extreme-light value); ink-black calligraphy title; ochre #B5651D reserved for the timeline hairline and hollow numbers — the single accent color on the page. Composition energy: one "command then unfold" path — the calligraphy title sets the tone → the top-right note hints → the horizontal timeline unfolds three steps across the bottom; vast rice-paper negative space, the steps occupy only one bottom band. Texture: the paper ground must carry faint ink-bleed texture plus fine paper-fiber grain — a dead flat white ground is forbidden. Text effects: the tutorial voice “marks the key point” — only ink black and ochre in the line: ① recolor the title's keyword (e.g. the verb) in ochre #B5651D, keep the rest ink black; ② draw one hand-drawn wavy underline beneath the keyword in ochre #B5651D, line width 1/2 of stroke width, slightly wobbly, never touching strokes; only these 2 treatments — no arrows. No other text. All text clear of the 5% edge margins on left and right. Scholarly, restrained. Landscape 5:2, 1500×600.
  ```
  占位符：`{N1..N3}` 线框数字（01/02/03）、`{S1..S3}` 短句（每句 ≤4 字，越短越安全）、
  `{TIP}` 右上点睛（≤8 字）。
- **绝不清单**：
  - 绝不红笔刷横条标题：本风格的强调色只有赭石。
  - 绝不纵向步骤卡拼贴+箭头：步骤只沿底部横向时间线展开。
  - 绝不实心圆形序号章：数字只用线框空心。
  - 绝不步骤超过 3 个：超过 3 个立刻变说明书。
  - 绝不无纹理的死白底：无墨韵无纸纤维的平板底一律重画。
  - 绝不透视变形大标题。
  - 绝不标题超 3 种颜色：本风格只用墨黑+赭石两种，多一色就杂。
  - 绝不竖排+旋转组合：大标题永远水平。
  - 绝不装饰压笔画：下划线线宽≤笔画宽 1/2，不压字。
  - 绝不装饰超量：变色+手绘下划线 2 种封顶，不再加箭头。

---

## 11. ip-fun · IP 趣味

- **适用场景**：实战案例、数据战报、复盘、系列连载（上/下篇）。
  示例图：`assets/examples/ip-fun.png`（原创：戴眼镜的小刺猬 IP + "读书打卡计划"）。
- **设计语言（抽象原则）**：
  - 暖色氛围做主角情绪：整张的"热气"是第一眼记忆。
  - 标题顶部叠放压阵：深棕大字在上，IP 形象在下半部做记忆点舞台，
    禁止左右对半分区。
  - 数字收进角落印章：数据是注脚，不是标题。
  - 署名做边角点缀：竖排小字，不进主视觉流。
- **配色故事**：橙黄暖色 `#FF9E2C → #FFC53D` 做主色（阳光、热闹）；
  标题与副标题用深棕 `#4A2C0A`（在暖底上最稳的重色）；
  朱红 `#E6392B` 只做右下印章，是全图唯一的跳色。
- **标题写法规范**：
  - 大标题 4~8 字深棕粗黑顶部叠放，字高占画面 1/4~1/3，如"读书打卡计划"；
    下方深棕小字副标题（如"每天一幅 · 进化看得见"）。
  - 数据（如"30天"）放右下角圆形印章内小字，不放大。
  - 署名（如"@书山有路"）放左下角竖排小字。
- **标题文案提炼公式**：天数挑战 + 动词结果。
  示例（虚构演示）："30天读书打卡"。
- **prompt 配方**：
  ```
  中文：IP 趣味风中文封面。字体量级：标题压阵——顶部叠放深棕色（#4A2C0A）超大粗黑中文标题"{TITLE}"（逐字准确），字高占画面 1/4~1/3；下方深棕色小字副标题"{SUBTITLE}"（≤12字）只做注解；标题与 IP 形象上下叠放，禁止左右对半分区。配色系统：橙黄暖色 #FF9E2C → #FFC53D 全幅主色（阳光热闹，走高饱和暖色）；深棕 #4A2C0A 标题在暖底上形成对比重心；右下角圆形印章内"{NUMBER}"小字（必须真实）用朱红 #E6392B，是全图唯一的跳色注脚。构图能量：一条对角线动线——顶部大标题（情绪钩子）→ 下半部原创趣味 IP 形象（{CHARACTER}，如戴贝雷帽的狐狸画家在画架前作画，暖色调，约占画面40%）做记忆点舞台 → 右下印章（数据注脚）收束；左下角竖排小字署名"{BYLINE}"做边角点缀，不进主视觉流。质感细节：暖色底必须加一层细腻纸纹颗粒 + 一团柔和的阳光光晕，拒绝塑料感平滑渲染。文字特效：潮玩感来自“贴纸+徽章”，全句颜色不超过 3 种——①标题里的关键词（如挑战词“接单”）原位下方垫一块深棕 #4A2C0A 实色矩形（色块在字下方、标题总字数不变，严禁把关键词复制一份做成独立元素），色块高度为字高的 1.2 倍，字换成米白色压在色块上、明暗对立；②标题字后方加一层同字形、朱红 #E6392B、向右下错位 4px 的字，只错位一层，做出徽章凸起的轻微立体感；色块与立体已是两种效果，不再加描边和阴影。除上述文字外无其他文字；所有文字避开左右各 5% 的边缘区域，横构图5:2，尺寸1500×600。

  EN: Fun-IP Chinese cover. Type scale: the title holds the fort — a stacked top dark-brown (#4A2C0A) extra-bold Chinese title "{TITLE}" (exact), glyph height 1/4 to 1/3 of the frame, with a small dark-brown subtitle "{SUBTITLE}" (max 12 characters) below as annotation only; title and IP character stack vertically — a left-right split layout is forbidden. Color system: warm orange-yellow #FF9E2C → #FFC53D full-bleed ground (sunny, high-saturation warmth); the dark-brown #4A2C0A title forms the contrast anchor on the warm ground; a small round seal bottom-right with "{NUMBER}" micro-text (must be factual) in vermilion #E6392B — the single accent footnote on the page. Composition energy: one diagonal reading path — top title (emotion hook) → an original playful IP character ({CHARACTER}, e.g. a beret-wearing fox painter at an easel, warm tones, ~40% of frame) staging the lower half as the memorable element → bottom-right seal (data footnote) closes the read; a small vertical byline "{BYLINE}" bottom-left as a corner garnish, kept out of the main visual flow. Texture: the warm ground must carry fine paper-grain plus a soft sunlight halo — plasticky smooth rendering is forbidden. Text effects: the collectible-toy feel comes from “sticker plus badge” — at most 3 colors in the line: ① slide a solid dark-brown #4A2C0A rectangle under the title's keyword in place (e.g. the challenge word; block sits beneath the glyphs, total character count unchanged — never duplicate the keyword as a separate element), block height 1.2× glyph height, off-white type over it with opposing light-dark contrast; ② add one same-glyph layer behind the title in vermilion #E6392B, offset 4px down-right, a single offset only, for a badge-like subtle 3D lift; block plus 3D is already two effects — never add outline or shadow. No other text. All text clear of the 5% edge margins on left and right. Landscape 5:2, 1500×600.
  ```
  占位符：`{SUBTITLE}` 副标题（≤12 字）、`{NUMBER}` 印章内数字（如"30天"，必须真实）、
  `{BYLINE}` 边角署名（如"@书山有路"）、`{CHARACTER}` 原创趣味 IP 形象描述，
  必须与主题道具绑定（如绘画主题 → 狐狸画家 + 画架），不得照抄任何现有 IP 形象。
- **绝不清单**：
  - 绝不左文右图对半分：标题与形象必须上下叠放/错位，禁止左右镜像分区。
  - 绝不巨型彩色数字做标题：数字只进印章，且必须在正文中有出处。
  - 绝不冷色调主色：本风格必须是暖色，冷底直接变味。
  - 绝不形象遮挡标题字：形象是记忆点舞台，占比可到 40%，但吃字就作废。
  - 绝不塑料感平滑渲染：无纸纹无颗粒的"CG 塑料感"一律重画。
  - 绝不透视变形大标题：要动感用轻微立体代替。
  - 绝不一句话超 3 种颜色。
  - 绝不描边+阴影+立体三重叠加：本风格只用色块+轻微立体，不再加描边和阴影。
  - 绝不竖排+旋转组合：左下竖排署名保持不转；旋转只许右下印章≤8°，大标题永远水平。
  - 绝不色块吞字：色块高度≤1.3 倍字高，米白字压深棕块、明暗对立。
  - 绝不装饰超量：色块+立体 2 种封顶。

---

## 20. orange-warm · 橙色暖阳风

- **用在哪**：生活方式、美食、旅行、亲子、温暖治愈类内容。
- **配色故事**：活力橙（#FF6B35）→ 蜜桃渐变 → 奶油白，暖阳般的热情亲和。
- **字体**：白色 Display 级巨标题压橙色渐变底；点题词用深棕描边。
- **透视/景深**：暖光粒子前景虚化；中景主体清晰；背景橙色光晕。
- **绝不**：橙色过饱和刺眼；白色标题在浅橙上对比不足。

---

## 21. sketch-cartoon · 卡通素描风

- **用在哪**：创意、手作、儿童、轻松科普、幽默内容。
- **配色故事**：牛皮纸底 + 手绘线稿 + 卡通平涂上色，亲切手作感。
- **字体**：手写体标题 + 描边；点题词用彩色马克笔高亮。
- **透视/景深**：纸纹质感；元素手绘风格统一；轻微透视。
- **绝不**：线稿潦草难认；上色溢出线稿；风格不统一（一半写实一半卡通）。

---

## 22. cyber-neon · 赛博霓虹风

- **用在哪**：AI前沿、科幻、极客、游戏、未来科技。
- **配色故事**：深空黑（#0A0A0F）+ 霓虹蓝/品红/青，全息投影质感。
- **字体**：霓虹发光标题（多层光晕）；故障艺术（glitch）点缀；等宽字体英文。
- **透视/景深**：全息投影层次；霓虹光轨；数字雨/网格背景；强烈透视。
- **绝不**：霓虹色超过 3 种；发光过强导致标题难读；背景抢标题风头。

---

## 1. white-clean · 白色清新

- **适用场景**：干货清单、实测盘点、效率/副业/职场类选题；"替你筛好了、看完即用"类
  亲和干货的默认选择。示例图：`assets/examples/white-clean.png`（原创："远程工作效率手册"）。
- **设计语言（抽象原则）**：
  - 纯白底 + 大面积留白：干净清新，信息流里"透气"。
  - 标题极大：空间允许时字高冲击画面 1/3；1~2 行横跨顶部，关键词撞色。
  - 关键词装饰每次只用 2~3 种：撞色变色 / 马克笔横条衬底 / 色块衬底。
  - 场景化插图：3D 毛绒 / Q 版人物 + 与主题绑定的工作场景（悬浮卡片、工具、桌面），
    插图讲"正在用"的故事，不做无意义装饰。
  - 圆角胶囊标签行：浅色胶囊 + 小图标 + 短词，收束卖点。
  - 小装饰点到为止：星星、感叹号、波浪线，至多 2 处。
- **配色故事**：纯白 `#FFFFFF` 全幅主色（走极端浅明度）；标题墨黑 `#1A1A1A` 打底；
  撞色只给标题关键词（优选组合三选一，见配方）；胶囊用撞色对应的浅色系。
- **标题写法规范**：
  - 短标题 6~10 字，1~2 行，顶部横跨，空间允许时字高冲击 1/3（底线 ≥1/4），
    如"一人公司起步指南"。
  - 每行至多 1 个撞色关键词。
  - 胶囊标签行 3 个短词，`·` 分隔（如"实测筛选 · 长文精选 · 全流程实操"），
    字号约为标题的 1/4。
- **标题文案提炼公式**：人群/场景 + 结果承诺。
  示例（虚构演示）："打工人副业增收课"。
- **prompt 配方**：
  ```
  中文：白色清新风中文封面。字体量级：标题是绝对视觉重心——顶部横跨墨黑色（#1A1A1A）超大粗黑中文标题"{TITLE}"（逐字准确），1~2 行，空间允许时字高冲击画面 1/3（底线≥1/4）；中部一条浅色圆角胶囊标签行"{TAGLINE}"（如"实测筛选 · 长文精选 · 全流程实操"，必须真实）收束卖点，字号约为标题的 1/4。字体优选组合 {FONT_COMBO} 三选一：A 超粗黑体（力量感，笔画粗、字面满）/ B 圆润黑体（亲和感，笔画圆润、字角圆）/ C 黑体正文 + 英文关键词斜体（国际感）。配色系统：纯白 #FFFFFF 全幅主色（极端浅明度，大面积留白）；标题墨黑 #1A1A1A 打底；撞色优选组合 {COLOR_COMBO} 三选一：A 品牌蓝 #2B7FFF + 活力橙红 #FF5A2E / B 电光紫 #7C5CFF + 薄荷青 #00C2A8 / C 墨黑 #1A1A1A + 品牌蓝 #2B7FFF，撞色只给标题关键词（每行至多 1 个撞色词）；胶囊用撞色对应的浅色（如 #EAF2FF 系）。构图能量：一条"主题→背书→场景"动线——顶部大标题横跨全宽（钩子与主题合一）→ 中部胶囊标签行（背书）→ 底部场景化插图舞台（{SCENE}，如毛绒质感 3D 小角色在悬浮卡片与主题工具之间忙碌、带柔和投影，约占画面 35%，必须与主题绑定、讲"正在用"的故事）做记忆点落点；标题与插图上下叠放，禁止左右对半镜像分区。花式优选组合 {FX_COMBO} 每次只用 2~3 种：①关键词变色高亮（撞色，见配色组合）；②黄色 #FFD93B 马克笔横条衬底（横条略宽于字、不压笔画）；③关键词原位垫实色块（色块高度为字高的 1.2 倍，字色与色块明暗对立，标题总字数不变、严禁复制关键词做独立元素）。方向/透视优选组合 {DIR_COMBO} 三选一：A 标题全水平、胶囊轻微错位叠放；B 撞色关键词整体上扬 ≤8°（字不转、整体转）；C 插图轻微俯视透视、标题保持水平。大标题永远水平，绝不透视变形。质感细节：纯白底必须带一层极淡的纸纹 + 插图区一团柔和的浅色光晕，拒绝死白平板底。除标题、胶囊行外无其他文字；所有文字与关键元素避开左右各 5% 的边缘区域，横构图 5:2，尺寸 1500×600。

  EN: Clean-white Chinese cover. Type scale: the title is the absolute visual anchor — an oversized ink-black (#1A1A1A) extra-bold Chinese title "{TITLE}" (exact) spanning the top in 1–2 lines, glyph height pushing toward 1/3 of the frame when space allows (floor 1/4); one light rounded-capsule tag row "{TAGLINE}" (e.g. "实测筛选 · 长文精选 · 全流程实操", must be factual) mid-page cinches the selling points at ~1/4 of the title size. Font combo {FONT_COMBO}, pick one of three: A ultra-bold heiti (powerful, heavy strokes, full letterforms) / B rounded heiti (friendly, soft strokes, rounded corners) / C heiti body with italic English keywords (international feel). Color system: full-bleed pure white #FFFFFF ground (extreme-light value, generous negative space); ink-black #1A1A1A title base; accent combo {COLOR_COMBO}, pick one of three: A brand blue #2B7FFF + vivid orange-red #FF5A2E / B electric purple #7C5CFF + mint teal #00C2A8 / C ink black #1A1A1A + brand blue #2B7FFF — accents touch title keywords only (at most one accented word per line); capsules use the matching light tints (e.g. the #EAF2FF family). Composition energy: one "theme → proof → scene" path — the giant title spans the top (hook and theme in one) → the capsule tag row (proof) → a scenario illustration stage at the bottom ({SCENE}, e.g. a fluffy 3D mascot busy among floating cards and topic tools with soft shadows, ~35% of frame, must tie to the topic and tell a "being used" story) as the memorable landing; title and illustration stack vertically — a mirrored left-right split is forbidden. Flourish combo {FX_COMBO}, use only 2–3 per image: ① keyword recolor highlight (accent color per the palette combo); ② yellow #FFD93B marker highlighter bar behind a keyword (bar slightly wider than the glyphs, never touching strokes); ③ solid color block under a keyword in place (block height 1.2× glyph height, opposing light-dark contrast, total character count unchanged — never duplicate the keyword as a separate element). Direction/perspective combo {DIR_COMBO}, pick one of three: A fully horizontal title with slightly offset-stacked capsules; B the accented keyword tilted upward ≤8° as a whole (glyphs not rotated, the block rotated); C illustration in slight top-down perspective while the title stays horizontal. The main title is always horizontal — never warped in perspective. Texture: the white ground must carry one whisper-faint paper grain plus one soft light-tint halo in the illustration zone — a dead flat white ground is forbidden. No text besides the title and capsule row. All text and key elements clear of the 5% edge margins on left and right. Landscape 5:2, 1500×600.
  ```
  占位符：`{TAGLINE}` 胶囊标签行（3 短词，`·` 分隔，≤14 字，必须真实）、
  `{SCENE}` 场景化插图描述（必须与主题绑定：角色 + 场景 + 主题道具，讲"正在用"的故事）、
  `{FONT_COMBO}` 字体三选一（A 超粗黑 / B 圆润黑 / C 黑体+英文斜体）、
  `{COLOR_COMBO}` 撞色三选一（A 蓝+橙红 / B 紫+青 / C 黑+品牌蓝）、
  `{FX_COMBO}` 花式每次 2~3 种（变色 / 马克笔横条 / 色块衬底）、
  `{DIR_COMBO}` 方向三选一（A 全水平 / B 关键词上扬≤8° / C 插图俯视）。
- **绝不清单**：
  - 绝不深底/灰底：本风格必须是纯白底，底色一深直接变味。
  - 绝不标题字高不足 1/4：空间允许必须冲击 1/3。
  - 绝不左右对半镜像分区：标题与插图必须上下叠放。
  - 绝不每行超 1 个撞色词：撞色一多就"吵"。
  - 绝不一句话超 3 种颜色：标题内只许墨黑 + 撞色组合的两种。
  - 绝不透视变形大标题：大标题永远水平。
  - 绝不色块吞字：色块高度≤1.3 倍字高，明暗对立。
  - 绝不装饰压笔画：横条/圈注不压字。
  - 绝不装饰超量：花式 2~3 种封顶，小装饰（星星/感叹号）至多 2 处。
  - 绝不无意义插图：插图必须与主题绑定、讲"正在用"的故事，纯装饰角色一律不用。

### 震撼升级包（2026-10-01：白色清新不等于平淡）

白色清新的"清新"是干净通透，不是寡淡。以下 6 种手法按需选用 2~3 种，
是本风格从"好看"到"震撼"的升级开关：

1. **前景压字（破框而出）**：3D 角色/主题物件从画面底部升起，压住标题下 1/4，
   标题上 3/4 保持清晰可读。字与形象前后穿插，制造"破框而出"的空间纵深——
   这是电影海报最常用的震撼手法。压字处加一层柔和投影，字不脏。
2. **字体的雕塑感**：标题拒绝 plain font block——超粗黑体 + 1px 深色描边 +
   向右下 3px 的同色深一号投影，三层做出"刻出来"的体积感；或给撞色关键词
   加轻微挤压变形（竖向压 95%），字形本身就有张力。
3. **纵深三层**：远景（极淡的撞色光晕/大面积留白）→ 中景（标题横幅）→
   前景（角色/物件/纸片，带真实投影）。三层明暗拉开，拒绝所有元素贴在一个平面上。
4. **对角线动能**：主体元素沿左下→右上对角线排布（如纸片飞散、角色攀爬），
   打破全水平构图的呆板；标题本身永远水平，动能交给元素走位。
5. **体积光**：一束柔和的斜向光从左上打下来，照亮标题区，背景形成自然的明暗渐变——
   光就是最便宜的"震撼"。
6. **撞色只给一处、给足**：纯白底上撞色天然醒目。选定一个撞色（如电光紫 #7C5CFF
   或活力橙红 #FF5A2E），只给标题里的 1 个关键词 + 1 个小元素（如印章/胶囊），
   别处一律黑白灰。少即是多，多即是吵。

升级版 prompt 追加段（拼在原配方末尾）：
```
震撼升级：{UPGRADE}（从上方 6 种选 2~3 种，如"前景压字+体积光"）。纵深三层必须拉开：
远景淡光晕 → 中景标题 → 前景主体带投影；标题雕塑感（描边+投影）拒绝 plain font block；
对角线动能由元素走位承担，标题保持水平。
```

---

## 2. bg-blur · 背景虚化

- **适用场景**：生活方式、职场日常、运动健康、城市观察；"氛围感 + 主题"类文章的
  默认选择。示例图：`assets/examples/bg-blur.png`（原创："城市晨跑指南"）。
- **设计语言（抽象原则）**：
  - 虚化摄影背景 + 清晰前景主体：大光圈景深对比本身就是记忆点。
  - 背景走浅色调虚化（明亮、通透），拒绝暗黑压抑。
  - 前景主体锐利清晰，与主题强绑定（人物半身 / 产品特写 / 主题物件三选一）。
  - 大标题压在清晰区：空间允许时字高冲击 1/3，字色与背景明度对立。
  - 光斑/柔光只做氛围，不进文字区。
- **配色故事**：浅色虚化摄影背景（米白 / 浅灰 / 柔光，极端浅明度）；标题深色
  （墨黑 / 深棕）；强调色只给一处（关键词或一处光斑色）。
- **标题写法规范**：
  - 短标题 6~10 字，单行或双行，压在画面清晰区，空间允许时字高冲击 1/3（底线 ≥1/4）。
  - 标题字加浅色光晕衬底或细描边，保证在虚化背景上可读。
- **标题文案提炼公式**：场景 + 痛点/获得。
  示例（虚构演示）："通勤包里的效率术"。
- **prompt 配方**：
  ```
  中文：背景虚化风中文封面。字体量级：大标题压在清晰区——深色超大粗黑中文标题"{TITLE}"（逐字准确），单行或双行，空间允许时字高冲击画面 1/3（底线≥1/4），是全图唯一的视觉重心；标题字加一层浅色光晕衬底（或 2px 浅色描边，描边宽≤笔画宽 1/5），保证在虚化背景上清晰可读。字体优选组合 {FONT_COMBO} 三选一：A 超粗黑体（醒目）/ B 人文黑体（亲和）/ C 粗黑 + 数字/英文斜体混排。配色系统：浅色调虚化摄影背景 {BG_SCENE}（极端浅明度：明亮、通透，拒绝暗黑）；标题深色（墨黑 #1A1A1A / 深棕二选一）；强调色优选组合 {COLOR_COMBO} 三选一：A 暖橙 #FF8A3D（配光斑）/ B 品牌蓝 #2B7FFF / C 朱红 #E6392B，强调色只给标题关键词一处。构图能量：一条"氛围→主体→主题"动线——浅色虚化背景（氛围，大光圈虚化 + 柔和光斑，不进文字区）→ 清晰前景主体（{SUBJECT}，锐利清晰、约占画面 30~40%，必须与主题强绑定）→ 大标题压在主体旁的清晰区（主题）；背景与主体明暗/虚实对立，景深对比就是记忆点。花式优选组合 {FX_COMBO} 每次只用 2 种：①关键词变色高亮（强调色）；②关键词字号放大到其余字的 1.4 倍（不换行）。方向/透视优选组合 {DIR_COMBO} 三选一：A 标题全水平、主体三分法站位；B 标题沿主体轮廓轻微上扬 ≤8°；C 前景主体轻微仰视透视、标题保持水平。大标题不做透视变形。质感细节：背景虚化必须有真实的光斑层次 + 前景主体边缘锐利，拒绝"全图均匀模糊"的假虚化。除标题外无其他文字；所有文字与关键主体避开左右各 5% 的边缘区域，横构图 5:2，尺寸 1500×600。

  EN: Background-blur Chinese cover. Type scale: the big title presses the sharp zone — an oversized dark extra-bold Chinese title "{TITLE}" (exact), one or two lines, glyph height pushing toward 1/3 of the frame when space allows (floor 1/4), the single visual anchor of the page; the title carries one light halo backing (or a 2px light outline, outline width ≤ 1/5 of stroke width) so it stays legible over the blur. Font combo {FONT_COMBO}, pick one of three: A ultra-bold heiti (punchy) / B humanist heiti (friendly) / C bold heiti mixed with italic numerals/English. Color system: light-toned blurred photographic background {BG_SCENE} (extreme-light value: bright, airy — dark and moody is forbidden); dark title (ink black #1A1A1A / deep brown, pick one); accent combo {COLOR_COMBO}, pick one of three: A warm orange #FF8A3D (pairs with bokeh) / B brand blue #2B7FFF / C vermilion #E6392B — the accent touches exactly one title keyword. Composition energy: one "atmosphere → subject → theme" path — the light blurred background (atmosphere: wide-aperture blur plus soft bokeh, kept out of the text zone) → the sharp foreground subject ({SUBJECT}, tack-sharp, 30–40% of frame, must tie strongly to the topic) → the big title pressed into the clear zone beside the subject (theme); background and subject oppose in light and in sharpness — the depth-of-field contrast IS the memorable element. Flourish combo {FX_COMBO}, use only 2 per image: ① keyword recolor highlight (accent color); ② keyword enlarged to 1.4× the other glyphs (no line break). Direction/perspective combo {DIR_COMBO}, pick one of three: A fully horizontal title with the subject on a rule-of-thirds position; B the title rising gently ≤8° along the subject's contour; C the foreground subject in slight low-angle perspective while the title stays horizontal. The main title is never warped in perspective. Texture: the background blur must show real bokeh layering, and the foreground subject must have crisp edges — uniformly blurred "fake bokeh" is forbidden. No text besides the title. All text and key subjects clear of the 5% edge margins on left and right. Landscape 5:2, 1500×600.
  ```
  占位符：`{BG_SCENE}` 背景虚化场景三选一（明亮办公室虚化 / 城市街景光斑虚化 / 自然柔光虚化，
  必须浅色调）、`{SUBJECT}` 清晰前景主体三选一（人物半身 / 产品特写 / 主题物件，
  必须与主题强绑定）、`{FONT_COMBO}` 字体三选一、`{COLOR_COMBO}` 强调色三选一
  （橙/蓝/朱红，只给一处）、`{FX_COMBO}` 花式 2 种（变色 + 字号对比）、
  `{DIR_COMBO}` 方向三选一。
- **绝不清单**：
  - 绝不暗黑虚化背景：本风格背景必须是浅色调，暗底直接变味。
  - 绝不全图均匀模糊：背景虚化必须有光斑层次，前景主体必须锐利。
  - 绝不标题落在虚化重灾区：标题必须压在清晰区，否则可读性全失。
  - 绝不标题字高不足 1/4：空间允许必须冲击 1/3。
  - 绝不一句话超 3 种颜色：深色标题 + 一处强调色。
  - 绝不透视变形大标题。
  - 绝不光斑进文字区：光斑只做背景氛围。
  - 绝不主体与主题无关：前景主体必须与主题强绑定，无意义摆拍一律不用。
  - 绝不装饰超量：变色 + 字号对比 2 种封顶。

---

## 3. paper-collage · 纸感拼贴

- **适用场景**：手账、整理术、生活灵感、旧物改造、轻教程；"手作感 / 人味"类选题的
  默认选择。示例图：`assets/examples/paper-collage.png`（原创："旧物改造计划"）。
- **设计语言（抽象原则）**：
  - 浅色底 + 纸片拼贴：撕边 / 圆角 / 便签纸片错位叠放，拼贴本身就是构图。
  - 固定手法三选一：和纸胶带 / 回形针 / 图钉，"贴上去"的真实感。
  - 标题落在最大纸片上（或牛皮纸标签），空间允许时字高冲击 1/3。
  - 小贴纸 / 小标签点缀，元素总数 ≤5。
  - 手工感：撕纸毛边、胶带半透明，拒绝 CG 塑料感。
- **配色故事**：米白 / 浅灰底（极端浅明度）；纸片用马卡龙浅色系优选组合
  （浅蓝 / 浅粉 / 浅黄 / 浅绿三选一）；标题深色；一处跳色（朱红 / 赭石）只给最小的标签。
- **标题写法规范**：
  - 短标题 4~8 字，印在最大纸片中央，空间允许时字高冲击 1/3（底线 ≥1/4），如"手账整理术"。
  - 纸片上不加第二行小字，干净。
- **标题文案提炼公式**：旧物 / 日常 + 动词改造。
  示例（虚构演示）："工位改造计划"。
- **prompt 配方**：
  ```
  中文：纸感拼贴风中文封面。字体量级：标题是视觉重心——深色超大粗黑中文标题"{TITLE}"（逐字准确），印在最大纸片中央，空间允许时字高冲击画面 1/3（底线≥1/4）；纸片上不加第二行小字。字体优选组合 {FONT_COMBO} 三选一：A 超粗黑体（海报感）/ B 手写体（人味，笔画清晰可辨）/ C 黑体 + 英文小字混排。配色系统：米白 / 浅灰底（极端浅明度）；纸片马卡龙浅色系优选组合 {COLOR_COMBO} 三选一：A 浅蓝 #D6E9FF + 浅黄 #FFF3C4 / B 浅粉 #FFDCE5 + 浅绿 #D9F2E2 / C 牛皮纸 #E8DCC8 + 纯白 #FFFFFF；标题深色（墨黑 / 深棕二选一）；跳色只给最小的标签一处（朱红 #E6392B / 赭石 #B5651D 二选一）。构图能量：一条"底→纸片→标题"动线——浅色底（呼吸）→ 3~5 张纸片 {PAPER_COMBO} 错位叠放拼贴（撕边 / 圆角 / 便签三选一，纸片带撕纸毛边与柔和投影）→ 最大纸片上的大标题（主题）；纸片用 {FIX_COMBO} 固定（和纸胶带 / 回形针 / 图钉三选一，半透明/金属质感真实）；1~2 张小贴纸或小标签做点缀（元素总数 ≤5）。花式优选组合 {FX_COMBO} 每次只用 2 种：①标题关键词变色（跳色）；②小标签上手写感圈注（只圈一处）。方向/透视优选组合 {DIR_COMBO} 三选一：A 纸片全水平、错位叠放；B 最大纸片整体倾斜 ≤8°（字不转、纸转）；C 轻微俯视拼贴桌面、标题保持水平。大标题不做透视变形。质感细节：纸片必须有撕纸毛边 + 纸纹 + 柔和投影，胶带半透明，拒绝 CG 塑料感。除标题、小标签短词外无其他文字；所有文字与关键纸片避开左右各 5% 的边缘区域，横构图 5:2，尺寸 1500×600。

  EN: Paper-collage Chinese cover. Type scale: the title is the visual anchor — an oversized dark extra-bold Chinese title "{TITLE}" (exact) printed at the center of the largest paper scrap, glyph height pushing toward 1/3 of the frame when space allows (floor 1/4); no second line of small text on the scrap. Font combo {FONT_COMBO}, pick one of three: A ultra-bold heiti (poster feel) / B handwriting style (human touch, strokes clean and legible) / C heiti mixed with small English. Color system: off-white / light-gray ground (extreme-light value); pastel paper palette combo {COLOR_COMBO}, pick one of three: A light blue #D6E9FF + light yellow #FFF3C4 / B light pink #FFDCE5 + light green #D9F2E2 / C kraft #E8DCC8 + pure white #FFFFFF; dark title (ink black / deep brown, pick one); one pop of color reserved for the smallest tag only (vermilion #E6392B / ochre #B5651D, pick one). Composition energy: one "ground → scraps → title" path — the light ground (breathing room) → 3–5 paper scraps {PAPER_COMBO} in offset collage (torn edge / rounded corner / sticky-note, pick one; scraps carry torn fibrous edges and soft shadows) → the big title on the largest scrap (theme); scraps fastened with {FIX_COMBO} (washi tape / paper clip / push pin, pick one, realistic translucent/metal texture); 1–2 small stickers or tags as garnish (at most 5 elements total). Flourish combo {FX_COMBO}, use only 2 per image: ① title keyword recolor (pop color); ② hand-drawn circle on a small tag (only one circle). Direction/perspective combo {DIR_COMBO}, pick one of three: A all scraps horizontal in offset stack; B the largest scrap tilted ≤8° as a whole (glyphs not rotated, the scrap rotated); C slight top-down view of the collage desk while the title stays horizontal. The main title is never warped in perspective. Texture: scraps must show torn fibrous edges plus paper grain plus soft shadows, tape translucent — plasticky CG rendering is forbidden. No text besides the title and small tag words. All text and key scraps clear of the 5% edge margins on left and right. Landscape 5:2, 1500×600.
  ```
  占位符：`{PAPER_COMBO}` 纸片三选一（撕边 / 圆角 / 便签）、`{FIX_COMBO}` 固定手法三选一
  （和纸胶带 / 回形针 / 图钉）、`{FONT_COMBO}` 字体三选一、`{COLOR_COMBO}` 纸片配色三选一、
  `{FX_COMBO}` 花式 2 种（变色 + 圈注）、`{DIR_COMBO}` 方向三选一。
- **绝不清单**：
  - 绝不深底：本风格必须是浅色底。
  - 绝不纸片超 5 张：元素总数 ≤5，多一张就碎。
  - 绝不标题字高不足 1/4：空间允许必须冲击 1/3。
  - 绝不 CG 塑料感：无毛边无纸纹无投影的纸片一律重画。
  - 绝不透视变形大标题。
  - 绝不一句话超 3 种颜色。
  - 绝不纸片上加第二行小字。
  - 绝不装饰超量：变色 + 圈注 2 种封顶。

---

## 4. news-flash · 资讯快报

- **适用场景**：资讯、快讯、热点解读、人物专访预告、"祛魅/揭秘"类选题。
  示例图：`assets/examples/news-flash.png`（原创："科技周报精选"）。
- **设计语言（抽象原则）**：
  - 标题是绝对视觉重心：单色大字，一眼即主题，快讯的干脆来自"不加修饰"。
  - 信息分层三层：顶部眉题小字（给栏目/时效）→ 中央大标题（给主题）→
    右下角落生活静物（给"正在发生"的现场感）。
  - 点缀手法：俯视桌面静物（报纸/咖啡/闹钟）给氛围，点缀不进文字区。
  - 纸感来自质感：纸纹米底 + 大面积空旷，留白就是呼吸感。
- **配色故事**：纸纹米 `#F4F1E8` 做主色（纸感、阅读感）；标题以纯黑为主打底、爆点关键词做朱红点睛
  （快讯的干脆来自纯黑的利落，朱红只给爆点词一处）；静物保留真实色彩（红闹钟是唯一跳色，小面积）。
- **标题写法规范**：
  - 短标题 4~6 字，纯黑粗黑单行，如"今日AI速览"，字高占画面约 1/3。
  - 顶部眉题小字交代栏目/时效（如"晨间快讯 · 每日更新"），字号约为标题的 25%。
  - 感叹号/问号至多一个；标题里彩色只给爆点关键词一处（朱红）。
- **标题文案提炼公式**：时间范围 + 领域 + "速览/必看"。
  示例（虚构演示）："一周AI大事"。
- **prompt 配方**：
  ```
  中文：资讯快报风中文封面。字体量级：标题是绝对视觉重心——左上纯黑色单行超大粗黑中文标题"{TITLE}"（逐字准确），字高占画面 1/3；标题以纯黑为主打底，爆点关键词做朱红点睛（见“文字特效”段），其余字一律纯黑；标题上方顶部眉题小字"{EYEBROW}"（栏目/时效，如"晨间快讯 · 每日更新"，必须真实）交代上下文，字号约为标题的 1/4。配色系统：纸纹米 #F4F1E8 全幅主色（纸感、阅读感，走极端浅明度）；标题纯黑单色——单色是本风格的魂；右下角俯视桌面静物（{PROPS}，如一叠报纸、一杯冒热气的咖啡、一只红色小闹钟，2~3件）保留真实色彩，其中红色小闹钟是全图唯一的跳色。构图能量：一条"时效→主题→现场"动线——眉题（时效）→ 大标题（主题）→ 右下静物（"正在发生"的现场感落点）；静物只做氛围点缀，绝不进文字区。质感细节：纸底必须带干净细腻的纸纹 + 一处真实的纸张折痕或柔和阴影，拒绝死平无质感的白底，也拒绝做旧脏污。文字特效：突发感靠“爆点词炸出来”，标题里只用纯黑、朱红两种颜色——①标题里的爆点关键词（如“暴跌”）换成朱红 #E6392B，其余字保持纯黑；②爆点词字号放大到其余字的 1.5 倍，其余字保持原字号，不换行；③从标题向右下静物方向画一条朱红 #E6392B 手绘箭头，只画一条，线条粗细均匀、不压字，制造“正在发生”的现场感。除标题、眉题、静物外无其他文字；所有文字与关键元素避开左右各 5% 的边缘区域，横构图5:2，尺寸1500×600。

  EN: News-flash Chinese cover. Type scale: the title is the absolute visual anchor — a huge solid-black single-line extra-bold Chinese title "{TITLE}" (exact) at upper-left, glyph height 1/3 of the frame; monochrome IS the attitude, zero colored characters inside the title; a small top eyebrow "{EYEBROW}" (column/timeliness, e.g. "晨间快讯 · 每日更新", must be factual) sets context above the title at ~1/4 of the title size. Color system: full-bleed paper-beige #F4F1E8 ground (extreme-light value); pure-black monochrome title; a top-down desk still life bottom-right ({PROPS}, e.g. a stack of newspapers, a steaming coffee cup, a small red alarm clock, 2–3 items), the small red alarm clock the single accent color on the page. Composition energy: one "timeliness → theme → scene" path — eyebrow (timeliness) → big title (theme) → bottom-right still life (the "happening now" landing); the still life is atmosphere only, never entering the text zone. Texture: the paper ground must carry clean fine paper grain plus one real paper crease or soft shadow — a dead flat textureless ground is forbidden, and so is grimy distressed aging. Text effects: breaking-news energy comes from the “exploding” keyword — only pure black and vermilion in the title: ① recolor the title's breaking keyword (e.g. “暴跌”) in vermilion #E6392B, keep the rest pure black; ② enlarge the keyword to 1.5× the other glyphs, keep the rest at base size, no line break; ③ draw one vermilion hand-drawn arrow from the title toward the bottom-right still life, a single arrow with even line weight, never covering glyphs, for the “happening now” feel. No other text. All text and key elements clear of the 5% edge margins on left and right. Landscape 5:2, 1500×600.
  ```
  占位符：`{EYEBROW}` 眉题（栏目/时效，≤10 字）、`{PROPS}` 桌面静物描述（2~3 件，
  与主题相关，如报纸/咖啡/闹钟）。
- **绝不清单**：
  - 绝不两行撞色标题：标题必须单行（纯黑打底、爆点词朱红点睛），撞色+感叹号是别人的版式。
  - 绝不标题里出现第二个彩色：彩色只给爆点关键词一处（朱红），多一处就“吵”。
  - 绝不透视变形大标题：要动感用字号对比+箭头。
  - 绝不一句话超 3 种颜色：标题里只许纯黑+朱红两种。
  - 绝不竖排+旋转组合：大标题永远水平；旋转只许小元素≤8°。
  - 绝不箭头压字或超过 1 条：只画一条手绘箭头，不压笔画。
  - 绝不装饰超量：变色+字号对比+箭头 3 种封顶。
  - 绝不胶囊形副标题条：时效只进眉题小字。
  - 绝不静物进文字区：静物超过 3 件或压字，整张作废。
  - 绝不做旧脏纸纹：要干净纸纹 + 一处真实折痕，拒绝"脏"和"死平"两个极端。

---

## 7. minimal · 极简留白

- **适用场景**：随笔、书评、轻观点、生活感悟；公众号"轻阅读"类文章，
  或系列中需要"呼吸感"的穿插封面。
  示例图：`assets/examples/minimal.png`（原创："独处指南"）。
- **设计语言（抽象原则）**：
  - 留白是主角：≥60% 空旷，呼吸感就是信息。
  - 点缀手法：一枚朱红印泥圆点做第一眼点睛，一处微小水墨笔触（银杏叶）
    做呼吸，细节精致、位置克制。
  - 标题写法：中等字号 + 字重 Bold + 字距拉宽，轻、慢、稳里藏着分量——
    "慢"的味道全在字距和字重里。
  - 元素总数 ≤3（点睛+点缀+标题），多一件都是负担。
- **配色故事**：冷白 `#F5F6F4` 做主色（干净、冷静）；淡墨只做点缀；
  一枚朱红 `#C73E2C` 印泥圆点是全图唯一的点睛色；
  标题用深灰，不用纯黑（纯黑太"重"，极简感全失）。
- **标题写法规范**：
  - 短标题 4~8 字，如"慢思考"；字距拉宽；字体用 Noto Sans SC Bold
    （比 Medium 重一级，用字重而非字号制造张力；仍不用 Black，太重则极简感全失）。
  - 不加副标题、不加标签条，克制到底。
- **标题文案提炼公式**：一个"慢/轻/少"字眼 + 一个具体生活词。
  示例（虚构演示）："慢煮生活"。
- **prompt 配方**：
  ```
  中文：极简留白风中文封面。字体量级：克制中的张力——深灰色（#3A3A38，不用纯黑）中文标题"{TITLE}"（逐字准确），字高约占画面 1/6，字重用 Bold（比 Medium 重一级，用字重而非字号制造分量），字距拉宽，"慢"的味道全在字距里；标题置于左下安全区内。配色系统：冷白 #F5F6F4 全幅主色（干净冷静，≥85% 留白，留白本身就是构图）；淡墨只做一处水墨点缀；一枚朱红（#C73E2C）印泥圆点（直径约画面 2%）是全图唯一的点睛色、唯一的记忆点。构图能量：一条极简动线——朱红点睛（第一眼）→ 淡墨银杏叶（呼吸）→ 宽字距标题（落点）；元素总数 ≤3（点睛+点缀+标题），多一件都是负担。质感细节：冷白底必须带一层极淡的宣纸纤维纹理，拒绝死白平板底；水墨笔触保留飞白的手工感。文字特效：克制到底——标题字本身不加任何装饰（不变色、不描边、不加阴影、不旋转、不下划线）；全图唯一的装饰就是那枚朱红 #C73E2C 印泥圆点点睛（直径约画面 2%，见“配色系统”段），与深灰标题字形成明暗对立；装饰种类只许这 1 种，多一种即破功。除标题外无其他文字；所有元素避开左右各 5% 的边缘区域，横构图5:2，尺寸1500×600。

  EN: Minimalist negative-space Chinese cover. Type scale: tension inside restraint — a dark-gray (#3A3A38, never pure black) Chinese title "{TITLE}" (exact), glyph height ~1/6 of the frame, set in Bold weight (one step heavier than Medium — weight, not size, carries the presence), letter-spacing stretched wide; the "slow" feeling lives in the spacing; title sits in the lower-left safe zone. Color system: full-bleed cool white #F5F6F4 ground (clean, calm, at least 85% negative space — the emptiness IS the composition); light ink wash for one brush accent only; one vermilion (#C73E2C) seal-paste dot (~2% of frame diameter) — the single accent color and the single memorable element on the page. Composition energy: one minimal path — vermilion dot (first glance) → light-ink ginkgo leaf (breathing room) → wide-tracked title (landing); at most 3 elements total (dot, accent, title), one more is a burden. Texture: the cool-white ground must carry one whisper-faint layer of rice-paper fiber texture — a dead flat white ground is forbidden; the ink stroke keeps dry-brush flying-white handmadeness. Text effects: restraint to the end — the title glyphs carry zero decoration (no recolor, no outline, no shadow, no rotation, no underline); the single decorative accent on the page is that vermilion #C73E2C seal-paste dot (~2% of frame diameter, defined in the color system above), set against the dark-gray title with opposing light-dark contrast; exactly 1 decoration type allowed — one more breaks the style. No text besides the title. All elements clear of the 5% edge margins on left and right. Landscape 5:2, 1500×600.
  ```
- **绝不清单**：
  - 绝不元素超过 3 个：对"杂物"零容忍，prompt 明确"一处""微小"，防模型加云加山。
  - 绝不纯黑标题：纯黑太"重"，极简感全失，用深灰。
  - 绝不两种以上的颜色：冷白+淡墨+一处朱红，多一色就"吵"。
  - 绝不标题贴边：留白即构图，标题必须悬在呼吸感里。
  - 绝不死白平板底：无纸纤维纹理的底一律重画。
  - 绝不使用变色/旋转/手绘装饰：标题字本身零装饰，唯一的装饰是朱红印泥圆点点睛。
  - 绝不装饰超量：装饰种类只许 1 种，多一种即破功。
  - 绝不透视变形大标题。
  - 绝不一句话超 3 种颜色：标题字色只用深灰一种。
  - 绝不竖排+旋转组合：大标题永远水平；本风格连小元素旋转也不用。

---

## 8. magazine · 杂志编辑风

- **适用场景**：深度访谈、人物特写、商业分析、年度盘点；需要"质感/信任感"时用它，
  公众号长文首选。
  示例图：`assets/examples/magazine.png`（原创："对话：匠人精神"）。
- **设计语言（抽象原则）**：
  - 质感来自克制：影棚颗粒 + 一条细色线，就是杂志感。
  - 人物手法：侧脸剪影（泛指描述）退为全幅背景氛围，给"人"的存在感但不抢标题。
  - 信息分层三层：人物氛围 → 细色线（定调）→ 标题（给主题），标题与人物上下叠放。
  - 同一色调只用一种底：浅底/深底不混用。
- **配色故事**：暖灰 `#E9E5DB` 做主色（影棚质感）；砖红 `#A63A2A` 只做一条细线点睛；
  标题炭黑，沉稳。
- **标题写法规范**：
  - 短标题 4~8 字，如"创造者访谈"；字体用 Noto Serif SC Bold（宋体感）或思源黑体 Bold。
  - 标题上方一条砖红细线是杂志感的灵魂，别省略。
- **标题文案提炼公式**：身份标签 + 反常识断言。
  示例（虚构演示）："投资人：别追风口"。
- **prompt 配方**：
  ```
  中文：杂志编辑风中文封面。字体量级：标题压前景——炭黑色典雅粗体中文标题"{TITLE}"（逐字准确，Noto Serif SC Bold 宋体感），字高占画面 1/4~1/3，居中偏下压在人物氛围之上，是全图唯一的视觉重心；标题上方一条砖红色（#A63A2A）细线定调，是杂志感的灵魂。配色系统：暖灰 #E9E5DB 全幅主色（影棚质感，走克制的中间偏浅明度）；砖红 #A63A2A 只给细线和标题关键词两处，是全图唯一的强调色；标题炭黑沉稳。构图能量：一条"氛围→定调→主题"动线——全幅低对比黑白人物侧脸剪影（{SUBJECT}，泛指描述，如穿西装的人物侧脸剪影）退为背景氛围、不抢戏 → 砖红细线（定调）→ 大标题（主题）；标题与人物上下叠放，禁止左右分区。质感细节：暖灰底必须带影棚级的细腻胶片颗粒 + 人物区一处真实的柔光阴影，拒绝塑料平滑的人像渲染。文字特效：杂志封面的强调全在标题排印上，标题里只用炭黑、砖红两种颜色——①标题里的关键词（如反常识断言词“别追”）换成砖红 #A63A2A，其余字保持炭黑；②关键词字号放大到其余字的 1.5 倍，其余字保持原字号，不换行；装饰只用这 2 种，留白处不加任何装饰字。除标题外无其他文字；所有文字避开左右各 5% 的边缘区域，克制高级，横构图5:2，尺寸1500×600。

  EN: Editorial magazine-style Chinese cover. Type scale: the title presses the foreground — an elegant charcoal-black bold Chinese title "{TITLE}" (exact, Noto Serif SC Bold with serif character), glyph height 1/4 to 1/3 of the frame, centered-lower, layered over the portrait atmosphere as the single visual anchor of the page; one thin brick-red (#A63A2A) rule above the title sets the tone — the soul of the magazine feel. Color system: full-bleed warm gray #E9E5DB ground (studio texture, restrained light-mid value); brick red #A63A2A reserved for the rule line only — the single accent color on the page; charcoal-black title, composed. Composition energy: one "atmosphere → tone → theme" path — a full-bleed low-contrast black-and-white profile silhouette ({SUBJECT}, generic description, e.g. a suited figure in profile) recedes as background atmosphere, never stealing the show → brick-red rule (tone) → big title (theme); title and figure stack vertically, a left-right split is forbidden. Texture: the warm-gray ground must carry studio-grade fine film grain plus one patch of real soft-light shadow in the figure zone — plasticky smooth portrait rendering is forbidden. Text effects: a magazine cover's emphasis lives in the title typography — only charcoal black and brick red in the title: ① recolor the title's keyword (e.g. the contrarian claim) in brick red #A63A2A, keep the rest charcoal black; ② enlarge the keyword to 1.5× the other glyphs, keep the rest at base size, no line break; only these 2 treatments — no decorative words in the negative space. No text besides the title. All text clear of the 5% edge margins on left and right. Restrained, premium. Landscape 5:2, 1500×600.
  ```
  占位符：`{SUBJECT}` 人物泛指描述（职业/姿态，不得出现可识别的真实人物长相）。
- **绝不清单**：
  - 绝不出现可识别的真实人物长相：人物必须用"泛指"描述。
  - 绝不左右分区：标题与人物必须叠放，禁止左文右图式分区。
  - 绝不浅底深底混用：同一色调只用一种底。
  - 绝不留白处加装饰字：杂志风的力量全在克制。
  - 绝不塑料平滑的人像渲染：无胶片颗粒无真实光影一律重画。
  - 绝不透视变形大标题。
  - 绝不标题超 3 种颜色：只用炭黑+砖红两种。
  - 绝不竖排+旋转组合：大标题永远水平。
  - 绝不装饰超量：变色+字号对比 2 种封顶。

---

## 12. chao-wan-3d · 3D萌系潮玩

- **适用场景**：爆款盘点、新手干货、合集清单；"消除冰冷感、让人想点开"的亲和型选题默认选择。
  示例图：`assets/examples/chao-wan-3d.png`（原创）。
- **设计语言（抽象原则）**：
  - 泡泡玛特盲盒感：毛绒/黏土质感 3D 角色是绝对主角，占画面 40%+。
  - 柔光散射：整个画面像被柔光箱照着，阴影极淡、边缘圆润。
  - 黏土拟物卡片：信息卡片做成黏土质感的小物件，拿在角色手里或飘在空中。
  - 手绘小星星/小花点缀，至多 3 处。
- **配色故事**：奶油白/浅粉/浅蓝马卡龙底（极端浅明度）；标题深色打底 +
  一处高饱和撞色（橙红/电光蓝二选一）；角色用暖色毛绒质感。
- **标题写法规范**：
  - 短标题 6~10 字，超大，字高冲击 1/3；关键词撞色 + 白色描边（贴纸感）。
  - 数字钩子放大 1.5~2 倍 + 换对比色（如黑字中的橙红数字）。
  - 底部胶囊标签行 3 短词，`·` 分隔。
- **标题文案提炼公式**：数字 + 筛选动作 + 价值承诺。
  示例（虚构演示）："12个治愈时刻"。
- **prompt 配方**：
  ```
  中文：3D萌系潮玩风中文封面。字体量级：超大深色标题"{TITLE}"（逐字准确），字高冲击画面 1/3，
  关键词"{KEYWORDS}"换撞色 {ACCENT} + 白色描边（贴纸感）；数字钩子"{NUMBER}"字号放大到其余字的
  1.8 倍、换对比色。配色：{BG} 马卡龙浅色底（极端浅明度）；标题深色打底。构图：左侧 45%
  留白放标题（大标题 → 数字钩子 → 胶囊标签行"{TAGLINE}"），右侧 55% 是毛绒/黏土质感 3D
  角色（{CHARACTER}，占画面 40%+，柔光散射、阴影极淡）抱着/举着黏土质感信息卡片
  （{CARDS}）；手绘小星星点缀至多 3 处。质感：柔光散射 + 细腻绒毛质感，拒绝塑料感。
  除标题、胶囊行外无其他文字；所有文字避开左右各 10% 边缘；横构图，尺寸 1500×600。

  EN: 3D cute-toy Chinese cover. Huge dark title "{TITLE}" (exact), glyph height 1/3 of frame;
  keyword "{KEYWORDS}" in accent {ACCENT} with white outline (sticker feel); number hook
  "{NUMBER}" at 1.8× size in contrasting color. {BG} macaron pastel ground. Layout: left 45%
  negative space for title stack, right 55% fluffy/clay 3D character ({CHARACTER}, 40%+ of
  frame, soft diffused light) holding clay info cards ({CARDS}); ≤3 hand-drawn stars.
  No text besides title and capsule row "{TAGLINE}". All text clear of 10% edge margins.
  Landscape 1500×600.
  ```
  占位符：`{KEYWORDS}` 撞色关键词、`{NUMBER}` 数字钩子（必须真实）、`{ACCENT}` 撞色
  （橙红 #FF5A2E / 电光蓝 #2B7FFF 二选一）、`{BG}` 底色（奶油白 #FFF8F0 / 浅粉 #FFE8F0 /
  浅蓝 #E8F2FF 三选一）、`{CHARACTER}` 毛绒角色描述、`{CARDS}` 黏土卡片内容、
  `{TAGLINE}` 胶囊标签行。
- **绝不清单**：
  - 绝不角色占比不足 40%：角色是主角，小了就失去潮玩感。
  - 绝不硬阴影：本风格阴影必须极淡，硬阴影直接变味。
  - 绝不标题无白色描边：贴纸感是本风格的灵魂。
  - 绝不数字与标题同色同字号：数字钩子必须 1.5~2 倍 + 换色。
  - 绝不深底：本风格必须是浅底。

---

## 13. hard-core-type · 硬核立体字

- **适用场景**：深度硬核教程、从入门到精通、架构指南；"这篇很硬核"的技术深度文默认选择。
  示例图：`assets/examples/hard-core-type.png`（原创）。
- **设计语言（抽象原则）**：
  - 文字即建筑：标题做成混凝土/粗糙岩石/红黑砖石质感的 3D 立体字，
    像纪念碑一样立在画面里。
  - 巨物反差：Tiny Human vs Huge Object——小小的人物在巨字下翻书/攀爬，
    反差本身就是震撼。
  - 强透视：低角度仰视，巨字向远方延伸。
- **配色故事**：深灰/暗色底（走极端深明度）或浅灰混凝土底；
  标题用材质本色（混凝土灰/岩石棕/砖红）；一处高饱和强调（橙红/电光蓝）。
- **标题写法规范**：
  - 短标题 4~8 字，3D 立体字，字高占画面 1/2+（巨字就是画面）。
  - 材质三选一：混凝土 / 粗糙岩石 / 红黑砖石。
  - 小人物（{TINY_HUMAN}）在巨字下做动作（翻书/攀爬/仰望）。
- **标题文案提炼公式**：领域 + "指南/精通/架构"。
  示例（虚构演示）："结构之道"。
- **prompt 配方**：
  ```
  中文：硬核立体字风中文封面。字体量级：标题"{TITLE}"（逐字准确）做成 {MATERIAL}
  质感的 3D 立体巨字，字高占画面 1/2 以上，低角度仰视、强透视向远方延伸——
  字本身就是建筑、就是画面。配色：{BG} 底；巨字用材质本色；强调色 {ACCENT}
  只给一处（小人物的衣服/一处光源）。构图：巨物反差——小小的人物（{TINY_HUMAN}，
  占画面 ~10%）在巨字下翻书/攀爬/仰望；一条视觉动线从人物指向巨字。
  质感：材质必须有真实的粗糙颗粒 + 体积光 + 长阴影，拒绝光滑 CG。
  除标题外无其他文字；标题避开左右各 10% 边缘；横构图，尺寸 1500×600。

  EN: Hardcore 3D-type Chinese cover. Title "{TITLE}" (exact) as monumental 3D letters
  in {MATERIAL} texture, glyph height 1/2+ of frame, low-angle strong perspective.
  {BG} ground; accent {ACCENT} touches one element only. Tiny human ({TINY_HUMAN},
  ~10% of frame) climbs/reads beneath the giant type — the scale contrast IS the impact.
  Real rough grain + volumetric light + long shadows. No text besides title.
  All text clear of 10% margins. Landscape 1500×600.
  ```
  占位符：`{MATERIAL}` 材质三选一（混凝土 / 粗糙岩石 / 红黑砖石）、`{BG}` 底色
  （深灰 #2A2A2E / 浅灰混凝土 #D8D8DC 二选一）、`{ACCENT}` 强调色（橙红/电光蓝）、
  `{TINY_HUMAN}` 小人物动作描述。
- **绝不清单**：
  - 绝不小字：本风格字高不足 1/2 直接作废。
  - 绝无巨物反差：没有小人物，巨字就只是一块石头。
  - 绝不光滑材质：无颗粒无阴影的"塑料巨字"一律重画。
  - 绝不平视：必须低角度仰视，平视无压迫感。

---

## 14. dark-saas · 暗色SaaS玻璃拟态

- **适用场景**：产品发布、工具实战测评、开发者工作流、ROI 降本增效。
  示例图：`assets/examples/dark-saas.png`（原创）。
- **设计语言（抽象原则）**：
  - Dark Mode + 毛玻璃（Glassmorphism）：深色底 + 半透明毛玻璃卡片悬浮。
  - 微光发光边框：卡片边缘有一圈极细的发光描边。
  - 工作流节点图：节点 + 连线，讲"自动化流程"的故事。
  - App 悬浮多维投影：界面卡片以不同角度悬浮，有真实投影。
- **配色故事**：深空黑/深蓝黑 `#0A0E1A` 全幅底；毛玻璃卡片半透明；
  强调色单选：电光蓝 `#2B7FFF` / 霓虹紫 `#7C5CFF` / 荧光绿 `#3DFF88`，
  只给发光边框 + 关键词一处。
- **标题写法规范**：
  - 短标题 4~8 字，白色/浅色大字，字高 1/4~1/3；英文专有名词放大
    （如 `Demo` 单独做发光描边）。
  - 底部 4 个胶囊徽标（如"更高效 / 更安全 / 更好体验 / 更强生产力"）。
- **标题文案提炼公式**：产品名 + 版本/核心卖点。
  示例（虚构演示）："云端协作指南"。
- **prompt 配方**：
  ```
  中文：暗色SaaS风中文封面。字体量级：白色大号标题"{TITLE}"（逐字准确），字高占画面
  1/4~1/3；英文专有名词"{EN_TERM}"单独放大 + {ACCENT} 发光描边。配色：深空黑 #0A0E1A
  全幅底；毛玻璃卡片（{UI_CARDS}，半透明、{ACCENT} 微光发光边框）以不同角度悬浮，
  有真实多维投影。构图：左侧 45% 标题区（标题 → 副标题"{SUBTITLE}" → 4 个胶囊徽标
  "{BADGES}"），右侧 55% 是工作流节点图（{WORKFLOW}，节点+连线+微光）+ 悬浮 UI 卡片。
  质感：深底加细腻噪点 + 一团 {ACCENT} 光晕，拒绝死黑。文字特效：标题关键词
  "{KEYWORDS}"换 {ACCENT} 色。除标题、副标题、徽标外无其他文字；
  所有文字避开左右各 10% 边缘；横构图，尺寸 1500×600。

  EN: Dark SaaS Chinese cover. Large white title "{TITLE}" (exact), 1/4~1/3 of frame;
  English term "{EN_TERM}" enlarged with {ACCENT} glow outline. Deep space black #0A0E1A
  ground; frosted-glass cards ({UI_CARDS}, {ACCENT} glow borders) floating at angles
  with real shadows. Left 45%: title → subtitle "{SUBTITLE}" → 4 badge chips "{BADGES}".
  Right 55%: workflow node graph ({WORKFLOW}) + floating UI. Fine grain + {ACCENT} halo
  on dark ground. Keyword "{KEYWORDS}" in {ACCENT}. No other text. 10% margins.
  Landscape 1500×600.
  ```
  占位符：`{EN_TERM}` 英文专有名词、`{ACCENT}` 强调色三选一（电光蓝/霓虹紫/荧光绿）、
  `{UI_CARDS}` 悬浮卡片描述、`{SUBTITLE}` 副标题、`{BADGES}` 4 个胶囊徽标、
  `{WORKFLOW}` 工作流节点描述、`{KEYWORDS}` 标题关键词。
- **绝不清单**：
  - 绝不浅底：本风格必须是深底。
  - 绝不实心不透明卡片：必须是毛玻璃半透明。
  - 绝不无发光边框：发光边框是本风格的灵魂。
  - 绝不第二种强调色：强调色只许一种。

---

## 15. anime-desk · 日系动漫工位

- **适用场景**：行业科普、职业揭秘、经验避坑、个人 IP 打造。
  示例图：`assets/examples/anime-desk.png`（原创）。
- **设计语言（抽象原则）**：
  - 2.5D Q版人物：二次元平涂 + 轻微立体感，表情生动（专注/惊讶/微笑）。
  - 工位桌搭：多层堆叠的书（书脊印关键词）、AI 马克杯、代码弹窗、
    悬浮的图表/灯泡——每个道具讲故事。
  - 轻微透视：桌面轻微俯视，人物三分法站位。
- **配色故事**：纯白/浅色底；标题深色 + 一处高饱和撞色（蓝/橙红）；
  道具用马卡龙浅色系；人物发色/衣服给一处跳色。
- **标题写法规范**：
  - 短标题 6~10 字，超大，字高冲击 1/3；关键词撞色 + 白色描边。
  - 感叹号/问号可做装饰（如"算法工程师！"）。
  - 蓝色胶囊副标题（如"薪资？日常？统统告诉你"）。
- **标题文案提炼公式**：人群/职业 + 揭秘/祛魅动词。
  示例（虚构演示）："带你看懂数据分析师的一天"。
- **prompt 配方**：
  ```
  中文：日系动漫风中文封面。字体量级：超大深色标题"{TITLE}"（逐字准确），字高冲击
  1/3；关键词"{KEYWORDS}"换撞色 {ACCENT} + 白色描边（贴纸感）。配色：{BG} 浅色底；
  道具马卡龙浅色系。构图：左侧 50% 标题区（大标题 → 蓝色胶囊副标题"{SUBTITLE}"），
  右侧 50% 是 2.5D Q版人物（{CHARACTER}，二次元平涂+轻微立体，表情 {EXPRESSION}）
  坐在工位前；桌搭道具：{PROPS}（书脊印关键词、AI 马克杯、代码弹窗、悬浮图表，
  每个道具讲故事）；小装饰（感叹号/放射线）至多 2 处。质感：平涂干净 + 柔和投影，
  拒绝死白。文字特效：数字钩子"{NUMBER}"放大 1.5 倍 + 换 {ACCENT} 色。
  除标题、副标题外无其他文字；所有文字避开左右各 10% 边缘；横构图 1500×600。

  EN: Anime-desk Chinese cover. Huge dark title "{TITLE}" (exact), 1/3 of frame;
  keyword "{KEYWORDS}" in {ACCENT} with white outline. {BG} light ground.
  Left 50%: title → blue capsule subtitle "{SUBTITLE}". Right 50%: 2.5D chibi character
  ({CHARACTER}, cel-shaded, expressive {EXPRESSION}) at a desk with storytelling props
  ({PROPS}: labeled book spines, AI mug, code popup, floating charts). ≤2 decorations.
  Number hook "{NUMBER}" at 1.5× in {ACCENT}. No other text. 10% margins. 1500×600.
  ```
  占位符：`{KEYWORDS}` 撞色关键词、`{ACCENT}` 撞色（蓝/橙红）、`{BG}` 底色、
  `{SUBTITLE}` 胶囊副标题、`{CHARACTER}` 人物描述、`{EXPRESSION}` 表情、
  `{PROPS}` 桌搭道具、`{NUMBER}` 数字钩子（必须真实）。
- **绝不清单**：
  - 绝不写实人物：本风格必须是 2.5D Q版。
  - 绝无故事道具：桌搭道具每个必须讲故事，无意义摆件一律不用。
  - 绝不标题无白色描边。

---

## 16. diorama-book · 微缩立体书

- **适用场景**：宏大系统学习路线、知识地图、万字长文。
  示例图：`assets/examples/diorama-book.png`（原创）。
- **设计语言（抽象原则）**：
  - Diorama 微缩盆景：一本书打开，书页上立起微缩景观（山川/城市/电路）。
  - 立体书探险：发光路径在书页间穿梭，引导视线。
  - 移轴光影：微缩摄影感，边缘轻微虚化。
  - 吉卜力 + 赛博朋克融合：温暖与科技的混搭。
- **配色故事**：暖色微缩景观（吉卜力绿/暖黄）+ 赛博霓虹点缀；
  标题深色压在留白区；发光路径用暖金/电光蓝。
- **标题写法规范**：
  - 短标题 4~8 字，大标题压在顶部留白区，字高 1/4~1/3。
  - 数字钩子（如"万字"）放大 + 换色。
- **标题文案提炼公式**：领域 + "精通/地图/路线"。
  示例（虚构演示）："开源协作入门地图"。
- **prompt 配方**：
  ```
  中文：微缩立体书风中文封面。字体量级：顶部留白区大号深色标题"{TITLE}"（逐字准确），
  字高 1/4~1/3；数字钩子"{NUMBER}"放大 1.5 倍 + 换 {ACCENT} 色。配色：暖色微缩景观
  + {ACCENT} 霓虹点缀。构图：下半部是一本打开的立体书，书页上立起微缩景观
  （{DIORAMA}，吉卜力+赛博朋克融合）；一条发光路径（{ACCENT}）在书页间穿梭；
  移轴摄影感，边缘轻微虚化。质感：微缩模型质感 + 暖光 + 细腻颗粒。
  除标题外无其他文字；标题避开左右各 10% 边缘；横构图 1500×600。

  EN: Diorama pop-up book Chinese cover. Large dark title "{TITLE}" (exact) in top
  negative space, 1/4~1/3 of frame; number hook "{NUMBER}" at 1.5× in {ACCENT}.
  Open pop-up book fills lower half; miniature landscape ({DIORAMA}, Ghibli meets
  cyberpunk) rises from pages; glowing {ACCENT} path winds through. Tilt-shift blur
  at edges. Miniature-model texture + warm light. No other text. 10% margins. 1500×600.
  ```
  占位符：`{NUMBER}` 数字钩子（必须真实）、`{ACCENT}` 强调色（暖金/电光蓝）、
  `{DIORAMA}` 微缩景观描述。
- **绝不清单**：
  - 绝不无立体书：书是本风格的载体，无书即无风格。
  - 绝无发光路径：路径是视线引导，无路径即散。
  - 绝不写实大场景：必须是微缩感，移轴虚化不能少。

---

## 17. cinematic-flow · 电影科技流

- **适用场景**：多工具自动化工作流（A+B+C）、影视视频 AI 生产力。
  示例图：`assets/examples/cinematic-flow.png`（原创）。
- **设计语言（抽象原则）**：
  - 电影级光影：冷蓝主调 + 霓虹光效，强明暗对比。
  - 横向粒子能量光带：从左向右的光流，讲"流程"的故事。
  - 多帧序列：同一主体多帧残影，表现"穿梭/加速"。
  - 超写实人物/主体：细节拉满，拒绝卡通。
- **配色故事**：深蓝黑底；冷蓝 `#2B7FFF` + 霓虹紫/青光效；标题白色/浅色；
  强调色只给光带 + 关键词一处。
- **标题写法规范**：
  - 短标题 4~8 字，白色大字，字高 1/4~1/3，压在左侧留白区。
  - 流程公式可做副标题（如"A → B → C"）。
- **标题文案提炼公式**：工具A + 工具B + 结果。
  示例（虚构演示）："配音+剪辑工作流"。
- **prompt 配方**：
  ```
  中文：电影科技流风中文封面。字体量级：白色大号标题"{TITLE}"（逐字准确），字高
  1/4~1/3，压在左侧 40% 留白区；副标题"{SUBTITLE}"（如"A → B → C"流程公式）。
  配色：深蓝黑底；冷蓝 + 霓虹光效。构图：水平线性流动——左侧标题区 →
  中部横向粒子能量光带（{ACCENT}，从左向右）→ 右侧超写实主体（{SUBJECT}，
  多帧序列残影、穿梭感）；强明暗对比，电影级调色。质感：体积光 + 粒子细节 +
  胶片颗粒。除标题、副标题外无其他文字；所有文字避开左右各 10% 边缘；
  横构图 1500×600。

  EN: Cinematic tech-flow Chinese cover. Large white title "{TITLE}" (exact),
  1/4~1/3 of frame, in left 40% negative space; subtitle "{SUBTITLE}" (e.g. "A → B → C").
  Deep blue-black ground; cold blue + neon glow. Horizontal flow: title → particle
  energy light-band ({ACCENT}, left to right) → hyperreal subject ({SUBJECT},
  multi-frame ghosting). Strong chiaroscuro, cinematic grade. Volumetric light +
  film grain. No other text. 10% margins. 1500×600.
  ```
  占位符：`{SUBTITLE}` 流程公式副标题、`{ACCENT}` 光带色（冷蓝/霓虹紫/青）、
  `{SUBJECT}` 超写实主体描述。
- **绝不清单**：
  - 绝不卡通主体：本风格必须超写实。
  - 绝无光带：光带是流程的视觉隐喻，无光带即无风格。
  - 绝不浅底：本风格必须是深底。

---

## 18. academic-print · 学院版画

- **适用场景**：论文解读、底层原理解析、严肃评测、方法论/提示词研究。
  示例图：`assets/examples/academic-print.png`（原创）。
- **设计语言（抽象原则）**：
  - 19世纪铜版雕刻线稿：精密机械/解剖图式的线稿，严谨即美。
  - 牛皮纸/撕纸纹理：纸的质感是底色。
  - 衬线宋体标题：学术正统，字距宽松。
  - 印章标签 + 学术对齐线：红印章点睛，对齐线框定版式。
- **配色故事**：牛皮纸 `#E8DCC8` / 米白底；标题墨黑衬线；朱红 `#E6392B`
  只给印章 + 一处关键词；线稿用深棕/墨色。
- **标题写法规范**：
  - 短标题 6~12 字，衬线宋体，字高 1/4~1/3，字距宽松。
  - 右上角朱红印章（如"实测"）。
  - 副标题用打字机字体（如"3万字写作测评"）。
- **标题文案提炼公式**：研究对象 + 方法/结论。
  示例（虚构演示）："3万字写作研究"。
- **prompt 配方**：
  ```
  中文：学院版画风中文封面。字体量级：墨黑衬线宋体大标题"{TITLE}"（逐字准确），
  字高 1/4~1/3，字距宽松；打字机字体副标题"{SUBTITLE}"；右上角朱红印章"{SEAL}"。
  配色：牛皮纸 #E8DCC8 底 + 撕纸纹理；线稿深棕/墨色；朱红只给印章+关键词
  "{KEYWORDS}"。构图：左侧 55% 标题区（学术对齐线框定），右侧 45% 是铜版雕刻线稿
  （{ENGRAVING}，19世纪精密机械/解剖图风）；印章点睛。质感：纸纹 + 雕刻线条 +
  印章肌理。除标题、副标题、印章外无其他文字；所有文字避开左右各 10% 边缘；
  横构图 1500×600。

  EN: Academic print Chinese cover. Ink-black serif title "{TITLE}" (exact),
  1/4~1/3 of frame, generous letter-spacing; typewriter subtitle "{SUBTITLE}";
  vermilion seal "{SEAL}" top-right. Kraft paper #E8DCC8 ground with torn-paper
  texture; copperplate engraving ({ENGRAVING}, 19th-century precision style) right 45%;
  academic alignment rules frame left 55% title zone. Vermilion only for seal +
  keyword "{KEYWORDS}". Paper grain + engraved lines. No other text. 10% margins.
  1500×600.
  ```
  占位符：`{SUBTITLE}` 打字机副标题、`{SEAL}` 印章文字（如"实测"，必须真实）、
  `{KEYWORDS}` 朱红关键词、`{ENGRAVING}` 雕刻线稿描述。
- **绝不清单**：
  - 绝不黑体标题：本风格必须衬线宋体。
  - 绝不无纸纹：纸的质感是底色，无纹理即无风格。
  - 绝不花哨撞色：朱红只给两处，多一处即俗。

---

## 19. gallery-grid · 样张矩阵

- **适用场景**：模型/工具评测、风格 LoRA 展示、生图模型发版。
  示例图：`assets/examples/gallery-grid.png`（原创）。
- **设计语言（抽象原则）**：
  - Moodboard 密集排版：多张样例图平铺，本身就是内容。
  - 多样性展示：同一提示词不同风格 / 同一模型不同场景。
  - 实操测试对比：左右/上下对比排布。
  - 标题压阵：大标题压在顶部，不抢样张的戏。
- **配色故事**：浅灰/白底做画框；标题深色 + 一处撞色；样张本身色彩丰富，
  标题必须克制。
- **标题写法规范**：
  - 短标题 4~8 字，顶部大标题，字高 1/4（给样张让路）。
  - 右下角小标签（如"本机 × 云端"）。
- **标题文案提炼公式**：模型/工具名 + "实测/样张"。
  示例（虚构演示）："绘图模型横评"。
- **prompt 配方**：
  ```
  中文：样张矩阵风中文封面。字体量级：顶部深色大标题"{TITLE}"（逐字准确），字高
  1/4（给样张让路）；右下角小标签"{SPECS}"。配色：浅灰/白底画框；标题深色 +
  一处撞色 {ACCENT}。构图：下半部 2×3 或 3×3 样张矩阵（{SAMPLES}，多样性展示：
  {VARIETY}）；样张间细线分隔；标题压阵不抢戏。质感：画框投影 + 纸纹。
  除标题、小标签外无其他文字；所有文字避开左右各 10% 边缘；横构图 1500×600。

  EN: Gallery-grid Chinese cover. Dark title "{TITLE}" (exact) at top, 1/4 of frame;
  small spec tag "{SPECS}" bottom-right. Light gray/white mat; one accent {ACCENT}.
  Lower half: 2×3 or 3×3 sample matrix ({SAMPLES}, variety: {VARIETY}); hairline
  dividers; mat shadows + paper grain. No other text. 10% margins. 1500×600.
  ```
  占位符：`{SPECS}` 规格小标签（必须真实）、`{ACCENT}` 撞色、`{SAMPLES}` 样张描述、
  `{VARIETY}` 多样性维度。
- **绝不清单**：
  - 绝不标题过大：标题字高超 1/4 就抢了样张的戏。
  - 绝不样张无多样性：样张必须展示变化，重复即废。
  - 绝不花哨标题：样张已够丰富，标题必须克制。

---

## 风格速查（22 种：1~12 浅色，13~22 深色/高饱和）

| 风格 | 一句话 | 标题字号占比 | 首选题材 |
|---|---|---|---|
| white-clean | 纯白底 + 冲击 1/3 的撞色巨标题 + 场景化插图 + 胶囊标签，清新透气 | 冲击 1/3 | 干货清单/实测盘点/效率职场 |
| bg-blur | 浅色虚化摄影背景 + 锐利前景主体，大标题压清晰区 | 冲击 1/3 | 生活方式/职场日常/运动健康 |
| paper-collage | 马卡龙纸片拼贴 + 和纸胶带/回形针，标题印最大纸片上 | 冲击 1/3 | 手账/整理术/旧物改造 |
| news-flash | 纸纹米底 + 纯黑大标题 + 朱红爆点词点睛，快讯的干脆 | ~1/3 | 资讯/快讯/热点解读 |
| big-type | 标题即画面：1/3 幅墨黑书法烫金，奶油亮底一声断言 | 1/3~2/5 | 观点/深度/发布宣言 |
| tutorial-steps | 宣纸书法 1/3 镇场 + 底部赭石时间线，三步即上手 | ~1/3 | 教程/上手指南 |
| minimal | 85% 留白 + 一处朱红点睛 + 宽字距深灰标题，张力拉满 | ~1/6（字重补） | 随笔/书评/轻观点 |
| magazine | 暖灰影棚颗粒 + 人像氛围 + 砖红细线，标题压阵 | 1/4~1/3 | 访谈/人物特写/商业分析 |
| chao-wan-3d | 毛绒/黏土 3D 潮玩角色 + 贴纸感标题 + 柔光散射，亲和爆款 | 冲击 1/3 | 爆款盘点/新手干货/合集清单 |
| anime-desk | 2.5D Q版人物 + 工位桌搭故事道具，二次元平涂 | 冲击 1/3 | 行业科普/职业揭秘/个人IP |
| diorama-book | 微缩立体书 + 发光路径 + 移轴光影，知识探险 | 1/4~1/3 | 学习路线/知识地图/万字长文 |
| academic-print | 铜版雕刻线稿 + 牛皮纸 + 衬线宋体 + 朱红印章，学术正统 | 1/4~1/3 | 论文解读/原理解析/方法论 |
| gallery-grid | 样张矩阵 Moodboard + 标题压阵，多样性展示 | 1/4（让路） | 模型评测/LoRA展示/生图发版 |
| dark-saas | 深空黑 + 毛玻璃卡片 + 发光边框 + 工作流节点，极客 | 1/4~1/3 | 产品发布/工具测评/工作流 |
| cinematic-flow | 冷蓝霓虹 + 粒子光带 + 超写实主体，电影级流程 | 1/4~1/3 | 自动化工作流/AI生产力 |
| hard-core-type | 混凝土/岩石 3D 巨字 + 小人物反差，纪念碑式震撼 | 1/2+ | 硬核教程/架构指南 |
| gan-huo | 深炭灰底 + 米白 1/3 巨标题 + 朱红印章点睛，一眼即干货 | ~1/3 | 干货清单/评测/盘点 |
| brand-launch | 深海军蓝 + 荧光绿唯一强调，品牌大标题压阵 | 1/4~1/3 | 产品发布/版本更新 |
| ip-fun | 暖橙舞台 + 深棕叠放巨标题 + 趣味 IP 记忆点 | 1/4~1/3 | 实战案例/数据战报 |
| orange-warm | 活力橙渐变 + 白色巨标题 + 暖光粒子，热情亲和 | 冲击 1/3 | 生活方式/美食/旅行/亲子 |
| sketch-cartoon | 手绘素描线稿 + 卡通上色 + 纸纹，亲切手作感 | 1/4~1/3 | 创意/手作/儿童/轻松科普 |
| cyber-neon | 赛博霓虹 + 全息投影 + 故障艺术，未来科技感 | 1/4~1/3 | AI前沿/科幻/极客/游戏 |
---

## 构图骨架（4 种 Layout Template）

风格决定"长什么样"，骨架决定"怎么摆"。选风格后，再选一种骨架：

### L1. 左文右图 / 黄金分割

- **结构**：左侧 40%~50% 纯粹留白（或浅色纯色底），放标题 + 副标题 + 数据标签；
  右侧 50%~60% 放高精度 3D 角色 / UI 展台 / 场景插画。
- **优势**：文字在移动端滚动时先进入视野，不与背景打架，可读性极强。
- **适用风格**：white-clean、chao-wan-3d、anime-desk、dark-saas、diorama-book。
- **铁律**：左右交界处留一条"呼吸带"，文字绝不压到右侧主体上。

### L2. 水平线性流动 / 公式流

- **结构**：左（输入）→ 中（处理流/光效）→ 右（输出/宿主）。
- **视觉中心**：一条极度顺畅的指引线（光带/箭头/路径），契合"把复杂变简单"的心理诉求。
- **适用风格**：cinematic-flow、dark-saas、tutorial-steps。
- **铁律**：流动方向必须从左向右（阅读习惯），逆流即乱。

### L3. 沉浸式场景中嵌字

- **结构**：文字本身成为场景中的物理存在——3D 雕塑招牌、仪器铭牌、书页立字。
- **优势**：整体性最强，视觉冲击力最大。
- **适用风格**：hard-core-type、diorama-book、academic-print。
- **铁律**：字必须是场景的"原住民"（材质/光影与场景一致），不能是后期贴上去的。

### L4. 报刊网格 / 剪报卡片

- **结构**：左右或上下网格；左侧标题用正统版面规范，右侧用便签贴纸/撕纸边缘
  突出硬核数据。
- **适用风格**：gallery-grid、academic-print、paper-collage、news-flash。
- **铁律**：网格线必须对齐，错一位即廉价。

---

## 文案排版密码（Typography Rules）

从一线头部封面提炼的文本层级规范，所有风格通用：

### 超级大字（Main Title）

- 汉字字重极粗（方正大黑 / 汉仪润圆 / 造字工房力黑一类），字高冲击 1/3（hard-core-type 可到 1/2+）。
- 手法三选一：高饱和撞色 / 微渐变 / 双层立体描边（白色描边 + 阴影 = 贴纸感）。
- 英文/专有名词单独放大（如 `Skill`、`Demo`、`GitHub`、`Studio`），可做斜体。

### 数字钩子（Quantifiable Hooks）

- 每张封面几乎都有突出的大数字：`3天`、`26篇`、`从0到1`、`万字`、`3万字`。
- **技巧**：数字字号放大到其余字的 1.5~2 倍，并换对比色（黑字中的亮橙数字）。
- 数字必须真实有出处，绝不编造。

### 底部微型标签条（Chips / Badges）

- 格式：`⚡实测筛选 | 📄长文精选 | 📊全流程实操` 或 4 胶囊徽标。
- **作用**：填充下部边角空白，增强专业交付感和信任背书。
- 字号约为标题的 1/4，至多 4 个。

### 文案提炼公式（风格转译器）

用户输入通常很简单（如"写了一篇 DeepSeek 部署的万字教程"），技能自动完成：

1. **提炼短标题 + 核心数字**：→ "DeepSeek 部署实测 / 万字"
2. **推荐风格**：极客硬核 → dark-saas / hard-core-type；新手向 → chao-wan-3d / anime-desk
3. **注入安全区**：所有文字与关键主体避开左右各 10% 边缘

---

## 高级感设计系统（Premium Design System）

> 为什么有些封面"土"？因为只用了"黑体加粗+换色+居中"。
> 高级感来自 4 个维度的精致化：字体、角度、景深、光影。
> 以下手法按需选用 2~4 种，是"好看"到"高级"的分水岭。

### 一、字体高级感（拒绝 plain font block）

1. **字重对比**：标题内粗细搭配——如"远程工作"用超粗黑、"效率手册"用中黑，
   粗细反差本身就是设计。
2. **中英混排精致化**：英文不用默认字体——用细体英文 + 字母间距拉开，
   放在中文标题下方或旁边做点缀，字号为中文的 1/3。
3. **描边层次**：双层描边（外层白 3px + 内层色 1px）> 单层描边 > 无描边。
   渐变描边（上浅下深）比纯色描边更高级。
4. **字形微调**：关键词字间距放宽 0.1em；数字用等宽字体；长标题行距 1.2 倍。
5. **真立体字**：3D 挤压（extrude）5~10px + 侧面暗色，不是简单的投影。
   只给标题中最重要的 2~4 个字做立体，全标题立体即土。

### 二、角度动感（有条件使用，非必选项）

> **重要**：不是每个标题都要倾斜。倾斜是手段不是目的，根据版面和场景判断：
> - 适合倾斜：动感主题（运动/突破/发布）、单行短标题、画面右侧有空间
> - 不适合倾斜：严肃主题（学术/财报/官方）、双行标题（倾斜后难读）、
>   标题已占满宽度（倾斜会出界）
> - 替代方案：标题水平 + 元素走对角线，同样有动感且更稳

1. **标题倾斜（条件触发）**：整体倾斜 5~15°（左低右高为佳），字不转、整体转。
   仅当主题动感 + 单行标题 + 右侧有空间时使用。
2. **双行标题规范**：两行标题必须水平（倾斜双行难读）；
   两行之间用字重/颜色区分（上行粗黑、下行撞色，或反之）；
   行距 1.1~1.3 倍，上下行左对齐或居中对齐（二选一，不混用）。
3. **元素透视**：近大远小——前景元素大、后景元素小，形成透视纵深。
4. **对角线构图**：主要视觉元素沿左下→右上对角线分布，打破对称呆板。
   （标题水平时，用元素走对角线来提供动感）
5. **旋转点缀**：印章/标签旋转 8~15°，比端正摆放更生动。

### 二点五、重点词高亮（标题的点题之眼）

每个标题都有 1~2 个"点题词"（核心概念/品牌/数字），必须重点突出：
1. **识别点题词**：标题中最重要的名词/动词/数字（如"效率手册"中的"效率"）。
2. **高亮三选一**：撞色变色 / 色块衬底 / 真立体——只选一种，不叠加。
3. **层级**：点题词字号可放大到其余字的 1.2~1.5 倍，但不换行。
4. **禁忌**：全标题高亮 = 没有高亮；超过 2 个高亮词即乱。

### 三、景深层次（拒绝三层了事）

至少 4 层，从远到近：
1. **远景氛围**：虚化光斑 / 渐变 / 纹理，纯氛围不抢戏。
2. **中景主体**：角色 / 场景 / 产品，清晰但比标题层弱。
3. **标题层**：最清晰、最锐利，压在中景之上。
4. **前景装饰**：故意虚化的前景元素（如虚化的树叶/纸片/光点），
   制造"镜头感"，这是电影感的关键。

### 四、光影质感（拒绝平光）

1. **体积光**：一束明确的光从斜上方打下来，照亮标题区，背景自然渐变。
2. **镜头光晕**：1~2 处 lens flare / 光斑，点到为止。
3. **材质纹理**：纸纹 / 布纹 / 噪点 / 颗粒，拒绝死平。
4. **投影真实**：投影方向一致（光从左上打来，影就往右下），
   投影柔和不脏。

### 高级感自检（生成后必过）

| # | 检查项 | 土的表现 | 高级的改法 |
|---|--------|----------|------------|
| 1 | 标题有字体设计吗？ | 黑体加粗+换色 | 字重对比/描边层次/真立体 |
| 2 | 有角度变化吗？ | 全正面平视且元素呆板 | 条件倾斜/对角线元素/透视（三选一，不硬倾斜） |
| 2.5 | 点题词突出了吗？ | 全标题一样重 | 1~2 个点题词高亮（撞色/色块/立体三选一） |
| 3 | 景深几层？ | 3层（背景+标题+角色） | 4层+（加前景虚化） |
| 4 | 光有方向吗？ | 平光/无光 | 体积光+一致投影 |
| 5 | 装饰精致吗？ | 星星/胶囊/横条三件套 | 几何线/纹理/光斑 |
