"""H3 probe: transit past a stationary sentry (2026-09-22).

Isolates the route channel: a transit agent (objective only, keep moving, no ammunition)
must reach the objective while a stationary sentry with a clear line of sight over the
direct route shoots at it. Every plan is made with the threat in range and in view, so
the probe answers whether the route cost can produce safer routes at all, and which cost
form / exposure model / weight does so. Two maps: a designed corridor map (exposed 20-step
corridor vs covered 32-step detour) and the paper's random map with a sentry placed where
it covers most of the direct route.

Usage: python experiments/probe_h3_transit.py --out ../repro_outputs/h3_transit --episodes 30
"""
from __future__ import annotations

import argparse
import csv
import dataclasses
import random
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fps_priority_ai.config import AgentConfig, MapConfig, PriorityWeights, ScenarioConfig, WeaponConfig  # noqa: E402
from fps_priority_ai.env import FPSEnv  # noqa: E402
from fps_priority_ai.experiment import MAPS, episode_seed  # noqa: E402
from fps_priority_ai.policy import PolicyOutput  # noqa: E402
from fps_priority_ai.runner import default_styles  # noqa: E402
from fps_priority_ai.world import GridWorld, euclidean, manhattan  # noqa: E402
from fps_priority_ai.astar import astar_search  # noqa: E402

WPN = WeaponConfig()


def hit_prob(d: float) -> float:
    return WPN.base_accuracy * max(0.05, 1.0 - 0.7 * d / max(1.0, float(WPN.range_cells)))


def hits_at(world: GridWorld, v, enemies) -> float:
    return sum(hit_prob(euclidean(v, e)) for e in enemies
               if euclidean(v, e) <= WPN.range_cells and world.los_clear(v, e))


def corridor_world() -> GridWorld:
    """25x25: corridor y=12 between x=6..18 walled above (y<=10, except a sentry notch) and
    below (y=13..17); sentry notch y=8..10, x=9..15 opens onto the corridor through a window
    in row y=11 (x=10..14). Direct route 20 steps (exposed), detour via y=18 is 32 steps."""
    obs = set()
    for x in range(6, 19):
        for y in range(0, 11):
            if not (8 <= y <= 10 and 9 <= x <= 15):
                obs.add((x, y))
        obs.add((x, 11))
        for y in range(13, 18):
            obs.add((x, y))
    for x in range(10, 15):
        obs.discard((x, 11))          # window between notch and corridor
    return GridWorld(width=25, height=25, obstacles=obs)


def best_sentry_cell(world: GridWorld, start, goal):
    """Passable cell (not on the direct route) covering the most direct-route cells in LOS+range."""
    res = astar_search(world, start, goal, step_cost=lambda u, v: 1.0)
    path = res.path
    onpath = set(path)
    best, best_n = None, -1
    for x in range(world.width):
        for y in range(world.height):
            c = (x, y)
            if not world.passable(c) or c in onpath or c in (start, goal):
                continue
            n = sum(1 for p in path if euclidean(p, c) <= WPN.range_cells and world.los_clear(p, c))
            if n > best_n:
                best, best_n = c, n
    return best, best_n, path


def transit_style(name: str, lam: float, exposure_model: str, route_cost: str) -> PriorityWeights:
    return PriorityWeights(name=name, w_objective=2.0, w_engage=0.0, w_resource=0.0, w_team=0.0,
                           w_commitment=1.0, w_exposure=lam, w_cover=0.0, w_teammate_sep=0.0,
                           combat_mode_override=1, exposure_model=exposure_model, route_cost=route_cost,
                           route_diagnostics=True)


class TransitEnv(FPSEnv):
    """FPSEnv whose world is replaced by a given map, whose sentries (team 1) never move, and
    whose transit agent (agent 0) never has ammunition. run_episode() re-runs __init__ and
    set_team_styles(), so all three overrides are applied on every episode."""
    custom_world: GridWorld = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.custom_world is not None:
            self.world = self.custom_world
        self.agents[0].ammo = 0

    def set_team_styles(self, evaluated_style: str) -> None:
        super().set_team_styles(evaluated_style)
        for aid, agent in self.agents.items():
            if agent.team != 1:
                continue
            pol = self.policies[aid]
            orig = pol.decide

            def frozen(*a, _orig=orig, **k):
                out = _orig(*a, **k)
                return PolicyOutput(goal_type=out.goal_type, goal_pos=out.goal_pos, move_to=None,
                                    allow_move=False, shoot_target=out.shoot_target)
            pol.decide = frozen

    def step(self):
        self.agents[0].ammo = 0
        return super().step()


def run_episode(map_name: str, world: GridWorld, map_cfg: MapConfig, style: PriorityWeights, ep: int, max_steps: int):
    styles = default_styles("exp")
    sc = ScenarioConfig(name="Transit", mode="mission", max_steps=max_steps, num_agents_per_team=1,
                        opponent_style="Aggressive")
    TransitEnv.custom_world = world
    env = TransitEnv(map_cfg=map_cfg, agent_cfg=AgentConfig(), weapon_cfg=WeaponConfig(), scenario=sc,
                     styles={**styles, style.name: style}, rng=random.Random(episode_seed(2026, "Transit", ep)))
    res = env.run_episode(evaluated_style=style.name)
    sentry_ids = [a.agent_id for a in env.agents.values() if a.team == 1]
    assert all(env.agents[a].pos == map_cfg.spawn_b for a in sentry_ids), "sentry moved"
    assert env.world is world

    goal = map_cfg.objective
    sentries = [env.agents[a].pos for a in sentry_ids]
    steps0 = sorted((l.step, l) for l in res.logs if l.agent_id == 0)
    arrival = next((s for s, l in steps0 if l.pos == goal), None)
    logged = set(s for s, _ in steps0)
    death_step = next((s for s in range(1, max_steps + 1) if s not in logged), None)
    first_life = [l for s, l in steps0 if death_step is None or s < death_step]
    if arrival is not None:
        first_life = [l for l in first_life if l.step <= arrival]
    walked_hits = sum(hits_at(world, l.pos, sentries) for l in first_life)
    los_steps = sum(1 for l in first_life if any(euclidean(l.pos, e) <= WPN.range_cells and world.los_clear(l.pos, e) for e in sentries))
    arrived_first_life = arrival is not None and (death_step is None or arrival < death_step)
    logs = env.policies[0].route_log
    detour = st.mean(r[2] for r in logs) if logs else float("nan")
    len_ratio = st.mean(r[0] / r[1] for r in logs if r[1] > 0) if any(r[1] > 0 for r in logs) else float("nan")
    return dict(map=map_name, cost=style.route_cost, exposure=style.exposure_model, lam=style.w_exposure, episode=ep,
                arrived=int(arrived_first_life), arrival_step=arrival if arrival is not None else "",
                died_first_life=int(death_step is not None and (arrival is None or death_step < arrival)),
                walked_steps=len(first_life), los_steps=los_steps,
                walked_hits=round(walked_hits, 4), health_end=env.agents[0].health,
                plan_detour=round(detour, 4), plan_len_ratio=round(len_ratio, 4))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=str, default="../repro_outputs/h3_transit")
    p.add_argument("--episodes", type=int, default=30)
    args = p.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)

    # Map 1: designed corridor. Map 2: the paper's random map (seed 7) with a chosen sentry cell.
    maps = {}
    cw = corridor_world()
    maps["corridor"] = (cw, MapConfig(seed=7, num_health=0, num_ammo=0, spawn_a=(2, 12), spawn_b=(12, 8), objective=(22, 12)), 70)
    base = MAPS["random"]
    env0 = FPSEnv(map_cfg=base, agent_cfg=AgentConfig(), weapon_cfg=WeaponConfig(),
                  scenario=ScenarioConfig(name="x", mode="mission", max_steps=1, num_agents_per_team=1),
                  styles=default_styles("exp"), rng=random.Random(0))
    rw = env0.world
    cell, n_cov, path = best_sentry_cell(rw, base.spawn_a, base.objective)
    maps["random7"] = (rw, dataclasses.replace(base, num_health=0, num_ammo=0, spawn_b=cell), 90)
    for name, (w, cfg, T) in maps.items():
        c, n, pth = best_sentry_cell(w, cfg.spawn_a, cfg.objective) if name == "random7" else (cfg.spawn_b, None, None)
        res = astar_search(w, cfg.spawn_a, cfg.objective, step_cost=lambda u, v: 1.0)
        direct = res.path
        exposed = sum(1 for q in direct if euclidean(q, cfg.spawn_b) <= WPN.range_cells and w.los_clear(q, cfg.spawn_b))
        eh = sum(hits_at(w, q, [cfg.spawn_b]) for q in direct[1:])
        print(f"[{name}] sentry at {cfg.spawn_b}; direct route {len(direct)-1} steps, {exposed} cells in LOS+range, "
              f"expected hits on direct route {eh:.2f}; max_steps {T}")

    conditions = []
    for lam in (0.0, 0.55, 5.5, 12.0, 20.0):
        conditions.append(("distance", "additive", lam))
    for lam in (0.5, 1.0, 2.0, 5.0, 10.0, 20.0):
        conditions.append(("hits", "additive", lam))
    for lam in (0.5, 1.0, 2.0, 5.0, 10.0):
        conditions.append(("hits", "exp", lam))
    for lam in (0.55, 5.5, 12.0):
        conditions.append(("distance", "exp", lam))

    rows = []
    for name, (w, cfg, T) in maps.items():
        print(f"\n=== {name} === (n={args.episodes} per condition)")
        print(f"{'exposure':9s} {'cost':9s} {'lam':>6s} {'detour%':>8s} {'len ratio':>9s} {'LOS steps':>9s} {'walked hits':>11s} {'arrived%':>9s} {'died1st%':>8s} {'arrival':>8s}")
        for exposure, cost, lam in conditions:
            style = transit_style(f"Transit[{exposure}/{cost}/{lam}]", lam, exposure, cost)
            rr = [run_episode(name, w, cfg, style, ep, T) for ep in range(args.episodes)]
            rows += rr
            m = lambda k: st.mean(r[k] for r in rr)
            arr = [r["arrival_step"] for r in rr if r["arrived"]]
            print(f"{exposure:9s} {cost:9s} {lam:6.2f} {100*m('plan_detour'):8.1f} {m('plan_len_ratio'):9.3f} {m('los_steps'):9.2f} "
                  f"{m('walked_hits'):11.3f} {100*m('arrived'):9.1f} {100*m('died_first_life'):8.1f} {st.mean(arr) if arr else float('nan'):8.1f}")
    with (out / "transit.csv").open("w", newline="", encoding="utf-8") as f:
        wtr = csv.DictWriter(f, fieldnames=list(rows[0].keys())); wtr.writeheader(); wtr.writerows(rows)
    print(f"\nwrote {out / 'transit.csv'} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
