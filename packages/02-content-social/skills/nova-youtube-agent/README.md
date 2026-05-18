# Nova — YouTube Growth Agent for OpenClaw

Nova is an AI agent that handles your YouTube content strategy end-to-end.
Competitor research. Channel analysis. Video ideas. Scripts. Performance tracking. Feedback loop.

Built for [OpenClaw](https://openclaw.ai). Self-installs in under 5 minutes.

---

## What It Does

🔍 **Competitor Scan**
Finds outlier videos (2x+ avg) across your competitor channels and extracts what's working

📊 **Channel Analysis**
Analyzes your own videos to find patterns in what performs and what doesn't

💡 **Idea Generation**
Interviews you first, then generates research-backed ideas grounded in real experience

📝 **Script Writing**
Full scripts in your voice with a complete SEO package (title variants, description, tags, chapters, thumbnail)

📈 **Performance Logging**
Tracks how each video does after publishing

🔄 **Feedback Loop**
Logs every approval and rejection with reasons - Nova never repeats a rejected angle

🧠 **Learning Loop**
Reads all memory files before every session - gets smarter the longer you use it

---

## Requirements

- [OpenClaw](https://openclaw.ai) installed
- Any supported AI model (Claude, GPT-4o, Gemini - all work)
- A YouTube channel (any size, any niche)

---

## Installation

Just tell your OpenClaw agent:

```
Install Nova
```

OpenClaw will detect the skill and Nova will run onboarding automatically.

---

## First Run - Onboarding

First time you run Nova, she'll ask you 10 questions:

- Your name and channel name
- Channel URL
- Your niche (one sentence)
- Your target audience
- Your subscriber goal + deadline
- Current subscriber count
- How you naturally talk (voice description)
- 5-10 competitor channels to monitor
- What to avoid (flops, off-brand formats)
- Your top 2-3 videos (optional - for voice calibration)

Takes about 5 minutes. Nova writes your answers to `config.md` automatically. You never do this again.

---

## Usage

After setup, just talk to her naturally:

```
Nova, scan my competitors for what's working this week

Nova, I want to make a video - interview me and let's find an idea

Nova, write a full script for [idea]

Nova, my last video got 4,200 views - log the performance

Nova, show me the feedback loop - what patterns have you noticed?
```

---

## Memory System

Nova keeps a `memory/` folder with:

- `approved-ideas.md` - every idea you said yes to
- `rejected-ideas.md` - every idea you rejected + why
- `performance-log.md` - every video's stats after publishing
- `competitor-scans.md` - history of niche research
- `voice-examples.md` - your voice patterns and phrases
- `channel-analysis.md` - channel performance analysis history

Before every session, Nova reads all of these. She never repeats a rejected angle. She weights suggestions toward what's actually performed on your channel. The longer you use her, the better the ideas.

---

## File Structure

```
nova-youtube-agent/
├── README.md          ← You're reading this
├── SKILL.md           ← Nova's full instructions (all 7 systems)
├── config.md          ← Auto-created during onboarding
├── example-config.md  ← Real example for reference
└── memory/
    ├── approved-ideas.md       ← Auto-populated
    ├── rejected-ideas.md       ← Auto-populated
    ├── performance-log.md      ← Auto-populated
    ├── competitor-scans.md     ← Auto-populated
    ├── channel-analysis.md     ← Auto-populated
    └── voice-examples.md       ← Auto-populated
```

Note: `config.md` and all `memory/` files are created automatically. Your personal data never leaves your machine.

---

## Customization

- To change your channel details: edit `config.md`
- To change how Nova behaves: edit `SKILL.md` (plain English, no code)
- To reset and start fresh: delete `config.md` and all `memory/` files, then run "Install Nova" again

---

## FAQ

**Does this work for any niche?**
Yes. Onboarding calibrates Nova to your niche, voice, and competitors.

**Do I need to be technical?**
No. If you can install OpenClaw and answer 10 questions, you're set.

**Does Nova post videos automatically?**
No. Nova handles strategy and scripts. Filming and publishing stays with you.

**Is my data private?**
Yes. `config.md` and all `memory/` files stay on your machine.

**What model works best?**
Claude Sonnet or GPT-4o. Both work well for this.

---

## Credits

Built by [Sharbel](https://youtube.com/@sharbel) - founder, AI builder, creator.

Video: [The AI Agent That Got Me YouTube Monetized](https://youtu.be/MwGbZkYYHVw)

If this helps you, star the repo. More agent builds on the channel.

---

## License

MIT - free to use, modify, and share.
