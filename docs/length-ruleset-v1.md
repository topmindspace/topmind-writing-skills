# 长度规则集运行契约 v1

`runtime/length-ruleset.mjs` 提供 `parseLengthRuleSet(jsonText)` 和 `evaluateLengthRuleSet({ ruleSetJson, target, document, asOf, creationSnapshotFingerprint? })`。它是宿主无关的 JSON 加载、结构校验、入口匹配和长度报告入口。本包不附带平台规则，入口也不加载 YAML。规则数据中的“官方来源”仍需维护者逐条核对原文、发布入口与适用账号；URL 字段本身不是核验凭证。

输入根对象仅有 `schemaVersion: 1`、`id`、`version`、`rules`。每条规则仅支持 `platform_limit` 或 `creator_preference`，四维 `applies_to` 必须明确给出 `platform`、`format`、`entrypoint`、`account_capability`，不限定的维度填 `any`，未知目标填 `unknown`。当前只执行 `max_characters` / `unicode_code_points` 的 `title` 或 `body` 上限；加权 X 计数和图片规则不在本版本能力内。规则集上限为 1 MiB、1000 条，重复 ID、非 JSON 数值、敏感键和未识别字段会被拒绝。

X 的[普通帖帮助页](https://help.x.com/en/using-x/types-of-posts)写有典型 280 字符限制，[官方 twitter-text v3 配置](https://github.com/twitter/twitter-text/blob/master/config/v3.json)定义加权长度和 URL、emoji 计数。本版本只做 Unicode 码点上限，不能代替该算法。引入官方 JS 实现前须处理其运行依赖与独立宿主包的装载，并以目标入口实测；本地预检始终不能代替编辑器最终核对。

`npm run host:pack` 现在先在隔离临时目录加载 `runtime.capabilities` 的每个入口并验证可调用导出，再更新宿主包目录。此门禁能发现未随包携带的运行依赖或错误的导出声明；它只验证模块可加载，不代表平台规则已核准或能力行为已验收。

活跃的平台硬规则必须给出 HTTPS 来源、`checked_at`、逐条 `review_after` 和 `official_primary` 来源级别。`asOf` 是调用方明确传入的 ISO 日期，纳入报告指纹；早于 `checked_at` 或超过 `review_after` 时该规则不执行，结果转人工复核。活跃个人偏好须有 `user_confirmed` 与 `confirmed_at`，只返回警告，不能放宽平台上限；评估日期早于确认日时不执行。直接调用低层 `length.evaluate` 也执行这些日期条件，不能绕过规则集入口。`proposed_unconfirmed` 偏好不会自动启用。

报告保留统一能力结果外壳，并给出规则集 ID/版本、`input.rulesDigest`、`input.documentDigest`、检查与诊断。应用层把 `parseLengthRuleSet` 返回的同一份 `rules` 交给 Kernel `creator.snapshot` 的 `ruleset.rules`，并可传 `lengthValidation` 绑定送检文本、提供者和评估日期；随后把快照 `fingerprint` 作为 `creationSnapshotFingerprint` 传给 `evaluateLengthRuleSet`。Kernel `compareCreationLengthReport` 或 UTR `creator.matchLengthReport` 核对两份声明及快照指纹。独立技能调用可省略该参数，但不能关联为当前工作区报告。交接前仍须重算快照；源稿或资源变化后旧报告失效。`documentDigest` 只锁定送检的 `platform_text`，尚未证明它由所选母稿和渲染产物产生；匹配结果固定不表示可发布。
