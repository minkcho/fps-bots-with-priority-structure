"""Redefined H2 (2026-09-23): the commitment weight controls goal-switching frequency.

Reads sensitivity_commitment.csv (Mission and Control, Mission--Cooperation base, w_commit sweep)
and results.csv from a results directory and reports, per scenario, the mean goal-switch rate per
100 alive steps and objective commitment at each w_commit, Spearman rho between w_commit and the
switch rate, and paired Wilcoxon tests (w_commit 0.45 vs 0; 1.25 vs 0) with matched-pairs
rank-biserial r. Needs scipy (venv). Usage: python experiments/analyze_h2_switching.py --dir ../repro_outputs/v3
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


def paired(a, b):
    d = np.asarray(b, float) - np.asarray(a, float)
    nz = d[d != 0]
    if len(nz) == 0:
        return 1.0, 0.0
    p = stats.wilcoxon(nz).pvalue
    ranks = stats.rankdata(np.abs(nz)); wp = ranks[nz > 0].sum(); wn = ranks[nz < 0].sum()
    return float(p), float((wp - wn) / (wp + wn))


def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument("--dir", default="../repro_outputs/v3"); args = ap.parse_args()
    d = Path(args.dir)
    df = pd.read_csv(d / "sensitivity_commitment.csv")
    wcol = [c for c in df.columns if "commit" in c.lower() and c != "objective_commitment_ratio"][0]
    out = [f"# Redefined H2: commitment weight vs goal switching ({d.name} directory)\n"]
    for sc, g in df.groupby("scenario"):
        out.append(f"\n## {sc}\n")
        out.append("| w_commit | goal switches / 100 steps | objective commitment | engagement redirection | deaths |")
        out.append("|---|---|---|---|---|")
        for w, gg in g.groupby(wcol):
            out.append(f"| {w:g} | {gg['goal_switch_rate_per_100'].mean():.2f} ± {1.96*gg['goal_switch_rate_per_100'].std(ddof=1)/np.sqrt(len(gg)):.2f} | {gg['objective_commitment_ratio'].mean():.2f} | {gg['engagement_redirection_rate_per_100'].mean():.2f} | {gg['deaths'].mean():.2f} |")
        rho, p = stats.spearmanr(g[wcol], g["goal_switch_rate_per_100"])
        out.append(f"\nSpearman rho(w_commit, goal switches) = {rho:+.2f}, p = {p:.3g} (n = {len(g)})")
        base = g[g[wcol] == 0].sort_values("episode")
        for w in (0.45, 1.25):
            cur = g[np.isclose(g[wcol], w)].sort_values("episode")
            eps = sorted(set(base["episode"]) & set(cur["episode"]))
            a = base.set_index("episode").loc[eps, "goal_switch_rate_per_100"]; b = cur.set_index("episode").loc[eps, "goal_switch_rate_per_100"]
            pw, r = paired(a, b)
            out.append(f"Paired Wilcoxon, goal switches, w_commit {w} vs 0: median diff {float(np.median(b.values - a.values)):+.2f}, r = {r:+.2f}, p = {pw:.3g}")
    res = pd.read_csv(d / "results.csv")
    out.append("\n## Main experiment: goal switches per 100 steps by style\n")
    out.append("| Scenario | " + " | ".join(res["style"].unique()) + " |")
    out.append("|---|" + "---|" * res["style"].nunique())
    for sc, g in res.groupby("scenario", sort=False):
        out.append(f"| {sc} | " + " | ".join(f"{g[g['style']==s]['goal_switch_rate_per_100'].mean():.2f}" for s in res["style"].unique()) + " |")
    text = "\n".join(out); print(text); (d / "h2_switching_summary.md").write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
