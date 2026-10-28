"""Style-interpolation experiment (paper: "Style interpolation").

Blends two priority structures, w(alpha) = (1 - alpha) w_A + alpha w_B, over all
goal-selection, commitment, and navigation weights. The combat-movement mode is
discrete and cannot be blended, so it is fixed to keep moving for every alpha; the
sweep therefore isolates the continuous, weight-driven part of a style.

Pairs:
  - Deathmatch: Aggressive -> Survival-Aware
  - Mission:    Mission–Cooperation -> Persistent Objective

--pairs (2026-10-12) runs other pairs instead, as "Scenario:StyleA:StyleB" items separated by ";" (styles by full
name or abbreviation MC, PO, Agg, SA), and --name sets the output file (default interpolation.csv, so the default
run is unchanged); --alphas sets the blend weights (default 0, 0.25, 0.5, 0.75, 1). The final testbed needs the five rule flags (FPS_TEAMMATE_SWAP, FPS_LOCAL_AVOIDANCE,
FPS_FORGET_MEMORY, FPS_SYMMETRIC_LOS, FPS_REACHABLE_PLACEMENT = 1).

Usage:
  python experiments/run_interpolation.py --out ../repro_outputs --episodes 30 --seed 2026
  python experiments/run_interpolation.py --pairs "Mission:Agg:MC;Control:Agg:MC" --name interpolation_agg_mc.csv \
      --out ../repro_outputs/blend_agg_mc/random --map random --episodes 100
"""

from __future__ import annotations

import argparse
from dataclasses import replace
from pathlib import Path

# Ensure project root is on sys.path when executed as a script
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fps_priority_ai.config import PriorityWeights
from fps_priority_ai.runner import DEFAULT_MODEL, STYLE_MODELS, default_styles, default_scenarios
from fps_priority_ai.experiment import MAPS, run_condition, write_csv

PAIRS = [
    ("Deathmatch", "Aggressive", "Survival-Aware"),
    ("Mission", "Mission–Cooperation", "Persistent Objective"),
]
ALPHAS = [0.0, 0.25, 0.5, 0.75, 1.0]
WEIGHT_FIELDS = ["w_objective", "w_engage", "w_resource", "w_team", "w_commitment",
                 "w_exposure", "w_cover", "w_teammate_sep"]
KEEP_MOVING = 1
ABBR = {"MC": "Mission–Cooperation", "PO": "Persistent Objective", "AGG": "Aggressive", "SA": "Survival-Aware"}


def parse_pairs(spec: str) -> list[tuple[str, str, str]]:
    out = []
    for item in spec.split(";"):
        sc, a, b = [s.strip() for s in item.split(":")]
        out.append((sc, ABBR.get(a.upper(), a), ABBR.get(b.upper(), b)))
    return out


def blend(a: PriorityWeights, b: PriorityWeights, alpha: float) -> PriorityWeights:
    values = {f: (1.0 - alpha) * getattr(a, f) + alpha * getattr(b, f) for f in WEIGHT_FIELDS}
    return replace(a, name=f"blend[{a.name}->{b.name}]@{alpha:.2f}",
                   combat_mode_override=KEEP_MOVING, **values)


def run(out_dir: Path, episodes: int, seed: int, map_name: str = "random", model: str = DEFAULT_MODEL,
        pairs: list[tuple[str, str, str]] | None = None, name: str = "interpolation.csv",
        alphas: list[float] | None = None) -> Path:
    styles = default_styles(model)
    scenarios = {sc.name: sc for sc in default_scenarios()}
    rows = []
    for sc_name, name_a, name_b in (pairs or PAIRS):
        for alpha in (alphas or ALPHAS):
            style = blend(styles[name_a], styles[name_b], alpha)
            rows += run_condition(scenarios[sc_name], style, styles, episodes, seed,
                                  {"scenario": sc_name, "pair": f"{name_a} -> {name_b}",
                                   "alpha": f"{alpha:.2f}"}, MAPS[map_name])
    return write_csv(out_dir / name, ["scenario", "pair", "alpha"], rows)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=str, default="outputs_ec")
    p.add_argument("--episodes", type=int, default=30)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--map", type=str, default="random", choices=sorted(MAPS),
                   help="Map layout (default: the scattered-obstacle map of the paper)")
    p.add_argument("--model", type=str, default=DEFAULT_MODEL, choices=list(STYLE_MODELS),
                   help="Style set: exp (main model, exponential route metric) or additive (v2 model)")
    p.add_argument("--pairs", type=str, default=None, help='e.g. "Mission:Agg:MC;Control:Agg:MC" (default: the two pairs of the paper)')
    p.add_argument("--name", type=str, default="interpolation.csv", help="output file name")
    p.add_argument("--alphas", type=str, default=None, help="comma-separated blend weights (default 0,0.25,0.5,0.75,1)")
    args = p.parse_args()

    csv_path = run(Path(args.out), args.episodes, args.seed, args.map, args.model,
                   parse_pairs(args.pairs) if args.pairs else None, args.name,
                   [float(x) for x in args.alphas.split(",")] if args.alphas else None)
    print(f"Saved: {csv_path.resolve()}")


if __name__ == "__main__":
    main()
