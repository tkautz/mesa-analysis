"""§S4/E A third kindergarten specification: births in the combined attendance area, five years earlier, times an entry ratio.
Births by elementary attendance area are the district's own series (Board enrollment packets 2015-2025, BD1; parsed by
scripts/parse_bvsd_births_by_area.py). The combined area = Bear Creek + Mesa + BC-Mesa + BC-Creekside areas (the four areas the matrix
uses). Entry ratio r_{s,t} = K_{s,t} / B_{t-5} for each school s; simulated K = B_{t-5} x r drawn jointly for the two schools from a window
of observed years (main: 2020-2025; sensitivity: 2014-2025). Grade progression as in analysis/03 (shared year draws). B_2025 is not yet
published for the areas; it is set to B_2024 scaled by the county's 2025/2024 change (CDPHE) with a sensitivity at the 2022-24 mean.
Outputs: analysis/output/table18_births_k.csv, table18_births_spec.csv; figures/fig19_births_k.*"""
import sys; sys.path.insert(0, "analysis")
from common import *
import numpy as np, pandas as pd, matplotlib.pyplot as plt
style()
src = open("analysis/03_independent_projection.py").read(); exec(src[:src.index("# ---------------- main projection")])

wide = pd.read_csv(CLEAN / "bvsd_births_by_attendance_area_wide.csv")
idx = "normalized_area" if "normalized_area" in wide.columns else ("area" if "area" in wide.columns else wide.columns[0])
wide = wide.set_index(idx)
ycols = [c for c in wide.columns if str(c).isdigit()]
B = wide.loc[["Bear Creek", "Mesa", "BC-Mesa", "BC-Creekside"], ycols].astype(float)
B.columns = [int(c) for c in ycols]; Bsum = B.sum(0)
print("combined-area births:", Bsum.loc[2005:2024].astype(int).to_dict())

off = load_official(); K = off.pivot(index="fall", columns="school", values="K").astype(float)
hist = pd.DataFrame({"fall": K.index, "births_5yr_earlier": [Bsum.get(f - 5, np.nan) for f in K.index], "K_bear_creek": K["Bear Creek"].values, "K_mesa": K["Mesa"].values})
hist["K_both"] = hist.K_bear_creek + hist.K_mesa; hist["ratio_both"] = hist.K_both / hist.births_5yr_earlier
hist["ratio_bc"] = hist.K_bear_creek / hist.births_5yr_earlier; hist["ratio_mesa"] = hist.K_mesa / hist.births_5yr_earlier
# county comparison (SDO births, D1)
sdo = pd.read_csv(ROOT / "data/raw/demography/sdo_components_of_change_boulder_state_1970_2060.csv"); sdo = sdo[sdo.countyfips == 13].set_index("year").births
hist["county_births_5yr_earlier"] = [sdo.get(f - 5, np.nan) for f in K.index]; hist["ratio_to_county_pct"] = 100 * hist.K_both / hist.county_births_5yr_earlier
hist.to_csv(OUT / "table18_births_k.csv", index=False); print(hist.round(3).to_string(index=False))

# future births inputs: K in fall t uses births in t-5
cdphe_2024, cdphe_2025 = 2418, 2465        # CDPHE calendar-year county births (D4/D5)
B_future = {2026: Bsum[2021], 2027: Bsum[2022], 2028: Bsum[2023], 2029: Bsum[2024], 2030: Bsum[2024] * cdphe_2025 / cdphe_2024}
B_future_alt = dict(B_future); B_future_alt[2030] = Bsum.loc[2022:2024].mean()
print("births feeding K 2026-2030:", {k: round(v, 1) for k, v in B_future.items()}, "| alt 2030:", round(B_future_alt[2030], 1))

pair = {"bearcreekelementary": G["bearcreekelementary"], "mesaelementaryschool": G["mesaelementaryschool"]}
def simulate_births(gdict, upto, horizon, n, seed, window, bfut):
    r = np.random.default_rng(seed); pools = {k: ratios(g, upto) for k, g in gdict.items()}; yrs = list(next(iter(pools.values()))[1].index)
    draws = r.choice(len(yrs), size=(n, horizon))
    wyears = [y for y in range(window[0], window[1] + 1)]; wdraw = r.choice(len(wyears), size=(n, horizon))
    rat = {"bearcreekelementary": hist.set_index("fall").ratio_bc, "mesaelementaryschool": hist.set_index("fall").ratio_mesa}
    out = {}
    for k, g in gdict.items():
        pr = pools[k][1].loc[yrs].values; rv = np.array([rat[k].loc[y] for y in wyears])
        cur = np.tile(g.loc[upto, GR].values, (n, 1)).astype(float); tot = np.zeros((n, horizon)); grades = np.zeros((n, horizon, 6))
        for h in range(horizon):
            d = draws[:, h]; nxt = np.empty_like(cur); nxt[:, 0] = bfut[upto + 1 + h] * rv[wdraw[:, h]]
            for i in range(1, 6): nxt[:, i] = cur[:, i - 1] * pr[d, i - 1]
            cur = nxt; tot[:, h] = cur.sum(1); grades[:, h] = cur
        out[k] = (tot, grades)
    return out
rows = []
for lab, window, bfut in (("births spec, ratio window 2020-25", (2020, 2025), B_future), ("births spec, ratio window 2014-25", (2014, 2025), B_future),
                          ("births spec, ratio window 2014-23 (excludes the 2024-25 ratios)", (2014, 2023), B_future), ("births spec, ratio window 2014-24 (excludes 2025)", (2014, 2024), B_future),
                          ("births spec, 2020-25, B2025 at 2022-24 mean", (2020, 2025), B_future_alt)):
    sim = simulate_births(pair, 2025, 5, N, 21, window, bfut)
    bc, me = sim["bearcreekelementary"][0], sim["mesaelementaryschool"][0]
    for fall in (2027, 2030):
        j = fall - 2026; E = bc[:, j] + 0.9 * me[:, j]
        rows.append(dict(run=lab, fall=fall, bc_median=np.median(bc[:, j]), mesa_median=np.median(me[:, j]), both_median=np.median(bc[:, j] + me[:, j]),
                         merged90_median=np.median(E), merged90_p10=np.percentile(E, 10), merged90_p90=np.percentile(E, 90), p_over_450=(E > 450).mean(), p_over_492=(E > 492).mean(),
                         k_both_median=np.median(sim["bearcreekelementary"][1][:, j, 0] + sim["mesaelementaryschool"][1][:, j, 0])))
    if lab.endswith("2020-25"):
        np.savez_compressed(OUT / "paths_births_spec.npz", bear_creek=bc, mesa=me, falls=np.arange(2026, 2031))
P = np.load(OUT / "paths_modelA.npz"); falls = list(P["falls"])
for lab, (a, b) in (("trend (analysis/03)", ("bear_creek", "mesa")), ("level (analysis/03)", ("bear_creek_level", "mesa_level"))):
    for fall in (2027, 2030):
        j = falls.index(fall); E = P[a][:, j] + 0.9 * P[b][:, j]
        rows.append(dict(run=lab, fall=fall, bc_median=np.median(P[a][:, j]), mesa_median=np.median(P[b][:, j]), both_median=np.median(P[a][:, j] + P[b][:, j]), merged90_median=np.median(E),
                         merged90_p10=np.percentile(E, 10), merged90_p90=np.percentile(E, 90), p_over_450=(E > 450).mean(), p_over_492=(E > 492).mean(), k_both_median=np.nan))
spec = pd.DataFrame(rows); spec.to_csv(OUT / "table18_births_spec.csv", index=False); print(spec.round(2).to_string(index=False))

# ---- Fig 19 ----
fig, axes = plt.subplots(1, 2, figsize=(PAGE_W, 2.9))
ax = axes[0]; yrs = np.arange(2005, 2025)
ax.bar(yrs, Bsum.loc[2005:2024].values, color=ROLE["background"], width=0.7, label="births in the four areas (district series), by birth year")
kk = hist.set_index("fall").K_both; ax.plot(kk.index - 5, kk.values, color=ROLE["merged"], lw=2, marker="o", ms=3.5, label="kindergarten at the two schools five years later")
for y in (2021, 2022, 2023, 2024): ax.text(y, Bsum[y] + 2, f"{Bsum[y]:.0f}", ha="center", fontsize=6.5, color=MUTED)
ax.set_xlabel("birth year (kindergarten = birth year + 5)"); ax.set_ylabel("children"); ax.legend(fontsize=6, loc="lower left"); ax.set_ylim(0, 125); ax.set_xticks(range(2005, 2025, 3))
bmin_year = int(Bsum.loc[2005:2024].idxmin()); ax.set_title(f"Births fell to {Bsum[bmin_year]:.0f} in {bmin_year}; kindergarten did not follow", fontsize=8.4, loc="left")
ax = axes[1]; rr = hist.set_index("fall").ratio_both
ax.plot(rr.index, rr.values, color=ROLE["merged"], lw=2, marker="o", ms=3.5); ax.axhline(1, color=MUTED, lw=0.8, ls=":")
for f, v in rr.items(): ax.text(f, v + 0.06, f"{v:.1f}", ha="center", fontsize=6.3, color=ROLE["merged"])
ax.set_xlabel("kindergarten year"); ax.set_ylabel("kindergarten / births five years earlier"); ax.set_ylim(0, 3.2); ax.set_xticks(range(2014, 2026, 2))
r_pre = rr.loc[:2023]; ax.set_title(f"Entry ratio: {r_pre.min():.1f}–{r_pre.max():.1f} through 2023, {rr.loc[2024]:.1f} in 2024", fontsize=8.4, loc="left")
fig.suptitle("Kindergarten at Mesa and Bear Creek runs well above the areas' own births: families arrive after birth, and choose in", fontsize=8.6, fontweight="bold", x=0.01, ha="left", y=1.02)
save(fig, "fig19_births_k", source="BVSD 'Births by Elementary Attendance Area' tables in the Board's annual enrollment updates (Bear Creek, Mesa, BC-Mesa, BC-Creekside areas; data/raw/bvsd/boarddocs/); BVSD October pupil-count files (kindergarten)")
