# Mad Scientist Essential Skill Collections

**12独立packages · 可单独安装或整体使用**

> For Hermes/OpenClaw AI agent systems. Each package is a sellable, installable unit.

---

## Packages

| Package | Version | Skills | Description |
|---------|---------|--------|-------------|
| [`@mad-scientist/real-estate`](./packages/01-real-estate) | 1.0.0 | 7 | SDAT, skip-trace, RentCast, Home Depot rehab |
| [`@mad-scientist/content-social`](./packages/02-content-social) | 1.0.0 | 15 | YT thumbnails, OpusClip, Blotato, image gen |
| [`@mad-scientist/productivity`](./packages/03-productivity) | 1.0.0 | 9 | Notion, file-delivery, agentmail, Gmail, PDF |
| [`@mad-scientist/devops-infrastructure`](./packages/04-devops-infrastructure) | 1.0.0 | 6 | Vercel, Traefik, systemd port reservation |
| [`@mad-scientist/data-research`](./packages/05-data-research) | 1.0.0 | 12 | Apify, Apollo, Brave search, Census, SEO |
| [`@mad-scientist/ai-agents`](./packages/06-ai-agents) | 1.0.0 | 18 | Bob, Sarah caller, OpenClaw, HR, autonomous |
| [`@mad-scientist/image-graphics`](./packages/07-image-graphics) | 1.0.0 | 8 | GPT Image 2, HeyGen, Remotion, Nano Banana |
| [`@mad-scientist/communication`](./packages/08-communication) | 1.0.0 | 1 | Discord bot control |
| [`@mad-scientist/media-lifestyle`](./packages/09-media-lifestyle) | 1.0.0 | 10 | YouTube, Spotify, weather, healthcheck, gifs |
| [`@mad-scientist/openclaw-mcp`](./packages/10-openclaw-mcp) | 1.0.0 | 2 | OpenClaw platform, MCP client & server |
| [`@mad-scientist/software-development`](./packages/11-software-development) | 1.0.0 | 1 | Code review, debugging, TDD |
| [`@mad-scientist/tools`](./packages/12-tools) | 1.0.0 | 31 | MLOps, gaming, smart-home, GitHub, GHL |

**Total: 120 skills across 12 packages**

---

## Quick Start

```bash
git clone https://github.com/Mad-Scientist-sudo/Mad-scientist-essential-skill-collections.git
cd Mad-scientist-essential-skill-collections
pnpm install
```

## Install Individual Package

```bash
# Real Estate skills only
npm install @mad-scientist/real-estate

# Content & Social skills only
npm install @mad-scientist/content-social

# All AI agents
npm install @mad-scientist/ai-agents
```

## Monorepo Structure

```
Mad-scientist-essential-skill-collections/
├── packages/
│   ├── 01-real-estate/           ← @mad-scientist/real-estate
│   │   ├── package.json
│   │   ├── README.md
│   │   └── skills/               ← 7 individual skills
│   ├── 02-content-social/         ← @mad-scientist/content-social
│   │   └── skills/               ← 15 individual skills
│   └── ...
├── pnpm-workspace.yaml            ← workspace config
└── package.json                   ← root meta-package
```

## Publishing (for maintainers)

```bash
# Publish each package independently
cd packages/01-real-estate && npm publish --access public
cd packages/02-content-social && npm publish --access public
# etc.
```

---

## License

Proprietary — © 2026 Mad Scientist LLC. All rights reserved.
