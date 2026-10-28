"""Part E of the fitting experiment: fingerprint measures that separate the AssaultCube and Xonotic logics (2026-09-26).

Part D (FITTING_PLAN_D_2026-09-26.md) met H-D1 but the AssaultCube fit was confused with the Xonotic tree on three
held-out maps. Part E adds to the Part D fingerprint the three measures that separate the two source-based trees by
at least one pooled SD on both the game-inspired and the held-out maps in a development check
(check_fingerprint_candidates.py, seeds 5101; repro_outputs/dev_fingerprint/check.txt): retreat_share (low status with
an enemy visible -> Resource goal), far_pursuit_share (no opponent within 10 cells -> Enemy goal) and contact_distance
(mean distance to the nearest opponent while one is visible). New seeds 7029-7033 (smoke 9329-9333); the Part D fits
(fitD[...]) run on the same test seeds as the comparison. Everything else as in Part D.

Part D changes from Part C, kept here:
  targets      the AssaultCube and Xonotic trees revised from the bots' source code (AC-BT: fixed priority chain;
               XO-BT: one rating scale for items and opponents); CSO-BT and OW-BT unchanged. In Parts B and C the two
               earlier reconstructions (now AC-BT-v1, XO-BT-v1) were behaviourally identical (D2 0.02).
  fingerprint  the four goal-intent metrics plus four behavioural measures per map x scenario: kills and deaths per
               100 alive agent-steps, the share of alive steps with an opponent in line of sight within weapon range,
               and item control (share of good-status alive steps on the Resource goal). Part C's fits matched the
               deathmatch trees' goal statistics while fighting far less; these measures make that visible.
  seeds        new bases: target 6032, train 6029, mode selection 6033, validation 6031, test 6030 (smoke 9229-9233)
  comparison   the Part C fits (fitC[...]) are run on the same test seeds
Implementation: the stages of run_fitting_c.py (frozen for Part C) with run_fitting.FP extended in place and the new
seed bases; outputs in the same formats. Usage: python experiments/run_fitting_e.py --stage all --out
../repro_outputs/v7_fit --jobs 12 [--quick]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import replace
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting as rf  # noqa: E402

BEHAVIOUR = ["kill_rate_per_100", "death_rate_per_100", "los_frac", "resource_goal_share_good",
             "retreat_share", "far_pursuit_share", "contact_distance"]
rf.FP[:] = rf.FP + [m for m in BEHAVIOUR if m not in rf.FP]           # fingerprint used by summarise / dims / J
rf.OUTCOMES[:] = [m for m in rf.OUTCOMES if m not in rf.FP]            # no metric counted twice in summarise

import run_fitting_c as rfc  # noqa: E402  (imported after the patch; it uses rf.FP through rf)

SEED_BASES = {"c_target": 7032, "c_train": 7029, "c_select": 7033, "c_valid": 7031, "c_test": 7030}
QUICK_SEED_BASES = {"c_target": 9332, "c_train": 9329, "c_select": 9333, "c_valid": 9331, "c_test": 9330}


def make_policy_d(spec: tuple):
    if spec[0] == "fitD":                  # ("fitD", game, mode, *x): the Part D fit, relabelled
        return rfc.fitted_style_c(f"fitD[{spec[1]}]", spec[2], spec[3:])
    return rfc.make_policy_c(spec)


def label_d(spec: tuple) -> str:
    return f"fitD[{spec[1]}]" if spec[0] == "fitD" else rfc.label_c(spec)


def run_block_d(task: tuple) -> list[dict]:
    spec, map_name, scenario, kind, first, n = task
    styles = rf.default_styles("exp")
    sc = next(s for s in rf.default_scenarios() if s.name == scenario)
    policy = make_policy_d(spec)
    rows = []
    for ep in range(first, first + n):
        row = rf.run_episode(sc, policy, styles, rf.fit_seed(kind, map_name, scenario, ep), rf.MAPS[map_name])
        rows.append({"agent": label_d(spec), "map": map_name, "scenario": scenario, "seed_kind": kind,
                     "episode": ep, **row})
    return rows


def stage_test_d(out: Path, jobs: int, part_d: Path) -> None:
    fitted = json.loads((out / "fitted.json").read_text())
    fd = json.loads((part_d / "fitted.json").read_text())
    specs = ([("fitc", f"fit[{g}]", fitted[g]["combat_mode"], *fitted[g]["x"]) for g in rfc.GAMES]
             + [("fitD", g, fd[g]["combat_mode"], *fd[g]["x"]) for g in rfc.GAMES]
             + [("tree", g) for g in rfc.GAMES] + [("style", s) for s in rf.STYLE_NAMES]
             + [("style_off", s) for s in rf.STYLE_NAMES])
    tasks = [(sp, mp, sc, "c_test", 0, rfc.EPISODES["test"]) for sp in specs for mp in rf.TRAIN_MAPS + rf.HELDOUT_MAPS
             for sc in rf.SCENARIOS]
    with Pool(jobs) as pool:
        rows = [r for block in pool.imap_unordered(run_block_d, tasks, chunksize=1) for r in block]
    rf.write_rows(out / "test_rows.csv", rows)
    print(f"test: {len(rows)} episodes", flush=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--stage", required=True, choices=["0", "1", "1b", "2", "3", "test", "all"])
    p.add_argument("--out", default="../repro_outputs/v7_fit")
    p.add_argument("--part-d", default="../repro_outputs/v6_fit", help="Part D output (its fitted.json)")
    p.add_argument("--jobs", type=int, default=8)
    p.add_argument("--quick", action="store_true", help="smoke test with tiny budgets and smoke seeds (not for results)")
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rf.SEED_BASES.update(QUICK_SEED_BASES if a.quick else SEED_BASES)
    if a.quick:
        rfc.N_SOBOL, rfc.N_SELECT, rfc.N_ELITE, rfc.DE_GENERATIONS, rfc.N_FINALISTS = 8, 2, 5, 1, 2
        for k in rfc.EPISODES:
            rfc.EPISODES[k] = 2 if k == "test" else 1
    (out / f"run_stage{a.stage}.json").write_text(json.dumps({"stage": a.stage, "quick": a.quick,
                                                              "seed_bases": QUICK_SEED_BASES if a.quick else SEED_BASES,
                                                              "fingerprint": rf.FP, "testbed": rf.testbed_flags(),
                                                              "start": time.strftime("%Y-%m-%d %H:%M:%S")}))
    stages = ["0", "1", "1b", "2", "3", "test"] if a.stage == "all" else [a.stage]
    for s in stages:
        t = time.time()
        {"0": lambda: rfc.stage0(out, a.jobs), "1": lambda: rfc.stage1(out, a.jobs), "1b": lambda: rfc.stage1b(out, a.jobs),
         "2": lambda: rfc.stage2(out, a.jobs), "3": lambda: rfc.stage3(out, a.jobs),
         "test": lambda: stage_test_d(out, a.jobs, Path(a.part_d))}[s]()
        print(f"stage {s} done in {time.time() - t:.0f} s", flush=True)


if __name__ == "__main__":
    main()
