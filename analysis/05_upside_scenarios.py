"""Upside cases: what would it take for Bear Creek to fill? Deterministic arithmetic on BVSD's own figures plus the two model
specifications. Outputs: analysis/output/table05_upside.csv, table05_turnover.csv, table05_implied_capture.csv,
figures/fig09_upside_ladder.*, fig10_kindergarten.*"""
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
YIELD_PER_SFD = 58 / 324                                               # boundary study Sept 9 2025 p.22
K = off.pivot(index="fall", columns="school", values="K"); Kc = K.sum(axis=1)
# steady-state multiplier: sum over grades of cumulative mean progression (K->1, ..., K->5), averaged over the two schools
mult = []
for s in ["Bear Creek", "Mesa"]:
    g = off[off.school == s].set_index("fall")[["K", "G1", "G2", "G3", "G4", "G5"]].astype(float)
    r = [(g.iloc[:, i] / g.iloc[:, i - 1].shift(1)).dropna().mean() for i in range(1, 6)]
    mult.append(np.cumprod([1] + r).sum())
MULT = float(np.mean(mult)); K_FILL = 492 / MULT
print(f"steady-state multiplier {MULT:.2f}; K that fills 492 at observed gains: {K_FILL:.0f}")
r = 0.9; rows = []
def add(name, lo, hi=None, kind="deterministic", key="", note=""): rows.append(dict(key=key, scenario=name, low=lo, high=hi if hi is not None else lo, kind=kind, note=note))
add("Proposal's range (deck p. 51)", 403, 462, "BVSD", "A")
add("District's Jan 2026 projections added, 80–100% of Mesa follow", j26.loc[2030, "Bear Creek"] + 0.8 * j26.loc[2030, "Mesa"], j26.loc[2030, "Bear Creek"] + j26.loc[2030, "Mesa"], "BVSD-derived", "B")
add("Residents 522 × Bear Creek's current 79% capture + current 95 OE-in", CAPTURE_BC * RES_2030 + OE_IN_BC, kind="deterministic", key="C")
add("Residents 522 × 85% capture + current 95 OE-in", 0.85 * RES_2030 + OE_IN_BC, kind="deterministic", key="D")
add("Residents 522 × 90% capture + OE-in grows to 120", 0.90 * RES_2030 + 120, kind="deterministic", key="E")
E = P["bear_creek"][:, j30] + r * P["mesa"][:, j30]; add("Model, Trend assumption, 90% follow (central; 1-in-10 high)", np.median(E), np.percentile(E, 90), "model", "F")
E = P["bear_creek_level"][:, j30] + r * P["mesa_level"][:, j30]; add("Model, Level assumption, 90% follow (central; 1-in-10 high)", np.median(E), np.percentile(E, 90), "model", "G")
k_early = Kc.loc[2014:2019].mean(); k_recent = Kc.loc[2023:2025].mean()
add(f"K returns to 2014–19 average ({k_early:.0f}/yr) at observed grade gains, 90% follow", k_early * MULT * 0.9, kind="deterministic", key="H", note=f"steady state; multiplier {MULT:.2f}")
add(f"K stays at 2023–25 average ({k_recent:.0f}/yr) at observed grade gains, 90% follow", k_recent * MULT * 0.9, kind="deterministic", key="I", note=f"steady state; multiplier {MULT:.2f}")
tab = pd.DataFrame(rows); tab["low"] = tab.low.round(0); tab["high"] = tab.high.round(0)
E_med = np.median(P["bear_creek"][:, j30] + r * P["mesa"][:, j30])
turn = pd.DataFrame([dict(target=t, students_needed=max(0, t - E_med), homes_at_avg_yield=max(0, t - E_med) / YIELD_PER_SFD, homes_at_one_child=max(0, t - E_med)) for t in (450, 492)])
turn["note"] = f"from Trend-assumption central estimate {E_med:.0f}; avg yield {YIELD_PER_SFD:.3f} elementary students per single-family dwelling (BVSD boundary study p.22)"
tab.to_csv(OUT / "table05_upside.csv", index=False); turn.to_csv(OUT / "table05_turnover.csv", index=False)
print(tab.to_string(index=False)); print(turn.round(0).to_string(index=False))
impl_capture = pd.DataFrame([dict(bound="low 403", capture_oe95=(403 - OE_IN_BC) / RES_2030, capture_oe_both=(403 - OE_IN_BC - 68) / RES_2030), dict(bound="high 462", capture_oe95=(462 - OE_IN_BC) / RES_2030, capture_oe_both=(462 - OE_IN_BC - 68) / RES_2030)])
print(impl_capture.round(2).to_string(index=False)); impl_capture.to_csv(OUT / "table05_implied_capture.csv", index=False)
n_over = int((tab.high >= 492).sum()); n_over_low = int((tab.low >= 492).sum()); print("cases >=492: central", n_over_low, "high", n_over)

# Fig 9: ladder with the proposal range shaded, factual title, lettered rows
fig, ax = plt.subplots(figsize=(PAGE_W, 3.6))
colors = {"BVSD": ROLE["proposal"], "BVSD-derived": "#6b6a66", "deterministic": ROLE["merged"], "model": ROLE["level"]}
ax.axvspan(403, 462, color=ROLE["proposal"], alpha=0.10, lw=0); ax.text(432, -1.15, "proposal's range 403–462", ha="center", va="center", fontsize=6.8, color=ROLE["proposal"])
for i, rr in enumerate(tab[::-1].itertuples()):
    y = i; c = colors[rr.kind]
    if rr.low == rr.high: ax.plot([rr.low], [y], "o", color=c, ms=6); ax.text(rr.low + 4, y, f"{rr.low:.0f}", va="center", fontsize=7)
    else: ax.plot([rr.low, rr.high], [y, y], color=c, lw=5, solid_capstyle="round"); ax.plot([rr.low], [y], "o", color="white", mec=c, mew=1.5, ms=5); ax.text(rr.high + 4, y, f"{rr.low:.0f}–{rr.high:.0f}", va="center", fontsize=7)
ax.set_yticks(range(len(tab))); ax.set_yticklabels([f"{k}. {sc}" for k, sc in zip(tab[::-1].key, tab[::-1].scenario)], fontsize=6.6)
for x, lab in [(300, "2 rounds"), (450, "3 rounds"), (492, "capacity")]:
    ax.axvline(x, color=MUTED, lw=0.8, ls=":"); ax.text(x, -0.9, lab, fontsize=6.8, color=MUTED, ha="center", va="center")
ax.set_xlim(280, 640); ax.set_ylim(-1.6, len(tab) - 0.5); ax.set_xlabel("merged-school enrollment at Bear Creek, 2030-31 (K-5)"); ax.grid(axis="y", visible=False)
ax.set_title(f"Merged-school enrollment in 2030-31 under nine cases: {n_over_low} reach 492 at their central value, {n_over} at their 1-in-10 high", fontsize=8.4, loc="left")
save(fig, "fig09_upside_ladder", source="deck pp. 44, 51; Feb 2026 report p. 9; BVSD October pupil-count files; independent model. Model rows show the central estimate (dot) to the 1-in-10 high.")

# Fig 10: kindergarten intake, stacked
fig, ax = plt.subplots(figsize=(PAGE_W, 2.8))
ax.bar(K.index, K["Bear Creek"], 0.7, color=ROLE["bear_creek"], label="Bear Creek"); ax.bar(K.index, K["Mesa"], 0.7, bottom=K["Bear Creek"], color=ROLE["mesa"], label="Mesa")
for x, v in Kc.items(): ax.text(x, v + 1.5, f"{v:.0f}", ha="center", fontsize=6.5)
ax.plot([2013.6, 2019.4], [k_early, k_early], color=TEXT, lw=1.2); ax.text(2018.2, k_early + 2, f"2014–19 average {k_early:.0f}", fontsize=6.8, ha="center", bbox=dict(fc="white", ec="none", pad=0.6))
ax.plot([2022.6, 2025.4], [k_recent, k_recent], color=TEXT, lw=1.2); ax.text(2025.5, k_recent + 3, f"2023–25\naverage {k_recent:.0f}", fontsize=6.8, ha="left", va="bottom")
ax.axhline(K_FILL, color=MUTED, lw=0.9, ls=":"); ax.text(2013.6, K_FILL - 2, f"about {K_FILL:.0f} a year fills 492 seats at observed grade-to-grade gains", fontsize=6.5, color=MUTED, va="top", ha="left", bbox=dict(fc="white", ec="none", pad=0.6))
ax.set_xlabel("October of school year"); ax.set_ylabel("kindergarten students, both schools"); ax.legend(loc="upper right", fontsize=7); ax.set_ylim(0, 125); ax.set_xlim(2013.3, 2027.2)
ax.set_title("Kindergarten intake at the two schools, 2014–2025", fontsize=9, loc="left")
save(fig, "fig10_kindergarten", source="BVSD October pupil-count files (CDE Head Count Summary), grade columns; steady-state multiplier from observed 2015–2025 grade-progression ratios")
pd.Series(dict(mult=MULT, k_fill=K_FILL, k_early=k_early, k_recent=k_recent, n_cases_over_492=n_over)).to_csv(OUT / "summary05.csv")
