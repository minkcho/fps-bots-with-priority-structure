"""Analysis of Part F of the fitting experiment (2026-09-26; a copy of analyze_fitting_e.py: the same Part E fingerprint,
the Part E fits as the comparison, H-F1 / H-F2 as H-E1 / H-E2, and the question of this round -- is the Xonotic tree
approximated at least in the improved tier? -- with the retreat share of each fit and tree on the game maps).

1. The frozen Part B analysis (analyze_fitting.py) on the Part F output, with the Part E fingerprint (the four
   goal-intent metrics and the seven behavioural measures of run_fitting_e.py): distances, own-tree share, gap closure
   G with bootstrap CI, noise floor, classifier AUC, untargeted outcomes, held-out maps, Part B verdict labels
   -> fitting_summary.{json,md}.
2. The Part C tiers (close / improved / not approximated; H-F1 = at least "improved" for >= 3 of 4 trees, H-F2 =
   "close" for >= 3 of 4), the fit index 1 - G^2, and the Part E fits (fitE[...]) on the same test seeds with the
   paired bootstrap CI of G(F) - G(E) -> fitting_f_summary.{json,md}.
Usage: python experiments/analyze_fitting_f.py --dir ../repro_outputs/v8_fit [--boot 1000]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting as rf  # noqa: E402

BEHAVIOUR = ["kill_rate_per_100", "death_rate_per_100", "los_frac", "resource_goal_share_good",
             "retreat_share", "far_pursuit_share", "contact_distance"]
rf.FP[:] = rf.FP + [m for m in BEHAVIOUR if m not in rf.FP]
rf.OUTCOMES[:] = [m for m in rf.OUTCOMES if m not in rf.FP]
import analyze_fitting as af  # noqa: E402  (after the patch: af.FP is the extended fingerprint)


def tiers(d: Path, boot: int) -> None:
    summ = json.loads((d / "fitting_summary.json").read_text())
    fitted = json.loads((d / "fitted.json").read_text())
    s1b = json.loads((d / "stage1b.json").read_text())
    df = pd.read_csv(d / "test_rows.csv")
    stage0 = json.loads((d / "stage0.json").read_text())
    cells = af.Cells(df, af.FP)
    sc_game = af.scales_for(df, stage0, af.TRAIN_MAPS)
    styles = [s for s in df.agent.unique() if s in af.HAND.values() or s.endswith("[route off]")]
    rng = np.random.default_rng(8030)
    out, md = {"trees": {}}, ["# Part F: relief of the commitment penalty for urgent item switches (test seeds)", ""]
    n_improved = n_close = 0
    for g in af.TREES:
        r = summ[g]
        gm, ho = r["game_maps"], r["heldout"]
        own_ho = sum(1 for m in ho.values() if m["nearest"] == g)
        close_ho = sum(1 for m in ho.values() if m["nearest"] == g and m["G"] < 0.5)
        ident = gm["own_nearest_share"] >= 0.95
        close = ident and gm["G_ci"][1] < 0.5 and close_ho >= 4
        improved = ident and gm["G_ci"][1] < 1.0 and own_ho >= 4
        tier = "close" if close else "improved" if improved else "not approximated"
        n_close += close
        n_improved += close or improved
        fc = f"fitE[{g}]"
        gc = af.gap(cells, fc, g, styles, sc_game)
        diffs = []
        for _ in range(boot):
            idx = rng.integers(0, cells.n_ep, cells.n_ep)
            diffs.append(af.gap(cells, f"fit[{g}]", g, styles, sc_game, idx) - af.gap(cells, fc, g, styles, sc_game, idx))
        res = {"tier": tier, "mode": fitted[g]["combat_mode"], "selection_J": s1b[g]["selection_J"],
               "weights": fitted[g]["weights"], "extension": fitted[g]["extension"],
               "own_nearest_share": gm["own_nearest_share"], "G": gm["G"], "G_ci": gm["G_ci"],
               "fit_index": 1 - gm["G"] ** 2, "fit_index_ci": [1 - gm["G_ci"][1] ** 2, 1 - gm["G_ci"][0] ** 2],
               "heldout_own_nearest": own_ho, "heldout_close": close_ho, "part_b_verdict_label": r["verdict"],
               "G_part_e_same_seeds": gc, "G_diff_F_minus_E": float(np.mean(diffs)),
               "G_diff_ci": [float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))]}
        out["trees"][g] = res
        md += [f"## {g}: {tier} (mode {res['mode']})", "",
               "- parameters: " + ", ".join(f"{k} {v:.3f}" for k, v in {**res['weights'], **res['extension']}.items()),
               "- mode selection J: " + ", ".join(f"{m} {v:.2f}" for m, v in res["selection_J"].items()),
               f"- own tree nearest in {100 * res['own_nearest_share']:.0f}% of resamples; G {res['G']:.2f} "
               f"[{res['G_ci'][0]:.2f}, {res['G_ci'][1]:.2f}]; fit index 1 - G^2 = {res['fit_index']:.2f} "
               f"[{res['fit_index_ci'][0]:.2f}, {res['fit_index_ci'][1]:.2f}]",
               f"- held-out maps: own tree nearest on {own_ho}/5, with G < 0.5 on {close_ho}/5",
               f"- Part E fit on the same seeds: G {gc:.2f}; G(F) - G(E) = {res['G_diff_F_minus_E']:+.2f} "
               f"[{res['G_diff_ci'][0]:+.2f}, {res['G_diff_ci'][1]:+.2f}]",
               f"- verdict under the Part B definitions: {r['verdict']}", ""]
    out["H_F1_improved_3_of_4"] = n_improved >= 3
    out["H_F2_close_3_of_4"] = n_close >= 3
    xo = out["trees"]["XO-BT"]["tier"]
    out["XO_at_least_improved"] = xo in ("close", "improved")
    md += [f"H-F1 (at least 'improved' on >= 3 of 4 trees): {n_improved}/4 -> {'met' if n_improved >= 3 else 'not met'}",
           f"H-F2 ('close' on >= 3 of 4 trees): {n_close}/4 -> {'met' if n_close >= 3 else 'not met'}",
           f"Question of this round (Xonotic tree at least 'improved'): {'yes' if out['XO_at_least_improved'] else 'no'} ({xo})"]
    game = df[df["map"].isin(af.TRAIN_MAPS)]
    ret = pd.to_numeric(game["retreat_share"], errors="coerce").groupby(game["agent"]).mean()
    out["retreat_share_game_maps"] = {a: float(ret[a]) for a in ret.index
                                      if a in af.TREES or a.startswith("fit[") or a.startswith("fitE[")}
    md += ["", "Retreat share on the game maps (mean over maps, scenarios and episodes): "
           + "; ".join(f"{g} tree {ret[g]:.2f}, fit {ret[f'fit[{g}]']:.2f}, Part E fit {ret[f'fitE[{g}]']:.2f}"
                       for g in af.TREES)]
    (d / "fitting_f_summary.json").write_text(json.dumps(out, indent=1, default=float))
    (d / "fitting_f_summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="../repro_outputs/v8_fit")
    p.add_argument("--boot", type=int, default=1000)
    a = p.parse_args()
    sys.argv = [sys.argv[0], "--dir", a.dir]
    af.main()
    tiers(Path(a.dir), a.boot)


if __name__ == "__main__":
    main()
