"""Round v13, Part FV analysis: the pre-registered tests of the form variants (FAMILY_ADAPT_PLAN_V13_*.md, §5-§6).

Reads rows_a.csv, rows_b.csv and rows_c.csv of run_form_variants.py (one directory) and writes summary.md and
summary.json there. Episodes of different conditions with the same map, scenario and episode number share their seed
(common random numbers), so every comparison is paired by episode.
  FV-H1  style separability: for the main model, each of the six distance transforms (part a) and the matched-dwell
         style set (part c), the four styles are classified from the H1 signature metrics (analyze_hypotheses.classify:
         5-fold cross-validated logistic regression, N_PERM permutations) in each map x scenario; a set keeps the
         styles apart if each of its accuracies is >= ACC_MIN with permutation p_Holm < ALPHA (Holm over the set's six
         cells, as for H1 in the report), over the cells in which the main model on the same seeds reaches MAIN_MIN
         (a cell below it is uninformative for every set); met if every set other than the main model keeps them apart.
         Reported with it: which style is highest or lowest on key signature metrics (ORDERING), against the main model
  FV-H2  distance scale: in Mission, the far-objective share of FAR_STYLES rises with the half-distance h within each
         shape (Page's trend test, episodes as blocks; inverse h = 1, 4, 8, 16, exp h = 4, 8, 16), and at the matched
         h in H_STEEP the exp shape is below the inverse one (one-sided paired Wilcoxon); p_Holm < ALPHA per family
  FV-H3  dwell time (Mission-Cooperation, part b): goal switches fall with N = 0, 2, 5, 10, 20, 40 (Page's trend test)
         and each N in DWELL_BELOW is below N = 0 (one-sided paired Wilcoxon), in every map x scenario; p_Holm < ALPHA
  FV-H4  dwell vs penalty at matched switching (part c): the predictions of FV4 (style, scenario, measure, sign)
         against the main model, one-sided paired Wilcoxon, p_Holm < ALPHA
Also reported (not tested): means per condition, the switching rates of the matched dwell against the main model,
the penalty and dwell curves of part b, and the identity checks (part a's and part c's main rows, part b's
w_commitment = 0.45 rows and part a's Mission-Cooperation main rows must be identical: same policy, same seeds).
Usage: python experiments/analyze_form_variants.py --dir ../repro_outputs/v13_family [--perm 1000]
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_hypotheses import classify  # noqa: E402
from analyze_stats import holm, wilcoxon_paired  # noqa: E402

ALPHA = 0.05
N_PERM = 1000
ACC_MIN = 0.60                      # FV-H1 (fixed in the protocol from the pilot)
MAIN_MIN = 0.65                     # FV-H1: cells in which the main model is below this are uninformative
FAR_STYLES = ["MC", "PO"]           # FV-H2
H_STEEP = [4]                       # FV-H2: matched h at which exp < inverse is predicted
DWELLS = [0, 2, 5, 10, 20, 40]      # FV-H3 (N = 0 is the w_commitment = 0 condition pen_0.00)
DWELL_BELOW = [2, 5, 10, 20, 40]    # FV-H3: N predicted below N = 0 in every map x scenario
FV4 = [(s, "Deathmatch", col, sign) for s in ("MC", "PO")      # FV-H4: (style, scenario, measure, predicted sign
       for col, sign in (("engagement_redirection_rate_per_100", +1),  # of matched dwell - main model)
                         ("resource_goal_share_good", -1), ("retreat_share", -1))]
STYLES = ["MC", "PO", "Agg", "SA"]
SCENARIOS = ["Mission", "Deathmatch", "Control"]
MAPS = ["random", "urban"]
TRANSFORM_SETS = ["main", "inv_h4", "inv_h8", "inv_h16", "exp_h4", "exp_h8", "exp_h16"]
SHAPES = {"inverse": ["main", "inv_h4", "inv_h8", "inv_h16"], "exp": ["exp_h4", "exp_h8", "exp_h16"]}
KEY = ["map", "scenario", "episode"]
ORDERING = {"Mission": [("objective_commitment_ratio", "max"), ("avg_ally_proximity", "min")],   # (metric, extreme)
            "Deathmatch": [("engagement_redirection_rate_per_100", "max"), ("resource_seeking_rate_per_100", "max")],
            "Control": [("control_score", "max"), ("avg_ally_proximity", "min")]}


def load(d: Path, part: str) -> pd.DataFrame | None:
    p = d / f"rows_{part}.csv"
    if not p.exists():
        return None
    df = pd.read_csv(p)
    for c in df.columns:
        if c not in ("part", "style", "variant", "map", "scenario"):
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def one_sided(p_two: float, effect: float, sign: int) -> float:
    """One-sided p from a two-sided p and the sign of the effect (as in analyze_map_confirmation.py)."""
    return p_two / 2 if effect * sign > 0 else 1 - p_two / 2


def paired(df: pd.DataFrame, a: dict, b: dict, col: str) -> tuple[np.ndarray, np.ndarray]:
    """Values of col for the conditions a and b (column filters), matched by map, scenario and episode."""
    x = df.loc[np.logical_and.reduce([df[k] == v for k, v in a.items()])].set_index(KEY)[col]
    y = df.loc[np.logical_and.reduce([df[k] == v for k, v in b.items()])].set_index(KEY)[col]
    j = pd.concat([x.rename("x"), y.rename("y")], axis=1, join="inner").dropna()
    return j["x"].to_numpy(), j["y"].to_numpy()


def wilcoxon_one_sided(x: np.ndarray, y: np.ndarray, sign: int) -> dict:
    w = wilcoxon_paired(x, y)
    diff = float(np.mean(x - y)) if len(x) else float("nan")
    return {**w, "mean_x": float(np.mean(x)) if len(x) else None, "mean_y": float(np.mean(y)) if len(y) else None,
            "mean_diff": diff, "p_one": one_sided(w["p"], w["r"] if w["r"] else diff, sign)}


def page(df: pd.DataFrame, order: list, filt: dict, col: str) -> dict:
    """Page's trend test for col rising along order (conditions in the variant column), episodes as blocks."""
    sub = df.loc[np.logical_and.reduce([df[k] == v for k, v in filt.items()]) & df["variant"].isin(order)]
    wide = sub.pivot_table(index=KEY, columns="variant", values=col, aggfunc="first")[order].dropna()
    if len(wide) < 2:
        return {"n_blocks": int(len(wide)), "L": None, "p": 1.0, "means": {}}
    res = stats.page_trend_test(wide.to_numpy())
    return {"n_blocks": int(len(wide)), "L": float(res.statistic), "p": float(res.pvalue),
            "means": {v: float(wide[v].mean()) for v in order}}


def with_holm(tests: list[dict], key: str = "p") -> list[dict]:
    adj = holm([t[key] for t in tests]) if tests else []
    for t, pa in zip(tests, adj):
        t["p_holm"] = pa
    return tests


def fv_h1(a: pd.DataFrame, c: pd.DataFrame | None, n_perm: int) -> dict:
    sets = [("a", v, a[a["variant"] == v]) for v in TRANSFORM_SETS]
    if c is not None:
        sets.append(("c", "dwell_matched", c[c["variant"] == "dwell_matched"]))
    tests = []
    for part, v, d in sets:
        cells = []
        for m in MAPS:
            for sc in SCENARIOS:
                dm = d[(d["map"] == m) & (d["scenario"] == sc)]
                if dm.groupby("style").size().min() < 5:      # 5-fold cross-validation (smoke tests only)
                    r = {"accuracy": float("nan"), "p": 1.0, "chance": 0.25, "n": int(len(dm))}
                else:
                    r = classify(d[d["map"] == m], sc, n_perm=n_perm)
                cells.append({"part": part, "set": v, "map": m, "scenario": sc, **r})
        tests += with_holm(cells)
    main_acc = {(t["map"], t["scenario"]): t["accuracy"] for t in tests if t["set"] == "main"}
    informative = {k for k, acc in main_acc.items() if acc >= MAIN_MIN}
    verdict = {}
    for part, v, _ in sets:
        cells = [t for t in tests if t["set"] == v and (t["map"], t["scenario"]) in informative]
        verdict[v] = bool(cells) and all(t["accuracy"] >= ACC_MIN and t["p_holm"] < ALPHA for t in cells)
    return {"tests": tests, "met_per_set": verdict, "uninformative_cells": sorted(set(main_acc) - informative),
            "met": all(ok for v, ok in verdict.items() if v != "main")}


def ordering(a: pd.DataFrame, c: pd.DataFrame | None) -> list[dict]:
    """Per set, map and scenario: the style with the highest (lowest) mean of ORDERING's metrics, and whether it is
    the main model's (reported, not tested)."""
    frames = [a] + ([c[c["variant"] == "dwell_matched"]] if c is not None else [])
    d = pd.concat(frames)
    out = []
    for sc, metrics in ORDERING.items():
        for col, how in metrics:
            g = d[d["scenario"] == sc].groupby(["variant", "map", "style"])[col].mean()
            for m in MAPS:
                ref = g.xs(("main", m), level=("variant", "map"))
                ref_style = ref.idxmax() if how == "max" else ref.idxmin()
                for v in d["variant"].unique():
                    x = g.xs((v, m), level=("variant", "map"))
                    st = x.idxmax() if how == "max" else x.idxmin()
                    out.append({"set": v, "map": m, "scenario": sc, "metric": col, "extreme": how, "style": st,
                                "main_style": ref_style, "same": bool(st == ref_style)})
    return out


def fv_h2(a: pd.DataFrame) -> dict:
    trend = []
    for s in FAR_STYLES:
        for m in MAPS:
            for shape, order in SHAPES.items():
                r = page(a, order, {"style": s, "map": m, "scenario": "Mission"}, "far_objective_share")
                trend.append({"style": s, "map": m, "shape": shape, **r})
    with_holm(trend)
    steep = []
    for s in FAR_STYLES:
        for m in MAPS:
            for h in H_STEEP:
                x, y = paired(a[(a["style"] == s) & (a["map"] == m) & (a["scenario"] == "Mission")],
                              {"variant": f"exp_h{h}"}, {"variant": f"inv_h{h}"}, "far_objective_share")
                steep.append({"style": s, "map": m, "h": h, **wilcoxon_one_sided(x, y, -1)})
    with_holm(steep, "p_one")
    return {"trend": trend, "steep": steep,
            "met_trend": all(t["p_holm"] < ALPHA and t["L"] is not None for t in trend),
            "met_steep": all(t["p_holm"] < ALPHA for t in steep)}


def fv_h3(b: pd.DataFrame) -> dict:
    label = {0: "pen_0.00", **{n: f"dwell_{n}" for n in DWELLS if n}}
    order = [label[n] for n in reversed(DWELLS)]          # Page's test for a rise: switches rise as N falls
    trend, below = [], []
    for m in MAPS:
        for sc in SCENARIOS:
            trend.append({"map": m, "scenario": sc,
                          **page(b, order, {"map": m, "scenario": sc}, "goal_switch_rate_per_100")})
            for n in DWELL_BELOW:
                x, y = paired(b[(b["map"] == m) & (b["scenario"] == sc)], {"variant": label[n]},
                              {"variant": "pen_0.00"}, "goal_switch_rate_per_100")
                below.append({"map": m, "scenario": sc, "N": n, **wilcoxon_one_sided(x, y, -1)})
    for t in below:
        t["p"] = t["p_one"]
    tests = with_holm(trend + below)
    return {"trend": trend, "below": below, "met": all(t["p_holm"] < ALPHA for t in tests)}


def fv_h4(c: pd.DataFrame) -> dict:
    tests = []
    for s, sc, col, sign in FV4:
        for m in MAPS:
            x, y = paired(c[(c["style"] == s) & (c["map"] == m) & (c["scenario"] == sc)],
                          {"variant": "dwell_matched"}, {"variant": "main"}, col)
            tests.append({"style": s, "scenario": sc, "measure": col, "sign": sign, "map": m,
                          **wilcoxon_one_sided(x, y, sign)})
    with_holm(tests, "p_one")
    return {"tests": tests, "met": all(t["p_holm"] < ALPHA for t in tests)}


def identity_checks(a, b, c) -> list[str]:
    out = []
    cols = [col for col in a.columns if col not in ("part", "variant", "style")]

    def same(x: pd.DataFrame, y: pd.DataFrame, label: str) -> None:
        x = x.sort_values(KEY)[cols].reset_index(drop=True)
        y = y.sort_values(KEY)[cols].reset_index(drop=True)
        ok = len(x) == len(y) and len(x) > 0 and x.equals(y)
        out.append(f"{label}: {'identical' if ok else 'DIFFERENT'} ({len(x)} rows)")

    if c is not None:
        for s in STYLES:
            same(a[(a["style"] == s) & (a["variant"] == "main")], c[(c["style"] == s) & (c["variant"] == "main")],
                 f"part a main vs part c main, {s}")
    if b is not None:
        same(a[(a["style"] == "MC") & (a["variant"] == "main")], b[b["variant"] == "pen_0.45"],
             "part a MC main vs part b w_commitment 0.45")
    return out


def means_table(df: pd.DataFrame, by: list, cols: list) -> list[str]:
    g = df.groupby(by, sort=False)[cols].mean()
    lines = ["| " + " | ".join(by + cols) + " |", "|" + "---|" * (len(by) + len(cols))]
    for k, r in g.iterrows():
        k = k if isinstance(k, tuple) else (k,)
        lines.append("| " + " | ".join(map(str, k)) + " | "
                     + " | ".join("" if pd.isna(r[c]) else f"{r[c]:.3f}" for c in cols) + " |")
    return lines


def fmt_p(p: float) -> str:
    return "<0.001" if p < 0.001 else f"{p:.3f}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--perm", type=int, default=N_PERM)
    args = ap.parse_args()
    d = Path(args.dir)
    a, b, c = load(d, "a"), load(d, "b"), load(d, "c")
    import scipy
    import sklearn
    res: dict = {"alpha": ALPHA, "acc_min": ACC_MIN, "main_min": MAIN_MIN, "n_perm": args.perm,
                 "versions": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
                              "pandas": pd.__version__, "sklearn": sklearn.__version__}}
    md = [f"# Round v13, Part FV: form variants ({d.name})", ""]
    if a is not None:
        res["FV-H1"] = fv_h1(a, c, args.perm)
        res["FV-H2"] = fv_h2(a)
        h1, h2 = res["FV-H1"], res["FV-H2"]
        md += ["## FV-H1 style separability (accuracy, permutation p_Holm)", "",
               "| set | " + " | ".join(f"{m} {sc}" for m in MAPS for sc in SCENARIOS) + " | kept apart |",
               "|---|" + "---|" * (len(MAPS) * len(SCENARIOS) + 1)]
        for v, ok in h1["met_per_set"].items():
            cells = [t for t in h1["tests"] if t["set"] == v]
            md.append(f"| {v} | " + " | ".join(f"{t['accuracy']:.2f} ({fmt_p(t['p_holm'])})" for t in cells)
                      + f" | {'yes' if ok else 'no'} |")
        res["ordering"] = order = ordering(a, c)
        md += ["", f"Cells in which the main model is below {MAIN_MIN} (uninformative for every set): "
               + (", ".join(f"{m} {sc}" for m, sc in h1["uninformative_cells"]) or "none"),
               "", f"FV-H1 {'met' if h1['met'] else 'not met'} (every variant set kept apart; ACC_MIN {ACC_MIN}).", "",
               "### Ordering (reported): style with the highest or lowest mean, same as the main model?", "",
               "| set | " + " | ".join(f"{m} {sc} {col.split('_')[0]} {how}" for sc, ms in ORDERING.items()
                                     for col, how in ms for m in MAPS) + " |",
               "|---|" + "---|" * sum(len(ms) * len(MAPS) for ms in ORDERING.values())]
        for v in dict.fromkeys(t["set"] for t in order):
            row = [t for t in order if t["set"] == v]
            md.append(f"| {v} | " + " | ".join(f"{t['style']}{'' if t['same'] else ' (≠)'}" for t in row) + " |")
        md += ["",
               "## FV-H2 far-objective share in Mission (Page's trend over h; exp vs inverse at matched h)", "",
               "| style | map | shape | means along h | L | p_Holm |", "|---|---|---|---|---|---|"]
        for t in h2["trend"]:
            md.append(f"| {t['style']} | {t['map']} | {t['shape']} | "
                      + ", ".join(f"{k} {v:.3f}" for k, v in t["means"].items())
                      + f" | {t['L'] if t['L'] is None else round(t['L'], 1)} | {fmt_p(t['p_holm'])} |")
        md += ["", "| style | map | h | exp | inverse | r | p_Holm (exp < inverse) |", "|---|---|---|---|---|---|---|"]
        for t in h2["steep"]:
            md.append(f"| {t['style']} | {t['map']} | {t['h']} | {t['mean_x']:.3f} | {t['mean_y']:.3f} | "
                      f"{t['r']:.2f} | {fmt_p(t['p_holm'])} |")
        md += ["", f"FV-H2 trend {'met' if h2['met_trend'] else 'not met'}; "
               f"exp below inverse at h in {H_STEEP} {'met' if h2['met_steep'] else 'not met'}.", ""]
        md += ["## Means per condition (part a)", ""]
        for sc in SCENARIOS:
            md += [f"### {sc}", ""] + means_table(a[a["scenario"] == sc], ["style", "variant"], [
                "objective_commitment_ratio", "far_objective_share", "goal_switch_rate_per_100",
                "engagement_redirection_rate_per_100", "retreat_share", "share_teammate", "kill_rate_per_100",
                "death_rate_per_100", "control_score"]) + [""]
    if b is not None:
        res["FV-H3"] = fv_h3(b)
        h3 = res["FV-H3"]
        md += ["## FV-H3 dwell time, Mission-Cooperation (goal switches per 100 steps)", "",
               "| map | scenario | means N = " + ", ".join(map(str, reversed(DWELLS))) + " | p_Holm (trend) |",
               "|---|---|---|---|"]
        for t in h3["trend"]:
            md.append(f"| {t['map']} | {t['scenario']} | " + ", ".join(f"{v:.2f}" for v in t["means"].values())
                      + f" | {fmt_p(t['p_holm'])} |")
        md += ["", "| map | scenario | N | N | N = 0 | r | p_Holm |", "|---|---|---|---|---|---|---|"]
        for t in h3["below"]:
            md.append(f"| {t['map']} | {t['scenario']} | {t['N']} | {t['mean_x']:.2f} | {t['mean_y']:.2f} | "
                      f"{t['r']:.2f} | {fmt_p(t['p_holm'])} |")
        b = b.assign(win=np.where(b["scenario"] == "Control", (b["control_score"] >= 120).astype(float), np.nan))
        md += ["", f"FV-H3 {'met' if h3['met'] else 'not met'}.", "",
               "### Penalty and dwell curves (part b, means over maps)", ""]
        for sc in SCENARIOS:
            md += [f"#### {sc}", ""] + means_table(b[b["scenario"] == sc], ["variant"], [
                "goal_switch_rate_per_100", "objective_commitment_ratio", "engagement_redirection_rate_per_100",
                "retreat_share", "share_teammate", "idle_item_chain_rate_per_100", "win"]) + [""]
    if c is not None:
        res["FV-H4"] = fv_h4(c)
        h4 = res["FV-H4"]
        md += ["## FV-H4 matched dwell vs penalty (part c)", "",
               "| style | scenario | measure | map | dwell | main | r | p_Holm |", "|---|---|---|---|---|---|---|---|"]
        for t in h4["tests"]:
            md.append(f"| {t['style']} | {t['scenario']} | {t['measure']} | {t['map']} | {t['mean_x']:.3f} | "
                      f"{t['mean_y']:.3f} | {t['r']:.2f} | {fmt_p(t['p_holm'])} |")
        md += ["", f"FV-H4 {'met' if h4['met'] else 'not met'}.", "", "### Means, matched dwell vs main (part c)", ""]
        for sc in SCENARIOS:
            md += [f"#### {sc}", ""] + means_table(c[c["scenario"] == sc], ["style", "variant"], [
                "goal_switch_rate_per_100", "objective_commitment_ratio", "engagement_redirection_rate_per_100",
                "retreat_share", "resource_goal_share_good", "idle_item_chain_rate_per_100", "share_teammate",
                "control_score"]) + [""]
    if a is not None:
        res["identity_checks"] = identity_checks(a, b, c)
        md += ["## Identity checks (same policy, same seeds)", ""] + [f"- {x}" for x in res["identity_checks"]] + [""]
    (d / "summary.md").write_text("\n".join(md) + "\n")
    (d / "summary.json").write_text(json.dumps(res, indent=1, default=float))
    print("\n".join(md))


if __name__ == "__main__":
    main()
