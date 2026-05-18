# OpenClaw Reference Notes — May 15 2026 Session

## Architecture: Container-only, no host binary

On this VPS, the `openclaw` binary exists ONLY inside the Docker container at `/data/.npm-global/bin/openclaw`. There is no host-level installation.

**Implications:**
- `which openclaw` → empty (do not be fooled)
- All commands require `docker exec openclaw-mm3f-openclaw-1 /data/.npm-global/bin/openclaw ...`
- Stopping the container kills the gateway with no fallback
- Restart: `cd /docker/openclaw-mm3f && docker compose up -d`

## Version

Both host and Docker report **OpenClaw 2026.5.12 (f066dd2)** — the version is the same. The old "dual install" confusion was from a misinterpretation of the process list. The PIDs 2619843 and 2619837 that looked like host-level processes were actually remnants from a PREVIOUS container run that didn't clean up properly.

## Protocol Mismatch Root Cause

**Symptom:** TUI showed `connecting | idle → not connected to gateway — message not sent → disconnected | disconnected → gateway disconnected: protocol mismatch | idle`

**Root cause:** The gateway had been stopped (container not running). The TUI was trying to connect to port 18789 with no server there. "Protocol mismatch" is the WebSocket upgrade failure when the server isn't speaking OpenClaw protocol (or isn't there at all).

**Fix:** Restart the container → gateway resumes on 18789 → TUI connects cleanly.

## Restart Verification Sequence

```bash
# 1. Restart container
cd /docker/openclaw-mm3f && docker compose up -d

# 2. Wait for gateway to initialize
sleep 10

# 3. Verify port is listening
ss -tlnp | grep 18789
# Should show: openclaw on 127.0.0.1:18789 LISTEN

# 4. Verify health
curl -s http://127.0.0.1:18789/health
# Expected: {"ok":true,"status":"live"}
```

## Compose File Location

- **Path:** `/docker/openclaw-mm3f/docker-compose.yml`
- **Data volume:** `./data:/data` (on host: `/docker/openclaw-mm3f/data`)
- **Workspace:** `/data/.openclaw/workspace/` (synced to host `/root/.openclaw/workspace/`)

## Agent Skills Comparison (Docker vs Host)

Both Docker and host workspace reference the same agent files (`/root/.openclaw/workspace/agents/`). TOOLS.md line counts were mostly similar, with minor differences:

| Agent | Host TOOLS.md | Docker TOOLS.md |
|-------|--------------|----------------|
| bob | 258 lines | 284 lines |
| eric | 158 lines | 141 lines |
| mark | 73 lines | 73 lines |
| michael | 317 lines | 317 lines |
| tammie | 76 lines | 44 lines |

The host is the primary workspace. Docker's workspace is a volume sync of the same files.