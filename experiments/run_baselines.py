"""Additional experiment: external baselines (paper: "External baselines").

Evaluates the four behaviour-tree baselines (reconstructed CSO, Overwatch, AssaultCube,
and Xonotic logic) and a utility-AI baseline (fps_priority_ai/baselines.py) in the three
scenarios against the same fixed Aggressive opponent as the main experiment, with the
common-random-number seeds of the main experiment.

Usage:
  python experiments/run_baselines.py --out ../repro_outputs --episodes 30 --seed 2026 [--map urban]
"""

from __future__ import annotations

import argparse
from pathlib import Path

# Ensure project root is on sys.path when executed as a script
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fps_priority_ai.baselines import default_baselines
from fps_priority_ai.runner import DEFAULT_MODEL, STYLE_MODELS, default_styles, default_scenarios
from fps_priority_ai.experiment import MAPS, run_condition, write_csv


def run(out_dir: Path, episodes: int, seed: int, map_name: str = "random", model: str = DEFAULT_MODEL) -> Path:
    styles = default_styles(model)
    rows = []
    for sc in default_scenarios():
        for baseline in default_baselines().values():
            rows += run_condition(sc, baseline, styles, episodes, seed,
                                  {"scenario": sc.name, "baseline": baseline.name}, MAPS[map_name])
    return write_csv(out_dir / "baselines.csv", ["scenario", "baseline"], rows)


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
