"""Round v13, Part FV: form variants of the unified policy (2026-09-29).

Two alternatives inside the same function family, both optional PriorityWeights fields whose defaults reproduce the
main model (config.py):
  distance transform  U(d) = 1 / (1 + d / tau) ("inverse") or exp(-d / tau) ("exp") for the Objective, Enemy and
                      Resource utilities, compared at a matched half-distance h (U(h) = 1/2): inverse tau = h, exp
                      tau = h / ln 2; the main model is inverse with h = 1
  minimum dwell time  a newly chosen goal type is kept for N steps (min_dwell_steps) in place of the switching penalty
                      (w_commitment = 0)
Parts:
  a      the four designed styles x {main, inverse h = 4, 8, 16, exp h = 4, 8, 16}
  b      Mission-Cooperation (the base style of H2): the penalty grid of H2 (w_commitment 0 ... 1.25) and dwell times
         N = 2 ... 40 with w_commitment = 0 (N = 0 is the penalty-0 condition)
  c      the four designed styles with the penalty replaced by a matched dwell time (--matched, fixed in the protocol),
         next to the main model
  calib  the four designed styles with dwell times over a wide grid (w_commitment = 0) next to the main model, to choose
         the matched N on development seeds
Every episode: a 25x25 map (random, urban), three scenarios, the Aggressive opponent, the testbed rules set by the
launcher; seed episode_seed(base, "<map>|<scenario>", episode), common to all conditions (common random numbers).
Each row is the standard metric row of experiment.run_episode_env plus measures of team 0 from the step logs:
  share_<goal>                  share of the alive agent-steps on each goal type
  far_objective_share           share of the alive agent-steps more than 12 cells (Manhattan) from the objective that are
                                on the Objective goal (Mission and Control; empty in Deathmatch); far_objective_steps
                                is its denominator
  idle_item_chain_rate_per_100  item chains per 100 alive agent-steps: an agent reaches the item it is heading for and,
                                in good status, heads for another item on the next step without leaving the Resource goal
Output: <out>/rows_<part>.csv and <out>/run_<part>.json (conditions, seeds, hashes, versions, testbed rules, times).
Usage: python experiments/run_form_variants.py --part a --seed-base 5801 --episodes 30 --jobs 12 \
           --out ../repro_outputs/dev_v13/fv
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import subprocess
import sys
import time
from dataclasses import replace
from multiprocessing import Pool
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fps_priority_ai import experiment  # noqa: E402
from fps_priority_ai.config import PriorityWeights  # noqa: E402
from fps_priority_ai.env import FPSEnv  # noqa: E402
from fps_priority_ai.experiment import MAPS, METRIC_COLUMNS, episode_seed, run_episode_env, testbed_flags  # noqa: E402
from fps_priority_ai.runner import default_scenarios, default_styles  # noqa: E402
from fps_priority_ai.world import manhattan  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SHORT = {"Mission–Cooperation": "MC", "Persistent Objective": "PO", "Aggressive": "Agg", "Survival-Aware": "SA"}
MAP_NAMES = ["random", "urban"]
SCENARIOS = {sc.name: sc for sc in default_scenarios()}
TRANSFORMS = ([("main", "inverse", 1.0)] + [(f"inv_h{h}", "inverse", float(h)) for h in (4, 8, 16)]
              + [(f"exp_h{h}", "exp", h / math.log(2.0)) for h in (4, 8, 16)])
PENALTIES = [0.0, 0.2, 0.45, 0.65, 0.85, 1.05, 1.25]      # the H2 grid of run_sensitivity_commitment.py
DWELLS = [2, 5, 10, 20, 40]
CALIB_DWELLS = [2, 3, 5, 8, 12, 20, 30, 50, 80, 120]
FAR_OBJECTIVE = 12
GOALS = ["objective", "teammate", "resource", "enemy", "roam"]
EXTRA_COLUMNS = ([f"share_{g}" for g in GOALS]
                 + ["far_objective_share", "far_objective_steps", "idle_item_chain_rate_per_100"])
KEYS = ["part", "style", "variant", "map", "scenario", "episode", "seed"]
CHANGED = ["w_commitment", "distance_utility", "distance_scale", "min_dwell_steps"]
HASHED = ["code/fps_priority_ai/config.py", "code/fps_priority_ai/policy.py", "code/fps_priority_ai/env.py",
          "code/fps_priority_ai/experiment.py", "code/fps_priority_ai/metrics.py",
          "code/experiments/run_form_variants.py"]


class LoggedEnv(FPSEnv):
    """FPSEnv that keeps the step logs of its last episode (run_episode_env returns the environment, not the logs)."""

    def run_episode(self, evaluated_style: str):
        res = super().run_episode(evaluated_style)
        self.last_logs = res.logs
        return res


experiment.FPSEnv = LoggedEnv   # run_episode_env builds its environment through this name; nothing else changes


def v13_seed(base: int, map_name: str, scenario: str, episode: int) -> int:
    """Episode seed of round v13: the map is part of the seed string, the condition is not (common random numbers)."""
    return episode_seed(base, f"{map_name}|{scenario}", episode)


def variant(style: PriorityWeights, label: str, **changes) -> PriorityWeights:
    # a name of its own: the opponent keeps the stock Aggressive style (run_episode_env adds the variant by name)
    return replace(style, name=f"{SHORT[style.name]}|{label}", **changes)


def conditions(part: str, matched: dict | None = None) -> list[tuple[str, str, PriorityWeights]]:
    """(style short name, variant label, policy) of one part."""
    styles = default_styles("exp")
    out = []
    if part == "a":
        for s in styles.values():
            for label, form, tau in TRANSFORMS:
                out.append((SHORT[s.name], label, variant(s, label, distance_utility=form, distance_scale=tau)))
    elif part == "b":
        mc = styles["Mission–Cooperation"]
        for w in PENALTIES:
            out.append(("MC", f"pen_{w:.2f}", variant(mc, f"pen_{w:.2f}", w_commitment=w)))
        for n in DWELLS:
            out.append(("MC", f"dwell_{n}", variant(mc, f"dwell_{n}", w_commitment=0.0, min_dwell_steps=n)))
    elif part in ("c", "calib"):
        for s in styles.values():
            short = SHORT[s.name]
            out.append((short, "main", variant(s, "main")))
            grid = [("dwell_matched", int(matched[short]))] if part == "c" else [(f"dwell_{n}", n) for n in CALIB_DWELLS]
            for label, n in grid:
                out.append((short, label, variant(s, label, w_commitment=0.0, min_dwell_steps=n)))
    else:
        raise ValueError(f"unknown part: {part!r}")
    return out


def log_measures(env: FPSEnv, logs) -> dict:
    """Measures of team 0 from the step logs (module docstring)."""
    mine = sorted((l for l in logs if l.team == 0), key=lambda l: (l.agent_id, l.step))
    n = len(mine)
    out: dict = {f"share_{g}": (sum(l.goal_type == g for l in mine) / n if n else "") for g in GOALS}
    obj = env.objective_pos()
    far = [l for l in mine if obj is not None and manhattan(l.pos, obj) > FAR_OBJECTIVE]
    out["far_objective_share"] = sum(l.goal_type == "objective" for l in far) / len(far) if far else ""
    out["far_objective_steps"] = len(far)
    chains = sum(1 for a, b in zip(mine, mine[1:])
                 if a.agent_id == b.agent_id and b.step == a.step + 1 and a.goal_type == b.goal_type == "resource"
                 and a.pos == a.goal_pos and b.goal_pos != a.goal_pos and not b.status_bad)
    out["idle_item_chain_rate_per_100"] = 100.0 * chains / n if n else ""
    return {k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in out.items()}


def run_task(task: tuple) -> dict:
    part, short, label, style, map_name, sc_name, ep, base = task
    seed = v13_seed(base, map_name, sc_name, ep)
    row, env = run_episode_env(SCENARIOS[sc_name], style, default_styles("exp"), seed, MAPS[map_name])
    return {"part": part, "style": short, "variant": label, "map": map_name, "scenario": sc_name, "episode": ep,
            "seed": seed, **row, **log_measures(env, env.last_logs)}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--part", required=True, choices=["a", "b", "c", "calib"])
    p.add_argument("--seed-base", type=int, required=True)
    p.add_argument("--episodes", type=int, default=100)
    p.add_argument("--matched", default=None, help='part c: JSON such as {"MC": 20, "PO": 30, "Agg": 5, "SA": 5}')
    p.add_argument("--jobs", type=int, default=12)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    rows_path = out / f"rows_{a.part}.csv"
    if rows_path.exists():
        sys.exit(f"{rows_path} exists: not overwriting it")
    matched = json.loads(a.matched) if a.matched else None
    if a.part == "c" and not matched:
        sys.exit("part c needs --matched")
    conds = conditions(a.part, matched)
    tasks = [(a.part, short, label, style, m, sc, ep, a.seed_base) for short, label, style in conds
             for m in MAP_NAMES for sc in SCENARIOS for ep in range(a.episodes)]
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    record = {"part": a.part, "seed_base": a.seed_base, "episodes": a.episodes, "maps": MAP_NAMES,
              "scenarios": list(SCENARIOS), "matched": matched, "n_tasks": len(tasks),
              "conditions": [{"style": short, "variant": label, **{f: getattr(s, f) for f in CHANGED}}
                             for short, label, s in conds],
              "testbed": testbed_flags(), "git_head": head, "sha256": {f: sha256(ROOT / f) for f in HASHED},
              "versions": {"python": platform.python_version(), "numpy": np.__version__},
              "start": time.strftime("%Y-%m-%d %H:%M:%S")}
    (out / f"run_{a.part}.json").write_text(json.dumps(record, indent=1))
    t0 = time.time()
    with Pool(a.jobs) as pool:
        rows = list(pool.imap_unordered(run_task, tasks, chunksize=4))
    rows.sort(key=lambda r: (r["style"], r["variant"], r["map"], r["scenario"], r["episode"]))
    with rows_path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=KEYS + METRIC_COLUMNS + EXTRA_COLUMNS)
        w.writeheader()
        w.writerows(rows)
    record.update({"end": time.strftime("%Y-%m-%d %H:%M:%S"), "rows": len(rows), "seconds": round(time.time() - t0)})
    (out / f"run_{a.part}.json").write_text(json.dumps(record, indent=1))
    print(f"part {a.part}: {len(rows)} episodes in {time.time() - t0:.0f} s -> {rows_path}", flush=True)


if __name__ == "__main__":
    main()
