"""Decision-time measurement of the priority policy (2026-10-13; exploratory, outside the pre-registered tests).

The paper's real-time premise (Section 4) says that a decision must fit a frame budget. This script measures, on
the final testbed, the wall-clock time of one decision of one agent (PriorityPolicy.decide: perception, utilities
and goal selection, combat mode, risk-aware A* when a replan is triggered, and the shot), the time of each A*
plan, and the nodes each A* search expands. Every agent of both teams is timed (the opponent plays Aggressive).
The policy code is not changed: the three functions are wrapped for the duration of the run, and the episodes use
the seeds of the main experiment (common random numbers), so their metric rows must equal those of
repro_outputs/v3_fixed[/urban]/results.csv; the script checks this and reports the result.

The timings are those of the Python reference implementation on one core; the node expansions are independent of
the implementation. The samples are kept in typed arrays and the garbage collector runs before each condition, so that
collections of the growing sample store do not fall inside the timed calls (with Python lists, a first run on
2026-10-13 showed maxima that grew with the run, up to about 90 ms, while the medians and 99th percentiles agreed).

Usage (the final testbed needs the five rule flags):
  FPS_TEAMMATE_SWAP=1 FPS_LOCAL_AVOIDANCE=1 FPS_FORGET_MEMORY=1 FPS_SYMMETRIC_LOS=1 FPS_REACHABLE_PLACEMENT=1 \
      python experiments/time_decisions.py --out ../repro_outputs/decision_time --episodes 20
"""

from __future__ import annotations

import argparse
import csv
import gc
import json
import platform
import statistics
import sys
import time
from array import array
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fps_priority_ai import policy as policy_mod  # noqa: E402
from fps_priority_ai.experiment import MAPS, episode_seed, run_episode_env, testbed_flags  # noqa: E402
from fps_priority_ai.runner import DEFAULT_MODEL, default_scenarios, default_styles  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
REFERENCE = {"random": ROOT / "repro_outputs/v3_fixed/results.csv",
             "urban": ROOT / "repro_outputs/v3_fixed/urban/results.csv"}
CHECK_COLUMNS = ["objective_commitment_ratio", "engagement_redirection_rate_per_100", "resource_seeking_rate_per_100",
                 "avg_ally_proximity", "kills", "deaths", "control_score", "steps", "goal_switch_rate_per_100",
                 "walked_hits_per_step", "hits_taken"]


class Recorder:
    """Wraps PriorityPolicy.decide, PriorityPolicy._plan and the A* search of the policy module."""

    def __init__(self) -> None:
        # Typed arrays, not lists: the cyclic garbage collector does not traverse them, so millions of samples do
        # not lengthen the collections that may fall inside a timed call (with lists, the maxima grew with the run).
        self.decide_ns = array("q")
        self.decide_plans = array("i")
        self.plan_ns = array("q")
        self.search_ns = array("q")
        self.expanded = array("i")
        self._plans_in_decide = 0
        self._orig = (policy_mod.PriorityPolicy.decide, policy_mod.PriorityPolicy._plan, policy_mod.astar_search)

    def install(self) -> None:
        orig_decide, orig_plan, orig_search = self._orig
        rec = self

        def decide(self_, *a, **k):
            rec._plans_in_decide = 0
            t = time.perf_counter_ns()
            out = orig_decide(self_, *a, **k)
            rec.decide_ns.append(time.perf_counter_ns() - t)
            rec.decide_plans.append(rec._plans_in_decide)
            return out

        def plan(self_, *a, **k):
            t = time.perf_counter_ns()
            out = orig_plan(self_, *a, **k)
            rec.plan_ns.append(time.perf_counter_ns() - t)
            rec._plans_in_decide += 1
            return out

        def search(*a, **k):
            t = time.perf_counter_ns()
            res = orig_search(*a, **k)
            rec.search_ns.append(time.perf_counter_ns() - t)
            rec.expanded.append(res.expanded if res is not None else -1)
            return res

        policy_mod.PriorityPolicy.decide = decide
        policy_mod.PriorityPolicy._plan = plan
        policy_mod.astar_search = search

    def uninstall(self) -> None:
        policy_mod.PriorityPolicy.decide, policy_mod.PriorityPolicy._plan, policy_mod.astar_search = self._orig

    def mark(self) -> tuple[int, int, int]:
        return len(self.decide_ns), len(self.plan_ns), len(self.search_ns)


def pct(xs: list[float], q: float) -> float:
    xs = sorted(xs)
    if not xs:
        return float("nan")
    i = min(len(xs) - 1, max(0, int(round(q * (len(xs) - 1)))))
    return xs[i]


def summarize(decide_ns, decide_plans, plan_ns, expanded) -> dict:
    us = [x / 1000.0 for x in decide_ns]
    pus = [x / 1000.0 for x in plan_ns]
    exp_ok = [e for e in expanded if e >= 0]
    return {
        "decisions": len(us),
        "decide_mean_us": statistics.fmean(us) if us else float("nan"),
        "decide_median_us": pct(us, 0.5), "decide_p95_us": pct(us, 0.95), "decide_p99_us": pct(us, 0.99),
        "decide_p999_us": pct(us, 0.999), "decide_max_us": max(us) if us else float("nan"),
        "replan_share": (sum(1 for p in decide_plans if p > 0) / len(decide_plans)) if decide_plans else float("nan"),
        "plans": len(pus),
        "plan_mean_us": statistics.fmean(pus) if pus else float("nan"),
        "plan_median_us": pct(pus, 0.5), "plan_p95_us": pct(pus, 0.95), "plan_p99_us": pct(pus, 0.99),
        "plan_max_us": max(pus) if pus else float("nan"),
        "searches": len(expanded),
        "expanded_mean": statistics.fmean(exp_ok) if exp_ok else float("nan"),
        "expanded_median": pct(exp_ok, 0.5), "expanded_p95": pct(exp_ok, 0.95),
        "expanded_max": max(exp_ok) if exp_ok else float("nan"),
        "searches_failed": sum(1 for e in expanded if e < 0),
    }


def load_reference(map_name: str) -> dict:
    path = REFERENCE.get(map_name)
    if path is None or not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        return {(r["scenario"], r["style"], int(r["episode"])): r for r in csv.DictReader(f)}


def same(a: object, b: str) -> bool:
    a = "" if a is None else str(a)
    if a == b:
        return True
    try:
        return abs(float(a) - float(b)) <= 1e-6
    except ValueError:
        return False


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=str, default="../repro_outputs/decision_time")
    p.add_argument("--episodes", type=int, default=20)
    p.add_argument("--seed", type=int, default=2026)
    p.add_argument("--maps", type=str, default="random,urban")
    args = p.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    styles = default_styles(DEFAULT_MODEL)
    rec = Recorder()
    rec.install()
    rows, checks = [], {"compared": 0, "identical": 0, "missing": 0}
    try:
        for map_name in args.maps.split(","):
            ref = load_reference(map_name)
            for sc in default_scenarios():
                for st in styles.values():
                    gc.collect()  # collect outside the timed calls, before each condition
                    d0, p0, s0 = rec.mark()
                    t_run = time.perf_counter()
                    steps = 0
                    for ep in range(args.episodes):
                        row, env = run_episode_env(sc, st, styles, episode_seed(args.seed, sc.name, ep), MAPS[map_name])
                        steps += int(row["steps"])
                        r = ref.get((sc.name, st.name, ep))
                        if r is None:
                            checks["missing"] += 1
                        else:
                            checks["compared"] += 1
                            checks["identical"] += int(all(same(row[c], r[c]) for c in CHECK_COLUMNS))
                    t_run = time.perf_counter() - t_run
                    d1, p1, s1 = rec.mark()
                    s = summarize(rec.decide_ns[d0:d1], rec.decide_plans[d0:d1], rec.plan_ns[p0:p1], rec.expanded[s0:s1])
                    rows.append({"map": map_name, "scenario": sc.name, "style": st.name, "episodes": args.episodes,
                                 "steps": steps, "wall_s": round(t_run, 3), **s})
                    print(f"{map_name:6s} {sc.name:10s} {st.name:20s} decide median {s['decide_median_us']:7.1f} us"
                          f"  p99 {s['decide_p99_us']:8.1f} us  max {s['decide_max_us']:8.1f} us"
                          f"  replan {s['replan_share']:.2f}  expanded mean {s['expanded_mean']:.0f}"
                          f" max {s['expanded_max']}", flush=True)
    finally:
        rec.uninstall()

    overall = summarize(rec.decide_ns, rec.decide_plans, rec.plan_ns, rec.expanded)
    with (out / "decision_time.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    meta = {
        "overall": overall,
        "reproduction_check": checks,
        "testbed_flags": testbed_flags(),
        "episodes_per_condition": args.episodes, "seed": args.seed, "maps": args.maps,
        "python": platform.python_version(), "implementation": platform.python_implementation(),
        "machine": platform.machine(), "processor": platform.processor(), "platform": platform.platform(),
    }
    (out / "decision_time_summary.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    lines = ["# Decision time of the priority policy (exploratory)", "",
             f"Python {meta['python']} ({meta['implementation']}), {meta['platform']}, one core; "
             f"maps {args.maps}; {args.episodes} episodes per condition; seed {args.seed}.", "",
             f"Reproduction check against the main experiment: {checks['identical']} of {checks['compared']} "
             f"episodes identical on {', '.join(CHECK_COLUMNS)} ({checks['missing']} without a reference row).", "",
             "| | value |", "|---|---|"]
    for k, v in overall.items():
        lines.append(f"| {k} | {v:.1f} |" if isinstance(v, float) else f"| {k} | {v} |")
    lines += ["", "Per condition: decision_time.csv (times in microseconds; expansions in nodes)."]
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
