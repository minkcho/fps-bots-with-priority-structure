"""Pre-registered calibration of the navigation-weight scale of the exponential route metric.

Criterion, fixed on 2026-09-22 before any outcome of the exponential model was examined: the
scale k* is the smallest k in GRID such that the pooled exposure ratio of Survival-Aware on the
random map (exposure summed along its planned paths divided by exposure summed along the shortest
paths, over all plans in the three scenarios) is at most THRESHOLD, on held-out seeds (base seed
2027, 30 episodes per scenario). If no k qualifies, k* is the k with the smallest ratio. All
styles, including the Aggressive opponent, use the exponential route metric with the v2
navigation weights scaled by k. Only planning diagnostics are recorded; the urban map is reported
for reference and not used for the selection.

Usage:
  python experiments/calibrate_scale.py --out ../repro_outputs/calibration --map random --k 5
  python experiments/calibrate_scale.py --out ../repro_outputs/calibration --summarise
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fps_priority_ai.experiment import MAPS, episode_seed, run_episode_env  # noqa: E402
from fps_priority_ai.runner import default_scenarios, default_styles  # noqa: E402

GRID = [1, 2, 3, 5, 7, 10, 15, 20, 30]
THRESHOLD = 0.85
SEED = 2027
FIELDS = ["map", "k", "scenario", "episode", "n_plans", "n_detour", "sum_len", "sum_len0", "sum_exp", "sum_exp0"]


def exp_styles(k: float):
    return {n: replace(s, route_cost="exp", w_exposure=s.w_exposure * k, w_cover=s.w_cover * k,
                       w_teammate_sep=s.w_teammate_sep * k) for n, s in default_styles("additive").items()}


def run(out: Path, map_name: str, ks, episodes: int, seed: int) -> Path:
    rows = []
    for k in ks:
        styles = exp_styles(k)
        ev = replace(styles["Survival-Aware"], name=f"Survival-Aware [calibration x{k}]", route_diagnostics=True)
        for sc in default_scenarios():
            for ep in range(episodes):
                _, env = run_episode_env(sc, ev, styles, episode_seed(seed, sc.name, ep), MAPS[map_name])
                logs = [e for aid, pol in env.policies.items() if env.agents[aid].team == 0 for e in pol.route_log]
                rows.append([map_name, k, sc.name, ep, len(logs), sum(e[0] > e[1] for e in logs),
                             sum(e[0] for e in logs), sum(e[1] for e in logs),
                             f"{sum(e[3] for e in logs):.6f}", f"{sum(e[4] for e in logs):.6f}"])
        print(f"{map_name} k={k} done", flush=True)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"calibration_{map_name}_k{'-'.join(str(k) for k in ks)}.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(FIELDS)
        w.writerows(rows)
    return path


def summarise(out: Path) -> None:
    agg = {}
    for p in sorted(out.glob("calibration_*_k*.csv")):
        with p.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                a = agg.setdefault((r["map"], float(r["k"])), [0, 0, 0, 0, 0.0, 0.0])
                for i, c in enumerate(["n_plans", "n_detour", "sum_len", "sum_len0"]):
                    a[i] += int(r[c])
                a[4] += float(r["sum_exp"])
                a[5] += float(r["sum_exp0"])
    md = ["# Calibration of the navigation-weight scale (pre-registered)\n",
          f"Criterion: smallest k in {GRID} with pooled Survival-Aware exposure ratio <= {THRESHOLD} on the random map "
          f"(held-out seeds, base seed {SEED}, 30 episodes per scenario); the urban map is reported for reference only.\n"]
    choice = None
    with (out / "calibration.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["map", "k", "plans", "detour_share", "length_ratio", "exposure_ratio"])
        for m in ("random", "urban"):
            rows = sorted((k, a) for (mm, k), a in agg.items() if mm == m)
            if not rows:
                continue
            md.append(f"\n## {m} map\n")
            md.append("| k | plans | detour share | length ratio | exposure ratio |")
            md.append("|---|---|---|---|---|")
            for k, a in rows:
                ratio = a[4] / a[5]
                w.writerow([m, f"{k:g}", a[0], f"{a[1] / a[0]:.6f}", f"{a[2] / a[3]:.6f}", f"{ratio:.6f}"])
                md.append(f"| {k:g} | {a[0]} | {100 * a[1] / a[0]:.2f}% | {a[2] / a[3]:.3f} | {ratio:.3f} |")
            if m == "random":
                ok = [k for k, a in rows if a[4] / a[5] <= THRESHOLD]
                choice = min(ok) if ok else min(rows, key=lambda t: t[1][4] / t[1][5])[0]
                md.append(f"\n**k* = {choice:g}** " + ("(smallest k meeting the criterion)" if ok else
                                                       "(no k met the criterion; smallest ratio)"))
    (out / "calibration_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=str, required=True)
    p.add_argument("--map", type=str, default="random", choices=sorted(MAPS))
    p.add_argument("--k", type=str, default=",".join(str(k) for k in GRID), help="comma-separated subset of GRID")
    p.add_argument("--episodes", type=int, default=30)
    p.add_argument("--seed", type=int, default=SEED)
    p.add_argument("--summarise", action="store_true")
    args = p.parse_args()
    if args.summarise:
        summarise(Path(args.out))
        return
    ks = [float(k) if "." in k else int(k) for k in args.k.split(",")]
    assert all(k in GRID for k in ks), ks
    print(f"Saved: {run(Path(args.out), args.map, ks, args.episodes, args.seed).resolve()}")


if __name__ == "__main__":
    main()
