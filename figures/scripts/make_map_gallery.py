"""Figure 3 (map gallery) for the MDPI version, 2026-10-12.

Same panels as make_map_gallery.py in the artifact repository (ec_repro_artifact_new/code/experiments; its draw()
is imported, so the maps, markers, and the four descriptors under each title are unchanged; the titles are set here on
three lines, name / visibility and cover / cut and headroom, with shorter names), arranged
as the author asked: row 1 the random development map and its three generated maps, row 2 the urban map and its
three, row 3 blocks, walls, mixed, row 4 the four game-inspired maps. Drawn at the printed size (the 18.46 cm full
page width used by the wide floats) in TeX Gyre Pagella at 7.5 pt, like Figures 4-7.

Usage (with the artifact repository's virtual environment):
  python figures/make_map_gallery.py --code <ec_repro_artifact_new/code> \
      --descriptors <repro_outputs/maps/testbed_fixed/descriptors.csv> --out figures/fig_map_gallery.pdf
"""
from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

LABELS = {
    "random": "random, seed 7", "urban": "urban, seed 11",
    "blocks": "blocks (large buildings)", "walls": "walls (thin walls)", "mixed": "mixed (buildings and walls)",
    "cso": "cso: bomb-site lanes", "ow": "ow: control point", "ac": "ac: close-quarters loops", "xo": "xo: open arena",
}


def label(name: str) -> str:
    if name in LABELS:
        return LABELS[name]
    kind, seed = name.split("_s")
    return f"{kind} generator, seed {seed}"


ROWS = [
    ["random", "random_s101", "random_s102", "random_s103"],
    ["urban", "urban_s101", "urban_s102", "urban_s103"],
    ["blocks", "walls", "mixed", None],
    ["cso", "ow", "ac", "xo"],
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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--code", required=True)
    ap.add_argument("--descriptors", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--fontsize", type=float, default=7.5)
    ap.add_argument("--height", type=float, default=8.2, help="figure height in inches")
    a = ap.parse_args()
    sys.path.insert(0, str(Path(a.code) / "experiments"))
    sys.path.insert(0, str(a.code))
    from make_map_gallery import draw  # the artifact's panel drawing (maps, markers, title with descriptors)

    descs = {r["map"]: r for r in csv.DictReader(open(a.descriptors))}
    use_pagella()
    fs = a.fontsize
    fig, axes = plt.subplots(4, 4, figsize=(7.27, a.height))
    for row, names in zip(axes, ROWS):
        for ax, n in zip(row, names):
            if n is None:
                ax.axis("off")
                continue
            draw(ax, n, descs.get(n))
            d = descs.get(n)
            title = label(n)
            if d:
                title += (f"\nvisibility {float(d['visibility']):.0f}, cover {float(d['cover']):.2f}"
                          f"\ncut {d['cut']}, headroom {float(d['headroom']):.2f}")
            ax.set_title(title, fontsize=fs, linespacing=1.1)
    handles = {}
    for row in axes:
        for ax in row:
            for h, l in zip(*ax.get_legend_handles_labels()):
                handles.setdefault(l, h)
    fig.legend(list(handles.values()), list(handles.keys()), loc="lower center", ncol=len(handles), fontsize=fs,
               frameon=False, handletextpad=0.4, columnspacing=1.5)
    fig.tight_layout(rect=(0, 0.035, 1, 1), h_pad=2.2, w_pad=0.4)  # h_pad: a clear gap between the rows (author)
    fig.savefig(a.out)
    plt.close(fig)


if __name__ == "__main__":
    main()
