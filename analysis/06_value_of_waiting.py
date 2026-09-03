"""What one more October count would change. Pre-posterior: draw a 2026 outcome from the model, append it, refit, re-project
2030-31; repeat 120 times under each kindergarten specification. Report the spread of the refit central estimate and the
expected band width. Outputs: analysis/output/table06_waiting.csv, figures/fig11_waiting.*"""
import sys; sys.path.insert(0, "analysis")
from common import *
import numpy as np, pandas as pd, matplotlib.pyplot as plt
style()
src = open("analysis/03_independent_projection.py").read().split("# ---------------- main projection")[0]
ns = {}; exec(compile(src, "m3", "exec"), ns)
G, simulate_A, GR = ns["G"], ns["simulate_A"], ns["GR"]
pair = {"bearcreekelementary": G["bearcreekelementary"], "mesaelementaryschool": G["mesaelementaryschool"]}
r = 0.9; NOUT = 120
def stats(sim, j): E = sim["bearcreekelementary"][0][:, j] + r * sim["mesaelementaryschool"][0][:, j]; return np.percentile(E, 90) - np.percentile(E, 10), np.median(E)
rows, dists = [], {}
for spec in ("trend", "level"):
    now = simulate_A(pair, 2025, 5, n=6000, seed=1, k_mode=spec); w_now, m_now = stats(now, 4)
    rows.append(dict(spec=spec, decision_year=2026, information="counts through Oct 2025", horizon_years=5, width80_2030=w_now, median_2030=m_now))
    for extra in (1, 2):
        ws, ms = [], []
        for s_ in range(NOUT):
            sim = simulate_A(pair, 2025, extra, n=1, seed=1000 + s_, k_mode=spec)
            gd = {}
            for k, g in pair.items():
                g2 = g.copy()
                for h in range(extra): g2.loc[2025 + h + 1] = sim[k][1][0, h]
                gd[k] = g2.sort_index()
            fut = simulate_A(gd, 2025 + extra, 5 - extra, n=1500, seed=5000 + s_, k_mode=spec); w, m = stats(fut, 4 - extra); ws.append(w); ms.append(m)
        ms = np.array(ms); lo, hi = np.percentile(ms, [10, 90])
        boot = [np.subtract(*np.percentile(np.random.default_rng(s_).choice(ms, len(ms)), [90, 10])) for s_ in range(500)]
        rows.append(dict(spec=spec, decision_year=2026 + extra, information=f"{extra} more October count(s)", horizon_years=5 - extra, width80_2030=np.mean(ws), median_2030=np.mean(ms),
                         median_spread_p10_p90=hi - lo, spread_ci90_lo=np.percentile(boot, 5), spread_ci90_hi=np.percentile(boot, 95),
                         share_above_462=(ms > 462).mean(), share_below_403=(ms < 403).mean(), share_above_492=(ms > 492).mean(), today_median=m_now))
        if extra == 1: dists[spec] = ms
tab = pd.DataFrame(rows); tab.to_csv(OUT / "table06_waiting.csv", index=False); print(tab.round(1).to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(PAGE_W, 3.1), sharey=True); fig.subplots_adjust(wspace=0.12, top=0.78)
for ax, spec in zip(axes, ("trend", "level")):
    ms = dists[spec]; m_now = tab[(tab.spec == spec) & (tab.decision_year == 2026)].median_2030.iloc[0]
    ax.axvspan(403, 462, color=ROLE["proposal"], alpha=0.10, lw=0)
    ax.hist(ms, bins=np.arange(330, 640, 12), color=ROLE[spec], edgecolor="white")
    ax.set_ylim(0, 24); ax.axvline(m_now, color=TEXT, lw=1.2); ax.text(m_now, 23.5, f"today's estimate {m_now:.0f}", fontsize=6.3, va="top", ha="center", bbox=dict(fc="white", ec="none", pad=1))
    for x, lab in [(450, "450"), (492, "492")]: ax.axvline(x, color=MUTED, lw=0.8, ls=":"); ax.text(x, 21, lab, fontsize=6.3, color=MUTED, ha="center", va="top", bbox=dict(fc="white", ec="none", pad=0.5))
    lo, hi = np.percentile(ms, [10, 90]); above = (ms > 462).mean(); below = (ms < 403).mean()
    ax.set_title(f"{'Trend' if spec == 'trend' else 'Level'} assumption\n1-in-10 low to high: {hi - lo:.0f} students apart\n{above:.0%} of counts land above 462; {below:.0%} below 403", fontsize=7.2, loc="left")
    ax.set_xlabel("estimate after the Oct 2026 count", fontsize=7.5); ax.set_xlim(330, 640)
axes[0].set_ylabel("simulated Oct 2026 outcomes (of 120)", fontsize=7.5); axes[0].text(432, 2, "proposal's\nrange", ha="center", fontsize=6.3, color=ROLE["proposal"])
fig.suptitle("Central estimate for merged 2030-31 enrollment after one more October count (90% of Mesa follow)", x=0.01, y=0.99, ha="left", fontsize=8.4, fontweight="bold")
save(fig, "fig11_waiting", source="independent cohort-survival model re-fitted after each of 120 simulated October 2026 counts (analysis/06)")
