"""Round I (v16) of the fitting experiment (DRAFT protocol FITTING_PLAN_I_DRAFT.md, 2026-09-30; not frozen, not run):
per-scenario fits. The pooled fit of Part G-fit gives one setting per tree over the three scenarios (Table 6 of the
journal draft); this round fits one setting per game-scenario case, in the scenarios the game's logic targets (user's
decision of 2026-09-30: "시나리오마다 다른 값을 얻으려면 시나리오별 적합(여섯 번 탐색) 먼저 해보자"):
  CSO-BT in Mission and in Control, OW-BT in Mission and in Control, AC-BT in Deathmatch, XO-BT in Deathmatch.

Procedure: Part G-fit (run_fitting_g.py) with the objective restricted to the case's scenario. Per case the objective J
is the Part E fingerprint on that scenario's dimensions of the four game maps (41 for Mission or Control, 37 for
Deathmatch, of the 119), with the stage-0 targets and scales of this round.
  check  reproduction check on already-used seeds (no new seeds): the four trees and the four G-fit fits against
         repro_outputs/v11_fit/test_rows.csv (seed base 11030), as in run_fitting_h.py
  0      targets and scales: 4 trees + 4 designed styles x 4 game maps x 3 scenarios x 50 episodes (run_fitting_c.stage0)
  1      screen: per mode, 512 scrambled-Sobol points on all 12 cells (2 episodes per cell; run_fitting_c.summaries);
         the objective of every case is computed from the same episodes (the policy does not depend on the case)
  1b     mode ranking per case: the best 4 screen points of each mode on the selection seeds, 12 episodes per cell of
         the case's scenario; the modes ranked by the lowest objective, the best 2 searched
  2      differential evolution per case and searched mode, from the best 32 screen points of that mode, 4
         generations, deferred updating, 4 episodes per cell of the case's scenario
  3      validation per case: the 8 best distinct candidates of each searched mode (16) on the validation seeds, 12
         episodes per cell of the case's scenario; the lowest validation objective is the fitted setting of the case
  test   new test seeds, 50 episodes per agent x map x scenario on the 4 game maps and 5 held-out maps: the six case fits
         (fitsc[<tree>:<scenario>]) in their scenario, the trees in the native scenarios of their tree (the targets and
         the identification candidates), and the designed styles and their route-off versions in all three scenarios
         (gap-closure denominators, held-out scales). Nothing else is run (user, 2026-09-30: only the six fitted
         settings; no earlier fits, no hand-set settings)
Seeds (never used before): target 16032, train 16029, mode selection 16033, validation 16031, test 16030; smoke
16529-16533.
Outputs in --out: check.txt, check_rows.csv, stage0.json, stage0_rows.csv, stage1.json, stage1b.json,
stage2_evaluations.jsonl, fitted.json (per case, with the 16 finalists), test_rows.csv, run_stage<k>.json.
Usage: python experiments/run_fitting_i.py --stage all --out ../repro_outputs/v16_scenario_fit --jobs 12 [--quick]
"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting_h as rfh  # noqa: E402  (NATIVE, the reproduction check against the G-fit test rows, run_block_h;
#                                          Part E fingerprint and the eight-parameter mapping through run_fitting_f)

rff, rf, rfc = rfh.rff, rfh.rf, rfh.rfc

ROOT = Path(__file__).resolve().parents[2]
SEED_BASES = {"c_target": 16032, "c_train": 16029, "c_select": 16033, "c_valid": 16031, "c_test": 16030}
QUICK_SEED_BASES = {"c_target": 16532, "c_train": 16529, "c_select": 16533, "c_valid": 16531, "c_test": 16530}
CHECK_BASES = dict(rfh.CHECK_BASES)                       # {"chk_v11": 11030}: already used, check only
N_MODES = 2                                               # modes searched per case
HASHED = list(rfh.HASHED)
CASES = [(g, sc) for g in rfc.GAMES for sc in rfh.NATIVE[g]]


def key_of(game: str, scen: str) -> str:
    return f"{game}|{scen}"


def label_of(game: str, scen: str) -> str:
    return f"fitsc[{game}:{scen}]"


def case_scales(scales: dict, scen: str) -> dict:
    """The stage-0 scales restricted to one scenario's dimensions (keys 'map|scenario|metric')."""
    return {k: v for k, v in scales.items() if k.split("|")[1] == scen}


def summaries_sc(pool, mode: int, points, kind: str, n: int, scen: str) -> list[dict]:
    """run_fitting_c.summaries restricted to one scenario's cells of the four game maps."""
    tasks, owner = [], []
    for i, x in enumerate(points):
        spec = ("fitc", "fitc", int(mode), *[float(v) for v in x])
        for mp in rf.TRAIN_MAPS:
            tasks.append((spec, mp, scen, kind, 0, n))
            owner.append(i)
    rows = [[] for _ in points]
    for i, block in zip(owner, pool.imap(rfc.run_block_c, tasks, chunksize=1)):
        rows[i] += block
    return [rf.summarise(r) for r in rows]


# --- stage 2 workers ---------------------------------------------------------------------------------------------
TARGETS: dict = {}
CASE_SCALES: dict = {}
SEARCH_LOG = ""


def _init_worker_i(targets: dict, cscales: dict) -> None:
    TARGETS.update(targets)
    CASE_SCALES.update(cscales)


def _eval_search_i(x, key: str, mode: int) -> float:
    game, scen = key.split("|")
    spec = ("fitc", "fitc", int(mode), *[float(v) for v in x])
    rows = []
    for mp in rf.TRAIN_MAPS:
        rows += rfc.run_block_c((spec, mp, scen, "c_train", 0, rfc.EPISODES["search"]))
    j = rf.objective_value(rf.summarise(rows), TARGETS[game], CASE_SCALES[key])
    with open(SEARCH_LOG, "a") as fh:
        fh.write(json.dumps({"case": key, "game": game, "scenario": scen, "mode": int(mode),
                             "x": [float(v) for v in x], "J": j}) + "\n")
    return j


# --- stages ------------------------------------------------------------------------------------------------------
def stage1_i(out: Path, jobs: int) -> None:
    """Screen as in run_fitting_c.stage1 (one screen per mode on all 12 cells), with the objective of every case."""
    from scipy.stats import qmc
    targets, scales = rfc.load_stage0(out)
    pts = qmc.Sobol(d=rfc.DIM, scramble=True, seed=rf.SEED_BASES["c_train"]).random_base2(m=int(math.log2(rfc.N_SOBOL)))
    res = {"points": pts.tolist(), "J": {}}
    with Pool(jobs) as pool:
        for m in rfc.MODES:
            summ = rfc.summaries(pool, m, pts, "c_train", rfc.EPISODES["screen"])
            res["J"][str(m)] = {key_of(g, sc): [rf.objective_value(s, targets[g], case_scales(scales, sc)) for s in summ]
                                for g, sc in CASES}
            print(f"stage 1 mode {m}: best J " + ", ".join(f"{k} {min(v):.2f}" for k, v in res["J"][str(m)].items()),
                  flush=True)
    (out / "stage1.json").write_text(json.dumps(res))


def stage1b_i(out: Path, jobs: int) -> None:
    """Mode ranking per case on the selection seeds, in the case's scenario; the best N_MODES are searched."""
    targets, scales = rfc.load_stage0(out)
    s1 = json.loads((out / "stage1.json").read_text())
    pts = s1["points"]
    todo: dict = {}                                       # (mode, scenario) -> screen points to run
    for g, sc in CASES:
        for m in rfc.MODES:
            for i in np.argsort(s1["J"][str(m)][key_of(g, sc)])[:rfc.N_SELECT]:
                todo.setdefault((m, sc), set()).add(int(i))
    summ_of: dict = {}
    with Pool(jobs) as pool:
        for (m, sc), idx in sorted(todo.items()):
            idx = sorted(idx)
            for i, s in zip(idx, summaries_sc(pool, m, [pts[i] for i in idx], "c_select", rfc.EPISODES["select"], sc)):
                summ_of[(m, sc, i)] = s
    res = {}
    for g, sc in CASES:
        key = key_of(g, sc)
        cs = case_scales(scales, sc)
        per_mode = {}
        for m in rfc.MODES:
            cand = [int(i) for i in np.argsort(s1["J"][str(m)][key])[:rfc.N_SELECT]]
            per_mode[str(m)] = min(rf.objective_value(summ_of[(m, sc, i)], targets[g], cs) for i in cand)
        modes = sorted(rfc.MODES, key=lambda m: per_mode[str(m)])[:N_MODES]    # stable: ties to the lower index
        res[key] = {"game": g, "scenario": sc, "selection_J": per_mode, "mode": modes[0], "modes": modes}
        print(f"stage 1b {key}: selection J by mode " + ", ".join(f"{m} {per_mode[str(m)]:.2f}" for m in rfc.MODES)
              + f" -> searched modes {modes}", flush=True)
    (out / "stage1b.json").write_text(json.dumps(res, indent=1))


def stage2_i(out: Path, jobs: int) -> None:
    """Differential evolution per case and searched mode (run_fitting_c.stage2 budgets; one evaluation log)."""
    global SEARCH_LOG
    from scipy.optimize import differential_evolution
    targets, scales = rfc.load_stage0(out)
    s1 = json.loads((out / "stage1.json").read_text())
    s1b = json.loads((out / "stage1b.json").read_text())
    SEARCH_LOG = str(out / "stage2_evaluations.jsonl")   # read by _eval_search_i in the forked workers
    cscales = {key_of(g, sc): case_scales(scales, sc) for g, sc in CASES}
    bounds = [(0.0, 1.0)] * rfc.DIM
    with Pool(jobs, initializer=_init_worker_i, initargs=(targets, cscales)) as pool:
        for g, sc in CASES:
            key = key_of(g, sc)
            for m in s1b[key]["modes"]:
                order = np.argsort(s1["J"][str(m)][key])[:rfc.N_ELITE]
                init = np.array([s1["points"][int(i)] for i in order])
                r = differential_evolution(_eval_search_i, bounds, args=(key, m), init=init,
                                           maxiter=rfc.DE_GENERATIONS, updating="deferred", workers=pool.map,
                                           polish=False, seed=rf.SEED_BASES["c_train"], tol=0.0)
                print(f"stage 2 {key} (mode {m}): best J {r.fun:.3f} ({r.nfev} evaluations)", flush=True)


def stage3_i(out: Path, jobs: int) -> None:
    """Validation per case: the N_FINALISTS best distinct candidates of each searched mode; the lowest validation
    objective is the fitted setting."""
    targets, scales = rfc.load_stage0(out)
    s1b = json.loads((out / "stage1b.json").read_text())
    evals = [json.loads(l) for l in (out / "stage2_evaluations.jsonl").read_text().splitlines() if l.strip()]
    fitted = {}
    with Pool(jobs) as pool:
        for g, sc in CASES:
            key = key_of(g, sc)
            cs = case_scales(scales, sc)
            finalists = []
            for m in s1b[key]["modes"]:
                cands, seen = [], set()
                for e in sorted((e for e in evals if e["case"] == key and e["mode"] == m), key=lambda e: e["J"]):
                    k = tuple(round(v, 6) for v in e["x"])
                    if k not in seen:
                        seen.add(k)
                        cands.append(e)
                    if len(cands) == rfc.N_FINALISTS:
                        break
                summ = summaries_sc(pool, m, [c["x"] for c in cands], "c_valid", rfc.EPISODES["validation"], sc)
                finalists += [{"x": c["x"], "mode": m, "train_J": c["J"],
                               "validation_J": rf.objective_value(s, targets[g], cs)} for c, s in zip(cands, summ)]
            b = min(finalists, key=lambda f: f["validation_J"])          # first minimum: ties to the earlier candidate
            p = rff.params_f(b["x"])
            fitted[key] = {"game": g, "scenario": sc, "x": b["x"], "combat_mode": b["mode"],
                           "searched_modes": s1b[key]["modes"], "params": p,
                           "weights": {k: p[k] for k in ("w_objective", "w_engage", "w_resource", "w_team", "w_commitment")},
                           "extension": {k: p[k] for k in ("resource_idle_factor", "resource_distance_scale",
                                                           "hunt_unseen", "urgent_switch_relief")},
                           "train_J": b["train_J"], "validation_J": b["validation_J"], "finalists": finalists}
            print(f"stage 3 {key} (mode {b['mode']} of {s1b[key]['modes']}): validation J {b['validation_J']:.3f} "
                  f"(train {b['train_J']:.3f}), " + ", ".join(f"{k} {v:.3f}" for k, v in p.items()), flush=True)
    (out / "fitted.json").write_text(json.dumps(fitted, indent=1))


def stage_test_i(out: Path, jobs: int) -> None:
    """Test: the six case fits in their scenario, the trees in their native scenarios, the designed styles and their
    route-off versions in all scenarios; game maps and held-out maps."""
    fitted = json.loads((out / "fitted.json").read_text())
    maps = rf.TRAIN_MAPS + rf.HELDOUT_MAPS
    n = rfc.EPISODES["test"]
    tasks = []
    for g, sc in CASES:
        f = fitted[key_of(g, sc)]
        sp = ("fitx", label_of(g, sc), int(f["combat_mode"]), *[float(v) for v in f["x"]])
        tasks += [(sp, mp, sc, "c_test", 0, n) for mp in maps]
    for g in rfc.GAMES:
        tasks += [(("tree", g), mp, sc, "c_test", 0, n) for mp in maps for sc in rfh.NATIVE[g]]
    for s in rf.STYLE_NAMES:
        tasks += [(sp, mp, sc, "c_test", 0, n) for sp in (("style", s), ("style_off", s)) for mp in maps
                  for sc in rf.SCENARIOS]
    with Pool(jobs) as pool:
        rows = [r for b in pool.imap_unordered(rfh.run_block_h, tasks, chunksize=1) for r in b]
    rf.write_rows(out / "test_rows.csv", rows)
    print(f"test: {len(rows)} episodes", flush=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--stage", required=True, choices=["check", "0", "1", "1b", "2", "3", "test", "all"])
    p.add_argument("--out", default="../repro_outputs/v16_scenario_fit")
    p.add_argument("--jobs", type=int, default=12)
    p.add_argument("--quick", action="store_true", help="smoke test with tiny budgets and smoke seeds (not for results)")
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    bases = QUICK_SEED_BASES if a.quick else SEED_BASES
    rf.SEED_BASES.update(bases)
    if a.quick:
        rfc.N_SOBOL, rfc.N_SELECT, rfc.N_ELITE, rfc.DE_GENERATIONS, rfc.N_FINALISTS = 8, 2, 5, 1, 2
        for k in rfc.EPISODES:
            rfc.EPISODES[k] = 2 if k == "test" else 1
    import scipy
    _, fit_rec = rfh.fit_specs()                              # the G-fit fits: reproduction-check input only
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    (out / f"run_stage{a.stage}.json").write_text(json.dumps({
        "stage": a.stage, "quick": a.quick, "seed_bases": bases, "check_bases": CHECK_BASES, "fingerprint": rf.FP,
        "dim": rfc.DIM, "cases": [key_of(g, sc) for g, sc in CASES], "modes_searched_per_case": N_MODES,
        "budgets": {"N_SOBOL": rfc.N_SOBOL, "N_SELECT": rfc.N_SELECT, "N_ELITE": rfc.N_ELITE,
                    "DE_GENERATIONS": rfc.DE_GENERATIONS, "N_FINALISTS": rfc.N_FINALISTS, "episodes": rfc.EPISODES},
        "check_fits": fit_rec, "sha256": {f: rfh.sha256(ROOT / f) for f in HASHED}, "git_head": head,
        "versions": {"python": sys.version.split()[0], "numpy": np.__version__, "scipy": scipy.__version__},
        "testbed": rf.testbed_flags(), "start": time.strftime("%Y-%m-%d %H:%M:%S")}, indent=1))
    stages = ["check", "0", "1", "1b", "2", "3", "test"] if a.stage == "all" else [a.stage]
    for s in stages:
        t = time.time()
        if s == "check":
            if not rfh.stage_check(out, a.jobs) and a.stage == "all":
                sys.exit("reproduction check failed: not running the fit")
            rf.SEED_BASES.update(bases)
        else:
            {"0": lambda: rfc.stage0(out, a.jobs), "1": lambda: stage1_i(out, a.jobs),
             "1b": lambda: stage1b_i(out, a.jobs), "2": lambda: stage2_i(out, a.jobs),
             "3": lambda: stage3_i(out, a.jobs), "test": lambda: stage_test_i(out, a.jobs)}[s]()
        print(f"stage {s} done in {time.time() - t:.0f} s", flush=True)


if __name__ == "__main__":
    main()
