"""Figure 5 (combat-movement mode ablation) for the MDPI version, 2026-10-11.

Same numbers as make_mode_ablation() in the artifact repository
(ec_repro_artifact_new/code/experiments/make_extra_figures.py; mean and 95% t-interval per style, full policy
from results.csv against the weights-only variant from mode_ablation.csv), redrawn as a 2 x 2 panel grid at the
printed size (the 18.46 cm full page width used by the wide floats, by 11 cm) in TeX Gyre Pagella at 7.5 pt, with one shared legend above the panels
and two-line style names under the bars.

Usage (with the artifact repository's virtual environment, which has the helper module on its path):
  python figures/make_mode_ablation.py --csv <results.csv> --mode-csv <mode_ablation.csv> \
      --code <ec_repro_artifact_new/code> --out figures/fig_mode_ablation.pdf
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

STYLES_ORDER = ["Mission–Cooperation", "Persistent Objective", "Aggressive", "Survival-Aware"]
TICK_LABELS = ["Mission–\nCooperation", "Persistent\nObjective", "Aggressive", "Survival-\nAware"]
PANELS = [
    ("Mission", "objective_commitment_ratio", "Objective commitment ratio", "Mission: objective commitment"),
    ("Deathmatch", "engagement_redirection_rate_per_100", "Switches per 100 alive steps", "Deathmatch: engagement redirection"),
    ("Deathmatch", "resource_seeking_rate_per_100", "Switches per 100 alive steps", "Deathmatch: resource seeking"),
    ("Control", "control_score", "Control score", "Control: score"),
]


def use_pagella() -> None:
    try:
        path = subprocess.run(["kpsewhich", "texgyrepagella-regular.otf"], capture_output=True, text=True).stdout.strip()
    except OSError:
        path = ""
    if path:
        font_manager.fontManager.addfont(path)
        matplotlib.rcParams["font.family"] = "serif"
        matplotlib.rcParams["font.serif"] = ["TeX Gyre Pagella"]


def normalise(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    return df


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--mode-csv", required=True)
    ap.add_argument("--code", required=True, help="path to the artifact's code/ directory (for mean_ci)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--print", action="store_true")
    a = ap.parse_args()
    sys.path.insert(0, str(Path(a.code) / "experiments"))
    sys.path.insert(0, str(a.code))
    from make_ec_figures import mean_ci  # the artifact's 95% t-interval helper

    df, mode_df = normalise(pd.read_csv(a.csv)), normalise(pd.read_csv(a.mode_csv))
    use_pagella()
    fs = 7.5
    fig, axes = plt.subplots(2, 2, figsize=(7.27, 4.3))
    axes = axes.ravel()
    x = np.arange(len(STYLES_ORDER))
    width = 0.4
    for ax, (sc, col, ylabel, title) in zip(axes, PANELS):
        for i, (label, src) in enumerate((("Full (pinned mode)", df), ("Weights-only (keep moving)", mode_df))):
            means, cis = [], []
            for s in STYLES_ORDER:
                vals = src[(src["scenario"] == sc) & (src["style"] == s)][col].astype(float).values
                m, c = mean_ci(vals)
                means.append(m); cis.append(c)
            if a.print:
                print(title, "|", label, "|", " ".join(f"{m:.3f}±{c:.3f}" for m, c in zip(means, cis)))
            offs = (i - 0.5) * width
            ax.bar(x + offs, means, width=width * 0.92, yerr=cis, capsize=2, label=label, linewidth=0)
        ax.set_xticks(x)
        ax.set_xticklabels(TICK_LABELS, fontsize=fs)
        ax.tick_params(axis="y", labelsize=fs, length=2)
        ax.tick_params(axis="x", length=2)
        ax.set_title(title, fontsize=fs)
        ax.set_ylabel(ylabel, fontsize=fs)
        ax.grid(True, axis="y", linewidth=0.3, alpha=0.4)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, fontsize=fs, frameon=False)
    fig.tight_layout(rect=(0, 0, 1, 0.95), h_pad=1.2)
    fig.savefig(a.out)
    plt.close(fig)


if __name__ == "__main__":
    main()
