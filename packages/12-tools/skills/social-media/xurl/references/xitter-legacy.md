---
name: xitter-legacy
description: Legacy X/Twitter skill via x-cli (third-party Python CLI). Superseded by xurl (official X CLI). Retained for reference.
---

# xitter — Legacy X/Twitter via x-cli (SUPERSEDED by xurl)

**This skill is archived. Use the `xurl` skill instead.**

## Why xurl replaced xitter

- `xurl` is the official X Developer Platform CLI
- `xitter` wraps a third-party Python CLI (`x-cli`) with 5 env vars
- xurl supports OAuth 2.0 PKCE (no secrets passed inline), media upload, DMs, and full v2 API
- xitter has a smaller API surface and requires the older OAuth 1.0a flow

## xitter content (for reference only)

If you ever need to resurrect xitter work:

**Installation:**
```bash
uv tool install git+https://github.com/Infatoshi/x-cli.git
```

**Required credentials (5 env vars):**
```
X_API_KEY=...
X_API_SECRET=...
X_BEARER_TOKEN=...
X_ACCESS_TOKEN=...
X_ACCESS_TOKEN_SECRET=...
```

**Storage:** `~/.config/x-cli/.env`

**Common commands:**
```bash
x-cli tweet post "Hello world"
x-cli user get openai
x-cli me mentions --max 20
x-cli like 1234567890
x-cli retweet 1234567890
x-cli tweet search "AI agents" --max 20
```

**Pitfalls (same as before):**
- X API access is paid for meaningful usage
- 403 oauth1-permissions → regenerate access token with Read+Write permissions
- Reply restrictions → use `tweet quote` instead
- Rate limits apply per endpoint

**When to use xitter instead of xurl:**
Only if the user specifically needs `x-cli` shortcuts and has already configured x-cli credentials. For all new work, use xurl.
