"""Paper tables of the pre-registered fitting experiment (2026-09-25; presentation only).

Reads the outputs of run_fitting.py and analyze_fitting.py (not part of the frozen analysis; it only formats them):
  <dir>/fitted.json            fitted parameters per tree (weights, combat mode, training and validation objective)
  <dir>/fitting_summary.json   evaluation per tree: (a) nearest tree, (b) gap closure G, (c) noise floor,
                               (d) classifier AUC, (e) untargeted outcomes, held-out maps, verdict
Writes to --out:
  fitting_results.tex    one row per tree: mode, fitted weights, own tree nearest (share of resamples), G with CI,
                         closest designed style, noise floor, AUC (fingerprint, label-free), largest |d| of the
                         untargeted outcomes, held-out maps passed, verdict
  fitting_distances.tex  bias-corrected squared distances D2 of each fitted policy to the four trees (game maps)
  fitting_heldout.tex    per held-out map: nearest tree and G of each fitted policy
  fitting_modes.tex      (with --modes; exploratory) validation objective of the best screen point per tree and combat
                         mode (run_fitting_modes.py), next to the pre-registered fit
  fitting_gaps.tex       (with --gaps; exploratory) goal choice by situation, trees vs fitted policies
                         (diagnose_fitting_gaps.py, fitting_gaps.md)
  fitting_c.tex          (Part C, when <dir>/fitting_c_summary.json exists) per tree: mode, all fitted parameters,
                         own-tree share, G with CI, fit index 1 - G^2, held-out maps, G of the Part B fit on the same
                         seeds and the paired difference, tier
  fitting_tree_distances.tex  (with --tree-distances) D2 between the four trees on the game maps (test seeds);
                         with --fingerprint-d on the Part D fingerprint (goal intent + behavioural measures)
  fitting_d.tex          (Part D, when <dir>/fitting_d_summary.json exists) as fitting_c.tex, compared with the Part C fits
  fitting_e.tex          (Part E, when <dir>/fitting_e_summary.json exists) as fitting_c.tex, compared with the Part D fits;
                         with --fingerprint-e the tree distances use the Part E fingerprint (Part D's plus retreat, far
                         pursuit and contact distance)
  fitting_e_measures.tex (Part E, when <dir>/fitting_e_extra.json of analyze_fitting_e_extra.py exists; exploratory)
                         retreat, far pursuit and item control of the two deathmatch trees and their fits
  fitting_f.tex          (Part F, when <dir>/fitting_f_summary.json exists) as fitting_c.tex with the relief rho,
                         compared with the Part E fits; fitting_f_measures.tex as fitting_e_measures.tex (Part E and
                         Part F fits; needs analyze_fitting_e_extra.py --prev fitE)
  fitting_g_eval.tex     (Part G-eval, when <dir>/eval_summary.json of analyze_fitting_g_eval.py exists; nothing fitted)
                         the Xonotic fits of Parts D, E and F and the Part F fits of the other three trees against the
                         revised trees and, on the same episodes, the earlier trees: own-tree share, G with CI, held-out
                         maps, tier, and the paired differences Delta D2 and Delta G (revised - earlier own tree). With
                         only eval_summary.json in <dir> (repro_outputs/v10_eval) this is the only table written.
  fitting_g.tex          (Part G-fit, when <dir>/fitting_g_summary.json of analyze_fitting_g.py exists) per tree: fitted
                         and searched modes, parameters, own-tree share, G with CI, D2 to the own tree, fit index,
                         held-out maps, G of the Part F fit on the same seeds and the paired difference, tier
  fitting_g_scenarios.tex (with --scenarios <scenario_breakdown.json of analyze_fitting_g_scenarios.py>; exploratory) G
                         and tier of the new fits and of the Part D Xonotic fit per scenario, next to the pooled values
Usage: python experiments/make_fitting_outputs.py --dir ../repro_outputs/v4_fit --out ../repro_outputs/v4_fit/paper
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

MODES = {0: "hold", 1: "keep moving", 2: "chase", 3: "evade"}
TREES = ["CSO-BT", "OW-BT", "AC-BT", "XO-BT"]
WEIGHTS = [("w_objective", "$w_{\\textsc{Obj}}$"), ("w_engage", "$w_{\\textsc{Eng}}$"), ("w_resource", "$w_{\\textsc{Res}}$"),
           ("w_team", "$w_{\\textsc{Team}}$"), ("w_commitment", "$w_{\\mathrm{commit}}$")]
STYLE_TEX = {"Mission–Cooperation": "Mission--Cooperation", "Persistent Objective": "Persistent Objective",
             "Aggressive": "Aggressive", "Survival-Aware": "Survival-Aware"}
MAP_TEX = {"random": "random", "urban": "urban", "random_s101": "random 101", "urban_s101": "urban 101",
           "blocks": "blocks"}


def style_tex(s: str) -> str:
    for a, b in STYLE_TEX.items():
        s = s.replace(a, b)
    return s.replace("[route off]", "(route off)")


def results_table(summary: dict, fitted: dict) -> str:
    head = ["Tree", "Mode"] + [lab for _, lab in WEIGHTS] + [
        "Own nearest", "$G$ [95\\% CI]", "Closest designed style", "Noise floor", "AUC fingerprint", "AUC label-free",
        "max $|d|$", "Held-out ($G<0.5$)", "Verdict"]
    lines = ["\\begin{tabular}{ll" + "c" * len(WEIGHTS) + "cclcccccl}", "\\toprule", " & ".join(head) + " \\\\",
             "\\midrule"]
    for t in TREES:
        if t not in summary:
            continue
        r, f = summary[t], fitted[t]
        gm, nf, cl = r["game_maps"], r["noise_floor"], r["classifier"]
        dmax_key = max(r["untargeted_d"], key=lambda k: abs(r["untargeted_d"][k]))
        n_ok = sum(1 for m in r["heldout"].values() if m["nearest"] == t and m["G"] < 0.5)
        cells = [t, MODES.get(r["mode"], str(r["mode"]))] + [f"{f['weights'][k]:.2f}" for k, _ in WEIGHTS] + [
            f"{100 * gm['own_nearest_share']:.0f}\\%",
            f"{gm['G']:.2f} [{gm['G_ci'][0]:.2f}, {gm['G_ci'][1]:.2f}]",
            style_tex(gm["best_style"]),
            "within" if nf["within"] else "outside",
            f"{cl['fingerprint']['auc']:.2f} [{cl['fingerprint']['ci'][0]:.2f}, {cl['fingerprint']['ci'][1]:.2f}]",
            f"{cl['label_free']['auc']:.2f}",
            f"{abs(r['untargeted_d'][dmax_key]):.2f}",
            f"{n_ok}/{len(r['heldout'])}",
            r["verdict"]]
        lines.append(" & ".join(cells) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


def distances_table(summary: dict) -> str:
    lines = ["\\begin{tabular}{l" + "c" * len(TREES) + "}", "\\toprule",
             "Fitted to & " + " & ".join(TREES) + " \\\\", "\\midrule"]
    for t in TREES:
        if t not in summary:
            continue
        d = summary[t]["game_maps"]["D2"]
        best = min(d, key=d.get)
        cells = [(f"\\textbf{{{d[u]:.3f}}}" if u == best else f"{d[u]:.3f}") for u in TREES]
        lines.append(f"{t} & " + " & ".join(cells) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


def heldout_table(summary: dict) -> str:
    maps = list(next(summary[t] for t in TREES if t in summary)["heldout"])
    lines = ["\\begin{tabular}{l" + "c" * len(maps) + "}", "\\toprule",
             "Fitted to & " + " & ".join(MAP_TEX.get(m, m) for m in maps) + " \\\\", "\\midrule"]
    for t in TREES:
        if t not in summary:
            continue
        cells = []
        for m in maps:
            h = summary[t]["heldout"][m]
            mark = "" if h["nearest"] == t else f" ({h['nearest']})"
            cells.append(f"{h['G']:.2f}{mark}")
        lines.append(f"{t} & " + " & ".join(cells) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


def modes_table(modes: dict, fitted: dict) -> str:
    lines = ["\\begin{tabular}{l" + "c" * (len(MODES) + 1) + "}", "\\toprule",
             "Tree & " + " & ".join(MODES.values()) + " & pre-registered fit \\\\", "\\midrule"]
    for t in TREES:
        own = fitted[t]["combat_mode"]
        cells = []
        for m in MODES:
            v = f"{modes[t][str(m)]['validation_J']:.2f}"
            cells.append(f"\\underline{{{v}}}" if m == own else v)
        best = min(MODES, key=lambda m: modes[t][str(m)]["validation_J"])
        cells[best] = f"\\textbf{{{cells[best]}}}"
        lines.append(f"{t} & " + " & ".join(cells) + f" & {fitted[t]['validation_J']:.2f} \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


def gaps_table(md_path: Path) -> str:
    rows = [l for l in md_path.read_text().splitlines() if l.startswith("| P(")]
    lines = ["\\begin{tabular}{l" + "cc" * len(TREES) + "}", "\\toprule",
             "Situation $\\to$ goal & " + " & ".join(f"\\multicolumn{{2}}{{c}}{{{t}}}" for t in TREES) + " \\\\",
             " & " + " & ".join("tree & fit" for _ in TREES) + " \\\\", "\\midrule"]
    import re
    for r in rows:
        m = re.match(r"^\| P\((\w+) \| (.*?)\) \| (.*) \|$", r)
        goal, cond, rest = m.group(1), m.group(2), m.group(3)
        cells = [c.strip() for c in rest.split("|")]
        lines.append(f"{cond} $\\to$ {goal} & " + " & ".join(cells) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


def part_c_table(c: dict, prev: str = "B") -> str:
    head = ["Tree", "Mode", "$w_{\\textsc{Obj}}$", "$w_{\\textsc{Eng}}$", "$w_{\\textsc{Res}}$", "$w_{\\textsc{Team}}$",
            "$w_{\\mathrm{commit}}$", "$g_0$", "$\\tau$", "$\\eta$", "Own nearest", "$G$ [95\\% CI]", "$1-G^2$",
            "Held-out", f"$G$ Part {prev}", "$\\Delta G$ [95\\% CI]", "Tier"]
    kg = {"B": "G_part_b_same_seeds", "C": "G_part_c_same_seeds", "D": "G_part_d_same_seeds",
          "E": "G_part_e_same_seeds"}[prev]
    kd = {"B": "G_diff_C_minus_B", "C": "G_diff_D_minus_C", "D": "G_diff_E_minus_D", "E": "G_diff_F_minus_E"}[prev]
    rho = all("urgent_switch_relief" in c["trees"][t]["extension"] for t in TREES)
    if rho:
        head.insert(head.index("$\\eta$") + 1, "$\\rho$")
    lines = ["\\begin{tabular}{ll" + "c" * (15 if rho else 14) + "l}", "\\toprule", " & ".join(head) + " \\\\",
             "\\midrule"]
    for t in TREES:
        r = c["trees"][t]
        w, e = r["weights"], r["extension"]
        cells = [t, MODES[r["mode"]]] + [f"{w[k]:.2f}" for k, _ in WEIGHTS] + [
            f"{e['resource_idle_factor']:.2f}", f"{e['resource_distance_scale']:.1f}", f"{e['hunt_unseen']:.2f}"] + (
            [f"{e['urgent_switch_relief']:.2f}"] if rho else []) + [
            f"{100 * r['own_nearest_share']:.0f}\\%", f"{r['G']:.2f} [{r['G_ci'][0]:.2f}, {r['G_ci'][1]:.2f}]",
            f"{r['fit_index']:.2f}", f"{r['heldout_own_nearest']}/5 ({r['heldout_close']}/5)",
            f"{r[kg]:.2f}",
            f"${r[kd]:+.2f}$ [${r['G_diff_ci'][0]:+.2f}$, ${r['G_diff_ci'][1]:+.2f}$]", r["tier"]]
        lines.append(" & ".join(cells) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


def part_e_measures_table(extra: dict, prev: str = "D", cur: str = "E") -> str:
    """Exploratory (Part E, F): retreat, far pursuit and item control per agent, Deathmatch scenario, game-inspired
    maps and held-out maps (means over maps and episodes; analyze_fitting_e_extra.py with --prev fit<prev>)."""
    agents = [("AC-BT", "AssaultCube tree"), (f"fit{prev}[AC-BT]", f"\\quad Part {prev} fit"),
              ("fit[AC-BT]", f"\\quad Part {cur} fit"), ("XO-BT", "Xonotic tree"),
              (f"fit{prev}[XO-BT]", f"\\quad Part {prev} fit"), ("fit[XO-BT]", f"\\quad Part {cur} fit")]
    cols = [("retreat_share", "Retreat"), ("far_pursuit_share", "Far pursuit"), ("resource_goal_share_good", "Item control")]
    lines = ["\\begin{tabular}{l" + "cc" * len(cols) + "}", "\\toprule",
             " & " + " & ".join(f"\\multicolumn{{2}}{{c}}{{{lab}}}" for _, lab in cols) + " \\\\",
             "Agent & " + " & ".join("game & held-out" for _ in cols) + " \\\\", "\\midrule"]
    for ag, lab in agents:
        g = extra["means"]["game maps"][f"{ag}|Deathmatch"]
        h = extra["means"]["held-out maps"][f"{ag}|Deathmatch"]
        lines.append(f"{lab} & " + " & ".join(f"{g[c]:.2f} & {h[c]:.2f}" for c, _ in cols) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


G_EVAL_ROWS = [("fitD[XO-BT]", "XO-BT", "D"), ("fitE[XO-BT]", "XO-BT", "E"), ("fit[XO-BT]", "XO-BT", "F"),
               ("fit[CSO-BT]", "CSO-BT", "F"), ("fit[OW-BT]", "OW-BT", "F"), ("fit[AC-BT]", "AC-BT", "F")]
REVISED_TREES = {"AC-BT", "XO-BT"}


def g_eval_table(ev: dict) -> str:
    """Part G-eval: each fit against the revised trees ("adopted" in the paper: the trees used since 2026-09-27) and, on
    the same resamples, the earlier trees of Parts D-F (Xonotic per step, AssaultCube of 2026-09-25); CSO-BT and OW-BT
    were not revised, so their paired differences are left out."""
    head = ["Tree", "Fit", "Own nearest", "$G$ [95\\% CI]", "Held-out", "Tier", "Own nearest", "$G$ [95\\% CI]",
            "Held-out", "Tier", "$\\Delta D^2$ [95\\% CI]", "$\\Delta G$ [95\\% CI]"]
    lines = ["\\begin{tabular}{llcccl" + "cccl" + "cc}", "\\toprule",
             " & & \\multicolumn{4}{c}{Adopted trees} & \\multicolumn{4}{c}{Trees of Parts D--F} & "
             "\\multicolumn{2}{c}{Own tree: adopted $-$ Parts D--F} \\\\",
             "\\cmidrule(lr){3-6}\\cmidrule(lr){7-10}\\cmidrule(lr){11-12}", " & ".join(head) + " \\\\", "\\midrule"]

    def g(r: dict) -> str:
        return f"{r['G']:.2f} [{r['G_ci'][0]:.2f}, {r['G_ci'][1]:.2f}]"

    def diff(v: float, ci: list) -> str:
        return f"${v:+.2f}$ [${ci[0]:+.2f}$, ${ci[1]:+.2f}$]"

    for i, (f, tree, part) in enumerate(G_EVAL_ROWS):
        if i and G_EVAL_ROWS[i - 1][1] == "XO-BT" and tree != "XO-BT":
            lines.append("\\midrule")
        r, e, pd = ev["fits"][f]["revised"], ev["fits"][f]["earlier"], ev["fits"][f]["paired"]
        cells = [tree, f"Part {part}"]
        for x in (r, e):
            cells += [f"{100 * x['own_nearest_share']:.0f}\\%", g(x),
                      f"{x['heldout_own_nearest']}/5 ({x['heldout_close']}/5)", x["tier"]]
        cells += [diff(pd["dD2"], pd["dD2_ci"]), diff(pd["dG"], pd["dG_ci"])] if tree in REVISED_TREES else ["--", "--"]
        lines.append(" & ".join(cells) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


MODE_NAMES = {0: "hold", 1: "keep moving", 2: "chase", 3: "evade"}
SCENARIO_ORDER = ["Mission", "Deathmatch", "Control"]
NATIVE_SCENARIOS = {"CSO-BT": {"Mission", "Control"}, "OW-BT": {"Mission", "Control"}, "AC-BT": {"Deathmatch"},
                    "XO-BT": {"Deathmatch"}}
TIER_SHORT = {"close": "close", "improved": "improved", "not approximated": "not appr."}


def g_fit_table(gs: dict) -> str:
    """Part G-fit: the new fits against the adopted trees (pooled, pre-registered analysis)."""
    head = ["Tree", "Mode", "Searched", "$w_{\\textsc{Obj}}$", "$w_{\\textsc{Eng}}$", "$w_{\\textsc{Res}}$",
            "$w_{\\textsc{Team}}$", "$w_{\\mathrm{commit}}$", "$g_0$", "$\\tau$", "$\\eta$", "$\\rho$", "Own nearest",
            "$G$ [95\\% CI]", "$D^2$", "$1-G^2$", "Held-out", "$G$ Part F", "$\\Delta G$ [95\\% CI]", "Tier"]
    lines = ["\\begin{tabular}{lll" + "c" * 16 + "l}", "\\toprule", " & ".join(head) + " \\\\", "\\midrule"]
    for t in TREES:
        r = gs["trees"][t]
        w, e = r["weights"], r["extension"]
        pr = gs["paired"][f"fit[{t}] - fitF[{t}]"]
        cells = [t, MODE_NAMES[r["mode"]], ", ".join(MODE_NAMES[m] for m in r["searched_modes"])]
        cells += [f"{w[k]:.2f}" for k, _ in WEIGHTS]
        cells += [f"{e['resource_idle_factor']:.2f}", f"{e['resource_distance_scale']:.1f}", f"{e['hunt_unseen']:.2f}",
                  f"{e['urgent_switch_relief']:.2f}", f"{100 * r['own_nearest_share']:.0f}\\%",
                  f"{r['G']:.2f} [{r['G_ci'][0]:.2f}, {r['G_ci'][1]:.2f}]", f"{r['D2'][t]:.2f}", f"{r['fit_index']:.2f}",
                  f"{r['heldout_own_nearest']}/5 ({r['heldout_close']}/5)", f"{gs['earlier_fits'][f'fitF[{t}]']['G']:.2f}",
                  f"${pr['dG']:+.2f}$ [${pr['dG_ci'][0]:+.2f}$, ${pr['dG_ci'][1]:+.2f}$]", r["tier"]]
        lines.append(" & ".join(cells) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


def g_fit_scenario_table(br: dict, gs: dict) -> str:
    """Exploratory: G and tier per scenario of the new fits and of the Part D Xonotic fit (native scenarios in bold),
    next to the pooled values of the pre-registered analysis."""
    lines = ["\\begin{tabular}{ll" + "c" * (len(SCENARIO_ORDER) + 1) + "}", "\\toprule",
             "Fit & Tree & " + " & ".join(SCENARIO_ORDER) + " & Pooled \\\\", "\\midrule"]
    rows = [(f"fit[{t}]", t, "G-fit") for t in TREES] + [("fitD[XO-BT]", "XO-BT", "Part D fit")]
    for label, t, name in rows:
        cells = [name, t]
        for sc in SCENARIO_ORDER:
            r = br["scenarios"][sc][label]
            txt = f"{r['G']:.2f} {TIER_SHORT[r['tier']]}"
            cells.append(f"\\textbf{{{txt}}}" if sc in NATIVE_SCENARIOS[t] else txt)
        pooled = gs["trees"][t] if label.startswith("fit[") else gs["earlier_fits"][label]
        cells.append(f"{pooled['G']:.2f} {TIER_SHORT[pooled['tier']]}")
        lines.append(" & ".join(cells) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


def tree_distance_table(d: Path) -> str:
    import sys
    import pandas as pd
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import analyze_fitting as af      # frozen analysis: distances
    df = pd.read_csv(d / "test_rows.csv")
    s0 = json.loads((d / "stage0.json").read_text())
    cells = af.Cells(df, af.FP)
    sc = af.scales_for(df, s0, af.TRAIN_MAPS)
    lines = ["\\begin{tabular}{l" + "c" * len(TREES) + "}", "\\toprule", " & " + " & ".join(TREES) + " \\\\",
             "\\midrule"]
    for a in TREES:
        lines.append(f"{a} & " + " & ".join("--" if a == b else f"{af.d2(cells, a, b, sc):.2f}" for b in TREES)
                     + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="../repro_outputs/v4_fit")
    p.add_argument("--out", required=True)
    p.add_argument("--modes", default="", help="(exploratory) modes_validation.json of run_fitting_modes.py")
    p.add_argument("--gaps", default="", help="(exploratory) fitting_gaps.md of diagnose_fitting_gaps.py")
    p.add_argument("--tree-distances", action="store_true", help="D2 between the trees (needs analyze_fitting)")
    p.add_argument("--fingerprint-d", action="store_true", help="tree distances on the Part D fingerprint")
    p.add_argument("--fingerprint-e", action="store_true", help="tree distances on the Part E fingerprint")
    p.add_argument("--scenarios", default="", help="(exploratory) scenario_breakdown.json of analyze_fitting_g_scenarios.py")
    a = p.parse_args()
    if a.fingerprint_d or a.fingerprint_e:
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import run_fitting as rf
        extra = ["kill_rate_per_100", "death_rate_per_100", "los_frac", "resource_goal_share_good"]
        if a.fingerprint_e:
            extra += ["retreat_share", "far_pursuit_share", "contact_distance"]
        rf.FP[:] = rf.FP + [m for m in extra if m not in rf.FP]
        rf.OUTCOMES[:] = [m for m in rf.OUTCOMES if m not in rf.FP]
    d, out = Path(a.dir), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if (d / "eval_summary.json").exists():
        (out / "fitting_g_eval.tex").write_text(g_eval_table(json.loads((d / "eval_summary.json").read_text())) + "\n")
        print(f"written: {out}/fitting_g_eval.tex")
        if not (d / "fitting_summary.json").exists():
            return
    if (d / "fitting_g_summary.json").exists():
        gs = json.loads((d / "fitting_g_summary.json").read_text())
        (out / "fitting_g.tex").write_text(g_fit_table(gs) + "\n")
        if a.scenarios:
            br = json.loads(Path(a.scenarios).read_text())
            (out / "fitting_g_scenarios.tex").write_text(g_fit_scenario_table(br, gs) + "\n")
        print(f"written: {out}/fitting_g.tex" + (", fitting_g_scenarios.tex" if a.scenarios else ""))
    summary = json.loads((d / "fitting_summary.json").read_text())
    fitted = json.loads((d / "fitted.json").read_text())
    (out / "fitting_results.tex").write_text(results_table(summary, fitted) + "\n")
    (out / "fitting_distances.tex").write_text(distances_table(summary) + "\n")
    (out / "fitting_heldout.tex").write_text(heldout_table(summary) + "\n")
    if a.modes:
        (out / "fitting_modes.tex").write_text(modes_table(json.loads(Path(a.modes).read_text()), fitted) + "\n")
    if a.gaps:
        (out / "fitting_gaps.tex").write_text(gaps_table(Path(a.gaps)) + "\n")
    if (d / "fitting_c_summary.json").exists():
        (out / "fitting_c.tex").write_text(part_c_table(json.loads((d / "fitting_c_summary.json").read_text())) + "\n")
    if (d / "fitting_d_summary.json").exists():
        (out / "fitting_d.tex").write_text(part_c_table(json.loads((d / "fitting_d_summary.json").read_text()),
                                                        prev="C") + "\n")
    if (d / "fitting_e_summary.json").exists():
        (out / "fitting_e.tex").write_text(part_c_table(json.loads((d / "fitting_e_summary.json").read_text()),
                                                        prev="D") + "\n")
    if (d / "fitting_f_summary.json").exists():
        (out / "fitting_f.tex").write_text(part_c_table(json.loads((d / "fitting_f_summary.json").read_text()),
                                                        prev="E") + "\n")
    if (d / "fitting_e_extra.json").exists():
        extra = json.loads((d / "fitting_e_extra.json").read_text())
        if (d / "fitting_f_summary.json").exists():
            (out / "fitting_f_measures.tex").write_text(part_e_measures_table(extra, prev="E", cur="F") + "\n")
        else:
            (out / "fitting_e_measures.tex").write_text(part_e_measures_table(extra) + "\n")
    if a.tree_distances:
        (out / "fitting_tree_distances.tex").write_text(tree_distance_table(d) + "\n")
    print(f"written: {out}/fitting_results.tex, fitting_distances.tex, fitting_heldout.tex")


if __name__ == "__main__":
    main()
