#!/usr/bin/env python3
"""
Generate Instagram carousel slides using PIL/Pillow.
Provides pixel-perfect control for text-heavy, typography-focused slides.
"""

import argparse
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Canvas size for Instagram carousels
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 1080

# Default margins (safety zone for mobile viewing)
MARGIN_TOP = 80
MARGIN_BOTTOM = 80
MARGIN_LEFT = 80
MARGIN_RIGHT = 80

def wrap_text(text, font, max_width):
    """
    Wrap text to fit within max_width using the given font.
    Returns a list of lines.
    """
    lines = []
    words = text.split()
    current_line = ""
    
    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = font.getbbox(test_line)
        width = bbox[2] - bbox[0]
        
        if width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return lines

def create_cover_slide(headline, bg_color, text_color, font_size, logo_path=None):
    """
    Create a bold cover slide (Slide 1) with centered headline.
    """
    img = Image.new('RGB', (CANVAS_WIDTH, CANVAS_HEIGHT), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Use a bold sans-serif font (fallback to default if not found)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Wrap headline text
    max_text_width = CANVAS_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    lines = wrap_text(headline, font, max_text_width)
    
    # Calculate total text height
    line_height = font_size * 1.2
    total_height = line_height * len(lines)
    
    # Center text vertically
    y = (CANVAS_HEIGHT - total_height) / 2
    
    # Draw each line centered
    for line in lines:
        bbox = font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        x = (CANVAS_WIDTH - text_width) / 2
        draw.text((x, y), line, fill=text_color, font=font)
        y += line_height
    
    # Add logo if provided
    if logo_path:
        try:
            logo = Image.open(logo_path)
            logo.thumbnail((100, 100))
            logo_x = CANVAS_WIDTH - logo.width - 40
            logo_y = CANVAS_HEIGHT - logo.height - 40
            img.paste(logo, (logo_x, logo_y), logo if logo.mode == 'RGBA' else None)
        except:
            pass
    
    return img

def create_value_slide(headline, body, authority, bg_color, headline_color, body_color, logo_path=None):
    """
    Create a value slide (Slides 2-7) with headline, body copy, and authority signal.
    """
    img = Image.new('RGB', (CANVAS_WIDTH, CANVAS_HEIGHT), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Fonts
    try:
        headline_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 42)
        authority_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    except:
        headline_font = body_font = authority_font = ImageFont.load_default()
    
    y_offset = MARGIN_TOP + 100
    max_text_width = CANVAS_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    
    # Draw headline
    headline_lines = wrap_text(headline, headline_font, max_text_width)
    for line in headline_lines:
        draw.text((MARGIN_LEFT, y_offset), line, fill=headline_color, font=headline_font)
        y_offset += 100
    
    y_offset += 80  # spacing
    
    # Draw body copy
    body_lines = wrap_text(body, body_font, max_text_width)
    for line in body_lines:
        draw.text((MARGIN_LEFT, y_offset), line, fill=body_color, font=body_font)
        y_offset += 60
    
    # Draw authority signal at bottom
    if authority:
        authority_y = CANVAS_HEIGHT - MARGIN_BOTTOM - 120
        authority_lines = wrap_text(authority, authority_font, max_text_width)
        for line in authority_lines:
            draw.text((MARGIN_LEFT, authority_y), line, fill=body_color, font=authority_font)
            authority_y += 45
    
    # Add logo if provided
    if logo_path:
        try:
            logo = Image.open(logo_path)
            logo.thumbnail((100, 100))
            logo_x = CANVAS_WIDTH - logo.width - 40
            logo_y = CANVAS_HEIGHT - logo.height - 40
            img.paste(logo, (logo_x, logo_y), logo if logo.mode == 'RGBA' else None)
        except:
            pass
    
    return img

def create_cta_slide(cta_text, bg_color, text_color, logo_path=None):
    """
    Create a CTA slide (Slide 9) with centered call-to-action.
    """
    img = Image.new('RGB', (CANVAS_WIDTH, CANVAS_HEIGHT), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
    except:
        font = ImageFont.load_default()
    
    max_text_width = CANVAS_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    lines = wrap_text(cta_text, font, max_text_width)
    
    line_height = 90
    total_height = line_height * len(lines)
    y = (CANVAS_HEIGHT - total_height) / 2
    
    for line in lines:
        bbox = font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        x = (CANVAS_WIDTH - text_width) / 2
        draw.text((x, y), line, fill=text_color, font=font)
        y += line_height
    
    # Add logo if provided
    if logo_path:
        try:
            logo = Image.open(logo_path)
            logo.thumbnail((100, 100))
            logo_x = CANVAS_WIDTH - logo.width - 40
            logo_y = CANVAS_HEIGHT - logo.height - 40
            img.paste(logo, (logo_x, logo_y), logo if logo.mode == 'RGBA' else None)
        except:
            pass
    
    return img

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def main():
    parser = argparse.ArgumentParser(description='Generate Instagram carousel slides')
    parser.add_argument('--layout', choices=['cover', 'value', 'cta'], required=True,
                        help='Slide layout type')
    parser.add_argument('--headline', help='Headline text')
    parser.add_argument('--body', help='Body copy text')
    parser.add_argument('--authority', help='Authority signal text')
    parser.add_argument('--text', help='Main text (for cover/cta slides)')
    parser.add_argument('--bg-color', default='#FFFFFF', help='Background color (hex)')
    parser.add_argument('--headline-color', default='#1A237E', help='Headline color (hex)')
    parser.add_argument('--body-color', default='#333333', help='Body text color (hex)')
    parser.add_argument('--text-color', default='#FFFFFF', help='Text color for cover/cta (hex)')
    parser.add_argument('--font-size', type=int, default=100, help='Font size for cover/cta')
    parser.add_argument('--logo', help='Path to logo file')
    parser.add_argument('--output', required=True, help='Output filename')
    
    args = parser.parse_args()
    
    # Convert hex colors to RGB
    bg_color = hex_to_rgb(args.bg_color)
    
    if args.layout == 'cover':
        text = args.text or args.headline
        if not text:
            print("Error: --text or --headline required for cover layout")
            return
        text_color = hex_to_rgb(args.text_color)
        img = create_cover_slide(text, bg_color, text_color, args.font_size, args.logo)
    
    elif args.layout == 'value':
        if not args.headline:
            print("Error: --headline required for value layout")
            return
        headline_color = hex_to_rgb(args.headline_color)
        body_color = hex_to_rgb(args.body_color)
        img = create_value_slide(
            args.headline,
            args.body or "",
            args.authority or "",
            bg_color,
            headline_color,
            body_color,
            args.logo
        )
    
    elif args.layout == 'cta':
        text = args.text or args.headline
        if not text:
            print("Error: --text or --headline required for cta layout")
            return
        text_color = hex_to_rgb(args.text_color)
        img = create_cta_slide(text, bg_color, text_color, args.logo)
    
    # Save the image
    img.save(args.output, 'PNG', quality=95)
    print(f"✅ Slide saved: {args.output}")

if __name__ == '__main__':
    main()
