"""Part C of the fitting experiment: parameter regression with an extended parameter set (2026-09-25).

Purpose (user, 2026-09-25): not an exact reproduction of the game logics, but a parameter regression -- which
setting of the unified policy comes closest to each reconstructed game logic (behaviour tree)?  Part B fitted the
four goal weights and the commitment weight with the combat mode fixed per game. Its exploratory analysis located
the shortfall in the fixed mode, in condition-first rules that the graded utilities cannot express, and in the
pursuit of unseen opponents. Part C therefore fits, per tree:
  mode   the combat mode, a discrete parameter (hold, keep moving, chase, evade), chosen on separate seeds
  x      seven continuous parameters in [0, 1]^7:
         u1..u3  goal weights on the simplex (stick-breaking, as in Part B)
         u4      commitment relative to the goal weights, kappa = 0.5 u4 (as in Part B)
         u5      resource_idle_factor = 0.5 u5 (soft status gate; main model 0.25)
         u6      resource_distance_scale = 10^(2 u6), i.e. 1..100 (main model 1)
         u7      hunt_unseen = u7 (pursuit of unseen opponents; main model 0)
All route weights stay 0 (unit-cost A*, as in the trees). Everything else -- episodes, fingerprint, objective J,
standardisation, output formats -- is the machinery of run_fitting.py (frozen for Part B), so that the frozen
analyze_fitting.py evaluates Part C unchanged. New seed bases (none used before): target 4032, train 4029, mode
selection 4033, validation 4031, test 4030; smoke tests 9129-9133.

Stages
  0     targets and scales: trees and designed styles, 50 episodes per game map x scenario (target seeds)
  1     screen: per mode, 512 scrambled-Sobol points (2 episodes per cell); the policy does not depend on the tree,
        so one screen per mode serves all four trees
  1b    mode selection: per tree and mode, the best four screen points on the selection seeds (12 episodes per
        cell); the mode of the lowest objective is the tree's mode
  2     differential evolution in the selected mode from the best 32 screen points of that mode, 4 generations,
        deferred updating, 4 episodes per cell
  3     the best 8 distinct candidates on the validation seeds (12 episodes per cell); lowest objective = fitted
  test  new test seeds, 50 episodes per agent x map x scenario on the four game maps and five held-out maps, for the
        Part C fits (fit[...]), the Part B fits (fitB[...]), the trees, the designed styles and their route-off versions
Outputs in --out: stage0.json, stage0_rows.csv, stage1.json, stage1b.json, stage2_evaluations.jsonl, fitted.json,
test_rows.csv, run_stage<k>.json.
Usage: python experiments/run_fitting_c.py --stage all --out ../repro_outputs/v5_fit --jobs 8 [--quick]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from dataclasses import replace
from multiprocessing import Pool
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting as rf  # noqa: E402

GAMES = list(rf.GAMES)                      # the four trees (the Part B mode of each is rf.GAMES[game])
MODES = [0, 1, 2, 3]
SEED_BASES = {"c_target": 4032, "c_train": 4029, "c_select": 4033, "c_valid": 4031, "c_test": 4030}
QUICK_SEED_BASES = {"c_target": 9132, "c_train": 9129, "c_select": 9133, "c_valid": 9131, "c_test": 9130}
EPISODES = {"target": 50, "screen": 2, "select": 12, "search": 4, "validation": 12, "test": 50}
N_SOBOL, N_SELECT, N_ELITE, DE_GENERATIONS, N_FINALISTS = 512, 4, 32, 4, 8
KAPPA_MAX, G0_MAX, LOG_TAU_MAX = 0.5, 0.5, 2.0
DIM = 7
TARGETS: dict = {}
SCALES: dict = {}
SEARCH_LOG = ""


def params(x) -> dict:
    u = [float(v) for v in x]
    w = rf.simplex(u[0], u[1], u[2])
    return {"w_objective": w[0], "w_engage": w[1], "w_resource": w[2], "w_team": w[3],
            "w_commitment": KAPPA_MAX * u[3], "resource_idle_factor": G0_MAX * u[4],
            "resource_distance_scale": 10.0 ** (LOG_TAU_MAX * u[5]), "hunt_unseen": u[6]}


def fitted_style_c(label: str, mode: int, x) -> object:
    base = rf.default_styles("exp")["Aggressive"]
    return replace(base, name=label, w_exposure=0.0, w_cover=0.0, w_teammate_sep=0.0, combat_mode_override=int(mode),
                   **params(x))


def make_policy_c(spec: tuple):
    kind = spec[0]
    if kind == "fitc":                      # ("fitc", label, mode, *x)
        return fitted_style_c(spec[1], spec[2], spec[3:])
    if kind == "fitB":                      # ("fitB", game, *x): the Part B fit, relabelled
        s = rf.fitted_style(spec[1], spec[2:])
        return replace(s, name=f"fitB[{spec[1]}]")
    return rf.make_policy(spec)


def label_c(spec: tuple) -> str:
    if spec[0] == "fitc":
        return spec[1]
    if spec[0] == "fitB":
        return f"fitB[{spec[1]}]"
    return rf.agent_label(spec)


def run_block_c(task: tuple) -> list[dict]:
    """task = (spec, map, scenario, seed kind, first episode, number) -> metric rows (as rf.run_block)."""
    spec, map_name, scenario, kind, first, n = task
    styles = rf.default_styles("exp")
    sc = next(s for s in rf.default_scenarios() if s.name == scenario)
    policy = make_policy_c(spec)
    rows = []
    for ep in range(first, first + n):
        row = rf.run_episode(sc, policy, styles, rf.fit_seed(kind, map_name, scenario, ep), rf.MAPS[map_name])
        rows.append({"agent": label_c(spec), "map": map_name, "scenario": scenario, "seed_kind": kind,
                     "episode": ep, **row})
    return rows


def summaries(pool, mode: int, points, kind: str, n: int) -> list[dict]:
    """Fingerprint summaries (rf.summarise) of the policy with each parameter point and the given mode."""
    tasks, owner = [], []
    for i, x in enumerate(points):
        spec = ("fitc", "fitc", int(mode), *[float(v) for v in x])
        for mp in rf.TRAIN_MAPS:
            for sc in rf.SCENARIOS:
                tasks.append((spec, mp, sc, kind, 0, n))
                owner.append(i)
    rows = [[] for _ in points]
    for i, block in zip(owner, pool.imap(run_block_c, tasks, chunksize=4)):
        rows[i] += block
    return [rf.summarise(r) for r in rows]


def _init_worker(targets: dict, scales: dict) -> None:
    TARGETS.update(targets)
    SCALES.update(scales)


def _eval_search(x, game, mode):
    rows = []
    spec = ("fitc", "fitc", int(mode), *[float(v) for v in x])
    for mp in rf.TRAIN_MAPS:
        for sc in rf.SCENARIOS:
            rows += run_block_c((spec, mp, sc, "c_train", 0, EPISODES["search"]))
    j = rf.objective_value(rf.summarise(rows), TARGETS[game], SCALES)
    with open(SEARCH_LOG, "a") as fh:
        fh.write(json.dumps({"game": game, "mode": int(mode), "x": [float(v) for v in x], "J": j}) + "\n")
    return j


def load_stage0(out: Path) -> tuple[dict, dict]:
    s0 = json.loads((out / "stage0.json").read_text())
    return s0["targets"], s0["scales"]


# ------------------------------------------------------------------------------------------------ stages
def stage0(out: Path, jobs: int) -> None:
    specs = [("tree", g) for g in GAMES] + [("style", s) for s in rf.STYLE_NAMES]
    tasks = [(sp, mp, sc, "c_target", 0, EPISODES["target"]) for sp in specs for mp in rf.TRAIN_MAPS
             for sc in rf.SCENARIOS]
    with Pool(jobs) as pool:
        rows = [r for block in pool.imap_unordered(run_block_c, tasks) for r in block]
    rf.write_rows(out / "stage0_rows.csv", rows)
    by_agent: dict = {}
    for r in rows:
        by_agent.setdefault(r["agent"], []).append(r)
    summ = {a: rf.summarise(rs) for a, rs in by_agent.items()}
    targets = {g: {"|".join(k): summ[g][k][0] for k in summ[g] if k[2] in rf.FP} for g in GAMES}
    scales, dropped = {}, []
    for d in rf.dims(rf.TRAIN_MAPS):
        means = [summ[a][d][0] for a in summ if d in summ[a]]
        pooled_sd = math.sqrt(np.mean([summ[a][d][1] for a in summ if d in summ[a]]))
        s = max(pooled_sd, 0.05 * (max(means) - min(means)))
        if s <= 0:
            dropped.append("|".join(d))
            continue
        scales["|".join(d)] = s
    (out / "stage0.json").write_text(json.dumps({"targets": targets, "scales": scales, "dropped": dropped,
                                                 "testbed": rf.testbed_flags()}, indent=1))
    print(f"stage 0: {len(rows)} episodes, {len(scales)} dimensions ({len(dropped)} without variation)", flush=True)


def stage1(out: Path, jobs: int) -> None:
    from scipy.stats import qmc
    targets, scales = load_stage0(out)
    pts = qmc.Sobol(d=DIM, scramble=True, seed=rf.SEED_BASES["c_train"]).random_base2(m=int(math.log2(N_SOBOL)))
    res = {"points": pts.tolist(), "J": {}}
    with Pool(jobs) as pool:
        for m in MODES:
            summ = summaries(pool, m, pts, "c_train", EPISODES["screen"])
            res["J"][str(m)] = {g: [rf.objective_value(s, targets[g], scales) for s in summ] for g in GAMES}
            print(f"stage 1 mode {m}: best J " + ", ".join(f"{g} {min(res['J'][str(m)][g]):.2f}" for g in GAMES),
                  flush=True)
    (out / "stage1.json").write_text(json.dumps(res))


def stage1b(out: Path, jobs: int) -> None:
    targets, scales = load_stage0(out)
    s1 = json.loads((out / "stage1.json").read_text())
    pts = s1["points"]
    todo: dict = {}
    for g in GAMES:
        for m in MODES:
            for i in np.argsort(s1["J"][str(m)][g])[:N_SELECT]:
                todo.setdefault(m, set()).add(int(i))
    sel: dict = {}
    with Pool(jobs) as pool:
        for m, idx in todo.items():
            idx = sorted(idx)
            summ = summaries(pool, m, [pts[i] for i in idx], "c_select", EPISODES["select"])
            for i, s in zip(idx, summ):
                sel[(m, i)] = {g: rf.objective_value(s, targets[g], scales) for g in GAMES}
    res = {}
    for g in GAMES:
        per_mode = {}
        for m in MODES:
            cand = [int(i) for i in np.argsort(s1["J"][str(m)][g])[:N_SELECT]]
            per_mode[str(m)] = min(sel[(m, i)][g] for i in cand)
        best = min(MODES, key=lambda m: per_mode[str(m)])
        res[g] = {"selection_J": per_mode, "mode": best}
        print(f"stage 1b {g}: selection J by mode " + ", ".join(f"{m} {per_mode[str(m)]:.2f}" for m in MODES)
              + f" -> mode {best}", flush=True)
    (out / "stage1b.json").write_text(json.dumps(res, indent=1))


def stage2(out: Path, jobs: int) -> None:
    global SEARCH_LOG
    from scipy.optimize import differential_evolution
    targets, scales = load_stage0(out)
    s1 = json.loads((out / "stage1.json").read_text())
    s1b = json.loads((out / "stage1b.json").read_text())
    SEARCH_LOG = str(out / "stage2_evaluations.jsonl")
    bounds = [(0.0, 1.0)] * DIM
    with Pool(jobs, initializer=_init_worker, initargs=(targets, scales)) as pool:
        for g in GAMES:
            m = s1b[g]["mode"]
            order = np.argsort(s1["J"][str(m)][g])[:N_ELITE]
            init = np.array([s1["points"][int(i)] for i in order])
            r = differential_evolution(_eval_search, bounds, args=(g, m), init=init, maxiter=DE_GENERATIONS,
                                       updating="deferred", workers=pool.map, polish=False,
                                       seed=rf.SEED_BASES["c_train"], tol=0.0)
            print(f"stage 2 {g} (mode {m}): best J {r.fun:.3f} ({r.nfev} evaluations)", flush=True)


def stage3(out: Path, jobs: int) -> None:
    targets, scales = load_stage0(out)
    s1b = json.loads((out / "stage1b.json").read_text())
    evals = [json.loads(l) for l in (out / "stage2_evaluations.jsonl").read_text().splitlines() if l.strip()]
    fitted = {}
    with Pool(jobs) as pool:
        for g in GAMES:
            m = s1b[g]["mode"]
            cands, seen = [], set()
            for e in sorted((e for e in evals if e["game"] == g and e["mode"] == m), key=lambda e: e["J"]):
                key = tuple(round(v, 6) for v in e["x"])
                if key not in seen:
                    seen.add(key)
                    cands.append(e)
                if len(cands) == N_FINALISTS:
                    break
            summ = summaries(pool, m, [c["x"] for c in cands], "c_valid", EPISODES["validation"])
            js = [rf.objective_value(s, targets[g], scales) for s in summ]
            b = int(np.argmin(js))
            p = params(cands[b]["x"])
            fitted[g] = {"x": cands[b]["x"], "combat_mode": m,
                         "weights": {k: p[k] for k in ("w_objective", "w_engage", "w_resource", "w_team", "w_commitment")},
                         "extension": {k: p[k] for k in ("resource_idle_factor", "resource_distance_scale", "hunt_unseen")},
                         "train_J": cands[b]["J"], "validation_J": js[b],
                         "finalists": [{"x": c["x"], "train_J": c["J"], "validation_J": j} for c, j in zip(cands, js)]}
            print(f"stage 3 {g} (mode {m}): validation J {js[b]:.3f} (train {cands[b]['J']:.3f}), "
                  + ", ".join(f"{k} {v:.3f}" for k, v in p.items()), flush=True)
    (out / "fitted.json").write_text(json.dumps(fitted, indent=1))


def stage_test(out: Path, jobs: int, part_b: Path) -> None:
    fitted = json.loads((out / "fitted.json").read_text())
    fb = json.loads((part_b / "fitted.json").read_text())
    specs = ([("fitc", f"fit[{g}]", fitted[g]["combat_mode"], *fitted[g]["x"]) for g in GAMES]
             + [("fitB", g, *fb[g]["x"]) for g in GAMES]
             + [("tree", g) for g in GAMES] + [("style", s) for s in rf.STYLE_NAMES]
             + [("style_off", s) for s in rf.STYLE_NAMES])
    tasks = [(sp, mp, sc, "c_test", 0, EPISODES["test"]) for sp in specs for mp in rf.TRAIN_MAPS + rf.HELDOUT_MAPS
             for sc in rf.SCENARIOS]
    with Pool(jobs) as pool:
        rows = [r for block in pool.imap_unordered(run_block_c, tasks, chunksize=1) for r in block]
    rf.write_rows(out / "test_rows.csv", rows)
    print(f"test: {len(rows)} episodes", flush=True)


def main() -> None:
    global N_SOBOL, N_SELECT, N_ELITE, DE_GENERATIONS, N_FINALISTS
    p = argparse.ArgumentParser()
    p.add_argument("--stage", required=True, choices=["0", "1", "1b", "2", "3", "test", "all"])
    p.add_argument("--out", default="../repro_outputs/v5_fit")
    p.add_argument("--part-b", default="../repro_outputs/v4_fit", help="Part B output (its fitted.json)")
    p.add_argument("--jobs", type=int, default=8)
    p.add_argument("--quick", action="store_true", help="smoke test with tiny budgets and smoke seeds (not for results)")
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rf.SEED_BASES.update(QUICK_SEED_BASES if a.quick else SEED_BASES)
    if a.quick:
        N_SOBOL, N_SELECT, N_ELITE, DE_GENERATIONS, N_FINALISTS = 8, 2, 5, 1, 2
        for k in EPISODES:
            EPISODES[k] = 1
    (out / f"run_stage{a.stage}.json").write_text(json.dumps({"stage": a.stage, "quick": a.quick,
                                                              "seed_bases": QUICK_SEED_BASES if a.quick else SEED_BASES,
                                                              "testbed": rf.testbed_flags(),
                                                              "start": time.strftime("%Y-%m-%d %H:%M:%S")}))
    stages = ["0", "1", "1b", "2", "3", "test"] if a.stage == "all" else [a.stage]
    for s in stages:
        t = time.time()
        {"0": lambda: stage0(out, a.jobs), "1": lambda: stage1(out, a.jobs), "1b": lambda: stage1b(out, a.jobs),
         "2": lambda: stage2(out, a.jobs), "3": lambda: stage3(out, a.jobs),
         "test": lambda: stage_test(out, a.jobs, Path(a.part_b))}[s]()
        print(f"stage {s} done in {time.time() - t:.0f} s", flush=True)


if __name__ == "__main__":
    main()
