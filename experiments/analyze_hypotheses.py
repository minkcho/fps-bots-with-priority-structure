"""Hypothesis tests and effect sizes for H1-H4 (one map directory; no new simulation).

Reads results.csv, sensitivity_commitment.csv, lambda_scale.csv, mode_ablation.csv, and
interpolation.csv from --dir and writes hypotheses_summary.md / hypotheses_summary.json.

Pre-specified primary tests (Holm-adjusted together within the map):
  H1  Kruskal-Wallis across the four styles (effect size epsilon^2) for Mission objective
      commitment, Mission ally distance, Deathmatch engagement redirection, Deathmatch
      resource seeking, and Control score; style classification from episode metrics per
      scenario (5-fold stratified CV logistic regression, permutation test, 1000 perms);
      combat-mode ablation: Survival-Aware resource seeking and Aggressive engagement
      redirection in Deathmatch, full vs weights-only (paired Wilcoxon).
  H2  Mission objective commitment and Control score, w_commit = 0.45 vs 0 (paired Wilcoxon).
  H3  Deathmatch Survival-Aware engagement redirection and Mission Mission-Cooperation ally
      distance, lambda scale 1 vs 0 (paired Wilcoxon).
  H4  Spearman rho between alpha and Mission ally distance (MC -> PO) and Deathmatch
      engagement redirection (Agg -> SA).
Effect sizes: epsilon^2 (Kruskal-Wallis), rank-biserial r / Cliff's delta, Hodges-Lehmann
shift (independent: median of pairwise differences; paired: median of differences) with
percentile bootstrap 95% CIs (2000 resamples, fixed seed), Spearman rho, and CV accuracy.
Secondary pairwise style contrasts (Mann-Whitney, delta, HL with bootstrap CI) are reported
without adjustment.

Usage:
  python experiments/analyze_hypotheses.py --dir ../repro_outputs
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, permutation_test_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_stats import METRICS, SCENARIOS, STYLES, fmt_p, holm, load, mann_whitney, wilcoxon_paired  # noqa: E402

B = 2000
SEED = 0


def hl_independent(a, b, rng):
    a, b = np.asarray(a, float), np.asarray(b, float)
    est = float(np.median(np.subtract.outer(a, b)))
    boots = [np.median(np.subtract.outer(rng.choice(a, len(a)), rng.choice(b, len(b)))) for _ in range(B)]
    return est, float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))


def hl_paired(x, y, rng):
    dlt = np.asarray(x, float) - np.asarray(y, float)
    est = float(np.median(dlt))
    boots = [np.median(rng.choice(dlt, len(dlt))) for _ in range(B)]
    return est, float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))


def kruskal(df, sc, col):
    groups = [df[(df["scenario"] == sc) & (df["style"] == st)][col].astype(float).dropna().values for st in STYLES]
    n, k = sum(len(g) for g in groups), len(groups)
    if all(np.all(g == groups[0][0]) for g in groups):
        return {"H": 0.0, "p": 1.0, "eps2": 0.0}
    h, pv = stats.kruskal(*groups)
    return {"H": float(h), "p": float(pv), "eps2": float(max(0.0, (h - k + 1) / (n - k)))}


def classify(df, sc, n_perm: int = 1000):
    cols = ["objective_commitment_ratio", "engagement_redirection_rate_per_100", "resource_seeking_rate_per_100",
            "avg_ally_proximity", "kills", "deaths"] + (["control_score"] if sc == "Control" else [])
    g = df[df["scenario"] == sc].dropna(subset=cols)
    X, y = g[cols].astype(float).values, g["style"].values
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    acc, _, pv = permutation_test_score(model, X, y, cv=cv, n_permutations=n_perm, random_state=SEED, scoring="accuracy")
    return {"accuracy": float(acc), "p": float(pv), "chance": 1.0 / len(STYLES), "n": int(len(g))}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", type=str, required=True)
    p.add_argument("--map-name", type=str, default=None, help="map name for the title (2026-09-25)")
    p.add_argument("--permutations", type=int, default=1000,
                   help="label permutations of the classification test (confirmation run: 5000)")
    args = p.parse_args()
    d = Path(args.dir)
    main_df, sens = load(d / "results.csv"), load(d / "sensitivity_commitment.csv")
    # (2026-09-25) lambda_scale.csv only feeds the earlier-formulation rows; it is optional (confirmation run)
    lam = load(d / "lambda_scale.csv") if (d / "lambda_scale.csv").exists() else pd.DataFrame()
    mode, interp = load(d / "mode_ablation.csv"), load(d / "interpolation.csv")
    rng = np.random.default_rng(SEED)
    primary = []   # (hypothesis, label, statistic text, effect text, p)
    S: dict = {"primary": [], "secondary_contrasts": [], "classification": {}}

    # ---------------- H1 ----------------
    for sc, col in [("Mission", "objective_commitment_ratio"), ("Mission", "avg_ally_proximity"),
                    ("Deathmatch", "engagement_redirection_rate_per_100"),
                    ("Deathmatch", "resource_seeking_rate_per_100"), ("Control", "control_score")]:
        r = kruskal(main_df, sc, col)
        primary.append(("H1", f"Kruskal-Wallis, {sc} {METRICS[col]}", f"H = {r['H']:.1f}",
                        f"eps2 = {r['eps2']:.2f}", r["p"], r))
    for sc in SCENARIOS:
        r = classify(main_df, sc, args.permutations)
        S["classification"][sc] = r
        primary.append(("H1", f"Style classification, {sc}", f"accuracy = {r['accuracy']:.2f} (chance 0.25)",
                        f"5-fold CV, {args.permutations} permutations", r["p"], r))
    for st, col in [("Survival-Aware", "resource_seeking_rate_per_100"), ("Aggressive", "engagement_redirection_rate_per_100")]:
        full = main_df[(main_df["scenario"] == "Deathmatch") & (main_df["style"] == st)].sort_values("episode")[col].values
        wo = mode[(mode["scenario"] == "Deathmatch") & (mode["style"] == st)].sort_values("episode")[col].values
        w = wilcoxon_paired(full, wo)
        hl = hl_paired(full, wo, rng)
        primary.append(("H1", f"Mode ablation, Deathmatch {st} {METRICS[col]} (full - weights-only)",
                        f"median diff = {hl[0]:+.2f} [{hl[1]:+.2f}, {hl[2]:+.2f}]", f"r = {w['r']:+.2f}", w["p"],
                        {**w, "hl": hl}))

    LBL = {**METRICS, "goal_switch_rate_per_100": "GoalSwitches", "walked_hits_per_step": "WalkedHits",
           "los_frac": "LOSFraction"}
    superseded = []   # earlier formulations of the hypotheses, kept for comparison (not in the Holm family)

    # ---------------- H2 (redefined 2026-09-23: interruption tolerance = goal-switching frequency) ----------------
    for sc, col in [("Mission", "goal_switch_rate_per_100"), ("Control", "goal_switch_rate_per_100")]:
        if col not in sens.columns:
            continue
        a = sens[(sens["scenario"] == sc) & (sens["w_commitment"].round(2) == 0.45)].sort_values("episode")[col].values
        b = sens[(sens["scenario"] == sc) & (sens["w_commitment"] == 0.0)].sort_values("episode")[col].values
        w = wilcoxon_paired(a, b)
        hl = hl_paired(a, b, rng)
        primary.append(("H2", f"{sc} {LBL[col]}, w_commit 0.45 - 0", f"median diff = {hl[0]:+.2f} [{hl[1]:+.2f}, {hl[2]:+.2f}]",
                        f"r = {w['r']:+.2f}", w["p"], {**w, "hl": hl}))
    for sc, col in [("Mission", "objective_commitment_ratio"), ("Control", "control_score")]:
        a = sens[(sens["scenario"] == sc) & (sens["w_commitment"].round(2) == 0.45)].sort_values("episode")[col].values
        b = sens[(sens["scenario"] == sc) & (sens["w_commitment"] == 0.0)].sort_values("episode")[col].values
        w = wilcoxon_paired(a, b)
        hl = hl_paired(a, b, rng)
        superseded.append(("H2 (earlier formulation)", f"{sc} {METRICS[col]}, w_commit 0.45 - 0", f"median diff = {hl[0]:+.2f} [{hl[1]:+.2f}, {hl[2]:+.2f}]",
                           f"r = {w['r']:+.2f}", w["p"], {**w, "hl": hl}))

    # ---------------- H3 (broadened 2026-09-24, after the evade fix; stated as post hoc in the paper) ----------------
    # Primary: in Deathmatch, removing the exposure term (lambda_E = 0, cost-term ablation) raises the walked
    # exposure of every style: full - no_exposure, paired by episode, one test per style; plus a sign test over
    # all 12 scenario x style conditions. The originally pre-specified Survival-Aware lambda-scale tests are
    # reported below as secondary.
    ct_path = d / "cost_term_ablation.csv"
    if ct_path.exists():
        ct = load(ct_path)
        neg = tot = 0
        for sc in SCENARIOS:
            for st in STYLES:
                g = ct[(ct["scenario"] == sc) & (ct["style"] == st)]
                a = g[g["variant"] == "full"].sort_values("episode")["walked_hits_per_step"].values
                b = g[g["variant"] == "no_exposure"].sort_values("episode")["walked_hits_per_step"].values
                if len(a) == 0 or len(a) != len(b):
                    continue
                tot += 1; neg += int(np.mean(a) < np.mean(b))
                if sc == "Deathmatch":
                    w = wilcoxon_paired(a, b)
                    hl = hl_paired(a, b, rng)
                    primary.append(("H3", f"Deathmatch {st} WalkedHits, lambda_E configured - 0",
                                    f"median diff = {hl[0]:+.4f} [{hl[1]:+.4f}, {hl[2]:+.4f}]", f"r = {w['r']:+.2f}", w["p"],
                                    {**w, "hl": hl}))
        if tot:
            pv = float(stats.binomtest(neg, tot, 0.5, alternative="greater").pvalue)
            primary.append(("H3", "Sign test, WalkedHits lower with the exposure term (all scenarios x styles)",
                            f"{neg}/{tot} conditions lower", "one-sided binomial", pv, {"neg": neg, "n": tot, "p": pv}))
    for sc, st, col, fam in [("Deathmatch", "Survival-Aware", "walked_hits_per_step", "superseded"),
                             ("Deathmatch", "Survival-Aware", "los_frac", "superseded"),
                             ("Deathmatch", "Survival-Aware", "deaths", "superseded"),
                             ("Deathmatch", "Survival-Aware", "engagement_redirection_rate_per_100", "superseded"),
                             ("Mission", "Mission–Cooperation", "avg_ally_proximity", "superseded")]:
        if col not in lam.columns:
            continue
        g = lam[(lam["scenario"] == sc) & (lam["style"] == st)]
        a = g[g["lambda_scale"] == 1].sort_values("episode")[col].values
        b = g[g["lambda_scale"] == 0].sort_values("episode")[col].values
        w = wilcoxon_paired(a, b)
        hl = hl_paired(a, b, rng)
        entry = ("H3" if fam == "primary" else "H3 (earlier formulation: Survival-Aware lambda scale)", f"{sc} {st} {LBL[col]}, lambda x1 - x0",
                 f"median diff = {hl[0]:+.3f} [{hl[1]:+.3f}, {hl[2]:+.3f}]", f"r = {w['r']:+.2f}", w["p"], {**w, "hl": hl})
        (primary if fam == "primary" else superseded).append(entry)

    # ---------------- H3b (pre-specified 2026-09-23: teammate term on) ----------------
    tt_path = (d / "teammate_term.csv") if d.name != "urban" else (d / "teammate_term.csv")
    if tt_path.exists():
        tt = load(tt_path)
        g = tt[(tt["scenario"] == "Deathmatch") & (tt["style"] == "Mission–Cooperation")]
        a = g[g["lambda_T"] == 10].sort_values("episode")["avg_ally_proximity"].values
        b = g[g["lambda_T"] == 0].sort_values("episode")["avg_ally_proximity"].values
        w = wilcoxon_paired(a, b)
        hl = hl_paired(a, b, rng)
        primary.append(("H3b", "Deathmatch Mission–Cooperation AllyDist, lambda_T 10 - 0",
                        f"median diff = {hl[0]:+.2f} [{hl[1]:+.2f}, {hl[2]:+.2f}]", f"r = {w['r']:+.2f}", w["p"], {**w, "hl": hl}))

    # ---------------- H4 ----------------
    for sc, col in [("Mission", "avg_ally_proximity"), ("Deathmatch", "engagement_redirection_rate_per_100")]:
        g = interp[interp["scenario"] == sc][["alpha", col]].dropna()
        rho, pv = stats.spearmanr(g["alpha"], g[col])
        primary.append(("H4", f"{sc} {METRICS[col]} along alpha ({interp[interp['scenario'] == sc]['pair'].iloc[0]})",
                        f"rho = {rho:+.2f}", f"n = {len(g)}", float(pv), {"rho": float(rho), "p": float(pv)}))

    adj = holm([t[4] for t in primary])
    map_label = args.map_name or ("urban" if d.name == "urban" else "random")
    md = [f"# Hypothesis tests and effect sizes ({map_label} map)\n",
          "## Primary tests (Holm-adjusted across all primary tests of this map)\n",
          "| Hypothesis | Test | Statistic | Effect size | p | p (Holm) |", "|---|---|---|---|---|---|"]
    for (h, label, stat, eff, pv, raw), pa in zip(primary, adj):
        md.append(f"| {h} | {label} | {stat} | {eff} | {fmt_p(pv)} | {fmt_p(pa)} |")
        S["primary"].append({"hypothesis": h, "test": label, "statistic": stat, "effect": eff, "p": pv, "p_holm": pa, "raw": raw})
    md += ["\n## Earlier formulations of the hypotheses (unadjusted; not in the Holm family)\n",
           "| Hypothesis | Test | Statistic | Effect size | p |", "|---|---|---|---|---|"]
    S["secondary"] = []
    for (h, label, stat, eff, pv, raw) in superseded:
        md.append(f"| {h} | {label} | {stat} | {eff} | {fmt_p(pv)} |")
        S["secondary"].append({"hypothesis": h, "test": label, "statistic": stat, "effect": eff, "p": pv, "raw": raw})

    # ---------------- secondary pairwise style contrasts ----------------
    md.append("\n## Secondary pairwise style contrasts (Mann-Whitney; delta = Cliff's delta = rank-biserial r; HL = Hodges-Lehmann shift A - B with bootstrap 95% CI; unadjusted)\n")
    md.append("| Scenario | Metric | A | B | delta | HL [95% CI] | p |")
    md.append("|---|---|---|---|---|---|---|")
    for sc, col in [("Mission", "objective_commitment_ratio"), ("Mission", "avg_ally_proximity"),
                    ("Deathmatch", "engagement_redirection_rate_per_100"), ("Deathmatch", "resource_seeking_rate_per_100"),
                    ("Control", "control_score")]:
        for a_st, b_st in itertools.combinations(STYLES, 2):
            a = main_df[(main_df["scenario"] == sc) & (main_df["style"] == a_st)][col].astype(float).values
            b = main_df[(main_df["scenario"] == sc) & (main_df["style"] == b_st)][col].astype(float).values
            mw = mann_whitney(a, b)
            hl = hl_independent(a, b, rng)
            S["secondary_contrasts"].append({"scenario": sc, "metric": METRICS[col], "a": a_st, "b": b_st, **mw, "hl": hl})
            md.append(f"| {sc} | {METRICS[col]} | {a_st} | {b_st} | {mw['r']:+.2f} | {hl[0]:+.2f} [{hl[1]:+.2f}, {hl[2]:+.2f}] | {fmt_p(mw['p'])} |")

    (d / "hypotheses_summary.json").write_text(json.dumps(S, indent=2, ensure_ascii=False, default=float), encoding="utf-8")
    (d / "hypotheses_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Saved: {(d / 'hypotheses_summary.md').resolve()}")


if __name__ == "__main__":
    main()
