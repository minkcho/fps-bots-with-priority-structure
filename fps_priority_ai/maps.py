"""Map registry (2026-09-25).

- Base maps of the paper: "random" (scattered obstacles, seed 7) and "urban" (buildings, seed 11).
- Map sample for the pre-registered confirmation run: new seeds of the two generators and three alternative
  building layouts ("blocks", "walls", "mixed"). Generator seeds are the first three seeds from 101 upward whose
  map passes the reachability check (`first_valid_seeds`); they are fixed below and re-checked on import.
- Game-inspired maps (one per reconstructed game; `maps_game.py`): symmetric hand-designed layouts with fixed
  spawn and item cells (approved in the design review and frozen on 2026-09-25).

Every registered map is checked on import: both teams' spawn cells, the objective and any fixed item cells must
be passable and lie in one connected component of the free cells (`check_map`).
"""
from __future__ import annotations

import random
from collections import deque
from dataclasses import replace
from typing import Callable, Dict, Iterable, List, Set, Tuple

from .config import MapConfig, Vec2
from .env import build_world, spawn_position
from .maps_game import GAME_MAPS
from .world import GridWorld

BASE_MAPS: Dict[str, MapConfig] = {
    "random": MapConfig(width=25, height=25, obstacle_density=0.18, seed=7),
    "urban": MapConfig(width=25, height=25, seed=11, layout="buildings", building_density=0.25),
}


def key_cells(cfg: MapConfig, world: GridWorld, agents_per_team: int = 2) -> List[Vec2]:
    """Spawn cells of both teams and the objective."""
    cells = [spawn_position(cfg, world, t, i) for t in (0, 1) for i in range(agents_per_team)]
    return cells + [cfg.objective]


def component(world: GridWorld, start: Vec2) -> Set[Vec2]:
    seen, queue = {start}, deque([start])
    while queue:
        x, y = queue.popleft()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if n not in seen and world.passable(n):
                seen.add(n)
                queue.append(n)
    return seen


def map_ok(cfg: MapConfig) -> bool:
    world = build_world(cfg)
    cells = key_cells(cfg, world)
    if not all(world.passable(c) for c in cells):
        return False
    cells += [pos for _, pos in cfg.item_cells]
    if not all(world.passable(c) for c in cells):
        return False
    comp = component(world, cells[0])
    return all(c in comp for c in cells)


def check_map(name: str, cfg: MapConfig) -> None:
    if not map_ok(cfg):
        raise ValueError(f"map {name!r}: spawn cells and objective are not all passable and connected")


def first_valid_seeds(base: MapConfig, start: int = 101, count: int = 3) -> List[int]:
    """Selection rule of the map sample: the first `count` seeds from `start` upward that pass the check."""
    seeds, s = [], start
    while len(seeds) < count:
        if map_ok(replace(base, seed=s)):
            seeds.append(s)
        s += 1
    return seeds


# Fixed result of first_valid_seeds(...) (recomputed and compared in tests/test_maps.py).
SAMPLE_SEEDS = {"random": (101, 102, 103), "urban": (101, 102, 103)}


def _custom_buildings(seed: int, density: float, shape: Callable[[random.Random], Tuple[int, int]],
                      protected: Iterable[Vec2], size: int = 25) -> Tuple[Vec2, ...]:
    """Rectangular obstacles of a given shape with a one-cell street around each and a free 3x3 zone around the
    protected cells (the generator of experiments/probe_exposure_headroom.py, with the secondary spawn cells
    protected as well)."""
    rng = random.Random(seed)
    zone = {(px + dx, py + dy) for (px, py) in protected for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    obstacles: Set[Vec2] = set()
    reserved: Set[Vec2] = set()
    target = int(density * size * size)
    for _ in range(8000):
        if len(obstacles) >= target:
            break
        w, h = shape(rng)
        x0, y0 = rng.randint(1, size - 1 - w), rng.randint(1, size - 1 - h)
        cells = {(x, y) for x in range(x0, x0 + w) for y in range(y0, y0 + h)}
        if cells & zone or cells & reserved:
            continue
        obstacles |= cells
        reserved |= {(x, y) for x in range(x0 - 1, x0 + w + 1) for y in range(y0 - 1, y0 + h + 1)}
    return tuple(sorted(obstacles))


def _big(r: random.Random) -> Tuple[int, int]:
    return r.randint(3, 6), r.randint(3, 6)


def _wall(r: random.Random) -> Tuple[int, int]:
    return (1, r.randint(4, 8)) if r.random() < 0.5 else (r.randint(4, 8), 1)


def _mixed(r: random.Random) -> Tuple[int, int]:
    return _big(r) if r.random() < 0.5 else _wall(r)


def _alternative_layouts() -> Dict[str, MapConfig]:
    base = MapConfig(width=25, height=25, seed=11, layout="custom")
    protected = [base.spawn_a, base.spawn_b, base.objective, (4, 2), (20, 22)]
    return {
        "blocks": replace(base, obstacles=_custom_buildings(11, 0.30, _big, protected)),
        "walls": replace(base, obstacles=_custom_buildings(11, 0.20, _wall, protected)),
        "mixed": replace(base, obstacles=_custom_buildings(11, 0.28, _mixed, protected)),
    }


def _sample_maps() -> Dict[str, MapConfig]:
    maps = {}
    for kind in ("random", "urban"):
        for s in SAMPLE_SEEDS[kind]:
            maps[f"{kind}_s{s}"] = replace(BASE_MAPS[kind], seed=s)
    maps.update(_alternative_layouts())
    return maps


MAPS: Dict[str, MapConfig] = {**BASE_MAPS, **_sample_maps(), **GAME_MAPS}
# The 11 maps of the pre-registered confirmation run (2026-09-25).
CONFIRMATION_MAPS: Tuple[str, ...] = ("random", "urban", "random_s101", "random_s102", "random_s103",
                                      "urban_s101", "urban_s102", "urban_s103", "blocks", "walls", "mixed")

for _name, _cfg in MAPS.items():
    check_map(_name, _cfg)
