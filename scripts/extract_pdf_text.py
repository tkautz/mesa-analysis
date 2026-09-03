"""Extract full text of every PDF under data/raw/bvsd/ to a sibling .txt (pdfplumber, page-delimited),
and build data/clean/pdf_page_index.csv: one row per (pdf, page) with page count, char count and
whether the page mentions Mesa / Bear Creek. Pages with zero extractable text are flagged (OCR candidates).
"""
import re, csv, sys
from pathlib import Path
import pdfplumber
rows = []
pdfs = sorted(Path("data/raw/bvsd").rglob("*.pdf"))
for p in pdfs:
    out = p.with_suffix(".txt")
    with pdfplumber.open(p) as pdf, open(out, "w", encoding="utf-8") as f:
        n = len(pdf.pages)
        for i, page in enumerate(pdf.pages, 1):
            try:
                t = page.extract_text() or ""
            except Exception as e:
                t = f"[extract_text failed: {e}]"
            f.write(f"\n===== {p.name} | page {i} of {n} =====\n{t}\n")
            rows.append(dict(pdf=str(p), page=i, n_pages=n, chars=len(t),
                             mentions_mesa=bool(re.search(r"\bMesa\b", t)),
                             mentions_bear_creek=bool(re.search(r"Bear\s*Creek", t, re.I)),
                             no_text=(len(t.strip()) == 0)))
    print(f"{n:4d} pages  {p}", file=sys.stderr)
with open("data/clean/pdf_page_index.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
