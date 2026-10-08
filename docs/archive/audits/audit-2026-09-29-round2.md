# tms-skills 第二轮审计报告（深水审计 + 整改）

日期：2026-09-29 · 基线 c8e3980（已 push）→ 本次 commit（本地，未 push/tag）
目标：按 Anthropic Agent Skills 最佳实践全方位对标，cover 风格库 + 示例图，发版 0.3.0 准备。

## 一、对标结论（4 技能）

| 维度 | top-ppt-html | topmind-wechat-post | topmind-x-article | topmind-cover |
|---|---|---|---|---|
| SKILL.md 精简（<500 行） | 142 行 ✅ | 217 行 ✅（摘要级重叠为有意 L0 骨架） | 71 行 ✅ | ✅（B 重构后） |
| description 第三人称+触发词 | ✅ 本轮重写（降误触发） | ✅ 本轮重写（"定稿"→"公众号定稿"） | ✅ | ✅（去口语化） |
| 渐进披露 | L0/L1/L2 + 零冗余门禁 ✅ | 本轮去重 2 处 ✅ | ✅ | ✅（公式去重） |
| 脚本幂等/干净报错/无重依赖 | ✅（全 stdlib） | ✅ | ✅（修 2 bug 后） | ✅（删 `--slug` 悬空参数） |
| 触发边界 | ✅ | ✅（补跨技能路由） | ✅ | ✅（补 thumbnail 触发词） |
| 输出可靠性 | 12 铁律可执行 ✅ | 阈值具体 ✅ | 10 条转换规则 ✅ | 安全区铁律 ✅ |

## 二、本轮改动汇总

**A1（top-ppt-html + wechat-post）：7 处**
- 两技能 description 改第三人称，加触发词限定（"做报告时说"、"公众号定稿"），降误触发
- wechat-post：修序号矛盾（排版层自动生成）、2 处与 references 去重、When NOT to use 补跨技能路由

**A2（x-article）：3 处**
- `md2x.py`：`---` 分隔线被丢弃 → 转空行（与 x-format.md 文档一致）
- `md2x.py`：`***粗斜体***` 剥离残留 `*`
- description 路由点名 `短推文（→ topmind-x）`

**B（topmind-cover，重点）**
- `references/cover-styles.md` 扩为 6 风格：震撼大字报 / 科技未来感 / 杂志编辑风 / 极简留白 / 国潮插画 / 赛博故障艺术（适用场景、配色 hex、字体、中英 prompt 配方、避坑）
- `assets/examples/` 新增 12 张示例图（6×1200×675 + 6×900×383，共 6.4MB，随 npm 包发布）
- SKILL.md 新增"步骤 0 选风格"三步工作流；删 `--slug` 悬空参数；标题中央垂直 60% 安全区铁律；补外部依赖声明
- 应用 A2 审计 P0×2/P1×3/P2×2

**C（文档）**
- 根 README 中英：cover 风格库 + 12 示例图亮点小节
- 三新技能 README 中英：与 SKILL.md 对齐（选风格步骤、安全区、跨技能路由、External dependencies）
- CHANGELOG 新增 `0.3.0` 条目；PUBLISHING 核查无口径冲突
- 根版本 0.2.0→0.3.0 及 9 处版本引用同步

## 三、cover 风格库与示例图说明

- 风格 id：`big-poster` / `tech-future` / `magazine` / `minimal` / `guochao` / `cyber-glitch`
- 生成：media 图像服务（B 分队时 503 过载，协调者重试后恢复，共 11 次调用含 5 次返工）
- 质量：6 张主图中文标题逐张验过，无乱码；5 张因标题超出安全区被中央裁剪切掉，全部返工（标题移入中央 60%）
- 体积：12 张 8.2MB → 公众号裁剪版 256 色量化 → 6.4MB（≤8MB 目标）；进 npm 包（npx 安装即得，与 top-ppt-html 4.1MB 示例资产惯例一致）
- 清单：`topmind-cover/assets/examples/README.md`（12 文件表 + 安全区说明 + 反例警示 + 复用声明）

## 四、门禁结果（全绿）

- `ci_privacy_scan.py`：PASS（195 文件，无隐私/弃用发现）
- `sync_npm_files.js --check`：in sync
- `ci_skill_gates.sh --with-pptx`：all skills green
- 4 技能 `negative_tests.py`：全过
- `run_skill_gates.js versions`：4 技能通过；`test_install_guards.js`：全过

## 五、遗留 / 暂缓项

1. **未改行为的事项**（记入，不动手）：x-article 的 setext 标题、`---` 开头 frontmatter 误吞、表格前导 `|`、`[a](b(c))` 嵌套 URL；top-ppt-html `fast` 触发词 eval 口径（改 eval 另议）；wechat-post 217 行是否压到 150 行；4 技能 description 中英混合口径是否统一
2. **上一轮暂缓延续**：Windows CI 矩阵未加；安装器 `--to` 吞 flag / EEXIST 堆栈（中等-6/7）
3. **示例图返工记录**：首版 5 张标题被裁，说明"安全区铁律"确有必要，已在风格库和示例清单中固化

## 六、发版建议

建议按 **0.3.0** 发版：新功能（风格库+示例图）+ 多项质量整改，符合 minor 语义。技能 version 保持不动（独立演进）。
发版步骤：`git push origin main` → CI 绿 → `git tag v0.3.0 && git push origin v0.3.0` → Release workflow 自动发布 npm。
