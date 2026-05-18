# Apify MCP Session Setup Reference

## Initial Setup (One-Time)

The Apify MCP session must be created before using any `mcpc @apify` commands.

### Create Session

```bash
export APIFY_TOKEN="YOUR_APIFY_TOKEN_HERE"
mcpc connect mcp.apify.com @apify --header "Authorization: Bearer ${APIFY_TOKEN}"
```

**Expected output:**
```
✓ Session @apify created
[@apify → https://mcp.apify.com (HTTP)]

Server: apify-mcp-server (version: 0.9.16)
...
```

### Verify Session

```bash
mcpc @apify
# Should show session info, capabilities, and tools
```

---

## Session Lifecycle

### Check Status
```bash
mcpc  # Lists all sessions and their status
```

**Session states:**
- 🟢 **live**: Bridge running, server responding
- 🟡 **disconnected**: Bridge running but server unreachable (auto-recovers)
- 🟡 **crashed**: Bridge crashed (auto-restarts on next use)
- 🔴 **unauthorized**: Auth failed (run `mcpc @apify restart`)
- 🔴 **expired**: Session ID rejected (run `mcpc @apify restart`)

### Restart Session
```bash
mcpc @apify restart
```

### Close Session
```bash
mcpc @apify close
```

---

## Credential Storage

- **Token location**: `.secrets/apify.env` (not committed)
- **Session metadata**: `~/.mcpc/sessions.json`
- **Auth tokens**: `~/.mcpc/credentials.json` (file-based, chmod 0600)
  - OS keychain used when available (gnome-keyring on Linux Desktop)

---

## Troubleshooting

### "Session not found"
```bash
# Re-create the session
export APIFY_TOKEN="YOUR_APIFY_TOKEN_HERE"
mcpc connect mcp.apify.com @apify --header "Authorization: Bearer ${APIFY_TOKEN}"
```

### "Cannot connect to bridge"
```bash
# Check if bridge is running
ps aux | grep mcpc

# Restart session
mcpc @apify restart
```

### "401 Unauthorized"
```bash
# Verify token
cat ~/.openclaw/workspace/.secrets/apify.env

# Restart session with correct token
mcpc @apify close
export APIFY_TOKEN="<your_token>"
mcpc connect mcp.apify.com @apify --header "Authorization: Bearer ${APIFY_TOKEN}"
```

---

## Session Persistence

The `@apify` session persists across:
- Shell sessions
- System reboots (bridge auto-restarts on first use)
- Network disconnections (auto-reconnects)

**When to recreate:**
- After `mcpc clean sessions`
- After manually deleting `~/.mcpc/sessions.json`
- If session state is 🔴 **expired** and restart doesn't fix it
