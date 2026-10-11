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

对每个发现的技能目录依次：

1. 有运行时依赖才装：有锁文件 `npm ci --omit=dev`，没有则 `npm install --omit=dev --no-package-lock`；目前各技能都没有依赖，这一步跳过，不生成锁文件
2. `package_skill.py --check` + `audit_{styles,docs,skill,css}.py`
3. `negative_tests.py`
4. （若存在）`test_feedback_gates.py`

### 本地复现

```bash
# 与 CI 同款全门禁
bash scripts/ci_skill_gates.sh

# 仓库级
npm run check && npm run audit && npm run privacy
```

## 共享真源与规范校验

- `node scripts/sync_shared.js --check`：`shared/manifest.json` 声明的共享脚本与 `writing-principles.md`，各技能副本必须与 `shared/` 真源逐字节一致（`prepack` 也会跑）。
- `node scripts/check_evals.js`：`evals/evals.json` 每个技能 ≥3 条、含负例。
- `agentskills validate <skill>`（`pip install skills-ref==0.1.1`）：frontmatter 顶层只允许规范字段，自定义字段在 `metadata` 下。

## npm publish（显式失败，防假绿）

Release 的 publish 步骤：

1. 无 `NPM_TOKEN` → **显式失败**（拒绝发无 npm 包的 Release）
2. `npm publish` 返回 **E409 / 版本冲突** → **显式失败**（说明打 tag 前没 bump 版本；禁止复用 tag 号）
3. 其它错误 → 失败

## 重跑

- PR / push：GitHub Actions → 对应 workflow → **Re-run failed jobs** / **Re-run all jobs**
- 发版：修好后推新 commit + 新 tag（npm 版本不可覆盖；已发布号走上面的幂等路径）
- 本地：修完再跑 `bash scripts/ci_skill_gates.sh`，确认 exit 0 再推

## 红线（勿为过 CI 而削弱）

- 各技能 `audit_*.py` 定义的质量门禁（如去 AI 味、数字来源、配图校验）
- `negative_tests.py` 的负向用例必须全绿
