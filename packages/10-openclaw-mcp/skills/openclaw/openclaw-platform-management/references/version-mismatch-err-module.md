# OpenClaw ERR_MODULE_NOT_FOUND — Version Mismatch Fix (May 14 2026)

## Error Summary

**Symptom:** Gateway `/health` returns `{"ok":true,"status":"live"}` on localhost, but external access returns `000`. WebSocket requests fail with `UNAVAILABLE`. Logs show repeated:

```
Cannot find module '/data/.npm-global/lib/node_modules/openclaw/dist/task-registry.maintenance-DuW0FRWY.js'
Cannot find module '/data/.npm-global/lib/node_modules/openclaw/dist/managed-image-attachments-BBVq6nY1.js'
Cannot find module '/data/.openclaw/plugin-runtime-deps/openclaw-2026.4.29-c27ae31043c7/dist/cleanup-kBh9Q3mQ.js'
```

**Root Cause:** `lastTouchedVersion` in openclaw.json (2026.5.5) did not match the installed npm package version (2026.5.7). OpenClaw bundles JS files with content-hashed filenames. When version metadata doesn't match the installed package, the gateway tries to load chunks with stale hash suffixes that no longer exist.

## Diagnosis

```bash
# 1. Check installed npm package version
docker exec openclaw-mm3f-openclaw-1 npm list -g openclaw

# 2. Check what version openclaw.json thinks is running
docker exec openclaw-mm3f-openclaw-1 cat /data/.openclaw/openclaw.json | python3 -c "
import json,sys; d=json.load(sys.stdin); print(d.get('meta', {}))"

# 3. List actual hash suffixes in dist/
docker exec openclaw-mm3f-openclaw-1 ls /data/.npm-global/lib/node_modules/openclaw/dist/ | grep -E "cleanup|task-registry.maintenance|managed-image"

# 4. Compare — error shows hash DuW0FRWY but actual is DxA2A4eM
# If they don't match → version mismatch confirmed
```

**Actual dist contents on 2026.5.7:**
```
cleanup-CQawj5mF.js           # error referenced kBh9Q3mQ — MISSING
task-registry-DxA2A4eM.js     # error referenced DuW0FRWY — MISSING
managed-image-attachments-B3bNoT7I.js  # error referenced BBVq6nY1 — MISSING
```

## Fix (Two Steps)

**Step 1 — Restart container to force re-sync:**
```bash
cd /docker/openclaw-mm3f && docker compose restart openclaw
```

**Step 2 — Update lastTouchedVersion in openclaw.json:**
```bash
docker exec openclaw-mm3f-openclaw-1 sed -i 's/"lastTouchedVersion": "2026.5.5"/"lastTouchedVersion": "2026.5.7"/' /data/.openclaw/openclaw.json
```

## Verification

```bash
# External port should now return 200 (OpenClaw web UI)
curl -s -o /dev/null -w "%{http_code}" "http://$CHARLES_HOST_IP:49248/"
# Expected: 200

# Internal health should still be 200
curl -s http://127.0.0.1:18789/health
# Expected: {"ok":true,"status":"live"}

# Container logs should show clean startup
docker logs openclaw-mm3f-openclaw-1 --tail 20
# Expected: no ERR_MODULE_NOT_FOUND in recent entries
```

## Key Insight

`lastTouchedVersion` is OpenClaw's internal schema version tracker — it must match the installed `openclaw` npm package version for the gateway to resolve the correct content-hashed JS chunk filenames. This is NOT the same as the application version field — it lives inside `meta` in openclaw.json and gets updated by the gateway on startup. When it diverges from reality (e.g., after an npm package upgrade without a config regeneration), module resolution breaks.

## Related Patterns

- Error Pattern 1 (cleanup-*.js dispatch errors): Same root cause — stale plugin-runtime-deps path from old version. Telegram still works because sendMessage is a different code path. See `references/openclaw-nonfatal-errors.md`.
- Session pruning: Cosmetic noise, unrelated. Repeats every 60s. Not an error.
