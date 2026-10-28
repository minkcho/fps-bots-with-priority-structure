"""Exploratory figure (2026-09-28): the 25x25 development maps next to their three 50x50 variants of
explore_map50.py (spread50, zoom50, regen50), drawn at the same cell size so that the change of scale is visible.
Output: repro_outputs/dev_map50/map_variants.png.  Usage: python experiments/plot_map50_variants.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from explore_map50 import descriptors, variants  # noqa: E402
from fps_priority_ai.env import build_world  # noqa: E402

TITLES = {"base25": "25x25 (original)", "spread50": "spread50 (positions x2)", "zoom50": "zoom50 (2x2 blocks)",
          "regen50": "regen50 (same generator)"}


def main() -> None:
    vs = variants()
    fig, axes = plt.subplots(2, 4, figsize=(16, 8.4), gridspec_kw={"width_ratios": [1, 2, 2, 2]})
    for row, name in enumerate(("random", "urban")):
        for col, kind in enumerate(("base25", "spread50", "zoom50", "regen50")):
            cfg = vs[f"{name}/{kind}"]
            world = build_world(cfg)
            grid = np.zeros((cfg.height, cfg.width))
            for x, y in world.obstacles:
                grid[y, x] = 1
            ax = axes[row, col]
            ax.imshow(grid, cmap="Greys", origin="upper", vmin=0, vmax=1.4, interpolation="nearest")
            for (x, y), c, m in ((cfg.spawn_a, "tab:blue", "X"), (cfg.spawn_b, "tab:red", "X"), (cfg.objective, "gold", "*")):
                ax.plot(x, y, marker=m, color=c, markersize=11 if m == "*" else 8, markeredgecolor="black")
            d = descriptors(cfg)
            ax.set_title(f"{name} {TITLES[kind]}\ndensity {d['density']:.2f}, visibility {d['visibility']:.0f}, "
                         f"path {d['path_to_objective']}", fontsize=9)
            ax.set_xticks([])
            ax.set_yticks([])
    fig.tight_layout()
    out = Path(__file__).resolve().parents[2] / "repro_outputs" / "dev_map50" / "map_variants.png"
    fig.savefig(out, dpi=110)
    print(f"written: {out}")


if __name__ == "__main__":
    main()
