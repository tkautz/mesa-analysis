"""§S1 The bridge from residents to enrollment, on the district's own Enrollment Pattern Matrix.

Identity (five terms, all observable in the matrix for 2017-18 … 2025-26):
    enrollment at the two schools = residents of the four areas that form the proposed combined area x combined-area capture
                                    + in-district choice from outside the area + out-of-district + placements (+ unmatched)
Applied to the deck's own resident projections (p. 51: 473 in 2027-28, 522 in 2030-31) at the 2025-26 pattern, and inverted to show
what capture rate or what external-seat count the proposal's ranges (392-445, 403-462) require. A policy re-expression: under
JECC-R open enrollment lasts for the school level, so "managing choice" acts on new entrants only; the table shows external seats
under a halt or a cap on new external admissions from 2027-28.
Inputs: data/clean/oe_matrix_*.csv (scripts/parse_oe_matrices.py), raw 2025-26 matrix text (destinations), deck p. 51.
Outputs: analysis/output/table14_bridge.csv, table14_capture_history.csv, table14_destinations.csv, table14_new_entrants.csv;
         figures/fig16_bridge.*, fig17_capture_history.*"""
import sys, re; sys.path.insert(0, "analysis")
from common import *
import numpy as np, pandas as pd, matplotlib.pyplot as plt
style()

ident = pd.read_csv(CLEAN / "oe_matrix_combined_area_identity.csv")
elem = ident[ident.matrix == "elem"].sort_values("year").reset_index(drop=True)
today = elem[elem.year == "2025-26"].iloc[0]
CAP = today.combined_area_capture                      # 0.827
EXT_ID = int(today.external_in_district_choice)        # 75
OOD = int(today.out_of_district)                       # 23
PLC = int(today.placements)                            # 23
UNM = int(today.unmatched)                             # 0
EXT = EXT_ID + OOD + PLC + UNM                         # 121
RES_TODAY = int(today.residents_combined_area)         # 502
ENR_TODAY = int(today.enrollment_both)                 # 536
assert round(RES_TODAY * CAP) + EXT == ENR_TODAY or abs(RES_TODAY * CAP + EXT - ENR_TODAY) < 1
RESIDENTS = {2027: 473.0, 2030: 522.0}                 # deck p. 51
RANGE = {2027: (392, 445), 2030: (403, 462)}           # deck p. 51
CAPACITY = 492; THREE = 450
print(f"2025-26 pattern: residents {RES_TODAY}, attending BC or Mesa {int(today.residents_attending_bc_or_mesa)} ({CAP:.1%}), "
      f"external {EXT} = {EXT_ID} in-district + {OOD} out-of-district + {PLC} placements + {UNM} unmatched; enrollment {ENR_TODAY}")

# ---- bridge table ----
rows = []
for fall, R in RESIDENTS.items():
    lo, hi = RANGE[fall]
    res_att = R * CAP; tot = res_att + EXT
    row = dict(fall=fall, residents_deck=R, capture_2025_26=CAP, residents_attending=res_att, external_in_district=EXT_ID, out_of_district=OOD,
               placements=PLC, external_total=EXT, enrollment_today_pattern=tot, range_lo=lo, range_hi=hi, capacity=CAPACITY)
    for tgt, lab in [(lo, "lo"), (hi, "hi"), (THREE, "450"), (CAPACITY, "492")]:
        row[f"capture_needed_{lab}_ext_held"] = (tgt - EXT) / R
        row[f"external_needed_{lab}_capture_held"] = tgt - res_att
        row[f"external_cut_{lab}_capture_held"] = EXT - (tgt - res_att)
    rows.append(row)
bridge = pd.DataFrame(rows); bridge.to_csv(OUT / "table14_bridge.csv", index=False)
print(bridge.round(3).T.to_string())

# ---- capture history ----
hist = elem[["year", "residents_combined_area", "residents_attending_bc_or_mesa", "combined_area_capture", "own_school_capture", "crossflow_between_the_two",
             "external_in_district_choice", "out_of_district", "placements", "unmatched", "enrollment_both"]].copy()
hist["external_total"] = hist.external_in_district_choice + hist.out_of_district + hist.placements + hist.unmatched
hist["enrollment_at_522_residents_this_pattern"] = 522 * hist.combined_area_capture + hist.external_total
hist.to_csv(OUT / "table14_capture_history.csv", index=False); print(hist.round(3).to_string(index=False))
cap_min, cap_max = hist.combined_area_capture.min(), hist.combined_area_capture.max()
need_lo, need_hi = bridge.loc[bridge.fall == 2030, "capture_needed_lo_ext_held"].iloc[0], bridge.loc[bridge.fall == 2030, "capture_needed_hi_ext_held"].iloc[0]
print(f"capture observed 2017-18..2025-26: {cap_min:.1%} to {cap_max:.1%}; needed for 403-462 at {EXT} external seats: {need_lo:.1%} to {need_hi:.1%}")

# ---- where residents of the four areas attend (all school rows of the 2025-26 matrix) ----
AREAS = ["Bear Creek", "Columbine", "Creekside", "Crest View", "Douglass", "Eisenhower", "Flatirons", "Foothill", "Heatherwood", "Mesa", "Whittier",
         "Optional Bear Creek/Creekside", "Optional Bear Creek/Mesa", "Aspen Creek K-8", "Birch", "Emerald", "Kohl", "Lafayette", "Ryan", "Sanchez",
         "Meadowlark", "Coal Creek", "Fireside", "Louisville", "Monarch K-8", "Eldorado K-8", "Superior", "Gold Hill", "Jamestown", "Nederland"]
SOUTH = ["Bear Creek", "Mesa", "Optional Bear Creek/Creekside", "Optional Bear Creek/Mesa"]
SCHOOLS = ["Bear Creek", "Columbine", "Creekside", "Crest View", "Douglass", "Eisenhower", "Flatirons", "Foothill", "Heatherwood", "Mesa", "Whittier",
           "Aspen Creek K-8", "Birch", "Emerald", "Kohl", "Lafayette Elem.", "Ryan", "Sanchez", "Meadowlark", "Coal Creek", "Fireside", "Louisville Elem.",
           "Monarch K-8", "Eldorado K-8", "Superior", "Gold Hill", "Jamestown", "Nederland Elem.", "BCSIS", "Boulder Universal", "Halcyon", "High Peaks",
           "Comm. Montessori", "Uni-Hill Int.", "Pioneer", "Horizons", "Peak to Peak"]
raw = (ROOT / "data/raw/bvsd/oe_matrices/elem_matrix_2025-26.txt").read_text(encoding="utf-8")
dest = {}
for line in raw.splitlines():
    for s in SCHOOLS:
        m = re.match(rf"^(?:[a-zA-Z] )*{re.escape(s)}\s\*?\s?((?:\d+ ){{30}})", line)
        if m:
            dest[s] = [int(x) for x in m.group(1).split()]
tab = pd.DataFrame(dest, index=AREAS).T
d_rows = []
for area in SOUTH:
    col = tab[area]
    for s, v in col[col > 0].sort_values(ascending=False).items():
        kind = "own school" if s in ("Bear Creek", "Mesa") else ("focus/charter" if s in ("BCSIS", "High Peaks", "Comm. Montessori", "Uni-Hill Int.", "Horizons", "Peak to Peak", "Pioneer", "Boulder Universal", "Halcyon") else "other neighborhood school")
        d_rows.append(dict(area=area, attends=s, students=int(v), kind=kind))
dests = pd.DataFrame(d_rows); dests.to_csv(OUT / "table14_destinations.csv", index=False)
summ = dests.groupby(["area", "kind"]).students.sum().unstack(fill_value=0)
print(summ.to_string())
mesa_leavers = dests[(dests.area == "Mesa") & (dests.attends != "Mesa")]
print("Mesa-area residents attending elsewhere:", int(mesa_leavers.students.sum()), "of which at Bear Creek:", int(mesa_leavers[mesa_leavers.attends == "Bear Creek"].students.sum()))

# ---- new-entrant re-expression on the district's own transition rules ----
# Policy JECC: open enrollment granted lasts for the school level (elementary), "unless school assignment ... necessitates adjustments";
# JECC-R sets the lottery preferences. Deck p. 63: in-district students at a closed school are placed in their new neighborhood school,
# or may apply through open enrollment with a one-year first priority; out-of-district students must apply through open enrollment;
# offers "depend on available space". So: Bear Creek's own outside students (in-district from outside the four areas + out-of-district)
# continue and age out one grade a year (approximation: one sixth per grade); the 23 placements persist (the programs move to Bear Creek);
# Mesa's non-resident students (in-district outside the area + out-of-district) have no automatic seat and are shown both ways;
# new outside admissions are capped at N per year.
rows_sch = elem_rows = pd.read_csv(CLEAN / "oe_matrix_school_summary_mesa_bearcreek.csv"); rows_sch = rows_sch[(rows_sch.year == "2025-26") & (rows_sch.matrix == "elem")].set_index("school")
by_area = pd.read_csv(CLEAN / "oe_matrix_school_by_area_mesa_bearcreek.csv"); by_area = by_area[(by_area.year == "2025-26") & (by_area.matrix == "elem")]
SOUTH4 = ["Bear Creek", "Mesa", "Optional Bear Creek/Creekside", "Optional Bear Creek/Mesa"]
def outside_in_district(school):   # students at the school living outside the four areas (in-district)
    g = by_area[by_area.school == school]; return int(g.students.sum() - g[g.area.isin(SOUTH4)].students.sum())
BC_OUT = outside_in_district("Bear Creek") + int(rows_sch.loc["Bear Creek", "oe_out_of_district"])     # 43 + 13 = 56
MESA_OUT = outside_in_district("Mesa") + int(rows_sch.loc["Mesa", "oe_out_of_district"])              # 32 + 10 = 42
print(f"Bear Creek outside students (in-district from outside the area + out-of-district): {BC_OUT}; Mesa: {MESA_OUT}; placements {PLC}")
ne = []
for cap_new in (0, 10, 20):
    for mesa_readmitted in (False, True):
        for fall in (2027, 2030):
            yrs_since = fall - 2026
            bc_remaining = BC_OUT * max(0, 6 - yrs_since) / 6.0
            mesa_remaining = MESA_OUT * max(0, 6 - yrs_since) / 6.0 if mesa_readmitted else 0.0
            ext = bc_remaining + PLC + mesa_remaining + cap_new * yrs_since
            R = RESIDENTS[fall]
            ne.append(dict(new_outside_admissions_per_year=cap_new, mesa_nonresidents_readmitted=mesa_readmitted, fall=fall, residents=R, residents_attending=R * CAP,
                           bear_creek_outside_remaining=bc_remaining, placements=PLC, mesa_nonresidents_remaining=mesa_remaining, new_admissions=cap_new * yrs_since,
                           outside_total=ext, enrollment=R * CAP + ext, range_lo=RANGE[fall][0], range_hi=RANGE[fall][1]))
ne = pd.DataFrame(ne); ne.to_csv(OUT / "table14_new_entrants.csv", index=False)
print(ne.round(1).to_string(index=False))

# ---- Fig 16: bridge (waterfall), two panels ----
fig, axes = plt.subplots(1, 2, figsize=(PAGE_W, 3.0), sharey=True)
tot27 = bridge.loc[bridge.fall == 2027, "enrollment_today_pattern"].iloc[0]; tot30 = bridge.loc[bridge.fall == 2030, "enrollment_today_pattern"].iloc[0]
for ax, fall in zip(axes, RESIDENTS):
    b = bridge[bridge.fall == fall].iloc[0]; lo, hi = RANGE[fall]
    steps = [("residents", b.residents_deck, ROLE["background"]), (f"× {CAP:.0%}\ncapture", b.residents_attending - b.residents_deck, "#d9d8d3"),
             ("+ in-district\nchoice", b.external_in_district, ROLE["merged"]), ("+ out-of-\ndistrict", b.out_of_district, "#7c6fd0"),
             ("+ place-\nments", b.placements, "#b0a8e6"), ("today's\npattern", b.enrollment_today_pattern, ROLE["merged"])]
    x = np.arange(len(steps)); base = 0.0
    for i, (lab, v, colr) in enumerate(steps):
        if i == 0 or i == len(steps) - 1:
            ax.bar(i, v, color=colr, width=0.72); ax.text(i, v + 7, f"{v:.0f}", ha="center", fontsize=7.5, fontweight="bold"); base = v if i == 0 else base
        else:
            bottom = base if v >= 0 else base + v
            ax.bar(i, abs(v), bottom=bottom, color=colr, width=0.72)
            if v >= 0: ax.text(i, base + v + 7, f"{v:+.0f}", ha="center", fontsize=7)
            else: ax.text(i + 0.42, base + v / 2, f"{v:+.0f}", ha="left", va="center", fontsize=7)
            base = base + v
    ax.axhspan(lo, hi, color=ROLE["proposal"], alpha=0.15, lw=0); ax.text(1.55, lo + 4, f"proposal's range {lo}–{hi}", fontsize=6.4, color=ROLE["proposal"], va="bottom", ha="left")
    ax.axhline(CAPACITY, color=MUTED, lw=0.9, ls=":"); ax.text(-0.45, CAPACITY + 7, "capacity 492", fontsize=6.4, color=MUTED, ha="left")
    ax.set_xticks(x); ax.set_xticklabels([s[0] for s in steps], fontsize=6.0); ax.set_title(f"{fall}-{str(fall + 1)[2:]}: {b.residents_deck:.0f} residents (deck p. 51)", fontsize=8.2, loc="left"); ax.grid(axis="x", visible=False)
axes[0].set_ylabel("students at Bear Creek if merged (K-5)"); axes[0].set_ylim(0, 620)
fig.suptitle(f"Residents × capture + outside enrollment at the December 2025 pattern: {tot27:.0f} in 2027-28 and {tot30:.0f} in 2030-31, against ranges of 392-445 and 403-462",
             fontsize=8.0, fontweight="bold", x=0.01, ha="left", y=1.02)
save(fig, "fig16_bridge", source="deck p. 51 (projected residents, ranges); BVSD Enrollment Pattern Matrix 2025-26 (12/5/2025): combined-area capture 415/502, external seats 75 + 23 + 23; identity, no model")

# ---- Fig 17: capture history vs what the range needs ----
fig, ax = plt.subplots(figsize=(PAGE_W, 2.6))
yrs = np.arange(len(hist)); ax.plot(yrs, hist.combined_area_capture * 100, color=ROLE["merged"], lw=2.2, marker="o", ms=4, label="combined-area capture (residents of the four areas attending Bear Creek or Mesa)")
ax.plot(yrs, hist.own_school_capture * 100, color=ROLE["background"], lw=1.6, marker="o", ms=3, label="own-school capture (matrix 'attending neighborhood school')")
ax.axhspan(need_lo * 100, need_hi * 100, color=ROLE["proposal"], alpha=0.15, lw=0); ax.text(0.05, (need_lo + need_hi) / 2 * 100, f"capture the 403–462 range requires\nat today's {EXT} external seats: {need_lo:.0%}–{need_hi:.0%}", fontsize=6.8, color=ROLE["proposal"], va="center")
for i, v in enumerate(hist.combined_area_capture * 100): ax.text(i, v + 1.5, f"{v:.0f}%", ha="center", fontsize=6.5, color=ROLE["merged"])
ax.set_xticks(yrs); ax.set_xticklabels(hist.year, fontsize=7); ax.set_ylim(40, 100); ax.set_ylabel("share of residents, %"); ax.legend(loc="lower left", fontsize=6.3)
ax.set_title("Combined-area capture has stayed between 81% and 87% for nine years; the proposal's range needs 54–65%", fontsize=8.6, loc="left")
save(fig, "fig17_capture_history", source="BVSD Enrollment Pattern Matrices 2017-18 to 2025-26 (elementary), bvsd.org planning-and-engineering page; parsed by scripts/parse_oe_matrices.py")
