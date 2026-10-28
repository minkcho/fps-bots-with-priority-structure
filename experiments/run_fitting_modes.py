"""Exploratory: fitting each behaviour tree with every combat mode (2026-09-25; protocol part B, "also reported").

The pre-registered fit fixes each game's combat mode (CSO hold, Overwatch keep moving, AssaultCube chase, Xonotic
evade). This script asks how much the fixed mode limits the fit, with the protocol's own machinery and seeds:
  screen      the 128 scrambled-Sobol points of stage 1 (same points, training seeds, 2 episodes per map x scenario)
              are simulated once per mode; the fitted policy depends only on its parameters and its mode, so the
              same runs give the objective J for all four trees. For a tree's own mode this repeats stage 1 of the
              pre-registered fit, and J must be identical (determinism check, reported).
  validation  the best four screen points of every (tree, mode) on the validation seeds (12 episodes per cell)
  reachable   per mode, the range of each fingerprint dimension over the 128 screen points; a tree target outside
              that range by more than 2 standard errors of the target (stage-0 rows) is "unreachable by weights"
Nothing here feeds the pre-registered verdicts. Screen + validation only (no differential evolution), so the
comparison between modes is on equal footing but weaker than the pre-registered fit of the own mode.
Output: <out>/modes_screen.json, modes_validation.json, modes_summary.md
Usage: python experiments/run_fitting_modes.py --fit ../repro_outputs/v4_fit --out ../repro_outputs/v4_fit_modes --jobs 8
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting as rf  # noqa: E402

MODES = {0: "hold", 1: "keep moving", 2: "chase", 3: "evade"}
N_VALID = 4
for _m in MODES:
    rf.GAMES[f"mode{_m}"] = _m      # pseudo-games: fitted_style("mode<m>", x) has combat mode m (names are dict keys only)
TREES = ["CSO-BT", "OW-BT", "AC-BT", "XO-BT"]


def run_points(pool, mode: int, points, kind: str, n: int) -> list[dict]:
    """Summaries (rf.summarise) of the fitted policy with each parameter point and the given mode."""
    tasks, owner = [], []
    for i, x in enumerate(points):
        spec = ("fit", f"mode{mode}", *[float(v) for v in x])
        for mp in rf.TRAIN_MAPS:
            for sc in rf.SCENARIOS:
                tasks.append((spec, mp, sc, kind, 0, n))
                owner.append(i)
    rows = [[] for _ in points]
    for i, block in zip(owner, pool.imap(rf.run_block, tasks, chunksize=4)):
        rows[i] += block
    return [rf.summarise(r) for r in rows]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--fit", default="../repro_outputs/v4_fit")
    p.add_argument("--out", default="../repro_outputs/v4_fit_modes")
    p.add_argument("--jobs", type=int, default=8)
    a = p.parse_args()
    fit, out = Path(a.fit), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    s0 = json.loads((fit / "stage0.json").read_text())
    targets, scales = s0["targets"], s0["scales"]
    stage1 = json.loads((fit / "stage1.json").read_text())
    fitted = json.loads((fit / "fitted.json").read_text())
    points = [e["x"] for e in stage1["CSO-BT"]]              # the Sobol points are the same for every tree
    assert all([e["x"] for e in stage1[g]] == points for g in TREES)
    screen, summaries = {}, {}
    with Pool(a.jobs) as pool:
        for m in MODES:
            summ = run_points(pool, m, points, "train", rf.EPISODES["screen"])
            summaries[m] = summ
            screen[m] = {g: [rf.objective_value(s, targets[g], scales) for s in summ] for g in TREES}
            print(f"screen mode {m} ({MODES[m]}): best J " + ", ".join(f"{g} {min(screen[m][g]):.2f}" for g in TREES),
                  flush=True)
        # determinism check: own mode reproduces stage 1
        check = {g: float(max(abs(a_ - b_) for a_, b_ in zip(screen[rf.GAMES[g]][g], [e["J"] for e in stage1[g]])))
                 for g in TREES}
        print("determinism check (max |J - stage-1 J|): " + ", ".join(f"{g} {v:.2e}" for g, v in check.items()), flush=True)
        (out / "modes_screen.json").write_text(json.dumps({"points": points, "J": {str(m): screen[m] for m in MODES},
                                                           "determinism_check": check}, indent=1))
        # validation of the best screen points of every (tree, mode)
        todo = {}
        for g in TREES:
            for m in MODES:
                for i in np.argsort(screen[m][g])[:N_VALID]:
                    todo.setdefault(m, set()).add(int(i))
        valid = {}
        for m, idx in todo.items():
            idx = sorted(idx)
            summ = run_points(pool, m, [points[i] for i in idx], "validation", rf.EPISODES["validation"])
            for i, s in zip(idx, summ):
                valid[(m, i)] = {g: rf.objective_value(s, targets[g], scales) for g in TREES}
            print(f"validation mode {m}: {len(idx)} points", flush=True)
    best = {g: {} for g in TREES}
    for g in TREES:
        for m in MODES:
            cand = [i for i in np.argsort(screen[m][g])[:N_VALID]]
            i = min(cand, key=lambda i: valid[(m, int(i))][g])
            w = rf.simplex(*points[i][:3])
            best[g][m] = {"point": int(i), "x": points[i], "screen_J": screen[m][g][i], "validation_J": valid[(m, int(i))][g],
                          "weights": {"w_objective": w[0], "w_engage": w[1], "w_resource": w[2], "w_team": w[3],
                                      "w_commitment": points[i][3]}}
    (out / "modes_validation.json").write_text(json.dumps(best, indent=1))
    # reachable ranges per mode (screen means) vs the tree targets (+- 2 SE from the stage-0 rows)
    import csv
    trows = [r for r in csv.DictReader((fit / "stage0_rows.csv").open()) if r["agent"] in TREES]
    se = {}
    for g in TREES:
        for key in scales:
            mp, sc, met = key.split("|")
            v = [float(r[met]) for r in trows if r["agent"] == g and r["map"] == mp and r["scenario"] == sc
                 and r[met] not in ("", "nan")]
            se[(g, key)] = float(np.std(v, ddof=1) / math.sqrt(len(v))) if len(v) > 1 else 0.0
    md = ["# Exploratory: fitting with every combat mode (screen + validation; not part of the verdicts)", "",
          "Determinism check, own mode vs stage 1 (max |J difference|): "
          + ", ".join(f"{g} {v:.1e}" for g, v in check.items()), "",
          "## Validation J of the best screen point per tree and mode (lower = closer; own mode in bold)", "",
          "| tree | " + " | ".join(MODES.values()) + " | pre-registered fit (own mode, after DE) |", "|---|---|---|---|---|---|"]
    for g in TREES:
        cells = []
        for m in MODES:
            v = f"{best[g][m]['validation_J']:.2f}"
            cells.append(f"**{v}**" if m == rf.GAMES[g] else v)
        md.append(f"| {g} | " + " | ".join(cells) + f" | {fitted[g]['validation_J']:.2f} |")
    md += ["", "## Dimensions unreachable by weights (target outside the screen range by > 2 SE)", ""]
    for g in TREES:
        for m in MODES:
            bad = []
            for key in scales:
                vals = [s[tuple(key.split("|"))][0] for s in summaries[m] if tuple(key.split("|")) in s]
                lo, hi, t = min(vals), max(vals), targets[g][key]
                if t < lo - 2 * se[(g, key)] or t > hi + 2 * se[(g, key)]:
                    bad.append(f"{key} (target {t:.2f}, range {lo:.2f}-{hi:.2f})")
            md.append(f"- {g}, {MODES[m]}{' (own mode)' if m == rf.GAMES[g] else ''}: {len(bad)} of {len(scales)}"
                      + (": " + "; ".join(bad[:6]) + (" ..." if len(bad) > 6 else "") if bad else ""))
    (out / "modes_summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
