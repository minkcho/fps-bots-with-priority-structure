"""Compare the additive route cost (v2 model) with the exponential route metric (v3 main model).

Reads, for both maps, the outputs of the core experiments and of analyze_hypotheses.py from
the additive directory (--a) and the exponential-model directory (--b) and writes
model_comparison.md / model_comparison.json into --out (default: --b):

  1. primary hypothesis tests (H1-H4) side by side (effect, Holm-adjusted p)
  2. main-experiment metrics per scenario and style side by side, with paired Wilcoxon
     tests exp vs additive (episodes paired by seed; Holm within each condition)
  3. dose-response of the exp model in the lambda-scale sweep (k relative to the new defaults)

Usage:
  python experiments/compare_models.py --a ../repro_outputs/_v2_additive --b ../repro_outputs
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_stats import (METRICS, SCENARIOS, STYLES, control_outcomes, fmt, fmt_p, holm, load,  # noqa: E402
                           mean_ci, wilcoxon_paired)

KEY = {"Mission": ["objective_commitment_ratio", "avg_ally_proximity", "engagement_redirection_rate_per_100", "deaths"],
       "Deathmatch": ["engagement_redirection_rate_per_100", "resource_seeking_rate_per_100", "avg_ally_proximity",
                      "kills", "deaths"],
       "Control": ["control_score", "objective_commitment_ratio", "avg_ally_proximity", "deaths"]}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--a", type=str, required=True, help="additive-model output directory (random map)")
    p.add_argument("--b", type=str, required=True, help="exp-model output directory (random map)")
    p.add_argument("--out", type=str, default=None, help="output directory (default: --b)")
    args = p.parse_args()
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from fps_priority_ai.runner import EXP_MODEL_SCALE
    S: dict = {}
    md = [f"# v2 (additive route cost) vs v3 main model (exp route metric over the expected-hits field, lambda_E x{EXP_MODEL_SCALE:.2f}, lambda_T = 0, goal termination, separated spawns, evade hysteresis)\n"]
    for m, sub in [("random", ""), ("urban", "urban")]:
        da, db = Path(args.a) / sub, Path(args.b) / sub
        S[m] = {}
        # 1) hypotheses
        ha = json.loads((da / "hypotheses_summary.json").read_text(encoding="utf-8"))["primary"]
        hb = json.loads((db / "hypotheses_summary.json").read_text(encoding="utf-8"))["primary"]
        md.append(f"\n## {m} map: primary hypothesis tests (Holm across the primary tests of each model)\n")
        # The primary tests were redefined for v3 (H2 switching, H3 walked exposure, H3b), so the two
        # lists are shown side by side as separate tables rather than paired row by row.
        for label, hs in (("additive (v2)", ha), ("exp (v3)", hb)):
            md.append(f"\n### {label}\n")
            md.append("| Hyp. | Test | Statistic; effect | p_Holm |")
            md.append("|---|---|---|---|")
            for t in hs:
                md.append(f"| {t['hypothesis']} | {t['test']} | {t['statistic']}; {t['effect']} | {fmt_p(t['p_holm'])} |")
        S[m]["hypotheses"] = {"additive": ha, "exp": hb}
        # 2) main experiment
        ra, rb = load(da / "results.csv"), load(db / "results.csv")
        n_common = len(set(ra["episode"]) & set(rb["episode"]))
        md.append(f"\n## {m} map: main experiment, exp vs additive (paired by seed on the {n_common} common episodes; "
                  f"Holm within condition)\n")
        md.append("| Scenario | Style | Metric | additive | exp | r | p_Holm |")
        md.append("|---|---|---|---|---|---|---|")
        S[m]["main"] = {}
        for sc in SCENARIOS:
            for st in STYLES:
                a = ra[(ra["scenario"] == sc) & (ra["style"] == st)].sort_values("episode")
                b = rb[(rb["scenario"] == sc) & (rb["style"] == st)].sort_values("episode")
                # (2026-09-24) the runs may differ in episode count (v2 n=30, final v3 n=100); episode seeds depend
                # only on the index, so pair on the common episodes
                common = sorted(set(a["episode"]) & set(b["episode"]))
                a, b = a[a["episode"].isin(common)], b[b["episode"].isin(common)]
                tests = [wilcoxon_paired(b[c].values, a[c].values) for c in KEY[sc]]
                for c, t, pa in zip(KEY[sc], tests, holm([t["p"] for t in tests])):
                    t.update({"p_holm": pa, "additive": mean_ci(a[c]), "exp": mean_ci(b[c])})
                    S[m]["main"][f"{sc}|{st}|{METRICS[c]}"] = t
                    md.append(f"| {sc} | {st} | {METRICS[c]} | {fmt(t['additive'])} | {fmt(t['exp'])} | {t['r']:+.2f} | "
                              f"{fmt_p(pa)} |")
                if sc == "Control":
                    wa, wb = control_outcomes(a)["wins"], control_outcomes(b)["wins"]
                    S[m]["main"][f"Control|{st}|wins"] = {"additive": wa, "exp": wb}
        md.append("\nControl wins (additive -> exp): " + "; ".join(
            f"{st}: {S[m]['main'][f'Control|{st}|wins']['additive']} -> {S[m]['main'][f'Control|{st}|wins']['exp']}"
            for st in STYLES))
        # 3) dose-response of the exp model
        lam = load(db / "lambda_scale.csv")
        md.append(f"\n## {m} map: exp-model lambda-scale sweep (k relative to the new defaults; x1 = defaults)\n")
        S[m]["lambda_scale"] = {}
        for (sc, st), g in lam.groupby(["scenario", "style"], sort=False):
            cols = ["avg_ally_proximity", "engagement_redirection_rate_per_100", "deaths", "kills"]
            md.append(f"\n### {sc} / {st}\n")
            md.append("| k | " + " | ".join(METRICS[c] for c in cols) + " |")
            md.append("|---|" + "---|" * len(cols))
            entry = {}
            for k in sorted(g["lambda_scale"].unique()):
                gk = g[g["lambda_scale"] == k]
                entry[f"{k:g}"] = {METRICS[c]: mean_ci(gk[c]) for c in cols}
                md.append(f"| x{k:g} | " + " | ".join(fmt(mean_ci(gk[c])) for c in cols) + " |")
            for c in cols:
                sub_ = g[["lambda_scale", c]].dropna()
                if sub_[c].nunique() > 1:
                    rho, pv = stats.spearmanr(sub_["lambda_scale"], sub_[c])
                    entry[f"rho|{METRICS[c]}"] = {"rho": float(rho), "p": float(pv)}
                    md.append(f"- Spearman rho(k, {METRICS[c]}) = {rho:+.2f}, p = {fmt_p(pv)}")
            S[m]["lambda_scale"][f"{sc}|{st}"] = entry
    out = Path(args.out or args.b)
    (out / "model_comparison.json").write_text(json.dumps(S, indent=2, ensure_ascii=False, default=float), encoding="utf-8")
    (out / "model_comparison.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Saved: {(out / 'model_comparison.md').resolve()}")


if __name__ == "__main__":
    main()
