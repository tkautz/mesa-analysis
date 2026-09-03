"""Package-wide decoding of the deck's post-change ranges: for each component, the share of the sending school's projected
students that the range implies land at the receiving school(s), using the Feb 2026 (Jan 2026 run) standalone projections.
Same arithmetic as the Mesa decoding (41-71%). Output: analysis/output/table10_package_implied_shares.csv"""
import sys; sys.path.insert(0, "analysis")
from common import *
import pandas as pd
cap = pd.read_csv(CLEAN / "capacity_summary_all_schools_by_vintage.csv"); cap = cap[cap.vintage == "feb2026"].set_index("school")
def pj(s, yr): return float(cap.loc[s, f"proj_{yr}"])
# components: sending school(s) -> receiving school(s); deck ranges (lo, hi) by year; deck page
COMP = [
 ("Mesa -> Bear Creek", ["Mesa Elementary School"], ["Bear Creek Elementary"], {"2027-28": (392, 445), "2030-31": (403, 462)}, 51),
 ("Birch -> Kohl", ["Birch Elementary"], ["Kohl Elementary School"], {"2027-28": (433, 473), "2030-31": (437, 474)}, 25),
 ("Flatirons -> Foothill + Whittier", ["Flatirons Elementary School"], ["Foothill Elementary School", "Whittier International Elementary"], {"2027-28": (488 + 337, 497 + 357), "2030-31": (484 + 315, 492 + 329)}, 54),
 ("Douglass -> Coal Creek + Eisenhower + Heatherwood", ["Douglass Elementary School"], ["Coal Creek Elementary School", "Eisenhower Elementary School", "Heatherwood Elementary School"], {"2027-28": (396 + 289 + 260, 426 + 294 + 267), "2030-31": (395 + 297 + 260, 427 + 302 + 268)}, 48),
 ("Monarch K-5 -> Fireside + Superior + Eldorado K-5", ["Monarch K-8 School"], ["Fireside Elementary School", "Superior Elementary School", "Eldorado K-8"], {"2027-28": (427 + 343 + 447, 436 + 365 + 458), "2030-31": (421 + 353 + 424, 430 + 377 + 436)}, 37),
]
rows = []
for name, send, recv, ranges, page in COMP:
    for yr, (lo, hi) in ranges.items():
        s_proj = sum(pj(s, yr) for s in send); r_proj = sum(pj(r, yr) for r in recv); total = s_proj + r_proj
        rows.append(dict(component=name, year=yr, sending_proj=s_proj, receivers_proj=r_proj, sum_standalone=total, range_lo=lo, range_hi=hi,
                         implied_share_lo=(lo - r_proj) / s_proj, implied_share_hi=(hi - r_proj) / s_proj, students_outside_range_at_hi=total - hi, deck_page=page))
t = pd.DataFrame(rows); t.to_csv(OUT / "table10_package_implied_shares.csv", index=False)
pd.set_option("display.width", 220); print(t.round(2).to_string(index=False))

# ---- Fig 13: implied share following, by component ----
import matplotlib.pyplot as plt, numpy as np
style()
fig, ax = plt.subplots(figsize=(PAGE_W, 2.9))
d = t[t.year == "2030-31"].reset_index(drop=True); d27 = t[t.year == "2027-28"].reset_index(drop=True)
for i, r in d.iterrows():
    y = len(d) - 1 - i
    ax.plot([r.implied_share_lo * 100, r.implied_share_hi * 100], [y + 0.15, y + 0.15], color=ROLE["merged"], lw=5, solid_capstyle="butt")
    r2 = d27.iloc[i]; ax.plot([r2.implied_share_lo * 100, r2.implied_share_hi * 100], [y - 0.15, y - 0.15], color="#9a99b8", lw=5, solid_capstyle="butt")
    ax.text(r.implied_share_hi * 100 + 1.5, y + 0.15, f"{r.implied_share_lo:.0%}–{r.implied_share_hi:.0%}", fontsize=6.8, va="center")
    ax.text(r2.implied_share_hi * 100 + 1.5, y - 0.15, f"{r2.implied_share_lo:.0%}–{r2.implied_share_hi:.0%}", fontsize=6.8, va="center", color="#6b6a66")
ax.set_yticks(range(len(d))); ax.set_yticklabels([f"{c} (p. {p})" for c, p in zip(d.component[::-1], d.deck_page[::-1])], fontsize=6.8)
ax.set_xlim(30, 115); ax.set_xlabel("share of the sending school's projected students that the deck's range implies land at the receiving school(s)")
ax.plot([], [], color=ROLE["merged"], lw=5, label="2030-31"); ax.plot([], [], color="#9a99b8", lw=5, label="2027-28"); ax.legend(loc="lower right", fontsize=7)
ax.axvline(100, color=MUTED, lw=0.8, ls=":"); ax.grid(axis="y", visible=False)
ax.set_title("The deck's ranges imply different retention shares for different components", fontsize=9, loc="left")
save(fig, "fig13_package_implied_shares", source="deck pp. 25, 37, 48, 51, 54 (post-change ranges); Feb 2026 report p. 9 (standalone projections). Share = (range end − receivers' standalone projections) ÷ sending school's standalone projection.")
