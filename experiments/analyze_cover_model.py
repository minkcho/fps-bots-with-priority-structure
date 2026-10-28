"""Statistical summary of the threat-relative cover experiment (one map directory).

Expects in --dir:
  results.csv, ablation_navigation.csv, lambda_scale.csv   (adjacency cover, main pipeline)
  cover_model.csv                                          (run_cover_model.py)
  threat_cover/results.csv, threat_cover/lambda_scale.csv  (--cover-model threat)
Writes cover_summary.md / cover_summary.json into --dir.

Usage:
  python experiments/analyze_cover_model.py --dir ../repro_outputs
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from scipy import stats

sys_path = Path(__file__).resolve().parent
import sys
sys.path.insert(0, str(sys_path))

from analyze_stats import METRICS, STYLES, SCENARIOS, check_same, control_outcomes, fmt, fmt_p, load, mean_ci, wilcoxon_paired  # noqa: E402

COLS = ["engagement_redirection_rate_per_100", "resource_seeking_rate_per_100", "avg_ally_proximity",
        "objective_commitment_ratio", "kills", "deaths"]
VARIANTS = ["distance_only", "adjacency_cover_only", "threat_cover_only", "adjacency_full", "threat_full"]
CONTRASTS = [("adjacency_cover_only", "distance_only"), ("threat_cover_only", "distance_only"),
             ("threat_cover_only", "adjacency_cover_only"), ("threat_full", "adjacency_full")]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", type=str, required=True)
    args = p.parse_args()
    d = Path(args.dir)
    main_df, nav, lam = load(d / "results.csv"), load(d / "ablation_navigation.csv"), load(d / "lambda_scale.csv")
    cov = load(d / "cover_model.csv")
    main_t, lam_t = load(d / "threat_cover" / "results.csv"), load(d / "threat_cover" / "lambda_scale.csv")
    S: dict = {}
    md = [f"# Threat-relative cover: statistical summary ({'urban' if d.name == 'urban' else 'random'} map)\n"]

    # consistency (common random numbers)
    for (sc, st), g in cov[cov["variant"] == "adjacency_full"].groupby(["scenario", "style"]):
        check_same(g, main_df[(main_df["scenario"] == sc) & (main_df["style"] == st)], f"adjacency_full {sc}/{st}")
    for (sc, st), g in cov[cov["variant"] == "distance_only"].groupby(["scenario", "style"]):
        ref = nav[(nav["scenario"] == sc) & (nav["style"] == st) & (nav["variant"] == "distance_only")]
        if len(ref):
            check_same(g, ref, f"distance_only {sc}/{st}")
    md.append("Consistency checks (CRN): adjacency_full = main; distance_only = navigation ablation. **passed**\n")

    # 1) decomposition
    S["decomposition"] = {}
    md.append("## Route-cost decomposition (paired Wilcoxon; r > 0: first variant higher)\n")
    for (sc, st), g in cov.groupby(["scenario", "style"], sort=False):
        md.append(f"\n### {sc} / {st}\n")
        md.append("| Variant | " + " | ".join(METRICS[c] for c in COLS) + " |")
        md.append("|---|" + "---|" * len(COLS))
        entry = {"means": {}, "tests": {}}
        for v in VARIANTS:
            gv = g[g["variant"] == v]
            entry["means"][v] = {METRICS[c]: mean_ci(gv[c]) for c in COLS}
            md.append(f"| {v} | " + " | ".join(fmt(mean_ci(gv[c])) for c in COLS) + " |")
        md.append("")
        for a, b in CONTRASTS:
            ga = g[g["variant"] == a].sort_values("episode")
            gb = g[g["variant"] == b].sort_values("episode")
            parts = []
            for c in ("engagement_redirection_rate_per_100", "deaths", "avg_ally_proximity"):
                r = wilcoxon_paired(ga[c].values, gb[c].values)
                entry["tests"][f"{a} vs {b}|{METRICS[c]}"] = r
                parts.append(f"{METRICS[c]} r={r['r']:+.2f}, p={fmt_p(r['p'])}")
            md.append(f"- {a} vs {b}: " + "; ".join(parts))
        S["decomposition"][f"{sc}|{st}"] = entry

    # 2) main experiment with threat cover
    S["main_threat"] = {}
    md.append("\n## Main experiment: threat cover vs adjacency cover (evaluated team; paired Wilcoxon)\n")
    md.append("| Scenario | Style | Metric | Adjacency | Threat | r | p |")
    md.append("|---|---|---|---|---|---|---|")
    key = {"Mission": ["objective_commitment_ratio", "avg_ally_proximity", "deaths"],
           "Deathmatch": ["engagement_redirection_rate_per_100", "resource_seeking_rate_per_100", "deaths"],
           "Control": ["control_score", "objective_commitment_ratio", "deaths"]}
    for sc in SCENARIOS:
        for st in STYLES:
            a = main_df[(main_df["scenario"] == sc) & (main_df["style"] == st)].sort_values("episode")
            t = main_t[(main_t["scenario"] == sc) & (main_t["style"] == st)].sort_values("episode")
            entry = {}
            for c in key[sc]:
                r = wilcoxon_paired(t[c].values, a[c].values)
                r.update({"adjacency": mean_ci(a[c]), "threat": mean_ci(t[c])})
                entry[METRICS[c]] = r
                md.append(f"| {sc} | {st} | {METRICS[c]} | {fmt(r['adjacency'])} | {fmt(r['threat'])} | {r['r']:+.2f} | {fmt_p(r['p'])} |")
            if sc == "Control":
                entry["wins"] = {"adjacency": control_outcomes(a)["wins"], "threat": control_outcomes(t)["wins"]}
            S["main_threat"][f"{sc}|{st}"] = entry
    md.append("\nControl wins (adjacency -> threat): " + "; ".join(
        f"{st}: {S['main_threat'][f'Control|{st}']['wins']['adjacency']} -> {S['main_threat'][f'Control|{st}']['wins']['threat']}"
        for st in STYLES))

    # 3) lambda scale with threat cover
    S["lambda_scale_threat"] = {}
    md.append("\n## Navigation-weight scale with threat cover (Spearman rho between k and metric)\n")
    for (sc, st), g in lam_t.groupby(["scenario", "style"], sort=False):
        md.append(f"\n### {sc} / {st}\n")
        md.append("| scale | AllyDist | EngRedirect | ResSeek | Kills | Deaths |")
        md.append("|---|---|---|---|---|---|")
        entry = {"per_scale": {}, "spearman": {}}
        for k in sorted(g["lambda_scale"].unique()):
            gk = g[g["lambda_scale"] == k]
            cols = ["avg_ally_proximity", "engagement_redirection_rate_per_100", "resource_seeking_rate_per_100", "kills", "deaths"]
            entry["per_scale"][f"{k:g}"] = {METRICS[c]: mean_ci(gk[c]) for c in cols}
            md.append(f"| x{k:g} | " + " | ".join(fmt(mean_ci(gk[c])) for c in cols) + " |")
        for c in ["avg_ally_proximity", "engagement_redirection_rate_per_100", "deaths"]:
            sub = g[["lambda_scale", c]].dropna()
            if sub[c].nunique() > 1:
                rho, pv = stats.spearmanr(sub["lambda_scale"], sub[c])
                entry["spearman"][METRICS[c]] = {"rho": float(rho), "p": float(pv)}
                md.append(f"- Spearman rho(scale, {METRICS[c]}) = {rho:+.2f}, p = {fmt_p(pv)}")
        x0 = g[g["lambda_scale"] == 0].sort_values("episode")
        x1 = g[g["lambda_scale"] == 1].sort_values("episode")
        for c in ["avg_ally_proximity", "engagement_redirection_rate_per_100", "deaths"]:
            r = wilcoxon_paired(x1[c].values, x0[c].values)
            entry[f"x1_vs_x0|{METRICS[c]}"] = r
            md.append(f"- Paired Wilcoxon x1 vs x0 ({METRICS[c]}): r = {r['r']:+.2f}, p = {fmt_p(r['p'])}")
        S["lambda_scale_threat"][f"{sc}|{st}"] = entry

    (d / "cover_summary.json").write_text(json.dumps(S, indent=2, ensure_ascii=False), encoding="utf-8")
    (d / "cover_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Saved: {(d / 'cover_summary.md').resolve()}")


if __name__ == "__main__":
    main()
