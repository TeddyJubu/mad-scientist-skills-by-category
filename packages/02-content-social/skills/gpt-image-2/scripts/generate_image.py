#!/usr/bin/env python3
from __future__ import annotations

# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "openai>=2.0.0",
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
# ]
# ///

import os
from pathlib import Path

# Auto-load env vars from /root/.hermes/.env if present (uv run doesn't inherit shell env)
_env_path = Path("/root/.hermes/.env")
if _env_path.exists():
    for _line in _env_path.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _key, _val = _line.split("=", 1)
            os.environ.setdefault(_key.strip(), _val.strip())

"""Generate an image with OpenAI GPT Image 2.

Calls OpenAI's Images API directly using OPENAI_API_KEY (no FAL gateway).
On any OpenAI failure, falls back to Google Gemini 3.1 Flash Image.

Prints `provider=openai` or `provider=gemini` on the last stdout line so
callers can tell which model was actually used.
"""

import argparse
import base64
import sys

PRIMARY_MODEL = "gpt-image-2"
FALLBACK_MODEL = "gemini-3.1-flash-image-preview"


def try_openai(prompt: str, size: str, quality: str, out_path: Path) -> tuple[bool, str]:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return False, "OPENAI_API_KEY not set"
    try:
        from openai import OpenAI

        client = OpenAI(api_key=key)
        result = client.images.generate(
            model=PRIMARY_MODEL,
            prompt=prompt,
            size=size if size != "auto" else "auto",
            quality=quality,
            n=1,
        )
        b64 = result.data[0].b64_json
        img_bytes = base64.b64decode(b64)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(img_bytes)
        return True, ""
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def try_gemini(prompt: str, out_path: Path) -> tuple[bool, str]:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        return False, "GEMINI_API_KEY/GOOGLE_API_KEY not set"
    try:
        from google import genai
        from PIL import Image as PILImage
        from io import BytesIO

        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model=FALLBACK_MODEL,
            contents=prompt,
        )
        for candidate in response.candidates:
            for part in candidate.content.parts:
                data = getattr(getattr(part, "inline_data", None), "data", None)
                if not data:
                    continue
                if isinstance(data, str):
                    data = base64.b64decode(data)
                img = PILImage.open(BytesIO(data))
                if img.mode == "RGBA":
                    bg = PILImage.new("RGB", img.size, (255, 255, 255))
                    bg.paste(img, mask=img.split()[3])
                    img = bg
                elif img.mode != "RGB":
                    img = img.convert("RGB")
                out_path.parent.mkdir(parents=True, exist_ok=True)
                img.save(str(out_path), "PNG")
                return True, ""
        return False, "no image data in Gemini response"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an image with gpt-image-2 (Gemini fallback).")
    parser.add_argument("--prompt", "-p", required=True, help="Image description")
    parser.add_argument("--filename", "-f", required=True, help="Output path (PNG)")
    parser.add_argument("--size", "-s", default="1024x1024",
                        choices=["1024x1024", "1536x1024", "1024x1536", "auto"],
                        help="Output size (OpenAI only; Gemini fallback ignores)")
    parser.add_argument("--quality", "-q", default="high",
                        choices=["low", "medium", "high", "auto"],
                        help="Quality tier (OpenAI only)")
    args = parser.parse_args()

    out = Path(args.filename)

    print(f"Trying primary: {PRIMARY_MODEL} (size={args.size}, quality={args.quality})...")
    ok, err = try_openai(args.prompt, args.size, args.quality, out)
    if ok:
        print(f"Saved: {out.resolve()}")
        print("provider=openai")
        return 0

    print(f"Primary failed: {err}", file=sys.stderr)
    print(f"Falling back to: {FALLBACK_MODEL}...")
    ok2, err2 = try_gemini(args.prompt, out)
    if ok2:
        print(f"Saved: {out.resolve()}")
        print("provider=gemini")
        return 0

    print(f"Fallback failed: {err2}", file=sys.stderr)
    print("Both providers failed.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
