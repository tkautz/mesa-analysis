"""Reassemble the image-only 'BVSD Capacity Summary' tables from OCR lines (data/raw/bvsd/page_renders/*.ocr.txt)
by grouping tokens into rows by y-coordinate. FLAGGED AS OCR: numbers must be checked against the page render.
Pages: trend_report_feb2026 p9 (2025-26 summary), trend_report_feb2025 p9 (2024-25), trend_report_feb2024 p11 (2023-24).
Output: data/clean/capacity_summary_<vintage>_ocr.csv (all elementary rows), plus a Mesa/Bear Creek print.
"""
import re, pandas as pd
PAGES = {"feb2026": "trend_report_feb2026_p09", "feb2025": "trend_report_feb2025_p09", "feb2024": "trend_report_feb2024_p11"}
for vint, stem in PAGES.items():
    lines = [l.rstrip("\n") for l in open(f"data/raw/bvsd/page_renders/{stem}.ocr.txt", encoding="utf-8")]
    toks = []
    for l in lines:
        y, x, c, t = int(l[:5]), int(l[6:11]), float(l[12:16]), l[17:]
        toks.append((y, x, c, t))
    # group by y within 14 px
    toks.sort()
    rows, cur, cy = [], [], None
    for y, x, c, t in toks:
        if cy is None or abs(y - cy) <= 14:
            cur.append((x, t, c)); cy = y if cy is None else cy
        else:
            rows.append(sorted(cur)); cur = [(x, t, c)]; cy = y
    rows.append(sorted(cur))
    out = []
    for r in rows:
        first = r[0][1]
        if re.match(r"^[A-Za-z][A-Za-z .\-'^]+$", first) and len(r) > 5:
            # split tokens that OCR glued (e.g. '49263%') is rare; keep raw tokens
            nums = [t for _, t, _ in r[1:]]
            out.append(dict(school=first.strip("^ "), tokens=" ".join(nums), n_tokens=len(nums), min_conf=round(min(c for _, _, c in r), 2)))
    df = pd.DataFrame(out)
    df.to_csv(f"data/clean/capacity_summary_{vint}_ocr.csv", index=False)
    print("####", vint, len(df), "rows")
    print(df[df.school.str.contains("Mesa|Bear|Elementary|Total", case=False)].to_string(index=False))
