"""Cohesion probe (2026-09-23): does the route-level teammate term lambda_T bind a team when the
goal layer does not?

Two objective-only agents (w_Team = 0, so no regroup goal; keep-moving mode) spawn in different
corners and walk to a common objective. Opponents are present but frozen and unarmed, and the
exposure and cover weights are 0, so only the teammate term shapes routes. lambda_T in
{0, 0.3, 1, 3, 10} for each cost form (exp: attraction exp(-lambda_T * sum 1/d); additive and
square: separation penalty lambda_T * d/r_view). Maps: a designed block map (central 9x9 obstacle between the two routes), random, urban.
Metrics until the second arrival: mean ally distance while both are en route, merge step (first
step with ally distance <= 1.5), arrival steps (within one cell of the objective), and path length relative to the shortest path.
Usage: python experiments/probe_cohesion.py --map open --form exp --out ../repro_outputs/v3/cohesion
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

from fps_priority_ai.astar import astar_search  # noqa: E402
from fps_priority_ai.config import AgentConfig, MapConfig, PriorityWeights, ScenarioConfig, WeaponConfig  # noqa: E402
from fps_priority_ai.env import FPSEnv  # noqa: E402
from fps_priority_ai.experiment import MAPS, episode_seed  # noqa: E402
from fps_priority_ai.policy import PolicyOutput  # noqa: E402
from fps_priority_ai.runner import default_styles  # noqa: E402
from fps_priority_ai.world import GridWorld, euclidean  # noqa: E402

LAMS = [0.0, 0.3, 1.0, 3.0, 5.0, 10.0, 20.0]


def nearest_passable(world, c):
    best = None
    for x in range(world.width):
        for y in range(world.height):
            if world.passable((x, y)) and (best is None or euclidean((x, y), c) < euclidean(best, c)):
                best = (x, y)
    return best


class CohesionEnv(FPSEnv):
    custom_world: GridWorld = None
    spawns = ((2, 2), (2, 22))

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        if self.custom_world is not None:
            self.world = self.custom_world
            for aid, ag in self.agents.items():
                if ag.team == 0:
                    ag.pos = self._spawn_pos(0, aid)

    def _spawn_pos(self, team, index=0):
        if team == 0:
            return self.spawns[index % 2]
        return self.map_cfg.spawn_b

    def set_team_styles(self, evaluated_style):
        super().set_team_styles(evaluated_style)
        for aid, ag in self.agents.items():
            if ag.team == 1:
                pol = self.policies[aid]; orig = pol.decide

                def frozen(*a, _orig=orig, **k):
                    o = _orig(*a, **k)
                    return PolicyOutput(o.goal_type, o.goal_pos, None, False, None)
                pol.decide = frozen

    def step(self):
        for ag in self.agents.values():
            if ag.team == 1:
                ag.ammo = 0
        return super().step()


def style(form, lam, replan=0):
    return PriorityWeights(name=f"Coh[{form}/{lam:g}/r{replan}]", replan_interval=replan, w_objective=2.0, w_engage=0.0, w_resource=0.0, w_team=0.0,
                           w_commitment=1.0, w_exposure=0.0, w_cover=0.0, w_teammate_sep=lam,
                           combat_mode_override=1, route_cost=form, exposure_model="hits")


def world_for(map_name):
    if map_name == "block":
        # central 9x9 block: the two shortest routes pass on opposite sides, so travelling together costs a detour
        return GridWorld(width=25, height=25, obstacles={(x, y) for x in range(8, 17) for y in range(8, 17)})
    env0 = FPSEnv(map_cfg=MAPS[map_name], agent_cfg=AgentConfig(), weapon_cfg=WeaponConfig(),
                  scenario=ScenarioConfig(name="x", mode="mission", max_steps=1), styles=default_styles("exp"), rng=random.Random(0))
    return env0.world


def run_one(world, cfg, st_, ep, T=90):
    sc = ScenarioConfig(name="Cohesion", mode="mission", max_steps=T, num_agents_per_team=2, opponent_style="Aggressive")
    CohesionEnv.custom_world = world
    env = CohesionEnv(map_cfg=cfg, agent_cfg=AgentConfig(), weapon_cfg=WeaponConfig(), scenario=sc,
                      styles={**default_styles("exp"), st_.name: st_}, rng=random.Random(episode_seed(2026, "Cohesion", ep)))
    res = env.run_episode(evaluated_style=st_.name)
    goal = cfg.objective
    by = defaultdict(dict)
    for l in res.logs:
        if l.team == 0:
            by[l.step][l.agent_id] = l
    arrive = {}
    for s in sorted(by):
        for aid, l in by[s].items():
            if euclidean(l.pos, goal) <= 1.5 and aid not in arrive:
                arrive[aid] = s
    end = max(arrive.values()) if len(arrive) == 2 else T
    first = min(arrive.values()) if arrive else T
    d_route = [euclidean(*[x.pos for x in ag.values()]) for s, ag in sorted(by.items()) if s <= first and len(ag) == 2]
    merge = next((s for s, ag in sorted(by.items()) if len(ag) == 2 and euclidean(*[x.pos for x in ag.values()]) <= 1.5), "")
    shortest = [len(astar_search(world, sp, goal, step_cost=lambda u, v: 1.0).path) - 1 for sp in CohesionEnv.spawns]
    lens = [arrive[a] / shortest[a % 2] for a in arrive] if arrive else []
    return dict(ally_dist_en_route=round(st.mean(d_route), 3) if d_route else "", merge_step=merge,
                first_arrival=first, both_arrived=int(len(arrive) == 2), last_arrival=end if len(arrive) == 2 else "",
                arrival_len_ratio=round(st.mean(lens), 3) if lens else "")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--map", required=True, choices=["block", "random", "urban"])
    p.add_argument("--form", required=True, choices=["exp", "additive", "square"])
    p.add_argument("--episodes", type=int, default=30)
    p.add_argument("--replan", type=int, default=0)
    p.add_argument("--out", default="../repro_outputs/v3/cohesion")
    a = p.parse_args()
    world = world_for(a.map)
    CohesionEnv.spawns = (nearest_passable(world, (2, 2)), nearest_passable(world, (2, 22)))
    goal = nearest_passable(world, (22, 12))
    cfg = dataclasses.replace(MAPS["random"] if a.map == "block" else MAPS[a.map], num_health=0, num_ammo=0,
                              objective=goal, spawn_b=nearest_passable(world, (22, 22)), spawn_separation=0)
    rows = []
    for lam in LAMS:
        s = style(a.form, lam, a.replan)
        rs = [run_one(world, cfg, s, ep) for ep in range(a.episodes)]
        for ep, r in enumerate(rs):
            rows.append(dict(map=a.map, form=a.form, replan=a.replan, lam_T=lam, episode=ep, **r))
        m = lambda k: st.mean(float(r[k]) for r in rs if r[k] != "") if any(r[k] != "" for r in rs) else float("nan")
        print(f"{a.map:6s} {a.form:8s} r{a.replan} lamT={lam:<4g} ally en route {m('ally_dist_en_route'):.2f}  merge step {m('merge_step'):.1f} "
              f"(merged {sum(r['merge_step'] != '' for r in rs)}/{len(rs)})  both arrived {sum(r['both_arrived'] for r in rs)}/{len(rs)}  "
              f"last arrival {m('last_arrival'):.1f}  len ratio {m('arrival_len_ratio'):.3f}", flush=True)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    with (out / f"cohesion_{a.map}_{a.form}_r{a.replan}.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    main()
