# Productivity Skills
**Package:** `@mad-scientist/productivity` | **3 Skills** | Version 1.0.0

---

## What This Package Does

Notion, email, Google Workspace, document, and PDF workflows

## Skills In This Package

### 1. agentmail-productivity
**Folder:** `skills/agentmail`

agentmail lets the user create and manage dedicated email inboxes for AI agents, send and receive emails programmatically, and handle email-based workflows with webhooks and real-time events, which is useful when they need an agent to have its own email identity for outreach, notifications, or handling incoming email without relying on traditional personal email accounts.

### 2. notion-mastery
**Folder:** `skills/notion-mastery`

Build beautiful, well-organized Notion pages and databases — from a single meeting note to a full team wiki, CRM, OKR tracker, or project hub. Use this skill whenever the user mentions Notion, asks to create or update a Notion page or database, wants to design a workspace, build a template, sync content into Notion, or even hints at workflows like "wiki", "team space", "project tracker", "second brain", "meeting notes hub", "PARA", "Zettelkasten", "company knowledge base", or "personal dashboard" — even if they don't explicitly say "Notion". Also triggers on Notion API questions, block JSON, database schema design, property types, formula syntax, relations, rollups, and on requests to convert markdown or other documents into Notion. Designed to work in agents that consume the agentskills.io SKILL.md format (Anthropic, Hermes Agent, OpenClaw) whether they call the API via MCP, the official SDK, or raw HTTP.

### 3. pdf-generation
**Folder:** `skills/pdf-generation`

pdf-generation lets the user create PDF documents from text, HTML, or structured data when weasyprint fails due to font subsetting bugs, using fpdf2 as a reliable fallback so they can still produce clean, usable PDFs for reports, invoices, or printed materials.

## Agent Install

```bash
npm install @mad-scientist/productivity
```

Or copy the `skills/` directory into your agent skills root.

## License

Proprietary - (c) 2026 Mad Scientist LLC. All rights reserved.
