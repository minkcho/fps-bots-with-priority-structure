"""Combat-mode ablation (paper: "Combat-mode ablation").

Separates weight-driven from mode-driven behaviour: every style is re-run with its
pinned combat-movement mode replaced by keep moving (mode 1), i.e. with goal
selection governed by the priority weights alone ("weights-only"). The "full"
condition is the main experiment itself; common-random-number seeds pair each
weights-only episode with the main-experiment episode of the same index.

Usage:
  python experiments/run_mode_ablation.py --out ../repro_outputs --episodes 30 --seed 2026
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

KEEP_MOVING = 1


def run(out_dir: Path, episodes: int, seed: int, map_name: str = "random", model: str = DEFAULT_MODEL,
        scenario: str | None = None, only_styles: list | None = None) -> Path:
    """(2026-09-25) optional filters for the confirmation run, which needs only the two pre-specified mode tests."""
    styles = default_styles(model)
    rows = []
    for sc in default_scenarios():
        if scenario and sc.name != scenario:
            continue
        for st in styles.values():
            if only_styles and st.name not in only_styles:
                continue
            variant = replace(st, name=st.name + " [weights-only]", combat_mode_override=KEEP_MOVING)
            rows += run_condition(sc, variant, styles, episodes, seed,
                                  {"scenario": sc.name, "style": st.name, "variant": "weights_only"}, MAPS[map_name])
    return write_csv(out_dir / "mode_ablation.csv", ["scenario", "style", "variant"], rows)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=str, default="outputs_ec")
    p.add_argument("--episodes", type=int, default=30)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--map", type=str, default="random", choices=sorted(MAPS),
                   help="Map layout (default: the scattered-obstacle map of the paper)")
    p.add_argument("--model", type=str, default=DEFAULT_MODEL, choices=list(STYLE_MODELS),
                   help="Style set: exp (main model, exponential route metric) or additive (v2 model)")
    p.add_argument("--scenario", default=None, help="run one scenario only")
    p.add_argument("--styles", default=None, help="comma-separated style names (default: all four)")
    args = p.parse_args()

    only = [x.strip() for x in args.styles.split(",")] if args.styles else None
    csv_path = run(Path(args.out), args.episodes, args.seed, args.map, args.model, args.scenario, only)
    print(f"Saved: {csv_path.resolve()}")


if __name__ == "__main__":
    main()
