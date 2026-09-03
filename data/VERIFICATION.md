# Verification log

**Bottom line: nothing in this repo has been verified against a primary BVSD or CDE document.** All seven primary URLs were denied by the session's egress policy (SOURCES.md F1–F7). What could be checked is (a) internal consistency of the enrollmentdata.org transcription, (b) the transcription against the figures the repo owner supplied in CLAUDE.md, and (c) arithmetic identities. Status codes: `MATCH`, `MISMATCH`, `UNVERIFIED` (no primary available).

## A. CLAUDE.md "Key facts" vs enrollmentdata.org transcription

| # | Figure | CLAUDE.md | Transcription | Where | Status |
|---|---|---|---|---|---|
| 1 | Bear Creek capacity | 492 (3.5 rounds) | 492, 3.5 | `BVSD_Capacity_Forecast_2025-2031.csv` row "Bear Creek" | MATCH (transcription); UNVERIFIED vs Oct 2025 deck slide 17 / Feb 2026 p. 9 |
| 2 | Mesa capacity | 418 (3.0 rounds) | 418, 3.0 | same file, row "Mesa" | MATCH; UNVERIFIED vs primary |
| 3 | Feb 2026 proj 2029-30 Bear Creek | 310 | 310 | same file, `Proj_2029-30` | MATCH; UNVERIFIED vs Feb 2026 p. 9 |
| 4 | Feb 2026 proj 2029-30 Mesa | 202 | 202 | same | MATCH; UNVERIFIED |
| 5 | Feb 2026 proj 2030-31 Bear Creek | 320 | 320 | same, `Proj_2030-31` | MATCH; UNVERIFIED |
| 6 | Feb 2026 proj 2030-31 Mesa | 201 | 201 | same | MATCH; UNVERIFIED |
| 7 | Oct 2025 actual Bear Creek | 312 | 312 | `BVSD_October_Headcount_2014-2025.csv` BEAR CREEK 2025; map line 772; capacity CSV `Enroll_2025-26` | MATCH across all three; UNVERIFIED vs BVSD pupil count |
| 8 | Oct 2025 actual Mesa | 225 | 225 (headcount CSV, map line 750) / **224** (capacity CSV `Enroll_2025-26`) | see CONFLICTS.md C2 | MATCH with headcount, MISMATCH with Feb 2026 table |
| 9 | Aug 2026 "up to 462 students in 2030" at Bear Creek | 462 | 462 = `hi` for y=2030 | `maps/index.html` line 1063 (author cites deck pp. 25/37/39/48/51/54) | MATCH; UNVERIFIED vs deck pp. 37, 39 |
| 10 | Oct 2025 deck proj 2029-30 Bear Creek 272 / Mesa 224 | 272 / 224 | not transcribed by enrollmentdata (it used the Oct 2025 deck for middle schools only) | — | UNVERIFIED (CLAUDE.md only) |
| 11 | Programmatic thresholds ~150/round, 3 rounds ~450 (Oct 2025 slide 8) | — | not in transcription | — | UNVERIFIED |
| 12 | LRAC thresholds (≤2 rounds & ≤60%; ≤1.5 rounds & ≤50%) | — | author's About page states the same thresholds, attributed to bvsd.org Resilient Schools pages | `maps/about/index.html` | MATCH with a secondary source; UNVERIFIED vs bvsd.org |

## B. Internal consistency of the transcription (Mesa and Bear Creek)

| # | Check | Result |
|---|---|---|
| 13 | Headcount CSV vs map history, Bear Creek, 2014–2025 | MATCH all 12 years |
| 14 | Headcount CSV vs map history, Mesa, 2014–2025 | MISMATCH in 10 of 12 years (only 2014 and 2025 agree); see CONFLICTS.md C1 for both series |
| 15 | Headcount CSV vs map history, all elementary schools | 238 of 324 school-years differ; all 27 schools agree for 2025; `data/clean/enrollmentdata_internal_check.csv` |
| 16 | Capacity CSV vs map `elementaryForecast`, Mesa and Bear Creek | MATCH (capacity and all five projections) |
| 17 | Grade columns sum to `enrollment`, 2024 and 2025 | MATCH: Mesa 231, 225; Bear Creek 318, 312 |
| 18 | Grade columns sum to `enrollment`, 2023 | first six columns MATCH (233, 299); seventh column (13, 16) is extra — CONFLICTS.md C5 |
| 19 | Grade columns, 2016–2022 | only four grades present; cannot reconcile |
| 20 | `max_enrollment` column | equals the 2014–2025 peak (Mesa 330 in 2014, Bear Creek 448 in 2017), i.e. it is a peak, not capacity — CONFLICTS.md C3 |
| 21 | `CapPct` columns in capacity CSV | Bear Creek 312/492 = 63.4% → "63%" MATCH; Mesa 224/418 = 53.6% → "54%" MATCH (consistent with 224, not 225) |
| 22 | Aug 2026 post-change utilization vs capacity 492 | 462/492 = 93.9% → "94%" MATCH; 403/492 = 81.9% → "82%" MATCH; 445/492 = 90.4% → "90%" MATCH; 392/492 = 79.7% → "80%" MATCH |

## C. CDE vs BVSD October count
Not possible: no CDE file was retrieved (F5, F6). When they are, note the definitional differences before comparing: CDE pupil membership is the Oct 1 count-date membership and includes PK where the school offers it; BVSD's "October pupil count" is the district's own headcount whose PK treatment must be read off the file header. Compare K-5 to K-5 and record PK separately.

## D. Aug 2026 deck vs Feb 2026 report
The deck (F1) was not retrieved. The only Aug 2026 figures available are the transcribed post-change ranges (Bear Creek 2027-28: 392–445; 2030-31: 403–462; Mesa closes 2027-28). They are in `data/clean/projections_by_vintage.csv` alongside the Feb 2026 and (unverified) Oct 2025 figures, with a `vintage` column and `verified_against_primary=False` on every row.
