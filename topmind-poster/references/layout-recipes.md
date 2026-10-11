# 版式配方

出图时反复要用到的数字与样式。写 HTML 之前先查这里，别每次现调。

## 一、画布

| 用途 | 宽度 | 说明 |
|---|---|---|
| 公众号长图 / 通用分享 | 1080 | 手机一屏宽，最稳 |
| 内容密度高（榜单、多栏、多列） | 1180 | 列宽够放 6–8 个字的标签 |
| X / 推特长图 | 1200 | X 会自动压缩，别超 1200 |

```css
body { width: 1180px; margin: 0; }        /* 写死，不要 max-width */
.page { padding: 52px 56px 44px; }        /* 上下留白比左右大一点更稳 */
```

**不要用 `max-width` + 百分比**：截图宽度会随窗口变，同一份 HTML 两次出图宽度不一样。

## 二、字号层级

| 层级 | 字号 | 字重 | 用途 |
|---|---|---|---|
| 主标题 | 64–76px | 800–900 | 一屏只有一处 |
| 章节标题 | 38–44px | 700 | 每段一处 |
| 卡片标题 / 工具名 | 30–36px | 600–700 | 卡片第一行 |
| 正文 | 22–26px | 400 | `line-height: 1.6` |
| 图注 / 来源 | 17–19px | 400 | 用 `--ink-3` 弱化 |

字号往下越界（正文 < 20px）在手机上就看不清了。**宁少写几行，别缩字号。**

## 三、配色

浅底和深底各一套，写死 hex（不要引用主题变量，落盘图里解析不到）。

### 浅底（公众号、报告类）

```css
--bg:      #F7F8FA;   /* 页面底 */
--card:    #FFFFFF;   /* 卡片 */
--line:    #E5E8EE;   /* 分隔线 */
--ink-1:   #0F172A;   /* 主文字 */
--ink-2:   #475569;   /* 次文字 */
--ink-3:   #94A3B8;   /* 图注、来源 */
--accent:  #1D63D2;   /* 强调、填充条 */
```

### 深底（榜单、封面延伸、科技感）

```css
--bg:      #0A0D14;   /* 近黑，不是纯黑 —— 纯黑死板 */
--card:    #141922;   /* 卡片 */
--line:    #232A36;   /* 分隔线 */
--ink-1:   #F1F5F9;
--ink-2:   #A8B3C4;
--ink-3:   #6B7688;
--gold:    #D9A62E;   /* 金，配 #F3DE9B 做渐变 */
```

**卡片阴影**（浅底）——比纯边框干净得多：

```css
box-shadow: 0 1px 2px rgba(15,23,42,.05), 0 10px 26px -18px rgba(15,23,42,.22);
```

**深底不要用阴影**（看不出来），改用 1px 描边 + 极淡内发光：

```css
border: 1px solid var(--line);
box-shadow: inset 0 1px 0 rgba(255,255,255,.04);
```

## 四、栅格

```css
.cards { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
```

**不要用 `flex-wrap`**：内容长短不一的卡片会排成「一个 / 两个」交替，纵向浪费一半、视觉也乱。

**奇数张卡的最后一张会孤零零占半边**，加一行让它铺满：

```css
.cards > .card:last-child:nth-child(odd) { grid-column: 1 / -1; }
```

## 五、进度条 / 柱状图（高频出错点）

```html
<div class="bar">
  <span class="bl">Claude Code</span>
  <span class="track"><span class="fill" style="width:39%"></span></span>
  <span class="bv">39%</span>
</div>
```

```css
.bar   { display: flex; align-items: center; gap: 12px; }
.bl    { width: 208px; flex: 0 0 208px; text-align: right; }  /* 标签列：够长，别 ellipsis 截断 */
.track { flex: 1; height: 20px; background: rgba(148,163,184,.18);
         border-radius: 5px; overflow: hidden; }
.fill  { display: block; height: 100%;              /* ← 缺这行整条填充消失 */
         background: linear-gradient(90deg,#1D63D2,#4A90E2); }
.bv    { width: 84px; flex: 0 0 84px; font-variant-numeric: tabular-nums; }
```

两个必守项：

1. `.fill` 必须 `display:block`（`<span>` 默认 inline，`width/height` 全失效 → 填充整条不可见，极易误判成「配色太浅」）
2. 标签列 `width` 给足，否则长名字被 `text-overflow: ellipsis` 切成 `…`。**208px 装得下约 9 个中文字 / 20 个英文字符**

## 六、徽章 / 图标

用内联 SVG，写死 `stroke`，**不要用 emoji**（字体不一致、跨端变形、打印会掉色）。

```html
<svg viewBox="0 0 24 24" width="22" height="22" fill="none"
     stroke="#D9A62E" stroke-width="1.8" stroke-linejoin="round">
  <path d="M12 3 20 7.5v9L12 21 4 16.5v-9z"/>
  <path d="m9 12 2 2 4-4"/>
</svg>
```

要成组出现时写个 `badge(level)` 函数按段位返回不同色值，别在 HTML 里散着写。

## 七、常用版式模板

### 榜单型（分级 / 排名）

```
页眉：标题 + 副标题（口径与时点）
每档：段位色块 + 段位名 + 席位数 + 卡片网格
页脚：来源 + [章节N / 总M]
```

### 对比型（A vs B）

左中右三栏：`grid-template-columns: 1fr 84px 1fr`，中间列放 `VS` 或箭头。**不要用表格**——表格在窄屏上要么挤要么溢出。

### 数据卡型

```
大数字（64px tabular-nums）+ 一行说明（22px）
+ 一个小趋势标记（↑2.3pt / ↓6pt）
+ 图注：来源与时点（17px --ink-3）
```

数字用 `font-variant-numeric: tabular-nums`，多行数字才对齐。

## 八、页眉页脚

每张图（尤其分段图）都带：

- **页眉**：章节编号 + 标题——读者单张转发也能对上号
- **页脚**：`章节名 / 总张数` + 来源

```css
.foot { margin-top: 34px; padding-top: 18px; border-top: 1px solid var(--line);
        display: flex; justify-content: space-between;
        font-size: 17px; color: var(--ink-3); }
```
