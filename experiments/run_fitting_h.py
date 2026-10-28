"""Round H (v15) of the fitting experiment (DRAFT protocol FITTING_PLAN_H_DRAFT.md, 2026-09-30; not frozen, not run):
hand-set settings of the unified policy, read from Table 1, observation O4 and the rules of Section 3 of the journal
draft (paper-0929), evaluated against the four behaviour trees with the grading of Part G-fit. Nothing is fitted or
searched. The question: how far does a designer get who sets the policy for a game by reading, and how much farther
does the search of Part G-fit go?

Agents (labels in test_rows.csv)
  hand[CSO-BT], hand[OW-BT], hand[AC-BT], hand[XO-BT]   the hand-set settings (HANDSET below; recorded in handset.json)
  fit[CSO-BT], fit[OW-BT], fit[AC-BT], fit[XO-BT]       the Part G-fit fits (repro_outputs/v11_fit/fitted.json), same
                                                        episodes, for paired comparison
  CSO-BT, OW-BT, AC-BT, XO-BT                           the trees (default_baselines(); the targets)
  the four designed styles and their route-off versions (gap-closure denominators, held-out scales)
Stages
  check  reproduction check on already-used seeds (no new seeds): episodes 0-1 of every map and scenario on the G-fit
         test seeds (base 11030) for the four trees and the four G-fit fits, compared column by column with
         repro_outputs/v11_fit/test_rows.csv (the file exists on the compute server)
  0      targets and scales: 4 trees + 4 designed styles x 4 game maps x 3 scenarios x 50 episodes (run_fitting_c.stage0;
         seed base TARGET)
  test   all agents above x (4 game maps + 5 held-out maps) x 3 scenarios x 50 episodes (seed base TEST)
Seeds (never used before; checked against FITTING_PLAN_G_FIT_2026-09-28.md section 3.6, FAMILY_ADAPT_PLAN_V13_2026-09-29.md
and the code): target 15032, test 15030; smoke 15532, 15530.
Usage: python experiments/run_fitting_h.py --stage all --out ../repro_outputs/v15_handset --jobs 12 [--quick]
       python experiments/run_fitting_h.py --stage check --out <dir> --jobs 4
       python experiments/run_fitting_h.py --stage settings --out <dir>      (write handset.json only, no episodes)
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import subprocess
import sys
import time
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting_f as rff  # noqa: E402  (Part E fingerprint; eight-parameter mapping of Part F / G-fit)

rf, rfc = rff.rf, rff.rfc

ROOT = Path(__file__).resolve().parents[2]
V11 = ROOT / "repro_outputs" / "v11_fit"
SEED_BASES = {"c_target": 15032, "c_test": 15030}
QUICK_SEED_BASES = {"c_target": 15532, "c_test": 15530}
CHECK_BASES = {"chk_v11": 11030}                          # already used (G-fit test seeds): check only
HASHED = ["code/fps_priority_ai/baselines.py", "code/fps_priority_ai/policy.py", "code/fps_priority_ai/config.py"]

# --- The hand-set settings: rules fixed in the protocol, one setting per game --------------------------------------
# Goal weights: the dominant priorities of Table 1 (objective, engagement, resources, cooperation) on a fixed ladder,
# then normalised to the simplex. "Conditional" resource seeking gets the medium weight; the condition itself is
# expressed by the status gate (g0) and the relief (rho) below, not by the weight.
LADDER = {"very high": 1.0, "high": 0.8, "medium-high": 0.6, "medium": 0.4, "low-medium": 0.3, "low": 0.15,
          "conditional": 0.4}
TABLE1 = {"CSO-BT": ("high", "medium", "conditional", "high"),
          "OW-BT": ("very high", "medium", "conditional", "medium-high"),
          "AC-BT": ("low", "high", "low-medium", "low"),
          "XO-BT": ("low", "medium-high", "high", "low")}
# Commitment kappa = w_commitment / sum of the goal weights (search range [0, 0.5]), from the interruption rules (O2):
# high = contact does not override the movement goal and the bot returns to its task (CSO leader-follower cohesion,
# Overwatch), low = a fixed order that redirects on every contact (AssaultCube), medium = a goal kept for a timer
# interval (Xonotic).
KAPPA = {"high": 0.3, "medium": 0.2, "low": 0.1}
# Mode (O4): 0 hold (CSO), 1 keep moving (Overwatch, Xonotic), 2 chase (AssaultCube).
# Optional elements, from the "Low health/ammo" and "Enemy visible" rows of Table 1 and the pseudocode of Fig. 1:
#   g0 (resource_idle_factor, range [0, 0.5]): 0 = items only in low status (Overwatch: "seek health if low");
#       0.5 = items also in good status (AssaultCube: "else missing items"; Xonotic: "also in good status");
#       0.25 = the main model's default where the rule is unspecified (CSO: "opportunistic pickup").
#   tau (resource_distance_scale, range [1, 100]): 100 = distance-free item choice in low status (Overwatch, whose
#       health rule does not depend on distance); 12 = the Xonotic bot's route discount 12 / (12 + d) at the grid scale
#       (Appendix B, tab:tree_conversion); 1 = the main model's default (CSO, AssaultCube).
#   eta (hunt_unseen, range [0, 1]): 1 = an unseen opponent is rated like a visible one (AssaultCube hunts enemies out
#       of view; Xonotic rates all enemies); 0 = the main model (CSO, Overwatch: only visible or remembered enemies).
#   rho (urgent_switch_relief, range [0, 1]): 1 = an explicit low-status item rule overrides the current activity
#       (Overwatch: health low; AssaultCube: ammunition critical in combat; Xonotic: turns to items when weak);
#       0 = no such rule (CSO: "opportunistic pickup").
# Native scenarios (user's decision of 2026-09-30): the scenarios in which a game's logic, its hand-set setting and its
# fit are run and graded; CSO and Overwatch are objective games, AssaultCube and Xonotic deathmatch games.
NATIVE = {"CSO-BT": ["Mission", "Control"], "OW-BT": ["Mission", "Control"], "AC-BT": ["Deathmatch"],
          "XO-BT": ["Deathmatch"]}
RULES = {"CSO-BT": {"commitment": "high", "mode": 0, "resource_idle_factor": 0.25, "resource_distance_scale": 1.0,
                    "hunt_unseen": 0.0, "urgent_switch_relief": 0.0},
         "OW-BT": {"commitment": "high", "mode": 1, "resource_idle_factor": 0.0, "resource_distance_scale": 100.0,
                   "hunt_unseen": 0.0, "urgent_switch_relief": 1.0},
         "AC-BT": {"commitment": "low", "mode": 2, "resource_idle_factor": 0.5, "resource_distance_scale": 1.0,
                   "hunt_unseen": 1.0, "urgent_switch_relief": 1.0},
         "XO-BT": {"commitment": "medium", "mode": 1, "resource_idle_factor": 0.5, "resource_distance_scale": 12.0,
                   "hunt_unseen": 1.0, "urgent_switch_relief": 1.0}}


def handset_params(game: str) -> dict:
    """The intended parameter values of one hand-set setting (goal weights on the simplex)."""
    raw = [LADDER[level] for level in TABLE1[game]]
    tot = sum(raw)
    w = [v / tot for v in raw]
    r = RULES[game]
    return {"w_objective": w[0], "w_engage": w[1], "w_resource": w[2], "w_team": w[3],
            "w_commitment": KAPPA[r["commitment"]], "resource_idle_factor": r["resource_idle_factor"],
            "resource_distance_scale": r["resource_distance_scale"], "hunt_unseen": r["hunt_unseen"],
            "urgent_switch_relief": r["urgent_switch_relief"]}


def to_x(pr: dict) -> list[float]:
    """Inverse of run_fitting_c.params / run_fitting_f.params_f: the search coordinates of a parameter setting."""
    u1 = pr["w_objective"]
    u2 = pr["w_engage"] / (1.0 - u1)
    u3 = pr["w_resource"] / ((1.0 - u1) * (1.0 - u2))
    x = [u1, u2, u3, pr["w_commitment"] / rfc.KAPPA_MAX, pr["resource_idle_factor"] / rfc.G0_MAX,
         math.log10(pr["resource_distance_scale"]) / rfc.LOG_TAU_MAX, pr["hunt_unseen"], pr["urgent_switch_relief"]]
    if not all(0.0 <= v <= 1.0 + 1e-12 for v in x):
        raise ValueError(f"hand-set setting outside the searched parameter space: {x}")
    return [min(max(v, 0.0), 1.0) for v in x]


def handset_specs() -> tuple[list[tuple], dict]:
    """The four hand-set settings as agent specs, with a record that includes the round-trip check."""
    specs, rec = [], {}
    for g in rfc.GAMES:
        pr = handset_params(g)
        x = to_x(pr)
        back = rff.params_f(x)
        err = max(abs(back[k] - pr[k]) for k in pr)
        if err > 1e-9:
            raise AssertionError(f"{g}: parameter round trip differs by {err}")
        specs.append(("fitx", f"hand[{g}]", int(RULES[g]["mode"]), *x))
        rec[f"hand[{g}]"] = {"game": g, "table1": TABLE1[g], "rules": RULES[g], "params": pr, "combat_mode": RULES[g]["mode"],
                             "x": x, "round_trip_max_abs_error": err}
    return specs, rec


def fit_specs() -> tuple[list[tuple], dict]:
    """The four Part G-fit fits as agent specs (paired comparison), with a record of their source."""
    fitted = json.loads((V11 / "fitted.json").read_text())
    specs, rec = [], {}
    for g in rfc.GAMES:
        f = fitted[g]
        specs.append(("fitx", f"fit[{g}]", int(f["combat_mode"]), *[float(v) for v in f["x"]]))
        rec[f"fit[{g}]"] = {"game": g, "source": str(V11 / "fitted.json"), "combat_mode": f["combat_mode"], "x": f["x"],
                            "params": rff.params_f(f["x"])}
    return specs, rec


def make_policy_h(spec: tuple):
    if spec[0] == "fitx":                     # ("fitx", label, mode, *x)
        return rfc.fitted_style_c(spec[1], spec[2], spec[3:])
    return rfc.make_policy_c(spec)


def label_h(spec: tuple) -> str:
    return spec[1] if spec[0] == "fitx" else rfc.label_c(spec)


def run_block_h(task: tuple) -> list[dict]:
    spec, map_name, scenario, kind, first, n = task
    styles = rf.default_styles("exp")
    sc = next(s for s in rf.default_scenarios() if s.name == scenario)
    policy = make_policy_h(spec)
    return [{"agent": label_h(spec), "map": map_name, "scenario": scenario, "seed_kind": kind, "episode": ep,
             **rf.run_episode(sc, policy, styles, rf.fit_seed(kind, map_name, scenario, ep), rf.MAPS[map_name])}
            for ep in range(first, first + n)]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stage_check(out: Path, jobs: int, episodes: int = 2) -> bool:
    """Reproduction check: the current code must reproduce stored G-fit test rows of the trees and fits on their seeds."""
    rf.SEED_BASES.update(CHECK_BASES)
    fits, _ = fit_specs()
    plan = [(("tree", g), "chk_v11", V11 / "test_rows.csv", g) for g in rfc.GAMES]
    plan += [(sp, "chk_v11", V11 / "test_rows.csv", sp[1]) for sp in fits]
    maps = rf.TRAIN_MAPS + rf.HELDOUT_MAPS
    tasks = [(sp, mp, sc, kind, 0, episodes) for sp, kind, _, _ in plan for mp in maps for sc in rf.SCENARIOS]
    with Pool(jobs) as pool:
        rows = [r for b in pool.imap_unordered(run_block_h, tasks, chunksize=1) for r in b]
    rf.write_rows(out / "check_rows.csv", rows)
    new = {}
    with (out / "check_rows.csv").open() as fh:
        for r in csv.DictReader(fh):
            new[(r["agent"], r["map"], r["scenario"], r["episode"])] = r
    stored_rows: dict = {}
    with (V11 / "test_rows.csv").open() as fh:
        for r in csv.DictReader(fh):
            if int(r["episode"]) < episodes:
                stored_rows.setdefault(r["agent"], {})[(r["map"], r["scenario"], r["episode"])] = r
    lines, ok_all = [], True
    for sp, kind, path, stored in plan:
        old = stored_rows.get(stored, {})
        n = same = 0
        diffs: dict = {}
        for (m, sc, ep), o in old.items():
            nr = new[(label_h(sp), m, sc, ep)]
            cols = [c for c in o if c in nr and c not in ("agent", "seed_kind")]
            n += 1
            bad = [c for c in cols if o[c] != nr[c]]
            same += not bad
            for c in bad:
                diffs[c] = diffs.get(c, 0) + 1
        ok = n > 0 and same == n
        ok_all &= ok
        lines.append(f"{label_h(sp)} vs {path.parent.name} '{stored}' (seed base {CHECK_BASES[kind]}): {same}/{n} "
                     f"episodes identical in every shared column" + ("" if ok else f"; differing columns {diffs}"))
    lines.append("REPRODUCTION CHECK " + ("PASSED" if ok_all else "FAILED"))
    (out / "check.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines), flush=True)
    return ok_all


def stage_test(out: Path, jobs: int) -> None:
    """Native scenarios only (user's decision of 2026-09-30): a hand-set setting, its fit and its tree run in the
    scenarios that the game's logic targets; the designed styles (gap-closure denominators, held-out scales) run in
    every scenario."""
    hands, _ = handset_specs()
    fits, _ = fit_specs()
    maps = rf.TRAIN_MAPS + rf.HELDOUT_MAPS
    n = rfc.EPISODES["test"]
    tasks = []
    for sp in hands + fits:                                   # ("fitx", "hand[<tree>]" / "fit[<tree>]", mode, *x)
        g = sp[1][sp[1].index("[") + 1:-1]
        tasks += [(sp, mp, sc, "c_test", 0, n) for mp in maps for sc in NATIVE[g]]
    for g in rfc.GAMES:
        tasks += [(("tree", g), mp, sc, "c_test", 0, n) for mp in maps for sc in NATIVE[g]]
    for s in rf.STYLE_NAMES:
        tasks += [(sp, mp, sc, "c_test", 0, n) for sp in (("style", s), ("style_off", s)) for mp in maps
                  for sc in rf.SCENARIOS]
    with Pool(jobs) as pool:
        rows = [r for b in pool.imap_unordered(run_block_h, tasks, chunksize=1) for r in b]
    rf.write_rows(out / "test_rows.csv", rows)
    print(f"test: {len(rows)} episodes", flush=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--stage", required=True, choices=["settings", "check", "0", "test", "all"])
    p.add_argument("--out", default="../repro_outputs/v15_handset")
    p.add_argument("--jobs", type=int, default=12)
    p.add_argument("--quick", action="store_true", help="smoke test: smoke seeds, 2 episodes per cell (not a result)")
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    bases = QUICK_SEED_BASES if a.quick else SEED_BASES
    rf.SEED_BASES.update(bases)
    if a.quick:
        rfc.EPISODES["target"] = rfc.EPISODES["test"] = 2
    _, hand_rec = handset_specs()
    _, fit_rec = fit_specs()
    (out / "handset.json").write_text(json.dumps({"ladder": LADDER, "table1": TABLE1, "kappa": KAPPA, "rules": RULES,
                                                  "settings": hand_rec}, indent=1))
    if a.stage == "settings":
        print(json.dumps(hand_rec, indent=1))
        return
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    (out / f"run_stage{a.stage}.json").write_text(json.dumps({
        "stage": a.stage, "quick": a.quick, "seed_bases": bases, "check_bases": CHECK_BASES, "fingerprint": rf.FP,
        "episodes": {"target": rfc.EPISODES["target"], "test": rfc.EPISODES["test"]}, "handset": hand_rec, "fits": fit_rec,
        "sha256": {f: sha256(ROOT / f) for f in HASHED}, "git_head": head, "testbed": rf.testbed_flags(),
        "start": time.strftime("%Y-%m-%d %H:%M:%S")}, indent=1))
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
