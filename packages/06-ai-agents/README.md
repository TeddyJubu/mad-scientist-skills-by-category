# Ai Agents Skills
**Package:** `@mad-scientist/ai-agents` | **6 Skills** | Version 1.0.0

---

## What This Package Does

Agent operations, voice workflows, browser automation, and agent setup

## Skills In This Package

### 1. Agent Browser
**Folder:** `skills/agent-browser`

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

### 2. beautiful-websites
**Folder:** `skills/beautiful-websites`

Find local businesses with outdated websites, redesign them with premium single-file HTML sites, and deploy them to Vercel. Use when the user wants to generate proof-of-work redesigns for outreach, create portfolio pieces from real business sites, or run the full pipeline (scrape → qualify → redesign → deploy) for a specific niche and city. Triggers on phrases like "beautiful websites", "redesign local business sites", "run the pipeline for [niche] in [city]", or any request to scrape, qualify, redesign, and deploy business websites.

### 3. hr-hiring
**Folder:** `skills/hr-hiring`

HR workflow for creating optimized Upwork job posts, saving them to Notion, and evaluating applicant files from Google Drive. Use this skill when the user wants to hire for a new role, post a job on Upwork, or evaluate candidates for a job.

### 4. openai-whisper-api
**Folder:** `skills/openai-whisper-api`

Transcribe audio via OpenAI Audio Transcriptions API (Whisper).

### 5. rei-ai-zoom-processor
**Folder:** `skills/rei-ai-zoom-processor`

rei-ai-zoom-processor lets the user turn a Zoom or any video transcript into a structured Markdown document and PDF with bullet-point summaries, timestamps, and extracted resources, which is useful when they want to capture meeting notes, create training materials, or turn recorded conversations into searchable, shareable documents without manual summarization.

### 6. sarah-outbound-caller
**Folder:** `skills/sarah-outbound-caller`

sarah-outbound-caller lets the user deploy and manage Sarah, a VAPI-powered AI voice assistant that runs four distinct outbound call types — REI property acquisition, event reminders, community engagement, and agency outreach — with strict script isolation per campaign, which is useful when they want to automate calling campaigns, set up new call flows, or manage multi-vertical outreach without manual dialing.

## Agent Install

```bash
npm install @mad-scientist/ai-agents
```

Or copy the `skills/` directory into your agent skills root.

## License

Proprietary - (c) 2026 Mad Scientist LLC. All rights reserved.
