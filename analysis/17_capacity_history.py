"""§S3 Program-capacity history for the two buildings: School Profile books (2011, 2012, 2014) and the trend-report tables (Jan 2024, 2025, 2026).
Outputs: analysis/output/table17_capacity.csv"""
import sys; sys.path.insert(0, "analysis")
from common import *
import pandas as pd
prof = pd.read_csv(CLEAN / "school_profile_capacity_mesa_bearcreek.csv")
vint = pd.read_csv(CLEAN / "capacity_summary_mesa_bearcreek_by_vintage.csv")
print(vint.head(12).to_string())
cap = vint[vint.school_year == "capacity"]
rows = []
for _, r in prof.drop_duplicates(["school", "capacity_year"]).iterrows():
    rows.append(dict(school=r.school, as_of=f"{r.capacity_year} (School Profile book {r.book})", program_capacity=r.program_capacity, classrooms=r.possible_classrooms,
                     rounds=None, source=f"data/raw/bvsd/school_profiles/school_profiles_{r.book}.pdf, school page"))
label = {"feb2024": "Jan 2024 (Feb 2024 report p. 11)", "feb2025": "Jan 2025 (Feb 2025 report p. 9)", "feb2026": "Jan 2026 (Feb 2026 report p. 9)"}
for _, r in cap.iterrows():
    if r.measure in ("capacity", "program_capacity"):
        rounds = cap[(cap.school == r.school) & (cap.vintage == r.vintage) & (cap.measure.str.contains("round"))].value
        rows.append(dict(school=r.school, as_of=label.get(r.vintage, r.vintage), program_capacity=r.value, classrooms=None,
                         rounds=float(rounds.iloc[0]) if len(rounds) else None, source=r.get("_source", "trend report capacity table")))
tab = pd.DataFrame(rows).sort_values(["school", "as_of"]); tab.to_csv(OUT / "table17_capacity.csv", index=False); print(tab.to_string(index=False))
