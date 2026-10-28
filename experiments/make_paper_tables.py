"""Emit the LaTeX (booktabs) tables of the main results from the saved final-run outputs (2026-09-24).

Replaces the hand-transcribed tables of the earlier drafts. Inputs (per map directory, random = --dir,
urban = --dir/urban): results.csv, baselines.csv, hypotheses_summary.json.
Outputs in --out:
  results_main.tex, results_urban.tex  behavioural metrics per style (mean +- 95% t CI; Control wins)
  hyp_tests.tex                        primary hypothesis tests of both maps (effect, p_Holm) and the
                                       earlier formulations (unadjusted p)
  baselines.tex                        external baselines next to the styles (random map; wins on both maps)
  testbed_comparison.tex               (with --earlier) primary tests on the earlier testbed and on --dir
  stall_rules.tex                      (with --stalls) episodes with a movement stall per set of testbed rules
Usage: python experiments/make_paper_tables.py --dir ../repro_outputs/v3 --out ../new_paper/tables
       python experiments/make_paper_tables.py --dir ../repro_outputs/v3_fixed --earlier ../repro_outputs/v3 \
           --stalls ../repro_outputs/v3/analysis --out ../new_paper/tables
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_stats import mean_ci, control_outcomes  # noqa: E402

STYLES = ["Mission–Cooperation", "Persistent Objective", "Aggressive", "Survival-Aware"]
STYLE_TEX = {"Mission–Cooperation": "Mission--Cooperation", "Persistent Objective": "Persistent Objective",
             "Aggressive": "Aggressive", "Survival-Aware": "Survival-Aware"}
BASELINES = [("CSO-BT", "CSO-BT"), ("OW-BT", "OW-BT"), ("AC-BT", "AC-BT"), ("XO-BT", "XO-BT"),
             ("UtilityAI", "Utility AI")]


def pm(v, nd=2):
    s = mean_ci(v)
    return "--" if s["mean"] is None else f"{s['mean']:.{nd}f} $\\pm$ {s['ci']:.{nd}f}"


def mean_str(v, nd=2):
    s = mean_ci(v)
    return "--" if s["mean"] is None else f"{s['mean']:.{nd}f}"


def fmt_p(p):
    return "$<0.001$" if p < 0.001 else f"{p:.3f}"


def results_table(df: pd.DataFrame) -> str:
    rows = []
    for st in STYLES:
        m = df[(df["scenario"] == "Mission") & (df["style"] == st)]
        d = df[(df["scenario"] == "Deathmatch") & (df["style"] == st)]
        c = df[(df["scenario"] == "Control") & (df["style"] == st)]
        co = control_outcomes(c)
        rows.append(" & ".join([STYLE_TEX[st], pm(m["objective_commitment_ratio"]), pm(m["avg_ally_proximity"]),
                                pm(d["engagement_redirection_rate_per_100"]), pm(d["resource_seeking_rate_per_100"]),
                                pm(d["walked_hits_per_step"], 3), pm(c["control_score"], 1),
                                f"{co['wins']}/{co['n']}"]) + " \\\\")
    head = ("\\begin{tabular}{lccccccc}\n\\toprule\n"
            " & \\multicolumn{2}{c}{Mission} & \\multicolumn{3}{c}{Deathmatch} & \\multicolumn{2}{c}{Control} \\\\\n"
            "\\cmidrule(lr){2-3}\\cmidrule(lr){4-6}\\cmidrule(lr){7-8}\n"
            "Style & ObjCommit & AllyDist & EngRedirect & ResSeek & WalkedHits & Score & Wins \\\\\n\\midrule\n")
    return head + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}"


PRETTY = [
    ("Kruskal-Wallis", "Kruskal--Wallis"), ("Control CtrlScore", "Control score"), ("SA Deaths", "SA deaths"),
    ("ObjCommit", "objective commitment"), ("AllyDist", "ally distance"),
    ("EngRedirect", "engagement redirection"), ("ResSeek", "resource seeking"), ("CtrlScore", "Control score"),
    ("GoalSwitches", "goal switches"), ("WalkedHits", "walked exposure"), ("LOSFraction", "LOS fraction"),
    ("Mission–Cooperation", "MC"), ("Persistent Objective", "PO"), ("Aggressive", "Agg"), ("Survival-Aware", "SA"),
    ("lambda_E configured - 0", "$\\lambda_E$ conf.\\ $-$ 0"), ("lambda_T 10 - 0", "$\\lambda_T$ 10 $-$ 0"),
    ("lambda x1 - x0", "$\\lambda\\times1-\\lambda\\times0$"), ("w_commit 0.45 - 0", "$w_{\\mathrm{commit}}$ 0.45 $-$ 0"),
    ("(full - weights-only)", "(full $-$ weights-only)"), (" -> ", " $\\to$ "), ("along alpha", "along $\\alpha$"),
    ("Style classification", "Style classification (5-fold CV)"),
    ("Sign test, walked exposure lower with the exposure term (all scenarios x styles)",
     "Sign test, walked exposure lower with the term (12 conditions)"),
]


def pretty(test: str) -> str:
    for a, b in PRETTY:
        test = test.replace(a, b)
    return test


def effect(t: dict) -> str:
    stat, eff = t.get("statistic", ""), t.get("effect", "")
    m = re.match(r"median diff = ([+-]?[\d.]+) \[([+-]?[\d.]+), ([+-]?[\d.]+)\]", stat)
    if m:
        r = re.search(r"r = ([+-]?[\d.]+)", eff)
        return f"${m.group(1)}$ [${m.group(2)}$, ${m.group(3)}$], $r={r.group(1)}$"
    if eff.startswith("eps2"):
        return "$\\varepsilon^2=" + eff.split("=")[1].strip() + "$"
    if stat.startswith("accuracy"):
        return "acc.\\ " + stat.split("=")[1].split("(")[0].strip()
    if stat.startswith("rho"):
        return "$\\rho=" + stat.split("=")[1].strip() + "$"
    if "conditions lower" in stat:
        return stat.replace(" conditions lower", " lower")
    return stat


def hyp_table(ra: dict, ua: dict) -> str:
    lines = ["\\begin{tabular}{llcccc}", "\\toprule",
             " & & \\multicolumn{2}{c}{Random map} & \\multicolumn{2}{c}{Urban map} \\\\",
             "\\cmidrule(lr){3-4}\\cmidrule(lr){5-6}",
             "Hyp. & Test & Effect & $p_{\\mathrm{Holm}}$ & Effect & $p_{\\mathrm{Holm}}$ \\\\", "\\midrule"]
    uby = {t["test"]: t for t in ua["primary"]}
    for t in ra["primary"]:
        u = uby[t["test"]]
        hyp = t['hypothesis'] + ("$^{\\ddagger}$" if t['hypothesis'] == "H3" else "")   # (2026-09-24) specified after the preliminary run
        lines.append(f"{hyp} & {pretty(t['test'])} & {effect(t)} & {fmt_p(t['p_holm'])} & "
                     f"{effect(u)} & {fmt_p(u['p_holm'])} \\\\")
    lines.append("\\midrule")
    lines.append("\\multicolumn{6}{l}{\\emph{Earlier formulations (not in the Holm family; unadjusted $p$)}} \\\\")
    uby = {(t["hypothesis"], t["test"]): t for t in ua["secondary"]}
    for t in ra["secondary"]:
        u = uby[(t["hypothesis"], t["test"])]
        hyp = t["hypothesis"].split(" (")[0]
        lines.append(f"{hyp} & {pretty(t['test'])} & {effect(t)} & {fmt_p(t['p'])} & "
                     f"{effect(u)} & {fmt_p(u['p'])} \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


def baselines_table(rb: pd.DataFrame, ub: pd.DataFrame, rr: pd.DataFrame, ur: pd.DataFrame) -> str:
    def row(label, r_sub, u_ctrl):
        m, d = r_sub("Mission"), r_sub("Deathmatch")
        wr, wu = control_outcomes(r_sub("Control")), control_outcomes(u_ctrl)
        return " & ".join([label, mean_str(m["objective_commitment_ratio"]), mean_str(m["avg_ally_proximity"]),
                           mean_str(d["engagement_redirection_rate_per_100"]),
                           mean_str(d["resource_seeking_rate_per_100"]),
                           f"{mean_str(d['kills'], 1)} / {mean_str(d['deaths'], 1)}",
                           f"{wr['wins']} / {wu['wins']}"]) + " \\\\"
    lines = ["\\begin{tabular}{lcccccc}", "\\toprule",
             " & \\multicolumn{2}{c}{Mission} & \\multicolumn{3}{c}{Deathmatch} & Control wins \\\\",
             "\\cmidrule(lr){2-3}\\cmidrule(lr){4-6}\\cmidrule(lr){7-7}",
             "Agent & ObjCommit & AllyDist & EngRedirect & ResSeek & Kills / Deaths & random / urban \\\\", "\\midrule"]
    for key, label in BASELINES:
        lines.append(row(label, lambda sc, k=key: rb[(rb["scenario"] == sc) & (rb["baseline"] == k)],
                         ub[(ub["scenario"] == "Control") & (ub["baseline"] == key)]))
    lines.append("\\midrule")
    for st in STYLES:
        lines.append(row(STYLE_TEX[st], lambda sc, s=st: rr[(rr["scenario"] == sc) & (rr["style"] == s)],
                         ur[(ur["scenario"] == "Control") & (ur["style"] == st)]))
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


def risk_budget_table(rd: Path, ud: Path) -> str:
    """Normalised risk budgets in Deathmatch: planner-level control (Survival-Aware, random map) and outcomes."""
    nb = {m: pd.read_csv(d / "risk_budget_normalised.csv") for m, d in (("random", rd), ("urban", ud))}
    main_df = {m: pd.read_csv(d / "results.csv") for m, d in (("random", rd), ("urban", ud))}

    def cell(df, st, beta, col, nd):
        sub = df[(df["style"] == st) & (df["beta"].astype(float) == beta)]
        return f"{sub[col].astype(float).mean():.{nd}f}"

    def fixed(m, st, col, nd):
        sub = main_df[m][(main_df[m]["scenario"] == "Deathmatch") & (main_df[m]["style"] == st)]
        return f"{sub[col].astype(float).mean():.{nd}f}"

    sa, ag = "Survival-Aware", "Aggressive"
    lines = ["\\begin{tabular}{lcccccccc}", "\\toprule",
             " & \\multicolumn{5}{c}{Survival-Aware} & \\multicolumn{3}{c}{Aggressive} \\\\",
             "\\cmidrule(lr){2-6}\\cmidrule(lr){7-9}",
             "$\\beta$ & Position & $\\mu$ & WalkedHits & Deaths & Deaths (urban) & WalkedHits & Deaths & Deaths (urban) \\\\",
             "\\midrule",
             " & ".join(["fixed", "--", "--", fixed("random", sa, "walked_hits_per_step", 3), fixed("random", sa, "deaths", 2),
                         fixed("urban", sa, "deaths", 2), fixed("random", ag, "walked_hits_per_step", 3),
                         fixed("random", ag, "deaths", 2), fixed("urban", ag, "deaths", 2)]) + " \\\\"]
    for beta in (1.0, 0.75, 0.5, 0.25, 0.0):
        r, u = nb["random"], nb["urban"]
        lines.append(" & ".join([f"{beta:.2f}", cell(r, sa, beta, "budget_position", 2), cell(r, sa, beta, "mean_lambda", 2),
                                 cell(r, sa, beta, "walked_hits_per_step", 3), cell(r, sa, beta, "deaths", 2),
                                 cell(u, sa, beta, "deaths", 2), cell(r, ag, beta, "walked_hits_per_step", 3),
                                 cell(r, ag, beta, "deaths", 2), cell(u, ag, beta, "deaths", 2)]) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


def h3_outcomes_table(rd: Path, hits_dir: Path) -> str:
    """(2026-09-24) Primary H3 readout next to the independent outcomes (hits taken, deaths), Deathmatch, per style.

    Walked exposure: primary test (p_Holm over the 20 primary tests of a map, from hypotheses_summary.json).
    Hits taken and deaths: cost-term ablation of the hits-taken rerun (identical episodes), paired Wilcoxon,
    Holm over the four styles of a map and readout."""
    from analyze_stats import wilcoxon_paired, holm
    prim = {"random": json.loads((rd / "hypotheses_summary.json").read_text())["primary"],
            "urban": json.loads((rd / "urban" / "hypotheses_summary.json").read_text())["primary"]}
    out = ["\\begin{tabular}{llccc}", "\\toprule",
           "Map & Style & Walked exposure (primary) & Hits taken & Deaths \\\\", "\\midrule"]
    for mp, sub in (("random", ""), ("urban", "urban")):
        ct = pd.read_csv(hits_dir / sub / "cost_term_ablation.csv")
        cells = {}
        for col in ("walked_hits_per_step", "hits_taken_per_step", "deaths"):
            tests, changes = [], []
            for st in STYLES:
                f = ct[(ct.scenario == "Deathmatch") & (ct["style"] == st) & (ct.variant == "full")].sort_values("episode")
                z = ct[(ct.scenario == "Deathmatch") & (ct["style"] == st) & (ct.variant == "no_exposure")].sort_values("episode")
                tests.append(wilcoxon_paired(f[col].values.astype(float), z[col].values.astype(float)))
                mf, mz = f[col].astype(float).mean(), z[col].astype(float).mean()
                changes.append(100.0 * (mf - mz) / mz)
            adj = holm([t["p"] for t in tests])
            cells[col] = [(c, t, a) for c, t, a in zip(changes, tests, adj)]
        byname = {t["test"]: t for t in prim[mp]}
        for i, st in enumerate(STYLES):
            key = f"Deathmatch {st} WalkedHits, lambda_E configured - 0"
            pw = byname[key]["p_holm"]
            c_w = cells["walked_hits_per_step"][i][0]
            c_h, t_h, a_h = cells["hits_taken_per_step"][i]
            c_d, t_d, a_d = cells["deaths"][i]
            out.append(" & ".join([mp if i == 0 else "", STYLE_TEX[st],
                                   f"${c_w:+.0f}\\%$, {fmt_p(pw)}",
                                   f"${c_h:+.0f}\\%$, $r={t_h['r']:+.2f}$, {fmt_p(a_h)}",
                                   f"${c_d:+.0f}\\%$, $r={t_d['r']:+.2f}$, {fmt_p(a_d)}"]) + " \\\\")
        out.append("\\midrule")
    out[-1] = "\\bottomrule"
    out.append("\\end{tabular}")
    return "\n".join(out)


def effect_short(t: dict) -> str:
    """(2026-09-25) Compact effect of a primary test: r for paired tests, else as in effect()."""
    stat, eff = t.get("statistic", ""), t.get("effect", "")
    if stat.startswith("median diff"):
        return "$r=" + re.search(r"r = ([+-]?[\d.]+)", eff).group(1) + "$"
    if "conditions lower" in stat:
        return stat.split(" conditions")[0]
    return effect(t)


def testbed_table(earlier: Path, present: Path) -> str:
    """(2026-09-25) Primary tests of both maps on the earlier testbed and on the present one (Holm within each
    testbed and map); p-values in bold mark tests whose verdict at 0.05 differs between the testbeds."""
    lines = ["\\begin{tabular}{llcccccccc}", "\\toprule",
             " & & \\multicolumn{4}{c}{Random map} & \\multicolumn{4}{c}{Urban map} \\\\",
             "\\cmidrule(lr){3-6}\\cmidrule(lr){7-10}",
             " & & \\multicolumn{2}{c}{Earlier} & \\multicolumn{2}{c}{Present} & \\multicolumn{2}{c}{Earlier} & "
             "\\multicolumn{2}{c}{Present} \\\\",
             "Hyp. & Test & Effect & $p_{\\mathrm{Holm}}$ & Effect & $p_{\\mathrm{Holm}}$ & Effect & $p_{\\mathrm{Holm}}$ & "
             "Effect & $p_{\\mathrm{Holm}}$ \\\\", "\\midrule"]
    load = lambda d: {t["test"]: t for t in json.loads((d / "hypotheses_summary.json").read_text())["primary"]}
    ra, rp, ua, up = load(earlier), load(present), load(earlier / "urban"), load(present / "urban")
    for name, t in ra.items():
        cells = []
        for a, b in ((t, rp[name]), (ua[name], up[name])):
            for x in (a, b):
                p = fmt_p(x["p_holm"])
                if (a["p_holm"] < 0.05) != (b["p_holm"] < 0.05):
                    p = "\\textbf{" + p + "}"
                cells += [effect_short(x), p]
        lines.append(f"{t['hypothesis']} & {pretty(name)} & " + " & ".join(cells) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


STALL_SETS = [("", "none (earlier testbed)"), ("swap", "teammate swap"), ("avoid", "local avoidance"),
              ("forget", "forget reached memory"), ("los", "symmetric line of sight"),
              ("fixes_no_los", "swap, avoidance, forget"), ("allfixes", "swap, avoidance, forget, LOS"),
              ("fixes5", "all five (final testbed)")]


def stall_rules_table(analysis: Path) -> str:
    """(2026-09-25) Episodes of the main experiment with a movement stall of at least 50 steps (either team), per
    set of testbed rules, from analyze_stalls.py outputs stalls_<map>[_<tag>].md."""
    def n(mp, tag):
        f = analysis / (f"stalls_{mp}_{tag}.md" if tag else f"stalls_{mp}.md")
        m = re.search(r"either team: (\d+)/(\d+)", f.read_text())
        return f"{int(m.group(1))}/{int(m.group(2))}"
    lines = ["\\begin{tabular}{lcc}", "\\toprule", "Rules on & Random map & Urban map \\\\", "\\midrule"]
    for tag, label in STALL_SETS:
        lines.append(f"{label} & {n('random', tag)} & {n('urban', tag)} \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="../repro_outputs/v3", help="random-map directory; the urban map is <dir>/urban")
    p.add_argument("--out", default="../new_paper/tables")
    p.add_argument("--earlier", default="", help="(2026-09-25) earlier-testbed directory for testbed_comparison.tex")
    p.add_argument("--stalls", default="", help="(2026-09-25) directory of analyze_stalls.py outputs for stall_rules.tex")
    p.add_argument("--baselines-dir", default="", help="(2026-09-26) read baselines.csv from this directory and its urban/ "
                   "(revised AssaultCube and Xonotic trees) instead of --dir")
    args = p.parse_args()
    rd, ud, out = Path(args.dir), Path(args.dir) / "urban", Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rr, ur = pd.read_csv(rd / "results.csv"), pd.read_csv(ud / "results.csv")
    (out / "results_main.tex").write_text(results_table(rr) + "\n")
    (out / "results_urban.tex").write_text(results_table(ur) + "\n")
    ra = json.loads((rd / "hypotheses_summary.json").read_text())
    ua = json.loads((ud / "hypotheses_summary.json").read_text())
    (out / "hyp_tests.tex").write_text(hyp_table(ra, ua) + "\n")
    bd = Path(args.baselines_dir) if args.baselines_dir else rd
    rb, ub = pd.read_csv(bd / "baselines.csv"), pd.read_csv(bd / "urban" / "baselines.csv")
    (out / "baselines.tex").write_text(baselines_table(rb, ub, rr, ur) + "\n")
    (out / "risk_budget.tex").write_text(risk_budget_table(rd, ud) + "\n")
    # hits taken: the final-run directory itself once its CSVs carry the column, else the 2026-09-24 rerun (v3_hits)
    has_col = "hits_taken_per_step" in pd.read_csv(rd / "cost_term_ablation.csv", nrows=1).columns
    hits_dir = rd if has_col else rd.parent / "v3_hits"
    if (hits_dir / "cost_term_ablation.csv").exists():
        (out / "h3_outcomes.tex").write_text(h3_outcomes_table(rd, hits_dir) + "\n")
    if args.earlier:
        (out / "testbed_comparison.tex").write_text(testbed_table(Path(args.earlier), rd) + "\n")
    if args.stalls:
        (out / "stall_rules.tex").write_text(stall_rules_table(Path(args.stalls)) + "\n")
    print(f"tables written to {out}")


if __name__ == "__main__":
    main()
