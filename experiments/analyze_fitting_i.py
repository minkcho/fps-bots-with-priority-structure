"""Analysis of Round I (v16; DRAFT protocol FITTING_PLAN_I_DRAFT.md, 2026-09-30): per-scenario fits, graded per
game-scenario case with the definitions of Part G-fit (analyze_fitting.py helpers d2 / gap / scales_for / Cells with
the Part E fingerprint; tiers as in analyze_fitting_g_eval.tier).

Cases: CSO-BT in Mission and in Control, OW-BT in Mission and in Control, AC-BT in Deathmatch, XO-BT in Deathmatch.
Per case, for the case fit fitsc[<tree>:<scenario>], on that scenario's dimensions of the game maps:
  D2 to the trees of the scenario family (objective family: CSO-BT, OW-BT; deathmatch family: AC-BT, XO-BT), share of
  1000 bootstrap resamples (episode indices, paired across agents) in which the own tree is nearest, G with 95% CI
  (denominator: the nearest designed style in that scenario), held-out maps with the own tree nearest (and with
  G < 0.5), tier (close / improved / not approximated), contributions of each fingerprint metric to D2(fit, own tree)
Per case from the run: the stage-1b selection objectives of the four modes, the searched modes, the fitted mode and
  whether it is the first-ranked, the best validation objective of each searched mode.
Also: behaviour means (retreat, far pursuit, item control, contact distance) of the trees and the case fits per
  scenario; the per-case table in the columns of Table 3 of the paper plus the four optional parameters and the grade
  (scenario_fit_table.md / .tex: one row per case); the headline lines and the predictions of the plan, each marked
  met / not met.
Usage: python experiments/analyze_fitting_i.py --dir ../repro_outputs/v16_scenario_fit [--boot 1000]
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
BOOT_SEED = 16030
MODE_NAMES = {0: "hold", 1: "keep moving", 2: "chase", 3: "evade"}
PARAM_COLS = [("w_objective", "w_Obj"), ("w_engage", "w_Eng"), ("w_resource", "w_Res"), ("w_team", "w_Team"),
              ("w_commitment", "w_commit"), ("resource_idle_factor", "g0"), ("resource_distance_scale", "tau"),
              ("hunt_unseen", "eta"), ("urgent_switch_relief", "rho")]


def family(scen: str) -> list[str]:
    """The trees that are run in a scenario (the candidates of the identification test)."""
    return [t for t in GAMES if scen in NATIVE[t]]


def label(g: str, sc: str) -> str:
    return f"fitsc[{g}:{sc}]"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="../repro_outputs/v16_scenario_fit")
    p.add_argument("--boot", type=int, default=1000)
    a = p.parse_args()
    d = Path(a.dir)
    df = pd.read_csv(d / "test_rows.csv")
    stage0 = json.loads((d / "stage0.json").read_text())
    fitted = json.loads((d / "fitted.json").read_text())
    s1b = json.loads((d / "stage1b.json").read_text())
    cells = af.Cells(df, af.FP)
    present = set(df.agent)
    styles = [s for s in df.agent.unique() if s in af.HAND.values() or s.endswith("[route off]")]
    sc_game_all = af.scales_for(df, stage0, af.TRAIN_MAPS)
    heldout = [m for m in af.HELDOUT_MAPS if m in set(df["map"])]
    sc_ho_all = {m: af.scales_for(df, stage0, [m]) for m in heldout}
    cases = [(g, sc) for g, sc in CASES if label(g, sc) in present]

    def restrict(scales: dict, scen: str) -> dict:
        return {dd: s for dd, s in scales.items() if dd[1] == scen}

    # bootstrap (paired resamples of episode indices, shared by every case and quantity)
    rng = np.random.default_rng(BOOT_SEED)
    boot = {(g, sc): {"own": 0, "G": []} for g, sc in cases}
    for _ in range(a.boot):
        idx = rng.integers(0, cells.n_ep, cells.n_ep)
        for g, sc in cases:
            sg = restrict(sc_game_all, sc)
            lb = label(g, sc)
            den = min(max(af.d2(cells, s, g, sg, idx), 1e-12) for s in styles)
            dd = {t: af.d2(cells, lb, t, sg, idx) for t in family(sc)}
            b = boot[(g, sc)]
            b["own"] += min(dd, key=dd.get) == g
            b["G"].append(math.sqrt(max(dd[g], 0.0) / den))
    ci = lambda x: [float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))] if len(x) else [float("nan")] * 2  # noqa: E731

    out: dict = {"cases": {}, "search": {}, "behaviour": {}}
    md = ["# Round I (v16): per-scenario fits, graded per game-scenario case (test seeds; native scenarios only)", ""]
    for g, sc in cases:
        sg = restrict(sc_game_all, sc)
        trees = family(sc)
        key = f"{g}|{sc}"
        lb = label(g, sc)
        dist = {t: af.d2(cells, lb, t, sg) for t in trees}
        G = af.gap(cells, lb, g, styles, sg)
        ho = {}
        for m in heldout:
            sm = restrict(sc_ho_all[m], sc)
            dm = {t: af.d2(cells, lb, t, sm) for t in trees}
            ho[m] = {"nearest": min(dm, key=dm.get), "G": af.gap(cells, lb, g, styles, sm), "D2": dm}
        own_ho = sum(1 for v in ho.values() if v["nearest"] == g)
        close_ho = sum(1 for v in ho.values() if v["nearest"] == g and v["G"] < 0.5)
        b = boot[(g, sc)]
        share = b["own"] / a.boot
        g_ci = ci(b["G"])
        f = fitted[key]
        res = {"agent": lb, "game": g, "scenario": sc, "n_dims": len(sg), "params": f["params"],
               "combat_mode": f["combat_mode"], "D2": dist, "nearest": min(dist, key=dist.get),
               "own_nearest_share": share, "G": G, "G_ci": g_ci, "heldout": ho, "heldout_own_nearest": own_ho,
               "heldout_close": close_ho, "tier": tier(share, g_ci, own_ho, close_ho),
               "contributions": contributions(cells, lb, g, sg)}
        out["cases"][key] = res
        ranking = sorted([int(m) for m in s1b[key]["selection_J"]], key=lambda m: s1b[key]["selection_J"][str(m)])
        best_by_mode = {m: min(x["validation_J"] for x in f["finalists"] if x["mode"] == m) for m in f["searched_modes"]}
        srch = {"selection_J": s1b[key]["selection_J"], "ranking": ranking, "searched_modes": f["searched_modes"],
                "fitted_mode": f["combat_mode"], "fitted_mode_first_ranked": f["combat_mode"] == ranking[0],
                "validation_J": f["validation_J"], "train_J": f["train_J"], "best_validation_J_by_mode": best_by_mode}
        out["search"][key] = srch
        md += [f"## {g} in {sc} ({len(sg)} dimensions on the game maps; trees of the family: {', '.join(trees)}): "
               f"{res['tier']}", "",
               "- setting: " + ", ".join(f"{c} {f['params'][k]:.3f}" for k, c in PARAM_COLS)
               + f", mode {f['combat_mode']} ({MODE_NAMES[int(f['combat_mode'])]})",
               "- D2 (game maps): " + ", ".join(f"{t} {v:.2f}" for t, v in dist.items())
               + f"; nearest {res['nearest']}; own tree nearest in {100 * share:.0f}% of resamples; "
               f"G {G:.2f} [{g_ci[0]:.2f}, {g_ci[1]:.2f}]",
               f"- held-out maps: own tree nearest on {own_ho}/{len(heldout)} (with G < 0.5 on {close_ho}/{len(heldout)}): "
               + "; ".join(f"{m} {v['nearest']} (G {v['G']:.2f})" for m, v in ho.items()),
               "- contributions to D2(fit, own tree): " + ", ".join(
                   f"{k} {v:.2f}" for k, v in sorted(res["contributions"].items(), key=lambda kv: -kv[1])),
               "- search: stage-1b selection J by mode "
               + ", ".join(f"{m} ({MODE_NAMES[m]}) {s1b[key]['selection_J'][str(m)]:.2f}" for m in ranking)
               + f"; searched {f['searched_modes']}; fitted mode {f['combat_mode']} ({MODE_NAMES[int(f['combat_mode'])]}), "
               f"first-ranked: {'yes' if srch['fitted_mode_first_ranked'] else 'no'}; validation J {f['validation_J']:.3f} "
               f"(train {f['train_J']:.3f}; best per searched mode "
               + ", ".join(f"{m} {v:.3f}" for m, v in best_by_mode.items()) + ")", ""]

    md += ["## Behaviour (means over the game maps and episodes, per scenario)", "",
           "| agent | scenario | " + " | ".join(MEASURES) + " |", "|---|---|" + "---|" * len(MEASURES)]
    for ag in list(GAMES) + [label(g, sc) for g, sc in CASES]:
        for scen in af.SCENARIOS:
            sub = df[(df.agent == ag) & df["map"].isin(af.TRAIN_MAPS) & (df.scenario == scen)]
            if not len(sub):
                continue
            vals = {m: float(pd.to_numeric(sub[m], errors="coerce").mean()) for m in MEASURES}
            out["behaviour"][f"{ag}|{scen}"] = vals
            md.append(f"| {ag} | {scen} | " + " | ".join(f"{vals[m]:.2f}" for m in MEASURES) + " |")

    # headline lines and the predictions of the plan
    keys = [f"{g}|{sc}" for g, sc in cases]
    case = out["cases"]
    ident = lambda r: r["own_nearest_share"] >= 0.95 and r["heldout_own_nearest"] >= 4  # noqa: E731
    n_impr = sum(case[k]["tier"] in ("close", "improved") for k in keys)
    n_close = sum(case[k]["tier"] == "close" for k in keys)
    full = len(keys) == len(CASES)
    pred = [
        ("P1: every case fit identifies its own tree (own tree nearest in >= 95% of resamples and on >= 4 of 5 held-out "
         "maps)", full and all(ident(case[k]) for k in keys)),
        (f"H-I1: case fits at least 'improved' in >= 4 of the {len(keys)} cases", n_impr >= 4),
        (f"H-I2: case fits 'close' in >= 3 of the {len(keys)} cases", n_close >= 3),
    ]
    md += ["", "## Headline", "",
           f"- case fits at least 'improved': {n_impr}/{len(keys)}; 'close': {n_close}/{len(keys)}",
           "- tiers: " + ", ".join(f"{k} {case[k]['tier']}" for k in keys),
           "- G: " + ", ".join(f"{k} {case[k]['G']:.2f} [{case[k]['G_ci'][0]:.2f}, {case[k]['G_ci'][1]:.2f}]" for k in keys),
           "- fitted mode first-ranked in stage 1b: " + ", ".join(
               f"{k} {'yes' if out['search'][k]['fitted_mode_first_ranked'] else 'no'}" for k in keys),
           "", "## Predictions of the plan", ""] + [f"- {t}: {'met' if ok else 'NOT met'}" for t, ok in pred]
    out["predictions"] = {t: bool(ok) for t, ok in pred}
    table_md, table_tex = case_table(out, cases, len(heldout))
    (d / "scenario_fit_table.md").write_text(table_md)
    (d / "scenario_fit_table.tex").write_text(table_tex)
    md += ["", table_md]
    (d / "scenario_fit_summary.json").write_text(json.dumps(out, indent=1, default=float))
    (d / "scenario_fit_summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


def case_table(out: dict, cases: list, n_heldout: int) -> tuple[str, str]:
    """Per-case table (Table 3 columns + optional parameters + grade), one row per case, as markdown and as a LaTeX
    tabular."""
    fmt = lambda k, v: (f"{v:.0f}" if k == "resource_distance_scale" else f"{v:.2f}")  # noqa: E731
    head = ["Case"] + [c for _, c in PARAM_COLS] + ["Mode", "Nearest", "G [95% CI]", "Held-out", "Tier"]
    tex_head = ["Case", "$w_{\\textsc{Obj}}$", "$w_{\\textsc{Eng}}$", "$w_{\\textsc{Res}}$", "$w_{\\textsc{Team}}$",
                "$w_{\\mathrm{commit}}$", "$g_0$", "$\\tau$", "$\\eta$", "$\\rho$", "Mode", "Nearest", "$G$ [95\\% CI]",
                "Held-out", "Tier"]
    rows_md, rows_tex = [], []
    for g, sc in cases:
        res = out["cases"][f"{g}|{sc}"]
        vals = [fmt(k, res["params"][k]) for k, _ in PARAM_COLS]
        grade = [res["nearest"], f"{res['G']:.2f} [{res['G_ci'][0]:.2f}, {res['G_ci'][1]:.2f}]",
                 f"{res['heldout_own_nearest']}/{n_heldout} ({res['heldout_close']})", res["tier"]]
        cells = [f"{g} : {sc}"] + vals + [MODE_NAMES[int(res["combat_mode"])]] + grade
        rows_md.append("| " + " | ".join(cells) + " |")
        rows_tex.append(" & ".join(cells).replace("%", "\\%") + " \\\\")
    md = "\n".join(["## Per case: fitted setting and grade", "", "| " + " | ".join(head) + " |",
                    "|" + "---|" * len(head)] + rows_md + [
                    "", "Columns: goal weights (sum 1), w_commit = kappa (relative to the goal-weight sum), the four optional "
                    "parameters, mode; nearest tree of the family; G with the 95% CI; held-out maps with the own tree nearest "
                    "(and G < 0.5); tier."]) + "\n"
    tex = "\n".join(["% Round I (v16): per-case fitted setting and grade; generated by analyze_fitting_i.py",
                     "\\begin{tabular}{@{}l" + "c" * len(PARAM_COLS) + "l lccl@{}}", "\\toprule",
                     " & ".join(tex_head) + " \\\\", "\\midrule"] + rows_tex + ["\\bottomrule", "\\end{tabular}"]) + "\n"
    return md, tex


if __name__ == "__main__":
    main()
