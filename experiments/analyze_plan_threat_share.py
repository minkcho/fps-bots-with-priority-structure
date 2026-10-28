"""Share of plans made with a threat in the planner's field (2026-09-24).

Re-runs episodes with the main-model styles (route diagnostics on) and reports, for the evaluated team, the share
of plans whose exposure-blind (shortest) path has non-zero expected-hits exposure at planning time, i.e. plans on
which the exposure term of the route cost can act at all, and the share of plans that take a detour.

Usage: python experiments/analyze_plan_threat_share.py --scenario Deathmatch --map random --episodes 30
"""
from __future__ import annotations

import argparse
import dataclasses
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
    p.add_argument("--map", default="random", choices=sorted(MAPS))
    p.add_argument("--episodes", type=int, default=30)
    p.add_argument("--seed", type=int, default=2026)
    args = p.parse_args()
    sc = next(s for s in default_scenarios() if s.name == args.scenario)
    for name in default_styles():
        styles = default_styles()
        styles[name] = dataclasses.replace(styles[name], route_diagnostics=True)
        logs = []
        for ep in range(args.episodes):
            env = FPSEnv(map_cfg=MAPS[args.map], agent_cfg=AgentConfig(), weapon_cfg=WeaponConfig(), scenario=sc,
                         styles=styles, rng=random.Random(episode_seed(args.seed, sc.name, ep)))
            env.run_episode(evaluated_style=name)
            for aid, a in env.agents.items():
                if a.team == 0 and hasattr(env.policies[aid], "route_log"):
                    logs += env.policies[aid].route_log
        n = len(logs)
        threat = sum(1 for r in logs if r[4] > 0)
        detour = sum(r[2] for r in logs)
        print(f"{args.scenario} / {args.map} / {name}: {n} plans, exposed shortest path {100.0 * threat / n:.1f}%, "
              f"detour {100.0 * detour / n:.1f}%")


if __name__ == "__main__":
    main()
