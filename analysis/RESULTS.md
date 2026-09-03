# Results summary (revised after adversarial QA, 2026-09-03)

Full write-up: `report/report.tex` / `report/report.pdf`. Numbers below are the canonical ones used in the appendix, email and script; sources are `analysis/output/*.csv`.

## Summary paragraph
The district proposes an irreversible step on the basis of projections with no stated margin of error. Its own January 2026 projections for Bear Creek and Mesa add to 521 students in 2030-31; the Bear Creek building holds 492; the proposal's merged-school range tops out at 462. The gap is an assumption about how many Mesa families leave, or about how much open enrollment the district will cut, and the proposal does not say which. The district's projections for these two schools have moved 10–14% between successive runs, and closing Mesa cannot be undone while keeping it open can.

## Canonical numbers
- Revisions: Bear Creek 2029-30 272 → 310 (+14%); Mesa 224 → 202 (−10%); Bear Creek 2028-29 248 → 274 → 288 (+16% over two runs).
- District sums: 521 (2030-31), 496 (2027-28); range 403–462 / 392–445; implied share following 41–71% / 49–75%; implied capture 59–70% (OE-in 95 held) or 46–57% (Mesa's 68 also held).
- Errors (all schools): 1-yr median 3.2%, P90 9.4% (n = 59); 2-yr median 5.7%, P90 13.0% (n = 29); revisions 4–5 yrs out P80 ≈ 12%, max 46%.
- Model, 2030-31, 90% following: Trend 430 (360–510), P>450 37%, P>492 16%, P<300 1%; Level 503 (429–582), 82%, 57%, 0%. Gap 73. 2027-28: 473 / 494; P>492 30% / 52%.
- Bear Creek alone 2030-31: Trend 268, Level 317, district 320. Both schools: Trend 448, Level 523, district 521.
- Level sensitivity (merged, 90%): 547 (2-yr window), 503 (3), 519 (5), 505 (6); 484 median-centred (P>492 45%).
- Backtest (26 schools): 80% coverage Trend 74%/72%, Level 76%/72%; 95% 88/88 and 92/88; 50% 40/32 and 48/32; median APE Trend 3.3/8.4, Level 4.0/6.5 vs BVSD 3.3/5.7 (paired n 49/24).
- Waiting: central estimate spread after one count 100 (Trend; CI 87–109), 107 (Level); Trend 27% of counts above 462, 20% below 403; band 150 → 128 (Trend), 151 → 141 (Level).
- Kindergarten: combined 105, 105, 95, 102, 86, 79, 62, 82, 77, 58, 84, 76; 2014–19 mean 95; 2023–25 mean 73; steady-state multiplier 7.08; 69/yr fills 492.
- Class size (21 rooms, 90%): Trend 20.5 (17–24), Level 23.9 (20–28); at 18 rooms 23.9 / 27.9.
- Costs (deck p. 60): $3.5–4.0M recurring; $7.5–10.0M facility + $5.0M transition; payback 3.1–4.3 yrs.
- Pearman (verified): −$447 / −$433 per pupil, both insignificant; balanced-budget unchanged; −287 students; no staff effect.
- Resident counts: 503 → 473 → 522 (p. 51) vs ≈445 (p. 44).
- Three outcomes (90% following): 2030-31 Trend 63% below 450 / 21% in 450–492 / 16% above 492; Level 18 / 24 / 57. 2027-28 Trend 25 / 45 / 30; Level 13 / 35 / 52 (table04_buckets.csv).
- Accounting identity (table11): today capture 74.2% (373/503), choice seats 163 (140 in-district OE + 23 out-of-district). On deck p. 51 residents: 2027-28 473 → 514 at today's rates; 2030-31 522 → 550. 403–462 needs capture 46–57% at 163 seats, or 16–75 seats at 74% capture; 492 needs 63% or 105 seats. 2027-28: 392–445 needs 48–60% or 41–94 seats; 492 needs 70% or 141 seats.
- Package ranges (table08): Bear Creek 2030-31 width 59 (next Kohl 37, Coal Creek 32); seats left at top 30 (Superior 31, Coal Creek 65, Kohl 67).
- Sections by grade (table12; guideline 25, 90% following): 2027-28 central 22 (trend) / 23 (level) sections, P(>21 rooms) 65% / 78%; 2030-31 20 / 23, P(>21) 31% / 76%; at guideline 23: 92/97/53/91%.
- Shock dependence (table13, 2030-31, 90%): joint vs independent draws: trend 431 vs 432, 80% width 149 vs 135, P>492 15% vs 13%; level 503 vs 503, 153 vs 138, 57% vs 58%.
