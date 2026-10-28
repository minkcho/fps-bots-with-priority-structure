"""Additional experiment: reformulated route metric (paper: "Exponential route metric").

Compares the additive route cost of the main experiment with a zero-centred additive cost
and an exponential metric in which opponents stretch space and cover and teammates contract
it (fps_priority_ai/policy.py: PriorityPolicy._alt_search):

  additive         A  1 + lE E + lC (1 - Cover) + lT Sep                    (v2 main model)
  centred          B  max(0.1, 1 + lE E - lC Cover + lT Sep)
  exp              C  exp(lE E - lC Cover - lA PhiA), lA = lT, PhiA = sum 1 / max(d_teammate, 1)
  exp_geo          D  C with E replaced by sum over opponents of 1 / max(walking distance, 0.5)
  exp_geo_replan   E  D with replanning every 5 steps
  additive_replan  A+R  A with replanning every 5 steps (control for the replanning effect)

Every variant runs all scenarios x styles with the three v2 navigation weights scaled by
k in {0, 1, 3, 10} (k = 0: distance-only), against the Aggressive opponent of the main model.
This is a v2-era diagnostic of the route-cost FORM on the v2 weights and distance field; since
2026-09-23 no variant equals the main model (see run_h3_factorial.py for the main-model study).
Per episode the evaluated team's plans are summarised (route_diagnostics): number of plans,
plans longer than the shortest path, plans differing from the shortest path, summed planned
and shortest lengths, and the exposure E summed along planned and shortest paths.

Usage:
  python experiments/run_route_metric.py --out ../repro_outputs --map random --variants exp
  python experiments/run_route_metric.py --out ../repro_outputs --merge   # after all variants
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import replace
from pathlib import Path

# Ensure project root is on sys.path when executed as a script
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fps_priority_ai.runner import DEFAULT_MODEL, EXP_MODEL_SCALE, STYLE_MODELS, default_styles, default_scenarios
from fps_priority_ai.experiment import MAPS, episode_seed, run_episode_env, write_csv

VARIANTS = {
    "additive": {"route_cost": "additive"},
    "centred": {"route_cost": "centred"},
    "exp": {"route_cost": "exp"},
    "exp_geo": {"route_cost": "exp", "threat_field": "geodesic"},
    "exp_geo_replan": {"route_cost": "exp", "threat_field": "geodesic", "replan_interval": 5},
    "additive_replan": {"route_cost": "additive", "replan_interval": 5},
}
# Scales of the v2 (additive) navigation weights. Since 2026-09-22 the main model (exp over the
# expected-hits field, lambda_E scaled only) is no longer a member of this family; the experiment is a
# v2-era diagnostic kept for the model-comparison section.
SCALES = [0, 1, 3, 10]
KEYS = ["scenario", "style", "variant", "lambda_scale"]
DIAG = ["n_plans", "n_detour", "n_differs", "sum_len", "sum_len0", "sum_exp", "sum_exp0"]


def run(out_dir: Path, episodes: int, seed: int, map_name: str, variants, model: str = DEFAULT_MODEL) -> Path:
    styles = default_styles("additive")      # the variants scale the v2 navigation weights
    env_styles = default_styles(model)       # opponent: the Aggressive style of the main model
    rows = []
    for v in variants:
        for k in SCALES:
            for sc in default_scenarios():
                for name, base in styles.items():
                    style = replace(base, name=f"{base.name} [{v} x{k}]", w_exposure=base.w_exposure * k,
                                    w_cover=base.w_cover * k, w_teammate_sep=base.w_teammate_sep * k,
                                    route_diagnostics=True, **VARIANTS[v])
                    for ep in range(episodes):
                        row, env = run_episode_env(sc, style, env_styles, episode_seed(seed, sc.name, ep), MAPS[map_name])
                        logs = [e for aid, pol in env.policies.items() if env.agents[aid].team == 0
                                for e in pol.route_log]
                        row.update({"scenario": sc.name, "style": name, "variant": v, "lambda_scale": k, "episode": ep,
                                    "n_plans": len(logs), "n_detour": sum(e[0] > e[1] for e in logs),
                                    "n_differs": sum(e[2] for e in logs), "sum_len": sum(e[0] for e in logs),
                                    "sum_len0": sum(e[1] for e in logs), "sum_exp": f"{sum(e[3] for e in logs):.6f}",
                                    "sum_exp0": f"{sum(e[4] for e in logs):.6f}"})
                        rows.append(row)
            print(f"{map_name} {v} x{k} done", flush=True)
    return write_csv(out_dir / "route_metric_parts" / f"{v if len(variants) == 1 else '-'.join(variants)}.csv",
                     KEYS, rows, extra_columns=DIAG)


def merge(out_dir: Path) -> Path:
    parts = [out_dir / "route_metric_parts" / f"{v}.csv" for v in VARIANTS]
    missing = [p.name for p in parts if not p.exists()]
    assert not missing, f"missing parts: {missing}"
    out = out_dir / "route_metric.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = None
        for p in parts:
            with p.open(newline="", encoding="utf-8") as g:
                reader = csv.reader(g)
                header = next(reader)
                if writer is None:
                    writer = csv.writer(f)
                    writer.writerow(header)
                writer.writerows(reader)
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=str, default="outputs_ec")
    p.add_argument("--episodes", type=int, default=30)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--map", type=str, default="random", choices=sorted(MAPS))
    p.add_argument("--variants", type=str, default=",".join(VARIANTS),
                   help="Comma-separated subset of " + ", ".join(VARIANTS))
    p.add_argument("--merge", action="store_true", help="Merge the per-variant parts into route_metric.csv")
    p.add_argument("--model", type=str, default=DEFAULT_MODEL, choices=list(STYLE_MODELS),
                   help="Style set of the opponent (main model)")
    args = p.parse_args()
    if args.merge:
        print(f"Saved: {merge(Path(args.out)).resolve()}")
        return
    variants = [v.strip() for v in args.variants.split(",") if v.strip()]
    assert all(v in VARIANTS for v in variants), variants
    print(f"Saved: {run(Path(args.out), args.episodes, args.seed, args.map, variants, args.model).resolve()}")


if __name__ == "__main__":
    main()
