"""Map gallery (2026-09-25): obstacle layout, spawn cells, objective and fixed item cells of registered maps.

Maps whose items are placed at random free cells in every episode (the base maps and the map sample) are drawn
without items. Descriptors (analyze_map_descriptors.py) are added under each panel title when --descriptors is
given.

Usage:
  python experiments/make_map_gallery.py --maps cso,ow,ac,xo --cols 4 \
      --descriptors ../repro_outputs/maps/descriptors.csv --out ../repro_outputs/maps/fig_map_gallery_game.pdf
  python experiments/make_map_gallery.py --descriptors ../repro_outputs/maps/descriptors.csv \
      --out ../repro_outputs/maps/fig_map_gallery.pdf          (all registered maps)
"""
from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import ListedColormap  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fps_priority_ai.env import build_world  # noqa: E402
from fps_priority_ai.maps import CONFIRMATION_MAPS, MAPS, key_cells  # noqa: E402

LABELS = {
    "random": "random (scattered cells, seed 7)",
    "urban": "urban (buildings, seed 11)",
    "blocks": "blocks (large buildings)",
    "walls": "walls (thin walls)",
    "mixed": "mixed (buildings and walls)",
    "cso": "cso: bomb-site lanes (CSO)",
    "ow": "ow: control point (Overwatch)",
    "ac": "ac: close-quarters loops (AssaultCube)",
    "xo": "xo: open arena (Xonotic)",
}


def label(name: str) -> str:
    if name in LABELS:
        return LABELS[name]
    kind, seed = name.split("_s")
    return f"{kind} generator, seed {seed}"


def draw(ax, name: str, desc: dict | None) -> None:
    cfg = MAPS[name]
    world = build_world(cfg)
    grid = [[1 if (x, y) in world.obstacles else 0 for x in range(world.width)] for y in range(world.height)]
    ax.imshow(grid, cmap=ListedColormap(["white", "0.30"]), vmin=0, vmax=1, origin="upper",
              extent=(-0.5, world.width - 0.5, world.height - 0.5, -0.5))
    for k in range(world.width + 1):
        ax.axvline(k - 0.5, color="0.85", lw=0.3, zorder=0)
    for k in range(world.height + 1):
        ax.axhline(k - 0.5, color="0.85", lw=0.3, zorder=0)
    keys = key_cells(cfg, world)
    for kind, marker, color, lab in (("health", "o", "tab:green", "Health item"), ("ammo", "^", "tab:orange", "Ammo item")):
        pts = [p for k, p in cfg.item_cells if k == kind]
        if pts:
            ax.scatter([p[0] for p in pts], [p[1] for p in pts], marker=marker, s=26, color=color, label=lab, zorder=3)
    ax.scatter([p[0] for p in keys[0:2]], [p[1] for p in keys[0:2]], marker="P", s=70, color="tab:blue",
               label="Spawn team 0", zorder=4)
    ax.scatter([p[0] for p in keys[2:4]], [p[1] for p in keys[2:4]], marker="X", s=70, color="tab:red",
               label="Spawn team 1", zorder=4)
    ax.scatter([cfg.objective[0]], [cfg.objective[1]], marker="*", s=150, color="gold", edgecolor="k", lw=0.6,
               label="Objective / control point", zorder=5)
    title = label(name)
    if desc:
        title += (f"\nvisibility {float(desc['visibility']):.0f}, cover {float(desc['cover']):.2f}, "
                  f"cut {desc['cut']}, headroom {float(desc['headroom']):.2f}")
    ax.set_title(title, fontsize=8)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-0.5, world.width - 0.5)
    ax.set_ylim(world.height - 0.5, -0.5)
    ax.set_aspect("equal")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--maps", default=None, help="comma-separated map names (default: confirmation maps, then the rest)")
    p.add_argument("--cols", type=int, default=5)
    p.add_argument("--descriptors", default=None, help="descriptors.csv of analyze_map_descriptors.py")
    p.add_argument("--out", required=True, help="output .pdf (a .png is written alongside)")
    a = p.parse_args()
    names = a.maps.split(",") if a.maps else list(CONFIRMATION_MAPS) + [m for m in MAPS if m not in CONFIRMATION_MAPS]
    descs = {}
    if a.descriptors and Path(a.descriptors).exists():
        descs = {r["map"]: r for r in csv.DictReader(open(a.descriptors))}
    cols = min(a.cols, len(names))
    rows = math.ceil(len(names) / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(3.1 * cols, 3.4 * rows + 0.5), squeeze=False)
    for ax in axes.flat[len(names):]:
        ax.axis("off")
    for ax, n in zip(axes.flat, names):
        draw(ax, n, descs.get(n))
    handles, labels_ = {}, {}
    for ax in axes.flat[:len(names)]:
        for h, l in zip(*ax.get_legend_handles_labels()):
            handles.setdefault(l, h)
    fig.legend(list(handles.values()), list(handles.keys()), loc="lower center", ncol=len(handles), fontsize=8,
               frameon=False)
    fig.tight_layout(rect=(0, 0.05 if rows > 1 else 0.08, 1, 1))
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    fig.savefig(out.with_suffix(".png"), dpi=160)
    print(f"saved {out} and {out.with_suffix('.png')}")


if __name__ == "__main__":
    main()
