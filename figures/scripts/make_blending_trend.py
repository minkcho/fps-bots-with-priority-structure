"""Figure for Section 6.4 (H4, style blending), MDPI version, 2026-10-12.

Trends along the blend weight alpha from interpolation.csv of the random and the urban map (artifact repository
ec_repro_artifact_new, repro_outputs/v3_fixed and v3_fixed/urban; the same data as make_interpolation() of
code/experiments/make_extra_figures.py): engagement redirection along Aggressive -> Survival-Aware in Deathmatch and
the nearest-ally distance along Mission-Cooperation -> Persistent Objective in Mission; mean and 95% t-interval per
alpha (n = 100), one line per map. Bottom row (2026-10-13, exploratory, author), on a fine alpha grid
(run_interpolation.py --pairs ... --alphas ...; alpha = 0 and 1 reproduce the weights-only runs of the two styles):
(c) objective commitment along Aggressive -> Mission-Cooperation in Mission
(repro_outputs/blend_agg_mc/<map>/interpolation_agg_mc_fine_Mission.csv); (d) resource seeking along Persistent
Objective -> Survival-Aware in Control (repro_outputs/blend_po_sa/<map>/interpolation_po_sa_fine_Control.csv). Text width (13.85 cm),
TeX Gyre Pagella 7.5 pt, like the other figures.

Usage (artifact virtual environment):
  python figures/make_blending_trend.py --random-dir <repro_outputs/v3_fixed> --urban-dir <repro_outputs/v3_fixed/urban> \
      --outputs-root <repro_outputs> --code <ec_repro_artifact_new/code> --out figures/fig_blending_trend.pdf
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

PANELS = [("Aggressive -> Survival-Aware", "Deathmatch", "engagement_redirection_rate_per_100",
           "Engagement redirection\n(per 100 alive steps)", "(a) Aggressive → Survival-Aware\n(Deathmatch)"),
          ("Mission–Cooperation -> Persistent Objective", "Mission", "avg_ally_proximity",
           "Nearest-ally distance", "(b) Mission–Cooperation → Persistent Objective\n(Mission)")]
BOTTOM = [("blend_agg_mc", "interpolation_agg_mc_fine_Mission.csv", "objective_commitment_ratio",
           "Objective commitment", "(c) Aggressive → Mission–Cooperation\n(Mission)", (0.0, 1.0)),
          ("blend_po_sa", "interpolation_po_sa_fine_Control.csv", "resource_seeking_rate_per_100",
           "Resource seeking\n(per 100 alive steps)", "(d) Persistent Objective → Survival-Aware\n(Control)", (0.0, 0.5))]
# Reference for (d): Survival-Aware with its evade mode in Control (main experiment, results.csv), dashed, per map.
REF_D = ("Survival-Aware", "Control", "resource_seeking_rate_per_100")
MAP_COLORS = {"random": "#0072b2", "urban": "#e69f00"}


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
    ap.add_argument("--random-dir", required=True)
    ap.add_argument("--urban-dir", required=True)
    ap.add_argument("--outputs-root", required=True, help="the artifact's repro_outputs directory")
    ap.add_argument("--code", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--print", action="store_true")
    ap.add_argument("--width-cm", type=float, default=13.85, help="canvas width in cm (18.46 = full page width, as in the paper)")
    ap.add_argument("--height-cm", type=float, default=9.652, help="canvas height in cm (3.8 in)")
    a = ap.parse_args()
    sys.path.insert(0, str(Path(a.code) / "experiments"))
    sys.path.insert(0, str(a.code))
    from make_ec_figures import mean_ci

    data = {"random": pd.read_csv(Path(a.random_dir) / "interpolation.csv"),
            "urban": pd.read_csv(Path(a.urban_dir) / "interpolation.csv")}
    use_pagella()
    fs = 7.5
    fig, axs = plt.subplots(2, 2, figsize=(a.width_cm / 2.54, a.height_cm / 2.54))
    axes = axs[0]
    for ax, (pair, sc, col, ylabel, title) in zip(axes, PANELS):
        for m, df in data.items():
            g = df[(df["pair"] == pair) & (df["scenario"] == sc)]
            alphas = sorted(g["alpha"].astype(float).unique())
            st = [mean_ci(g[g["alpha"].astype(float) == x][col].astype(float).values) for x in alphas]
            ms = np.array([s[0] for s in st]); cs = np.array([s[1] for s in st])
            if a.print:
                print(f"{m} {sc} {col}:", " ".join(f"{v:.2f}" for v in ms))
            ax.plot(alphas, ms, marker="o", ms=3, lw=1.0, color=MAP_COLORS[m], label=f"{m} map")
            ax.fill_between(alphas, ms - cs, ms + cs, color=MAP_COLORS[m], alpha=0.18, lw=0)
        ax.set_title(title, fontsize=fs, linespacing=1.1)
        ax.set_xlabel("Blend weight $\\alpha$", fontsize=fs)
        ax.set_ylabel(ylabel, fontsize=fs)
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.tick_params(labelsize=fs, length=2)
        ax.grid(True, axis="y", linewidth=0.3, alpha=0.4)
    axes[0].legend(fontsize=fs, frameon=False, loc="upper right")
    for k, (ax, (sub_dir, fname, col, ylabel, title, ylim)) in enumerate(zip(axs[1], BOTTOM)):
        for m in ("random", "urban"):
            g = pd.read_csv(Path(a.outputs_root) / sub_dir / m / fname)
            alphas = sorted(g["alpha"].astype(float).unique())
            st = [mean_ci(g[g["alpha"].astype(float) == x][col].astype(float).values) for x in alphas]
            ms = np.array([s[0] for s in st]); cs = np.array([s[1] for s in st])
            if a.print:
                print(f"{m} {fname} {col}:", " ".join(f"{x:.2f}:{v:.2f}" for x, v in zip(alphas, ms)))
            ax.plot(alphas, ms, marker="o", ms=2.5, lw=1.0, color=MAP_COLORS[m], label=f"{m} map")
            ax.fill_between(alphas, ms - cs, ms + cs, color=MAP_COLORS[m], alpha=0.18, lw=0)
        if k == 1:
            refs = []
            for m, d in (("random", a.random_dir), ("urban", a.urban_dir)):
                res = pd.read_csv(Path(d) / "results.csv")
                res["style"] = res["style"].astype(str).str.replace("\u2013", "-", regex=False)
                v = res[(res["style"] == REF_D[0]) & (res["scenario"] == REF_D[1])][REF_D[2]].astype(float).mean()
                refs.append(v)
                ax.axhline(v, color=MAP_COLORS[m], ls="--", lw=0.8)
                if a.print:
                    print(f"{m} reference {REF_D}: {v:.3f}")
            ax.text(0.02, min(refs) - 0.012, "\u2191 Survival-Aware with its evade mode", fontsize=fs, va="top", ha="left")
        ax.set_title(title, fontsize=fs, linespacing=1.1)
        ax.set_xlabel("Blend weight $\\alpha$", fontsize=fs)
        ax.set_ylabel(ylabel, fontsize=fs)
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
        if ylim:
            ax.set_ylim(*ylim)
        ax.tick_params(labelsize=fs, length=2)
        ax.grid(True, axis="y", linewidth=0.3, alpha=0.4)
    fig.tight_layout(w_pad=1.5, h_pad=1.0)
    fig.savefig(a.out)
    plt.close(fig)


if __name__ == "__main__":
    main()
