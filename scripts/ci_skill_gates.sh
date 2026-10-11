#!/usr/bin/env bash
# Shared skill-package gates for CI + Release (single source of truth).
# Usage (from repo root):
#   bash scripts/ci_skill_gates.sh
# Env:
#   PYTHON / NODE optional overrides
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="${PYTHON:-python3}"
for arg in "$@"; do
  case "$arg" in
    -h|--help)
      sed -n '2,8p' "$0"
      exit 0
      ;;
  esac
done

SKILLS=()
# NOTE: `while read` instead of `mapfile` — macOS ships bash 3.2, which has no `mapfile`.
while IFS= read -r line; do
  [[ -n "$line" ]] && SKILLS+=("$line")
done < <(node scripts/discover_skills.js)
if [[ ${#SKILLS[@]} -eq 0 ]]; then
  echo "ci_skill_gates: no skills discovered" >&2
  exit 1
fi
echo "ci_skill_gates: discovered ${SKILLS[*]}"

run_one() {
  local skill="$1"
  echo "=== gates: ${skill} ==="
  pushd "$skill" >/dev/null

  # 没有运行时依赖就不调用 npm：`npm install` 会顺手写出一个空的 package-lock.json，
  # 之前 poster、viral-posts 的临时锁文件就是这样混进 npm 包的。
  if node -e 'const p=require("./package.json");process.exit(Object.keys(p.dependencies||{}).length?0:1)'; then
    if [[ -f package-lock.json ]]; then
      npm ci --omit=dev
    else
      npm install --omit=dev --no-package-lock
    fi
  else
    echo "skip npm install: ${skill} has no runtime dependencies"
  fi

  # 清理测试运行产生的 __pycache__ 和 dist，避免 package 检查误报
  find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
  find . -name "*.pyc" -delete 2>/dev/null || true
  rm -rf dist 2>/dev/null || true

  "$PY" scripts/package_skill.py --check
  "$PY" scripts/audit_styles.py
  "$PY" scripts/audit_docs.py
  "$PY" scripts/audit_skill.py
  "$PY" scripts/audit_css.py

  "$PY" scripts/negative_tests.py

  # Optional feedback-gate unit tests when present (fast; keep green)
  if [[ -f scripts/test_feedback_gates.py ]]; then
    "$PY" scripts/test_feedback_gates.py
  fi

  popd >/dev/null
  echo "=== gates OK: ${skill} ==="
}

for skill in "${SKILLS[@]}"; do
  run_one "$skill"
done

echo "ci_skill_gates: all skills green"
