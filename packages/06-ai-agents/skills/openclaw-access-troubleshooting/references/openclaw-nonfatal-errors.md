# OpenClaw Non-Fatal Error Reference

## Error Pattern 1: ERR_MODULE_NOT_FOUND (cleanup-*.js)

**First occurrence (May 14 05:25:43):**
```
2026-05-14T05:25:43.341-04:00 [telegram] dispatch failed: Error [ERR_MODULE_NOT_FOUND]: Cannot find module '/data/.openclaw/plugin-runtime-deps/openclaw-2026.4.29-c27ae31043c7/dist/cleanup-kBh9Q3mQ.js' imported from /data/.openclaw/plugin-runtime-deps/openclaw-2026.4.29-c27ae31043c7/dist/store-CX_a-msa.js
2026-05-14T05:25:44.440-04:00 [telegram] sendMessage ok chat=8597738529 message=5653
```

**Second occurrence (May 14 05:27:01):**
```
2026-05-14T05:27:01.892-04:00 [telegram] dispatch failed: Error [ERR_MODULE_NOT_FOUND]: Cannot find module '/data/.openclaw/plugin-runtime-deps/openclaw-2026.4.29-c27ae31043c7/dist/cleanup-kBh9Q3mQ.js' imported from /data/.openclaw/plugin-runtime-deps/openclaw-2026.4.29-c27ae31043c7/dist/store-CX_a-msa.js
2026-05-14T05:27:03.197-04:00 [telegram] sendMessage ok chat=8597738529 message=5655
```

**Diagnosis:** Despite the dispatch error, `sendMessage ok` confirms the Telegram bot is fully operational. The error is in the plugin runtime dependency layer, not the Telegram channel itself.

**Heartbeat failure (same root cause, May 14 04:50:21 and 05:20:21):**
```
2026-05-14T04:50:21.712-04:00 [heartbeat] failed: Cannot find module '/data/.npm-global/lib/node_modules/openclaw/dist/cleanup-kBh9Q3mQ.js' imported from /data/.npm-global/lib/node_modules/openclaw/dist/store-CX_a-msa.js
```

**Diagnosis:** Heartbeat fires every 30 minutes and fails with the same module error. The container continues running fine. The heartbeat failure is cosmetic.

**Path note:** The error references `/data/.openclaw/` paths, but on this machine the actual openclaw data lives at `/root/.openclaw/`. The container's internal `/data` volume is mapped to host `./data` but that directory doesn't exist on this host — it only exists inside the container. The plugin-runtime-deps path being stale is an internal OpenClaw issue, not a path-mapping problem.

**Bots confirmed up via:**
- `update-offset-*.json` files with recent timestamps (bot IDs: 8542419526/bob, 8510126838/mark, 8692099563/eric, 8740077082/michael, 8736136072/tammie)
- `docker exec openclaw-mm3f-openclaw-1 ps aux` showing two node processes: `node server.mjs` (PID 10) and `openclaw` (PID 22)
- Telegram sendMessage succeeding immediately after the dispatch errors

## Error Pattern 2: Session Pruning (cosmetic noise)

```
[sessions/store] pruned stale session entries
```
Repeats every minute. This is normal OpenClaw housekeeping — not an error. Do not flag this in status reports.

---

## Status Report Template (for health checks)

When Charles asks "how is everything doing?", use this structure:

```
✅ Core Systems:
- Hermes Gateway: Active (running X days)
- Docker stack: All N containers healthy
- Traefik: Up
- Filebrowser: Up (port 7000)
- Mission Control: Up

✅ OpenClaw (Eric's home):
- Container: Running
- Telegram: Connected (sending/receiving)
- Note: Non-fatal module error in logs (ERR_MODULE_NOT_FOUND: cleanup-*.js) — messages still go through

🤖 Team Status (by bot):
- Bob ✅ polling (lastUpdateId: X)
- Mark ✅ polling (lastUpdateId: X)
- [etc.]

📅 Cron Jobs:
- Daily EOD Report: Scheduled for tonight 9 PM ET ✅
- Health check cron: Paused (manual override)

⚠️ Any issues found (with log evidence)
```