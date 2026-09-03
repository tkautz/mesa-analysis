"""§ Descriptive: the district's own numbers. Fig 2 (lead figure): what the district's own projections, range and resident counts
imply. Fig 1: BVSD's projections by run vs October counts, Bear Creek and Mesa.
Outputs: figures/fig01_vintages.*, figures/fig02_district_arithmetic.*, analysis/output/table01_vintages.csv, summary01.csv"""
import sys; sys.path.insert(0, "analysis")
from common import *
import matplotlib.pyplot as plt
style()
off = load_official(); vin = load_vintages(); rng_ = load_merged_range()
proj = vin[(vin.measure == "enrollment")].pivot_table(index=["school", "fall"], columns="vintage", values="value")
act = off.set_index(["school", "fall"]).funded_headcount.rename("actual")
t1 = proj.join(act, how="outer").reset_index(); t1 = t1[t1.fall >= 2023].sort_values(["school", "fall"]); t1.to_csv(OUT / "table01_vintages.csv", index=False)

# ---------- Fig 2 (lead): what the district's own numbers imply ----------
j26 = proj.xs("jan2026", axis=1)
rows = [("2030-31", j26.loc[("Bear Creek", 2030)], j26.loc[("Mesa", 2030)], 403, 462, 522),
        ("2027-28", j26.loc[("Bear Creek", 2027)], j26.loc[("Mesa", 2027)], 392, 445, 473)]
fig, ax = plt.subplots(figsize=(PAGE_W, 3.1))
y = 0
ylabels = []
for sy, bc, mesa, lo, hi, res in rows:
    tot = bc + mesa
    ax.barh(y + 0.22, bc, 0.36, color=ROLE["bear_creek"], left=0); ax.barh(y + 0.22, mesa, 0.36, color=ROLE["mesa"], left=bc)
    ax.text(bc - 4, y + 0.22, f"Bear Creek {bc:.0f}", va="center", ha="right", color="white", fontsize=7.2)
    ax.text(bc + mesa / 2, y + 0.22, f"Mesa {mesa:.0f}", va="center", ha="center", color="white", fontsize=7.2)
    ax.text(tot + 4, y + 0.22, f"{tot:.0f}", va="center", fontsize=8, fontweight="bold")
    ax.barh(y - 0.22, hi - lo, 0.36, left=lo, color=ROLE["proposal"]); ax.text(lo + (hi - lo) / 2, y - 0.22, f"{lo}–{hi}", va="center", ha="center", fontsize=7.5, fontweight="bold", color="white")
    gap = tot - hi; share = 100 * gap / mesa
    ax.annotate("", xy=(hi, y - 0.22), xytext=(tot, y - 0.22), arrowprops=dict(arrowstyle="<->", color=TEXT, lw=0.8))
    ax.text(tot + 4, y - 0.22, f"{gap:.0f} students not in the range\n({share:.0f}% of Mesa's projection)", ha="left", va="center", fontsize=6.6, color=TEXT)
    ylabels += [(y + 0.22, f"{sy}\ndistrict's two\nprojections, added"), (y - 0.22, f"{sy}\nproposal's range")]
    y -= 1.3
ax.set_yticks([p for p, _ in ylabels]); ax.set_yticklabels([l for _, l in ylabels], fontsize=7)
for x, lab, dy in [(450, "3 rounds\n(450)", 0.62), (492, "capacity\n(492)", 0.62)]:
    ax.axvline(x, color=MUTED, lw=0.9, ls=":"); ax.text(x, dy, lab, fontsize=6.8, color=MUTED, ha="center", va="bottom")
ax.set_xlim(200, 600); ax.set_ylim(-1.9, 1.05); ax.set_xlabel("students at Bear Creek (K-5)"); ax.grid(axis="y", visible=False)
ax.set_title("The district's own projections for the two schools add to 521 (2030-31) and 496 (2027-28);\nits merged-school range tops out at 462 and 445", fontsize=8.6, loc="left")
save(fig, "fig02_district_arithmetic", source="Feb 2026 Annual Enrollment Trend Report p. 9 (separate projections); Aug 25 2026 proposal deck p. 51 (range). Implied share of Mesa students following: 41–71% (2030-31), 49–75% (2027-28).")

# ---------- Fig 1: projections by run vs counts, two panels ----------
fig, axes = plt.subplots(1, 2, figsize=(PAGE_W, 3.0), sharex=True)
RUNC = {"jan2024": "#b9b8b3", "jan2025": "#7a7975", "jan2026": TEXT}; RUNL = {"jan2024": "Jan 2024 run", "jan2025": "Jan 2025 run (re-used Oct 2025)", "jan2026": "Jan 2026 run"}
for ax, sch in zip(axes, ["Bear Creek", "Mesa"]):
    col = ROLE["bear_creek" if sch == "Bear Creek" else "mesa"]
    a = off[off.school == sch].set_index("fall").funded_headcount; a = a.loc[2019:]
    ax.plot(a.index, a.values, color=col, lw=2.2, marker="o", ms=3.5, zorder=5, label="October count")
    p = vin[(vin.measure == "enrollment") & (vin.school == sch)].pivot(index="fall", columns="vintage", values="value")
    for v in ["jan2024", "jan2025", "jan2026"]:
        s_ = p[v].dropna(); ax.plot(s_.index, s_.values, color=RUNC[v], lw=1.4, ls="--", marker="s", ms=2.5, label=RUNL[v])
        ax.text(s_.index[-1] + 0.15, s_.values[-1], f"{s_.values[-1]:.0f}", fontsize=7, color=RUNC[v], va="center")
    y25, y26 = p.loc[2029, "jan2025"], p.loc[2029, "jan2026"]
    ax.annotate("", xy=(2029, y26), xytext=(2029, y25), arrowprops=dict(arrowstyle="-|>", color=col, lw=1.2))
    ax.text(2028.85, (y25 + y26) / 2, f"{y26 - y25:+.0f} ({100 * (y26 - y25) / y25:+.0f}%)\nJan 2025 → Jan 2026", fontsize=6.6, color=col, va="center", ha="right")
    ax.set_title(sch, fontsize=9); ax.set_xlim(2018.5, 2031.5); ax.set_xticks([2019, 2021, 2023, 2025, 2027, 2029]); ax.set_xticklabels(["2019", "2021", "2023", "2025", "2027", "2029"]); ax.set_xlabel("October of school year"); ax.set_ylabel("students (K-5)")
axes[0].legend(loc="lower left", fontsize=6.5)
fig.suptitle("BVSD's 2029-30 projections moved +38 (Bear Creek) and −22 (Mesa) between the Jan 2025 and Jan 2026 runs", x=0.01, ha="left", fontsize=8.8, fontweight="bold")
save(fig, "fig01_vintages", source="Feb 2024 report p. 11; Feb 2025 report p. 9; Feb 2026 report p. 9; BVSD October pupil-count files")
summ = dict(sum_jan2026_2030=int(j26.loc[("Bear Creek", 2030)] + j26.loc[("Mesa", 2030)]), sum_jan2026_2027=int(j26.loc[("Bear Creek", 2027)] + j26.loc[("Mesa", 2027)]),
            bc_rev_2029=int(proj.loc[("Bear Creek", 2029), "jan2026"] - proj.loc[("Bear Creek", 2029), "jan2025"]), mesa_rev_2029=int(proj.loc[("Mesa", 2029), "jan2026"] - proj.loc[("Mesa", 2029), "jan2025"]),
            bc_rev_2028_j24_j26=int(proj.loc[("Bear Creek", 2028), "jan2026"] - proj.loc[("Bear Creek", 2028), "jan2024"]))
pd.Series(summ).to_csv(OUT / "summary01.csv"); print(summ)
