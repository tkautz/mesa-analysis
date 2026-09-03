# scripts/ — data preparation (no analysis)

Run from the repo root, in order:

1. `python3 scripts/build_clean_enrollmentdata.py` — Step 2 clean tables from the vendored enrollmentdata.org CSVs.
2. `python3 scripts/extract_map_embedded_data.py` — parse the JS data literals in `data/raw/enrollmentdata/maps/index.html`.
3. `python3 scripts/compare_map_vs_csv.py` — cross-check the two October-count series inside the enrollmentdata repo.
4. `python3 scripts/build_projections_by_vintage.py` — `data/clean/projections_by_vintage.csv`.

Modeling belongs in `analysis/` (session 2). Nothing here reads a primary BVSD or CDE document, because none could be downloaded from this session (see `data/SOURCES.md`).
