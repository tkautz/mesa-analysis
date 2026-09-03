"""§3 Independent projection with honest uncertainty.
Model A (primary): grade-progression (cohort-survival) model per school, joint block bootstrap over years.
  For each simulated future year, one historical year t* is drawn at random (same t* for every grade and
  every school in the draw, so the 2020 shock stays one event and cross-school correlation is kept) and that
  year's kindergarten growth ratio and grade-progression ratios are applied. 10,000 paths to fall 2030.
Model B (robustness): random walk with drift on log total enrollment; drift and sigma from 2014-2025 log-differences
  (drift uncertainty via bootstrap of the differences).
Backtest: fit through fall 2023 -> predict 2024, 2025 (compare with BVSD's Jan 2024 run); fit through 2024 -> predict 2025
  (compare with the Jan 2025 run). Coverage of 50/80/95% intervals across all elementary schools.
Outputs: analysis/output/paths_modelA.npz (Mesa, Bear Creek joint paths), quantile tables, figures/fig05_fan.*, fig06_backtest.*"""
import sys, re; sys.path.insert(0, "analysis")
from common import *
import numpy as np, pandas as pd, matplotlib.pyplot as plt
style(); rng = np.random.default_rng(20260903)
N = 10000; GR = ["K", "G1", "G2", "G3", "G4", "G5"]

allsch = load_all_schools()
def norm(s): return re.sub(r"[^a-z]", "", str(s).lower())
ALIAS = {"aspencreekk8k5": "aspencreekk8", "eldoradok8k5": "eldoradok8", "monarchk8schoolk5": "monarchk8school", "whittierinternationalelementaryschool": "whittierinternationalelementary", "meadowlarkschoolk5": "meadowlarkschool", "horizonsk8schoolk5": "horizonsk8school", "peaktopeakk12charterk5": "peaktopeakk12charter"}
allsch["key"] = allsch.school_as_printed.map(norm).replace(ALIAS)
allsch = allsch.dropna(subset=["K"])
# schools with a full 2014-2025 K-5 record (drop programs / tiny mountain schools for the calibration set)
full = allsch.groupby("key").fall.nunique(); keys = [k for k in full[full == 12].index if k not in ("goldhillelementaryschool", "jamestownelementaryschool", "boulderuniversal", "communitybased", "mapletonearlychildhoodcenter", "boulderexplore")]
G = {k: allsch[allsch.key == k].set_index("fall")[GR].astype(float).sort_index() for k in keys}
print(len(keys), "schools in calibration set")

def ratios(g, upto):
    """kindergarten growth ratio and grade progression ratios by year, using data through fall `upto`."""
    g = g.loc[:upto]
    kg = (g.K / g.K.shift(1)).dropna()
    pr = pd.DataFrame({f"r{i}": (g[GR[i]] / g[GR[i - 1]].shift(1)) for i in range(1, 6)}).dropna()
    return kg, pr

def k_trend(g, upto, n, r):
    """log K = a + b*(t - upto) + e, OLS on years <= upto; (a, b) by pairs-bootstrap (n draws); residuals by year."""
    g = g.loc[:upto]; t = (g.index.values - upto).astype(float); y = np.log(g.K.values)
    X = np.c_[np.ones_like(t), t]; beta = np.linalg.lstsq(X, y, rcond=None)[0]; resid = y - X @ beta
    idx = r.integers(0, len(t), size=(n, len(t)))
    A = np.zeros(n); B = np.zeros(n)
    for i in range(n):
        Xi, yi = X[idx[i]], y[idx[i]]; b = np.linalg.lstsq(Xi, yi, rcond=None)[0]; A[i], B[i] = b
    return A, B, pd.Series(resid, index=g.index), beta

def simulate_A(gdict, upto, horizon, n=N, k_mode="trend", seed=None, level_window=3):
    """Joint simulation for a dict of schools. Returns {key: (totals (n,horizon), grades (n,horizon,6))}.
    k_mode: 'trend' (log-linear trend in K with parameter uncertainty), 'level' (K held at the 2023-25 mean, with
    parameter uncertainty from a bootstrap of the three window years and mean-centred year noise), 'rw' (random walk
    in K, bootstrapped growth ratios; over-disperses, shown for reference). The two K specifications are co-equal.
    level_window: number of years in the level window (default 3)."""
    r = np.random.default_rng(seed) if seed is not None else rng
    pools = {k: ratios(g, upto) for k, g in gdict.items()}
    yrs = list(next(iter(pools.values()))[1].index)                     # years with progression ratios (2015..upto)
    draws = r.choice(len(yrs), size=(n, horizon))                        # same historical year for all schools/grades
    out = {}
    for k, g in gdict.items():
        kg, pr = pools[k]; kg = kg.loc[yrs].values; pr = pr.loc[yrs].values
        A, B, resid, beta = k_trend(g, upto, n, r); resid = resid.loc[yrs].values
        # level spec: E[K] = window mean. Noise = trend residuals mean-centred in log space (the raw residual pool is skewed);
        # parameter uncertainty = bootstrap resample of the window years (one draw per path).
        win = g.loc[upto - level_window + 1:upto, "K"].values
        lvl = np.log(win[r.integers(0, len(win), size=(n, len(win)))].mean(1))
        resid_c = resid - resid.mean()
        cur = np.tile(g.loc[upto, GR].values, (n, 1)).astype(float)
        tot = np.zeros((n, horizon)); grades = np.zeros((n, horizon, 6))
        for h in range(horizon):
            d = draws[:, h]; nxt = np.empty_like(cur)
            if k_mode == "trend":   nxt[:, 0] = np.exp(A + B * (h + 1) + resid[d])
            elif k_mode == "level": nxt[:, 0] = np.exp(lvl + resid_c[d])
            elif k_mode == "rw":    nxt[:, 0] = cur[:, 0] * kg[d]
            for i in range(1, 6): nxt[:, i] = cur[:, i - 1] * pr[d, i - 1]
            cur = nxt; tot[:, h] = cur.sum(1); grades[:, h] = cur
        out[k] = (tot, grades)
    return out

def simulate_B(total, upto, horizon, n=N, seed=99):
    """Check model: random walk with drift on log totals. Drift bootstrapped from historical log-differences, drawn ONCE per
    path; the innovation sequence is generated from a fixed seed so that schools simulated separately share shocks."""
    rB = np.random.default_rng(seed)
    s = np.log(total.loc[:upto]); d = s.diff().dropna().values
    drift = rB.choice(d, size=(n, len(d))).mean(1)
    z = rB.standard_normal((n, horizon))
    paths = np.zeros((n, horizon)); cur = np.full(n, s.loc[upto])
    for h in range(horizon):
        cur = cur + drift + d.std(ddof=1) * z[:, h]
        paths[:, h] = np.exp(cur)
    return paths

def qtab(paths, first_fall, name):
    q = np.percentile(paths, [2.5, 10, 25, 50, 75, 90, 97.5], axis=0)
    return pd.DataFrame(q.T, columns=["p2.5", "p10", "p25", "p50", "p75", "p90", "p97.5"], index=[first_fall + i for i in range(paths.shape[1])]).rename_axis("fall").assign(series=name)

# ---------------- main projection: fit through fall 2025, horizon 5 (2026..2030) ----------------
pair = {"bearcreekelementary": G["bearcreekelementary"], "mesaelementaryschool": G["mesaelementaryschool"]}
simA = simulate_A(pair, 2025, 5)
bc, mesa = simA["bearcreekelementary"][0], simA["mesaelementaryschool"][0]
simL = simulate_A(pair, 2025, 5, k_mode="level", seed=3); simR = simulate_A(pair, 2025, 5, k_mode="rw", seed=4)
bcL, mesaL = simL["bearcreekelementary"][0], simL["mesaelementaryschool"][0]
np.savez_compressed(OUT / "paths_modelA.npz", bear_creek=bc, mesa=mesa, bear_creek_level=simL["bearcreekelementary"][0], mesa_level=simL["mesaelementaryschool"][0], bear_creek_rw=simR["bearcreekelementary"][0], mesa_rw=simR["mesaelementaryschool"][0], bear_creek_grades=simA["bearcreekelementary"][1], mesa_grades=simA["mesaelementaryschool"][1], falls=np.arange(2026, 2031))
tot = load_official()
totB = {s: simulate_B(tot[tot.school == s].set_index("fall").funded_headcount.astype(float), 2025, 5) for s in ["Bear Creek", "Mesa"]}
tabs = pd.concat([qtab(bc, 2026, "A Bear Creek"), qtab(mesa, 2026, "A Mesa"), qtab(bc + mesa, 2026, "A Combined"), qtab(bcL, 2026, "A-level Bear Creek"), qtab(mesaL, 2026, "A-level Mesa"), qtab(bcL + mesaL, 2026, "A-level Combined"), qtab(simR["bearcreekelementary"][0] + simR["mesaelementaryschool"][0], 2026, "A-rw Combined"),
                  qtab(totB["Bear Creek"], 2026, "B Bear Creek"), qtab(totB["Mesa"], 2026, "B Mesa"), qtab(totB["Bear Creek"] + totB["Mesa"], 2026, "B Combined")])
tabs.round(0).to_csv(OUT / "table03_intervals.csv"); print(tabs.round(0).to_string())

# ---------------- backtest across all schools ----------------
bt = []
for spec in ("trend", "level"):
    for upto, vint in [(2023, "jan2024"), (2024, "jan2025")]:
        sim = simulate_A(G, upto, 2 if upto == 2023 else 1, n=4000, seed=7, k_mode=spec)
        # BCSIS and High Peaks are one row (BCSIS-HP) in the district's tables: sum the two simulated schools for the comparison
        if "bcsis" in sim and "highpeakselementary" in sim:
            sim["bcsis"] = (sim["bcsis"][0] + sim["highpeakselementary"][0], None); del sim["highpeakselementary"]
        for k, (t, _) in sim.items():
            for h in range(t.shape[1]):
                fall = upto + 1 + h
                if k == "bcsis": act = G["bcsis"].loc[fall, GR].sum() + G["highpeakselementary"].loc[fall, GR].sum()
                else: act = G[k].loc[fall, GR].sum() if fall in G[k].index else np.nan
                q = np.percentile(t[:, h], [2.5, 10, 25, 50, 75, 90, 97.5])
                bt.append(dict(spec=spec, key=k, fit_through=upto, vintage=vint, target_fall=fall, horizon=h + 1, actual=act, p50=q[3], p2_5=q[0], p10=q[1], p25=q[2], p75=q[4], p90=q[5], p97_5=q[6],
                               in50=(q[2] <= act <= q[4]), in80=(q[1] <= act <= q[5]), in95=(q[0] <= act <= q[6]), above_p90=(act > q[5]), below_p10=(act < q[1]),
                               ape_model=100 * abs(q[3] - act) / act, pct_err_model=100 * (q[3] - act) / act))
bt = pd.DataFrame(bt)
# BVSD's own errors for the same school-years (from §2)
err = pd.read_csv(CLEAN / "projection_errors_all_schools.csv"); err["key"] = err.school.map(norm).replace(ALIAS)
bt = bt.merge(err[["key", "vintage", "target_fall", "abs_pct_error"]].rename(columns={"abs_pct_error": "ape_bvsd"}), on=["key", "vintage", "target_fall"], how="left")
bt.to_csv(CLEAN / "backtest_modelA_all_schools.csv", index=False)
cov = bt.groupby(["spec", "horizon"]).agg(n=("key", "size"), cov50=("in50", "mean"), cov80=("in80", "mean"), cov95=("in95", "mean"), n_above_p90=("above_p90", "sum"), n_below_p10=("below_p10", "sum"),
                                         median_ape_model=("ape_model", "median"), median_ape_bvsd=("ape_bvsd", "median"), mean_signed_model=("pct_err_model", "mean"),
                                         p90_ape_model=("ape_model", lambda s: s.quantile(.9)), p90_ape_bvsd=("ape_bvsd", lambda s: s.quantile(.9)), n_paired=("ape_bvsd", "count"))
print(cov.round(2).to_string()); cov.to_csv(OUT / "table03_backtest.csv")
print(bt[bt.key.isin(pair)].round(1)[["spec", "key", "vintage", "target_fall", "actual", "p50", "p10", "p90", "in80", "ape_model", "ape_bvsd"]].to_string(index=False))
# level-window sensitivity for the merged school, 2030-31, 90% following
sens = []
for w in (2, 3, 5, 6):
    sw = simulate_A(pair, 2025, 5, k_mode="level", seed=3, level_window=w, n=4000)
    E = sw["bearcreekelementary"][0][:, 4] + 0.9 * sw["mesaelementaryschool"][0][:, 4]
    sens.append(dict(level_window_years=w, window=f"{2026 - w}-{2025}", merged_2030_median=np.median(E), p10=np.percentile(E, 10), p90=np.percentile(E, 90), p_over_450=(E > 450).mean(), p_over_492=(E > 492).mean()))
# robustness: median-centred residuals instead of mean-centred (window 3)
def simulate_level_mediancentred(gdict, upto, horizon, n, seed):
    r = np.random.default_rng(seed); pools = {k: ratios(g, upto) for k, g in gdict.items()}; yrs = list(next(iter(pools.values()))[1].index)
    draws = r.choice(len(yrs), size=(n, horizon)); out = {}
    for k, g in gdict.items():
        kg, pr = pools[k]; pr = pr.loc[yrs].values; A, B, resid, beta = k_trend(g, upto, n, r); resid = resid.loc[yrs].values
        win = g.loc[upto - 2:upto, "K"].values; lvl = np.log(win[r.integers(0, 3, size=(n, 3))].mean(1)); resid_c = resid - np.median(resid)
        cur = np.tile(g.loc[upto, GR].values, (n, 1)).astype(float); tot = np.zeros((n, horizon))
        for h in range(horizon):
            d = draws[:, h]; nxt = np.empty_like(cur); nxt[:, 0] = np.exp(lvl + resid_c[d])
            for i in range(1, 6): nxt[:, i] = cur[:, i - 1] * pr[d, i - 1]
            cur = nxt; tot[:, h] = cur.sum(1)
        out[k] = tot
    return out
sm = simulate_level_mediancentred(pair, 2025, 5, 4000, 3); E = sm["bearcreekelementary"][:, 4] + 0.9 * sm["mesaelementaryschool"][:, 4]
sens.append(dict(level_window_years=3, window="2023-2025 (median-centred noise)", merged_2030_median=np.median(E), p10=np.percentile(E, 10), p90=np.percentile(E, 90), p_over_450=(E > 450).mean(), p_over_492=(E > 492).mean()))
sens = pd.DataFrame(sens); sens.to_csv(OUT / "table03_level_window_sensitivity.csv", index=False); print(sens.round(2).to_string(index=False))
# first-year kindergarten under each spec vs the last five observed intakes (Bear Creek)
k26 = {sp: np.percentile(simulate_A(pair, 2025, 1, k_mode=sp, seed=5, n=4000)["bearcreekelementary"][1][:, 0, 0], [10, 50, 90]) for sp in ("trend", "level")}
pd.DataFrame(k26, index=["p10", "p50", "p90"]).T.assign(observed_2021_25=str(G["bearcreekelementary"].loc[2021:2025, "K"].astype(int).tolist())).to_csv(OUT / "table03_k2026_by_spec.csv"); print(pd.DataFrame(k26, index=["p10", "p50", "p90"]).T.round(1))

# ---------------- Fig 5: fan charts ----------------
vin = load_vintages(); rngdeck = load_merged_range()
fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.8))  # legacy fan (superseded by fig05a/b in 04); kept for the record
hist = {"Bear Creek": tot[tot.school == "Bear Creek"].set_index("fall").funded_headcount, "Mesa": tot[tot.school == "Mesa"].set_index("fall").funded_headcount}
hist["Combined"] = hist["Bear Creek"] + hist["Mesa"]
sims = {"Bear Creek": bc, "Mesa": mesa, "Combined": bc + mesa}; falls = np.arange(2026, 2031)
simsL = {"Bear Creek": bcL, "Mesa": mesaL, "Combined": bcL + mesaL}
for ax, s in zip(axes, ["Bear Creek", "Mesa", "Combined"]):
    col = SCHOOL_COLOR[s]
    for lo, hi, a in [(2.5, 97.5, 0.15), (10, 90, 0.25), (25, 75, 0.4)]:
        ax.fill_between(np.r_[2025, falls], np.r_[hist[s].loc[2025], np.percentile(sims[s], lo, axis=0)], np.r_[hist[s].loc[2025], np.percentile(sims[s], hi, axis=0)], color=col, alpha=a, lw=0)
    ax.plot(np.r_[2025, falls], np.r_[hist[s].loc[2025], np.median(sims[s], axis=0)], color=col, lw=1.6, label="Model A (K trend): median, 50/80/95% bands")
    ax.plot(np.r_[2025, falls], np.r_[hist[s].loc[2025], np.median(simsL[s], axis=0)], color=C["green"], lw=1.6, label="Model A-level (K at 2023-25 mean): median, 80% band")
    for q in (10, 90): ax.plot(np.r_[2025, falls], np.r_[hist[s].loc[2025], np.percentile(simsL[s], q, axis=0)], color=C["green"], lw=1.0, ls=":")
    ax.plot(hist[s].index, hist[s].values, color=TEXT, lw=2.2, marker="o", ms=3, label="October count", zorder=5)
    p = vin[(vin.vintage == "jan2026") & (vin.measure == "enrollment")]
    pj = p.groupby("fall").value.sum() if s == "Combined" else p[p.school == s].set_index("fall").value
    ax.plot(pj.index, pj.values, color=VINTAGE_COLOR["jan2026"], ls="--", marker="s", ms=3, lw=1.6, label="BVSD Jan 2026 run")
    if s != "Mesa":
        ax.fill_between([2027, 2030], [392, 403], [445, 462], color=VINTAGE_COLOR["aug2026"], alpha=0.18, label="Aug 2026 post-merger range")
        ax.axhline(492, color=MUTED, lw=0.8, ls=":"); ax.text(2018.6, 495, "Bear Creek capacity 492", fontsize=7.5, color=MUTED)
        ax.axhline(450, color=MUTED, lw=0.8, ls=":"); ax.text(2018.6, 453, "3 rounds (~450)", fontsize=7.5, color=MUTED)
    ax.set_xlim(2018.5, 2030.5); ax.set_title(s if s != "Combined" else "Mesa + Bear Creek"); ax.set_xlabel("October of school year"); ax.set_ylabel("students (K-5)")
h, l = axes[0].get_legend_handles_labels(); fig.legend(h, l, loc="lower center", ncol=3, fontsize=7.5, bbox_to_anchor=(0.5, -0.1))
fig.suptitle("Independent cohort-survival projections under two kindergarten specifications vs BVSD's point projection", x=0.01, ha="left", fontsize=11, fontweight="bold")
save(fig, "fig05_fan")

# ---------------- Fig 6: backtest (appendix) ----------------
fig, axes = plt.subplots(1, 2, figsize=(PAGE_W, 2.9))
ax = axes[0]; x = np.arange(3); w = 0.2; greys = ["#3b3a37", "#7a7975", "#a9a8a3", "#cfcec9"]
for i, ((sp, h), d) in enumerate(cov.iterrows()):
    ax.bar(x + (i - 1.5) * w, [d.cov50, d.cov80, d.cov95], w, color=greys[i], label=f"{sp} spec, {h}-yr ahead (n={int(d.n)})")
for xx, nom in zip(x, [0.5, 0.8, 0.95]): ax.plot([xx - 0.45, xx + 0.45], [nom, nom], color=TEXT, lw=1.2)
ax.set_xticks(x); ax.set_xticklabels(["50% range", "80% range", "95% range"]); ax.set_ylim(0, 1.05); ax.set_ylabel("share of actual counts inside the range")
ax.set_title("Share of actuals inside each range, 26 schools\n(black tick = the share the range is designed to catch)", fontsize=8.5); ax.legend(loc="upper left", fontsize=6)
ax = axes[1]
d = bt[(bt.spec == "trend")].dropna(subset=["ape_bvsd"])
ax.scatter(d.ape_bvsd, d.ape_model, s=14, color=ROLE["background"], edgecolor="white", lw=0.4)
for k, col, lab in [("bearcreekelementary", ROLE["bear_creek"], "Bear Creek"), ("mesaelementaryschool", ROLE["mesa"], "Mesa")]:
    dd = d[d.key == k]; ax.scatter(dd.ape_bvsd, dd.ape_model, s=40, color=col, edgecolor=TEXT, lw=0.6, zorder=6, label=lab)
m = max(d.ape_bvsd.max(), d.ape_model.max()); ax.plot([0, m], [0, m], color=MUTED, lw=0.8, ls=":"); ax.text(m * 0.7, m * 0.72, "equal error", fontsize=7, color=MUTED, rotation=38)
ax.set_xlabel("BVSD projection: absolute error, %"); ax.set_ylabel("model central estimate: absolute error, %"); ax.set_title("Same school-years, trend spec: model vs BVSD", fontsize=8.5); ax.legend(fontsize=7)
save(fig, "fig06_backtest", source="BVSD October pupil-count files 2014-15 to 2025-26; Feb 2024 and Feb 2025 trend reports")
