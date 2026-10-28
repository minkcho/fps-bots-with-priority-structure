"""Where the Objective style's exposure arises in Control (2026-09-24).

Re-runs conditions of the factorial simulation (run_h3_factorial.py: Control scenario, Objective style, cover and
teammate weights 0, event replanning) and splits the evaluated team's expected hits per alive step into steps near
the control point (Euclidean distance <= --near cells) and steps away from it. Used for the explanation of the
urban-map Objective anomaly in Section 7.3 (the distance field raises exposure while the expected-hits field does not).

Usage:
  python experiments/analyze_point_exposure.py --map urban --episodes 100 \
      --out ../repro_outputs/v3/analysis/point_exposure_control_urban_objective.txt
"""
from __future__ import annotations

import argparse
import random
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from run_h3_factorial import build, evaluated_style  # noqa: E402
from probe_h3_transit import hits_at  # noqa: E402
from fps_priority_ai.config import AgentConfig, WeaponConfig  # noqa: E402
from fps_priority_ai.experiment import episode_seed  # noqa: E402
from fps_priority_ai.runner import default_styles  # noqa: E402
from fps_priority_ai.world import euclidean  # noqa: E402

CONDITIONS = [  # (label, field, knowledge, form, lambda_E)
    ("distance-only A*", "none", "none", "additive", 0.0),
    ("hits / exp", "hits", "all", "exp", 10.0),
    ("distance / exp", "distance", "all", "exp", 10.0),
    ("distance / additive", "distance", "all", "additive", 10.0),
]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--map", default="urban")
    p.add_argument("--episodes", type=int, default=100)
    p.add_argument("--near", type=float, default=2.0, help="radius around the control point (cells)")
    p.add_argument("--out", default=None)
    args = p.parse_args()

    world, cfg, sc, base, extra, env_cls, T = build("control", args.map, "Objective")
    point = cfg.objective
    lines = [f"Control / {args.map} / Objective style, {args.episodes} episodes, near = within {args.near:g} cells of {point}",
             "| condition | share of steps near point | hits/step near | hits/step away | first arrival (step) | deaths |",
             "|---|---|---|---|---|---|"]
    for label, field, knowledge, form, lam in CONDITIONS:
        style = evaluated_style(base, field, knowledge, form, 0, lam)
        near_h, near_n, away_h, away_n, deaths, arrivals = 0.0, 0, 0.0, 0, [], []
        for ep in range(args.episodes):
            styles = {**default_styles("exp"), **extra, style.name: style}
            env = env_cls(map_cfg=cfg, agent_cfg=AgentConfig(), weapon_cfg=WeaponConfig(), scenario=sc,
                          styles=styles, rng=random.Random(episode_seed(2026, sc.name, ep)))
            res = env.run_episode(evaluated_style=style.name)
            w = env.world
            by_step = defaultdict(lambda: {0: [], 1: []})
            for l in res.logs:
                by_step[l.step][l.team].append(l)
            first = None
            for step in sorted(by_step):
                enemies = [l.pos for l in by_step[step][1]]
                for l in by_step[step][0]:
                    h = hits_at(w, l.pos, enemies) if enemies else 0.0
                    if euclidean(l.pos, point) <= args.near:
                        near_h += h; near_n += 1
                        if first is None:
                            first = step
                    else:
                        away_h += h; away_n += 1
            arrivals.append(first if first is not None else T)
            deaths.append(sum(a.deaths for a in env.agents.values() if a.team == 0))
        total = near_n + away_n
        lines.append(f"| {label} | {near_n / total:.3f} | {near_h / max(near_n, 1):.4f} | {away_h / max(away_n, 1):.4f} | "
                     f"{st.mean(arrivals):.1f} | {st.mean(deaths):.2f} |")
        print(lines[-1], flush=True)
    text = "\n".join(lines) + "\n"
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text)
    print(text)


if __name__ == "__main__":
    main()
