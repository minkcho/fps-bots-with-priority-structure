"""Map descriptors (2026-09-25): measurable properties of every registered map, for the "Test environments"
chapter and for relating hypothesis results to map properties.

Per map:
  density        obstacle cells / all cells
  path A, path B mean shortest-path length from the team's two spawn cells to the objective (balance)
  visibility     mean number of free cells within the view radius (9) and in line of sight of a free cell
  cover          share of free cells with at least one obstacle among their 4 neighbours
  diversity      length of the shortest spawn->objective path that avoids the interior cells of the first shortest
                 path, relative to the shortest path (mean over the two teams' first spawn cells; inf = no such path)
  area           number of free cells reachable from the spawn cells (playable area)
  cut            minimum number of free cells whose removal separates the two teams' spawn zones (free cells within
                 Chebyshev distance 2 of a team's spawn cells); by Menger's theorem the number of vertex-disjoint
                 paths between the zones, i.e. the total width of the map's narrowest cross-section (chokepoints).
                 (Replaces the first draft's count of disjoint paths between single spawn cells, which a spawn
                 cell's four neighbours bound.)
  headroom       expected-hits exposure retained by the safest path relative to the shortest path, over 300 random
                 start-goal pairs with two random opponents (the procedure of probe_h3_headroom.py, expected-hits
                 field); lower = more exposure can be avoided by route choice
Usage: python experiments/analyze_map_descriptors.py --out ../repro_outputs/maps [--maps random,urban,...]
         [--tex ../new_paper/tables/map_descriptors.tex]
"""
from __future__ import annotations

import argparse
import csv
import math
import random
import statistics as st
import sys
from collections import deque
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fps_priority_ai.env import build_world  # noqa: E402
from fps_priority_ai.maps import CONFIRMATION_MAPS, MAPS, component, key_cells  # noqa: E402
from fps_priority_ai.world import euclidean, manhattan  # noqa: E402
from probe_h3_headroom import DEFS, dijkstra  # noqa: E402

VIEW = 9
HITS = "hits: 1[LOS and d<=7] P_hit(d)"


def bfs_len(world, start, goal, blocked=frozenset()):
    """Shortest 4-connected path length from start to goal avoiding `blocked` (None if unreachable)."""
    if start == goal:
        return 0
    seen, queue = {start: 0}, deque([start])
    while queue:
        u = queue.popleft()
        for v in world.neighbors4(u):
            if v in blocked or v in seen:
                continue
            seen[v] = seen[u] + 1
            if v == goal:
                return seen[v]
            queue.append(v)
    return None


def shortest_path(world, start, goal):
    return dijkstra(world, start, goal, lambda v: 1.0)


def zone(world, cells, radius: int = 2) -> set:
    return {(x, y) for x in range(world.width) for y in range(world.height) if world.passable((x, y))
            and any(max(abs(x - c[0]), abs(y - c[1])) <= radius for c in cells)}


def min_cut(world, zone_a: set, zone_b: set) -> int:
    """Minimum vertex cut between two cell sets = number of vertex-disjoint paths between them (unit node
    capacities outside the zones, Edmonds-Karp on the split graph with a super source and sink)."""
    free = [(x, y) for x in range(world.width) for y in range(world.height) if world.passable((x, y))]
    INF = 10 ** 9
    cap = {}

    def add(u, v, c):
        cap[(u, v)] = cap.get((u, v), 0) + c
        cap.setdefault((v, u), 0)
    for c in free:
        add((c, "in"), (c, "out"), INF if (c in zone_a or c in zone_b) else 1)
        for n in world.neighbors4(c):
            add((c, "out"), (n, "in"), INF)
    for c in zone_a:
        add("S", (c, "in"), INF)
    for c in zone_b:
        add((c, "out"), "T", INF)
    adj = {}
    for (u, v) in cap:
        adj.setdefault(u, []).append(v)
    src, snk, flow = "S", "T", 0
    while True:
        prev, queue = {src: None}, deque([src])
        while queue and snk not in prev:
            u = queue.popleft()
            for v in adj.get(u, []):
                if v not in prev and cap[(u, v)] > 0:
                    prev[v] = u
                    queue.append(v)
        if snk not in prev:
            return flow
        v = snk
        while prev[v] is not None:
            u = prev[v]
            cap[(u, v)] -= 1
            cap[(v, u)] += 1
            v = u
        flow += 1
        if flow > len(free):      # zones touch: no finite cut
            return flow


def descriptors(name: str) -> dict:
    cfg = MAPS[name]
    world = build_world(cfg)
    keys = key_cells(cfg, world)
    comp = component(world, keys[0])
    free = sorted(comp)
    density = len(world.obstacles) / (world.width * world.height)
    obj = cfg.objective
    path_a = st.mean(bfs_len(world, c, obj) for c in keys[0:2])
    path_b = st.mean(bfs_len(world, c, obj) for c in keys[2:4])
    vis = st.mean(sum(1 for c in free if c != s and euclidean(c, s) <= VIEW and world.los_clear(s, c)) for s in free)
    cover = st.mean(float(any(world.in_bounds(n) and not world.passable(n)
                              for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))) for (x, y) in free)
    div = []
    for s in (keys[0], keys[2]):
        p = shortest_path(world, s, obj)
        alt = bfs_len(world, s, obj, blocked=frozenset(p[1:-1]))
        div.append(alt / (len(p) - 1) if alt is not None else math.inf)
    cut = min_cut(world, zone(world, keys[0:2]), zone(world, keys[2:4]))
    # headroom with the expected-hits field (same sampling as probe_h3_headroom.py, within the main component)
    rng = random.Random(1)
    f = DEFS[HITS]
    samples = []
    while len(samples) < 300:
        s, g, e1, e2 = rng.sample(free, 4)
        if manhattan(s, g) >= 8:
            samples.append((s, g, [e1, e2]))
    ratios = []
    for s, g, E in samples:
        cache = {}

        def rk(v, E=E, cache=cache):
            if v not in cache:
                cache[v] = f(world, v, E)
            return cache[v]
        p0 = dijkstra(world, s, g, lambda v: 1.0)
        ps = dijkstra(world, s, g, lambda v: 1e-3 + rk(v))
        r0 = sum(rk(v) for v in p0[1:])
        if r0 > 1e-9:
            ratios.append(sum(rk(v) for v in ps[1:]) / r0)
    return {"map": name, "layout": cfg.layout, "seed": cfg.seed, "density": round(density, 3), "area": len(comp),
            "path_a": round(path_a, 1), "path_b": round(path_b, 1), "visibility": round(vis, 1),
            "cover": round(cover, 3), "diversity": round(st.mean(div), 2), "cut": cut,
            "headroom": round(st.mean(ratios), 3)}


def tex_table(rows) -> str:
    lines = ["\\begin{tabular}{lcccccccc}", "\\toprule",
             "Map & Density & Area & Path to objective (team 0 / 1) & Visibility & Cover & Path diversity & Cut & Headroom \\\\",
             "\\midrule"]
    for r in rows:
        name = r["map"].replace("_", "\\_")   # outside the f-string (Python < 3.12 on the server)
        lines.append(f"{name} & {r['density']:.2f} & {r['area']} & {r['path_a']:.0f} / {r['path_b']:.0f} & "
                     f"{r['visibility']:.0f} & {r['cover']:.2f} & {r['diversity']:.2f} & {r['cut']} & {r['headroom']:.2f} \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="../repro_outputs/maps")
    p.add_argument("--maps", default=None, help="comma-separated map names (default: the confirmation maps, then the rest)")
    p.add_argument("--tex", default=None)
    p.add_argument("--jobs", type=int, default=8)
    a = p.parse_args()
    names = a.maps.split(",") if a.maps else list(CONFIRMATION_MAPS) + [m for m in MAPS if m not in CONFIRMATION_MAPS]
    with Pool(min(len(names), a.jobs)) as pool:
        rows = pool.map(descriptors, names)
    for r in rows:
        print(r, flush=True)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    with (out / "descriptors.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    md = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * len(rows[0])]
    md += ["| " + " | ".join(str(v) for v in r.values()) + " |" for r in rows]
    (out / "descriptors.md").write_text("\n".join(md) + "\n")
    if a.tex:
        Path(a.tex).write_text(tex_table(rows) + "\n")
    print(f"saved {out}/descriptors.csv")


if __name__ == "__main__":
    main()
