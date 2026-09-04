# mesa-analysis

Evidence base for a memo to the BVSD board on the proposed Mesa Elementary / Bear Creek Elementary consolidation (vote Sept 22, 2026; effective 2027-28 if approved).

## Ground rules
- Every figure must cite a source file in data/raw and a page or row. No numbers from memory.
- Keep raw source files unmodified in data/raw. Derived tables go in data/clean. Analysis in analysis/. Figures in figures/.
- Log every source in data/SOURCES.md: URL, retrieval date, what it contains, how it was extracted.
- When two sources disagree, record both in data/CONFLICTS.md; do not silently pick one.
- Distinguish district-published projections from actuals in every table (column or file name).
- Prefer pdfplumber/camelot for PDF tables; fall back to OCR only if needed, and flag it.
- Python; pandas; matplotlib. Keep a requirements.txt current.

## Key facts already established (verify, don't assume)
- Bear Creek capacity 492 (3.5 rounds, 21 classrooms); Mesa capacity 418 (3.0 rounds). Source: Feb 2026 trend report p. 9 (also Oct 21 2025 work session slide 17). Bear Creek was 467 in the Feb 2024 table and 475–478 in the 2011–2014 School Profile books (CONFLICTS C3, table17).
- Oct 2025 deck slide 17 = Jan 2025 run: 2029-30 Bear Creek 272, Mesa 224. Feb 2026 report (Jan 2026 run): 2029-30 Bear Creek 310, Mesa 202; 2030-31 320, 201.
- Aug 25 2026 proposal: merged school 392–445 (2027-28) and 403–462 (2030-31) at Bear Creek; residents 503 → 473 → 522 (deck **p. 51**, not pp. 37/39).
- Oct 2025 official funded head count: Bear Creek 312, Mesa **224** (CDE membership 225). Aug 28, 2026 preliminary: Bear Creek 330, Mesa 204.
- Enrollment Pattern Matrix 12/5/2025: four South Boulder areas 502 residents; 415 attend Bear Creek or Mesa (83%); outside enrollment 121 (75 + 23 + 23). Residents of the four areas 733 (2017-18) → 502 (2025-26).
- District programmatic thresholds: ~150 per round; 3 rounds ~450 (Oct 2025 work session slide 8). Staffing formula 1 : 24.58 (FY27 budget book p. 121); BVEA class-size goals 26 / 29 / 31.
- LRAC thresholds: Advisory = <=2 rounds and <=60% capacity; Engagement = <=1.5 rounds and <=50%.
- Policy JECC-R: open enrollment lasts for the duration of the school level (choice management acts on new entrants only).

## Open questions the data should eventually answer
1. Why did Bear Creek's out-year projection rise ~14% between the Jan 2025 and Jan 2026 runs? Boundary change ruled out as the main cause (C6); consistent with the 2024 rebound in area births (C30). Not confirmed by any document.
2. What capture rate and what outside enrollment does 403–462 assume? Answered on the district's own matrix: 54–65% or a cut to 30 (table14); the district's own assumption is still unstated.
3. How accurate have BVSD's school-level projections been? Answered: table20 (ten Octobers, district's own scoring) and §2 of the report.
4. What share of each school's enrollment is resident vs. open-enrolled? Answered: oe_matrix_* clean files, 2017-18 … 2025-26.
5. Still open: the AIM/RISE room footprint; the basis of 522 residents; the Sept 8 materials.
