# 组合玩法（范式 × 风格 × 标题字 × 场景层 × 配色）

> 使用范围：本页是可拆用的配方与样例，参数描述某种具体效果，不是所有封面的通用要求。当前用户要求、真实素材、核字与实际裁切优先。可删槽位、改构图、用纯色或无人物；整张生成与后期叠字并列选择，只读当前方向需要的章节。

> 用法：先按主题选一个组合，把 `{title}`、`{subtitle}` 换成自己的内容，整段英文交给生图模型。组合是我们自己总结的配方，不对应任何具体作品。

## 组合公式

封面 = 范式（构图骨架，X1–X16）× 风格（`cover-styles.md` 的风格名）× 标题字处理（材质、立体方式）× 场景层（主角、道具、远近景）× 配色（60-30-10，单一强调色）。每次只在一两个维度上做变化，其余维度保持克制。

## 优雅与克制的起步参数（按方案调整）

1. 一个焦点：画面只有一个主角，标题和主角呼应，不抢。
2. 主标题占画面高 25–45%，副标题约 10%，标签 6–8%；小字不得低于 6%。
3. 强调色只落在 1–3 个字上；全图最多三种主色。
4. 字与场景同一个世界：同一光源方向、同一透视、同一阴影软硬。
5. 重特效（霓虹、金属、玻璃）只给主标题，副标题用干净的无衬线。
6. 留白至少 30%；不要堆砌图标、贴纸和装饰线。
7. 所有文字放在画面中部水平带内，裁成 5:2 时不被切掉。
8. 主标题 ≤ 8 字，文案按作者原文；生成前跑 `scripts/check-title.py`，避开形近字（于/干/千、未/末、己/已/巳、拨/拔、即/既）。
9. 出图逐字核对，错字按问题与成本决定局部修正或直接采用场景图加 `scripts/title-engine.py` 叠字。

## 组合速查

| 组合 | 范式 | 风格 | 标题字 | 场景层 | 配色 | 何时用 |
|---|---|---|---|---|---|---|
| C01 晨雾石刻 | X1 | hard-core-type | 粗黑体刻石，侧光 | 晨雾山谷、远景小人 | 石灰+苔绿+一点朱红 | 宣言、方法论、年度复盘 |
| C02 黄铜铸字 | X1 | hard-core-type | 黑体铸黄铜，倒影 | 深色水泥展厅地面 | 炭灰+黄铜+冷白 | 架构、工程、硬核干货 |
| C03 冰晶发布 | X2 | brand-launch | 玻璃挤出字，边缘霓虹 | 深蓝渐变舞台、产品悬浮 | 深海蓝+冰白+青色光 | 产品发布、版本更新 |
| C04 日出铬金 | X2 | brand-launch | 铬金属倒角字 | 日出地平线、光晕 | 暖金+午夜紫+白 | 新品、里程碑、周年 |
| C05 软糖萌趣 | X3 | ip-fun | 圆润软糖 3D 字 | IP 小动物抱着字 | 奶白+薄荷+一点橙 | 打卡、入门、亲子、轻科普 |
| C06 黏土小镇 | X3 | chao-wan-3d | 黏土手捏字 | 微缩黏土场景 | 奶油+天蓝+番茄红 | 生活方式、兴趣教程 |
| C07 巨数冲击 | X4 | white-clean | 超大 3D 数字+短标题 | 卡通主角站数字旁 | 白底+钴蓝+亮黄 | 榜单、盘点、实测 |
| C08 卡片轻舟 | X5 | white-clean | 干净粗黑体 | 浮动玻璃卡片+人物 | 白→浅蓝+橙 | 工具教程、效率指南 |
| C09 一色到底 | X6 | orange-warm | 超粗黑体占满 | 无场景，满版色块 | 满版橙+白+黑 | 观点、口号、短评 |
| C10 墨色长镜 | X7 | cinematic-flow | 书法大字，墨晕 | 电影感远景、剪影 | 墨黑+宣纸灰+朱印 | 故事、变局、文化 |
| C11 套色印刷 | X8 | news-flash | 粗体孔版印刷字 | 网点、错版、纸纹 | 米纸+荧光粉+深蓝 | 周报、清单、复盘 |
| C12 剪纸拼贴 | X8 | paper-collage | 剪纸字，投影 | 彩纸层叠拼贴 | 牛皮纸+橄榄+珊瑚 | 手作、生活改造 |
| C13 三步阶梯 | X9 | tutorial-steps | 标题在上，编号在下 | 三格步骤插画 | 暖白+焦糖+深棕 | N 步教程、流程 |
| C14 侧光人像 | X10 | bg-blur | 标题竖排或侧排 | 人物半身，背景虚化 | 低饱和+单一暖色 | 个人 IP、访谈、运动 |
| C15 暗夜玻璃 | X11 | dark-saas | 细描边+发光字 | 暗色玻璃面板、连线 | 墨蓝+电光青 | AI、自动化、开发者 |
| C16 霓虹雨夜 | X11 | cyber-neon | 霓虹灯管字 | 雨夜街巷、倒影 | 黑紫+品红+青 | 科技观点、未来趋势 |
| C17 书中山河 | X12 | diorama-book | 招牌字立于场景 | 打开的书里长出微缩世界 | 羊皮纸+青绿+金 | 学习路线、知识地图 |
| C18 杂志留白 | X14 | magazine | 衬线大字+细副标 | 编辑感静物摄影 | 米白+墨黑+一点红 | 深度长文、人物 |
| C19 举牌发声 | X15 | white-clean | 牌子上的手写粗字 | 卡通人物举牌 | 浅色+活力黄 | 口号、活动、出发 |
| C20 手账小记 | X16 | sketch-cartoon | 马克笔手写字 | 手账便签+涂鸦 | 奶油纸+铅笔灰+一色 | 合集、漫步、轻教程 |
| C21 对照两岸 | X13 | gan-huo | 中轴分隔，两侧对称 | 左右两种场景对比 | 冷/暖双色+白 | A vs B、新旧对比 |
| C22 星图典藏 | X14 | academic-print | 古典衬线+金箔 | 星图、仪器版画 | 深蓝+金+象牙 | 科学史、学术科普 |

## 组合模板

### C01 晨雾石刻

- 范式 X1，风格 `hard-core-type`；适合：宣言、方法论、年度复盘。

```text
Monumental headline carved as weathered limestone blocks standing on a misty valley floor, low raking morning light, tiny hiker for scale, one character inlaid with vermilion stone. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C02 黄铜铸字

- 范式 X1，风格 `hard-core-type`；适合：架构、工程、硬核干货。

```text
Headline cast in brushed brass letters standing on a polished dark concrete floor, soft studio top light, crisp reflections, subtitle as small engraved plaque. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C03 冰晶发布

- 范式 X2，风格 `brand-launch`；适合：产品发布、版本更新。

```text
Thick frosted-glass extruded headline floating above a dark blue stage, thin cyan rim light, a sleek product object hovering beside it, gentle floor glow. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C04 日出铬金

- 范式 X2，风格 `brand-launch`；适合：新品、里程碑、周年。

```text
Polished chrome bevelled headline in front of a sunrise horizon, warm lens glow on the edges, purple dusk sky above, clean subtitle in light sans. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C05 软糖萌趣

- 范式 X3，风格 `ip-fun`；适合：打卡、入门、亲子、轻科普。

```text
Soft glossy gummy-candy 3D headline with rounded edges, a cute round mascot animal hugging the last character, pastel studio backdrop, soft contact shadows. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C06 黏土小镇

- 范式 X3，风格 `chao-wan-3d`；适合：生活方式、兴趣教程。

```text
Handmade clay headline with fingerprint texture standing in a tiny clay town, warm diffuse light, small clay character waving, tilt-shift depth of field. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C07 巨数冲击

- 范式 X4，风格 `white-clean`；适合：榜单、盘点、实测。

```text
Huge glossy 3D numeral as the hero, a cheerful cartoon character leaning on it, short bold headline beside, plain light background with soft floor shadow. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C08 卡片轻舟

- 范式 X5，风格 `white-clean`；适合：工具教程、效率指南。

```text
Light SaaS look: friendly person with laptop on the right, three floating rounded glass cards with icons only, headline in bold dark sans on the left, one word in orange. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C09 一色到底

- 范式 X6，风格 `orange-warm`；适合：观点、口号、短评。

```text
Full-bleed saturated color field, a massive ultra-bold headline filling most of the height, tiny subtitle underneath, one small graphic shape as accent, nothing else. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C10 墨色长镜

- 范式 X7，风格 `cinematic-flow`；适合：故事、变局、文化。

```text
Cinematic wide shot of a lone figure on a ridge in drifting ink mist, headline in expressive brush calligraphy across the sky, a small red seal stamp as the accent. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C11 套色印刷

- 范式 X8，风格 `news-flash`；适合：周报、清单、复盘。

```text
Risograph print poster on off-white paper, giant headline in two overprinted ink layers slightly misregistered, halftone dot texture, small spot illustrations. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C12 剪纸拼贴

- 范式 X8，风格 `paper-collage`；适合：手作、生活改造。

```text
Layered cut-paper collage, headline cut from thick colored card with real drop shadows, torn paper edges, a few paper plants and objects arranged around. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C13 三步阶梯

- 范式 X9，风格 `tutorial-steps`；适合：N 步教程、流程。

```text
Headline across the upper area, below it three illustrated step panels with big numerals 1 2 3 and objects only, consistent warm lighting, clean gutters. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C14 侧光人像

- 范式 X10，风格 `bg-blur`；适合：个人 IP、访谈、运动。

```text
Half-body portrait on the right with shallow depth of field, headline stacked on the left in heavy sans lit by the same warm side light, soft bokeh city. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C15 暗夜玻璃

- 范式 X11，风格 `dark-saas`；适合：AI、自动化、开发者。

```text
Dark interface-inspired scene with layered glass panels connected by glowing lines, headline in bright clean sans with subtle glow, icons only on panels. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C16 霓虹雨夜

- 范式 X11，风格 `cyber-neon`；适合：科技观点、未来趋势。

```text
Headline built from neon tubes mounted on a wet alley wall at night, magenta and cyan reflections in puddles, light rain, one character in a different color. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C17 书中山河

- 范式 X12，风格 `diorama-book`；适合：学习路线、知识地图。

```text
An open book with a miniature landscape growing out of its pages, paths and tiny travellers, headline as a carved wooden signboard standing on the pages. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C18 杂志留白

- 范式 X14，风格 `magazine`；适合：深度长文、人物。

```text
Editorial magazine cover feel: one refined still-life object in soft window light, generous negative space, headline in elegant high-contrast serif, thin rule lines. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C19 举牌发声

- 范式 X15，风格 `white-clean`；适合：口号、活动、出发。

```text
Cartoon character holding up a big cardboard sign with the headline written in thick marker, cheerful pose, bright simple background, subtitle below the sign. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C20 手账小记

- 范式 X16，风格 `sketch-cartoon`；适合：合集、漫步、轻教程。

```text
Hand-drawn notebook page with sticky notes, doodles and washi tape, headline in bold marker lettering, a small sketched character, restrained single accent color. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C21 对照两岸

- 范式 X13，风格 `gan-huo`；适合：A vs B、新旧对比。

```text
Split composition: cool muted scene on the left, warm vivid scene on the right, headline centered across the seam on a solid band, perfectly balanced. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```

### C22 星图典藏

- 范式 X14，风格 `academic-print`；适合：科学史、学术科普。

```text
Antique engraving style star chart with brass instruments, headline in classical serif foil-stamped in gold, ivory subtitle, subtle paper grain. Typography rules: headline exactly "{title}", subtitle exactly "{subtitle}", Simplified Chinese characters exactly as given, no other text. Headline about 25-45% of image height, subtitle about 10%, one alignment line, 6% safe margin. One accent color on 1-3 key characters only. Letters share the scene lighting, shadows and perspective. Keep all text within the central horizontal band. One focal point, generous negative space, no watermark, no logo, no gibberish. Wide 16:9.
```
