"""Per-scenario summary across the fitting rounds with source-based trees (2026-09-28; exploratory; user: "결과 나오면
시나리오별로 정리해서 보여줘"). Reads the per-scenario breakdowns (analyze_fitting_scenarios.py for Parts D, E, F and
G-eval; analyze_fitting_g_scenarios.py for Part G-fit) and the pooled results of the pre-registered analyses, and writes
one table per tree: rows = the fits (target trees in brackets), columns = Mission / Deathmatch / Control (G and the
exploratory tier; native scenarios marked *) and the pooled G and tier of the pre-registered analysis.
Formatting only; nothing is simulated or re-estimated.
Usage: python experiments/summarize_scenarios.py --root ../repro_outputs --out ../repro_outputs/scenario_summary_2026-09-28.md
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

GAMES = ["CSO-BT", "OW-BT", "AC-BT", "XO-BT"]
SCENARIOS = ["Mission", "Deathmatch", "Control"]
NATIVE = {"CSO-BT": {"Mission", "Control"}, "OW-BT": {"Mission", "Control"}, "AC-BT": {"Deathmatch"},
          "XO-BT": {"Deathmatch"}}
TIER = {"close": "close", "improved": "improved", "not approximated": "not appr."}
# (row label, target, breakdown dir, label in the breakdown, pooled file, pooled kind, trees it applies to)
ROWS = [
    ("Part D fit", "D–F trees", "v6_fit_scenarios", "fit[{g}]", "v6_fit/fitting_d_summary.json", "trees", GAMES),
    ("Part E fit", "D–F trees", "v7_fit_scenarios", "fit[{g}]", "v7_fit/fitting_e_summary.json", "trees", GAMES),
    ("Part F fit", "D–F trees", "v8_fit_scenarios", "fit[{g}]", "v8_fit/fitting_f_summary.json", "trees", GAMES),
    ("Part F fit, G-eval", "adopted", "v10_eval_scenarios", "fit[{g}]", "v10_eval/eval_summary.json", "geval", GAMES),
    ("Part D fit, G-eval", "adopted", "v10_eval_scenarios", "fitD[{g}]", "v10_eval/eval_summary.json", "geval", ["XO-BT"]),
    ("Part E fit, G-eval", "adopted", "v10_eval_scenarios", "fitE[{g}]", "v10_eval/eval_summary.json", "geval", ["XO-BT"]),
    ("Part D fit, G-fit seeds", "adopted", "v11_fit_scenarios", "fitD[{g}]", "v11_fit/fitting_g_summary.json", "gfit_cmp",
     ["XO-BT"]),
    ("**G-fit**", "adopted", "v11_fit_scenarios", "fit[{g}]", "v11_fit/fitting_g_summary.json", "trees", GAMES),
]


def pooled(root: Path, path: str, kind: str, label: str, g: str) -> tuple[float, str]:
    j = json.loads((root / path).read_text())
    if kind == "trees":
        r = j["trees"][g]
        return r["G"], r["tier"]
    if kind == "geval":
        r = j["fits"][label]["revised"]
        return r["G"], r["tier"]
    r = j["earlier_fits"][label]                                    # comparison fits of Part G-fit
    return r["G"], r["tier"]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="../repro_outputs")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    root = Path(a.root)
    br = {}
    md = ["# Fits per scenario across the rounds with source-based trees (exploratory)", "",
          "G and exploratory tier per scenario (the scenario's dimensions only; native scenarios marked *), and the "
          "pooled G and tier of the pre-registered analysis. Targets: 'D–F trees' = the trees of Parts D–F (per-step "
          "Xonotic tree, AssaultCube tree of 2026-09-25); 'adopted' = the trees since 2026-09-27. Values of different "
          "rounds come from different seeds and scales.", ""]
    for g in GAMES:
        head = " | ".join(f"{s}{'*' if s in NATIVE[g] else ''}" for s in SCENARIOS)
        md += [f"## {g}", "", f"| fit | target | {head} | pooled |", "|---|---|---|---|---|---|"]
        for name, target, bdir, lab, pfile, kind, trees in ROWS:
            if g not in trees:
                continue
            label = lab.format(g=g)
            if bdir not in br:
                f = root / bdir / "scenario_breakdown.json"
                br[bdir] = json.loads(f.read_text()) if f.exists() else None
            b = br[bdir]
            cells = []
            for s in SCENARIOS:
                r = (b or {}).get("scenarios", {}).get(s, {}).get(label)
                cells.append("n/a" if r is None else f"{r['G']:.2f} {TIER[r['tier']]}")
            try:
                pg, pt = pooled(root, pfile, kind, label, g)
                pcell = f"{pg:.2f} {TIER[pt]}"
            except (KeyError, FileNotFoundError):
                pcell = "n/a"
            md.append(f"| {name} | {target} | " + " | ".join(cells) + f" | {pcell} |")
        md.append("")
    Path(a.out).write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
