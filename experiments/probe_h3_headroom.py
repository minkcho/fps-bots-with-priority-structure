"""H3 probe 0: structural headroom of the route channel under exposure definitions (2026-09-22).

For 300 random start-goal pairs with two random opponents, compare the shortest path with the
safest path (minimum exposure, length as tie-break) under each exposure definition: exposure
ratio safest/shortest, length ratio, and lambda* = dL/dR, the weight at which the safest path
becomes cheaper than the shortest one under the additive cost 1 + lambda * E.
Usage: python experiments/probe_h3_headroom.py > ../repro_outputs/h3_transit/headroom.txt
"""
from __future__ import annotations

import heapq
import random
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fps_priority_ai.config import AgentConfig, WeaponConfig  # noqa: E402
from fps_priority_ai.env import FPSEnv  # noqa: E402
from fps_priority_ai.experiment import MAPS  # noqa: E402
from fps_priority_ai.runner import default_scenarios, default_styles  # noqa: E402
from fps_priority_ai.world import euclidean, manhattan  # noqa: E402

R_VIEW, R_WPN = 9, 7


def phit(d):
    return 0.55 * max(0.05, 1 - 0.7 * d / 7)


DEFS = {
    "distance (v2): LOS 1/d, else 0.2/d": lambda w, v, E: sum((1.0 if w.los_clear(v, e) else 0.2) / max(euclidean(v, e), 0.5) for e in E),
    "LOS only: 1/d if LOS else 0": lambda w, v, E: sum((1.0 / max(euclidean(v, e), 0.5)) if w.los_clear(v, e) else 0.0 for e in E),
    "visible indicator: 1[LOS and d<=9]": lambda w, v, E: sum(1.0 for e in E if euclidean(v, e) <= R_VIEW and w.los_clear(v, e)),
    "hits: 1[LOS and d<=7] P_hit(d)": lambda w, v, E: sum(phit(euclidean(v, e)) for e in E if euclidean(v, e) <= R_WPN and w.los_clear(v, e)),
}


def dijkstra(world, start, goal, cost):
    dist = {start: 0.0}; prev = {start: None}; pq = [(0.0, 0, start)]; c = 0
    while pq:
        d, _, u = heapq.heappop(pq)
        if u == goal:
            break
        if d > dist[u]:
            continue
        for v in world.neighbors4(u):
            nd = d + cost(v)
            if nd < dist.get(v, float("inf")):
                dist[v] = nd; prev[v] = u; c += 1; heapq.heappush(pq, (nd, c, v))
    p = []; n = goal
    while n is not None:
        p.append(n); n = prev[n]
    return p[::-1]


def main() -> None:
    styles = default_styles("exp")
    sc = [s for s in default_scenarios() if s.name == "Deathmatch"][0]
    rng = random.Random(1)
    print("map | definition | R0 per step | safest/shortest exposure | length ratio | pairs with R0>0 | lambda* median | lambda* p75")
    for mname in ("random", "urban"):
        env = FPSEnv(map_cfg=MAPS[mname], agent_cfg=AgentConfig(), weapon_cfg=WeaponConfig(), scenario=sc, styles=styles, rng=random.Random(1))
        world = env.world
        cells = [(x, y) for x in range(world.width) for y in range(world.height) if world.passable((x, y))]
        samples = []
        while len(samples) < 300:
            s, g, e1, e2 = rng.sample(cells, 4)
            if manhattan(s, g) >= 8:
                samples.append((s, g, [e1, e2]))
        for name, f in DEFS.items():
            ratios, lens, r0s, lstars, nz = [], [], [], [], 0
            for s, g, E in samples:
                cache = {}
                def rk(v):
                    if v not in cache:
                        cache[v] = f(world, v, E)
                    return cache[v]
                p0 = dijkstra(world, s, g, lambda v: 1.0)
                ps = dijkstra(world, s, g, lambda v: 1e-3 + rk(v))
                R0 = sum(rk(v) for v in p0[1:]); Rs = sum(rk(v) for v in ps[1:])
                L0, Ls = len(p0) - 1, len(ps) - 1
                r0s.append(R0 / L0)
                if R0 > 1e-9:
                    nz += 1; ratios.append(Rs / R0); lens.append(Ls / L0)
                    if R0 - Rs > 1e-9 and Ls > L0:
                        lstars.append((Ls - L0) / (R0 - Rs))
            q = lambda xs, p: sorted(xs)[int(p * (len(xs) - 1))] if xs else float("nan")
            print(f"{mname} | {name} | {st.mean(r0s):.3f} | {st.mean(ratios):.3f} | {st.mean(lens):.3f} | {nz} | {q(lstars, 0.5):.2f} | {q(lstars, 0.75):.2f}")


if __name__ == "__main__":
    main()
