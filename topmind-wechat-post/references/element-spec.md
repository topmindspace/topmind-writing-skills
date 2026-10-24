# 元素渲染规范

`md2wechat.py` 把 Markdown 转成公众号内联样式 HTML 的**唯一依据**。
改渲染逻辑或新增语法时，先改本文件再改代码；`audit_inline()` 是本文件的自动校验版本。

合规分级（贯穿全篇）：

| 级别 | 含义 | 处理原则 |
|---|---|---|
| **S** 安全 | 内联纯色/边框/字号，不会静默失效 | 可以放心依赖 |
| **D** 降级 | 可能被丢弃，但丢了不破坏结构与可读性 | 可用，但**不得作为唯一区分手段** |
| **X** 禁用 | 会静默失效或整段被吞 | 一律不用；`audit_inline` 判 ERROR |

---

## 一、块级元素

| Markdown | 产物 | 级 | 说明 |
|---|---|---|---|
| `# 标题` | `<p style="20px/700/center">` | S | 不用 `<h1>`（微信按标题语义覆盖字号） |
| `## 标题` | `<h2 style="18px/700;color:text_strong">`；手写序号原样保留，都没写时才自动编号 | S | 见下方「章节编号」 |
| `### 标题` | `<h3 style="16px/600">` | S | |
| `#### 标题` | `<h4 style="15px/600">` | S | |
| 段落 | `<p style="margin:0 0 {para_gap};line-height:{line_height};letter-spacing:0.5px;text-align:left;word-break:break-word">` | S | `text-align` 只允许 left/center/right |
| `---` | 嵌套 `<section>`：外层 `margin:32px 0`，内层 `<section style="width:12%;height:2px;background:accent;margin:0 auto">` | S | 宽度用百分比，块级 `margin:0 auto` 居中，**不用 `display:inline-block`**：那是生成器自己的输出，用户无从修正，inline-block 会在合规自检里留下一条洗不掉的 WARN |
| `> 引用` | `<section>` + `background:surface` + 大圆角（无衬条，MD3 优雅） | S | **不用 `<blockquote>`**：微信有原生引用样式会覆盖我们的配色 |
| `- 项` / `1. 项` | `<ul>`/`<ol>` + `<li>`，支持嵌套 | S | 圆点颜色取 accent |
| ```` ```lang ```` | `<section background:code_bg>` → 语言标签 `<section>` → 代码体 `<section style="white-space:pre-wrap;word-break:break-all">` | S | **不用 `<pre>`**；详见「代码块」 |
| 表格（≤3 列） | `<table style="width:100%">`，表头行是首个 `<tr>` | S | **不写 `table-layout:fixed`**，**不用 `thead/tbody/colgroup`** |
| 表格（≥4 列） | 自动转卡片：每行一张 `<section>`，首列作标题、其余「列名 + 值」成对 | S | 公众号列数 >4 必然横向溢出，卡片化是唯一稳的解法 |
| `![说明](src)` | `<section>` → `<p center>` → `<img style="max-width:100%;height:auto;display:block;margin:0 auto">` | S | **不用 `width:100%`**（小图被拉满变糊）；**不用 `<figure>`** |
| `*图注*`（紧随图片） | `<p style="13px;color:text_light;center">` | S | 独立 `<p>`，不嵌在图片块里 |

---

## 二、行内元素

| Markdown | 产物 | 级 | 视觉层级 |
|---|---|---|---|
| `**文字**` | `<strong style="font-weight:600;color:text_strong">` | S | 加粗（源稿推荐的唯一强调手段） |
| `*文字*` | `<em style="font-style:normal;color:text_muted">` | S | 弱化 |
| `` `代码` `` | `<code style="background:surface;color:accent;font-family:mono">` | S | |
| `==文字==` | `<strong>` + `background:accent_soft` | S | 兼容读取：旧稿高亮照常渲染，新稿不用 |
| `++文字++` 或 `<u>文字</u>` | `<span style="border-bottom:2px solid accent_light;font-weight:600;color:text_strong">` | S | 兼容读取：旧稿下划线照常渲染，新稿不用 |
| `~~文字~~` | `<span style="background:accent_soft;font-weight:600">` | S | 兼容读取：旧稿半高亮照常渲染，新稿不用 |
| `[!文字]` | `<span style="11px;color:accent;background:accent_soft;padding:1px 6px">` | S | 徽章；不用 `inline-block` |
| `[文字](url)` | 正文 `文字` + 上标 `[n]`，文末「参考链接」块 | S | 公众号正文不支持可点外链 |

### 强调（源稿只用标准 Markdown）

源稿是单源纯 Markdown（Obsidian、X 派生、公众号派生共用），强调只用 `**加粗**` 和引用块，不写 `++下划线++`、`==高亮==`、`~~荧光笔~~` 这类扩展标记。

- 加粗留给结论句、关键数据、产品名；没有固定上限，`lint-wechat.py` 只在强调占比超过 20% 时提醒「重点过多」
- 旧稿里已有的扩展标记，`md2wechat.py` 照常渲染（兼容读取），lint 不报、不计覆盖率

---

## 三、容器（只用于旧交付包）

`:::` 是自研中间标记（公众号不认 Markdown，由 `md2wechat.py` 转成内联样式 HTML）。
**新源稿不用容器**（单源 Markdown，见 `typography-rules.md`）；本节只为旧交付包和 `out/` 下可选的派生稿保留。

| 写法 | 产物 | 用在哪 |
|---|---|---|
| `::: note` | 灰边说明块 | 补充说明 |
| `::: tip` | 绿边提示块 | 实操建议 |
| `::: warn` | 琥珀边注意块 | 风险提醒 |
| `::: danger` | 红边警告块 | 严重风险 |
| `::: pull` | 上下框线 + 居中金句 | 全文点睛，1–2 处 |
| `::: stat` | 浅底卡片 + 大号 accent 数字 | 关键数据（`数值 \| 说明` 每行一条） |
| `::: dialogue` | 说话人 + 气泡 | 访谈、问答 |
| `::: toc` | 前言导读卡 | 一般不用手写，见「自动导读」 |
| `::: sign` | 尾部签名区 | 一般不用手写，见「自动签名」 |

容器名拼错会**静默降级成 note**——`lint-wechat.py` 会报未知容器。
别名（`info`/`memo`→note，`success`/`ok`→tip，`quote`/`golden`→pull，`data`/`metric`→stat，
`chat`/`talk`→dialogue）等价。

---

## 四、三段自动行为

### 章节编号

- **默认保留手写序号**：任一二级标题带手写序号（`一、` / `第一章` / `1.`）时，标题原样输出，
  不再叠加自动编号，前言导读用「·」列项：`## 一、官方总表` → `一、官方总表`
- 整篇二级标题都没写序号时，才由排版层自动编号
- `--auto-number` 恢复旧行为：剥离手写序号后统一编号（`## 一、官方总表` → `01 官方总表`）；
  剥离规则：中文序号（`一、`/`第一、`）、阿拉伯序号（`1.`/`01 `），
  带负向断言保护：`## 3.4× 成本` **不会**被误剥成 `4× 成本`
- 自动编号的样式由 `h2_style` 决定：`number`（01 + 左竖条，默认）/ `bar`（仅左竖条）/
  `underline`（下划线）/ `center`（上下框线）/ `plain`（无装饰）
- **末章若为收束类用 `∞` 而不是顺延数字**：标题匹配
  总结/结语/小结/尾声/后记/写在最后/写在后面/收尾/结尾/余论 时，编号取 `∞`
  （`number` 样式下生效）。理由：数字编号暗示"还有下一节"，与收束章的定位打架。
  实测 `## 六、总结` → `∞ 总结`，其余仍为 `01`…`05`。
- 手写序号与自动编号二选一，**不要混用**（部分标题写、部分不写），否则手写的那几节会和自动编号重号

### 前言导读

- 触发条件（满足任一，且 `toc` 未被 `--no-toc` 关闭）：
  - 章节数 ≥ `toc_min_h2`（默认 4）
  - 章节数 ≥ 3 且正文 ≥ `toc_min_chars`（默认 2000 中文字）
- 位置：**首个正文段落之后**（不是标题与封面图之间）
- 内容：最多 `toc_max`（默认 5）条，超出时附注「……共 N 节」
  ——**不假装全文只有这几节**
- **导读的标记必须与正文标题一致**：
  - 标题带编号（`number`）→ 导读也编号，末章收束类同为 `∞`
  - 标题不带编号（`center`/`underline`/`plain`）→ 导读用中性圆点 `·`，
    **不能凭空造出 01/02**（否则读者在正文里找不到对应的编号）
- 显式 `::: toc` 优先于自动插入

### 尾部签名

`--signature` 三态：

| 值 | 行为 |
|---|---|
| `auto`（默认） | 稿件末尾**已自带**签名/CTA 则不再追加，避免出现两处签名区 |
| `on` | 无条件追加 |
| `off` | 只在显式写了 `::: sign` 时渲染 |

- 署名区**不渲染「自我介绍」行**（「我是{{作者名}}，{{一句话简介}}」读者不关心）；
  只保留三连 CTA。`--author` / `--author-bio` 参数保留仅为兼容旧调用，不再使用
- 判定「已自带」的口径：正文末尾 8 个非空段落内出现
  `点赞 / 在看 / 三连 / 点个关注 / 欢迎关注 / 关注「 / 扫码 / 分享给`

---

## 五、代码块

- **不用 `<pre>`**：公众号端不自动换行，窄屏横向溢出，且格式检测会标风险项
- 用 `<section>` + `white-space:pre-wrap` + `word-break:break-all`
- 缩进与换行由代码自身提供：**HTML 源码里不在 pre-wrap 容器内插入任何格式化换行**
  （插了就会渲染出伪空行和大左缩进）
- **色板跟随主题**（`code_scheme`）：
  - `mono`（默认）：只用「主色 + 明暗层级」。注释最暗、字符串次之、
    关键字取主色的提亮版、其余用 `code_text`
  - `palenight`：Material Palenight 的 16 色，**已不推荐**——
    天蓝/翠绿/橙红与砖红、琥珀等主色毫无关系，一篇文章里会出现两套色彩语言
- 语言标签显示在代码体上方，字号 11px，颜色取 accent

---

## 六、`audit_inline()` 检查清单

每次生成 HTML 后自动跑，`ERROR` 必须清零。检查项已按本文件分级：

**ERROR**：`<div>` `<figure>` `<figcaption>` `<pre>` `<thead>` `<tbody>` `<colgroup>`
`<h1>` `<iframe>` `<video>` `<script>` `<style>`；`text-align` 非标准值；
px 固定宽度；`white-space:pre/nowrap`；`position/float/transform/opacity`；
`display:flex/grid`；`-webkit-*`；`linear-gradient`；`box-shadow`；`rgba()/hsla()`；
`var(--)`；`@media/@keyframes`；`class` 属性；Markdown 标记残留（`==`、`**`）

**WARN**：`table-layout:fixed`（列宽均分）、`display:inline-block`（非常规 display 值）、
`border-radius`（可能被丢，属优雅降级）、图片 `width:100%`、`id` 属性、
`<img width="...">` 属性

WARN 表示「已知风险，需确认是否可接受」，不能直接忽略。
