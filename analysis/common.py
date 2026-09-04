"""Shared loaders, constants and figure style for the analysis scripts. Run scripts from the repo root."""
from pathlib import Path
import pandas as pd, numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
CLEAN, FIG, OUT = ROOT / "data/clean", ROOT / "figures", ROOT / "analysis/output"
FIG.mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)

# Validated reference palette (dataviz skill, light mode): fixed categorical order.
C = dict(blue="#2a78d6", orange="#eb6834", aqua="#1baf7a", yellow="#eda100", magenta="#e87ba4", green="#008300", violet="#4a3aa7", red="#e34948")
SCHOOL_COLOR = {"Bear Creek": C["blue"], "Mesa": C["orange"], "Combined": C["violet"]}
# semantic roles used across all figures (one meaning per colour)
ROLE = dict(bear_creek=C["blue"], mesa=C["orange"], merged=C["violet"], proposal=C["red"], district_run="#6b6a66", background="#c9c8c3",
            trend=C["violet"], level=C["aqua"])   # trend/level: the two kindergarten specifications, both on merged-school axes
SPEC_LABEL = {"trend": "Trend assumption (kindergarten keeps falling)", "level": "Level assumption (kindergarten holds at 2023-25 average)"}
PAGE_W = 6.5   # printed text width in inches; author figures at this width so fonts print at size
VINTAGE_COLOR = {"jan2024": C["aqua"], "jan2025": C["yellow"], "jan2026": C["blue"], "aug2026": C["red"]}
VINTAGE_LABEL = {"jan2024": "Jan 2024 run (Feb 2024 report)", "jan2025": "Jan 2025 run (Feb 2025 report; re-used Oct 2025)", "jan2026": "Jan 2026 run (Feb 2026 report)", "aug2026": "Aug 2026 proposal (post-merger range)"}
TEXT, MUTED, GRID = "#0b0b0b", "#52514e", "#e6e5e1"
CAPACITY = {"Bear Creek": 492, "Mesa": 418}
CAP_BC_2024 = 467
ROUNDS_BC = 3.5            # 21 sections
THREE_ROUNDS, TWO_ROUNDS, ONE_ROUND = 450, 300, 150

def style():
    mpl.rcParams.update({
        "figure.dpi": 150, "savefig.dpi": 220, "font.size": 8.5, "font.family": "DejaVu Sans",
        "axes.edgecolor": GRID, "axes.linewidth": 0.8, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
        "axes.spines.top": False, "axes.spines.right": False, "axes.titleweight": "bold", "axes.titlesize": 10.5,
        "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "text.color": TEXT,
        "legend.frameon": False, "legend.fontsize": 7.5, "axes.titlesize": 9.5, "axes.labelsize": 8, "lines.linewidth": 2, "lines.markersize": 5,
        "figure.facecolor": "white", "axes.facecolor": "white",
    })

def save(fig, name, source=None):
    import textwrap
    # Titles are authored as one line; wrap them so the tight bounding box stays at the figure width and text prints at size.
    W = fig.get_figwidth()
    if fig._suptitle is not None:
        t = fig._suptitle; fs = t.get_fontsize(); chars = max(40, int(W * 72 / (fs * 0.64)))   # DejaVu Sans averages about 0.6 em per character
        t.set_text("\n".join(textwrap.wrap(t.get_text(), width=chars)))
    axes = fig.get_axes(); ncols = max(1, len({round(a.get_position().x0, 2) for a in axes}))
    for ax in axes:
        aw = ax.get_position().width * W   # a left-aligned title or a centred axis label runs relative to the axes box, not the canvas
        for tt in (ax.title, getattr(ax, "_left_title", None), getattr(ax, "_right_title", None)):   # loc="left" titles live in _left_title
            if tt is not None and tt.get_text():
                fs = tt.get_fontsize(); chars = max(30, int(aw * 72 / (fs * 0.64)))
                tt.set_text("\n".join(textwrap.wrap(tt.get_text(), width=chars)))
        xl = ax.xaxis.label
        if xl.get_text():
            chars = max(30, int(aw * 72 / (xl.get_fontsize() * 0.64)))
            xl.set_text("\n".join(textwrap.wrap(xl.get_text(), width=chars)))
    if source:
        wrapped = "\n".join(textwrap.wrap(f"Source: {source}", width=int(W * 17)))
        fig.text(0.0, -0.02, wrapped, fontsize=6.5, color=MUTED, ha="left", va="top", transform=fig.transFigure)
    for ext in ("png", "svg", "pdf"):
        fig.savefig(FIG / f"{name}.{ext}", bbox_inches="tight")
    plt.close(fig)
    print("saved", FIG / f"{name}.png")

def sy_to_fall(sy):  # "2029-30" -> 2029
    return int(str(sy)[:4])

def load_official():
    """Official BVSD October funded head count, Mesa + Bear Creek, grades K-5, 2014-15..2025-26."""
    d = pd.read_csv(CLEAN / "bvsd_pupil_count_mesa_bearcreek.csv")
    d = d[d.file_family == "headcount"].copy()
    d["fall"] = d.school_year.map(sy_to_fall)
    return d[["school", "school_year", "fall", "funded_headcount", "K", "G1", "G2", "G3", "G4", "G5"]].sort_values(["school", "fall"]).reset_index(drop=True)

def load_all_schools():
    d = pd.read_csv(CLEAN / "bvsd_pupil_count_all_elementary.csv")
    d["fall"] = d.school_year.map(sy_to_fall)
    return d

def load_vintages():
    """Mesa/Bear Creek projections by vintage (verified against primary pages)."""
    d = pd.read_csv(CLEAN / "capacity_summary_mesa_bearcreek_by_vintage.csv")
    d["vintage"] = d.vintage.replace({"feb2024": "jan2024", "feb2025": "jan2025", "feb2026": "jan2026"})
    d = d[d.school_year != "capacity"].copy()
    d["fall"] = d.school_year.map(sy_to_fall)
    return d

def load_merged_range():
    return pd.read_csv(CLEAN / "aug2026_deck_p51.csv")
