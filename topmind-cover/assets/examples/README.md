# 封面风格示例图

55 张示例（随 git 仓库与 GitHub Release zip 分发；npm 包为瘦身只带 `overview.png`）：22 种风格 × 2 种尺寸 = 44 张
+ 11 张变体样张（白色清新 alt / b / c / d 及其微信尺寸版、`white-clean-showcase.png`、背景虚化 alt、纸感拼贴 alt），
另附 `overview.png`（22 风格总览缩略图 + 风格名标注，选风格时先看它）。

- `<style>.png`（1500×600，X 长文封面 / 公众号共用主尺寸，5:2）
- `<style>-wechat.png`（900×383，公众号封面大图，中央裁剪版）
- `<style>-alt.png`（同风格第二张演示样张；白色清新 / 背景虚化 / 纸感拼贴
  三种风格各有 2 张：主样张与 alt 样张用了不同的优选组合）
- `<style>-alt-wechat.png`（900×383，alt 样张的公众号尺寸版；目前只有 white-clean 有，即
  `white-clean-alt-wechat.png`，`crop-cover.py` 流程产出双尺寸，新增 alt 样张时一并产出）
- `overview.png`（22 风格总览缩略图 + 风格名标注，选风格时先看它）

22 种风格（白色清新 `white-clean` / 背景虚化 `bg-blur` / 纸感拼贴 `paper-collage` /
资讯快报 `news-flash` / 巨字宣言 `big-type` / 教程步骤 `tutorial-steps` /
极简留白 `minimal` / 杂志编辑 `magazine` / 3D萌系潮玩 `chao-wan-3d` /
日系动漫 `anime-desk` / 微缩立体书 `diorama-book` / 学院版画 `academic-print` /
样张矩阵 `gallery-grid` / 暗色SaaS `dark-saas` / 电影科技流 `cinematic-flow` /
硬核立体字 `hard-core-type` / 爆款干货 `gan-huo` / 品牌发布 `brand-launch` /
IP 趣味 `ip-fun` / 橙色暖阳 `orange-warm` / 卡通素描 `sketch-cartoon` / 赛博霓虹 `cyber-neon`，浅色优先排序）：适用场景索引与配方见 `../references/cover-styles.md`。

## 生成方式（v0.8.38 起）

全部示例改为**整张生成**：按 `../../references/cover-combos.md` 的命名组合（范式 × 风格 × 标题字 × 场景层 × 配色）写一段英文 prompt，标题原文写死，让字和场景在同一光照与透视里一起画出；出图后逐字核对，再按 5:2 裁出主图（1500×600）、按中部水平带裁出公众号版（900×383），并做轻度锐化与 PNG 调色板压缩。各图使用的组合标在 `cover-styles.md` 每个风格的「示例图」一行。组合是我们自己总结的配方，只参考公开封面合集里的抽象规律，仓库不收录任何第三方原图或原文。

## 原创与虚构声明（重要）

本目录 55 张示例图均为**原创设计**（只演示抽象设计原则，不临摹任何第三方封面的
版式与配色；复用本库设计时亦不得与第三方封面构成实质相似——只学原则，不学版式）。
图中标题文案、数字、品牌名、署名均为**虚构演示内容**（如"破晓 6.0"、
"@老周带单"）——直接复用前请换成自己的真实标题；凡封面上的数字必须在正文中有
出处，严禁编造数据。

## 复用声明

**示例图可直接拿去用/改，作封面底图或风格参考。**拿去用时按 `scripts/crop-cover.py`
的流程重新裁剪双尺寸并按包规约命名落盘；改图时保留原风格的配色与版式语言，
只换主体与标题字，以维持系列感。

## X 短文封面示例（16:9，2026-10-14 新增）

X 短文 / 短帖默认配一张 16:9 封面（1200×675）。本次新增 6 个场景的示例提示词与虚构填充文案，
见 `../../references/cover-prompts.md` 第 2 章（2.1 资讯快讯 / 2.2 数据榜单 / 2.3 产品发布 /
2.4 教程上手 / 2.5 观点评论 / 2.6 运营段子，填充示例见 2.7）。

对应样张按 `x-<场景>.png` 命名（如 `x-news.png`、`x-data.png`），出图后用
`python3 scripts/crop-cover.py <主图> --preset x-post --out-dir <目录>` 统一为 1200×675 再放入本目录，
并同步更新本说明的样张数量。当前仓库尚未放入这 6 张样张，选风格时先参考同风格的 5:2 样张。
