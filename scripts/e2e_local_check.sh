#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_BIN="$ROOT_DIR/.venv/bin"
CLI_BIN="$VENV_BIN/clawshire"

run() {
  echo
  echo "==> $*"
  "$@"
}

run_annual_analysis_smoke() {
  echo
  echo "==> $CLI_BIN annual-analysis company 000001 --year 2025 --format json"
  local output
  if output="$("$CLI_BIN" annual-analysis company 000001 --year 2025 --format json 2>&1)"; then
    printf '%s\n' "$output"
    return 0
  fi
  printf '%s\n' "$output"
  if [[ "$output" == *"该年报已有分析任务在进行中，请稍后再试"* ]]; then
    echo "annual-analysis smoke accepted: existing in-progress task"
    return 0
  fi
  return 1
}

if [[ ! -x "$VENV_BIN/python" ]]; then
  echo "missing virtualenv python: $VENV_BIN/python" >&2
  exit 1
fi

if [[ ! -x "$CLI_BIN" ]]; then
  echo "missing CLI entrypoint: $CLI_BIN" >&2
  exit 1
fi

cd "$ROOT_DIR"

run "$VENV_BIN/pytest" -q
run "$VENV_BIN/python" scripts/check_skill_drift.py
run "$CLI_BIN" --help
run "$CLI_BIN" version
run "$CLI_BIN" auth --help
run find skills -maxdepth 3 -type f

if [[ -n "${CLAWSHIRE_API_KEY:-}" ]]; then
  run "$CLI_BIN" auth status
  run "$CLI_BIN" auth check
  run "$CLI_BIN" user info
  run "$CLI_BIN" notice stock 603402 --start-date 2026-04-01 --end-date 2026-04-20 --page-size 3
  run "$CLI_BIN" annual-report latest --year 2025 --keyword 平安银行 --page-size 3
  run_annual_analysis_smoke
else
  echo
  echo "CLAWSHIRE_API_KEY is not set; skipped live auth and API checks."
fi
