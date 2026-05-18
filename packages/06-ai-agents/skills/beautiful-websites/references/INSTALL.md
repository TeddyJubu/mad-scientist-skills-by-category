# Installation Guide

## Prerequisites

- **Node.js 18+** (check with `node --version`)
- **OpenClaw** installed and running

---

## Quick Setup

Run the setup script:

```bash
cd ~/.openclaw/workspace/skills/beautiful-websites/scripts
./setup.sh
```

This will:
1. Check Node.js version
2. Install Playwright
3. Install Chromium browser
4. Install Chromium system dependencies (Linux only)
5. Install Vercel CLI globally
6. Check for .env file

---

## Manual Setup

If you prefer to install manually:

### 1. Install Playwright

```bash
npm install playwright
npx playwright install chromium
```

**Linux only:**
```bash
npx playwright install-deps chromium
```

### 2. Install Vercel CLI

```bash
npm install -g vercel
```

### 3. Configure API Keys

Create a `.env` file in your workspace root (`~/.openclaw/workspace/.env`) with:

```env
APIFY_TOKEN=your_token_here
VERCEL_TOKEN=your_token_here  # optional for local, required for remote/SSH
```

**Get your API keys:**

- **APIFY_TOKEN:** apify.com → Settings → Integrations
- **VERCEL_TOKEN:** vercel.com/account/tokens (remote/SSH only)

### 4. Authenticate Vercel (local only)

If you're on a local machine (not remote/SSH), run:

```bash
vercel login
```

This opens a browser for OAuth authentication. Skip this if you added `VERCEL_TOKEN` to `.env`.

---

## Verify Installation

Test that everything works:

```bash
# Check Node.js version (must be 18+)
node --version

# Check Playwright
npx playwright --version

# Check Vercel CLI
vercel --version

# Test screenshot script
cd ~/.openclaw/workspace/skills/beautiful-websites/scripts
node screenshot.js --url https://example.com --out test.png
```

If the screenshot test succeeds, you'll see `test.png` in the scripts directory.

---

## Workspace Structure

After installation, your workspace should look like:

```
~/.openclaw/workspace/
├── .env (APIFY_TOKEN, VERCEL_TOKEN)
├── skills/
│   └── beautiful-websites/
│       ├── SKILL.md
│       ├── scripts/
│       │   ├── setup.sh
│       │   └── screenshot.js
│       └── references/
│           ├── WORKFLOW.md
│           ├── INSTALL.md
│           └── website_prompt_v1.md
```

---

## First Run

Once installed, test the pipeline with:

```
Run the beautiful websites pipeline for nail salons in [YOUR_CITY]
```

Replace `[YOUR_CITY]` with a real city (e.g. "Austin TX", "Portland OR", "Melbourne").

---

## Troubleshooting

### Node.js version too old

**Error:** `node --version` shows 16.x or older

**Fix:** Upgrade Node.js:

```bash
# On Hostinger VPS (via Homebrew)
brew upgrade node

# Or install NVM and switch to Node 20
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
nvm use 20
```

### Playwright fails on Linux

**Error:** `Error: Failed to launch chromium because executable doesn't exist`

**Fix:** Install system dependencies:

```bash
npx playwright install-deps chromium
```

### Vercel deploy fails with "No credentials found"

**Error:** `Error: No credentials found`

**Fix (local):** Run `vercel login`

**Fix (remote/SSH):** Add `VERCEL_TOKEN` to `.env`

### Apify scrape fails with 401

**Error:** `Error: Request failed with status code 401`

**Fix:** Check that `APIFY_TOKEN` is set correctly in `.env`

### Screenshot returns blank page

**Cause:** Some sites load content dynamically with JavaScript

**Fix:** The screenshot script already handles this with multiple scroll passes. If it still fails, the site may be blocking headless browsers or using heavy client-side rendering.

---

## Updating Dependencies

To update Playwright or Vercel CLI:

```bash
# Update Playwright
npm update playwright
npx playwright install chromium

# Update Vercel CLI
npm update -g vercel
```

---

## Uninstall

To remove the skill:

```bash
rm -rf ~/.openclaw/workspace/skills/beautiful-websites
```

To remove global dependencies:

```bash
npm uninstall -g vercel
npm uninstall playwright
```

---

## Support

For issues or questions, reference:

- **SKILL.md** — main skill documentation
- **WORKFLOW.md** — detailed pipeline workflow
- **OpenClaw docs** — docs.openclaw.ai
