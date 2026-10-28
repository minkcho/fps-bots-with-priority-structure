"""Why the Part F Xonotic fit does not pursue distant opponents (2026-09-27; exploratory diagnostic, no new parameters).

Replays episodes of the Xonotic tree (as revised, and with the havocbot strategy timer of 15/12 steps), the Part F fit
of it, and counterfactual settings of that fit in which one
existing parameter is changed (rho = 1; w_team = 0; eta = 1; rho = 1 with w_team = 0), and records the evaluated team's
goal choice step by step with the situation: far (no living opponent within 10 cells, as in far_pursuit_share), low
status, enemy visible, regrouped (a living teammate within 1.5 cells, so that the policy has no Teammate candidate).
Reports conditional goal-choice frequencies and the mean ally distance.
Development seeds (base 5501, never used for a result), game-inspired maps, three scenarios, 20 episodes per cell.
Output: <out>/diagnosis.md
Usage: python experiments/diagnose_part_f.py --out ../repro_outputs/dev_xo_diagnosis --jobs 4
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from collections import defaultdict
from dataclasses import replace
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting_f as rff  # noqa: E402  (eight-parameter mapping of Part F)

rf, rfc = rff.rf, rff.rfc
from fps_priority_ai.config import AgentConfig, WeaponConfig  # noqa: E402
from fps_priority_ai.env import FPSEnv  # noqa: E402
from fps_priority_ai.world import euclidean  # noqa: E402

rf.SEED_BASES["dev_diag"] = 5501
FIT = Path(__file__).resolve().parents[2] / "repro_outputs" / "v8_fit"
EPISODES = 20
CHANGES = {"fit": {}, "fit rho=1": {"urgent_switch_relief": 1.0}, "fit w_team=0": {"w_team": 0.0},
           "fit eta=1": {"hunt_unseen": 1.0}, "fit rho=1 w_team=0": {"urgent_switch_relief": 1.0, "w_team": 0.0}}


def make(name: str):
    if name in ("XO-BT", "AC-BT"):
        # (2026-09-27, after the tree review) the per-step Xonotic tree and the AssaultCube tree of 2026-09-25 (dataclass
        # defaults), as when this diagnosis ran; default_baselines() now differs
        from fps_priority_ai.baselines import BaselineStyle
        return BaselineStyle(name=name, kind=name)
    if name == "XO-BT timer":
        from fps_priority_ai.baselines import BaselineStyle
        return BaselineStyle(name=name, kind="XO-BT", xo_interval=15, xo_interval_moving=12)
    f = json.loads((FIT / "fitted.json").read_text())["XO-BT"]
    return replace(rfc.fitted_style_c(name, f["combat_mode"], f["x"]), **CHANGES[name])


def run(task):
    name, map_name, scenario, ep = task
    styles = rf.default_styles("exp")
    sc = next(s for s in rf.default_scenarios() if s.name == scenario)
    policy = make(name)
    env = FPSEnv(map_cfg=rf.MAPS[map_name], agent_cfg=AgentConfig(), weapon_cfg=WeaponConfig(), scenario=sc,
                 styles={**styles, policy.name: policy}, rng=random.Random(rf.fit_seed("dev_diag", map_name, scenario, ep)))
    env.__init__(map_cfg=env.map_cfg, agent_cfg=env.agent_cfg, weapon_cfg=env.weapon_cfg, scenario=sc,
                 styles=env.styles, rng=env.rng)
    env.set_team_styles(evaluated_style=policy.name)
    recs = []
    for aid, pol in env.policies.items():
        if env.agents[aid].team != 0:
            continue
        orig = pol.decide

        def wrapped(world, agent, agents, items, objective, step, _orig=orig):
            out = _orig(world=world, agent=agent, agents=agents, items=items, objective=objective, step=step)
            opp = [a.pos for a in agents.values() if a.alive and a.team != agent.team]
            tms = [a.pos for a in agents.values() if a.alive and a.team == agent.team and a.agent_id != agent.agent_id]
            dmin = min((euclidean(agent.pos, o) for o in opp), default=None)
            dtm = min((euclidean(agent.pos, t) for t in tms), default=None)
            recs.append({"goal": out.goal_type, "far": dmin is None or dmin > 10.0,
                         "low": agent.health <= env.agent_cfg.low_health_threshold
                         or agent.ammo <= env.agent_cfg.low_ammo_threshold,
                         "vis": len(agent.memory.last_visible_enemies) > 0,
                         "regrouped": dtm is not None and dtm <= 1.5, "dtm": dtm, "scenario": scenario})
            return out
        pol.decide = wrapped
    for _ in range(sc.max_steps):
        env.step()
        if sc.mode == "control" and max(env.team_scores.values()) >= sc.score_to_win:
            break
    return name, recs


def share(recs, cond, goal):
    sel = [r for r in recs if cond(r)]
    return (sum(r["goal"] == goal for r in sel) / len(sel), len(sel)) if sel else (float("nan"), 0)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="../repro_outputs/dev_xo_diagnosis")
    p.add_argument("--jobs", type=int, default=4)
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    names = ["XO-BT", "XO-BT timer", *CHANGES, "AC-BT"]
    tasks = [(n, m, sc, ep) for n in names for m in rf.TRAIN_MAPS for sc in rf.SCENARIOS for ep in range(EPISODES)]
    recs = defaultdict(list)
    with Pool(a.jobs) as pool:
        for name, r in pool.imap_unordered(run, tasks, chunksize=2):
            recs[name] += r
    far_good = lambda r: r["far"] and not r["low"]  # noqa: E731
    rows = [("far: enemy (far pursuit)", lambda r: r["far"], "enemy"),
            ("far, good status: enemy", far_good, "enemy"),
            ("far, good status: teammate", far_good, "teammate"),
            ("far, good status: resource", far_good, "resource"),
            ("far, good status: roam", far_good, "roam"),
            ("far, good status: objective", far_good, "objective"),
            ("far, good, regrouped: enemy", lambda r: far_good(r) and r["regrouped"], "enemy"),
            ("far, good, not regrouped: enemy", lambda r: far_good(r) and not r["regrouped"], "enemy"),
            ("low status, enemy visible: resource (retreat)", lambda r: r["low"] and r["vis"], "resource")]
    md = ["# Goal choice by situation: Xonotic tree, its Part F fit and counterfactual settings of the fit "
          "(development seeds 5501, game maps, 20 episodes per cell; evaluated team, alive steps; not a result)", "",
          "| situation: goal | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
    res = {}
    for lab, cond, goal in rows:
        cells = []
        for n in names:
            v, k = share(recs[n], cond, goal)
            res.setdefault(n, {})[lab] = [v, k]
            cells.append("--" if k == 0 else f"{v:.2f}")
        md.append(f"| {lab} | " + " | ".join(cells) + " |")
    md.append("| share of steps far | " + " | ".join(f"{sum(r['far'] for r in recs[n]) / len(recs[n]):.2f}"
                                                  for n in names) + " |")
    md.append("| share of far, good steps regrouped | " + " | ".join(
        f"{share(recs[n], far_good, None)[1] and sum(r['regrouped'] for r in recs[n] if far_good(r)) / share(recs[n], far_good, None)[1]:.2f}"
        for n in names) + " |")
    md.append("| mean ally distance (cells) | " + " | ".join(
        f"{sum(r['dtm'] for r in recs[n] if r['dtm'] is not None) / max(1, sum(r['dtm'] is not None for r in recs[n])):.2f}"
        for n in names) + " |")
    (out / "diagnosis.json").write_text(json.dumps(res, indent=1, default=float))
    (out / "diagnosis.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
