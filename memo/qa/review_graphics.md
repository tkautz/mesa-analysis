# QA review 5: graphics and persuasion, 2026-09-03

## Two facts that apply to almost every figure
1. Print scale: text width 6.5 in; figures authored at 8.4–12.2 in and shrunk, so smallest text prints at 4.0–5.3 pt (fig01 5.2, fig02 4.1, fig03 5.3, fig05 4.6, fig07 4.8, fig09 4.0). Fix once in common.py: author at figsize width 6.5.
2. Palette semantics drift: blue is Bear Creek, also Jan 2026 run, A-trend, 1-yr horizon, 90% retention, background dots. Violet is "all district figures" (Fig 2) and "deterministic cases" (Fig 9). In greyscale green #008300 (111) and blue #2a78d6 (119) and red (126) are indistinguishable; green/red adjacency in Fig 5 fails colorblind readers.

## Per-figure
| Fig | Verdict | Top defect | Fix |
|---|---|---|---|
| 1 | Redesign | Merged-school range drawn on the Bear Creek-alone panel (reads as BC jumping to 400–460). | Two panels (BC, Mesa), x from 2020, direct-label runs, bracket annotate +38/−22; red band only on merged axes. Keep "(re-used Oct 2025)" in a label. |
| 2 | Redesign lightly, promote to Summary | Eight rows mixing residents/actuals/projections; rotated clipped labels; 4.1 pt. | Stacked bar (320+201=521; 293+203=496) over red range bar (403–462; 392–445), bracket "59 students = 29% of Mesa's projected; range implies 41–71% follow". Residents to Table 1. |
| 3 | Modest redesign | Background dots same blue as BC highlight; right title asserts a weak relationship. | Grey background; right panel as three size bins (<300, 300–400, >400, n shown) titled "Absolute error by school size". |
| 4 | Keep w/ fixes | Empty "1 yr" tick; P10–P90 hairlines; outliers set axis. | Drop 1-yr tick; shaded P10–P90 band with "±12%" at 4–5 yr; n under columns; consider merging with Fig 3 left. |
| 5 | Split | Seven encodings; district path same blue as A-trend fan; green vs red; red band on BC-alone panel; Combined panel is 100% follow while text is 90%; the 319≈320 fact invisible. | 5a: Bear Creek only, from 2018, two medians + one 80% band each (fill vs dotted), district's path ending at labeled "320" dot, annotate "A-level 319 / A-trend 268". 5b: merged at 90% follow, two 80% bands, 450/492 lines, proposal bracket at 2030, P(>492) 16%/58% on chart. Drop 50/95 fills. |
| 6 | Keep, fix labels; appendix | "(bars = nominal)" wrong; blue/orange mean different things in the two panels. | Greys for bars, black ticks nominal; grey background dots; label 45° "equal error". |
| 7 | Redesign or table | 108 cells at 4.8 pt; P(<300) column all 0%; specs 6 in apart. | One panel: x = share following, y = probability, four lines (P>450, P>492 × trend/level), 2030–31, highlight 90%. Rest to appendix table. |
| 8 | Cut or redesign | Density axis; A-trend only; 21 sections vs "3-round" framing (at 18 sections medians 24 trend / 28 level). | Dot-range chart: rows 80/90/100% × trend/level, median + P10–P90, at 21 and 18 sections, district class-size target if documented. |
| 9 | Re-title, light redesign | Title is an inference ("plausible"); bottom row 392 contradicts it; 4.0 pt labels; blue = model here. | Title "Merged-school enrollment in 2030–31 under nine cases: five exceed 492"; shade 403–462 as a column; labels ≤35 chars with lettered key; group rows by kind; author at 6.5 in. |
| 10 | Keep, fix | Label collides with line; legend on points; title asserts the contested point. | Stacked bars (BC base, Mesa top); drop line; 82/yr at right; ticks at 95 (2014–19 mean) and 73 (2023–25 mean); title "Kindergarten intake at the two schools, 2014–2025; 82 a year fills 492 seats". |
| 11 | Drop right panel | Histogram lacks 403–462/450/492 references; right panel argues against waiting; 431 vs 430. | Single histogram with 403–462 shaded, 450/492 dotted, "x% of simulated counts push the estimate above 462; y% below 403"; narrowing to one sentence; reconcile 431/430. |

## Document-level
1. Carrying figures: Fig 2 redesigned (Summary, full width), Fig 5a (the 320 on the A-level median), Fig 9 re-titled. Fig 1 is context, should not lead.
2. Missing figure: "What the district's own numbers imply": number line 300–560, two rows (2030–31, 2027–28), stacked blue+orange bar (320+201→521; 293+203→496) over red range bar (403–462; 392–445), dotted 450/492 with top labels, bracket "59 students (29% of Mesa's projected) not in the range" / "51 (25%)", note "range implies 41–71% follow (deck p. 51 vs Feb 2026 p. 9)", source line on the image. Replaces Fig 2. Second missing figure = 5a. P(>492) bars as an inset on 5b.
3. Fan bands not readable as built; one 80% band per spec (fill vs outline), medians only; 50/95 in table.
4. Titles must be facts: Fig 9, 10, 3-right, 6-left, 11-left, 1 re-titled as listed.
5. Consistency: semantic palette (BC blue, Mesa orange, merged violet, proposal red only on merged axes, district projections grey/vintage set, A-trend solid / A-level dotted same hue, background light grey); figsize at page width; suptitle alignment; a "Source:" footer on every PNG via save(); reconcile 431/430, 100% vs 90% in Fig 5, 21 vs 18 sections in Fig 8.

## Five highest persuasion-per-hour changes
1. Build the district's-own-numbers chart, put it in the Summary (replaces Fig 2). 1–2 h.
2. Re-title Fig 9, shade proposal range column, shorten labels, author at 6.5 in. 1 h.
3. Split Fig 5 into 5a (BC two-spec with 320 dot) and 5b (merged at 90% with P(>492) on chart). 2–3 h.
4. Page-width figsize everywhere; remove merged band from BC-alone panels in Figs 1, 5. 1–2 h.
5. Fig 11 single histogram with range shaded; drop right panel; reconcile 431/430. 0.5 h.
Sixth hour: Fig 7 → four-line chart; grey background dots in Figs 3, 4, 6.
