"""Additional experiment: designer risk budgets (paper: "Additional experiment: designer risk budgets").

A risk budget beta replaces a style's fixed w_exposure: for every plan, the policy
bisects w_exposure in [0, LAMBDA_MAX] for the smallest value whose path exposure meets
the budget (Lagrangian relaxation of the risk-constrained problem; see
PriorityPolicy._plan_with_budget). Two budget definitions are available:
  --mode relative   : budget = beta * R(P0), P0 = exposure-blind path, beta in {1,.75,.5,.25}
  --mode normalised : budget = R_min + beta * (R(P0) - R_min), R_min = exposure of the
                      safest path in the family, beta in {1,.75,.5,.25,0}
The fixed-weight reference is the main experiment itself (common random numbers).

Besides the standard metrics, each row reports the team-0 plan statistics:
  n_plans, budget_adherence (fraction of plans within budget),
  exposure_ratio (mean R(P)/R(P0) over plans with R(P0) > 0),
  length_overhead (mean |P|/|P0| over plans with |P0| > 0), mean_lambda,
  budget_position (normalised mode: mean (R(P) - R_min)/(R(P0) - R_min) over plans
  with R(P0) > R_min; 1 = exposure-blind route, 0 = safest route).

Usage:
  python experiments/run_risk_budget.py --out ../repro_outputs --episodes 30 --seed 2026 --mode normalised
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import replace
from pathlib import Path

# Ensure project root is on sys.path when executed as a script
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fps_priority_ai.runner import DEFAULT_MODEL, STYLE_MODELS, default_styles, default_scenarios
from fps_priority_ai.experiment import MAPS, episode_seed, run_episode_env, write_csv

SCENARIO = "Deathmatch"
STYLES = ["Survival-Aware", "Aggressive"]
BETAS = {"relative": [1.0, 0.75, 0.5, 0.25], "normalised": [1.0, 0.75, 0.5, 0.25, 0.0]}
PLAN_COLUMNS = ["n_plans", "budget_adherence", "exposure_ratio", "length_overhead", "mean_lambda",
                "budget_position"]


def plan_stats(env) -> dict:
    logs = [e for aid, pol in env.policies.items() if env.agents[aid].team == 0 for e in pol.plan_log]
    ratios = [e["r"] / e["r0"] for e in logs if e["r0"] > 0]
    overheads = [e["len"] / e["len0"] for e in logs if e["len0"] > 0]
    positions = [(e["r"] - e["r_min"]) / (e["r0"] - e["r_min"]) for e in logs
                 if e["r_min"] == e["r_min"] and e["r0"] - e["r_min"] > 1e-9]
    mean = lambda v: f"{sum(v) / len(v):.6f}" if v else ""
    return {
        "n_plans": len(logs),
        "budget_adherence": mean([e["ok"] for e in logs]),
        "exposure_ratio": mean(ratios),
        "length_overhead": mean(overheads),
        "mean_lambda": mean([e["lam"] for e in logs]),
        "budget_position": mean(positions),
    }


def run(out_dir: Path, episodes: int, seed: int, style_names: list[str], mode: str,
        map_name: str = "random", model: str = DEFAULT_MODEL) -> Path:
    styles = default_styles(model)
    sc = {s.name: s for s in default_scenarios()}[SCENARIO]
    rows = []
    for style_name in style_names:
        for beta in BETAS[mode]:
            variant = replace(styles[style_name], name=f"{style_name} [{mode} budget {beta:.2f}]",
                              risk_budget=beta, risk_budget_mode=mode)
            for ep in range(episodes):
                row, env = run_episode_env(sc, variant, styles, episode_seed(seed, sc.name, ep), MAPS[map_name])
                rows.append({"scenario": sc.name, "style": style_name, "beta": f"{beta:.2f}",
                             "episode": ep, **row, **plan_stats(env)})
    name = (f"risk_budget_{mode}.csv" if len(style_names) == len(STYLES)
            else f"risk_budget_{mode}_{style_names[0].split()[0]}.csv")
    return write_csv(out_dir / name, ["scenario", "style", "beta"], rows, extra_columns=PLAN_COLUMNS)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=str, default="outputs_ec")
    p.add_argument("--episodes", type=int, default=30)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--mode", type=str, default="normalised", choices=sorted(BETAS))
    p.add_argument("--map", type=str, default="random", choices=sorted(MAPS))
    p.add_argument("--style", type=str, default=None,
                   help="Run a single style (for parallel runs); default runs both")
    p.add_argument("--model", type=str, default=DEFAULT_MODEL, choices=list(STYLE_MODELS),
                   help="Style set: exp (main model, exponential route metric) or additive (v2 model)")
    args = p.parse_args()

    names = [args.style] if args.style else STYLES
    csv_path = run(Path(args.out), args.episodes, args.seed, names, args.mode, args.map, args.model)
    print(f"Saved: {csv_path.resolve()}")


if __name__ == "__main__":
    main()
