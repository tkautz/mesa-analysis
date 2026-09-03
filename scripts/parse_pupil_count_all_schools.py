"""All-school October funded head count AND K-5 grade counts from the BVSD CDE Head Count Summary PDFs (elementary page).
Output: data/clean/bvsd_pupil_count_all_elementary.csv"""
import re, glob
from pathlib import Path
import pandas as pd
rows = []
for txt in sorted(glob.glob("data/raw/bvsd/pupil_count/*_cde_headcount_summary*.txt")):
    sy = Path(txt).name[:7]; text = open(txt, encoding="utf-8").read()
    p1 = re.split(r"\n===== [^\n]+ \| page 2 of", text)[0]
    has_pk = "PRE-K" in p1
    for line in p1.splitlines():
        m = re.match(r"^(?:\d{3} )?([A-Za-z][A-Za-z0-9 .'’&/()-]+?)\s+\*?\s*(\d[\d,]*)\s+(\d[\d,]*)\s+(\d[\d,]*(?:\.\d)?)((?:\s+\d+)*)\s*$", line)
        if not m or m.group(1).strip() == "COUNT COUNT FTE KDG" or re.match(r"(TOTAL|General Fund|Charter Fund|Total)", m.group(1), re.I):
            continue
        g = [int(x) for x in m.group(5).split()]
        r = dict(school_as_printed=m.group(1).strip(), school_year=sy, headcount_prior_year_as_printed=int(m.group(2).replace(",", "")),
                 funded_headcount=int(m.group(3).replace(",", "")), funded_fte=float(m.group(4).replace(",", "")),
                 _source=f"data/raw/bvsd/pupil_count/{Path(txt).name[:-4]}.pdf", _page=1)
        if has_pk and len(g) >= 7: r["PK"] = g[0]; g = g[1:]
        elif has_pk and len(g) == 6: r["PK"] = None
        if len(g) >= 6:
            for k, v in zip(["K", "G1", "G2", "G3", "G4", "G5"], g[:6]): r[k] = v
        rows.append(r)
df = pd.DataFrame(rows)
df["grade_sum_K5"] = df[["K", "G1", "G2", "G3", "G4", "G5"]].sum(axis=1, min_count=6)
df["grade_check"] = (df.grade_sum_K5 + df.PK.fillna(0)) == df.funded_headcount
df.to_csv("data/clean/bvsd_pupil_count_all_elementary.csv", index=False)
print(df.groupby("school_year").agg(n=("school_as_printed", "size"), with_grades=("K", "count"), grade_ok=("grade_check", "sum")).to_string())
print(df[~df.grade_check & df.K.notna()][["school_as_printed", "school_year", "funded_headcount", "PK", "grade_sum_K5"]].head(12).to_string(index=False))
