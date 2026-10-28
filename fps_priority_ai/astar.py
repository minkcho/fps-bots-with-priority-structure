from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple
import heapq
import math

from .world import GridWorld, manhattan, Vec2

HeuristicFn = Callable[[Vec2, Vec2], float]
StepCostFn = Callable[[Vec2, Vec2], float]


@dataclass
class AStarResult:
    path: List[Vec2]
    cost: float
    expanded: int


def astar_search(
    world: GridWorld,
    start: Vec2,
    goal: Vec2,
    step_cost: StepCostFn,
    heuristic: HeuristicFn = lambda a, b: float(manhattan(a, b)),
    max_expansions: int = 50_000,
) -> Optional[AStarResult]:
    """
    Generic A* on a 4-neighborhood grid.

    `step_cost(u, v)` should be >= 0.
    """
    if start == goal:
        return AStarResult(path=[start], cost=0.0, expanded=0)

    # Priority queue items: (f, g, node)
    frontier: List[Tuple[float, float, Vec2]] = []
    heapq.heappush(frontier, (heuristic(start, goal), 0.0, start))

    came_from: Dict[Vec2, Optional[Vec2]] = {start: None}
    g_score: Dict[Vec2, float] = {start: 0.0}

    expanded = 0

    while frontier:
        f, g, current = heapq.heappop(frontier)
        expanded += 1
        if expanded > max_expansions:
            return None

        if current == goal:
            # Reconstruct
            path: List[Vec2] = []
            node: Optional[Vec2] = current
            while node is not None:
                path.append(node)
                node = came_from[node]
            path.reverse()
            return AStarResult(path=path, cost=g_score[current], expanded=expanded)

        for nxt in world.neighbors4(current):
            step = step_cost(current, nxt)
            if step < 0:
                raise ValueError("step_cost must be non-negative")
            tentative = g_score[current] + step
            if nxt not in g_score or tentative < g_score[nxt]:
                came_from[nxt] = current
                g_score[nxt] = tentative
                priority = tentative + heuristic(nxt, goal)
                heapq.heappush(frontier, (priority, tentative, nxt))

    return None
