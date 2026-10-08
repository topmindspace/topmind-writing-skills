# tms-skills 第三轮审计整改报告（2026-09-29）

目标：cover 风格按爆款封面重沉淀 + 样张重制 + 4 技能真实跑测核实，发版 0.3.1 准备。
基线：`5b57472`（v0.3.0 已发布）→ 本轮 commit：`0ae73a9`（本地，未 push、未打 tag）。

## 一、cover 风格库重沉淀（子任务 A）

用户反馈上一轮 6 风格样张不够好，提供了 7 张爆款参考封面（Muse爆款干货 / Skill指南 /
typesafe Jev / Reddit教程 / AI视频实战 / 算法工程师祛魅 + 1 张缩略图条）。
另从用户 Mac 拉回 Manus 2.0 文章封面（`/tmp/manus-cover.png`）验证配方。

`topmind-cover/references/cover-styles.md` 重写为 **8 种风格**（6 新 + 2 保留），
旧 6 种（big-poster/tech-future/guochao/cyber-glitch 等）删除：

| 风格 id | 中文名 | 一句话 | 适用 |
|---|---|---|---|
| gan-huo | 爆款干货 | 萌物/IP + 巨型标题 + 彩色数字 + 底部胶囊标签条 | 干货清单/评测/盘点 |
| big-type | 巨字宣言 | 标题字占画面 35%~45%、分两行撞色 | 观点/深度/发布 |
| brand-launch | 品牌发布 | 品牌色渐变大标题 + 产品展示 + 卖点图标条 | 产品发布/版本更新 |
| tutorial-steps | 教程步骤 | 红笔刷横条标题 + 步骤卡片拼贴 + 圆形序号章 | 教程/上手指南 |
| ip-fun | IP 趣味 | 巨型彩色数字前置 + 趣味 IP + 署名 | 实战案例/数据战报 |
| news-flash | 资讯快报 | 两行大字（上黑下彩）+ 胶囊问句副标题 + 人物点缀 | 资讯/解读/快讯 |
| minimal | 极简留白 | 保留旧版精华（≥60% 留白） | 随笔/书评/轻阅读 |
| magazine | 杂志编辑 | 保留旧版精华（三分法/人物/标题上细红线） | 访谈/商业分析 |

每种含：适用场景、构图公式、配色 hex、标题写法规范（4~8 字短标题、数字/关键词彩色突出）、
中英 prompt 配方（`{TITLE}`/`{KEYWORDS}` 占位符）、避坑；"中央 60% 安全区"铁律保留。

### 从参考图提炼的 5 条规律

1. 标题字巨大化：占画面高度 22%~45%，数字/品牌词彩色放大（如"600万播放"的 600万）。
2. 左文右图通用分区：左侧纵向堆叠文案，右侧放萌物/IP/产品，配图不遮挡文字。
3. 三层文字结构：大标题 + 胶囊/笔刷副标题 + 底部标签条/卖点图标条。
4. 数字前置造冲击："600万播放""从0到1""26篇"，且数字必须真实。
5. 背景极简浅色为主，元素总数 ≤5，不繁杂。

Manus 封面验证：蓝色萌物（右）+ 巨型"Manus 2.0"（2.0 蓝色突出）+ 深蓝副标题 +
蓝色胶囊 + 小标签条，正好符合 gan-huo 配方。

## 二、样张重制（子任务 B）

`topmind-cover/assets/examples/`：**16 张 + 1 总览**，旧 12 张已移除（可恢复 trash，2026-10-29 过期）。

| 风格 | 主图标题（虚构演示文案） | 目检 |
|---|---|---|
| gan-huo | 实测精选干货 | ✓ |
| big-type | 从入门到精通 | ✓（返工 1 次） |
| brand-launch | 星火最佳实践 | ✓（返工 1 次） |
| tutorial-steps | 上手极简教程 | ✓（返工 1 次） |
| ip-fun | 100天·AI绘画实战复盘 | ✓（零返工） |
| news-flash | 带你祛魅/算法工程师！ | ✓（零返工） |
| minimal | 秋日随笔 | ✓（返工 2 次） |
| magazine | 年度商业盘点 | ✓（返工 1 次） |

- 8 张主图 1200×675 + 8 张公众号裁剪版 900×383（`crop-cover.py` 中央裁剪），
  公众号版逐张目检确认标题/标签条完整保留（裁剪保留带 21.6%~78.4%）。
- `overview.png`：2360×854，2 行×4 列，Noto Sans CJK SC 标注"中文名 + 英文 id"。
- **返工 7 次，全部是"底部元素超出安全区"同一类问题**（元素压到 80% 以下被中央裁剪切掉），
  已全部上移修正。
- 体积：单张 <1.5MB（最大 big-type.png 1128KB），overview.png 1317KB，合计约 7.6MB。
- `assets/examples/README.md` 重写：8 风格清单 + 安全区说明（含返工反例）+ 复用声明
  （"示例标题/数字为虚构演示"）。
- `node scripts/sync_npm_files.js --check` 通过：该脚本只同步技能目录级清单，PNG 增删不影响。

## 三、文档嵌入精简样张（子任务 C）

5 个文件：根 `README.md` / `README.en.md`、`topmind-cover/README.md` / `README.en.md`、
`topmind-cover/SKILL.md`。
- 各嵌入 `overview.png` 总览图一处，URL 为 GitHub 绝对地址
  `https://github.com/topmindspace/tms-skills/raw/main/topmind-cover/assets/examples/overview.png`
 （npm README 相对路径不显示，必须绝对 URL）。
- 配 8 风格一行式索引（风格名中英 + 一句话适用场景），不堆大图。
- 用法"6 选 1"→"8 选 1"；旧 6 风格 20+ 残留模式扫描**零残留**。

## 四、全技能真实跑测（子任务 D）

| 脚本 | 结果 |
|---|---|
| `md2x.py`（x-article） | ✓ 标题/加粗/链接/图片→[图N]/表格/分隔线等样例全对 |
| `md2wechat.py`（wechat-post） | ✓，**修 1 真 bug**（见下） |
| `crop-cover.py`（cover） | ✓ 12 个输出尺寸精确 |
| `bin/tms-skills.js install` | ✓ list/install 冒烟通过 |
| `ci_skill_gates.sh --with-pptx` | ✓ all skills green |
| 4× `negative_tests.py` | ✓ 全过 |
| 规范性（version/name 一致性） | ✓ |

**修复的 bug**：`topmind-wechat-post/scripts/md2wechat.py` —
本地图片文件缺失时，HTML 保留断链 `<img>`、终端提示"未内嵌"，
但"图片上传清单.md"和"图片 N 张"计数**完全漏掉这一项**（用户按清单补图会漏传）。
修复：缺失时登记 `{"src","local":None,"remote":False,"missing":True}`，
清单输出 `⚠ 本地文件缺失：` 行，计数自动包含。diff 9 行，未改渲染行为。

**未修、记入本报告的事项**：
1. frontmatter 字段集不统一（wechat-post 缺 author/license/homepage；top-ppt-html 另有 compatibility 无 triggers）——门禁全过，不算明显错误。
2. `md2x` 边界：文档以 `---` 开头但无 frontmatter 时分隔线被误删；`**加粗里有 *斜体***` 残留双空格（cosmetic）。
3. `md2wechat` 缺失图片的 HTML 保留断链 `<img>`——占位设计选择，清单已标注。
4. Windows CI 矩阵、安装器 2 个中等问题（`--to` 吞 flag / EEXIST 堆栈）——此前已暂缓。

## 五、发版准备 0.3.1

用户要求"版本号尽量从最小版本号 bump"→ **patch**：
根 `package.json` 0.3.0→**0.3.1**；9 处版本引用同步
（根 README 中英、top-ppt-html README 中英、PUBLISHING 当前线）；
CHANGELOG 新增 0.3.1 条目；4 技能 `version` 不动。

## 六、门禁结果（全绿）

- `ci_privacy_scan.py`：PASS（196 文件）
- `sync_npm_files.js --check`：in sync
- `ci_skill_gates.sh --with-pptx`：all skills green
- 4 技能 `negative_tests.py`：全过
- `run_skill_gates.js versions` + `test_install_guards.js`：全过

## 七、遗留项

1. 本轮 commit `0ae73a9` 未 push、未打 tag，待发版（push main → CI 绿 → `v0.3.1` tag → Release 自动发 npm）。
2. D 节未修的 4 项（见上）。
3. npm README 总览图依赖 main 分支已有 `overview.png`——push 后 URL 即生效。
