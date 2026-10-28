"""Commitment-weight sensitivity experiment (paper: "Sensitivity to goal commitment").

Sweeps w_commitment on the Mission–Cooperation base style (its hold combat mode is
retained) and evaluates the Mission and Control scenarios against the fixed
Aggressive opponent. Seeds follow the common-random-numbers design of
fps_priority_ai.experiment, so the sweep value 0.45 reproduces the corresponding
main-experiment episodes exactly.

--style (2026-10-12) sweeps another designed style instead (its own combat mode is retained); the configured
value of that style (Persistent Objective 0.85, Aggressive and Survival-Aware 0.25) reproduces its main-experiment
episodes when it is among --values. The default (Mission–Cooperation) writes sensitivity_commitment.csv exactly as
before; another style writes sensitivity_commitment_<PO|Agg|SA>.csv. The final testbed needs the five rule flags
(FPS_TEAMMATE_SWAP, FPS_LOCAL_AVOIDANCE, FPS_FORGET_MEMORY, FPS_SYMMETRIC_LOS, FPS_REACHABLE_PLACEMENT = 1).

Usage:
  python experiments/run_sensitivity_commitment.py --out ../repro_outputs --episodes 30 --seed 2026
  python experiments/run_sensitivity_commitment.py --style SA --values 0,0.2,0.25,0.45,0.65,0.85,1.05,1.25 \
      --out ../repro_outputs/commit_sweep_styles/random --map random --episodes 100
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

BASE_STYLE = "Mission–Cooperation"
STYLE_ABBR = {"Mission–Cooperation": "MC", "Persistent Objective": "PO", "Aggressive": "Agg", "Survival-Aware": "SA"}
DEFAULT_VALUES = "0.0,0.2,0.45,0.65,0.85,1.05,1.25"


def resolve_style(name: str) -> str:
    """Full style name from a full name or its abbreviation (MC, PO, Agg, SA; case-insensitive)."""
    for full, abbr in STYLE_ABBR.items():
        if name.lower() in (full.lower(), abbr.lower(), full.replace("–", "-").lower()):
            return full
    raise SystemExit(f"unknown style: {name}")


def run(out_dir: Path, episodes: int, seed: int, values: list[float], map_name: str = "random",
        model: str = DEFAULT_MODEL, style_name: str = BASE_STYLE) -> Path:
    styles = default_styles(model)
    base = styles[style_name]
    abbr = STYLE_ABBR[style_name]
    rows = []
    for sc in default_scenarios():
        if sc.name not in ("Mission", "Control"):
            continue
        for wc in values:
            variant = replace(base, name=f"{abbr}-commit-{wc:.2f}", w_commitment=wc)
            rows += run_condition(sc, variant, styles, episodes, seed,
                                  {"scenario": sc.name, "w_commitment": f"{wc:.2f}"}, MAPS[map_name])
    fname = "sensitivity_commitment.csv" if style_name == BASE_STYLE else f"sensitivity_commitment_{abbr}.csv"
    return write_csv(out_dir / fname, ["scenario", "w_commitment"], rows)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=str, default="outputs_ec")
    p.add_argument("--episodes", type=int, default=30)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--map", type=str, default="random", choices=sorted(MAPS),
                   help="Map layout (default: the scattered-obstacle map of the paper)")
    p.add_argument("--values", type=str, default=DEFAULT_VALUES,
                   help="Comma-separated w_commitment values to sweep")
    p.add_argument("--model", type=str, default=DEFAULT_MODEL, choices=list(STYLE_MODELS),
                   help="Style set: exp (main model, exponential route metric) or additive (v2 model)")
    p.add_argument("--style", type=str, default=BASE_STYLE,
                   help="Designed style to sweep: Mission–Cooperation (default), or PO, Agg, SA")
    args = p.parse_args()

    values = [float(v) for v in args.values.split(",")]
    csv_path = run(Path(args.out), args.episodes, args.seed, values, args.map, args.model, resolve_style(args.style))
    print(f"Saved: {csv_path.resolve()}")


if __name__ == "__main__":
    main()
