# Supadata Transcript Modes

## Mode Comparison

| Mode | Behavior | Use Case |
|------|----------|----------|
| `native` | Only fetch existing transcript from platform | When you know the video has captions and want to avoid AI costs |
| `auto` | Try native first, fallback to AI if unavailable | Default — best balance of speed and reliability |
| `generate` | Always use AI to generate transcript | When native quality is poor or you need consistent formatting |

## When to Use Each Mode

### `native` (Platform Transcript Only)

**Use when:**
- Video definitely has captions/subtitles
- You want fastest response time
- You want to avoid AI generation costs
- You're okay with transcript being unavailable if no captions exist

**Fails when:**
- Video has no captions
- Captions are auto-generated but not available via API
- Platform doesn't support transcript export

**Example:**
```bash
bash ~/.openclaw/workspace/skills/supadata-transcript/scripts/transcribe.sh \
  "https://youtu.be/dQw4w9WgXcQ" \
  --mode native
```

### `auto` (Try Native, Fallback to AI)

**Use when:**
- You want transcript regardless of whether captions exist
- You want to minimize AI usage (only when necessary)
- You're transcribing mixed content (some with captions, some without)

**Behavior:**
1. First, checks if native transcript exists
2. If yes: returns platform transcript immediately
3. If no: generates transcript using AI

**Example:**
```bash
bash ~/.openclaw/workspace/skills/supadata-transcript/scripts/transcribe.sh \
  "https://youtu.be/dQw4w9WgXcQ" \
  --mode auto
```

### `generate` (Always Use AI)

**Use when:**
- Native transcripts are low quality (auto-generated captions with errors)
- You need consistent formatting across all videos
- You want to transcribe audio-only content or file URLs
- Platform captions are in wrong language or poorly formatted

**Always generates transcript from scratch, even if captions exist.**

**Example:**
```bash
bash ~/.openclaw/workspace/skills/supadata-transcript/scripts/transcribe.sh \
  "https://youtu.be/dQw4w9WgXcQ" \
  --mode generate
```

## Language Support

### Available Languages

Supadata supports [150+ languages](https://supadata.ai/documentation/youtube/supported-language-codes) for transcript fetch and AI generation.

**Common language codes (ISO 639-1):**
- `en` — English
- `es` — Spanish
- `zh` — Chinese (Simplified)
- `zh-TW` — Chinese (Traditional)
- `ja` — Japanese
- `ko` — Korean
- `fr` — French
- `de` — German
- `it` — Italian
- `pt` — Portuguese
- `ru` — Russian
- `ar` — Arabic
- `hi` — Hindi

### Language Behavior by Mode

| Mode | Language Handling |
|------|-------------------|
| `native` | Returns requested language if available; fails if not |
| `auto` | Returns native transcript in requested language if available; generates in requested language if native unavailable |
| `generate` | Always generates transcript in requested language |

**Example (Spanish transcript):**
```bash
bash ~/.openclaw/workspace/skills/supadata-transcript/scripts/transcribe.sh \
  "https://youtu.be/dQw4w9WgXcQ" \
  --lang es \
  --mode auto
```

## Cost Optimization Tips

1. **Use `native` mode for known captioned videos** to avoid AI costs
2. **Use `auto` mode for mixed content** to only pay for AI when needed
3. **Batch process videos** with similar characteristics using the same mode
4. **Check `availableLangs` first** before requesting specific language with `generate` mode

## File URLs

When transcribing file URLs (MP3, MP4, WAV, etc.), mode is **always `generate`** regardless of what you specify.

**Example:**
```bash
bash ~/.openclaw/workspace/skills/supadata-transcript/scripts/transcribe.sh \
  "https://example.com/audio.mp3" \
  --mode native  # Ignored — will use 'generate' automatically
```

## Performance Comparison

| Mode | Typical Response Time | Cost |
|------|----------------------|------|
| `native` | ~1-3 seconds | Free (platform transcript) |
| `auto` (native available) | ~1-3 seconds | Free |
| `auto` (fallback to AI) | ~30-120 seconds | AI generation cost |
| `generate` | ~30-120 seconds | AI generation cost |

*Large videos may require async processing (job ID returned), adding 1-5 minutes.*
