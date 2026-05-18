#!/usr/bin/env python3
"""
Opus Clip + Blotato Video Posting Workflow

Takes a YouTube URL, sends it to Opus Clip for short-form clip generation,
selects the top 2 clips by virality score, posts clip #1 immediately,
and schedules clip #2 for 4 hours later.

Usage:
    nohup python3.11 opus_blotato_workflow.py "<youtube_url>" > workflow.log 2>&1 &
"""

import sys
import time
import json
import requests
from datetime import datetime, timezone, timedelta

# Configuration
BLOTATO_API_KEY = "blt_C4H/l9gOlOm/+pt4wXQqWiJ9VBMl3n/FEW17OKovrtw="
BLOTATO_BASE_URL = "https://api.blotato.com"
ZAPIER_MCP_URL = "https://actions.zapier.com/v1"  # Replace with actual Zapier MCP endpoint if different

# Blotato account configurations
BLOTATO_ACCOUNTS = [
    {
        "id": "15082",
        "platform": "facebook",
        "targetType": "page",
        "pageId": "491473457567789"
    },
    {
        "id": "21244",
        "platform": "youtube",
        "targetType": "channel",
        "title_prefix": "Viral Clip:",
        "privacyStatus": "public",
        "notifySubscribers": True
    },
    {
        "id": "24117",
        "platform": "instagram",
        "targetType": "feed"
    },
    {
        "id": "23181",
        "platform": "tiktok",
        "targetType": "video",
        "privacyLevel": "public",
        "disabledComments": False,
        "disabledDuet": False,
        "disabledStitch": False,
        "isBrandedContent": False,
        "isYourBrand": False,
        "isAiGenerated": False
    },
    {
        "id": "10251",
        "platform": "twitter",
        "targetType": "tweet"
    }
]


def log(message):
    """Print timestamped log message"""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{timestamp}] {message}")
    sys.stdout.flush()


def submit_to_opus_clip(youtube_url):
    """
    Submit YouTube URL to Opus Clip via Zapier MCP
    Returns: project_id or None on failure
    """
    log(f"Submitting YouTube URL to Opus Clip: {youtube_url}")
    
    # This is a placeholder - replace with actual Zapier MCP integration
    # The actual implementation would use the opusclip_submit tool via MCP
    # For now, this is a mock implementation showing the expected flow
    
    try:
        # Mock response - in real implementation, call Zapier MCP endpoint
        # response = requests.post(ZAPIER_MCP_URL + "/opusclip_submit", 
        #                         json={"videoUrl": youtube_url})
        # project_id = response.json()["projectId"]
        
        log("ERROR: This script requires Zapier MCP integration to be configured")
        log("Please ensure the Zapier MCP server is running and accessible")
        return None
        
    except Exception as e:
        log(f"Error submitting to Opus Clip: {e}")
        return None


def poll_for_clips(project_id, max_attempts=50, interval=30):
    """
    Poll Opus Clip for completed clips using opusclip_get_transcript_of_clips
    Returns: list of clips with IDs, titles, and virality scores
    """
    log(f"Polling for clips from project {project_id} (max {max_attempts} attempts, {interval}s interval)")
    
    for attempt in range(1, max_attempts + 1):
        log(f"Attempt {attempt}/{max_attempts}")
        
        try:
            # Mock implementation - replace with actual MCP call
            # response = requests.post(ZAPIER_MCP_URL + "/opusclip_get_transcript_of_clips",
            #                         json={"projectId": project_id})
            # clips = response.json()["clips"]
            
            # For demonstration, returning empty list
            clips = []
            
            if clips and len(clips) > 0:
                log(f"Found {len(clips)} clips!")
                return clips
            
            log(f"No clips ready yet. Waiting {interval}s...")
            time.sleep(interval)
            
        except Exception as e:
            log(f"Error polling for clips: {e}")
            time.sleep(interval)
    
    log("Max polling attempts reached. No clips found.")
    return []


def get_clip_download_url(clip_id):
    """
    Get direct MP4 download URL for a specific clip
    clip_id format: PROJECT_ID.CLIP_SHORT_ID (e.g., P3022413qNyO.7vyo4D2QPT)
    Returns: direct MP4 URL or None
    """
    # Extract short ID (after the dot)
    if '.' in clip_id:
        short_id = clip_id.split('.')[1]
    else:
        short_id = clip_id
    
    # Prefix with 'c.' as required by Opus Clip API
    prefixed_id = f"c.{short_id}"
    
    log(f"Getting download URL for clip {prefixed_id}")
    
    try:
        # Mock implementation - replace with actual MCP call
        # response = requests.post(ZAPIER_MCP_URL + "/opusclip_get_your_video_with_captions",
        #                         json={"clipId": prefixed_id})
        # download_url = response.json()["downloadUrl"]
        
        log("ERROR: This script requires Zapier MCP integration to be configured")
        return None
        
    except Exception as e:
        log(f"Error getting download URL: {e}")
        return None


def post_to_blotato(video_url, caption, scheduled_time=None):
    """
    Post video to all connected Blotato accounts
    If scheduled_time is provided (ISO 8601 UTC), schedule the post
    Returns: list of successful post IDs
    """
    log(f"Posting to Blotato (scheduled: {scheduled_time or 'immediate'})")
    
    successful_posts = []
    
    for account in BLOTATO_ACCOUNTS:
        try:
            # Build the request payload
            payload = {
                "post": {
                    "accountId": account["id"],
                    "mediaUrls": [video_url],
                    "content": caption,
                    "targetType": account["targetType"]
                }
            }
            
            # Add platform-specific fields
            if account["platform"] == "facebook":
                payload["post"]["target"] = {"pageId": account["pageId"]}
            
            elif account["platform"] == "youtube":
                payload["post"]["target"] = {
                    "title": f"{account.get('title_prefix', '')} {caption[:50]}",
                    "privacyStatus": account.get("privacyStatus", "public"),
                    "shouldNotifySubscribers": account.get("notifySubscribers", True)
                }
            
            elif account["platform"] == "tiktok":
                payload["post"]["target"] = {
                    "privacyLevel": account.get("privacyLevel", "public"),
                    "disabledComments": account.get("disabledComments", False),
                    "disabledDuet": account.get("disabledDuet", False),
                    "disabledStitch": account.get("disabledStitch", False),
                    "isBrandedContent": account.get("isBrandedContent", False),
                    "isYourBrand": account.get("isYourBrand", False),
                    "isAiGenerated": account.get("isAiGenerated", False)
                }
            
            # Add scheduled time if provided
            if scheduled_time:
                payload["scheduledTime"] = scheduled_time
            
            # Make API request
            headers = {
                "Authorization": f"Bearer {BLOTATO_API_KEY}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{BLOTATO_BASE_URL}/posts",
                headers=headers,
                json=payload
            )
            
            if response.status_code in [200, 201]:
                post_id = response.json().get("id")
                log(f"✓ Posted to {account['platform']} (account {account['id']}): {post_id}")
                successful_posts.append({
                    "platform": account["platform"],
                    "account_id": account["id"],
                    "post_id": post_id
                })
            else:
                log(f"✗ Failed to post to {account['platform']}: {response.status_code} - {response.text}")
        
        except Exception as e:
            log(f"✗ Error posting to {account['platform']}: {e}")
    
    return successful_posts


def main():
    if len(sys.argv) < 2:
        print("Usage: python3.11 opus_blotato_workflow.py <youtube_url>")
        sys.exit(1)
    
    youtube_url = sys.argv[1]
    
    log("=== Starting Opus Clip + Blotato Workflow ===")
    log(f"YouTube URL: {youtube_url}")
    
    # Step 1: Submit to Opus Clip
    project_id = submit_to_opus_clip(youtube_url)
    if not project_id:
        log("ERROR: Failed to submit video to Opus Clip")
        sys.exit(1)
    
    # Step 2: Poll for clips (up to 25 minutes)
    clips = poll_for_clips(project_id, max_attempts=50, interval=30)
    if not clips or len(clips) == 0:
        log("ERROR: No clips generated")
        sys.exit(1)
    
    # Step 3: Sort by virality score and select top 2
    sorted_clips = sorted(clips, key=lambda x: x.get("viralityScore", 0), reverse=True)
    top_2_clips = sorted_clips[:2]
    
    log(f"Selected top 2 clips:")
    for i, clip in enumerate(top_2_clips, 1):
        log(f"  {i}. {clip.get('title', 'Untitled')} (virality: {clip.get('viralityScore', 0)})")
    
    # Step 4: Get download URLs for both clips
    clip_1_url = get_clip_download_url(top_2_clips[0]["id"])
    clip_2_url = get_clip_download_url(top_2_clips[1]["id"]) if len(top_2_clips) > 1 else None
    
    if not clip_1_url:
        log("ERROR: Failed to get download URL for clip #1")
        sys.exit(1)
    
    # Step 5: Post clip #1 immediately
    caption_1 = f"{top_2_clips[0].get('title', 'Check out this viral clip!')} #viral #shorts"
    log("\n=== Posting Clip #1 (Immediate) ===")
    results_1 = post_to_blotato(clip_1_url, caption_1)
    log(f"Posted clip #1 to {len(results_1)} platforms")
    
    # Step 6: Schedule clip #2 for 4 hours later
    if clip_2_url:
        scheduled_dt = datetime.now(timezone.utc) + timedelta(hours=4)
        scheduled_iso = scheduled_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        caption_2 = f"{top_2_clips[1].get('title', 'Another viral moment!')} #viral #shorts"
        
        log("\n=== Scheduling Clip #2 (4 hours from now) ===")
        log(f"Scheduled time: {scheduled_iso}")
        results_2 = post_to_blotato(clip_2_url, caption_2, scheduled_time=scheduled_iso)
        log(f"Scheduled clip #2 for {len(results_2)} platforms")
    else:
        log("\n=== Skipping Clip #2 (only 1 clip available) ===")
    
    log("\n=== Workflow Complete ===")


if __name__ == "__main__":
    main()
