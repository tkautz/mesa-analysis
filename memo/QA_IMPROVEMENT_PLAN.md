# Adversarial QA: findings and improvement plan (for approval before implementation)

Five independent reviews were run on the appendix, email and script: statistics, exposition, plain-language reader, district-staff rebuttal, and graphics. Their full notes are in `memo/qa/`. This plan merges them, ranks by risk, and asks for decisions where the reviews conflict or where the change is substantive. Nothing has been changed yet.

## A. Errors that must be fixed (would be found by a hostile reader)

| # | Finding | Source | Fix |
|---|---|---|---|
| A1 | **Model A-level is implemented with the trend-fit residuals, which are skewed.** The level spec's Bear Creek kindergarten median comes out 7% above the stated 2023–25 mean, and it carries no parameter uncertainty. Re-run with median-centred residuals: merged 2030–31 median 484 (not 501), P(>492) 44% (not 58%), P(>450) 76% (not 85%); with mean-centred residuals 496 / 53% / 82%. The "71-student gap exceeds the 59-student range" sentence is false under one reasonable centring (gap 54) and true under another (66). The "district 320 ≈ A-level 319" match weakens to 320 vs ~302–312. | statistics #1 | Re-implement: centre the residuals (mean-centred is the natural convention, state it), bootstrap the level window for parameter uncertainty, report a window-sensitivity line (3/5/6-year windows). Rewrite every dependent sentence: gap "roughly 55–70 students, comparable to the 59-student width of the district's range"; reframe 6.4 as "the district's 320 sits at or above the corrected level specification, so it assumes at least no further decline". Update Tables 4, 5, 6, C, Figures 5, 7, 9, and the email's 58% and 319. |
| A2 | Only the trend spec was back-tested; the level spec and Model B were not. Level backtest actually looks fine (80% band 73%/73%) and errs in the opposite direction (over-projects) from trend (under-projects). | statistics #2 | Report both specs' backtests; say the two err in opposite directions, which is the reason to show both. |
| A3 | "Calibrated" hides three things: the 50% band covers only 40%/35%; at two years 6 of 26 actuals exceed the model's P90 (upper tail too thin); the model missed Bear Creek low both backtest years (282 vs 318; 265 vs 312), worse than the district and in the direction of the district's later upward revision that the appendix calls unexplained. | statistics #3; district #7 | Show all three bands and the tail counts; say "roughly calibrated, with a thin upper tail at two years, which if anything understates P(>492)"; add the Bear Creek rows and use them: an independent cohort model also missed Bear Creek low, so the district's upward revision is defensible, and the point is the size of the misses, not their direction. |
| A4 | Steady-state kindergarten arithmetic contradicts the model's own grade-progression gains (cumulative K→5 gain 1.31–1.35). Figure 9's "K × 6" rows (392, 515) and the "82 a year fills 492" annotation are wrong by that factor; the model row for the same assumption gives ~500. | statistics #7 | Multiply the K × 6 rows by observed cumulative progression, or drop them; change "82 a year" to "about 65 a year at observed gains (the 2023–25 mean is 73)". |
| A5 | "Errors are larger for small schools" is not statistically supported (medians equal at one year; p ≈ 0.11–0.38 at two). | statistics #8 | Replace with "the largest two-year misses occurred at schools under 300 students" or drop the right panel of Fig 3. |
| A6 | The ±50 "one count moves the estimate" result is a property of the trend refit (correlation 0.91 with the simulated kindergarten draw); under the level spec the band does not narrow at all (133→135). Stated with false precision (bootstrap range 86–110). | statistics #5; plain-language 4d | Report under both specs; say "roughly 90–110 students"; describe it as sensitivity of the estimate to a single kindergarten cohort; drop the narrowing claim (or state it as trend-only) and lead instead with "first count under the new boundaries and the new portfolio". |
| A7 | Citation slips: "moved 10–16% between annual runs" — the 16% (248→288) is across two runs; the over-60/housing-turnover statement is FAQ p. 6, not p. 8; "60 to 119" uses the level median (522) where the premise is the district's 521 (59–118); "mountain schools excluded" vs "except Gold Hill and Jamestown" (Nederland is in); "every elementary school" (University Hill is absent from the Feb 2024 table); 13.0% is an interpolated quantile (nearest-rank 12.5). | district audit; statistics #12 | Fix each. Say "10–14% between successive runs, and 16% over two runs". |
| A8 | Model-vs-district comparison mis-pairs BCSIS (model) with BCSIS-HP (district); paired n is 49/24 not 52/26. Model B re-draws drift each year and ignores cross-school correlation. | statistics #10, #11 | Sum the two simulated schools before pairing; fix Model B or label it a rough check. |
| A9 | "25 PK students at Mesa that BVSD's tables omit" reads as an accusation; the PK exclusion is printed on the documents (deck p. 12 footnote; Feb 2026 p. 6; the count files are K-12 funded counts). | district #15 | Rewrite as a definitional note: "BVSD's tables are K-5 by design; CDE separately records 13–25 PK students at Mesa." Cut "omit". |
| A10 | Public GitHub repo, `analysis/PLAN.md` line 4: projections "are produced by the same office that proposes the closure". Not in the letter, but findable. | district #16 | Delete the clause from PLAN.md (history stays; it is not in the deliverables). |
| A11 | Fig 11 shows 431, text says 430 (different seed). | graphics | Reconcile. |

## B. Argument vulnerabilities (the district's best counters) and proposed responses

The district-perspective review rated five counters "fatal" or "strong" against the case as written. Each has a response; the question is how much to concede in the email.

| # | Counter | Proposed response |
|---|---|---|
| B1 | **"521 vs 462" ignores that the range is defined on residents, and standalone projections are not additive** (each school's number contains open-enrollment inflow from the other's area; read on 522 residents, 403–462 is 77–89% capture, at or above today's rates, with choice managed). | This is the strongest counter and it is right that the letter presents only one reading. Present the decoding as the fork it already is in appendix §7, in the email too: "Read one way, the range assumes 30–60% of Mesa's projected students go elsewhere; read the other way, it assumes the district will cap open enrollment at a school it says should attract students. The deck does not say which." Add the statistics reviewer's point that including Mesa's own 68 open-enrolled-in students makes the implied capture 46–57%, so 59–70% is already the reading most favourable to the district. Keep the arithmetic; drop "an assumption the deck does not state" (the footnote states the dependence; say "does not state the share"). |
| B2 | **Choice management is the district's stated answer to the upside case** (FAQ p. 3), not a contradiction of it, because the rationale is resident-based. | Keep the corollary (pulling the choice lever moves the school back toward 2.5 rounds) but phrase it as a question the Board should have answered: "Does the range already assume choice management at Bear Creek, and at what level?" That is an evidence-standard point, not a gotcha. |
| B3 | **The parent's own model says Mesa and Bear Creek both decline; Mesa meets the engagement criteria under either spec; so the model supports acting.** Rated "fatal" to "decline to approve" as a substitute for action. | Concede it explicitly and early (it strengthens the concession paragraph): "My own model agrees Mesa stays small. The question is not whether Mesa is small but whether the merged school fits, and on that the district's documents are silent." The ask is about the evidence for the merger's fit, not about Mesa's status. |
| B4 | **"Keeping Mesa open is cheap" is asserted; the record calls small schools structurally costly.** | Change to what can be shown: "The district has published no Mesa-specific cost of one more year, and every remedy for over-enrollment it might need later (boundaries, choice limits, portables) is reversible; closing Mesa is not." Move "cheap" out of the summary box. |
| B5 | **Pearman is the wrong channel** (California district-exit revenue vs within-BVSD choice with first priority), null results, different formula. Rated fatal as used. | Two options. (a) Cut Pearman from the email entirely and keep one carefully bounded sentence in the appendix (evidence that closure savings can be offset by enrollment loss; mechanism differs here). (b) Keep in the email but only as "closure savings are routinely offset by students who leave; BVSD's own range assumes some leave, and the deck does not say where their funding goes." Recommendation: (a). |
| B6 | **Over-capacity has reversible remedies; two BVSD schools already run over 107% with portables; under-enrollment has none.** | Accept the first half; it supports the asymmetry argument in reverse. Response: reversible remedies cost money the deck does not count (portables, boundary redraws) and the merged school's stated purpose is a three-round program, not a 107% building; state that the deck's one-time cost line assumes none of them. Add Meadowlark's portables as evidence the district knows the cost. |
| B7 | **Fairness across regions**: the same range method underlies Kohl, Superior (96–98% of capacity), Foothill. | Do not engage in the email. In the appendix, one sentence: the standard applies to every component; this appendix covers the one the author can speak to. Superior at 96–98% is worth a footnote as evidence the range method is not conservative everywhere. |
| B8 | **Nov 1 open-enrollment calendar; a 2027 decision means 2028-29 at the earliest.** | State it plainly in the appendix ("the cost of meeting the standard is one enrollment cycle") rather than leaving the district to say it. |
| B9 | **Timing objections and the "announcement effect" are true of any vote date.** | Keep the announcement effect only as a reason the 2026-27 Mesa base is uncertain; drop the "compressed window" bullet. |

## C. New material the reviews surfaced (worth adding)

| # | Item | Source |
|---|---|---|
| C1 | **Deck p. 44's 2030 resident markers read ≈268 (Bear Creek) + ≈177 (Mesa) ≈ 445, while deck p. 51 says 522 residents for the combined area.** The district's own two pages disagree by ~77 students, on top of the 503 → 473 → 522 path. This is unrebutted and belongs in the "what the district's own numbers imply" figure and the gaps list, phrased as a definitional question. | district Part 2 #1 |
| C2 | The trend spec's first-year kindergarten (median 39 for Bear Creek) sits below four of the last five observed intakes (48, 50, 32, 51, 48). This is the plain-language reason the level spec deserves at least equal weight; say it with the numbers. | statistics #6 |
| C3 | The two specs err in opposite directions in backtest (trend under-projects, level over-projects). That is the honest framing for "co-equal". | statistics #2 |

## D. Structure and readability (exposition and plain-language reviews agree)

1. **Lead with the district's own arithmetic, in the summary box, the email's first screen, and the script's first point**: 521 / 492 / 403–462 / the unstated share. Zero modelling. Both reviewers independently called this the single highest-value change. (With B1 folded in: state the fork in one sentence.)
2. **Say "that is not the finding" once**, not four times.
3. **Reorder section 6**: method (150 words, plain) → the kindergarten assumption decides the answer (with the 320-vs-corrected-level comparison and C2) → results. Backtest, small-sample caution and Fig 6 to Appendix B.
4. **Move §3 (data/verification) to Appendix B**; keep the 467→492 restatement in §2, split into three sentences.
5. **Halve §9** to the four facts that bear on Bear Creek; drop the duplicated FAQ quote; drop the duplicated capture fork from §8.
6. **Promote** the resident-count inconsistency (503 → 473 → 522, plus C1) from the gaps list into §4.
7. **Topic sentences** on every evidence section; **takeaway captions** on every figure (drafts exist in `memo/qa/review_exposition.md`).
8. **Glossary box** after the summary and one term each: run; October count; merged school; round ("21 classrooms" not "sections"); Trend assumption / Level assumption (drop "Model A-trend/A-level" outside Appendix B); share of Mesa students who follow; capture rate; central estimate; 80% range with "1-in-10 low / high"; margin of error.
9. **Split the ten sentences over 35 words** listed in the exposition review; replace P10/P90, exceedance probability, probability mass, mean signed error, parametric, realization risk, closure regime, pairs bootstrap, log-linear, random walk.
10. **Tone pass**: "undisclosed" → "not stated in the documents"; "dropped without published scoring" → "no comparison has been published"; remove "announcement effect" as a heading.
11. **Target length** 11 pages main + 3 appendix (from 16), American spelling, `\label`/`\ref` for all figure and section references before reordering.

## E. Figures

Consensus of graphics, plain-language and exposition reviews.

| Fig | Action |
|---|---|
| New (replaces 2) | **"What the district's own numbers imply"**: two rows (2030–31, 2027–28), stacked bar 320+201 = 521 / 293+203 = 496 over the red range bar 403–462 / 392–445, dotted 450 and 492, bracket "59 students (29% of Mesa's projected enrollment) outside the range; implies 41–71% follow", source line on the image. Place under the summary box. Add a third row for residents: 503 today, 473, 522 (p. 51) vs ≈445 (p. 44). |
| 1 | Two panels (Bear Creek, Mesa) from 2020, direct-labelled runs, bracket annotations +38 / −22, red band removed from the Bear-Creek-alone axis. Factual title. |
| 3 | Grey background dots; right panel replaced by three size bins or dropped (A5). |
| 4 | Drop the empty 1-yr tick; P10–P90 as a shaded band annotated "±12%"; n under columns; consider merging with Fig 3. |
| 5 | Split: **5a** Bear Creek only, two medians with one 80% band each (fill vs outline), the district's path ending at a labelled "320" dot, annotation "corrected level median ≈ X / trend 268"; **5b** merged school at 90% following, both 80% bands, 450/492 lines, proposal bracket at 2030, P(>492) under both specs written on the chart. Drop 50/95% fills. |
| 6 | To Appendix B; greys for bars, black ticks = nominal, label the 45° line; add the level spec. |
| 7 | Replace the 108-cell grid with one panel: x = share following, y = probability, four lines (P>450, P>492 × trend/level), 2030–31; highlight 90%. |
| 8 | Redesign as dot-range (80/90/100% × trend/level, at 21 and 18 classrooms) or cut and state two numbers in text. |
| 9 | Factual title ("…under nine cases: N exceed 492"); shade the proposal range as a column; labels ≤ 35 characters with a lettered key; fix the K × 6 rows (A4); group rows by kind. |
| 10 | Stacked bars; drop the line; ticks at the 2014–19 and 2023–25 means; "about 65 a year fills 492 at observed gains"; factual title. |
| 11 | Single histogram with 403–462 shaded and 450/492 marked, both specs (or trend with the level result in the caption); drop the narrowing panel; "roughly 90–110". |
| All | Author at 6.5-inch width so printed text is ≥ 8 pt; one semantic palette (Bear Creek blue, Mesa orange, merged violet, proposal red only on merged axes, trend solid / level dotted in one hue, background grey); "Source:" footer on every PNG; consistent title alignment. |

## F. Email and script

1. Email: open with the district's arithmetic (D1) and the fork (B1); the standard as a five-item list; split the enrollment paragraph into "How much the projections move" and "What the range assumes"; concede B3 explicitly; cut Pearman (B5a) or bound it; replace "cheap" (B4); subject line ≤ 40 characters ("Mesa/Bear Creek: enrollment evidence before the Sept. 22 vote"); update 58%/319/71 to the corrected level spec (A1); "60 to 118". A full 709-word draft in the exposition review is a good base once A1's numbers are known.
2. Script: put the 521 / 462 point first; "one chance in six … better than one in two" → after A1 this becomes roughly "one in six … about even"; "Third, proof that the merged school fits the building"; "…moves in and takes classrooms"; "stays small is fair"; cut to ≤ 280 words; add the one concrete Sept 8 question: "what share of Mesa students does 462 assume follow to Bear Creek?"; align "four things" with the five-item standard or say so knowingly.

## G. Leave alone

The concession paragraph; the five-clause standard; the revision table (Table 2) and every number in Tables 2–6 (all reproduce); the "pre-empting one objection" idea (once); the joint year-draw and out-of-sample backtest design; the district-arithmetic derivations (implied share, capture, payback); the "before you close a school you can't reopen" line.

## H. Decisions needed from you

1. **A1 centring convention**: mean-centred (recommended; keeps the level spec's expected kindergarten equal to the 2023–25 mean) or median-centred (more conservative; gap 54). I will report the window sensitivity either way.
2. **Which spec is primary downstream** (Fig 8, Fig 11, class sizes)? Options: (a) carry both everywhere (recommended; heavier figures); (b) level primary with trend as the lower-bound sensitivity, justified by C2 and C3.
3. **Pearman**: cut from the email (recommended) or keep bounded.
4. **Concede B3 in the email** ("my own model agrees Mesa stays small")? Recommended yes; it costs nothing and removes the district's strongest rhetorical counter.
5. **Add the p. 44 vs p. 51 resident discrepancy (C1) to the email's open questions**, replacing one of the five (candidate to drop: school-age care)?
6. **Appendix length**: cut to ~11 + 3 pages per D11, or keep everything and only reorder?
7. **Section 11 claim**: keep "±2 classrooms" (as "roughly 90–110 students, trend spec") or replace with the plainer "the October 2026 count will be the first taken under the new boundaries and the new portfolio, and standard (i) cannot be met without it"?

## I. Effort and order

1. A1–A8 model and number fixes, regenerate all outputs (half a day). 2. New lead figure, Fig 5 split, Fig 7/9/10/11 redesigns, common.py sizing and palette (half a day). 3. Appendix restructure and rewrite with labels/refs (half a day). 4. Email and script (one hour). 5. Rebuild, re-verify every number against the CSVs and pages, update STATUS.md and the verify-personally list (one hour).
