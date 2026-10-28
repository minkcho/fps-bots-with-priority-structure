"""Analysis of Round H (v15; DRAFT protocol FITTING_PLAN_H_DRAFT.md, 2026-09-30): hand-set settings against the trees,
graded like Part G-fit but per game-scenario case (analyze_fitting.py helpers d2 / gap / scales_for / Cells with the
Part E fingerprint; tiers as in analyze_fitting_g_eval.tier), next to the Part G-fit fits on the same episodes.

Cases (user's decision of 2026-09-30: every logic is graded in the scenarios it targets, nothing else is run):
  CSO-BT in Mission and in Control, OW-BT in Mission and in Control, AC-BT in Deathmatch, XO-BT in Deathmatch.
Per case and agent (hand[<tree>], fit[<tree>]), on that scenario's dimensions of the game maps:
  D2 to the trees of the scenario family (objective family: CSO-BT, OW-BT; deathmatch family: AC-BT, XO-BT), share of
  1000 paired bootstrap resamples in which the own tree is nearest, G with 95% CI (denominator: the nearest designed
  style in that scenario), held-out maps with the own tree nearest (and with G < 0.5), tier (close / improved / not
  approximated), contributions of each fingerprint metric to D2(agent, own tree)
Paired per case, on the same resamples (hand-set minus fit of the same tree):
  dG = G(hand) - G(fit) with 95% CI; the share S = (1 - G(hand)) / (1 - G(fit)) of the fit's improvement over the
  designed styles that the hand-set setting achieves (resamples with G(fit) >= 1 are dropped from S and counted)
Also: behaviour means (retreat, far pursuit, item control, contact distance) per agent and scenario; the headline lines
and the predictions of the plan, each marked met / not met; and a per-case table in the columns of Table 3 of the paper
(goal weights, commitment weight, mode) plus the four optional parameters and the grade of the case, one row per case
for the hand-set setting and one for the fit (handset_table.md and handset_table.tex; the values of the two scenarios
of one game are identical because the setting is read per game).
Usage: python experiments/analyze_fitting_h.py --dir ../repro_outputs/v15_handset [--boot 1000]
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
from analyze_fitting_g_eval import tier, contributions  # noqa: E402

GAMES = ["CSO-BT", "OW-BT", "AC-BT", "XO-BT"]
NATIVE = {"CSO-BT": ["Mission", "Control"], "OW-BT": ["Mission", "Control"], "AC-BT": ["Deathmatch"],
          "XO-BT": ["Deathmatch"]}
CASES = [(g, sc) for g in GAMES for sc in NATIVE[g]]
MEASURES = ["retreat_share", "far_pursuit_share", "resource_goal_share_good", "contact_distance"]
BOOT_SEED = 15030


def family(scen: str) -> list[str]:
    """The trees that are run in a scenario (the candidates of the identification test)."""
    return [t for t in GAMES if scen in NATIVE[t]]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="../repro_outputs/v15_handset")
    p.add_argument("--boot", type=int, default=1000)
    a = p.parse_args()
    d = Path(a.dir)
    df = pd.read_csv(d / "test_rows.csv")
    stage0 = json.loads((d / "stage0.json").read_text())
    handset = json.loads((d / "handset.json").read_text())
    cells = af.Cells(df, af.FP)
    present = set(df.agent)
    styles = [s for s in df.agent.unique() if s in af.HAND.values() or s.endswith("[route off]")]
    sc_game_all = af.scales_for(df, stage0, af.TRAIN_MAPS)
    heldout = [m for m in af.HELDOUT_MAPS if m in set(df["map"])]
    sc_ho_all = {m: af.scales_for(df, stage0, [m]) for m in heldout}
    cases = [(g, sc) for g, sc in CASES if f"hand[{g}]" in present and f"fit[{g}]" in present]

    def restrict(scales: dict, scen: str) -> dict:
        return {dd: s for dd, s in scales.items() if dd[1] == scen}

    # bootstrap (paired resamples of episode indices, shared by every case, agent and quantity)
    rng = np.random.default_rng(BOOT_SEED)
    boot = {(g, sc, ag): {"own": 0, "G": []} for g, sc in cases for ag in ("hand", "fit")}
    pairs = {(g, sc): {"dG": [], "S": [], "fit_ge1": 0} for g, sc in cases}
    for _ in range(a.boot):
        idx = rng.integers(0, cells.n_ep, cells.n_ep)
        for g, sc in cases:
            sg = restrict(sc_game_all, sc)
            trees = family(sc)
            den = min(max(af.d2(cells, s, g, sg, idx), 1e-12) for s in styles)
            gval = {}
            for ag in ("hand", "fit"):
                label = f"{ag}[{g}]"
                dd = {t: af.d2(cells, label, t, sg, idx) for t in trees}
                b = boot[(g, sc, ag)]
                b["own"] += min(dd, key=dd.get) == g
                gval[ag] = math.sqrt(max(dd[g], 0.0) / den)
                b["G"].append(gval[ag])
            pr = pairs[(g, sc)]
            pr["dG"].append(gval["hand"] - gval["fit"])
            if gval["fit"] < 1.0:
                pr["S"].append((1.0 - gval["hand"]) / (1.0 - gval["fit"]))
            else:
                pr["fit_ge1"] += 1
    ci = lambda x: [float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))] if len(x) else [float("nan")] * 2  # noqa: E731

    out: dict = {"cases": {}, "paired": {}, "behaviour": {}, "handset": handset["settings"]}
    md = ["# Round H (v15): hand-set settings against the trees, per game-scenario case, next to the Part G-fit fits "
          "(test seeds; native scenarios only; nothing fitted)", ""]
    for g, sc in cases:
        sg = restrict(sc_game_all, sc)
        trees = family(sc)
        key = f"{g}|{sc}"
        out["cases"][key] = {}
        md += [f"## {g} in {sc} ({len(sg)} dimensions on the game maps; trees of the family: {', '.join(trees)})", ""]
        for ag in ("hand", "fit"):
            label = f"{ag}[{g}]"
            dist = {t: af.d2(cells, label, t, sg) for t in trees}
            G = af.gap(cells, label, g, styles, sg)
            ho = {}
            for m in heldout:
                sm = restrict(sc_ho_all[m], sc)
                dm = {t: af.d2(cells, label, t, sm) for t in trees}
                ho[m] = {"nearest": min(dm, key=dm.get), "G": af.gap(cells, label, g, styles, sm), "D2": dm}
            own_ho = sum(1 for v in ho.values() if v["nearest"] == g)
            close_ho = sum(1 for v in ho.values() if v["nearest"] == g and v["G"] < 0.5)
            b = boot[(g, sc, ag)]
            share = b["own"] / a.boot
            g_ci = ci(b["G"])
            res = {"agent": label, "D2": dist, "nearest": min(dist, key=dist.get), "own_nearest_share": share, "G": G,
                   "G_ci": g_ci, "heldout": ho, "heldout_own_nearest": own_ho, "heldout_close": close_ho,
                   "tier": tier(share, g_ci, own_ho, close_ho), "contributions": contributions(cells, label, g, sg)}
            out["cases"][key][ag] = res
            md += [f"### {label}: {res['tier']}", "",
                   "- D2 (game maps): " + ", ".join(f"{t} {v:.2f}" for t, v in dist.items())
                   + f"; nearest {res['nearest']}; own tree nearest in {100 * share:.0f}% of resamples; "
                   f"G {G:.2f} [{g_ci[0]:.2f}, {g_ci[1]:.2f}]",
                   f"- held-out maps: own tree nearest on {own_ho}/{len(heldout)} (with G < 0.5 on {close_ho}/{len(heldout)}): "
                   + "; ".join(f"{m} {v['nearest']} (G {v['G']:.2f})" for m, v in ho.items()),
                   "- contributions to D2(agent, own tree): " + ", ".join(
                       f"{k} {v:.2f}" for k, v in sorted(res["contributions"].items(), key=lambda kv: -kv[1])), ""]
        gh, gf = out["cases"][key]["hand"]["G"], out["cases"][key]["fit"]["G"]
        pr = pairs[(g, sc)]
        S = (1.0 - gh) / (1.0 - gf) if gf < 1.0 else float("nan")
        res = {"G_hand": gh, "G_fit": gf, "dG": float(np.mean(pr["dG"])), "dG_ci": ci(pr["dG"]), "S": S,
               "S_ci": ci(pr["S"]), "resamples_with_G_fit_ge_1": pr["fit_ge1"]}
        out["paired"][key] = res
        md += [f"### paired (hand-set minus fit): dG {res['dG']:+.2f} [{res['dG_ci'][0]:+.2f}, {res['dG_ci'][1]:+.2f}]; "
               f"share of the fit's improvement S {S:.2f} [{res['S_ci'][0]:.2f}, {res['S_ci'][1]:.2f}]"
               + (f" ({pr['fit_ge1']} resamples with G fit >= 1 dropped)" if pr["fit_ge1"] else ""), ""]

    md += ["## Behaviour (means over the game maps and episodes, per scenario)", "",
           "| agent | scenario | " + " | ".join(MEASURES) + " |", "|---|---|" + "---|" * len(MEASURES)]
    for ag in [t for t in GAMES] + [f"{k}[{g}]" for g in GAMES for k in ("hand", "fit")]:
        for scen in af.SCENARIOS:
            sub = df[(df.agent == ag) & df["map"].isin(af.TRAIN_MAPS) & (df.scenario == scen)]
            if not len(sub):
                continue
            vals = {m: float(pd.to_numeric(sub[m], errors="coerce").mean()) for m in MEASURES}
            out["behaviour"][f"{ag}|{scen}"] = vals
            md.append(f"| {ag} | {scen} | " + " | ".join(f"{vals[m]:.2f}" for m in MEASURES) + " |")

    # headline lines and the predictions of the plan
    keys = [f"{g}|{sc}" for g, sc in cases]
    hand = {k: out["cases"][k]["hand"] for k in keys}
    n_ident = sum(hand[k]["own_nearest_share"] >= 0.95 for k in keys)
    n_impr = sum(hand[k]["tier"] in ("close", "improved") for k in keys)
    n_close = sum(hand[k]["tier"] == "close" for k in keys)
    n_half = sum(1 for k in keys if not math.isnan(out["paired"][k]["S"]) and out["paired"][k]["S"] >= 0.5)
    p1_keys = [k for k in keys if not k.startswith("AC-BT")]
    pred = [
        ("P1: the hand-set setting identifies its own tree (>= 95% of resamples) in the four objective cases and for "
         "XO-BT in Deathmatch", all(hand[k]["own_nearest_share"] >= 0.95 for k in p1_keys)),
        (f"H-H1: hand-set at least 'improved' in >= 4 of the {len(keys)} cases", n_impr >= 4),
        (f"H-H2: share S >= 0.5 in >= 3 of the {len(keys)} cases", n_half >= 3),
        ("P4: no hand-set case is 'close'", n_close == 0),
        ("P5: the search improves on the hand-set setting in every case (dG > 0 with the 95% CI above 0)",
         all(out["paired"][k]["dG_ci"][0] > 0 for k in keys) and len(keys) == len(CASES)),
    ]
    md += ["", "## Headline", "",
           f"- cases in which the hand-set setting identifies its own tree: {n_ident}/{len(keys)}",
           f"- cases at least 'improved': {n_impr}/{len(keys)}; 'close': {n_close}/{len(keys)}",
           "- tiers: " + ", ".join(f"{k} {hand[k]['tier']}" for k in keys),
           "- shares S of the fit's improvement: " + ", ".join(f"{k} {out['paired'][k]['S']:.2f}" for k in keys),
           "", "## Predictions of the plan", ""] + [f"- {t}: {'met' if ok else 'NOT met'}" for t, ok in pred]
    out["predictions"] = {t: bool(ok) for t, ok in pred}
    table_md, table_tex = case_tables(out, cases, json.loads((d / "run_stageall.json").read_text()), len(heldout))
    (d / "handset_table.md").write_text(table_md)
    (d / "handset_table.tex").write_text(table_tex)
    md += ["", table_md]
    (d / "handset_summary.json").write_text(json.dumps(out, indent=1, default=float))
    (d / "handset_summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


MODE_NAMES = {0: "hold", 1: "keep moving", 2: "chase", 3: "evade"}
PARAM_COLS = [("w_objective", "w_Obj"), ("w_engage", "w_Eng"), ("w_resource", "w_Res"), ("w_team", "w_Team"),
              ("w_commitment", "w_commit"), ("resource_idle_factor", "g0"), ("resource_distance_scale", "tau"),
              ("hunt_unseen", "eta"), ("urgent_switch_relief", "rho")]


def case_tables(out: dict, cases: list, run_rec: dict, n_heldout: int) -> tuple[str, str]:
    """Per-case table (Table 3 columns + optional parameters + grade): hand-set and fit rows for each case, as markdown and
    as a LaTeX tabular. Parameter values come from the run record (run_stageall.json: 'handset' and 'fits')."""
    params = {**run_rec["handset"], **run_rec["fits"]}
    fmt = lambda k, v: (f"{v:.0f}" if k == "resource_distance_scale" else f"{v:.2f}")  # noqa: E731
    head = (["Case", "Agent"] + [c for _, c in PARAM_COLS] + ["Mode", "Nearest", "G [95% CI]", "Held-out", "Tier", "S"])
    rows_md, rows_tex = [], []
    for g, sc in cases:
        key = f"{g}|{sc}"
        S = out["paired"][key]["S"]
        for ag in ("hand", "fit"):
            label = f"{ag}[{g}]"
            pr, res = params[label]["params"], out["cases"][key][ag]
            vals = [fmt(k, pr[k]) for k, _ in PARAM_COLS]
            grade = [res["nearest"], f"{res['G']:.2f} [{res['G_ci'][0]:.2f}, {res['G_ci'][1]:.2f}]",
                     f"{res['heldout_own_nearest']}/{n_heldout} ({res['heldout_close']})", res["tier"],
                     f"{S:.2f}" if ag == "hand" and not math.isnan(S) else ("n/a" if ag == "hand" else "")]
            cells = [f"{g} : {sc}", ag] + vals + [MODE_NAMES[int(params[label]["combat_mode"])]] + grade
            rows_md.append("| " + " | ".join(cells) + " |")
            rows_tex.append(" & ".join(cells).replace("%", "\\%") + " \\\\")
    md = "\n".join(["## Per case: setting and grade (hand-set row, then the fit of the same tree)", "",
                     "| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + rows_md + [
                     "", "Columns: goal weights (sum 1), w_commit = kappa (relative to the goal-weight sum), the four optional "
                     "parameters, mode; nearest tree of the family; G with the 95% CI; held-out maps with the own tree nearest "
                     "(and G < 0.5); tier; S = (1 - G_hand) / (1 - G_fit), the share of the fit's improvement over the designed "
                     "styles that the hand-set setting achieves (n/a when G_fit >= 1)."]) + "\n"
    tex_head = ["Case", "Agent", "$w_{\\textsc{Obj}}$", "$w_{\\textsc{Eng}}$", "$w_{\\textsc{Res}}$", "$w_{\\textsc{Team}}$",
                "$w_{\\mathrm{commit}}$", "$g_0$", "$\\tau$", "$\\eta$", "$\\rho$", "Mode", "Nearest", "$G$ [95\\% CI]",
                "Held-out", "Tier", "$S$"]
    tex = "\n".join(["% Round H (v15): per-case setting and grade; generated by analyze_fitting_h.py",
                      "\\begin{tabular}{@{}ll" + "c" * len(PARAM_COLS) + "l lcclc@{}}", "\\toprule",
                      " & ".join(tex_head) + " \\\\", "\\midrule"] + rows_tex
                     + ["\\bottomrule", "\\end{tabular}"]) + "\n"
    return md, tex


if __name__ == "__main__":
    main()
