"""All-school October funded head count from the BVSD CDE Head Count Summary PDFs (elementary page only).
Output: data/clean/bvsd_pupil_count_all_elementary.csv  (school as printed, school_year, funded_headcount, prior-year as printed)."""
import re, glob
from pathlib import Path
import pandas as pd
rows = []
for txt in sorted(glob.glob("data/raw/bvsd/pupil_count/*_cde_headcount_summary*.txt")):
    sy = Path(txt).name[:7]; text = open(txt, encoding="utf-8").read()
    p1 = re.split(r"\n===== [^\n]+ \| page 2 of", text)[0]
    for line in p1.splitlines():
        m = re.match(r"^(?:\d{3} )?([A-Za-z][A-Za-z .'’&/()-]+?)\s+\*?\s*(\d[\d,]*)\s+(\d[\d,]*)\s+(\d[\d,]*(?:\.\d)?)\s", line)
        if m and m.group(1).strip() != "COUNT COUNT FTE KDG" and not re.match(r"(TOTAL|General Fund|Charter Fund|Total)", m.group(1), re.I):
            rows.append(dict(school_as_printed=m.group(1).strip(), school_year=sy, headcount_prior_year_as_printed=int(m.group(2).replace(",", "")),
                             funded_headcount=int(m.group(3).replace(",", "")), funded_fte=float(m.group(4).replace(",", "")),
                             _source=f"data/raw/bvsd/pupil_count/{Path(txt).name[:-4]}.pdf", _page=1))
df = pd.DataFrame(rows)
df.to_csv("data/clean/bvsd_pupil_count_all_elementary.csv", index=False)
print(df.groupby("school_year").size().to_string()); print(df[df.school_year == "2025-26"].school_as_printed.tolist())
