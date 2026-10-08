# 第七轮审计报告（2026-09-29）：发版前最后一轮

> 范围：最佳实践合规审计 + top-ppt-html 全量逻辑审查 + 全文档精简 + 性能可靠性。
> 本轮结束时工作树为**可发版状态**（备发 0.3.5）。四路 worker 并行，协调者集成。

## 一、最佳实践合规审计（Worker 1，只读审计）

基准：https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices 全文 + skill 规范。

| 技能 | 结论 | 主要问题 |
|------|------|----------|
| top-ppt-html | 部分合规 | SKILL.md 13309/13312 字节（**阻塞发版**，见下）；description 缺跨技能路由；7 个二级引用未被 SKILL.md 直接索引 |
| topmind-cover | 部分合规 | description "配图"与正文 When NOT to use 自相矛盾；触发词缺"题图/首图/banner"；SKILL.md 内嵌 GitHub 外链 `<img>`；原创声明长段占正文 |
| topmind-wechat-post | 部分合规 | 全 flag 命令串两处长篇复制；description 缺 cover/x-article 路由；触发词缺"微信编辑器/状态同步"；年份硬编码 |
| topmind-x-article | 合规 | 仅 2 轻微项（"写稿"边界未声明；触发词缺"转纯文本"） |

触发精准度：每技能 2 误触发 + 2 漏触发反例验证（详见 `/tmp/r7-w1-compliance.md`），漏触发主因是触发词缺口，误触发主因是 description 过宽——本轮 17 条修复清单全部落地（见三）。

**阻塞项**：`top-ppt-html/SKILL.md` 13309/13312 字节，仅剩 3 字节——`scripts/audit_skill.py` 设 13KB 预算，超限则 `npm run audit` 失败 → CI 红 → 发版阻塞。修复顺序强制：先瘦身（Worker 3：13309→11801，腾出 1508 字节）再加词（Worker 1 清单）。瘦身时保留"整读…= FAIL"文案（另一门禁要求）。

无需改动项：四技能目录名=frontmatter name=package.json name 一致；description 均 ≤1024 字符；SKILL.md 均 <500 行；references/scripts 无死链；非标准 frontmatter 字段（action_category/triggers/triggers_cn/updated）为安装器所依赖，已在根 README 声明为本仓库扩展字段。

## 二、top-ppt-html 全量逻辑审查（Worker 2，地毯式）

**修 31 个 bug**：严重 1｜高 3｜中 15｜低 12（本轮新发现 9 个）。

- **严重**：architecture 模式 PPTX 构建必崩——scaffold 发射的 `[标题, 注解]` 数组节点被 `build_pptx.js` 直接塞给 `pptxgenjs.addText()`，9/9 风格全灭（裸 TypeError）。已归一化修复，9/9 重建 strict 0/0。
- **高**：`render_from_model` 把数组节点打成字面量 `['节点一', '一行注']`；halftable 表格压住 Exhibit 徽标叠印（ELEMENT_OVERLAP）；HTML/PPTX 条目格式不一致。
- **中/低**：缺 pptxgenjs 裸堆栈、`ANNOTATION_BAND_OVERLAP` 对文本框系统误报（已豁免）、`render_from_model` 接受 NaN/Infinity、输出写失败 Traceback、gen_channel_a 失败留空目录等。

**功能矩阵**（3 模式 × 9 风格 × 双交付 = 54 格）：生成链路 54/54 全通；PPTX strict：presentation 9/9、architecture 9/9 全绿（修复前 9/9 构建失败），research 9/9 各 1E/1W（校验器保守安全网，已知决策项）；HTML strict 黄金成品 3/3 全绿。

**可靠性矩阵**（约 60 测项，8 CLI × 空文件/非法 JSON/非 UTF-8/超大文件/缺依赖/只读路径等）：零 Traceback、零 Node 堆栈，失败项全部非零退出+干净报错，无半截产物。

**遗留 10 项**（需决策）：`chart_label_presence` 死代码（需模型上下文重构，未假修）、scaffold 内容策略、门禁设计取舍、A 通道（assets/pptx-export.js 手写 OOXML）同族数组节点风险未验证（`cross_verify.py --full-ab` 可回归）。

## 三、文档精简（Worker 3 + 协调者集成 Worker 1 清单）

**33 个文件：-389 行 / -30707 字节**（精简前后对照见 `/tmp/r7-w3-docs.md`）。

| 文件 | 前（行/字节） | 后（行/字节） | 变化 |
|------|--------------|--------------|------|
| top-ppt-html/SKILL.md | 142 / 13309 | 130 / 12075* | -12 / -1234 |
| topmind-cover/SKILL.md | 105 / 5326 | 93 / 4344 | -12 / -982 |
| topmind-wechat-post/SKILL.md | 219 / 9956 | 212 / 9545 | -7 / -411 |
| topmind-x-article/SKILL.md | 74 / 2855 | 73 / 2969 | -1 / +114 |
| README.md / README.en.md | 188 / 11082 | 116 / 5600+ | -72 / -5482 |

\* 11801（Worker 3 瘦身）+ Worker 1 清单加词（triggers 列表、跨技能路由）= 12075，余量 1237 字节，安全。

Worker 1 的 17 条清单落地情况：G1（ppt frontmatter 补 triggers/action_category）✓、G3a（删正文写死版本号）✓、G3b（年份硬编码→`<当年>`）✓、G3c（W3 已改"发布实战规范"）✓、P1（description 补 cover 路由）✓、P2（瘦身）✓、P3（L2 索引已在"整读=FAIL"行内联）✓、C1（description"配图"→"题图"）✓、C2（触发词补题图/首图/banner）✓、C3（删 GitHub 外链 `<img>`，改本地路径文字）✓、C4（原创声明移入 cover-styles.md 顶部，SKILL.md 只留一句）✓、W1（W3 已压缩，无重复块）✓、W2（description 补 cover/x-article 路由）✓、W3（触发词补微信编辑器/粘贴到公众号/状态同步）✓、W4（三关已是硬阈值条目，无需再动）✓、X1（When NOT to use 补写稿边界）✓、X2（触发词补转纯文本/X纯文本/发article）✓、G2（命名不一致记为已知债务，不改）。

另：修复 docs/ci.md 与 PUBLISHING.md 的 npm publish 策略矛盾（按"显式失败防假绿"对齐）；PUBLISHING.md 保留 HTTPS+PAT 推送精确命令与 Bearer/Basic 坑位（精简版 3 行）。

## 四、性能与可靠性（Worker 4：三技能 + 安装器）

**性能实测**（中等规模真实输入）：md2x 300KB 0.33s；md2wechat 218KB+80图 0.42s（embed 0.47s）；crop-cover 4000×2250 1.79s；安装器 <0.5s。

**修 5 处 low-hanging fruit**（输出逐字节一致，无行为改动）：audit_inline 8 次全正文扫描→单遍预编译（原占大正文耗时 ~47%）；行内模式预编译到模块级；highlight 语言正则缓存；link_repl 脚注 O(n²)→O(n)。**实测提升**：md2wechat 11MB 13.8s→10.0s（-27%）；md2x 49MB 62.5s→42.2s（-32%）。

**可靠性**：修 2 真 bug——非法 UTF-8 输入抛 UnicodeDecodeError Traceback→干净报错；磁盘满时半截 HTML→原子写（tmp+os.replace）。矩阵其余项（空文件/超大文件/特殊字符/图片缺失/缺 Pillow/非法 skill id/装进源目录树）全部干净。

## 五、发版准备 0.3.5

- 根 `package.json` 0.3.4→**0.3.5**（patch）；CHANGELOG 新增 0.3.5 条目，注明 0.3.2/0.3.3/0.3.4 未发布已并入；9 处版本引用同步；4 技能 version 不动。
- **门禁全绿**：`ci_privacy_scan.py` PASS（200 文件）· `sync_npm_files.js --check` in sync · `ci_skill_gates.sh --with-pptx` all green · 4 技能 `negative_tests.py` 全过 · `run_skill_gates.js versions` PASS · `test_install_guards.js` 全过 · `npm run audit`（top-ppt-html，含 13KB 预算）全过。

## 六、遗留项

1. **未 push、未打 tag**：发版步骤 push main → CI → 打 `v0.3.5` tag → Release 自动发 npm。SSH 隧道仍被代理墙掐断，需 HTTPS + PAT Basic 认证（PAT 需用户再给）。
2. top-ppt-html 行为候选（需产品决策）：render_from_model 不同步 style/theme、超长中文图表标签不截断、图片超限 WARN 不升级 FAIL、代码块页型缺失、chart_label_presence 死代码、A 通道同族风险。
3. wechat-post/x-article 前几轮行为候选未动（缺图进合规自检、border-radius WARN 去噪、无前导 `|` 表格等）。
4. 历史遗留：Windows/macOS CI 矩阵、安装器 2 个中等问题。
5. `top-ppt-html` 与 `topmind-*` 命名不一致记为已知债务（改名破坏用户侧已安装路径）。
