# HeyGen Research Notes

Research gathered while creating "How To Create a HeyGen Account" guide (2026-05-17). These are session-specific domain facts — not a full product manual.

## What Is HeyGen

AI video generator that creates realistic talking avatar videos from text, photos, or scripts. No camera, no editing software, no production crew needed.

**Use cases:** Real estate agent videos, course creators, YouTube content, product demos, training/onboarding, marketing, localization/translation.

## Signup Flow

**URL:** `https://app.heygen.com/signup` → redirects to `https://auth.heygen.com/signup`

**Sign-up methods:**
- Google (fastest)
- Apple
- SSO (enterprise/school accounts)
- Email (sends a magic link; "Use password instead" link available)

**Gotcha:** The email field has a Cloudflare challenge widget. Even when the field appears empty, the page may be waiting for Cloudflare verification before the Send Link button enables.

## Free Plan (what you get without paying)

- 3 videos per month
- Videos up to 1 minute
- 720p export
- Standard processing speed
- 500+ Stock Digital Twins
- Access to Avatar IV and Video Agent
- 1 Custom Digital Twin
- 30+ languages
- Video sharing & commenting
- **Has watermark** on exports

## Paid Plans (as of 2026-05)

| Plan | Price | Credits | Max Length | Export | Watermark |
|------|-------|---------|------------|--------|-----------|
| Free | $0/mo | 3/month | 1 min | 720p | Yes |
| Creator | $29/mo | 600 | 30 min | 1080p | No |
| Pro | $49/mo | 1,000 | 30 min | 4K | No |
| Business | $149/mo | 1,500 | 60 min | 4K | No |
| Enterprise | Contact | Unlimited | No max | 4K | No |

**Creator and up:** Voice Cloning (unlimited on Creator+), 175+ languages and dialects, credit rollovers.

**Charles uses:** Pro plan ($49/mo) — 4K export and 1,000 credits.

## Charles's HeyGen IDs

- **Avatar ID:** `88c37101a7b34c7da97532c24ad6d135`
- **Voice ID:** `16e17a9c75554c68b586c2ac343619f7`
- **Workflow:** Transcribe (Whisper) → Rewrite (AI) → HeyGen

## Avatar Types

1. **Photo Avatar** — upload a headshot photo, turns it into a talking avatar
2. **Public/Stock Avatar** — pre-made diverse professional avatars
3. **Digital Twin** — film a short video of yourself to clone yourself

## Key Features

- **Video Agent:** type an idea, get a share-ready video
- **Avatar IV:** extended avatar video generation
- **Translate:** dub videos into 175+ languages with lip-sync
- **AI Studio:** text-based video editor (like editing a document)
- **Voice Cloning:** upload recording for personalized voice

## Common Issues

| Problem | Fix |
|---------|-----|
| No email link arrived | Check spam; verify email was typed correctly |
| Cloudflare challenge | Normal — complete the image puzzle (e.g., "click all squares with cars") |
| Watermark on video | Upgrade to Creator ($29/mo) or higher |
| Avatar looks fake/creepy | Use high-quality headshot with good lighting, direct eye contact, avoid sunglasses |
| No login option visible | Click "Sign in with email" → option toggles the email field |

## Official Links

- Homepage: `https://www.heygen.com`
- Signup: `https://app.heygen.com/signup`
- Pricing: `https://www.heygen.com/pricing`
- API pricing: `https://www.heygen.com/api-pricing`

## Notes

- HeyGen is browser-based — no download required
- Works on Mac, Windows, Chromebook
- Videos stored on HeyGen's servers
- Check Terms of Service for commercial use rights
- Has an API for developers and automation (Charles uses this)