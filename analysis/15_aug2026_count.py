"""§S2 The first 2026-27 count. (a) The Student Enrollment Center's Aug 28, 2026 count for every elementary school against the January 2026
run's projection for 2026-27 (Feb 2026 report p. 9). (b) A conditional run of the cohort model with the Aug 28 grade counts inserted as a
pseudo-October-2026 observation, under both kindergarten assumptions: "if the October count equals the August count".
Inputs: data/clean/enrollment_2026-27_weekly_elementary.csv (P20), capacity_summary_all_schools_by_vintage.csv, analysis/03 model.
Outputs: analysis/output/table15_aug2026_vs_projection.csv, table15_conditional.csv; figures/fig20_aug2026.*"""
import sys, re; sys.path.insert(0, "analysis")
from common import *
import numpy as np, pandas as pd, matplotlib.pyplot as plt
style()

wk = pd.read_csv(CLEAN / "enrollment_2026-27_weekly_elementary.csv")
aug = wk[wk.date == wk.date.max()].copy(); DATE = wk.date.max()
vin = pd.read_csv(CLEAN / "capacity_summary_all_schools_by_vintage.csv")
j26 = vin[vin.vintage == "feb2026"][["school", "capacity", "enroll_base", "proj_2026-27", "proj_2027-28", "proj_2030-31"]].copy()
def key(s):
    s = str(s).lower()
    s = re.sub(r"\(k-5\)|k-5|k-8|k5|k8|elementary|elem\.?|school|international|charter|k-12|k12", " ", s)
    return re.sub(r"[^a-z]", "", s)
aug["key"] = aug.school.map(key); j26["key"] = j26.school.map(key)
# the district's table combines BCSIS and High Peaks as one row (BCSIS): sum the two Aug rows to match
hp = aug[aug.key == "highpeaks"]; bcs = aug[aug.key == "bcsis"]
if len(hp) and len(bcs):
    row = bcs.iloc[0].copy(); row["school"] = "BCSIS + HIGH PEAKS"; row["count"] = bcs["count"].iloc[0] + hp["count"].iloc[0]
    for c in ["oct2023", "oct2024", "oct2025", "k", "g1", "g2", "g3", "g4", "g5"]: row[c] = bcs[c].iloc[0] + hp[c].iloc[0]
    aug = pd.concat([aug[~aug.key.isin(["bcsis", "highpeaks"])], pd.DataFrame([row])], ignore_index=True)
ALIAS = {"montessori": "communitymontessori", "creekside": "creeksideatmartinpark", "sanchez": "aliciasanchez"}
aug["key"] = aug.key.replace(ALIAS)
m = aug.merge(j26, on="key", how="left", suffixes=("", "_table"))
m = m[m.school != "TOTAL ELEMENTARY"].copy()
m["diff"] = m["count"] - m["proj_2026-27"]; m["pct_diff"] = 100 * m["diff"] / m["proj_2026-27"]; m["vs_oct2025_pct"] = 100 * (m["count"] / m.oct2025 - 1)
unmatched = m[m["proj_2026-27"].isna()].school.tolist(); print("unmatched Aug rows:", unmatched)
out = m[["school", "school_table", "oct2023", "oct2024", "oct2025", "count", "proj_2026-27", "diff", "pct_diff", "vs_oct2025_pct", "capacity", "proj_2027-28", "proj_2030-31"]].rename(columns={"count": f"count_{DATE}"})
out.to_csv(OUT / "table15_aug2026_vs_projection.csv", index=False)
mm = m.dropna(subset=["proj_2026-27"]); small = mm[~mm.key.isin(["goldhill", "jamestown"])]
print(f"{len(small)} matched schools; sum Aug {small['count'].sum():.0f} vs sum Jan 2026 projection {small['proj_2026-27'].sum():.0f} ({100 * (small['count'].sum() / small['proj_2026-27'].sum() - 1):+.1f}%); "
      f"vs Oct 2025 {100 * (small['count'].sum() / small.oct2025.sum() - 1):+.1f}%; median school pct diff {small.pct_diff.median():+.1f}%; share above projection {(small['diff'] > 0).mean():.0%}")
print(out[out.school.isin(["BEAR CREEK", "MESA"])].round(1).to_string(index=False))
print(out.sort_values("pct_diff").round(1)[["school", "oct2025", f"count_{DATE}", "proj_2026-27", "pct_diff"]].to_string(index=False))

# ---- (b) conditional model run ----
src = open("analysis/03_independent_projection.py").read(); exec(src[:src.index("# ---------------- main projection")])
pair = {"bearcreekelementary": G["bearcreekelementary"].copy(), "mesaelementaryschool": G["mesaelementaryschool"].copy()}
AUG = {"bearcreekelementary": aug[aug.school == "BEAR CREEK"].iloc[0], "mesaelementaryschool": aug[aug.school == "MESA"].iloc[0]}
pair26 = {}
for k, g in pair.items():
    g2 = g.copy(); a = AUG[k]; g2.loc[2026] = [float(a[c]) for c in ["k", "g1", "g2", "g3", "g4", "g5"]]; pair26[k] = g2.sort_index()
print({k: g.loc[2026].astype(int).tolist() for k, g in pair26.items()})
rows = []
for spec, seed in (("trend", None), ("level", 3)):
    base = simulate_A(pair, 2025, 5, k_mode=spec, seed=seed); cond = simulate_A(pair26, 2026, 4, k_mode=spec, seed=(seed or 0) + 11)
    for fall in (2027, 2030):
        jb, jc = fall - 2026, fall - 2027
        Eb = base["bearcreekelementary"][0][:, jb] + 0.9 * base["mesaelementaryschool"][0][:, jb]
        Ec = cond["bearcreekelementary"][0][:, jc] + 0.9 * cond["mesaelementaryschool"][0][:, jc]
        for lab, E in (("baseline (data through Oct 2025)", Eb), (f"conditional (Aug {DATE[-5:]} count as Oct 2026)", Ec)):
            rows.append(dict(spec=spec, fall=fall, run=lab, median=np.median(E), p10=np.percentile(E, 10), p90=np.percentile(E, 90), p_over_450=(E > 450).mean(), p_over_492=(E > 492).mean(),
                             bc_median=np.median(base["bearcreekelementary"][0][:, jb] if lab.startswith("baseline") else cond["bearcreekelementary"][0][:, jc]),
                             mesa_median=np.median(base["mesaelementaryschool"][0][:, jb] if lab.startswith("baseline") else cond["mesaelementaryschool"][0][:, jc])))
    # kindergarten in the conditional run's first simulated year (2027) vs the observed Aug 2026 K
    k27 = cond["bearcreekelementary"][1][:, 0, 0] + cond["mesaelementaryschool"][1][:, 0, 0]
    print(f"{spec}: simulated combined K for 2027 median {np.median(k27):.0f} (p10-p90 {np.percentile(k27, 10):.0f}-{np.percentile(k27, 90):.0f}); Aug 2026 observed {AUG['bearcreekelementary'].k + AUG['mesaelementaryschool'].k:.0f}")
cond_tab = pd.DataFrame(rows); cond_tab.to_csv(OUT / "table15_conditional.csv", index=False); print(cond_tab.round(2).to_string(index=False))

# ---- Fig 20: the two schools' October counts, the Jan 2026 run, and the Aug 28, 2026 count ----
off = load_official(); v = load_vintages()
fig, axes = plt.subplots(1, 2, figsize=(PAGE_W, 2.9), sharey=False)
for ax, s, rowname in zip(axes, ["Bear Creek", "Mesa"], ["BEAR CREEK", "MESA"]):
    h = off[off.school == s].set_index("fall").funded_headcount.loc[2018:]
    ax.plot(h.index, h.values, color=SCHOOL_COLOR[s], lw=2.2, marker="o", ms=3.5, label="October count", zorder=5)
    for vint, ls in (("jan2025", ":"), ("jan2026", "--")):
        p = v[(v.vintage == vint) & (v.measure == "enrollment") & (v.school == s)].set_index("fall").value
        ax.plot(p.index, p.values, color=ROLE["district_run"], lw=1.4, ls=ls, marker="s", ms=2.5, label=VINTAGE_LABEL[vint].split(" (")[0])
    a = aug[aug.school == rowname].iloc[0]
    ax.plot([2026], [a["count"]], marker="*", ms=12, color=SCHOOL_COLOR[s], mec=TEXT, mew=0.7, ls="none", label=f"Aug 28, 2026 count (preliminary)", zorder=7)
    ax.text(2026.25, a["count"], f"{a['count']:.0f}", fontsize=7.5, color=SCHOOL_COLOR[s], va="center", fontweight="bold")
    pj = v[(v.vintage == "jan2026") & (v.measure == "enrollment") & (v.school == s) & (v.fall == 2026)].value.iloc[0]
    ax.annotate("", xy=(2026, a["count"]), xytext=(2026, pj), arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    ax.text(2025.75, (a["count"] + pj) / 2, f"{a['count'] - pj:+.0f} vs Jan 2026", fontsize=6.5, color=MUTED, ha="right", va="center")
    ax.set_title(s, fontsize=9, loc="left"); ax.set_xlim(2017.5, 2031); ax.set_xlabel("October of school year"); ax.set_xticks(range(2018, 2031, 2))
axes[0].set_ylabel("students (K-5)"); axes[1].legend(fontsize=6.0, loc="upper right")
fig.suptitle("The first 2026-27 count: Bear Creek 330 against a January projection of 299; Mesa 204 against 217", fontsize=8.6, fontweight="bold", x=0.01, ha="left", y=1.02)
save(fig, "fig20_aug2026", source="BVSD Student Enrollment Center weekly Enrollment Count, Aug 28, 2026 (preliminary, PK excluded); Feb 2025 p. 9 and Feb 2026 p. 9 (district runs); BVSD October pupil-count files")
