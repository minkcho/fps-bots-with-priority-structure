"""Compact version of Figure 4 (behavioral fingerprints) for the MDPI version, 2026-10-10.

Same data pipeline as make_fingerprint_heatmap() in the artifact repository
(ec_repro_artifact_new/code/experiments/make_extra_figures.py): mean of each intent metric per
(scenario, style) condition from results.csv, min-max normalized per metric over the 12 conditions,
ally distance inverted so that the last column reads as cohesion. Only the drawing differs: the canvas is the
printed size (the 13.85 cm text width by 7.6 cm), the text is TeX Gyre Pagella (the Palatino clone of TeX Live,
the body font of the MDPI class) at 7.5 pt, the size of Figures 5-7 and smaller than the 10-pt body text, as the author asked;
no in-figure title (the caption carries it); full style names. The in-figure title of the earlier version ("Normalised behaviour fingerprints ...")
is therefore gone.

Usage:
  python figures/make_fingerprint_heatmap.py --csv <results.csv of the random-map main experiment> \
      --out figures/fig_fingerprint_heatmap.pdf
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import subprocess


def use_pagella() -> str:
    """Register TeX Gyre Pagella from TeX Live, if present, and return the family name to use."""
    try:
        path = subprocess.run(["kpsewhich", "texgyrepagella-regular.otf"], capture_output=True, text=True).stdout.strip()
    except OSError:
        path = ""
    if path:
        font_manager.fontManager.addfont(path)
        matplotlib.rcParams["font.family"] = "serif"
        matplotlib.rcParams["font.serif"] = ["TeX Gyre Pagella"]
        return "TeX Gyre Pagella"
    return matplotlib.rcParams["font.family"][0]

STYLES_ORDER = ["Mission–Cooperation", "Persistent Objective", "Aggressive", "Survival-Aware"]
SCENARIOS_ORDER = ["Mission", "Deathmatch", "Control"]
METRIC_COLS = [
    ("objective_commitment_ratio", "Objective\ncommitment"),
    ("engagement_redirection_rate_per_100", "Engagement\nredirection"),
    ("resource_seeking_rate_per_100", "Resource\nseeking"),
    ("avg_ally_proximity", "Cohesion\n(inverted\nally distance)"),
]


def fingerprint_matrix(df: pd.DataFrame):
    df = df.copy()
    rows, labels = [], []
    for sc in SCENARIOS_ORDER:
        for st in STYLES_ORDER:
            sub = df[(df["scenario"] == sc) & (df["style"] == st)]
            rows.append([float(sub[c].astype(float).mean()) for c, _ in METRIC_COLS])
            labels.append(f"{sc} / {st}")
    data = np.asarray(rows, dtype=float)
    norm = np.zeros_like(data)
    for j in range(data.shape[1]):
        col = data[:, j]
        rng = col.max() - col.min()
        norm[:, j] = 0.0 if rng == 0 else (col - col.min()) / rng
    norm[:, 3] = 1.0 - norm[:, 3]
    return norm, labels


def draw(norm, labels, out_path: Path, width_cm: float = 13.85, height_cm: float = 7.6) -> None:
    use_pagella()
    fs = 7.5
    fig, ax = plt.subplots(figsize=(width_cm / 2.54, height_cm / 2.54))
    im = ax.imshow(norm, aspect="auto", vmin=0.0, vmax=1.0)
    ax.set_xticks(np.arange(len(METRIC_COLS)))
    ax.set_xticklabels([lab for _, lab in METRIC_COLS], fontsize=fs)
    ax.set_yticks(np.arange(len(labels)))
    ax.set_yticklabels(labels, fontsize=fs)
    ax.tick_params(length=2)
    for i in range(norm.shape[0]):
        for j in range(norm.shape[1]):
            ax.text(j, i, f"{norm[i, j]:.2f}", ha="center", va="center", fontsize=fs,
                    color="white" if norm[i, j] < 0.5 else "black")
    cb = fig.colorbar(im, ax=ax, shrink=0.9, pad=0.02)
    cb.ax.tick_params(labelsize=fs, length=2)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--print", action="store_true", help="print the normalized matrix")
    p.add_argument("--width-cm", type=float, default=13.85, help="canvas width in cm (13.85 = text width; 18.46 = full page width, as in the paper)")
    p.add_argument("--height-cm", type=float, default=7.6, help="canvas height in cm (8.5 in the paper)")
    a = p.parse_args()
    norm, labels = fingerprint_matrix(pd.read_csv(a.csv))
    if a.print:
        for lab, row in zip(labels, norm):
            print(lab, " ".join(f"{v:.2f}" for v in row))
    draw(norm, labels, Path(a.out), a.width_cm, a.height_cm)


if __name__ == "__main__":
    main()
