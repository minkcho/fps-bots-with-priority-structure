"""Main experiment: 3 scenarios x 4 styles against the fixed Aggressive opponent.

Seeds follow the common-random-numbers design of fps_priority_ai.experiment, so every
style is evaluated on the same initial states episode by episode.

Usage:
  python experiments/run_ec_experiments.py --out ../repro_outputs --episodes 30 --seed 2026
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


def run(out_dir: Path, episodes: int, seed: int, map_name: str = "random",
        cover_model: str = "adjacency", model: str = DEFAULT_MODEL, spawn_separation: int | None = None,
        goal_termination: bool = True) -> Path:
    styles = default_styles(model)
    map_cfg = MAPS[map_name] if spawn_separation is None else replace(MAPS[map_name], spawn_separation=spawn_separation)
    rows = []
    for sc in default_scenarios():
        for st in styles.values():
            # A non-default cover model applies to the evaluated team only; the renamed variant
            # leaves the opponent's stock style untouched.
            ev = st if cover_model == "adjacency" else replace(st, name=f"{st.name} [{cover_model} cover]",
                                                               cover_model=cover_model)
            if not goal_termination:    # ablation: v2 goal semantics (a regrouped pair may stay on the Teammate goal)
                ev = replace(ev, name=f"{ev.name} [no goal termination]", teammate_goal_terminates=False)
            rows += run_condition(sc, ev, styles, episodes, seed, {"scenario": sc.name, "style": st.name}, map_cfg)
    return write_csv(out_dir / "results.csv", ["scenario", "style"], rows)


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
    p.add_argument("--spawn-separation", type=int, default=None,
                   help="Cells between a team's two spawn cells (default: MapConfig, 2; 0 = stacked, v2)")
    p.add_argument("--no-goal-termination", action="store_true",
                   help="Ablation: evaluated team keeps the v2 Teammate-goal semantics (no termination on regrouping)")
    args = p.parse_args()

    csv_path = run(Path(args.out), args.episodes, args.seed, args.map, args.cover_model, args.model,
                   args.spawn_separation, not args.no_goal_termination)
    print(f"Saved: {csv_path.resolve()}")


if __name__ == "__main__":
    main()
