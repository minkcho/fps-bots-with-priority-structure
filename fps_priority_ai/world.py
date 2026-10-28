from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Set, Tuple

import math
import os
import random

# Symmetric line of sight (2026-09-25): the Bresenham line from a to b can differ from the line from b to a, so
# one agent could see another that does not see it. With FPS_SYMMETRIC_LOS=1 the line is always traced from
# the lexicographically smaller end point. Off by default (the paper's final run).
SYMMETRIC_LOS = os.environ.get("FPS_SYMMETRIC_LOS", "0") == "1"
# Reachable placement (2026-09-25): items and random targets (roam points) only on free cells reachable from the
# spawn cells (a generated map can contain isolated free cells, e.g. one on the random map of seed 7, and an item
# there cannot be picked up). With FPS_REACHABLE_PLACEMENT=1, build_world sets GridWorld.reachable. Off by default.
REACHABLE_PLACEMENT = os.environ.get("FPS_REACHABLE_PLACEMENT", "0") == "1"

Vec2 = Tuple[int, int]


def manhattan(a: Vec2, b: Vec2) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean(a: Vec2, b: Vec2) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def bresenham_line(a: Vec2, b: Vec2) -> List[Vec2]:
    """Return list of grid cells on the line from a to b inclusive."""
    x0, y0 = a
    x1, y1 = b
    points: List[Vec2] = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = 1 if x1 >= x0 else -1
    sy = 1 if y1 >= y0 else -1

    if dy <= dx:
        err = dx / 2.0
        while x != x1:
            points.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y1:
            points.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy

    points.append((x1, y1))
    return points


@dataclass
class GridWorld:
    width: int
    height: int
    obstacles: Set[Vec2]
    # cells that random_empty_cell may return (None: every free cell; see REACHABLE_PLACEMENT)
    reachable: Optional[Set[Vec2]] = None

    @classmethod
    def random_world(
        cls,
        width: int,
        height: int,
        obstacle_density: float,
        seed: int,
        protected: Optional[Set[Vec2]] = None,
    ) -> "GridWorld":
        rng = random.Random(seed)
        protected = protected or set()
        obstacles: Set[Vec2] = set()
        for x in range(width):
            for y in range(height):
                if (x, y) in protected:
                    continue
                # Keep a border mostly free to reduce trapped areas.
                border = x in (0, width - 1) or y in (0, height - 1)
                p = obstacle_density * (0.25 if border else 1.0)
                if rng.random() < p:
                    obstacles.add((x, y))
        return cls(width=width, height=height, obstacles=obstacles)

    @classmethod
    def building_world(
        cls,
        width: int,
        height: int,
        seed: int,
        target_density: float = 0.25,
        min_size: int = 2,
        max_size: int = 4,
        protected: Optional[Set[Vec2]] = None,
        max_attempts: int = 5000,
    ) -> "GridWorld":
        """Urban layout: rectangular buildings separated by one-cell streets.

        Buildings keep a one-cell gap to each other, to the map border, and to the
        protected cells (spawns, objective), so all free cells form one connected
        street network; building walls provide line-of-sight blocking and cover.
        """
        rng = random.Random(seed)
        protected = protected or set()
        blocked_zone: Set[Vec2] = set()
        for (px, py) in protected:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    blocked_zone.add((px + dx, py + dy))
        obstacles: Set[Vec2] = set()
        reserved: Set[Vec2] = set()  # building cells plus their one-cell margin
        target = int(target_density * width * height)
        for _ in range(max_attempts):
            if len(obstacles) >= target:
                break
            w = rng.randint(min_size, max_size)
            h = rng.randint(min_size, max_size)
            x0 = rng.randint(1, width - 1 - w)
            y0 = rng.randint(1, height - 1 - h)
            cells = {(x, y) for x in range(x0, x0 + w) for y in range(y0, y0 + h)}
            margin = {(x, y) for x in range(x0 - 1, x0 + w + 1) for y in range(y0 - 1, y0 + h + 1)}
            if cells & blocked_zone or cells & reserved:
                continue
            obstacles |= cells
            reserved |= margin
        return cls(width=width, height=height, obstacles=obstacles)

    def in_bounds(self, p: Vec2) -> bool:
        x, y = p
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, p: Vec2) -> bool:
        return p not in self.obstacles and self.in_bounds(p)

    def neighbors4(self, p: Vec2) -> List[Vec2]:
        x, y = p
        candidates = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        return [q for q in candidates if self.passable(q)]

    def los_clear(self, a: Vec2, b: Vec2) -> bool:
        """Line-of-sight: True if no obstacle blocks a->b (excluding endpoints)."""
        if SYMMETRIC_LOS and b < a:
            a, b = b, a
        for cell in bresenham_line(a, b)[1:-1]:
            if cell in self.obstacles:
                return False
        return True

    def cover_score(self, p: Vec2) -> float:
        """
        Cover heuristic in [0, 1].
        A cell has higher cover if it has obstacles adjacent in 4-neighborhood.
        """
        if p in self.obstacles:
            return 1.0
        x, y = p
        adj = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        k = 0
        for q in adj:
            if q in self.obstacles:
                k += 1
        return k / 4.0

    def random_empty_cell(self, rng: random.Random, protected: Optional[Set[Vec2]] = None) -> Vec2:
        protected = protected or set()
        while True:
            p = (rng.randrange(self.width), rng.randrange(self.height))
            if self.passable(p) and p not in protected and (self.reachable is None or p in self.reachable):
                return p

    def component(self, start: Vec2) -> Set[Vec2]:
        """Free cells 4-connected to start."""
        seen, frontier = {start}, [start]
        while frontier:
            nxt = []
            for p in frontier:
                for q in self.neighbors4(p):
                    if q not in seen:
                        seen.add(q)
                        nxt.append(q)
            frontier = nxt
        return seen


class BlockedView:
    """A GridWorld seen by the path search with extra impassable cells (local avoidance of a blocking agent,
    2026-09-25); line of sight, cover and everything else are those of the underlying world."""

    def __init__(self, world: GridWorld, blocked: Set[Vec2]):
        self._world = world
        self._blocked = set(blocked)

    def passable(self, p: Vec2) -> bool:
        return p not in self._blocked and self._world.passable(p)

    def neighbors4(self, p: Vec2) -> List[Vec2]:
        return [q for q in self._world.neighbors4(p) if q not in self._blocked]

    def __getattr__(self, name):
        return getattr(self._world, name)
