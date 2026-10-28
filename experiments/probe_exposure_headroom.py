"""Exposure-avoidance headroom of a map (paper: Section "Second map with building cover").

For random start/goal pairs and random opponent positions, compares the exposure of the
safest path in the weighted-sum family (w_exposure = 50) with that of the exposure-blind
path (w_exposure = 0), using the exposure term E(v) of the planner. Reports the mean and
median ratio R_min / R0 for the two paper maps and three alternative building layouts.

Usage:
  python experiments/probe_exposure_headroom.py
"""

from __future__ import annotations

import random
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fps_priority_ai.astar import astar_search
from fps_priority_ai.world import GridWorld, euclidean

PROTECTED = {(2, 2), (22, 22), (22, 2)}


def exposure_fn(world: GridWorld, enemies):
    cache = {}

    def E(v):
        if v not in cache:
            cache[v] = sum((1.0 if world.los_clear(v, ep) else 0.2) / max(euclidean(v, ep), 0.5) for ep in enemies)
        return cache[v]
    return E


def headroom(world: GridWorld, pairs: int = 300, seed: int = 1):
    rng = random.Random(seed)
    free = [(x, y) for x in range(world.width) for y in range(world.height) if world.passable((x, y))]
    ratios = []
    for _ in range(pairs):
        s, g = rng.sample(free, 2)
        E = exposure_fn(world, rng.sample(free, 2))

        def plan(lam):
            res = astar_search(world, s, g, step_cost=lambda u, v: 1.0 + lam * E(v))
            return res.path if res else None
        p0, p1 = plan(0.0), plan(50.0)
        if p0 and p1:
            r0 = sum(E(v) for v in p0[1:])
            if r0 > 0:
                ratios.append(sum(E(v) for v in p1[1:]) / r0)
    return st.mean(ratios), st.median(ratios)


def custom_buildings(seed: int, density: float, shape, prot=PROTECTED) -> GridWorld:
    rng = random.Random(seed)
    zone = {(px + dx, py + dy) for (px, py) in prot for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    obstacles, reserved, target = set(), set(), int(density * 625)
    for _ in range(8000):
        if len(obstacles) >= target:
            break
        w, h = shape(rng)
        x0, y0 = rng.randint(1, 24 - w), rng.randint(1, 24 - h)
        cells = {(x, y) for x in range(x0, x0 + w) for y in range(y0, y0 + h)}
        if cells & zone or cells & reserved:
            continue
        obstacles |= cells
        reserved |= {(x, y) for x in range(x0 - 1, x0 + w + 1) for y in range(y0 - 1, y0 + h + 1)}
    return GridWorld(25, 25, obstacles)


def main() -> None:
    big = lambda r: (r.randint(3, 6), r.randint(3, 6))
    wall = lambda r: (1, r.randint(4, 8)) if r.random() < 0.5 else (r.randint(4, 8), 1)
    mixed = lambda r: big(r) if r.random() < 0.5 else wall(r)
    layouts = {
        "random map (paper, seed 7)": GridWorld.random_world(25, 25, 0.18, 7, PROTECTED),
        "urban map (paper, seed 11)": GridWorld.building_world(25, 25, 11, 0.25, 2, 4, PROTECTED),
        "large blocks 3-6": custom_buildings(11, 0.30, big),
        "long walls 1x4-8": custom_buildings(11, 0.20, wall),
        "mixed blocks/walls": custom_buildings(11, 0.28, mixed),
    }
    for name, world in layouts.items():
        m, med = headroom(world)
        print(f"{name:28s} density {len(world.obstacles) / 625:.3f}  R_min/R0 mean {m:.3f} median {med:.3f}")


if __name__ == "__main__":
    main()
