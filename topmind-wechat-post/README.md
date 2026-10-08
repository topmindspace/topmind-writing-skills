# topmind-wechat-post · 公众号创作技能

[English](./README.en.md) | 中文

公众号文章全生命周期：交付包、审校改写、质量三关、状态同步、微信内联排版与发布清单。

- 版本：**v0.3.1**（随 `@topmindspace/topmind-writing-skills@0.8.25` 发布）

## 安装

```bash
npx @topmindspace/topmind-writing-skills install topmind-wechat-post
```

## 用法

```bash
export TOPMIND_WORKSPACE=/path/to/workspace   # 推荐：按名称发现「长文」类别 + {当年}-公众号；或用 --base 指定交付包根

# 新建交付包
python3 scripts/new-article.py --slug demo --title "标题" --direction reverse

# 排版体检 + 自动修复
python3 scripts/lint-wechat.py --input <包>/公众号稿.md --fix

# 去 AI 味扫描（目标 ≥85；装了 qu-aiwei-zh 时同时看作者姿态分）
python3 scripts/scan_ai_flavor.py <包>/公众号稿.md

# Markdown → 全内联 HTML（必加 --embed-images，否则粘贴丢图）
python3 scripts/md2wechat.py --input <包>/公众号稿.md --out-dir <包> --slug demo --embed-images

# 状态同步
python3 scripts/sync-status.py --set 定稿 <包> --apply

# 有源稿时：改稿保真双向溯源
python3 scripts/audit-provenance.py --draft <包>/公众号稿.md --source <包>/源稿-*.md
```

脚本纯 Python 标准库，零依赖。

## 最小示例

输入 `demo.md`：

    # 标题

    开头钩子段落。

    ## 第一章

    正文文字，**重点**加粗。

    ![示意图](images/a.png)

```bash
# 先在 demo.md 同级放一张真实图片到 images/a.png（缺图会进"未内嵌"清单，粘贴后丢图）
mkdir -p images && cp /path/to/你的图.png images/a.png
python3 scripts/md2wechat.py --input demo.md --out-dir demo --slug demo --embed-images
```

输出 `demo/demo-公众号版.html`（浏览器打开 → 点「复制正文」→ 粘贴到公众号后台）：

```html
<!-- 二级标题自动编号；"总结"类末章编号为 ∞ -->
<h2 ...><span ...>1</span>第一章</h2>
<!-- 图片 base64 内嵌，粘贴即带图 -->
<img src="data:image/png;base64,iVBORw0KGgo..." ...>
```

附带 `demo/图片上传清单.md`：图片 / mermaid 图表 / 参考链接的上传与核对清单。

## md2wechat 参数

| 参数 | 说明 |
|------|------|
| `--input` / `--out-dir` / `--slug` | 必填：输入 md、输出目录、文件名标识 |
| `--embed-images` | 图片 base64 内嵌（必加，否则粘贴丢图） |
| `--theme` | 主题标识 / 中文名 / JSON 路径，或 `genre:题材` 按题材自动选；`--list-themes` 查看全部 |
| `--link-mode` | 外链形态：`footnote`（默认：正文上标 `[n]` + 文末「参考链接」）/ `inline`（文字正常、URL 灰小字：`文字（url）`）/ `note`（整块灰小字：`文字（url）`） |
| `--asset-root` | 素材根目录，用于解析稿中 `../assets/` 形式的图片路径 |
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

本技能工作流会路由到以下**仓库外**技能（不含于本仓库，一般随用户侧 workbuddy
环境提供）。缺失时对应能力降级/不可用，不影响本仓库脚本的全部功能：

- `humanizer-zh`：中文去 AI 味的保真边界；缺失时「只去 AI 味不排版」路径不可用。
- `qu-aiwei-zh`：中文去 AI 味扫描定位（含作者姿态层）；`scripts/scan_ai_flavor.py` 是转发器，找得到就调它，找不到回落内置实现（只有词面分，会提示）。

## 开发

```bash
python3 scripts/package_skill.py --check
python3 scripts/negative_tests.py
```
