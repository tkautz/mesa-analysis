"""§2 How accurate have BVSD's school-level projections been? All elementary schools, three vintages.
Direct errors: Jan 2024 run vs Oct 2024 (1 yr) and Oct 2025 (2 yr); Jan 2025 run vs Oct 2025 (1 yr).
Revisions: same target year, successive runs, as a lower bound on uncertainty at 2-5 year horizons.
Outputs: data/clean/projection_errors_all_schools.csv, data/clean/projection_revisions_all_schools.csv,
         figures/fig03_errors_by_horizon.*, figures/fig04_revisions_by_horizon.*, analysis/output/summary02.csv"""
import sys, re; sys.path.insert(0, "analysis")
from common import *
import numpy as np, pandas as pd, matplotlib.pyplot as plt
style()
cap = pd.read_csv(CLEAN / "capacity_summary_all_schools_by_vintage.csv")
cap = cap[cap.ocr_check].copy()
cap["vintage"] = cap.vintage.replace({"feb2024": "jan2024", "feb2025": "jan2025", "feb2026": "jan2026"})
cap["base_fall"] = cap.base_year.map(sy_to_fall)
off = load_all_schools()
def norm(s): return re.sub(r"[^a-z]", "", str(s).lower())
ALIAS = {"aspencreekk8k5": "aspencreekk8", "eldoradok8k5": "eldoradok8", "monarchk8schoolk5": "monarchk8school", "whittierinternationalelementaryschool": "whittierinternationalelementary", "meadowlarkschoolk5": "meadowlarkschool"}
off["key"] = off.school_as_printed.map(norm).replace(ALIAS)
official = off.groupby(["key", "fall"]).funded_headcount.first()
def actual(school, fall):
    if school == "BCSIS":  # table row is BCSIS-HP = BCSIS + High Peaks
        return official.get(("bcsis", fall), np.nan) + official.get(("highpeakselementary", fall), np.nan)
    return official.get((norm(school), fall), np.nan)
MOUNTAIN = {"Gold Hill Elementary School", "Jamestown Elementary School"}

# ---------- direct errors ----------
rows = []
for _, r in cap.iterrows():
    for h in (1, 2):
        fall = r.base_fall + h; col = f"proj_{fall}-{str(fall + 1)[2:]}"
        if col not in r or pd.isna(r[col]): continue
        a = actual(r.school, fall)
        if fall > 2025 or pd.isna(a): continue
        rows.append(dict(vintage=r.vintage, school=r.school, target_fall=fall, horizon_years=h, projected=r[col], actual=a,
                         error=r[col] - a, pct_error=100 * (r[col] - a) / a, base_enroll=r.enroll_base, mountain=r.school in MOUNTAIN))
err = pd.DataFrame(rows); err["abs_pct_error"] = err.pct_error.abs()
err.to_csv(CLEAN / "projection_errors_all_schools.csv", index=False)
e = err[~err.mountain]
summ = e.groupby("horizon_years").agg(n=("school", "size"), median_ape=("abs_pct_error", "median"), mean_ape=("abs_pct_error", "mean"),
                                     p80_ape=("abs_pct_error", lambda s: s.quantile(.8)), p90_ape=("abs_pct_error", lambda s: s.quantile(.9)),
                                     max_ape=("abs_pct_error", "max"), mean_signed=("pct_error", "mean"), share_under=("pct_error", lambda s: (s < 0).mean()),
                                     rmse_pct=("pct_error", lambda s: np.sqrt((s ** 2).mean())))
print(summ.round(1).to_string())
small = e[e.base_enroll < 300].groupby("horizon_years").abs_pct_error.agg(["median", lambda s: s.quantile(.8), "size"])
print("schools < 300 students:\n", small.round(1).to_string())
print(err[err.school.str.contains("Mesa|Bear Creek")].round(1).to_string(index=False))
# district total from the reports themselves (elem. total rows): Feb 2024 proj 2024-25 9,842 vs Feb 2025 actual 9,952; Feb 2025 proj 2025-26 9,825 vs 9,689
tot = pd.DataFrame([dict(vintage="jan2024", target="2024-25", projected=9842, actual=9952), dict(vintage="jan2024", target="2025-26", projected=9619, actual=9689),
                    dict(vintage="jan2025", target="2025-26", projected=9825, actual=9689)])
tot["pct_error"] = 100 * (tot.projected - tot.actual) / tot.actual; print(tot.round(2).to_string(index=False))
tot.to_csv(OUT / "table02_district_totals.csv", index=False)

# ---------- revisions between runs for the same target year ----------
rev_rows = []
piv = {}
for _, r in cap.iterrows():
    for k in range(1, 6):
        fall = r.base_fall + k; col = f"proj_{fall}-{str(fall + 1)[2:]}"
        if col in r and not pd.isna(r[col]): piv[(r.school, r.vintage, fall)] = (r[col], k)
for (sch, v, fall), (p, k) in piv.items():
    nxt = {"jan2024": "jan2025", "jan2025": "jan2026"}.get(v)
    if nxt and (sch, nxt, fall) in piv:
        p2, k2 = piv[(sch, nxt, fall)]
        rev_rows.append(dict(school=sch, target_fall=fall, from_vintage=v, to_vintage=nxt, horizon_at_first=k, first=p, revised=p2,
                             revision=p2 - p, pct_revision=100 * (p2 - p) / p, mountain=sch in MOUNTAIN))
rev = pd.DataFrame(rev_rows); rev["abs_pct_revision"] = rev.pct_revision.abs()
rev.to_csv(CLEAN / "projection_revisions_all_schools.csv", index=False)
rv = rev[~rev.mountain]
rsum = rv.groupby("horizon_at_first").agg(n=("school", "size"), median_abs=("abs_pct_revision", "median"), p80_abs=("abs_pct_revision", lambda s: s.quantile(.8)),
                                          p90_abs=("abs_pct_revision", lambda s: s.quantile(.9)), max_abs=("abs_pct_revision", "max"))
print(rsum.round(1).to_string())
print(rev[rev.school.str.contains("Mesa|Bear Creek")].round(1).to_string(index=False))

# ---------- Fig 3: errors by horizon ----------
fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), gridspec_kw=dict(width_ratios=[1.3, 1]))
ax = axes[0]; rng = np.random.default_rng(1)
for h, x0 in [(1, 0), (2, 1)]:
    d = e[e.horizon_years == h]
    xs = x0 + rng.uniform(-0.18, 0.18, len(d))
    ax.scatter(xs, d.pct_error, s=18, color=C["blue"], alpha=0.55, edgecolor="white", lw=0.5)
    for sch, col in [("Bear Creek Elementary", SCHOOL_COLOR["Bear Creek"]), ("Mesa Elementary School", SCHOOL_COLOR["Mesa"])]:
        dd = d[d.school == sch]
        for _, q in dd.iterrows():
            ax.scatter([x0 + (0.22 if sch.startswith("Bear") else -0.22)], [q.pct_error], s=55, color=col, edgecolor=TEXT, lw=0.8, zorder=6)
            ax.annotate(f"{sch.split()[0]} {q.vintage[3:]}", (x0 + (0.22 if sch.startswith("Bear") else -0.22), q.pct_error), xytext=(6 if sch.startswith("Bear") else -6, 0), textcoords="offset points", ha="left" if sch.startswith("Bear") else "right", va="center", fontsize=7.5)
    q10, q90 = d.pct_error.quantile([.1, .9]); ax.plot([x0 - 0.3, x0 + 0.3], [q10, q10], color=MUTED, lw=1); ax.plot([x0 - 0.3, x0 + 0.3], [q90, q90], color=MUTED, lw=1)
    ax.text(x0 + 0.32, q90, "P90", fontsize=7, color=MUTED, va="center"); ax.text(x0 + 0.32, q10, "P10", fontsize=7, color=MUTED, va="center")
ax.axhline(0, color=TEXT, lw=0.8); ax.set_xticks([0, 1]); ax.set_xticklabels(["1 year ahead\n(n=%d)" % (e.horizon_years == 1).sum(), "2 years ahead\n(n=%d)" % (e.horizon_years == 2).sum()])
ax.set_ylabel("projection minus actual, % of actual"); ax.set_title("School-level projection errors, all BVSD elementary schools")
ax = axes[1]
ax.scatter(e.base_enroll, e.abs_pct_error, s=18, color=C["blue"], alpha=0.55, edgecolor="white", lw=0.5)
for sch, col in [("Bear Creek Elementary", SCHOOL_COLOR["Bear Creek"]), ("Mesa Elementary School", SCHOOL_COLOR["Mesa"])]:
    dd = e[e.school == sch]; ax.scatter(dd.base_enroll, dd.abs_pct_error, s=55, color=col, edgecolor=TEXT, lw=0.8, zorder=6, label=sch.split(" Elementary")[0])
ax.set_xlabel("school enrollment in the run's base year"); ax.set_ylabel("absolute error, %"); ax.set_title("Smaller schools, larger errors"); ax.legend(loc="upper right")
save(fig, "fig03_errors_by_horizon")

# ---------- Fig 4: revisions by horizon ----------
fig, ax = plt.subplots(figsize=(7.5, 3.8))
for k in sorted(rv.horizon_at_first.unique()):
    d = rv[rv.horizon_at_first == k]; xs = k + rng.uniform(-0.18, 0.18, len(d))
    ax.scatter(xs, d.pct_revision, s=18, color=C["blue"], alpha=0.55, edgecolor="white", lw=0.5)
    q10, q90 = d.pct_revision.quantile([.1, .9]); ax.plot([k - 0.3, k + 0.3], [q10, q10], color=MUTED, lw=1); ax.plot([k - 0.3, k + 0.3], [q90, q90], color=MUTED, lw=1)
for sch, col, dx in [("Bear Creek Elementary", SCHOOL_COLOR["Bear Creek"], 0.24), ("Mesa Elementary School", SCHOOL_COLOR["Mesa"], -0.24)]:
    dd = rv[rv.school == sch]; ax.scatter(dd.horizon_at_first + dx, dd.pct_revision, s=55, color=col, edgecolor=TEXT, lw=0.8, zorder=6, label=sch.split(" Elementary")[0])
ax.axhline(0, color=TEXT, lw=0.8); ax.set_xticks(range(1, 6)); ax.set_xticklabels([f"{k} yr" for k in range(1, 6)])
ax.set_xlabel("how far ahead the target year was in the earlier run"); ax.set_ylabel("next year's run minus this year's, % of this year's")
ax.set_title("Year-to-year revisions to the same target year, all schools (P10–P90 bars)"); ax.legend(loc="upper left")
save(fig, "fig04_revisions_by_horizon")

pd.concat([summ.add_prefix("err_"), rsum.add_prefix("rev_")], axis=1).to_csv(OUT / "summary02.csv")
