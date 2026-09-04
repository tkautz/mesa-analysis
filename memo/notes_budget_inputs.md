# Notes: budget inputs (extracted 2026-09-04)

Outputs: `data/clean/budget_inputs_fy2027.csv` (103 cited items), `data/clean/site_budgets_mesa_bearcreek.csv` (3,064 CDE lines, four schools, FY2024-25), `data/clean/site_budgets_mesa_bearcreek_summary.csv` (tidy totals). Pages are `===== page N =====` indices of the `.txt` exports (FY27 book folio = N-2).

## Found
- **General Fund** (FY27 book p139/p171): FY27 proposed expenditures $386,231,155; FY26 estimated actual $382,553,239, revised $391,349,026, adopted $379,390,356. Revenue $440,114,931; beginning balance $65,648,539; resources $505,763,470 (computed sum). Res. 26-25 GF appropriation $506,613,945.
- **PPR** $11,890 (p31); funded pupil count 26,538.3 (p40, Uniform Budget Summary); heads 26,973.
- **Elementary formulas** (pp. 121-122): teachers 1:24.58; specials .0556 FTE/section; librarian 1.0 (>350) / 0.5; counselor 1.0 (350+) / 0.5 (200-350); paras .0326 hrs/student, FRL x1.5, .25 FTE per K section; SRA $65/pupil (+$125 FRL, $25 ELL, $25 SPED). BVEA C-6 class-size goals 26/29/31 (agreement p19).
- **Benefits** (p237): PERA 21.40% + Medicare 1.45% + LTD 0.16% = 23.01% of salary, plus $10,300/yr per eligible employee. Computed GF benefits/salaries 0.3187 (p171); elementary level 0.3380 (p167).
- **Counts**: 29 elementary schools (p94); elementary GF FTE 866.784, 484.062 teachers (p119); elementary level budget $107.46M (p167).
- **Budget-book site budgets** (GF, FY27): Bear Creek $3,688,335 / 30.511 FTE / 299 pupils; Mesa $3,024,735 / 25.343 / 217; Flatirons $2,330,098; Heatherwood $3,151,609 (pp. 94, 96, 99, 119, 167).
- **CDE files**: trial balances with a school-code column (0652, 5838; Flatirons 2970, Heatherwood 3882), amounts in cents. Fund-10 expenditures: Bear Creek $3.62M (FY24) / $3.98M (FY25); Mesa $3.37M / $3.52M; all funds $4.13M / $4.49M and $4.17M / $4.26M. District fund-10 sums match audited GF totals within 1-2%.

## Not found
- No printed average teacher salary; per-FTE loaded costs are flagged `derived`.
- The BVEA *revised 2026* salary table is not in the agreement text (MOU pp. 112-113 gives placement rules only). Only the *grandfathered* 2026-27 schedule exists on disk: BA $62,764-$73,368; MA $89,531-$109,139; top cell $127,458.

## Caveats
- The June 9 adoption item designates the Proposed Budget document as the adopted book; no separate adopted build. The CDE Uniform Budget Summary "General Fund" ($410.2M) folds sub-funds into Fund 10; not comparable to $386.2M.
- GF FTE prints as 2,792.131 (p120/p171) and 2,792.877 (p58).
- FY2025 xlsx is a "Working TB" (period-12 YTD), possibly pre-audit.
- Program/object labels come from the book's code lists (pp. 155-171, 260-261); sub-objects left at major class.
- `data/SOURCES.md` not modified (add-only rule); entry still needed.
