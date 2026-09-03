"""Cross-check the two October-count series inside the enrollmentdata repo:
(a) BVSD_October_Headcount_2014-2025.csv and (b) the history arrays embedded in maps/index.html.
Both claim to transcribe the BVSD October pupil count. Output: data/clean/enrollmentdata_internal_check.csv
"""
import pandas as pd, re
csv = pd.read_csv("data/clean/BVSD_October_Headcount_2014-2025.csv")
mp = pd.read_csv("data/clean/enrollmentdata_map_history_all_schools.csv")
mp = mp[mp.level == "elementary"]
def norm(s):
    s = s.upper().replace("ELEMENTARY", "").replace("INTERNATIONAL", "").replace("PK-8", "").replace("ESCUELA BILINGUE ", "")
    return re.sub(r"[^A-Z ]", "", s).strip()
mp["key"] = mp.school.map(norm); csv["key"] = csv.school.map(norm)
m = csv[csv.level == "Elementary"].merge(mp, on=["key", "october_year"], how="outer", suffixes=("_csv", "_map"))
m = m.dropna(subset=["enrollment_csv", "enrollment_map"])
m["diff_map_minus_csv"] = m.enrollment_map - m.enrollment_csv
out = m[["school_csv", "school_map", "october_year", "enrollment_csv", "enrollment_map", "diff_map_minus_csv", "_source_line"]]
out.to_csv("data/clean/enrollmentdata_internal_check.csv", index=False)
print("matched school-years:", len(out), "| mismatches:", (out.diff_map_minus_csv != 0).sum())
print(out[out.diff_map_minus_csv != 0].groupby("school_csv").agg(n=("october_year", "size"), years=("october_year", lambda s: f"{s.min()}-{s.max()}"), min_diff=("diff_map_minus_csv", "min"), max_diff=("diff_map_minus_csv", "max")))
print(out[out.school_csv.isin(["MESA", "BEAR CREEK"])].to_string())
