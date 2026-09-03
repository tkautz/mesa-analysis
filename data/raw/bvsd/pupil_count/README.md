# BVSD October pupil count files (hand-downloaded 2026-09-03 from bvsd.org "Enrollment Statistics: Pupil Count")

Three file families per school year, 2014-15 … 2025-26 (original filenames in ../MANIFEST.csv):
- `*_cde_headcount_summary.pdf` — "Summary of Colorado Department of Education - Funded Head Count", school x grade, with prior-year column. PRE-K column present 2014-15 … 2022-23 (always 0 for Mesa and Bear Creek); absent from 2023-24.
- `*_fte_summary.pdf` — funded FTE by grade (same layout).
- `*_special_programs_summary.pdf` — ELL, Free/Reduced lunch, SPED, 504, TAG, **Out of District**, gender, race/ethnicity by school.
Count date is the first school day of October (printed in the header, e.g. "October 5, 2016"); files were re-issued after CDE audit ("Updated: 01/22/2026").

Gaps: no 2020-21 FTE summary was supplied. `2020-21_special_programs_summary_v3.pdf` is actually an FTE summary (its header says "FUNDED FTE COUNT", updated 12/02/2019) — it is kept under the name it was downloaded with; `2020-21_special_programs_summary_v2_1.pdf` is the real special-programs file.

Parsed by `scripts/parse_pupil_count.py` → `data/clean/bvsd_pupil_count_mesa_bearcreek.csv`. Text layer is machine-readable (no OCR).
