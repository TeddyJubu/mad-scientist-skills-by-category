# Mad Scientist Essential Skill Collections

A **pnpm monorepo** — 12 категорий skill packages, each publishable independently.

## Packages

| # | Package | Skills | Description |
|---|---------|--------|-------------|
| 01 | `@mad-scientist/real-estate` | 6 | SDAT, skip-trace, RentCast, Home Depot rehab |
| 02 | `@mad-scientist/content-social` | 14 | Blotato, YT thumbnails, opus-clip, image gen |
| 03 | `@mad-scientist/productivity` | 11 | Notion, file-delivery, agentmail, pdf-gen |
| 04 | `@mad-scientist/devops-infrastructure` | 6 | Vercel deploy, Traefik, systemd port reservation |
| 05 | `@mad-scientist/data-research` | 10 | Apify, Apollo, Brave search, Census, SEO audit |
| 06 | `@mad-scientist/ai-agents` | 19 | Bob, Sarah caller, OpenClaw, HR hiring, autonomous agents |
| 07 | `@mad-scientist/image-graphics` | 9 | GPT Image 2, HeyGen, Remotion, Nano Banana |
| 08 | `@mad-scientist/communication` | 1 | Discord |
| 09 | `@mad-scientist/media-lifestyle` | 11 | YouTube, Spotify, weather, healthcheck, gif-search |
| 10 | `@mad-scientist/openclaw-mcp` | 2 | MCP client & server, OpenClaw platform |
| 11 | `@mad-scientist/software-development` | 1 | Code review, debugging, TDD, planning skills |
| 12 | `@mad-scientist/tools` | 33 | MLOps, gaming, smart-home, feeds, github, ghl |

## Quick Start

```bash
# Clone the repo
git clone https://github.com/Mad-Scientist-sudo/Mad-scientist-essential-skill-collections.git
cd Mad-scientist-essential-skill-collections

# Install all packages
pnpm install

# Install a specific category only
cd packages/01-real-estate
pnpm install

# Link a package into Hermes
ln -s $(pwd)/skills ~/.hermes/skills/real-estate
```

## Structure

```
mad-scientist-essential-skill-collections/
├── packages/
│   ├── 01-real-estate/
│   │   ├── package.json       ← @mad-scientist/real-estate
│   │   └── skills/
│   │       ├── sdat-property-search/
│   │       ├── batchdata-skip-trace/
│   │       └── ...
│   ├── 02-content-social/
│   │   └── skills/
│   │       ├── gpt-image-2/
│   │       ├── yt-thumbnail-creator/
│   │       └── ...
│   └── ...
├── pnpm-workspace.yaml         ← tells pnpm to treat packages/* as workspace packages
├── package.json                ← root meta-package
└── README.md
```

## Publishing a Package

```bash
cd packages/01-real-estate
pnpm publish --access public
```

Each package is versioned independently and can be published to npm/GitHub Packages.
