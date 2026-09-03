"""Appendix B sensitivity: cross-school dependence of year shocks. The main model draws the same historical year for both schools
(reproducing the observed cross-school correlation, including 2020). The opposite extreme draws years independently per school
(zero correlation). The two bracket any common-plus-idiosyncratic decomposition. Outputs: analysis/output/table13_shock_sensitivity.csv"""
import sys; sys.path.insert(0, "analysis")
src = open("analysis/03_independent_projection.py").read(); exec(src[:src.index("def simulate_B")])   # data + simulate_A only
import numpy as np, pandas as pd
pair = {"bearcreekelementary": G["bearcreekelementary"], "mesaelementaryschool": G["mesaelementaryschool"]}
rows = []
for spec, seed in (("trend", None), ("level", 3)):
    joint = simulate_A(pair, 2025, 5, k_mode=spec, seed=seed if seed is not None else 11)
    ind_bc = simulate_A({"bearcreekelementary": pair["bearcreekelementary"]}, 2025, 5, k_mode=spec, seed=101)
    ind_m = simulate_A({"mesaelementaryschool": pair["mesaelementaryschool"]}, 2025, 5, k_mode=spec, seed=202)
    for lab, bc, m in (("joint (main)", joint["bearcreekelementary"][0], joint["mesaelementaryschool"][0]),
                       ("independent", ind_bc["bearcreekelementary"][0], ind_m["mesaelementaryschool"][0])):
        for fall, j in ((2027, 1), (2030, 4)):
            E = bc[:, j] + 0.9 * m[:, j]
            rows.append(dict(spec=spec, draw=lab, fall=fall, median=np.median(E), p10=np.percentile(E, 10), p90=np.percentile(E, 90),
                             width80=np.percentile(E, 90) - np.percentile(E, 10), p_over_450=(E > 450).mean(), p_over_492=(E > 492).mean(),
                             corr_bc_mesa=np.corrcoef(bc[:, j], m[:, j])[0, 1]))
t = pd.DataFrame(rows); t.to_csv(OUT / "table13_shock_sensitivity.csv", index=False); print(t.round(3).to_string(index=False))
