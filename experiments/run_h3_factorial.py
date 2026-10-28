"""H3 factorial experiment (2026-09-22): every route-channel option on every H3 scenario.

Factors (all opt-in style fields):
  field      exposure_model   distance (paper v2) | hits (expected hits, LOS+range) | anticipatory (time-to-contact)
  knowledge  threat_knowledge all (omniscient) | memory (visible + remembered)
  form       route_cost       additive | exp | square
  replan     replan_interval  0 (events only) | 5 (also every 5 steps)
  lam        w_exposure       0 (baseline, once per replan) and a grid
The cover and separation weights are set to 0 so that only the exposure channel varies.

Scenarios (--scenario / --map / --style):
  transit       unarmed objective-only agent past a frozen sentry (corridor | random | urban)
  control       Control against Aggressive (the paper's scenario) (random | urban); style SA | Objective
  control_hold  Control against "Holder" opponents that start on and hold the point (random | urban); style SA | Objective
  deathmatch    Deathmatch against Aggressive (random | urban); style SA | Objective
Per-episode metrics: route level (LOS-step fraction, expected hits along the walked path, detour
rate, planned length/exposure ratios), outcomes (deaths, kills, control score/win, arrival), and
the goal-level metrics of the paper. Rows are written to <out>/<scenario>_<map>_<style>[_shard].csv.

Usage: python experiments/run_h3_factorial.py --scenario transit --map corridor --out ../repro_outputs/h3_factorial
       python experiments/run_h3_factorial.py --scenario deathmatch --map random --style SA --shard 0/4 ...
"""
from __future__ import annotations

import argparse
import csv
import dataclasses
import itertools
import random
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from probe_h3_transit import TransitEnv, best_sentry_cell, corridor_world, hits_at, WPN  # noqa: E402
from fps_priority_ai.config import AgentConfig, MapConfig, PriorityWeights, ScenarioConfig, WeaponConfig  # noqa: E402
from fps_priority_ai.env import FPSEnv  # noqa: E402
from fps_priority_ai.experiment import MAPS, episode_seed  # noqa: E402
from fps_priority_ai.metrics import compute_metrics  # noqa: E402
from fps_priority_ai.runner import default_styles  # noqa: E402
from fps_priority_ai.world import GridWorld, euclidean  # noqa: E402
from fps_priority_ai.astar import astar_search  # noqa: E402

FIELDS = ["distance", "hits", "anticipatory"]
KNOWLEDGE = ["all", "memory"]
FORMS = ["additive", "exp", "square"]
REPLAN = [0, 5]
LAMS = [0.5, 2.0, 5.0, 10.0, 20.0]


def holder_style() -> PriorityWeights:
    """Opponent that walks to the control point and holds it, shooting anything visible."""
    return PriorityWeights(name="Holder", w_objective=2.0, w_engage=0.3, w_resource=0.0, w_team=0.2,
                           w_commitment=1.0, w_exposure=0.0, w_cover=0.0, w_teammate_sep=0.0,
                           combat_mode_override=0)


def objective_style() -> PriorityWeights:
    """Evaluated agent that pursues the objective only and keeps moving on contact (shoots reflexively)."""
    return PriorityWeights(name="Objective", w_objective=2.0, w_engage=0.0, w_resource=0.0, w_team=0.0,
                           w_commitment=1.0, w_exposure=0.0, w_cover=0.0, w_teammate_sep=0.0,
                           combat_mode_override=1)


def evaluated_style(base: PriorityWeights, field: str, knowledge: str, form: str, replan: int, lam: float,
                    cover: float = 0.0, sep: float = 0.0) -> PriorityWeights:
    name = f"{base.name}[{field}/{knowledge}/{form}/r{replan}/l{lam:g}]"
    if field == "v2":   # the paper's configured additive model: distance field, omniscient, lambda_E as given
        return dataclasses.replace(base, name=name, w_exposure=lam, w_cover=cover, w_teammate_sep=sep,
                                   exposure_model="distance", threat_knowledge="all", route_cost="additive",
                                   replan_interval=replan, route_diagnostics=True)
    return dataclasses.replace(base, name=name, w_exposure=lam, w_cover=cover, w_teammate_sep=sep,
                               exposure_model=field if lam > 0 else "distance",
                               threat_knowledge=knowledge if lam > 0 else "all",
                               route_cost=form if lam > 0 else "additive",
                               replan_interval=replan, route_diagnostics=True)


def conditions(fields, knowledge, forms, replan, lams, v2_lam=None):
    conds = [("none", "none", "additive", r, 0.0) for r in replan]
    if v2_lam is not None:
        conds += [("v2", "all", "additive", r, v2_lam) for r in replan]
    conds += list(itertools.product(fields, knowledge, forms, replan, lams))
    return conds


def build(scenario: str, map_name: str, style_name: str):
    """Returns (world, map_cfg, scenario_cfg, base_style, extra_styles, env_cls, max_steps)."""
    styles = default_styles("exp")   # 2026-09-24: main-model styles and opponent (was the v2 additive set)
    if scenario == "transit":
        if map_name == "corridor":
            world = corridor_world()
            cfg = MapConfig(seed=7, num_health=0, num_ammo=0, spawn_a=(2, 12), spawn_b=(12, 8), objective=(22, 12))
            T = 70
        else:
            base = MAPS[map_name]
            env0 = FPSEnv(map_cfg=base, agent_cfg=AgentConfig(), weapon_cfg=WeaponConfig(),
                          scenario=ScenarioConfig(name="x", mode="mission", max_steps=1, num_agents_per_team=1),
                          styles=styles, rng=random.Random(0))
            world = env0.world
            cell, _, _ = best_sentry_cell(world, base.spawn_a, base.objective)
            cfg = dataclasses.replace(base, num_health=0, num_ammo=0, spawn_b=cell)
            T = 90
        sc = ScenarioConfig(name="Transit", mode="mission", max_steps=T, num_agents_per_team=1, opponent_style="Aggressive")
        base_style = dataclasses.replace(objective_style(), name="Transit")
        return world, cfg, sc, base_style, {}, TransitEnv, T
    base = MAPS[map_name]
    if scenario == "control_hold":
        # defenders start on the control point and hold it; the evaluated team must approach it
        base = dataclasses.replace(base, spawn_b=base.objective)
        sc = ScenarioConfig(name="ControlHold", mode="control", max_steps=550, num_agents_per_team=2,
                            opponent_style="Holder", score_to_win=120)
        extra = {"Holder": holder_style()}
    elif scenario == "control":
        sc = ScenarioConfig(name="Control", mode="control", max_steps=550, num_agents_per_team=2,
                            opponent_style="Aggressive", score_to_win=120)
        extra = {}
    elif scenario == "deathmatch":
        sc = ScenarioConfig(name="Deathmatch", mode="deathmatch", max_steps=550, num_agents_per_team=2, opponent_style="Aggressive")
        extra = {}
    else:
        raise SystemExit(f"unknown scenario {scenario}")
    if style_name == "SA":
        base_style = [v for k, v in styles.items() if "Survival" in k][0]
    elif style_name == "Objective":
        base_style = objective_style()
    else:
        raise SystemExit(f"unknown style {style_name}")
    return None, base, sc, base_style, extra, FPSEnv, 550


def run_one(scenario, map_name, world, cfg, sc, style, extra, env_cls, ep, T):
    styles = {**default_styles("exp"), **extra, style.name: style}   # opponent = main-model Aggressive
    if env_cls is TransitEnv:
        TransitEnv.custom_world = world
    env = env_cls(map_cfg=cfg, agent_cfg=AgentConfig(), weapon_cfg=WeaponConfig(), scenario=sc, styles=styles,
                  rng=random.Random(episode_seed(2026, sc.name, ep)))
    res = env.run_episode(evaluated_style=style.name)
    w = env.world
    team0 = [a for a in env.agents.values() if a.team == 0]
    kills = sum(a.kills for a in team0); deaths = sum(a.deaths for a in team0)
    control_score = res.team_scores.get(0) if sc.mode == "control" else None
    m = compute_metrics(logs=res.logs, team_id=0, kills=kills, deaths=deaths, control_score=control_score)
    # route-level readouts along the walked paths
    bystep = defaultdict(lambda: {0: [], 1: []})
    for l in res.logs:
        bystep[l.step][l.team].append(l)
    alive = los = 0; hits = 0.0; dmin = []
    for step, d in bystep.items():
        enemies = [l.pos for l in d[1]]
        for l in d[0]:
            alive += 1
            if enemies:
                dmin.append(min(euclidean(l.pos, e) for e in enemies))
                h = hits_at(w, l.pos, enemies)
                hits += h
                los += int(any(euclidean(l.pos, e) <= WPN.range_cells and w.los_clear(l.pos, e) for e in enemies))
    logs = []
    for aid, a in env.agents.items():
        if a.team == 0 and hasattr(env.policies[aid], "route_log"):
            logs += env.policies[aid].route_log
    plan_detour = st.mean(r[2] for r in logs) if logs else float("nan")
    plan_len_ratio = st.mean(r[0] / r[1] for r in logs if r[1] > 0) if any(r[1] > 0 for r in logs) else float("nan")
    e0 = sum(r[4] for r in logs); plan_exp_ratio = (sum(r[3] for r in logs) / e0) if e0 > 0 else float("nan")
    row = dict(alive_steps=alive, los_frac=round(los / max(alive, 1), 4), walked_hits=round(hits, 4),
               walked_hits_per_step=round(hits / max(alive, 1), 5), mean_dmin=round(st.mean(dmin), 3) if dmin else "",
               n_plans=len(logs), plan_detour=round(plan_detour, 4), plan_len_ratio=round(plan_len_ratio, 4),
               plan_exp_ratio=round(plan_exp_ratio, 4), kills=kills, deaths=deaths,
               objective_commitment=round(m.objective_commitment_ratio, 4),
               engagement_redirection=round(m.engagement_redirection_rate_per_100, 4),
               resource_seeking=round(m.resource_seeking_rate_per_100, 4),
               ally_distance=round(m.avg_ally_proximity, 4) if m.avg_ally_proximity is not None else "",
               control_score=control_score if control_score is not None else "",
               win=int(control_score >= sc.score_to_win) if control_score is not None else "", steps=res.steps)
    if scenario == "transit":
        goal = cfg.objective
        steps0 = sorted((l.step, l) for l in res.logs if l.agent_id == 0)
        arrival = next((s for s, l in steps0 if l.pos == goal), None)
        logged = set(s for s, _ in steps0)
        death_step = next((s for s in range(1, T + 1) if s not in logged), None)
        row.update(arrived=int(arrival is not None and (death_step is None or arrival < death_step)),
                   arrival_step=arrival if arrival is not None else "",
                   died_first_life=int(death_step is not None and (arrival is None or death_step < arrival)))
    return row


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--scenario", required=True, choices=["transit", "control", "control_hold", "deathmatch"])
    p.add_argument("--map", required=True, choices=["corridor", "random", "urban"])
    p.add_argument("--style", default="SA", choices=["SA", "Objective"])
    p.add_argument("--out", default="../repro_outputs/h3_factorial")
    p.add_argument("--episodes", type=int, default=30)
    p.add_argument("--fields", default=",".join(FIELDS))
    p.add_argument("--knowledge", default=",".join(KNOWLEDGE))
    p.add_argument("--forms", default=",".join(FORMS))
    p.add_argument("--replan", default=",".join(map(str, REPLAN)))
    p.add_argument("--lams", default=",".join(map(str, LAMS)))
    p.add_argument("--shard", default="0/1", help="i/n: run the i-th of n interleaved slices of the condition list")
    p.add_argument("--quick", action="store_true", help="smoke test: 2 episodes, lam 5 only")
    p.add_argument("--cover", type=float, default=0.0, help="lambda_C for all conditions (0 = exposure channel only)")
    p.add_argument("--sep", type=float, default=0.0, help="lambda_T for all conditions")
    p.add_argument("--v2-baseline", type=float, default=None, help="add the configured additive model with this lambda_E")
    args = p.parse_args()
    if args.quick:
        args.episodes, args.lams = 2, "5"
    conds = conditions(args.fields.split(","), args.knowledge.split(","), args.forms.split(","),
                       [int(x) for x in args.replan.split(",")], [float(x) for x in args.lams.split(",")], args.v2_baseline)
    i, n = (int(x) for x in args.shard.split("/"))
    conds = conds[i::n]
    world, cfg, sc, base, extra, env_cls, T = build(args.scenario, args.map, args.style)
    style_tag = "Transit" if args.scenario == "transit" else args.style
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    fname = f"{args.scenario}_{args.map}_{style_tag}" + (f"_shard{i}of{n}" if n > 1 else "") + ".csv"
    print(f"{len(conds)} conditions, cover={args.cover}, sep={args.sep}, v2={args.v2_baseline}", flush=True)
    rows = []
    for ci, (field, knowledge, form, replan, lam) in enumerate(conds):
        style = evaluated_style(base, field, knowledge, form, replan, lam, cover=args.cover if lam > 0 else 0.0, sep=args.sep if lam > 0 else 0.0)
        for ep in range(args.episodes):
            r = run_one(args.scenario, args.map, world, cfg, sc, style, extra, env_cls, ep, T)
            rows.append(dict(scenario=args.scenario, map=args.map, style=style_tag, field=field, knowledge=knowledge,
                             form=form, replan=replan, lam=lam, episode=ep, **r))
        m = lambda k: st.mean(x[k] for x in rows[-args.episodes:] if x[k] != "")
        print(f"[{ci+1}/{len(conds)}] {field:12s} {knowledge:6s} {form:8s} r{replan} lam={lam:<5g} "
              f"hits/step={m('walked_hits_per_step'):.4f} los={m('los_frac'):.3f} detour={m('plan_detour'):.3f} deaths={m('deaths'):.2f}", flush=True)
    with (out / fname).open("w", newline="", encoding="utf-8") as f:
        wtr = csv.DictWriter(f, fieldnames=list(rows[0].keys())); wtr.writeheader(); wtr.writerows(rows)
    print(f"wrote {out / fname} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
