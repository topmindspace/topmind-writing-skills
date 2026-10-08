---
name: topmind-poster
description: "HTML+CSS 排版并输出高清长图 / 海报 / 信息图 PNG，也覆盖「一段一图」的分段图批量出图（一篇长文 = N 张图，生成器 + 渲染器工作流）。Use when 长图、海报、信息图、分级榜、榜单图、月报长图、竖版长图、分段图、一张图讲清楚、给文章配图、把 HTML 渲染成 PNG、重做这张图、出 2× 高清图、自动裁掉底部空白、把超长图拆成多张。Do NOT use for 单张文章封面（→ topmind-cover）、多页演示或 PPTX（→ topmind-presentation）、纯数据图表 SVG。"
license: MIT
metadata:
  version: "0.1.1"
  action_category: "write"
  triggers: "长图, 海报, 信息图, 分级榜, 榜单图, 月报长图, 分段图, HTML 转 PNG, 高清出图, poster, long image, 做一张长图, 重做这张图, 更新这张图, 把这张图优化一下, 出一张高清图, 把长图拆成几张, 给文章配图"
  author: "TopMindSpace"
  homepage: "https://github.com/topmindspace/topmind-writing-skills#readme"
  updated: "2026-10-08"
---

# topmind-poster · HTML → 高清长图 PNG

榜单、信息图、月报长图、海报，以及「一段一图」的分段图批量出图。

## 什么时候用

- 用户丢一张海报 / 分级榜 / 信息图，说「再调研一下，更新重做」
- 要做公众号 / X 的竖版长图、信息图、月度榜单
- 已有 HTML 想导出 2× 高清 PNG 并裁掉多余留白
- 一篇长文要配 N 张分段图（不要一张 1:5 的超长图）

## When NOT to use · 何时不用

- **文章封面**（一张图定调、无密集文本）→ 走 `topmind-cover`，它有自己的生图配方与裁剪链
- **多页演示 / PPTX** → 走 `topmind-presentation`
- **纯数据图表 SVG**（要能二次编辑矢量）→ 走 `svg-infographic-kit`
- **文章正文排版**（公众号内联样式、X 长文一键复制）→ 走 `topmind-wechat-post` / `topmind-x-article`
- **要求「画得好看」的插画 / 概念图**（没有精确文本）→ 走生图，别用 HTML 硬凑

判据就一条：**图里有没有必须逐字正确的文本与数字**。有 → 本技能；没有 → 生图更快更容易出效果。

## 为什么不用图片生成模型

榜单 / 信息图里有大量精确文本、数字、品牌名。图片生成模型会改字、糊字、编造数字。**这类图必须走「HTML 排版 → 无头浏览器截图」**，文本 100% 可控、可 diff、可迭代。

封面是例外——封面是「一张图定调」，没有密集文本，适合走 `topmind-cover` 的生图路线。

## 与其他技能的分工

| 要做的东西 | 用哪个 |
|---|---|
| 一张图讲清楚、信息密集、带精确数字 | **本技能** |
| 文章封面（震撼、主题突出、无密集文本） | `topmind-cover` |
| 多页演示 / PPTX | `topmind-presentation` |
| 纯数据图表 SVG | `svg-infographic-kit` |
| 文章正文排版（公众号 / X 长文） | `topmind-wechat-post` / `topmind-x-article` |

本技能负责**出图那一环**：它们写好文章，本技能把其中一段做成能单独转发的图。

## 标准流程

### 1. 定画布宽度

| 用途 | 宽度（CSS px） |
|---|---|
| 公众号长图 / 通用分享 | **1080** |
| 内容密度高（榜单、多栏） | **1180** |
| X / 推特长图 | 1200 |

`body { width: <W>px; }`，不要用 `max-width` + 百分比，否则截图宽度会随窗口变。

### 2. 排版要点

- 字体栈写全：`"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans CJK SC",-apple-system,sans-serif`
- 卡片用 `box-shadow: 0 1px 2px rgba(15,23,42,.05), 0 10px 26px -18px rgba(15,23,42,.22)`——比纯边框干净得多
- **多条目列表用 `display:grid; grid-template-columns:repeat(2,minmax(0,1fr))`**，不要用 flex-wrap。flex-wrap 会让内容长短不同的条目排成 1 个 / 2 个一行，纵向空间浪费一半、视觉也乱
- 颜色写死 hex，不要引用 IDE 主题变量（落盘图像里解析不到）

### 3. 渲染

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --no-sandbox --disable-gpu --disable-gpu-sandbox \
  --hide-scrollbars --force-device-scale-factor=2 \
  --window-size=<W>,<足够大的高度，如8000> \
  --screenshot=raw.png "file://$PWD/poster.html"
```

**五个参数一个都不能少：**

| 参数 | 不加会怎样 |
|---|---|
| `--headless=new` | 新版无头；`--headless=old` 也可以 |
| `--no-sandbox --disable-gpu-sandbox` | **必须**。macOS 沙箱下会报 `sandbox initialization failed: Operation not permitted`，随后 `GPU process exited unexpectedly` + `FATAL: GPU process isn't usable. Goodbye.` 直接不出图 |
| `--disable-gpu` | 避免 GPU 进程报错刷屏 |
| `--hide-scrollbars` | 右侧滚动条会印进图里 |
| `--force-device-scale-factor=2` | 只用 1× 输出，文字在高分屏上发虚 |

`--window-size` 的**高度给足**（8000 起步），后面自动裁，不要试图先算高度。

### 4. 自动裁掉底部空白

窗口高度的富余部分会是纯背景色，扫底裁掉：

```bash
python3 scripts/render_poster.py poster.html -o poster.png
```

脚本做完整三步（截图 → 扫底 → 裁切），等价于手写：

```python
from PIL import Image
im = Image.open('raw.png').convert('RGB'); w,h = im.size
bg = im.getpixel((5, h - 6))      # 从窗口底部取基准色，不是左上角（见坑 5）
px = im.load(); last = 0
for y in range(h-1, -1, -1):
    if any(px[x,y] != bg for x in range(0, w, 7)):   # 每 7 px 采样，够快够准
        last = y; break
im.crop((0,0,w,min(h, last+1+88))).save('poster.png')  # 88 = 2× 下的 44px 尾巴
```

跑完打印 `im.size` 核对。若内容底边几乎等于窗口高度，**说明内容被截断了**，加大 `--window-size` 重跑。

### 5. 出图后必须自检

**不要生成完就看都不看。** 把长图按等分切成 3–4 段、缩到 700px 宽，逐段用 Read 看图：

```python
im = Image.open('poster.png'); w,h = im.size
n = 4; step = h//n
for i in range(n):
    top, bot = i*step, (h if i==n-1 else (i+1)*step)
    sl = im.crop((0, top, w, bot))
    sl.resize((700, int(sl.height*700/w)), Image.LANCZOS).save(f'p{i+1}.png')
```

重点查四件事：

1. **文字截断**：标签列宽不够会出现 `…`，加宽对应 `width` / `flex-basis`
2. **元素缺失**（见坑 2）
3. **溢出**：有没有文字出框、卡片被压扁
4. **数字与来源**：随机抽 3–5 个关键数字回原文核对

## 已知坑（都踩过）

### 坑 1：无头 Chrome 在本机被沙箱拦

见上表。**症状**：命令返回 0 但 PNG 不存在，或 stderr 刷 `GPU process isn't usable`。

### 坑 2：柱状图 / 进度条填充整条消失

```html
<!-- ❌ 填充不可见：span 默认 display:inline，width/height 全部失效 -->
<div class="track"><span class="fill" style="width:73%"></span></div>

<!-- ✅ -->
<style>.track{flex:1;height:20px;overflow:hidden}
       .fill{display:block;height:100%}  /* ← 关键就这一行 */</style>
```

**极易误判**：看起来像「配色太浅 / 渐变没生效」，实际是元素没有盒子。同类问题还会出现在 `.tag`、徽章、任何用 `<span>` 当块用的地方。

### 坑 3：flex 子项里的百分比高度

父级必须给确定高度（如 `height:20px`），子级 `height:100%` 才生效。父级若是 `auto`，子级 100% 解析为 0。

### 坑 4：切图预览的偏移算错

按 `缩放比例 × 坐标` 反推原始像素位置容易错。**直接用等分切片**（上面第 5 步的代码）比手工估坐标可靠。

预览缩到 700px 后，**正文小字会出现「乱码 / 豆腐块」的假象**（重采样伪影）。判定真假要按原始坐标裁一小块出来看，不要在预览图上就下「字坏了」的结论。

### 坑 5：裁切用的背景色不能从「左上角」取

第 4 步的 `im.getpixel((5,5))` **只在页面是纯色底时成立**。如果页面顶部压了绝对定位的装饰层（聚光渐变、金色网格、顶部发光条），左上角像素是装饰色，用它当基准扫底会一行都匹配不上 → 裁切失效、图尾留一大片空白。

**正确做法**：窗口高度远大于内容，所以从**窗口底部**取基准色（那里必定是纯 `body` 背景）：

```python
bg = im.getpixel((5, h - 6))     # h = 窗口高度，不是内容高度
```

前提是：装饰层只出现在页面顶部、且 `body` 背景是纯色。**整页铺平铺纹理会让扫底彻底失效**——纹理要么去掉，要么只放进内容盒子里，别让它延伸到内容之外的窗口区域。

### 坑 6：PNG 重采样会让体积「变大」而不是变小

反直觉但真实（实测一张 2360×4507 的深底文字图）：

| 处理 | 体积 |
|---|---|
| 原始 2360px PNG | 2086 KB |
| LANCZOS 缩到 1600px 再存 PNG | **2557 KB**（更大了） |
| 缩到 1600px + 调色板量化 256 色 | 968 KB |
| 缩到 1600px + JPEG q90 | 492 KB |

原因：原图是 2× 整数倍渲染，像素色阶本来就少，PNG 压得很好；LANCZOS 插值引入大量中间色，把 PNG 的调色板优势打没了。**要压体积就量化或转 JPEG，别指望「缩小尺寸」**。深底 + 文字这类图，JPEG q90 几乎看不出损失。

### 坑 7：`str.format()` 拼 CSS 会 KeyError

把 CSS 塞进 Python 模板字符串再用 `.format()` 注入正文，CSS 里的 `{` 会被当成占位符：

```
KeyError: '\n  --bg'
```

**改成占位符 + `replace()`**：

```python
SHELL = '<style>' + CSS + '</style>...<div class="page">@@BODY@@</div>...'
doc = SHELL.replace('@@BODY@@', body).replace('{title}', title)
```

## 版式配方

画布尺寸、栅格、配色与排版配方见 [`references/layout-recipes.md`](./references/layout-recipes.md)。

## 多段图工作流（一篇长文 = N 张图）

发长文时常见需求：**不要一张 1:5 的超长图，要一段一图**（便于逐段插进 X 长文 / 公众号）。

不要手工写 N 个 HTML。用一个生成器 + 一个渲染器：

```
build/gen.py      # CSS 常量 + 每个 section 一个 secNN() 函数，产出 N 个独立 HTML
build/render.py   # PAGES 列表 [(html, png)]，循环截图 + 自动裁切
```

`render.py` 每个页面重复第 3、4 步，`--window-size` 高度取所有页面里最高的那个的富余值，统一裁切。12 张图全流程约 30 秒。

**排版要点**：

- 每张图都带完整页眉（章节编号）+ 页脚（`章节名 / 总张数`），读者单张转发也能对上号
- 卡片网格用 `grid-template-columns:1fr 1fr`
- **条目数为奇数时，最后一张会孤零零占半边**。加一行让它铺满：

  ```css
  .cards > .card:last-child:nth-child(odd) { grid-column: 1 / -1; }
  ```

- 徽章 / 图标用内联 SVG（写死 `stroke` 色），不要用 emoji（字体不一致、跨端会变形）

**发布包的分工**（X 长文场景，实测）：

| 落点 | 分辨率 | 为什么 |
|---|---|---|
| `images/` | 全分辨率 PNG（2360px） | **上传用**。X 上传要的是这个 |
| `build/embed/` | 1600px JPEG q90 | **内嵌进单文件 HTML 用**。全分辨率内嵌会让 HTML 涨到 25MB+ |

构建完必查三项：`data-URI` 数量、`[图N]` 连续无缺号、逐张解码与源文件**逐字节比对**。只数数量不看顺序，会出现「数量对、图序整体错位一格」的静默错版。

## 交付清单

出图后至少给三样：

1. `poster.png`——最终长图
2. `poster.html`——可编辑源文件（用户要改字改数必须能自己动）
3. `依据与勘误.md`——每个数字的来源链接 + 口径说明 + 存疑清单

**第 3 项不要省。** 图会被转发出去，别人看不懂「这个 55.5% 是谁家的口径」，图本身没有地方写。

## 内容层面的三条纪律（做榜单 / 信息图时）

1. **每个数字标来源与时点**——「55.5%」和「55.5%（2026-09）」「55.5%（Similarweb 网页口径）」是三个不同的东西
2. **不同量纲不横比**——网页流量份额 ≠ 移动端月活 ≠ 付费席位；同榜混排必须显式声明「按赛道分档，不做统一排名」
3. **不确定的宁可不写**——二手转述的单个数字（无原始榜单交叉验证）要么标注「媒体转述口径」，要么删掉，不要留在图上充数
