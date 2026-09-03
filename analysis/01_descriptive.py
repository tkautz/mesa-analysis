"""§1 Descriptive: how much have BVSD's own projections for Mesa and Bear Creek moved between runs,
and how does the proposal's post-merger range compare with the district's own separate numbers?
Outputs: figures/fig01_vintages.*, figures/fig02_range_arithmetic.*, analysis/output/table01_vintages.csv"""
import sys; sys.path.insert(0, "analysis")
from common import *
import matplotlib.pyplot as plt
style()
off = load_official(); vin = load_vintages(); rng = load_merged_range()

# ---------- Table 1: projections by vintage and target year ----------
proj = vin[(vin.measure == "enrollment")].pivot_table(index=["school", "fall"], columns="vintage", values="value")
act = off.set_index(["school", "fall"]).funded_headcount.rename("actual")
t1 = proj.join(act, how="outer").reset_index()
t1 = t1[t1.fall >= 2023].sort_values(["school", "fall"])
t1.to_csv(OUT / "table01_vintages.csv", index=False)
print(t1.to_string(index=False))

# ---------- Fig 1: spaghetti of vintages vs actuals ----------
fig, axes = plt.subplots(1, 3, figsize=(11, 3.6), sharey=False)
for ax, sch in zip(axes, ["Bear Creek", "Mesa", "Combined"]):
    if sch == "Combined":
        a = off.groupby("fall").funded_headcount.sum()
        p = vin[vin.measure == "enrollment"].groupby(["vintage", "fall"]).value.sum().unstack(0)
        p = p[(vin[vin.measure == "enrollment"].groupby(["vintage", "fall"]).value.count().unstack(0) == 2)]
    else:
        a = off[off.school == sch].set_index("fall").funded_headcount
        p = vin[(vin.measure == "enrollment") & (vin.school == sch)].pivot(index="fall", columns="vintage", values="value")
    ax.plot(a.index, a.values, color=TEXT, lw=2.2, marker="o", ms=3.5, label="October count (official)", zorder=5)
    for v in ["jan2024", "jan2025", "jan2026"]:
        s = p[v].dropna()
        ax.plot(s.index, s.values, color=VINTAGE_COLOR[v], lw=1.8, ls="--", marker="s", ms=3, label=VINTAGE_LABEL[v].split(" (")[0])
    if sch == "Bear Creek":
        lo = rng[(rng.measure == "enrolled_students_low")].set_index("school_year").value; hi = rng[(rng.measure == "enrolled_students_high")].set_index("school_year").value
        yrs = [sy_to_fall(y) for y in lo.index]
        ax.fill_between(yrs, lo.values, hi.values, color=VINTAGE_COLOR["aug2026"], alpha=0.18, label="Aug 2026 post-merger range")
        ax.plot(yrs, hi.values, color=VINTAGE_COLOR["aug2026"], lw=1.2); ax.plot(yrs, lo.values, color=VINTAGE_COLOR["aug2026"], lw=1.2)
        ax.axhline(CAPACITY["Bear Creek"], color=MUTED, lw=0.8, ls=":"); ax.text(2014.2, CAPACITY["Bear Creek"] + 4, "capacity 492", color=MUTED, fontsize=8)
        ax.axhline(THREE_ROUNDS, color=MUTED, lw=0.8, ls=":"); ax.text(2014.2, THREE_ROUNDS + 4, "3 rounds (~450)", color=MUTED, fontsize=8)
    if sch == "Mesa":
        ax.axhline(TWO_ROUNDS, color=MUTED, lw=0.8, ls=":"); ax.text(2014.2, TWO_ROUNDS + 4, "2 rounds (~300)", color=MUTED, fontsize=8)
    if sch == "Combined":
        ax.axhline(CAPACITY["Bear Creek"], color=MUTED, lw=0.8, ls=":"); ax.text(2014.2, CAPACITY["Bear Creek"] + 6, "Bear Creek capacity 492", color=MUTED, fontsize=8)
        ax.fill_between([2027, 2030], [392, 403], [445, 462], color=VINTAGE_COLOR["aug2026"], alpha=0.18, label="Aug 2026 post-merger range")
    ax.set_title(f"{sch}" + (" (Mesa + Bear Creek)" if sch == "Combined" else ""))
    ax.set_xlim(2014, 2031); ax.set_xlabel("October of school year"); ax.set_ylabel("students (K-5)")
h, l = axes[0].get_legend_handles_labels(); fig.legend(h, l, loc="lower center", ncol=5, fontsize=8, bbox_to_anchor=(0.5, -0.06))
fig.suptitle("BVSD's projections for the two schools were revised substantially between annual runs", x=0.01, ha="left", fontsize=11, fontweight="bold")
save(fig, "fig01_vintages")

# ---------- Fig 2: the arithmetic behind 403–462 ----------
sep_2030 = vin[(vin.vintage == "jan2026") & (vin.measure == "enrollment") & (vin.fall == 2030)].set_index("school").value
sep_2027 = vin[(vin.vintage == "jan2026") & (vin.measure == "enrollment") & (vin.fall == 2027)].set_index("school").value
res_now = 275 + 228
items = [
    ("Bear Creek + Mesa, Jan 2026 projections, 2030-31", sep_2030.sum(), None),
    ("Bear Creek + Mesa, Jan 2026 projections, 2027-28", sep_2027.sum(), None),
    ("Bear Creek + Mesa, actual Oct 2025", 312 + 224, None),
    ("Resident students of both areas, 2025-26 (deck p.51)", res_now, None),
    ("Resident students, combined area, 2030-31 (deck p.51)", 522, None),
    ("Resident students, combined area, 2027-28 (deck p.51)", 473, None),
    ("Proposal: merged enrollment 2030-31 (deck p.51)", 403, 462),
    ("Proposal: merged enrollment 2027-28 (deck p.51)", 392, 445),
]
fig, ax = plt.subplots(figsize=(8.6, 4.2))
for i, (lab, lo, hi) in enumerate(items[::-1]):
    y = i
    if hi is None:
        ax.plot([lo], [y], "o", color=SCHOOL_COLOR["Combined"], ms=7); ax.text(lo + 4, y, f"{lo:.0f}", va="center", fontsize=8.5)
    else:
        ax.plot([lo, hi], [y, y], color=VINTAGE_COLOR["aug2026"], lw=6, solid_capstyle="round"); ax.text(hi + 4, y, f"{lo}–{hi}", va="center", fontsize=8.5)
ax.set_yticks(range(len(items))); ax.set_yticklabels([x[0] for x in items[::-1]], fontsize=8.5)
for x, lab in [(THREE_ROUNDS, "3 rounds (~450)"), (CAPACITY["Bear Creek"], "capacity 492"), (0.95 * 492, "95% of capacity")]:
    ax.axvline(x, color=MUTED, lw=0.9, ls=":"); ax.text(x, len(items) - 0.4, lab, rotation=90, va="top", ha="right", fontsize=7.5, color=MUTED)
ax.set_xlim(300, 560); ax.set_xlabel("students at Bear Creek (K-5)"); ax.grid(axis="y", visible=False)
ax.set_title("The proposal's own range sits below the sum of its own projections for the two schools")
save(fig, "fig02_range_arithmetic")

# numbers for the report
summ = dict(sum_jan2026_2030=int(sep_2030.sum()), sum_jan2026_2027=int(sep_2027.sum()),
            bc_rev_2029=int(proj.loc[("Bear Creek", 2029), "jan2026"] - proj.loc[("Bear Creek", 2029), "jan2025"]),
            mesa_rev_2029=int(proj.loc[("Mesa", 2029), "jan2026"] - proj.loc[("Mesa", 2029), "jan2025"]),
            bc_rev_2028_j24_j26=int(proj.loc[("Bear Creek", 2028), "jan2026"] - proj.loc[("Bear Creek", 2028), "jan2024"]))
pd.Series(summ).to_csv(OUT / "summary01.csv"); print(summ)
