#!/usr/bin/env python3
"""
Review Poster Script
Checks PDF poster attributes (size, fonts, images) using pypdf.
"""

import sys
import os
import argparse
from pathlib import Path
from math import isclose

try:
    from pypdf import PdfReader
except ImportError:
    print("Error: pypdf not installed. Please install with: uv pip install pypdf")
    sys.exit(1)

def check_poster(pdf_path: Path):
    print(f"\nAnalyzing: {pdf_path.name}")
    print("=" * 40)
    
    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return

    # 1. Page Count
    num_pages = len(reader.pages)
    print(f"Pages: {num_pages}", end="")
    if num_pages == 1:
        print(" (✓ Correct for poster)")
    else:
        print(" (⚠️ Warning: Posters usually have 1 page)")

    # 2. Page Dimensions (in points, 1 inch = 72 pts)
    page = reader.pages[0]
    width_pt = float(page.mediabox.width)
    height_pt = float(page.mediabox.height)
    
    width_in = width_pt / 72.0
    height_in = height_pt / 72.0
    
    # Common sizes
    a0_w, a0_h = 33.1, 46.8
    arch_e_w, arch_e_h = 36.0, 48.0
    
    print(f"Size:  {width_in:.1f}\" x {height_in:.1f}\" ({width_pt:.0f} x {height_pt:.0f} pts)")
    
    if isclose(width_in, a0_w, abs_tol=0.5) and isclose(height_in, a0_h, abs_tol=0.5):
         print("       ✓ Matches A0 size")
    elif isclose(width_in, arch_e_w, abs_tol=0.5) and isclose(height_in, arch_e_h, abs_tol=0.5):
         print("       ✓ Matches Arch E size")
    else:
         print("       ℹ Non-standard size (Verify conference requirements)")

    # 3. File Size
    size_mb = pdf_path.stat().st_size / (1024 * 1024)
    print(f"File:  {size_mb:.2f} MB", end="")
    if size_mb > 20:
        print(" (⚠️ Large file - check image compression)")
    else:
        print(" (✓ Good size)")

    # 4. Fonts (Basic check for embedding)
    # This is a heuristic as pypdf font extraction is complex
    try:
        fonts = set()
        if '/Resources' in page and '/Font' in page['/Resources']:
            font_dict = page['/Resources']['/Font']
            fonts.update(font_dict.keys())
        
        print(f"Fonts: {len(fonts)} detected")
        # In pypdf, checking embedding status is nontrivial without parsing structures
        # We rely on user to check visual output or use Adobe Reader ('Cmd-D' -> Fonts)
        print("       ℹ Open in Adobe Reader (Ctrl+D > Fonts) to verify embedding.")
    except Exception:
        print("       ⚠️ Could not analyze fonts")

    # 5. Images (Heuristic)
    # Extract images to check resolution is expensive and complex in pure python
    # We warn if file size is consistent with high-res images
    print("Images: Visual inspection required.")
    
    print("-" * 40)
    print("Manual Checklist:")
    print("[ ] Zoom to 100% - is text crisp?")
    print("[ ] Check images for pixelation")
    print("[ ] Verify margins (min 0.5 inch)")
    print("[ ] Colors (RGB for screen, CMYK for print)")
    print("=" * 40)

def main():
    parser = argparse.ArgumentParser(description="Review poster PDF")
    parser.add_argument("pdf", help="PDF file to check")
    
    args = parser.parse_args()
    
    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"Error: File '{pdf_path}' not found")
        sys.exit(1)
        
    check_poster(pdf_path)

if __name__ == "__main__":
    main()
