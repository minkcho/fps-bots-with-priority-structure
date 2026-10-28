"""Fitting the unified policy to the four reconstructed game logics (2026-09-25; protocol: CONFIRMATION_PLAN,
part B; nothing here is run before that protocol is frozen).

For each behaviour tree (CSO-BT, OW-BT, AC-BT, XO-BT; fps_priority_ai/baselines.py) the priority policy is fitted with
that game's combat mode fixed (CSO hold, Overwatch keep moving, AssaultCube chase, Xonotic evade: the modes of the
style designed for the game) and distance-only routing (lambda_E = lambda_C = lambda_T = 0, the trees' unit-cost
A*). The goal argmax, argmax_g w_g u_g - w_commitment [g != incumbent], does not change when all five weights are
scaled together, so four parameters are identifiable: the goal weights on the simplex (stick-breaking of
u in [0, 1]^3) and kappa = w_commitment / sum of the goal weights in [0, 0.5].

Behavioural fingerprint: objective commitment, engagement redirection, resource seeking and ally distance per
scenario and map (Deathmatch objective commitment, always 0, is left out; so is any dimension on which the eight
reference agents do not vary at all, e.g. resource seeking on the map without pickups).

Objective (to minimise): J = mean over the dimensions d of [(xbar_d - mu_d)^2 - v_d / n_d] / s_d^2, where xbar_d,
v_d, n_d are the candidate's episode mean, variance and count, mu_d the tree's mean from stage 0 and s_d the pooled
within-condition episode SD of the eight reference agents (four trees, four hand-designed styles) from stage 0,
floored at 5% of the range of their means. Kills, deaths, wins and hits taken never enter the objective.

Stages (maps: the four game-inspired maps; scenarios: Mission, Deathmatch, Control; opponent: Aggressive):
  0  targets and scales: 4 trees + 4 styles x 4 maps x 3 scenarios x 50 episodes (seed base TARGET)
  1  screen: 128 scrambled Sobol points x 24 episodes (2 per map x scenario; seed base TRAIN)
  2  differential evolution from the best 32 stage-1 points: 3 generations, deferred updating, no polishing,
     48 episodes per evaluation (4 per map x scenario; seed base TRAIN)
  3  validation: the best 8 distinct stage-2 candidates x 144 episodes (12 per map x scenario; seed base
     VALIDATION); the candidate with the lowest validation J is the fitted policy
  test  fitted policies, trees, styles and styles with the route terms off x (4 game maps + 5 held-out maps) x
     3 scenarios x 50 episodes (seed base TEST); analysed by analyze_fitting.py
Episode seeds depend on the seed base, the map, the scenario and the episode index (common random numbers across
agents within a map; independent across maps).

Usage:
  python experiments/run_fitting.py --stage 0 --out ../repro_outputs/v4_fit --jobs 16
  python experiments/run_fitting.py --stage 1|2|3|test --out ../repro_outputs/v4_fit --jobs 16 [--games CSO-BT,...]
  python experiments/run_fitting.py --stage all --out ../repro_outputs/v4_fit --jobs 16
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
import sys
import time
from dataclasses import replace
from multiprocessing import Pool
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fps_priority_ai.baselines import default_baselines  # noqa: E402
from fps_priority_ai.experiment import MAPS, run_episode, testbed_flags  # noqa: E402
from fps_priority_ai.runner import default_scenarios, default_styles  # noqa: E402

GAMES = {"CSO-BT": 0, "OW-BT": 1, "AC-BT": 2, "XO-BT": 3}          # combat mode fixed per game
HAND = {"CSO-BT": "Mission–Cooperation", "OW-BT": "Persistent Objective", "AC-BT": "Aggressive",
        "XO-BT": "Survival-Aware"}                                    # hand-designed style of each game
STYLE_NAMES = list(HAND.values())
TRAIN_MAPS = ["cso", "ow", "ac", "xo"]
HELDOUT_MAPS = ["random", "urban", "random_s101", "urban_s101", "blocks"]
SCENARIOS = ["Mission", "Deathmatch", "Control"]
FP = ["objective_commitment_ratio", "engagement_redirection_rate_per_100", "resource_seeking_rate_per_100",
      "avg_ally_proximity"]
OUTCOMES = ["kills", "deaths", "control_score", "hits_taken_per_step", "walked_hits_per_step", "los_frac"]
# (the smoke test of 2026-09-24 ran a few episodes on the bases 2029-2032, so the confirmatory run uses fresh bases;
# --quick uses its own bases so that smoke tests never touch these)
SEED_BASES = {"target": 3032, "train": 3029, "validation": 3031, "test": 3030}
QUICK_SEED_BASES = {"target": 9032, "train": 9029, "validation": 9031, "test": 9030}
KAPPA_MAX = 0.5
N_SOBOL, N_ELITE, DE_GENERATIONS, N_FINALISTS = 128, 32, 3, 8
EPISODES = {"target": 50, "screen": 2, "search": 4, "validation": 12, "test": 50}


# ----------------------------------------------------------------------------------------------- agents
def simplex(u1: float, u2: float, u3: float) -> list[float]:
    """Stick-breaking map from [0, 1]^3 to the four goal weights (sum 1)."""
    return [u1, (1 - u1) * u2, (1 - u1) * (1 - u2) * u3, (1 - u1) * (1 - u2) * (1 - u3)]


def fitted_style(game: str, x) -> object:
    u1, u2, u3, kappa = (float(v) for v in x)
    w = simplex(u1, u2, u3)
    base = default_styles("exp")["Aggressive"]
    return replace(base, name=f"fit[{game}]", w_objective=w[0], w_engage=w[1], w_resource=w[2], w_team=w[3],
                   w_commitment=kappa, w_exposure=0.0, w_cover=0.0, w_teammate_sep=0.0,
                   combat_mode_override=GAMES[game])


def make_policy(spec: tuple):
    kind = spec[0]
    if kind == "tree":
        return default_baselines()[spec[1]]
    styles = default_styles("exp")
    if kind == "style":
        return styles[spec[1]]
    if kind == "style_off":                       # hand style with the route terms switched off
        s = styles[spec[1]]
        return replace(s, name=f"{s.name} [route off]", w_exposure=0.0, w_cover=0.0, w_teammate_sep=0.0)
    if kind == "fit":
        return fitted_style(spec[1], spec[2:])
    raise ValueError(spec)


def agent_label(spec: tuple) -> str:
    return {"tree": lambda s: s[1], "style": lambda s: s[1], "style_off": lambda s: f"{s[1]} [route off]",
            "fit": lambda s: f"fit[{s[1]}]"}[spec[0]](spec)


def fit_seed(kind: str, map_name: str, scenario: str, ep: int) -> int:
    return random.Random(f"fit|{SEED_BASES[kind]}|{map_name}|{scenario}|{ep}").randrange(10 ** 9)


# ----------------------------------------------------------------------------------------------- episodes
def run_block(task: tuple) -> list[dict]:
    """task = (spec, map, scenario, seed kind, first episode, number of episodes) -> metric rows."""
    spec, map_name, scenario, kind, first, n = task
    styles = default_styles("exp")
    sc = next(s for s in default_scenarios() if s.name == scenario)
    policy = make_policy(spec)
    rows = []
    for ep in range(first, first + n):
        row = run_episode(sc, policy, styles, fit_seed(kind, map_name, scenario, ep), MAPS[map_name])
        rows.append({"agent": agent_label(spec), "map": map_name, "scenario": scenario, "seed_kind": kind,
                     "episode": ep, **row})
    return rows


def to_float(v) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return float("nan")


def summarise(rows: list[dict]) -> dict:
    """Per (map, scenario, metric): mean, variance (ddof 1) and count over episodes."""
    acc: dict = {}
    for r in rows:
        for m in FP + OUTCOMES:
            v = to_float(r.get(m))
            if not math.isnan(v):
                acc.setdefault((r["map"], r["scenario"], m), []).append(v)
    return {k: (float(np.mean(v)), float(np.var(v, ddof=1)) if len(v) > 1 else 0.0, len(v)) for k, v in acc.items()}


def objective_value(summary: dict, target: dict, scales: dict) -> float:
    terms = []
    for key, s in scales.items():
        k = tuple(key.split("|"))
        if k not in summary or key not in target:
            terms.append(float("inf"))
            continue
        xbar, v, n = summary[k]
        terms.append(((xbar - target[key]) ** 2 - v / n) / s ** 2)
    return float(np.mean(terms))


# ----------------------------------------------------------------------------------------------- helpers
def write_rows(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cols = list(rows[0].keys())
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def dims(map_names) -> list[tuple]:
    return [(mp, sc, m) for mp in map_names for sc in SCENARIOS for m in FP
            if not (sc == "Deathmatch" and m == "objective_commitment_ratio")]


def evaluate(game: str, x, kind: str, n_per_cell: int, first: int = 0) -> tuple[float, dict]:
    """J of the fitted policy with parameters x on n_per_cell episodes per map x scenario (serial)."""
    spec = ("fit", game, *[float(v) for v in x])
    rows = []
    for mp in TRAIN_MAPS:
        for sc in SCENARIOS:
            rows += run_block((spec, mp, sc, kind, first, n_per_cell))
    summ = summarise(rows)
    return objective_value(summ, TARGETS[game], SCALES), summ


TARGETS: dict = {}
SCALES: dict = {}


def _init_worker(targets: dict, scales: dict) -> None:
    TARGETS.update(targets)
    SCALES.update(scales)


def _eval_screen(args):
    game, x = args
    j, _ = evaluate(game, x, "train", EPISODES["screen"])
    return j


def _eval_search(x, game):
    j, _ = evaluate(game, x, "train", EPISODES["search"])
    with open(SEARCH_LOG, "a") as fh:
        fh.write(json.dumps({"game": game, "x": [float(v) for v in x], "J": j}) + "\n")
    return j


SEARCH_LOG = ""


def _eval_validation(args):
    game, x = args
    j, summ = evaluate(game, x, "validation", EPISODES["validation"])
    return j


# ----------------------------------------------------------------------------------------------- stages
def stage0(out: Path, jobs: int) -> None:
    specs = [("tree", g) for g in GAMES] + [("style", s) for s in STYLE_NAMES]
    tasks = [(sp, mp, sc, "target", 0, EPISODES["target"]) for sp in specs for mp in TRAIN_MAPS for sc in SCENARIOS]
    with Pool(jobs) as pool:
        rows = [r for block in pool.imap_unordered(run_block, tasks) for r in block]
    write_rows(out / "stage0_rows.csv", rows)
    by_agent = {}
    for r in rows:
        by_agent.setdefault(r["agent"], []).append(r)
    summ = {a: summarise(rs) for a, rs in by_agent.items()}
    targets = {g: {"|".join(k): summ[g][k][0] for k in summ[g] if k[2] in FP} for g in GAMES}
    scales, dropped = {}, []
    for d in dims(TRAIN_MAPS):
        means = [summ[a][d][0] for a in summ if d in summ[a]]
        pooled_sd = math.sqrt(np.mean([summ[a][d][1] for a in summ if d in summ[a]]))
        rng = max(means) - min(means)
        s = max(pooled_sd, 0.05 * rng)
        if s <= 0:
            dropped.append("|".join(d))
            continue
        scales["|".join(d)] = s
    (out / "stage0.json").write_text(json.dumps({"targets": targets, "scales": scales, "dropped": dropped,
                                                 "testbed": testbed_flags()}, indent=1))
    print(f"stage 0: {len(rows)} episodes, {len(scales)} dimensions ({len(dropped)} without variation: {dropped})")


def load_stage0(out: Path) -> tuple[dict, dict]:
    s0 = json.loads((out / "stage0.json").read_text())
    return s0["targets"], s0["scales"]


def stage1(out: Path, jobs: int, games) -> None:
    from scipy.stats import qmc
    targets, scales = load_stage0(out)
    res = {}
    with Pool(jobs, initializer=_init_worker, initargs=(targets, scales)) as pool:
        for game in games:
            pts = qmc.Sobol(d=4, scramble=True, seed=SEED_BASES["train"]).random_base2(m=int(math.log2(N_SOBOL)))
            pts[:, 3] *= KAPPA_MAX
            js = pool.map(_eval_screen, [(game, p) for p in pts])
            res[game] = [{"x": p.tolist(), "J": j} for p, j in zip(pts, js)]
            best = min(js)
            print(f"stage 1 {game}: {len(pts)} points, best J {best:.3f}", flush=True)
    (out / "stage1.json").write_text(json.dumps(res, indent=1))


def stage2(out: Path, jobs: int, games) -> None:
    global SEARCH_LOG
    from scipy.optimize import differential_evolution
    targets, scales = load_stage0(out)
    s1 = json.loads((out / "stage1.json").read_text())
    SEARCH_LOG = str(out / "stage2_evaluations.jsonl")
    bounds = [(0.0, 1.0)] * 3 + [(0.0, KAPPA_MAX)]
    with Pool(jobs, initializer=_init_worker, initargs=(targets, scales)) as pool:
        for game in games:
            elite = sorted(s1[game], key=lambda e: e["J"])[:N_ELITE]
            init = np.array([e["x"] for e in elite])
            r = differential_evolution(_eval_search, bounds, args=(game,), init=init, maxiter=DE_GENERATIONS,
                                       updating="deferred", workers=pool.map, polish=False, seed=SEED_BASES["train"],
                                       tol=0.0)
            print(f"stage 2 {game}: best J {r.fun:.3f} at {np.round(r.x, 3).tolist()} ({r.nfev} evaluations)", flush=True)


def stage3(out: Path, jobs: int, games) -> None:
    targets, scales = load_stage0(out)
    evals = [json.loads(l) for l in (out / "stage2_evaluations.jsonl").read_text().splitlines() if l.strip()]
    fitted = json.loads((out / "fitted.json").read_text()) if (out / "fitted.json").exists() else {}
    with Pool(jobs, initializer=_init_worker, initargs=(targets, scales)) as pool:
        for game in games:
            cands, seen = [], set()
            for e in sorted((e for e in evals if e["game"] == game), key=lambda e: e["J"]):
                key = tuple(round(v, 6) for v in e["x"])
                if key not in seen:
                    seen.add(key)
                    cands.append(e)
                if len(cands) == N_FINALISTS:
                    break
            js = pool.map(_eval_validation, [(game, c["x"]) for c in cands])
            best = int(np.argmin(js))
            x = cands[best]["x"]
            w = simplex(*x[:3])
            fitted[game] = {"x": x, "weights": {"w_objective": w[0], "w_engage": w[1], "w_resource": w[2],
                                                "w_team": w[3], "w_commitment": x[3]},
                            "combat_mode": GAMES[game], "train_J": cands[best]["J"], "validation_J": js[best],
                            "finalists": [{"x": c["x"], "train_J": c["J"], "validation_J": j} for c, j in zip(cands, js)]}
            print(f"stage 3 {game}: validation J {js[best]:.3f} (train {cands[best]['J']:.3f}), weights "
                  f"{np.round(w, 3).tolist()}, kappa {x[3]:.3f}", flush=True)
    (out / "fitted.json").write_text(json.dumps(fitted, indent=1))


def stage_test(out: Path, jobs: int) -> None:
    fitted = json.loads((out / "fitted.json").read_text())
    specs = ([("fit", g, *fitted[g]["x"]) for g in GAMES if g in fitted] + [("tree", g) for g in GAMES]
             + [("style", s) for s in STYLE_NAMES] + [("style_off", s) for s in STYLE_NAMES])
    tasks = [(sp, mp, sc, "test", 0, EPISODES["test"]) for sp in specs for mp in TRAIN_MAPS + HELDOUT_MAPS
             for sc in SCENARIOS]
    with Pool(jobs) as pool:
        rows = [r for block in pool.imap_unordered(run_block, tasks, chunksize=1) for r in block]
    write_rows(out / "test_rows.csv", rows)
    print(f"test: {len(rows)} episodes")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--stage", required=True, choices=["0", "1", "2", "3", "test", "all"])
    p.add_argument("--out", default="../repro_outputs/v4_fit")
    p.add_argument("--jobs", type=int, default=16)
    p.add_argument("--games", default=",".join(GAMES))
    p.add_argument("--quick", action="store_true", help="smoke test with tiny budgets (not for results)")
    a = p.parse_args()
    if a.quick:
        global N_SOBOL, N_ELITE, DE_GENERATIONS, N_FINALISTS
        N_SOBOL, N_ELITE, DE_GENERATIONS, N_FINALISTS = 8, 5, 1, 2
        EPISODES.update({"target": 2, "screen": 1, "search": 1, "validation": 1, "test": 1})
        SEED_BASES.update(QUICK_SEED_BASES)
        HELDOUT_MAPS[:] = HELDOUT_MAPS[:1]
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    games = a.games.split(",")
    (out / f"run_stage{a.stage}.json").write_text(json.dumps({"stage": a.stage, "games": games,
                                                              "testbed": testbed_flags(), "started": time.ctime()}))
    stages = ["0", "1", "2", "3", "test"] if a.stage == "all" else [a.stage]
    for s in stages:
        t0 = time.time()
        if s == "0":
            stage0(out, a.jobs)
        elif s == "1":
            stage1(out, a.jobs, games)
        elif s == "2":
            stage2(out, a.jobs, games)
        elif s == "3":
            stage3(out, a.jobs, games)
        else:
            stage_test(out, a.jobs)
        print(f"stage {s} done in {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
