# Image Editing API Diagnostics — May 2026 Session

## OpenAI gpt-image-2 edit attempt (FAILED)

**What was tried:**
- `client.images.edit(model="gpt-image-2", image=img_bytes, ...)` via Python SDK
- `/images/edits` REST endpoint with gpt-image-2 payload

**Error:**
```
openai.BadRequestError: Error code: 400 - 
{'error': {'message': "Unknown parameter: 'image'.", 'type': 'invalid_request_error', 'param': 'image', 'code': 'unknown_parameter'}}
```

**Root cause:** OpenAI's `/images/edits` endpoint only supports `dall-e-2`. gpt-image-2 has no edit capability in the API.

**Curl attempt with large base64 payload (FAILED):**
- OSError: [Errno 7] Argument list too long: 'curl'
- Fix: Use Python urllib instead of subprocess with curl for payloads > ~100KB

---

## Gemini image edit attempt via Python SDK (FAILED until fixed)

**Initial error:** `ModuleNotFoundError: No module named 'google.generativeai'`

**Diagnosis:**
```bash
# The correct import is google.genai (NOT google.generativeai)
python3 -c "import sys; sys.path.insert(0,'/root/.hermes/hermes-agent/venv/lib/python3.11/site-packages'); import google.genai; print('OK')"
# Output: OK

# Confirm model name
python3 -c "
import sys; sys.path.insert(0,'/root/.hermes/hermes-agent/venv/lib/python3.11/site-packages')
from google.genai import models
print([m for m in dir(models) if 'generate' in m.lower()])
# Output: ['generate_content', 'generate_images', ...]
"
```

**Working curl pattern (used in session):**
```bash
API_KEY=$(grep '^GOOGLE_API_KEY=' /root/.hermes/.env | cut -d= -f2)
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=${API_KEY}" \
  -H 'Content-Type: application/json' \
  -d @/tmp/payload.json \
  -o /tmp/response.json
```

**Working Python urllib pattern (preferred for large payloads):**
```python
import urllib.request, json
payload = {"contents": [{"parts": [{"inline_data": {...}}, {"text": "prompt"}]}]}
data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={"Authorization": f"Bearer {api_key}"}, method="POST")
with urllib.request.urlopen(req, timeout=180) as resp:
    body = resp.read()
```

---

## PIL targeted edit (WORKED)

For date-only changes on thumbnails, PIL is the reliable fallback:
- Original image: `/root/.hermes/image_cache/img_eae64c391347.jpg` (1280x714)
- Font used: `/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf`
- Text position found via `ImageStat` scanning of high-contrast bands in bottom 25%
