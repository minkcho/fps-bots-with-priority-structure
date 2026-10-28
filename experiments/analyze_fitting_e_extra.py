"""Exploratory additions to Part E of the fitting experiment (2026-09-26; not part of the frozen analysis).

From the saved Part E outputs (no new episodes), on the Part E fingerprint (the four goal-intent metrics and the seven
behavioural measures; distances and scales exactly as in analyze_fitting.py):
  contributions  contribution of each metric to D2(fit, own tree) on the game maps (the bias-corrected terms of the
                 metric's dimensions divided by the number of dimensions, so the contributions sum to D2), for the
                 fits and for the previous round's fits on the same seeds (--prev: fitD for Part E, fitE for Part F)
  xonotic        per metric, the contributions to D2(fit[XO-BT], XO-BT) and to D2(fit[XO-BT], AC-BT): which metrics
                 put the Xonotic fit nearer the AssaultCube tree; the same for the two trees against each other
  means          mean of each behavioural measure per agent and scenario, on the game maps and on the held-out maps
Output: <dir>/fitting_e_extra.md
Usage: python experiments/analyze_fitting_e_extra.py --dir ../repro_outputs/v7_fit [--prev fitD]
       python experiments/analyze_fitting_e_extra.py --dir ../repro_outputs/v8_fit --prev fitE   (Part F)
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
import analyze_fitting as af  # noqa: E402  (after the patch: af.FP is the Part E fingerprint)

SHORT = {"objective_commitment_ratio": "commitment", "engagement_redirection_rate_per_100": "redirection",
         "resource_seeking_rate_per_100": "resource seeking", "avg_ally_proximity": "ally distance",
         "kill_rate_per_100": "kill rate", "death_rate_per_100": "death rate", "los_frac": "contact share",
         "resource_goal_share_good": "item control", "retreat_share": "retreat", "far_pursuit_share": "far pursuit",
         "contact_distance": "contact distance"}


def terms(cells, a, b, scales) -> dict:
    t = {}
    for d, s in scales.items():
        ma, va, na = cells.stats(a, d)
        mb, vb, nb = cells.stats(b, d)
        if na and nb:
            t[d] = ((ma - mb) ** 2 - va / na - vb / nb) / s ** 2
    return t


def by_metric(t: dict) -> dict:
    n = len(t)
    return {m: sum(v for d, v in t.items() if d[2] == m) / n for m in af.FP}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="../repro_outputs/v7_fit")
    p.add_argument("--prev", default="fitD", help="label prefix of the previous round's fits (fitD, fitE)")
    a = p.parse_args()
    pv = a.prev
    d = Path(a.dir)
    df = pd.read_csv(d / "test_rows.csv")
    stage0 = json.loads((d / "stage0.json").read_text())
    cells = af.Cells(df, af.FP)
    sc = af.scales_for(df, stage0, af.TRAIN_MAPS)
    out = {"contributions": {}, "xonotic": {}, "means": {}}
    part = {"fitD": "E", "fitE": "F"}.get(pv, "?")
    md = [f"# Part {part}: exploratory additions (game maps, test seeds; not part of the frozen analysis)", ""]

    md += ["## Contribution of each metric to D2(fit, own tree)", "",
           "| metric | " + " | ".join(f"{g} fit | {g} {pv}" for g in af.TREES) + " |",
           "|---|" + "---|---|" * len(af.TREES)]
    contrib = {}
    for g in af.TREES:
        contrib[g] = {"fit": by_metric(terms(cells, f"fit[{g}]", g, sc)), pv: by_metric(terms(cells, f"{pv}[{g}]", g, sc))}
    for m in af.FP:
        md.append(f"| {SHORT[m]} | " + " | ".join(f"{contrib[g]['fit'][m]:.2f} | {contrib[g][pv][m]:.2f}"
                                                  for g in af.TREES) + " |")
    md.append("| **D2** | " + " | ".join(f"{sum(contrib[g]['fit'].values()):.2f} | {sum(contrib[g][pv].values()):.2f}"
                                          for g in af.TREES) + " |")
    out["contributions"] = contrib

    pairs = {"fit[XO-BT] vs XO-BT": ("fit[XO-BT]", "XO-BT"), "fit[XO-BT] vs AC-BT": ("fit[XO-BT]", "AC-BT"),
             f"{pv}[XO-BT] vs XO-BT": (f"{pv}[XO-BT]", "XO-BT"), f"{pv}[XO-BT] vs AC-BT": (f"{pv}[XO-BT]", "AC-BT"),
             "fit[AC-BT] vs AC-BT": ("fit[AC-BT]", "AC-BT"), "fit[AC-BT] vs XO-BT": ("fit[AC-BT]", "XO-BT"),
             "AC-BT vs XO-BT": ("AC-BT", "XO-BT")}
    xo = {k: by_metric(terms(cells, x, y, sc)) for k, (x, y) in pairs.items()}
    out["xonotic"] = xo
    md += ["", "## The two deathmatch trees: contributions to D2 by metric", "",
           "| metric | " + " | ".join(pairs) + " |", "|---|" + "---|" * len(pairs)]
    for m in af.FP:
        md.append(f"| {SHORT[m]} | " + " | ".join(f"{xo[k][m]:.2f}" for k in pairs) + " |")
    md.append("| **D2** | " + " | ".join(f"{sum(xo[k].values()):.2f}" for k in pairs) + " |")

    agents = af.TREES + [f"fit[{g}]" for g in af.TREES] + [f"{pv}[{g}]" for g in af.TREES]
    for label, maps in (("game maps", af.TRAIN_MAPS), ("held-out maps", af.HELDOUT_MAPS)):
        sub = df[df["map"].isin(maps) & df.agent.isin(agents)]
        g = sub.groupby(["agent", "scenario"])[BEHAVIOUR + ["objective_commitment_ratio",
                                                            "engagement_redirection_rate_per_100",
                                                            "resource_seeking_rate_per_100"]].mean()
        out["means"][label] = {f"{ag}|{s}": g.loc[(ag, s)].to_dict() for ag, s in g.index}
        for s in af.SCENARIOS:
            cols = BEHAVIOUR
            md += ["", f"## Means, {label}, {s}", "", "| agent | " + " | ".join(SHORT[c] for c in cols) + " |",
                   "|---|" + "---|" * len(cols)]
            for ag in agents:
                if (ag, s) in g.index:
                    md.append(f"| {ag} | " + " | ".join(f"{g.loc[(ag, s), c]:.3f}" for c in cols) + " |")
    (d / "fitting_e_extra.json").write_text(json.dumps(out, indent=1, default=float))
    (d / "fitting_e_extra.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
