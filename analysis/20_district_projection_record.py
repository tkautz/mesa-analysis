"""§D The district's own scoring of its school-level projections, ten Octobers (2015-2019, 2021-2025).
Source: the "Compare Projection to Head Count" tables in the December/January enrollment packets (data/raw/bvsd/boarddocs/, BD1), parsed
by scripts/parse_district_projection_vs_headcount.py. Each table sets the spring "planning projection" for the coming October against the
funded head count. Elementary schools only, excluding the district's own asterisked outliers only where noted, and excluding Gold Hill and
Jamestown (under 25 students) from the percentiles.
Outputs: analysis/output/table20_accuracy_by_year.csv, table20_accuracy_summary.csv, table20_bear_creek_mesa.csv; figures/fig21_district_record.*"""
import sys; sys.path.insert(0, "analysis")
from common import *
import numpy as np, pandas as pd, matplotlib.pyplot as plt
style()
d = pd.read_csv(CLEAN / "district_projection_vs_headcount_2015_2025.csv")
e = d[(d.level == "elementary") & (~d.is_total.astype(bool))].copy()
e = e[~e.school.str.contains("GOLD HILL|JAMESTOWN|BOULDER EXPLORE|BU LINK|BOULDER UNIVERSAL|HALCYON|Total|TOTAL", regex=True)]   # tiny schools and online/alternative programs
e = e.dropna(subset=["planning_projection", "funded_headcount"]); e = e[e.funded_headcount > 0]
e["pct_err"] = 100 * (e.planning_projection - e.funded_headcount) / e.funded_headcount; e["abs_pct_err"] = e.pct_err.abs()
e["size_bin"] = pd.cut(e.funded_headcount, [0, 300, 400, 10000], labels=["under 300", "300-400", "over 400"])
print("projection dates by year:", d.groupby("october_year").projection_date.first().to_dict())
by_year = e.groupby("october_year").agg(n=("school", "size"), median_abs=("abs_pct_err", "median"), p80_abs=("abs_pct_err", lambda s: s.quantile(.8)), p90_abs=("abs_pct_err", lambda s: s.quantile(.9)),
                                       max_abs=("abs_pct_err", "max"), mean_signed=("pct_err", "mean"), share_over=("pct_err", lambda s: (s > 0).mean()))
by_year.to_csv(OUT / "table20_accuracy_by_year.csv"); print(by_year.round(1).to_string())
summ = pd.DataFrame([dict(group="all elementary, 10 Octobers", n=len(e), median_abs=e.abs_pct_err.median(), p80_abs=e.abs_pct_err.quantile(.8), p90_abs=e.abs_pct_err.quantile(.9), max_abs=e.abs_pct_err.max(),
                          mean_signed=e.pct_err.mean(), share_over=(e.pct_err > 0).mean())] +
                    [dict(group=f"size {b}", n=len(g), median_abs=g.abs_pct_err.median(), p80_abs=g.abs_pct_err.quantile(.8), p90_abs=g.abs_pct_err.quantile(.9), max_abs=g.abs_pct_err.max(), mean_signed=g.pct_err.mean(), share_over=(g.pct_err > 0).mean())
                     for b, g in e.groupby("size_bin", observed=True)] +
                    [dict(group="Bear Creek", n=(e.school == "BEAR CREEK").sum(), median_abs=e[e.school == "BEAR CREEK"].abs_pct_err.median(), p80_abs=np.nan, p90_abs=np.nan, max_abs=e[e.school == "BEAR CREEK"].abs_pct_err.max(), mean_signed=e[e.school == "BEAR CREEK"].pct_err.mean(), share_over=(e[e.school == "BEAR CREEK"].pct_err > 0).mean()),
                     dict(group="Mesa", n=(e.school == "MESA").sum(), median_abs=e[e.school == "MESA"].abs_pct_err.median(), p80_abs=np.nan, p90_abs=np.nan, max_abs=e[e.school == "MESA"].abs_pct_err.max(), mean_signed=e[e.school == "MESA"].pct_err.mean(), share_over=(e[e.school == "MESA"].pct_err > 0).mean())])
summ.to_csv(OUT / "table20_accuracy_summary.csv", index=False); print(summ.round(1).to_string(index=False))
bm = e[e.school.isin(["BEAR CREEK", "MESA"])][["october_year", "school", "planning_projection", "funded_headcount", "difference", "pct_err"]].sort_values(["school", "october_year"])
bm.to_csv(OUT / "table20_bear_creek_mesa.csv", index=False); print(bm.round(1).to_string(index=False))
# comparison with the report's existing one-year figures (Jan 2024 and Jan 2025 runs from the trend reports): overlap years 2024, 2025
prev = pd.read_csv(CLEAN / "projection_errors_all_schools.csv")
print("trend-report-based one-year errors (existing §4):", prev.groupby("vintage").abs_pct_error.median().round(1).to_dict())

# ---- Fig 21: strip plot of percent errors by October, Bear Creek and Mesa highlighted ----
fig, ax = plt.subplots(figsize=(PAGE_W, 3.0)); rng = np.random.default_rng(1)
for i, (yr, g) in enumerate(e.groupby("october_year")):
    x = i + rng.uniform(-0.18, 0.18, len(g)); ax.scatter(x, g.pct_err, s=12, color=ROLE["background"], edgecolor="white", lw=0.3, zorder=3)
    for s, colr in (("BEAR CREEK", ROLE["bear_creek"]), ("MESA", ROLE["mesa"])):
        v = g[g.school == s].pct_err
        if len(v): ax.scatter([i], v.values, s=42, color=colr, edgecolor=TEXT, lw=0.6, zorder=5, label=s.title() if i == 0 else None)
    q10, q90 = g.pct_err.quantile(.1), g.pct_err.quantile(.9); ax.plot([i - 0.3, i + 0.3], [q10, q10], color=MUTED, lw=0.9); ax.plot([i - 0.3, i + 0.3], [q90, q90], color=MUTED, lw=0.9)
ax.axhline(0, color=TEXT, lw=0.8); ax.set_xticks(range(len(by_year))); ax.set_xticklabels([f"Oct {y}" for y in by_year.index], fontsize=7)
ax.set_ylabel("projection minus count, % of count"); ax.legend(fontsize=7, loc="upper left")
ax.set_title(f"The district's own scoring: spring projection vs October count, all elementary schools, ten years (grey ticks: 1-in-10 low and high)", fontsize=8.2, loc="left")
save(fig, "fig21_district_record", source="BVSD 'Compare Projection to Head Count' tables in the Board's annual enrollment updates, Oct 2015-2025 (BoardDocs; data/raw/bvsd/boarddocs/); Gold Hill, Jamestown and online programs excluded")
