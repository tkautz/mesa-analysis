# Analysis plan — APPROVED 2026-09-03 with additions (see §7–8)

## The claim the analysis has to support
The Mesa → Bear Creek consolidation is justified in BVSD's own documents by (a) current utilization and (b) five-year enrollment projections (proposal deck pp. 50–51; bvsd.org p. 7). The decision is irreversible in practice. The projections it rests on carry no stated uncertainty, have moved materially between annual runs, and are produced by the same office that proposes the closure. The memo asks the Board to require a higher standard of evidence before an irreversible act: one more October count, an independent projection with confidence bands, and a decision in 2027.

What the analysis must NOT do: claim that enrollment *will* be higher than projected. The case is about the width of the band and the asymmetry of the mistakes, not the sign.

## What we have (all in data/clean, every number page-cited)
- Official October counts, K–5 by grade, both schools, 2014-15 … 2025-26 (BVSD), cross-checked with CDE 2019-20 … 2025-26.
- All 30+ elementary schools' October counts, 12 years.
- Three independent BVSD projection vintages (Jan 2024, Jan 2025, Jan 2026), each 5 years ahead, for every elementary school, plus the Oct 2025 deck (a re-print of Jan 2025).
- BVSD's post-consolidation range (392–445 in 2027-28; 403–462 in 2030-31), its resident-student counts (275 + 228 in 2025-26; 473 / 522 projected for the combined area), capacities (492 / 418), thresholds (150 per round; ≤2 rounds & ≤60% advisory).
- The Bear Creek capacity restatement (467 → 492) and the size of the 2026-27 boundary change (37 students, 23 already at Bear Creek).

## Proposed work, in order

### 1. "How much have the district's own numbers moved?" (descriptive, no model)
- **Fig 1** Spaghetti plot: Mesa and Bear Creek actuals 2014–2025 with the Jan 2024, Jan 2025 and Jan 2026 projection paths overlaid, plus the Aug 2026 consolidated range. One panel per school and one for the pair. Annotate the 2029-30 Bear Creek revision (272 → 310) and Mesa (224 → 202).
- **Table 1** Same numbers, with the year-over-year revision for each target year.
- **Fig 2** Implied "who follows" arithmetic behind 403–462: the range against Mesa + Bear Creek separate projections (521), against resident counts (503 today, 522 projected), and against the 450 three-round line and 492 capacity. No modelling, just the district's own figures on one axis.
- Output: figures/fig01_vintages.png, fig02_range_arithmetic.png; analysis/01_descriptive.py.

### 2. "How accurate have these projections been?" (empirical error distribution, all schools)
- Data: Jan 2024 vintage → actual 2024-25 (1-yr) and 2025-26 (2-yr); Jan 2025 vintage → actual 2025-26 (1-yr). ≈32 schools × 3 = ~95 school-level errors; district-level errors from the reports' own admissions (Feb 2026 p. 5: projected −0.9%, actual −1.9%).
- Metrics: percent error, absolute percent error, signed bias; median and 80/90% quantiles by horizon; error vs school size (small schools should be noisier — Mesa is small).
- Horizon extrapolation: only 1- and 2-year-ahead errors are observable. I will (a) report those honestly, (b) show the *revision* between successive vintages for the same target year at 3–5 years out as a lower bound on the uncertainty at those horizons (a forecaster who revises a 4-year-ahead number by 14% is telling you the 4-year band is at least that wide), and (c) note that in the published literature cohort-survival school-level errors grow roughly with the square root of horizon. If F12 (older trend reports) arrives, 3- to 5-year errors become directly measurable and this section gets much stronger.
- **Fig 3** Error distribution by horizon (dot/strip plot per school, Mesa and Bear Creek highlighted). **Fig 4** Revision magnitude vs horizon.
- Output: analysis/02_projection_accuracy.py, data/clean/projection_errors_all_schools.csv.

### 3. Independent projection with honest uncertainty (the "error band")
- Model A (primary): grade-progression (cohort-survival) model per school, fitted to the 12 years of grade-level counts. Uncertainty by bootstrapping the year-specific progression ratios and kindergarten intake (block bootstrap over years, so 2020's shock is kept as one draw), 10,000 paths to 2030-31. Reported as 50/80/95% prediction intervals.
- Model B (robustness): a simple total-enrollment model (log-linear trend with AR(1) errors, or a random walk with drift), prediction intervals from the residual variance. Chosen because it makes fewer assumptions and will disagree with A in an instructive way.
- Both models run for Mesa, Bear Creek, the sum, and (for calibration) every other elementary school, so we can show the bands are not tuned to this pair: the 80% band should contain about 80% of the 2024-25 and 2025-26 actuals when the model is fit on data through 2023-24 (a backtest).
- **Fig 5** Fan charts for Mesa, Bear Creek and combined, with BVSD's point projections and the 403–462 range overlaid. **Fig 6** Backtest coverage.
- Output: analysis/03_independent_projection.py; data/clean/independent_projection_paths.parquet (or csv summary).

### 4. Consolidation scenario grid: "what if they're wrong in either direction"
- Inputs: the Model A joint distribution for Bear Creek + Mesa; a retention parameter r (share of Mesa students who enrol at Bear Creek rather than open-enrol elsewhere) over 60–100%; plus an OE-in response parameter (does Bear Creek's ~95 open-enrolled-in students hold?).
- Outputs, for 2027-28 and 2030-31: probability combined enrollment at Bear Creek exceeds 450 (three rounds), 467 (95% of capacity), 492 (capacity); implied average class size per grade at 21 sections (3.5 rounds × 6); probability it falls below 300 (two rounds) — i.e. the downside where the merged school ends up in the same advisory status Mesa is in now.
- **Fig 7** Heatmap of P(over capacity) and P(below 2 rounds) over r × year. **Fig 8** Class-size distribution at r = 80/90/100%.
- Output: analysis/04_consolidation_scenarios.py.

### 5. Value of waiting one year (short, quantitative)
- Using Model A: re-fit with one more simulated observation (Oct 2026 count) and show how much the 2030-31 interval narrows in expectation; state what BVSD would also have by Sept 2027 (a Jan 2027 projection run incorporating the 2026-27 boundary change, one more CDE count, an outside projection if commissioned).
- Cost asymmetry table, qualitative with numbers where documents supply them: reversible error (keep Mesa open a year: one year of two-school operating cost, which the district has not quantified in these documents) vs irreversible error (close Mesa, enrollment runs high: portables/redraws/split classes; enrollment runs low: a 3-round building at 2 rounds).
- **Fig 9** Interval width for 2030-31 as a function of decision date.
- Output: analysis/05_value_of_waiting.py.

### 6. Write-up
- analysis/RESULTS.md: every figure with its one-sentence takeaway, the numbers behind it, and page citations; a limitations section (three vintages only; capacity restatement; PK definitions; no cost data).
- Memo-ready bullets (not the memo): 8–10 sentences you can lift.

## Decisions I need from you
1. **Scope OK as above?** Sections 1–4 are the core; 5 is the option-value framing an economist will want but it is the most assumption-laden. I recommend doing all five; say if you want 5 cut or expanded.
2. **Older projection vintages.** If you can find the Feb 2023 and Feb 2022 Annual Enrollment Trend Reports (or any BVSD 5-year table from 2016–2021) on BoardDocs, section 2 becomes a direct 3–5-year-ahead accuracy test instead of a lower bound. Worth 20 minutes of searching before I start section 2.
3. **Model choice.** Cohort-survival with block bootstrap as primary (matches BVSD's own method, so the comparison is like-for-like), simple trend model as robustness. Alternative: a Bayesian hierarchical model pooling all 30 schools (tighter, but harder to explain to a board). I recommend the first.
4. **Retention range** for section 4: 60–100%. BVSD's own 403–462 implies roughly 45–75% of Mesa's projected 2030 enrollment landing at Bear Creek if Bear Creek's own path is 320 (the numbers will be shown, not assumed). Say if you want a different range.
5. **Figure style**: matplotlib, one consistent palette, PNG + SVG, sized for a memo page. Anything else (slide format, colorblind-safe only) tell me now.

## What I will not do without asking
Draft memo prose; assert a direction for the error; use the enrollmentdata transcription for any number; add data sources beyond those in data/raw.

## Estimated effort
Sections 1–2: one session. Sections 3–4: one to two sessions. Section 5 and write-up: one session.

## Additions approved 2026-09-03 (owner's instructions)
### 7. Upside scenarios: what would it take for Bear Creek to fill?
Error is shown three ways: (i) the district's own track record (§2), (ii) statistical prediction intervals (§3), and (iii) named scenarios that push enrollment up, each with the arithmetic of how far it moves the merged school toward 450 / 492:
- **Leveling-off**: the decline stops (kindergarten intake and progression hold at 2023–2025 levels) rather than continuing at the projected rate. Test against the data: has combined K intake at the two schools already flattened?
- **Housing turnover / aging-out**: BVSD's own FAQ says the over-60 population is the fastest-growing segment and "aging in place" constrains turnover. The flip side is that this cohort turns over eventually. Parametric: each 1% of homes in the combined area that turns over to a family with children adds N students (using BVSD's own yield figure of 58 elementary students per 324 single-family dwellings from the Sept 9 2025 boundary study, p. 22). Show the turnover rate that reaches 450 and 492 by 2030-31 and 2035.
- **Open-enrollment inflow**: the merged school inherits Bear Creek's ~95 OE-in students; scenarios where OE-in rises because a 3-round school with full programs attracts families, or because Mesa families who would have open-enrolled elsewhere stay.
- **Resident capture**: today 68% (Mesa) / 79% (Bear Creek) of resident students attend their neighborhood school; show the merged enrollment if capture rises to 85–90%.
- **Combined scenario tables**: 2027-28 and 2030-31 enrollment under each, with the number of sections and average class size at 21 classrooms.
Data limits to state plainly: no Census/ACS age structure or housing counts for the attendance areas are in the repo; the turnover scenario is parametric and cites BVSD's own yield figure.

### 8. Deliverable format
- `report/report.tex` (LaTeX, article class, all figures and tables, full method and scripts referenced by path) plus `report/report.pdf`. No TeX distribution is installed in this session, so the PDF is rendered from the same source via pandoc → HTML → Chromium; the .tex compiles with pdflatex on any TeX install.
- Executive summary on page 1, and a boxed **five-sentence paragraph**: (1) BVSD proposes an irreversible closure on projections that carry no stated uncertainty; (2) the district's own projections for these schools moved by X between annual runs and missed by Y at one to two years; (3) under plausible upside scenarios the merged school reaches/exceeds three rounds or capacity by 2030; (4) an independent model puts the 80% band at [a, b]; (5) request: defer the decision one year and obtain an independent projection with confidence bands.
- Other arguments to weigh in the write-up: the Bear Creek capacity restatement (467 → 492) changes utilization by 5 points on its own; Mesa's 25 PK students are absent from the tables; the district's stated goal of three rounds (~450) is within the merged school's own range only at the top; the boundary change was too small to explain the Bear Creek revision; the option value of one more count is high because the Jan 2027 run will be the first to include the new boundaries and the proposal's own OE-priority rules.
