# STATUS — updated 2026-09-03 (session 6b: overnight execution of the revision plan)

## Session 6b execution log (author approved the plan 2026-09-03 evening: run overnight, commit when done)
- [x] Plan decisions recorded (`memo/REPORT_REVISION_PLAN.md` §6); records request drafted, not sent (`memo/records_request_draft.md`).
- [x] `analysis/14_matrix_bridge.py` → table14_* (bridge 512 / 553; capture needed 57–69% / 54–65% vs 81–87% observed; external seats needed at today's capture: 2030-31 floor unreachable, top needs 30 of 121; JECC-R new-entrant table: zero new external admissions from 2027-28 still gives 492 in 2027-28 and 472 in 2030-31), fig16_bridge, fig17_capture_history.
- [x] `analysis/16_resident_history.py` → table16 (733 → 502), fig18_residents. `analysis/17_capacity_history.py` → table17.
- [x] `12_sections_by_grade.py` re-run on the published class-size bases (24.58; 26/29/31) → table12, fig15.
- [x] `15_aug2026_count.py` → table15_aug2026_vs_projection (30 schools matched), table15_conditional, fig20.
- [x] parsers `scripts/parse_district_projection_vs_headcount.py`, `scripts/parse_bvsd_births_by_area.py` → clean files (all Bear Creek/Mesa checks match).
- [x] budget inputs → `data/clean/budget_inputs_fy2027.csv`, `site_budgets_mesa_bearcreek*.csv`, `memo/notes_budget_inputs.md`; `19_budget_arithmetic.py` → table19_*.
- [x] `18_births_kindergarten.py` → table18_*, fig19; `20_district_projection_record.py` → table20_*, fig21.
- [x] `report/report.tex` rewritten to the plan's structure (executive summary page; six sections; appendices A–G); builds with pdflatex (MiKTeX) at **21 pages** (was 28); `analysis/RESULTS.md` replaced with the new canonical numbers.
- [x] four-lens QA (statistics, district rebuttal, exposition + citation audit, graphics) → `memo/qa/review_v2_*.md`. No blocker. Fixed: JECC (not JECC-R) carries the duration clause, with its exception, and the new-entrant table now follows the district's own transition rules (deck p. 63); "23 sections" re-expressed as 19–23 classes by basis with the allocation (19–20 FTE) stated; births range corrected to 60–88 (2005–14) and the births specification reported across windows (505–592) with its caveats; deck p. 70's own compressed timeline cited and the process paragraph made neutral; placements labelled as residence-unknown; bias sentence made consistent (+1%); charter-operator attribution corrected; FAQ re-quoted; "503 residents" vs "503 students" disambiguated; probability captions labelled as shares of simulated paths; figure titles wrapped centrally in `common.save()` so PNGs print at page width; stale hard-coded figure titles replaced by data-driven ones. Not adopted: swapping Sections 3 and 4 (the executive summary now lists the model finding before the rooms finding, and Section 3 points forward to Section 4 for the model).
- [x] verification table below checked against the outputs; commit and push (see git log).

## Numbers in the executive summary, with where to check them (session 6b)
| Claim | Value | Check |
|---|---|---|
| Residents 2030-31; range | 522; 403–462 | deck p. 51 (text layer) |
| Combined-area capture; outside enrollment | 83% (415/502); 121 = 75 + 23 + 23 | `data/clean/oe_matrix_combined_area_identity.csv` (2025-26 elem); render `page_renders/elem_matrix_2025-26_p1.png` |
| Today's pattern on 522 / 473 residents | 553 / 512; residents alone 432 / 391 | `analysis/output/table14_bridge.csv` |
| Capture needed; observed range | 54–65% (2030-31), 57–69% (2027-28); 80.6–87.3% | same; `table14_capture_history.csv` |
| Outside enrollment needed at today's capture | 2030-31: floor unreachable, top needs 30 (cut 91 of 121) | `table14_bridge.csv` |
| New-entrant table on the district's rules | 0/yr, Mesa's non-residents not re-admitted → 461 (2027-28), 473 (2030-31); re-admitted 496 / 487 | `table14_new_entrants.csv`; policy **JECC** (duration clause, line 58 of `data/raw/bvsd/policy/JECC_assignment_of_students_to_schools.txt`), JECC-R (preferences); deck p. 63 |
| Bond schedule | Mesa $1,384,757 / $42,034 / $24,000 / 2028; Bear Creek $2,787,641 | FY27 budget book printed p. 207 (txt page 209) |
| Bear Creek 2029-30 revision | 272 → 310 (+14%) | Feb 2025 p. 9; Feb 2026 p. 9 |
| Aug 28, 2026 count | Bear Creek 330 vs 299; Mesa 204 vs 217; pair 534 vs 516 | `data/raw/bvsd/enrollment_2026-27_weekly/enrollment_2026-08-28.pdf`; Feb 2026 p. 9 |
| Sections at 24.58 | 23 in 2027-28 (both specs); over 21 rooms 73% / 85% | `analysis/output/table12_sections.csv`; budget book p. 121 (txt page index 121) |
| Model 2030-31 | 430 / 503 | `table04_scenarios.csv` (2030, 0.9) |
| Births by area | 33 (2019) → 70 (2024) | `data/clean/bvsd_births_by_attendance_area_wide.csv`, rows Bear Creek + Mesa + BC-Mesa + BC-Creekside |
| Births spec | 546 (2014–25 window), 592 (2020–25) | `table18_births_spec.csv` |
| June 9, 2026 timeline | study Sept, action Oct; study package contents | `data/raw/bvsd/boarddocs/declining_enrollment_community_engagement_board_update_2026-06-09.txt` p. 37 |
| Site budgets | Mesa $3,024,735 / 25.343 FTE / 217; Bear Creek $3,688,335 / 30.511 / 299; Mesa FY25 admin $0.36M, O&M $0.29M | `data/clean/budget_inputs_fy2027.csv`; `site_budgets_mesa_bearcreek_summary.csv`; `memo/notes_budget_inputs.md` |
| General Fund | $386.2M (book) / $410.2M (state summary); saving 0.9–1.0% | `data/CONFLICTS.md` C31; `table19_budget.csv` |

## Session 6: data gathering (done) and a plan for the report (awaiting approval)
- **Nothing in `report/` was changed.** The plan is `memo/REPORT_REVISION_PLAN.md`: executive summary page + six-page summary + appendices (target 20–22 pages from 28), an adversarial claim-by-claim review of the district's plan as a new appendix, a self-review list of what to fix in the current report, new analysis scripts 14–21, and the decisions the author has to make.
- **Web access works from this machine** (bvsd.org, resources.finalsite.net, cde.state.co.us, go.boarddocs.com with a browser user-agent, gis.dola.colorado.gov, census). Downloaders: `scripts/fetch_bvsd_web_docs.py` (bvsd.org files, manifest `data/raw/bvsd/MANIFEST_web_fetch.csv`), `scripts/fetch_public_docs.py` (press/budget/policy; `data/raw/_fetch_records.jsonl`), BoardDocs fetcher notes in `data/raw/bvsd/boarddocs/FETCH_LOG.md`.
- **New raw sources** (all logged in `data/SOURCES.md`, Rounds 4–4d): Enrollment Pattern Matrices 2016-17 … 2025-26 (P18); School Profile books 2011–2025 (P19); weekly 2026-27 enrollment counts Aug 4–28, 2026 (P20); 2020-21 FTE file (P21); LRAC agendas/minutes and policy BDFF (P22); bond reports (P23); 21 dated page copies (P24); demography (D1–D11, 92 files: three births series, SDO single-year-of-age, ACS/decennial tracts); press (N1–N4, 22 items), FY26/FY27 budgets (B1–B2), policies JECC/JECC-R and the BVEA agreement (J1–J2); BoardDocs (BD1–BD7, 141 PDFs incl. the December enrollment packets 2015–2025 with the district's own projection-vs-count tables and births by attendance area, the June 9, 2026 engagement deck, the May 20, 2025 boundary work session).
- **New clean tables**: `data/clean/oe_matrix_*.csv` (parsed by `scripts/parse_oe_matrices.py`; identity checks pass; 2025-26 rows checked by eye, VERIFICATION §F), `enrollment_2026-27_weekly_elementary.csv`, `school_profile_oe_mesa_bearcreek.csv`, `school_profile_capacity_mesa_bearcreek.csv`. Renders: `data/raw/bvsd/page_renders/{elem,k}_matrix_{2024-25,2025-26}_p1.png`.
- **New conflicts** C20–C28 (three resident definitions; profile books disagree across editions; matrix vs profile OE counts; combined-area residents 733 → 502 vs the deck's 503 → 522; Aug 2026 count vs Jan 2026 projection; births period definitions; press 445 vs 462; "$494M" resolved; class-size guideline 25 vs published 24.58 / 26–31).
- **Numbers that will change in the report** (do not quote the old ones): 74% capture → 83% combined-area (own-school 74% on the matrix's own denominator); 163 choice seats → 121 external (75 in-district + 23 out-of-district + 23 placements) with 43 cross-flows inside the future area; "≈550" → 553; residents alone at today's capture 432 in 2030-31 (above the range's floor of 403); capture needed for 403–462: 54–65% vs 81–87% observed since 2017-18; Aug 28, 2026 count Bear Creek 330 / Mesa 204 (sum 534 vs Jan 2026 projection 516); class-size inputs 24.58 (staffing) and 26/29/31 (BVEA).
- **Still not obtainable**: Sept 8 agenda (not posted as of this session; re-check from Sept 4); any Aug 25 attachment beyond the deck (none exists); Tableau dashboard data (manual read); 2016-17 matrix (visual read); CDE 2014–2019 files (low value).
- **Not committed.** `git status` shows the new folders and the three log files modified; commit when the author has looked at the plan.

## Session 5c: third review, report-side items (email left to the author)
- Summary box reordered around the bridge (can-house statement vs FAQ; 522 → 403–462 with no published connection; ≈550 as a reconciliation benchmark, not a forecast); 521 vs 492 now labelled a diagnostic, with the non-additivity caveat.
- Probabilities labelled scenario-conditional in the Summary; §9 no longer says the district "has not modeled" flows.
- Four-term identity stated in §6 (residents × capture + external in-district + out-of-district + placements/other); only out-of-district is separable from the documents on file.
- New Table "The Bear Creek worksheet" in §11 (16 rows, after the reviewer's checklist); Appendix D staff list now points to it and keeps the package-level items, with births named in (5) and the crossflow/placements question as (8).
- Still needed from the author: the December 2025 Enrollment Pattern Matrix (bvsd.org planning-and-engineering page, "Open Enrollment Matrices"); on receipt, Table 11 and Fig. 14 are rebuilt on the matrix's categories (plan in `memo/qa/RESPONSE_to_chatgpt_review_3.md`).

## Session 5b: second ChatGPT review implemented (`memo/qa/RESPONSE_to_chatgpt_review_2.md`)
- The 163 "choice seats" are now split into 23 observed out-of-district and 140 derived; x of the 140 may live inside the combined area. New `table11_crossflow_sensitivity.csv`; Fig. 14 relabelled (combined-area capture; external choice seats) with the locus of today's pattern as x varies. Report §6 states the three x-invariant conclusions (≈550 at today's pattern; capture below today's; cut of more than half of choice enrollment) and demotes 46–57% / 16–75 to the x = 0 row. Email, Summary and script carry only the invariant statements.
- Conditional wording for 29–59% ("read against the standalone projections") in the Summary, §10, §11 and the email; "only if" replaced everywhere by the two-specification statement.
- Appendix D softened: Summary paragraph and appendix introduction now say the items are listed for staff clarification; "two definitions of a round" dropped (divisor noted in the glossary); staff-request list gains the cross-flow question (6). Item list otherwise unchanged.
- New verify item: the cross-flow number is unknown; the email's open question asks for it.

## Session 5: what changed (from `memo/qa/RESPONSE_to_chatgpt_review.md`, items 1–3 of the plan)
- **Accounting grid** (`analysis/11_accounting_grid.py` → `table11_accounting_grid.csv`, `table11_breakeven.csv`, `figures/fig14_accounting_grid.*`). Merged enrollment = residents × capture + choice seats, on the deck's own resident projections (473 / 522, p. 51). Today's rates (74% capture, 163 seats) give 514 in 2027-28 and 550 in 2030-31. Reaching 403–462 needs capture 46–57% at today's seats or 16–75 seats at today's capture. Now the lead figure of §6; Fig. 7 (lines by share following) moved to Appendix C. The earlier capture figures (59–70% / 46–57%) are superseded by the grid's single accounting; the 46–57% survives because it is the same case (all 163 seats kept).
- **Three-outcome table** (`table04_buckets.csv`; report Table in §5 and full version in Appendix C). At 90% following in 2030-31: Trend 63/21/16, Level 18/24/57 (below 450 / 450–492 / above 492). 450 is called a benchmark, not a threshold.
- **Bear Creek as outlier on the district's own numbers** (from `table08_package_ranges.csv`): widest 2030-31 range (59 vs 37 next) and smallest margin at the top (30 seats). New Table in §6, Summary bullet, one email sentence.
- **Email rewritten** (body 750 words): opens with the 521/492/462 line, then the district's "can house" statement (bvsd.org page, saved copy p. 7) against the FAQ's "during the transition year" (p. 3) and the 522 → 550 arithmetic; item 2 of the standard is now the one-page worksheet; outlier sentence; one-in-four line; model described as "patterned on the district's published method"; preschool question dropped for length (still in the appendix). Verbatim ask unchanged, plus one sentence: if staff can produce the worksheet and it shows a fit, the Board has a fair test.
- **Script** (~317 words): same two changes; the closing question for staff is now "what capture rate and how many choice seats does 462 assume?"
- Report, second pass (plan items 4–8, all done): Pearman moved to a footnote in §10; p. 44/p. 51 moved in Appendix D from "disagree" to "not reconciled" and phrased as a question; 89% land-area figure removed; §9 "channels" paragraph softened (both directions; net not modeled); housing-turnover case shortened to two sentences; **classroom feasibility** (`analysis/12_sections_by_grade.py`, table12, fig15 in §6: sections needed = sum over grades of ceil(grade/guideline); guideline 25/23 and rooms 21/18 are assumptions, labelled); **K-2/3-5 comparison table** in §11 with "not published" cells; **off-ramp paragraph** in the conclusion (conditional approval with published triggers; appendix only, not in the email); **shock-dependence sensitivity** (`analysis/13_shock_sensitivity.py`, table13, one paragraph in Appendix B). Fig 8 (class size) moved to Appendix C.
- Sources the author could not retrieve (logged in FETCH_FAILURES.txt): the "Supporting Data" page and the Sept. 8 agenda. Email claim softened to "none of the documents it has published shows"; Appendix D timeline item carries an explicit caveat.
- Deferred: births-based kindergarten spec (no CDPHE series).

## New numbers to verify personally before sending
- 373 residents attending own school (p. 44 bar labels: Mesa 156, Bear Creek 217) and 503 residents (p. 51: 228 + 275) → 74%.
- 163 choice seats: 140 = 536 enrolled − 373 − 23; the 23 out-of-district are from the 2025-26 special-programs summary p. 1 (Mesa 10, Bear Creek 13).
- "can house the projected enrollment of both schools in 2027-28 and beyond": `data/raw/bvsd/bvsd_page_declining_enrollment.txt` lines 134–135 (saved copy p. 7). Confirmed live 2026-09-03 5:07 PM MT (P17, pasted text). Note the adjacent sentence, also live: combining the areas "provides the resident student population for a three-round school"; on the deck's own 522 residents that is true only if every resident attends, since 522 x 74% = 387.
- FAQ "during the transition year ... open enrollment, space and staffing plan": `resilient_schools_faq.txt` lines 86–89 (p. 3).



## Decisions taken on the QA plan's section H (my best guess at your preferences; review in the final version)
1. **Level-specification centering: mean-centered** (the expected kindergarten intake equals the 2023–25 mean), with parameter uncertainty from a bootstrap of the three window years. The median-centered variant (484, P>492 45%) and the 2/5/6-year windows (547/519/505) are reported as sensitivities in Appendix B and in §5.2. With this convention the headline level numbers are essentially unchanged (503 / 57% / 82%), but they are now defensible against the statistics reviewer's blocker.
2. **Both specifications carried everywhere.** Figures 5a/5b, 7, 8, 9 and 11 and every table show Trend and Level side by side; the backtest covers both. The appendix says which assumption each headline uses.
3. **Pearman cut from the email.** It stays in appendix §10 in one bounded paragraph with the verified figures and the wrong-channel caveat stated up front. The email's cost paragraph now rests only on deck p. 60 and the range's own leakage assumption.
4. **Concession added to the email**: "my own model agrees Mesa stays small." The appendix concedes the same in the Summary and §5.3.
5. **The p. 44 vs p. 51 resident discrepancy replaces the school-age-care question in the email's five open questions.** School-age care stays in the appendix list (§11).
6. **Appendix cut and reordered** to the exposition reviewer's outline: 12 main sections, three appendices; method/backtest detail moved to Appendix B; glossary box after the Summary; every figure and section referenced by label. Length is now set by content (check page count in `report/report.pdf`).
7. **The "two classrooms" claim is kept but demoted and qualified**: §8 leads with "first count under the new boundaries; standard (i) cannot be met without it," then gives the roughly 100-student spread under both assumptions, calls it sensitivity of the estimate to one kindergarten cohort, and reports that the band narrows only modestly. The email mentions it in one clause.

## What changed in this session
- **Model.** Level spec re-implemented (mean-centered residuals, bootstrapped window); both specs back-tested, plus tail counts and Bear Creek rows; BCSIS/High Peaks summed for the district comparison; Model B drift drawn once per path with shared shocks; level-window and centering sensitivity table; first-year kindergarten by spec vs the last five observed intakes.
- **Numbers that changed.** Level merged 2030-31 at 90%: 503 (was 501), P>492 57% (58%), P>450 82% (85%); Bear Creek level 317 (was 319); gap 73 (was 71); backtest 80% coverage 74/72 (was 75/73), paired n 49/24 (was 52/26); steady-state kindergarten rows in Fig 9 now use the observed grade-to-grade multiplier (7.08): 463 and 608 (were 392 and 515); "82 a year fills 492" → "about 69 a year at observed gains".
- **Figures.** All eleven redesigned at page width with a source line on the image: new lead figure (district's own arithmetic), two-panel run comparison, grey-background error plots with size bins, Bear Creek two-spec chart with the district's 320, merged two-spec chart with P>492 on it, probability lines instead of the heatmap, class-size dot-range at 21 and 18 rooms, upside ladder with a factual title and shaded range, stacked kindergarten bars, two-panel waiting histogram with the range shaded. Backtest figure moved to Appendix B.
- **Text.** Appendix rewritten to the reviewed outline; "not the finding" once; plain-language terms (Trend/Level assumption, share following, 1-in-10 low/high, 80% range, central estimate); topic sentences; captions carry takeaways; American spelling; "not explained in the documents reviewed"; PK line rewritten as definitional; small-sample and non-independence cautions; capture fork with the district's likely counter stated and answered; Coal Creek corrected to Louisville/Superior; FAQ p. 6 citation fixed; "10–14% between successive runs, 16% over two runs".
- **Email** (body ≤ 750 words): opens with 521/492/462 and the ask; standard as a five-item list; enrollment split into two headed paragraphs; concession; Pearman out; leakage and p. 44/p. 51 questions in. **Script** (~290 words): the 521/462 point first; "one in six … better than even"; ends with one question for staff.
- **Logs.** CONFLICTS C13 (p. 44 vs p. 51 residents), C14 (Coal Creek region); SOURCES L1 marked verified with the exact Pearman figures; PLAN.md clause about "the same office" removed; RESULTS.md replaced with the canonical numbers.

## Numbers in the email, with where to check them
| Claim | Value | Check |
|---|---|---|
| Sum of district's 2030-31 projections | 320 + 201 = 521 | `data/raw/bvsd/trend_report_feb2026.pdf` p. 9 (render in `data/raw/bvsd/page_renders/`) |
| Capacity | 492 | same page; work session slide 17 |
| Range | 403–462 | `resilient_schools_proposal_2026-08-25.pdf` p. 51 |
| Revisions 272→310, 224→202; 248, 274, 288 | | Feb 2025 p. 9; Feb 2026 p. 9; Feb 2024 p. 11 |
| Two-year P90 13%, n = 29 | | `analysis/output/summary02.csv` |
| Bear Creek district 320 vs model 317 (level) / 268 (trend) | | `analysis/output/table03_intervals.csv` (fall 2030) |
| Two schools ≈ 523 (level) | | same file, "A-level Combined" |
| 60 to 120 go elsewhere | 523 − 462 = 61; 523 − 403 = 120 | arithmetic |
| P>492 57% (level) / 16% (trend); central 430; gap 73 | | `analysis/output/table04_scenarios.csv` (fall 2030, retention 0.9) |
| "tested on 26 schools" | | `analysis/output/table03_backtest.csv` |
| Two classrooms either way | spread ≈ 100 | `analysis/output/table06_waiting.csv` |
| Costs $3.5–4.0M; $7.5–10M + $5.0M; payback 3–4 yrs | | deck p. 60; arithmetic |
| 29–59% do not follow | 1 − 0.71; 1 − 0.41 | `analysis/output/table04_implied_retention.csv` |
| Residents 503 / 473 / 522 vs ≈445 | | deck p. 51 (text); deck p. 44 (chart, `data/clean/aug2026_deck_p44.csv`) |
| Three schools close, two focus schools move | Douglass, Flatirons, Birch; High Peaks, Community Montessori | deck pp. 46, 52, 23 |
| "one of very few Boulder-region schools near three rounds" | Foothill 484–492, Bear Creek 403–462 | deck pp. 54, 51; Coal Creek is Louisville/Superior (work session slide 12) |
| AIM/RISE at Bear Creek; preschool by Oct. 1; K-2/3-5 "uncertain" | | bvsd.org page p. 7; deck p. 64 / FAQ p. 4; deck p. 56, work session slide 45 |

## Verify personally before sending (the numbers most likely to be quoted back)
Deck p. 51 (all of Table 1, especially 473 and 522); deck p. 44 (the 2030 resident markers, by eye); deck p. 60 (three dollar figures, "budgeted, FY27", "some offset by savings from Bond projects"); deck p. 49 (0.71 miles); Feb 2026 p. 9 (Bear Creek 320, Mesa 201, capacity 492); Feb 2024 p. 11 (Bear Creek 248 for 2028-29); Sept 9 2025 boundary study p. 22 (37 and 23); work session slide 12 (Coal Creek's region); FAQ p. 6 (over-60 / housing turnover).

## Still unsourced in the repo (flagged in-line where used; not used in the email)
- "$494M" budget denominator: not in any document; the appendix no longer uses it.
- Boulder Reporting Lab Aug. 20 story: no longer cited; the vacant-building bullet cites only FAQ p. 3.

## Earlier sessions
Session 1 (data), session 2 (analysis), session 3 (email/appendix/script) notes are in the git history of this file. QA reviews: `memo/qa/`; plan: `memo/QA_IMPROVEMENT_PLAN.md`.
