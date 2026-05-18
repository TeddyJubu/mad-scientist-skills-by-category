#!/usr/bin/env python3
"""
aggregate_content.py - Collect AI + Real Estate content from multiple sources.

Usage:
    python3 aggregate_content.py --output content.json
"""

import json
import sys
import argparse
from datetime import datetime, timedelta
import subprocess
import os
import urllib.parse

def search_brave(query, count=10):
    """Search web via Brave Search API."""
    # Load API key
    secrets_path = os.path.expanduser('~/.openclaw/workspace/skills/brave-search/.secrets/brave.env')
    api_key = None
    
    try:
        with open(secrets_path, 'r') as f:
            for line in f:
                if line.startswith('BRAVE_API_KEY='):
                    api_key = line.split('=', 1)[1].strip()
                    break
    except Exception as e:
        print(f"Warning: Could not load Brave API key: {e}", file=sys.stderr)
        return []
    
    if not api_key:
        print("Warning: BRAVE_API_KEY not found", file=sys.stderr)
        return []
    
    # URL encode query
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.search.brave.com/res/v1/web/search?q={encoded_query}&count={count}"
    
    # Execute search
    cmd = ['curl', '-s', '-H', 'Accept: application/json', '-H', f'X-Subscription-Token: {api_key}', url]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        data = json.loads(result.stdout)
        
        results = []
        for item in data.get('web', {}).get('results', []):
            results.append({
                'title': item.get('title', ''),
                'url': item.get('url', ''),
                'description': item.get('description', ''),
                'age': item.get('age', '')
            })
        
        # Also include news results if available
        for item in data.get('news', {}).get('results', []):
            results.append({
                'title': item.get('title', ''),
                'url': item.get('url', ''),
                'description': item.get('description', ''),
                'age': item.get('age', '')
            })
        
        return results
    except Exception as e:
        print(f"Brave search error for '{query}': {e}", file=sys.stderr)
        return []

def search_youtube(query, days=7):
    """Search YouTube for recent videos."""
    # Search YouTube for videos published in last 7 days
    date_filter = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
    
    # Use yt-dlp to search
    cmd = [
        'yt-dlp',
        f'ytsearch10:{query}',
        '--dump-json',
        '--no-download',
        '--dateafter', date_filter,
        '--no-warnings'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    video = json.loads(line)
                    videos.append({
                        'title': video.get('title'),
                        'url': video.get('webpage_url'),
                        'channel': video.get('uploader'),
                        'published': video.get('upload_date'),
                        'views': video.get('view_count', 0)
                    })
                except:
                    pass
        return videos
    except subprocess.TimeoutExpired:
        print(f"YouTube search timed out for '{query}'", file=sys.stderr)
        return []
    except Exception as e:
        print(f"YouTube search error: {e}", file=sys.stderr)
        return []

def aggregate_all_sources():
    """Aggregate content from all sources."""
    
    # Search queries optimized for REI + AI content
    queries = {
        'news': 'AI artificial intelligence real estate investing news 2026',
        'tools': 'AI tools software real estate investors automation',
        'automations': 'real estate investor AI automation workflow ChatGPT',
        'youtube': 'AI automation for real estate investors 2026'
    }
    
    content = {
        'news': [],
        'tools': [],
        'automations': [],
        'youtube': [],
        'generated_at': datetime.now().isoformat()
    }
    
    # Collect news (top 5, will use best 3)
    print("Searching for AI real estate news...", file=sys.stderr)
    content['news'] = search_brave(queries['news'], count=5)
    print(f"  Found {len(content['news'])} news items", file=sys.stderr)
    
    # Collect tools (top 5, will use best 3)
    print("Searching for AI tools...", file=sys.stderr)
    content['tools'] = search_brave(queries['tools'], count=5)
    print(f"  Found {len(content['tools'])} tools", file=sys.stderr)
    
    # Collect automations (top 5, will use best 3)
    print("Searching for automations...", file=sys.stderr)
    content['automations'] = search_brave(queries['automations'], count=5)
    print(f"  Found {len(content['automations'])} automations", file=sys.stderr)
    
    # Collect YouTube videos
    print("Searching YouTube...", file=sys.stderr)
    content['youtube'] = search_youtube(queries['youtube'], days=7)
    print(f"  Found {len(content['youtube'])} videos", file=sys.stderr)
    
    return content

def main():
    parser = argparse.ArgumentParser(description='Aggregate REI AI content')
    parser.add_argument('--output', default='content.json', help='Output JSON file')
    args = parser.parse_args()
    
    content = aggregate_all_sources()
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Content aggregated successfully!", file=sys.stderr)
    print(f"   {len(content['news'])} news | {len(content['tools'])} tools | "
          f"{len(content['automations'])} automations | {len(content['youtube'])} videos", file=sys.stderr)
    print(f"   Saved to: {args.output}", file=sys.stderr)

if __name__ == '__main__':
    main()
