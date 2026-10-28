from __future__ import annotations

import argparse
import csv
import os
from dataclasses import asdict, replace
from pathlib import Path
from typing import Dict, List

import random

from .config import AgentConfig, ExperimentConfig, MapConfig, PriorityWeights, ScenarioConfig, WeaponConfig
from .env import FPSEnv
from .metrics import compute_metrics


# Style sets: "exp" is the main model (v3, fixed 2026-09-22 from the route-channel study,
# repro_outputs/h3_factorial and h3_confirm): the exponential route metric over the expected-hits
# exposure field (LOS within weapon range x hit probability; opponents known to the planner), with
# lambda_E in "extra steps accepted per expected hit avoided": Survival-Aware 20, and the other styles
# at the v2 ratios (x 20/0.55). The cover weights keep their v2 values; the route-level teammate
# term is off (lambda_T = 0, 2026-09-23).
# "additive" is the v2 model (additive route cost, distance field).
EXP_MODEL_SCALE = 20.0 / 0.55   # lambda_E multiplier relative to the v2 weights (Survival-Aware 0.55 -> 20)
STYLE_MODELS = ("exp", "additive")
DEFAULT_MODEL = "exp"


def default_styles(model: str = DEFAULT_MODEL) -> Dict[str, PriorityWeights]:
    """
    Four configurations inspired by cross-game observations:
    - Mission–Cooperation (CSO-like)
    - Persistent Objective (Overwatch-like)
    - Aggressive (AssaultCube-like)
    - Survival-Aware (Xonotic-like)
    """
    styles = [
        PriorityWeights(
            name="Mission–Cooperation",
            w_objective=1.20, w_engage=0.55, w_resource=0.35, w_team=0.95, w_commitment=0.45,
            w_exposure=0.35, w_cover=0.25, w_teammate_sep=0.30,
            combat_mode_override=0,  # hold when enemy visible
        ),
        PriorityWeights(
            name="Persistent Objective",
            w_objective=1.35, w_engage=0.45, w_resource=0.70, w_team=0.85, w_commitment=0.85,
            w_exposure=0.30, w_cover=0.20, w_teammate_sep=0.25,
            combat_mode_override=1,  # keep moving
        ),
        PriorityWeights(
            name="Aggressive",
            w_objective=0.20, w_engage=1.35, w_resource=0.45, w_team=0.15, w_commitment=0.25,
            w_exposure=0.10, w_cover=0.10, w_teammate_sep=0.05,
            combat_mode_override=2,  # chase
        ),
        PriorityWeights(
            name="Survival-Aware",
            w_objective=0.20, w_engage=0.85, w_resource=1.10, w_team=0.10, w_commitment=0.25,
            w_exposure=0.55, w_cover=0.45, w_teammate_sep=0.05,
            combat_mode_override=3,  # evade
        ),
    ]
    assert model in STYLE_MODELS, model
    if model == "exp":
        # 2026-09-23: the route-level teammate term is switched off in the main model (cohesion is
        # produced by the goal layer; the term is an optional setting, see probe_cohesion.py).
        styles = [replace(s, route_cost="exp", exposure_model="hits", threat_knowledge="all",
                          w_exposure=round(s.w_exposure * EXP_MODEL_SCALE, 2), w_teammate_sep=0.0) for s in styles]
    return {s.name: s for s in styles}


def default_scenarios() -> List[ScenarioConfig]:
    return [
        ScenarioConfig(name="Mission", mode="mission", max_steps=550, num_agents_per_team=2, opponent_style="Aggressive"),
        ScenarioConfig(name="Deathmatch", mode="deathmatch", max_steps=550, num_agents_per_team=2, opponent_style="Aggressive"),
        ScenarioConfig(name="Control", mode="control", max_steps=550, num_agents_per_team=2, opponent_style="Aggressive", score_to_win=120),
    ]


def run_experiments(cfg: ExperimentConfig) -> Path:
    from .viz import save_map_figure, save_trajectory_figure  # matplotlib only when figures are drawn
    out_dir = Path(cfg.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    styles = {s.name: s for s in cfg.styles}
    rng = random.Random(cfg.seed)

    # Write config snapshot
    (out_dir / "config.json").write_text(
        str({
            "map_cfg": asdict(cfg.map_cfg),
            "agent_cfg": asdict(cfg.agent_cfg),
            "weapon_cfg": asdict(cfg.weapon_cfg),
            "scenarios": [asdict(s) for s in cfg.scenarios],
            "styles": [asdict(s) for s in cfg.styles],
            "episodes": cfg.episodes,
            "seed": cfg.seed,
        }),
        encoding="utf-8",
    )

    # Master CSV
    csv_path = out_dir / "results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "scenario", "style", "episode",
            "objective_commitment_ratio",
            "engagement_redirection_rate_per_100",
            "resource_seeking_rate_per_100",
            "avg_ally_proximity",
            "kills", "deaths",
            "control_score",
            "steps",
        ])

        # For each scenario and style
        for sc in cfg.scenarios:
            for style in cfg.styles:
                for ep in range(cfg.episodes):
                    # Each episode gets its own seed for map items & tie-breaking
                    local_rng = random.Random(rng.randrange(10**9))
                    env = FPSEnv(
                        map_cfg=cfg.map_cfg,
                        agent_cfg=cfg.agent_cfg,
                        weapon_cfg=cfg.weapon_cfg,
                        scenario=sc,
                        styles=styles,
                        rng=local_rng,
                    )
                    res = env.run_episode(evaluated_style=style.name)

                    # Compute kills/deaths for team 0
                    kills = sum(a.kills for a in env.agents.values() if a.team == 0)
                    deaths = sum(a.deaths for a in env.agents.values() if a.team == 0)
                    control_score = res.team_scores.get(0) if sc.mode == "control" else None

                    m = compute_metrics(
                        logs=res.logs,
                        team_id=0,
                        kills=kills,
                        deaths=deaths,
                        control_score=control_score,
                    )

                    writer.writerow([
                        sc.name, style.name, ep,
                        f"{m.objective_commitment_ratio:.4f}",
                        f"{m.engagement_redirection_rate_per_100:.4f}",
                        f"{m.resource_seeking_rate_per_100:.4f}",
                        f"{m.avg_ally_proximity:.4f}" if m.avg_ally_proximity is not None else "",
                        kills, deaths,
                        control_score if control_score is not None else "",
                        res.steps,
                    ])

                    # Save one trajectory figure per (scenario, style) on episode 0
                    if ep == 0:
                        fig_dir = out_dir / "figures"
                        fig_dir.mkdir(exist_ok=True)
                        save_map_figure(
                            world=env.world,
                            items=env.items,
                            agents=env.agents,
                            objective=env.objective_pos(),
                            out_path=str(fig_dir / f"map_{sc.name}.png"),
                            title=f"Map ({sc.name})",
                        )
                        save_trajectory_figure(
                            world=env.world,
                            logs=res.logs,
                            team_id=0,
                            out_path=str(fig_dir / f"traj_{sc.name}_{style.name}.png"),
                            title=f"Trajectories: {sc.name} / {style.name} (team0)",
                        )

    return out_dir


def build_default_experiment(out_dir: str, episodes: int, seed: int) -> ExperimentConfig:
    styles = list(default_styles().values())
    scenarios = default_scenarios()
    map_cfg = MapConfig(width=25, height=25, obstacle_density=0.18, seed=7)
    agent_cfg = AgentConfig()
    weapon_cfg = WeaponConfig()
    return ExperimentConfig(
        map_cfg=map_cfg,
        agent_cfg=agent_cfg,
        weapon_cfg=weapon_cfg,
        scenarios=scenarios,
        styles=styles,
        episodes=episodes,
        seed=seed,
        out_dir=out_dir,
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="Run priority-structure FPS AI experiments.")
    ap.add_argument("--out", type=str, default="outputs", help="Output directory.")
    ap.add_argument("--episodes", type=int, default=10, help="Number of episodes per (scenario, style).")
    ap.add_argument("--seed", type=int, default=123, help="Random seed.")
    args = ap.parse_args()

    cfg = build_default_experiment(out_dir=args.out, episodes=args.episodes, seed=args.seed)
    out_dir = run_experiments(cfg)
    print(f"Done. Results saved to: {out_dir.resolve()}")


if __name__ == "__main__":
    main()
