"""Part G-eval of the fitting experiment (DRAFT protocol FITTING_PLAN_G_EVAL_DRAFT.md, 2026-09-27; not frozen, not run):
an evaluation-only re-test of existing fits against the revised AssaultCube and Xonotic trees. Nothing is fitted.

After the tree review (paper/REVIEW_trees_2026-09-27.md) the user fixed the targets (commit e0e7525): the Xonotic tree
keeps its goal for the havocbot strategy timer with the early re-rating rules, the AssaultCube tree uses one length
scale (25 units per cell) and source-like hunting. default_baselines() returns these revised trees; the dataclass
defaults of BaselineStyle reproduce the trees of Parts D-F (per-step Xonotic tree, 2026-09-25 AssaultCube tree).

Agents (labels in test_rows.csv)
  fit[CSO-BT], fit[OW-BT], fit[AC-BT], fit[XO-BT]  the Part F fits (repro_outputs/v8_fit/fitted.json)
  fitD[XO-BT], fitE[XO-BT]                           the Part D and Part E Xonotic fits (v6_fit, v7_fit fitted.json;
                                                     seven parameters, relief rho = 0 = exactly those policies)
  CSO-BT, OW-BT, AC-BT, XO-BT                        the revised trees (default_baselines(); the targets)
  AC-BT[0925], XO-BT[step]                           the earlier trees (BaselineStyle dataclass defaults), for paired
                                                     distance differences on the same episodes
  the four designed styles and their route-off versions (gap-closure denominators, held-out scales)
Stages
  check  reproduction check on already-used seeds (no new seeds): episodes 0-1 of every map and scenario on the Part F
         test seeds (base 8030) for fit[XO-BT], AC-BT[0925] and XO-BT[step], and on the Part E test seeds (base 7030)
         for fitD[XO-BT] and fitE[XO-BT], compared column by column with v8_fit / v7_fit test_rows.csv
  0      targets and scales with the revised trees: 4 trees + 4 designed styles x 4 game maps x 3 scenarios x 50
         episodes (run_fitting_c.stage0; seed base TARGET)
  test   all agents above x (4 game maps + 5 held-out maps) x 3 scenarios x 50 episodes (seed base TEST)
Seeds (never used before; checked against STATE.md, the FITTING_PLAN_* files, the code and repro_outputs): target 10032,
test 10030; smoke 9532, 9530.
Usage: python experiments/run_fitting_g_eval.py --stage all --out ../repro_outputs/v10_eval --jobs 12 [--quick]
       python experiments/run_fitting_g_eval.py --stage check --out <dir> --jobs 4
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting_f as rff  # noqa: E402  (Part E fingerprint; eight-parameter mapping, a 7-component x gets rho = 0)

rf, rfc = rff.rf, rff.rfc
from fps_priority_ai.baselines import BaselineStyle  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
FIT_DIRS = {"D": ROOT / "repro_outputs" / "v6_fit", "E": ROOT / "repro_outputs" / "v7_fit",
            "F": ROOT / "repro_outputs" / "v8_fit"}
SEED_BASES = {"c_target": 10032, "c_test": 10030}
QUICK_SEED_BASES = {"c_target": 9532, "c_test": 9530}
CHECK_BASES = {"chk_v8": 8030, "chk_v7": 7030}           # already used (Part F / Part E test seeds): check only
EARLIER = {"AC-BT[0925]": BaselineStyle("AC-BT[0925]", "AC-BT"), "XO-BT[step]": BaselineStyle("XO-BT[step]", "XO-BT")}
HASHED = ["code/fps_priority_ai/baselines.py", "code/fps_priority_ai/policy.py", "code/fps_priority_ai/config.py"]


def make_policy_g(spec: tuple):
    if spec[0] == "fitx":                     # ("fitx", label, mode, *x)
        return rfc.fitted_style_c(spec[1], spec[2], spec[3:])
    if spec[0] == "earlier":                  # ("earlier", label)
        return EARLIER[spec[1]]
    return rfc.make_policy_c(spec)


def label_g(spec: tuple) -> str:
    return spec[1] if spec[0] in ("fitx", "earlier") else rfc.label_c(spec)


def run_block_g(task: tuple) -> list[dict]:
    spec, map_name, scenario, kind, first, n = task
    styles = rf.default_styles("exp")
    sc = next(s for s in rf.default_scenarios() if s.name == scenario)
    policy = make_policy_g(spec)
    return [{"agent": label_g(spec), "map": map_name, "scenario": scenario, "seed_kind": kind, "episode": ep,
             **rf.run_episode(sc, policy, styles, rf.fit_seed(kind, map_name, scenario, ep), rf.MAPS[map_name])}
            for ep in range(first, first + n)]


def fit_specs() -> tuple[list[tuple], dict]:
    """The six evaluated fits as agent specs, and a record of their sources."""
    fits = {k: json.loads((d / "fitted.json").read_text()) for k, d in FIT_DIRS.items()}
    chosen = [("fit[CSO-BT]", "F", "CSO-BT"), ("fit[OW-BT]", "F", "OW-BT"), ("fit[AC-BT]", "F", "AC-BT"),
              ("fit[XO-BT]", "F", "XO-BT"), ("fitD[XO-BT]", "D", "XO-BT"), ("fitE[XO-BT]", "E", "XO-BT")]
    specs, rec = [], {}
    for label, part, game in chosen:
        f = fits[part][game]
        specs.append(("fitx", label, int(f["combat_mode"]), *[float(v) for v in f["x"]]))
        rec[label] = {"part": part, "game": game, "source": str(FIT_DIRS[part] / "fitted.json"),
                      "combat_mode": f["combat_mode"], "x": f["x"], "params": rff.params_f(f["x"])}
    return specs, rec


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stage_check(out: Path, jobs: int, episodes: int = 2) -> bool:
    """Reproduction check: the current code must reproduce stored test rows of Parts E and F on their own seeds."""
    rf.SEED_BASES.update(CHECK_BASES)
    specs, _ = fit_specs()
    by = {s[1]: s for s in specs}
    plan = [  # (spec, seed kind, stored file, stored label)
        (by["fit[XO-BT]"], "chk_v8", FIT_DIRS["F"] / "test_rows.csv", "fit[XO-BT]"),
        (("earlier", "AC-BT[0925]"), "chk_v8", FIT_DIRS["F"] / "test_rows.csv", "AC-BT"),
        (("earlier", "XO-BT[step]"), "chk_v8", FIT_DIRS["F"] / "test_rows.csv", "XO-BT"),
        (by["fitD[XO-BT]"], "chk_v7", FIT_DIRS["E"] / "test_rows.csv", "fitD[XO-BT]"),
        (by["fitE[XO-BT]"], "chk_v7", FIT_DIRS["E"] / "test_rows.csv", "fit[XO-BT]"),
    ]
    maps = rf.TRAIN_MAPS + rf.HELDOUT_MAPS
    tasks = [(sp, mp, sc, kind, 0, episodes) for sp, kind, _, _ in plan for mp in maps for sc in rf.SCENARIOS]
    with Pool(jobs) as pool:
        rows = [r for b in pool.imap_unordered(run_block_g, tasks, chunksize=1) for r in b]
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
        for (m, sc, ep), o in old.items():
            nr = new[(label_g(sp), m, sc, ep)]
            cols = [c for c in o if c in nr and c not in ("agent", "seed_kind")]
            n += 1
            bad = [c for c in cols if o[c] != nr[c]]
            same += not bad
            for c in bad:
                diffs[c] = diffs.get(c, 0) + 1
        ok = n > 0 and same == n
        ok_all &= ok
        lines.append(f"{label_g(sp)} vs {path.parent.name} '{stored}' (seed base {CHECK_BASES[kind]}): {same}/{n} "
                     f"episodes identical in every shared column" + ("" if ok else f"; differing columns {diffs}"))
    lines.append("REPRODUCTION CHECK " + ("PASSED" if ok_all else "FAILED"))
    (out / "check.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)
    return ok_all


def stage_test(out: Path, jobs: int) -> None:
    specs, _ = fit_specs()
    specs = (specs + [("tree", g) for g in rfc.GAMES] + [("earlier", k) for k in EARLIER]
             + [("style", s) for s in rf.STYLE_NAMES] + [("style_off", s) for s in rf.STYLE_NAMES])
    tasks = [(sp, mp, sc, "c_test", 0, rfc.EPISODES["test"]) for sp in specs for mp in rf.TRAIN_MAPS + rf.HELDOUT_MAPS
             for sc in rf.SCENARIOS]
    with Pool(jobs) as pool:
        rows = [r for b in pool.imap_unordered(run_block_g, tasks, chunksize=1) for r in b]
    rf.write_rows(out / "test_rows.csv", rows)
    print(f"test: {len(rows)} episodes", flush=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--stage", required=True, choices=["check", "0", "test", "all"])
    p.add_argument("--out", default="../repro_outputs/v10_eval")
    p.add_argument("--jobs", type=int, default=12)
    p.add_argument("--quick", action="store_true", help="smoke test: smoke seeds, 2 episodes per cell (not a result)")
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    bases = QUICK_SEED_BASES if a.quick else SEED_BASES
    rf.SEED_BASES.update(bases)
    if a.quick:
        rfc.EPISODES["target"] = rfc.EPISODES["test"] = 2
    _, rec = fit_specs()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    (out / f"run_stage{a.stage}.json").write_text(json.dumps({
        "stage": a.stage, "quick": a.quick, "seed_bases": bases, "check_bases": CHECK_BASES, "fingerprint": rf.FP,
        "episodes": {"target": rfc.EPISODES["target"], "test": rfc.EPISODES["test"]}, "fits": rec,
        "earlier_trees": {k: repr(v) for k, v in EARLIER.items()}, "sha256": {f: sha256(ROOT / f) for f in HASHED},
        "git_head": head, "testbed": rf.testbed_flags(), "start": time.strftime("%Y-%m-%d %H:%M:%S")}, indent=1))
    stages = ["check", "0", "test"] if a.stage == "all" else [a.stage]
    for s in stages:
        t = time.time()
        if s == "check":
            if not stage_check(out, a.jobs) and a.stage == "all":
                sys.exit("reproduction check failed: not running the evaluation")
            rf.SEED_BASES.update(bases)
        elif s == "0":
            rfc.stage0(out, a.jobs)
        else:
            stage_test(out, a.jobs)
        print(f"stage {s} done in {time.time() - t:.0f} s", flush=True)


if __name__ == "__main__":
    main()
