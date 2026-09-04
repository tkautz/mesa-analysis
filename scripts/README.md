# scripts/ — data preparation (no analysis)

Run from the repo root, in order:

1. `build_clean_enrollmentdata.py` — Step 2 clean tables from the vendored enrollmentdata.org CSVs.
2. `extract_map_embedded_data.py` — parse the JS data literals in `data/raw/enrollmentdata/maps/index.html`.
3. `compare_map_vs_csv.py` — cross-check the two October-count series inside the enrollmentdata repo.
4. `sort_manual_files.py`, `sort_manual_files_round3.py` — one-offs (already run): moved hand-downloaded `data/manual/` files into `data/raw/`; manifest at `data/raw/bvsd/MANIFEST.csv`.
5. `extract_pdf_text.py` — pdfplumber full text of every PDF under `data/raw/bvsd/` to a sibling `.txt`, plus `data/clean/pdf_page_index.csv`.
6. `ocr_page_renders.py` — rapidocr over the rendered image-only pages in `data/raw/bvsd/page_renders/` (renders made with pypdfium2 at scale 3). **OCR output; flagged.**
7. `reconstruct_capacity_tables_ocr.py` — regroup OCR tokens into table rows for the three capacity-summary pages (all schools; OCR-grade).
8. `parse_pupil_count.py` — Mesa / Bear Creek rows from the 36 pupil-count PDFs.
9. `parse_pupil_count_all_schools.py` — all elementary schools' funded head count, 12 years.
10. `parse_cde.py` — CDE membership rows for both schools and the CDE-vs-BVSD comparison.
11. `build_primary_tables.py` — the verified Mesa / Bear Creek tables from primary documents, `projections_by_vintage.csv`, `resident_vs_enrolled_mesa_bearcreek.csv`, `verification_headcount_sources.csv`.
12. `build_projections_by_vintage.py` — superseded by step 11 (kept for the record of the transcription-only version).

Added 2026-09-03/04 (session 6; web access from the local machine):

13. `fetch_bvsd_web_docs.py` — downloads bvsd.org files (Enrollment Pattern Matrices, School Profile books, weekly 2026-27 counts, LRAC and bond files, dated page copies) into `data/raw/bvsd/<subfolder>/`, never overwriting; sibling `.txt` for every PDF/HTML; manifest `data/raw/bvsd/MANIFEST_web_fetch.csv`.
14. `fetch_public_docs.py` (+ `build_raw_manifests.py`) — press, budget and policy documents into `data/raw/press/`, `data/raw/bvsd/budget/`, `data/raw/bvsd/policy/`; records in `data/raw/_fetch_records.jsonl`.
15. `parse_oe_matrices.py` — Bear Creek / Mesa rows and South Boulder area totals from the Enrollment Pattern Matrices 2017-18 … 2025-26 → `data/clean/oe_matrix_*.csv` (identity checks in the script). `render_matrix_pages.py` renders matrix pages for visual checks.
16. `parse_school_profiles.py` — ten-year OE profiles and program capacities for both schools from the School Profile books → `data/clean/school_profile_*.csv`.
17. `parse_weekly_2026_27.py` — the Student Enrollment Center's weekly 2026-27 counts → `data/clean/enrollment_2026-27_weekly_elementary.csv`.
18. `parse_district_projection_vs_headcount.py` — the district's "Compare Projection to Head Count" tables, ten Octobers → `data/clean/district_projection_vs_headcount_2015_2025.csv`.
19. `parse_bvsd_births_by_area.py` — the district's births-by-attendance-area tables → `data/clean/bvsd_births_by_attendance_area*.csv`.

Modeling belongs in `analysis/` (scripts 01–20; see `analysis/PLAN.md` and `memo/REPORT_REVISION_PLAN.md`).
