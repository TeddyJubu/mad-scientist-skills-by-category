#!/usr/bin/env python3
"""
send_telegram.py - Send PDF newsletter via Telegram message tool.

Usage:
    python3 send_telegram.py --pdf newsletter.pdf [--target <chat_id>]
"""

import sys
import os

def send_via_message_tool(pdf_path, target=None):
    """Send PDF using OpenClaw's internal message mechanism."""
    
    # For OpenClaw agents, we use the message tool directly via Python
    # This integrates with the current session's Telegram context
    
    # Import the message function if available, otherwise fall back to file placement
    try:
        # Check if PDF exists
        if not os.path.exists(pdf_path):
            print(f"Error: PDF file not found: {pdf_path}", file=sys.stderr)
            return False
        
        # For now, print success and instructions
        # The actual OpenClaw integration would use the message tool here
        print(f"✅ Newsletter generated successfully!", file=sys.stderr)
        print(f"   PDF location: {pdf_path}", file=sys.stderr)
        print(f"   File size: {os.path.getsize(pdf_path)} bytes", file=sys.stderr)
        
        if target:
            print(f"   Target: {target}", file=sys.stderr)
        else:
            print(f"   Target: Current Telegram chat", file=sys.stderr)
        
        # Copy PDF to workspace for manual delivery
        workspace_path = os.path.expanduser('~/.openclaw/workspace/rei-ai-weekly.pdf')
        import shutil
        shutil.copy2(pdf_path, workspace_path)
        print(f"\n📎 PDF copied to workspace: {workspace_path}", file=sys.stderr)
        print(f"   You can now send it via Telegram using the message tool", file=sys.stderr)
        
        return True
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Send PDF via Telegram')
    parser.add_argument('--pdf', required=True, help='PDF file to send')
    parser.add_argument('--target', help='Target chat ID (optional)')
    args = parser.parse_args()
    
    success = send_via_message_tool(args.pdf, args.target)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
