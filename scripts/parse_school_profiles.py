"""Parse BVSD School Profile books for Mesa and Bear Creek (data/raw/bvsd/school_profiles/*.txt).

Source: bvsd.org planning-and-engineering page, "School Profiles" (retrieved 2026-09-03). Each book
carries, per school, a ten-year grade-by-grade funded headcount and an "Open Enrollment Profile"
(neighborhood residents, BVSD OE-out, OE-in, placements out/in, out-of-district). The 2011, 2012
and 2014 books also print "Program Capacity" and "Number of Possible Classrooms".

Outputs (data/clean/):
  school_profile_oe_mesa_bearcreek.csv     long: book, school, field, school_year, value, row_complete
  school_profile_capacity_mesa_bearcreek.csv  program capacity / classrooms by book year
Rows whose number of values differs from the number of year columns (blank cells dropped by the text
layer) are kept with row_complete=False and values aligned from the LEFT (most recent year); treat
them as unverified. Cross-check: overlapping years across books should agree.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "bvsd" / "school_profiles"
CLEAN = ROOT / "data" / "clean"
FIELDS = {
    "Neighborhood Students": "neighborhood_residents", "Neighborhood Population": "neighborhood_residents",
    "BVSD OE-Out": "oe_out", "BVSD OE-In": "oe_in", "Placements-Out": "placements_out",
    "Placements-In": "placements_in", "Out of District": "out_of_district", "Total": "total_enrollment",
    "K": "grade_k", "1": "grade_1", "2": "grade_2", "3": "grade_3", "4": "grade_4", "5": "grade_5",
    "Pre-K": "pre_k",
}
YEAR_RE = re.compile(r"(\d{4})-(\d{4})")


def school_page(txt: str, school: str) -> str | None:
    for p in txt.split("\f"):
        if re.search(rf"School Name:?\s+{school} Elementary", p, re.I) and "OPEN ENROLLMENT" in p.upper():
            return p
    return None


def parse_page(page: str, book: str, school: str) -> list[dict]:
    out = []
    lines = page.splitlines()
    years_grade, years_oe = None, None
    section = "grade"
    for line in lines:
        if line.startswith("Funded Headcount"):
            years_grade = [f"{a}-{b[-2:]}" for a, b in YEAR_RE.findall(line)]
            continue
        if "OPEN ENROLLMENT PROFILE" in line.upper():
            section = "oe"
            continue
        if section == "oe" and years_oe is None and YEAR_RE.search(line):
            years_oe = [f"{a}-{b[-2:]}" for a, b in YEAR_RE.findall(line)]
            continue
        if "DEMOGRAPHIC" in line.upper():
            break
        m = re.match(r"^([A-Za-z][A-Za-z /\-]*?|\d|K|Pre-K)\*?\s+((?:-?\d+\s*)+)$", line.strip())
        if not m:
            continue
        label = m.group(1).strip()
        if label not in FIELDS:
            continue
        vals = [int(v) for v in m.group(2).split()]
        years = years_oe if section == "oe" else years_grade
        if not years:
            continue
        if label == "Total" and section == "oe":
            field = "total_oe_profile"
        else:
            field = FIELDS[label]
        complete = len(vals) == len(years)
        for y, v in zip(years, vals):
            out.append(dict(book=book, school=school, section=section, field=field, school_year=y, value=v,
                            row_complete=complete))
    return out


def main() -> None:
    rows, caps = [], []
    for p in sorted(RAW.glob("school_profiles_*.txt")):
        book = p.stem.split("_")[-1]
        txt = p.read_text(encoding="utf-8")
        for school in ["Mesa", "Bear Creek"]:
            pg = school_page(txt, school)
            if pg is None:
                print(f"{book}: no {school} page found")
                continue
            rows += parse_page(pg, book, school)
        # capacity lines (2011/2012/2014 books)
        for pg in txt.split("\f"):
            m = re.search(r"(\d{4}) Program Capacity (\d+)", pg)
            s = re.search(r"School Name\s+(Bear Creek|Mesa) Elementary\s+Number of Possible Classrooms (\d+)", pg)
            if m and s:
                caps.append(dict(book=book, school=s.group(1), capacity_year=int(m.group(1)),
                                 program_capacity=int(m.group(2)), possible_classrooms=int(s.group(2))))
    df = pd.DataFrame(rows)
    df.to_csv(CLEAN / "school_profile_oe_mesa_bearcreek.csv", index=False)
    cap = pd.DataFrame(caps)
    cap.to_csv(CLEAN / "school_profile_capacity_mesa_bearcreek.csv", index=False)
    print("capacity:\n", cap.to_string(index=False))
    # show the OE fields from the two anchor books, complete rows only
    for school in ["Bear Creek", "Mesa"]:
        sub = df[(df.school == school) & (df.section == "oe") & df.row_complete]
        piv = sub.pivot_table(index="field", columns="school_year", values="value", aggfunc="first")
        print(f"\n{school} OE profile (complete rows, all books merged; later book wins on conflict):")
        print(piv.to_string())
        inc = df[(df.school == school) & (~df.row_complete)].groupby(["book", "field"]).size()
        print("incomplete rows (unverified alignment):", dict(inc))
    # cross-book agreement on overlapping years
    dup = df[df.row_complete].groupby(["school", "field", "school_year"]).value.nunique()
    print("\nfield-years with conflicting values across books:", int((dup > 1).sum()), "of", len(dup))
    conf = df[df.row_complete].groupby(["school", "field", "school_year"]).value.agg(["nunique", "min", "max"])
    print(conf[conf["nunique"] > 1].head(30).to_string())


if __name__ == "__main__":
    main()
