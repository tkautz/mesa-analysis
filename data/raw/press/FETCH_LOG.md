# Fetch log — press, budget, policy and BVSD web documents (retrieved 2026-09-03)

All files were fetched with `scripts/fetch_public_docs.py` (requests, browser User-Agent
`Mozilla/5.0 (Windows NT 10.0; Win64; x64) ... Chrome/128.0 Safari/537.36`), except where noted.
Each HTML page has a sibling `.txt` (article/body text via BeautifulSoup); each PDF has a sibling `.txt`
(pdfplumber text layer, `===== page N =====` markers); each XLSX has a sibling `.txt` (sheet names + first 40 rows).
Per-folder `MANIFEST.csv` (file, url, publisher, title, date, retrieved_utc, md5, notes) built by
`scripts/build_raw_manifests.py` from `data/raw/_fetch_records.jsonl`.
No pre-existing repository file was modified.

## 1. Press coverage (data/raw/press/)

Search strategy: WebSearch (Anthropic) for BRL/Daily Camera/Boulder Weekly/CPR/Chalkbeat/Colorado Sun/
9News/KDVR/CBS/Denver7; BRL `tag/bvsd` and `category/education` listing pages and the BRL WordPress
search API to enumerate 2026 stories; DuckDuckGo HTML endpoint for dailycamera.com (Anthropic's crawler
is blocked from dailycamera.com and denverpost.com, so WebSearch could not be domain-restricted there).

Found and saved:

| Publisher | Date | File (html + txt) | Notes |
|---|---|---|---|
| Boulder Reporting Lab | 2026-08-20 | `brl_2026-08-20_emails_show_bvsd_preparing_for_closures` | district emails story (Jenna Sampson) |
| Boulder Reporting Lab | 2026-08-25 | `brl_2026-08-25_bvsd_proposes_closing_four_elementary_schools` | proposal story; "$3.5–4M annually", "as much as $10 million" facility modifications, Mesa/Bear Creek "up to 462 students in 2030" |
| Boulder Reporting Lab | 2026-06-09 | `brl_2026-06-09_parents_organize_to_save_their_schools` | South Boulder Advocacy / Mesa PTO (Sasha Schwartz); via WP REST API (site returned HTTP 429 to page requests) |
| Boulder Reporting Lab | 2026-04-26 | `brl_2026-04-26_inside_bvsds_final_meeting_on_possible_closures` | via WP REST API |
| Boulder Reporting Lab | 2026-03-22 | `brl_2026-03-22_a_school_consolidation_once_divided_boulder` | 2000 South Boulder consolidation history; via WP REST API |
| Boulder Reporting Lab | 2026-03-10 | `brl_2026-03-10_too_many_schools_too_few_students` | via WP REST API |
| BRL newsletter | 2026-08 | `brl_newsletter_2026-08_bvsd_names_the_4_elementary_schools` | (+ `_DATE.txt` sidecar if the API date was captured) |
| Daily Camera (Amy Bounds) | 2026-08-25 | `dailycamera_2026-08-25_boulder_valley_school_district_closures` | full text visible (not paywalled at fetch time) |
| Daily Camera | 2026-08-24 | `dailycamera_2026-08-24_school_board_school_closures_plan` | full text |
| Daily Camera | 2026-06-10 | `dailycamera_2026-06-10_consolidation_declining_enrollment` | full text |
| Daily Camera | 2026-02-11 | `dailycamera_2026-02-11_enrollment_trends_small_schools` | full text |
| Daily Camera | 2026-01-28 | `dailycamera_2026-01-28_declining_enrollment_timeline` | **paywalled**: only the lede is visible ("This article is only available to subscribers") |
| Daily Camera | 2025-12-10 | `dailycamera_2025-12-10_enrollment_declines` | **paywalled**: lede only |
| Daily Camera | 2025-01-14 | `dailycamera_2025-01-14_attendance_boundary_review_strategies` | boundary review; full text |
| Boulder Weekly (Mei Gifford) | 2026-08-28 | `boulderweekly_2026_bvsd_discusses_consolidation_and_closure_options` | |
| Denver7 | 2026-08 | `denver7_2026-08_bvsd_proposes_six_school_closures` | |
| CBS Colorado | 2026-08 | `cbs_colorado_2026-08_bvsd_proposes_closing_schools` | short |
| The Mountain-Ear | 2026-09-03 | `mountain_ear_2026_bvsd_proposes_consolidations_and_closures` | |
| savedouglass.com | 2026-09-03 | `savedouglass_com_home_2026-09-03`, `savedouglass_com_https_savedouglass_com_es_2026-09-03` | advocacy site (English + Spanish); "$494M budget", "$12.5–$15M one-time", "$3.5 to 4M a year" |
| mesapto.com | 2026-09-03 | `mesapto_com_home_2026-09-03` | Mesa PTO site; links "BVSD School Closures" |
| change.org | 2016-10-18 | `changeorg_petition_keep_mesa_elementary_integrated` | **old** (2016) petition about moving the ICAN program out of Mesa; not about the 2026 proposal — kept for context only |

Not found / not obtained:
- **Chalkbeat Colorado, Colorado Public Radio, Colorado Sun**: no story on the BVSD Resilient Schools proposal found by search (searches restricted to those domains returned only unrelated items — school ratings, weather closures, DPS closures).
- **9News** (two stories: "Boulder Valley Schools weighs consolidation, closures as enrollment declines continue"; "BVSD announces possible elementary school consolidation") and **KDVR/FOX31** ("BVSD lays out plans for school consolidation"): HTTP 403 to both curl and WebFetch; no Wayback snapshot. URLs recorded here:
  - https://www.9news.com/article/news/education/boulder-valley-schools-consolidation-closures-meeting/73-af9d9300-50b0-480a-a981-d9165dff96f9
  - https://www.9news.com/article/news/education/boulder-valley-school-district-possible-elementary-school-consolidation/73-390187db-7848-4c72-b007-476f6494cca3
  - https://kdvr.com/news/local/boulder-valley-school-district-lays-out-plans-for-school-consolidation/
- **Daily Camera paywalled stories (2026-01-28, 2025-12-10)**: Wayback snapshots exist (20260316130646, 20251220201912) but web.archive.org returned HTTP 429 on every attempt; retry later.
- **BRL newsletter "Some BVSD schools may close. Here's what we know."** (post id 110888): HTTP 429 from both the page and the WP REST API at every attempt.
- No **Save Mesa** website found; the community effort is "South Boulder Advocacy" (Mesa PTO president Sasha Schwartz) as described in BRL 2026-06-09; the Bear Creek PTO page (`data/raw/bvsd/web/bear_creek_pto_page_2026-09-03`) has no statement on the proposal.
- No press item mentioning a **Sept. 8 agenda posting**; the BoardDocs public meetings list (checked 2026-09-03) has no Sept. 8 or Sept. 22 meeting yet (latest posted: Aug. 25).

## 2. BVSD budget documents (data/raw/bvsd/budget/)

The budget page (`bvsd_financial_transparency_budget_page_2026-09-03.html`) lists documents as Finalsite
resource-manager links (`/fs/resource-manager/view/<uuid>`), which WebFetch stripped; links were parsed from the raw HTML.

| File | What it is | Source |
|---|---|---|
| `bvsd_2026-27_proposed_budget.pdf` (266 pp., 7.7 MB) | 2026-27 Proposed Budget book (the book the Board adopted June 9, 2026; BVSD posts no separate "adopted" book until the January revision) | BoardDocs DUFK9H50C728 |
| `bvsd_2026-27_uniform_budget_summary.pdf` | FY2026-27 Uniform Budget Summary (CDE form; "Adopted: June 09, 2026"; budgeted pupil count 26,538.3) | bvsd.org resource baf89f7c… |
| `bvsd_2025-26_adopted_budget_june.pdf` (8.3 MB) | 2025-26 Adopted Budget (June 2025) | bvsd.org resource 3672fd26… |
| `bvsd_2025-26_uniform_budget_summary.pdf` | FY2025-26 Uniform Budget Summary | bvsd.org resource 8c684680… |
| `bvsd_2025-26_revised_budget_book.pdf` (12.1 MB) | 2025-26 Revised Budget (Jan 2026) | resources.finalsite.net |
| `bvsd_2024-25_adopted_budget_june.pdf` | 2024-25 Adopted Budget | resources.finalsite.net |
| `cde_financial_transparency_0480_FY2025_website_view.xlsx`, `..._FY2024_...` | CDE Financial Transparency "website view" account-level actuals (district 0480; includes school location codes) — the only school-level expenditure data BVSD posts | financial-data-files page |
| `boarddocs_agenda_2026-06-09_regular_meeting.html`, `boarddocs_item_2026-06-09_adoption_of_2026-27_budget_DUHS2L709640.html` | June 9, 2026 agenda and item 8.8 "Resolutions 26-19, -20, -21, -25 Adoption of the 2026-27 Budget" (consent; passed 6-0) | BoardDocs API |

Not obtained: the four resolution PDFs attached to item DUHS2L709640 (BoardDocs loads attachments through a
JavaScript call that is not exposed by the public API endpoints tried). There is no separate "school-level
budget" document; the staffing allocation formulas are the "School Allocation Formulas" section of the budget
book (2026-27 Proposed Budget printed pp. 119–123 = PDF pp. 121–125). No average-teacher-salary figure is
printed in the budget books; the 2026-27 salary schedule is in `data/raw/bvsd/policy/`.

## 3. Board policies (data/raw/bvsd/policy/)

BVSD does not use the CASB numbers JFBA / JFBA-R; its open-enrollment policy is **JECC "School Assignment and
School Choice"** (adopted 1991, revised 2024-02-27) and **JECC-R "School Choice Procedure (Open Enrollment)"**
(revised through 2024-10-24). Saved from the Section J list
(`data/raw/bvsd/web/bvsd_policies_section_j_list_2026-09-03.html`): JC (School Attendance Areas), JEC (School
Admissions), JEC-R-E1, JECBA, JECC, JECC-R, JECD, JECD-R, JECD-R-E, JECE, JFABD, JFABD-R, JFABE, JFABE-R.
Also here: BVEA negotiated agreements 2024-2026 and **2026-2029** (effective Aug 1 2026–Jul 31 2029; class size
in section C-6, classload in C-5.10), BVEA 2021 tentative-agreement summary, and the 2026-27 BVEA salary schedule.

## 4. BVSD web pages (data/raw/bvsd/web/)

Open Enrollment page, Choice Enrollment page and FAQ, Resilient Schools Transportation FAQ, Resilient Schools
Proposal FAQ, Resilient Schools landing page, Supporting Data page, three BVSD news posts (Aug 25 letter
"Resilient Schools Proposal"; "Developing the proposal"; "Proposal presented to Board August 25"; Dec 2025
"Latest enrollment data confirms need for holistic action"), the HR negotiated-agreements page, the budget and
financial-data-files pages, the Section J policy list, the Bear Creek PTO page, and the Tableau workbook
metadata (`tableau_bvsd_enrollment_dashboard_workbook_metadata_2026-09-03.json/.txt`).

## 5. Tableau "BVSD Enrollment Dashboard"

Tableau Public profile API: `allowDataAccess = false` (viewer "Download > Data / Crosstab" disabled);
`.twb/.twbx` download returns 404; the embed page is now a JS/AWS-WAF-gated shell, so the bootstrapSession
scraping route (TableauScraper) fails. Views: Welcome/Bienvenidos; Annual Trends; Enrollment Patterns;
Enrollment Gains/Losses; Home School/Private School. Last published 2026-02-26. **Manual export (screenshots
or "View Data" if the district enables it) is required** for resident vs open-enrolled by school.

## Concurrent session note
While this fetch ran (2026-09-03 ~20:20–20:50 MT) another session was writing into the same repo
(`scripts/fetch_bvsd_web_docs.py`, manifest `data/raw/bvsd/MANIFEST_web_fetch.csv`; folders
`data/raw/bvsd/{boarddocs,bond,lrac,oe_matrices,school_profiles,enrollment_2026-27_weekly}`, `data/raw/demography/`,
`data/clean/oe_matrix_*`, and edits to `data/CONFLICTS.md`, `data/SOURCES.md`, `data/VERIFICATION.md`).
Its files in `data/raw/bvsd/web/` (`comms_*`, `news_*`, `page_*`) are **not** listed in the `MANIFEST.csv` files
built here, which cover only the files in `data/raw/_fetch_records.jsonl`. Three of its pages duplicate pages
saved here under different names (`page_declining_enrollment`, `page_faq`, `page_supporting_data`
≈ `bvsd_declining_enrollment_page`, `bvsd_resilient_schools_proposal_faq`, `bvsd_resilient_schools_proposal_supporting_data`).

## Confirmed URL for an existing repo document
`data/raw/bvsd/resilient_schools_proposal_2026-08-25.pdf` is byte-identical (md5 0368dfeef0675456a386de5d6378881f)
to https://go.boarddocs.com/co/bvsd/Board.nsf/pfiles/DXBFUX40E0C7/$file/Resilient%20Schools%20Proposal%20FINAL%2008-25-2026%20(1).pdf
(linked from the BVSD "Supporting Data" page).
