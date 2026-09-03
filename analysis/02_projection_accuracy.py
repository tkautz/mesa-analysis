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
MOUNTAIN = {"Gold Hill Elementary School", "Jamestown Elementary School"}   # the two tiny mountain schools (<30 students); Nederland is kept

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

# ---------- Fig 3: errors by horizon (left) and by school size (right) ----------
fig, axes = plt.subplots(1, 2, figsize=(PAGE_W, 3.0), gridspec_kw=dict(width_ratios=[1.25, 1]))
ax = axes[0]; rng = np.random.default_rng(1)
for h, x0 in [(1, 0), (2, 1)]:
    d = e[e.horizon_years == h]; xs = x0 + rng.uniform(-0.18, 0.18, len(d))
    ax.scatter(xs, d.pct_error, s=14, color=ROLE["background"], edgecolor="white", lw=0.4)
    for sch, col, dx in [("Bear Creek Elementary", ROLE["bear_creek"], 0.24), ("Mesa Elementary School", ROLE["mesa"], -0.24)]:
        for _, q in d[d.school == sch].iterrows():
            ax.scatter([x0 + dx], [q.pct_error], s=40, color=col, edgecolor=TEXT, lw=0.6, zorder=6)
            ax.annotate(f"{sch.split()[0]} {q.vintage[3:]}", (x0 + dx, q.pct_error), xytext=(5 if dx > 0 else -5, 0), textcoords="offset points", ha="left" if dx > 0 else "right", va="center", fontsize=6)
    q10, q90 = d.pct_error.quantile([.1, .9]); ax.plot([x0 - 0.3, x0 + 0.3], [q10, q10], color=TEXT, lw=1); ax.plot([x0 - 0.3, x0 + 0.3], [q90, q90], color=TEXT, lw=1)
    ax.text(x0 + 0.32, q90, f"1-in-10 high {q90:+.0f}%", fontsize=6, color=TEXT, va="center"); ax.text(x0 + 0.32, q10, f"1-in-10 low {q10:+.0f}%", fontsize=6, color=TEXT, va="center")
ax.axhline(0, color=TEXT, lw=0.8); ax.set_xticks([0, 1]); ax.set_xticklabels([f"1 year ahead (n={(e.horizon_years == 1).sum()})", f"2 years ahead (n={(e.horizon_years == 2).sum()})"], fontsize=7.5)
ax.set_ylabel("projection minus actual, % of actual"); ax.set_title("School-level projection errors, all BVSD elementary schools", fontsize=8.5); ax.set_xlim(-0.6, 1.9)
ax = axes[1]
bins = [(0, 300, "< 300"), (300, 400, "300–400"), (400, 10000, "> 400")]
for i, (lo, hi, lab) in enumerate(bins):
    for h, dx, colr in [(1, -0.18, "#7a7975"), (2, 0.18, TEXT)]:
        d = e[(e.horizon_years == h) & (e.base_enroll >= lo) & (e.base_enroll < hi)]
        if len(d) == 0: continue
        xs = i + dx + rng.uniform(-0.08, 0.08, len(d)); ax.scatter(xs, d.abs_pct_error, s=12, color=colr, alpha=0.6, edgecolor="white", lw=0.3, label=f"{h}-yr ahead" if i == 0 else None)
        ax.plot([i + dx - 0.13, i + dx + 0.13], [d.abs_pct_error.median()] * 2, color=colr, lw=1.6)
        ax.text(i + dx, -1.8, f"n={len(d)}", ha="center", fontsize=6, color=colr)
ax.set_xticks(range(3)); ax.set_xticklabels([b[2] for b in bins]); ax.set_xlabel("school size (base-year enrollment)"); ax.set_ylabel("absolute error, %"); ax.set_ylim(-3, 24)
ax.set_title("Absolute error by school size (bar = median)", fontsize=8.5); ax.legend(loc="upper right", fontsize=6.5)
save(fig, "fig03_errors_by_horizon", source="Feb 2024 and Feb 2025 trend reports (capacity tables) vs BVSD October pupil-count files 2024-25 and 2025-26; Gold Hill and Jamestown excluded")

# ---------- Fig 4: revisions by horizon ----------
fig, ax = plt.subplots(figsize=(PAGE_W, 2.8))
hz = sorted(rv.horizon_at_first.unique()); q10s, q90s = [], []
for k in hz:
    d = rv[rv.horizon_at_first == k]; xs = k + rng.uniform(-0.18, 0.18, len(d))
    ax.scatter(xs, d.pct_revision, s=14, color=ROLE["background"], edgecolor="white", lw=0.4)
    q10, q90 = d.pct_revision.quantile([.1, .9]); q10s.append(q10); q90s.append(q90)
ax.fill_between(hz, q10s, q90s, color=ROLE["merged"], alpha=0.12, lw=0, label="1-in-10 low to 1-in-10 high")
for sch, col, dx in [("Bear Creek Elementary", ROLE["bear_creek"], 0.24), ("Mesa Elementary School", ROLE["mesa"], -0.24)]:
    dd = rv[rv.school == sch]; ax.scatter(dd.horizon_at_first + dx, dd.pct_revision, s=40, color=col, edgecolor=TEXT, lw=0.6, zorder=6, label=sch.split(" Elementary")[0])
p80 = rv[rv.horizon_at_first.isin([4, 5])].abs_pct_revision.quantile(.8)
ax.text(4.5, q90s[-1] + 3, f"4–5 years out: 4 in 5 revisions are within ±{p80:.0f}%", ha="center", fontsize=6.8, color=ROLE["merged"])
ax.axhline(0, color=TEXT, lw=0.8); ax.set_xticks(hz); ax.set_xticklabels([f"{k} yr out\n(n={int((rv.horizon_at_first == k).sum())})" for k in hz], fontsize=7)
ax.set_xlabel("how far ahead the target year was in the earlier run"); ax.set_ylabel("next run minus this run, % of this run")
ax.set_title("Year-to-year revisions to the same target year, all schools", fontsize=8.5, loc="left"); ax.legend(loc="upper left", fontsize=6.5)
save(fig, "fig04_revisions_by_horizon", source="Feb 2024, Feb 2025 and Feb 2026 trend reports (capacity tables); Gold Hill and Jamestown excluded")

pd.concat([summ.add_prefix("err_"), rsum.add_prefix("rev_")], axis=1).to_csv(OUT / "summary02.csv")
