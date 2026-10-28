"""Development check of the revised AssaultCube and Xonotic trees (2026-09-25; not a result).

Runs the revised trees (AC-BT, XO-BT), the earlier reconstructions (AC-BT-v1, XO-BT-v1), CSO-BT, OW-BT and the four
designed styles on the four game-inspired maps x three scenarios with development seeds (base 5001, never used for
a result), and reports the bias-corrected squared standardised distance D2 between every pair of trees on the
fitting fingerprint (41 dimensions; scale: pooled within-condition SD over all agents, floored at 5% of the range of
their means, as in stage 0 of the fit), together with the mean metrics and outcomes of each tree.
Usage: python experiments/check_revised_trees.py --episodes 30 --jobs 8
"""
from __future__ import annotations

import argparse
import math
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting as rf  # noqa: E402
from fps_priority_ai.baselines import BaselineStyle  # noqa: E402

TREES = ["CSO-BT", "OW-BT", "AC-BT", "XO-BT", "AC-BT-v1", "XO-BT-v1"]
rf.SEED_BASES["dev_revised"] = 5001


def run(task):
    name, mp, sc_name, ep = task
    styles = rf.default_styles("exp")
    sc = next(s for s in rf.default_scenarios() if s.name == sc_name)
    policy = BaselineStyle(name=name, kind=name) if name in TREES else styles[name]
    row = rf.run_episode(sc, policy, styles, rf.fit_seed("dev_revised", mp, sc_name, ep), rf.MAPS[mp])
    return {"agent": name, "map": mp, "scenario": sc_name, "episode": ep, **row}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--episodes", type=int, default=30)
    p.add_argument("--jobs", type=int, default=8)
    a = p.parse_args()
    agents = TREES + rf.STYLE_NAMES
    tasks = [(n, mp, sc, ep) for n in agents for mp in rf.TRAIN_MAPS for sc in rf.SCENARIOS for ep in range(a.episodes)]
    with Pool(a.jobs) as pool:
        rows = pool.map(run, tasks, chunksize=8)
    by = {}
    for r in rows:
        by.setdefault(r["agent"], []).append(r)
    summ = {n: rf.summarise(rs) for n, rs in by.items()}
    scales = {}
    for d in rf.dims(rf.TRAIN_MAPS):
        means = [summ[n][d][0] for n in agents if d in summ[n]]
        s = max(math.sqrt(np.mean([summ[n][d][1] for n in agents if d in summ[n]])), 0.05 * (max(means) - min(means)))
        if s > 0:
            scales[d] = s

    def d2(x, y):
        t = [((summ[x][d][0] - summ[y][d][0]) ** 2 - summ[x][d][1] / summ[x][d][2] - summ[y][d][1] / summ[y][d][2]) / s ** 2
             for d, s in scales.items()]
        return float(np.mean(t))
    print(f"D2 between trees (game maps, {a.episodes} development episodes per cell, {len(scales)} dimensions)")
    print("          " + " ".join(f"{t:>9s}" for t in TREES))
    for x in TREES:
        print(f"{x:9s} " + " ".join(f"{'--' if x == y else f'{d2(x, y):.2f}':>9s}" for y in TREES))
    print("\nD2 from each tree to the designed styles:")
    for x in TREES:
        print(f"{x:9s} " + ", ".join(f"{s} {d2(x, s):.2f}" for s in rf.STYLE_NAMES))
    print("\nMean metrics on the game maps (Deathmatch / Mission):")
    cols = ["objective_commitment_ratio", "engagement_redirection_rate_per_100", "resource_seeking_rate_per_100",
            "avg_ally_proximity", "kills", "deaths", "los_frac"]
    for sc in ("Deathmatch", "Mission"):
        for x in TREES:
            rs = [r for r in by[x] if r["scenario"] == sc]
            vals = []
            for c in cols:
                v = [float(r[c]) for r in rs if r[c] not in ("", None) and not (isinstance(r[c], float) and math.isnan(r[c]))]
                vals.append(f"{c.split('_')[0][:7]} {np.mean(v):.2f}")
            print(f"  {sc:10s} {x:9s} " + " ".join(vals))


if __name__ == "__main__":
    main()
