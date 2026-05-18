#!/usr/bin/env python3
"""
generate_pdf.py - Generate dynamic, visually stunning PDF newsletter.

Usage:
    python3 generate_pdf.py --input content.json --output newsletter.pdf
"""

import json
import sys
import argparse
from datetime import datetime
from weasyprint import HTML, CSS
import os

# Real Deal Meetup branding
BRAND_COLORS = {
    'primary': '#FF6B35',      # Orange/red accent
    'secondary': '#004E89',    # Deep blue
    'tertiary': '#2EC4B6',     # Teal accent
    'background': '#F7F9FB',   # Light gray
    'text': '#1A1A1A',         # Near black
    'accent': '#FFB627',       # Gold
    'light': '#FFFFFF',
    'gradient_start': '#FF6B35',
    'gradient_end': '#FFB627'
}

def generate_html(content):
    """Generate dynamic HTML newsletter with modern UI/UX."""
    
    now = datetime.now()
    week_str = now.strftime('%B %d, %Y')
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        @page {{\n            size: Letter;\n            margin: 0.45in 0.5in;\n        }}\n        \n        body {{\n            font-family: 'Helvetica Neue', Arial, sans-serif;\n            color: {BRAND_COLORS['text']};\n            line-height: 1.5;\n            margin: 0;\n            padding: 0;\n            background: {BRAND_COLORS['background']};\n            font-size: 13px;\n        }}\n        \n        .container {{\n            max-width: 100%;\n            margin: 0 auto;\n        }}\n        \n        /* Hero Header */\n        .hero {{\n            background: linear-gradient(135deg, {BRAND_COLORS['secondary']} 0%, {BRAND_COLORS['primary']} 60%, {BRAND_COLORS['accent']} 100%);\n            color: white;\n            padding: 24px 24px;\n            text-align: center;\n            border-radius: 10px;\n            margin-bottom: 16px;\n        }}\n        \n        .hero h1 {{\n            margin: 0 0 6px 0;\n            font-size: 30px;\n            font-weight: 900;\n            letter-spacing: -0.5px;\n        }}\n        \n        .hero .subtitle {{\n            font-size: 13px;\n            opacity: 0.95;\n            margin: 0 0 4px 0;\n            font-weight: 300;\n        }}\n        \n        .hero .date {{\n            font-size: 12px;\n            opacity: 0.85;\n            font-weight: 600;\n            letter-spacing: 1px;\n            text-transform: uppercase;\n        }}\n        \n        /* Section Headers */\n        .section {{\n            margin-bottom: 14px;\n        }}\n        \n        .section-header {{\n            display: flex;\n            align-items: center;\n            margin-bottom: 10px;\n            margin-top: 14px;\n            padding-bottom: 6px;\n            border-bottom: 3px solid {BRAND_COLORS['primary']};\n            page-break-after: avoid;\n        }}\n        \n        .section-icon {{\n            font-size: 22px;\n            margin-right: 10px;\n        }}\n        \n        .section-title {{\n            color: {BRAND_COLORS['secondary']};\n            font-size: 20px;\n            font-weight: 800;\n            margin: 0;\n        }}\n        \n        /* Card Styles */\n        .cards {{\n            display: block;\n        }}\n        \n        .card {{\n            background: white;\n            border-radius: 8px;\n            padding: 12px 14px 12px 18px;\n            margin-bottom: 10px;\n            box-shadow: 0 2px 6px rgba(0,0,0,0.07);\n            position: relative;\n            overflow: hidden;\n            page-break-inside: avoid;\n        }}\n        \n        .card::before {{\n            content: '';\n            position: absolute;\n            left: 0;\n            top: 0;\n            height: 100%;\n            width: 4px;\n            background: linear-gradient(180deg, {BRAND_COLORS['primary']} 0%, {BRAND_COLORS['accent']} 100%);\n        }}\n        \n        .card:nth-child(even) {{\n            background: #F4F7FA;\n        }}\n        \n        .card:nth-child(even)::before {{\n            background: linear-gradient(180deg, {BRAND_COLORS['tertiary']} 0%, {BRAND_COLORS['secondary']} 100%);\n        }}\n        \n        .card-title {{\n            font-size: 14px;\n            font-weight: 700;\n            color: {BRAND_COLORS['secondary']};\n            margin: 0 0 6px 0;\n            line-height: 1.3;\n        }}\n        \n        .card-source {{\n            font-size: 10px;\n            font-weight: 700;\n            color: {BRAND_COLORS['primary']};\n            text-transform: uppercase;\n            letter-spacing: 0.5px;\n            margin: 0 0 5px 0;\n        }}\n        \n        .card-description {{\n            font-size: 12px;\n            color: #444;\n            line-height: 1.55;\n            margin: 0 0 6px 0;\n        }}\n        \n        .card-why {{\n            font-size: 11px;\n            color: #222;\n            background: #FFF8EE;\n            border-left: 3px solid {BRAND_COLORS['accent']};\n            padding: 5px 8px;\n            margin-top: 6px;\n            border-radius: 0 4px 4px 0;\n            line-height: 1.4;\n        }}\n        \n        .card-why strong {{\n            color: {BRAND_COLORS['primary']};\n        }}\n        \n        .card-meta {{\n            font-size: 11px;\n            color: #888;\n            margin-top: 6px;\n            font-weight: 600;\n        }}\n        \n        /* Video cards */\n        .video-card {{\n            background: linear-gradient(135deg, {BRAND_COLORS['secondary']} 0%, {BRAND_COLORS['primary']} 100%);\n            color: white;\n        }}\n        \n        .video-card::before {{\n            display: none;\n        }}\n        \n        .video-card .card-title {{\n            color: white;\n        }}\n        \n        .video-card .card-meta {{\n            color: rgba(255,255,255,0.85);\n        }}\n        \n        /* Footer */\n        .footer {{\n            margin-top: 16px;\n            padding: 16px 20px;\n            background: linear-gradient(135deg, {BRAND_COLORS['secondary']} 0%, {BRAND_COLORS['primary']} 100%);\n            color: white;\n            text-align: center;\n            border-radius: 8px;\n            page-break-inside: avoid;\n        }}\n        \n        .footer-title {{\n            font-size: 14px;\n            font-weight: 700;\n            margin: 0 0 4px 0;\n        }}\n        \n        .footer-text {{\n            font-size: 11px;\n            opacity: 0.9;\n            margin: 3px 0;\n        }}\n        \n        /* Accent Elements */\n        .divider {{\n            height: 2px;\n            background: linear-gradient(90deg, {BRAND_COLORS['primary']} 0%, {BRAND_COLORS['accent']} 50%, {BRAND_COLORS['tertiary']} 100%);\n            margin: 12px 0;\n            border-radius: 2px;\n        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Hero Header -->
        <div class="hero">
            <div class="hero-content">
                <h1>🏡 REI AI WEEKLY</h1>
                <p class="subtitle">AI News, Tools & Automations for Real Estate Investors</p>
                <p class="date">{week_str}</p>
            </div>
        </div>
"""
    
    # News section
    if content.get('news') and len(content['news']) > 0:
        html += '''
        <div class="section">
            <div class="section-header">
                <div class="section-icon">📰</div>
                <h2 class="section-title">AI News</h2>
            </div>
            <div class="cards">
'''
        for idx, item in enumerate(content['news'], 1):
            title = item.get('title', 'Untitled')
            source = item.get('source', '')
            desc = item.get('description', 'No description available.')
            why = item.get('why', '')
            source_html = f'<p class="card-source">{source}</p>' if source else ''
            why_html = f'<div class="card-why"><strong>💡 Why It Matters:</strong> {why}</div>' if why else ''
            html += f'''
                <div class="card">
                    {source_html}
                    <h3 class="card-title">{title}</h3>
                    <p class="card-description">{desc}</p>
                    {why_html}
                </div>
'''
        html += '            </div>\n        </div>\n'
    
    # Divider
    html += '        <div class="divider"></div>\n'
    
    # Tools section
    if content.get('tools') and len(content['tools']) > 0:
        html += '''
        <div class="section">
            <div class="section-header">
                <div class="section-icon">🛠️</div>
                <h2 class="section-title">New Tools</h2>
            </div>
            <div class="cards">
'''
        for idx, item in enumerate(content['tools'], 1):
            title = item.get('title', 'Untitled')
            source = item.get('source', '')
            desc = item.get('description', 'No description available.')
            why = item.get('why', '')
            source_html = f'<p class="card-source">{source}</p>' if source else ''
            why_html = f'<div class="card-why"><strong>💡 Why It Matters:</strong> {why}</div>' if why else ''
            html += f'''
                <div class="card">
                    {source_html}
                    <h3 class="card-title">{title}</h3>
                    <p class="card-description">{desc}</p>
                    {why_html}
                </div>
'''
        html += '            </div>\n        </div>\n'
    
    # Divider
    html += '        <div class="divider"></div>\n'
    
    # Automations section
    if content.get('automations') and len(content['automations']) > 0:
        html += '''
        <div class="section">
            <div class="section-header">
                <div class="section-icon">⚡</div>
                <h2 class="section-title">Trending Automations</h2>
            </div>
            <div class="cards">
'''
        for idx, item in enumerate(content['automations'], 1):
            title = item.get('title', 'Untitled')
            source = item.get('source', '')
            desc = item.get('description', 'No description available.')
            why = item.get('why', '')
            source_html = f'<p class="card-source">{source}</p>' if source else ''
            why_html = f'<div class="card-why"><strong>💡 Why It Matters:</strong> {why}</div>' if why else ''
            html += f'''
                <div class="card">
                    {source_html}
                    <h3 class="card-title">{title}</h3>
                    <p class="card-description">{desc}</p>
                    {why_html}
                </div>
'''
        html += '            </div>\n        </div>\n'
    
    # YouTube section (if available)
    if content.get('youtube') and len(content['youtube']) > 0:
        html += '        <div class="divider"></div>\n'
        html += '''
        <div class="section">
            <div class="section-header">
                <div class="section-icon">▶️</div>
                <h2 class="section-title">Featured Videos</h2>
            </div>
            <div class="cards">
'''
        for idx, video in enumerate(content['youtube'], 1):
            title = video.get('title', 'Untitled')
            channel = video.get('channel', 'Unknown')
            views = video.get('views', 0)
            views_str = f'{views:,} views' if views else ''
            html += f'''
                <div class="card video-card">
                    <h3 class="card-title">{title}</h3>
                    <p class="card-meta">📺 {channel}{" • " + views_str if views_str else ""}</p>
                </div>
'''
        html += '            </div>\n        </div>\n'
    
    # Footer
    html += f'''
        <div class="footer">
            <p class="footer-title">🏡 Real Deal Meetup</p>
            <p class="footer-text">Curated weekly with AI-powered content discovery</p>
            <p class="footer-text">Your trusted source for REI AI insights</p>
        </div>
    </div>
</body>
</html>
'''
    
    return html

def main():
    parser = argparse.ArgumentParser(description='Generate PDF newsletter')
    parser.add_argument('--input', default='content.json', help='Input JSON file')
    parser.add_argument('--output', default='newsletter.pdf', help='Output PDF file')
    args = parser.parse_args()
    
    # Load content
    with open(args.input, 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    # Generate HTML
    html_content = generate_html(content)
    
    # Generate PDF
    HTML(string=html_content).write_pdf(args.output)
    
    print(f"PDF generated: {args.output}", file=sys.stderr)

if __name__ == '__main__':
    main()
