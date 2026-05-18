# OpenClaw Dual-Install Pattern — Session Reference

## Context
Charles noticed his OpenClaw TUI showed "protocol mismatch / gateway disconnected" after an earlier session where OpenClaw was moved from Docker to the host level. The root cause: **two OpenClaw installations fighting over port 18789**.

---

## What Exists on This System

### Host-level installation (primary)
- Binary: `/data/linuxbrew/.linuxbrew/bin/node` (Node wrapper) wrapping `openclaw`
- PID: 2619843 — owns port 18789 (verified via `lsof -i :18789`)
- Working directory: `/data`
- Spawned by PID 2619837: `sh -c openclaw gateway run --port 18789 >> /tmp/gateway.log 2>&1`
- TUI sessions: PIDs 2623610, 4113409, 4116604 (`openclaw-tui`)
- Version: OpenClaw 2026.5.12 (f066dd2)

### Docker container (redundant)
- Container: `openclaw-mm3f-openclaw-1` (image: `ghcr.io/hostinger/hvps-openclaw:latest`)
- Status in container logs: `EADDRINUSE: address already in use 127.0.0.1:18789`
- Gateway inside container never starts — crashes immediately
- Version (same binary in container): OpenClaw 2026.5.12

### Workspace files
- Host workspace: `/root/.openclaw/workspace/` — has `AGENTS.md`, `TOOLS.md`, `MEMORY.md`, agent dirs (bob, eric, mark, michael, tammie)
- Docker workspace: `/data/.openclaw/workspace/` — same files, synced (verified via `diff` on TOOLS.md sizes)

---

## Key Files and Commands Used

### Check which gateway owns port 18789
```bash
lsof -i :18789
# Output:
# COMMAND       PID    USER   FD   TYPE ...
# openclaw  2619843   root   22u  IPv4 ...
# openclaw  2619843   root   23u  IPv6 ...
```

### Check gateway health
```bash
curl -s http://127.0.0.1:18789/health
# {"ok":true,"status":"live"}
```

### Check skills count in Docker vs host
```bash
# Docker skills (inside container):
docker exec openclaw-mm3f-openclaw-1 openclaw skills | grep "Skills ("
# Skills (59/97 ready)

# MCP — none configured (both host and container):
docker exec openclaw-mm3f-openclaw-1 openclaw mcp list
# No MCP servers configured
```

### Check agent TOOLS.md sizes
| Agent | Host lines | Docker lines |
|-------|-----------|--------------|
| bob | 258 | 284 |
| eric | 158 | 141 |
| mark | 73 | 73 |
| michael | 317 | 317 |
| tammie | 76 | 44 |

### Check OpenClaw version in Docker vs host
```bash
docker exec openclaw-mm3f-openclaw-1 openclaw --version
# OpenClaw 2026.5.12 (f066dd2)
# Host is also 2026.5.12 — same binary version
```

---

## Resolution

**Host-level is the primary.** Docker container's redundant gateway was disabled by the port conflict. The TUI sessions (PIDs 2623610, 4113409, 4116604) all connect to the host-level gateway.

**Options going forward:**
1. Leave Docker container running — it just spam-logs the crash but doesn't interfere
2. Stop the Docker container entirely (cleaner logs, no value add)
3. Disable the container's gateway in its `openclaw.json` config

Charles chose option 1 for now — leave it running.

---

## TUI "protocol mismatch" Error — Full Text

```
openclaw tui - ws://127.0.0.1:18789 - agent main - session main
connecting | idle
not connected to gateway — message not sent
disconnected | disconnected
gateway disconnected: protocol mismatch | idle
```

**Cause:** Container's old gateway crashed before establishing WebSocket. The host-level gateway is working fine — just the container's TUI attempt that fails.

---

## Related Commands

```bash
# Check all openclaw processes
ps aux | grep openclaw | grep -v grep

# Check docker container logs (shows the crash)
docker logs openclaw-mm3f-openclaw-1 --tail 30

# Check gateway token (for API calls)
cat /proc/2619843/environ | tr '\0' '\n' | grep OPENCLAW_GATEWAY_TOKEN
```