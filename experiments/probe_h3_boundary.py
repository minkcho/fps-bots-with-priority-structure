"""H3 probe 2: detour decision boundary of each route-cost form (2026-09-22).

Planning calls only (no simulation). On a corridor map whose covered detour is dL steps longer
than the exposed direct route, and with 1 or 2 stationary sentries covering the direct route,
find for each (exposure model, cost form) the smallest lambda_E at which the first plan takes
the detour. For the additive expected-hits cost the boundary is lambda_E = dL / dR exactly
(dR = expected hits on the direct route); the other forms trade time against risk with a
different shape. Usage: python experiments/probe_h3_boundary.py
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from probe_h3_transit import TransitEnv, transit_style, hits_at, WPN  # noqa: E402
from fps_priority_ai.astar import astar_search  # noqa: E402
from fps_priority_ai.config import AgentConfig, MapConfig, ScenarioConfig, WeaponConfig  # noqa: E402
from fps_priority_ai.runner import default_styles  # noqa: E402
from fps_priority_ai.world import GridWorld, euclidean  # noqa: E402


def corridor_world(h: int) -> GridWorld:
    """Corridor y=12 (x=6..18) with sentry notch above; solid block y=13..12+h below, so the
    covered detour via y=13+h is 2*(h+1) steps longer than the 20-step direct route."""
    obs = set()
    for x in range(6, 19):
        for y in range(0, 11):
            if not (8 <= y <= 10 and 9 <= x <= 15):
                obs.add((x, y))
        obs.add((x, 11))
        for y in range(13, 13 + h):
            obs.add((x, y))
    for x in range(10, 15):
        obs.discard((x, 11))
    return GridWorld(width=25, height=25, obstacles=obs)


LAMS = [0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30, 40, 60, 100]
FORMS = [("hits", "additive"), ("hits", "exp"), ("hits", "square"), ("distance", "additive"), ("distance", "exp")]


def first_plan_detours(world, cfg, n_sentries, style, direct_len):
    sc = ScenarioConfig(name="Transit", mode="mission", max_steps=1, num_agents_per_team=n_sentries, opponent_style="Aggressive")
    TransitEnv.custom_world = world
    styles = default_styles("exp")
    env = TransitEnv(map_cfg=cfg, agent_cfg=AgentConfig(), weapon_cfg=WeaponConfig(), scenario=sc,
                     styles={**styles, style.name: style}, rng=random.Random(0))
    env.set_team_styles(evaluated_style=style.name)
    path = env.policies[0]._plan(env.world, env.agents[0], env.agents, cfg.objective)
    return (len(path) - 1) > direct_len, len(path) - 1


def main() -> None:
    cfg0 = MapConfig(seed=7, num_health=0, num_ammo=0, spawn_a=(2, 12), spawn_b=(12, 8), objective=(22, 12))
    print(f"{'dL':>3s} {'sentries':>8s} {'dR(hits)':>8s} {'dL/dR':>6s} | " + " ".join(f"{e[:4]}/{c[:4]:>5s}" for e, c in FORMS))
    for h in (1, 3, 5, 8, 11):
        world = corridor_world(h)
        direct = astar_search(world, cfg0.spawn_a, cfg0.objective, step_cost=lambda u, v: 1.0).path
        direct_len = len(direct) - 1
        for n_s in (1, 2):
            dR = n_s * sum(hits_at(world, q, [cfg0.spawn_b]) for q in direct[1:])
            dL = 2 * (h + 1)
            cells = []
            for expo, cost in FORMS:
                lam_switch = None
                for lam in LAMS:
                    style = transit_style("T", lam, expo, cost)
                    det, L = first_plan_detours(world, cfg0, n_s, style, direct_len)
                    if det:
                        lam_switch = lam
                        break
                cells.append(f"{lam_switch if lam_switch is not None else '>100':>10}")
            print(f"{dL:3d} {n_s:8d} {dR:8.2f} {dL/dR:6.2f} | " + " ".join(cells))


if __name__ == "__main__":
    main()
