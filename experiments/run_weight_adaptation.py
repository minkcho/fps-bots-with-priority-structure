"""Round v13, Part WA: runtime weight adaptation (difficulty adjustment) of the unified policy (2026-09-29).

A demonstration of the adaptation rules of the report (tab:adapt_rules). The weights of the evaluated team (team 0)
change during an episode through the first-order filter w(t) = w(t-1) + (w*(t) - w(t-1)) / T, abruptly (T = 1) or
gradually (T = 50 steps), and the team's behaviour is recorded per 25-step bin. The testbed has no human player, so
the closed-loop triggers read the adapting team's own state; the Aggressive opponent does not adapt. Control runs
without the early end at 120 points, so that every episode lasts 550 steps and the time course is complete.

Rules (the target values are those of the designed style that embodies the rule's intent; lambda_E = w_exposure):
  R1  team losing in Control        w_objective -> 1.35, w_commitment -> 0.85   (Persistent Objective)
  R2  team repeatedly eliminated    w_team -> 0.95                              (Mission-Cooperation)
  R3  low on health or ammunition   w_resource -> 1.10, lambda_E -> 20.0        (Survival-Aware)
  R4  few engagements               w_engage -> 1.35, lambda_E -> 3.64          (Aggressive)
Parts:
  step    open loop: from step t0 + 1 = 201 on the weights move to the rule's targets; schedules none / abrupt /
          gradual. R1 on Aggressive in Control; R2 on Aggressive, R3 on Mission-Cooperation, R4 on Persistent
          Objective and on Mission-Cooperation in Deathmatch; the two channels of R3 separately, the goal part
          (R3goal: w_resource only) on Mission-Cooperation and the route part (R3route: lambda_E only) on Aggressive
  closed  closed loop: from step 101 on, a rule is active while its trigger holds over the last 100 steps --
          R1 opponent score - own score >= 10 (Control only), R2 >= 2 deaths of the team, R3 >= 30% of the team's
          alive agent-steps in low status, R4 no opponent visible to the team. Active rules add offsets to the goal
          weights (R1 +1.0 w_objective and +0.5 w_commitment, R2 +0.8 w_team, R3 +0.65 w_resource, R4 +0.9 w_engage)
          and multiply lambda_E (R3 x2, R4 x0.5); schedules fixed (triggers computed as shadows, weights unchanged) /
          abrupt / gradual; the four designed styles x three scenarios
Per episode and 25-step bin (team 0): alive agent-steps; steps on the Objective, Resource, Teammate and Enemy goals;
goal switches (consecutive steps of one agent, as in metrics.compute_metrics); expected hits and steps with an
opponent in line of sight (experiment.walked_exposure, step by step); ally distance while both are alive; kills and
deaths; Control points of both teams; agent-steps in low status and those on the Resource goal; the applied weights
(bin means) and the share of steps each rule is active.
Per episode (closed loop): the same sums over the steps on which each rule is active.
Seeds: episode_seed(base, "<map>|<scenario>", episode), common to all schedules and rules (common random numbers).
Output: <out>/bins_<part>.csv, <out>/episodes_<part>.csv, <out>/run_<part>.json.
Usage: python experiments/run_weight_adaptation.py --part step --seed-base 5901 --episodes 30 --jobs 12 \
           --out ../repro_outputs/dev_v13/wa
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import random
import subprocess
import sys
import time
from collections import defaultdict, deque
from dataclasses import replace
from multiprocessing import Pool
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fps_priority_ai.config import AgentConfig, WeaponConfig  # noqa: E402
from fps_priority_ai.env import FPSEnv  # noqa: E402
from fps_priority_ai.experiment import MAPS, episode_seed, testbed_flags, walked_exposure  # noqa: E402
from fps_priority_ai.runner import default_scenarios, default_styles  # noqa: E402
from fps_priority_ai.world import euclidean  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
SHORT = {"Mission–Cooperation": "MC", "Persistent Objective": "PO", "Aggressive": "Agg", "Survival-Aware": "SA"}
LONG = {v: k for k, v in SHORT.items()}
MAP_NAMES = ["random", "urban"]
FIELDS = ["w_objective", "w_engage", "w_resource", "w_team", "w_commitment", "w_exposure"]
RULES = ["R1", "R2", "R3", "R4"]
BIN, T0, T_GRADUAL, WINDOW = 25, 200, 50.0, 100
SCHEDULES = {"none": None, "abrupt": 1.0, "gradual": T_GRADUAL}            # open loop: T (None = no change)
CLOSED_SCHEDULES = {"fixed": None, "abrupt": 1.0, "gradual": T_GRADUAL}    # closed loop: T (None = shadows only)
STEP_RULES = {   # condition: (base style, scenario, target values); the base is a style whose weights the rule's
    # change can act on (development pilot 2026-09-29: Aggressive's chase mode overrides w_resource, so the goal part
    # of R3 runs on Mission-Cooperation, whose hold mode leaves the goal weights in force; lambda_E rises most on
    # Aggressive, so the route part of R3 runs there; R4 runs on Persistent Objective and on Mission-Cooperation)
    "R1@Agg": ("Agg", "Control", {"w_objective": 1.35, "w_commitment": 0.85}),
    "R2@Agg": ("Agg", "Deathmatch", {"w_team": 0.95}),
    "R3@MC": ("MC", "Deathmatch", {"w_resource": 1.10, "w_exposure": 20.0}),
    "R3goal@MC": ("MC", "Deathmatch", {"w_resource": 1.10}),
    "R3route@Agg": ("Agg", "Deathmatch", {"w_exposure": 20.0}),
    "R4@PO": ("PO", "Deathmatch", {"w_engage": 1.35, "w_exposure": 3.64}),
    "R4@MC": ("MC", "Deathmatch", {"w_engage": 1.35, "w_exposure": 3.64}),
}
OFFSETS = {"R1": {"w_objective": 1.0, "w_commitment": 0.5}, "R2": {"w_team": 0.8}, "R3": {"w_resource": 0.65},
           "R4": {"w_engage": 0.9}}
LAMBDA_FACTORS = {"R3": 2.0, "R4": 0.5}
TRIGGERS = {"R1_gap": 10, "R2_deaths": 2, "R3_low_share": 0.3}
COUNTS = ["alive", "obj", "res", "tm", "enemy", "switches", "exp_hits", "los", "ally_sum", "ally_n", "kills", "deaths",
          "pts_own", "pts_opp", "low", "low_res"]
HASHED = ["code/fps_priority_ai/config.py", "code/fps_priority_ai/policy.py", "code/fps_priority_ai/env.py",
          "code/fps_priority_ai/experiment.py", "code/experiments/run_weight_adaptation.py"]


class Controller:
    """Team 0's weights over one episode: open-loop targets (a rule's values after step T0) or closed-loop targets (the
    active rules), applied through w += (w* - w) / T; T = None leaves the weights unchanged (closed loop: shadows)."""

    def __init__(self, mode: str, T: float | None, targets: dict | None = None):
        self.mode, self.T, self.targets = mode, T, targets or {}

    def start(self, env: FPSEnv) -> None:
        self.team = [aid for aid, a in env.agents.items() if a.team == 0]
        self.base = {f: getattr(env.policies[self.team[0]].style, f) for f in FIELDS}
        self.w = dict(self.base)
        self.window: deque = deque(maxlen=WINDOW)       # per step: (team deaths, alive agent-steps, low status, seen)
        self.records: list = []                        # per step: (weights, active rules)
        self.scores: list = []                         # per step: Control points of teams 0 and 1 after the step

    def active(self, env: FPSEnv, t: int) -> set:
        if self.mode != "closed" or t <= WINDOW:
            return set()
        on = set()
        if env.scenario.mode == "control" and env.team_scores[1] - env.team_scores[0] >= TRIGGERS["R1_gap"]:
            on.add("R1")
        if sum(d for d, _, _, _ in self.window) >= TRIGGERS["R2_deaths"]:
            on.add("R2")
        alive = sum(n for _, n, _, _ in self.window)
        if alive and sum(low for _, _, low, _ in self.window) / alive >= TRIGGERS["R3_low_share"]:
            on.add("R3")
        if not any(seen for _, _, _, seen in self.window):
            on.add("R4")
        return on

    def target(self, t: int, on: set) -> dict:
        if self.mode == "step":
            return {**self.base, **self.targets} if t > T0 else dict(self.base)
        w = dict(self.base)
        for r in on:
            for f, d in OFFSETS[r].items():
                w[f] += d
            w["w_exposure"] *= LAMBDA_FACTORS.get(r, 1.0)
        return w

    def before_step(self, env: FPSEnv) -> None:
        t = env.step_idx + 1
        on = self.active(env, t)
        if self.T is not None:
            goal = self.target(t, on)
            new = {f: self.w[f] + (goal[f] - self.w[f]) / self.T for f in FIELDS}
            if new != self.w:
                self.w = new
                for aid in self.team:
                    env.policies[aid].style = replace(env.policies[aid].style, **self.w)
        self.records.append((dict(self.w), on))

    def after_step(self, env: FPSEnv, logs) -> None:
        mine = [l for l in logs if l.team == 0]
        deaths = sum(1 for l in logs if l.team != 0 and l.killed_enemy)
        self.window.append((deaths, len(mine), sum(l.status_bad for l in mine), any(l.enemy_visible for l in mine)))
        self.scores.append((env.team_scores[0], env.team_scores[1]))


class AdaptiveEnv(FPSEnv):
    """FPSEnv whose steps call the controller before the decisions and after the outcomes; FPSEnv.run_episode
    re-initialises the environment, keeps the controller, and the step logs of the episode are kept."""

    def __init__(self, *args, controller: Controller | None = None, **kwargs):
        if controller is not None:
            self.controller = controller
        super().__init__(*args, **kwargs)

    def step(self):
        if self.step_idx == 0:
            self.controller.start(self)
        self.controller.before_step(self)
        logs = super().step()
        self.controller.after_step(self, logs)
        return logs

    def run_episode(self, evaluated_style: str):
        res = super().run_episode(evaluated_style)
        self.last_logs = res.logs
        return res


def per_step(env: AdaptiveEnv, logs) -> dict:
    """Team 0's per-step counts (COUNTS), indexed by step (1 ... steps)."""
    by_step = defaultdict(list)
    for l in logs:
        by_step[l.step].append(l)
    rec = {t: dict.fromkeys(COUNTS, 0.0) for t in range(1, env.step_idx + 1)}
    prev: dict = {}
    for t in sorted(by_step):
        ls = by_step[t]
        mine = [l for l in ls if l.team == 0]
        r = rec[t]
        r["alive"] = len(mine)
        for l in mine:
            r["obj"] += l.goal_type == "objective"
            r["res"] += l.goal_type == "resource"
            r["tm"] += l.goal_type == "teammate"
            r["enemy"] += l.goal_type == "enemy"
            p = prev.get(l.agent_id)
            if p is not None and p[0] == t - 1 and p[1] != l.goal_type:
                r["switches"] += 1
            prev[l.agent_id] = (t, l.goal_type)
            r["kills"] += l.killed_enemy
            r["low"] += l.status_bad
            r["low_res"] += l.status_bad and l.goal_type == "resource"
        r["deaths"] = sum(1 for l in ls if l.team != 0 and l.killed_enemy)
        if mine:
            h, lf = walked_exposure(env, ls)
            r["exp_hits"], r["los"] = h * len(mine), lf * len(mine)
        if len(mine) == 2:
            r["ally_sum"], r["ally_n"] = euclidean(mine[0].pos, mine[1].pos), 1
    return rec


def run_task(task: tuple) -> tuple[list, dict]:
    part, cond, style_short, sc_name, schedule, T, targets, map_name, ep, base = task
    styles = default_styles("exp")
    style = replace(styles[LONG[style_short]], name=f"{style_short}|adaptive")
    sc = {s.name: s for s in default_scenarios()}[sc_name]
    if sc.mode == "control":
        sc = replace(sc, score_to_win=10**9)          # no early end: the full 550-step time course
    seed = episode_seed(base, f"{map_name}|{sc_name}", ep)
    ctrl = Controller("step" if part == "step" else "closed", T, targets)
    env = AdaptiveEnv(map_cfg=MAPS[map_name], agent_cfg=AgentConfig(), weapon_cfg=WeaponConfig(), scenario=sc,
                      styles={**styles, style.name: style}, rng=random.Random(seed), controller=ctrl)
    env.run_episode(evaluated_style=style.name)
    rec = per_step(env, env.last_logs)
    last = (0, 0)
    for t, (own, opp) in enumerate(ctrl.scores, start=1):
        rec[t]["pts_own"], rec[t]["pts_opp"] = own - last[0], opp - last[1]
        last = (own, opp)
    keys = {"part": part, "condition": cond, "style": style_short, "scenario": sc_name, "schedule": schedule,
            "map": map_name, "episode": ep}
    bins = []
    for b in range((env.step_idx + BIN - 1) // BIN):
        ts = range(b * BIN + 1, min(env.step_idx, (b + 1) * BIN) + 1)
        row = {**keys, "bin": b, **{c: round(sum(rec[t][c] for t in ts), 6) for c in COUNTS}}
        for f in FIELDS:
            row[f] = round(sum(ctrl.records[t - 1][0][f] for t in ts) / len(ts), 6)
        for r in RULES:
            row[f"active_{r}"] = round(sum(r in ctrl.records[t - 1][1] for t in ts) / len(ts), 6)
        bins.append(row)
    episode = {**keys, "seed": seed, "steps": env.step_idx,
               **{c: round(sum(v[c] for v in rec.values()), 6) for c in COUNTS}}
    for r in RULES:
        on = [t for t in rec if r in ctrl.records[t - 1][1]]
        episode[f"{r}_active_steps"] = len(on)
        for c in COUNTS:
            episode[f"{r}_{c}"] = round(sum(rec[t][c] for t in on), 6)
    return bins, episode


def tasks_for(part: str, episodes: int, base: int, conditions: list | None = None) -> list[tuple]:
    out = []
    if part == "step":
        for cond, (style_short, sc_name, targets) in STEP_RULES.items():
            if conditions and cond not in conditions:
                continue
            for schedule, T in SCHEDULES.items():
                for m in MAP_NAMES:
                    for ep in range(episodes):
                        out.append((part, cond, style_short, sc_name, schedule, T, targets, m, ep, base))
    else:
        for style_short in SHORT.values():
            for sc in default_scenarios():
                for schedule, T in CLOSED_SCHEDULES.items():
                    for m in MAP_NAMES:
                        for ep in range(episodes):
                            out.append((part, "closed", style_short, sc.name, schedule, T, None, m, ep, base))
    return out


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, rows: list) -> None:
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--part", required=True, choices=["step", "closed"])
    p.add_argument("--seed-base", type=int, required=True)
    p.add_argument("--episodes", type=int, default=100)
    p.add_argument("--jobs", type=int, default=12)
    p.add_argument("--conditions", default=None, help="step part: comma-separated subset of STEP_RULES")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if (out / f"bins_{a.part}.csv").exists():
        sys.exit(f"{out / f'bins_{a.part}.csv'} exists: not overwriting it")
    conditions = a.conditions.split(",") if a.conditions else None
    tasks = tasks_for(a.part, a.episodes, a.seed_base, conditions)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    record = {"part": a.part, "seed_base": a.seed_base, "episodes": a.episodes, "maps": MAP_NAMES, "n_tasks": len(tasks),
              "conditions": conditions,
              "bin": BIN, "t0": T0, "T_gradual": T_GRADUAL, "window": WINDOW, "step_rules": STEP_RULES,
              "offsets": OFFSETS, "lambda_factors": LAMBDA_FACTORS, "triggers": TRIGGERS,
              "control_early_end": False, "testbed": testbed_flags(), "git_head": head,
              "sha256": {f: sha256(ROOT / f) for f in HASHED},
              "versions": {"python": platform.python_version(), "numpy": np.__version__},
              "start": time.strftime("%Y-%m-%d %H:%M:%S")}
    (out / f"run_{a.part}.json").write_text(json.dumps(record, indent=1))
    t0 = time.time()
    with Pool(a.jobs) as pool:
        results = list(pool.imap_unordered(run_task, tasks, chunksize=2))
    order = lambda r: (r["condition"], r["style"], r["scenario"], r["schedule"], r["map"], r["episode"])  # noqa: E731
    bins = sorted((b for bs, _ in results for b in bs), key=lambda r: (*order(r), r["bin"]))
    episodes = sorted((e for _, e in results), key=order)
    write(out / f"bins_{a.part}.csv", bins)
    write(out / f"episodes_{a.part}.csv", episodes)
    record.update({"end": time.strftime("%Y-%m-%d %H:%M:%S"), "episodes_run": len(episodes),
                   "seconds": round(time.time() - t0)})
    (out / f"run_{a.part}.json").write_text(json.dumps(record, indent=1))
    print(f"part {a.part}: {len(episodes)} episodes in {time.time() - t0:.0f} s -> {out}", flush=True)


if __name__ == "__main__":
    main()
