"""Render Enrollment Pattern Matrix pages to PNG in data/raw/bvsd/page_renders/ for visual checks.

Usage: python scripts/render_matrix_pages.py [year ...]   (default: 2025-26)
Writes <stem>_p1.png at 2.4x scale; never overwrites an existing render.
"""
import sys
from pathlib import Path

import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "bvsd" / "oe_matrices"
OUT = ROOT / "data" / "raw" / "bvsd" / "page_renders"

years = sys.argv[1:] or ["2025-26"]
for yr in years:
    for kind in ["elem", "k"]:
        src = RAW / f"{kind}_matrix_{yr}.pdf"
        dst = OUT / f"{kind}_matrix_{yr}_p1.png"
        if not src.exists() or dst.exists():
            print("skip", dst.name)
            continue
        pdfium.PdfDocument(str(src))[0].render(scale=2.4).to_pil().save(dst)
        print("wrote", dst.relative_to(ROOT))
