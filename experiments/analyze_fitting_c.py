"""Analysis of Part C of the fitting experiment (parameter regression; 2026-09-25).

Runs after the frozen analyze_fitting.py has written fitting_summary.json for the Part C output directory (same
distances, gap closure G, bootstrap, noise floor, classifier and untargeted outcomes as Part B). Adds:
  tiers       per tree, the pre-registered regression tiers
                close       own tree nearest in >= 95% of resamples on the game maps, upper 95% CI of G < 0.5, and own
                            tree nearest with G < 0.5 on >= 4 of the 5 held-out maps (= Part B's "success")
                improved    own tree nearest in >= 95% of resamples, upper 95% CI of G < 1 (closer than every designed
                            style), and own tree nearest on >= 4 of the 5 held-out maps
                not approximated  otherwise
  fit index   1 - G^2 with its bootstrap CI: the share of the squared distance left by the closest designed style
              that the fitted parameters remove
  Part B      the Part B fits (fitB[...]) on the same test seeds: their G, and the paired bootstrap CI of
              G(Part C) - G(Part B)
  headlines   H-C1: >= 3 of 4 trees at least "improved"; H-C2: >= 3 of 4 trees "close"
Output: <dir>/fitting_c_summary.{json,md}
Usage: python experiments/analyze_fitting_c.py --dir ../repro_outputs/v5_fit [--boot 1000]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyze_fitting as af  # noqa: E402  (frozen Part B analysis: distances, gap closure)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="../repro_outputs/v5_fit")
    p.add_argument("--boot", type=int, default=1000)
    a = p.parse_args()
    d = Path(a.dir)
    summ = json.loads((d / "fitting_summary.json").read_text())
    fitted = json.loads((d / "fitted.json").read_text())
    s1b = json.loads((d / "stage1b.json").read_text())
    df = pd.read_csv(d / "test_rows.csv")
    stage0 = json.loads((d / "stage0.json").read_text())
    cells = af.Cells(df, af.FP)
    sc_game = af.scales_for(df, stage0, af.TRAIN_MAPS)
    styles = [s for s in df.agent.unique() if s in af.HAND.values() or s.endswith("[route off]")]
    rng = np.random.default_rng(4030)
    out, md = {"trees": {}}, ["# Part C: parameter regression (test seeds; game maps unless stated)", ""]
    n_improved = n_close = 0
    for g in af.TREES:
        r = summ[g]
        gm = r["game_maps"]
        ho = r["heldout"]
        own_ho = sum(1 for m in ho.values() if m["nearest"] == g)
        close_ho = sum(1 for m in ho.values() if m["nearest"] == g and m["G"] < 0.5)
        ident = gm["own_nearest_share"] >= 0.95
        close = ident and gm["G_ci"][1] < 0.5 and close_ho >= 4
        improved = ident and gm["G_ci"][1] < 1.0 and own_ho >= 4
        tier = "close" if close else "improved" if improved else "not approximated"
        n_close += close
        n_improved += close or improved
        # Part B fit on the same test seeds, paired bootstrap of the difference in G
        fb = f"fitB[{g}]"
        gb = af.gap(cells, fb, g, styles, sc_game)
        diffs = []
        for _ in range(a.boot):
            idx = rng.integers(0, cells.n_ep, cells.n_ep)
            diffs.append(af.gap(cells, f"fit[{g}]", g, styles, sc_game, idx) - af.gap(cells, fb, g, styles, sc_game, idx))
        res = {"tier": tier, "mode": fitted[g]["combat_mode"], "selection_J": s1b[g]["selection_J"],
               "weights": fitted[g]["weights"], "extension": fitted[g]["extension"],
               "own_nearest_share": gm["own_nearest_share"], "G": gm["G"], "G_ci": gm["G_ci"],
               "fit_index": 1 - gm["G"] ** 2, "fit_index_ci": [1 - gm["G_ci"][1] ** 2, 1 - gm["G_ci"][0] ** 2],
               "heldout_own_nearest": own_ho, "heldout_close": close_ho, "part_b_verdict_label": r["verdict"],
               "G_part_b_same_seeds": gb, "G_diff_C_minus_B": float(np.mean(diffs)),
               "G_diff_ci": [float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))]}
        out["trees"][g] = res
        md += [f"## {g}: {tier} (mode {res['mode']})", "",
               "- parameters: " + ", ".join(f"{k} {v:.3f}" for k, v in {**res['weights'], **res['extension']}.items()),
               "- mode selection J: " + ", ".join(f"{m} {v:.2f}" for m, v in res["selection_J"].items()),
               f"- own tree nearest in {100 * res['own_nearest_share']:.0f}% of resamples; G {res['G']:.2f} "
               f"[{res['G_ci'][0]:.2f}, {res['G_ci'][1]:.2f}]; fit index 1 - G^2 = {res['fit_index']:.2f} "
               f"[{res['fit_index_ci'][0]:.2f}, {res['fit_index_ci'][1]:.2f}]",
               f"- held-out maps: own tree nearest on {own_ho}/5, with G < 0.5 on {close_ho}/5",
               f"- Part B fit on the same seeds: G {gb:.2f}; G(C) - G(B) = {res['G_diff_C_minus_B']:+.2f} "
               f"[{res['G_diff_ci'][0]:+.2f}, {res['G_diff_ci'][1]:+.2f}]",
               f"- verdict under the Part B definitions: {r['verdict']}", ""]
    out["H_C1_improved_3_of_4"] = n_improved >= 3
    out["H_C2_close_3_of_4"] = n_close >= 3
    md += [f"H-C1 (at least 'improved' on >= 3 of 4 trees): {n_improved}/4 -> {'met' if n_improved >= 3 else 'not met'}",
           f"H-C2 ('close' on >= 3 of 4 trees): {n_close}/4 -> {'met' if n_close >= 3 else 'not met'}"]
    (d / "fitting_c_summary.json").write_text(json.dumps(out, indent=1, default=float))
    (d / "fitting_c_summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
