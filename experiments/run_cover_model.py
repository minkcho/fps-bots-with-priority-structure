"""Additional experiment: threat-relative cover (paper: "Threat-relative cover").

Decomposes the route cost into its risk terms and compares the two cover models for
three conditions: (Deathmatch, Survival-Aware), (Deathmatch, Aggressive), and
(Mission, Mission–Cooperation). Variants, all with the style's goal weights and mode:
  distance_only        : lambda_E = lambda_C = lambda_T = 0
  adjacency_cover_only : lambda_E = 0, lambda_C and lambda_T as configured, adjacency cover
  threat_cover_only    : lambda_E = 0, lambda_C and lambda_T as configured, threat cover
  adjacency_full       : all weights as configured, adjacency cover (= main experiment)
  threat_full          : all weights as configured, threat cover
Seeds follow the common-random-numbers design, so variants are paired by episode.

Usage:
  python experiments/run_cover_model.py --out ../repro_outputs --episodes 30 --seed 2026 [--map urban]
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
    ("Deathmatch", "Survival-Aware"),
    ("Deathmatch", "Aggressive"),
    ("Mission", "Mission–Cooperation"),
]


def variants(base):
    return {
        "distance_only": replace(base, name=base.name + " [dist-only]",
                                 w_exposure=0.0, w_cover=0.0, w_teammate_sep=0.0),
        "adjacency_cover_only": replace(base, name=base.name + " [adj cover only]", w_exposure=0.0),
        "threat_cover_only": replace(base, name=base.name + " [threat cover only]", w_exposure=0.0,
                                     cover_model="threat"),
        "adjacency_full": base,
        "threat_full": replace(base, name=base.name + " [threat cover]", cover_model="threat"),
    }


def run(out_dir: Path, episodes: int, seed: int, map_name: str = "random", model: str = DEFAULT_MODEL) -> Path:
    styles = default_styles(model)
    scenarios = {sc.name: sc for sc in default_scenarios()}
    rows = []
    for sc_name, style_name in CONDITIONS:
        for variant_name, style in variants(styles[style_name]).items():
            rows += run_condition(scenarios[sc_name], style, styles, episodes, seed,
                                  {"scenario": sc_name, "style": style_name, "variant": variant_name},
                                  MAPS[map_name])
    return write_csv(out_dir / "cover_model.csv", ["scenario", "style", "variant"], rows)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=str, default="outputs_ec")
    p.add_argument("--episodes", type=int, default=30)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--map", type=str, default="random", choices=sorted(MAPS))
    p.add_argument("--model", type=str, default=DEFAULT_MODEL, choices=list(STYLE_MODELS),
                   help="Style set: exp (main model, exponential route metric) or additive (v2 model)")
    args = p.parse_args()

    csv_path = run(Path(args.out), args.episodes, args.seed, args.map, args.model)
    print(f"Saved: {csv_path.resolve()}")


if __name__ == "__main__":
    main()
