"""Part G-fit of the fitting experiment (DRAFT protocol FITTING_PLAN_G_FIT_DRAFT.md, 2026-09-27; not frozen): a new fit
of all four trees against the adopted trees (the targets of Part G-eval: default_baselines() since commit e0e7525;
CSO-BT and OW-BT unchanged since Part C).

Everything as in Part F (run_fitting_f.py: the Part E fingerprint, the eight-parameter mapping params_f, the stages and
budgets of run_fitting_c.py), except:
  search      stage 1b ranks the four modes by their selection objective (run_fitting_c.stage1b unchanged, the ranking
              added to stage1b.json as "modes"); the two best modes each get differential evolution from their best 32
              screen points (stage 2); stage 3 validates the 8 best distinct candidates of each of the two modes
              (16 per tree), and the lowest validation objective is the fitted policy (its mode is the fitted mode)
  diagnostic  the six fits evaluated in Part G-eval (the Part F fits of the four trees; the Part D and E Xonotic fits)
              and the Part E Overwatch fit (fitE[OW-BT], hold; diagnostic only, not in the test; added after the review
              of 2026-09-28) are also evaluated on the validation seeds against their own tree; not eligible
              (validation_diagnostic.json)
  test        the new fits (fit[...]), the six earlier fits as pre-specified comparisons (fitF[...], fitD[XO-BT],
              fitE[XO-BT]; a seven-component x gets rho = 0, i.e. exactly the Part D / E policy), the adopted trees, the
              designed styles and their route-off versions
  check       before stage 0, on already-used seeds only: episodes 0-1 of every map and scenario of the four adopted
              trees and of fitD[XO-BT] and fitE[XO-BT] against repro_outputs/v10_eval/test_rows.csv (seed base 10030),
              and of fitF[XO-BT] against repro_outputs/v8_fit/test_rows.csv (seed base 8030), column by column (columns
              present in only one of the two rows are listed); with --stage all the run stops on any differing episode
              (stage_check and the fit loading follow run_fitting_g_eval.py, which stays frozen for Part G-eval)
Seeds (never used before): target 11032, train 11029, mode selection 11033, validation 11031, test 11030; smoke
10529-10533.
Outputs in --out: check.txt, check_rows.csv, stage0.json, stage0_rows.csv, stage1.json, stage1b.json,
stage2_evaluations.jsonl, fitted.json (with "searched_modes" and the 16 finalists), validation_diagnostic.json,
test_rows.csv, run_stage<k>.json (seeds, budgets, comparison and diagnostic fits, SHA-256 of the tree and policy code,
git HEAD, python / numpy / scipy versions).
Usage: python experiments/run_fitting_g.py --stage all --out ../repro_outputs/v11_fit --jobs 12 [--quick]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting_f as rff  # noqa: E402  (Part E fingerprint; eight-parameter mapping, a 7-component x gets rho = 0)

rf, rfc = rff.rf, rff.rfc

ROOT = Path(__file__).resolve().parents[2]
FIT_DIRS = {"D": ROOT / "repro_outputs" / "v6_fit", "E": ROOT / "repro_outputs" / "v7_fit",
            "F": ROOT / "repro_outputs" / "v8_fit"}
EVAL_DIR = ROOT / "repro_outputs" / "v10_eval"
SEED_BASES = {"c_target": 11032, "c_train": 11029, "c_select": 11033, "c_valid": 11031, "c_test": 11030}
QUICK_SEED_BASES = {"c_target": 10532, "c_train": 10529, "c_select": 10533, "c_valid": 10531, "c_test": 10530}
CHECK_BASES = {"chk_v10": 10030, "chk_v8": 8030}          # already used (G-eval / Part F test seeds): check only
N_MODES = 2                                                 # modes searched per tree
HASHED = ["code/fps_priority_ai/baselines.py", "code/fps_priority_ai/policy.py", "code/fps_priority_ai/config.py"]
COMPARISONS = [("fitF[CSO-BT]", "F", "CSO-BT"), ("fitF[OW-BT]", "F", "OW-BT"), ("fitF[AC-BT]", "F", "AC-BT"),
               ("fitF[XO-BT]", "F", "XO-BT"), ("fitD[XO-BT]", "D", "XO-BT"), ("fitE[XO-BT]", "E", "XO-BT")]
DIAGNOSTIC_ONLY = [("fitE[OW-BT]", "E", "OW-BT")]           # validation diagnostic only, not in the test


def comparison_specs(items=None) -> tuple[list[tuple], dict]:
    """Earlier fits (default: the six comparisons) as ("fitc", label, mode, *x) specs (run_fitting_c.make_policy_c /
    label_c), and a record of their sources."""
    fits = {k: json.loads((d / "fitted.json").read_text()) for k, d in FIT_DIRS.items()}
    specs, rec = [], {}
    for label, part, game in (COMPARISONS if items is None else items):
        f = fits[part][game]
        specs.append(("fitc", label, int(f["combat_mode"]), *[float(v) for v in f["x"]]))
        rec[label] = {"part": part, "game": game, "source": str((FIT_DIRS[part] / "fitted.json").relative_to(ROOT)),
                      "combat_mode": f["combat_mode"], "x": f["x"], "params": rff.params_f(f["x"])}
    return specs, rec


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ------------------------------------------------------------------------------------------------ stages
def stage_check(out: Path, jobs: int, episodes: int = 2) -> bool:
    """Reproduction check on already-used seeds: the adopted trees and the Part D and E Xonotic fits must reproduce the
    stored G-eval test rows, and the Part F Xonotic fit its stored Part F test rows, in every shared column."""
    rf.SEED_BASES.update(CHECK_BASES)
    by = {s[1]: s for s in comparison_specs()[0]}
    plan = [(("tree", g), "chk_v10", EVAL_DIR / "test_rows.csv", g) for g in rfc.GAMES]   # (spec, kind, file, label)
    plan += [(by[lb], "chk_v10", EVAL_DIR / "test_rows.csv", lb) for lb in ("fitD[XO-BT]", "fitE[XO-BT]")]
    plan.append((by["fitF[XO-BT]"], "chk_v8", FIT_DIRS["F"] / "test_rows.csv", "fit[XO-BT]"))
    maps = rf.TRAIN_MAPS + rf.HELDOUT_MAPS
    tasks = [(sp, mp, sc, kind, 0, episodes) for sp, kind, _, _ in plan for mp in maps for sc in rf.SCENARIOS]
    with Pool(jobs) as pool:
        rows = [r for b in pool.imap_unordered(rfc.run_block_c, tasks, chunksize=1) for r in b]
    rf.write_rows(out / "check_rows.csv", rows)
    new = {}
    with (out / "check_rows.csv").open() as fh:
        for r in csv.DictReader(fh):
            new[(r["agent"], r["map"], r["scenario"], r["episode"])] = r
    lines, ok_all = [], True
    for sp, kind, path, stored in plan:
        old = {}
        with path.open() as fh:
            for r in csv.DictReader(fh):
                if r["agent"] == stored and int(r["episode"]) < episodes:
                    old[(r["map"], r["scenario"], r["episode"])] = r
        n = same = 0
        diffs: dict = {}
        unshared: set = set()
        for (m, sc, ep), o in old.items():
            nr = new[(rfc.label_c(sp), m, sc, ep)]
            cols = [c for c in o if c in nr and c not in ("agent", "seed_kind")]
            unshared |= set(o) ^ set(nr)
            n += 1
            bad = [c for c in cols if o[c] != nr[c]]
            same += not bad
            for c in bad:
                diffs[c] = diffs.get(c, 0) + 1
        ok = n > 0 and same == n
        ok_all &= ok
        lines.append(f"{rfc.label_c(sp)} vs {path.parent.name} '{stored}' (seed base {CHECK_BASES[kind]}): {same}/{n} "
                     f"episodes identical in every shared column" + ("" if ok else f"; differing columns {diffs}")
                     + (f"; columns in only one of the two rows: {sorted(unshared)}" if unshared else
                        "; same columns"))
    lines.append("REPRODUCTION CHECK " + ("PASSED" if ok_all else "FAILED"))
    (out / "check.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)
    return ok_all


def stage1b_g(out: Path, jobs: int) -> None:
    """Stage 1b of Part C unchanged, then the modes ranked by their selection objective; the best N_MODES are
    searched."""
    rfc.stage1b(out, jobs)
    s1b = json.loads((out / "stage1b.json").read_text())
    for g, r in s1b.items():
        r["modes"] = sorted(rfc.MODES, key=lambda m: r["selection_J"][str(m)])[:N_MODES]
        print(f"stage 1b {g}: searched modes {r['modes']}", flush=True)
    (out / "stage1b.json").write_text(json.dumps(s1b, indent=1))


def stage2_g(out: Path, jobs: int) -> None:
    """Differential evolution as in run_fitting_c.stage2, in each searched mode of every tree (one evaluation log)."""
    from scipy.optimize import differential_evolution
    targets, scales = rfc.load_stage0(out)
    s1 = json.loads((out / "stage1.json").read_text())
    s1b = json.loads((out / "stage1b.json").read_text())
    rfc.SEARCH_LOG = str(out / "stage2_evaluations.jsonl")     # read by rfc._eval_search in the forked workers
    bounds = [(0.0, 1.0)] * rfc.DIM
    with Pool(jobs, initializer=rfc._init_worker, initargs=(targets, scales)) as pool:
        for g in rfc.GAMES:
            for m in s1b[g]["modes"]:
                order = np.argsort(s1["J"][str(m)][g])[:rfc.N_ELITE]
                init = np.array([s1["points"][int(i)] for i in order])
                r = differential_evolution(rfc._eval_search, bounds, args=(g, m), init=init,
                                           maxiter=rfc.DE_GENERATIONS, updating="deferred", workers=pool.map,
                                           polish=False, seed=rf.SEED_BASES["c_train"], tol=0.0)
                print(f"stage 2 {g} (mode {m}): best J {r.fun:.3f} ({r.nfev} evaluations)", flush=True)


def stage3_g(out: Path, jobs: int) -> None:
    """The N_FINALISTS best distinct candidates of each searched mode on the validation seeds; the lowest validation
    objective is the fitted policy. The six earlier fits and fitE[OW-BT] are evaluated against their own tree as a
    diagnostic, after the selection."""
    targets, scales = rfc.load_stage0(out)
    s1b = json.loads((out / "stage1b.json").read_text())
    evals = [json.loads(l) for l in (out / "stage2_evaluations.jsonl").read_text().splitlines() if l.strip()]
    fitted, diag = {}, {}
    with Pool(jobs) as pool:
        for g in rfc.GAMES:
            finalists = []
            for m in s1b[g]["modes"]:
                cands, seen = [], set()
                for e in sorted((e for e in evals if e["game"] == g and e["mode"] == m), key=lambda e: e["J"]):
                    key = tuple(round(v, 6) for v in e["x"])
                    if key not in seen:
                        seen.add(key)
                        cands.append(e)
                    if len(cands) == rfc.N_FINALISTS:
                        break
                summ = rfc.summaries(pool, m, [c["x"] for c in cands], "c_valid", rfc.EPISODES["validation"])
                finalists += [{"x": c["x"], "mode": m, "train_J": c["J"],
                               "validation_J": rf.objective_value(s, targets[g], scales)} for c, s in zip(cands, summ)]
            b = min(finalists, key=lambda f: f["validation_J"])
            p = rff.params_f(b["x"])
            fitted[g] = {"x": b["x"], "combat_mode": b["mode"], "searched_modes": s1b[g]["modes"],
                         "weights": {k: p[k] for k in ("w_objective", "w_engage", "w_resource", "w_team", "w_commitment")},
                         "extension": {k: p[k] for k in ("resource_idle_factor", "resource_distance_scale",
                                                         "hunt_unseen", "urgent_switch_relief")},
                         "train_J": b["train_J"], "validation_J": b["validation_J"], "finalists": finalists}
            print(f"stage 3 {g} (mode {b['mode']} of {s1b[g]['modes']}): validation J {b['validation_J']:.3f} "
                  f"(train {b['train_J']:.3f}), " + ", ".join(f"{k} {v:.3f}" for k, v in p.items()), flush=True)
        specs, _ = comparison_specs(COMPARISONS + DIAGNOSTIC_ONLY)
        for sp in specs:
            label, m, x = sp[1], sp[2], list(sp[3:])
            game = next(gm for lb, _, gm in COMPARISONS + DIAGNOSTIC_ONLY if lb == label)
            s = rfc.summaries(pool, m, [x], "c_valid", rfc.EPISODES["validation"])[0]
            diag[label] = {"game": game, "mode": m, "validation_J": rf.objective_value(s, targets[game], scales)}
            print(f"stage 3 diagnostic {label}: validation J {diag[label]['validation_J']:.3f} "
                  f"(fit[{game}] {fitted[game]['validation_J']:.3f})", flush=True)
    (out / "fitted.json").write_text(json.dumps(fitted, indent=1))
    (out / "validation_diagnostic.json").write_text(json.dumps(diag, indent=1))


def stage_test_g(out: Path, jobs: int) -> None:
    fitted = json.loads((out / "fitted.json").read_text())
    comp, _ = comparison_specs()
    specs = ([("fitc", f"fit[{g}]", fitted[g]["combat_mode"], *fitted[g]["x"]) for g in rfc.GAMES] + comp
             + [("tree", g) for g in rfc.GAMES] + [("style", s) for s in rf.STYLE_NAMES]
             + [("style_off", s) for s in rf.STYLE_NAMES])
    tasks = [(sp, mp, sc, "c_test", 0, rfc.EPISODES["test"]) for sp in specs for mp in rf.TRAIN_MAPS + rf.HELDOUT_MAPS
             for sc in rf.SCENARIOS]
    with Pool(jobs) as pool:
        rows = [r for block in pool.imap_unordered(rfc.run_block_c, tasks, chunksize=1) for r in block]
    rf.write_rows(out / "test_rows.csv", rows)
    print(f"test: {len(rows)} episodes", flush=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--stage", required=True, choices=["check", "0", "1", "1b", "2", "3", "test", "all"])
    p.add_argument("--out", default="../repro_outputs/v11_fit")
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
    _, rec = comparison_specs()
    _, rec_diag = comparison_specs(DIAGNOSTIC_ONLY)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    (out / f"run_stage{a.stage}.json").write_text(json.dumps({
        "stage": a.stage, "quick": a.quick, "seed_bases": bases, "check_bases": CHECK_BASES, "fingerprint": rf.FP,
        "dim": rfc.DIM, "modes_searched_per_tree": N_MODES,
        "budgets": {"N_SOBOL": rfc.N_SOBOL, "N_SELECT": rfc.N_SELECT, "N_ELITE": rfc.N_ELITE,
                    "DE_GENERATIONS": rfc.DE_GENERATIONS, "N_FINALISTS": rfc.N_FINALISTS, "episodes": rfc.EPISODES},
        "comparisons": rec, "diagnostic_only": rec_diag, "sha256": {f: sha256(ROOT / f) for f in HASHED},
        "git_head": head, "versions": {"python": sys.version.split()[0], "numpy": np.__version__,
                                       "scipy": scipy.__version__},
        "testbed": rf.testbed_flags(), "start": time.strftime("%Y-%m-%d %H:%M:%S")}, indent=1))
    stages = ["check", "0", "1", "1b", "2", "3", "test"] if a.stage == "all" else [a.stage]
    for s in stages:
        t = time.time()
        if s == "check":
            if not stage_check(out, a.jobs) and a.stage == "all":
                sys.exit("reproduction check failed: not running the fit")
            rf.SEED_BASES.update(bases)
        else:
            {"0": lambda: rfc.stage0(out, a.jobs), "1": lambda: rfc.stage1(out, a.jobs),
             "1b": lambda: stage1b_g(out, a.jobs), "2": lambda: stage2_g(out, a.jobs),
             "3": lambda: stage3_g(out, a.jobs), "test": lambda: stage_test_g(out, a.jobs)}[s]()
        print(f"stage {s} done in {time.time() - t:.0f} s", flush=True)


if __name__ == "__main__":
    main()
