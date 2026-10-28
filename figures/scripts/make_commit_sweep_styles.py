"""Figure for Section 6.2 (exploratory commitment sweep of all four designed styles), MDPI version, 2026-10-12.

Data: repro_outputs/commit_sweep_styles/{random,urban}/sensitivity_commitment[_PO|_Agg|_SA].csv of the artifact
repository (ec_repro_artifact_new), written by code/experiments/run_sensitivity_commitment.py --style ... and checked
by code/experiments/analyze_commit_sweep_styles.py (every style at its configured weight reproduces the main
experiment). Goal switches per 100 alive steps, mean and 95% t-interval, log scale; open circles mark the configured
weights. Drawn at the printed size (the 18.46 cm full page width) in TeX Gyre Pagella at 7.5 pt, like Figures 4-7.

Usage (artifact virtual environment):
  python figures/make_commit_sweep_styles.py --root <repro_outputs/commit_sweep_styles> --code <ec_repro_artifact_new/code> \
      --out figures/fig_commit_sweep_styles.pdf
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

STYLES = [("MC", "sensitivity_commitment.csv", 0.45, "Mission–Cooperation (hold)", "tab:blue"),
          ("PO", "sensitivity_commitment_PO.csv", 0.85, "Persistent Objective (keep moving)", "tab:orange"),
          ("Agg", "sensitivity_commitment_Agg.csv", 0.25, "Aggressive (chase)", "tab:red"),
          ("SA", "sensitivity_commitment_SA.csv", 0.25, "Survival-Aware (evade)", "tab:green")]
MAPS = ["random"]  # the urban map gives the same curves (author, 2026-10-12: four near-identical panels not needed)
SCENARIOS = ["Mission", "Control"]
SW = "goal_switch_rate_per_100"


def use_pagella() -> None:
    try:
        path = subprocess.run(["kpsewhich", "texgyrepagella-regular.otf"], capture_output=True, text=True).stdout.strip()
    except OSError:
        path = ""
    if path:
        font_manager.fontManager.addfont(path)
        matplotlib.rcParams["font.family"] = "serif"
        matplotlib.rcParams["font.serif"] = ["TeX Gyre Pagella"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--code", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--fontsize", type=float, default=7.5)
    a = ap.parse_args()
    sys.path.insert(0, str(Path(a.code) / "experiments"))
    sys.path.insert(0, str(a.code))
    from make_ec_figures import mean_ci

    use_pagella()
    fs = a.fontsize
    fig, axes = plt.subplots(1, 2, figsize=(7.27, 2.5), sharex=True, squeeze=False)
    for i, m in enumerate(MAPS):
        for j, sc in enumerate(SCENARIOS):
            ax = axes[i, j]
            for abbr, fname, wconf, label, color in STYLES:
                df = pd.read_csv(Path(a.root) / m / fname)
                df["w"] = df["w_commitment"].astype(float).round(2)
                g = df[df["scenario"] == sc]
                ws = sorted(set(g["w"]))
                stats_ = [mean_ci(g[g["w"] == w][SW].astype(float).values) for w in ws]
                ms = np.array([s[0] for s in stats_]); cs = np.array([s[1] for s in stats_])
                ax.plot(ws, ms, marker="o", ms=2.5, lw=1.0, color=color, label=label)
                ax.fill_between(ws, ms - cs, ms + cs, color=color, alpha=0.15, lw=0)
                k = ws.index(wconf)
                ax.plot([wconf], [ms[k]], marker="o", ms=6, mfc="none", mec=color, mew=1.0)
            ax.set_yscale("log")
            ax.set_title(f"{sc}, {m} map", fontsize=fs)
            ax.tick_params(labelsize=fs, length=2, which="both")
            ax.grid(True, which="both", axis="y", linewidth=0.3, alpha=0.4)
            if j == 0:
                ax.set_ylabel("Goal switches per 100 alive steps", fontsize=fs)
            if i == len(MAPS) - 1:
                ax.set_xlabel("Commitment weight $w_{\\mathrm{commit}}$", fontsize=fs)
    h, l = axes[0, 0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=4, fontsize=fs, frameon=False)
    fig.tight_layout(rect=(0, 0, 1, 0.9), h_pad=0.8)
    fig.savefig(a.out)
    plt.close(fig)


if __name__ == "__main__":
    main()
