This file documents the expected API response structure when sending a YouTube video to OpusClip via Zapier MCP.

### Expected `tools/call` response for OpusClip:

```json
{
  "jsonrpc": "2.0",
  "result": {
    "status": "processing",
    "video_url": "https://youtube.com/watch?v=ABC123",
    "clip_url": "https://opusclip.com/clips/project-xyz123",
    "project_id": "project-xyz123",
    "message": "Video submitted for processing"
  },
  "id": 3
}
```

**Key fields to extract:**
- `result.clip_url` or `result.project_url` or `result.url` for the URL to the generated clips.
- `result.status` for the processing status.

### Error Response Example:

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32000,
    "message": "Invalid video URL",
    "data": { "field": "video_url", "value": "invalid-url" }
  },
  "id": 3
}
```
