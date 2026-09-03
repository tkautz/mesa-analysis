# STATUS — session 1 (data collection), updated 2026-09-03 (round 2)

## Collected
- **Primary BVSD documents** (hand-downloaded, sorted into `data/raw/bvsd/`, manifest in `MANIFEST.csv`): the Aug 25 2026 proposal deck (75 pp.), Feb 2024/2025/2026 trend reports, Oct 21 2025 work session, two executive summaries, LRAC June 2023 metrics, Resilient Schools FAQ, the Bear Creek/Creekside boundary-change page, and **36 October pupil-count PDFs (2014-15 … 2025-26)**. Full text extracted for every PDF; image-only table pages rendered and OCR'd (flagged).
- `data/clean/` highlights:
  - `bvsd_pupil_count_mesa_bearcreek.csv` — official head count, FTE, grades, out-of-district, FRL, SPED, ELL, race/gender, 12 years, both schools.
  - `capacity_summary_mesa_bearcreek_by_vintage.csv` and per-page `feb2024_report_p11.csv`, `feb2025_report_p9.csv`, `oct2025_deck_s17.csv`, `feb2026_report_p9.csv`, `aug2026_deck_p50/p51/p44.csv`.
  - `projections_by_vintage.csv` — rebuilt from primaries, every row verified, with page numbers.
  - `resident_vs_enrolled_mesa_bearcreek.csv` — 2025-26 resident / resident-attending / OE-in / out-of-district split (open question 4, partial).
  - `verification_headcount_sources.csv` — official vs enrollmentdata series.
- `data/SOURCES.md`, `data/CONFLICTS.md`, `data/VERIFICATION.md` rewritten; `scripts/` has nine reproducible steps.

## Failed / still missing
- Network egress from the session still blocks bvsd.org, BoardDocs and CDE, so nothing was fetched programmatically. Not in the hand-downloaded batch: the bvsd.org declining-enrollment page (F4), all CDE membership XLSX files (F5/F6), the 2020-21 FTE summary (F8). Wish-list: F9–F11 in SOURCES.md.
- No PR (repo had no base branch; creating one was denied). Branch: `claude/bvsd-mesa-bear-creek-data-vdbcu6`.

## Three things in the data that most surprised me (round 2)
1. **The Oct 2025 deck did not contain new projections.** Slide 17 is number-for-number the Feb 2025 report's table (Jan 24 2025 run). The "Oct 2025 vs Feb 2026" change in CLAUDE.md is really a Jan 2025 vs Jan 2026 change, and the Jan 2026 Bear Creek path is the first vintage that turns upward (288 → 310 → 320). The deck itself flags that its Boulder charts "do not reflect new 2026-27 attendance area boundaries", and the boundary page documents the Bear Creek/Creekside dual area becoming Bear Creek-only from 2026-27.
2. **Bear Creek's capacity was restated from 467 (3.0 rounds) to 492 (3.5 rounds)** between the Jan 2024 and Jan 2025 tables, with no explanation in any document. Mesa stayed at 418.
3. **The resident split is lopsided.** In 2025-26 Mesa enrolled 224 students but only 156 of the 228 residents of its attendance area attend it (68%); 58 are in-district open-enrollees and 10 out-of-district. Bear Creek: 217 of 275 residents (79%), 82 OE-in, 13 out-of-district. The consolidated projection's "resident students 473 (2027-28) / 522 (2030-31)" is below 275 + 228 = 503 in the first year and above it in the second, which will matter when the retention arithmetic is done in session 2.

## Corrections to CLAUDE.md "Key facts" (not applied; owner's call)
- Mesa Oct 2025 actual is **224**, not 225 (official pupil count, and what BVSD uses everywhere).
- The "462" figure is on deck **p. 51**, not pp. 37/39.

## Not started (by design)
No modeling, no memo text, no figures. `analysis/` and `figures/` are empty.
