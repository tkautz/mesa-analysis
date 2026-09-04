"""Parse BVSD's annual "Comparison Projections vs October YYYY Enrollment" tables.

Sources: data/raw/bvsd/boarddocs/*compare*head_count*.txt -- text layers of the BoardDocs
enrollment-update attachments for the October 2015 through October 2025 pupil counts (ten tables;
no October 2020 table was posted). Each table lists, per school, the PLANNING ENROLLMENT PROJECTION
(dated the preceding winter or spring), the FUNDED HEAD COUNT on the October count date, and the
DIFFERENCE (number and percent), with level subtotals (TOTAL ELEMENTARY / MIDDLE / SENIOR /
SECONDARY, GRAND TOTAL, and General Fund / Charter Fund subtotals). K-8 schools appear split as
"K-5" and "6-8" rows; charters are listed within their level.

Output: data/clean/district_projection_vs_headcount_2015_2025.csv, one row per printed row
(schools and totals). level is inferred from the section headers: elementary (ELEMENTARY LEVEL
page), middle (SECONDARY LEVEL page up to TOTAL MIDDLE), high (after TOTAL MIDDLE up to TOTAL
SENIOR), secondary (TOTAL SECONDARY) and district (GRAND TOTAL rows). A trailing "*" (the
district's "outlier results, excluded from averages" marker) is stripped from the school name and
recorded in the asterisk column. check_ok = planning_projection + difference == funded_headcount;
rows whose difference is not printed ("-" or absent) get check_ok False and are listed.
Run: python scripts/parse_district_projection_vs_headcount.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "bvsd" / "boarddocs"
OUT = ROOT / "data" / "clean" / "district_projection_vs_headcount_2015_2025.csv"

NUM = re.compile(r"^-?[\d,]+$")
PCT = re.compile(r"^-?\d+(?:\.\d+)?%$")
SECTION = re.compile(r"^(ELEMENTARY|SECONDARY) LEVEL\s+(\d{1,2}/\d{1,2}/\d{4})\s+(\d{1,2}/\d{1,2}/\d{4})")
TITLE_YEAR = re.compile(r"Oct(?:ober|\.)?\s+(\d{4})")

# Caller-supplied check values: october_year -> (planning_projection, funded_headcount).
EXPECTED = {
    "BEAR CREEK": {2015: (434, 441), 2016: (447, 438), 2017: (429, 448), 2018: (459, 425), 2019: (412, 400),
                   2021: (335, 345), 2022: (336, 342), 2023: (317, 298), 2024: (296, 318), 2025: (308, 312)},
    "MESA": {2015: (334, 320), 2016: (301, 287), 2017: (276, 271), 2018: (256, 260), 2019: (249, 261),
             2021: (240, 247), 2022: (264, 246), 2023: (239, 233), 2024: (218, 230), 2025: (230, 224)},
}


def to_int(tok: str) -> int:
    return int(tok.replace(",", ""))


def split_row(line: str):
    """Return (name, numeric tail tokens) for a data row, else None (titles, headers, footers)."""
    toks = line.split()
    tail: list[str] = []
    while toks and len(tail) < 4 and (NUM.match(toks[-1]) or PCT.match(toks[-1]) or toks[-1] == "-"):
        tail.insert(0, toks.pop())
    if len(tail) < 2 or not toks:
        return None
    name = " ".join(toks)
    if not re.match(r"[A-Za-z]", name):  # e.g. "1 of 2 05 Compare Proj-Head Count 15.xls"
        return None
    return name, tail


def parse_file(path: Path) -> list[dict]:
    meeting_date = path.stem[-10:]
    pages = path.read_text(encoding="utf-8").split("\x0c")
    title_years: list[int] = []
    rows: list[dict] = []
    level = proj_date = head_date = None
    for page_no, page in enumerate(pages, start=1):
        for raw in page.splitlines():
            line = raw.strip()
            if not line:
                continue
            if line.startswith("Compari"):
                m = TITLE_YEAR.search(line)
                if m:
                    title_years.append(int(m.group(1)))
                continue
            m = SECTION.match(line)
            if m:
                level = "elementary" if m.group(1) == "ELEMENTARY" else "middle"
                proj_date, head_date = m.group(2), m.group(3)
                continue
            parsed = split_row(line)
            if parsed is None:
                continue
            name, tail = parsed
            asterisk = name.endswith("*")
            school = name.rstrip("*").strip()
            up = school.upper()
            is_total = "TOTAL" in up
            row_level = level
            if is_total:
                for key, lvl in (("ELEM", "elementary"), ("MIDDLE", "middle"), ("SENIOR", "high"),
                                 ("SECONDARY", "secondary"), ("GRAND", "district")):
                    if key in up:
                        row_level = lvl
                        break
            proj, head = to_int(tail[0]), to_int(tail[1])
            diff = pct = None
            for tok in tail[2:]:
                if PCT.match(tok):
                    pct = float(tok.rstrip("%"))
                elif NUM.match(tok):
                    diff = to_int(tok)
            rows.append(dict(source_file=path.name, meeting_date=meeting_date, page=page_no,
                             projection_date=proj_date, headcount_date=head_date, level=row_level,
                             school=school, asterisk=asterisk, planning_projection=proj,
                             funded_headcount=head, difference=diff, pct_difference=pct, is_total=is_total))
            if up == "TOTAL MIDDLE":
                level = "high"
            elif up == "TOTAL SENIOR":
                level = "secondary"
    if not title_years or not rows:
        raise ValueError(f"{path.name}: no title year or no rows parsed")
    october_year = title_years[0]
    head_year = int(rows[0]["headcount_date"].split("/")[-1])
    if head_year != october_year:
        print(f"WARNING {path.name}: title says October {october_year} but count date is {rows[0]['headcount_date']}")
    if len(set(title_years)) > 1:
        print(f"NOTE {path.name}: page titles name different Octobers {title_years}; using page 1 ({october_year})")
    for r in rows:
        r["october_year"] = october_year
    return rows


def main() -> None:
    files = sorted(RAW.glob("*compare*head_count*.txt"))
    print(f"{len(files)} source files")
    rows = []
    for p in files:
        rows.extend(parse_file(p))
    df = pd.DataFrame(rows)
    df["difference"] = df["difference"].astype("Int64")
    df["check_ok"] = (df.planning_projection + df.difference == df.funded_headcount).fillna(False).astype(bool)
    cols = ["october_year", "source_file", "meeting_date", "page", "projection_date", "headcount_date", "level",
            "school", "asterisk", "planning_projection", "funded_headcount", "difference", "pct_difference",
            "is_total", "check_ok"]
    df = df[cols].sort_values(["october_year", "page"], kind="stable").reset_index(drop=True)
    df.to_csv(OUT, index=False)

    print("\n== Arithmetic check: planning_projection + difference == funded_headcount ==")
    bad = df[~df.check_ok].copy()
    bad["reason"] = [("difference not printed" if pd.isna(d) else f"proj+diff={p + d} != head")
                     for p, d in zip(bad.planning_projection, bad.difference)]
    print(f"{len(df)} rows, {len(bad)} exceptions (kept, check_ok=False):")
    print(bad[["october_year", "level", "school", "planning_projection", "funded_headcount", "difference",
               "pct_difference", "reason"]].to_string(index=False))

    print("\n== Bear Creek and Mesa vs expected ==")
    fails = 0
    for school, exp in EXPECTED.items():
        sub = df[(df.school == school) & (df.level == "elementary")].set_index("october_year")
        out = []
        for yr, (ep, eh) in exp.items():
            got = ((int(sub.loc[yr, "planning_projection"]), int(sub.loc[yr, "funded_headcount"]))
                   if yr in sub.index else None)
            ok = got == (ep, eh)
            fails += not ok
            out.append(dict(october_year=yr, school=school, projection=got[0] if got else None,
                            headcount=got[1] if got else None, expected=f"{ep}/{eh}", match=ok))
        print(pd.DataFrame(out).to_string(index=False))
        if len(sub) != len(exp):
            print(f"  NOTE: {school} has {len(sub)} elementary rows, expected {len(exp)}")
    print("ALL MATCH" if fails == 0 else f"{fails} MISMATCHES")

    print("\n== Elementary rows per year and TOTAL ELEMENTARY ==")
    out = []
    for yr, g in df[df.level == "elementary"].groupby("october_year"):
        schools = g[~g.is_total]
        tot = g[g.school == "TOTAL ELEMENTARY"]
        tp = int(tot.planning_projection.iloc[0]) if len(tot) else None
        th = int(tot.funded_headcount.iloc[0]) if len(tot) else None
        sp, sh = int(schools.planning_projection.sum()), int(schools.funded_headcount.sum())
        out.append(dict(october_year=yr, n_elem_school_rows=len(schools), sum_projection=sp, total_row_projection=tp,
                        sum_headcount=sh, total_row_headcount=th, sums_match=(tp == sp and th == sh)))
    print(pd.DataFrame(out).to_string(index=False))
    print(f"\n{len(df)} rows -> {OUT}")
    if fails:
        sys.exit(1)


if __name__ == "__main__":
    main()
