"""Parse BVSD's "Births By Elementary Attendance Area" tables.

Sources: data/raw/bvsd/boarddocs/*births*.txt -- text layers of the BoardDocs enrollment-update
attachments for the Feb 2016 through Dec 2025 board meetings (ten tables). Each table is a matrix
of resident births by elementary attendance area for a rolling window of birth years (21 years
through the 2021 table, 18 years from the 2022 table on), plus Unlocated, BVSD, Boulder Total and
E County Total rows. The date printed under the title is the district's extract date; the
2017-01-24 attachment prints "10/15/2013", which is stale (the table contains 2015 births), so
precedence between overlapping tables uses the board meeting date from the file name instead.

Outputs:
  data/clean/bvsd_births_by_attendance_area.csv       long: one row per (table, area, birth_year)
  data/clean/bvsd_births_by_attendance_area_wide.csv  normalized_area x birth_year, value from the
                                                      latest table (by meeting_date) that reports it;
                                                      disagreements lists year: value@meeting_date
                                                      pairs where the overlapping tables differ.
Area names are kept as printed (area) and normalized (normalized_area: "Aspen Crk" -> "Aspen Creek",
"Eldorado (K-5)" -> "Eldorado", "Monarch (K-5)" -> "Monarch"). row_ok is False when a row's number
of values differs from the number of year headers.
Run: python scripts/parse_bvsd_births_by_area.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "bvsd" / "boarddocs"
OUT_LONG = ROOT / "data" / "clean" / "bvsd_births_by_attendance_area.csv"
OUT_WIDE = ROOT / "data" / "clean" / "bvsd_births_by_attendance_area_wide.csv"

NUM = re.compile(r"^[\d,]+$")
DATE = re.compile(r"^\d{1,2}/\d{1,2}/\d{4}$")
KYEAR = re.compile(r"^K in (\d{4})$")
NORMALIZE = {"Aspen Crk": "Aspen Creek", "Eldorado (K-5)": "Eldorado", "Monarch (K-5)": "Monarch"}
TOTALS = {"BVSD", "Boulder Total", "E County Total"}
FOCUS = ["Bear Creek", "Mesa", "BC-Mesa", "BC-Creekside"]


def parse_file(path: Path) -> list[dict]:
    meeting_date = path.stem[-10:]
    lines = [l.strip() for l in path.read_text(encoding="utf-8").replace("\x0c", "\n").splitlines()]
    lines = [l for l in lines if l]
    if not lines[0].startswith("Births By Elementary Attendance Area"):
        raise ValueError(f"{path.name}: unexpected first line {lines[0]!r}")
    table_date = k_year = years = None
    rows: list[dict] = []
    for line in lines[1:]:
        if DATE.match(line):
            table_date = line
            continue
        m = KYEAR.match(line)
        if m:
            k_year = int(m.group(1))
            continue
        if line.startswith("ElemName"):
            years = [int(t) for t in line.split()[1:]]
            continue
        if years is None:
            print(f"  {path.name}: skipped preamble line {line!r}")
            continue
        toks = line.split()
        vals: list[int] = []
        while toks and NUM.match(toks[-1]):
            vals.insert(0, int(toks.pop().replace(",", "")))
        if not toks or not vals:
            print(f"  {path.name}: skipped line {line!r}")
            continue
        area = " ".join(toks)
        row_ok = len(vals) == len(years)
        if not row_ok:
            print(f"  FLAG {path.name}: {area!r} has {len(vals)} values for {len(years)} year headers")
        for y, v in zip(years, vals):
            rows.append(dict(birth_year=y, area=area, normalized_area=NORMALIZE.get(area, area), births=v,
                             is_total=area in TOTALS, row_ok=row_ok, source_file=path.name,
                             meeting_date=meeting_date, table_date=table_date, k_year=k_year))
    if table_date is None or not rows:
        raise ValueError(f"{path.name}: missing table date or rows")
    print(f"  {path.name}: table_date {table_date}, K in {k_year}, years {years[0]}-{years[-1]} "
          f"({len(years)} cols), {len({r['area'] for r in rows})} areas")
    return rows


def main() -> None:
    files = sorted(RAW.glob("*births*.txt"))
    print(f"{len(files)} source files")
    rows = []
    for p in files:
        rows.extend(parse_file(p))
    long = pd.DataFrame(rows)
    long["k_year"] = long["k_year"].astype("Int64")
    long = long.sort_values(["meeting_date", "birth_year", "is_total", "area"], kind="stable").reset_index(drop=True)
    long.to_csv(OUT_LONG, index=False)

    print("\n== Row-length check ==")
    print(f"{(~long.row_ok).sum()} rows flagged (row_ok=False) out of {len(long)}")

    print("\n== Column-sum check: sum of area rows (incl. Unlocated) vs BVSD row, per table and year ==")
    sums = long[~long.is_total].groupby(["meeting_date", "birth_year"]).births.sum()
    bvsd = long[long.area == "BVSD"].set_index(["meeting_date", "birth_year"]).births
    cmp = pd.concat([sums.rename("sum_areas"), bvsd.rename("bvsd_row")], axis=1)
    cmp["diff"] = cmp.sum_areas - cmp.bvsd_row
    mism = cmp[cmp["diff"] != 0]
    print(f"{len(cmp)} table-years checked, {len(mism)} mismatches")
    if len(mism):
        print(mism.to_string())

    print("\n== Overlap check: (area, birth_year) reported by more than one table ==")
    g = long.groupby(["normalized_area", "birth_year"])
    overlap = g.births.agg(n_tables="size", n_values="nunique").reset_index()
    overlap = overlap[overlap.n_tables > 1]
    dis = overlap[overlap.n_values > 1]
    print(f"{len(overlap)} overlapping cells, {len(dis)} disagree")
    detail = {}
    for (area, yr), grp in g:
        if grp.births.nunique() > 1:
            detail[(area, yr)] = " vs ".join(f"{v}@{d}" for d, v in zip(grp.meeting_date, grp.births))
    if detail:
        print(pd.DataFrame([dict(normalized_area=a, birth_year=y, values=s)
                            for (a, y), s in detail.items()]).to_string(index=False))

    # Wide: latest meeting_date wins per (normalized_area, birth_year).
    latest = long.sort_values("meeting_date", kind="stable").drop_duplicates(["normalized_area", "birth_year"],
                                                                             keep="last")
    wide = latest.pivot(index="normalized_area", columns="birth_year", values="births")
    wide.columns = [str(c) for c in wide.columns]
    meta = long.groupby("normalized_area").agg(is_total=("is_total", "first"),
                                               areas_as_printed=("area", lambda s: "|".join(sorted(set(s)))))
    meta["n_disagreeing_years"] = [sum(1 for (aa, _) in detail if aa == a) for a in meta.index]
    meta["disagreements"] = ["; ".join(f"{y}: {detail[(aa, y)]}" for (aa, y) in sorted(detail) if aa == a)
                             for a in meta.index]
    wide = meta.join(wide).reset_index()
    wide = wide.sort_values(["is_total", "normalized_area"], kind="stable").reset_index(drop=True)
    for c in wide.columns:
        if c.isdigit():
            wide[c] = wide[c].astype("Int64")
    wide.to_csv(OUT_WIDE, index=False)

    print("\n== Wide table, Bear Creek / Mesa / BC-Mesa / BC-Creekside, 1994-2024 (latest table per cell) ==")
    yrs = [str(y) for y in range(1994, 2025)]
    focus = wide.set_index("normalized_area").loc[FOCUS, yrs].T
    focus.index.name = "birth_year"
    focus["BC+Mesa+BC-Mesa"] = focus[["Bear Creek", "Mesa", "BC-Mesa"]].sum(axis=1)
    print(focus.to_string())
    print(f"\n{len(long)} long rows -> {OUT_LONG}\n{len(wide)} areas x {len(yrs)} years -> {OUT_WIDE}")


if __name__ == "__main__":
    main()
