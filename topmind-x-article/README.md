# topmind-x-article · X 长文一键发布

[English](./README.en.md) | 中文

一篇长文只有一份源稿 `<文章名>/<文章名>.md`：默认先过 topmind-revise、交付这份 Markdown；
要发 X 时再按需派生"复制 → 粘贴 → 发"的 X 长文（Article）发布包到 `out/`。

- 版本：**v0.4.22**（随 `@topmindspace/topmind-writing-skills@0.8.45` 发布）

## 安装

```bash
npx @topmindspace/topmind-writing-skills install topmind-x-article
```

## 用法

```bash
# 0. 建文章文件夹 + 结构体检（图片写 ![说明](images/01-xx.png)，出处写在下一行「来源：……」）
python3 scripts/article_scaffold.py --title "文章名"
python3 scripts/check_article.py 文章名/

# 1. 按需：一键复制 HTML（首选），产物 文章名/out/X长文.html
python3 scripts/md2x-html.py 文章名/文章名.md
# 直接读源稿的 ![]() 按文档顺序嵌图，封面缺省读 frontmatter 的 cover；
# 禁止手工拼 --images 列表（文件名排序 ≠ 文档顺序，曾导致整段配图错位）。
# 浏览器打开 X长文.html → 点页顶「一键复制全文」→ 粘贴进 X Article 编辑器正文
# （首个 # 标题不进剪贴板，手动填入 X 标题栏；封面在 X 独立入口单独上传）
# 旧结构：md2x-html.py X长文.md --out X长文.html --images-from 公众号稿.md

# 2. 按需：纯文本兜底（HTML 复制异常时），产物 文章名/out/X发布稿.txt
python3 scripts/md2x.py 文章名/文章名.md

# 3. 封面图：用 topmind-cover 生成 1500×600

# 4. 按 references/publish-checklist.md 逐项发布
```

## 转换规则

HTML 链路按 `references/x-html-format.md`：富文本粘贴进 X 编辑器（标题/加粗/链接/
列表/引用块保留）；` ``` ` 提示词块渲染为引用块 + 「复制提示词」按钮；GFM 表格转列表
（X 粘贴丢弃 `<table>`）；首个 `#` 标题不进剪贴板；配图 base64 内嵌、按 `[图N]` 编号，
带不入编辑器时用图下「下载图片」按编号上传。

提示词的复制分双通道：作者侧用 HTML 里的「复制提示词」按钮（发布前取用文本）；
读者侧一键复制只能来自 X 原生代码块（Insert → Code 手动逐块转换；原生代码块带
native copy button，粘贴 `<pre>` 会被 X 丢弃，走不过去）。

纯文本兜底按 `references/x-format.md`：标题→纯文本行、分隔线→空行、加粗/斜体/
行内代码去标记、链接→`文字（url）`、图片→`[图N]`（文末附配图清单）、表格→"项：值"列表、
引用去 `>`；列表默认转「· 」「1）」（嵌套缩进两格，最多两层，因为 X 纯文本不渲染 Markdown 列表；
`--list-style emoji` 可选 🔹 / ▫️ / 1️⃣，`--list-style keep` 保留原符号，规则见 `references/x-post-format.md`）。转完必须人工通读一遍；
可用 `python3 scripts/lint_x_post.py X发布稿.txt --long` 自检。X 长文 HTML 走 X Article 编辑器富文本，原生列表保留。

## 最小示例

输入（10 行 markdown）：

```markdown
# 晨光 3.0 发布了

**全新设计**的写作助手，新增了离线模式。

![发布会现场](cover.png)

| Token 消耗 | -20% |
| 耗时 | -30% |

详见[官方博客](https://example.com/blog)。
```

`python3 scripts/md2x.py 原稿.md --out X发布稿.txt` 得到：

```
晨光 3.0 发布了

全新设计的写作助手，新增了离线模式。

[图1]

Token 消耗：-20%
耗时：-30%

详见官方博客（https://example.com/blog）。

—— 配图清单 ——
[图1] 发布会现场
```

复制 `X发布稿.txt` 全文 → 粘贴进 X Article 编辑器 → 按 `[图N]` 顺序上传配图 → 发布。

## 发布

X 长文目前走人工粘贴发布（X Article 编辑器），API 不发长文。
发布后按清单做：首条评论置顶补信息、全文抓回核对。

## 外部依赖

以下技能**不在本仓库**（由宿主智能体环境另行提供）。缺失时对应路由能力
不可用，不影响本技能核心流程（原稿转文本、封面、发布清单）：

- `topmind-x`（topmind-skills 包）：短推文发帖连接器，须用户确认后才发；xurl 只覆盖短推文，不发长文。短帖写稿走 `topmind-viral-posts` / `topmind-briefs`。
- `topmind-capture`：「只想存档不发布」时的收录路由。

## 开发

```bash
python3 scripts/package_skill.py --check   # 发布前校验
python3 scripts/negative_tests.py          # 异常输入测试
```

## 原创示例

我们自己写的示例输出见 [`examples/`](./examples/)（虚构或中性题材，不收录任何第三方原文）。
