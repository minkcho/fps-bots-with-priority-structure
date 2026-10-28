"""Why the fitted policies miss the trees (2026-09-25; exploratory diagnostic of the fitting experiment).

Replays the first episodes of the fitting test stage (same seeds, so the same episodes as test_rows.csv) for each
behaviour tree and its fitted policy on the four game-inspired maps, and records the evaluated team's goal choice
step by step together with the situation: an enemy visible, only a remembered enemy position, neither; low status.
Reports conditional goal-choice frequencies that isolate the decision rules of the trees:
  P(enemy | visible)            engages what it sees
  P(enemy | remembered only)    pursues a remembered position
  P(enemy | none known)         hunts an opponent it neither sees nor remembers (omniscient targeting)
  P(resource | low status)      puts items first when health or ammunition is low (also with an enemy visible)
  P(objective | free)           Mission/Control: goes to the objective when no enemy is known and status is fine
  P(teammate), leader/follower  CSO roles: the lowest-id agent leads, the other follows
Output: <fit>/fitting_gaps.md
Usage: python experiments/diagnose_fitting_gaps.py --fit ../repro_outputs/v4_fit --episodes 20 --jobs 8
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run_fitting as rf  # noqa: E402
from fps_priority_ai.config import AgentConfig, WeaponConfig  # noqa: E402
from fps_priority_ai.env import FPSEnv  # noqa: E402
from fps_priority_ai.experiment import MAPS  # noqa: E402
from fps_priority_ai.runner import default_scenarios, default_styles  # noqa: E402

TREES = ["CSO-BT", "OW-BT", "AC-BT", "XO-BT"]


def run(task):
    """task = (spec, map, scenario, episode) -> list of per-step records of the evaluated team (team 0)."""
    spec, map_name, scenario, ep = task
    styles = default_styles("exp")
    sc = next(s for s in default_scenarios() if s.name == scenario)
    policy = rf.make_policy(spec)
    env = FPSEnv(map_cfg=MAPS[map_name], agent_cfg=AgentConfig(), weapon_cfg=WeaponConfig(), scenario=sc,
                 styles={**styles, policy.name: policy}, rng=random.Random(rf.fit_seed("test", map_name, scenario, ep)))
    # reproduce FPSEnv.run_episode exactly: it re-initialises with the same random stream, then assigns the styles
    env.__init__(map_cfg=env.map_cfg, agent_cfg=env.agent_cfg, weapon_cfg=env.weapon_cfg, scenario=sc,
                 styles=env.styles, rng=env.rng)
    env.set_team_styles(evaluated_style=policy.name)
    recs, pre = [], {}
    for aid, pol in env.policies.items():
        if env.agents[aid].team != 0:
            continue
        orig = pol.decide

        def wrapped(world, agent, agents, items, objective, step, _orig=orig, _aid=aid):
            pre[_aid] = agent.memory.last_seen_enemy_pos is not None
            out = _orig(world=world, agent=agent, agents=agents, items=items, objective=objective, step=step)
            vis = len(agent.memory.last_visible_enemies) > 0
            low = agent.health <= env.agent_cfg.low_health_threshold or agent.ammo <= env.agent_cfg.low_ammo_threshold
            recs.append({"aid": _aid, "leader": _aid == min(a.agent_id for a in agents.values() if a.team == 0),
                         "goal": out.goal_type, "vis": vis, "mem": pre[_aid] and not vis, "low": low,
                         "objective": objective is not None})
            return out
        pol.decide = wrapped
    for _ in range(sc.max_steps):
        env.step()
        if sc.mode == "control" and max(env.team_scores.values()) >= sc.score_to_win:
            break
    return recs


def rate(recs, cond, goal):
    sel = [r for r in recs if cond(r)]
    return (sum(r["goal"] == goal for r in sel) / len(sel), len(sel)) if sel else (float("nan"), 0)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--fit", default="../repro_outputs/v4_fit")
    p.add_argument("--episodes", type=int, default=20)
    p.add_argument("--jobs", type=int, default=8)
    a = p.parse_args()
    fitted = json.loads((Path(a.fit) / "fitted.json").read_text())
    specs = {}
    for g in TREES:
        specs[g] = ("tree", g)
        specs[f"fit[{g}]"] = ("fit", g, *fitted[g]["x"])
    tasks, keys = [], []
    for name, spec in specs.items():
        for mp in rf.TRAIN_MAPS:
            for sc in rf.SCENARIOS:
                for ep in range(a.episodes):
                    tasks.append((spec, mp, sc, ep))
                    keys.append((name, sc))
    recs = defaultdict(list)
    with Pool(a.jobs) as pool:
        for (name, sc), r in zip(keys, pool.imap(run, tasks, chunksize=2)):
            for x in r:
                x["scenario"] = sc
            recs[name] += r
    rows = [
        ("P(enemy | visible)", lambda r: r["vis"], "enemy"),
        ("P(enemy | remembered only)", lambda r: r["mem"], "enemy"),
        ("P(enemy | none known)", lambda r: not r["vis"] and not r["mem"], "enemy"),
        ("P(resource | low status)", lambda r: r["low"], "resource"),
        ("P(resource | low status, enemy visible)", lambda r: r["low"] and r["vis"], "resource"),
        ("P(objective | free; Mission/Control)", lambda r: r["objective"] and not r["vis"] and not r["mem"] and not r["low"], "objective"),
        ("P(teammate | leader)", lambda r: r["leader"], "teammate"),
        ("P(teammate | follower)", lambda r: not r["leader"], "teammate"),
    ]
    md = [f"# Goal choice by situation, trees vs fitted policies (game maps, test seeds, first {a.episodes} episodes per "
          "map and scenario; evaluated team, alive steps)", "",
          "| situation -> goal | " + " | ".join(f"{g} | fit" for g in TREES) + " |",
          "|---|" + "---|" * (2 * len(TREES))]
    for lab, cond, goal in rows:
        cells = []
        for g in TREES:
            for name in (g, f"fit[{g}]"):
                v, n = rate(recs[name], cond, goal)
                cells.append("--" if n == 0 else f"{v:.2f}")
        md.append(f"| {lab} | " + " | ".join(cells) + " |")
    md += ["", "Share of steps in each situation (tree / fit): " + "; ".join(
        f"{g}: visible {sum(r['vis'] for r in recs[g]) / len(recs[g]):.2f}/{sum(r['vis'] for r in recs['fit[' + g + ']']) / len(recs['fit[' + g + ']']):.2f}"
        for g in TREES)]
    out = Path(a.fit) / "fitting_gaps.md"
    out.write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
