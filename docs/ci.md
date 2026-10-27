# CI / Release 说明

## 工作流

| 工作流 | 触发 | 做什么 |
|--------|------|--------|
| **CI** (`.github/workflows/ci.yml`) | `push`/`pull_request`（main） | 隐私扫描 · files 同步 · 共享真源一致性 · 评测骨架 · 安装器冒烟 · 官方校验器 · 技能门禁 |
| **Release** (`.github/workflows/release.yml`) | `push` tag `v*` | 同上技能门禁 → 打包 zip → GitHub Release → npm publish → 修剪旧 Release（留 2） |

并发：CI 同 ref `cancel-in-progress`；Release 不取消（避免发一半被掐）。

## 技能门禁（单一事实源）

`scripts/ci_skill_gates.sh` 被 CI 与 Release **共用**：

```bash
bash scripts/ci_skill_gates.sh
```

先跑一次仓库级的去 AI 味规则回归 `python3 scripts/test_lint_rules.py`（「不应报」的正常写法被误报、该报的没报、H 提示卡住了 `--strict`，都算失败），再跑 `python3 scripts/test_creative_contracts.py`，验证默认保真、显式转换、风格提示与实际格式错误的区别；随后对每个发现的技能目录依次：

1. 有运行时依赖才装：有锁文件 `npm ci --omit=dev`，没有则 `npm install --omit=dev --no-package-lock`；目前各技能都没有依赖，这一步跳过，不生成锁文件
2. `package_skill.py --check` + `audit_{styles,docs,skill,css}.py`；仓库级 `test_skill_packaging.py` 验证重复打包、双语说明和产物排除，源目录禁用文件检查保持有效
3. `negative_tests.py`（cover 含 `test_crop_cover.py`：多平台尺寸、独立裁切、位置、等比、EXIF 与原图保护；CI / Release 显式安装 Pillow，确保执行图片测试）
4. （若存在）`test_feedback_gates.py`

### 本地复现

```bash
# 与 CI 同款全门禁
python3 -m pip install 'Pillow>=10,<13' 'numpy>=1.26,<3'
bash scripts/ci_skill_gates.sh

# 仓库级
npm run check && npm run audit && npm run privacy
```

## 共享真源与规范校验

- `node scripts/sync_shared.js --check`：`shared/manifest.json` 声明的共享脚本（`de_ai_lint.py`、`lint_x_post.py`、`count_words.py`、`revise_check.py`、`audit-provenance.py` 等）与共享文档（`social-writing-principles.md`、`information-design.md`、`core-voice.md`、`de-ai-rules.md` 等），各技能副本必须与 `shared/` 真源逐字节一致（`prepack` 也会跑）。
- `node scripts/check_evals.js`：`evals/evals.json` 每个技能 ≥3 条、含负例；用例 prompt 必须命中 expected_skill 的触发词；description 的 Do NOT 只能指向存在的技能。
- `agentskills validate <skill>`（`pip install skills-ref==0.1.1`）：frontmatter 顶层只允许规范字段，自定义字段在 `metadata` 下。

## npm publish（显式失败，防假绿）

Release 的 publish 步骤：

1. 无 `NPM_TOKEN` → **显式失败**（拒绝发无 npm 包的 Release）
2. 该版本已在 npm 上 → 跳过发布，视为成功（同一 tag 重跑不会失败）
3. `npm publish` 报 E409 / 版本冲突 → 再查一次 registry：版本已可见算成功；不可见则失败，提示先 bump 版本再打新 tag
4. 其它错误 → 失败

## 重跑

- PR / push：GitHub Actions → 对应 workflow → **Re-run failed jobs** / **Re-run all jobs**
- 发版：修好后推新 commit + 新 tag（npm 版本不可覆盖；同一 tag 重跑时，已发布的版本会被跳过）
- 本地：修完再跑 `bash scripts/ci_skill_gates.sh`，确认 exit 0 再推

## 硬约束（不为过 CI 而削弱）

- 各技能 `audit_*.py` 定义的质量门禁（如去 AI 味、数字来源、配图校验）
- `negative_tests.py` 的负向用例必须全绿
- `scripts/test_lint_rules.py` 的「不应报」用例不许删来过 CI：误报就改规则，不改用例

## 创作行为与质量评测

`evals/evals.json` 包含路由、用户偏好、参考阅读和创作选择场景。`check_evals.js` 只验证用例结构与路由词，不执行模型，不证明写作质量。真实任务比较方法见 [审查报告](./creative-skills-audit.md)。

## 创作知识与工具行为

共享 manifest 的目录项递归分发知识包。`test_knowledge.py` 验证中文检索、技能与状态过滤、摘要不泄露正文、读取截断、目录范围、候选新增和失败回滚；`test_cover_freedom.py` 验证审美提示不阻塞、作者语言保留、无效出字结构仍失败。Node 测试验证目录分发和宿主资源完整，ZIP 测试确认知识文件不漏包。CI / Release 安装 Pillow 与 NumPy，避免跳过图片与标题工具检查。

图册的横竖切换、手机布局和实际看图属于本地视觉检查，不以字符串或样例数量代替。评测新增知识使用、例外和创作选择场景；结构检查不声称执行了模型评测。

## 真实分发包完整性

CI / Release 都先生成 8 个技能 ZIP 和宿主包，再运行 `npm run check:release`。校验版本、文件清单、SHA-256、知识卡 / 双语文档 / 图册与源文件一致性、latest.json 和产物排除；`test_release_artifacts.py` 覆盖遗漏、篡改和缓存混入。npm 包检查同时确认必需资源，避免只查“没有垃圾”却漏掉正文件。
