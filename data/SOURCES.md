# Sources

Three retrieval rounds on **2026-09-03**. Round 1 (remote session, egress-blocked) got only the enrollmentdata.org GitHub repo. Rounds 2–3: the repo owner downloaded BVSD and CDE documents in a browser and committed them to `data/manual/`; `scripts/sort_manual_files.py` and `scripts/sort_manual_files_round3.py` moved them to `data/raw/bvsd/` and `data/raw/cde/` (original filename → new path, md5, duplicates in `data/raw/bvsd/MANIFEST.csv`). Retrieval URLs for round 2 are the ones in the task brief and the bvsd.org pupil-count page; the browser session's exact URLs were not logged, so each entry below cites the document's own header instead. Every PDF has a sibling `.txt` (pdfplumber text layer); page-level index in `data/clean/pdf_page_index.csv`.

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
| P14 | `boundary_study_item_2025-09-09.pdf` | "BOE Attendance Boundary Study Item", Sept 9 2025 (30 pp.) | 30 | **pp. 22–25**: Dual Bear Creek/Creekside → Bear Creek: 37 elementary students in the dual area, 23 (62%) already at Bear Creek, 7 (19%) at Creekside; grade breakout; family feedback; options | text |
| P15 | `boundary_worksession_2025-03-11.pdf` | "BOE Attendance Boundary Worksession", Mar 11 2025 | 20 | p. 5 region capacity/resident/enrolled; pp. 17–19 South Boulder composition and options (A: BC/Creekside dual → Bear Creek, 37 students) | text |
| P16 | `bvsd_page_declining_enrollment.pdf` | bvsd.org "Resilient Schools: Responding to declining enrollment", printed 9/2/26 (the task-brief F4 page, as PDF rather than HTML) | 23 | pp. 6–7 Mesa/Bear Creek rationale text | text |
| P13 | `pupil_count/*.pdf` (36 files) | BVSD October count: CDE head count, FTE, special programs, 2014-15 … 2025-26 | 1–2 each | **Official Mesa/Bear Creek head count, grades, FTE, out-of-district, FRL, SPED, ELL** | text (`parse_pupil_count.py`) |

Duplicates removed (byte-identical): second copies of P1's Oct 2025 deck, P3, P4, the 2024-25 exec summary, and two extra copies of P7 (see MANIFEST.csv).

## Primary CDE documents (data/raw/cde/)
| ID | File | What it is | Used for | Extraction |
|---|---|---|---|---|
| C1 | `2019-20 … 2024-25_membership_grade_by_school.xlsx` (6 files) | CDE "Pupil Membership by School and Grade", statewide, one sheet | Boulder Valley Re 2 (0480), school codes **0652 Bear Creek Elementary School**, **5838 Mesa Elementary School** (codes confirmed against the School Name column in every file); PK, half/full-day K, grades 1–5, PK-12 total | openpyxl (`scripts/parse_cde.py`) |
| C2 | `2025-26_pupil_membership_school_level.xlsx` | CDE "Student October 2025-26: School Level PK-12th Grade Pupil Membership" (sheets: PK12_MembershipTrends, Grade, Grade_RaceEthnicityGender, FRL_*, IPST) | same rows; FRL cells for both schools are suppressed ("*") | openpyxl |
Not available from CDE in these files: resident vs non-resident / open-enrollment status by school. 2014-15 … 2018-19 CDE files were not in the batch (BVSD's own files cover those years).

## Secondary: enrollmentdata.org transcription (data/raw/enrollmentdata/)
- https://github.com/yoavlurie/bvsd-enrollment, commit `37a9bf9` (2026-08-27), CC0. Cloned 2026-09-03; `.git` removed. See round-1 notes in git history for its contents. Now used only as a cross-check (VERIFICATION.md §B) and for the attendance-area GeoJSON.

## Literature and secondary sources cited in the appendix (NOT in the repository — verify before sending)
| ID | Item | Status | Action |
|---|---|---|---|
| L1 | Francis A. Pearman II, "The Fiscal Consequences of School Closures in California: Evidence from a Statewide Synthetic Difference-in-Differences Design," Stanford SCALE, May 2026. Figures used (as supplied by the repo owner, not read from the PDF): ~800 districts, 2011–2019; closures cut spending ~$447 per student and revenue ~$433 per student as families left; no significant improvement in the probability of a balanced budget; no significant reduction in teachers, principals or total staff. | **PDF not in repo; figures unverified** | Place the PDF in `data/raw/literature/` and check each figure against its tables before the email is sent. |
| L2 | Boulder Reporting Lab, Aug. 20, 2026 story on district emails (reported to quote the superintendent's concern about a charter or other operator occupying a vacated building) and its "up to $10M one-time" figure. | **Not in repo; not quoted in the appendix beyond "reported"** | Save the article to `data/raw/press/` and quote it directly, or drop the reference. |
| L3 | savedouglass.com "$12.5–15M one-time against a ~$494M budget" | Not in repo | The $12.5–15M is reproducible from deck p. 60 (CONFLICTS C11); the $494M denominator is not in any document here and must be sourced from BVSD's FY27 adopted budget. |
| L4 | BVSD news article, "Enrollment drops more than expected, Board expresses desire to take action to respond," Susan Cousins, Dec. 12, 2025 (`data/raw/bvsd/news_bvsd_enrollment_drops_more_than_expected.pdf`, p. 1) | **In repo** | Source for: births "leveling after a steep decline until 2019"; kindergarten "higher than projected"; "for the second year in a row, the rate of new kindergarteners showing up was 93% of the number of births five years prior"; district count down 525 (1.9%), "1% more than projected". |

## Still not retrieved
| # | Document | URL | Why it matters |
|---|---|---|---|
| F5a | CDE "Pupil Membership by School and Grade" XLSX for **2014-15 … 2018-19** (2019-20 onward received) | https://www.cde.state.co.us/cdereval/rvprioryearpmdata | completes the CDE series (low priority; BVSD files cover these years) |
| F8 | BVSD 2020-21 FTE Summary | bvsd.org pupil-count page | completes the FTE series (minor) |
| F9 | 2025-26 Enrollment Trend Report Executive Summary (if published) | BoardDocs, Feb 10 2026 agenda | companion to P2 |
| F10 | May 20 2025 boundary work session and the Sept 23 2025 adoption item (Mar 11 and Sept 9 received as P15/P14) | BoardDocs id DF3M2M592725 (from P10); Sept 23 2025 agenda | open question 1 (minor now) |
| F12 | **Older Annual Enrollment Trend Reports (Feb 2023, Feb 2022) and any pre-LRAC 5-year projection tables (2016–2021)** | BoardDocs | extends the projection-vintage record from 3 to 5+ vintages, which is what the accuracy analysis needs most |
| F13 | Colorado State Demography Office county/school-age population projections (Boulder County) | https://demography.dola.colorado.gov/ | independent, published-with-uncertainty comparison |
| F11 | Sept 8 2026 Board meeting materials on the proposal | BoardDocs | any revised numbers |
