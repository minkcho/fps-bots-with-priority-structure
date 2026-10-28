"""Navigation-shaping ablation experiment (paper: "Ablation of navigation shaping").

Compares each style's full risk-aware A* against a distance-only variant with
w_exposure = w_cover = w_teammate_sep = 0, for two representative conditions:
  - (Mission, Mission–Cooperation): largest w_teammate_sep, probes the cohesion claim
  - (Deathmatch, Survival-Aware):   largest w_exposure/w_cover, probes the deaths claim

Seeds follow the common-random-numbers design of fps_priority_ai.experiment: the
"full" variant reproduces the corresponding main-experiment episodes exactly, and
full vs distance-only episodes are paired by seed.

Usage:
  python experiments/run_ablation_navigation.py --out ../repro_outputs --episodes 30 --seed 2026
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


def run(out_dir: Path, episodes: int, seed: int, map_name: str = "random", model: str = DEFAULT_MODEL) -> Path:
    styles = default_styles(model)
    scenarios = {sc.name: sc for sc in default_scenarios()}
    rows = []
    for sc_name, style_name in CONDITIONS:
        base = styles[style_name]
        variants = {
            "full": base,
            "distance_only": replace(base, name=base.name + " [dist-only]",
                                     w_exposure=0.0, w_cover=0.0, w_teammate_sep=0.0),
        }
        for variant_name, style in variants.items():
            rows += run_condition(scenarios[sc_name], style, styles, episodes, seed,
                                  {"scenario": sc_name, "style": style_name, "variant": variant_name}, MAPS[map_name])
    return write_csv(out_dir / "ablation_navigation.csv", ["scenario", "style", "variant"], rows)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=str, default="outputs_ec")
    p.add_argument("--episodes", type=int, default=30)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--map", type=str, default="random", choices=sorted(MAPS),
                   help="Map layout (default: the scattered-obstacle map of the paper)")
    p.add_argument("--model", type=str, default=DEFAULT_MODEL, choices=list(STYLE_MODELS),
                   help="Style set: exp (main model, exponential route metric) or additive (v2 model)")
    args = p.parse_args()

    csv_path = run(Path(args.out), args.episodes, args.seed, args.map, args.model)
    print(f"Saved: {csv_path.resolve()}")


if __name__ == "__main__":
    main()
