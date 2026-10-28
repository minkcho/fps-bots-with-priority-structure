"""Additional experiment: leave-one-out ablation of the route-cost terms.

For every style and scenario, one navigation weight at a time is set to zero:
  full          : lambda_E, lambda_C, lambda_T as configured (= main experiment)
  no_exposure   : lambda_E = 0
  no_cover      : lambda_C = 0
  no_separation : lambda_T = 0
(The distance-only planner with all three terms off is covered by
run_ablation_navigation.py and run_lambda_scale.py, scale 0.)
Seeds follow the common-random-numbers design, so variants are paired by episode.

Usage:
  python experiments/run_cost_term_ablation.py --out ../repro_outputs --episodes 30 --seed 2026 [--map urban]
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


def variants(base):
    return {
        "full": base,
        "no_exposure": replace(base, name=base.name + " [no exposure]", w_exposure=0.0),
        "no_cover": replace(base, name=base.name + " [no cover]", w_cover=0.0),
        "no_separation": replace(base, name=base.name + " [no separation]", w_teammate_sep=0.0),
    }


def run(out_dir: Path, episodes: int, seed: int, map_name: str = "random", model: str = DEFAULT_MODEL,
        scenario: str | None = None, variant: str | None = None) -> Path:
    """(2026-09-24) optional --scenario/--variant filters shard the run; shards are written to
    cost_term_ablation__<scenario>__<variant>.csv and concatenated afterwards."""
    styles = default_styles(model)
    rows = []
    for sc in default_scenarios():
        if scenario is not None and sc.name != scenario:
            continue
        for st in styles.values():
            for variant_name, style in variants(st).items():
                if variant is not None and variant_name != variant:
                    continue
                rows += run_condition(sc, style, styles, episodes, seed,
                                      {"scenario": sc.name, "style": st.name, "variant": variant_name},
                                      MAPS[map_name])
    name = "cost_term_ablation.csv" if scenario is None and variant is None else \
        f"cost_term_ablation__{scenario or 'all'}__{variant or 'all'}.csv"
    return write_csv(out_dir / name, ["scenario", "style", "variant"], rows)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=str, default="outputs_ec")
    p.add_argument("--episodes", type=int, default=30)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--map", type=str, default="random", choices=sorted(MAPS))
    p.add_argument("--model", type=str, default=DEFAULT_MODEL, choices=list(STYLE_MODELS),
                   help="Style set: exp (main model, exponential route metric) or additive (v2 model)")
    p.add_argument("--scenario", type=str, default=None, help="run one scenario only (shard)")
    p.add_argument("--variant", type=str, default=None, choices=["full", "no_exposure", "no_cover", "no_separation"],
                   help="run one variant only (shard)")
    args = p.parse_args()

    csv_path = run(Path(args.out), args.episodes, args.seed, args.map, args.model, args.scenario, args.variant)
    print(f"Saved: {csv_path.resolve()}")


if __name__ == "__main__":
    main()
