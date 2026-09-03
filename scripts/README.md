# scripts/ — data preparation (no analysis)

Run from the repo root, in order:

1. `build_clean_enrollmentdata.py` — Step 2 clean tables from the vendored enrollmentdata.org CSVs.
2. `extract_map_embedded_data.py` — parse the JS data literals in `data/raw/enrollmentdata/maps/index.html`.
3. `compare_map_vs_csv.py` — cross-check the two October-count series inside the enrollmentdata repo.
4. `sort_manual_files.py` — one-off: moved the hand-downloaded `data/manual/` files into `data/raw/bvsd/` (already run; manifest at `data/raw/bvsd/MANIFEST.csv`).
5. `extract_pdf_text.py` — pdfplumber full text of every PDF under `data/raw/bvsd/` to a sibling `.txt`, plus `data/clean/pdf_page_index.csv`.
6. `ocr_page_renders.py` — rapidocr over the rendered image-only pages in `data/raw/bvsd/page_renders/` (renders made with pypdfium2 at scale 3). **OCR output; flagged.**
7. `reconstruct_capacity_tables_ocr.py` — regroup OCR tokens into table rows for the three capacity-summary pages (all schools; OCR-grade).
8. `parse_pupil_count.py` — Mesa / Bear Creek rows from the 36 pupil-count PDFs.
9. `build_primary_tables.py` — the verified Mesa / Bear Creek tables from primary documents, `projections_by_vintage.csv`, `resident_vs_enrolled_mesa_bearcreek.csv`, `verification_headcount_sources.csv`.
10. `build_projections_by_vintage.py` — superseded by step 9 (kept for the record of the transcription-only version).

Modeling belongs in `analysis/` (session 2).
