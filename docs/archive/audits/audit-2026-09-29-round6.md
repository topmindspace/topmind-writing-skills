# 第六轮审计整改报告（2026-09-29）

主题：top-ppt-html 全面审查 + 全仓横扫，备发 0.3.4。

## 一、top-ppt-html 全面审查

### 1.1 SKILL.md 深审（Worker A）— 修 3 处小问题，零行为改动

- `SKILL.md`：修 Header 工具栏表格 `H 生成指引` 行的 `（=?）` 编辑残留标记
  → 按 `references/components-atoms.md` 改为"双通道说明（页面预览 vs 智能体精导）"
- `README.md`：① `SKILL.md | L0 路由（≤13KB）` 过时（实际约 16KB）→ 修正；
  ② 新增"最小示例（复制即跑 · 约 3 分钟）"命令链（scaffold → 填 REPORT_MODEL → render → validate → 可选 PPTX）
- `README.en.md`：同步英文版 Minimal example，中英上手信息对齐

核查结论（未改动项）：
- 元数据四处一致：package.json 0.1.19 ＝ SKILL.md frontmatter 0.1.19 ＝ README 中英 0.1.19 ＝ 根 CHANGELOG
- 脚本参数逐一核对无过时：validate_report（--strict/--json/--layout-qa）、validate_pptx、
  quality_gate、extract_snippet、build_pptx.js、render_from_model、scaffold_report 全部与文档一致
- description 精准：触发词"做PPT/汇报材料/路演/deck/slides/研究报告/白皮书"全覆盖；
  fast 口径与正文一致；四条"不做"边界逐条对应（纯代码工程/非报告类网页/视频图片生成/改写 Word/PPT 源文件）
- CHANGELOG 0.1.18/0.1.19 与 git log 吻合；references 页数契约/9 风格/29 页型/36 图表全对齐
- `package_skill.py --check`、`audit_docs.py`、`check_triggers.py` 全过；最小示例每条命令真实跑通

### 1.2 渲染管线 + build_pptx.js 实跑（Worker B）— 修 8 个 bug

虚构测试稿走完 render_from_model → hydrate_charts → data URI 内联 → validate --strict：
**95 PASS / 0 WARN / 0 FAIL**。PPTX 11 slides 实跑：16:9、微软雅黑、中文原生文本、原生图表，
strict 0 error / 0 warning。

注入缺陷验证（全部被抓）：
- 超大 data URI 图片 → 抓到（并顺手修了计量 bug：原按标签字符串长度计量，现按**解码后字节数**）
- 布局溢出 / LAYOUT_FILL 过满 → 抓到，可定位页码
- 空 `alt=""` → 原漏检，现视同缺失告警
- ELEMENT_OVERLAP（真实 PPTX 注入重叠框 → 报元素名+重叠面积）、LAYOUT_FILL（删正文仅留标题 → 触发）门禁有效

修复清单：
- `build_pptx.js`（6 处）：KPI 竖分隔线越过注释带；KPI/donut/image 页 `sec.points` 被丢弃；
  image 页图片底边越过注释带；cards 要点无脑 shrink 被 TEXT_OVERFLOW 抓（改有限缩字号统一选档）；
  points 纯字符串/`{t,d}` 形态渲染为空或 `[object Object]`（统一回落逻辑）
- `hydrate_charts.py`：空 labels/values、非数字 values、长度不一致原抛 Traceback
  → 新增 `ChartDataError` 干净报错（带 section 定位），禁静默截断
- `validate_report.py`（2 处）：`alt=""` 视同缺失；图片体积按解码字节计量（级别保持 WARN，strict 已拦截）

回归：未知参数 exit=2 干净报错；坏输入无 Traceback；`test_feedback_gates.py` 全 PASS；
`negative_tests.py` exit=0；`smoke_pptx.sh` OK。

### 1.3 模板与 references 抽查（Worker C）— 修 13 处死引用

- 抽 3 套覆盖度最低的风格（品牌红/靛紫/光谱彩色）实跑渲染：**全部成功**，
  token 与 styles.md 宣称值逐字一致，donut 色板正确（代码级验证；本机无浏览器未做像素目检）
- 修 13 处死引用（6 文件）：SKILL.md:142 错乱拼接的脚本路径；
  references/design-system.md、icons.md、tech-design.md、scripts/build_examples.py 中
  `docs/archive/…` → `../docs/archive/…`（仓库根真实存在）；modes.md 样例表改指归档
- 修后 `npm run audit`（audit_styles + audit_docs + audit_skill + audit_css）全部通过
- `dist/` 未入库（.gitignore 忽略），属本地回归产物，无问题

## 二、全仓横扫（Worker D）

### 2.1 修 1 个真 bug：cover-styles.md 截断

第五轮重写 `topmind-cover/references/cover-styles.md` 时把截断的工具输出写进文件：
文件尾字面量 `...[truncated 3507 chars]`，ip-fun 尾部丢失、news-flash/minimal/magazine 三节整节丢失，
而 README（中英）宣称"8 风格"。已按审计文档+样张实物补齐三节，8 节完整、无截断标记。

### 2.2 根文档

- `docs/PUBLISHING.md` 补三处：① **HTTPS+PAT 推送方式**
  （`git -c "http.extraHeader=Authorization: Basic <base64(x-access-token:PAT)>" push
  https://github.com/topmindspace/tms-skills.git main`；GitHub git 接口不认 Bearer 只认 Basic；
  origin 为 SSH 地址时须显式给 HTTPS URL；PAT 一次性用完即弃）；
  ② tag↔package.json 交叉校验（已核对 release.yml 第 37–50 行）；③ NPM_TOKEN/E409 加固
  （已核对 workflow 第 79–124 行）。另修过时文字"当前线 0.2.x"→"0.3.x（latest 指向 0.3.1）"
- 三个新技能 README（中英）补版本号行（仓库规约：SKILL.md/package.json/README/CHANGELOG 同值）
- 根 README.en 示例图体积与实测对齐（~8.9MB）
- CHANGELOG：0.3.2/0.3.3 明确标"未发布"（`git tag` 确认 v0.3.2/v0.3.3 不存在，npm 无此版本）

### 2.3 元数据与触发边界

- 四技能 SKILL.md frontmatter ↔ package.json ↔ README ↔ CHANGELOG 版本全对齐
  （top-ppt-html 0.1.19，其余 0.1.0）
- description 触发边界：四技能互不重叠、无真空；"X 长文封面"良性重叠已写清委托关系
  （x-article → cover 平台选 x；wechat-post → cover）

### 2.4 隐私与安装器

- `ci_privacy_scan.py`：**PASS**（199 文件）
- `bin/tms-skills.js list` 四技能正常；四技能 install --to /tmp 全过；
  `test_install_guards.js` 全部通过；`run_skill_gates.js versions` 通过；
  `sync_npm_files.js --check` in sync

## 三、发版准备 0.3.4

- 根 `package.json` 0.3.3 → **0.3.4**（patch）；9 处版本引用同步
  （根 README 中英、top-ppt-html README 中英、PUBLISHING 当前线）；
  CHANGELOG 新增 0.3.4 条目，0.3.2/0.3.3 注明未发布、已并入 0.3.4
- 4 技能 `version` 不动（整仓同 tag + 技能独立演进）
- **本地 commit，未 push、未打 tag**

## 四、门禁结果（全绿）

| 门禁 | 结果 |
|---|---|
| ci_privacy_scan.py | PASS（199 文件） |
| sync_npm_files.js --check | in sync |
| ci_skill_gates.sh --with-pptx | all skills green |
| 4 技能 negative_tests | 全过（top-ppt-html 的 FAIL 行为其反向验证故意注入） |
| run_skill_gates.js versions | 通过 |
| test_install_guards.js | 全部通过 |
| npm run audit（top-ppt-html） | audit_styles/docs/skill/css 全过 |

## 五、遗留项（需 parent/用户定夺）

1. **未 push、未打 tag**：发版步骤 push main → CI → 打 `v0.3.4` tag → Release 自动发 npm。
   SSH 隧道仍被代理墙掐断，需走 HTTPS + PAT Basic 认证（上次 PAT 已用完即弃，需用户再给）。
2. top-ppt-html 需产品决策的行为候选：render_from_model 不同步 style/theme；
   超长中文图表标签不截断；图片超限 WARN 不升级 FAIL；代码块页型缺失（schema 无 code 页型）；
   KPI/donut/image points 空间不足时 slice 舍去（有 MODEL_ROUNDTRIP 兜底）。
3. Worker A 留的 3 个文档小项：README.en 安装节 pin @0.3.3（已随本轮 bump 到 @0.3.4，
   但中英 pin 策略仍不对称）；README.en 整体短于中文版（有意设计）；fast 篇幅定义位置。
4. SKILL.md 体积 13309/13312 字节，贴着体积门禁上限——再加字会触发。
5. 历史遗留：Windows/macOS CI 矩阵、安装器 2 个中等问题；wechat-post/x-article 前几轮的行为候选。
