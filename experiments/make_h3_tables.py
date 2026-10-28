"""Emit LaTeX (booktabs) tables for the H3 route-channel sections from the saved results.

Inputs (relative to --root, default ../repro_outputs):
  h3_transit/headroom.txt, h3_transit/boundary.txt, h3_factorial/*.csv, h3_confirm/*.csv (optional)
Outputs: <out>/h3_headroom.tex, h3_boundary.tex, h3_factorial_dm.tex, h3_factorial_transit.tex,
         h3_factorial_effects.tex, h3_confirm.tex (if data present)
Usage: python experiments/make_h3_tables.py --root ../repro_outputs --out ../new_paper/tables
"""
from __future__ import annotations

import argparse
import csv
import statistics as st
from collections import defaultdict
from pathlib import Path


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def load(dirpath: Path):
    rows = []
    for f in sorted(dirpath.glob("*.csv")):
        rows += list(csv.DictReader(f.open(encoding="utf-8")))
    return rows


def mean(rows, k):
    v = [fnum(r.get(k)) for r in rows]
    v = [x for x in v if x is not None]
    return st.mean(v) if v else None


def fmt(x, nd=3):
    return "--" if x is None else f"{x:.{nd}f}"


def headroom_table(root: Path) -> str:
    lines = [l.strip() for l in (root / "h3_transit" / "headroom.txt").read_text().splitlines() if "|" in l][1:]
    out = ["\\begin{tabular}{llcccc}", "\\toprule",
           "Map & Exposure definition & $R_0$ per step & $R_{\\mathrm{safe}}/R_0$ & Length ratio & $\\lambda^{*}$ (median / p75) \\\\", "\\midrule"]
    for l in lines:
        m, name, r0, ratio, lr, nz, lmed, lp75 = [x.strip() for x in l.split("|")]
        name = name.replace("<=", "$\\le$").replace("P_hit(d)", "$P_{\\mathrm{hit}}(d)$").replace("1/d", "$1/d$").replace("0.2/d", "$0.2/d$")
        out.append(f"{m} & {name} & {r0} & {ratio} & {lr} & {lmed} / {lp75} \\\\")
    out += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(out)


def boundary_table(root: Path) -> str:
    lines = [l for l in (root / "h3_transit" / "boundary.txt").read_text().splitlines() if l.strip() and not l.lstrip().startswith("dL")]
    out = ["\\begin{tabular}{rrrr|ccccc}", "\\toprule",
           "$\\Delta L$ & Sentries & $\\Delta R$ (hits) & $\\Delta L/\\Delta R$ & hits/additive & hits/exp & hits/square & distance/additive & distance/exp \\\\", "\\midrule"]
    for l in lines:
        left, right = l.split("|")
        dL, ns, dR, ratio = left.split()
        cells = right.split()
        out.append(f"{dL} & {ns} & {dR} & {ratio} & " + " & ".join(cells) + " \\\\")
    out += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(out)


def factorial_tables(rows, lam_levels=("5", "10", "20")):
    groups = defaultdict(list)
    for r in rows:
        groups[(r["scenario"], r["map"], r["style"], r["field"], r["knowledge"], r["form"], r["replan"], f"{float(r['lam']):g}")].append(r)
    def base(sc, mp, sty, replan="0"):
        return groups.get((sc, mp, sty, "none", "none", "additive", replan, "0"), [])
    # Deathmatch SA: rows field x knowledge x form (replan 0), cells hits/step and deaths at lam 5/10/20
    out_dm = ["\\begin{tabular}{lll" + "cc" * (1 + len(lam_levels)) + "}", "\\toprule",
              "Field & Knowledge & Form & \\multicolumn{2}{c}{$\\lambda_E=0$} & " + " & ".join(f"\\multicolumn{{2}}{{c}}{{$\\lambda_E={l}$}}" for l in lam_levels) + " \\\\",
              " & & & hits & deaths" + " & hits & deaths" * len(lam_levels) + " \\\\", "\\midrule"]
    for mp in ("random", "urban"):
        b = base("deathmatch", mp, "SA")
        if not b:
            continue
        out_dm.append(f"\\multicolumn{{{3 + 2 * (1 + len(lam_levels))}}}{{l}}{{\\emph{{{mp} map}}}} \\\\")
        for field in ("distance", "hits", "anticipatory"):
            for kn in ("all", "memory"):
                for form in ("additive", "exp", "square"):
                    cells = [fmt(mean(b, "walked_hits_per_step"), 4), fmt(mean(b, "deaths"), 2)]
                    for l in lam_levels:
                        g = groups.get(("deathmatch", mp, "SA", field, kn, form, "0", l), [])
                        cells += [fmt(mean(g, "walked_hits_per_step"), 4), fmt(mean(g, "deaths"), 2)]
                    out_dm.append(f"{field} & {kn} & {form} & " + " & ".join(cells) + " \\\\")
    out_dm += ["\\bottomrule", "\\end{tabular}"]
    # Transit: per map, best of each field x form (knowledge all, replan 0) at lam 10: hits/step, arrived
    out_tr = ["\\begin{tabular}{llcccccc}", "\\toprule",
              "Map & Condition ($\\lambda_E=10$, omniscient, event replanning) & LOS steps & Walked hits & Detours & Length ratio & Arrival & First-life deaths \\\\", "\\midrule"]
    for mp in ("corridor", "random", "urban"):
        b = base("transit", mp, "Transit")
        if not b:
            continue
        out_tr.append(f"{mp} & distance-only A$^*$ ($\\lambda_E=0$) & {fmt(mean(b,'los_frac'))} & {fmt(mean(b,'walked_hits'),2)} & {fmt(mean(b,'plan_detour'))} & {fmt(mean(b,'plan_len_ratio'))} & {fmt(mean(b,'arrived'),2)} & {fmt(mean(b,'died_first_life'),2)} \\\\")
        for field in ("distance", "hits", "anticipatory"):
            for form in ("additive", "exp", "square"):
                g = groups.get(("transit", mp, "Transit", field, "all", form, "0", "10"), [])
                if not g:
                    continue
                out_tr.append(f" & {field}/{form} & {fmt(mean(g,'los_frac'))} & {fmt(mean(g,'walked_hits'),2)} & {fmt(mean(g,'plan_detour'))} & {fmt(mean(g,'plan_len_ratio'))} & {fmt(mean(g,'arrived'),2)} & {fmt(mean(g,'died_first_life'),2)} \\\\")
        gm = groups.get(("transit", mp, "Transit", "hits", "memory", "exp", "0", "10"), [])
        if gm:
            out_tr.append(f" & hits/exp, visible+remembered & {fmt(mean(gm,'los_frac'))} & {fmt(mean(gm,'walked_hits'),2)} & {fmt(mean(gm,'plan_detour'))} & {fmt(mean(gm,'plan_len_ratio'))} & {fmt(mean(gm,'arrived'),2)} & {fmt(mean(gm,'died_first_life'),2)} \\\\")
    out_tr += ["\\bottomrule", "\\end{tabular}"]
    # Main effects (relative change of walked hits/step vs baseline, conditions with lam >= 5) per set
    sets = sorted(set((r["scenario"], r["map"], r["style"]) for r in rows))
    out_ef = ["\\begin{tabular}{lll|ccc|cc|ccc|cc}", "\\toprule",
              "Scenario & Map & Style & distance & hits & anticip. & all & memory & additive & exp & square & replan 0 & replan 5 \\\\", "\\midrule"]
    for sc, mp, sty in sets:
        b = base(sc, mp, sty)
        bh = mean(b, "walked_hits_per_step")
        if not bh:
            continue
        rel = defaultdict(list)
        for key, g in groups.items():
            if key[:3] != (sc, mp, sty) or key[3] in ("none", "v2") or float(key[7]) < 5:
                continue
            h = mean(g, "walked_hits_per_step")
            if h is None:
                continue
            r = (h - bh) / bh
            rel["field:" + key[3]].append(r); rel["kn:" + key[4]].append(r); rel["form:" + key[5]].append(r); rel["replan:" + key[6]].append(r)
        cell = lambda k: f"{100 * st.mean(rel[k]):+.0f}\\%" if rel.get(k) else "--"
        out_ef.append(f"{('held-point control' if sc == 'control_hold' else sc.replace('_', ' '))} & {mp} & {sty} & " + " & ".join(cell(k) for k in ("field:distance", "field:hits", "field:anticipatory", "kn:all", "kn:memory", "form:additive", "form:exp", "form:square", "replan:0", "replan:5")) + " \\\\")
    out_ef += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(out_dm), "\n".join(out_tr), "\n".join(out_ef)


def confirm_table(rows, scenarios=None):
    """(2026-09-24) `scenarios` restricts the table to some scenarios (the full table overflows a page)."""
    groups = defaultdict(list)
    for r in rows:
        if scenarios is not None and r["scenario"] not in scenarios:
            continue
        groups[(r["scenario"], r["map"], r["style"], r["field"], r["knowledge"], r["form"], f"{float(r['lam']):g}")].append(r)
    sets = sorted(set(k[:3] for k in groups))
    out = ["\\begin{tabular}{llllcccc}", "\\toprule",
           "Scenario / map / style & Field & Knowledge & $\\lambda_E$ & Walked hits per step & LOS fraction & Deaths & Outcome \\\\", "\\midrule"]
    for sc, mp, sty in sets:
        outcome = "arrived" if sc == "transit" else ("win" if sc.startswith("control") else "kills")
        head = f"{('held-point control' if sc == 'control_hold' else sc.replace('_', ' '))} / {mp} / {sty}"
        for key in sorted((k for k in groups if k[:3] == (sc, mp, sty)), key=lambda k: (k[3] != "none", k[3] != "v2", k[3], k[4], float(k[6]))):
            g = groups[key]
            label = {"none": "distance-only A$^*$", "v2": "earlier additive model"}.get(key[3], f"{key[3]} / exp")
            out.append(f"{head} & {label} & {key[4] if key[3] not in ('none','v2') else '--'} & {key[6]} & {fmt(mean(g,'walked_hits_per_step'),4)} & {fmt(mean(g,'los_frac'))} & {fmt(mean(g,'deaths'),2)} & {outcome} {fmt(mean(g,outcome),2)} \\\\")
            head = ""
        out.append("\\midrule")
    out[-1] = "\\bottomrule"
    out.append("\\end{tabular}")
    return "\n".join(out)


def h2_switching_table(v3: Path) -> str:
    """w_commit sweep: goal switches per 100 steps and objective commitment, Mission and Control, both maps."""
    def load_sens(d):
        rows = list(csv.DictReader((d / "sensitivity_commitment.csv").open(encoding="utf-8")))
        wcol = [c for c in rows[0] if "commit" in c.lower() and c != "objective_commitment_ratio"][0]
        g = defaultdict(list)
        for r in rows:
            g[(r["scenario"], f"{float(r[wcol]):g}")].append(r)
        return g
    maps = {"random": load_sens(v3), "urban": load_sens(v3 / "urban")}
    ws = sorted({k[1] for g in maps.values() for k in g}, key=float)
    out = ["\\begin{tabular}{r|cccc|cccc}", "\\toprule",
           " & \\multicolumn{4}{c|}{Random map} & \\multicolumn{4}{c}{Urban map} \\\\",
           "$w_{\\mathrm{commit}}$ & Mission switches & Mission commit. & Control switches & Control wins & Mission switches & Mission commit. & Control switches & Control wins \\\\", "\\midrule"]
    for w in ws:
        cells = []
        for mp in ("random", "urban"):
            g = maps[mp]
            for sc in ("Mission", "Control"):
                rs = g.get((sc, w), [])
                sw = mean(rs, "goal_switch_rate_per_100"); cm = mean(rs, "objective_commitment_ratio")
                if sc == "Mission":
                    cells += [fmt(sw, 2), fmt(cm, 2)]
                else:
                    wins = sum(1 for r in rs if fnum(r.get("control_score")) is not None and fnum(r["control_score"]) >= 120)
                    cells += [fmt(sw, 2), f"{wins}/{len(rs)}" if rs else "--"]
        out.append(f"{float(w):g} & " + " & ".join(cells) + " \\\\")
    out += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(out)


def _earlier(label: str) -> str:
    """(2026-09-24) the paper calls the v2 model the earlier formulation."""
    return label.replace("(v2)", "(earlier)")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="../repro_outputs")
    p.add_argument("--out", default="../new_paper/tables")
    p.add_argument("--factorial-dir", default=None, help="factorial results directory (default <root>/h3_factorial)")
    p.add_argument("--confirm-dir", default=None, help="confirmation results directory (default <root>/h3_confirm)")
    p.add_argument("--v3-dir", default=None, help="v3 results directory with sensitivity_commitment.csv (and urban/) for the H2 switching table")
    args = p.parse_args()
    root, out = Path(args.root), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "h3_headroom.tex").write_text(_earlier(headroom_table(root)) + "\n")
    (out / "h3_boundary.tex").write_text(boundary_table(root) + "\n")
    fac = load(Path(args.factorial_dir) if args.factorial_dir else root / "h3_factorial")
    dm, tr, ef = factorial_tables(fac)
    (out / "h3_factorial_dm.tex").write_text(dm + "\n")
    (out / "h3_factorial_transit.tex").write_text(tr + "\n")
    (out / "h3_factorial_effects.tex").write_text(ef + "\n")
    cdir = Path(args.confirm_dir) if args.confirm_dir else root / "h3_confirm"
    if cdir.exists() and list(cdir.glob("*.csv")):
        crow = load(cdir)
        (out / "h3_confirm.tex").write_text(confirm_table(crow) + "\n")
        for tag, scs in (("transit", {"transit"}), ("dm", {"deathmatch"}), ("control", {"control"})):
            (out / f"h3_confirm_{tag}.tex").write_text(confirm_table(crow, scs) + "\n")
        print("confirm table written from", cdir)
    if args.v3_dir:
        (out / "h2_switching.tex").write_text(h2_switching_table(Path(args.v3_dir)) + "\n")
        print("H2 switching table written")
    print("tables written to", out)


if __name__ == "__main__":
    main()
