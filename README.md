# Mad Scientist Collection of Skills by Category

<p align="center">
  <strong>A packaged monorepo of client-ready Mad Scientist agent skills, organized into 9 installable categories.</strong>
</p>

<p align="center">
  <img alt="Skills" src="https://img.shields.io/badge/skills-108-111827?style=for-the-badge">
  <img alt="Packages" src="https://img.shields.io/badge/packages-9-7c3aed?style=for-the-badge">
  <img alt="Workspace" src="https://img.shields.io/badge/workspace-pnpm-2563eb?style=for-the-badge">
  <img alt="Quality" src="https://img.shields.io/badge/quality-validated-059669?style=for-the-badge">
</p>

---

## What This Is

Mad Scientist Collection of Skills by Category is a pnpm workspace that turns a large agent skill library into independent category packages. This cleaned edition removes system/default skills that should not be presented as client giveaway skills.

## AI Agent Install Guide

Use this repository when your agent understands package categories or when you want to install one category at a time. Installing means making the `SKILL.md` folders available; do not run every skill script during install.

### 1. Clone

```bash
git clone https://github.com/TeddyJubu/mad-scientist-skills-by-category.git
cd mad-scientist-skills-by-category
```

### 2. Validate Before Loading

```bash
test "$(find packages -name SKILL.md | wc -l | tr -d ' ')" = "108"
```

### 3. Install One Category

```bash
export AGENT_SKILLS_ROOT="${AGENT_SKILLS_ROOT:-$HOME/.hermes/skills}"
mkdir -p "$AGENT_SKILLS_ROOT/mad-scientist-real-estate"
rsync -a --delete packages/01-real-estate/skills/ "$AGENT_SKILLS_ROOT/mad-scientist-real-estate/"
```

## Package Map

- `packages/01-real-estate` (6 skills): Property research, owner lookup, skip tracing, repair estimates, and real estate workflows
- `packages/02-content-social` (15 skills): YouTube, social posting, content repurposing, thumbnails, scripts, and marketing assets
- `packages/03-productivity` (3 skills): Notion, email, Google Workspace, document, and PDF workflows
- `packages/04-devops-infrastructure` (2 skills): Deployment, hosting, Docker, Vercel, and infrastructure workflows
- `packages/05-data-research` (14 skills): Web research, public data, search, scraping, SEO, and source collection
- `packages/06-ai-agents` (6 skills): Agent operations, voice workflows, browser automation, and agent setup
- `packages/07-image-graphics` (6 skills): Image generation, editing, design, avatars, video, and visual production
- `packages/09-media-lifestyle` (3 skills): Weather, audio, YouTube transcripts, and media utility workflows
- `packages/12-tools` (53 skills): General-purpose utilities across ML, GitHub, email, creative production, and operations

## Packages

| Package | Skills | Best for |
|---|---:|---|
| [`@mad-scientist/real-estate`](./packages/01-real-estate) | 6 | Property research, owner lookup, skip tracing, repair estimates, and real estate workflows |
| [`@mad-scientist/content-social`](./packages/02-content-social) | 15 | YouTube, social posting, content repurposing, thumbnails, scripts, and marketing assets |
| [`@mad-scientist/productivity`](./packages/03-productivity) | 3 | Notion, email, Google Workspace, document, and PDF workflows |
| [`@mad-scientist/devops-infrastructure`](./packages/04-devops-infrastructure) | 2 | Deployment, hosting, Docker, Vercel, and infrastructure workflows |
| [`@mad-scientist/data-research`](./packages/05-data-research) | 14 | Web research, public data, search, scraping, SEO, and source collection |
| [`@mad-scientist/ai-agents`](./packages/06-ai-agents) | 6 | Agent operations, voice workflows, browser automation, and agent setup |
| [`@mad-scientist/image-graphics`](./packages/07-image-graphics) | 6 | Image generation, editing, design, avatars, video, and visual production |
| [`@mad-scientist/media-lifestyle`](./packages/09-media-lifestyle) | 3 | Weather, audio, YouTube transcripts, and media utility workflows |
| [`@mad-scientist/tools`](./packages/12-tools) | 53 | General-purpose utilities across ML, GitHub, email, creative production, and operations |

Total: **108 skills across 9 packages**.

## Maintainer Notes

- Keep package counts aligned with `find packages -name SKILL.md`.
- Keep package-level `README.md` files short and operational.
- Keep secrets out of committed docs and scripts.
- Do not re-add system/default skills removed by the client cleanup pass.

## License

Proprietary - (c) 2026 Mad Scientist LLC. All rights reserved.
