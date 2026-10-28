"""Statistical summary of the route-metric experiment (one map directory).

Expects in --dir: results.csv, lambda_scale.csv, route_metric.csv (run_route_metric.py).
Writes route_metric_summary.md / route_metric_summary.json into --dir.

  1. route diagnostics per variant and scale k, pooled over the evaluated team's plans:
     detour rate (planned path longer than the shortest path), share of plans differing from
     the shortest path, planned / shortest length, and exposure along planned / shortest paths
  2. dose-response in the two representative conditions (Deathmatch / Survival-Aware,
     Mission / Mission-Cooperation): Spearman rho between k and each metric, and paired
     Wilcoxon tests of k = 1, 3, 10 against k = 0 (Holm within each variant and metric)
  3. every variant against the additive cost at the same k, all conditions (paired Wilcoxon,
     Holm within each condition, variant, and k)
  4. style signatures per variant and k (Kruskal-Wallis epsilon^2 as for H1; Control wins)

Usage:
  python experiments/analyze_route_metric.py --dir ../repro_outputs
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_stats import (METRICS, SCENARIOS, STYLES, check_same, control_outcomes, fmt, fmt_p,  # noqa: E402
                           holm, load, mean_ci, wilcoxon_paired)
from analyze_hypotheses import kruskal  # noqa: E402

VARIANTS = ["additive", "centred", "exp", "exp_geo", "exp_geo_replan", "additive_replan"]
REP = [("Deathmatch", "Survival-Aware", ["engagement_redirection_rate_per_100", "deaths", "avg_ally_proximity",
                                         "resource_seeking_rate_per_100", "kills"]),
       ("Mission", "Mission–Cooperation", ["avg_ally_proximity", "objective_commitment_ratio", "deaths"])]
KEY = {"Mission": ["objective_commitment_ratio", "avg_ally_proximity", "engagement_redirection_rate_per_100", "deaths"],
       "Deathmatch": ["engagement_redirection_rate_per_100", "resource_seeking_rate_per_100", "avg_ally_proximity", "deaths"],
       "Control": ["control_score", "objective_commitment_ratio", "avg_ally_proximity", "deaths"]}
SIGNATURE = [("Mission", "objective_commitment_ratio"), ("Mission", "avg_ally_proximity"),
             ("Deathmatch", "engagement_redirection_rate_per_100"), ("Deathmatch", "resource_seeking_rate_per_100"),
             ("Control", "control_score")]



def _native(obj):
    """Recursively convert numpy scalar keys/values to native Python types for json.dump
    (pandas >= 3 / numpy >= 2 yield numpy.int64 group keys)."""
    import numpy as _np
    if isinstance(obj, dict):
        return {(_k.item() if isinstance(_k, _np.generic) else _k): _native(_v) for _k, _v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_native(x) for x in obj]
    if isinstance(obj, _np.generic):
        return obj.item()
    return obj

def diag(g: pd.DataFrame) -> dict:
    n = g["n_plans"].sum()
    return {"plans": int(n), "detour": float(g["n_detour"].sum() / n) if n else float("nan"),
            "differs": float(g["n_differs"].sum() / n) if n else float("nan"),
            "len_ratio": float(g["sum_len"].sum() / g["sum_len0"].sum()),
            "exp_ratio": float(g["sum_exp"].sum() / g["sum_exp0"].sum())}


def add_ratios(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["detour_rate"] = df["n_detour"] / df["n_plans"].where(df["n_plans"] > 0)
    df["exposure_ratio"] = df["sum_exp"] / df["sum_exp0"].where(df["sum_exp0"] > 0)
    return df


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", type=str, required=True)
    p.add_argument("--model", type=str, default="exp", choices=["exp", "additive"],
                   help="Main model of the directory: exp (v3; no variant equals it) or additive (v2: variant additive x1 equals the main experiment)")
    args = p.parse_args()
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from fps_priority_ai.runner import EXP_MODEL_SCALE
    d = Path(args.dir)
    main_df, lam = load(d / "results.csv"), load(d / "lambda_scale.csv")
    rm = add_ratios(load(d / "route_metric.csv"))
    scales = sorted(rm["lambda_scale"].unique())
    ks = [k for k in scales if k != 0]
    main_variant, main_k = ("exp", EXP_MODEL_SCALE) if args.model == "exp" else ("additive", 1)
    S: dict = {}
    md = [f"# Route metric: statistical summary ({'urban' if d.name == 'urban' else 'random'} map)\n"]

    # ---------------- consistency (common random numbers) ----------------
    sel = lambda v, k: rm[(rm["variant"] == v) & (rm["lambda_scale"] == k)]
    if not sel(main_variant, main_k).empty:    # only when the main model is a member of the variant family (v2)
        for (sc, st), g in sel(main_variant, main_k).groupby(["scenario", "style"]):
            check_same(g, main_df[(main_df["scenario"] == sc) & (main_df["style"] == st)], f"{main_variant} x{main_k} {sc}/{st}")
    for v in ["centred", "exp", "exp_geo"]:
        for (sc, st), g in sel(v, 0).groupby(["scenario", "style"]):
            ref = sel("additive", 0)
            check_same(g, ref[(ref["scenario"] == sc) & (ref["style"] == st)], f"{v} x0 {sc}/{st}")
    for (sc, st), g in sel("exp_geo_replan", 0).groupby(["scenario", "style"]):
        ref = sel("additive_replan", 0)
        check_same(g, ref[(ref["scenario"] == sc) & (ref["style"] == st)], f"replan x0 {sc}/{st}")
    for sc, st, _ in REP:
        ref = lam[(lam["scenario"] == sc) & (lam["style"] == st) & (lam["lambda_scale"] == 0)]
        g = sel("additive", 0)
        check_same(g[(g["scenario"] == sc) & (g["style"] == st)], ref, f"additive x0 = lambda_scale x0 {sc}/{st}")
    md.append(f"Consistency checks (CRN): {main_variant} x{main_k} = main experiment; at x0 the additive, centred, exp, and exp_geo "
              "variants coincide (distance-only) and equal the lambda-scale sweep; exp_geo_replan x0 = additive_replan x0. "
              "**passed**\n")

    # ---------------- 1. route diagnostics ----------------
    S["diagnostics"] = {}
    for label, sub in [("all styles", rm), ("Survival-Aware", rm[rm["style"] == "Survival-Aware"]),
                       ("Mission–Cooperation", rm[rm["style"] == "Mission–Cooperation"])]:
        md.append(f"\n## Route diagnostics, {label} (pooled over plans; detour = planned path longer than the shortest)\n")
        md.append("| variant | k | plans | detour | differs | len_ratio | exp_ratio |")
        md.append("|---|---|---|---|---|---|---|")
        for v in VARIANTS:
            for k in scales:
                r = diag(sub[(sub["variant"] == v) & (sub["lambda_scale"] == k)])
                S["diagnostics"][f"{label}|{v}|{k}"] = r
                md.append(f"| {v} | x{k} | {r['plans']} | {100 * r['detour']:.2f}% | {100 * r['differs']:.1f}% | "
                          f"{r['len_ratio']:.3f} | {r['exp_ratio']:.3f} |")

    # ---------------- 2. dose-response ----------------
    S["dose_response"] = {}
    for sc, st, cols in REP:
        md.append(f"\n## Dose-response: {sc} / {st}\n")
        md.append("| variant | k | " + " | ".join(METRICS[c] for c in cols) + " | detour rate | exposure ratio |")
        md.append("|---|---|" + "---|" * (len(cols) + 2))
        g0 = rm[(rm["scenario"] == sc) & (rm["style"] == st)]
        for v in VARIANTS:
            gv = g0[g0["variant"] == v]
            entry = {"means": {}, "spearman": {}, "vs_x0": {}}
            for k in scales:
                gk = gv[gv["lambda_scale"] == k]
                entry["means"][k] = {c: mean_ci(gk[c]) for c in cols + ["detour_rate", "exposure_ratio"]}
                md.append(f"| {v} | x{k} | " + " | ".join(fmt(entry["means"][k][c]) for c in cols) +
                          f" | {fmt(entry['means'][k]['detour_rate'], 3)} | {fmt(entry['means'][k]['exposure_ratio'], 3)} |")
            lines = []
            for c in cols + ["detour_rate", "exposure_ratio"]:
                sub = gv[["lambda_scale", c]].dropna()
                if sub[c].nunique() > 1:
                    rho, pv = stats.spearmanr(sub["lambda_scale"], sub[c])
                    entry["spearman"][c] = {"rho": float(rho), "p": float(pv)}
                x0 = gv[gv["lambda_scale"] == 0].sort_values("episode")[c].values
                tests = [wilcoxon_paired(gv[gv["lambda_scale"] == k].sort_values("episode")[c].values, x0) for k in ks]
                for t, pa in zip(tests, holm([t["p"] for t in tests])):
                    t["p_holm"] = pa
                entry["vs_x0"][c] = dict(zip([f"{k:g}" for k in ks], tests))
                name = METRICS.get(c, c)
                sp = entry["spearman"].get(c)
                lines.append(f"{name}: rho={sp['rho']:+.2f} (p={fmt_p(sp['p'])})" if sp else f"{name}: constant")
                lines[-1] += "; vs x0: " + ", ".join(f"x{k} r={t['r']:+.2f} pH={fmt_p(t['p_holm'])}"
                                                     for k, t in zip(ks, tests))
            md.append("")
            md.append(f"- **{v}**: " + " | ".join(lines))
            md.append("")
            S["dose_response"][f"{sc}|{st}|{v}"] = entry

    # ---------------- 3. variant vs additive at the same k ----------------
    S["vs_additive"] = {}
    md.append("\n## Variants vs additive at the same k (paired Wilcoxon; Holm within condition x variant x k; "
              "listed if p_Holm < 0.05)\n")
    for k in ks:
        md.append(f"\n### k = {k}\n")
        for v in VARIANTS[1:]:
            hits = []
            for sc in SCENARIOS:
                for st in STYLES:
                    a = rm[(rm["variant"] == "additive") & (rm["lambda_scale"] == k) & (rm["scenario"] == sc) &
                           (rm["style"] == st)].sort_values("episode")
                    b = rm[(rm["variant"] == v) & (rm["lambda_scale"] == k) & (rm["scenario"] == sc) &
                           (rm["style"] == st)].sort_values("episode")
                    tests = [wilcoxon_paired(b[c].values, a[c].values) for c in KEY[sc]]
                    for c, t, pa in zip(KEY[sc], tests, holm([t["p"] for t in tests])):
                        t.update({"p_holm": pa, "additive": mean_ci(a[c]), "variant": mean_ci(b[c])})
                        S["vs_additive"][f"{k}|{v}|{sc}|{st}|{METRICS[c]}"] = t
                        if pa < 0.05:
                            hits.append(f"{sc}/{st} {METRICS[c]} {fmt(t['additive'])} -> {fmt(t['variant'])} "
                                        f"(r={t['r']:+.2f}, pH={fmt_p(pa)})")
            md.append(f"- **{v}**: " + ("; ".join(hits) if hits else "no adjusted-significant difference"))

    # ---------------- 4. style signatures ----------------
    S["signatures"] = {}
    md.append("\n## Style signatures per variant (Kruskal-Wallis epsilon^2 across the four styles; Control wins)\n")
    md.append("| variant | k | " + " | ".join(f"{sc} {METRICS[c]}" for sc, c in SIGNATURE) + " | Control wins (MC/PO/Agg/SA) |")
    md.append("|---|---|" + "---|" * (len(SIGNATURE) + 1))
    for v in VARIANTS:
        for k in scales:
            g = rm[(rm["variant"] == v) & (rm["lambda_scale"] == k)]
            eps = [kruskal(g, sc, c)["eps2"] for sc, c in SIGNATURE]
            wins = [control_outcomes(g[(g["scenario"] == "Control") & (g["style"] == st)])["wins"] for st in STYLES]
            S["signatures"][f"{v}|{k}"] = {"eps2": eps, "wins": wins}
            md.append(f"| {v} | x{k} | " + " | ".join(f"{e:.2f}" for e in eps) + " | " + "/".join(map(str, wins)) + " |")

    (d / "route_metric_summary.json").write_text(json.dumps(_native(S), indent=2, ensure_ascii=False, default=float),
                                                 encoding="utf-8")
    (d / "route_metric_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Saved: {(d / 'route_metric_summary.md').resolve()}")


if __name__ == "__main__":
    main()
