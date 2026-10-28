"""Part F of the fitting experiment: relief of the commitment penalty for urgent item switches (2026-09-26).

Part E (FITTING_PLAN_E_2026-09-26.md) met H-E1, but the Xonotic tree was not approximated: its fit lay nearer the
AssaultCube tree, and retreat (low status with an enemy visible -> Resource goal; fit 0.21 against 0.72) and far
pursuit accounted for 81% of its squared distance to its tree. In the fitted setting the commitment penalty (0.40)
exceeded every possible resource score (w_resource 0.31), so a weakened agent never left a fight for an item. The user
(2026-09-26) chose one extension: urgent_switch_relief rho in [0, 1], which multiplies the commitment penalty for a
switch to the Resource goal in low status by (1 - rho) and leaves it unchanged otherwise (rho = 0: the main model;
144/144 rows identical, repro_outputs/dev_relief/defaults_compare.txt). Everything else as in Part E: the fingerprint
(four goal-intent metrics and seven behavioural measures), the four combat modes, the budgets, the test.
  x      eight continuous parameters in [0, 1]^8: u1..u7 as in Part C (run_fitting_c.params), u8 = rho
  seeds  new bases: target 8032, train 8029, mode selection 8033, validation 8031, test 8030 (smoke 9429-9433)
  comparison  the Part E fits (fitE[...]; rho = 0, i.e. exactly the Part E policies) on the same test seeds
Implementation: the stages of run_fitting_c.py (frozen for Part C) with run_fitting.FP extended in place as in Part E,
run_fitting_c.params replaced by the eight-parameter mapping and run_fitting_c.DIM = 8 (forked workers inherit the
patches); stage 3 adds rho to the "extension" entry of fitted.json. Usage: python experiments/run_fitting_f.py
--stage all --out ../repro_outputs/v8_fit --jobs 12 [--quick]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting as rf  # noqa: E402

BEHAVIOUR = ["kill_rate_per_100", "death_rate_per_100", "los_frac", "resource_goal_share_good",
             "retreat_share", "far_pursuit_share", "contact_distance"]
rf.FP[:] = rf.FP + [m for m in BEHAVIOUR if m not in rf.FP]           # fingerprint used by summarise / dims / J
rf.OUTCOMES[:] = [m for m in rf.OUTCOMES if m not in rf.FP]            # no metric counted twice in summarise

import run_fitting_c as rfc  # noqa: E402  (imported after the patch; it uses rf.FP through rf)

SEED_BASES = {"c_target": 8032, "c_train": 8029, "c_select": 8033, "c_valid": 8031, "c_test": 8030}
QUICK_SEED_BASES = {"c_target": 9432, "c_train": 9429, "c_select": 9433, "c_valid": 9431, "c_test": 9430}

_params_c = rfc.params


def params_f(x) -> dict:
    """Part C's seven parameters plus rho = u8; a seven-component x (a Part E fit) gets rho = 0."""
    u = [float(v) for v in x]
    return {**_params_c(u[:7]), "urgent_switch_relief": u[7] if len(u) > 7 else 0.0}


rfc.params = params_f                     # used by rfc.fitted_style_c and rfc.stage3
rfc.DIM = 8                               # Sobol screen and differential-evolution bounds


def make_policy_f(spec: tuple):
    if spec[0] == "fitE":                  # ("fitE", game, mode, *x): the Part E fit, relabelled
        return rfc.fitted_style_c(f"fitE[{spec[1]}]", spec[2], spec[3:])
    return rfc.make_policy_c(spec)


def label_f(spec: tuple) -> str:
    return f"fitE[{spec[1]}]" if spec[0] == "fitE" else rfc.label_c(spec)


def run_block_f(task: tuple) -> list[dict]:
    spec, map_name, scenario, kind, first, n = task
    styles = rf.default_styles("exp")
    sc = next(s for s in rf.default_scenarios() if s.name == scenario)
    policy = make_policy_f(spec)
    rows = []
    for ep in range(first, first + n):
        row = rf.run_episode(sc, policy, styles, rf.fit_seed(kind, map_name, scenario, ep), rf.MAPS[map_name])
        rows.append({"agent": label_f(spec), "map": map_name, "scenario": scenario, "seed_kind": kind,
                     "episode": ep, **row})
    return rows


def stage3_f(out: Path, jobs: int) -> None:
    rfc.stage3(out, jobs)
    fitted = json.loads((out / "fitted.json").read_text())
    for g in fitted:
        fitted[g]["extension"]["urgent_switch_relief"] = params_f(fitted[g]["x"])["urgent_switch_relief"]
    (out / "fitted.json").write_text(json.dumps(fitted, indent=1))


def stage_test_f(out: Path, jobs: int, part_e: Path) -> None:
    fitted = json.loads((out / "fitted.json").read_text())
    fe = json.loads((part_e / "fitted.json").read_text())
    specs = ([("fitc", f"fit[{g}]", fitted[g]["combat_mode"], *fitted[g]["x"]) for g in rfc.GAMES]
             + [("fitE", g, fe[g]["combat_mode"], *fe[g]["x"]) for g in rfc.GAMES]
             + [("tree", g) for g in rfc.GAMES] + [("style", s) for s in rf.STYLE_NAMES]
             + [("style_off", s) for s in rf.STYLE_NAMES])
    tasks = [(sp, mp, sc, "c_test", 0, rfc.EPISODES["test"]) for sp in specs for mp in rf.TRAIN_MAPS + rf.HELDOUT_MAPS
             for sc in rf.SCENARIOS]
    with Pool(jobs) as pool:
        rows = [r for block in pool.imap_unordered(run_block_f, tasks, chunksize=1) for r in block]
    rf.write_rows(out / "test_rows.csv", rows)
    print(f"test: {len(rows)} episodes", flush=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--stage", required=True, choices=["0", "1", "1b", "2", "3", "test", "all"])
    p.add_argument("--out", default="../repro_outputs/v8_fit")
    p.add_argument("--part-e", default="../repro_outputs/v7_fit", help="Part E output (its fitted.json)")
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
                                                              "fingerprint": rf.FP, "dim": rfc.DIM,
                                                              "testbed": rf.testbed_flags(),
                                                              "start": time.strftime("%Y-%m-%d %H:%M:%S")}))
    stages = ["0", "1", "1b", "2", "3", "test"] if a.stage == "all" else [a.stage]
    for s in stages:
        t = time.time()
        {"0": lambda: rfc.stage0(out, a.jobs), "1": lambda: rfc.stage1(out, a.jobs), "1b": lambda: rfc.stage1b(out, a.jobs),
         "2": lambda: rfc.stage2(out, a.jobs), "3": lambda: stage3_f(out, a.jobs),
         "test": lambda: stage_test_f(out, a.jobs, Path(a.part_e))}[s]()
        print(f"stage {s} done in {time.time() - t:.0f} s", flush=True)


if __name__ == "__main__":
    main()
