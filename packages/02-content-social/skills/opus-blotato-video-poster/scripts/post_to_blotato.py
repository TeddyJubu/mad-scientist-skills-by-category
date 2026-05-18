#!/usr/bin/env python3
"""Post Opus Clip results to Blotato"""

import sys
import json
import requests
from datetime import datetime, timezone, timedelta

BLOTATO_API_KEY = "blt_C4H/l9gOlOm/+pt4wXQqWiJ9VBMl3n/FEW17OKovrtw="
BLOTATO_BASE_URL = "https://api.blotato.com"
MCP_TOKEN = "ODAzNmQ3ZWYtMzI1YS00YTNhLTk0OTktMTM1NDUyZGQwM2Q0OktYVzFDV3BoaitFcEhER2gxN3FYSHdLMVIyWHlNM3d2a1J5YlNvRHNId3M9"
MCP_ENDPOINT = "https://mcp.zapier.com/api/v1/connect"

BLOTATO_ACCOUNTS = [
    {"id": "15082", "platform": "facebook", "targetType": "page", "pageId": "491473457567789"},
    {"id": "21244", "platform": "youtube", "targetType": "channel", "title_prefix": "Viral Clip:"},
    {"id": "24117", "platform": "instagram", "targetType": "feed"},
    {"id": "23181", "platform": "tiktok", "targetType": "video"},
    {"id": "10251", "platform": "twitter", "targetType": "tweet"}
]

def log(msg):
    print(f"[{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}] {msg}", flush=True)

def get_clip_download_url(clip_id):
    """Get direct MP4 URL for a clip using MCP"""
    # Extract short ID (format: PROJECT_ID.CLIP_SHORT_ID)
    short_id = clip_id.split('.')[-1] if '.' in clip_id else clip_id
    prefixed_id = f"c.{short_id}"
    
    log(f"Getting download URL for clip {prefixed_id}")
    
    try:
        response = requests.post(
            MCP_ENDPOINT,
            headers={
                "Authorization": f"Bearer {MCP_TOKEN}",
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json"
            },
            json={
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "opusclip_get_your_video_with_captions",
                    "arguments": {"clipId": prefixed_id}
                },
                "id": int(datetime.now().timestamp())
            },
            stream=True
        )
        
        for line in response.iter_lines():
            if line and line.startswith(b'data:'):
                data = json.loads(line.decode('utf-8').replace('data: ', ''))
                if 'result' in data and 'content' in data['result']:
                    for item in data['result']['content']:
                        if item.get('type') == 'text':
                            result = json.loads(item['text'])
                            url = result.get('results', {}).get('downloadUrl')
                            if url:
                                log(f"✓ Got download URL: {url[:60]}...")
                                return url
    except Exception as e:
        log(f"Error getting download URL: {e}")
    return None

def post_to_blotato(video_url, caption, scheduled_time=None):
    """Post video to all Blotato accounts"""
    log(f"Posting to Blotato ({'scheduled' if scheduled_time else 'immediate'})")
    successful = []
    
    for account in BLOTATO_ACCOUNTS:
        try:
            payload = {
                "post": {
                    "accountId": account["id"],
                    "mediaUrls": [video_url],
                    "content": caption,
                    "targetType": account["targetType"]
                }
            }
            
            if account["platform"] == "facebook":
                payload["post"]["target"] = {"pageId": account["pageId"]}
            elif account["platform"] == "youtube":
                payload["post"]["target"] = {
                    "title": f"{account.get('title_prefix', '')} {caption[:50]}",
                    "privacyStatus": "public",
                    "shouldNotifySubscribers": True
                }
            elif account["platform"] == "tiktok":
                payload["post"]["target"] = {
                    "privacyLevel": "public",
                    "disabledComments": False,
                    "disabledDuet": False,
                    "disabledStitch": False,
                    "isBrandedContent": False,
                    "isYourBrand": False,
                    "isAiGenerated": False
                }
            
            if scheduled_time:
                payload["scheduledTime"] = scheduled_time
            
            response = requests.post(
                f"{BLOTATO_BASE_URL}/posts",
                headers={
                    "Authorization": f"Bearer {BLOTATO_API_KEY}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            
            if response.status_code in [200, 201]:
                post_id = response.json().get("id")
                log(f"✓ {account['platform']}: {post_id}")
                successful.append(account["platform"])
            else:
                log(f"✗ {account['platform']}: {response.status_code} - {response.text}")
        except Exception as e:
            log(f"✗ {account['platform']}: {e}")
    
    return successful

def main():
    if len(sys.argv) < 3:
        print("Usage: post_to_blotato.py <project_id> <clips_json>")
        sys.exit(1)
    
    project_id = sys.argv[1]
    clips_json = sys.argv[2]
    
    log(f"=== Processing Opus Clip Results for {project_id} ===")
    
    clips = json.loads(clips_json)
    
    # Sort by virality score
    sorted_clips = sorted(clips, key=lambda x: x.get('viralityScore', 0), reverse=True)
    top_2 = sorted_clips[:2]
    
    log(f"Top 2 clips:")
    for i, clip in enumerate(top_2, 1):
        log(f"  {i}. {clip.get('title', 'Untitled')} (virality: {clip.get('viralityScore', 0)})")
    
    # Get download URLs
    clip_1_url = get_clip_download_url(top_2[0]['id'])
    if not clip_1_url:
        log("ERROR: Failed to get URL for clip #1")
        sys.exit(1)
    
    # Post clip #1 immediately
    caption_1 = f"{top_2[0].get('title', 'Check out this viral clip!')} #viral #shorts"
    log("\n=== Posting Clip #1 (Immediate) ===")
    results_1 = post_to_blotato(clip_1_url, caption_1)
    log(f"Posted to: {', '.join(results_1)}")
    
    # Schedule clip #2
    if len(top_2) > 1:
        clip_2_url = get_clip_download_url(top_2[1]['id'])
        if clip_2_url:
            scheduled_dt = datetime.now(timezone.utc) + timedelta(hours=4)
            scheduled_iso = scheduled_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
            caption_2 = f"{top_2[1].get('title', 'Another viral moment!')} #viral #shorts"
            
            log(f"\n=== Scheduling Clip #2 for {scheduled_iso} ===")
            results_2 = post_to_blotato(clip_2_url, caption_2, scheduled_time=scheduled_iso)
            log(f"Scheduled for: {', '.join(results_2)}")
    
    log("\n=== Complete ===")

if __name__ == "__main__":
    main()
