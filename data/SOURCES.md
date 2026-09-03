# Sources

Retrieval date for everything below: **2026-09-03** (UTC), from a Claude Code remote session whose network egress policy allows only GitHub and package registries. Every non-GitHub host was denied. Exact errors are in `data/raw/bvsd/FETCH_FAILURES.txt`.

## Retrieved

### S1. enrollmentdata.org transcription (yoavlurie/bvsd-enrollment)
- URL: https://github.com/yoavlurie/bvsd-enrollment (live site https://enrollmentdata.org, not reachable from here)
- Retrieved: 2026-09-03 via `git clone`; commit `37a9bf9e704e2b13c1e370c0956b89efb3d0a8fb` (2026-08-27 12:54:49 -0600, "Open source under CC0 1.0"). Recorded in `data/raw/enrollmentdata_git_commit.txt`. The `.git` directory was removed; `LICENSE` (CC0 1.0) kept.
- Location: `data/raw/enrollmentdata/` (unmodified).
- Contents and what each was used for:
  - `BVSD_October_Headcount_2014-2025.csv` — per-school October headcount 2014–2025 with partial grade columns. Author's About page attributes it to "bvsd.org — Enrollment Statistics: Historical Pupil Count". Copied to `data/clean/` with `_source` column; Mesa/Bear Creek rows melted to `data/clean/mesa_bearcreek_headcount.csv`.
  - `BVSD_Capacity_Forecast_2025-2031.csv` — elementary capacity, rounds, 2025-26 enrollment and 2026-27…2030-31 projections. Author attributes it to the Feb 10 2026 Annual Enrollment Trend Report, "Capacity Summary 2025-26 (updated 1/26/2026)", report p. 9. Copied to `data/clean/` with `_source` column.
  - `maps/index.html` (identical to `maps/bvsd-enrollment-map.html`) — the dashboard. Contains JS literals transcribing: (a) a second October-history series per school (`schools[]`), (b) the Feb 2026 elementary forecast (`elementaryForecast`), (c) the Aug 25 2026 proposal's post-change enrollment ranges and utilization (`proposalProjections`, attributed by the author to deck pp. 25, 37, 39, 48, 51, 54), (d) proposal action text (`proposals`). Parsed by `scripts/extract_map_embedded_data.py` into `data/clean/enrollmentdata_map_*.csv` and `data/clean/aug2026_proposal_*_transcribed.csv`; every row carries the source line number.
  - `maps/about/index.html` — the author's bibliography (quoted in STATUS.md).
  - `BVSD_Attendance_Areas.geojson`, `BVSD_Attendance_Areas_Summary.csv` — attendance-area polygons with BVSD ArcGIS attributes (SchCode, StdtPop, Capacity, Enroll, Perc_Cap; vintage unknown) plus Feb 2026 forecast fields joined on by the author. Includes a **"BC-Mesa"** polygon (SchCode 1, StdtPop 134). Mesa/Bear Creek/BC-Mesa attributes exported to `data/clean/attendance_area_attributes_mesa_bearcreek.csv`.
- Caveat: this is a private transcription, "not affiliated with or endorsed by BVSD". Its two internal October-count series disagree for most schools (see CONFLICTS.md C1).

### S2. CLAUDE.md "Key facts" (user-supplied)
- Figures the repo owner typed into CLAUDE.md, attributed to the Oct 21 2025 deck (slides 8, 17), the Feb 2026 report and the Aug 25 2026 deck (pp. 37, 39). Used only in `data/clean/projections_by_vintage.csv` rows with `verified_against_primary=False`, because the primary documents could not be fetched. Treat as unverified.

## NOT retrieved (all denied by egress policy)

For each, the attempt was (i) `curl -sSL` from the container → `curl: (56) CONNECT tunnel failed, response 403` (proxy status page: `gateway answered 403 to CONNECT (policy denial or upstream failure)`); (ii) the WebFetch tool → `EGRESS_BLOCKED: Access to <host> is blocked by the network egress proxy.`; (iii) a Google Drive search for the document titles → no results. No content was fabricated; no PDF text, tables or page numbers in this repo come from these documents directly.

| # | Document | URL | Intended location |
|---|---|---|---|
| F1 | Resilient Schools Proposal FINAL 08-25-2026 (Aug 25 2026 deck) | https://go.boarddocs.com/co/bvsd/Board.nsf/pfiles/DXBFUX40E0C7/$file/Resilient%20Schools%20Proposal%20FINAL%2008-25-2026%20(1).pdf | data/raw/bvsd/ |
| F2 | Annual Enrollment Trend Report, February 2026 | https://go.boarddocs.com/co/bvsd/Board.nsf/pfiles/DQTRAN6D12DA/$file/Annual%20Enrollment%20Trend%20Report%20_%20February%202026.pdf | data/raw/bvsd/ |
| F3 | Enrollment Worksession 10.21.2025 (Oct 21 2025 deck) | https://go.boarddocs.com/co/bvsd/Board.nsf/pfiles/DMJTXV756DA8/$file/Enrollment%20Worksession%20_%2010.21.2025%20(1).pdf | data/raw/bvsd/ |
| F4 | BVSD "Resilient Schools: Responding to declining enrollment" page | https://www.bvsd.org/current-topics/declining-enrollment | data/raw/bvsd/ (HTML + txt) |
| F5 | CDE prior-year pupil membership index (PK-12 Membership Grade Level by School, 2014-15 … 2024-25) | https://www.cde.state.co.us/cdereval/rvprioryearpmdata | data/raw/cde/ |
| F6 | CDE current-year pupil membership (2025-26) | https://cde.state.co.us/cdereval/pupilcurrent | data/raw/cde/ |
| F7 | BVSD historical October pupil count files | https://www.bvsd.org/departments/enrollment/enrollment-statistics/pupil-count | data/raw/bvsd/pupil_count/ |

Also blocked: web.archive.org, boulderreportinglab.org, enrollmentdata.org. WebSearch returned result snippets only; none were used for figures.

## To fetch by hand (drop into the listed directory, then re-run the verification)
- F1–F3 PDFs → `data/raw/bvsd/`; then `pdfplumber` text + tables for every page mentioning Mesa or Bear Creek → `data/clean/<vintage>_deck_p<NN>.csv`.
- F4 → `data/raw/bvsd/declining-enrollment.html` and `.txt`.
- F5/F6 XLSX for each year → `data/raw/cde/`; Boulder Valley RE-2 (district 0480), school codes to be confirmed against names in the file (task brief says 5838 Mesa, 0652 Bear Creek — **unconfirmed**).
- F7 → `data/raw/bvsd/pupil_count/`.
