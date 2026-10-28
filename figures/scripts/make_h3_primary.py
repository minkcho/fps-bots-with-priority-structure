"""Figure 7 (primary H3 tests) for the MDPI version; split in two and merged again on 2026-10-12 (author), one row.

Same numbers as make_h3_primary_figure.py in the artifact repository (ec_repro_artifact_new/code/experiments),
from cost_term_ablation.csv of the random and the urban map:
(a), (b) Deathmatch, expected hits per walked step for each style with the configured exposure weight and with
lambda_E = 0 (mean and 95% t-interval), random and urban map; (c) relative change of the mean walked exposure,
configured vs lambda_E = 0, for every scenario x style condition on both maps (marker: style; color: map), the
conditions of the sign test. (a), (b) in the top row (full style names under the bars, one y axis), (c) across the bottom row with a small legend beside it; full page width, TeX Gyre Pagella 7.5 pt (the legend of (c) 7 pt).

Usage (with the artifact repository's virtual environment):
  python figures/make_h3_primary.py --random-dir <repro_outputs/v3_fixed> --urban-dir <repro_outputs/v3_fixed/urban> \
      --code <ec_repro_artifact_new/code> --out figures/fig_h3_primary.pdf
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
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

STYLES_ORDER = ["Mission–Cooperation", "Persistent Objective", "Aggressive", "Survival-Aware"]
TICK_LABELS = ["Mission–\nCooperation", "Persistent\nObjective", "Aggressive", "Survival-\nAware"]
TICK_ABBR = ["MC", "PO", "Agg", "SA"]  # (a), (b): abbreviations of Table 2, so that (c) gets the width (author, 2026-10-12)
SCENARIOS_ORDER = ["Mission", "Deathmatch", "Control"]
MARKERS = {"Mission–Cooperation": "o", "Persistent Objective": "s", "Aggressive": "^", "Survival-Aware": "D"}
MAP_COLORS = {"random": "#0072b2", "urban": "#e69f00"}
COL = "walked_hits_per_step"


def use_pagella() -> None:
    try:
        path = subprocess.run(["kpsewhich", "texgyrepagella-regular.otf"], capture_output=True, text=True).stdout.strip()
    except OSError:
        path = ""
    if path:
        font_manager.fontManager.addfont(path)
        matplotlib.rcParams["font.family"] = "serif"
        matplotlib.rcParams["font.serif"] = ["TeX Gyre Pagella"]


def load(d: Path) -> pd.DataFrame:
    df = pd.read_csv(d / "cost_term_ablation.csv")
    return df


def bars(ax, name, df, title, mean_ci, fs, show_print):
    x = np.arange(len(STYLES_ORDER))
    width = 0.4
    sub = df[df["scenario"] == "Deathmatch"]
    for i, (variant, label) in enumerate((("full", "configured $\\lambda_E$"), ("no_exposure", "$\\lambda_E=0$"))):
        means, cis = [], []
        for st in STYLES_ORDER:
            vals = sub[(sub["style"] == st) & (sub["variant"] == variant)][COL].astype(float).values
            m, c = mean_ci(vals)
            means.append(m); cis.append(c)
        if show_print:
            print(f"{name} | {label} |", " ".join(f"{m:.4f}±{c:.4f}" for m, c in zip(means, cis)))
        ax.bar(x + (i - 0.5) * width, means, width=width * 0.92, yerr=cis, capsize=1.5, label=label, linewidth=0,
               error_kw={"elinewidth": 0.8})
    ax.set_xticks(x)
    ax.set_xticklabels(TICK_LABELS, fontsize=fs)
    ax.tick_params(axis="y", labelsize=fs, length=2)
    ax.tick_params(axis="x", length=2, pad=1.5)
    ax.set_title(title, fontsize=fs)
    ax.grid(True, axis="y", linewidth=0.3, alpha=0.4)
    ax.set_ylim(0, 0.16)
    ax.legend(loc="upper left", fontsize=fs, frameon=False, handlelength=1.2, borderaxespad=0.3)


def scatter(ax, maps, fs, show_print):
    for mi, (name, df) in enumerate(maps):
        for si, sc in enumerate(SCENARIOS_ORDER):
            for ti, st in enumerate(STYLES_ORDER):
                cond = df[(df["scenario"] == sc) & (df["style"] == st)]
                full = cond[cond["variant"] == "full"][COL].astype(float).mean()
                base = cond[cond["variant"] == "no_exposure"][COL].astype(float).mean()
                rel = 100.0 * (full - base) / base
                if show_print:
                    print(f"{name} {sc} {st}: {rel:.1f}%")
                xx = si + (mi - 0.5) * 0.36 + (ti - 1.5) * 0.06
                ax.scatter([xx], [rel], marker=MARKERS[st], s=14, color=MAP_COLORS[name], edgecolor="black", linewidth=0.35, zorder=3)
    ax.axhline(0.0, color="0.3", linewidth=0.8)
    ax.set_xticks(np.arange(len(SCENARIOS_ORDER)))
    ax.set_xticklabels(SCENARIOS_ORDER, fontsize=fs)
    ax.tick_params(axis="y", labelsize=fs, length=2)
    ax.tick_params(axis="x", length=2, pad=1.5)
    ax.set_title("(c) All scenario $\\times$ style conditions", fontsize=fs)
    ax.set_ylabel("Change of walked\nexposure (%)", fontsize=fs)
    ax.grid(True, axis="y", linewidth=0.3, alpha=0.4)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--random-dir", required=True)
    ap.add_argument("--urban-dir", required=True)
    ap.add_argument("--code", required=True, help="path to the artifact's code/ directory (for mean_ci)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--height", type=float, default=3.35, help="figure height in inches")
    ap.add_argument("--print", action="store_true")
    ap.add_argument("--hpad", type=float, default=0.6, help="vertical gap between the two rows, in font-size units (2.0 in the paper)")
    a = ap.parse_args()
    sys.path.insert(0, str(Path(a.code) / "experiments"))
    sys.path.insert(0, str(a.code))
    from make_ec_figures import mean_ci

    maps = [("random", load(Path(a.random_dir))), ("urban", load(Path(a.urban_dir)))]
    use_pagella()
    fs = 7.5
    fig = plt.figure(figsize=(7.27, a.height))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.05])
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1], sharey=ax_a)
    ax_c = fig.add_subplot(gs[1, :])
    bars(ax_a, "random", maps[0][1], "(a) Deathmatch, random map", mean_ci, fs, a.print)
    bars(ax_b, "urban", maps[1][1], "(b) Deathmatch, urban map", mean_ci, fs, a.print)
    ax_a.set_ylabel("Walked expected hits\nper step", fontsize=fs)
    ax_b.tick_params(axis="y", labelleft=False)
    scatter(ax_c, maps, fs, a.print)
    handles = [Line2D([], [], marker=MARKERS[st], color="0.6", markeredgecolor="black", markeredgewidth=0.4, linestyle="", markersize=4.5, label=st) for st in STYLES_ORDER]
    handles += [Patch(facecolor=MAP_COLORS[m], edgecolor="black", linewidth=0.4, label=f"{m} map") for m in ("random", "urban")]
    fig.tight_layout(h_pad=a.hpad, w_pad=1.0)
    pos = ax_c.get_position()
    ax_c.set_position([pos.x0, pos.y0, pos.width * 0.8, pos.height])
    ax_c.legend(handles=handles, loc="center left", bbox_to_anchor=(1.01, 0.5), ncol=1, fontsize=7, frameon=False,
                handletextpad=0.5, labelspacing=0.5, borderaxespad=0.0)
    fig.savefig(a.out)
    plt.close(fig)


if __name__ == "__main__":
    main()
