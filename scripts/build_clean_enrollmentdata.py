"""Step 2: derive clean tables from the vendored enrollmentdata.org transcription.

Inputs (unmodified): data/raw/enrollmentdata/*.csv
Outputs: data/clean/BVSD_October_Headcount_2014-2025.csv (+ _source column)
         data/clean/BVSD_Capacity_Forecast_2025-2031.csv (+ _source column)
         data/clean/mesa_bearcreek_headcount.csv (Mesa + Bear Creek, long format)
"""
import pandas as pd
from pathlib import Path

RAW = Path("data/raw/enrollmentdata")
CLEAN = Path("data/clean")
SRC = "enrollmentdata.org transcription of BVSD October pupil count (github.com/yoavlurie/bvsd-enrollment, commit 37a9bf9, CC0)"
SRC_CAP = "enrollmentdata.org transcription of BVSD Feb 10 2026 Annual Enrollment Trend Report, elementary Capacity Summary 2025-26 (report p. 9) (github.com/yoavlurie/bvsd-enrollment, commit 37a9bf9, CC0)"

hc = pd.read_csv(RAW / "BVSD_October_Headcount_2014-2025.csv")
hc["_source"] = SRC
hc.to_csv(CLEAN / "BVSD_October_Headcount_2014-2025.csv", index=False)

cap = pd.read_csv(RAW / "BVSD_Capacity_Forecast_2025-2031.csv")
cap["_source"] = SRC_CAP
cap.to_csv(CLEAN / "BVSD_Capacity_Forecast_2025-2031.csv", index=False)

# Mesa + Bear Creek, long format: one row per school x year x measure
sub = hc[hc["school"].isin(["MESA", "BEAR CREEK"])].copy()
id_cols = ["school", "level", "october_year", "school_year"]
value_cols = [c for c in hc.columns if c not in id_cols + ["_source"]]
long = sub.melt(id_vars=id_cols, value_vars=value_cols, var_name="measure", value_name="value")
long = long.dropna(subset=["value"]).sort_values(["school", "october_year", "measure"])
long["data_type"] = "actual"  # October count = actual; no projections in this file
long["_source"] = SRC
long["_source_row"] = "data/raw/enrollmentdata/BVSD_October_Headcount_2014-2025.csv, rows where school in {MESA, BEAR CREEK}"
long.to_csv(CLEAN / "mesa_bearcreek_headcount.csv", index=False)
print(long.groupby(["school", "measure"]).size().unstack(fill_value=0))
