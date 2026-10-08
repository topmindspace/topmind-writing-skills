# topmind-x-article · X 长文一键发布

[English](./README.en.md) | 中文

把 Markdown 原稿变成"复制 → 粘贴 → 发"的 X 长文（Article）发布包。

- 版本：**v0.4.8**（随 `@topmindspace/topmind-writing-skills@0.8.24` 发布）

## 安装

```bash
npx @topmindspace/topmind-writing-skills install topmind-x-article
```

## 用法

```bash
# 1. 原稿转一键复制 HTML（首选）
python3 scripts/md2x-html.py <原稿>.md --out <包>/X长文.html \
  --images-from 公众号稿.md [--cover cover-1500x600.png]
# --images-from 从公众号稿按文档顺序派生图片（X 稿由公众号稿派生时必用）；
# 禁止手工拼 --images 列表（文件名排序 ≠ 文档顺序，曾导致整段配图错位）。
# 浏览器打开 X长文.html → 点页顶「一键复制全文」→ 粘贴进 X Article 编辑器正文
# （首个 # 标题不进剪贴板，手动填入 X 标题栏；封面在 X 独立入口单独上传）

# 2. 纯文本兜底（HTML 复制异常时）
python3 scripts/md2x.py <原稿>.md --out <包>/X发布稿.txt

# 3. 封面图：用 topmind-cover 生成 1200×675

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
引用去 `>`。转完必须人工通读一遍。

## 最小示例

输入（10 行 markdown）：

```markdown
# Manus 2.0 发布了

**从零重建**的 Agent，新增了 Cue 个人助手。

![发布会现场](cover.png)

| Token 消耗 | -23.2% |
| 耗时 | -28.2% |

详见[官方博客](https://manus.im/blog)。
```

`python3 scripts/md2x.py 原稿.md --out X发布稿.txt` 得到：

```
Manus 2.0 发布了

从零重建的 Agent，新增了 Cue 个人助手。

[图1]

Token 消耗：-23.2%
耗时：-28.2%

详见官方博客（https://manus.im/blog）。

—— 配图清单 ——
[图1] 发布会现场
```

复制 `X发布稿.txt` 全文 → 粘贴进 X Article 编辑器 → 按 `[图N]` 顺序上传配图 → 发布。

## 发布

X 长文目前走人工粘贴发布（X Article 编辑器），API 不发长文。
发布后按清单做：首条评论置顶补信息、全文抓回核对。

## 外部依赖

以下技能**不在本仓库**（一般随用户侧 workbuddy 环境提供）。缺失时对应路由能力
不可用，不影响本技能核心流程（原稿转文本、封面、发布清单）：

- `topmind-x`（topmind-skills 包）：短推文发帖连接器，须用户确认后才发；xurl 只覆盖短推文，不发长文。短帖写稿走 `topmind-viral-posts` / `topmind-briefs`。
- `topmind-capture`：「只想存档不发布」时的收录路由。

## 开发

```bash
python3 scripts/package_skill.py --check   # 发布前校验
python3 scripts/negative_tests.py          # 异常输入测试
```
