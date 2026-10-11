#!/usr/bin/env bash
# Deprecate obsolete @topmindspace/tms-skills 2.x line on npm (one-shot @2.x + verify).
# Prefer: GitHub Actions workflow "Deprecate npm 2.x" (uses NPM_TOKEN).
# Or run manually after `npm login` / with NPM_TOKEN in env.
set -euo pipefail

MSG_EN="Obsolete after repo reset. Renamed to @topmindspace/topmind-writing-skills. Do not install ^2."
MSG_ZH="仓库重置后 2.x 已废弃。已改名为 @topmindspace/topmind-writing-skills。请勿安装 ^2。"
MSG="${MSG_ZH} / ${MSG_EN}"

echo "Deprecating @topmindspace/tms-skills@2.x ..."
npm deprecate "@topmindspace/tms-skills@2.x" "$MSG"

echo "Verify:"
npm view @topmindspace/tms-skills --json | node -e '
const d=JSON.parse(require("fs").readFileSync(0,"utf8"));
console.log("latest=", d.version);
console.log("deprecated=", d.deprecated||"(no package-level deprecated field)");
'
echo "Done. Per-version deprecate is covered by the @2.x range."
