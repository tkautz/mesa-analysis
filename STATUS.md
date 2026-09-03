# STATUS — updated 2026-09-03 (session 2: analysis and report)

## Session 2 (analysis) — done
- `analysis/01_descriptive.py` … `06_value_of_waiting.py` run end-to-end from the repo root; outputs in `figures/` (11 figures, PNG/SVG/PDF) and `analysis/output/` (tables).
- `report/report.tex` (LaTeX source), `report/report.pdf` and `report/report.html` (rendered via pandoc + Chromium because no TeX install is available in the session; the .tex compiles with pdflatex). Executive summary and the five-sentence paragraph are on page 1; also in `analysis/RESULTS.md`.
- Plan and approved additions: `analysis/PLAN.md`.

## Session 1 — collected
- **Primary BVSD documents** (hand-downloaded, sorted into `data/raw/bvsd/`, manifest in `MANIFEST.csv`): the Aug 25 2026 proposal deck (75 pp.), Feb 2024/2025/2026 trend reports, Oct 21 2025 work session, two executive summaries, LRAC June 2023 metrics, Resilient Schools FAQ, the Bear Creek/Creekside boundary-change page, and **36 October pupil-count PDFs (2014-15 … 2025-26)**. Full text extracted for every PDF; image-only table pages rendered and OCR'd (flagged).
- `data/clean/` highlights:
  - `bvsd_pupil_count_mesa_bearcreek.csv` — official head count, FTE, grades, out-of-district, FRL, SPED, ELL, race/gender, 12 years, both schools.
  - `capacity_summary_mesa_bearcreek_by_vintage.csv` and per-page `feb2024_report_p11.csv`, `feb2025_report_p9.csv`, `oct2025_deck_s17.csv`, `feb2026_report_p9.csv`, `aug2026_deck_p50/p51/p44.csv`.
  - `projections_by_vintage.csv` — rebuilt from primaries, every row verified, with page numbers.
  - `resident_vs_enrolled_mesa_bearcreek.csv` — 2025-26 resident / resident-attending / OE-in / out-of-district split (open question 4, partial).
  - `verification_headcount_sources.csv` — official vs enrollmentdata series.
- **Round 3**: CDE pupil membership 2019-20 … 2025-26 (`data/raw/cde/`, parsed to `data/clean/cde_mesa_bearcreek.csv`, compared in `verification_cde_vs_bvsd.csv`); the Mar 11 and Sept 9 2025 attendance-boundary board documents; the bvsd.org Resilient Schools page. All-school official head counts 2014-15 … 2025-26 in `bvsd_pupil_count_all_elementary.csv` (input for the projection-accuracy analysis).
- `data/SOURCES.md`, `data/CONFLICTS.md`, `data/VERIFICATION.md` updated; `scripts/` has twelve reproducible steps.
- `analysis/PLAN.md` — proposed analysis plan awaiting approval.

## Failed / still missing
- Network egress from the session still blocks bvsd.org, BoardDocs and CDE, so nothing was fetched programmatically. Still missing (low priority): CDE 2014-15 … 2018-19 files, the 2020-21 FTE summary, the May 20 2025 boundary session. **Most valuable next fetch: older Annual Enrollment Trend Reports (Feb 2022, Feb 2023) or any earlier BVSD 5-year projection tables**, because the accuracy analysis currently has only three projection vintages.
- No PR (repo had no base branch; creating one was denied). Branch: `claude/bvsd-mesa-bear-creek-data-vdbcu6`.

## Round 3 additions
4. **The boundary change cannot explain the projection jump.** The dual Bear Creek/Creekside area has 37 elementary students, 23 already at Bear Creek; the Sept 2025 change moves the remaining handful. Bear Creek's 2029-30 projection nonetheless rose by 38 students between the Jan 2025 and Jan 2026 runs, for reasons no document states.
5. **CDE and BVSD agree to within 1–2 students on K–5**, and the enrollmentdata "225" for Mesa is CDE's K–5 membership (BVSD's funded count is 224). Mesa has 25 PK students in CDE's 2025-26 file that appear in no BVSD table.

## Three things in the data that most surprised me (round 2)
1. **The Oct 2025 deck did not contain new projections.** Slide 17 is number-for-number the Feb 2025 report's table (Jan 24 2025 run). The "Oct 2025 vs Feb 2026" change in CLAUDE.md is really a Jan 2025 vs Jan 2026 change, and the Jan 2026 Bear Creek path is the first vintage that turns upward (288 → 310 → 320). The deck itself flags that its Boulder charts "do not reflect new 2026-27 attendance area boundaries", and the boundary page documents the Bear Creek/Creekside dual area becoming Bear Creek-only from 2026-27.
2. **Bear Creek's capacity was restated from 467 (3.0 rounds) to 492 (3.5 rounds)** between the Jan 2024 and Jan 2025 tables, with no explanation in any document. Mesa stayed at 418.
3. **The resident split is lopsided.** In 2025-26 Mesa enrolled 224 students but only 156 of the 228 residents of its attendance area attend it (68%); 58 are in-district open-enrollees and 10 out-of-district. Bear Creek: 217 of 275 residents (79%), 82 OE-in, 13 out-of-district. The consolidated projection's "resident students 473 (2027-28) / 522 (2030-31)" is below 275 + 228 = 503 in the first year and above it in the second, which will matter when the retention arithmetic is done in session 2.

## Corrections to CLAUDE.md "Key facts" (not applied; owner's call)
- Mesa Oct 2025 actual is **224**, not 225 (official pupil count, and what BVSD uses everywhere).
- The "462" figure is on deck **p. 51**, not pp. 37/39.

## Not done
Memo prose beyond the executive summary; cost quantification (no district cost data in the documents); Census/ACS age and housing data for the two attendance areas (would firm up the turnover scenario).
