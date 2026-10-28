"""Round v13, Part WA analysis: the pre-registered tests of the weight-adaptation demonstration
(FAMILY_ADAPT_PLAN_V13_*.md, §5-§6).

Reads bins_step.csv, bins_closed.csv and episodes_closed.csv of run_weight_adaptation.py (one directory) and writes
summary.md and summary.json there. Per episode, a measure over a window is the ratio of the window's sums (e.g.
objective share = steps on the Objective goal / alive agent-steps of team 0). The schedules of a condition share their
episodes' seeds, so every comparison is paired by map and episode.
Windows (25-step bins): pre = steps 101-200, first = 201-225, early = 201-250, late = 351-550.
  WA-H1  the behaviour follows the weights: in the late window the measure of each condition in RULE_MEASURES moves
         in the predicted direction against the unchanged run, under the abrupt and the gradual schedule, on both maps
         (one-sided paired Wilcoxon, p_Holm < ALPHA)
  WA-H2  gradual application: (a) in the first window the change against the unchanged run is smaller under the
         gradual schedule than under the abrupt one, for the conditions in FIRST_RULES (one-sided paired Wilcoxon of
         gradual against abrupt, in the direction opposite to the rule's; p_Holm < ALPHA); (b) in the late window the
         gradual schedule is at least half-way from the unchanged run to the abrupt one, for the conditions in
         HALF_RULES: the contrast s * (gradual - abrupt / 2 - unchanged / 2) (s = predicted sign) has a bootstrap CI
         lower bound >= 0; the ratio (gradual - unchanged) / (abrupt - unchanged) is reported for reference
  WA-H3  salience: (a) after an abrupt change of the conditions in BURST_RULES the goal-switch rate in the first window
         exceeds the unchanged run's, and the gradual schedule's rate is below the abrupt one's (one-sided paired
         Wilcoxon, p_Holm < ALPHA); the late-window rates of the three schedules are reported; (b) after an abrupt
         change of the conditions in NO_BURST_RULES the early-window goal-switch rate exceeds the unchanged run's by
         less than MARGIN switches per 100 agent-steps (upper bound of the bootstrap CI of the mean difference)
  WA-H4  closed loop, for the rules, styles and scenarios in CLOSED_TESTS, gradual controller against fixed weights:
         (a) on the steps on which the rule is active (shadow triggers in the fixed run): one-sided paired Wilcoxon over
         the episodes of both maps (pairs matched by map and episode) in which the rule is active for at least
         MIN_ACTIVE steps in both runs, in every style x scenario cell with at least MIN_EPISODES such episodes
         (p_Holm < ALPHA over the eligible cells; per-map values for reference); (b) onset-locked: the two runs are
         identical until the first activation of any rule (the controller changes no weight before), so in the
         episodes whose first active bin b* (of the fixed run) holds the rule alone and b* <= 17, the rule's measure
         over bins b* + 1 ... b* + 4 is compared (same test, cells and eligibility count, Holm over the eligible cells)
Identity checks (reported before any result; a difference is a defect of the run): bins 1-8 (steps 1-200) identical
across the schedules of every open-loop condition; the unchanged runs identical across open-loop conditions that share
style and scenario; the unchanged open-loop runs identical to the fixed closed-loop runs of the same style and
scenario; the first active bin identical across the three closed-loop schedules.
Bootstrap: paired resampling of episodes, BOOT resamples, one stream with seed SEED (WA-H2(b), then WA-H3(b)).
Usage: python experiments/analyze_weight_adaptation.py --dir ../repro_outputs/v13_adapt
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_stats import holm, wilcoxon_paired  # noqa: E402

ALPHA = 0.05
BOOT, SEED = 2000, 13032
MARGIN = 1.0               # WA-H3(b): switches per 100 agent-steps
MIN_ACTIVE, MIN_EPISODES = 25, 20   # WA-H4
ONSET_BINS, LAST_ONSET = 4, 17      # WA-H4(b): bins after the onset bin; the latest onset bin (17 + 4 = 21)
MAPS = ["random", "urban"]
WINDOWS = {"pre": range(4, 8), "first": [8], "early": [8, 9], "late": range(14, 22)}
RATIOS = {   # measure: (numerator, denominator, factor)
    "objective": ("obj", "alive", 1.0), "resource": ("res", "alive", 1.0), "teammate": ("tm", "alive", 1.0),
    "enemy": ("enemy", "alive", 1.0), "switches": ("switches", "alive", 100.0),
    "exp_hits": ("exp_hits", "alive", 1.0), "los": ("los", "alive", 1.0), "ally_dist": ("ally_sum", "ally_n", 1.0),
    "kills": ("kills", "alive", 100.0), "deaths": ("deaths", "alive", 100.0), "low_res": ("low_res", "low", 1.0)}
RULE_MEASURES = {"R1@Agg": [("objective", +1)], "R2@Agg": [("ally_dist", -1)], "R3@MC": [("resource", +1)],
                 "R3goal@MC": [("resource", +1)], "R3route@Agg": [("exp_hits", -1)], "R4@PO": [("los", +1)]}
FIRST_RULES = {"R2@Agg": ("ally_dist", -1), "R3goal@MC": ("resource", +1), "R4@MC": ("enemy", +1)}
HALF_RULES = ["R1@Agg", "R2@Agg", "R3@MC", "R3goal@MC", "R3route@Agg"]
BURST_RULES = ["R2@Agg", "R4@MC"]
NO_BURST_RULES = ["R3route@Agg", "R1@Agg"]
CLOSED_TESTS = {"R2": ("ally_dist", -1, ["Agg", "PO", "SA"], ["Mission", "Deathmatch", "Control"]),
                "R1": ("pts_gap", +1, ["Agg", "SA"], ["Control"])}
RULES = ["R1", "R2", "R3", "R4"]
COUNTS = ["alive", "obj", "res", "tm", "enemy", "switches", "exp_hits", "los", "ally_sum", "ally_n", "kills", "deaths",
          "pts_own", "pts_opp", "low", "low_res"]
WEIGHTS = ["w_objective", "w_engage", "w_resource", "w_team", "w_commitment", "w_exposure"]
SAME_BASE = [["R2@Agg", "R3route@Agg"], ["R3@MC", "R3goal@MC", "R4@MC"]]          # open-loop conditions, same runs
OPEN_CLOSED = {"R2@Agg": ("Agg", "Deathmatch"), "R3@MC": ("MC", "Deathmatch"), "R4@PO": ("PO", "Deathmatch"),
               "R1@Agg": ("Agg", "Control")}                                     # unchanged open = fixed closed
DESCRIBE = {"R1@Agg": ["objective", "switches"], "R2@Agg": ["ally_dist", "switches"],
            "R3@MC": ["resource", "low_res", "exp_hits", "switches"], "R3goal@MC": ["resource", "low_res", "switches"],
            "R3route@Agg": ["exp_hits", "resource", "enemy", "switches"], "R4@PO": ["los", "exp_hits", "switches"],
            "R4@MC": ["enemy", "los", "switches"]}


def one_sided(p_two: float, effect: float, sign: int) -> float:
    return p_two / 2 if effect * sign > 0 else 1 - p_two / 2


def window_values(bins: pd.DataFrame, window: str, measure: str) -> pd.DataFrame:
    """Per condition, schedule, map and episode: the measure over the window (ratio of sums)."""
    num, den, f = RATIOS[measure]
    w = bins[bins["bin"].isin(list(WINDOWS[window]))]
    g = w.groupby(["condition", "schedule", "map", "episode"])[[num, den]].sum()
    return (f * g[num] / g[den].replace(0, np.nan)).rename(measure).reset_index()


def pair(v: pd.DataFrame, cond: str, a: str, b: str, m: str, measure: str) -> tuple[np.ndarray, np.ndarray]:
    x = v[(v["condition"] == cond) & (v["schedule"] == a) & (v["map"] == m)].set_index("episode")[measure]
    y = v[(v["condition"] == cond) & (v["schedule"] == b) & (v["map"] == m)].set_index("episode")[measure]
    j = pd.concat([x.rename("x"), y.rename("y")], axis=1, join="inner").dropna()
    return j["x"].to_numpy(), j["y"].to_numpy()


def aligned(v: pd.DataFrame, cond: str, schedules: tuple, m: str, measure: str) -> list[np.ndarray]:
    """The measure of several schedules of a condition on one map, matched by episode (complete episodes only)."""
    cols = [v[(v["condition"] == cond) & (v["schedule"] == s) & (v["map"] == m)].set_index("episode")[measure].rename(s)
            for s in schedules]
    j = pd.concat(cols, axis=1, join="inner").dropna()
    return [j[s].to_numpy() for s in schedules]


def test(x: np.ndarray, y: np.ndarray, sign: int) -> dict:
    w = wilcoxon_paired(x, y)
    diff = float(np.mean(x - y)) if len(x) else float("nan")
    return {"n": int(len(x)), "mean_x": float(np.mean(x)) if len(x) else None,
            "mean_y": float(np.mean(y)) if len(y) else None, "mean_diff": diff, "r": w["r"],
            "p": one_sided(w["p"], w["r"] if w["r"] else diff, sign)}


def boot(fn, *arrays, rng) -> tuple[float, float]:
    n = len(arrays[0])
    vals = []
    for _ in range(BOOT):
        i = rng.integers(0, n, n)
        vals.append(fn(*(a[i] for a in arrays)))
    return float(np.nanpercentile(vals, 2.5)), float(np.nanpercentile(vals, 97.5))


def late_ratio(g: np.ndarray, a: np.ndarray, n0: np.ndarray) -> float:
    """(gradual - unchanged) / (abrupt - unchanged), mean differences; NaN if the abrupt change is zero (reference)."""
    den = float(np.mean(a - n0))
    return float(np.mean(g - n0)) / den if den else float("nan")


def half_contrast(sign: int):
    """Mean of s * (gradual - abrupt / 2 - unchanged / 2): >= 0 iff the gradual schedule is at least half-way from the
    unchanged run to the abrupt one in the predicted direction (for an abrupt change in that direction)."""
    return lambda g, a, n0: float(np.mean(sign * (g - a / 2 - n0 / 2)))


def with_holm(tests: list[dict]) -> list[dict]:
    for t, pa in zip(tests, holm([t["p"] for t in tests]) if tests else []):
        t["p_holm"] = pa
    return tests


def wa_h1(bins: pd.DataFrame) -> dict:
    tests = []
    for cond, ms in RULE_MEASURES.items():
        for measure, sign in ms:
            v = window_values(bins, "late", measure)
            for sch in ("abrupt", "gradual"):
                for m in MAPS:
                    x, y = pair(v, cond, sch, "none", m, measure)
                    tests.append({"rule": cond, "measure": measure, "sign": sign, "schedule": sch, "map": m,
                                  **test(x, y, sign)})
    with_holm(tests)
    per_rule = {c: all(t["p_holm"] < ALPHA for t in tests if t["rule"] == c) for c in RULE_MEASURES}
    return {"tests": tests, "met_per_rule": per_rule, "met": all(per_rule.values())}


def wa_h2(bins: pd.DataFrame, rng) -> dict:
    first, late = [], []
    for cond, (measure, sign) in FIRST_RULES.items():
        v1 = window_values(bins, "first", measure)
        for m in MAPS:
            x, y = pair(v1, cond, "gradual", "abrupt", m, measure)
            first.append({"rule": cond, "measure": measure, "map": m, **test(x, y, -sign)})
    for cond in HALF_RULES:
        for measure, sign in RULE_MEASURES[cond]:
            v3 = window_values(bins, "late", measure)
            for m in MAPS:
                g, a, n0 = aligned(v3, cond, ("gradual", "abrupt", "none"), m, measure)
                fn = half_contrast(sign)
                lo, hi = boot(fn, g, a, n0, rng=rng)
                late.append({"rule": cond, "measure": measure, "map": m, "n": int(len(g)),
                             "mean_gradual": float(np.mean(g)), "mean_abrupt": float(np.mean(a)),
                             "mean_unchanged": float(np.mean(n0)), "contrast": fn(g, a, n0), "ci": [lo, hi],
                             "ratio": late_ratio(g, a, n0), "ok": lo >= 0})
    with_holm(first)
    return {"first": first, "late": late, "met_first": all(t["p_holm"] < ALPHA for t in first),
            "met_late": all(t["ok"] for t in late)}


def wa_h3(bins: pd.DataFrame, rng) -> dict:
    v1 = window_values(bins, "first", "switches")
    burst = []
    for cond in BURST_RULES:
        for m in MAPS:
            x, y = pair(v1, cond, "abrupt", "none", m, "switches")
            burst.append({"rule": cond, "map": m, "comparison": "abrupt > none", **test(x, y, +1)})
            x, y = pair(v1, cond, "gradual", "abrupt", m, "switches")
            burst.append({"rule": cond, "map": m, "comparison": "gradual < abrupt", **test(x, y, -1)})
    with_holm(burst)
    vl = window_values(bins, "late", "switches")
    late = []
    for cond in BURST_RULES:
        for m in MAPS:
            u, a_, g = aligned(vl, cond, ("none", "abrupt", "gradual"), m, "switches")
            late.append({"rule": cond, "map": m, "none": float(np.mean(u)), "abrupt": float(np.mean(a_)),
                         "gradual": float(np.mean(g))})
    ve = window_values(bins, "early", "switches")
    route = []
    for cond in NO_BURST_RULES:
        for m in MAPS:
            x, y = pair(ve, cond, "abrupt", "none", m, "switches")
            lo, hi = boot(lambda a, b: np.mean(a - b), x, y, rng=rng)
            route.append({"rule": cond, "map": m, "mean_x": float(np.mean(x)), "mean_y": float(np.mean(y)),
                          "mean_diff": float(np.mean(x - y)), "ci": [lo, hi], "ok": hi < MARGIN})
    return {"burst": burst, "late": late, "route": route, "met_burst": all(t["p_holm"] < ALPHA for t in burst),
            "met_route": all(t["ok"] for t in route)}


def closed_value(e: pd.DataFrame, rule: str, measure: str) -> pd.Series:
    if measure == "pts_gap":
        return (e[f"{rule}_pts_own"] - e[f"{rule}_pts_opp"]) / e[f"{rule}_active_steps"].replace(0, np.nan)
    num, den, f = RATIOS[measure]
    return f * e[f"{rule}_{num}"] / e[f"{rule}_{den}"].replace(0, np.nan)


def paired_cells(e: pd.DataFrame, sign: int, keys: list) -> tuple[pd.DataFrame, int]:
    """Gradual against fixed values (column val) matched by map and episode; e holds only eligible episodes."""
    x = e[e["schedule"] == "gradual"].set_index(keys)["val"]
    y = e[e["schedule"] == "fixed"].set_index(keys)["val"]
    j = pd.concat([x.rename("x"), y.rename("y")], axis=1, join="inner").dropna()
    return j, len(j)


def verdicts(tests: list[dict]) -> dict:
    per_rule = {}
    for rule in CLOSED_TESTS:
        ts = [t for t in tests if t["rule"] == rule]
        per_rule[rule] = {"cells": len(ts), "significant": sum(t["p_holm"] < ALPHA for t in ts),
                          "met": bool(ts) and all(t["p_holm"] < ALPHA for t in ts)}
    return per_rule


def wa_h4a(e: pd.DataFrame) -> dict:
    tests, per_map = [], []
    for rule, (measure, sign, styles, scenarios) in CLOSED_TESTS.items():
        e = e.assign(val=closed_value(e, rule, measure))
        for (s, sc), g in e.groupby(["style", "scenario"], sort=False):
            if s not in styles or sc not in scenarios:
                continue
            j, n = paired_cells(g[g[f"{rule}_active_steps"] >= MIN_ACTIVE], sign, ["map", "episode"])
            if n < MIN_EPISODES:
                continue
            tests.append({"rule": rule, "measure": measure, "sign": sign, "style": s, "scenario": sc, "map": "both",
                          **test(j["x"].to_numpy(), j["y"].to_numpy(), sign)})
            for m in MAPS:
                jm = j.xs(m, level="map") if m in j.index.get_level_values("map") else j.iloc[:0]
                per_map.append({"rule": rule, "style": s, "scenario": sc, "map": m, "n": int(len(jm)),
                                "gradual": float(jm["x"].mean()) if len(jm) else None,
                                "fixed": float(jm["y"].mean()) if len(jm) else None})
    with_holm(tests)
    per_rule = verdicts(tests)
    return {"tests": tests, "per_map": per_map, "per_rule": per_rule, "met": all(r["met"] for r in per_rule.values())}


def onset_table(bc: pd.DataFrame) -> pd.DataFrame:
    """Per style, scenario, schedule, map and episode: the first bin with any rule active and the rules active in it."""
    act = bc[[f"active_{r}" for r in RULES]].to_numpy() > 0
    on = bc.assign(any_on=act.any(axis=1), rules=["".join(r for r, a in zip(RULES, row) if a) for row in act])
    first = on[on["any_on"]].sort_values("bin").groupby(["style", "scenario", "schedule", "map", "episode"]).first()
    return first[["bin", "rules"]].rename(columns={"bin": "onset"}).reset_index()


def wa_h4b(bc: pd.DataFrame) -> dict:
    onset = onset_table(bc)
    fixed = onset[onset["schedule"] == "fixed"].drop(columns="schedule")
    tests = []
    for rule, (measure, sign, styles, scenarios) in CLOSED_TESTS.items():
        eligible = fixed[(fixed["rules"] == rule) & (fixed["onset"] <= LAST_ONSET)]
        w = bc.merge(eligible, on=["style", "scenario", "map", "episode"])
        w = w[(w["bin"] > w["onset"]) & (w["bin"] <= w["onset"] + ONSET_BINS)]
        g = w.groupby(["style", "scenario", "schedule", "map", "episode"])[COUNTS].sum()
        if measure == "pts_gap":
            val = (g["pts_own"] - g["pts_opp"]) / (25.0 * ONSET_BINS)
        else:
            num, den, f = RATIOS[measure]
            val = f * g[num] / g[den].replace(0, np.nan)
        v = val.rename("val").reset_index()
        for (s, sc), cell in v.groupby(["style", "scenario"], sort=False):
            if s not in styles or sc not in scenarios:
                continue
            j, n = paired_cells(cell, sign, ["map", "episode"])
            if n < MIN_EPISODES:
                continue
            tests.append({"rule": rule, "measure": measure, "sign": sign, "style": s, "scenario": sc, "map": "both",
                          **test(j["x"].to_numpy(), j["y"].to_numpy(), sign)})
    with_holm(tests)
    per_rule = verdicts(tests)
    counts = {rule: int(((fixed["rules"] == rule) & (fixed["onset"] <= LAST_ONSET)).sum()) for rule in RULES}
    return {"tests": tests, "per_rule": per_rule, "met": all(r["met"] for r in per_rule.values()),
            "episodes_with_rule_first": counts}


def identity_checks(bins: pd.DataFrame | None, bc: pd.DataFrame | None) -> list[str]:
    out = []
    key = ["map", "episode", "bin"]
    cols = COUNTS + WEIGHTS

    def same(x: pd.DataFrame, y: pd.DataFrame, label: str) -> None:
        x = x.sort_values(key).reset_index(drop=True)
        y = y.sort_values(key).reset_index(drop=True)
        ok = (len(x) == len(y) and len(x) > 0 and x[key].equals(y[key])
              and np.allclose(x[cols].to_numpy(float), y[cols].to_numpy(float), rtol=0, atol=1e-9))
        out.append(f"{label}: {'identical' if ok else 'DIFFERENT'} ({len(x)} bins)")

    if bins is not None:
        pre = bins[bins["bin"] < 8]
        for cond in bins["condition"].unique():
            for sch in ("abrupt", "gradual"):
                same(pre[(pre["condition"] == cond) & (pre["schedule"] == sch)],
                     pre[(pre["condition"] == cond) & (pre["schedule"] == "none")], f"{cond}: steps 1-200, {sch} vs none")
        none = bins[bins["schedule"] == "none"]
        for group in SAME_BASE:
            for cond in group[1:]:
                same(none[none["condition"] == cond], none[none["condition"] == group[0]],
                     f"unchanged runs: {cond} vs {group[0]}")
        if bc is not None:
            fixed = bc[bc["schedule"] == "fixed"]
            for cond, (s, sc) in OPEN_CLOSED.items():
                same(none[none["condition"] == cond], fixed[(fixed["style"] == s) & (fixed["scenario"] == sc)],
                     f"unchanged {cond} vs closed-loop fixed {s} {sc}")
    if bc is not None:
        o = onset_table(bc).pivot_table(index=["style", "scenario", "map", "episode"], columns="schedule",
                                        values="onset", aggfunc="first")
        o = o.dropna(how="all")
        agree = (o.nunique(axis=1, dropna=False) == 1).all() if len(o) else False
        out.append(f"closed loop: first active bin {'identical' if agree else 'DIFFERENT'} across the three "
                   f"schedules ({len(o)} episodes with an activation)")
    return out


def fmt_p(p: float) -> str:
    return "<0.001" if p < 0.001 else f"{p:.3f}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    args = ap.parse_args()
    d = Path(args.dir)
    rng = np.random.default_rng(SEED)
    res: dict = {"alpha": ALPHA, "margin": MARGIN, "boot": BOOT, "seed": SEED,
                 "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
                              "pandas": pd.__version__}}
    md = [f"# Round v13, Part WA: weight adaptation ({d.name})", ""]
    bins = pd.read_csv(d / "bins_step.csv") if (d / "bins_step.csv").exists() else None
    bc = pd.read_csv(d / "bins_closed.csv") if (d / "bins_closed.csv").exists() else None
    res["identity_checks"] = identity_checks(bins, bc)
    md += ["## Identity checks (same runs by construction)", ""] + [f"- {x}" for x in res["identity_checks"]] + [""]
    if bins is not None:
        res["WA-H1"], res["WA-H2"], res["WA-H3"] = wa_h1(bins), wa_h2(bins, rng), wa_h3(bins, rng)
        h1, h2, h3 = res["WA-H1"], res["WA-H2"], res["WA-H3"]
        md += ["## WA-H1 late window (steps 351-550) against the unchanged run", "",
               "| rule | measure | schedule | map | changed | unchanged | r | p_Holm |", "|---|---|---|---|---|---|---|---|"]
        md += [f"| {t['rule']} | {t['measure']} | {t['schedule']} | {t['map']} | {t['mean_x']:.3f} | {t['mean_y']:.3f} | "
               f"{t['r']:.2f} | {fmt_p(t['p_holm'])} |" for t in h1["tests"]]
        md += ["", "WA-H1 per rule: " + ", ".join(f"{k} {'met' if v else 'not met'}" for k, v in h1["met_per_rule"].items()),
               "", "## WA-H2 gradual against abrupt", "", "First window (201-225), gradual against abrupt:", "",
               "| rule | measure | map | gradual | abrupt | r | p_Holm |", "|---|---|---|---|---|---|---|"]
        md += [f"| {t['rule']} | {t['measure']} | {t['map']} | {t['mean_x']:.3f} | {t['mean_y']:.3f} | {t['r']:.2f} | "
               f"{fmt_p(t['p_holm'])} |" for t in h2["first"]]
        md += ["", "Late window: gradual at least half-way from unchanged to abrupt, contrast "
               "s * (gradual - abrupt/2 - unchanged/2) (ratio for reference):", "",
               "| rule | measure | map | unchanged | abrupt | gradual | contrast | 95% CI | ratio | CI low >= 0 |",
               "|---|---|---|---|---|---|---|---|---|---|"]
        md += [f"| {t['rule']} | {t['measure']} | {t['map']} | {t['mean_unchanged']:.3f} | {t['mean_abrupt']:.3f} | "
               f"{t['mean_gradual']:.3f} | {t['contrast']:.4f} | [{t['ci'][0]:.4f}, {t['ci'][1]:.4f}] | "
               f"{t['ratio']:.2f} | {'yes' if t['ok'] else 'no'} |" for t in h2["late"]]
        md += ["", f"WA-H2 first window {'met' if h2['met_first'] else 'not met'}, late window "
               f"{'met' if h2['met_late'] else 'not met'}.", "", "## WA-H3 goal switches per 100 agent-steps", "",
               "| rule | map | comparison | first | reference | r | p_Holm |", "|---|---|---|---|---|---|---|"]
        md += [f"| {t['rule']} | {t['map']} | {t['comparison']} | {t['mean_x']:.2f} | {t['mean_y']:.2f} | {t['r']:.2f} | "
               f"{fmt_p(t['p_holm'])} |" for t in h3["burst"]]
        md += ["", "Late window (351-550), switches per 100 agent-steps (reported):", "",
               "| rule | map | unchanged | abrupt | gradual |", "|---|---|---|---|---|"]
        md += [f"| {t['rule']} | {t['map']} | {t['none']:.2f} | {t['abrupt']:.2f} | {t['gradual']:.2f} |"
               for t in h3["late"]]
        md += ["", "No burst (abrupt against unchanged), steps 201-250:", "",
               "| rule | map | changed | unchanged | difference | 95% CI | below MARGIN |", "|---|---|---|---|---|---|---|"]
        md += [f"| {t['rule']} | {t['map']} | {t['mean_x']:.2f} | {t['mean_y']:.2f} | {t['mean_diff']:.2f} | "
               f"[{t['ci'][0]:.2f}, {t['ci'][1]:.2f}] | {'yes' if t['ok'] else 'no'} |" for t in h3["route"]]
        md += ["", f"WA-H3 bursts {'met' if h3['met_burst'] else 'not met'}, no burst "
               f"{'met' if h3['met_route'] else 'not met'}.", "", "## Time courses (means per 25-step bin)", ""]
        for cond, measures in DESCRIBE.items():
            for measure in measures:
                num, den, f = RATIOS[measure]
                g = bins[bins["condition"] == cond].groupby(["schedule", "bin"])[[num, den]].sum()
                s = (f * g[num] / g[den].replace(0, np.nan)).unstack("bin")
                md += [f"{cond} {measure}: " + "; ".join(
                    f"{sch} " + " ".join(f"{x:.2f}" for x in s.loc[sch].to_numpy()) for sch in s.index), ""]
    if (d / "episodes_closed.csv").exists():
        e = pd.read_csv(d / "episodes_closed.csv")
        res["WA-H4a"] = h4 = wa_h4a(e)
        md += ["## WA-H4(a) closed loop: measure on the active steps, gradual against fixed (shadow triggers)", "",
               "The active steps are selected by each run's own triggers (see the protocol); maps pooled.", "",
               "| rule | measure | style | scenario | map | n | gradual | fixed | r | p_Holm |",
               "|---|---|---|---|---|---|---|---|---|---|"]
        md += [f"| {t['rule']} | {t['measure']} | {t['style']} | {t['scenario']} | {t['map']} | {t['n']} | "
               f"{t['mean_x']:.3f} | {t['mean_y']:.3f} | {t['r']:.2f} | {fmt_p(t['p_holm'])} |" for t in h4["tests"]]
        md += ["", "WA-H4(a) per rule: " + ", ".join(
            f"{k} {v['significant']}/{v['cells']} cells" + (" met" if v["met"] else " not met")
            for k, v in h4["per_rule"].items()), "", "Per map (reference): " + "; ".join(
            f"{t['rule']} {t['style']} {t['scenario']} {t['map']} n {t['n']} "
            + (f"{t['gradual']:.3f}/{t['fixed']:.3f}" if t["n"] else "-") for t in h4["per_map"]), ""]
        if bc is not None:
            res["WA-H4b"] = h4b = wa_h4b(bc)
            md += [f"## WA-H4(b) onset-locked: bins onset+1 ... onset+{ONSET_BINS} after the first activation "
                   "(the rule alone in the onset bin), gradual against fixed", "",
                   "| rule | measure | style | scenario | map | n | gradual | fixed | r | p_Holm |",
                   "|---|---|---|---|---|---|---|---|---|---|"]
            md += [f"| {t['rule']} | {t['measure']} | {t['style']} | {t['scenario']} | {t['map']} | {t['n']} | "
                   f"{t['mean_x']:.3f} | {t['mean_y']:.3f} | {t['r']:.2f} | {fmt_p(t['p_holm'])} |"
                   for t in h4b["tests"]]
            md += ["", "WA-H4(b) per rule: " + ", ".join(
                f"{k} {v['significant']}/{v['cells']} cells" + (" met" if v["met"] else " not met")
                for k, v in h4b["per_rule"].items()),
                "Episodes (both maps, all styles and scenarios, fixed run) whose first active bin holds the rule alone: "
                + ", ".join(f"{k} {v}" for k, v in h4b["episodes_with_rule_first"].items()), ""]
        md += ["### Activity and outcomes per episode (means)", "",
            "| style | scenario | schedule | R1 | R2 | R3 | R4 | switches/100 | kills/100 | deaths/100 | points own - opp |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
        for (s, sc, sch), g in e.groupby(["style", "scenario", "schedule"], sort=False):
            t = g.sum(numeric_only=True)
            md.append(f"| {s} | {sc} | {sch} | " + " | ".join(f"{t[f'{r}_active_steps'] / t['steps']:.2f}"
                                                              for r in ("R1", "R2", "R3", "R4"))
                      + f" | {100 * t['switches'] / t['alive']:.2f} | {100 * t['kills'] / t['alive']:.2f} | "
                      f"{100 * t['deaths'] / t['alive']:.2f} | {(t['pts_own'] - t['pts_opp']) / len(g):.1f} |")
    (d / "summary.md").write_text("\n".join(md) + "\n")
    (d / "summary.json").write_text(json.dumps(res, indent=1, default=float))
    print("\n".join(md))


if __name__ == "__main__":
    main()
