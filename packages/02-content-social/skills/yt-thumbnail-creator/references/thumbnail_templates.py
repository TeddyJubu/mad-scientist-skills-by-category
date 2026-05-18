#!/usr/bin/env python3
"""
MrBeast-Style YouTube Thumbnail Templates (PIL Compositing)
-----------------------------------------------------------
Generates 3 thumbnail variants by compositing the exact (unmodified) headshot
onto programmatic backgrounds — guaranteed face preservation (no AI face redraw).

Usage:
    /root/.hermes/hermes-agent/venv/bin/python3 thumbnail_templates.py <headshot_path>

Outputs:
    /root/thumbnails/thumb1_red.png
    /root/thumbnails/thumb2_gold.png  
    /root/thumbnails/thumb3_split.png
"""

from PIL import Image, ImageDraw, ImageFont
import os, sys, math

W, H = 1280, 720

def load_headshot(path):
    img = Image.open(path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    return img

def get_font():
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    ]
    for fp in candidates:
        if os.path.exists(fp):
            return fp
    raise FileNotFoundError("No bold font found")

FONT_PATH = get_font()

def draw_outlined_text(draw, text, pos, font, fill_color, outline_color=(0,0,0), outline_width=8):
    """Draw text with thick outline for thumbnail readability"""
    for dx in range(-outline_width, outline_width+1):
        for dy in range(-outline_width, outline_width+1):
            if dx*dx + dy*dy <= outline_width*outline_width:
                draw.text((pos[0]+dx, pos[1]+dy), text, font=font, fill=outline_color)
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if dx*dx + dy*dy <= 16:
                draw.text((pos[0]+dx+4, pos[1]+dy+4), text, font=font, fill=(0,0,0,180))
    draw.text(pos, text, font=font, fill=fill_color)

def paste_face_with_stroke(face_img, bg, x, y, stroke_width=8, stroke_color=(255,255,255)):
    """Paste face with white border stroke (MrBeast signature)"""
    target_w = 380
    ratio = target_w / face_img.width
    target_h = int(face_img.height * ratio)
    scaled_face = face_img.resize((target_w, target_h), Image.LANCZOS)
    sw = stroke_width * 2
    bg.paste(Image.new('RGBA', (target_w+sw, target_h+sw), stroke_color), (x-stroke_width, y-stroke_width))
    bg.paste(scaled_face, (x, y), scaled_face)

def template1_warning(headshot, text, output_path):
    """Red/Black - Bold Warning style"""
    bg = Image.new('RGB', (W, H), (180, 10, 10))
    draw = ImageDraw.Draw(bg)
    
    # Diagonal speed lines
    for i in range(20):
        y_start = i * 40 - 100
        draw.line([(500, y_start), (W+100, y_start+400)], fill=(120, 0, 0, 100), width=4)
    
    # Sunburst
    for angle in range(0, 360, 15):
        rad = math.radians(angle)
        x2 = 750 + 500 * math.cos(rad)
        y2 = 360 + 500 * math.sin(rad)
        draw.line([(750, 360), (x2, y2)], fill=(210, 30, 30), width=50)

    # Face
    paste_face_with_stroke(headshot, bg, 30, 60, stroke_width=10)
    
    # Text
    text_x = 460
    font_big = ImageFont.truetype(FONT_PATH, 96)
    font_med = ImageFont.truetype(FONT_PATH, 76)
    draw_outlined_text(draw, text.split()[0] + "-" + text.split()[1], (text_x, 80), font_big, (255,255,255))
    draw_outlined_text(draw, text.split()[2], (text_x, 210), font_big, (255,230,50))
    draw_outlined_text(draw, text.split()[3], (text_x, 340), font_med, (255,255,255))
    
    bg.save(output_path, quality=95)

def template2_gold(headshot, text, output_path):
    """Gold/Black - Power/Premium style"""
    bg = Image.new('RGB', (W, H), (12, 12, 14))
    draw = ImageDraw.Draw(bg)
    
    # Gold rays
    for angle in range(0, 360, 10):
        rad = math.radians(angle)
        x2 = 640 + 500 * math.cos(rad)
        y2 = 360 + 500 * math.sin(rad)
        draw.line([(640, 360), (x2, y2)], fill=(220, 180, 40), width=25)

    # Face bottom-left
    paste_face_with_stroke(headshot, bg, 40, H-400, stroke_width=8, stroke_color=(200,180,80))
    
    # Gold text
    text_x = 400
    font_big = ImageFont.truetype(FONT_PATH, 96)
    font_med = ImageFont.truetype(FONT_PATH, 76)
    draw_outlined_text(draw, "ONE-CLICK", (text_x, 80), font_big, (255,210,0))
    draw_outlined_text(draw, "REHAB", (text_x, 210), font_big, (255,255,255))
    draw_outlined_text(draw, "ESTIMATOR", (text_x, 340), font_med, (255,255,255))

    bg.save(output_path, quality=95)

def template3_split(headshot, text, output_path):
    """Before/After Split style"""
    bg = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(bg)
    
    # Left half: dark
    for x in range(W//2):
        draw.line([(x, 0), (x, H)], fill=(15, 15, 30))
    
    # Right half: bright
    for x in range(W//2, W):
        p = (x - W//2) / (W//2)
        r = int(30 + 200 * p)
        g = int(40 + 180 * p)
        b = int(60 + 200 * p)
        draw.line([(x, 0), (x, H)], fill=(r, g, b))

    # Lightning divider
    pts = [(220, 0), (630, 80), (650, 160), (632, 250), (655, 340), (640, 430), (658, 520), (640, 720)]
    draw.line(pts, fill=(200, 200, 255), width=10)
    draw.line(pts, fill=(255, 255, 255), width=4)

    # Sun on right
    draw.ellipse([(950, 80), (1050, 180)], fill=(255, 230, 80))
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        draw.line([(1000, 130), (1000+70*math.cos(rad), 130+70*math.sin(rad))], fill=(255,240,150), width=3)

    # Face bottom-left
    paste_face_with_stroke(headshot, bg, 15, H-380, stroke_width=8)
    
    # Top text
    font_big = ImageFont.truetype(FONT_PATH, 96)
    font_med = ImageFont.truetype(FONT_PATH, 76)
    text_x = 300
    draw_outlined_text(draw, "ONE-CLICK", (text_x, 40), font_big, (255, 70, 70))
    draw_outlined_text(draw, "REHAB ESTIMATOR", (text_x, 170), font_med, (255, 220, 50))

    bg.save(output_path, quality=95)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python thumbnail_templates.py <headshot_path>")
        sys.exit(1)
    
    headshot = load_headshot(sys.argv[1])
    text = "ONE-CLICK REHAB ESTIMATOR"
    out_dir = "/root/thumbnails"
    os.makedirs(out_dir, exist_ok=True)
    
    template1_warning(headshot, text, f"{out_dir}/thumb1_red.png")
    template2_gold(headshot, text, f"{out_dir}/thumb2_gold.png")
    template3_split(headshot, text, f"{out_dir}/thumb3_split.png")
    
    print("All 3 thumbnails saved to /root/thumbnails/")