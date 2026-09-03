"""§4 Consolidation scenario grid. Merged enrollment at Bear Creek = Bear Creek path + r x Mesa path, where r is the share
of Mesa's students who enrol at Bear Creek (the rest open-enrol elsewhere). Uses the joint Model A paths.
Outputs: analysis/output/table04_scenarios.csv, figures/fig07_scenario_heatmap.*, fig08_class_size.*"""
import sys; sys.path.insert(0, "analysis")
from common import *
import numpy as np, pandas as pd, matplotlib.pyplot as plt
style()
P = np.load(OUT / "paths_modelA.npz"); falls = list(P["falls"])
SPECS = {"A-trend": (P["bear_creek"], P["mesa"]), "A-level": (P["bear_creek_level"], P["mesa_level"])}
SECTIONS = 21   # 3.5 rounds x 6 grades (deck p.51 capacity basis)
EFF_CAPS = [492, 470, 445]   # illustrative effective general-education capacities net of center-based program rooms (see report)
rs = np.round(np.arange(0.6, 1.0001, 0.05), 2); rows = []
for spec, (bc, mesa) in SPECS.items():
    for fall in (2027, 2030):
        j = falls.index(fall)
        for r in rs:
            E = bc[:, j] + r * mesa[:, j]
            row = dict(spec=spec, fall=fall, retention=r, median=np.median(E), p10=np.percentile(E, 10), p90=np.percentile(E, 90),
                       p_over_450=(E > 450).mean(), p_under_300=(E < 300).mean(),
                       class_size_median=np.median(E) / SECTIONS, class_size_p90=np.percentile(E, 90) / SECTIONS)
            for cap in EFF_CAPS: row[f"p_over_{cap}"] = (E > cap).mean()
            rows.append(row)
tab = pd.DataFrame(rows); tab.to_csv(OUT / "table04_scenarios.csv", index=False)
print(tab[tab.retention.isin([0.8, 0.9, 1.0])].round(2).to_string(index=False))
bc, mesa = SPECS["A-trend"]
# implied retention in BVSD's own range (deck p.51 vs Jan 2026 separate projections)
vin = load_vintages(); j26 = vin[(vin.vintage == "jan2026") & (vin.measure == "enrollment")].pivot(index="fall", columns="school", values="value")
impl = pd.DataFrame([dict(fall=2027, lo=392, hi=445, bc=j26.loc[2027, "Bear Creek"], mesa=j26.loc[2027, "Mesa"]), dict(fall=2030, lo=403, hi=462, bc=j26.loc[2030, "Bear Creek"], mesa=j26.loc[2030, "Mesa"])])
impl["r_implied_lo"] = (impl.lo - impl.bc) / impl.mesa; impl["r_implied_hi"] = (impl.hi - impl.bc) / impl.mesa; impl["sum_100pct"] = impl.bc + impl.mesa
impl.to_csv(OUT / "table04_implied_retention.csv", index=False); print(impl.round(2).to_string(index=False))

# Fig 7: probabilities by share following, both specs, 2030-31 (one panel)
fig, ax = plt.subplots(figsize=(PAGE_W, 3.0))
for spec, ls in [("A-trend", "-"), ("A-level", "--")]:
    t_ = tab[(tab.spec == spec) & (tab.fall == 2030)].sort_values("retention")
    for col, colr, lab in [("p_over_450", ROLE["merged"], "above 3 rounds (450)"), ("p_over_492", ROLE["proposal"], "above capacity (492)")]:
        ax.plot(t_.retention * 100, t_[col] * 100, ls=ls, color=colr, lw=2, marker="o", ms=3, label=f"{lab}, {'Trend' if spec == 'A-trend' else 'Level'} assumption")
        v = t_[t_.retention == 0.9][col].iloc[0] * 100; ax.text(91, v, f"{v:.0f}%", fontsize=7, va="center", color=colr)
ax.axvline(90, color=MUTED, lw=0.8, ls=":"); ax.text(90, 101, "90% follow", fontsize=7, color=MUTED, ha="center", va="bottom")
ax.set_xlabel("share of Mesa's students who enrol at Bear Creek"); ax.set_ylabel("chance in 2030-31, %"); ax.set_ylim(0, 100)
ax.set_xticks([60, 70, 80, 90, 100]); ax.set_xticklabels([f"{x}%" for x in [60, 70, 80, 90, 100]]); ax.legend(loc="upper left", fontsize=6.5)
ax.set_title("Chance the merged school exceeds three rounds or the building's capacity in 2030-31,\nby share of Mesa students who follow and by kindergarten assumption", fontsize=8.8, loc="left")
save(fig, "fig07_scenario_lines", source="independent cohort-survival model (analysis/03, 04); thresholds from Oct 2025 work session slide 8 and Feb 2026 report p. 9")

# Fig 8: class size as dot-range, both specs, 21 and 18 classrooms
rows8 = []
for spec, (bcs, ms) in SPECS.items():
    for r in (0.8, 0.9, 1.0):
        E = bcs[:, j] + r * ms[:, j]
        for secs in (21, 18):
            rows8.append(dict(spec=spec, retention=r, sections=secs, p10=np.percentile(E, 10) / secs, p50=np.median(E) / secs, p90=np.percentile(E, 90) / secs))
cs = pd.DataFrame(rows8); cs.to_csv(OUT / "table04_class_size.csv", index=False)
fig, ax = plt.subplots(figsize=(PAGE_W, 3.2)); yy = 0; ticks = []
for spec in ("A-trend", "A-level"):
    for r in (0.8, 0.9, 1.0):
        for secs, colr in ((21, ROLE["merged"]), (18, "#9a99b8")):
            d = cs[(cs.spec == spec) & (cs.retention == r) & (cs.sections == secs)].iloc[0]
            ax.plot([d.p10, d.p90], [yy, yy], color=colr, lw=3, solid_capstyle="round", alpha=0.9); ax.plot([d.p50], [yy], "o", color="white", mec=colr, mew=1.8, ms=6)
            ax.text(d.p90 + 0.3, yy, f"{d.p50:.1f} ({d.p10:.0f}–{d.p90:.0f})", fontsize=6.5, va="center")
            ticks.append((yy, f"{'Trend' if spec == 'A-trend' else 'Level'}, {int(r * 100)}% follow, {secs} classrooms")); yy -= 1
        yy -= 0.4
ax.set_yticks([t for t, _ in ticks]); ax.set_yticklabels([l for _, l in ticks], fontsize=6.8)
for x, lab, dx in [(450 / 21, "450 students\nat 21 rooms", -0.15), (492 / 21, "492 students\nat 21 rooms", 0.15)]:
    ax.axvline(x, color=MUTED, lw=0.8, ls=":"); ax.text(x + dx, yy + 0.2, lab, fontsize=6.2, color=MUTED, ha="right" if dx < 0 else "left", va="top")
ax.set_xlabel("average students per classroom, 2030-31 (central estimate; 1-in-10 low to 1-in-10 high)"); ax.grid(axis="y", visible=False); ax.set_xlim(14, 36); ax.set_ylim(yy - 0.6, 0.8)
ax.set_title("Average class size at the merged school in 2030-31 at 21 classrooms (3.5 rounds) and 18 (3 rounds)", fontsize=8.8, loc="left")
save(fig, "fig08_class_size", source="independent cohort-survival model; capacity basis from deck p. 51 (492 seats, 3.5 rounds)")
# ---- effective-capacity table (both specs, r = 0.9 and 1.0, 2027-28 and 2030-31) ----
eff = tab[tab.retention.isin([0.9, 1.0])][["spec", "fall", "retention", "median", "p90", "p_over_445", "p_over_470", "p_over_492"]]
eff.to_csv(OUT / "table04_effective_capacity.csv", index=False); print(eff.round(2).to_string(index=False))

# ---- Fig 5a: Bear Creek alone under the two kindergarten assumptions, with the district's path ----
off = load_official(); vin = load_vintages()
hist = off[off.school == "Bear Creek"].set_index("fall").funded_headcount.loc[2018:]
pj = vin[(vin.vintage == "jan2026") & (vin.measure == "enrollment") & (vin.school == "Bear Creek")].set_index("fall").value
fig, ax = plt.subplots(figsize=(PAGE_W, 3.1)); yrs = np.r_[2025, falls]
for spec, key, ls in [("trend", "bear_creek", "-"), ("level", "bear_creek_level", "--")]:
    pth = P[key]; med = np.r_[hist.loc[2025], np.median(pth, axis=0)]; lo = np.r_[hist.loc[2025], np.percentile(pth, 10, axis=0)]; hi = np.r_[hist.loc[2025], np.percentile(pth, 90, axis=0)]
    if spec == "trend": ax.fill_between(yrs, lo, hi, color=ROLE["trend"], alpha=0.15, lw=0, label="Trend assumption: 80% range")
    else: ax.plot(yrs, lo, color=ROLE["level"], lw=1, ls=":"); ax.plot(yrs, hi, color=ROLE["level"], lw=1, ls=":", label="Level assumption: 80% range")
    ax.plot(yrs, med, color=ROLE[spec], lw=2, ls=ls, label=f"{spec.capitalize()} assumption: central estimate")
    ax.text(2030.15, med[-1], f"{med[-1]:.0f}", fontsize=7.5, color=ROLE[spec], va="center", fontweight="bold")
ax.plot(hist.index, hist.values, color=ROLE["bear_creek"], lw=2.2, marker="o", ms=3.5, label="October count", zorder=5)
ax.plot(pj.index, pj.values, color=ROLE["district_run"], lw=1.6, ls="--", marker="s", ms=3, label="BVSD Jan 2026 run", zorder=6)
ax.plot([2030], [pj.loc[2030]], "s", color=ROLE["district_run"], ms=6, zorder=7); ax.text(2030.15, pj.loc[2030] + 9, f"district {pj.loc[2030]:.0f}", fontsize=7.5, color=ROLE["district_run"], va="center", fontweight="bold")
ax.set_xlim(2017.5, 2031.6); ax.set_xlabel("October of school year"); ax.set_ylabel("Bear Creek students (K-5)"); ax.legend(loc="lower left", fontsize=6.5, ncol=2)
ax.set_title("Bear Creek alone: the district's 2030-31 projection (320) sits on the Level assumption's central estimate, above the Trend assumption's", fontsize=8.2, loc="left")
save(fig, "fig05a_bearcreek_two_specs", source="independent cohort-survival model (both kindergarten assumptions); Feb 2026 report p. 9 (district run); BVSD October pupil-count files")

# ---- Fig 5b: merged school at 90% following under both assumptions ----
fig, ax = plt.subplots(figsize=(PAGE_W, 3.1)); j27, j30 = falls.index(2027), falls.index(2030)
comb_hist = off.groupby("fall").funded_headcount.sum().loc[2018:]
for spec, ls in [("A-trend", "-"), ("A-level", "--")]:
    bcs, ms = SPECS[spec]; E = bcs + 0.9 * ms; key = "trend" if spec == "A-trend" else "level"
    med = np.r_[comb_hist.loc[2025], np.median(E, axis=0)]; lo = np.r_[comb_hist.loc[2025], np.percentile(E, 10, axis=0)]; hi = np.r_[comb_hist.loc[2025], np.percentile(E, 90, axis=0)]
    if key == "trend": ax.fill_between(yrs, lo, hi, color=ROLE["trend"], alpha=0.15, lw=0, label="Trend: 80% range")
    else: ax.plot(yrs, lo, color=ROLE["level"], lw=1, ls=":"); ax.plot(yrs, hi, color=ROLE["level"], lw=1, ls=":", label="Level: 80% range")
    ax.plot(yrs, med, color=ROLE[key], lw=2, ls=ls, label=f"{key.capitalize()}: central estimate")
    p492 = (E[:, j30] > 492).mean(); p450 = (E[:, j30] > 450).mean()
    ax.text(2030.15, med[-1], f"{med[-1]:.0f}\nP>492: {p492:.0%}\nP>450: {p450:.0%}", fontsize=6.8, color=ROLE[key], va="center")
ax.plot(comb_hist.index, comb_hist.values, color=ROLE["merged"], lw=2.2, marker="o", ms=3.5, label="October count, both schools", zorder=5)
ax.plot([2027, 2027], [392, 445], color=ROLE["proposal"], lw=5, solid_capstyle="butt"); ax.plot([2030, 2030], [403, 462], color=ROLE["proposal"], lw=5, solid_capstyle="butt", label="proposal's range (deck p. 51)")
for y, lab in [(450, "3 rounds (450)"), (492, "capacity (492)")]: ax.axhline(y, color=MUTED, lw=0.8, ls=":"); ax.text(2017.6, y + 4, lab, fontsize=6.8, color=MUTED)
ax.set_xlim(2017.5, 2032.2); ax.set_xlabel("October of school year"); ax.set_ylabel("students at Bear Creek if merged (K-5)"); ax.legend(loc="lower left", fontsize=6.5, ncol=2)
ax.set_title("Merged school with 90% of Mesa students following: the kindergarten assumption moves the 2030-31 estimate by about 70 students", fontsize=8.2, loc="left")
save(fig, "fig05b_merged_two_specs", source="independent cohort-survival model; proposal range from deck p. 51; October counts from BVSD pupil-count files")
