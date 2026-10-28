"""Navigation-weight scale sweep (paper: "Ablation of navigation shaping").

Scales all three navigation weights of a style by k in {0, 1, 3, 10}: k = 0 is the
distance-only planner, k = 1 the style as configured (identical to the main
experiment under common random numbers), and k > 1 amplifies the route costs. The
sweep characterises the dose-response of the route channel beyond the 0-vs-1
ablation. Conditions match run_ablation_navigation.py.

Usage:
  python experiments/run_lambda_scale.py --out ../repro_outputs --episodes 30 --seed 2026
"""

from __future__ import annotations

import argparse
from dataclasses import replace
from pathlib import Path

# Ensure project root is on sys.path when executed as a script
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fps_priority_ai.runner import DEFAULT_MODEL, STYLE_MODELS, default_styles, default_scenarios
from fps_priority_ai.experiment import MAPS, run_condition, write_csv

CONDITIONS = [
    ("Mission", "Mission–Cooperation"),
    ("Deathmatch", "Survival-Aware"),
]
SCALES = [0, 1, 3, 10]
# For the main (exp) model, relative to its configured weights.
SCALES_EXP = [0, 0.25, 0.5, 1, 2]   # relative to the configured weights: Survival-Aware lambda_E 0, 5, 10, 20, 40


def run(out_dir: Path, episodes: int, seed: int, map_name: str = "random",
        cover_model: str = "adjacency", model: str = DEFAULT_MODEL) -> Path:
    styles = default_styles(model)
    scenarios = {sc.name: sc for sc in default_scenarios()}
    rows = []
    for sc_name, style_name in CONDITIONS:
        base = styles[style_name]
        if cover_model != "adjacency":
            base = replace(base, name=f"{base.name} [{cover_model} cover]", cover_model=cover_model)
        for k in (SCALES_EXP if model == "exp" else SCALES):
            style = base if k == 1 else replace(
                base, name=f"{base.name} [lambda x{k}]",
                w_exposure=base.w_exposure * k, w_cover=base.w_cover * k,
                w_teammate_sep=base.w_teammate_sep * k)
            rows += run_condition(scenarios[sc_name], style, styles, episodes, seed,
                                  {"scenario": sc_name, "style": style_name, "lambda_scale": k}, MAPS[map_name])
    return write_csv(out_dir / "lambda_scale.csv", ["scenario", "style", "lambda_scale"], rows)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=str, default="outputs_ec")
    p.add_argument("--episodes", type=int, default=30)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--map", type=str, default="random", choices=sorted(MAPS),
                   help="Map layout (default: the scattered-obstacle map of the paper)")
    p.add_argument("--cover-model", type=str, default="adjacency", choices=["adjacency", "threat"],
                   help="Cover term of the evaluated team's route cost")
    p.add_argument("--model", type=str, default=DEFAULT_MODEL, choices=list(STYLE_MODELS),
                   help="Style set: exp (main model, exponential route metric) or additive (v2 model)")
    args = p.parse_args()

    csv_path = run(Path(args.out), args.episodes, args.seed, args.map, args.cover_model, args.model)
    print(f"Saved: {csv_path.resolve()}")


if __name__ == "__main__":
    main()
