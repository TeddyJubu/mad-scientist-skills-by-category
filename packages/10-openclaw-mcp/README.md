# OpenClaw & MCP Skills
**Package:** `@mad-scientist/openclaw-mcp` | **2 Skills** | Version 1.0.0

---

## What This Package Does For You

This package is the control center for your OpenClaw AI platform. OpenClaw is the system that runs your AI agents (Sarah, Bob, Tammie, etc.) and connects them to tools. This package helps you set up, configure, and manage those connections.

The "MCP" part stands for Model Context Protocol — it's how your AI agents connect to external tools and data sources. This package shows you exactly how to add new connections so your agents can do more things.

---

## Skills In This Package

### 1. OpenClaw (Platform Management)
**What it does:** The main OpenClaw platform skill — manages the overall AI agent platform. Handles agent creation, configuration, updates, monitoring, and troubleshooting. Everything about running your AI team in one place.

**What to say:**  
> "Show me all my currently active AI agents and their status"
> "Update my Bob agent to use the latest skip-trace API"
> "Check if there are any errors in my OpenClaw logs from today"

**What you get:** Agent status overview, configuration updates applied, or a clean error report with fixes.

---

### 2. MCP (Model Context Protocol)
**What it does:** Shows you how to connect new tools and data sources to your AI agents through MCP. MCP is just a technical term for "the bridge between your AI and other apps." This skill walks you through setting up any MCP connection step by step.

**What to say:**  
> "I want my AI agent to have access to my QuickBooks — how do I set up that MCP connection?"
> "Set up an MCP connection to a PostgreSQL database so my agents can query it directly"

**What you get:** Step-by-step instructions for connecting your AI to the new tool or data source, including any required API keys and authentication steps.

---

## What You Can Do With MCP Connections

Once connected via MCP, your AI agents can:
- **Read your Google Sheets** — pull data from spreadsheets into reports
- **Query your database** — ask questions about your data in plain English
- **Post to Slack** — send updates to your team's Slack channels
- **Connect to Airtable** — manage your Airtable bases directly
- **Access Notion** — read and write to your Notion workspace
- **And much more** — any tool with an API can be connected

---

## How To Use This Package

### Installation
```bash
npm install @mad-scientist/openclaw-mcp
```

Or symlink into your Hermes skills folder:
```bash
ln -s $(pwd)/skills ~/.hermes/skills/openclaw-mcp
```

### Quick Start
```
skill_view(name="openclaw")
skill_view(name="mcp")
```

---

## What To Expect

| Skill | Time to Result | Best For |
|-------|---------------|----------|
| OpenClaw | 5-15 seconds | Agent management & monitoring |
| MCP | 5-15 minutes setup | Connect AI to new tools |

**Note:** MCP setup requires some technical configuration (API keys, authentication) — your AI agent will guide you through each step.

---

## License

Proprietary — © 2026 Mad Scientist LLC. All rights reserved. Internal use only.
