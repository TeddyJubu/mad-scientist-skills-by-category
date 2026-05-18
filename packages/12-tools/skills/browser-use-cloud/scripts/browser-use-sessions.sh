#!/usr/bin/env bash
set -euo pipefail

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

: "${BROWSER_USE_API_KEY:?BROWSER_USE_API_KEY is not set}"

page_size="${1:-5}"

curl -sS "https://api.browser-use.com/api/v3/sessions?page_size=$page_size" \
  -H "X-Browser-Use-API-Key: $BROWSER_USE_API_KEY" |
  jq '{
    total,
    page,
    pageSize,
    sessions: [
      .sessions[]? | {
        id,
        status,
        title,
        isTaskSuccessful,
        liveUrl,
        totalCostUsd,
        updatedAt
      }
    ]
  }'
