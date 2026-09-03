"""§4 Consolidation scenario grid. Merged enrollment at Bear Creek = Bear Creek path + r x Mesa path, where r is the share
of Mesa's students who enrol at Bear Creek (the rest open-enrol elsewhere). Uses the joint Model A paths.
Outputs: analysis/output/table04_scenarios.csv, figures/fig07_scenario_heatmap.*, fig08_class_size.*"""
import sys; sys.path.insert(0, "analysis")
from common import *
import numpy as np, pandas as pd, matplotlib.pyplot as plt
style()
P = np.load(OUT / "paths_modelA.npz"); falls = list(P["falls"])
SPECS = {"A-trend": (P["bear_creek"], P["mesa"]), "A-level": (P["bear_creek_level"], P["mesa_level"])}
SECTIONS = 21   # 3.5 rounds x 6 grades (deck p.51 capacity basis)
EFF_CAPS = [492, 470, 445]   # illustrative effective general-education capacities net of center-based program rooms (see report)
rs = np.round(np.arange(0.6, 1.0001, 0.05), 2); rows = []
for spec, (bc, mesa) in SPECS.items():
    for fall in (2027, 2030):
        j = falls.index(fall)
        for r in rs:
            E = bc[:, j] + r * mesa[:, j]
            row = dict(spec=spec, fall=fall, retention=r, median=np.median(E), p10=np.percentile(E, 10), p90=np.percentile(E, 90),
                       p_over_450=(E > 450).mean(), p_under_300=(E < 300).mean(),
                       class_size_median=np.median(E) / SECTIONS, class_size_p90=np.percentile(E, 90) / SECTIONS)
            for cap in EFF_CAPS: row[f"p_over_{cap}"] = (E > cap).mean()
            rows.append(row)
tab = pd.DataFrame(rows); tab.to_csv(OUT / "table04_scenarios.csv", index=False)
print(tab[tab.retention.isin([0.8, 0.9, 1.0])].round(2).to_string(index=False))
bc, mesa = SPECS["A-trend"]
# implied retention in BVSD's own range (deck p.51 vs Jan 2026 separate projections)
vin = load_vintages(); j26 = vin[(vin.vintage == "jan2026") & (vin.measure == "enrollment")].pivot(index="fall", columns="school", values="value")
impl = pd.DataFrame([dict(fall=2027, lo=392, hi=445, bc=j26.loc[2027, "Bear Creek"], mesa=j26.loc[2027, "Mesa"]), dict(fall=2030, lo=403, hi=462, bc=j26.loc[2030, "Bear Creek"], mesa=j26.loc[2030, "Mesa"])])
impl["r_implied_lo"] = (impl.lo - impl.bc) / impl.mesa; impl["r_implied_hi"] = (impl.hi - impl.bc) / impl.mesa; impl["sum_100pct"] = impl.bc + impl.mesa
impl.to_csv(OUT / "table04_implied_retention.csv", index=False); print(impl.round(2).to_string(index=False))

# Fig 7: heatmap-ish grid
fig, axes2 = plt.subplots(2, 3, figsize=(11, 6.8)); fig.subplots_adjust(top=0.9, hspace=0.35)
for row_i, spec in enumerate(SPECS):
  axes = axes2[row_i]; t_ = tab[tab.spec == spec]
  for ax, (col, title) in zip(axes, [("p_over_450", "P(above 3 rounds, 450)"), ("p_over_492", "P(above capacity, 492)"), ("p_under_300", "P(below 2 rounds, 300)")]):
    m = t_.pivot(index="retention", columns="fall", values=col)
    im = ax.imshow(m.values, cmap="Blues", vmin=0, vmax=1, aspect="auto", origin="lower")
    ax.set_xticks([0, 1]); ax.set_xticklabels(["2027-28", "2030-31"]); ax.set_yticks(range(len(rs))); ax.set_yticklabels([f"{int(r*100)}%" for r in rs], fontsize=7.5)
    for i in range(len(rs)):
        for k in range(2):
            v = m.values[i, k]; ax.text(k, i, f"{v:.0%}", ha="center", va="center", fontsize=7.5, color="white" if v > 0.55 else TEXT)
    ax.set_title(f"{title}\n[{'K trend' if spec == 'A-trend' else 'K level (2023-25 mean)'}]", fontsize=9); ax.set_ylabel("Mesa students who follow" if ax is axes[0] else ""); ax.grid(False)
fig.suptitle("Independent model: probabilities for the merged school, by Mesa retention share and kindergarten specification", x=0.01, ha="left", fontsize=11, fontweight="bold")
save(fig, "fig07_scenario_heatmap")

# Fig 8: class-size distributions 2030-31
fig, ax = plt.subplots(figsize=(7.5, 3.6)); j = falls.index(2030)
for r, col in [(0.8, C["aqua"]), (0.9, C["blue"]), (1.0, C["violet"])]:
    E = (bc[:, j] + r * mesa[:, j]) / SECTIONS
    ax.hist(E, bins=np.arange(10, 36, 0.5), histtype="step", lw=2, color=col, label=f"{int(r*100)}% of Mesa students follow", density=True)
for x, lab in [(450 / SECTIONS, "3 rounds (450)"), (492 / SECTIONS, "capacity (492)")]:
    ax.axvline(x, color=MUTED, lw=0.9, ls=":"); ax.text(x, ax.get_ylim()[1] * 0.95, lab, rotation=90, va="top", ha="right", fontsize=7.5, color=MUTED)
ax.set_xlabel(f"average students per classroom in 2030-31 at {SECTIONS} sections (3.5 rounds)"); ax.set_ylabel("density"); ax.legend(loc="upper left")
ax.set_title("Merged-school class size in 2030-31 under the independent model")
save(fig, "fig08_class_size")

# ---- effective-capacity table (both specs, r = 0.9 and 1.0, 2027-28 and 2030-31) ----
eff = tab[tab.retention.isin([0.9, 1.0])][["spec", "fall", "retention", "median", "p90", "p_over_445", "p_over_470", "p_over_492"]]
eff.to_csv(OUT / "table04_effective_capacity.csv", index=False); print(eff.round(2).to_string(index=False))
