---
name: topmind-cover
description: "设计高辨识度的文章、图文与视频封面、头图和缩略图，适配小红书、抖音、公众号、X Article 与短帖；追求清晰信息密度与真实层次，概念功能图诚实标注“功能示意，不是实拍”。密集信息长图用 topmind-poster。"
license: MIT
metadata:
  version: "0.5.2"
  action_category: "write"
  triggers: "封面, 封面图, 小红书封面, 抖音封面, 图文封面, 视频封面, X 短文封面, 短帖封面, 头图, 题图, 首图, 封面配图, 缩略图, banner, cover, thumbnail, 公众号封面, 公众号题图, 公众号头图, X 封面, X 首图, X 长文头图, 文章封面, 封面风格"
  author: "TopMindSpace"
  homepage: "https://github.com/topmindspace/topmind-writing-skills#readme"
  updated: "2026-11-15"
---

# topmind-cover · 高辨识度文章与多平台封面设计

让封面在手机信息流缩略图（约 300px 宽）下 **0.5 秒抓住眼球、一眼看清核心价值**，同时适配各平台真实裁切比例。默认中文；用户已有品牌、参考和风格要求优先。

## 一、核心设计心法：视觉吸引力、适度密度与诚实标注

1. **拒绝「假极简」与「廉价霓虹」，立住第一眼视觉重心**：
   - 「简约清晰」不是大片苍白背景配三个空洞大字，更不是满屏蓝紫发光粒子。
   - 用 **强字重结论 + 关键数字反差（Swiss Editorial）**、**Bento 模块化信息卡**、**真实原图荧光笔高亮拼贴**、**微距工业材质** 或 **手绘白板拆解** 建立视觉张力。
2. **诚实标注性质（防止视觉误导）**：
   - **概念封面与生成图**：凡涉及软件界面、产品功能表现的生成/概念封面，在边角或图注标明 **`功能示意，不是实拍`**，绝不冒充真实截图。
   - **原文证据封面**：使用论文、代码或官方文档原图做拼贴/裁切时，高亮关键行并保留真实上下文，**绝不自己排版伪造假论文页或假官方截图**。
   - **硬核技术与学术主题**：采用干净、克制的几何、图表或编辑排版风格，**不强贴卡通吉祥物或卖萌 logo**。

需要检索视觉方向或沉淀新经验时，见 [knowledge-library.md](references/knowledge-library.md)（含 `visual-density-and-evidence`、`cover-typography`、`cover-editorial` 等卡片）与 [creative-practice.md](references/creative-practice.md)。

## 二、五大视觉流派与双路径出图

用户给了参考就先实际看图；没给时可看 `assets/examples/overview.png` 或 [creative-atlas.html](assets/examples/creative-atlas.html)。[cover-styles.md](references/cover-styles.md) 的 5 大趋势与 22 种风格是灵感工具箱，而非呆板模板：

| 视觉流派 | 核心抓手 | 典型适用题材 |
|---|---|---|
| **字体与数字反差** (`big-type` / `news-flash` / `gan-huo`) | 超粗字重标题 + 巨大核心指标（如 `$0.25`、`10×`）或 Bento 信息卡 | 深度观点、测评榜单、工具合集、快讯 |
| **原图证据与拼贴** (`paper-collage` / `bg-blur` / `academic-print`) | 真实论文/代码/硬件原图裁切 + 荧光笔高亮关键行 | 论文精读、源码扒料、产品实测 |
| **微距材质与现代科技** (`dark-saas` / `hard-core-type` / `brand-launch`) | 阳极氧化铝、磨砂亚克力、纸雕压印等真实物理光影 | 开发者工具、本地部署、架构发布 |
| **场景叙事与空间隐喻** (`diorama-book` / `cinematic-flow` / `anime-desk`) | 等轴测系统沙盘、电影感追光空镜或生活光影细节 | 全局架构拆解、行业幕后、创作者故事 |
| **手绘拆解与反差幽默** (`sketch-cartoon` / `ip-fun` / `chao-wan-3d`) | 马克笔白板批注箭头，或小角色面对巨型物体的尺度反差 | 机制讲解、踩坑吐槽、入门科普 |

**释放 AI 原生表现力的两条出图路径**（详见 [cover-prompts.md](references/cover-prompts.md)）：
- **路径 A（字图一体直出）**：使用原生强文字模型（如 GPT-4o / GPT-Image、Gemini Imagen、Ideogram），用精炼导演级提示词直接给出「主体张力 + 材质色调 + 准确引号标题与字重位置」，不堆砌元指令废话。
- **路径 B（留白底图 + 脚本/HTML 精确叠字）**：让生图模型专注画好主体与干净负空间（`no text`），再用 `scripts/title-engine.py`、`scripts/overlay-title.py` 或 HTML 零误差排字。

构图动线看 [cover-patterns.md](references/cover-patterns.md)，跨媒介配色配方看 [cover-combos.md](references/cover-combos.md)，场景与字效看 [scene-builder.md](references/scene-builder.md) / [typography-system.md](references/typography-system.md)。

## 三、全平台尺寸匹配与独立裁切

先确定发布平台与形态，完整规格与安全区见 [platform-cover-specs.md](references/platform-cover-specs.md) 与 [image-sourcing.md](references/image-sourcing.md)：

| 目标平台与用途 | 推荐像素尺寸与比例 | 裁切脚本预设 (`--preset`) |
|---|---|---|
| **X Article 长文头图 + 公众号宽图** | `1500×600` (5:2) + `900×383` (2.35:1) | `article`（默认） |
| **公众号宽封面 + 转发/列表方图** | `900×383` (2.35:1) + `900×900` (1:1) | `wechat`（从原图分别独立裁切） |
| **X 普通短帖单图** | `1200×675` (16:9) | `x-post` |
| **小红书笔记 / 公众号小绿书 / 抖音图文** | `1080×1440` (3:4) | `xiaohongshu` / `douyin` |
| **横版视频双封面（16:9 母图含中央 4:3）** | `1920×1080` (16:9) + `1080×810` (4:3) | `landscape-pair` |
| **竖版视频双封面（9:16 母图含中央 3:4）** | `1080×1920` (9:16) + `1080×1440` (3:4) | `vertical-pair` |

```bash
python3 scripts/crop-cover.py <横版主图> --out-dir <交付目录>
python3 scripts/crop-cover.py <原图> --preset wechat --anchor center --out-dir <交付目录>
python3 scripts/crop-cover.py <主图> --preset x-post --out-dir <交付目录>
python3 scripts/crop-cover.py <竖版主图> --preset xiaohongshu --out-dir <交付目录>
python3 scripts/crop-cover.py <16比9母图> --preset landscape-pair --out-dir <交付目录>
python3 scripts/crop-cover.py <9比16母图> --preset vertical-pair --out-dir <交付目录>
```

## 四、核对与交付

出图后实际打开检查每个文字、数字、300px 缩略图可读性、各尺寸裁切完整性，以及概念功能图是否已标注 `功能示意，不是实拍`。密集数据长图交 `topmind-poster`。本技能只交付图像文件，不执行对外发布。
