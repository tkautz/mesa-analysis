# Conflicts between sources

Record both sides; do not resolve silently. Updated 2026-09-03 after the primary documents arrived. Items resolved by primaries are kept with their resolution.

## C1. Mesa October counts: BVSD official vs the two enrollmentdata series — RESOLVED IN FAVOR OF BVSD FILES
- Official (P13, `<year>_cde_headcount_summary.pdf` p. 1, "FUNDED HEAD COUNT" current-year column), Mesa 2014→2025: 330, 320, 287, 271, 260, 261, 235, 247, 246, 233, 230, **224**. Bear Creek: 417, 441, 438, 448, 425, 400, 341, 346, 342, 298, 318, **312**.
- enrollmentdata CSV differs from official in 6 of 12 Mesa years and 4 of 12 Bear Creek years, always by 1–2 students (e.g. Mesa 2025: 225 vs 224; Bear Creek 2019: 402 vs 400). The map series differs from official in 10 of 12 Mesa years by up to 32 (2018: 292 vs 260). Full table: `data/clean/verification_headcount_sources.csv`.
- Use `data/clean/bvsd_pupil_count_mesa_bearcreek.csv` from now on. `mesa_bearcreek_headcount.csv` (enrollmentdata) is retained only as the Step-2 artifact.
- Note the prior-year column in each BVSD file equals the previous file's current-year value in all 22 cases, so BVSD did not revise these counts after publication.

## C2. Mesa 2025-26: 224 vs 225 — RESOLVED
- 224 is the official funded head count (P13 2025-26, updated 1/22/2026) and is what P1 p. 51, P2 p. 9 and P5 use. 225 appears only in enrollmentdata and in CLAUDE.md. CLAUDE.md's "Mesa 225" should be corrected to 224.

## C3. Bear Creek capacity: 467 (3.0 rounds) in Feb 2024 vs 492 (3.5 rounds) from Feb 2025 on — OPEN
- P4 p. 11 (2023-24 summary): Bear Creek capacity **467**, 3.0 rounds. P3 p. 9, P5 slide 17, P2 p. 9, P1 p. 51: **492**, 3.5 rounds. Mesa is 418 / 3.0 in all four. No document explains the change (footnote in all three tables: "program capacity based on current use of the building"). Percent-of-capacity figures for Bear Creek are therefore not comparable across the Feb 2024 and later vintages.
- Separately, the ArcGIS attendance-area attributes in `data/raw/enrollmentdata/BVSD_Attendance_Areas.geojson` carry Bear Creek capacity 475 and Mesa 485 (vintage unknown), and the enrollmentdata headcount CSV's `max_enrollment` (448 / 330) is a 10-year peak, not capacity.

## C4. Attendance-area GeoJSON join error for "BC-Mesa" — unchanged
- The "BC-Mesa" polygon carries BC/SIS-HP's forecast attributes via a prefix-match join in the transcription. Ignore those attributes. The polygon itself is real: P1 p. 49 refers to "the Bear Creek, Mesa and dual attendance areas", and P10 documents a separate Bear Creek/Creekside dual area.

## C5. enrollmentdata headcount CSV grade columns — RESOLVED (unreliable; superseded)
- The official files give full K–5 (and PK through 2022-23) grade counts that sum exactly to the head count in all 24 Mesa/Bear Creek school-years. The transcription's 2023 seventh column (13 / 16) does not correspond to anything in the official file (PK was 0 for both schools every year it was reported).

## C6. Oct 2025 deck vs Feb 2026 report projections (open question 1) — DATA NOW IN HAND, NOT EXPLAINED
- P5 slide 17 (Oct 21 2025) and P3 p. 9 (Feb 2025, "updated 1/24/2025") are **identical** for Mesa and Bear Creek: 2029-30 Bear Creek 272 / Mesa 224. So the Oct 2025 deck re-used the January 2025 projection run; the jump is between the Jan 2025 and Jan 2026 runs.
- P2 p. 9 (updated 1/26/2026): 2029-30 Bear Creek 310 / Mesa 202; 2030-31 320 / 201.
- P5 slide 19 carries the note "Chart does not reflect new 2026-27 attendance area boundaries." P10: the Bear Creek/Creekside dual area west of Broadway and north of Table Mesa becomes Bear Creek-only from 2026-27 (adopted Sept 23 2025). Whether the Jan 2026 run incorporates that change is not stated in P2.
- Also: the Feb 2026 Bear Creek path is non-monotonic (299, 293, 288, then 310, 320), unlike every earlier vintage.

## C7. Page references in CLAUDE.md for the "462" figure
- CLAUDE.md cites "deck pp. 37, 39". In P1 as downloaded, pp. 37–39 are the Monarch/Eldorado pages; the Mesa/Bear Creek consolidation is **pp. 49–51** and the 403–462 range is on **p. 51**. The enrollmentdata About page's "pp. 25, 37, 39, 48, 51 and 54" list covers several schools; for this pair the right page is 51.

## C8. Resident-student counts across documents
- P1 p. 51 (2025-26): Bear Creek resident students 275, Mesa 228. P1 p. 44 bar labels (residents attending their neighborhood school): Bear Creek 217, Mesa 156.
- P5 slide 19 (2024-25, pre-boundary-change chart, no labels): the Bear Creek "attending neighborhood school" bar visibly extends past 300 while 2024-25 enrollment was 318, and the total resident bar reads ≈380; Mesa reads ≈155 / ≈228. A 2024-25 resident-attending count above ~300 is hard to reconcile with 217 a year later unless the dual attendance area was counted differently. Recorded as a puzzle; do not use the slide-19 bar readings as data.
- P1 p. 50 says Mesa "has the second lowest number of resident students in its attendance area" in Boulder; p. 44 shows Flatirons (≈195) lowest and Mesa (228) second-lowest, consistent.

## C9. Branch name — as before
- Work is on `claude/bvsd-mesa-bear-creek-data-vdbcu6`, not `data-collection`.
