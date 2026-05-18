#!/usr/bin/env python3
"""
Fish Audio TTS - Text to Speech Generation

Usage:
    python3 generate_audio.py --text "Your text here" --output audio.mp3
    python3 generate_audio.py --text "Your text here" --voice "voice_id" --output audio.mp3
"""

import os
import sys
import argparse
import requests
from pathlib import Path

# Default voice (E-Girl Voice)
DEFAULT_VOICE = "8ef4a238714b45718ce04243307c57a7"

def load_api_key():
    """Load Fish Audio API key from .secrets/fish-audio.env"""
    secrets_path = Path.home() / ".openclaw" / ".secrets" / "fish-audio.env"
    
    if not secrets_path.exists():
        print(f"ERROR: API key file not found: {secrets_path}")
        print("Create the file with: FISH_AUDIO_API_KEY=your_key_here")
        sys.exit(1)
    
    with open(secrets_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("FISH_AUDIO_API_KEY="):
                return line.split("=", 1)[1]
    
    print("ERROR: FISH_AUDIO_API_KEY not found in secrets file")
    sys.exit(1)

def generate_audio(text, voice_id, output_path):
    """Call Fish Audio API to generate speech"""
    api_key = load_api_key()
    
    url = "https://api.fish.audio/v1/tts"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "reference_id": voice_id
    }
    
    print(f"Generating audio with voice: {voice_id}")
    print(f"Text: {text[:100]}{'...' if len(text) > 100 else ''}")
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        print(f"ERROR: API returned status {response.status_code}")
        print(f"Response: {response.text}")
        sys.exit(1)
    
    # Save audio file
    with open(output_path, "wb") as f:
        f.write(response.content)
    
    file_size = os.path.getsize(output_path)
    print(f"✅ Audio generated successfully!")
    print(f"Output: {output_path}")
    print(f"Size: {file_size / 1024:.1f} KB")

def main():
    parser = argparse.ArgumentParser(description="Generate speech using Fish Audio TTS")
    parser.add_argument("--text", required=True, help="Text to convert to speech")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help="Voice model ID (default: E-Girl Voice)")
    parser.add_argument("--output", default="output.mp3", help="Output MP3 file path")
    
    args = parser.parse_args()
    
    generate_audio(args.text, args.voice, args.output)

if __name__ == "__main__":
    main()
