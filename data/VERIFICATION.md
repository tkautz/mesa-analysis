# Verification log (updated 2026-09-03, after primary documents arrived)

Status codes: `MATCH`, `MISMATCH`, `UNVERIFIED`. "Primary" = a BVSD document in `data/raw/bvsd/`. Extraction method matters: `text` = pdfplumber text layer; `ocr+eye` = image page, rapidocr output checked against the rendered PNG in `data/raw/bvsd/page_renders/` (both the OCR file and the PNG are in the repo); `eye` = read off a chart.

## A. CLAUDE.md "Key facts" vs primary documents

| # | Claim in CLAUDE.md | Primary | Page | Extraction | Status |
|---|---|---|---|---|---|
| 1 | Bear Creek capacity 492 (3.5 rounds), "Oct 21 2025 deck slide 17" | P5 slide 17: 492, 3.5 | 17 | ocr+eye | MATCH |
| 2 | Mesa capacity 418 (3.0 rounds), slide 17 | P5 slide 17: 418, 3.0 | 17 | ocr+eye | MATCH |
| 3 | Oct 2025 deck 2029-30: Bear Creek 272 | P5 slide 17: 272 (55%, 1.8 rnds) | 17 | ocr+eye | MATCH |
| 4 | Oct 2025 deck 2029-30: Mesa 224 | P5 slide 17: 224 (54%, 1.5) | 17 | ocr+eye | MATCH |
| 5 | Feb 2026 2029-30: Bear Creek 310, Mesa 202 | P2 p. 9: 310 / 202 | 9 | ocr+eye | MATCH |
| 6 | Feb 2026 2030-31: Bear Creek 320, Mesa 201 | P2 p. 9: 320 / 201 | 9 | ocr+eye | MATCH |
| 7 | Aug 2026 "up to 462 students in 2030", "deck pp. 37, 39" | P1 p. 51: "2030-31 Projected … Enrolled Students: 403 to 462, Utilization: 82% to 94%" | **51** (not 37/39) | text | MATCH on the number; MISMATCH on page (CONFLICTS C7) |
| 8 | Oct 2025 actuals: Bear Creek 312 | P13 2025-26 head count p. 1: 312; P1 p. 51: 312; P2 p. 9: 312 | 1 / 51 / 9 | text | MATCH |
| 9 | Oct 2025 actuals: Mesa 225 | P13 2025-26 head count p. 1: **224**; P1 p. 51: 224; P2 p. 9: 224 | 1 / 51 / 9 | text | MISMATCH — official is 224 (CONFLICTS C2) |
| 10 | Thresholds ~150 per round; 3 rounds ~450 (slide 8) | P5 slide 8: "Three Round (~450) … Two Round (~300) … One Round (~150)" | 8 | text | MATCH |
| 11 | LRAC Advisory ≤2 rounds & ≤60%; Engagement ≤1.5 rounds & ≤50% | P2 p. 10 (text): "Enrollment Advisory Status <=2 rounds and <=60% of capacity / Community Engagement Status <=1.5 rounds and <=50% of capacity"; P7 pp. 1–2; P4 pp. 6–7 | 10; 1–2; 6–7 | text | MATCH (P2 table legend says "and/or" for the initial colour flags; the boxed "all criteria met" uses "and") |

## B. enrollmentdata.org transcription vs primaries

| # | Check | Result |
|---|---|---|
| 12 | Feb 2026 capacity table (`BVSD_Capacity_Forecast_2025-2031.csv`) vs P2 p. 9, Mesa and Bear Creek, all 13 numbers each | MATCH (capacity, rounds, 2025-26 enrol, five projections; percentages match) |
| 13 | Feb 2026 table, all 32 other schools | not checked cell-by-cell; OCR table in `capacity_summary_feb2026_ocr.csv` for anyone who wants to |
| 14 | Aug 2026 post-change ranges in map (`proposalProjections`) vs P1 p. 51 | MATCH: 392–445 / 80–90% (2027-28); 403–462 / 82–94% (2030-31) |
| 15 | October head count, Bear Creek, 12 years, CSV and map vs P13 | MISMATCH in 4 years by 1–2 (2019, 2020, 2022, 2023); 8 MATCH |
| 16 | October head count, Mesa, 12 years, CSV vs P13 | MISMATCH in 6 years by 1–2; 6 MATCH |
| 17 | October head count, Mesa, map series vs P13 | MISMATCH in 10 years, up to 32 |
| 18 | Grade columns in enrollmentdata CSV vs P13 grade columns (2023–2025) | K–5 values MATCH except Mesa 2024 grade 2 (37 vs 36), Mesa 2025 grade 1 (36 vs 35) and Bear Creek 2023 K (33 vs 32), i.e. the CSV's +1 totals come from single-grade transcription slips; 2023 "6TH" column (13/16) has no counterpart |

## C. Internal consistency of the primaries

| # | Check | Result |
|---|---|---|
| 19 | Each P13 head-count file's prior-year column vs previous year's file (22 comparisons) | MATCH all — no post-publication revisions |
| 20 | P13 grade columns (PK+K–5) sum to funded head count, 24 school-years | MATCH all |
| 21 | P13 head count vs FTE-file head count (same year) | MATCH for every year checked (2025-26 both 312 / 224; 2020-21 FTE-type file 341 / 235) |
| 22 | P13 special-programs head count vs head-count file | MATCH all 12 years for both schools |
| 23 | P5 slide 17 vs P3 p. 9 (Mesa, Bear Creek rows, 20 numbers each) | MATCH — identical tables |
| 24 | P1 p. 50 "Bear Creek 63%, Mesa 54%; 2.1 / 1.5 classes per grade" vs P2 p. 9 | MATCH |
| 25 | P1 p. 51 utilization vs capacity 492: 392/492 = 79.7%, 445/492 = 90.4%, 403/492 = 81.9%, 462/492 = 93.9% | MATCH the printed 80/90/82/94% |
| 26 | P1 p. 51 resident totals vs p. 44 bar ends (275, 228) | MATCH |
| 27 | P1 p. 45 out-of-district segment vs P13 2025-26 special programs "Out of District" (Bear Creek 13, Mesa 10) | consistent by eye (segments ≈10–15 wide) |
| 28 | P2 p. 9 2025-26 enrol column vs P13 2025-26 head count, Mesa and Bear Creek | MATCH (224, 312) |
| 29 | P3 p. 9 2024-25 enrol vs P13 2024-25 head count | MATCH (230, 318) |
| 30 | P4 p. 11 2023-24 enrol vs P13 2023-24 head count | MATCH (233, 298) |
| 31 | OCR (rapidocr) vs visual read of the Mesa/Bear Creek rows on P2 p. 9, P3 p. 9, P4 p. 11, P5 slide 17 | one OCR slip: Mesa 2029 rounds "13" for "1.3" (P2 p. 9); all other tokens MATCH |

## D. CDE vs BVSD October count (2019-20 … 2025-26; `data/clean/verification_cde_vs_bvsd.csv`)

| # | Check | Result |
|---|---|---|
| 32 | School codes: 0652 / 5838 carry the names "Bear Creek Elementary School" / "Mesa Elementary School" under district 0480 "Boulder Valley Re 2" in all 7 CDE files | MATCH |
| 33 | CDE K–5 vs BVSD funded head count, 14 school-years | MATCH in 10; CDE higher by 1–2 in 4 (Bear Creek 2020-21 +2, 2023-24 +1; Mesa 2020-21 +1, 2025-26 +1) |
| 34 | Grade-by-grade, K–5, 14 school-years × 6 grades | all equal except the four single-grade cells behind row 33 |
| 35 | CDE PK: Bear Creek 16 (2023-24 only); Mesa 13, 20, 25 (2023-24 … 2025-26). BVSD files: PK 0 / not reported | definitional; see CONFLICTS C10 |
| 36 | CDE 2025-26 "PK12_MembershipTrends" 2024-25 column vs CDE 2024-25 file | MATCH (318; 250) |

Earlier note, kept for the definitions: BVSD's files are titled "Summary of Colorado Department of Education - Funded Head Count" as of the October count date (Oct 1–5). Definitions to note when it is: BVSD's files are titled "Summary of Colorado Department of Education - Funded Head Count" as of the October count date (Oct 1–5), and list PK separately (0 at Mesa and Bear Creek through 2022-23, column dropped after). CDE's pupil-membership file counts membership on the October count day and includes PK where offered; charter and "Boulder Universal" rows will differ. Compare K–5 to K–5.

## E. Projection-accuracy inputs (open question 3) — data only
`data/clean/capacity_summary_mesa_bearcreek_by_vintage.csv` now holds four vintages (Jan 2024, Jan 2025, Oct 2025 = Jan 2025, Jan 2026) of one-to-five-year projections plus the official actuals in `bvsd_pupil_count_mesa_bearcreek.csv`. Examples, projection → actual: Bear Creek 2024-25 (Jan 2024 vintage) 287 → 318; 2025-26 (Jan 2024) 273 → 312; 2025-26 (Jan 2025) 308 → 312. Mesa 2024-25 (Jan 2024) 220 → 230; 2025-26 (Jan 2024) 211 → 224; 2025-26 (Jan 2025) 230 → 224.
