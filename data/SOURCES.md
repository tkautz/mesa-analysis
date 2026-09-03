# Sources

Two retrieval rounds on **2026-09-03**. Round 1 (remote session, egress-blocked) got only the enrollmentdata.org GitHub repo. Round 2: the repo owner downloaded BVSD documents in a browser and committed them to `data/manual/`; `scripts/sort_manual_files.py` moved them to `data/raw/bvsd/` (original filename → new path, md5, duplicates in `data/raw/bvsd/MANIFEST.csv`). Retrieval URLs for round 2 are the ones in the task brief and the bvsd.org pupil-count page; the browser session's exact URLs were not logged, so each entry below cites the document's own header instead. Every PDF has a sibling `.txt` (pdfplumber text layer); page-level index in `data/clean/pdf_page_index.csv`.

## Primary BVSD documents (data/raw/bvsd/)

| ID | File | What it is | Pages | Used for | Extraction |
|---|---|---|---|---|---|
| P1 | `resilient_schools_proposal_2026-08-25.pdf` | "Resilient Schools Proposal", Board of Education, Aug 25 2026 | 75 | Mesa/Bear Creek pages **49–51**; Boulder region pp. 43–45; summary p. 58; boundaries p. 59; other options p. 56 | text layer for pp. 49–51, 50; charts on pp. 44–45 read by eye (`aug2026_deck_p44.csv`) |
| P2 | `trend_report_feb2026.pdf` | "LRAC Update & Annual Enrollment Trend Report", Feb 10 2026 | 14 | **p. 9** "BVSD Capacity Summary 2025-26 (updated 1/26/2026)" — image only; p. 10 metrics; p. 2 process history | p. 9 via OCR + visual check (`feb2026_report_p9.csv`) |
| P3 | `trend_report_feb2025.pdf` | same report, Feb 11 2025 | 12 | **p. 9** "BVSD Capacity Summary 2024-25 (updated 1/24/2025)" — image only; p. 11 advisory list | OCR + visual check (`feb2025_report_p9.csv`) |
| P4 | `trend_report_feb2024.pdf` | same report, Feb 27 2024 | 16 | **p. 11** "BVSD Capacity Summary 2023-24 (updated 1/26/2024)" — image only; pp. 6–7 phase definitions; p. 13 advisory list | OCR + visual check (`feb2024_report_p11.csv`) |
| P5 | `worksession_2025-10-21.pdf` | "Long Range Planning Update", Board work session Oct 21 2025 | 47 | **slide 17** Boulder-region capacity/projection table (image); slide 8 programmatic impacts (text); slide 12 region membership; slides 19–20 composition charts; slide 14 metrics | slide 17 OCR + visual check (`oct2025_deck_s17.csv`); slide 8 text |
| P6 | `trend_report_exec_summary_2023-24.pdf`, `trend_report_exec_summary_2024-25.pdf` | Executive summaries of P4/P3 | 2 each | Advisory-phase school lists (Mesa listed both years) | text |
| P7 | `lrac_final_metrics_2023-06-13.pdf` | "LRAC Metrics and Recommendations", June 13 2023 | 4 | Origin of the 60%/2-round and 50%/1.5-round thresholds | text (words run together; readable) |
| P8 | `resilient_schools_faq.pdf` | bvsd.org FAQ page, printed | 10 | Open-enrollment priority framework for 2027-28 | text |
| P9 | `resilient_schools_special_needs.pdf` | bvsd.org page | 3 | context only | text |
| P10 | `bvsd_page_bear_creek_creekside.pdf` | bvsd.org "Adopted Boundary Changes for the Bear Creek Elementary and Creekside Elementary Dual Enrollment Area", printed 9/2/26 | 3 | **2026-27 boundary change**: dual area west of Broadway / north of Table Mesa becomes Bear Creek-only, adopted Sept 23 2025 | text |
| P11 | `bvsd_enrollment_dashboard.pdf` | BVSD Enrollment Dashboard landing pages | 5 | context; no school-level numbers | text |
| P12 | `news_bvsd_enrollment_drops_more_than_expected.pdf`, `news_bvsd_enrollment_drops_less_than_expected_2024.pdf` | BVSD news articles | 6, 8 | Advisory-list context | text |
| P13 | `pupil_count/*.pdf` (36 files) | BVSD October count: CDE head count, FTE, special programs, 2014-15 … 2025-26 | 1–2 each | **Official Mesa/Bear Creek head count, grades, FTE, out-of-district, FRL, SPED, ELL** | text (`parse_pupil_count.py`) |

Duplicates removed (byte-identical): second copies of P1's Oct 2025 deck, P3, P4, the 2024-25 exec summary, and two extra copies of P7 (see MANIFEST.csv).

## Secondary: enrollmentdata.org transcription (data/raw/enrollmentdata/)
- https://github.com/yoavlurie/bvsd-enrollment, commit `37a9bf9` (2026-08-27), CC0. Cloned 2026-09-03; `.git` removed. See round-1 notes in git history for its contents. Now used only as a cross-check (VERIFICATION.md §B) and for the attendance-area GeoJSON.

## Still not retrieved
| # | Document | URL | Why it matters |
|---|---|---|---|
| F4 | bvsd.org "Resilient Schools: Responding to declining enrollment" page (HTML + text) | https://www.bvsd.org/current-topics/declining-enrollment | Task brief item; threshold language and process links |
| F5 | CDE "PK-12 Membership Grade Level by School" XLSX, 2014-15 … 2024-25 | https://www.cde.state.co.us/cdereval/rvprioryearpmdata | Independent count; school codes; PK definition |
| F6 | CDE current-year (2025-26) pupil membership | https://cde.state.co.us/cdereval/pupilcurrent | same |
| F8 | BVSD 2020-21 FTE Summary | bvsd.org pupil-count page | completes the FTE series (minor) |
| F9 | 2025-26 Enrollment Trend Report Executive Summary (if published) | BoardDocs, Feb 10 2026 agenda | companion to P2 |
| F10 | Board materials for the 2026-27 attendance-boundary adoption (Sept 23 2025) and the March 11 / May 20 / Sept 9 2025 work sessions linked from P10 | BoardDocs ids DEAUVH7DE6AF, DF3M2M592725, DL5GY6460A53 (from P10) | open question 1 |
| F11 | Sept 8 2026 Board meeting materials on the proposal | BoardDocs | any revised numbers |
