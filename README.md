# Mad Scientist Collection of Skills by Category

<p align="center">
  <strong>A packaged monorepo of Mad Scientist agent skills, organized into cleaned installable categories.</strong>
</p>

<p align="center">
  <img alt="Skills" src="https://img.shields.io/badge/skills-145-111827?style=for-the-badge">
  <img alt="Packages" src="https://img.shields.io/badge/packages-10-7c3aed?style=for-the-badge">
  <img alt="Workspace" src="https://img.shields.io/badge/workspace-pnpm-2563eb?style=for-the-badge">
  <img alt="Quality" src="https://img.shields.io/badge/quality-validated-059669?style=for-the-badge">
</p>

---

## What This Is

Mad Scientist Collection of Skills by Category is a pnpm workspace that organizes agent skills into independent packages. Each package contains a focused set of `SKILL.md` capabilities for Hermes, OpenClaw, Claude-style skill loaders, or any agent runtime that can discover skill folders.

This version removes client-excluded system/default skills and keeps the remaining skill categories intended for distribution.

## AI Agent Install Guide

Use this repository when your agent understands package categories or when you want to install one category at a time. Installing means making the `SKILL.md` folders available; do not run every skill script during install.

### 1. Clone

```bash
git clone https://github.com/Mad-Scientist-sudo/Mad-scientist-skills-by-catagory.git
cd Mad-scientist-skills-by-catagory
```

### 2. Validate Before Loading

```bash
test "$(find packages -name SKILL.md | wc -l | tr -d ' ')" = "145"

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
print("Validated 145 skills")
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

## Package Map

```text
Mad Scientist Collection of Skills by Category
├── packages/01-real-estate             property lookup, skip tracing, repairs
├── packages/02-content-social          YouTube, thumbnails, social posting
├── packages/03-productivity            cleaned productivity skills
├── packages/04-devops-infrastructure   cleaned deployment and infrastructure skills
├── packages/05-data-research           cleaned data and research workflows
├── packages/06-ai-agents               cleaned agent workflows
├── packages/07-image-graphics          cleaned image, graphics, and video skills
├── packages/08-communication           communication skills
├── packages/09-media-lifestyle         cleaned media and lifestyle skills
└── packages/12-tools                   cleaned broad utility bench
```

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

## Maintainer Notes

- Keep package counts in this README aligned with `find packages -name SKILL.md`.
- Keep package-level `README.md` files short and operational.
- Keep secrets out of committed docs and scripts.
- Prefer environment variables for host-specific values.
- Remove generated bytecode and cache folders before committing.
- Use small, package-scoped changes so downstream skill loaders stay stable.

## License

Proprietary - (c) 2026 Mad Scientist LLC. All rights reserved.
