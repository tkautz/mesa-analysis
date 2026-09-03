# STATUS — session 1 (data collection), 2026-09-03

## Collected
- **enrollmentdata.org transcription** (yoavlurie/bvsd-enrollment @ 37a9bf9, CC0) vendored to `data/raw/enrollmentdata/`, .git removed, LICENSE kept.
- `data/clean/`:
  - `BVSD_October_Headcount_2014-2025.csv`, `BVSD_Capacity_Forecast_2025-2031.csv` (with `_source`)
  - `mesa_bearcreek_headcount.csv` — long format, Mesa + Bear Creek, all years and grade columns, `data_type=actual`
  - `projections_by_vintage.csv` — oct2025 / feb2026 / aug2026 for Mesa and Bear Creek, every row flagged `verified_against_primary=False`
  - `aug2026_proposal_projections_transcribed.csv`, `aug2026_proposal_actions_transcribed.csv` — the Aug 25 2026 deck's post-change ranges and action text, as transcribed in the enrollmentdata map (deck pp. 25/37/39/48/51/54 per the author)
  - `enrollmentdata_map_history_all_schools.csv`, `enrollmentdata_map_elementary_forecast.csv`, `enrollmentdata_internal_check.csv` — the map's second data series and its comparison with the CSV
  - `attendance_area_attributes_mesa_bearcreek.csv` — ArcGIS attributes for Mesa, Bear Creek and the "BC-Mesa" polygon
- `data/SOURCES.md`, `data/CONFLICTS.md`, `data/VERIFICATION.md`; `scripts/` (four reproducible prep scripts); `requirements.txt`.

## Failed
Every primary source. The remote session's egress policy allows only GitHub and package registries; boarddocs.com, bvsd.org, cde.state.co.us, archive.org and news sites all returned `CONNECT tunnel failed, response 403` from curl and `EGRESS_BLOCKED` from WebFetch (log: `data/raw/bvsd/FETCH_FAILURES.txt`; per-URL table: SOURCES.md F1–F7). A Google Drive search for the document titles found nothing. Consequences:
- No PDF text or page-level table CSVs (`aug2026_deck_p37.csv` etc.) exist. Nothing was OCR'd or reconstructed.
- No CDE membership data, no BVSD pupil-count files, therefore no resident vs. open-enrolled split (open question 4) and no CDE-vs-BVSD comparison.
- The Oct 2025 vintage rests entirely on the numbers in CLAUDE.md.
- Branch: pushed to the session's designated branch `claude/bvsd-mesa-bear-creek-data-vdbcu6`, not `data-collection` (the harness pins the branch name). Rename on GitHub if you want `data-collection`.

## Fetch next (by hand, from a normal browser, into the directories in SOURCES.md)
1. The three BoardDocs PDFs (F1–F3). Then run pdfplumber on every page mentioning Mesa / Bear Creek and re-run VERIFICATION rows 1–12 against actual page numbers.
2. BVSD historical October pupil count files (F7) — this is the only way to settle CONFLICTS.md C1 (which of the two Mesa series is right) and C5 (grade columns).
3. CDE PK-12 Membership by School XLSX for 2014-15 … 2025-26 (F5/F6) and the school-level resident / non-resident or open-enrollment file if CDE publishes one; confirm school codes (5838 Mesa, 0652 Bear Creek are unconfirmed).
4. bvsd.org Resilient Schools page (F4) for the LRAC threshold language and the 2026-27 boundary-change documents (open question 1).

## Three things in the data that most surprised me
1. **The transcription disagrees with itself on Mesa.** The CSV and the live map in the same CC0 repo give different Mesa October counts in 10 of 12 years (e.g. 2018: 260 vs 292), while Bear Creek agrees in all 12. Across all elementary schools 238 of 324 school-years differ; only 2025 agrees everywhere. Any Mesa trend statement needs BVSD's own files first.
2. **462 is below the sum of the two schools' Feb 2026 projections.** Feb 2026 has Bear Creek 320 + Mesa 201 = 521 for 2030-31 (310 + 202 = 512 for 2029-30). The deck's post-merger range for Bear Creek in 2030 is 403–462, i.e. the *upper* bound already assumes fewer students than the two schools are projected to have separately. What retention share that implies is session 2's question 2, not answered here.
3. **BVSD's own GIS layer has a "BC-Mesa" attendance polygon** (SchCode 1, StdtPop 134, distinct from Bear Creek SchCode 119 / StdtPop 169 and Mesa SchCode 166 / StdtPop 258), and the ArcGIS capacity attributes (Bear Creek 475, Mesa 485) differ from the 492/418 used in the 2025-26 reports. Both are relevant to open question 1 (boundaries) and neither is dated.

## Not started (by design)
No modeling, no memo text, no figures. `analysis/` and `figures/` are empty.
