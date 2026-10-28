"""Asymmetric line of sight on the registered maps (2026-09-25).

The Bresenham line from a to b can differ from the line from b to a, so one agent can see another that does not see
it. This script counts, for every pair of free cells within the view radius, whether the line of sight is clear in
either direction and whether the two directions disagree, with the symmetric rule off (the earlier testbed) and on.
Used for the earlier-testbed appendix (audit of the movement and perception rules).

Usage: python experiments/analyze_los_symmetry.py [--maps random,urban,cso,ow,ac,xo]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fps_priority_ai import world as world_mod  # noqa: E402
from fps_priority_ai.config import AgentConfig  # noqa: E402
from fps_priority_ai.env import build_world  # noqa: E402
from fps_priority_ai.experiment import MAPS  # noqa: E402
from fps_priority_ai.world import euclidean  # noqa: E402


def count(map_name: str, view: float) -> tuple:
    w = build_world(MAPS[map_name])
    free = [(x, y) for x in range(w.width) for y in range(w.height) if w.passable((x, y))]
    n = asym = vis = 0
    for i, a in enumerate(free):
        for b in free[i + 1:]:
            if euclidean(a, b) <= view:
                n += 1
                ab, ba = w.los_clear(a, b), w.los_clear(b, a)
                vis += ab or ba
                asym += ab != ba
    return n, vis, asym


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--maps", default="random,urban,cso,ow,ac,xo")
    a = p.parse_args()
    view = AgentConfig().view_radius
    for sym in (False, True):
        world_mod.SYMMETRIC_LOS = sym
        print(f"symmetric line of sight: {'on' if sym else 'off'}")
        for m in a.maps.split(","):
            n, vis, asym = count(m, view)
            print(f"  {m}: pairs within view radius {n}, visible (either direction) {vis}, "
                  f"asymmetric {asym} ({100 * asym / max(vis, 1):.1f}% of visible pairs)")


if __name__ == "__main__":
    main()
