# 发布与贡献规范

本仓库发布**智能体技能（agent skills）**，须可安全开源。

**双通道分发**（同一套技能）：

| 通道 | 命令 | 特点 |
|------|------|------|
| **npm** | `npx @topmindspace/topmind-writing-skills install <skill-id>` | 钉版本、日常推荐 |
| **GitHub** | `npx github:topmindspace/topmind-writing-skills install <skill-id>` | 跟 HEAD、可 clone |

- 包：<https://www.npmjs.com/package/@topmindspace/topmind-writing-skills>
- 仓库：<https://github.com/topmindspace/topmind-writing-skills>

当前线：安装器 **0.8.26** · 技能 topmind-cover **0.4.3** · topmind-wechat-post **0.3.2** · topmind-x-article **0.4.9** · topmind-briefs **0.2.9** · topmind-viral-posts **0.3.3** · topmind-poster **0.1.2**（整仓同 tag 发版；见 CHANGELOG）。
公众号技能的唯一真源是本仓 `topmind-wechat-post`；topmind-skills 4.15.2 起删除了旧的 `topmind-wechat`。
演示技能已独立为 `topmind-presentation`（仓库 `topmind-presentation`），不在本仓发布线内。


## npm 2.x 弃用说明（仓库重置）

npm 上的旧包 `@topmindspace/tms-skills` **2.0.0–2.1.1 已弃用**（仓库重置前的过时线）；**不要安装 `^2`**。本仓已改名为 `@topmindspace/topmind-writing-skills`，旧包不再更新。

若需重写弃用文案，维护者可在已 `npm login` 的机器上执行 `bash scripts/deprecate-npm-2x.sh`（one-shot `@2.x` + verify）。


## 安装口径（文档与 CLI 一致）

| 优先级 | 命令 | 何时用 |
|--------|------|--------|
| **默认** | `npx @topmindspace/topmind-writing-skills install <skill-id>` | 日常 |
| 跟最新源 | `npx github:topmindspace/topmind-writing-skills install <skill-id>` | 要 HEAD |
| 备选 | `git clone` + `node topmind-writing-skills/bin/topmind-writing-skills.js install <skill-id>` | 离线 |
| 手工 | 解压 Release 的 `<skill-id>.zip` | 无 Node |

不要引导 `npm install <skill-id>`（技能 id 不是独立 npm 包）。

## 版本策略（务必遵守）

**整仓同 tag**：`git tag vX.Y.Z` 的 `X.Y.Z` = 根 `package.json` 的 `version`（即安装器 version，如当前 v0.7.4）；tag 号不代表任何技能版本。**各技能 `version` 独立演进**（如 topmind-x-article 0.4.0、topmind-cover 0.3.0），不与 tag 号绑定。

| 包 | 事实源 | 规则 |
|----|--------|------|
| 安装器（= tag 号） | 根 `package.json` `version` | semver；随每次发版 bump，打 tag 即定值 |
| 技能 | 各 `<skill-id>/package.json` 的 `version`，与 `SKILL.md` frontmatter 的 `metadata.version` 同值 | 独立 semver；只随技能自身实质变更 bump |

- **默认只升 patch**（从最小位升）；minor 只在新增技能等明显扩展时用。
- **建议**：版本号只在准备发版的那次提交里升，日常改动先写 CHANGELOG。0.8.17–0.8.20 曾升了号却没打 tag，npm 从 0.8.16 直接跳到 0.8.21；升了号就尽快发版，或在 CHANGELOG 注明未发布。
- **major 仅用于破坏性变更**：技能 id、CLI 名、注入标记、安装路径、不兼容模型字段。
- **禁止**无实质变更时跳大版本；禁止用版本号表达心情。
- npm 版本发布后不可覆盖；有变更就要新号。

## GitHub ≠ npm

| 动作 | GitHub | npm |
|------|:------:|:---:|
| `git push` | 更新 | **不变** |
| `git tag vX.Y.Z && git push --tags` | Release + zip | **自动 publish** |

**Release 保留策略：最多 2 个最近版本**（CI 只通过 API 删除更旧 **Release**；**git tags 保留**，便于历史追溯与 npm 对照）。npm 历史版本可钉。

CI/Release 细节见 [`docs/ci.md`](./ci.md)。

## 发布流程

1. 更新 `CHANGELOG.md`。
2. 按上表 bump 对应包的版本（各包内部多处同值：SKILL.md frontmatter / package.json / README / CHANGELOG）。
3. 门禁：
   ```bash
   npm run check && npm run audit && npm run privacy
   npm run check:shared && npm run check:evals && npm run validate:spec   # 共享真源一致 / 评测骨架 / 官方校验器
   ```
   改了 `shared/` 下的共享脚本或 `writing-principles.md` 时先 `npm run sync:shared`，不要直接改技能目录里的副本。
4. 新技能：`npm run sync:files`（把发现的技能目录写入 `package.json` `files`）。
5. 提交并打 tag：
   ```bash
   git tag vX.Y.Z
   git push origin main --tags
   ```

   > **HTTPS 推送**（SSH 不可用时）：用一次性令牌做 Basic 认证：
   > `git -c "http.extraHeader=Authorization: Basic <base64(x-access-token:TOKEN)>" push https://github.com/topmindspace/topmind-writing-skills.git main`
   > 注意：GitHub git 接口只接受 Basic，不接受 `Bearer`；origin 是 SSH 地址时要显式给 HTTPS URL；令牌一次性使用，不入库。

   Release workflow（`.github/workflows/release.yml`）按序执行：
   - **tag ↔ `package.json` 交叉校验**：`vX.Y.Z` 必须等于根 `package.json` 的 `version`，不一致直接失败
     （tag 号是安装器版本 ≠ 任何技能版本，见上文版本策略）。
   - 门禁 → 技能 zip → GitHub Release。
   - `npm publish`：先查 registry，版本已存在则跳过；**`NPM_TOKEN` 缺失 → 显式失败**（拒绝发无 npm 包的 Release）；
     publish 命中 **E409 / 版本冲突 → 显式失败**（说明打 tag 前没 bump 版本；禁止复用 tag 号）。
   - prune Releases（留最近 2 个；git tags 保留不删）。
6. 验证：`npm view @topmindspace/topmind-writing-skills version`

### 手工 publish

```bash
npm publish --access public --registry https://registry.npmjs.org/
```

Secret **`NPM_TOKEN`**（granular，scope `@topmindspace` 写权限）配置在 GitHub Actions；缺失则 Release 显式失败（静默跳过会产生"绿但没发包"的 Release，已改为显式失败）。

## 命名

| 面 | 规则 | 示例 |
|----|------|------|
| 技能 id / 目录 / frontmatter `name` | kebab-case，三处一致 | `topmind-briefs` |
| npm | `@topmindspace/*` | `@topmindspace/topmind-writing-skills` |
| CLI | 与仓库名一致 | `topmind-writing-skills` |

新代码禁止历史遗留标识（扫描器拦截）；文档不写更名流水账。

## 隐私检查清单

- [ ] 无绝对本地路径 / 用户名 / 主机名 / 凭据
- [ ] 扫描器不硬编码真实机器信息（本地词表 `scripts/.privacy-deny.local`，不入库）
- [ ] 无 IDE / 智能体本机状态、`node_modules`、`dist`、`scripts/_*`
- [ ] `SKILL.md` description ≤ 1024，含「做什么 + 何时用 + 何时不用」
- [ ] 根 `package.json` 的 `files` 覆盖全部技能目录

```bash
npm run privacy
```

## 打包矩阵

| 类别 | 技能 zip | npm 包 | git |
|------|:--------:|:------:|:---:|
| `SKILL.md` / `README.md` / `package.json` | ✅ | ✅ | ✅ |
| `assets/` `references/` `scripts/` `evals/` | ✅ | ✅ | ✅ |
| `bin/` | ❌ | ✅ | ✅ |
| 根 `docs/` | ❌ | ❌ | ✅ |
| `dist/` `node_modules/` 缓存 | ❌ | ❌ | ❌ |
| 临时 `scripts/_*` · `.privacy-deny.local` | ❌ | ❌ | ❌ |

## 新增技能

1. 根目录建 `<new-id>/SKILL.md`，`name` 与目录一致。
2. 附 `README.md`、`package.json`；有工具则 `package_skill.py --check`。
3. 登记 README 技能表、`npm run sync:files`、CHANGELOG（CI/Release 动态发现技能）。
4. 隐私清单全绿。

## 排错

| 现象 | 处理 |
|------|------|
| `ENEEDAUTH` / `403` 2FA | `npm login --registry https://registry.npmjs.org/`，granular token 或 `--otp` |
| `403` cannot publish over version | 已存在 → bump |
| Public 但 registry 404 | 索引延迟 / 指定官方 registry；publish 只用 `registry.npmjs.org` |
| tag 后 npm 未发 | 查 Actions 与 `NPM_TOKEN` |
