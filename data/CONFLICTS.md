# Conflicts between sources

Record both sides; do not resolve silently. Updated 2026-09-03 after the primary documents arrived. Items resolved by primaries are kept with their resolution.

## C1. Mesa October counts: BVSD official vs the two enrollmentdata series — RESOLVED IN FAVOR OF BVSD FILES
- Official (P13, `<year>_cde_headcount_summary.pdf` p. 1, "FUNDED HEAD COUNT" current-year column), Mesa 2014→2025: 330, 320, 287, 271, 260, 261, 235, 247, 246, 233, 230, **224**. Bear Creek: 417, 441, 438, 448, 425, 400, 341, 346, 342, 298, 318, **312**.
- enrollmentdata CSV differs from official in 6 of 12 Mesa years and 4 of 12 Bear Creek years, always by 1–2 students (e.g. Mesa 2025: 225 vs 224; Bear Creek 2019: 402 vs 400). The map series differs from official in 10 of 12 Mesa years by up to 32 (2018: 292 vs 260). Full table: `data/clean/verification_headcount_sources.csv`.
- Use `data/clean/bvsd_pupil_count_mesa_bearcreek.csv` from now on. `mesa_bearcreek_headcount.csv` (enrollmentdata) is retained only as the Step-2 artifact.
- Note the prior-year column in each BVSD file equals the previous file's current-year value in all 22 cases, so BVSD did not revise these counts after publication.

## C2. Mesa 2025-26: 224 vs 225 — RESOLVED
- 224 is the official funded head count (P13 2025-26, updated 1/22/2026) and is what P1 p. 51, P2 p. 9 and P5 use. 225 appears only in enrollmentdata and in CLAUDE.md. CLAUDE.md's "Mesa 225" should be corrected to 224.

## C3. Bear Creek capacity: 467 (3.0 rounds) in Feb 2024 vs 492 (3.5 rounds) from Feb 2025 on — OPEN
- P4 p. 11 (2023-24 summary): Bear Creek capacity **467**, 3.0 rounds. P3 p. 9, P5 slide 17, P2 p. 9, P1 p. 51: **492**, 3.5 rounds. Mesa is 418 / 3.0 in all four. No document explains the change (footnote in all three tables: "program capacity based on current use of the building"). Percent-of-capacity figures for Bear Creek are therefore not comparable across the Feb 2024 and later vintages.
- Separately, the ArcGIS attendance-area attributes in `data/raw/enrollmentdata/BVSD_Attendance_Areas.geojson` carry Bear Creek capacity 475 and Mesa 485 (vintage unknown), and the enrollmentdata headcount CSV's `max_enrollment` (448 / 330) is a 10-year peak, not capacity.

## C4. Attendance-area GeoJSON join error for "BC-Mesa" — unchanged
- The "BC-Mesa" polygon carries BC/SIS-HP's forecast attributes via a prefix-match join in the transcription. Ignore those attributes. The polygon itself is real: P1 p. 49 refers to "the Bear Creek, Mesa and dual attendance areas", and P10 documents a separate Bear Creek/Creekside dual area.

## C5. enrollmentdata headcount CSV grade columns — RESOLVED (unreliable; superseded)
- The official files give full K–5 (and PK through 2022-23) grade counts that sum exactly to the head count in all 24 Mesa/Bear Creek school-years. The transcription's 2023 seventh column (13 / 16) does not correspond to anything in the official file (PK was 0 for both schools every year it was reported).

## C6. Oct 2025 deck vs Feb 2026 report projections (open question 1) — DATA NOW IN HAND, NOT EXPLAINED
- P5 slide 17 (Oct 21 2025) and P3 p. 9 (Feb 2025, "updated 1/24/2025") are **identical** for Mesa and Bear Creek: 2029-30 Bear Creek 272 / Mesa 224. So the Oct 2025 deck re-used the January 2025 projection run; the jump is between the Jan 2025 and Jan 2026 runs.
- P2 p. 9 (updated 1/26/2026): 2029-30 Bear Creek 310 / Mesa 202; 2030-31 320 / 201.
- P5 slide 19 carries the note "Chart does not reflect new 2026-27 attendance area boundaries." P10: the Bear Creek/Creekside dual area west of Broadway and north of Table Mesa becomes Bear Creek-only from 2026-27 (adopted Sept 23 2025). Whether the Jan 2026 run incorporates that change is not stated in P2.
- Size of the boundary change (P14 p. 22, P15 p. 19): the dual Bear Creek/Creekside area holds **37 elementary students, of whom 23 already attend Bear Creek and 7 attend Creekside**; BVSD calls the dual area "generally unused". On these numbers the boundary change alone moves single digits of students per year, far less than the +38 (272 → 310) revision to Bear Creek's 2029-30 projection between the Jan 2025 and Jan 2026 runs. The hypothesis in CLAUDE.md open question 1 is therefore not supported by the documents as the main explanation; the reason for the revision is undocumented.
- Also: the Feb 2026 Bear Creek path is non-monotonic (299, 293, 288, then 310, 320), unlike every earlier vintage.

## C7. Page references in CLAUDE.md for the "462" figure
- CLAUDE.md cites "deck pp. 37, 39". In P1 as downloaded, pp. 37–39 are the Monarch/Eldorado pages; the Mesa/Bear Creek consolidation is **pp. 49–51** and the 403–462 range is on **p. 51**. The enrollmentdata About page's "pp. 25, 37, 39, 48, 51 and 54" list covers several schools; for this pair the right page is 51.

## C8. Resident-student counts across documents
- P1 p. 51 (2025-26): Bear Creek resident students 275, Mesa 228. P1 p. 44 bar labels (residents attending their neighborhood school): Bear Creek 217, Mesa 156.
- P5 slide 19 (2024-25, pre-boundary-change chart, no labels): the Bear Creek "attending neighborhood school" bar visibly extends past 300 while 2024-25 enrollment was 318, and the total resident bar reads ≈380; Mesa reads ≈155 / ≈228. A 2024-25 resident-attending count above ~300 is hard to reconcile with 217 a year later unless the dual attendance area was counted differently. Recorded as a puzzle; do not use the slide-19 bar readings as data.
- P1 p. 50 says Mesa "has the second lowest number of resident students in its attendance area" in Boulder; p. 44 shows Flatirons (≈195) lowest and Mesa (228) second-lowest, consistent.

## C10. CDE membership vs BVSD funded head count — definitional, small
- CDE (C1/C2) counts PK where offered: Bear Creek 16 PK in 2023-24 only; Mesa 13 / 20 / 25 PK in 2023-24 / 2024-25 / 2025-26. BVSD's files show PK = 0 for both schools (through 2022-23) and drop the column after. So CDE PK-12 for Mesa 2025-26 is **250**, K-5 is 225, BVSD funded K-5 is 224.
- K–5 differences: 2020-21 CDE is +2 (Bear Creek) / +1 (Mesa); 2023-24 +1 (Bear Creek, kindergarten); 2025-26 +1 (Mesa, grade 1). All others equal. CDE's K–5 membership ≥ BVSD's funded count in every case, consistent with "membership" vs "funded".
- Consequence: the enrollmentdata "Mesa 225" and its 2023 "6TH" column (13/16) are CDE values (K-5 count and PK), not transcription errors. `data/clean/verification_cde_vs_bvsd.csv` has the cell-level comparison.

## C11. One-time cost of the proposal: "$7.5–10M" vs "$12.5–15M" — DIFFERENT LINE ITEMS, BOTH IN THE DECK
- Deck p. 60 ("Reinvesting in the Student Experience") lists two one-time items: **Facility Modifications $7.5M–$10.0M** ("Some offset by savings from Bond projects") and **School Transition Support $5.0M** ("budgeted, FY27"; "Transition staffing, moving costs, transitional support"). Recurring annual savings: **$3.5M–$4.0M**.
- "Up to $10M one-time" (as reported by Boulder Reporting Lab) is the facility-modification line alone. "$12.5–15M one-time" (as circulated by savedouglass.com) is the sum of both lines. Both are arithmetically consistent with p. 60; neither the news story nor the savedouglass page is in the repository, so their exact wording is not verified here.
- No per-school breakdown, no vacant-building maintenance figure, no portable cost and no RISE/AIM relocation cost appears anywhere in the deck, the FAQ or the bvsd.org pages reviewed. The "~$494M budget" denominator circulated with the second figure does **not** appear in any document in the repository and must be sourced (BVSD adopted FY27 budget) before use.

## C12. Bear Creek's existing autism programming
- bvsd.org Resilient Schools page (p. 7 of the saved copy): "All existing AIM and RISE programs would be housed at Bear Creek." Deck p. 49: "Mesa's RISE Program moves to the Bear Creek building." Neither document states how many classrooms these programs occupy at either school or whether the 492-seat capacity nets them out. The effective-capacity scenarios in the appendix are therefore illustrative.

## C13. Resident students for the combined Bear Creek/Mesa area: deck p. 51 vs deck p. 44
- p. 51 (text layer): resident students 275 (Bear Creek) + 228 (Mesa) = 503 in 2025-26; 473 projected for the combined area in 2027-28; 522 in 2030-31.
- p. 44 (chart, read by eye; `data/clean/aug2026_deck_p44.csv`): 2030 projected-resident markers at about 268 (Bear Creek) and 177 (Mesa), about 445 in total.
- The two pages differ by about 77 residents for the same year, and the p. 51 path (503 → 473 → 522) falls then rises 10% in three years. No document defines the figures or reconciles them. Raised as an open question in the appendix and the email; not resolved.

## C14. Coal Creek's region
- The Oct 21 2025 work session (slide 12) places Coal Creek in the Louisville/Superior region, not Boulder. An earlier draft of the appendix listed it among Boulder schools near three rounds after the package; corrected 2026-09-03.

## C15. Program-capacity restatements, district-wide (Feb 2024 → Feb 2025 → Feb 2026 tables)
- Bear Creek 467→492; Coal Creek 516→492; Douglass 442→418 (2025). Kohl 516→541; Aspen Creek 461→442; Community Montessori 392→369; Louisville 615→590 (2026). Totals 14,608 → 14,585 → 14,543. No explanation in any table beyond the footnote "program capacity based on current use of the building." Source: `data/clean/capacity_summary_all_schools_by_vintage.csv`.

## C16. Deck p. 55 post-change Boulder utilization (67.9%) not reproducible
- Current state reproduces (63.1%, 2,585 open seats = Feb 2026 table + Horizons 243). Removing Flatirons 320 + Mesa 418 + Montessori building 369 and using the deck's 2030 enrollment 4,241 gives 71.9%; current enrollment gives 74.9%. Inputs behind 67.9% not stated.

## C17. Implied share following differs by component (deck pp. 25, 37, 48, 51, 54 vs Feb 2026 p. 9)
- 82–100% (Birch→Kohl; Douglass→3 schools), 82–96% (Flatirons→2 schools), 55–71% (Monarch K-5→3 schools), 41–71% (Mesa→Bear Creek), 2030-31. `analysis/output/table10_package_implied_shares.csv`.

## C18. Boulder residents −9% by 2030 (deck p. 43) vs Bear Creek/Mesa area residents +4% (p. 51)
- 3,870 → 3,522 region-wide; 503 → 522 for the combined area. Not reconciled in any document.

## C19. Deck "current" enrollments vs official October 2025 count
- Birch 259 (deck p. 25, Feb 2026 p. 9) vs 261 (pupil-count file); Fireside 405 vs 406; Aspen Creek 472 (table) vs 473. Basis of the January update not stated.

## C20. Three definitions of "resident students" for Bear Creek and Mesa, 2025-26 (added 2026-09-03)
- **Enrollment Pattern Matrix, 12/5/2025** (P18, `oe_matrix_area_totals_south_boulder.csv`): residents living in the Bear Creek area proper 162, Mesa area proper 176, Optional Bear Creek/Creekside 27, Optional Bear Creek/Mesa 137; the four areas together **502**.
- **Deck p. 51**: Bear Creek 275, Mesa 228, total **503**. The total matches the matrix's four areas within one student, so the deck appears to allocate the two optional areas between the schools (275 − 162 − 27 = 86 and 228 − 176 = 52 of the 137 Optional Bear Creek/Mesa residents, i.e. by school attended or by some other rule); no document states the rule.
- **School Profile Report, 12/17/2025** (P19): "Neighborhood Students" Bear Creek 264, Mesa 220, total **484**. Definition not stated in the book; it is neither the matrix's area-proper count nor the deck's.
- **Deck p. 44** (chart, by eye): 2030 projected residents about 268 + 177 ≈ 445 (C13).
- Consequence: any capture rate must name its denominator. The appendix's 74% (373/503) used p. 44 numerators over p. 51 denominators; the matrix gives own-school capture 372/502 = 74% and **combined-area capture 415/502 = 83%** on one consistent definition.

## C21. School Profile books disagree with each other for overlapping years
- Each book prints ten years; the same school-year appears in up to three books. For Bear Creek and Mesa, 51 of 598 field-years differ across books (`scripts/parse_school_profiles.py` output), e.g. Bear Creek "Neighborhood Population" 2012-13: 229 (one book) vs 384 (another); 2015-16: 433 vs 456; Mesa 2009-10: 264 vs 327. Some rows also lost blank cells in the text layer (`row_complete=False`). Until checked by eye, use the most recent book for each year and treat pre-2016 values as approximate. The 2016-17 … 2025-26 series (2025 book) is internally clean.

## C22. Open-enrollment counts: matrix vs profile, 2025-26
- Matrix (12/5/2025): Bear Creek OE-in from district 70, out-of-district 13, placements 13; Mesa 48 / 10 / 10. Profile (12/17/2025): Bear Creek BVSD OE-In 73, Out of District 13, Placements-In 13; Mesa OE-In 53 / 10 / 11. Twelve days apart and small differences (3–5 students); the profile is labelled "K-12" and may include preschool placements. Use the matrix for the decomposition (it is the one with a residence breakdown) and cite the date.

## C23. Combined-area resident history vs the deck's resident projection
- Matrix column totals (P18): residents of the four areas that form the proposed combined attendance area fell 733 (2017-18), 706, 688, 592, 592, 583, 535, 526, **502** (2025-26): −32% in eight years, −6% in the last two. Deck p. 51 projects 503 → 473 (2027-28) → **522** (2030-31), a rise of 10% over three years after the dip. No document gives the basis for the reversal. (This extends C13/C18 with the district's own resident history.)

## C24. January 2026 projection for 2026-27 vs the district's own August 2026 count
- Feb 2026 report p. 9 (Jan 2026 run) projects 2026-27: Bear Creek 299, Mesa 217, sum 516. The Student Enrollment Center's Aug 28, 2026 count (P20): Bear Creek **330**, Mesa **204**, sum **534**; Bear Creek 10% above its projection, Mesa 6% below, the pair 3.5% above. Preliminary (the official count is October 1); the district-wide elementary total on the same date (10,272) was 1.5% below October 2025. Not a conflict between documents; recorded here because the appendix's conditional-approval trigger (combined October 2026 count above 516) is already met on the preliminary count.

## C25. Boulder County births: three publishers, two period definitions (added 2026-09-03)
- SDO (D1) and the Census Bureau (D3) count births July–June; CDPHE (D4, D5) counts calendar years. Single-year differences of up to about 5% are therefore expected (e.g. 2009: SDO 3,187, Census 3,437, CDPHE 3,235). SDO and Census diverge in 2023–24 (2,398 / 2,304 vs 2,422 / 2,424), and SDO's 2025 projection (2,351) is 5% below CDPHE's 2025 actual (2,465). Use one series consistently (recommendation: CDPHE calendar-year births, lagged five years to the fall kindergarten cohort, with SDO as the sensitivity) and state the county-vs-district caveat (Boulder County includes St. Vrain Valley territory).

## C26. Press figures for the merged school: "up to 445" (Daily Camera) vs "up to 462" (Boulder Reporting Lab, deck)
- Daily Camera, 2026-08-25 (N3): Mesa + Bear Creek "up to 445 students … up to 90% of capacity". Boulder Reporting Lab, 2026-08-25 (N2): "up to 462 students in 2030". Deck p. 51 carries both: 392–445 (80–90%) for 2027-28 and 403–462 (82–94%) for 2030-31. Not a conflict in the record; a caution that the two figures circulate for different years.

## C27. "$494M budget" denominator — RESOLVED
- The figure circulated by savedouglass.com is the FY2025-26 adopted budget's "Total Resources: $493.8M" (B2, p. 49), which includes the beginning fund balance. FY2025-26 expenditures were $379.4M; the FY2026-27 Uniform Budget Summary gives General Fund expenditures of $410,202,100 (B1). Any share-of-budget statement should use an expenditure figure and name the year.

## C28. Class-size guideline: assumed 25 (report) vs published figures
- The report's sections analysis assumed a guideline of 25 (23 as sensitivity) because the FAQ names "district class-size guidelines" without a number. The FY2026-27 budget book (B1, p. 121) prints the elementary classroom-teacher staffing formula as 1 : 24.58, and the BVEA agreement (J2, §C-6) prints class-size goals of 26 (K–1), 29 (grades 2–3) and 31 (grades 4–5). The staffing formula governs how many teachers a school is allocated; the agreement's goals are ceilings for individual classes. Re-run the sections analysis on both, and say which the "3 classes per grade" design refers to (a question for staff).

## C29. Quirks in the December enrollment packets (BD1), noted while parsing (2026-09-04)
- The Dec 9, 2025 "Compare Projection to Head Count" table's second page is titled "Roll-up to Oct. 2024 Enrollment" while page 1 and the count date (10/1/2025) say 2025; the parser uses page 1's year.
- The Jan 24, 2017 births table prints the date 10/15/2013 although it contains 2015 births; the meeting date is used for precedence between overlapping editions.
- Births by area: the Lafayette row is lower in editions from Jan 2018 on because the Meadowlark area was split out (e.g. 2001: 235 → 150, Meadowlark 85); the "E County Total" row shows two different series across editions. Neither touches the Bear Creek, Mesa, BC-Mesa or BC-Creekside rows, which agree in every edition.
- The projection in these tables is the district's spring "planning projection" (dated Feb–May of the same year; Jan 23 for 2025), a five-to-eight-month horizon, not the January run's twelve-month horizon; the report labels it accordingly.

## C30. The district's Bear Creek path turns up in 2029-30; area births turned up in 2024
- The January 2026 run's Bear Creek path is 299, 293, 288, 310, 320 (2026-27 … 2030-31), the first run to turn upward (C6). Kindergarten in 2029-30 corresponds to births in 2024; the district's own table shows births in the four South Boulder areas at 33 (2019), 45, 46, 57, 54 and **70 (2024)**, so the 2029-30 kindergarten cohort is the first from a birth year back at the pre-2015 level. This is consistent with the timing of the upturn and with the district's stated births-based method (Feb 2026 p. 7), but no document says so; recorded as a hypothesis the district can confirm, not a finding.

## C31. Two "General Fund expenditure" figures for FY2026-27
- Budget book (B1): General Fund proposed expenditures $386,231,155. CDE Uniform Budget Summary (B1): General Fund expenditures $410,202,100, because the state form folds sub-funds into Fund 10. The report quotes both and computes the package saving's share on each (0.9–1.0%). The book also prints General Fund FTE two ways (2,792.131 and 2,792.877).

## C9. Branch name — as before
- Work is on `claude/bvsd-mesa-bear-creek-data-vdbcu6`, not `data-collection`.
