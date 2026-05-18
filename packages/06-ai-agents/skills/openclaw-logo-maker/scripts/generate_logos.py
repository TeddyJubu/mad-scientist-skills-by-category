#!/usr/bin/env python3
"""
OpenCLAW Logo Maker — generate_logos.py
Generates 10 professional logo variations using Google Gemini 3.1 Flash Preview API.

Usage:
    python generate_logos.py \
        --brand "Brand Name" \
        --industry "Industry/Niche" \
        --colors "Primary Colors" \
        --personality "Brand Personality" \
        --tagline "Optional Tagline" \
        --output outputs/brand-v1
"""

import argparse
import os
import sys
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw

# Check for google-genai
try:
    from google import genai
except ImportError:
    print("ERROR: google-genai not installed. Run: pip install google-genai pillow")
    sys.exit(1)


# =============================================================================
# LOGO PROMPT TEMPLATES — 10 Distinct Styles
# =============================================================================

def build_prompts(brand: str, industry: str, colors: str, personality: str,
                  tagline: str = "") -> list[dict]:
    """
    Build 10 distinct logo prompt templates for the brand.
    Returns list of dicts with: name, style_name, prompt, transparent_prompt
    """

    # Derive abbreviation from brand if not provided
    abbrev = "".join([w[0] for w in brand.split() if w[0].isupper()]) or brand[:3].upper()
    tagline_line = f'\nTagline: "{tagline}"' if tagline else ""

    prompts = []

    # -------------------------------------------------------------------------
    # STYLE 1: 3D Premium
    # -------------------------------------------------------------------------
    style_name = "3D-Premium"
    prompts.append({
        "name": style_name,
        "prompt": (
            f"Design a premium 3D logo for {brand}, a {industry} brand. "
            f"Personality: {personality}. "
            f"Colors: {colors} — use rich, dimensional gradients with gold/platinum highlights. "
            f"Style: Sophisticated 3D rendering with subtle depth, soft shadows, polished surfaces, "
            f"and a modern luxury tech aesthetic. "
            f"Composition: Clean, centered, professional. "
            f"Background: Fully transparent. "
            f"Format: Square aspect ratio, centered logo mark with or without wordmark. "
            f"Quality: Ultra-high resolution, photorealistic material rendering, premium finish.{tagline_line}"
        ),
    })

    # -------------------------------------------------------------------------
    # STYLE 2: Dynamic Gradient
    # -------------------------------------------------------------------------
    style_name = "Dynamic-Gradient"
    prompts.append({
        "name": style_name,
        "prompt": (
            f"Design a bold dynamic gradient logo for {brand}, a {industry} brand. "
            f"Personality: {personality}. "
            f"Colors: {colors} — bold, energetic gradient transitions from deep to bright tones. "
            f"Style: Forward-motion feel, sleek modern flow, energetic but professional. "
            f"Consider abstract swooshes, motion trails, or layered shapes with seamless color blends. "
            f"Background: Fully transparent. "
            f"Format: Square aspect ratio. "
            f"Quality: Crisp vector-like clarity, high-energy visual impact.{tagline_line}"
        ),
    })

    # -------------------------------------------------------------------------
    # STYLE 3: Geometric Abstract
    # -------------------------------------------------------------------------
    style_name = "Geometric-Abstract"
    prompts.append({
        "name": style_name,
        "prompt": (
            f"Design a geometric abstract logo for {brand}, a {industry} brand. "
            f"Personality: {personality}. "
            f"Colors: {colors} — use with precision and intentionality. "
            f"Style: Clean geometric shapes — triangles, hexagons, intersecting lines, "
            f"polygons, or tessellated patterns. Mathematical precision, minimalist execution. "
            f"The logo should feel intelligent, structured, and forward-thinking. "
            f"Background: Fully transparent. "
            f"Format: Square aspect ratio. "
            f"Quality: Sharp edges, perfect alignment, professional minimalism.{tagline_line}"
        ),
    })

    # -------------------------------------------------------------------------
    # STYLE 4: Luxury Minimal
    # -------------------------------------------------------------------------
    style_name = "Luxury-Minimal"
    prompts.append({
        "name": style_name,
        "prompt": (
            f"Design a luxury minimal logo for {brand}, a {industry} brand. "
            f"Personality: {personality}. "
            f"Colors: {colors} — muted gold, charcoal, cream, or sophisticated dark tones. "
            f"Style: Understated elegance, thin clean lines, maximum whitespace, "
            f"refined typography, premium feel without being loud. "
            f"Think high-end fashion house or private bank aesthetic. "
            f"Background: Fully transparent. "
            f"Format: Square aspect ratio, wordmark with subtle icon or icon-only mark. "
            f"Quality: Elegant restraint, flawless typography, timeless design.{tagline_line}"
        ),
    })

    # -------------------------------------------------------------------------
    # STYLE 5: Modern Flat
    # -------------------------------------------------------------------------
    style_name = "Modern-Flat"
    prompts.append({
        "name": style_name,
        "prompt": (
            f"Design a modern flat logo for {brand}, a {industry} brand. "
            f"Personality: {personality}. "
            f"Colors: {colors} — clean, bold, two-tone or three-tone palette. "
            f"Style: Clean 2D illustration, solid fills, no gradients, no shadows, "
            f"highly scalable, works from favicon to billboard. "
            f"Friendly yet professional, approachable yet credible. "
            f"Background: Fully transparent. "
            f"Format: Square aspect ratio. "
            f"Quality: Pixel-perfect at any size, vector-clean execution.{tagline_line}"
        ),
    })

    # -------------------------------------------------------------------------
    # STYLE 6: Futuristic Tech
    # -------------------------------------------------------------------------
    style_name = "Futuristic-Tech"
    prompts.append({
        "name": style_name,
        "prompt": (
            f"Design a futuristic tech logo for {brand}, a {industry} brand. "
            f"Personality: {personality}. "
            f"Colors: {colors} — neon accents on dark, or sharp bright tones on white. "
            f"Style: Sharp angles, circuit-inspired line work, circuit board motifs, "
            f"data stream aesthetics, AI/tech energy. The logo should feel like it belongs "
            f"to a cutting-edge AI or deep tech company. "
            f"Background: Fully transparent. "
            f"Format: Square aspect ratio. "
            f"Quality: Precision line work, technical aesthetic, high-tech visual language.{tagline_line}"
        ),
    })

    # -------------------------------------------------------------------------
    # STYLE 7: Iconic Monogram
    # -------------------------------------------------------------------------
    style_name = "Iconic-Monogram"
    prompts.append({
        "name": style_name,
        "prompt": (
            f"Design an iconic monogram logo for {brand}, a {industry} brand. "
            f"Personality: {personality}. "
            f"Colors: {colors} — use with sophistication. "
            f"Style: Elegant letter-based mark using initials or a stylized letterform. "
            f"Think luxury fashion house monogram but adapted for {industry}. "
            f"Interlocking letters, negative space, or layered typography. "
            f"Should be instantly recognizable as a symbol. "
            f"Background: Fully transparent. "
            f"Format: Square aspect ratio, icon-focused with or without wordmark. "
            f"Quality: Flawless letterform, elegant curves, timeless mark.{tagline_line}"
        ),
    })

    # -------------------------------------------------------------------------
    # STYLE 8: Nature-Inspired
    # -------------------------------------------------------------------------
    style_name = "Nature-Inspired"
    prompts.append({
        "name": style_name,
        "prompt": (
            f"Design a nature-inspired logo for {brand}, a {industry} brand. "
            f"Personality: {personality}. "
            f"Colors: {colors} — earth tones, organic greens, warm browns, or stylized natural palette. "
            f"Style: Organic shapes, leaf motifs, subtle botanical elements, "
            f"flowing curves, growth imagery. Professional, not whimsical — "
            f"think premium sustainable brand, not gardening catalog. "
            f"Background: Fully transparent. "
            f"Format: Square aspect ratio. "
            f"Quality: Organic fluidity, natural elegance, premium organic aesthetic.{tagline_line}"
        ),
    })

    # -------------------------------------------------------------------------
    # STYLE 9: Heritage-Classic
    # -------------------------------------------------------------------------
    style_name = "Heritage-Classic"
    prompts.append({
        "name": style_name,
        "prompt": (
            f"Design a heritage classic logo for {brand}, a {industry} brand. "
            f"Personality: {personality}. "
            f"Colors: {colors} — traditional palette: navy, burgundy, gold, cream, forest green. "
            f"Style: Traditional, established, trustworthy. Think iconic financial institution "
            f"or century-old professional firm. Emblems, crests, or refined traditional wordmark. "
            f"Strong typographic hierarchy, timeless layout. "
            f"Background: Fully transparent. "
            f"Format: Square aspect ratio. "
            f"Quality: Timeless design, old-money credibility, refined craftsmanship feel.{tagline_line}"
        ),
    })

    # -------------------------------------------------------------------------
    # STYLE 10: Abstract Dynamic
    # -------------------------------------------------------------------------
    style_name = "Abstract-Dynamic"
    prompts.append({
        "name": style_name,
        "prompt": (
            f"Design an abstract dynamic logo for {brand}, a {industry} brand. "
            f"Personality: {personality}. "
            f"Colors: {colors} — vibrant, trend-forward palette. "
            f"Style: Custom blend of modern design trends — glitch effects, isometric shapes, "
            f"liquid gradients, or collage-style composition. High energy, creative, stands out. "
            f"The most unique and distinctive of all variations — a true conversation piece. "
            f"Background: Fully transparent. "
            f"Format: Square aspect ratio. "
            f"Quality: Bold, distinctive, trend-forward, memorable.{tagline_line}"
        ),
    })

    return prompts


# =============================================================================
# IMAGE GENERATION — Gemini API
# =============================================================================

def generate_image(client, model: str, prompt: str, output_path: str) -> bool:
    """Generate a single logo image using Gemini API."""
    try:
        response = client.models.generate_content(
            model=model,
            contents=[{"role": "user", "parts": [{"text": prompt}]}]
        )
        # Extract image from response
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    img_data = part.inline_data.data
                    mime_type = part.inline_data.mime_type
                    ext = 'png' if 'png' in mime_type else 'jpg'
                    img_path = output_path.replace('.png', f'.{ext}')
                    with open(img_path, 'wb') as f:
                        f.write(img_data)
                    print(f"  ✓ Generated: {img_path}")
                    return img_path, True
            # Check for text parts (error or refusal)
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'text') and part.text:
                    print(f"  ✗ API returned text instead of image: {part.text[:200]}")
                    return "", False
        print(f"  ✗ No image data in response")
        return False
    except Exception as e:
        print(f"  ✗ Generation failed: {str(e)[:150]}")
        return "", False


# =============================================================================
# POST-PROCESSING — Background Variants
# =============================================================================

def create_white_bg_version(input_path: str) -> str:
    """
    Create a white-background version of a logo image (PNG or JPG).
    Always outputs PNG format for consistency.
    Returns path to the new file, or empty string on failure.
    """
    try:
        import re
        img = Image.open(input_path).convert("RGBA")
        white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        white_bg.paste(img, (0, 0), img)  # Paste using alpha as mask
        # Strip the '-transparent' suffix and any extension, then append '-white-bg.png'
        base = re.sub(r'-transparent(\.\w+)$', '', input_path)
        white_path = f"{base}-white-bg.png"
        white_bg.convert("RGB").save(white_path, "PNG", quality=95)
        print(f"  ✓ White bg: {white_path}")
        return white_path
    except Exception as e:
        print(f"  ✗ White bg creation failed: {e}")
        return ""


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="OpenCLAW Logo Maker — Generate 10 Logo Variations")
    parser.add_argument("--brand", required=True, help="Brand / Company Name")
    parser.add_argument("--industry", required=True, help="Industry / Niche")
    parser.add_argument("--colors", required=True, help="Primary Color(s)")
    parser.add_argument("--personality", required=True, help="Brand Personality")
    parser.add_argument("--tagline", default="", help="Optional tagline")
    parser.add_argument("--abbrev", default="", help="Optional abbreviation")
    parser.add_argument("--output", required=True, help="Output directory path")
    parser.add_argument("--model", default="gemini-3.1-flash-image-preview",
                        help="Gemini model name (default: gemini-3.1-flash-image-preview)")
    args = parser.parse_args()

    brand = args.brand
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n🎨 OpenCLAW Logo Maker")
    print(f"   Brand: {brand}")
    print(f"   Industry: {args.industry}")
    print(f"   Colors: {args.colors}")
    print(f"   Personality: {args.personality}")
    print(f"   Tagline: {args.tagline or '(none)'}")
    print(f"   Output: {output_dir}")
    print(f"   Model: {args.model}")
    print("=" * 60)

    # -------------------------------------------------------------------------
    # Initialize Gemini Client
    # -------------------------------------------------------------------------
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        # Try loading from .secrets/gemini.env
        secrets_file = Path.home() / ".openclaw" / "workspace" / ".secrets" / "gemini.env"
        if secrets_file.exists():
            with open(secrets_file) as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        api_key = line.split("=", 1)[1].strip()
                        break

    if not api_key:
        print("ERROR: GEMINI_API_KEY not found.")
        print("Set it with: export GEMINI_API_KEY='your-key'")
        print("Or save it in: ~/.openclaw/workspace/.secrets/gemini.env")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    # -------------------------------------------------------------------------
    # Build Prompts
    # -------------------------------------------------------------------------
    prompts_data = build_prompts(
        brand=brand,
        industry=args.industry,
        colors=args.colors,
        personality=args.personality,
        tagline=args.tagline
    )

    # -------------------------------------------------------------------------
    # Generate All 10 Logos
    # -------------------------------------------------------------------------
    print(f"\n🚀 Generating {len(prompts_data)} logo variations...\n")

    generated = []
    failed = []

    for i, item in enumerate(prompts_data, 1):
        print(f"[{i}/10] {item['name']}...")
        safe_name = item['name'].lower().replace(" ", "-")
        out_path = str(output_dir / f"{safe_name}-transparent.png")

        actual_path, success = generate_image(client, args.model, item['prompt'], out_path)

        if success:
            # Create white-bg version using the actual file path (may differ from requested path)
            white_path = create_white_bg_version(actual_path)
            generated.append(actual_path)
            if white_path:
                generated.append(white_path)
        else:
            failed.append(item['name'])

    # -------------------------------------------------------------------------
    # Package into ZIP
    # -------------------------------------------------------------------------
    zip_path = str(output_dir.parent / f"{output_dir.name}.zip")
    print(f"\n📦 Packaging into ZIP...")

    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in generated:
                if Path(file_path).exists():
                    zf.write(file_path, Path(file_path).name)
                    print(f"  ✓ Added: {Path(file_path).name}")
        print(f"  ✓ ZIP created: {zip_path}")
    except Exception as e:
        print(f"  ✗ ZIP creation failed: {e}")

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print(f"✅ COMPLETE — {len(generated)} files generated")
    print(f"   ZIP: {zip_path}")
    print(f"   Individual files: {output_dir}/")
    if failed:
        print(f"   ⚠ Failed ({len(failed)}): {', '.join(failed)}")
    print("=" * 60)

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
