"""Exploratory, not part of the frozen protocol FITTING_PLAN_I_2026-09-30.md (written 2026-09-30 after the results, for
the text of Section 9 of the journal draft): supporting quantities from the stored test episodes of Round I. Nothing is
simulated; reads <dir>/test_rows.csv, <dir>/stage0.json and <dir>/fitted.json.

Per case (the case fit fitsc[<tree>:<scenario>] against its tree, game maps, the case's scenario):
  (1) the denominator of G: D2 of every designed style and route-off version to the tree on the scenario's dimensions,
      the nearest one and its D2; D2(fit, tree)
  (2) noise floor (as item (c) of analyze_fitting.py): D(fit[S1], tree[S2]) against D(tree[S1], tree[S2]) over 1000
      random splits S1/S2 of the episode indices; "within" if the mean of the former is at most the 95th percentile of
      the latter
  (3) classifier two-sample test (analyze_fitting.classifier: logistic regression, 5-fold cross-validation, out-of-fold
      AUC with a bootstrap CI, permutation p) on the fingerprint metrics, on the episodes of the case's scenario
  (4) untargeted outcomes (as item (e) of analyze_fitting.py): Cohen's d of fit minus tree for kills, deaths, hits taken
      per step and, in Control, wins
  (5) the active weights in Deathmatch: the scenario has no objective candidate, so w_objective is not used there; the
      three other goal weights renormalised to sum 1 and the commitment weight divided by the same sum
Usage: python experiments/analyze_fitting_i_extra.py --dir ../repro_outputs/v16_scenario_fit
           --out ../repro_outputs/v16_scenario_fit_extra [--perm 1000 --boot 1000 --splits 1000]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting_f  # noqa: E402,F401  (Part E fingerprint patched into run_fitting before analyze_fitting is imported)
import analyze_fitting as af  # noqa: E402

GAMES = ["CSO-BT", "OW-BT", "AC-BT", "XO-BT"]
NATIVE = {"CSO-BT": ["Mission", "Control"], "OW-BT": ["Mission", "Control"], "AC-BT": ["Deathmatch"],
          "XO-BT": ["Deathmatch"]}
CASES = [(g, sc) for g in GAMES for sc in NATIVE[g]]
OUTCOMES = ["kills", "deaths", "hits_taken_per_step", "win"]
STREAM = 160301


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="../repro_outputs/v16_scenario_fit")
    p.add_argument("--out", default="../repro_outputs/v16_scenario_fit_extra")
    p.add_argument("--perm", type=int, default=1000)
    p.add_argument("--boot", type=int, default=1000)
    p.add_argument("--splits", type=int, default=1000)
    a = p.parse_args()
    d, out_dir = Path(a.dir), Path(a.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(d / "test_rows.csv")
    df["win"] = ((df.scenario == "Control") & (pd.to_numeric(df.control_score, errors="coerce") >= 120)).astype(float)
    df.loc[df.scenario != "Control", "win"] = np.nan
    stage0 = json.loads((d / "stage0.json").read_text())
    fitted = json.loads((d / "fitted.json").read_text())
    cells = af.Cells(df, af.FP)
    styles = [s for s in df.agent.unique() if s in af.HAND.values() or s.endswith("[route off]")]
    sc_game_all = af.scales_for(df, stage0, af.TRAIN_MAPS)
    rng = np.random.default_rng(STREAM)
    res: dict = {}
    md = ["# Round I (v16), exploratory supplement: denominators, noise floor, classifier, outcomes (stored test episodes; "
          "not part of the frozen protocol)", ""]
    for g, sc in CASES:
        key, fit = f"{g}|{sc}", f"fitsc[{g}:{sc}]"
        sg = {k: v for k, v in sc_game_all.items() if k[1] == sc}
        # (1) denominators
        dst = {s: af.d2(cells, s, g, sg) for s in styles}
        near = min(dst, key=dst.get)
        d_fit = af.d2(cells, fit, g, sg)
        # (2) noise floor
        fl, fs = [], []
        for _ in range(a.splits):
            perm = rng.permutation(cells.n_ep)
            s1, s2 = perm[: cells.n_ep // 2], perm[cells.n_ep // 2:]
            fl.append(af.dplain(cells, g, g, sg, s1, s2))
            fs.append(af.dplain(cells, fit, g, sg, s1, s2))
        floor = {"fit_mean": float(np.mean(fs)), "tree_p95": float(np.percentile(fl, 95)),
                 "within": float(np.mean(fs)) <= float(np.percentile(fl, 95))}
        # (3) classifier on the case's scenario
        sub = df[df.scenario == sc]
        clf = af.classifier(sub, fit, g, af.TRAIN_MAPS, af.FP, rng, a.perm, a.boot)
        # (4) outcomes
        eff = {}
        for c in OUTCOMES:
            if c == "win" and sc != "Control":
                continue
            x = sub[(sub.agent == fit) & sub["map"].isin(af.TRAIN_MAPS)][c]
            y = sub[(sub.agent == g) & sub["map"].isin(af.TRAIN_MAPS)][c]
            eff[c] = af.cohens_d(pd.to_numeric(x, errors="coerce"), pd.to_numeric(y, errors="coerce"))
        means = {c: {"fit": float(pd.to_numeric(sub[(sub.agent == fit) & sub["map"].isin(af.TRAIN_MAPS)][c],
                                                  errors="coerce").mean()),
                     "tree": float(pd.to_numeric(sub[(sub.agent == g) & sub["map"].isin(af.TRAIN_MAPS)][c],
                                                   errors="coerce").mean())} for c in eff}
        # (5) active weights in Deathmatch
        pr = fitted[key]["params"]
        active = None
        if sc == "Deathmatch":
            tot = pr["w_engage"] + pr["w_resource"] + pr["w_team"]
            active = {"w_engage": pr["w_engage"] / tot, "w_resource": pr["w_resource"] / tot, "w_team": pr["w_team"] / tot,
                      "w_commitment": pr["w_commitment"] / tot, "sum_of_active_weights": tot}
        res[key] = {"D2_fit": d_fit, "D2_styles": dst, "nearest_style": near, "D2_nearest_style": dst[near],
                    "G": float(np.sqrt(max(d_fit, 0.0) / max(dst[near], 1e-12))), "noise_floor": floor, "classifier": clf,
                    "cohens_d": eff, "outcome_means": means, "active_weights_deathmatch": active}
        md += [f"## {g} in {sc}", "",
               f"- D2(fit, tree) {d_fit:.2f}; nearest designed style {near} at D2 {dst[near]:.2f} (G {res[key]['G']:.2f}); "
               "all styles: " + ", ".join(f"{s} {v:.2f}" for s, v in sorted(dst.items(), key=lambda kv: kv[1])),
               f"- noise floor: fit {floor['fit_mean']:.3f} vs tree 95th percentile {floor['tree_p95']:.3f} -> "
               + ("within" if floor["within"] else "outside"),
               f"- classifier AUC {clf['auc']:.3f} (CI {clf['ci'][0]:.3f}-{clf['ci'][1]:.3f}, permutation p {clf['p_perm']:.4f})",
               "- Cohen's d (fit - tree): " + ", ".join(f"{c} {v:+.2f}" for c, v in eff.items())
               + "; means fit / tree: " + ", ".join(f"{c} {m['fit']:.3f} / {m['tree']:.3f}" for c, m in means.items())]
        if active:
            md.append("- active weights (Deathmatch has no objective candidate): "
                      + ", ".join(f"{k} {v:.3f}" for k, v in active.items()))
        md.append("")
    (out_dir / "extra.json").write_text(json.dumps(res, indent=1, default=float))
    (out_dir / "extra.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
