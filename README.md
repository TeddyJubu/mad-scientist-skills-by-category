# Mad Scientist Collection of Skills by Category

<p align="center">
  <strong>A packaged monorepo of Mad Scientist agent skills, organized into 12 installable categories.</strong>
</p>

<p align="center">
  <img alt="Skills" src="https://img.shields.io/badge/skills-204-111827?style=for-the-badge">
  <img alt="Packages" src="https://img.shields.io/badge/packages-12-7c3aed?style=for-the-badge">
  <img alt="Workspace" src="https://img.shields.io/badge/workspace-pnpm-2563eb?style=for-the-badge">
  <img alt="Quality" src="https://img.shields.io/badge/quality-validated-059669?style=for-the-badge">
</p>

---

## What This Is

Mad Scientist Collection of Skills by Category is a pnpm workspace that turns a large agent skill library into 12 independent packages. Each package contains a focused set of `SKILL.md` capabilities for Hermes, OpenClaw, Claude-style skill loaders, or any agent runtime that can discover skill folders.

Use the whole monorepo when you want the complete operating library. Use an individual package when you only need one business lane: real estate, content, productivity, devops, research, agents, media, software development, or broad tools.

## AI Agent Install Guide

Use this repository when your agent understands package categories or when you want to install one category at a time. Installing means making the `SKILL.md` folders available; do not run every skill script during install.

### 1. Clone

```bash
git clone https://github.com/TeddyJubu/mad-scientist-skills-by-category.git
cd mad-scientist-skills-by-category
```

### 2. Validate Before Loading

```bash
test "$(find packages -name SKILL.md | wc -l | tr -d ' ')" = "204"

python3 - <<'PY'
from pathlib import Path
import re
names = {}
bad = []
for path in Path("packages").rglob("SKILL.md"):
    text = path.read_text(errors="replace")
    name = re.search(r"^name:\s*(.+)", text, re.M)
    desc = re.search(r"^description:\s*(.+)", text, re.M)
    if not text.startswith("---") or not name or not desc:
        bad.append(str(path))
        continue
    key = name.group(1).strip().lower()
    names.setdefault(key, []).append(str(path))
dupes = {key: paths for key, paths in names.items() if len(paths) > 1}
if bad or dupes:
    raise SystemExit(f"Invalid files: {bad}\nDuplicate names: {dupes}")
print("Validated 204 skills")
PY
```

### 3. Install One Category

Set `AGENT_SKILLS_ROOT` to the folder your agent scans. This example installs only Real Estate.

```bash
export AGENT_SKILLS_ROOT="${AGENT_SKILLS_ROOT:-$HOME/.hermes/skills}"
mkdir -p "$AGENT_SKILLS_ROOT/mad-scientist-real-estate"

rsync -a --delete \
  --exclude ".env" \
  --exclude "*.env" \
  --exclude "__pycache__" \
  --exclude "*.pyc" \
  packages/01-real-estate/skills/ "$AGENT_SKILLS_ROOT/mad-scientist-real-estate/"
```

### 4. Install All Categories Into A Flat Skill Root

Use this when your runtime expects one directory containing skill folders.

```bash
export AGENT_SKILLS_ROOT="${AGENT_SKILLS_ROOT:-$HOME/.hermes/skills}"
mkdir -p "$AGENT_SKILLS_ROOT/mad-scientist-skills"

python3 - <<'PY'
from pathlib import Path
import os, re, shutil

root = Path(os.environ.get("AGENT_SKILLS_ROOT", str(Path.home() / ".hermes" / "skills"))) / "mad-scientist-skills"
root.mkdir(parents=True, exist_ok=True)

def slugify(value):
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return re.sub(r"-+", "-", value).strip("-")

for skill_file in Path("packages").rglob("SKILL.md"):
    text = skill_file.read_text(errors="replace")
    name = re.search(r"^name:\s*(.+)", text, re.M)
    if not name:
        raise SystemExit(f"Missing name in {skill_file}")
    slug = slugify(name.group(1).strip().strip("'\""))
    dest = root / slug
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(
        skill_file.parent,
        dest,
        ignore=shutil.ignore_patterns(".env", "*.env", "__pycache__", "*.pyc", "*.log", ".DS_Store"),
    )
print(f"Installed skills into {root}")
PY
```

### 5. Load Behavior For Agents

- For category-aware runtimes, scan `packages/<category>/skills/**/SKILL.md`.
- For flat skill-root runtimes, use the install-all command above or use [`mad-scientist-skill-monorepo`](https://github.com/TeddyJubu/mad-scientist-skill-monorepo).
- Use frontmatter `name` as the skill ID.
- Read a skill's local support files only after selecting that skill.
- Keep live credentials outside git in local `.env` files.

## Package Map

```text
Mad Scientist Collection of Skills by Category
├── packages/01-real-estate             property lookup, skip tracing, repairs
├── packages/02-content-social          YouTube, thumbnails, social posting
├── packages/03-productivity            Notion, email, files, docs, PDFs
├── packages/04-devops-infrastructure   Docker, Traefik, Vercel, systemd
├── packages/05-data-research           Apify, Census, Apollo, Brave, SEO
├── packages/06-ai-agents               agent workflows, voice, OpenClaw
├── packages/07-image-graphics          image generation, editing, video
├── packages/08-communication           Discord control
├── packages/09-media-lifestyle         weather, TTS, audio, video, Spotify
├── packages/10-openclaw-mcp            OpenClaw and MCP operations
├── packages/11-software-development    review, debugging, TDD, planning
└── packages/12-tools                   broad utility bench
```

## Packages

| Package | Skills | Best for |
|---|---:|---|
| [`@mad-scientist/real-estate`](./packages/01-real-estate) | 6 | Property research, owner lookup, skip tracing, repair estimates |
| [`@mad-scientist/content-social`](./packages/02-content-social) | 15 | Thumbnails, video clipping, posting, image generation, copywriting |
| [`@mad-scientist/productivity`](./packages/03-productivity) | 9 | Notion, email, Google Workspace, PDFs, file delivery |
| [`@mad-scientist/devops-infrastructure`](./packages/04-devops-infrastructure) | 6 | Deployments, servers, domains, ports, reverse proxying |
| [`@mad-scientist/data-research`](./packages/05-data-research) | 17 | Business contacts, scraping, Census data, SEO, research workflows |
| [`@mad-scientist/ai-agents`](./packages/06-ai-agents) | 21 | Agent operations, outbound voice, OpenClaw, browser automation |
| [`@mad-scientist/image-graphics`](./packages/07-image-graphics) | 8 | Image generation, editing, avatars, Remotion, design |
| [`@mad-scientist/communication`](./packages/08-communication) | 1 | Discord bot control |
| [`@mad-scientist/media-lifestyle`](./packages/09-media-lifestyle) | 10 | TTS, YouTube, Spotify, weather, video frames, health tracking |
| [`@mad-scientist/openclaw-mcp`](./packages/10-openclaw-mcp) | 3 | OpenClaw platform management and MCP configuration |
| [`@mad-scientist/software-development`](./packages/11-software-development) | 12 | Code review, debugging, TDD, planning, subagent workflows |
| [`@mad-scientist/tools`](./packages/12-tools) | 96 | MLOps, GitHub, smart home, CRM, creative, productivity, red teaming |

Total: **204 skills across 12 packages**.

## How It Works

Each package is a standalone folder with metadata and a `skills/` directory:

```text
packages/01-real-estate/
├── package.json
├── README.md
└── skills/
    ├── rentcast-property-report/
    │   └── SKILL.md
    ├── homedepot-repair-estimator/
    │   ├── SKILL.md
    │   ├── scripts/
    │   └── references/
    └── ...
```

Each skill is intentionally simple to inspect:

```text
skill-name/
├── SKILL.md       main instructions and metadata
├── scripts/       optional helpers
├── references/    API notes, examples, operating guides
├── templates/     reusable prompts, documents, or code
├── assets/        supporting assets
└── .env           local secrets only, never committed
```

## Developer Quick Start

```bash
git clone https://github.com/TeddyJubu/mad-scientist-skills-by-category.git
cd mad-scientist-skills-by-category
pnpm install
pnpm list
```

Install or inspect one category:

```bash
cd packages/01-real-estate
pnpm install
find skills -name SKILL.md
```

## Skill Metadata

Every `SKILL.md` should start with YAML frontmatter:

```yaml
---
name: example-skill
description: One clear sentence describing when and why to use this skill.
---
```

The `name` field should be stable, unique, and machine-friendly. Duplicate skill names make runtime discovery ambiguous.

## Secrets

Never commit live credentials. Store secrets locally:

```bash
~/.hermes/skills/<skill>/.env
~/.hermes/.env
```

Committed examples should use placeholders only:

```bash
API_KEY=your_api_key_here
CHARLES_HOST_IP=your_server_ip_here
```

## Quality Gates

The current collection has been checked for:

| Check | Status |
|---|---|
| `SKILL.md` frontmatter present | Passed |
| Unique skill names | Passed |
| JSON validity | Passed |
| Python syntax compilation | Passed |
| JavaScript syntax check | Passed |
| Shell syntax check | Passed |
| Bundled pytest suite | `109 passed, 8 skipped` |
| Obvious committed secret patterns | Clean, except masked examples |

## Maintainer Notes

- Keep package counts in this README aligned with `find packages -name SKILL.md`.
- Keep package-level `README.md` files short and operational.
- Keep secrets out of committed docs and scripts.
- Prefer environment variables for host-specific values.
- Remove generated bytecode and cache folders before committing.
- Use small, package-scoped changes so downstream skill loaders stay stable.

## License

Proprietary - (c) 2026 Mad Scientist LLC. All rights reserved.
