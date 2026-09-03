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
VINTAGE_COLOR = {"jan2024": C["aqua"], "jan2025": C["yellow"], "jan2026": C["blue"], "aug2026": C["red"]}
VINTAGE_LABEL = {"jan2024": "Jan 2024 run (Feb 2024 report)", "jan2025": "Jan 2025 run (Feb 2025 report; re-used Oct 2025)", "jan2026": "Jan 2026 run (Feb 2026 report)", "aug2026": "Aug 2026 proposal (post-merger range)"}
TEXT, MUTED, GRID = "#0b0b0b", "#52514e", "#e6e5e1"
CAPACITY = {"Bear Creek": 492, "Mesa": 418}
CAP_BC_2024 = 467
ROUNDS_BC = 3.5            # 21 sections
THREE_ROUNDS, TWO_ROUNDS, ONE_ROUND = 450, 300, 150

def style():
    mpl.rcParams.update({
        "figure.dpi": 150, "savefig.dpi": 200, "font.size": 9.5, "font.family": "DejaVu Sans",
        "axes.edgecolor": GRID, "axes.linewidth": 0.8, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
        "axes.spines.top": False, "axes.spines.right": False, "axes.titleweight": "bold", "axes.titlesize": 10.5,
        "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "text.color": TEXT,
        "legend.frameon": False, "legend.fontsize": 8.5, "lines.linewidth": 2, "lines.markersize": 5,
        "figure.facecolor": "white", "axes.facecolor": "white",
    })

def save(fig, name):
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
