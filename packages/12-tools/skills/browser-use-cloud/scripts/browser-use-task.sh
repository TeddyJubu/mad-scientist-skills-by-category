#!/usr/bin/env bash
set -euo pipefail

load_env() {
  for env_file in \
    "${BROWSER_USE_ENV:-}" \
    "/root/.hermes/browser-use.env" \
    "/data/.openclaw/workspace/.secrets/browser-use.env" \
    "/root/.openclaw/workspace/.secrets/browser-use.env"; do
    if [ -n "${env_file:-}" ] && [ -f "$env_file" ]; then
      set -a
      # shellcheck source=/dev/null
      . "$env_file"
      set +a
    fi
  done
}

usage() {
  cat >&2 <<'EOF'
Usage:
  browser-use-task.sh "natural language browser task"

Environment:
  BROWSER_USE_API_KEY      required
  BROWSER_USE_MODEL        optional, default claude-sonnet-4.6
  BROWSER_USE_POLL_SECONDS optional, default 2
  BROWSER_USE_TIMEOUT_SEC  optional, default 14400
EOF
}

load_env

if [ $# -lt 1 ]; then
  usage
  exit 2
fi

: "${BROWSER_USE_API_KEY:?BROWSER_USE_API_KEY is not set}"

task="$*"
model="${BROWSER_USE_MODEL:-claude-sonnet-4.6}"
poll_seconds="${BROWSER_USE_POLL_SECONDS:-2}"
timeout_sec="${BROWSER_USE_TIMEOUT_SEC:-14400}"
base_url="https://api.browser-use.com/api/v3"

payload="$(jq -n --arg task "$task" --arg model "$model" '{task: $task, model: $model}')"

session_json="$(curl -sS -X POST "$base_url/sessions" \
  -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$payload")"

session_id="$(printf '%s' "$session_json" | jq -r '.id // empty')"
if [ -z "$session_id" ]; then
  printf '%s\n' "$session_json" >&2
  exit 1
fi

start_ts="$(date +%s)"
last_status=""

while true; do
  current_json="$(curl -sS "$base_url/sessions/$session_id" \
    -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY")"
  status="$(printf '%s' "$current_json" | jq -r '.status // "unknown"')"
  if [ "$status" != "$last_status" ]; then
    printf 'Browser Use session %s status=%s liveUrl=%s\n' \
      "$session_id" \
      "$status" \
      "$(printf '%s' "$current_json" | jq -r '.liveUrl // empty')" >&2
    last_status="$status"
  fi
  case "$status" in
    idle|stopped|error|timed_out)
      printf '%s' "$current_json" | jq '{
        id,
        status,
        isTaskSuccessful,
        output,
        liveUrl,
        recordingUrls,
        screenshotUrl,
        totalCostUsd,
        llmCostUsd,
        browserCostUsd,
        proxyCostUsd,
        lastStepSummary,
        stepCount
      }'
      exit 0
      ;;
  esac
  now_ts="$(date +%s)"
  if [ "$((now_ts - start_ts))" -ge "$timeout_sec" ]; then
    printf 'Timed out waiting for Browser Use session %s\n' "$session_id" >&2
    printf '%s' "$current_json" | jq .
    exit 124
  fi
  sleep "$poll_seconds"
done
