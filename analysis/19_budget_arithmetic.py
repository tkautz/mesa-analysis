"""§S5 Budget arithmetic on published figures (FY2026-27 budget book, Uniform Budget Summary, CDE financial-transparency files, BVEA agreement).
What $3.5-4.0M a year buys; the package saving as a share of General Fund spending; the two schools' site budgets (the first Mesa-specific
figures in the record) and what part of them is formula-driven staffing that follows students.
Inputs: data/clean/budget_inputs_fy2027.csv, site_budgets_mesa_bearcreek_summary.csv (built 2026-09-04; see memo/notes_budget_inputs.md).
Outputs: analysis/output/table19_budget.csv, table19_site_budgets.csv"""
import sys; sys.path.insert(0, "analysis")
from common import *
import pandas as pd, numpy as np
inp = pd.read_csv(CLEAN / "budget_inputs_fy2027.csv"); site = pd.read_csv(CLEAN / "site_budgets_mesa_bearcreek_summary.csv")
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 60)
print(inp[["item", "value", "unit", "page_or_sheet"]].to_string(index=False)); print(site.to_string(index=False))
def get(pattern):
    m = inp[inp.item.str.contains(pattern, case=False, regex=True)]
    return float(str(m.value.iloc[0]).replace(",", "").replace("$", "")) if len(m) else np.nan
GF_BOOK = 386_231_155.0           # FY2026-27 budget book, General Fund proposed expenditures (txt pages 139/171; memo/notes_budget_inputs.md)
GF_UBS = 410_202_100.0            # CDE Uniform Budget Summary FY27 (B1); folds sub-funds into Fund 10, not comparable to the book figure
RATIO = 24.58                     # elementary classroom-teacher staffing formula, book p. 121
LOADED_TEACHER = 150_033.0        # derived: GF teachers & instructional support cost per FTE (notes); site-level at the two schools about 132,000
N_ELEM = 29
# site budgets (budget book per-school pages, FY27 General Fund; CDE financial-transparency fund-10 spending FY2024-25)
SITE = pd.DataFrame([dict(school="Mesa", fy27_book_gf_budget=3_024_735, fy27_fte=25.343, fy27_projected_pupils=217, fy25_cde_fund10_spending=3_518_665, fy25_school_administration=359_532, fy25_operations_maintenance=288_233, fy24_cde_fund10_spending=3_369_354),
                     dict(school="Bear Creek", fy27_book_gf_budget=3_688_335, fy27_fte=30.511, fy27_projected_pupils=299, fy25_cde_fund10_spending=3_977_000, fy25_school_administration=np.nan, fy25_operations_maintenance=np.nan, fy24_cde_fund10_spending=3_615_292)])
SITE["fy27_budget_per_projected_pupil"] = SITE.fy27_book_gf_budget / SITE.fy27_projected_pupils
SITE["fixed_lines_admin_plus_om_fy25"] = SITE.fy25_school_administration + SITE.fy25_operations_maintenance
SITE.to_csv(OUT / "table19_site_budgets_key.csv", index=False); print(SITE.round(0).to_string(index=False))
SAVINGS = (3.5e6, 4.0e6)
rows = []
for s in SAVINGS:
    rows.append(dict(item=f"package recurring saving ${s/1e6:.1f}M", share_of_GF_book=s / GF_BOOK if GF_BOOK == GF_BOOK else np.nan, share_of_GF_ubs=s / GF_UBS,
                     teacher_FTE_at_loaded_cost=s / LOADED_TEACHER, FTE_per_elementary_school=s / LOADED_TEACHER / N_ELEM, per_closed_school_of_six=s / 6))
tab = pd.DataFrame(rows); tab.to_csv(OUT / "table19_budget.csv", index=False); print(tab.round(3).to_string(index=False))
print(f"GF expenditures: book {GF_BOOK:,.0f}; UBS {GF_UBS:,.0f}; loaded teacher cost used {LOADED_TEACHER:,.0f}")
site.to_csv(OUT / "table19_site_budgets.csv", index=False)
