"""Movement stalls in the main experiment (2026-09-25).

The environment rejects a move into a cell occupied by another agent, and a rejected agent replans the same path
on the next step. Two agents that each want the other's cell (a swap), or an agent whose next cell is held by a
teammate or opponent that does not move, can therefore stay in place for the rest of an episode. This script
re-runs the episodes of the main experiment (same seeds) and records, per episode and team, stalls of at least
--min-steps consecutive steps: alive, allowed to move, goal cell more than one cell away (Chebyshev), and not
moved. Each stall is classified by what blocked the move on most of its steps:
  swap          the next cell is held by a teammate whose own next cell is the agent's cell
  teammate      the next cell is held by a teammate (not a swap)
  opponent      the next cell is held by an opponent
  no move       the policy returned no next cell (no path)
Outputs a per-episode CSV and a summary table (share of episodes with a stall, by scenario x style x team).

Usage: python experiments/analyze_stalls.py --map random --episodes 100 --out ../repro_outputs/v3/analysis
"""
from __future__ import annotations

import argparse
import csv
import random
import sys
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fps_priority_ai.config import AgentConfig, WeaponConfig  # noqa: E402
from fps_priority_ai.env import FPSEnv  # noqa: E402
from fps_priority_ai.experiment import MAPS, episode_seed, testbed_flags  # noqa: E402
from fps_priority_ai.runner import DEFAULT_MODEL, default_scenarios, default_styles  # noqa: E402

KINDS = ("swap", "teammate", "opponent", "no move")


def run_one(args):
    map_name, scenario_name, style_name, ep, base_seed, min_steps, agent_cfg = args
    styles = default_styles(DEFAULT_MODEL)
    sc = next(s for s in default_scenarios() if s.name == scenario_name)
    env = FPSEnv(map_cfg=MAPS[map_name], agent_cfg=agent_cfg, weapon_cfg=WeaponConfig(), scenario=sc,
                 styles=styles, rng=random.Random(episode_seed(base_seed, scenario_name, ep)))
    # reproduce FPSEnv.run_episode step by step, capturing each policy's decision
    env.__init__(map_cfg=env.map_cfg, agent_cfg=env.agent_cfg, weapon_cfg=env.weapon_cfg, scenario=sc,
                 styles=styles, rng=env.rng)
    env.set_team_styles(evaluated_style=style_name)
    outs = {}
    for aid, pol in env.policies.items():
        orig = pol.decide

        def wrapped(*a, _orig=orig, _aid=aid, **k):
            o = _orig(*a, **k)
            outs[_aid] = o
            return o
        pol.decide = wrapped
    run, kinds, longest = defaultdict(int), defaultdict(Counter), {0: (0, ""), 1: (0, "")}
    for _ in range(sc.max_steps):
        outs.clear()
        before = {i: a.pos for i, a in env.agents.items() if a.alive}
        env.step()
        for i, o in outs.items():
            a = env.agents[i]
            if i not in before:
                continue
            far = o.goal_pos is not None and max(abs(o.goal_pos[0] - before[i][0]), abs(o.goal_pos[1] - before[i][1])) > 1
            if far and o.allow_move and a.alive and a.pos == before[i]:
                if o.move_to is None:
                    kind = "no move"
                else:
                    holder = next((j for j, p in before.items() if p == o.move_to and j != i), None)
                    if holder is None:
                        kind = "no move"
                    elif env.agents[holder].team == a.team:
                        other = outs.get(holder)
                        kind = "swap" if other is not None and other.move_to == before[i] else "teammate"
                    else:
                        kind = "opponent"
                if run[i] == 0:
                    kinds[i] = Counter()
                kinds[i][kind] += 1
                run[i] += 1
                if run[i] > longest[a.team][0]:
                    longest[a.team] = (run[i], kinds[i].most_common(1)[0][0])
            else:
                run[i] = 0
        if sc.mode == "control" and max(env.team_scores.values()) >= sc.score_to_win:
            break
    row = {"map": map_name, "scenario": scenario_name, "style": style_name, "episode": ep}
    for t in (0, 1):
        n, k = longest[t]
        row[f"team{t}_longest_stall"] = n
        row[f"team{t}_stall_kind"] = k if n >= min_steps else ""
    return row


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--map", default="random", choices=sorted(MAPS))
    p.add_argument("--episodes", type=int, default=100)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--min-steps", type=int, default=50)
    p.add_argument("--jobs", type=int, default=8)
    p.add_argument("--tag", default="", help="suffix of the output files (e.g. the active testbed rules)")
    p.add_argument("--out", default="../repro_outputs/v3/analysis")
    a = p.parse_args()
    agent_cfg = AgentConfig()   # optional testbed rules come from the environment (testbed_flags)
    flags = [k for k, v in testbed_flags().items() if v]
    jobs = [(a.map, sc.name, st, ep, a.seed, a.min_steps, agent_cfg)
            for sc in default_scenarios() for st in default_styles(DEFAULT_MODEL) for ep in range(a.episodes)]
    with Pool(a.jobs) as pool:
        rows = pool.map(run_one, jobs, chunksize=4)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    tag = f"stalls_{a.map}" + (f"_{a.tag}" if a.tag else "")
    with (out / f"{tag}.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    lines = [f"# Movement stalls >= {a.min_steps} steps, {a.map} map, main experiment seeds (base {a.seed}), "
             f"{a.episodes} episodes per condition; optional testbed rules on: {', '.join(flags) or 'none'}", "",
             "| Scenario | Style | team 0: episodes with a stall | team 1: episodes with a stall | kinds (team 0 / team 1) |",
             "|---|---|---|---|---|"]
    for sc in default_scenarios():
        for st in default_styles(DEFAULT_MODEL):
            d = [r for r in rows if r["scenario"] == sc.name and r["style"] == st]
            k0 = Counter(r["team0_stall_kind"] for r in d if r["team0_stall_kind"])
            k1 = Counter(r["team1_stall_kind"] for r in d if r["team1_stall_kind"])
            lines.append(f"| {sc.name} | {st} | {sum(k0.values())}/{len(d)} | {sum(k1.values())}/{len(d)} | "
                         f"{dict(k0)} / {dict(k1)} |")
    tot = Counter()
    for r in rows:
        for t in (0, 1):
            if r[f"team{t}_stall_kind"]:
                tot[(t, r[f"team{t}_stall_kind"])] += 1
    any_stall = sum(1 for r in rows if r["team0_stall_kind"] or r["team1_stall_kind"])
    lines += ["", f"Episodes with a stall of either team: {any_stall}/{len(rows)}",
              "By team and kind: " + ", ".join(f"team {t} {k}: {n}" for (t, k), n in sorted(tot.items()))]
    text = "\n".join(lines) + "\n"
    (out / f"{tag}.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
