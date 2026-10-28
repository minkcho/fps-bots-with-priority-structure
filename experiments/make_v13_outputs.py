"""Tables and figures of the report's appendix on round v13 (2026-09-29; user: "부록으로만"), from the outputs of the
frozen round (FAMILY_ADAPT_PLAN_V13_2026-09-29.md): repro_outputs/v13_family/ (summary.json, rows_a.csv, rows_b.csv,
rows_c.csv) and repro_outputs/v13_adapt/ (summary.json, bins_step.csv). No simulation.
Writes new_paper/tables/v13_fv.tex (FV-H1, FV-H2), v13_fv4.tex (FV-H4), v13_wa_open.tex (WA-H1-H3),
v13_wa_closed.tex (WA-H4) and new_paper/figures/fig_v13_form.pdf, fig_v13_adaptation.pdf.
Usage: python experiments/make_v13_outputs.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

plt.rcParams.update({"font.size": 10.5, "legend.fontsize": 8.5})

ROOT = Path(__file__).resolve().parents[2]
FV, WA = ROOT / "repro_outputs" / "v13_family", ROOT / "repro_outputs" / "v13_adapt"
TABLES, FIGURES = ROOT / "new_paper" / "tables", ROOT / "new_paper" / "figures"
MAPS = ["random", "urban"]
SCEN = ["Mission", "Deathmatch", "Control"]
SETS = [("main", r"main: $1/(1+d)$"), ("inv_h4", r"inverse, $h=4$"), ("inv_h8", r"inverse, $h=8$"),
        ("inv_h16", r"inverse, $h=16$"), ("exp_h4", r"exp, $h=4$"), ("exp_h8", r"exp, $h=8$"),
        ("exp_h16", r"exp, $h=16$"), ("dwell_matched", "matched dwell")]
COND = {"R1@Agg": ("R1 @ Agg., Control", "objective share"), "R2@Agg": ("R2 @ Agg., Deathmatch", "ally distance"),
        "R3@MC": ("R3 @ M--C, Deathmatch", "Resource-goal share"),
        "R3goal@MC": ("R3 goal part @ M--C", "Resource-goal share"),
        "R3route@Agg": (r"R3 route part @ Agg.", "expected hits"),
        "R4@PO": ("R4 @ P.O., Deathmatch", "line of sight"), "R4@MC": ("R4 @ M--C, Deathmatch", "Enemy-goal share")}
RATIOS = {"objective": ("obj", "alive", 1.0), "resource": ("res", "alive", 1.0), "enemy": ("enemy", "alive", 1.0),
          "switches": ("switches", "alive", 100.0), "exp_hits": ("exp_hits", "alive", 1.0),
          "los": ("los", "alive", 1.0), "ally_dist": ("ally_sum", "ally_n", 1.0)}
MEASURE = {"R1@Agg": "objective", "R2@Agg": "ally_dist", "R3@MC": "resource", "R3goal@MC": "resource",
           "R3route@Agg": "exp_hits", "R4@PO": "los", "R4@MC": "enemy"}
STYLE = {"MC": "M--C", "PO": "P.O.", "Agg": "Agg.", "SA": "S-A"}


def p_fmt(p: float) -> str:
    return r"$<$0.001" if p < 0.001 else f"{p:.3f}"


def fv_tables(fv: dict, a: pd.DataFrame, c: pd.DataFrame) -> None:
    acc = {(t["set"], t["map"], t["scenario"]): t["accuracy"] for t in fv["FV-H1"]["tests"]}
    far = pd.concat([a, c[c["variant"] == "dwell_matched"]])
    far = far[far["scenario"] == "Mission"].groupby(["variant", "style", "map"])["far_objective_share"].mean()
    lines = [r"\begin{tabular}{l" + "c" * 6 + "c" * 4 + "}", r"\toprule",
             r" & \multicolumn{6}{c}{Style classification accuracy (FV-H1)} & \multicolumn{4}{c}{Far-objective share, "
             r"Mission (FV-H2)} \\",
             r"\cmidrule(lr){2-7}\cmidrule(lr){8-11}",
             r" & \multicolumn{3}{c}{random} & \multicolumn{3}{c}{urban} & \multicolumn{2}{c}{M--C} & "
             r"\multicolumn{2}{c}{P.O.} \\",
             r"Variant & Mission & Deathm. & Control & Mission & Deathm. & Control & random & urban & random & urban \\",
             r"\midrule"]
    for key, label in SETS:
        cells = [f"{acc[(key, m, sc)]:.2f}" for m in MAPS for sc in SCEN]
        shares = [f"{far[(key, s, m)]:.2f}" for s in ("MC", "PO") for m in MAPS]
        lines.append(f"{label} & " + " & ".join(cells + shares) + r" \\")
        if key in ("main", "inv_h16", "exp_h16"):
            lines.append(r"\addlinespace")
    lines += [r"\bottomrule", r"\end{tabular}"]
    (TABLES / "v13_fv.tex").write_text("\n".join(lines) + "\n")

    tests = {(t["style"], t["measure"], t["map"]): t for t in fv["FV-H4"]["tests"]}
    sw = c[c["scenario"] == "Deathmatch"].groupby(["style", "variant", "map"])["goal_switch_rate_per_100"].mean()
    names = [("goal_switch_rate_per_100", "Goal switches per 100 steps"),
             ("engagement_redirection_rate_per_100", "Engagement redirection per 100 steps"),
             ("resource_goal_share_good", "Item control (good status)"), ("retreat_share", "Retreat share")]
    lines = [r"\begin{tabular}{llcccccc}", r"\toprule",
             r" & & \multicolumn{3}{c}{random} & \multicolumn{3}{c}{urban} \\",
             r"\cmidrule(lr){3-5}\cmidrule(lr){6-8}",
             r"Style (dwell $N$) & Measure (Deathmatch) & penalty & dwell & $p_{\mathrm{Holm}}$ & penalty & dwell & "
             r"$p_{\mathrm{Holm}}$ \\", r"\midrule"]
    for s, n in (("MC", 20), ("PO", 120)):
        for col, name in names:
            row = [f"{STYLE[s]} ({n})" if col == names[0][0] else "", name]
            for m in MAPS:
                if col == "goal_switch_rate_per_100":
                    row += [f"{sw[(s, 'main', m)]:.2f}", f"{sw[(s, 'dwell_matched', m)]:.2f}", "--"]
                else:
                    t = tests[(s, col, m)]
                    row += [f"{t['mean_y']:.2f}", f"{t['mean_x']:.2f}", p_fmt(t["p_holm"])]
            lines.append(" & ".join(row) + r" \\")
        lines.append(r"\addlinespace")
    lines = lines[:-1] + [r"\bottomrule", r"\end{tabular}"]
    (TABLES / "v13_fv4.tex").write_text("\n".join(lines) + "\n")


def window(bins: pd.DataFrame, bins_range, measure: str) -> pd.Series:
    """Mean over episodes of the per-episode measure over the window (ratio of the window's sums), per condition,
    schedule and map -- the values the tests of analyze_weight_adaptation.py compare."""
    num, den, f = RATIOS[measure]
    w = bins[bins["bin"].isin(list(bins_range))]
    g = w.groupby(["condition", "schedule", "map", "episode"])[[num, den]].sum()
    per_episode = f * g[num] / g[den].replace(0, np.nan)
    return per_episode.groupby(["condition", "schedule", "map"]).mean()


def wa_tables(wa: dict, bins: pd.DataFrame) -> None:
    late = {c: window(bins, range(14, 22), MEASURE[c]) for c in COND}
    first_sw = window(bins, [8], "switches")
    h1 = {(t["rule"], t["schedule"], t["map"]): t["p_holm"] for t in wa["WA-H1"]["tests"]}
    lines = [r"\begin{tabular}{llcccccccl}", r"\toprule",
             r" & & & \multicolumn{3}{c}{Measure, steps 351--550} & \multicolumn{3}{c}{Goal switches, steps 201--225} & \\",
             r"\cmidrule(lr){4-6}\cmidrule(lr){7-9}",
             r"Condition & Measure & Map & unchanged & abrupt & gradual & unchanged & abrupt & gradual & "
             r"WA-H1 $p_{\mathrm{Holm}}$ (a / g) \\", r"\midrule"]
    for cond, (label, mname) in COND.items():
        for i, m in enumerate(MAPS):
            v = [late[cond][(cond, s, m)] for s in ("none", "abrupt", "gradual")]
            fmt = "{:.2f}" if MEASURE[cond] == "ally_dist" else "{:.3f}"
            sv = [first_sw[(cond, s, m)] for s in ("none", "abrupt", "gradual")]
            ps = (f"{p_fmt(h1[(cond, 'abrupt', m)])} / {p_fmt(h1[(cond, 'gradual', m)])}"
                  if (cond, "abrupt", m) in h1 else "--")
            lines.append(" & ".join([label if i == 0 else "", mname if i == 0 else "", m]
                                    + [fmt.format(x) for x in v] + [f"{x:.2f}" for x in sv] + [ps]) + r" \\")
        lines.append(r"\addlinespace")
    lines = lines[:-1] + [r"\bottomrule", r"\end{tabular}"]
    (TABLES / "v13_wa_open.tex").write_text("\n".join(lines) + "\n")

    a = {(t["rule"], t["style"], t["scenario"]): t for t in wa["WA-H4a"]["tests"]}
    b = {(t["rule"], t["style"], t["scenario"]): t for t in wa["WA-H4b"]["tests"]}
    lines = [r"\begin{tabular}{lllcccccccc}", r"\toprule",
             r" & & & \multicolumn{4}{c}{(b) after the first activation} & \multicolumn{4}{c}{(a) on the active steps} \\",
             r"\cmidrule(lr){4-7}\cmidrule(lr){8-11}",
             r"Rule & Style & Scenario & $n$ & gradual & fixed & $p_{\mathrm{Holm}}$ & $n$ & gradual & fixed & "
             r"$p_{\mathrm{Holm}}$ \\", r"\midrule"]
    for rule, measure in (("R2", "ally distance"), ("R1", "points per step, own $-$ opponent")):
        keys = [k for k in b if k[0] == rule]
        for i, k in enumerate(keys):
            tb, ta = b[k], a.get(k)
            row = [f"{rule}: {measure}" if i == 0 else "", STYLE[k[1]], k[2], str(tb["n"]), f"{tb['mean_x']:.2f}",
                   f"{tb['mean_y']:.2f}", p_fmt(tb["p_holm"])]
            row += ([str(ta["n"]), f"{ta['mean_x']:.2f}", f"{ta['mean_y']:.2f}", p_fmt(ta["p_holm"])] if ta else
                    ["--"] * 4)
            lines.append(" & ".join(row) + r" \\")
        lines.append(r"\addlinespace")
    lines = lines[:-1] + [r"\bottomrule", r"\end{tabular}"]
    (TABLES / "v13_wa_closed.tex").write_text("\n".join(lines) + "\n")


def fig_form(a: pd.DataFrame, b: pd.DataFrame) -> None:
    fig, ax = plt.subplots(1, 3, figsize=(11, 3.7))
    mis = a[a["scenario"] == "Mission"].groupby(["style", "variant"])["far_objective_share"].mean()
    for s, color in (("PO", "tab:red"), ("MC", "tab:blue")):
        hs_i = [1, 4, 8, 16]
        ax[0].plot(hs_i, [mis[(s, "main" if h == 1 else f"inv_h{h}")] for h in hs_i], "o-", color=color,
                   label=STYLE[s].replace("--", "–") + " inverse")
        ax[0].plot([4, 8, 16], [mis[(s, f"exp_h{h}")] for h in (4, 8, 16)], "s--", color=color,
                   label=STYLE[s].replace("--", "–") + " exp")
    ax[0].set_xscale("log", base=2)
    ax[0].set_xticks([1, 4, 8, 16], ["1 (main)", "4", "8", "16"])
    ax[0].set_xlabel("half-distance h (cells)")
    ax[0].set_ylabel("far-objective share (Mission)")
    ax[0].set_title("(a) distance transform", fontsize=10)
    ax[0].legend(loc="lower left")
    dm = b[b["scenario"] == "Deathmatch"].groupby("variant")[
        ["goal_switch_rate_per_100", "engagement_redirection_rate_per_100", "retreat_share"]].mean()
    pen = [v for v in dm.index if v.startswith("pen_")]
    dwell = ["pen_0.00"] + [f"dwell_{n}" for n in (2, 5, 10, 20, 40)]
    for k, (col, title) in enumerate((("engagement_redirection_rate_per_100", "(b) engagement redirection"),
                                      ("retreat_share", "(c) retreat share")), start=1):
        for keys, style, lab in ((sorted(pen, key=lambda v: float(v[4:])), "o-", r"penalty $w_{\mathrm{commit}}$"),
                                 (dwell, "s--", r"dwell $N$ ($w_{\mathrm{commit}}=0$)")):
            x, y = dm.loc[keys, "goal_switch_rate_per_100"], dm.loc[keys, col]
            ax[k].plot(x, y, style, label=lab)
            for kk, xx, yy in zip(keys, x, y):
                tag = kk[4:] if kk.startswith("pen_") else ("0" if kk == "pen_0.00" else kk[6:])
                if kk != "pen_0.00" or style == "o-":
                    ax[k].annotate(tag, (xx, yy), fontsize=7.5, xytext=(3, 3), textcoords="offset points")
        ax[k].set_xscale("log")
        ax[k].set_xlabel("goal switches per 100 steps (Deathmatch)")
        ax[k].set_ylabel(col.replace("_rate_per_100", " per 100 steps").replace("_", " "))
        ax[k].set_title(f"{title}\nMission–Cooperation, Deathmatch", fontsize=10)
        ax[k].legend()
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_v13_form.pdf")
    plt.close(fig)


def fig_adaptation(bins: pd.DataFrame) -> None:
    panels = [("R1@Agg", "objective", "(a) R1 @ Agg.: objective share (Control)"),
              ("R2@Agg", "ally_dist", "(b) R2 @ Agg.: ally distance"),
              ("R2@Agg", "switches", "(c) R2 @ Agg.: goal switches per 100"),
              ("R3goal@MC", "resource", "(d) R3 goal part @ M–C: Resource-goal share"),
              ("R3route@Agg", "exp_hits", "(e) R3 route part @ Agg.: expected hits"),
              ("R3route@Agg", "switches", "(f) R3 route part @ Agg.: goal switches per 100")]
    fig, axes = plt.subplots(2, 3, figsize=(11, 6.0), sharex=True)
    steps = 25 * np.arange(22) + 12.5
    for ax, (cond, measure, title) in zip(axes.ravel(), panels):
        num, den, f = RATIOS[measure]
        g = bins[bins["condition"] == cond].groupby(["schedule", "bin"])[[num, den]].sum()
        s = (f * g[num] / g[den]).unstack("bin")
        for sch, color, lab in (("none", "0.5", "unchanged"), ("abrupt", "tab:red", "abrupt (T = 1)"),
                                ("gradual", "tab:blue", "gradual (T = 50)")):
            ax.plot(steps, s.loc[sch].to_numpy(), color=color, label=lab, lw=1.6)
        ax.axvline(200, color="k", ls=":", lw=1)
        ax.set_title(title, fontsize=9.5)
    for ax in axes[1]:
        ax.set_xlabel("step (25-step bins; change from step 201)")
    axes[0, 0].legend()
    fig.tight_layout()
    fig.savefig(FIGURES / "fig_v13_adaptation.pdf")
    plt.close(fig)


def main() -> None:
    fv = json.loads((FV / "summary.json").read_text())
    wa = json.loads((WA / "summary.json").read_text())
    a, b, c = (pd.read_csv(FV / f"rows_{p}.csv") for p in ("a", "b", "c"))
    bins = pd.read_csv(WA / "bins_step.csv")
    fv_tables(fv, a, c)
    wa_tables(wa, bins)
    fig_form(a, b)
    fig_adaptation(bins)
    print("written:", *(str(p.relative_to(ROOT)) for p in (TABLES / "v13_fv.tex", TABLES / "v13_fv4.tex",
                                                          TABLES / "v13_wa_open.tex", TABLES / "v13_wa_closed.tex",
                                                          FIGURES / "fig_v13_form.pdf",
                                                          FIGURES / "fig_v13_adaptation.pdf")))


if __name__ == "__main__":
    main()
