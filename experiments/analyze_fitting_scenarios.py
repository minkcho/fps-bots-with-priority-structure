"""Exploratory per-scenario breakdown of a fitting round (2026-09-28; user: "결과 나오면 시나리오별로 정리해서 보여줘").

Generalises analyze_fitting_g_scenarios.py (Part G-fit) to the other rounds with source-based trees: Part D
(repro_outputs/v6_fit, Part D fingerprint), Part E (v7_fit), Part F (v8_fit) and Part G-eval (v10_eval) (Part E
fingerprint). The pre-registered analyses pool the three scenarios; here the same definitions (analyze_fitting.py
helpers d2 / gap / scales_for, the round's fingerprint and stage-0 scales, test-seed scales on each held-out map) are
restricted to the dimensions of one scenario at a time. Native scenarios: Mission and Control for CSO-BT and OW-BT,
Deathmatch for AC-BT and XO-BT.
Fits: every agent whose label starts with "fit" (fit[...], fitC[...], fitD[...], fitE[...]); the own tree is the label
in brackets. Trees: the four labels CSO-BT, OW-BT, AC-BT, XO-BT of the round's test rows (in G-eval the adopted trees;
the earlier trees AC-BT[0925] and XO-BT[step] of G-eval are not used here).
Per scenario and fit: D2 to the four trees on the game maps, the share of bootstrap resamples (episode indices, paired)
with the own tree nearest, G with 95% CI, the held-out maps with the own tree nearest (and with G < 0.5), and the tier
rule of Parts C-F applied to the scenario (exploratory label only); per scenario, the means of the fingerprint metrics
of the trees and the round's fits (fit[...]) on the game maps. Nothing is simulated.
Usage: python experiments/analyze_fitting_scenarios.py --dir ../repro_outputs/v7_fit --fingerprint e \
         --out ../repro_outputs/v7_fit_scenarios
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting as rf  # noqa: E402

GAMES = ["CSO-BT", "OW-BT", "AC-BT", "XO-BT"]
NATIVE = {"CSO-BT": {"Mission", "Control"}, "OW-BT": {"Mission", "Control"}, "AC-BT": {"Deathmatch"},
          "XO-BT": {"Deathmatch"}}
BEHAVIOUR_D = ["kill_rate_per_100", "death_rate_per_100", "los_frac", "resource_goal_share_good"]
BEHAVIOUR_E = BEHAVIOUR_D + ["retreat_share", "far_pursuit_share", "contact_distance"]
SHORT = {"objective_commitment_ratio": "obj", "engagement_redirection_rate_per_100": "redir",
         "resource_seeking_rate_per_100": "res", "avg_ally_proximity": "ally", "kill_rate_per_100": "kills",
         "death_rate_per_100": "deaths", "los_frac": "los", "resource_goal_share_good": "item",
         "retreat_share": "retreat", "far_pursuit_share": "far", "contact_distance": "contact"}


def tier(own_share, g_ci, own_ho, close_ho) -> str:
    """The tier rule of Parts C-F (as analyze_fitting_g_eval.tier, copied: importing that module would patch the
    Part E fingerprint)."""
    ident = own_share >= 0.95
    if ident and g_ci[1] < 0.5 and close_ho >= 4:
        return "close"
    if ident and g_ci[1] < 1.0 and own_ho >= 4:
        return "improved"
    return "not approximated"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", required=True)
    p.add_argument("--fingerprint", required=True, choices=["d", "e"])
    p.add_argument("--out", required=True)
    p.add_argument("--boot", type=int, default=1000)
    a = p.parse_args()
    extra = BEHAVIOUR_D if a.fingerprint == "d" else BEHAVIOUR_E      # as run_fitting_d.py / run_fitting_e.py
    rf.FP[:] = rf.FP + [m for m in extra if m not in rf.FP]
    rf.OUTCOMES[:] = [m for m in rf.OUTCOMES if m not in rf.FP]
    import analyze_fitting as af  # noqa: E402  (after the patch)

    d, out_dir = Path(a.dir), Path(a.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(d / "test_rows.csv")
    stage0 = json.loads((d / "stage0.json").read_text())
    cells = af.Cells(df, af.FP)
    styles = [s for s in df.agent.unique() if s in af.HAND.values() or s.endswith("[route off]")]
    sc_game = af.scales_for(df, stage0, af.TRAIN_MAPS)
    heldout = [m for m in af.HELDOUT_MAPS if m in set(df["map"])]
    sc_ho = {m: af.scales_for(df, stage0, [m]) for m in heldout}
    fits = sorted((x for x in df.agent.unique() if re.match(r"fit[A-Z]?\[", x)), key=lambda x: (x[3] != "[", x))
    own = {f: re.search(r"\[(.+)\]", f).group(1) for f in fits}
    rng = np.random.default_rng(11030)
    ci = lambda x: [float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))]  # noqa: E731

    res: dict = {"dir": str(d), "fingerprint": a.fingerprint, "scenarios": {}, "behaviour": {}}
    md = [f"# Per-scenario breakdown of {d.name} (exploratory; the pre-registered analysis pools the three scenarios)", "",
          f"Fingerprint: Part {a.fingerprint.upper()}; same definitions as the frozen analysis, restricted to one "
          "scenario's dimensions; native scenarios marked *.", ""]
    for scen in af.SCENARIOS:
        sg = {k: v for k, v in sc_game.items() if k[1] == scen}
        sh = {m: {k: v for k, v in sc_ho[m].items() if k[1] == scen} for m in heldout}
        boot = {f: {"own": 0, "G": []} for f in fits}
        for _ in range(a.boot):
            idx = rng.integers(0, cells.n_ep, cells.n_ep)
            den = {t: min(max(af.d2(cells, s, t, sg, idx), 1e-12) for s in styles) for t in GAMES}
            for f in fits:
                dd = {t: af.d2(cells, f, t, sg, idx) for t in GAMES}
                boot[f]["own"] += min(dd, key=dd.get) == own[f]
                boot[f]["G"].append(math.sqrt(max(dd[own[f]], 0.0) / den[own[f]]))
        rows = {}
        for f in fits:
            g = own[f]
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

    measures = [m for m in af.FP if m in df.columns]
    md += ["## Behaviour per scenario (game maps; means over maps and episodes)", "",
           "| scenario | agent | " + " | ".join(SHORT.get(m, m) for m in measures) + " |",
           "|---|---|" + "---|" * len(measures)]
    game = df[df["map"].isin(af.TRAIN_MAPS)]
    for scen in af.SCENARIOS:
        for ag in [x for g in GAMES for x in (g, f"fit[{g}]") if x in set(df.agent)]:
            sub = game[(game.agent == ag) & (game.scenario == scen)]
            vals = {m: float(pd.to_numeric(sub[m], errors="coerce").mean()) for m in measures}
            res["behaviour"][f"{scen}|{ag}"] = vals
            md.append(f"| {scen} | {ag} | " + " | ".join("--" if math.isnan(v) else f"{v:.2f}" for v in vals.values())
                      + " |")
    (out_dir / "scenario_breakdown.json").write_text(json.dumps(res, indent=1, default=float))
    (out_dir / "scenario_breakdown.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
