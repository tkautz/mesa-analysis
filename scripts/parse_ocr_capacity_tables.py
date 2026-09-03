"""Turn the OCR row reconstructions of the three capacity-summary pages into a numeric table for ALL schools.
Only integer columns (capacity, enrollment, five projections) are used; OCR'd percent strings are discarded.
Each row is checked: the table's own 'Enroll' value must equal the official BVSD head count for that year
(data/clean/bvsd_pupil_count_all_elementary.csv). Rows failing that check are flagged ocr_check=False.
Mesa / Bear Creek rows are overridden with the visually verified values from build_primary_tables.py.
Output: data/clean/capacity_summary_all_schools_by_vintage.csv
"""
import re, pandas as pd
YEARS = {"feb2024": ("2023-24", ["2024-25", "2025-26", "2026-27", "2027-28", "2028-29"]),
         "feb2025": ("2024-25", ["2025-26", "2026-27", "2027-28", "2028-29", "2029-30"]),
         "feb2026": ("2025-26", ["2026-27", "2027-28", "2028-29", "2029-30", "2030-31"])}
NAME_MAP = {  # OCR table label -> official head-count name (as printed in the 2025-26 file)
 "AspenCreek": "Aspen Creek K-8", "Aspen Creek": "Aspen Creek K-8", "BCSIS-HP": "BCSIS", "BearCreek": "Bear Creek Elementary", "Bear Creek": "Bear Creek Elementary",
 "Birch": "Birch Elementary", "CoalCreek": "Coal Creek Elementary School", "Coal Creek": "Coal Creek Elementary School", "Columbine": "Columbine Elementary School",
 "Montessori": "Community Montessori", "Creekside": "Creekside Elementary at Martin Park", "CrestView": "Crest View Elementary", "Crest View": "Crest View Elementary",
 "Douglass": "Douglass Elementary School", "Eisenhower": "Eisenhower Elementary School", "Eldorado": "Eldorado K-8", "Emerald": "Emerald Elementary School",
 "Fireside": "Fireside Elementary School", "Flatirons": "Flatirons Elementary School", "Foothill": "Foothill Elementary School", "GoldHill": "Gold Hill Elementary School",
 "Gold Hill": "Gold Hill Elementary School", "Heatherwood": "Heatherwood Elementary School", "Jamestown": "Jamestown Elementary School", "Kohl": "Kohl Elementary School",
 "Lafayette": "Lafayette Elementary School", "Louisville": "Louisville Elementary School", "Meadowlark^": "Meadowlark School", "Meadowlark": "Meadowlark School",
 "Mesa": "Mesa Elementary School", "Monarch": "Monarch K-8 School", "Nederland": "Nederland Elementary School", "Pioneer": "Pioneer Elementary School",
 "Ryan": "Ryan Elementary School", "Sanchez": "Alicia Sanchez Elementary School", "Superior": "Superior Elementary School", "UniversityHill": "University Hill Elementary School",
 "University Hill": "University Hill Elementary School", "University Hill (p)": "University Hill Elementary School", "UniversityHill(p)": "University Hill Elementary School",
 "Whittier": "Whittier International Elementary"}
off = pd.read_csv("data/clean/bvsd_pupil_count_all_elementary.csv")
def norm(s): return re.sub(r"[^a-z]", "", str(s).lower())
off["key"] = off.school_as_printed.map(norm)
# alias older printed names to the 2025-26 names (K-5 suffixes etc.)
ALIAS = {"aspencreekk8k5": "aspencreekk8", "eldoradok8k5": "eldoradok8", "monarchk8schoolk5": "monarchk8school", "horizonsk8schoolk5": "horizonsk8school",
         "peaktopeakk12charterk5": "peaktopeakk12charter", "communitymontessori": "communitymontessori", "whittierinternationalelementaryschool": "whittierinternationalelementary",
         "meadowlarkschoolk5": "meadowlarkschool", "meadowlark": "meadowlarkschool", "bcsis": "bcsis"}
off["key"] = off.key.replace(ALIAS)
official = off.groupby(["key", "school_year"]).funded_headcount.first()

rows = []
for vint, (base, projyears) in YEARS.items():
    d = pd.read_csv(f"data/clean/capacity_summary_{vint}_ocr.csv")
    for _, r in d.iterrows():
        label = str(r.school).strip()
        if label not in NAME_MAP: continue
        toks = str(r.tokens).split()
        def as_int(t):
            t2 = t.replace(",", "")
            return int(t2) if re.fullmatch(r"\d{1,4}", t2) else None
        ok_len = len(toks) == 20   # cap, rounds, enroll, pct, rnds, then 5 x (proj, pct, rnds): positional parse
        if ok_len:
            cap, enr = as_int(toks[0]), as_int(toks[2]); projs = [as_int(toks[5 + 3 * k]) for k in range(5)]
            ok_len = cap is not None and enr is not None and all(p is not None for p in projs)
        if not ok_len:
            cap, enr, projs = None, None, [None] * 5
        ints = toks
        key = norm(NAME_MAP[label])
        off_val = official.get((key, base))
        if label == "BCSIS-HP":
            off_val = official.get(("bcsis", base), 0) + official.get(("highpeakselementary", base), 0)
        row = dict(vintage=vint, school=NAME_MAP[label], ocr_label=label, base_year=base, capacity=cap, enroll_base=enr,
                   official_base=off_val, ocr_check=(ok_len and off_val is not None and abs(enr - off_val) <= 2), enroll_exact=(off_val is not None and enr == off_val), min_conf=r.min_conf, n_ints=len(ints))
        for y, p in zip(projyears, projs): row[f"proj_{y}"] = p
        rows.append(row)
out = pd.DataFrame(rows)
# override Mesa / Bear Creek with the visually verified rows
ver = pd.read_csv("data/clean/capacity_summary_mesa_bearcreek_by_vintage.csv")
for vint in YEARS:
    for sch, name in [("Mesa", "Mesa Elementary School"), ("Bear Creek", "Bear Creek Elementary")]:
        v = ver[(ver.vintage == vint) & (ver.school == sch) & (ver.measure == "enrollment")]
        m = (out.vintage == vint) & (out.school == name)
        for _, q in v.iterrows():
            col = "enroll_base" if q.data_type.startswith("actual") else f"proj_{q.school_year}"
            out.loc[m, col] = q.value
        out.loc[m, "ocr_check"] = True; out.loc[m, "verified_visually"] = True
# Feb 2024 p.11 Heatherwood row lost a token in OCR; values read from the rendered page (page_renders/trend_report_feb2024_p11.png)
m = (out.vintage == "feb2024") & (out.school == "Heatherwood Elementary School")
out.loc[m, ["capacity", "enroll_base", "proj_2024-25", "proj_2025-26", "proj_2026-27", "proj_2027-28", "proj_2028-29"]] = [492, 226, 227, 217, 209, 196, 203]
out.loc[m, ["ocr_check", "verified_visually"]] = [True, True]
out["verified_visually"] = out.verified_visually.fillna(False)
out.to_csv("data/clean/capacity_summary_all_schools_by_vintage.csv", index=False)
print(out.groupby("vintage").ocr_check.agg(["sum", "size"]))
print(out[~out.ocr_check][["vintage", "school", "enroll_base", "official_base", "n_ints", "min_conf"]].to_string())
