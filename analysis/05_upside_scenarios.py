"""§7 Upside scenarios: what would it take for Bear Creek to fill? Deterministic arithmetic from BVSD's own figures plus
model variants. Outputs: analysis/output/table05_upside.csv, figures/fig09_upside_ladder.*, fig10_kindergarten.*"""
import sys; sys.path.insert(0, "analysis")
from common import *
import numpy as np, pandas as pd, matplotlib.pyplot as plt
style()
P = np.load(OUT / "paths_modelA.npz"); falls = list(P["falls"]); j30 = falls.index(2030)
off = load_official(); vin = load_vintages()
j26 = vin[(vin.vintage == "jan2026") & (vin.measure == "enrollment")].pivot(index="fall", columns="school", values="value")
RES_2030, RES_2027, RES_NOW = 522, 473, 275 + 228                      # deck p.51
OE_IN_BC = 82 + 13                                                     # Bear Creek 2025-26: in-district OE-in (derived) + out-of-district
CAPTURE_BC, CAPTURE_MESA = 217 / 275, 156 / 228                         # deck p.44 / p.51
YIELD_PER_SFD = 58 / 324                                               # boundary study Sept 9 2025 p.22: 324 SFD, average yield 58 elementary
K = off.pivot(index="fall", columns="school", values="K"); Kc = K.sum(1)
print("combined K intake:", Kc.to_dict())
r = 0.9
rows = []
def add(name, lo, hi=None, kind="deterministic", note=""): rows.append(dict(scenario=name, low=lo, high=hi if hi is not None else lo, kind=kind, note=note))
add("BVSD proposal range, 2030-31 (deck p.51)", 403, 462, "BVSD", "range depends on share of Mesa students who follow")
add("BVSD Jan 2026 projections summed, 80% / 100% of Mesa follow", j26.loc[2030, "Bear Creek"] + 0.8 * j26.loc[2030, "Mesa"], j26.loc[2030, "Bear Creek"] + j26.loc[2030, "Mesa"], "BVSD-derived")
add("Resident capture at Bear Creek's current 79% + current OE-in (95), residents 522", CAPTURE_BC * RES_2030 + OE_IN_BC, note="deck p.44/p.51 capture; OE-in held at 2025-26 level")
add("Resident capture rises to 85% + current OE-in", 0.85 * RES_2030 + OE_IN_BC)
add("Resident capture 90% + OE-in grows to 120 (3-round school attracts)", 0.90 * RES_2030 + 120)
for nm, key in [("Independent model (trend K), 90% follow: median / P90", ""), ("Independent model, decline stops (K at 2023-25 level), 90% follow: median / P90", "_level")]:
    E = P["bear_creek" + key][:, j30] + r * P["mesa" + key][:, j30]; add(nm, np.median(E), np.percentile(E, 90), "model")
k_early = Kc.loc[2014:2019].mean(); k_recent = Kc.loc[2023:2025].mean()
add(f"Kindergarten intake returns to 2014-19 average ({k_early:.0f}/yr) x 6 grades, 90% follow", 6 * k_early * 0.9 + 0.0, note="steady state, ignoring progression gains/losses")
add(f"Kindergarten intake stays at 2023-25 average ({k_recent:.0f}/yr) x 6 grades, 90% follow", 6 * k_recent * 0.9)
tab = pd.DataFrame(rows); tab["low"] = tab.low.round(0); tab["high"] = tab.high.round(0)
# housing turnover arithmetic: students needed to reach 450 / 492 from the model median, in homes
E_med = np.median(P["bear_creek"][:, j30] + r * P["mesa"][:, j30])
turn = pd.DataFrame([dict(target=t, students_needed=max(0, t - E_med), homes_at_avg_yield=max(0, t - E_med) / YIELD_PER_SFD, homes_at_one_child=max(0, t - E_med)) for t in (450, 492)])
turn["note"] = f"from model median {E_med:.0f}; avg yield {YIELD_PER_SFD:.3f} elementary students per single-family dwelling (BVSD boundary study p.22)"
tab.to_csv(OUT / "table05_upside.csv", index=False); turn.to_csv(OUT / "table05_turnover.csv", index=False)
print(tab.to_string(index=False)); print(turn.round(0).to_string(index=False))
impl_capture = pd.DataFrame([dict(bound="low 403", capture=(403 - OE_IN_BC) / RES_2030), dict(bound="high 462", capture=(462 - OE_IN_BC) / RES_2030)])
print("capture implied by BVSD range if OE-in stays 95:", impl_capture.round(2).to_dict("records")); impl_capture.to_csv(OUT / "table05_implied_capture.csv", index=False)

# Fig 9: ladder
fig, ax = plt.subplots(figsize=(9.5, 4.6))
colors = {"BVSD": VINTAGE_COLOR["aug2026"], "BVSD-derived": C["yellow"], "deterministic": C["violet"], "model": C["blue"]}
for i, rr in enumerate(tab[::-1].itertuples()):
    y = i; c = colors[rr.kind]
    if rr.low == rr.high: ax.plot([rr.low], [y], "o", color=c, ms=7); ax.text(rr.low + 4, y, f"{rr.low:.0f}", va="center", fontsize=8)
    else: ax.plot([rr.low, rr.high], [y, y], color=c, lw=6, solid_capstyle="round"); ax.text(rr.high + 4, y, f"{rr.low:.0f}–{rr.high:.0f}", va="center", fontsize=8)
ax.set_yticks(range(len(tab))); ax.set_yticklabels(tab[::-1].scenario, fontsize=7.8)
for x, lab in [(300, "2 rounds"), (450, "3 rounds"), (492, "capacity")]:
    ax.axvline(x, color=MUTED, lw=0.9, ls=":"); ax.text(x + 2, len(tab) - 0.55, lab, fontsize=7.5, color=MUTED)
ax.set_xlim(280, 640); ax.set_xlabel("merged-school enrollment at Bear Creek, 2030-31 (K-5)"); ax.grid(axis="y", visible=False)
ax.set_title("Plausible upside cases put the merged school at or above the building's capacity")
save(fig, "fig09_upside_ladder")

# Fig 10: kindergarten intake, combined
fig, ax = plt.subplots(figsize=(7.5, 3.4))
ax.bar(K.index - 0.2, K["Bear Creek"], 0.4, color=SCHOOL_COLOR["Bear Creek"], label="Bear Creek K"); ax.bar(K.index + 0.2, K["Mesa"], 0.4, color=SCHOOL_COLOR["Mesa"], label="Mesa K")
ax.plot(Kc.index, Kc.values, color=TEXT, marker="o", ms=3.5, lw=1.8, label="combined K intake")
ax.axhline(492 / 6, color=MUTED, lw=0.9, ls=":"); ax.text(2013.6, 492 / 6 + 1.5, "steady-state K that fills 492 seats (82/yr)", fontsize=7.5, color=MUTED)
ax.set_xlabel("October of school year"); ax.set_ylabel("kindergarten students"); ax.legend(loc="upper right", ncol=3, fontsize=7.5)
ax.set_title("Kindergarten intake at the two schools: the decline flattened after 2020")
save(fig, "fig10_kindergarten")
