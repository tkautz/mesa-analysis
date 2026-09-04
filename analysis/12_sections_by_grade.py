"""§S3 Classroom feasibility by grade. For each simulated path (both kindergarten specs, 90% of Mesa's students following) the number
of general-education sections the merged school needs is sum over grades of ceil(grade enrollment / class size). Class sizes now come
from published figures (found 2026-09-03): the FY2026-27 budget book's elementary staffing formula, one classroom teacher per 24.58
students (p. 121), and the BVEA 2026-29 agreement's class-size goals by grade band, 26 (K-1), 29 (grades 2-3), 31 (grades 4-5) (§C-6).
The earlier assumption of 25 is kept as a third line for comparison with the previous draft. Rooms available are still assumed
(21 = 3.5 rounds x 6 grades, the basis of 492 on deck p. 51; 18 = a three-round school); RISE/AIM rooms are not netted out.
Outputs: analysis/output/table12_sections.csv, figures/fig15_sections_by_grade.*"""
import sys; sys.path.insert(0, "analysis")
from common import *
import numpy as np, pandas as pd, matplotlib.pyplot as plt
style()
P = np.load(OUT / "paths_modelA.npz"); falls = list(P["falls"])
# grade-level paths: re-simulate with the same seeds as analysis/03 (trend = first draw from the module rng; level = seed 3) and check
src = open("analysis/03_independent_projection.py").read(); exec(src[:src.index("def simulate_B")])
pair = {"bearcreekelementary": G["bearcreekelementary"], "mesaelementaryschool": G["mesaelementaryschool"]}
simT = simulate_A(pair, 2025, 5); simL = simulate_A(pair, 2025, 5, k_mode="level", seed=3)
assert np.allclose(simT["bearcreekelementary"][0], P["bear_creek"]) and np.allclose(simL["mesaelementaryschool"][0], P["mesa_level"]), "paths differ from saved"
GRADES = {"trend": (simT["bearcreekelementary"][1], simT["mesaelementaryschool"][1]), "level": (simL["bearcreekelementary"][1], simL["mesaelementaryschool"][1])}
R = 0.9; rows = []
# class-size bases: label -> per-grade array (K, 1, 2, 3, 4, 5)
BASES = {"staffing formula 24.58": np.full(6, 24.58), "BVEA goals 26/29/31": np.array([26, 26, 29, 29, 31, 31], dtype=float), "assumed 25 (earlier draft)": np.full(6, 25.0)}
for spec in ("trend", "level"):
    bcg, mg = GRADES[spec]
    merged = bcg + R * mg                       # (n, years, 6)
    for fall in (2027, 2030):
        j = falls.index(fall); Eg = merged[:, j, :]
        for lab, cs in BASES.items():
            sections = np.ceil(Eg / cs).sum(1)
            for rooms in (21, 18):
                rows.append(dict(spec=spec, fall=fall, class_size_basis=lab, rooms=rooms, retention=R, total_median=np.median(Eg.sum(1)),
                                 sections_p10=np.percentile(sections, 10), sections_p50=np.median(sections), sections_p90=np.percentile(sections, 90),
                                 p_sections_over_rooms=(sections > rooms).mean(), p_total_over_492=(Eg.sum(1) > 492).mean(),
                                 largest_grade_median=np.median(Eg.max(1)), sections_by_grade_median=str(np.median(np.ceil(Eg / cs), axis=0).astype(int).tolist())))
tab = pd.DataFrame(rows); tab.to_csv(OUT / "table12_sections.csv", index=False)
print(tab[tab.rooms == 21].round(2).to_string(index=False)); print(tab[(tab.rooms == 18)].round(2).to_string(index=False))

# Fig 15: dot-range of sections needed, rows = year x spec x class-size basis; vertical lines at 18 and 21 rooms
fig, ax = plt.subplots(figsize=(PAGE_W, 3.6)); yy = 0; ticks = []
for fall in (2027, 2030):
    for spec, colr in (("trend", ROLE["trend"]), ("level", ROLE["level"])):
        for lab, alpha in (("staffing formula 24.58", 1.0), ("BVEA goals 26/29/31", 0.6)):
            d = tab[(tab.spec == spec) & (tab.fall == fall) & (tab.class_size_basis == lab) & (tab.rooms == 21)].iloc[0]
            ax.plot([d.sections_p10, d.sections_p90], [yy, yy], color=colr, lw=3, alpha=alpha, solid_capstyle="round")
            ax.plot([d.sections_p50], [yy], "o", color="white", mec=colr, mew=1.8, ms=6, alpha=alpha)
            ax.text(d.sections_p90 + 0.25, yy, f"{d.sections_p50:.0f} ({d.sections_p10:.0f}–{d.sections_p90:.0f}); >21 rooms {d.p_sections_over_rooms:.0%}", fontsize=6.3, va="center")
            ticks.append((yy, f"{fall}-{str(fall + 1)[2:]}, {spec}, {lab.split(' (')[0]}")); yy -= 1
    yy -= 0.5
ax.set_yticks([t for t, _ in ticks]); ax.set_yticklabels([l for _, l in ticks], fontsize=6.6)
for x, lab in ((18, "18 rooms\n(3 rounds)"), (21, "21 rooms\n(3.5 rounds)")):
    ax.axvline(x, color=MUTED, lw=0.8, ls=":"); ax.text(x, 0.9, lab, fontsize=6.3, color=MUTED, ha="center", va="bottom")
ax.set_xlim(13, 35); ax.set_ylim(yy - 0.3, 1.9); ax.grid(axis="y", visible=False); fig.subplots_adjust(left=0.34, right=0.99)   # room for the row labels inside the 6.5-in canvas
ax.set_xlabel("general-education sections needed, K-5 (sum over grades of classes at the class size; central and 1-in-10 low to 1-in-10 high)")
ax.set_title("Sections the merged school needs at 90% following, by year, kindergarten assumption and published class-size basis", fontsize=8.4, loc="left")
save(fig, "fig15_sections_by_grade", source="independent cohort-survival model grade paths (analysis/03); rooms basis deck p. 51 (492 = 3.5 rounds); class sizes: FY2026-27 budget book p. 121 (1 : 24.58) and BVEA 2026-29 agreement §C-6 (26 / 29 / 31); RISE/AIM rooms not netted out")
