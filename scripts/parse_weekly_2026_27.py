"""Parse BVSD's 2026-27 weekly "Enrollment Count" PDFs (data/raw/bvsd/enrollment_2026-27_weekly/*.txt).

Source: bvsd.org/departments/enrollment/enrollment-statistics (retrieved 2026-09-03). Each file is
The Student Enrollment Center's count on the stated date: CDE funded heads for Oct 2023/2024/2025
("adjusted to exclude PK") and "Today's Enrollment" with a K-5 grade breakdown for elementary schools.
Output: data/clean/enrollment_2026-27_weekly_elementary.csv (date, school, oct2023, oct2024, oct2025,
count, k, g1, g2, g3, g4, g5). These are preliminary in-year counts, not the official October count.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "bvsd" / "enrollment_2026-27_weekly"
OUT = ROOT / "data" / "clean" / "enrollment_2026-27_weekly_elementary.csv"
ROW = re.compile(r"^([A-Z][A-Z0-9 .&'\-/]+?)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$")


def main() -> None:
    rows = []
    for p in sorted(RAW.glob("enrollment_*.txt")):
        date = p.stem.replace("enrollment_", "")
        txt = p.read_text(encoding="utf-8")
        block = txt.split("ELEMENTARY", 1)[1].split("TOTAL ELEMENTARY", 1)[0]
        for line in block.splitlines():
            m = ROW.match(line.strip())
            if m:
                name = m.group(1).strip()
                nums = [int(x.replace(",", "")) for x in m.groups()[1:]]
                rows.append(dict(date=date, school=name, oct2023=nums[0], oct2024=nums[1], oct2025=nums[2],
                                 count=nums[3], k=nums[4], g1=nums[5], g2=nums[6], g3=nums[7], g4=nums[8], g5=nums[9]))
        tot = re.search(r"TOTAL ELEMENTARY\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)", txt)
        if tot:
            rows.append(dict(date=date, school="TOTAL ELEMENTARY", **{k: int(v.replace(",", "")) for k, v in
                             zip(["oct2023", "oct2024", "oct2025", "count"], tot.groups())}))
    df = pd.DataFrame(rows)
    df.to_csv(OUT, index=False)
    print(df[df.school.isin(["BEAR CREEK", "MESA", "TOTAL ELEMENTARY"])].to_string(index=False))
    n_schools = df[df.date == df.date.max()].school.nunique()
    print(f"\n{len(df)} rows; {n_schools} schools on {df.date.max()} -> {OUT}")


if __name__ == "__main__":
    main()
