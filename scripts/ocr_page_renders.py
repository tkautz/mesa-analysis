"""OCR the image-only pages rendered to data/raw/bvsd/page_renders/*.png with rapidocr-onnxruntime.
Output: one .ocr.txt per PNG (text lines with bounding-box y/x so table rows can be reassembled) and
data/clean/ocr_page_lines.csv. FLAG: OCR output; verify against the rendered image before use.
"""
import glob, csv, sys
from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()
rows = []
for png in sorted(glob.glob("data/raw/bvsd/page_renders/*.png")):
    res, _ = ocr(png)
    res = res or []
    lines = []
    for box, text, conf in res:
        x = min(pt[0] for pt in box); y = min(pt[1] for pt in box)
        lines.append((round(y), round(x), text, float(conf)))
    lines.sort()
    with open(png[:-4] + ".ocr.txt", "w") as f:
        for y, x, t, c in lines:
            f.write(f"{y:5d} {x:5d} {c:.2f} {t}\n")
            rows.append(dict(png=png, y=y, x=x, conf=round(c, 3), text=t))
    print(png, len(lines), "lines", file=sys.stderr)
with open("data/clean/ocr_page_lines.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["png", "y", "x", "conf", "text"]); w.writeheader(); w.writerows(rows)
