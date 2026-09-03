"""District-claims ledger tests that need only data in hand (interrogation plan B1a, B2a, B3b, B4a, B4c, B7b, B9a, B10a).
Outputs: analysis/output/table08_*.csv"""
import sys; sys.path.insert(0, "analysis")
from common import *
import numpy as np, pandas as pd
# ---- B1a / B9a: package-wide post-change ranges from the deck (text layer), 2030-31 and 2027-28 ----
deck = pd.DataFrame([
 # school, capacity, lo27, hi27, lo30, hi30, page
 ("Kohl (receives Birch)", 541, 433, 473, 437, 474, 25), ("Fireside", 516, 427, 436, 421, 430, 37), ("Eldorado K-5", 568, 343, 365, 353, 377, 37), ("Superior", 467, 447, 458, 424, 436, 37),
 ("Coal Creek", 492, 396, 426, 395, 427, 48), ("Eisenhower", 492, 289, 294, 297, 302, 48), ("Heatherwood", 492, 260, 267, 260, 268, 48),
 ("Bear Creek (receives Mesa)", 492, 392, 445, 403, 462, 51), ("Foothill", 565, 488, 497, 484, 492, 54), ("Whittier", 442, 337, 357, 315, 329, 54)],
 columns=["school", "capacity", "lo_2027", "hi_2027", "lo_2030", "hi_2030", "deck_page"])
deck["pct_hi_2030"] = deck.hi_2030 / deck.capacity; deck["pct_lo_2030"] = deck.lo_2030 / deck.capacity
deck["rounds_lo_2030"] = deck.lo_2030 / 150; deck["rounds_hi_2030"] = deck.hi_2030 / 150; deck["seats_left_at_hi_2030"] = deck.capacity - deck.hi_2030
deck["range_width_2030"] = deck.hi_2030 - deck.lo_2030
deck.to_csv(OUT / "table08_package_ranges.csv", index=False); print(deck.round(2).to_string(index=False))
# unchanged Boulder-region and other elementary schools: Feb 2026 projections for 2030-31 (OCR table, checked rows)
cap = pd.read_csv(CLEAN / "capacity_summary_all_schools_by_vintage.csv"); cap = cap[(cap.vintage == "feb2026") & cap.ocr_check]
changed = {"Kohl Elementary School", "Birch Elementary", "Fireside Elementary School", "Eldorado K-8", "Superior Elementary School", "Monarch K-8 School", "Coal Creek Elementary School", "Eisenhower Elementary School",
           "Heatherwood Elementary School", "Douglass Elementary School", "Bear Creek Elementary", "Mesa Elementary School", "Foothill Elementary School", "Whittier International Elementary", "Flatirons Elementary School"}
unch = cap[~cap.school.isin(changed)][["school", "capacity", "proj_2030-31", "enroll_base"]].copy(); unch["rounds_2030"] = unch["proj_2030-31"] / 150
unch.to_csv(OUT / "table08_unchanged_2030.csv", index=False)
below2_unch = int((unch["proj_2030-31"] < 300).sum()); below2_pkg_lo = int((deck.lo_2030 < 300).sum()); below2_pkg_hi = int((deck.hi_2030 < 300).sum())
near2_pkg = deck[(deck.lo_2030 < 320)].school.tolist()
print(f"unchanged schools projected below 300 in 2030-31: {below2_unch} of {len(unch)}: {unch[unch['proj_2030-31'] < 300].school.tolist()}")
print(f"package schools below 300 at low end: {below2_pkg_lo}; at high end: {below2_pkg_hi}; within 20 of the line at low end: {near2_pkg}")
# ---- B2a / B10a: Boulder arithmetic from deck p. 43 / p. 55 / p. 58 ----
b = dict(boulder_pk5_schools_now=16, schools_needed_for_3_rounds_per_deck=10, projected_residents_2030=3522, projected_enrollment_2030=4241, open_seats_now=2585,
         util_now=0.631, util_post=0.679, capacity_reduction_package=1906, mesa_capacity=418)
b["mesa_share_of_capacity_reduction"] = 418 / 1906
b["boulder_capacity_now_implied"] = 2585 / (1 - 0.631)
b["boulder_enrolled_now_implied"] = b["boulder_capacity_now_implied"] * 0.631
b["schools_at_450_from_residents"] = 3522 / 450; b["schools_at_450_from_enrollment"] = 4241 / 450
b["boulder_schools_after_package"] = 16 - 3   # Douglass, Flatirons, Mesa closed; Montessori building closed but school continues
b["util_if_only_mesa_closed"] = b["boulder_enrolled_now_implied"] / (b["boulder_capacity_now_implied"] - 418)
pd.Series(b).to_csv(OUT / "table08_boulder_arithmetic.csv"); print(pd.Series(b).round(3).to_string())
# ---- B3b: equity ----
sp = pd.read_csv(CLEAN / "bvsd_pupil_count_mesa_bearcreek.csv"); sp = sp[(sp.file_family == "special_programs") & (sp.school_year == "2025-26")]
eq = sp.set_index("school")[["funded_headcount", "free_lunch_pct", "reduced_lunch_pct", "SPED_pct", "504_pct", "ELL_pct", "TAG_pct", "hispanic_pct", "caucasian_pct", "out_of_district_pct"]].T
eq.to_csv(OUT / "table08_equity_2025_26.csv"); print(eq.to_string())
# ---- B4a: elementary totals by run (from the capacity tables' total rows, OCR-checked against printed totals) ----
tot = pd.DataFrame([("jan2024", "2023-24", 10074, "2024-25", 9842, "2025-26", 9619, "2026-27", 9506, "2027-28", 9308, "2028-29", 9174, None, None),
                    ("jan2025", "2024-25", 9952, "2025-26", 9825, "2026-27", 9743, "2027-28", 9589, "2028-29", 9444, "2029-30", 9431, None, None),
                    ("jan2026", "2025-26", 9689, "2026-27", 9540, "2027-28", 9367, "2028-29", 9273, "2029-30", 9319, "2030-31", 9408, None, None)],
                   columns=["run", "base_year", "base_total", "y1", "p1", "y2", "p2", "y3", "p3", "y4", "p4", "y5", "p5", "x", "xx"]).drop(columns=["x", "xx"])
long = []
for _, r in tot.iterrows():
    long.append(dict(run=r.run, year=r.base_year, value=r.base_total, kind="actual"))
    for k in range(1, 6): long.append(dict(run=r.run, year=r[f"y{k}"], value=r[f"p{k}"], kind="projection"))
long = pd.DataFrame(long); long.to_csv(OUT / "table08_elementary_totals_by_run.csv", index=False)
piv = long.pivot(index="year", columns="run", values="value"); print(piv.to_string())
# ---- B4c: Mesa district run vs both specs ----
iv = pd.read_csv(OUT / "table03_intervals.csv"); iv = iv[(iv.fall == 2030) & iv.series.str.contains("Mesa|Bear Creek")][["series", "p50"]]
print(iv.to_string(index=False))
# ---- B7b: Heatherwood after entering the engagement phase ----
allsch = load_all_schools(); h = allsch[allsch.school_as_printed.str.contains("Heatherwood")][["school_year", "funded_headcount"]]
print(h.tail(5).to_string(index=False))
