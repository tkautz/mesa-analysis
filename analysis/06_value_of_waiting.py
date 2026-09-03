"""§5 Value of waiting one year. Pre-posterior: draw a 2026 outcome from the current model, append it to the data, refit and
re-project 2030 (a 4-year horizon). Compare the expected 80% interval width for 2030-31 with today's 5-year-horizon width.
Outputs: analysis/output/table06_waiting.csv, figures/fig11_waiting.*"""
import sys, importlib.util; sys.path.insert(0, "analysis")
from common import *
import numpy as np, pandas as pd, matplotlib.pyplot as plt
style()
spec = importlib.util.spec_from_file_location("m3", "analysis/03_independent_projection.py")
# reuse the model functions without re-running the script body: exec only the definitions
src = open("analysis/03_independent_projection.py").read().split("# ---------------- main projection")[0]
ns = {}; exec(compile(src, "m3", "exec"), ns)
G, simulate_A, GR = ns["G"], ns["simulate_A"], ns["GR"]
pair = {"bearcreekelementary": G["bearcreekelementary"], "mesaelementaryschool": G["mesaelementaryschool"]}
rng = np.random.default_rng(11); r = 0.9
def width(sim, j): E = sim["bearcreekelementary"][0][:, j] + r * sim["mesaelementaryschool"][0][:, j]; return np.percentile(E, 90) - np.percentile(E, 10), np.median(E)
now = simulate_A(pair, 2025, 5, n=6000, seed=1); w_now, m_now = width(now, 4)
rows = [dict(decision_year=2026, information="today: counts through Oct 2025", horizon_years=5, width80_2030=w_now, median_2030=m_now)]
# pre-posterior for deciding in Sept 2027 (one more count) and Sept 2028 (two more)
ms_first = None
for extra in (1, 2):
    ws, ms = [], []
    for s in range(120):
        sim = simulate_A(pair, 2025, extra, n=1, seed=1000 + s)
        gd = {}
        for k, g in pair.items():
            g2 = g.copy()
            for h in range(extra): g2.loc[2025 + h + 1] = sim[k][1][0, h]
            gd[k] = g2.sort_index()
        fut = simulate_A(gd, 2025 + extra, 5 - extra, n=1500, seed=5000 + s); w, m = width(fut, 4 - extra); ws.append(w); ms.append(m)
    if extra == 1: ms_first = np.array(ms)
    rows.append(dict(decision_year=2026 + extra, information=f"{extra} more October count(s)", horizon_years=5 - extra, width80_2030=np.mean(ws), median_2030=np.mean(ms), width80_sd_across_outcomes=np.std(ws), median_spread_p10_p90=np.percentile(ms, 90) - np.percentile(ms, 10)))
tab = pd.DataFrame(rows); tab.to_csv(OUT / "table06_waiting.csv", index=False); print(tab.round(1).to_string(index=False))
swing = pd.DataFrame(dict(median_2030_given_2026=ms_by_outcome)) if False else None
fig, (ax0, ax) = plt.subplots(1, 2, figsize=(10, 3.8), gridspec_kw=dict(width_ratios=[1.1, 1], wspace=0.3))
ax0.hist(ms_first, bins=15, color=C["blue"], edgecolor="white")
ax0.axvline(m_now, color=TEXT, lw=1.2); ax0.text(m_now + 2, ax0.get_ylim()[1] * 0.9, f"today's central\nestimate {m_now:.0f}", fontsize=8)
lo, hi = np.percentile(ms_first, [10, 90]); ax0.axvline(lo, color=MUTED, ls=":"); ax0.axvline(hi, color=MUTED, ls=":")
ax0.set_xlabel("central estimate for merged 2030-31, given the Oct 2026 count"); ax0.set_ylabel("simulated Oct 2026 outcomes"); ax0.set_title(f"One count moves the answer:\nP10-P90 span {hi - lo:.0f} students (about ±{(hi - lo) / 50:.0f} classrooms)", fontsize=9)
ax.bar(tab.decision_year, tab.width80_2030, 0.55, color=C["blue"])
for x, w in zip(tab.decision_year, tab.width80_2030): ax.text(x, w + 3, f"{w:.0f} students", ha="center", fontsize=8.5)
ax.set_xticks(tab.decision_year); ax.set_xticklabels(["decide 2026\n(data to Oct 2025)", "decide 2027\n(+Oct 2026)", "decide 2028\n(+Oct 2027)"], fontsize=8.5)
ax.set_ylabel("width of 80% interval, merged 2030-31"); ax.set_title("Expected narrowing of the band\n(A-trend, 90% of Mesa follow)", fontsize=9)
save(fig, "fig11_waiting")
