---
name: topmind-x-article
description: "创作或整理 X Article 长文，按需导出可复制 HTML、纯文本、封面与发布清单。保留单源稿与图文顺序，由用户在编辑器发布。普通短帖用 topmind-briefs 或 topmind-viral-posts，纯格式化用 topmind-format。"
license: MIT
metadata:
  version: "0.4.27"
  action_category: "write"
  triggers: "X 长文, 发 X 文章, 写 X 文章, X article, 长文发 X, X 发长文, X 文章排版, 转纯文本, X 纯文本, X发布稿, 发 article, 一键复制, 写 X 长文, X 长文发布, 推特长文, twitter 长文, Twitter Article"
  author: "TopMindSpace"
  homepage: "https://github.com/topmindspace/topmind-writing-skills#readme"
  updated: "2026-10-26"
---

# topmind-x-article · X 长文

创作或整理 X Article，并按需导出可复制 HTML、纯文本、封面和发布清单。默认中文；从用户当前已有稿件接着做，保留明确的语言、结构和风格要求。

## 写作与参考

有原稿先读原稿，有指定参考先实际阅读参考。看 [创作方法与样张](references/creative-practice.md) 的相关样张，提取如何展开主张、展示证据和安排节奏。新文章按素材选择评论、叙事、教程、研究等结构；题材不必套“过去—现在—未来”。

方向不明时可先比较少量标题与开头或结构片段；用户要直接成稿就自行选择贴题方向完成。复杂稿用 [信息设计](references/information-design.md) 的骨架，简单稿随写随调整。图表在能帮助理解时加入，自制结构图和纯文字都是选项。

事实、论证与文字一起核对：承重数字可溯源，必要归因和不确定性留在正文，引用与转述分清。[口吻经验](references/core-voice.md)、[研究方法](references/research-mode.md)、[图源方法](references/image-sourcing.md) 按任务读取；修改可用 [revision-workflow.md](references/revision-workflow.md) 或已安装的 `topmind-revise`，无需为简短或仅导出任务凑全套报告。

## 单源文件与可重建导出

已有文章沿用源稿；新发布包可以建 `<文章名>/<文章名>.md`，配套 `images/`、`cover/`、`素材来源.md`、`raw/`、`out/`。路径依据实际工作区或用户指定位置。

```bash
python3 scripts/article_scaffold.py --title "文章名" --base <已确认目录>
python3 scripts/check_article.py <文章目录>
```

这些脚本采用本仓文章包协议；纯聊天写作无需建完整目录。原稿修改保留可恢复版本，导出从同一源稿重新生成。目录与旧包兼容见 [platform-operations.md](references/platform-operations.md)，协作字段见 [workspace.md](references/workspace.md)。

## 用户需要发布包时

```bash
python3 scripts/md2x-html.py <文章目录>/<文章名>.md --preview
python3 scripts/md2x.py <文章目录>/<文章名>.md
```

- `out/X长文.html` 提供作者侧复制入口。全文复制带文字、格式和 `[图N]` 位置，配图需要在编辑器按位置粘贴或上传；不承诺一键带图。
- 封面由 X 编辑器单独上传。标题填标题栏，源稿第一个 H1 不进正文剪贴板。
- 表格可用 `--tables-as-images`；没有 Chrome 时脚本会降级成分行列表，交付时说明结果。富文本列表和纯文本列表分开处理；纯文本 `--list-style plain|emoji|keep` 都可选。
- 提示词代码块可在 X 编辑器用原生 Code 功能恢复读者侧复制按钮；当前导出链路见 [x-html-format.md](references/x-html-format.md)。
- 打开 HTML 或生成预览逐张核对图文顺序、表格与复制结果。原始 PNG 与压缩内嵌图可能编码不同，核对其内容和映射，不能把所有文件的字节相同当通用要求。
- 文字修订回到源稿再导出；提供实际检查过的最终文件。缺少浏览器或平台权限时如实记录验证范围。

纯文本说明见 [x-format.md](references/x-format.md)，发布核对见 [publish-checklist.md](references/publish-checklist.md)。已有定稿只要转换时直接执行转换，检查不扩展为擅自改稿。

## 交付与状态

用户只要稿子就交 Markdown；要发布包再给 HTML、纯文本、预览、图源与封面。必要限定留正文，详细来源另列；短帖派生见 [x-delivery-contract.md](references/x-delivery-contract.md)，链接位置可按实际用途调整。

本技能交付并供用户在 Article 编辑器操作；发布状态以真实发布结果为准，生成发布包不算“已发布”。封面用 `topmind-cover`，短文用 `topmind-briefs` / `topmind-viral-posts`，公众号用 `topmind-wechat-post`，独立改稿用 `topmind-revise`。外部技能未安装不妨碍本包的写稿与转换。
