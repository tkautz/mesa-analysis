# AGENTS.md — mesa-analysis

Evidence base for a memo to the BVSD Board on the proposed Mesa Elementary / Bear Creek Elementary consolidation (vote Sept 22, 2026; effective 2027-28 if approved). The current task is a **rewrite of `report/report.tex`** for a school-board audience; the analysis is finished. **Start with `memo/HANDOFF_codex.md`**, which explains the goal, the findings with their sources, the repository layout, the rules, and why the current draft reads badly. `CLAUDE.md` carries the same ground rules and the key facts.

## Ground rules
- Every figure in any deliverable must cite a source file under `data/raw/` and a page or row, or an output in `analysis/output/` or `data/clean/`. No numbers from memory.
- Files under `data/raw/` are read-only originals. Derived tables go in `data/clean/`, analysis in `analysis/`, figures in `figures/`.
- Log every new source in `data/SOURCES.md`; record disagreements between sources in `data/CONFLICTS.md`; do not silently pick one.
- Distinguish district projections from actuals, and scenario probabilities from forecasts, in every table and sentence.
- Do not edit `memo/board-email*.md` or `memo/public-comment-sept8.md` (the author writes those).
- Python 3, pandas, matplotlib; scripts run from the repository root. Build the report with `pdflatex` (MiKTeX is installed) via `report/build.sh` or two passes of `pdflatex -interaction=nonstopmode report.tex` in `report/`.
- Commit when a piece of work is complete, with a message that says what changed.
