# Conflicts between sources

Record both sides; do not resolve silently. Ordered roughly by importance for Mesa / Bear Creek.

## C1. Two October-count series inside the enrollmentdata repo disagree (Mesa affected, Bear Creek not)
- Side A: `data/raw/enrollmentdata/BVSD_October_Headcount_2014-2025.csv` (column `enrollment`).
- Side B: history arrays in `data/raw/enrollmentdata/maps/index.html` (`schools[]`, e.g. line 750 Mesa, line 772 Bear Creek), which is what enrollmentdata.org actually displays.
- Both claim to transcribe BVSD's October pupil count. Comparison (`scripts/compare_map_vs_csv.py`, output `data/clean/enrollmentdata_internal_check.csv`): 238 of 324 elementary school-years differ. Every 2025 value agrees. Only Bear Creek and BCSIS agree in every year.
- Mesa, October year: CSV vs map — 2014 330/330; 2015 320/316; 2016 288/307; 2017 272/294; 2018 260/292; 2019 261/272; 2020 237/223; 2021 247/243; 2022 245/253; 2023 233/240; 2024 231/226; 2025 225/225.
- Bear Creek: identical in all 12 years (417, 441, 438, 448, 425, 402, 342, 346, 340, 299, 318, 312).
- The differences are not a one-year shift and are not a constant PK offset (signs vary). Which side matches BVSD's published files is unknown until F7 (SOURCES.md) is retrieved. Downstream files: `mesa_bearcreek_headcount.csv` uses Side A; `enrollmentdata_map_history_all_schools.csv` is Side B.

## C2. Mesa 2025-26 enrollment: 224 vs 225
- `BVSD_Capacity_Forecast_2025-2031.csv` (attributed to Feb 2026 report p. 9, "Capacity Summary 2025-26 updated 1/26/2026"): Mesa `Enroll_2025-26` = **224**.
- `BVSD_October_Headcount_2014-2025.csv` and map history (attributed to the October pupil count): Mesa 2025 = **225**. CLAUDE.md also says 225.
- Bear Creek is 312 in all three. Possible cause: the report's 1/26/2026 update vs the October count date. Unresolved.

## C3. Capacity figures: Feb 2026 report vs ArcGIS attendance-area attributes vs headcount `max_enrollment`
- Feb 2026 transcription (`BVSD_Capacity_Forecast_2025-2031.csv`): Bear Creek **492** (3.5 rounds), Mesa **418** (3.0 rounds). CLAUDE.md attributes the same numbers to the Oct 2025 deck slide 17.
- ArcGIS layer attributes in `BVSD_Attendance_Areas.geojson` (vintage unknown): Bear Creek `Capacity` **475**, `Enroll` 378; Mesa `Capacity` **485**, `Enroll` 371.
- `BVSD_October_Headcount_2014-2025.csv` column `max_enrollment`: Bear Creek **448**, Mesa **330**. This column is the 10-year peak enrollment (matches the max of the series), **not** building capacity, despite the name.
- Do not mix these. The 492/418 figures are the district's current "program capacity based on current use of each building" (author's About page).

## C4. Attendance-area GeoJSON join error for "BC-Mesa"
- The "BC-Mesa" polygon (SchCode 1, StdtPop 134) carries `Forecast_*` attributes of capacity 590 / enrollment 536 / projections 529…526. Those are BC/SIS-HP's row from the Feb 2026 table, attached by a prefix-match join in the transcription. They are not Mesa or Bear Creek figures. Recorded in `data/clean/attendance_area_attributes_mesa_bearcreek.csv` `_note`.

## C5. Headcount CSV grade columns are partial and, for 2023, misaligned
- 2016–2022 rows carry only four grade columns (labelled KDG–3RD); the sum is well below `enrollment` (e.g. Mesa 2016: 211 of 288), so grades 4–5 are absent, not zero.
- 2023 rows carry seven values (KDG–6TH); the first six sum exactly to `enrollment` (Mesa 233, Bear Creek 299) and the seventh (Mesa 13, Bear Creek 16) is extra, most likely PK or another non-K-5 category mislabelled as 6TH. 2024 and 2025 have six values that sum exactly to `enrollment`.
- Other schools (e.g. Lafayette 2016: grade sum 643 vs enrollment 657) do not reconcile even with the seventh column, so the grade detail should be treated as unreliable until checked against F7.

## C6. Oct 2025 vs Feb 2026 projections (the memo's open question 1) — recorded, not explained
- CLAUDE.md (unverified, attributed to Oct 2025 deck): 2029-30 Bear Creek 272, Mesa 224.
- Feb 2026 transcription: 2029-30 Bear Creek 310, Mesa 202; 2030-31 Bear Creek 320, Mesa 201.
- The Oct 2025 deck itself was not retrieved (F3), so the Oct 2025 side rests entirely on CLAUDE.md.

## C7. Branch name
- Task brief asked for a branch named `data-collection`; the session's designated branch is `claude/bvsd-mesa-bear-creek-data-vdbcu6`, and the work was pushed there (see STATUS.md).
