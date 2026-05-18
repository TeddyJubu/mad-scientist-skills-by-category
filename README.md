# Mad Scientist Essential Skill Collections

**12独立packages · 可单独安装或整体使用**

> For Hermes/OpenClaw AI agent systems. Each package is a sellable, installable unit.

---

## What This Monorepo Gives You

This is a collection of AI agent skill packages — each one is a set of specialized tools your AI can use to do a specific job. Think of it like hiring a specialist for each part of your business. The Real Estate package handles property research. The Content package handles your social media. The AI Agents package runs your virtual team.

Every skill is designed to work inside **Hermes** or **OpenClaw** — your AI agent platforms. You load a skill, then tell your AI what you want in plain English. It figures out how to do it.

---

## Packages Overview

| Package | Skills | What It Does |
|---------|--------|-------------|
| [`@mad-scientist/real-estate`](./packages/01-real-estate) | 7 | Find property owners, estimate repairs, pull property records |
| [`@mad-scientist/content-social`](./packages/02-content-social) | 15 | Thumbnails, video clips, social posting, image generation |
| [`@mad-scientist/productivity`](./packages/03-productivity) | 9 | Notion, Gmail, Google Drive, PDFs, file delivery |
| [`@mad-scientist/devops-infrastructure`](./packages/04-devops-infrastructure) | 6 | Deploy websites, manage servers, set up domains |
| [`@mad-scientist/data-research`](./packages/05-data-research) | 12 | Find business contacts, scrape data, census, SEO |
| [`@mad-scientist/ai-agents`](./packages/06-ai-agents) | 18 | Bob, Sarah, Tammie, agent creation, automation |
| [`@mad-scientist/image-graphics`](./packages/07-image-graphics) | 8 | AI images, avatar videos, animated videos, photo editing |
| [`@mad-scientist/communication`](./packages/08-communication) | 1 | Discord bot management |
| [`@mad-scientist/media-lifestyle`](./packages/09-media-lifestyle) | 10 | YouTube, Spotify, weather, health tracking |
| [`@mad-scientist/openclaw-mcp`](./packages/10-openclaw-mcp) | 2 | OpenClaw platform, MCP connections |
| [`@mad-scientist/software-development`](./packages/11-software-development) | 1 | Code review, debugging, testing |
| [`@mad-scientist/tools`](./packages/12-tools) | 31 | ML training, smart home, GitHub, CRM, and more |

**Total: 120 skills across 12 packages**

---

## How It Works

Each package contains individual **skills** — standalone units that give your AI a specific capability. Skills are just folders with a `SKILL.md` file inside that tells your AI how to use them.

```
Example: Real Estate Package
├── package.json
├── README.md
└── skills/
    ├── sdat-property-search/     ← look up MD property records
    ├── rentcast-property-report/ ← investment analysis
    ├── homedepot-repair-estimator/ ← material cost estimates
    └── ...
```

You load a skill with: `skill_view(name="sdat-property-search")`

Then you just talk to your AI: "Look up the property at 123 Main Street, Baltimore"

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/Mad-Scientist-sudo/Mad-scientist-essential-skill-collections.git
cd Mad-scientist-essential-skill-collections

# Install all packages
pnpm install

# Or install one package only
cd packages/01-real-estate
pnpm install
```

---

## Installing Individual Packages

Each package is named and versioned — install them one at a time:

```bash
npm install @mad-scientist/real-estate      # Property research tools
npm install @mad-scientist/content-social   # Content & social media
npm install @mad-scientist/productivity     # Notion, email, files
npm install @mad-scientist/devops-infrastructure  # Servers & deployment
npm install @mad-scientist/data-research    # Research & data scraping
npm install @mad-scientist/ai-agents        # Your AI team (Bob, Sarah, etc.)
npm install @mad-scientist/image-graphics  # Images, videos, avatars
npm install @mad-scientist/communication    # Discord bot
npm install @mad-scientist/media-lifestyle  # YouTube, Spotify, weather
npm install @mad-scientist/openclaw-mcp    # Platform & integrations
npm install @mad-scientist/software-development  # Code tools
npm install @mad-scientist/tools           # Everything else
```

---

## Publishing (for maintainers)

```bash
cd packages/01-real-estate
npm publish --access public
```

---

## License

Proprietary — © 2026 Mad Scientist LLC. All rights reserved.
