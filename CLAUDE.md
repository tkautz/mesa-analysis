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
- Bear Creek capacity 492 (3.5 rounds); Mesa capacity 418 (3.0 rounds). Source: BVSD Oct 21 2025 board deck, slide 17.
- Oct 2025 deck projections 2029-30: Bear Creek 272, Mesa 224.
- Feb 2026 trend report projections 2029-30: Bear Creek 310, Mesa 202; 2030-31: Bear Creek 320, Mesa 201.
- Aug 25 2026 proposal states merged school "up to 462 students in 2030" at Bear Creek (deck pp. 37, 39).
- Oct 2025 actuals: Bear Creek 312, Mesa 225 (per enrollmentdata.org transcription of BVSD pupil count).
- District programmatic thresholds: ~150 per round; 3 rounds ~450 (Oct 2025 deck slide 8).
- LRAC thresholds: Advisory = <=2 rounds and <=60% capacity; Engagement = <=1.5 rounds and <=50%.

## Open questions the data should eventually answer
1. Why did Bear Creek's out-year projection rise ~14% and Mesa's fall ~10% between Oct 2025 and Feb 2026? (Hypothesis: new 2026-27 attendance boundaries.)
2. What retention rate does "462" imply, and what happens to Bear Creek class sizes at 80/90/100% retention?
3. How accurate have BVSD's school-level projections been historically?
4. What share of each school's enrollment is resident vs. open-enrolled?
