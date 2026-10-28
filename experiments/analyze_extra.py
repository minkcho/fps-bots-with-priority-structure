"""Statistical summary of the cost-term ablation and the external baselines (one map directory).

Expects in --dir: results.csv, cost_term_ablation.csv, baselines.csv.
Writes extra_summary.md / extra_summary.json into --dir.

  - leave-one-out cost-term ablation: each variant vs full, paired two-sided Wilcoxon with
    matched-pairs rank-biserial r, Holm-adjusted within each (scenario, style) family
  - baselines: per-condition means, Control wins; each behaviour tree vs its corresponding
    priority-structure style (MC-CSO, PO-OW, Agg-AC, SA-XO), two-sided Mann-Whitney U with
    rank-biserial r; fingerprint matching: nearest priority-structure style of every
    baseline in the min-max-normalised space of the four behavioural metrics

Usage:
  python experiments/analyze_extra.py --dir ../repro_outputs
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_stats import (METRICS, SCENARIOS, STYLES, check_same, control_outcomes, fmt, fmt_p,  # noqa: E402
                           holm, load, mann_whitney, mean_ci, wilcoxon_paired)

VARIANTS = ["no_exposure", "no_cover", "no_separation"]
BASELINES = ["CSO-BT", "OW-BT", "AC-BT", "XO-BT", "UtilityAI"]
PAIRS = {"CSO-BT": "Mission–Cooperation", "OW-BT": "Persistent Objective",
         "AC-BT": "Aggressive", "XO-BT": "Survival-Aware"}
FP_COLS = ["objective_commitment_ratio", "engagement_redirection_rate_per_100",
           "resource_seeking_rate_per_100", "avg_ally_proximity"]
KEY = {"Mission": ["objective_commitment_ratio", "avg_ally_proximity", "engagement_redirection_rate_per_100", "deaths"],
       "Deathmatch": ["engagement_redirection_rate_per_100", "resource_seeking_rate_per_100", "avg_ally_proximity", "deaths"],
       "Control": ["control_score", "objective_commitment_ratio", "avg_ally_proximity", "deaths"]}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", type=str, required=True)
    args = p.parse_args()
    d = Path(args.dir)
    main_df, ct, bl = load(d / "results.csv"), load(d / "cost_term_ablation.csv"), pd.read_csv(d / "baselines.csv")
    S: dict = {}
    md = [f"# Cost-term ablation and external baselines ({'urban' if d.name == 'urban' else 'random'} map)\n"]

    # ---------------- leave-one-out cost-term ablation ----------------
    for (sc, st), g in ct[ct["variant"] == "full"].groupby(["scenario", "style"]):
        check_same(g, main_df[(main_df["scenario"] == sc) & (main_df["style"] == st)], f"cost-term full {sc}/{st}")
    md.append("Consistency check (CRN): cost-term full = main. **passed**\n")
    md.append("## Leave-one-out cost-term ablation (paired Wilcoxon vs full; r > 0: variant higher; Holm per condition)\n")
    S["cost_terms"] = {}
    for sc in SCENARIOS:
        for st in STYLES:
            g = ct[(ct["scenario"] == sc) & (ct["style"] == st)]
            full = g[g["variant"] == "full"].sort_values("episode")
            md.append(f"\n### {sc} / {st}\n")
            md.append("| Variant | " + " | ".join(METRICS[c] for c in KEY[sc]) + " |")
            md.append("|---|" + "---|" * len(KEY[sc]))
            md.append("| full | " + " | ".join(fmt(mean_ci(full[c])) for c in KEY[sc]) + " |")
            tests, labels = [], []
            for v in VARIANTS:
                gv = g[g["variant"] == v].sort_values("episode")
                md.append(f"| {v} | " + " | ".join(fmt(mean_ci(gv[c])) for c in KEY[sc]) + " |")
                for c in KEY[sc]:
                    r = wilcoxon_paired(gv[c].values, full[c].values)
                    r.update({"full": mean_ci(full[c]), "variant": mean_ci(gv[c])})
                    tests.append(r); labels.append((v, METRICS[c]))
            adj = holm([t["p"] for t in tests])
            entry = {}
            sig = []
            for (v, m), t, pa in zip(labels, tests, adj):
                t["p_holm"] = pa
                entry[f"{v}|{m}"] = t
                if t["p"] < 0.05:
                    sig.append(f"{v} {m}: r={t['r']:+.2f}, p={fmt_p(t['p'])}, p_Holm={fmt_p(pa)}")
            md.append("")
            md.append("- nominally significant: " + ("; ".join(sig) if sig else "none"))
            S["cost_terms"][f"{sc}|{st}"] = entry

    # ---------------- external baselines ----------------
    S["baselines"] = {"per_condition": {}, "pairs": {}, "fingerprint": {}}
    md.append("\n## External baselines (vs fixed Aggressive opponent)\n")
    md.append("| Scenario | Agent | ObjCommit | AllyDist | EngRedirect | ResSeek | Kills | Deaths | Control |")
    md.append("|---|---|---|---|---|---|---|---|---|")
    rows = []
    for sc in SCENARIOS:
        for name in BASELINES + STYLES:
            g = bl[(bl["scenario"] == sc) & (bl["baseline"] == name)] if name in BASELINES else \
                main_df[(main_df["scenario"] == sc) & (main_df["style"] == name)]
            s = {METRICS[c]: mean_ci(g[c]) for c in METRICS if c in g and g[c].notna().any()}
            ctrl = ""
            if sc == "Control":
                co = control_outcomes(g)
                s["control"] = co
                ctrl = f"{fmt(s['CtrlScore'])}; wins {co['wins']}/{co['n']}"
            S["baselines"]["per_condition"][f"{sc}|{name}"] = s
            md.append(f"| {sc} | {name} | {fmt(s.get('ObjCommit'))} | {fmt(s.get('AllyDist'))} | {fmt(s.get('EngRedirect'))} | "
                      f"{fmt(s.get('ResSeek'))} | {fmt(s.get('Kills'), 1)} | {fmt(s.get('Deaths'), 1)} | {ctrl} |")
            rows.append({"scenario": sc, "agent": name, **{c: g[c].astype(float).mean() for c in FP_COLS}})

    md.append("\n## Behaviour trees vs corresponding priority-structure styles (Mann-Whitney; r > 0: BT higher)\n")
    md.append("| Scenario | Pair | Metric | BT | Style | r | p |")
    md.append("|---|---|---|---|---|---|---|")
    for sc in SCENARIOS:
        for bt, st in PAIRS.items():
            gb = bl[(bl["scenario"] == sc) & (bl["baseline"] == bt)]
            gs = main_df[(main_df["scenario"] == sc) & (main_df["style"] == st)]
            for c in KEY[sc]:
                r = mann_whitney(gb[c], gs[c])
                r.update({"bt": mean_ci(gb[c]), "style": mean_ci(gs[c])})
                S["baselines"]["pairs"][f"{sc}|{bt}|{METRICS[c]}"] = r
                md.append(f"| {sc} | {bt} / {st} | {METRICS[c]} | {fmt(r['bt'])} | {fmt(r['style'])} | {r['r']:+.2f} | {fmt_p(r['p'])} |")

    # fingerprint matching in the normalised 4-metric space (per scenario and pooled)
    fp = pd.DataFrame(rows)
    norm = fp.copy()
    for c in FP_COLS:
        lo, hi = fp[c].min(), fp[c].max()
        norm[c] = (fp[c] - lo) / (hi - lo) if hi > lo else 0.0
    md.append("\n## Fingerprint matching (nearest priority-structure style, normalised 4-metric space)\n")
    md.append("| Baseline | " + " | ".join(SCENARIOS) + " | pooled (12-D) |")
    md.append("|---|---|---|---|---|")
    for name in BASELINES:
        nearest = []
        for sc in SCENARIOS:
            b = norm[(norm["scenario"] == sc) & (norm["agent"] == name)][FP_COLS].values[0]
            dists = {st: float(np.linalg.norm(b - norm[(norm["scenario"] == sc) & (norm["agent"] == st)][FP_COLS].values[0]))
                     for st in STYLES}
            best = min(dists, key=dists.get)
            nearest.append(f"{best} ({dists[best]:.2f})")
            S["baselines"]["fingerprint"][f"{sc}|{name}"] = dists
        vec = lambda a: np.concatenate([norm[(norm["scenario"] == sc) & (norm["agent"] == a)][FP_COLS].values[0] for sc in SCENARIOS])
        pooled = {st: float(np.linalg.norm(vec(name) - vec(st))) for st in STYLES}
        best = min(pooled, key=pooled.get)
        S["baselines"]["fingerprint"][f"pooled|{name}"] = pooled
        md.append(f"| {name} | " + " | ".join(nearest) + f" | {best} ({pooled[best]:.2f}) |")

    (d / "extra_summary.json").write_text(json.dumps(S, indent=2, ensure_ascii=False), encoding="utf-8")
    (d / "extra_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Saved: {(d / 'extra_summary.md').resolve()}")


if __name__ == "__main__":
    main()
