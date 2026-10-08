# 封面风格示例图

42 张示例（随 git 仓库与 GitHub Release zip 分发；npm 包为瘦身只带 `overview.png`）：19 种风格 × 2 种尺寸 = 38 张 + 3 张 alt 样张
+ 1 张 alt 微信尺寸版（`white-clean-alt-wechat.png`），
另附 `overview.png`（19 风格总览缩略图 + 风格名标注，选风格时先看它）。

- `<style>.png`（1500×600，X 长文封面 / 公众号共用主尺寸，5:2）
- `<style>-wechat.png`（900×383，公众号封面大图，中央裁剪版）
- `<style>-alt.png`（同风格第二张演示样张；白色清新 / 背景虚化 / 纸感拼贴
  三种风格各有 2 张：主样张与 alt 样张用了不同的优选组合）
- `<style>-alt-wechat.png`（900×383，alt 样张的公众号尺寸版；目前只有 white-clean 有，即
  `white-clean-alt-wechat.png`，`crop-cover.py` 流程产出双尺寸，新增 alt 样张时一并产出）
- `overview.png`（19 风格总览缩略图 + 风格名标注，选风格时先看它）

19 种风格（白色清新 `white-clean` / 背景虚化 `bg-blur` / 纸感拼贴 `paper-collage` /
资讯快报 `news-flash` / 巨字宣言 `big-type` / 教程步骤 `tutorial-steps` /
极简留白 `minimal` / 杂志编辑 `magazine` / 3D萌系潮玩 `chao-wan-3d` /
日系动漫 `anime-desk` / 微缩立体书 `diorama-book` / 学院版画 `academic-print` /
样张矩阵 `gallery-grid` / 暗色SaaS `dark-saas` / 电影科技流 `cinematic-flow` /
硬核立体字 `hard-core-type` / 爆款干货 `gan-huo` / 品牌发布 `brand-launch` /
IP 趣味 `ip-fun`，浅色优先排序）：适用场景索引与配方见 `../references/cover-styles.md`。

## 原创与虚构声明（重要）

本目录 42 张示例图均为**原创设计**（只演示抽象设计原则，不临摹任何第三方封面的
版式与配色；复用本库设计时亦不得与第三方封面构成实质相似——只学原则，不学版式）。
图中标题文案、数字、品牌名、署名均为**虚构演示内容**（如"破晓 6.0"、
"@老周带单"）——直接复用前请换成自己的真实标题；凡封面上的数字必须在正文中有
出处，严禁编造数据。

## 复用声明

**示例图可直接拿去用/改，作封面底图或风格参考。**拿去用时按 `scripts/crop-cover.py`
的流程重新裁剪双尺寸并按包规约命名落盘；改图时保留原风格的配色与版式语言，
只换主体与标题字，以维持系列感。
