#!/bin/bash
# Setup script for beautiful-websites skill
# Run this once to install all dependencies

set -e

echo "🔧 Beautiful Websites Setup"
echo "============================"
echo ""

# Check Node.js version
echo "1. Checking Node.js version..."
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js 18+ required. Current: $(node --version)"
    exit 1
fi
echo "✅ Node.js $(node --version)"
echo ""

# Install Playwright
echo "2. Installing Playwright..."
npm install playwright
echo "✅ Playwright installed"
echo ""

# Install Chromium
echo "3. Installing Chromium browser..."
npx playwright install chromium
echo "✅ Chromium installed"
echo ""

# Install system dependencies (Linux only)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "4. Installing Chromium system dependencies (Linux)..."
    npx playwright install-deps chromium
    echo "✅ System dependencies installed"
else
    echo "4. Skipping system dependencies (not Linux)"
fi
echo ""

# Install Vercel CLI
echo "5. Installing Vercel CLI globally..."
npm install -g vercel
echo "✅ Vercel CLI installed"
echo ""

# Check for .env
echo "6. Checking for .env file..."
if [ -f "../.env" ] || [ -f "../../.env" ]; then
    echo "✅ .env file found"
else
    echo "⚠️  No .env file found. Create one with:"
    echo "    APIFY_TOKEN=your_token_here"
    echo "    VERCEL_TOKEN=your_token_here  # optional for remote/SSH"
fi
echo ""

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Add APIFY_TOKEN to your .env file (get it from apify.com)"
echo "  2. If on remote/SSH, add VERCEL_TOKEN to .env (vercel.com/account/tokens)"
echo "  3. If on local machine, run: vercel login"
echo "  4. Test the pipeline with: 'Run the beautiful websites pipeline for nail salons in [YOUR_CITY]'"
