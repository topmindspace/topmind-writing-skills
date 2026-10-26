# 封面范式库（整张生成用）

> 使用范围：本页是可拆用的配方与样例，参数描述某种具体效果，不是所有封面的通用要求。当前用户要求、真实素材、核字与实际裁切优先。可删槽位、改构图、用纯色或无人物；整张生成与后期叠字并列选择，只读当前方向需要的章节。

> 用法：选一个范式，把模板里的 `{占位}` 换成具体内容，再在末尾接上「通用排版尾句」，整段英文交给生图模型，让它把字和场景一起画出来。出图后按 `design-system.md` 第九节「中文字生图规约」逐字核对，错字按那一节的方法修正。
> 这些范式是我们自己归纳的抽象规律（构图、字的处理、配色、隐喻），不对应任何具体作品；用的时候换成自己的主题、主角和配色。

## 可选排版尾句（按方案删改）

```text
Typography rules: the headline text is exactly "{title}" in Simplified Chinese characters exactly as given, no extra, missing or altered characters, no traditional characters; the subtitle is exactly "{subtitle}". Hierarchy: one headline (about 25-45% of image height, heavy weight), one subtitle line (about 10% of image height), {tagline}all text aligned to {align}, inside a 6% safe margin, high contrast against its background. Only one accent color, used on 1-3 key characters. All letters share the scene's light direction, shadows and perspective. Keep all text within the central horizontal band of the image (it will be cropped to 5:2). Clean composition with one focal point and generous negative space, no other text, no watermark, no logo, no UI gibberish. Wide 16:9.
```

- `{tagline}` 要胶囊标签时写 `one row of 2-3 small rounded pill tags reading "标签1" "标签2" (about 6-7% of image height), `，不要时留空。
- `{align}` 写 `a single left alignment line at 7% from the left edge`（左文右图），或 `the vertical center axis`（居中构图）。
- 常用占位：`{title}` 主标题，`{subtitle}` 副标题，`{hero}` 主角或主体，`{accent}` 强调色，`{bg}` 底色，`{scene}` 场景，`{material}` 字的材质。

## 范式速查

| 编号 | 范式 | 适用主题 |
|---|---|---|
| X1 | 材质巨字立地 | 硬核方法论、架构、宣言、年度总结 |
| X2 | 玻璃金属挤出 + 霓虹 | 产品发布、版本更新、AI 新品 |
| X3 | 软糖 3D 萌字 + IP | IP 打卡、新手入门、轻松科普、亲子 |
| X4 | 卡通主角 + 超大数字钩子 | 盘点、榜单、实测、数据战报 |
| X5 | 浅底 SaaS 卡片 | 工具教程、产品指南、效率 |
| X6 | 满版强调色 + 极简大字 | 观点、短评、口号、警示 |
| X7 | 电影场景 + 书法字 | 故事、行业变局、对决、文化题材 |
| X8 | 纸感印刷巨字 | 干货清单、方法总结、复盘 |
| X9 | 编号流程上字下图 | 教程、流程、N 步上手 |
| X10 | 人物大头 + 侧边标题 | 个人 IP、访谈、观点 |
| X11 | 暗色玻璃科技 | AI 工具、工作流、开发者内容 |
| X12 | 微缩场景 + 标题招牌 | 知识地图、学习路线、行业全景 |
| X13 | 对比两侧 | A vs B、新旧对比、选择题 |
| X14 | 杂志编辑大片 | 深度长文、人物、商业分析 |
| X15 | 举牌 / 拉横幅 | 口号、涨粉、活动、短标题 |
| X16 | 手绘信息卡（克制版） | 保姆级教程、合集 |

## X1 材质巨字立地

- **适用主题**：硬核方法论、架构、宣言、年度总结
- **构图**：居中；巨字立在地面或平台上，小人物站在字旁给出尺度
- **标题处理**：标题做成真实材质的 3D 巨字（混凝土、石材、金属），与场景共用光照、投影和透视
- **配色**：低饱和中性色 + 一处强调色
- **场景元素**：广场 / 平台 / 地平线、一个小人物、雾或体积光
- **prompt 模板**（后接通用排版尾句）：

```text
Cinematic wide shot of a vast {scene}. In the middle ground, the headline "{title}" stands on the ground as giant three-dimensional {material} letters, sharing the scene's lighting, shadows and one-point perspective, as if built there. {hero} stands beside the letters for scale. The subtitle "{subtitle}" floats as a clean flat line in the calm upper third. Soft volumetric light, muted palette with {accent} accent.
```

- **常见失败与修正**：字悬空、不着地 → 写 standing on the ground, casting a shadow on the floor；字材质和场景不一致 → 写 sharing the scene's lighting；人物比字还大 → 写 tiny figure for scale

## X2 玻璃金属挤出 + 霓虹

- **适用主题**：产品发布、版本更新、AI 新品
- **构图**：左文右物：标题左 50%，产品或发光物件在右
- **标题处理**：标题为玻璃 / 拉丝金属挤出字，边缘带一圈与场景光源同色的霓虹描边
- **配色**：深海军蓝 / 黑 + 一种荧光色（绿 / 青 / 紫）
- **场景元素**：发光的产品、光束、反射地面、粒子
- **prompt 模板**（后接通用排版尾句）：

```text
Dark premium product-launch scene, deep navy background with a reflective floor. On the right, {hero} glows with {accent} rim light and light beams. On the left, the headline "{title}" in bold extruded glass-and-brushed-metal letters with a thin {accent} neon edge, lit by the same light source, slightly reflected on the floor. Below it, the subtitle "{subtitle}" in clean white sans-serif.
```

- **常见失败与修正**：霓虹太脏 / 发光糊字 → 写 crisp letters, subtle glow only on the edge；产品抢焦点 → 产品放右侧 40% 以内

## X3 软糖 3D 萌字 + IP

- **适用主题**：IP 打卡、新手入门、轻松科普、亲子
- **构图**：左字右 IP，IP 看向或指向标题
- **标题处理**：标题为圆润软糖 / 黏土 3D 字，柔和高光，与 IP 同材质
- **配色**：奶油色或暖橙底 + 两种糖果色，其中一种做强调
- **场景元素**：3D 毛绒 / 黏土 IP、两三个主题道具、柔光
- **prompt 模板**（后接通用排版尾句）：

```text
Soft 3D clay-and-candy illustration, warm {bg} background with gentle studio light. On the right, {hero}, cute and expressive, turns toward the headline and points at it. On the left, the headline "{title}" as puffy glossy jelly-candy 3D letters in {accent} and cream, same material and lighting as the character. Below, the subtitle "{subtitle}" in rounded bold sans-serif.
```

- **常见失败与修正**：字发软到认不出 → 写 letters stay crisp and legible；IP 盖住字 → IP confined to the right 45%

## X4 卡通主角 + 超大数字钩子

- **适用主题**：盘点、榜单、实测、数据战报
- **构图**：左侧超大数字或关键词，右侧卡通主角做夸张动作
- **标题处理**：数字放到主标题的 1.5–2 倍，作为第一焦点；关键词用强调色
- **配色**：白 / 米白底 + 黑字 + 一种强调色
- **场景元素**：卡通主角、与数字相关的道具（奖杯、计数器、榜单）
- **prompt 模板**（后接通用排版尾句）：

```text
Bold editorial cartoon illustration on a {bg} background. {hero} on the right reacts with an exaggerated expression and gestures toward the headline. On the left, a huge number dominates as the first focal point, part of the headline "{title}" in heavy black sans-serif with the number in {accent}. The subtitle "{subtitle}" sits below in medium weight.
```

- **常见失败与修正**：数字被写错 → 标题里只放一个数字，写 the number exactly as given；主角太多 → 只要 one character

## X5 浅底 SaaS 卡片

- **适用主题**：工具教程、产品指南、效率
- **构图**：左文右卡：标题左对齐，右侧 2–4 张悬浮 UI 卡片或一个产品主体
- **标题处理**：粗黑标题，一个词用强调色；卡片上不写可读字
- **配色**：白 / 浅灰蓝渐变 + 黑字 + 品牌强调色
- **场景元素**：悬浮玻璃卡片、图标、柔和阴影，或一个实物主体
- **prompt 模板**（后接通用排版尾句）：

```text
Clean light SaaS-style cover, soft white-to-pale-blue gradient background. On the right, {hero} with three floating rounded glass cards showing simple icons and abstract charts (no readable text), soft shadows. On the left, the headline "{title}" in heavy black sans-serif, one key word in {accent}. Below, the subtitle "{subtitle}" in grey medium sans-serif.
```

- **常见失败与修正**：卡片里出现乱码 → 写 cards show only icons and abstract shapes, no text；同质化 → 换一个实物主体代替卡片

## X6 满版强调色 + 极简大字

- **适用主题**：观点、短评、口号、警示
- **构图**：满版一种颜色，字居中或左对齐，几乎没有其他元素
- **标题处理**：标题占画面高 35–45%，白色或黑色超粗体
- **配色**：一种饱和色满版（红 / 橙 / 黄）+ 白或黑字
- **场景元素**：最多一个小图形符号
- **prompt 模板**（后接通用排版尾句）：

```text
Minimal bold poster, the whole background is flat saturated {accent}. The headline "{title}" in enormous ultra-heavy white Chinese sans-serif fills the center, perfectly crisp. The subtitle "{subtitle}" in small-caps-like medium white text below. Nothing else except {hero}.
```

- **常见失败与修正**：画面太空像没做完 → 加一个与主题相关的小图形；字被压扁 → 写 natural proportions

## X7 电影场景 + 书法字

- **适用主题**：故事、行业变局、对决、文化题材
- **构图**：电影宽画面，主体在一侧或中央，书法标题压在暗部
- **标题处理**：毛笔书法标题，墨色或金色，与场景的情绪一致
- **配色**：暗调 + 一种暖色光（金 / 橙 / 红）
- **场景元素**：电影级场景、人物剪影、烟雾、逆光
- **prompt 模板**（后接通用排版尾句）：

```text
Cinematic film still, {scene}, dramatic backlight and mist, dark moody tones with {accent} highlights. {hero}. In the darker negative space, the headline "{title}" written in powerful Chinese brush calligraphy in {accent}-tinted ink, integrated with the atmosphere. The subtitle "{subtitle}" in small clean serif below.
```

- **常见失败与修正**：书法字变形到认不出 → 写 legible standard calligraphy, regular script influence；字少于 6 个最稳

## X8 纸感印刷巨字

- **适用主题**：干货清单、方法总结、复盘
- **构图**：巨字占满左侧或整幅，纸张纹理，局部被物件压住
- **标题处理**：标题为丝网印刷 / 报纸大字，带油墨颗粒与轻微错版
- **配色**：米白纸底 + 黑 + 一种印刷红或蓝
- **场景元素**：纸张纹理、胶带、剪报、一个手部或人物
- **prompt 模板**（后接通用排版尾句）：

```text
Risograph print poster on off-white textured paper. The headline "{title}" in giant bold black printed letters with ink grain and slight misregistration, one word in {accent}. Beside the letters sits {hero}, partly overlapping the edge of one character without hiding it. The subtitle "{subtitle}" in a clean sans-serif strip below.
```

- **常见失败与修正**：压字遮掉关键笔画 → 写 never covering any stroke of the key word；纹理太重 → 写 subtle grain

## X9 编号流程上字下图

- **适用主题**：教程、流程、N 步上手
- **构图**：上方标题，下方 3–5 个编号卡片沿弧线或阶梯排开
- **标题处理**：标题一行或两行左对齐；卡片只有图标和编号，不写字
- **配色**：浅底 + 一种主色 + 一种强调色
- **场景元素**：编号卡片、箭头、主角站在流程旁讲解
- **prompt 模板**（后接通用排版尾句）：

```text
Friendly flat illustration on a {bg} background. Across the lower half, {steps} numbered rounded cards rise like a staircase from left to right, each showing only a simple icon and a big number, connected by a dotted arrow. {hero} stands beside the cards presenting them. In the upper left, the headline "{title}" in heavy sans-serif with one word in {accent}, and the subtitle "{subtitle}" below it.
```

- **常见失败与修正**：卡片上出现乱字 → 写 cards contain only icons and numerals；卡片超过 5 张 → 改成 3–4

## X10 人物大头 + 侧边标题

- **适用主题**：个人 IP、访谈、观点
- **构图**：人物（插画）占左 40%，标题在右侧对齐
- **标题处理**：粗体标题右侧排两行，关键词强调色；副标题细一档
- **配色**：中性色底 + 人物主色 + 一种强调色
- **场景元素**：插画人物半身像，表情明确，视线看向标题
- **prompt 模板**（后接通用排版尾句）：

```text
Stylized illustrated portrait, {hero} as a half-length character on the left 40%, confident expression, looking toward the right. Clean {bg} background with a subtle shape behind the character. On the right, the headline "{title}" in heavy sans-serif, two lines, left-aligned, one word in {accent}; the subtitle "{subtitle}" below.
```

- **常见失败与修正**：画成真实名人 → 写 original fictional character, not resembling any real person

## X11 暗色玻璃科技

- **适用主题**：AI 工具、工作流、开发者内容
- **构图**：左文右图；右侧玻璃拟态面板与节点连线
- **标题处理**：白色粗体标题，一个词用霓虹强调色，标题下有细线
- **配色**：深空黑 / 深蓝 + 青或紫霓虹
- **场景元素**：毛玻璃面板、节点、发光连线、微粒
- **prompt 模板**（后接通用排版尾句）：

```text
Dark futuristic tech cover, deep space black-blue background with subtle grid. On the right, {hero}: frosted glass panels and glowing nodes connected by {accent} light lines (no readable text on panels). On the left, the headline "{title}" in heavy white sans-serif with one word glowing {accent}, the subtitle "{subtitle}" in light grey beneath.
```

- **常见失败与修正**：面板上出现假文字 → 写 panels show only abstract shapes；整体太暗 → 写 key light on the panels

## X12 微缩场景 + 标题招牌

- **适用主题**：知识地图、学习路线、行业全景
- **构图**：移轴微缩世界占右侧或全画面，标题是场景里的一块招牌
- **标题处理**：标题写在场景中的招牌 / 立牌 / 书脊上，跟随场景透视
- **配色**：暖色移轴光 + 一种强调色
- **场景元素**：微缩建筑、小路、发光路径、小人
- **prompt 模板**（后接通用排版尾句）：

```text
Tilt-shift miniature diorama, {scene}, warm sunlight, tiny figures. {hero}. A large sign board standing in the scene displays the headline "{title}" in bold clean letters, following the scene's perspective and lighting. The subtitle "{subtitle}" appears on a smaller plaque below the sign.
```

- **常见失败与修正**：招牌太小 → 写 the sign occupies about 40% of the image width；透视太斜 → 写 sign faces the camera

## X13 对比两侧

- **适用主题**：A vs B、新旧对比、选择题
- **构图**：标题居中，左右两侧各一个对立物
- **标题处理**：标题中间的对比符号（VS / → / ≠）只出现一次，用强调色
- **配色**：左右两种冷暖对立色 + 中性标题
- **场景元素**：两个对立物或两个角色
- **prompt 模板**（后接通用排版尾句）：

```text
Symmetrical split composition, left side in cool {left_color} tones with {left}, right side in warm {right_color} tones with {right}. In the center, the headline "{title}" in heavy sans-serif, the comparison symbol in {accent}. The subtitle "{subtitle}" centered below.
```

- **常见失败与修正**：两侧不平衡 → 写 equal visual weight；符号重复出现 → 只在标题里写一次

## X14 杂志编辑大片

- **适用主题**：深度长文、人物、商业分析
- **构图**：大幅摄影感主体 + 衬线大标题，网格感强
- **标题处理**：宋体 / 衬线大标题，字距宽，一处细线分隔
- **配色**：暖灰 / 米白 + 黑 + 一种砖红
- **场景元素**：摄影棚光、人物或物件特写、颗粒
- **prompt 模板**（后接通用排版尾句）：

```text
Editorial magazine cover layout, warm grey studio backdrop with film grain. {hero} photographed in soft directional light on the right. On the left, the headline "{title}" in elegant high-contrast Chinese serif (Song style), generous letter spacing, a thin {accent} rule beneath it, and the subtitle "{subtitle}" in small clean sans-serif.
```

- **常见失败与修正**：衬线字笔画断裂 → 写 bold serif, strong strokes

## X15 举牌 / 拉横幅

- **适用主题**：口号、涨粉、活动、短标题
- **构图**：主角双手举牌，标题写在牌子上，牌子占画面 50%
- **标题处理**：牌子正对镜头，字平整不变形
- **配色**：高饱和底 + 白牌 + 黑字 + 一个强调词
- **场景元素**：主角、牌子、彩纸
- **prompt 模板**（后接通用排版尾句）：

```text
Playful illustration, {bg} background with a little confetti. {hero} holds up a large flat white sign facing the camera, the sign fills about half of the image. On the sign, the headline "{title}" in heavy black sans-serif, one word in {accent}, perfectly flat and undistorted. The subtitle "{subtitle}" on a small ribbon below the sign.
```

- **常见失败与修正**：牌子弯曲导致字变形 → 写 flat rigid board

## X16 手绘信息卡（克制版）

- **适用主题**：保姆级教程、合集
- **构图**：左侧大标题，右侧 3–4 张手绘便签卡（只画图标）
- **标题处理**：手写感粗体标题，下面一条马克笔高亮；便签只画图标
- **配色**：米白纸底 + 黑 + 黄色高亮 + 一种强调色
- **场景元素**：便签、胶带、铅笔、主角卡通形象
- **prompt 模板**（后接通用排版尾句）：

```text
Hand-drawn notebook illustration on cream paper. On the right, three or four sticky notes with doodled icons only (no words), tape and a pencil, plus {hero}. On the left, the headline "{title}" in bold marker-style lettering with a yellow highlighter stroke under one word, the subtitle "{subtitle}" in neat handwriting-style print below.
```

- **常见失败与修正**：便签写满小字 → 写 notes contain only doodles；手写体难认 → 写 bold, highly legible
