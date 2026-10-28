"""Hits actually taken: the independent outcome for H3 (2026-09-24, suggested by the v3 review).

The walked exposure (expected hits per walked step) uses the same definition the planner minimises; the number of
hits the evaluated team actually receives is an outcome the planner does not see. This script
  1. checks that the rerun with the hits-taken counter reproduces the final run (all shared columns identical),
  2. repeats the primary H3 comparison with hits taken per alive step as the readout (cost-term ablation, configured
     lambda_E vs lambda_E = 0; Deathmatch per style with Holm adjustment over the four styles of a map; one-sided sign
     test over the twelve scenario x style conditions),
  3. reports how closely expected and actual hits agree per episode (Spearman rho, main experiment).

Usage: python experiments/analyze_hits_taken.py --rerun ../repro_outputs/v3_hits --final ../repro_outputs/v3 \
           --out ../repro_outputs/v3_hits/hits_taken_summary.md
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_stats import wilcoxon_paired, holm  # noqa: E402

STYLES = ["Mission–Cooperation", "Persistent Objective", "Aggressive", "Survival-Aware"]
SCENARIOS = ["Mission", "Deathmatch", "Control"]
NEW = {"hits_taken", "hits_taken_per_step"}


def fmt_p(p):
    return "<0.001" if p < 0.001 else f"{p:.3f}"


def identical(new: pd.DataFrame, old: pd.DataFrame, key: list[str]) -> str:
    cols = [c for c in old.columns if c not in key and c not in NEW]
    m = new.merge(old, on=key, suffixes=("_n", "_o"))
    bad = []
    for c in cols:
        a, b = m[c + "_n"], m[c + "_o"]
        same = (a.isna() & b.isna()) | (a.astype(str) == b.astype(str))
        try:
            same |= np.isclose(pd.to_numeric(a, errors="coerce"), pd.to_numeric(b, errors="coerce"), equal_nan=True)
        except TypeError:
            pass
        if not same.all():
            bad.append(c)
    return f"{len(m)} of {len(old)} rows matched; " + ("all shared columns identical" if not bad else f"differences in {bad}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rerun", default="../repro_outputs/v3_hits")
    ap.add_argument("--final", default="../repro_outputs/v3")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    md = ["# Hits taken: independent outcome for H3 (rerun with the hits-taken counter, n = 100)", ""]
    for mp, sub in (("random", ""), ("urban", "urban")):
        rd, fd = Path(args.rerun) / sub, Path(args.final) / sub
        res_n, res_o = pd.read_csv(rd / "results.csv"), pd.read_csv(fd / "results.csv")
        ct_n, ct_o = pd.read_csv(rd / "cost_term_ablation.csv"), pd.read_csv(fd / "cost_term_ablation.csv")
        md += [f"## {mp} map", "",
               f"- Reproduction check, main experiment: {identical(res_n, res_o, ['scenario', 'style', 'episode'])}",
               f"- Reproduction check, cost-term ablation: {identical(ct_n, ct_o, ['scenario', 'style', 'variant', 'episode'])}", ""]
        # main experiment: hits taken per style and agreement with the expected hits
        md += ["### Main experiment: hits taken per alive step (mean) and agreement with walked expected hits", "",
               "| Scenario | Style | hits taken / step | walked expected hits / step | Spearman rho (episodes) |", "|---|---|---|---|---|"]
        for sc in SCENARIOS:
            for st in STYLES:
                d = res_n[(res_n.scenario == sc) & (res_n["style"] == st)]
                rho = stats.spearmanr(d.walked_hits_per_step, d.hits_taken_per_step).statistic
                md.append(f"| {sc} | {st} | {d.hits_taken_per_step.mean():.4f} | {d.walked_hits_per_step.mean():.4f} | {rho:+.2f} |")
        rho_all = stats.spearmanr(res_n.walked_hits_per_step, res_n.hits_taken_per_step).statistic
        md += ["", f"Pooled over all 1200 episodes: Spearman rho = {rho_all:+.2f}", ""]
        # H3 with hits taken
        md += ["### H3 with hits taken (cost-term ablation, configured lambda_E vs 0)", "",
               "| Scenario | Style | full | no exposure | change | r | p | p_Holm (DM, 4 styles) |", "|---|---|---|---|---|---|---|---|"]
        dm_p, rows, lower = [], [], 0
        for sc in SCENARIOS:
            for st in STYLES:
                f = ct_n[(ct_n.scenario == sc) & (ct_n["style"] == st) & (ct_n.variant == "full")].sort_values("episode")
                z = ct_n[(ct_n.scenario == sc) & (ct_n["style"] == st) & (ct_n.variant == "no_exposure")].sort_values("episode")
                t = wilcoxon_paired(f.hits_taken_per_step.values, z.hits_taken_per_step.values)
                mf, mz = f.hits_taken_per_step.mean(), z.hits_taken_per_step.mean()
                lower += int(mf < mz)
                rows.append((sc, st, mf, mz, t))
                if sc == "Deathmatch":
                    dm_p.append(t["p"])
        adj = iter(holm(dm_p))
        for sc, st, mf, mz, t in rows:
            ph = fmt_p(next(adj)) if sc == "Deathmatch" else ""
            md.append(f"| {sc} | {st} | {mf:.4f} | {mz:.4f} | {100 * (mf - mz) / mz:+.0f}% | {t['r']:+.2f} | {fmt_p(t['p'])} | {ph} |")
        sign_p = stats.binomtest(lower, 12, 0.5, alternative="greater").pvalue
        md += ["", f"Sign test: hits taken lower with the exposure term in {lower} of 12 conditions (one-sided binomial p = {fmt_p(sign_p)})", ""]
    text = "\n".join(md) + "\n"
    if args.out:
        Path(args.out).write_text(text)
    print(text)


if __name__ == "__main__":
    main()
