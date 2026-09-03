"""B5a: the district's rejected K-2 / 3-5 option (deck p. 56) simulated for the combined Mesa + Bear Creek area under both
kindergarten assumptions. Grade-level paths come from the joint Model A simulation (paths_modelA.npz, grade arrays).
Outputs: analysis/output/table07_reconfiguration.csv, figures/fig12_reconfiguration.*"""
import sys; sys.path.insert(0, "analysis")
from common import *
import numpy as np, pandas as pd, matplotlib.pyplot as plt
style()
P = np.load(OUT / "paths_modelA.npz"); falls = list(P["falls"])
# grade arrays exist for the trend spec; rebuild level-spec grade arrays by re-running the model with grades
src = open("analysis/03_independent_projection.py").read().split("# ---------------- main projection")[0]
ns = {}; exec(compile(src, "m3", "exec"), ns); G, simulate_A = ns["G"], ns["simulate_A"]
pair = {"bearcreekelementary": G["bearcreekelementary"], "mesaelementaryschool": G["mesaelementaryschool"]}
rows = []
for spec, seed in [("trend", 2), ("level", 3)]:
    sim = simulate_A(pair, 2025, 5, k_mode=spec, seed=seed, n=6000)
    gr = sim["bearcreekelementary"][1] + sim["mesaelementaryschool"][1]          # (n, 5, 6) combined area by grade
    for fall in (2027, 2030):
        j = falls.index(fall); g = gr[:, j, :]                                   # (n, 6): K..5
        for r in (0.9, 1.0):
            # share following applies to Mesa-origin students; apply r to Mesa's grades only
            gm = sim["mesaelementaryschool"][1][:, j, :] * r + sim["bearcreekelementary"][1][:, j, :]
            k2 = gm[:, :3].sum(1); g35 = gm[:, 3:].sum(1); tot = gm.sum(1)
            for name, arr, cap in [("K-2 building", k2, None), ("3-5 building", g35, None), ("both", tot, None)]:
                rows.append(dict(spec=spec, fall=fall, retention=r, unit=name, median=np.median(arr), p10=np.percentile(arr, 10), p90=np.percentile(arr, 90),
                                 per_grade_median=np.median(arr) / 3 if name != "both" else np.median(arr) / 6,
                                 classes_per_grade_at_25=np.median(arr) / 3 / 25 if name != "both" else np.median(arr) / 6 / 25))
tab = pd.DataFrame(rows); tab.to_csv(OUT / "table07_reconfiguration.csv", index=False)
print(tab.round(1).to_string(index=False))
# utilization of each building under K-2 at Mesa (418) and 3-5 at Bear Creek (492), and the reverse
fig, ax = plt.subplots(figsize=(PAGE_W, 3.0)); y = 0; ticks = []
for spec in ("trend", "level"):
    for fall in (2027, 2030):
        d = tab[(tab.spec == spec) & (tab.fall == fall) & (tab.retention == 0.9)]
        k2 = d[d.unit == "K-2 building"].iloc[0]; g35 = d[d.unit == "3-5 building"].iloc[0]
        for lab, row, colr in [("K-2 (3 grades)", k2, ROLE["mesa"]), ("3-5 (3 grades)", g35, ROLE["bear_creek"])]:
            ax.plot([row["p10"] / 3, row["p90"] / 3], [y, y], color=colr, lw=4, solid_capstyle="round"); ax.plot([row["median"] / 3], [y], "o", color="white", mec=colr, mew=1.5, ms=5)
            ax.text(row["p90"] / 3 + 1, y, f"{row['median'] / 3:.0f} per grade ({row['median'] / 3 / 25:.1f} classes at 25)", fontsize=6.5, va="center")
            ticks.append((y, f"{spec.capitalize()}, {fall}-{str(fall + 1)[2:]}, {lab}")); y -= 1
        y -= 0.4
ax.set_yticks([t for t, _ in ticks]); ax.set_yticklabels([l for _, l in ticks], fontsize=6.5)
ax.axvline(75, color=MUTED, lw=0.8, ls=":"); ax.text(75, y - 0.2, "3 classes of 25", fontsize=6.5, color=MUTED, ha="center", va="top")
ax.axvline(50, color=MUTED, lw=0.8, ls=":"); ax.text(50, y - 0.2, "2 classes of 25", fontsize=6.5, color=MUTED, ha="center", va="top"); ax.set_ylim(y - 1.2, 0.8)
ax.set_xlabel("students per grade in each building (central estimate; 1-in-10 low to high), 90% of Mesa students in the combined area"); ax.set_xlim(40, 130); ax.grid(axis="y", visible=False)
ax.set_title("The district's rejected K-2 / 3-5 option: students per grade in each of the two buildings", fontsize=8.8, loc="left")
save(fig, "fig12_reconfiguration", source="independent cohort-survival model, grade-level paths for the combined Mesa + Bear Creek area; option listed as studied on deck p. 56")
