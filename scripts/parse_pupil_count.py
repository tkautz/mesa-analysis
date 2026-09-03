"""Parse BVSD October pupil count PDFs (data/raw/bvsd/pupil_count/*.txt, pdfplumber text) for Mesa and
Bear Creek. Three file families per year:
  *_cde_headcount_summary  -> funded head count (prior yr, current yr), funded FTE, PK (2014-2022 only), K..5
  *_fte_summary            -> funded FTE (prior, current), head count, FTE by grade
  *_special_programs_summary -> ELL, Free, Reduced, SPED, 504, TAG, Out of District (#,%), gender, race
Output: data/clean/bvsd_pupil_count_mesa_bearcreek.csv (one row per school x year x file family), all actuals.
"""
import re, glob
from pathlib import Path
import pandas as pd

SCHOOLS = {"Mesa": r"^(?:166 )?Mesa Elementary(?: School)?", "Bear Creek": r"^(?:119 )?Bear Creek Elementary"}
rows = []
def num(s):
    s = s.replace(",", "").rstrip("%")
    return float(s) if re.fullmatch(r"-?\d+(\.\d+)?", s) else None

for txt in sorted(glob.glob("data/raw/bvsd/pupil_count/*.txt")):
    name = Path(txt).name
    sy = name[:7]
    fam = ("headcount" if "headcount" in name else "fte" if "fte" in name else "special_programs")
    text = open(txt, encoding="utf-8").read()
    pages = re.split(r"\n===== [^\n]+ \| page (\d+) of \d+ =====\n", text)
    # header facts
    m = re.search(r"(October \d+, \d{4})", text); count_date = m.group(1) if m else ""
    m = re.search(r"(?:Updated|Printed): ?(\d{1,2}/\d{1,2}/\d{4})", text); updated = m.group(1) if m else ""
    has_pk = bool(re.search(r"PRE-K", text)) and fam == "headcount"
    for i in range(1, len(pages), 2):
        pg, body = int(pages[i]), pages[i + 1]
        for sch, pat in SCHOOLS.items():
            for line in body.splitlines():
                if re.match(pat, line, re.I):
                    toks = re.sub(pat, "", line, flags=re.I).split()
                    vals = [num(t) for t in toks]
                    r = dict(school=sch, school_year=sy, file_family=fam, count_date=count_date, file_updated=updated,
                             _source=f"data/raw/bvsd/pupil_count/{name[:-4]}.pdf", _page=pg, _raw_line=line.strip())
                    if fam == "headcount":
                        r.update(headcount_prior_year_as_printed=vals[0], funded_headcount=vals[1], funded_fte=vals[2])
                        g = vals[3:]
                        if has_pk: r["PK"] = g[0]; g = g[1:]
                        for k, v in zip(["K", "G1", "G2", "G3", "G4", "G5"], g): r[k] = v
                    elif fam == "fte":
                        r.update(fte_prior_year_as_printed=vals[0], funded_fte=vals[1], funded_headcount=vals[2])
                        for k, v in zip(["K", "G1", "G2", "G3", "G4", "G5"], vals[3:]): r[f"fte_{k}"] = v
                    else:
                        # headcount, fte, then 16 (# %) pairs
                        r.update(funded_headcount=vals[0], funded_fte=vals[1])
                        labels = ["ELL", "free_lunch", "reduced_lunch", "SPED", "504", "TAG", "out_of_district", "female", "male",
                                  "american_indian", "asian", "african_american", "hispanic", "caucasian", "native_hawaiian", "multi"]
                        pairs = vals[2:]
                        for j, lab in enumerate(labels):
                            if 2 * j + 1 < len(pairs):
                                r[f"{lab}_n"] = pairs[2 * j]; r[f"{lab}_pct"] = pairs[2 * j + 1]
                    rows.append(r)
df = pd.DataFrame(rows).sort_values(["school", "school_year", "file_family"])
df.to_csv("data/clean/bvsd_pupil_count_mesa_bearcreek.csv", index=False)
hc = df[df.file_family == "headcount"]
print(hc[["school", "school_year", "count_date", "headcount_prior_year_as_printed", "funded_headcount", "funded_fte", "PK", "K", "G1", "G2", "G3", "G4", "G5"]].to_string(index=False))
sp = df[df.file_family == "special_programs"]
print(sp[["school", "school_year", "funded_headcount", "out_of_district_n", "out_of_district_pct", "free_lunch_pct", "SPED_pct", "ELL_pct"]].to_string(index=False))
# grade-sum check
hc2 = hc.copy(); hc2["gsum"] = hc2[["PK", "K", "G1", "G2", "G3", "G4", "G5"]].sum(axis=1)
print("grade-sum mismatches:", hc2[hc2.gsum != hc2.funded_headcount][["school", "school_year", "funded_headcount", "gsum"]].to_string(index=False))
# prior-year-as-printed vs previous file's current
piv = hc.pivot(index="school_year", columns="school", values="funded_headcount")
prior = hc.pivot(index="school_year", columns="school", values="headcount_prior_year_as_printed")
print("prior-year revisions (printed prior minus previous file's current):"); print((prior - piv.shift(1)).dropna().to_string())
