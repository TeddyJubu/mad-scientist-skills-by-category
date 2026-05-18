---
name: opus-blotato-video-poster
description: Takes a YouTube video URL, generates short viral clips via Opus Clip, selects the top 2 clips by virality score, posts clip #1 immediately to all connected Blotato social media accounts, and schedules clip #2 for 4 hours later. Use this skill when the user wants to post a YouTube video to social media, clip a YouTube video and distribute it, or run the Opus Clip + Blotato workflow.
---

# Opus Blotato Video Poster

Automates viral clip generation and social media distribution:

1. Submit YouTube URL to **Opus Clip** for short-form clip generation
2. Select **top 2 clips** by virality score
3. Post **clip #1** immediately to all connected Blotato accounts
4. Schedule **clip #2** for **4 hours later**

## Why This Workflow

Blotato cannot read metadata from YouTube URLs directly — it requires `.mp4` files. Opus Clip provides CDN-hosted video URLs that Blotato accepts.

## Credentials

- **Blotato API Key**: `blt_C4H/l9gOlOm/+pt4wXQqWiJ9VBMl3n/FEW17OKovrtw=`
- **Zapier MCP**: Requires configured MCP server for Opus Clip integration

## Connected Platforms

| Platform | Account ID | Target Type | Notes |
|----------|-----------|-------------|-------|
| Facebook | 15082 | page | Page ID: 491473457567789 |
| YouTube | 21244 | channel | Charles Blair |
| Instagram | 24117 | feed | @realmadscientist_ |
| TikTok | 23181 | video | @realmadscientist |
| Twitter/X | 10251 | tweet | @madscientistcb |

## Running the Workflow

Always run as a **background process** (Opus Clip takes 10–20 minutes):

```bash
nohup python3.11 scripts/opus_blotato_workflow.py "<youtube_url>" > workflow.log 2>&1 &
echo "PID: $!"
```

Monitor progress:

```bash
tail -f workflow.log
```

## Implementation Notes

### Opus Clip MCP Integration

The script requires a configured Zapier MCP server with these tools:

- `opusclip_submit` — Submit YouTube URL, returns `projectId`
- `opusclip_get_transcript_of_clips` — Poll for completed clips (reliable method)
- `opusclip_get_your_video_with_captions` — Get direct MP4 download URL

**Clip ID Format**: `PROJECT_ID.CLIP_SHORT_ID` (e.g., `P3022413qNyO.7vyo4D2QPT`)

**API Quirk**: When calling `opusclip_get_your_video_with_captions`, prefix the short ID with `c.` (e.g., `c.7vyo4D2QPT`)

### Polling Strategy

- **Max attempts**: 50 × 30 seconds = 25 minutes
- **Method**: `opusclip_get_transcript_of_clips` (not `opusclip_get_clips` — unreliable)
- **Why**: Opus Clip processing is slow; avoid timeouts by using `nohup`

### Blotato Platform Requirements

Each platform requires specific payload fields:

**Facebook**:
```json
{"target": {"pageId": "491473457567789"}}
```

**YouTube**:
```json
{
  "target": {
    "title": "Viral Clip: ...",
    "privacyStatus": "public",
    "shouldNotifySubscribers": true
  }
}
```

**TikTok**:
```json
{
  "target": {
    "privacyLevel": "public",
    "disabledComments": false,
    "disabledDuet": false,
    "disabledStitch": false,
    "isBrandedContent": false,
    "isYourBrand": false,
    "isAiGenerated": false
  }
}
```

**Instagram/Twitter**: Only `targetType` required

### Scheduling

Schedule clip #2 by adding `scheduledTime` to the root of the request body:

```json
{
  "post": { ... },
  "scheduledTime": "2026-03-09T22:00:00Z"
}
```

Compute 4 hours from now in Python:

```python
from datetime import datetime, timezone, timedelta
scheduled_dt = datetime.now(timezone.utc) + timedelta(hours=4)
scheduled_iso = scheduled_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
```

## Troubleshooting

**"Failed to read media metadata"** → Use Opus Clip CDN URLs, not YouTube URLs

**Polling times out** → Increase `max_attempts` or run with `nohup`

**Missing clips** → Ensure `opusclip_get_transcript_of_clips` is used (not `opusclip_get_clips`)

**Platform-specific errors** → Check required fields in Blotato API docs
