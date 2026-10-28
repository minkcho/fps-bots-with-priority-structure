"""Analysis of Part G-eval (DRAFT protocol FITTING_PLAN_G_EVAL_DRAFT.md, 2026-09-27): existing fits against the revised
trees. Definitions are those of Part F (analyze_fitting.py helpers d2 / gap / scales_for / Cells with the Part E
fingerprint; tiers as in analyze_fitting_f.tiers).

Per fit (fit[CSO-BT], fit[OW-BT], fit[AC-BT], fit[XO-BT] of Part F; fitD[XO-BT], fitE[XO-BT]):
  primary (revised trees, this round's stage-0 scales on the game maps, test-seed scales on each held-out map):
    D2 to the four revised trees, share of 1000 bootstrap resamples (episode indices, paired) in which the own tree
    is nearest, G with 95% CI, held-out maps with the own tree nearest (and with G < 0.5), tier
    (close / improved / not approximated)
  earlier trees (AC-BT[0925], XO-BT[step] in place of AC-BT, XO-BT; same scales, same resamples): the same quantities
  paired differences on the same resamples: D2(fit, revised own tree) - D2(fit, earlier own tree) and
    G(revised) - G(earlier), with 95% CI (AssaultCube and Xonotic fits)
  secondary: point estimates with the Part F stage-0 scales (repro_outputs/v8_fit/stage0.json) on the game maps
  contributions of each fingerprint metric to D2(fit, own tree) on the game maps (sum of that metric's terms / number
    of dimensions, so the contributions add up to D2)
Also: behaviour means (retreat, far pursuit, item control, contact distance) of trees and fits in Deathmatch and over
all scenarios; the Part E selection rule (separation of the revised AssaultCube and Xonotic trees >= 1 pooled
within-condition SD on both map families) for retreat, far pursuit and contact distance; the headline lines and the
predictions of the plan, each marked met / not met.
Usage: python experiments/analyze_fitting_g_eval.py --dir ../repro_outputs/v10_eval [--boot 1000]
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

ROOT = Path(__file__).resolve().parents[2]
GAMES = ["CSO-BT", "OW-BT", "AC-BT", "XO-BT"]
REVISED = {g: g for g in GAMES}
EARLIER = {"CSO-BT": "CSO-BT", "OW-BT": "OW-BT", "AC-BT": "AC-BT[0925]", "XO-BT": "XO-BT[step]"}
FITS = {"fit[CSO-BT]": "CSO-BT", "fit[OW-BT]": "OW-BT", "fit[AC-BT]": "AC-BT", "fit[XO-BT]": "XO-BT",
        "fitD[XO-BT]": "XO-BT", "fitE[XO-BT]": "XO-BT"}
MEASURES = ["retreat_share", "far_pursuit_share", "resource_goal_share_good", "contact_distance"]
SEP_MEASURES = ["retreat_share", "far_pursuit_share", "contact_distance"]


def tier(own_share, g_ci, own_ho, close_ho) -> str:
    ident = own_share >= 0.95
    if ident and g_ci[1] < 0.5 and close_ho >= 4:
        return "close"
    if ident and g_ci[1] < 1.0 and own_ho >= 4:
        return "improved"
    return "not approximated"


def contributions(cells, a, b, scales) -> dict:
    terms: dict = {}
    n = 0
    for d, s in scales.items():
        ma, va, na = cells.stats(a, d)
        mb, vb, nb = cells.stats(b, d)
        if na and nb:
            terms[d[2]] = terms.get(d[2], 0.0) + ((ma - mb) ** 2 - va / na - vb / nb) / s ** 2
            n += 1
    return {k: v / n for k, v in terms.items()}


def separation(df, a, b, maps, m) -> float:
    seps = []
    for mp in maps:
        for sc in af.SCENARIOS:
            x = pd.to_numeric(df[(df.agent == a) & (df["map"] == mp) & (df.scenario == sc)][m], errors="coerce").dropna()
            y = pd.to_numeric(df[(df.agent == b) & (df["map"] == mp) & (df.scenario == sc)][m], errors="coerce").dropna()
            if len(x) < 2 or len(y) < 2:
                continue
            sd = math.sqrt((x.var(ddof=1) + y.var(ddof=1)) / 2)
            if sd > 0:
                seps.append(abs(x.mean() - y.mean()) / sd)
    return float(np.mean(seps)) if seps else float("nan")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="../repro_outputs/v10_eval")
    p.add_argument("--part-f", default=str(ROOT / "repro_outputs" / "v8_fit"))
    p.add_argument("--boot", type=int, default=1000)
    a = p.parse_args()
    d = Path(a.dir)
    df = pd.read_csv(d / "test_rows.csv")
    stage0 = json.loads((d / "stage0.json").read_text())
    stage0_f = json.loads((Path(a.part_f) / "stage0.json").read_text())
    cells = af.Cells(df, af.FP)
    styles = [s for s in df.agent.unique() if s in af.HAND.values() or s.endswith("[route off]")]
    sc_game = af.scales_for(df, stage0, af.TRAIN_MAPS)
    sc_game_f = af.scales_for(df, stage0_f, af.TRAIN_MAPS)
    heldout = [m for m in af.HELDOUT_MAPS if m in set(df["map"])]
    sc_ho = {m: af.scales_for(df, stage0, [m]) for m in heldout}   # held-out scales: revised trees + designed styles
    all_trees = sorted(set(REVISED.values()) | set(EARLIER.values()))
    fits = [f for f in FITS if f in set(df.agent)]

    # bootstrap (paired resamples of episode indices, shared by every fit, tree set and quantity)
    rng = np.random.default_rng(10030)
    boot = {f: {"own_rev": 0, "own_early": 0, "G_rev": [], "G_early": [], "dD2": [], "dG": []} for f in fits}
    for _ in range(a.boot):
        idx = rng.integers(0, cells.n_ep, cells.n_ep)
        den = {t: min(max(af.d2(cells, s, t, sc_game, idx), 1e-12) for s in styles) for t in all_trees}
        for f in fits:
            g = FITS[f]
            dd = {t: af.d2(cells, f, t, sc_game, idx) for t in all_trees}
            rev = {t: dd[REVISED[t]] for t in GAMES}
            early = {t: dd[EARLIER[t]] for t in GAMES}
            b = boot[f]
            b["own_rev"] += min(rev, key=rev.get) == g
            b["own_early"] += min(early, key=early.get) == g
            gr = math.sqrt(max(dd[REVISED[g]], 0.0) / den[REVISED[g]])
            ge = math.sqrt(max(dd[EARLIER[g]], 0.0) / den[EARLIER[g]])
            b["G_rev"].append(gr)
            b["G_early"].append(ge)
            b["dD2"].append(dd[REVISED[g]] - dd[EARLIER[g]])
            b["dG"].append(gr - ge)
    ci = lambda x: [float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))]  # noqa: E731

    out: dict = {"fits": {}, "behaviour": {}, "separation": {}}
    md = ["# Part G-eval: existing fits against the revised trees (test seeds; evaluation only, nothing fitted)", ""]
    for f in fits:
        g = FITS[f]
        res: dict = {"game": g}
        for name, trees in (("revised", REVISED), ("earlier", EARLIER)):
            own = trees[g]
            dist = {t: af.d2(cells, f, trees[t], sc_game) for t in GAMES}
            dist_f = {t: af.d2(cells, f, trees[t], sc_game_f) for t in GAMES}
            G = af.gap(cells, f, own, styles, sc_game)
            ho = {}
            for m in heldout:
                dm = {t: af.d2(cells, f, trees[t], sc_ho[m]) for t in GAMES}
                ho[m] = {"nearest": min(dm, key=dm.get), "G": af.gap(cells, f, own, styles, sc_ho[m]), "D2": dm}
            own_ho = sum(1 for v in ho.values() if v["nearest"] == g)
            close_ho = sum(1 for v in ho.values() if v["nearest"] == g and v["G"] < 0.5)
            b = boot[f]
            share = (b["own_rev"] if name == "revised" else b["own_early"]) / a.boot
            g_ci = ci(b["G_rev"] if name == "revised" else b["G_early"])
            res[name] = {"D2": dist, "own_nearest_share": share, "G": G, "G_ci": g_ci, "heldout": ho,
                         "heldout_own_nearest": own_ho, "heldout_close": close_ho,
                         "tier": tier(share, g_ci, own_ho, close_ho),
                         "partF_scales": {"D2": dist_f, "G": af.gap(cells, f, own, styles, sc_game_f),
                                          "nearest": min(dist_f, key=dist_f.get)},
                         "contributions": contributions(cells, f, own, sc_game)}
        res["paired"] = {"dD2": float(np.mean(boot[f]["dD2"])), "dD2_ci": ci(boot[f]["dD2"]),
                         "dG": float(np.mean(boot[f]["dG"])), "dG_ci": ci(boot[f]["dG"])}
        out["fits"][f] = res
        r, e = res["revised"], res["earlier"]
        md += [f"## {f} (own tree {g}): {r['tier']} against the revised tree (earlier tree: {e['tier']})", "",
               "- revised trees, D2 (game maps): " + ", ".join(f"{t} {v:.2f}" for t, v in r["D2"].items())
               + f"; own tree nearest in {100 * r['own_nearest_share']:.0f}% of resamples; "
               f"G {r['G']:.2f} [{r['G_ci'][0]:.2f}, {r['G_ci'][1]:.2f}]",
               f"- held-out maps: own tree nearest on {r['heldout_own_nearest']}/5 (with G < 0.5 on "
               f"{r['heldout_close']}/5): " + "; ".join(f"{m} {v['nearest']} (G {v['G']:.2f})" for m, v in r["heldout"].items()),
               "- earlier trees, D2: " + ", ".join(f"{t} {v:.2f}" for t, v in e["D2"].items())
               + f"; own tree nearest in {100 * e['own_nearest_share']:.0f}%; G {e['G']:.2f} "
               f"[{e['G_ci'][0]:.2f}, {e['G_ci'][1]:.2f}]; held-out own nearest {e['heldout_own_nearest']}/5",
               f"- paired (revised - earlier own tree): D2 {res['paired']['dD2']:+.2f} [{res['paired']['dD2_ci'][0]:+.2f}, "
               f"{res['paired']['dD2_ci'][1]:+.2f}], G {res['paired']['dG']:+.2f} [{res['paired']['dG_ci'][0]:+.2f}, "
               f"{res['paired']['dG_ci'][1]:+.2f}]",
               "- Part F stage-0 scales (secondary): D2 " + ", ".join(f"{t} {v:.2f}" for t, v in r["partF_scales"]["D2"].items())
               + f"; G {r['partF_scales']['G']:.2f}; nearest {r['partF_scales']['nearest']}",
               "- contributions to D2(fit, revised own tree): " + ", ".join(
                   f"{k} {v:.2f}" for k, v in sorted(r["contributions"].items(), key=lambda kv: -kv[1])), ""]

    # behaviour means and the Part E selection rule
    md += ["## Behaviour (means over maps and episodes)", "",
           "| agent | family | scenarios | " + " | ".join(MEASURES) + " |", "|---|---|---|" + "---|" * len(MEASURES)]
    for ag in all_trees + fits:
        for fam, maps in (("game", af.TRAIN_MAPS), ("held-out", heldout)):
            for scs, sel in (("Deathmatch", ["Deathmatch"]), ("all", af.SCENARIOS)):
                g = df[(df.agent == ag) & df["map"].isin(maps) & df.scenario.isin(sel)]
                vals = {m: float(pd.to_numeric(g[m], errors="coerce").mean()) for m in MEASURES}
                out["behaviour"][f"{ag}|{fam}|{scs}"] = vals
                md.append(f"| {ag} | {fam} | {scs} | " + " | ".join(f"{vals[m]:.2f}" for m in MEASURES) + " |")
    md += ["", "## Part E selection rule with the revised trees (separation of AC-BT and XO-BT, pooled SD)", ""]
    for m in SEP_MEASURES:
        s = {fam: separation(df, "AC-BT", "XO-BT", maps, m) for fam, maps in (("game", af.TRAIN_MAPS),
                                                                               ("held-out", heldout))}
        out["separation"][m] = s
        md.append(f"- {m}: game {s['game']:.2f}, held-out {s['held-out']:.2f} -> "
                  + ("kept (>= 1 on both)" if min(s.values()) >= 1 else "would not pass (< 1)"))

    # headline lines and the predictions of the plan
    xo = [f for f in fits if FITS[f] == "XO-BT"]
    pred = []
    for f in xo:
        r = out["fits"][f]["revised"]
        pred.append((f"{f}: own tree nearest on the game maps (>= 95% of resamples)", r["own_nearest_share"] >= 0.95))
        pred.append((f"{f}: own tree nearest on at most 1 of 5 held-out maps", r["heldout_own_nearest"] <= 1))
        pred.append((f"{f}: not approximated", r["tier"] == "not approximated"))
        pred.append((f"{f}: D2 to the revised Xonotic tree below D2 to the per-step tree (paired CI below 0)",
                     out["fits"][f]["paired"]["dD2_ci"][1] < 0))
    if all(f in out["fits"] for f in ("fit[XO-BT]", "fitD[XO-BT]", "fitE[XO-BT]")):
        gs = {f: out["fits"][f]["revised"]["G"] for f in ("fit[XO-BT]", "fitD[XO-BT]", "fitE[XO-BT]")}
        pred.append(("Part F Xonotic fit has the lowest G of the three Xonotic fits", min(gs, key=gs.get) == "fit[XO-BT]"))
    for f in ("fit[CSO-BT]", "fit[OW-BT]", "fit[AC-BT]"):
        if f in out["fits"]:
            pred.append((f"{f}: improved (as in Part F)", out["fits"][f]["revised"]["tier"] == "improved"))
    pred.append(("Part E selection rule holds for retreat and far pursuit with the revised trees",
                 all(min(out["separation"][m].values()) >= 1 for m in ("retreat_share", "far_pursuit_share"))))
    n_xo = sum(out["fits"][f]["revised"]["tier"] in ("close", "improved") for f in xo)
    md += ["", "## Headline", "",
           f"- Xonotic fits at least 'improved' against the revised Xonotic tree: {n_xo}/{len(xo)}",
           "- tiers against the revised trees: " + ", ".join(f"{f} {out['fits'][f]['revised']['tier']}" for f in fits),
           "", "## Predictions of the plan", ""] + [f"- {t}: {'met' if ok else 'NOT met'}" for t, ok in pred]
    out["predictions"] = {t: bool(ok) for t, ok in pred}
    (d / "eval_summary.json").write_text(json.dumps(out, indent=1, default=float))
    (d / "eval_summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
