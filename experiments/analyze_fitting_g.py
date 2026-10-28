"""Analysis of Part G-fit (DRAFT protocol FITTING_PLAN_G_FIT_DRAFT.md, 2026-09-27; not frozen): the new fits of the four
trees against the adopted trees, with the six earlier fits as pre-specified comparisons on the same test seeds.

1. The frozen Part B analysis (analyze_fitting.py) on the Part G-fit output with the Part E fingerprint, as in Parts E
   and F -> fitting_summary.{json,md} (distances, own-tree share, G with bootstrap CI, noise floor, classifier AUC,
   untargeted outcomes, held-out maps of the new fits fit[...]).
2. Tiers of the new fits from fitting_summary.json, as in analyze_fitting_f.tiers (close / improved / not
   approximated), the fit index 1 - G^2, H-G1 (at least "improved" for >= 3 of 4 trees), H-G2 ("close" for >= 3 of 4),
   the two questions of the round ((a) all four trees at least improved? (b) the Xonotic tree close?), the stage-1b
   selection objectives of the four modes, the searched and fitted modes (and whether the fitted mode is the
   first-ranked one), and the validation objectives of the finalists and of the earlier fits (diagnostic: the six
   comparisons and fitE[OW-BT]).
3. The six earlier fits on the new test seeds (fitF[...], fitD[XO-BT], fitE[XO-BT]): D2 to the four adopted trees,
   share of bootstrap resamples with the own tree nearest, G with 95% CI, held-out maps with the own tree nearest (and
   with G < 0.5), tier (definitions of Part G-eval); paired bootstrap CIs (same resamples) of G(fit[g]) - G(fitF[g])
   for every tree and of G(fit[XO-BT]) - G(fitD[XO-BT]).
4. Exploratory (no criteria): retreat, far pursuit, item control and contact distance of trees and fits (Deathmatch and
   all scenarios, both map families) and the contribution of each fingerprint metric to D2(fit, own tree).
5. The predictions of the plan, each marked met / not met.
-> fitting_g_summary.{json,md}
Usage: python experiments/analyze_fitting_g.py --dir ../repro_outputs/v11_fit [--boot 1000 --perm 2000 --splits 1000]
(the defaults are those of the frozen Part B analysis; smoke tests pass smaller numbers)
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
from analyze_fitting_g_eval import contributions, tier  # noqa: E402

GAMES = ["CSO-BT", "OW-BT", "AC-BT", "XO-BT"]
MODES = {0: "hold", 1: "keep moving", 2: "chase", 3: "evade"}
NEW = {f"fit[{g}]": g for g in GAMES}
EARLIER = {"fitF[CSO-BT]": "CSO-BT", "fitF[OW-BT]": "OW-BT", "fitF[AC-BT]": "AC-BT", "fitF[XO-BT]": "XO-BT",
           "fitD[XO-BT]": "XO-BT", "fitE[XO-BT]": "XO-BT"}
PAIRS = [(f"fit[{g}]", f"fitF[{g}]") for g in GAMES] + [("fit[XO-BT]", "fitD[XO-BT]")]
MEASURES = ["retreat_share", "far_pursuit_share", "resource_goal_share_good", "contact_distance"]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="../repro_outputs/v11_fit")
    p.add_argument("--boot", type=int, default=1000)
    p.add_argument("--perm", type=int, default=2000)
    p.add_argument("--splits", type=int, default=1000)
    a = p.parse_args()
    d = Path(a.dir)

    # 1. the frozen Part B analysis
    sys.argv = [sys.argv[0], "--dir", str(d), "--boot", str(a.boot), "--perm", str(a.perm), "--splits", str(a.splits)]
    af.main()
    summ = json.loads((d / "fitting_summary.json").read_text())
    fitted = json.loads((d / "fitted.json").read_text())
    s1b = json.loads((d / "stage1b.json").read_text())
    diag = json.loads((d / "validation_diagnostic.json").read_text())
    df = pd.read_csv(d / "test_rows.csv")
    stage0 = json.loads((d / "stage0.json").read_text())
    cells = af.Cells(df, af.FP)
    styles = [s for s in df.agent.unique() if s in af.HAND.values() or s.endswith("[route off]")]
    sc_game = af.scales_for(df, stage0, af.TRAIN_MAPS)
    heldout = [m for m in af.HELDOUT_MAPS if m in set(df["map"])]
    sc_ho = {m: af.scales_for(df, stage0, [m]) for m in heldout}
    ci = lambda x: [float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))]  # noqa: E731

    # 2. tiers of the new fits (frozen analysis), headline claims, modes, validation objectives
    out: dict = {"trees": {}, "earlier_fits": {}, "paired": {}, "behaviour": {}}
    md = ["# Part G-fit: new fits against the adopted trees (test seeds)", ""]
    n_improved = n_close = 0
    for g in GAMES:
        r = summ[g]
        gm, ho = r["game_maps"], r["heldout"]
        own_ho = sum(1 for m in ho.values() if m["nearest"] == g)
        close_ho = sum(1 for m in ho.values() if m["nearest"] == g and m["G"] < 0.5)
        t = tier(gm["own_nearest_share"], gm["G_ci"], own_ho, close_ho)
        n_close += t == "close"
        n_improved += t in ("close", "improved")
        f = fitted[g]
        out["trees"][g] = {
            "tier": t, "mode": f["combat_mode"], "searched_modes": f["searched_modes"], "weights": f["weights"],
            "extension": f["extension"], "own_nearest_share": gm["own_nearest_share"], "G": gm["G"], "G_ci": gm["G_ci"],
            "fit_index": 1 - gm["G"] ** 2, "fit_index_ci": [1 - gm["G_ci"][1] ** 2, 1 - gm["G_ci"][0] ** 2],
            "D2": gm["D2"], "heldout": ho, "heldout_own_nearest": own_ho, "heldout_close": close_ho,
            "part_b_verdict_label": r["verdict"], "train_J": f["train_J"], "validation_J": f["validation_J"],
            "selection_J": s1b[g]["selection_J"], "fitted_mode_is_first_ranked": f["combat_mode"] == s1b[g]["mode"],
            "finalists_validation_J": {MODES[m]: sorted(x["validation_J"] for x in f["finalists"] if x["mode"] == m)
                                       for m in f["searched_modes"]},
            "earlier_fits_validation_J": {k: v["validation_J"] for k, v in diag.items() if v["game"] == g}}

    # 3. the earlier fits on the new seeds, and the paired differences (one set of resamples)
    agents = list(NEW) + [f for f in EARLIER if f in set(df.agent)]
    own = {**NEW, **EARLIER}
    rng = np.random.default_rng(11030)
    boot = {f: {"own": 0, "G": []} for f in agents}
    pair_d = {pr: [] for pr in PAIRS if pr[0] in agents and pr[1] in agents}
    for _ in range(a.boot):
        idx = rng.integers(0, cells.n_ep, cells.n_ep)
        den = {t: min(max(af.d2(cells, s, t, sc_game, idx), 1e-12) for s in styles) for t in GAMES}
        gi = {}
        for f in agents:
            dd = {t: af.d2(cells, f, t, sc_game, idx) for t in GAMES}
            boot[f]["own"] += min(dd, key=dd.get) == own[f]
            gi[f] = math.sqrt(max(dd[own[f]], 0.0) / den[own[f]])
            boot[f]["G"].append(gi[f])
        for pr in pair_d:
            pair_d[pr].append(gi[pr[0]] - gi[pr[1]])
    for f in agents:
        if f in NEW:
            continue
        g = own[f]
        ho = {}
        for m in heldout:
            dm = {t: af.d2(cells, f, t, sc_ho[m]) for t in GAMES}
            ho[m] = {"nearest": min(dm, key=dm.get), "G": af.gap(cells, f, g, styles, sc_ho[m])}
        own_ho = sum(1 for v in ho.values() if v["nearest"] == g)
        close_ho = sum(1 for v in ho.values() if v["nearest"] == g and v["G"] < 0.5)
        share, g_ci = boot[f]["own"] / a.boot, ci(boot[f]["G"])
        out["earlier_fits"][f] = {"game": g, "D2": {t: af.d2(cells, f, t, sc_game) for t in GAMES},
                                  "own_nearest_share": share, "G": af.gap(cells, f, g, styles, sc_game), "G_ci": g_ci,
                                  "heldout": ho, "heldout_own_nearest": own_ho, "heldout_close": close_ho,
                                  "tier": tier(share, g_ci, own_ho, close_ho)}
    for (x, y), v in pair_d.items():
        out["paired"][f"{x} - {y}"] = {"a": x, "b": y, "dG": float(np.mean(v)), "dG_ci": ci(v)}

    for g in GAMES:
        r = out["trees"][g]
        md += [f"## {g}: {r['tier']} (fitted mode {MODES[r['mode']]}; searched {', '.join(MODES[m] for m in r['searched_modes'])})",
               "",
               "- parameters: " + ", ".join(f"{k} {v:.3f}" for k, v in {**r['weights'], **r['extension']}.items()),
               "- mode ranking (stage-1b selection objective): " + ", ".join(
                   f"{MODES[int(m)]} {v:.2f}" for m, v in sorted(r["selection_J"].items(), key=lambda kv: kv[1]))
               + f"; fitted mode is the first-ranked one: {'yes' if r['fitted_mode_is_first_ranked'] else 'no'}",
               f"- own tree nearest in {100 * r['own_nearest_share']:.0f}% of resamples; G {r['G']:.2f} "
               f"[{r['G_ci'][0]:.2f}, {r['G_ci'][1]:.2f}]; fit index 1 - G^2 = {r['fit_index']:.2f}",
               "- D2 (game maps): " + ", ".join(f"{t} {v:.2f}" for t, v in r["D2"].items()),
               f"- held-out maps: own tree nearest on {r['heldout_own_nearest']}/5, with G < 0.5 on "
               f"{r['heldout_close']}/5: " + "; ".join(f"{m} {v['nearest']} (G {v['G']:.2f})" for m, v in r["heldout"].items()),
               f"- validation objective {r['validation_J']:.2f} (train {r['train_J']:.2f}); finalists by mode: "
               + "; ".join(f"{m} " + ", ".join(f"{j:.2f}" for j in js) for m, js in r["finalists_validation_J"].items()),
               "- earlier fits on the validation seeds (diagnostic): "
               + ", ".join(f"{k} {v:.2f}" for k, v in r["earlier_fits_validation_J"].items()),
               f"- verdict under the Part B definitions: {r['part_b_verdict_label']}", ""]
    md += ["## Earlier fits on the new test seeds (pre-specified comparisons)", ""]
    for f, r in out["earlier_fits"].items():
        md.append(f"- {f} (own tree {r['game']}): {r['tier']}; own tree nearest in {100 * r['own_nearest_share']:.0f}% "
                  f"of resamples; G {r['G']:.2f} [{r['G_ci'][0]:.2f}, {r['G_ci'][1]:.2f}]; held-out own nearest "
                  f"{r['heldout_own_nearest']}/5 (G < 0.5 on {r['heldout_close']}/5): "
                  + "; ".join(f"{m} {v['nearest']} (G {v['G']:.2f})" for m, v in r["heldout"].items()))
    md += ["", "## Paired differences (same resamples)", ""] + [
        f"- G({v['a']}) - G({v['b']}) = {v['dG']:+.2f} [{v['dG_ci'][0]:+.2f}, {v['dG_ci'][1]:+.2f}]"
        for v in out["paired"].values()]

    # 4. exploratory: behaviour and contributions
    md += ["", "## Behaviour (means over maps and episodes; exploratory)", "",
           "| agent | family | scenarios | " + " | ".join(MEASURES) + " |", "|---|---|---|" + "---|" * len(MEASURES)]
    for ag in GAMES + agents:
        for fam, maps in (("game", af.TRAIN_MAPS), ("held-out", heldout)):
            for scs, sel in (("Deathmatch", ["Deathmatch"]), ("all", af.SCENARIOS)):
                sub = df[(df.agent == ag) & df["map"].isin(maps) & df.scenario.isin(sel)]
                vals = {m: float(pd.to_numeric(sub[m], errors="coerce").mean()) for m in MEASURES}
                out["behaviour"][f"{ag}|{fam}|{scs}"] = vals
                md.append(f"| {ag} | {fam} | {scs} | " + " | ".join(f"{vals[m]:.2f}" for m in MEASURES) + " |")
    out["contributions"] = {f: contributions(cells, f, own[f], sc_game) for f in agents}
    md += ["", "## Contributions to D2(fit, own tree) on the game maps (exploratory)", ""] + [
        f"- {f}: " + ", ".join(f"{k} {v:.2f}" for k, v in sorted(c.items(), key=lambda kv: -kv[1]))
        for f, c in out["contributions"].items()]

    # headline and the predictions of the plan
    tiers = {g: out["trees"][g]["tier"] for g in GAMES}
    at_least = lambda t: t in ("close", "improved")  # noqa: E731
    below0 = lambda k: k in out["paired"] and out["paired"][k]["dG_ci"][1] < 0  # noqa: E731
    out["H_G1_improved_3_of_4"] = n_improved >= 3
    out["H_G2_close_3_of_4"] = n_close >= 3
    out["all_four_at_least_improved"] = n_improved == 4
    out["XO_close"] = tiers["XO-BT"] == "close"
    md += ["", "## Headline", "",
           f"- H-G1 (at least 'improved' on >= 3 of 4 trees): {n_improved}/4 -> {'met' if n_improved >= 3 else 'not met'}",
           f"- H-G2 ('close' on >= 3 of 4 trees): {n_close}/4 -> {'met' if n_close >= 3 else 'not met'}",
           f"- (a) all four trees at least improved: {'yes' if n_improved == 4 else 'no'} ("
           + ", ".join(f"{g} {t}" for g, t in tiers.items()) + ")",
           f"- (b) Xonotic tree close: {'yes' if out['XO_close'] else 'no'}"]
    trees = out["trees"]
    fd = out["earlier_fits"].get("fitD[XO-BT]", {})
    xo_c = out["contributions"].get("fit[XO-BT]", {})
    pred = [("CSO-BT: at least improved, in the chase mode", at_least(tiers["CSO-BT"]) and trees["CSO-BT"]["mode"] == 2),
            ("OW-BT: at least improved", at_least(tiers["OW-BT"])),
            ("OW-BT: hold is one of the two searched modes", 0 in trees["OW-BT"]["searched_modes"]),
            ("OW-BT: G(fit) - G(fitF) below 0 (95% CI)", below0("fit[OW-BT] - fitF[OW-BT]")),
            ("AC-BT: at least improved", at_least(tiers["AC-BT"])),
            ("AC-BT: G(fit) - G(fitF) below 0 (95% CI)", below0("fit[AC-BT] - fitF[AC-BT]")),
            ("AC-BT: own tree nearest on >= 4 of 5 held-out maps", trees["AC-BT"]["heldout_own_nearest"] >= 4),
            ("XO-BT: at least improved, in the hold mode", at_least(tiers["XO-BT"]) and trees["XO-BT"]["mode"] == 0),
            ("XO-BT: G(fit) - G(fitF) below 0 (95% CI)", below0("fit[XO-BT] - fitF[XO-BT]")),
            ("fitD[XO-BT] on the new seeds: at least improved", at_least(fd.get("tier", ""))),
            ("H-G1 met", out["H_G1_improved_3_of_4"]), ("H-G2 not met", not out["H_G2_close_3_of_4"]),
            ("(exploratory) far pursuit is the largest contribution to D2(fit[XO-BT], XO-BT)",
             bool(xo_c) and max(xo_c, key=xo_c.get) == "far_pursuit_share")]
    md += ["", "## Predictions of the plan", ""] + [f"- {t}: {'met' if ok else 'NOT met'}" for t, ok in pred]
    md += ["- not predicted (reported): XO-BT close; fitD[XO-BT] close on the new seeds "
           f"({fd.get('tier', 'n/a')}); G(fit[XO-BT]) - G(fitD[XO-BT]); G(fit[CSO-BT]) - G(fitF[CSO-BT])"]
    out["predictions"] = {t: bool(ok) for t, ok in pred}
    (d / "fitting_g_summary.json").write_text(json.dumps(out, indent=1, default=float))
    (d / "fitting_g_summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
