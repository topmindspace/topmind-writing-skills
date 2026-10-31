# 现有文章渲染器能力矩阵

日期：2026-10-28。用途：为创作工作台的 F0/F2 选择同一变体的预览与导出提供依据。下表只记录当前源码可确认的能力，不代表目标平台最终显示效果。

| 维度 | JavaScript `runtime/article-renderer.mjs` | Python `shared/scripts/md2wechat.py` |
| --- | --- | --- |
| 入口 | `renderArticle`、`prepareArticle`；机器结果 `renderArticleResult`、`prepareArticleResult`；原始字节入口 `prepareArticleResultFromSource`；本地文本辅助入口 `articleLocalTextDocument` | CLI `--input`，以文件为输入，可指定 `--out-dir`、`--slug` |
| 目标 | `wechat` 与 `x` 两种文章本地渲染 | 公众号 HTML |
| 主题 | `WRITING_THEMES` 中的内置主题 | `--theme` 读取主题 JSON，`--list-themes` 列出可用项 |
| 图片 | 由宿主 `readImage` 提供本地图片数据；字节入口对实际内嵌的 data URI 解码并记录字节摘要，供 Kernel 与快照正文图片核对；远程图只保留引用并提示待核对 | 解析本地图片并复制到输出目录；可选 `--embed-images` 内嵌为 data URI |
| 代码与图表 | 代码块输出行内样式；Mermaid 源码给诊断，需另行渲染 | 代码内联高亮；可选 `--render-mermaid` 生成图表资产 |
| 外链与表格 | 公众号外链转脚注；X 表格提示粘贴后检查 | `--link-mode` 选择外链模式；含表格转换和行内样式审计 |
| 附加版式 | 通用机器结果输出预览 HTML、剪贴板正文 HTML、原稿 Markdown、图片清单；字节入口另输出从受控 HTML 提取的 `local-clipboard-text`。不自动写文件。旧 `renderArticle.text` 仍为去掉 frontmatter 的原稿 | 可选目录、签名、自动编号与中英文间距；输出 HTML 与图片/图表清单，可选 `--preview` 截图 |
| 机器结果 | 版本化结果、产物 SHA-256、诊断和输入指纹；字节入口附所选稿原始字节摘要、路径及可选 Kernel 快照指纹，旧返回形状保留 | 目前主要是 CLI 文本和输出文件；尚无相同结果外壳 |
| 运行环境 | 可在宿主 JavaScript 运行时调用，读图由宿主提供 | 需要 Python；预览截图与 Mermaid 取决于本机可用工具 |

**实施决定：**一篇平台变体选定一个 renderer provider 与版本后，预览、复制、导出都使用该 provider 同一次输入快照的产物。宿主以选中稿原始 UTF-8 字节调用 `prepareArticleResultFromSource`，再以 Kernel `compareCreationArticleResult` 核对稿件路径/字节摘要、提供者、平台、主题与标题参数摘要、正文内嵌图片实际字节与快照资源、五份产物哈希；快照 `parameters` 应为 `{theme, title}`，未传标题用空串。源稿或资源变化须重算快照。不支持的 HTML/Obsidian 图片写法、非内嵌读图结果会保持不匹配。`articleLocalTextDocument` 从本地剪贴板 HTML 产物得到可送长度规则预检的文本：先无快照渲染并取得文本，再建立包含此文本摘要的快照，最后带快照指纹重渲染、校验长度并用 Kernel `compareCreationLocalLengthChain` 核对。此比较不证明封面和图片进入目标编辑器，也不证明粘贴后的真实文字。`source-markdown` 只用于保留原稿和人工交接，不能直接用作长度规则要求的 `platform_text`。首期以 JavaScript renderer 打通宿主内的本地预览/复制；已有 Python 公众号高保真导出继续保留。要把 Python 输出接入统一产物链，先做文件产物、依赖与诊断的适配和对照测试，再决定是否收敛两个实现。远程图片和目标编辑器的粘贴表现始终需要单独检查。
