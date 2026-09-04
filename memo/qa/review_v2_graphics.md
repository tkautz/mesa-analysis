# Graphics review v2: figures 15–21

Scope: `figures/fig15–fig21` as included in `report/report.tex` (24 pp.; target ~22), scripts `analysis/12, 14, 15, 16, 18, 20`, style in `analysis/common.py`. Read-only; nothing changed.

## 1. Systemic: every figure prints smaller than authored

Scripts author at `PAGE_W = 6.5 in`, but each title is one unwrapped line wider than the canvas; `save()` uses `bbox_inches="tight"`, so the PNG grows to the title's width and LaTeX scales the image back to `\textwidth`.

| fig | PNG width (in) | print scale | smallest text, authored → printed |
|---|---|---|---|
| 15 | 9.79 | 0.66 | row labels 6.6 → 4.4 pt |
| 16 | 9.79 | 0.66 | x labels 6.2 → 4.1 pt |
| 17 | 8.39 | 0.77 | legend 6.3 → 4.9 pt |
| 18 | 9.84 | 0.66 | legend 6.3 → 4.2 pt |
| 19 | 8.20 | 0.79 | legend 6.0 → 4.7 pt |
| 20 | 6.94 | 0.94 | legend 6.2 → 5.8 pt |
| 21 | 9.38 | 0.69 | x ticks 7.0 → 4.8 pt |

Fix once in `common.py`: a `title()` helper that wraps with `textwrap.fill(text, 88)`, and in `save()` a check that `fig.get_tightbbox(renderer).width <= PAGE_W + 0.15` with a warning. Re-run the six scripts.

## 2. Correctness: stale hard-coded titles

- **Fig 16** suptitle says "514 in 2027-28"; `table14_bridge.csv` gives 512.2, the bar reads 512, the caption says 512.
- **Fig 19** left title "Births fell to 30 in 2019": `table18_births_k.csv` gives 33 (the body text says 33). Right title "1.1–1.6 through 2022, 2.8 in 2024": CSV max through 2022 is 1.53, 2024 is 2.55 (body: "1.1 to 1.5 … 2.5"). Compute all three from the data.

Other spot-checks pass: fig 17 (80.6/87.3%; needed 54.0/65.3%), fig 18 (733, 502, 2020-21 = 592, deck 522), fig 20 (330 vs 299; 204 vs 217), fig 21 (Bear Creek 2018 +8.0, 2024 −6.9; Mesa 2022 +7.3), fig 15 (2027 trend/formula 23 (20–24) 73%; 2030 level/formula 23 (20–27) 79%; 2030 trend/BVEA 18 (15–21) 5%).

## 3. Figure by figure

**Fig 16 bridge.** Title factual after the 512 fix; chart shows it. All six two-line x labels collide; "capacity 492" sits on the 473/522 labels and the −82/−90 steps; "proposal's range" overprints the 553 bar. `ROLE["merged"]` colours both the "+ in-district choice" component and the total (two meanings); use the light violets for the three components. Footer complete. Improvement: one-word x labels ("residents", "× 83%", "+ choice", "+ out-of-district", "+ placements", "total") at 7 pt; "capacity 492" at `x = 5.4, ha="right"`; range label centred at `x = 3.5`, where the band is empty in both panels.

**Fig 17 capture history.** Title factual and shown; the cleanest of the seven. Palette fine. Footer: add the matrix date (12/5/2025). Improvement: add a dotted-outline rectangle 57–69% for the 2027-28 requirement (`capture_needed_*`, fall 2027) and label the grey line's last point "74%".

**Fig 18 residents.** Title factual. The legend covers the 2020–2023 bars and their totals; the red "503" overprints "502". Palette fine. Footer complete. Improvement: `legend(loc="lower right")` (2026–2031 below 445 is empty); drop the "503" text.

**Fig 19 births/kindergarten.** Suptitle factual once the panel numbers are fixed. Panel titles collide mid-figure; the left legend hides the 2009–2010 K points; right ticks read 2017.5, 2022.5. Footer cites a repo path; say "Board enrollment packets 2015–2025". Improvement: drop the panel titles, `fig.legend(loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.06))`, `axes[1].set_xticks(range(2014, 2026, 2))`.

**Fig 20 Aug 2026.** Title factual and shown. Fractional-year ticks on both panels; the legend overprints the Jan 2025 run's 2027–2029 points; "+31" collides with the 2025 marker. The red star gives `proposal` red a second meaning (an observed count); use the school colour with a black edge. `sharey=False` makes −13 look as large as +31; say so in the caption. Improvement: `set_xticks(range(2018, 2031, 2))`; `legend(loc="upper right")`; "+31/−13" at `x = 2026.2, ha="left"`.

**Fig 21 district record.** Title describes rather than states. Oct 2020 is absent with no gap. Palette consistent. Footer: add "projections dated Feb–May (Jan for 2025)". Improvement: title "The district's spring projections miss the October count by 3% at the median and 8% one year in ten; Bear Creek and Mesa sit inside the pack" (`table20_accuracy_summary.csv`); plot at `x = year` with an empty labelled 2020 slot.

**Fig 15 sections.** Title describes rather than states; the 18-room line is drawn but only "over 21 rooms" is reported. Trend violet / level aqua per `ROLE`; violet also means "merged total" in figs 16, 17, 19, a convention `common.py` accepts. Footer complete. Improvement: title "At the staffing formula the merged school needs 21–23 sections for 21 rooms (over in 35–85% of paths); at the agreement's goals 18–21"; append "; over 18: {p:.0%}" from the `rooms == 18` rows; year as group header, rows "trend, formula 24.58".

## 4. Placement (24 pp. → ~22)

Body (sections 1–6, pp. 3–11): keep **fig 16** (the argument), **fig 20** (the new fact), **fig 15** (the operating constraint). Move **fig 17** to Appendix D beside fig 18, ideally as one two-panel figure (residents left, capture right); §1 already states its sentence. Move **fig 19** to Appendix E beside fig 10; §4 keeps fig 05b. **Figs 18 and 21** stay in the appendix. Saves about 1.5 body pages and 0.5 appendix page.

## 5. Fixes, ranked

1. Wrap titles and guard canvas width in `common.py`; re-run (all seven).
2. Fig 19 panel titles: 33, 1.5, 2.5 from the data.
3. Fig 16 title: 512 from the data.
4. Fig 18 legend to lower right; drop "503".
5. Fig 19: panel titles off, figure legend below, integer ticks.
6. Fig 16 x labels, capacity and range label positions, component colours.
7. Fig 20 integer ticks, legend upper right, star in school colour.
8. Move figs 17 and 19 to the appendices; merge 17 with 18.
9. Figs 15 and 21 takeaway titles; fig 15 "over 18 rooms"; fig 21 2020 gap.
