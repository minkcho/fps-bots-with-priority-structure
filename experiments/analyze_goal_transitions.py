"""Which goal types a style switches between (2026-09-24).

Re-runs episodes of one scenario with the main-model styles and the main experiment's seeds and counts the
transitions of the selected goal type of the evaluated team (team 0) from step to step. Used for the sentence
on Mission-Cooperation's Deathmatch switches in Section 7.2 (regrouping cycles).

Usage:
  python experiments/analyze_goal_transitions.py --scenario Deathmatch --style "Mission–Cooperation" \
      --map random --episodes 30
"""
from __future__ import annotations

import argparse
import collections
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fps_priority_ai.config import AgentConfig, WeaponConfig  # noqa: E402
from fps_priority_ai.env import FPSEnv  # noqa: E402
from fps_priority_ai.experiment import MAPS, episode_seed  # noqa: E402
from fps_priority_ai.runner import default_scenarios, default_styles  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--scenario", default="Deathmatch")
    p.add_argument("--style", default="Mission–Cooperation")
    p.add_argument("--map", default="random", choices=sorted(MAPS))
    p.add_argument("--episodes", type=int, default=30)
    p.add_argument("--seed", type=int, default=2026)
    args = p.parse_args()

    styles = default_styles()
    sc = next(s for s in default_scenarios() if s.name == args.scenario)
    trans: collections.Counter = collections.Counter()
    steps = 0
    for ep in range(args.episodes):
        env = FPSEnv(map_cfg=MAPS[args.map], agent_cfg=AgentConfig(), weapon_cfg=WeaponConfig(), scenario=sc,
                     styles=styles, rng=random.Random(episode_seed(args.seed, sc.name, ep)))
        res = env.run_episode(evaluated_style=args.style)
        prev = {}
        for r in res.logs:
            if r.team != 0:
                continue
            steps += 1
            last = prev.get(r.agent_id)
            if last is not None and r.goal_type != last:
                trans[(last, r.goal_type)] += 1
            prev[r.agent_id] = r.goal_type
    total = sum(trans.values())
    print(f"{args.scenario} / {args.style} / {args.map}: {total} switches over {steps} logged agent-steps")
    for (a, b), n in trans.most_common():
        print(f"  {a:>9} -> {b:<9} {n:5d}  {100.0 * n / total:5.1f}%")


if __name__ == "__main__":
    main()
