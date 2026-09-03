# STATUS — updated 2026-09-03 (session 3, revision 2: reviewer fixes applied)

## Reviewer fixes applied (revision 2)
1. **Coal Creek** is in the Louisville/Superior region (Oct. 2025 work session slide 12). Appendix §9 and the email now say Bear Creek becomes "one of very few schools in the Boulder region" at or near three rounds; the two the deck projects there are Foothill (484–492, p. 54) and Bear Creek (403–462 upper end, p. 51).
2. **Capture-rate fork** added to appendix §7 (and cross-referenced in §8): 403–462 requires either capture of 59–70% with open enrollment held at 95, or capture near today's rates with choice cut to near zero; the FAQ (p. 3) says the district contemplates "managing choice enrollment beginning in 2027–28". Corollary stated: managing choice is the only lever against overcrowding and pulling it pushes the merged school back toward 2.5 rounds.
3. **Transportation question replaced** in the email and in appendix §13 by: where do the 29–59% of Mesa students the range assumes do not follow go, and what revenue leaves with them? Transportation remains in §13 as a factual gap statement only.
4. **Pearman verified** against the paper (now in `data/raw/literature/`). Corrections: revenue effect is −$432.70 (rounds to $433); both point estimates are statistically insignificant (SE $388 and $444), which the email and appendix now say; enrollment loss 287 students on average; "~800 districts" is not in the paper and was dropped. Flags removed from appendix §12, §14 and SOURCES L1.
5. **Sharper kindergarten point** in the email and appendix §6.4: the district's Bear Creek 2030-31 projection (320) matches Model A-level (319), not A-trend (268); under that assumption the pair is ~522 and 403–462 needs 60–119 students to leave.
6. **Resident growth 473 → 522** (deck p. 51; current areas hold 503) added to appendix §13 as an open question, with the possible definitional caveat.
7. **±50 result** now labelled Model A-trend, 90% retention (summary, §11, email).
8. **Figure 11** title overlap fixed; regenerated.

## What changed in session 3 (revision 1)
- **Framing replaced.** The deferral date and the enrollment trigger are gone. The argument is now an evidence standard, (i)–(v), with the burden on the district; the ask is verbatim: "Decline to approve the Mesa/Bear Creek component of the Resilient Schools proposal at this time, and direct staff to return with an analysis that meets this standard." No "vote no", "defer", or "postpone" anywhere in the three deliverables.
- **`memo/board-email.md`** (primary; body ≈ 700 words). **`memo/public-comment-sept8.md`** (≈ 280 words). **`report/report.tex`** retitled "Technical appendix", rebuilt to `report/report.pdf` / `.html`.
- **Analysis changes.** Two kindergarten specifications (A-trend, A-level) are co-equal in every results and scenario table (`analysis/03`, `04`); effective-capacity table at 492/470/445 (`analysis/output/table04_effective_capacity.csv`); value-of-waiting figure now leads with the swing in the central estimate (`analysis/06`, `figures/fig11_waiting`). Figures 5, 7 and 11 regenerated.
- **New appendix sections:** the evidence standard; two kindergarten specifications; RISE/AIM and effective capacity; portfolio interdependence; other sources of variance; cost and benefit; other gaps. Tone pass done ("not explained in the documents reviewed").
- **Data logs:** `data/CONFLICTS.md` C11 (one-time cost figures: $7.5–10M facility + $5.0M transition = $12.5–15M; "up to $10M" is the facility line alone), C12 (RISE/AIM room counts absent); `data/SOURCES.md` L1–L4 (Pearman, Boulder Reporting Lab, savedouglass, and the Dec. 12 2025 BVSD news article that carries the "93% of births" statement).

## Things the deck did NOT contain that the deliverables rely on (fix or remove before sending)
1. ~~Pearman~~ — DONE: verified against the paper (see revision-2 item 4).
2. **"~$494M" general-fund denominator** — appears in no document in the repo. Appendix §12 flags it in-line; the email does not use it. Source the FY27 adopted budget or delete the share-of-budget sentence from the appendix.
3. **Boulder Reporting Lab, Aug. 20, 2026 emails story** — not in the repo; the appendix says only that press reporting "has raised the possibility" of a charter or other operator. Save the article to `data/raw/press/` and quote it, or drop the bullet (appendix §10).
4. **Flatirons adjacency.** The session brief described Flatirons as adjacent to Bear Creek/Mesa. The deck assigns the Flatirons area to Foothill and Whittier (p. 52) and none of it to Bear Creek; the appendix says so and adds no upside row. The email does not claim adjacency.
5. **"Bear Creek already houses a center-based autism program."** Supported only by the bvsd.org page's "All existing AIM and RISE programs would be housed at Bear Creek" (p. 7 of the saved copy) and deck p. 49 (Mesa's RISE moves). No room counts anywhere. The effective-capacity table is labelled illustrative.
6. **K-2/3-5 "scored uncertain" and "no FA/FB scoring".** Documents support: deck p. 56 lists it under "other options studied"; Oct. 2025 work session slide 45 says "Impact on fiscal efficiency is uncertain." No FA/FB rubric or scores are in any document, so the email says "dropped without published scoring" (not that scoring exists and was withheld).

## Every number in the email, with where to check it (verify each against the page before sending)
| Claim in email | Value | File | Page |
|---|---|---|---|
| Bear Creek 2029-30 projection, Jan 2025 → Jan 2026 | 272 → 310 | `data/raw/bvsd/trend_report_feb2025.pdf`; `trend_report_feb2026.pdf` (image pages; renders in `data/raw/bvsd/page_renders/`) | p. 9; p. 9 |
| Mesa 2029-30, Jan 2025 → Jan 2026 | 224 → 202 | same | p. 9; p. 9 |
| Bear Creek 2028-29 across three runs | 248, 274, 288 | `trend_report_feb2024.pdf` p. 11; `feb2025` p. 9; `feb2026` p. 9 | |
| "moved 10–16% between annual runs" | +14% (272→310), −10% (224→202), +16% (248→288) | as above | |
| District's Jan 2026 projections sum | 320 + 201 = 521 | `trend_report_feb2026.pdf` | p. 9 |
| Bear Creek capacity | 492 | same; `worksession_2025-10-21.pdf` slide 17 | p. 9 |
| Proposal range 2030-31 | 403–462 | `resilient_schools_proposal_2026-08-25.pdf` | p. 51 |
| Implied retention | 41–71% | arithmetic: (403−320)/201, (462−320)/201 | `analysis/output/table04_implied_retention.csv` |
| Two-year 90th-percentile error | 13.0%, n = 29 | `data/clean/projection_errors_all_schools.csv`; `analysis/output/summary02.csv` | |
| ±50 students from one count | P10–P90 span 99 | `analysis/output/table06_waiting.csv` (`median_spread_p10_p90`) | |
| Backtest schools | 26 | `data/clean/backtest_modelA_all_schools.csv` | |
| Specification gap | 430 vs 501 (71) | `analysis/output/table04_scenarios.csv` (spec, fall 2030, retention 0.9) | |
| P(>492) under the two specs | 16%, 58% | same file, `p_over_492` | |
| Recurring savings; one-time costs | $3.5–4.0M; $7.5–10.0M + $5.0M | `resilient_schools_proposal_2026-08-25.pdf` | p. 60 |
| Payback 3–4 years | 12.5–15.0 / 3.5–4.0 = 3.1–4.3 | arithmetic | |
| Pearman $447 / $433, insignificant; balanced budget unchanged; 287 students; no staff effect | verified | `data/raw/literature/pearman_2026_...pdf` | abstract; p. 12 |
| District's Bear Creek 2030-31 = 320 vs Model A-level 319 / A-trend 268 | | `trend_report_feb2026.pdf` p. 9; `analysis/output/table03_intervals.csv` | |
| 522 − 462 = 60; 522 − 403 = 119 students "go elsewhere" | arithmetic | deck p. 51 | |
| Where the 29–59% go | question | deck p. 51 | |
| "29–59% of Mesa's projected students do not follow" | 1 − 0.71, 1 − 0.41 | arithmetic from p. 51 and Feb 2026 p. 9 | |
| Schools closing / moving in 2027-28 | Douglass, Flatirons, Birch; High Peaks, Montessori | deck pp. 46, 52, 23 | |
| "one of three Boulder schools near three rounds" | Foothill 484–492, Bear Creek 403–462, Coal Creek 395–427 | deck pp. 54, 51, 48 | |
| AIM/RISE at Bear Creek | statement only | `bvsd_page_declining_enrollment.pdf` p. 7 of saved copy; deck p. 49 | |
| School-age care at Bear Creek | statement only | same page; deck p. 64 | |
| Preschool locations by Oct. 1 | | deck p. 64; `resilient_schools_faq.pdf` p. 4 | |
| Transportation radius 1.5 miles | | deck p. 64 | |
| K-2/3-5 option; "uncertain" | | deck p. 56; `worksession_2025-10-21.pdf` slide 45 | |
| Advisory list every year | 2023-24, 2024-25 | `trend_report_feb2024.pdf` p. 13; `trend_report_feb2025.pdf` p. 11 | |
| Vote and discussion dates | Sept 8, Sept 22 | deck p. 3 | |

## Numbers in the public-comment script
272 → 310 (Feb 2025 p. 9 → Feb 2026 p. 9); 521 vs 462 (Feb 2026 p. 9; deck p. 51); "one chance in six" = P(>492) 16% under A-trend at 90% retention (`table04_scenarios.csv`); "ten to sixteen percent" as above.

## Verify personally, with the page open (the numbers most likely to be quoted back)
- Deck p. 51: 492 / 275 / 312; 418 / 228 / 224; 473 and 392–445 (2027-28); 522 and 403–462 (2030-31); the footnote wording.
- Deck p. 60: $3.5M–$4.0M recurring; $7.5M–$10.0M facility modifications, "Some offset by savings from Bond projects"; $5.0M "budgeted, FY27".
- Deck p. 49: "0.71 miles apart"; "Mesa's RISE Program moves to the Bear Creek building".
- Feb 2026 report p. 9 (image; render at `data/raw/bvsd/page_renders/trend_report_feb2026_p09.png`): Bear Creek 320 and Mesa 201 for 2030-31; 310 / 202 for 2029-30.
- Feb 2024 report p. 11 (render `trend_report_feb2024_p11.png`): Bear Creek 248 for 2028-29; Feb 2025 p. 9: 274; Feb 2026 p. 9: 288.
- Sept 9 2025 boundary study p. 22: 37 elementary students; 23 attending Bear Creek (62%).
- Oct 2025 work session slide 12: Coal Creek listed under Louisville/Superior.

## To-do before sending
- [x] Pearman PDF into `data/raw/literature/`; figures verified; flags removed.
- [ ] Decide on the $494M sentence (source it or cut it).
- [ ] Boulder Reporting Lab article into `data/raw/press/` or cut the charter bullet.
- [ ] Read `memo/board-email.md` against the table above; every number has a page.
- [ ] Fill nothing else in: the author line and disclosure are already on the appendix title page.

## Earlier sessions
Session 1 (data collection and verification) and session 2 (analysis) notes are in the git history of this file; the data logs (`data/SOURCES.md`, `CONFLICTS.md`, `VERIFICATION.md`) are current.
