"""§6 Accounting grid. Merged enrollment at Bear Creek written as the identity
    enrollment = combined-area residents x resident capture rate + choice seats (in-district open-enrolled + out-of-district),
evaluated on the district's own resident projections (deck p. 51: 473 in 2027-28, 522 in 2030-31) for a grid of capture rates and
choice-seat counts. No behavioural model: the grid says which combinations reproduce the proposal's range (392-445 / 403-462) and which
exceed the building (492). Today's rates come from deck pp. 44 and 51 and the 2025-26 special-programs summary (data/clean/resident_vs_enrolled_mesa_bearcreek.csv).
A second table borrows the relative dispersion of the independent model's combined-school paths to attach a chance of exceeding 492 to each cell.
Outputs: analysis/output/table11_accounting_grid.csv, table11_breakeven.csv, figures/fig14_accounting_grid.*"""
import sys; sys.path.insert(0, "analysis")
from common import *
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm
from matplotlib.patches import Rectangle
style()

rv = pd.read_csv(CLEAN / "resident_vs_enrolled_mesa_bearcreek.csv")
def val(school, m): return float(rv[(rv.school == school) & (rv.measure == m)].value.iloc[0])
RES_TODAY = val("Mesa", "resident_students_in_attendance_area") + val("Bear Creek", "resident_students_in_attendance_area")      # 503
ATT_TODAY = val("Mesa", "residents_attending_this_school") + val("Bear Creek", "residents_attending_this_school")                # 373
OE_IN = val("Mesa", "in_district_open_enrolled_in (derived)") + val("Bear Creek", "in_district_open_enrolled_in (derived)")       # 140
OOD = val("Mesa", "out_of_district_enrolled") + val("Bear Creek", "out_of_district_enrolled")                                     # 23
SEATS_TODAY = OE_IN + OOD; CAP_TODAY = ATT_TODAY / RES_TODAY
RESIDENTS = {2027: 473.0, 2030: 522.0}                     # deck p. 51
RANGE = {2027: (392, 445), 2030: (403, 462)}               # deck p. 51
print(f"today: residents {RES_TODAY:.0f}, attending {ATT_TODAY:.0f}, capture {CAP_TODAY:.1%}, choice seats {SEATS_TODAY:.0f} ({OE_IN:.0f} in-district + {OOD:.0f} out-of-district)")

captures = [0.55, 0.60, 0.65, 0.70, CAP_TODAY, 0.80, 0.85, 0.90]
seats = [0, 25, 50, 75, 100, 125, int(SEATS_TODAY)]
# relative dispersion borrowed from the independent model (combined school, 100% following, by spec)
P = np.load(OUT / "paths_modelA.npz"); falls = list(P["falls"])
ratio = {}
for spec, (a, b) in {"trend": ("bear_creek", "mesa"), "level": ("bear_creek_level", "mesa_level")}.items():
    for fall in RESIDENTS:
        E = P[a][:, falls.index(fall)] + P[b][:, falls.index(fall)]; ratio[(spec, fall)] = E / np.median(E)
rows = []
for fall, R in RESIDENTS.items():
    lo, hi = RANGE[fall]
    for c in captures:
        for s in seats:
            E = R * c + s
            row = dict(fall=fall, residents=R, capture=c, choice_seats=s, enrollment=E, in_district_range=(lo <= E <= hi), above_492=E > 492,
                       is_today_rates=(c == CAP_TODAY and s == int(SEATS_TODAY)))
            for spec in ("trend", "level"): row[f"p_over_492_{spec}"] = (E * ratio[(spec, fall)] > 492).mean()
            rows.append(row)
grid = pd.DataFrame(rows); grid.to_csv(OUT / "table11_accounting_grid.csv", index=False)

# break-even table: what one lever must do if the other stays at today's value
be = []
for fall, R in RESIDENTS.items():
    lo, hi = RANGE[fall]
    for target, lab in [(lo, "bottom of proposal range"), (hi, "top of proposal range"), (492, "building capacity")]:
        be.append(dict(fall=fall, target=target, target_label=lab, enrollment_at_today_rates=R * CAP_TODAY + SEATS_TODAY,
                       capture_needed_if_seats_today=(target - SEATS_TODAY) / R, seats_needed_if_capture_today=target - R * CAP_TODAY))
be = pd.DataFrame(be); be.to_csv(OUT / "table11_breakeven.csv", index=False); print(be.round(3).to_string(index=False))

# cross-flow sensitivity: x of the 140 derived "open-enrolled in" students may live inside the combined area (Mesa-area residents at
# Bear Creek or vice versa); after the merger they are residents, not external choice seats. Combined-area capture = (373 + x)/503,
# external seats = 163 - x. Which conclusions are invariant to x is the point of this table.
cf = []
for x in (0, 20, 40, 60, 80, 100):
    cap = (ATT_TODAY + x) / RES_TODAY; ext = SEATS_TODAY - x
    for fall, R in RESIDENTS.items():
        lo, hi = RANGE[fall]
        cf.append(dict(crossflow_x=x, combined_area_capture=cap, external_seats=ext, fall=fall, enrollment_today_pattern=R * cap + ext,
                       capture_needed_lo=(lo - ext) / R, capture_needed_hi=(hi - ext) / R, capture_gap_vs_today=cap - (hi - ext) / R,
                       seats_needed_hi=hi - R * cap, cut_needed_hi=ext - (hi - R * cap), cut_share_of_external=(ext - (hi - R * cap)) / ext))
cf = pd.DataFrame(cf); cf.to_csv(OUT / "table11_crossflow_sensitivity.csv", index=False); print(cf[cf.fall == 2030].round(3).to_string(index=False))

# ---- Fig 14: two panels (2027-28, 2030-31), cells = enrollment; one violet sequential ramp; proposal-range cells outlined in red ----
cmap = LinearSegmentedColormap.from_list("violet_seq", ["#f4f2fb", "#c9c2ec", "#8f82d2", ROLE["merged"], "#2a2160"])
bounds = [300, 350, 403, 450, 492, 550, 620]; norm = BoundaryNorm(bounds, cmap.N)
fig, axes = plt.subplots(1, 2, figsize=(PAGE_W, 3.55), sharey=True)
for ax, fall in zip(axes, RESIDENTS):
    g = grid[grid.fall == fall].pivot(index="capture", columns="choice_seats", values="enrollment").loc[captures, seats]
    im = ax.imshow(g.values, cmap=cmap, norm=norm, aspect="auto", origin="lower")
    lo, hi = RANGE[fall]
    for i, c in enumerate(captures):
        for k, s in enumerate(seats):
            E = g.iloc[i, k]; dark = E >= 450
            ax.text(k, i, f"{E:.0f}", ha="center", va="center", fontsize=6.6, color="white" if dark else TEXT, fontweight="bold" if E > 492 else "normal")
            if lo <= E <= hi: ax.add_patch(Rectangle((k - 0.5, i - 0.5), 1, 1, fill=False, ec=ROLE["proposal"], lw=1.6, zorder=4))
    ax.set_xticks(range(len(seats))); ax.set_xticklabels([f"{s}" if s != int(SEATS_TODAY) else f"{s}\n(today)" for s in seats], fontsize=6.8)
    ax.set_yticks(range(len(captures))); ax.set_yticklabels([f"{c:.0%}" if c != CAP_TODAY else f"{c:.0%} (today)" for c in captures], fontsize=6.8)
    ax.grid(False)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_title(f"{fall}-{str(fall + 1)[2:]}: {RESIDENTS[fall]:.0f} projected residents (p. 51)\nproposal's range {lo}-{hi} outlined in red", fontsize=7.8, loc="left")
    ti, tk = captures.index(CAP_TODAY), seats.index(int(SEATS_TODAY))
    ax.plot(tk - 0.33, ti + 0.3, marker="*", ms=7, color="white", mec=TEXT, mew=0.8, zorder=6)
    # locus of today's pattern if x of the 163 live inside the combined area (x = 0 at the star, up-left as x grows)
    xs = np.arange(0, 81, 2); locus_seats = SEATS_TODAY - xs; locus_cap = (ATT_TODAY + xs) / RES_TODAY
    ax.plot(np.interp(locus_seats, seats, range(len(seats))), np.interp(locus_cap, captures, range(len(captures))), color=TEXT, lw=1.1, ls="--", zorder=5)
axes[0].set_ylabel("combined-area resident capture rate", fontsize=7.5)
fig.supxlabel("external choice seats kept (enrolled from outside the combined area + out-of-district)", fontsize=7.2, y=0.04)
fig.subplots_adjust(bottom=0.2, wspace=0.14)
cb = fig.colorbar(im, ax=axes, orientation="vertical", fraction=0.035, pad=0.02, ticks=[300, 350, 403, 450, 492, 550, 620])
cb.ax.tick_params(labelsize=6.5); cb.set_label("students at the merged school", fontsize=7)
fig.suptitle("Residents x capture rate + choice seats: which combinations produce the proposal's range, and which exceed the building (492)", fontsize=8.6, fontweight="bold", x=0.01, ha="left", y=1.02)
save(fig, "fig14_accounting_grid", source="deck p. 51 (projected residents, ranges), p. 44 (residents attending, bar labels); 2025-26 special-programs summary (out-of-district); identity, no model; star = today's pattern with all 163 non-resident-attending students treated as external (x = 0); dashed line = the same pattern if x of them live inside the combined area, x up to 80")
print(grid[grid.is_today_rates][["fall", "enrollment", "p_over_492_trend", "p_over_492_level"]].round(2).to_string(index=False))
