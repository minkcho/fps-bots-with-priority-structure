"""Figure 7 (per-map effects of the meta-analyzed confirmation tests) for the MDPI version, 2026-10-12.

Same numbers as forest() in make_confirmation_outputs.py of the artifact repository
(ec_repro_artifact_new/code/experiments): per-map estimates with 95% intervals from confirmation_summary.json
(the nine new maps), the random-effects pooled estimate (diamond) with its prediction interval,
and the smallest effect of interest (dashed). Redrawn at the printed size (the 18.46 cm full page width used by
the wide floats, by 9.7 cm; the H3 panel titles on two lines) in TeX Gyre Pagella at 7.5 pt (author's choice, 2026-10-12, after 6-pt and 7-pt trials; the same size as Figures 5 and 6), full style names.

Usage (with the artifact repository's virtual environment):
  python figures/make_confirmation_forest.py --root <repro_outputs/v4_maps> --out figures/fig_confirmation_forest.pdf
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

STYLES = ["Mission\u2013Cooperation", "Persistent Objective", "Aggressive", "Survival-Aware"]  # keys of the summary (en dash)
STYLE_NAME = {"Mission\u2013Cooperation": "Mission–Cooperation", "Persistent Objective": "Persistent Objective",
              "Aggressive": "Aggressive", "Survival-Aware": "Survival-Aware"}
MAP_TEX = {"random": "random", "urban": "urban", "random_s101": "random 101", "random_s102": "random 102",
           "random_s103": "random 103", "urban_s101": "urban 101", "urban_s102": "urban 102", "urban_s103": "urban 103",
           "blocks": "blocks", "walls": "walls", "mixed": "mixed"}
SESOI = {"h3": -0.20, "hits": -0.20, "h3b": -0.20, "h4_eng": -0.30, "h4_coh": 0.10}


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
    ap.add_argument("--out", required=True)
    ap.add_argument("--fontsize", type=float, default=7.5)
    ap.add_argument("--print", action="store_true")
    ap.add_argument("--with-dev", action="store_true",
                    help="also draw the development maps re-run with the new seeds (open circles); off since 2026-10-13 (author)")
    a = ap.parse_args()
    root = Path(a.root)
    summary = json.loads((root / "confirmation_summary.json").read_text())
    f11 = root / "confirmation_summary_11maps.json"
    summary11 = json.loads(f11.read_text()) if (a.with_dev and f11.exists()) else None

    maps9 = summary["maps"]
    per = dict(summary["per_map"])
    dev = []
    if summary11:
        for m, v in summary11["per_map"].items():
            if m not in per:
                per[m] = v
                dev.append(m)
    panels = [(f"h3|{s}", f"H3 walked exposure\n{STYLE_NAME[s]}", "r", SESOI["h3"]) for s in STYLES] + [
        ("hits", "Hits taken (four styles)", "r", SESOI["hits"]), ("h3b", "H3b ally distance", "r", SESOI["h3b"]),
        ("h4_eng", "H4 engagement along $\\alpha$", "rho", SESOI["h4_eng"]),
        ("h4_coh", "H4 ally distance along $\\alpha$", "rho", SESOI["h4_coh"])]
    rows = maps9 + dev

    use_pagella()
    fs = a.fontsize
    fig, axes = plt.subplots(2, 4, figsize=(7.27, 3.45), sharey=True)
    for ax, (key, title, kind, sesoi) in zip(axes.ravel(), panels):
        for j, m in enumerate(rows):
            e = per[m][key]
            if kind == "r":
                est, lo, hi = e["r"], e["r"] - 1.96 * e["se"], e["r"] + 1.96 * e["se"]
            else:
                est, lo, hi = e["rho"], np.tanh(e["z"] - 1.96 * e["se"]), np.tanh(e["z"] + 1.96 * e["se"])
            y = len(rows) - j + (0 if m in maps9 else -0.5)
            ax.plot([lo, hi], [y, y], color="0.3", lw=0.8)
            ax.plot(est, y, "o", ms=3, color="k" if m in maps9 else "white", mec="k", mew=0.6)
        ma = summary["meta"][key]
        f = (lambda v: v) if kind == "r" else np.tanh
        mu, (c0, c1), (p0, p1) = f(ma["mu"]), [f(c) for c in ma["ci"]], [f(p) for p in ma["pi"]]
        if a.print:
            print(f"{title.replace(chr(10), ', ')}: pooled {mu:.2f} [{c0:.2f}, {c1:.2f}]")
        yp = -1.0
        ax.plot([p0, p1], [yp, yp], color="tab:blue", lw=0.8, alpha=0.6)
        ax.fill([c0, mu, c1, mu], [yp, yp + 0.4, yp, yp - 0.4], color="tab:blue")
        ax.axvline(0, color="0.6", lw=0.6)
        ax.axvline(sesoi, color="tab:red", lw=0.6, ls="--")
        ax.set_title(title, fontsize=fs)
        ax.set_xlabel("$r$" if kind == "r" else "$\\rho$", fontsize=fs)
        ax.tick_params(labelsize=fs, length=2, pad=1.5)
    ticks = [len(rows) - j + (0 if m in maps9 else -0.5) for j, m in enumerate(rows)] + [-1.0]
    labels = [MAP_TEX.get(m, m) + ("" if m in maps9 else " (dev.)") for m in rows] + ["pooled (9 maps)"]
    for ax in axes[:, 0]:
        ax.set_yticks(ticks)
        ax.set_yticklabels(labels, fontsize=fs)
    fig.tight_layout(h_pad=0.8, w_pad=0.6)
    fig.savefig(a.out)
    plt.close(fig)


if __name__ == "__main__":
    main()
