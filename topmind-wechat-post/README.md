# topmind-wechat-post · 公众号长文

[English](./README.en.md) | 中文

**从选题到发布清单，一篇公众号长文的完整流程。** 单源文章文件夹、骨架里先写「我的判断」、质量三关（事实 / 逻辑 / 去 AI 味，默认组合 `topmind-revise`）、图片内嵌的微信排版（粘贴即带图）、交付前的图文预览、发布清单和状态同步。

- 版本：**v0.3.19**

你可以这样说：「写公众号」「公众号排版」「公众号定稿」「出公众号发布清单」。

亮点：

- **先有判断**：骨架必填 3–5 条判断，每条写依据和读者会怎么反驳；方法论、架构、对比类文章至少一张自制图。
- **粘贴即带图**：`md2wechat.py --embed-images`，图片 base64 内嵌，手写小标题序号原样保留；「·」列表逐行分开。
- **图文预览**：`--preview` 按手机宽度截出 `out/预览.png`，交付前先看一遍。

一篇长文一个文件夹 `<文章名>/`，唯一源稿 `<文章名>.md`（Obsidian 里直接能看），图片按出现顺序放 `images/`；公众号 HTML 只在需要时生成到 `out/`。旧的 `YYYY-MM-DD-名/公众号稿.md` 交付包只读兼容，不自动迁移。

## 安装

```bash
npx @topmindspace/topmind-writing-skills install topmind-wechat-post
```

## 用法

```bash
export TOPMIND_WORKSPACE=/path/to/workspace   # 推荐：按名称发现「长文」类别 + {当年}-公众号；或用 --base 指定专题目录

# 新建文章文件夹：<专题>/标题/标题.md + images/ cover/ raw/ out/ 参考/ + 骨架.md、素材来源.md（--legacy --slug 建旧交付包）
python3 scripts/new-article.py --title "标题"
A=<专题>/标题

# 结构体检：frontmatter、标题一致、图片存在且按出现顺序编号、无 ::: / callout / ![[ ]]
python3 scripts/check_article.py $A

# 排版体检 + 自动修正（新源稿里的 ::: 容器报错）
python3 scripts/lint-wechat.py --input $A/标题.md --fix

# 去 AI 味（装了 topmind-revise 时由它跑）：W 每条有结论，H 只供判断；总分目标 ≥85
python3 scripts/de_ai_lint.py $A/标题.md --genre long
python3 scripts/scan_ai_flavor.py $A/标题.md

# 按需：Markdown → 全内联 HTML 到 $A/out/（必加 --embed-images，否则粘贴丢图）
python3 scripts/md2wechat.py --input $A/标题.md --embed-images --preview

# 状态同步：只改 frontmatter，目录名不变
python3 scripts/sync-status.py --set 定稿 $A --apply

# 有源稿时：改稿保真双向溯源
python3 scripts/audit-provenance.py --draft $A --source $A/raw/源稿.md
```

脚本纯 Python 标准库，零依赖。

## 最小示例

输入 `demo.md`：

    # 标题

    开头钩子段落。

    ## 一、第一章

    正文文字，**重点**加粗。

    ![示意图](images/a.png)

    来源：某项目官方文档

```bash
# 先在 demo.md 同级放一张真实图片到 images/a.png（缺图会进"未内嵌"清单，粘贴后丢图）
mkdir -p images && cp /path/to/你的图.png images/a.png
python3 scripts/md2wechat.py --input demo.md --out-dir demo --slug demo --embed-images
```

输出 `demo/demo-公众号版.html`（浏览器打开 → 点「复制正文」→ 粘贴到公众号后台）：

```html
<!-- 手写的「一、」原样保留，不再叠加自动编号（都没写时才自动编号；--auto-number 恢复旧行为） -->
<h2 ...>一、第一章</h2>
<!-- 图片下一行的「来源：」渲染成灰色小字图注 -->
<!-- 图片 base64 内嵌，粘贴即带图 -->
<img src="data:image/png;base64,iVBORw0KGgo..." ...>
```

附带 `demo/图片上传清单.md`：图片 / mermaid 图表 / 参考链接的上传与核对清单。

## md2wechat 参数

| 参数 | 说明 |
|------|------|
| `--input` | 必填：输入 md（新结构就是 `<文章名>.md`） |
| `--out-dir` / `--slug` | 可选：缺省分别为 `<输入目录>/out`、输入文件名 |
| `--auto-number` | 剥离手写小标题序号、统一自动编号（旧行为）；默认手写序号原样保留 |
| `--embed-images` | 图片 base64 内嵌（必加，否则粘贴丢图） |
| `--theme` | 主题标识 / 中文名 / JSON 路径，或 `genre:题材` 按题材自动选；`--list-themes` 查看全部 |
| `--link-mode` | 外链形态：`footnote`（默认：正文上标 `[n]` + 文末「参考链接」）/ `inline`（文字正常、URL 灰小字：`文字（url）`）/ `note`（整块灰小字：`文字（url）`） |
| `--asset-root` | 素材根目录，用于解析稿中 `../assets/` 形式的图片路径（缺省输入目录） |
| `--no-toc` | 不自动插入前言导读 |
| `--signature` / `--author` / `--author-bio` | 尾部签名区：`auto`（默认，有签名则不重复）/ `on` / `off`，署名与简介 |
| `--no-pangu` | 关闭中英文自动加空格 |
| `--render-mermaid` | 有 mmdc 时把 mermaid 渲染成 PNG |

## 三条路径

- **forward**：底稿 → 公众号（审校改写）
- **reverse**：选题原创 → 公众号 → 可选回推
- **站外拉取**：在线精选站 → 按 reverse 处理

## 质量三关

事实（一手来源）/ 逻辑（结构一致）/ 文字（去 AI 味 ≥85）。

## 相关技能

- 封面配图 → `topmind-cover`（X 长文 / 公众号共用封面）
- X 长文 → `topmind-x-article`（Markdown 原稿一键转 X 发布包）

## 外部依赖

无必需的外部技能。去 AI 味规则与检查随包自带（`references/de-ai-rules.md`、`scripts/lint_x_post.py --md`、`scripts/scan_ai_flavor.py`）。想接入自己的扫描脚本时设 `$TOPMIND_AI_SCAN=/path/to/script.py`，参数与退出码原样转发。

## 开发

```bash
python3 scripts/package_skill.py --check
python3 scripts/negative_tests.py
```

## 原创示例

我们自己写的示例输出见 [`examples/`](./examples/)（虚构或中性题材，不收录任何第三方原文）。
