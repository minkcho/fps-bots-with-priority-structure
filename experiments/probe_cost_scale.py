"""Diagnostic probe: how large is the route cost relative to distance, and how much does it
change the planned paths?

For every A* call of the evaluated team (team 0), the probe records the chosen risk-aware
path P and, for the same start, goal, and state, the distance-only path P0 (unit step cost).
Per call it stores the path lengths, the three extra-cost components summed along P
(lambda_E * E, lambda_C * (1 - Cover), lambda_T * Sep), and the exposure sum along P and P0.
The wrapper only reads state and runs a deterministic extra search, so the episodes are
identical to the main experiment at scale k = 1 (asserted against results.csv when given).

Runs all scenarios x styles x episodes for the navigation-weight scales k in {1, 3, 10}.

Usage:
  python experiments/probe_cost_scale.py --out ../repro_outputs/probe_cost_scale --map random \
      --results ../repro_outputs/results.csv
"""

from __future__ import annotations

import argparse
import csv
import gzip
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fps_priority_ai import policy as policy_mod  # noqa: E402
from fps_priority_ai.astar import astar_search  # noqa: E402
from fps_priority_ai.experiment import MAPS, episode_seed, run_episode  # noqa: E402
from fps_priority_ai.runner import default_scenarios, default_styles  # noqa: E402
from fps_priority_ai.world import euclidean  # noqa: E402

SCALES = [1, 3, 10]
FIELDS = ["map", "k", "scenario", "style", "episode", "goal", "d_enemy", "L", "L0", "differs",
          "XE", "XC", "XT", "E_P", "E_P0"]

_records: list = []
_ctx: dict = {}


def _cell_terms(world, agent_cfg, v, enemies, mates):
    exposure = 0.0
    for ep in enemies:
        d = max(euclidean(v, ep), 0.5)
        exposure += (1.0 if world.los_clear(v, ep) else 0.2) / d
    open_area = 1.0 - world.cover_score(v)
    sep = 0.0
    if mates:
        sep = min(euclidean(v, tp) for tp in mates) / max(1.0, float(agent_cfg.view_radius))
    return exposure, open_area, sep


def _install_hooks() -> None:
    orig_decide = policy_mod.PriorityPolicy.decide
    orig_plan = policy_mod.PriorityPolicy._plan

    def decide(self, world, agent, agents, items, objective, step):
        self._probe_items, self._probe_objective = items, objective
        return orig_decide(self, world, agent, agents, items, objective, step)

    def plan(self, world, agent, agents, goal):
        path = orig_plan(self, world, agent, agents, goal)
        if agent.team != 0 or not path or self.style.cover_model != "adjacency":
            return path
        enemies = [a.pos for a in agents.values() if a.alive and a.team != agent.team]
        mates = [a.pos for a in agents.values()
                 if a.alive and a.team == agent.team and a.agent_id != agent.agent_id]
        res0 = astar_search(world, agent.pos, goal, step_cost=lambda u, v: 1.0)
        path0 = res0.path if res0 is not None else path
        if goal == getattr(self, "_probe_objective", None):
            gclass = "objective"
        elif goal in enemies:
            gclass = "enemy"
        elif goal in mates:
            gclass = "teammate"
        elif any(it.active and it.pos == goal for it in getattr(self, "_probe_items", [])):
            gclass = "resource"
        else:
            gclass = "other"
        xe = xc = xt = ep_ = 0.0
        for v in path[1:]:
            e, o, s = _cell_terms(world, self.agent_cfg, v, enemies, mates)
            xe += self.style.w_exposure * e
            xc += self.style.w_cover * o
            xt += self.style.w_teammate_sep * s
            ep_ += e
        e0 = sum(_cell_terms(world, self.agent_cfg, v, enemies, mates)[0] for v in path0[1:])
        d_enemy = min((euclidean(agent.pos, e) for e in enemies), default=-1.0)
        _records.append([_ctx["map"], _ctx["k"], _ctx["scenario"], _ctx["style"], _ctx["episode"], gclass,
                         round(d_enemy, 3), len(path) - 1, len(path0) - 1, int(path != path0),
                         round(xe, 5), round(xc, 5), round(xt, 5), round(ep_, 5), round(e0, 5)])
        return path

    policy_mod.PriorityPolicy.decide = decide
    policy_mod.PriorityPolicy._plan = plan


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=str, required=True)
    p.add_argument("--map", type=str, default="random", choices=sorted(MAPS))
    p.add_argument("--episodes", type=int, default=30)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--results", type=str, default=None, help="results.csv of this map (k = 1 check)")
    p.add_argument("--scales", type=str, default=",".join(map(str, SCALES)))
    args = p.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    _install_hooks()

    ref = {}
    if args.results:
        with open(args.results, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                ref[(r["scenario"], r["style"], int(r["episode"]))] = r

    styles = default_styles("additive")   # diagnostic of the additive (v2) route cost
    scales = [int(s) for s in args.scales.split(",")]
    checked = 0
    for k in scales:
        for sc in default_scenarios():
            for name, base in styles.items():
                style = base if k == 1 else replace(
                    base, name=f"{base.name} [lambda x{k}]", w_exposure=base.w_exposure * k,
                    w_cover=base.w_cover * k, w_teammate_sep=base.w_teammate_sep * k)
                for ep in range(args.episodes):
                    _ctx.update(map=args.map, k=k, scenario=sc.name, style=name, episode=ep)
                    row = run_episode(sc, style, styles, episode_seed(args.seed, sc.name, ep), MAPS[args.map])
                    if k == 1 and ref:
                        r = ref[(sc.name, name, ep)]
                        for col in ("kills", "deaths", "avg_ally_proximity", "engagement_redirection_rate_per_100"):
                            assert abs(float(r[col]) - float(row[col])) < 1e-9, (sc.name, name, ep, col)
                        checked += 1
        print(f"k = {k} done ({len(_records)} plan records so far)", flush=True)

    path = out / f"plans_{args.map}_k{'-'.join(map(str, scales))}.csv.gz"
    with gzip.open(path, "wt", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(FIELDS)
        w.writerows(_records)
    print(f"k = 1 episodes identical to results.csv: {checked} checked" if checked else "no k = 1 check")
    print(f"Saved: {path.resolve()}")


if __name__ == "__main__":
    main()
