"""Parse BVSD Enrollment Pattern Matrices (data/raw/bvsd/oe_matrices/*.txt) for Bear Creek and Mesa.

Source: bvsd.org planning-and-engineering page, "Open Enrollment Matrices" (retrieved 2026-09-03).
Each matrix is one landscape page: rows = schools, columns = neighborhood attendance areas where
the school's students live, then summary columns. The text layer scrambles the rotated column
headers, but the data rows are clean. The column order (30 areas) is fixed from 2017-18 on and was
read from the 2017-18 file, whose header text is legible:
  Bear Creek*, Columbine, Creekside*, Crest View, Douglass, Eisenhower, Flatirons, Foothill,
  Heatherwood, Mesa*, Whittier, Optional Bear Creek/Creekside, Optional Bear Creek/Mesa,
  Aspen Creek K-8, Birch, Emerald, Kohl, Lafayette, Ryan, Sanchez, Meadowlark, Coal Creek,
  Fireside, Louisville, Monarch K-8, Eldorado K-8, Superior, Gold Hill, Jamestown, Nederland
Summary columns: Neighborhood Attending School, Open Enrolled from within District, Open Enrolled
from outside District, Placements into School, Unmatched Addresses, Total within BVSD Boundaries,
Student Enrollment, % of Enrollment from Attendance Area.
Identity checks (all years): sum of the 30 area cells = neighborhood + OE-in-district;
neighborhood = own area + both optional areas (for Bear Creek) / own area + Optional BC/Mesa (Mesa).

Outputs (data/clean/):
  oe_matrix_school_by_area_mesa_bearcreek.csv   long: year, matrix, school, area, students
  oe_matrix_school_summary_mesa_bearcreek.csv   summary columns per school-year
  oe_matrix_area_totals_south_boulder.csv        residents living in each of the four areas
  oe_matrix_combined_area_identity.csv           derived: combined-area capture and external seats
2016-17 uses an older layout (blank cells dropped from the text layer); it is skipped and flagged.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "bvsd" / "oe_matrices"
CLEAN = ROOT / "data" / "clean"

AREAS = ["Bear Creek", "Columbine", "Creekside", "Crest View", "Douglass", "Eisenhower", "Flatirons",
         "Foothill", "Heatherwood", "Mesa", "Whittier", "Optional Bear Creek/Creekside",
         "Optional Bear Creek/Mesa", "Aspen Creek K-8", "Birch", "Emerald", "Kohl", "Lafayette", "Ryan",
         "Sanchez", "Meadowlark", "Coal Creek", "Fireside", "Louisville", "Monarch K-8", "Eldorado K-8",
         "Superior", "Gold Hill", "Jamestown", "Nederland"]
SOUTH = ["Bear Creek", "Mesa", "Optional Bear Creek/Creekside", "Optional Bear Creek/Mesa"]
SUMMARY = ["neighborhood_attending", "oe_in_district", "oe_out_of_district", "placements_in",
           "unmatched", "total_within_bvsd", "enrollment"]
ROW_RE = re.compile(r"(Bear Creek|Mesa) \* ((?:\d+ )+)(Bear Creek|Mesa)\* ((?:\d+ )+)(\d+)%")


def parse_file(path: Path) -> tuple[list[dict], list[dict], list[dict], list[str]]:
    txt = path.read_text(encoding="utf-8")
    m = re.match(r"(elem|k)_matrix_(\d{4}-\d{2})", path.stem)
    matrix, year = m.group(1), m.group(2)
    long_rows, summ_rows, area_rows, notes = [], [], [], []
    header = txt.splitlines()[0]
    asof = re.search(r"(\d{1,2}/\d{1,2}/\d{4})", header)
    asof = asof.group(1) if asof else ""
    for mm in ROW_RE.finditer(txt):
        school = mm.group(1)
        cells = [int(x) for x in mm.group(2).split()]
        summ = [int(x) for x in mm.group(4).split()]
        pct = int(mm.group(5))
        if len(cells) != len(AREAS):
            notes.append(f"{path.name} {school}: {len(cells)} area cells (expected {len(AREAS)}); skipped")
            continue
        if len(summ) != len(SUMMARY):
            notes.append(f"{path.name} {school}: {len(summ)} summary cells (expected {len(SUMMARY)}); skipped")
            continue
        d = dict(zip(AREAS, cells))
        s = dict(zip(SUMMARY, summ))
        # identity checks
        own = d["Bear Creek"] + d["Optional Bear Creek/Creekside"] + d["Optional Bear Creek/Mesa"] if school == "Bear Creek" \
            else d["Mesa"] + d["Optional Bear Creek/Mesa"]
        chk1 = sum(cells) == s["neighborhood_attending"] + s["oe_in_district"]
        chk2 = own == s["neighborhood_attending"]
        chk3 = s["total_within_bvsd"] + s["oe_out_of_district"] == s["enrollment"]
        if not (chk1 and chk2 and chk3):
            notes.append(f"{path.name} {school}: identity check failed (sum={chk1}, own={chk2}, total={chk3})")
        for area, v in d.items():
            long_rows.append(dict(year=year, matrix=matrix, as_of=asof, school=school, area=area, students=v))
        summ_rows.append(dict(year=year, matrix=matrix, as_of=asof, school=school, **s,
                              pct_from_attendance_area=pct, checks_pass=chk1 and chk2 and chk3))
    # area totals: the line containing "living in" carries 30 residents counts then the district total
    tot = re.search(r"living in ((?:\d+ )+)(\d+) ", txt)
    pl = re.search(r"Area that are enrolled in ((?:\d+% )+)", txt)
    out = re.search(r"out of ((?:\d+ )+)(\d+)\s*$", txt, flags=re.M)
    placed = re.search(r"A ?rea ((?:\d+ )+)(\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+)%", txt)
    if tot:
        vals = [int(x) for x in tot.group(1).split()]
        pcts = [int(x.rstrip("%")) for x in pl.group(1).split()] if pl else [None] * len(AREAS)
        outs = [int(x) for x in out.group(1).split()] if out else [None] * len(AREAS)
        if len(vals) == len(AREAS):
            for i, area in enumerate(AREAS):
                area_rows.append(dict(year=year, matrix=matrix, as_of=asof, area=area, residents=vals[i],
                                      pct_attending_neighborhood_school=pcts[i] if len(pcts) == len(AREAS) else None,
                                      attending_out_of_area=outs[i] if len(outs) == len(AREAS) else None,
                                      district_total_residents=int(tot.group(2))))
        else:
            notes.append(f"{path.name}: area-total line has {len(vals)} cells; skipped")
    else:
        notes.append(f"{path.name}: area-total line not found")
    return long_rows, summ_rows, area_rows, notes


def main() -> None:
    L, S, A, N = [], [], [], []
    for p in sorted(RAW.glob("*_matrix_*.txt")):
        if p.stem.endswith("2016-17"):
            N.append(f"{p.name}: 2016-17 layout differs (blank cells dropped); not parsed")
            continue
        l, s, a, n = parse_file(p)
        L += l; S += s; A += a; N += n
    long_df = pd.DataFrame(L); summ_df = pd.DataFrame(S); area_df = pd.DataFrame(A)
    CLEAN.mkdir(exist_ok=True)
    long_df.to_csv(CLEAN / "oe_matrix_school_by_area_mesa_bearcreek.csv", index=False)
    summ_df.to_csv(CLEAN / "oe_matrix_school_summary_mesa_bearcreek.csv", index=False)
    area_df[area_df.area.isin(SOUTH)].to_csv(CLEAN / "oe_matrix_area_totals_south_boulder.csv", index=False)

    # Derived identity for the future combined area (Bear Creek + Mesa + both optional areas)
    rows = []
    for (year, matrix), g in long_df.groupby(["year", "matrix"]):
        piv = g.pivot(index="school", columns="area", values="students")
        sm = summ_df[(summ_df.year == year) & (summ_df.matrix == matrix)].set_index("school")
        ar = area_df[(area_df.year == year) & (area_df.matrix == matrix)].set_index("area")
        if not {"Bear Creek", "Mesa"} <= set(piv.index) or not set(SOUTH) <= set(ar.index):
            continue
        in_area = piv.loc[["Bear Creek", "Mesa"], SOUTH].sum().sum()
        residents = ar.loc[SOUTH, "residents"].sum()
        enrolled = sm.loc[["Bear Creek", "Mesa"], "enrollment"].sum()
        oe_in = sm.loc[["Bear Creek", "Mesa"], "oe_in_district"].sum()
        ood = sm.loc[["Bear Creek", "Mesa"], "oe_out_of_district"].sum()
        plc = sm.loc[["Bear Creek", "Mesa"], "placements_in"].sum()
        unm = sm.loc[["Bear Creek", "Mesa"], "unmatched"].sum()
        own = sm.loc[["Bear Creek", "Mesa"], "neighborhood_attending"].sum()
        crossflow = in_area - own  # residents of one area attending the other school
        external_in_district = oe_in - crossflow
        rows.append(dict(year=year, matrix=matrix, residents_combined_area=residents,
                         residents_attending_bc_or_mesa=in_area, combined_area_capture=round(in_area / residents, 3),
                         own_school_attending=own, own_school_capture=round(own / residents, 3),
                         crossflow_between_the_two=crossflow, external_in_district_choice=external_in_district,
                         out_of_district=ood, placements=plc, unmatched=unm, enrollment_both=enrolled,
                         identity_ok=(in_area + external_in_district + ood + plc + unm == enrolled)))
    ident = pd.DataFrame(rows).sort_values(["matrix", "year"])
    ident.to_csv(CLEAN / "oe_matrix_combined_area_identity.csv", index=False)
    pd.set_option("display.width", 250)
    print(ident.to_string(index=False))
    print("\nSummary rows:\n", summ_df.to_string(index=False))
    print("\nSouth Boulder area totals (elem):\n", area_df[(area_df.area.isin(SOUTH)) & (area_df.matrix == "elem")]
          .pivot(index="year", columns="area", values="residents").to_string())
    print("\nNotes:")
    for n in N:
        print(" -", n)


if __name__ == "__main__":
    main()
