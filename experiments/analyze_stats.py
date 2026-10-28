"""Statistical summary of all experiments (single source for the numbers in the paper).

Reads the six result CSVs and writes
  - stats_summary.json : machine-readable summary
  - stats_summary.md   : human-readable tables

Contents
  - per-condition mean and 95% t-based CI, Control wins / stalls
  - style contrasts: two-sided Mann-Whitney U with rank-biserial r, Holm-adjusted within
    each (scenario, metric) family of pairwise comparisons
  - paired comparisons (navigation ablation, combat-mode ablation, commitment 0 vs 0.45):
    two-sided Wilcoxon signed-rank with matched-pairs rank-biserial r; pairs share a
    common-random-number seed
  - interpolation and navigation-weight scale: Spearman rho between alpha / scale and each metric
  - optional additional experiment (risk_budget_relative.csv / risk_budget_normalised.csv,
    if present): plan statistics and
    behaviour per relative budget beta, Spearman rho along beta, paired Wilcoxon
    beta = 0.25 vs 1, and each budget condition vs the fixed-weight main experiment
  - consistency checks: the "full" / baseline conditions of the additional experiments
    must reproduce the main-experiment episodes exactly (common random numbers)

Usage:
  python experiments/analyze_stats.py --dir ../repro_outputs
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

STYLES = ["Mission–Cooperation", "Persistent Objective", "Aggressive", "Survival-Aware"]
SCENARIOS = ["Mission", "Deathmatch", "Control"]
METRICS = {
    "objective_commitment_ratio": "ObjCommit",
    "engagement_redirection_rate_per_100": "EngRedirect",
    "resource_seeking_rate_per_100": "ResSeek",
    "avg_ally_proximity": "AllyDist",
    "kills": "Kills",
    "deaths": "Deaths",
    "control_score": "CtrlScore",
}
WIN = 120


def mean_ci(v) -> dict:
    v = np.asarray(pd.Series(v).dropna(), dtype=float)
    n = len(v)
    if n == 0:
        return {"n": 0, "mean": None, "ci": None}
    m = float(v.mean())
    ci = float(stats.t.ppf(0.975, n - 1) * v.std(ddof=1) / np.sqrt(n)) if n > 1 else 0.0
    return {"n": n, "mean": m, "ci": ci}


def mann_whitney(a, b) -> dict:
    a = np.asarray(pd.Series(a).dropna(), dtype=float)
    b = np.asarray(pd.Series(b).dropna(), dtype=float)
    if len(a) == 0 or len(b) == 0 or (np.all(a == a[0]) and np.all(b == b[0]) and a[0] == b[0]):
        return {"U": None, "p": 1.0, "r": 0.0}
    res = stats.mannwhitneyu(a, b, alternative="two-sided")
    r = 2.0 * res.statistic / (len(a) * len(b)) - 1.0  # rank-biserial, > 0 means a tends to exceed b
    return {"U": float(res.statistic), "p": float(res.pvalue), "r": float(r)}


def wilcoxon_paired(x, y) -> dict:
    """Paired two-sided Wilcoxon signed-rank on x - y with matched-pairs rank-biserial r."""
    d = np.asarray(x, dtype=float) - np.asarray(y, dtype=float)
    d = d[~np.isnan(d)]
    nz = d[d != 0]
    if len(nz) == 0:
        return {"n_pairs": int(len(d)), "n_nonzero": 0, "p": 1.0, "r": 0.0, "median_diff": 0.0}
    ranks = stats.rankdata(np.abs(nz))
    w_pos, w_neg = ranks[nz > 0].sum(), ranks[nz < 0].sum()
    res = stats.wilcoxon(nz, zero_method="wilcox", alternative="two-sided")
    return {"n_pairs": int(len(d)), "n_nonzero": int(len(nz)), "p": float(res.pvalue),
            "r": float((w_pos - w_neg) / (w_pos + w_neg)), "median_diff": float(np.median(d))}


def holm(pvals: list[float]) -> list[float]:
    order = np.argsort(pvals)
    adj, running = [0.0] * len(pvals), 0.0
    for rank, idx in enumerate(order):
        running = max(running, min(1.0, (len(pvals) - rank) * pvals[idx]))
        adj[idx] = running
    return adj


def control_outcomes(df: pd.DataFrame) -> dict:
    cs = df["control_score"].astype(float)
    wins = df[cs >= WIN]
    stalls = df[(cs == 0) & (df["kills"] == 0) & (df["deaths"] == 0)]
    return {"wins": int(len(wins)), "n": int(len(df)), "stalls": int(len(stalls)),
            "median_steps_win": float(wins["steps"].median()) if len(wins) else None}


def summarise(df: pd.DataFrame) -> dict:
    out = {}
    for col in METRICS:
        if col in df and df[col].notna().any():
            out[METRICS[col]] = mean_ci(df[col])
    if df["control_score"].notna().any():
        out["control"] = control_outcomes(df)
    return out


def fmt(s: dict, digits: int = 2) -> str:
    if s is None or s.get("mean") is None:
        return "–"
    return f"{s['mean']:.{digits}f} ± {s['ci']:.{digits}f}"


def fmt_p(p: float) -> str:
    return "<0.001" if p < 0.001 else f"{p:.3f}"


def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "style" in df:
        df["style"] = df["style"].str.replace("Mission-Cooperation", "Mission–Cooperation")
    return df


def default_lambda(style: str, model: str = "exp") -> float:
    """Configured lambda_E of a style in the given style set (fps_priority_ai/runner.py)."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from fps_priority_ai.runner import default_styles
    return default_styles(model)[style].w_exposure


def check_same(a: pd.DataFrame, b: pd.DataFrame, label: str) -> None:
    cols = ["episode"] + [c for c in METRICS if c in a] + ["steps"]
    a2 = a[cols].sort_values("episode").reset_index(drop=True)
    b2 = b[cols].sort_values("episode").reset_index(drop=True)
    pd.testing.assert_frame_equal(a2, b2, check_dtype=False, obj=label)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", type=str, required=True, help="Directory with the result CSVs")
    p.add_argument("--model", type=str, default="exp", choices=["exp", "additive"],
                   help="Style set the CSVs were produced with (for the configured lambda_E row)")
    args = p.parse_args()
    d = Path(args.dir)

    main_df = load(d / "results.csv")
    sens = load(d / "sensitivity_commitment.csv")
    nav = load(d / "ablation_navigation.csv")
    mode = load(d / "mode_ablation.csv")
    interp = load(d / "interpolation.csv")
    lam = load(d / "lambda_scale.csv")
    S: dict = {"n_per_condition": int(main_df.groupby(["scenario", "style"]).size().min())}
    md: list[str] = [f"# Statistical summary (n = {S['n_per_condition']} episodes per condition)\n"]

    # ---- consistency checks (common random numbers) ----
    for (sc, st), g in nav[nav["variant"] == "full"].groupby(["scenario", "style"]):
        check_same(g, main_df[(main_df["scenario"] == sc) & (main_df["style"] == st)], f"nav full {sc}/{st}")
    for sc in ("Mission", "Control"):
        check_same(sens[(sens["scenario"] == sc) & (sens["w_commitment"].round(2) == 0.45)],
                   main_df[(main_df["scenario"] == sc) & (main_df["style"] == "Mission–Cooperation")],
                   f"sensitivity 0.45 {sc}")
    for (sc, st), g in lam[lam["lambda_scale"] == 1].groupby(["scenario", "style"]):
        check_same(g, main_df[(main_df["scenario"] == sc) & (main_df["style"] == st)], f"lambda x1 {sc}/{st}")
    for (sc, st), g in lam[lam["lambda_scale"] == 0].groupby(["scenario", "style"]):
        check_same(g, nav[(nav["scenario"] == sc) & (nav["style"] == st) & (nav["variant"] == "distance_only")],
                   f"lambda x0 {sc}/{st}")
    S["consistency_checks"] = "passed"
    md.append("Consistency checks (CRN): navigation-ablation full = main; commitment 0.45 = main MC; "
              "lambda x1 = main; lambda x0 = distance-only. **passed**\n")

    # ---- main experiment ----
    S["main"] = {}
    md.append("## Main experiment\n")
    md.append("| Scenario | Style | ObjCommit | AllyDist | EngRedirect | ResSeek | Kills | Deaths | Control |")
    md.append("|---|---|---|---|---|---|---|---|---|")
    for sc in SCENARIOS:
        for st in STYLES:
            g = main_df[(main_df["scenario"] == sc) & (main_df["style"] == st)]
            s = summarise(g)
            S["main"][f"{sc}|{st}"] = s
            ctrl = ""
            if "control" in s:
                c = s["control"]
                ctrl = f"{fmt(s['CtrlScore'])}; wins {c['wins']}/{c['n']}; stalls {c['stalls']}; med. steps {c['median_steps_win']}"
            md.append(f"| {sc} | {st} | {fmt(s.get('ObjCommit'))} | {fmt(s.get('AllyDist'))} | {fmt(s.get('EngRedirect'))} | "
                      f"{fmt(s.get('ResSeek'))} | {fmt(s.get('Kills'), 1)} | {fmt(s.get('Deaths'), 1)} | {ctrl} |")

    # ---- style contrasts ----
    families = {
        "Mission": ["objective_commitment_ratio", "avg_ally_proximity"],
        "Deathmatch": ["engagement_redirection_rate_per_100", "resource_seeking_rate_per_100", "avg_ally_proximity"],
        "Control": ["control_score", "objective_commitment_ratio", "avg_ally_proximity"],
    }
    S["contrasts"] = {}
    md.append("\n## Style contrasts (Mann–Whitney U, rank-biserial r > 0: first style higher; Holm within family)\n")
    md.append("| Scenario | Metric | Style A | Style B | r | p | p (Holm) |")
    md.append("|---|---|---|---|---|---|---|")
    for sc, cols in families.items():
        for col in cols:
            pairs = list(itertools.combinations(STYLES, 2))
            res = [mann_whitney(main_df[(main_df["scenario"] == sc) & (main_df["style"] == a)][col],
                                main_df[(main_df["scenario"] == sc) & (main_df["style"] == b)][col]) for a, b in pairs]
            adj = holm([r["p"] for r in res])
            for (a, b), r, pa in zip(pairs, res, adj):
                r["p_holm"] = pa
                S["contrasts"][f"{sc}|{METRICS[col]}|{a}|{b}"] = r
                md.append(f"| {sc} | {METRICS[col]} | {a} | {b} | {r['r']:+.2f} | {fmt_p(r['p'])} | {fmt_p(pa)} |")

    # ---- commitment sensitivity ----
    S["sensitivity"] = {}
    md.append("\n## Commitment sensitivity (Mission–Cooperation base)\n")
    md.append("| w_commit | Mission ObjCommit | Control score | Control wins | stalls |")
    md.append("|---|---|---|---|---|")
    for w in sorted(sens["w_commitment"].unique()):
        mi = sens[(sens["scenario"] == "Mission") & (sens["w_commitment"] == w)]
        co = sens[(sens["scenario"] == "Control") & (sens["w_commitment"] == w)]
        s = {"Mission": summarise(mi), "Control": summarise(co)}
        S["sensitivity"][f"{w:.2f}"] = s
        c = s["Control"]["control"]
        md.append(f"| {w:.2f} | {fmt(s['Mission']['ObjCommit'])} | {fmt(s['Control']['CtrlScore'])} | {c['wins']}/{c['n']} | {c['stalls']} |")
    for sc, col in (("Mission", "objective_commitment_ratio"), ("Control", "control_score")):
        a = sens[(sens["scenario"] == sc) & (sens["w_commitment"] == 0.0)].sort_values("episode")[col]
        b = sens[(sens["scenario"] == sc) & (sens["w_commitment"].round(2) == 0.45)].sort_values("episode")[col]
        r = wilcoxon_paired(b.values, a.values)
        S["sensitivity"][f"paired_0.45_vs_0|{sc}"] = r
        md.append(f"\nPaired Wilcoxon, w=0.45 vs w=0 ({sc}, {METRICS[col]}): r = {r['r']:+.2f}, p = {fmt_p(r['p'])}")

    # ---- navigation ablation ----
    S["nav_ablation"] = {}
    md.append("\n## Navigation ablation (full vs distance-only; paired Wilcoxon, r > 0: full higher)\n")
    md.append("| Condition | Metric | Full | Distance-only | r | p |")
    md.append("|---|---|---|---|---|---|")
    for (sc, st), g in nav.groupby(["scenario", "style"], sort=False):
        full = g[g["variant"] == "full"].sort_values("episode")
        dist = g[g["variant"] == "distance_only"].sort_values("episode")
        for col in ["avg_ally_proximity", "objective_commitment_ratio", "engagement_redirection_rate_per_100",
                    "resource_seeking_rate_per_100", "kills", "deaths"]:
            r = wilcoxon_paired(full[col].values, dist[col].values)
            r.update({"full": mean_ci(full[col]), "distance_only": mean_ci(dist[col])})
            S["nav_ablation"][f"{sc}|{st}|{METRICS[col]}"] = r
            md.append(f"| {sc}/{st} | {METRICS[col]} | {fmt(r['full'])} | {fmt(r['distance_only'])} | {r['r']:+.2f} | {fmt_p(r['p'])} |")

    # ---- combat-mode ablation ----
    S["mode_ablation"] = {}
    md.append("\n## Combat-mode ablation (full vs weights-only; paired Wilcoxon, r > 0: full higher)\n")
    md.append("| Scenario | Style | Metric | Full | Weights-only | r | p |")
    md.append("|---|---|---|---|---|---|---|")
    mode_cols = {
        "Mission": ["objective_commitment_ratio", "avg_ally_proximity", "engagement_redirection_rate_per_100", "resource_seeking_rate_per_100"],
        "Deathmatch": ["engagement_redirection_rate_per_100", "resource_seeking_rate_per_100", "avg_ally_proximity"],
        "Control": ["control_score", "objective_commitment_ratio", "engagement_redirection_rate_per_100", "resource_seeking_rate_per_100"],
    }
    for sc in SCENARIOS:
        for st in STYLES:
            full = main_df[(main_df["scenario"] == sc) & (main_df["style"] == st)].sort_values("episode")
            wo = mode[(mode["scenario"] == sc) & (mode["style"] == st)].sort_values("episode")
            entry = {"full": summarise(full), "weights_only": summarise(wo), "tests": {}}
            for col in mode_cols[sc]:
                r = wilcoxon_paired(full[col].values, wo[col].values)
                entry["tests"][METRICS[col]] = r
                md.append(f"| {sc} | {st} | {METRICS[col]} | {fmt(mean_ci(full[col]))} | {fmt(mean_ci(wo[col]))} | {r['r']:+.2f} | {fmt_p(r['p'])} |")
            S["mode_ablation"][f"{sc}|{st}"] = entry
    md.append("\nWeights-only Control outcomes: " + "; ".join(
        f"{st}: {S['mode_ablation'][f'Control|{st}']['weights_only']['control']['wins']}/"
        f"{S['mode_ablation'][f'Control|{st}']['weights_only']['control']['n']} wins" for st in STYLES))

    # ---- interpolation ----
    S["interpolation"] = {}
    md.append("\n## Style interpolation (mode fixed to keep moving; Spearman rho between alpha and metric)\n")
    for (sc, pair), g in interp.groupby(["scenario", "pair"], sort=False):
        cols = (["engagement_redirection_rate_per_100", "resource_seeking_rate_per_100", "avg_ally_proximity", "kills", "deaths"]
                if sc == "Deathmatch" else
                ["objective_commitment_ratio", "avg_ally_proximity", "engagement_redirection_rate_per_100", "kills", "deaths"])
        entry = {"per_alpha": {}, "spearman": {}}
        md.append(f"\n### {sc}: {pair}\n")
        md.append("| alpha | " + " | ".join(METRICS[c] for c in cols) + " |")
        md.append("|---|" + "---|" * len(cols))
        for a in sorted(g["alpha"].unique()):
            ga = g[g["alpha"] == a]
            entry["per_alpha"][f"{a:.2f}"] = {METRICS[c]: mean_ci(ga[c]) for c in cols}
            md.append(f"| {a:.2f} | " + " | ".join(fmt(mean_ci(ga[c])) for c in cols) + " |")
        md.append("")
        for c in cols:
            sub = g[["alpha", c]].dropna()
            rho, pv = stats.spearmanr(sub["alpha"], sub[c])
            entry["spearman"][METRICS[c]] = {"rho": float(rho), "p": float(pv)}
            md.append(f"- Spearman rho(alpha, {METRICS[c]}) = {rho:+.2f}, p = {fmt_p(pv)}")
        S["interpolation"][f"{sc}|{pair}"] = entry

    # ---- navigation-weight scale ----
    S["lambda_scale"] = {}
    md.append("\n## Navigation-weight scale (lambda x k; Spearman rho between k and metric)\n")
    lam_cols = ["avg_ally_proximity", "objective_commitment_ratio", "engagement_redirection_rate_per_100",
                "resource_seeking_rate_per_100", "kills", "deaths"]
    for (sc, st), g in lam.groupby(["scenario", "style"], sort=False):
        entry = {"per_scale": {}, "spearman": {}}
        md.append(f"\n### {sc} / {st}\n")
        md.append("| scale | " + " | ".join(METRICS[c] for c in lam_cols) + " |")
        md.append("|---|" + "---|" * len(lam_cols))
        for k in sorted(g["lambda_scale"].unique()):
            gk = g[g["lambda_scale"] == k]
            entry["per_scale"][f"{k:g}"] = {METRICS[c]: mean_ci(gk[c]) for c in lam_cols}
            md.append(f"| x{k:g} | " + " | ".join(fmt(mean_ci(gk[c])) for c in lam_cols) + " |")
        md.append("")
        for c in lam_cols:
            sub = g[["lambda_scale", c]].dropna()
            if sub[c].nunique() < 2:
                continue
            rho, pv = stats.spearmanr(sub["lambda_scale"], sub[c])
            entry["spearman"][METRICS[c]] = {"rho": float(rho), "p": float(pv)}
            md.append(f"- Spearman rho(scale, {METRICS[c]}) = {rho:+.2f}, p = {fmt_p(pv)}")
        S["lambda_scale"][f"{sc}|{st}"] = entry

    # ---- additional experiment: designer risk budgets (optional) ----
    for mode in ("relative", "normalised"):
        if not (d / f"risk_budget_{mode}.csv").exists():
            continue
        rb = load(d / f"risk_budget_{mode}.csv")
        S[f"risk_budget_{mode}"] = {}
        md.append(f"\n## Additional experiment: designer risk budgets, {mode} budget (Deathmatch)\n")
        plan_cols = ["budget_adherence", "exposure_ratio", "length_overhead", "mean_lambda"]
        if mode == "normalised":
            plan_cols = plan_cols + ["budget_position"]
        beh_cols = ["engagement_redirection_rate_per_100", "resource_seeking_rate_per_100",
                    "avg_ally_proximity", "kills", "deaths"]
        for st, g in rb.groupby("style", sort=False):
            ref = main_df[(main_df["scenario"] == "Deathmatch") & (main_df["style"] == st)].sort_values("episode")
            entry = {"per_beta": {}, "spearman": {}, "paired_0.25_vs_1": {}, "vs_fixed": {}}
            md.append(f"\n### {st} (fixed-weight reference: main experiment)\n")
            cols = plan_cols + beh_cols
            md.append("| beta | Adherence | ExposureRatio | LengthOverhead | lambda_E | " +
                      ("BudgetPosition | " if mode == "normalised" else "") +
                      " | ".join(METRICS[c] for c in beh_cols) + " |")
            md.append("|---|" + "---|" * len(cols))
            md.append("| fixed | – | – | – | " + f"{default_lambda(st, args.model):.2f} | " +
                      ("– | " if mode == "normalised" else "") +
                      " | ".join(fmt(mean_ci(ref[c])) for c in beh_cols) + " |")
            for b in sorted(g["beta"].unique(), reverse=True):
                gb = g[g["beta"] == b].sort_values("episode")
                entry["per_beta"][f"{b:.2f}"] = {c: mean_ci(gb[c]) for c in cols}
                md.append(f"| {b:.2f} | " + " | ".join(fmt(mean_ci(gb[c]), 3) for c in plan_cols) + " | " +
                          " | ".join(fmt(mean_ci(gb[c])) for c in beh_cols) + " |")
                entry["vs_fixed"][f"{b:.2f}"] = {METRICS[c]: wilcoxon_paired(gb[c].values, ref[c].values)
                                                 for c in beh_cols}
            md.append("")
            for c in cols:
                sub = g[["beta", c]].dropna()
                if sub[c].nunique() < 2:
                    continue
                rho, pv = stats.spearmanr(sub["beta"], sub[c])
                entry["spearman"][c] = {"rho": float(rho), "p": float(pv)}
                md.append(f"- Spearman rho(beta, {c}) = {rho:+.2f}, p = {fmt_p(pv)}")
            b_lo = g["beta"].min()
            lo = g[g["beta"] == b_lo].sort_values("episode")
            hi = g[g["beta"].round(2) == 1.00].sort_values("episode")
            md.append("")
            for c in cols:
                r = wilcoxon_paired(lo[c].values, hi[c].values)
                entry["paired_0.25_vs_1"][c] = r
                md.append(f"- Paired Wilcoxon beta={b_lo:.2f} vs 1 ({c}): r = {r['r']:+.2f}, p = {fmt_p(r['p'])}")
            S[f"risk_budget_{mode}"][st] = entry

    (d / "stats_summary.json").write_text(json.dumps(S, indent=2, ensure_ascii=False), encoding="utf-8")
    (d / "stats_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Saved: {(d / 'stats_summary.md').resolve()}")


if __name__ == "__main__":
    main()
