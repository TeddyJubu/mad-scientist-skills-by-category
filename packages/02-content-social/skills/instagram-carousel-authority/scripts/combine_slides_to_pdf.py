#!/usr/bin/env python3
"""
Combine individual carousel slide PNGs into a single PDF.
Usage: python3 combine_slides_to_pdf.py [slides_directory] [output.pdf]
"""

import sys
import os
from pathlib import Path
from PIL import Image

def combine_slides_to_pdf(slides_dir='.', output_pdf='carousel_final.pdf'):
    """
    Find all slide_*.png files in directory and combine into PDF.
    """
    slides_path = Path(slides_dir)
    
    # Find all slide PNG files and sort them
    slide_files = sorted(slides_path.glob('slide_*.png'))
    
    if not slide_files:
        print(f"❌ No slide_*.png files found in {slides_dir}")
        return False
    
    print(f"Found {len(slide_files)} slides:")
    for slide in slide_files:
        print(f"  - {slide.name}")
    
    # Open all images
    images = []
    for slide_file in slide_files:
        try:
            img = Image.open(slide_file)
            # Convert to RGB if needed (PDF doesn't support RGBA)
            if img.mode == 'RGBA':
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[3])  # Use alpha channel as mask
                images.append(rgb_img)
            else:
                images.append(img.convert('RGB'))
        except Exception as e:
            print(f"⚠️  Error loading {slide_file}: {e}")
    
    if not images:
        print("❌ No valid images to combine")
        return False
    
    # Save as PDF
    try:
        images[0].save(
            output_pdf,
            'PDF',
            save_all=True,
            append_images=images[1:],
            resolution=100.0
        )
        print(f"✅ PDF created: {output_pdf} ({len(images)} pages)")
        return True
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        return False

def main():
    if len(sys.argv) > 1:
        slides_dir = sys.argv[1]
    else:
        slides_dir = '.'
    
    if len(sys.argv) > 2:
        output_pdf = sys.argv[2]
    else:
        output_pdf = 'carousel_final.pdf'
    
    combine_slides_to_pdf(slides_dir, output_pdf)

if __name__ == '__main__':
    main()
