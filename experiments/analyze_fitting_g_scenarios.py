"""Exploratory, not part of the frozen protocol FITTING_PLAN_G_FIT_2026-09-28.md (user question 2026-09-28: "합친 결과
말고, 시나리오별 결과가 있나?"): the Part G-fit fits and the six comparison fits scenario by scenario.

The pre-registered fingerprint pools the three scenarios (119 dimensions over 4 game maps x 3 scenarios), so D2, G and
the nearest tree of the frozen analysis are pooled. Here the same definitions (analyze_fitting.py helpers d2 / gap /
scales_for, the Part E fingerprint, the stage-0 scales of the run, test-seed scales on each held-out map) are
restricted to the dimensions of one scenario at a time. Native scenarios (the game modes the trees were written for):
Mission and Control for CSO-BT and OW-BT, Deathmatch for AC-BT and XO-BT.
Per scenario and fit: D2 to the four adopted trees on the game maps, the share of bootstrap resamples (episode
indices, paired) with the own tree nearest, G with 95% CI, the held-out maps with the own tree nearest (and with
G < 0.5), and the tier rule of Parts C-F applied to the scenario (exploratory label only); per scenario, the means of
the goal-intent metrics and the behavioural measures of the trees and the new fits on the game maps.
Nothing is simulated; reads <dir>/test_rows.csv and <dir>/stage0.json.
Usage: python experiments/analyze_fitting_g_scenarios.py --dir ../repro_outputs/v11_fit --out ../repro_outputs/v11_fit_scenarios
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting_f  # noqa: E402,F401  (Part E fingerprint patched into run_fitting before analyze_fitting is imported)
import analyze_fitting as af  # noqa: E402
from analyze_fitting_g_eval import tier  # noqa: E402

GAMES = ["CSO-BT", "OW-BT", "AC-BT", "XO-BT"]
FITS = {**{f"fit[{g}]": g for g in GAMES}, "fitF[CSO-BT]": "CSO-BT", "fitF[OW-BT]": "OW-BT", "fitF[AC-BT]": "AC-BT",
        "fitF[XO-BT]": "XO-BT", "fitD[XO-BT]": "XO-BT", "fitE[XO-BT]": "XO-BT"}
NATIVE = {"CSO-BT": {"Mission", "Control"}, "OW-BT": {"Mission", "Control"}, "AC-BT": {"Deathmatch"},
          "XO-BT": {"Deathmatch"}}
MEASURES = ["objective_commitment_ratio", "engagement_redirection_rate_per_100", "resource_seeking_rate_per_100",
            "avg_ally_proximity", "kill_rate_per_100", "death_rate_per_100", "retreat_share", "far_pursuit_share",
            "resource_goal_share_good", "contact_distance"]
SHORT = {"objective_commitment_ratio": "obj", "engagement_redirection_rate_per_100": "redir",
         "resource_seeking_rate_per_100": "res", "avg_ally_proximity": "ally", "kill_rate_per_100": "kills",
         "death_rate_per_100": "deaths", "retreat_share": "retreat", "far_pursuit_share": "far",
         "resource_goal_share_good": "item", "contact_distance": "contact"}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="../repro_outputs/v11_fit")
    p.add_argument("--out", default="../repro_outputs/v11_fit_scenarios")
    p.add_argument("--boot", type=int, default=1000)
    a = p.parse_args()
    d, out_dir = Path(a.dir), Path(a.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(d / "test_rows.csv")
    stage0 = json.loads((d / "stage0.json").read_text())
    cells = af.Cells(df, af.FP)
    styles = [s for s in df.agent.unique() if s in af.HAND.values() or s.endswith("[route off]")]
    sc_game = af.scales_for(df, stage0, af.TRAIN_MAPS)
    heldout = [m for m in af.HELDOUT_MAPS if m in set(df["map"])]
    sc_ho = {m: af.scales_for(df, stage0, [m]) for m in heldout}
    fits = [f for f in FITS if f in set(df.agent)]
    rng = np.random.default_rng(11030)
    ci = lambda x: [float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))]  # noqa: E731

    res: dict = {"scenarios": {}, "behaviour": {}}
    md = ["# Part G-fit per scenario (exploratory; the pre-registered analysis pools the three scenarios)", "",
          "Same definitions as the frozen analysis, restricted to one scenario's dimensions; native scenarios marked *.", ""]
    for scen in af.SCENARIOS:
        sg = {k: v for k, v in sc_game.items() if k[1] == scen}
        sh = {m: {k: v for k, v in sc_ho[m].items() if k[1] == scen} for m in heldout}
        boot = {f: {"own": 0, "G": []} for f in fits}
        for _ in range(a.boot):
            idx = rng.integers(0, cells.n_ep, cells.n_ep)
            den = {t: min(max(af.d2(cells, s, t, sg, idx), 1e-12) for s in styles) for t in GAMES}
            for f in fits:
                dd = {t: af.d2(cells, f, t, sg, idx) for t in GAMES}
                boot[f]["own"] += min(dd, key=dd.get) == FITS[f]
                boot[f]["G"].append(math.sqrt(max(dd[FITS[f]], 0.0) / den[FITS[f]]))
        rows = {}
        for f in fits:
            g = FITS[f]
            dist = {t: af.d2(cells, f, t, sg) for t in GAMES}
            ho = {}
            for m in heldout:
                dm = {t: af.d2(cells, f, t, sh[m]) for t in GAMES}
                ho[m] = {"nearest": min(dm, key=dm.get), "G": af.gap(cells, f, g, styles, sh[m])}
            own_ho = sum(1 for v in ho.values() if v["nearest"] == g)
            close_ho = sum(1 for v in ho.values() if v["nearest"] == g and v["G"] < 0.5)
            share, g_ci = boot[f]["own"] / a.boot, ci(boot[f]["G"])
            rows[f] = {"tree": g, "native": scen in NATIVE[g], "n_dims": len(sg), "D2": dist,
                       "nearest": min(dist, key=dist.get), "own_nearest_share": share,
                       "G": af.gap(cells, f, g, styles, sg), "G_ci": g_ci, "heldout": ho,
                       "heldout_own_nearest": own_ho, "heldout_close": close_ho,
                       "tier": tier(share, g_ci, own_ho, close_ho)}
        res["scenarios"][scen] = rows
        md += [f"## {scen} ({len(sg)} dimensions on the game maps)", "",
               "| fit | tree | nearest tree | own nearest | G [95% CI] | held-out own (G<0.5) | tier (exploratory) |",
               "|---|---|---|---|---|---|---|"]
        for f, r in rows.items():
            md.append(f"| {f} | {r['tree']}{'*' if r['native'] else ''} | {r['nearest']} | "
                      f"{100 * r['own_nearest_share']:.0f}% | {r['G']:.2f} [{r['G_ci'][0]:.2f}, {r['G_ci'][1]:.2f}] | "
                      f"{r['heldout_own_nearest']}/5 ({r['heldout_close']}/5) | {r['tier']} |")
        md.append("")

    # behaviour per scenario (game maps): trees and new fits
    md += ["## Behaviour per scenario (game maps; means over maps and episodes)", "",
           "| scenario | agent | " + " | ".join(SHORT[m] for m in MEASURES) + " |",
           "|---|---|" + "---|" * len(MEASURES)]
    game = df[df["map"].isin(af.TRAIN_MAPS)]
    for scen in af.SCENARIOS:
        for ag in [x for g in GAMES for x in (g, f"fit[{g}]")]:
            sub = game[(game.agent == ag) & (game.scenario == scen)]
            vals = {m: float(pd.to_numeric(sub[m], errors="coerce").mean()) for m in MEASURES}
            res["behaviour"][f"{scen}|{ag}"] = vals
            md.append(f"| {scen} | {ag} | " + " | ".join("--" if math.isnan(v) else f"{v:.2f}" for v in vals.values())
                      + " |")
    (out_dir / "scenario_breakdown.json").write_text(json.dumps(res, indent=1, default=float))
    (out_dir / "scenario_breakdown.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
