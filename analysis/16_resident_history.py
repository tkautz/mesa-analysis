"""§D Resident history of the proposed combined area vs the deck's resident projection.
Matrix column totals ("Total Number of Students living in Attendance Area") for the four areas that form the combined area,
2017-18 … 2025-26, and the kindergarten matrices' K-age residents; the deck's 503 / 473 / 522 (p. 51) and the p. 44 chart's ≈445.
Outputs: analysis/output/table16_residents.csv; figures/fig18_residents.*"""
import sys; sys.path.insert(0, "analysis")
from common import *
import numpy as np, pandas as pd, matplotlib.pyplot as plt
style()
area = pd.read_csv(CLEAN / "oe_matrix_area_totals_south_boulder.csv")
SOUTH = ["Bear Creek", "Mesa", "Optional Bear Creek/Mesa", "Optional Bear Creek/Creekside"]
el = area[area.matrix == "elem"].pivot(index="year", columns="area", values="residents")[SOUTH]
el["combined_area"] = el.sum(1)
kk = area[area.matrix == "k"].pivot(index="year", columns="area", values="residents").reindex(el.index)[SOUTH].sum(1, min_count=4)
el["k_age_residents"] = kk
el["fall"] = [int(y[:4]) for y in el.index]
deck = pd.DataFrame({"fall": [2025, 2027, 2030], "deck_p51_residents": [503, 473, 522]})
el.to_csv(OUT / "table16_residents.csv"); print(el.to_string()); print(deck.to_string(index=False))
first, last = el.combined_area.iloc[0], el.combined_area.iloc[-1]
print(f"combined area residents {first:.0f} ({el.index[0]}) -> {last:.0f} ({el.index[-1]}): {last / first - 1:+.1%}; deck 503 -> 522 by 2030-31: {522 / 503 - 1:+.1%}")

fig, ax = plt.subplots(figsize=(PAGE_W, 3.1))
cols = {"Bear Creek": ROLE["bear_creek"], "Mesa": ROLE["mesa"], "Optional Bear Creek/Mesa": "#9bb7e6", "Optional Bear Creek/Creekside": "#c9d6ee"}
bottom = np.zeros(len(el))
for a in SOUTH:
    ax.bar(el.fall, el[a], bottom=bottom, color=cols[a], width=0.7, label=a.replace("Optional ", "optional "))
    bottom += el[a].values
for f, v in zip(el.fall, el.combined_area): ax.text(f, v + 8, f"{v:.0f}", ha="center", fontsize=7)
ax.plot(deck.fall, deck.deck_p51_residents, color=ROLE["proposal"], marker="D", ms=5, lw=1.8, ls="--", label="deck p. 51: residents of the combined area (503 today; 473, 522 projected)")
for f, v in zip(deck.fall, deck.deck_p51_residents):
    if f != 2025: ax.text(f + 0.15, v + 8, f"{v}", fontsize=7, color=ROLE["proposal"], fontweight="bold")
ax.plot([2030], [445], marker="v", ms=6, color=ROLE["district_run"], ls="none", label="deck p. 44 chart, 2030 (read by eye): ≈445")
ax.set_xlim(2016.4, 2031.2); ax.set_ylim(0, 800); ax.set_ylabel("K-5 residents of the four areas"); ax.set_xlabel("October of school year"); ax.set_xticks(range(2017, 2031))
ax.legend(loc="lower left", fontsize=6.0, ncol=2); ax.grid(axis="x", visible=False)
ax.set_title("Residents of the areas that would form the combined attendance area fell 733 → 502 in eight years; the deck projects 522 by 2030-31", fontsize=8.4, loc="left")
save(fig, "fig18_residents", source="BVSD Enrollment Pattern Matrices 2017-18 to 2025-26, column totals 'Total Number of Students living in Attendance Area'; deck pp. 44, 51")
