"""Paper table: the designed style nearest to each external baseline, per scenario and pooled (2026-09-27).

Reads <dir>/extra_summary.json and <dir>/urban/extra_summary.json (analyze_extra.py: "baselines" -> "fingerprint",
Euclidean distances in the normalised four-metric space, per scenario and pooled over the three scenarios) and writes a
LaTeX table with, per map and scenario, the nearest style, its distance and the margin to the second-nearest style.
Native scenarios (the kind of game mode each tree was written for, fixed before looking at these distances): the
objective scenarios Mission and Control for CSO-BT and OW-BT (Overwatch's payload mode has no exact counterpart), and
Deathmatch for AC-BT and XO-BT; they are underlined, and the style designed after a tree's game is set in bold.
Usage: python experiments/make_nearest_style_table.py --dir ../repro_outputs/v3_fixed_trees4 --out <file.tex>
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ABBR = {"Mission–Cooperation": "MC", "Persistent Objective": "PO", "Aggressive": "Agg", "Survival-Aware": "SA"}
ROWS = ["CSO-BT", "OW-BT", "AC-BT", "XO-BT", "UtilityAI"]
OWN = {"CSO-BT": "Mission–Cooperation", "OW-BT": "Persistent Objective", "AC-BT": "Aggressive", "XO-BT": "Survival-Aware"}
NATIVE = {"CSO-BT": {"Mission", "Control"}, "OW-BT": {"Mission", "Control"}, "AC-BT": {"Deathmatch"},
          "XO-BT": {"Deathmatch"}}
COLS = ["Mission", "Deathmatch", "Control", "pooled"]


def cell(dists: dict, tree: str, col: str) -> str:
    order = sorted(dists, key=dists.get)
    best, second = order[0], order[1]
    name = ABBR[best]
    if OWN.get(tree) == best:
        name = f"\\textbf{{{name}}}"
    text = f"{name} {dists[best]:.2f} (+{dists[second] - dists[best]:.2f})"
    return f"\\underline{{{text}}}" if col in NATIVE.get(tree, set()) else text


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="../repro_outputs/v3_fixed_trees4")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    d = Path(a.dir)
    maps = {"random": json.loads((d / "extra_summary.json").read_text()),
            "urban": json.loads((d / "urban" / "extra_summary.json").read_text())}
    lines = ["\\begin{tabular}{l" + "c" * (2 * len(COLS)) + "}", "\\toprule",
             " & " + " & ".join(f"\\multicolumn{{{len(COLS)}}}{{c}}{{{m} map}}" for m in maps) + " \\\\",
             "Baseline & " + " & ".join(" & ".join(COLS) for _ in maps) + " \\\\", "\\midrule"]
    for tree in ROWS:
        cells = []
        for S in maps.values():
            fp = S["baselines"]["fingerprint"]
            for col in COLS:
                cells.append(cell(fp[f"{col}|{tree}"], tree, col))
        lines.append(f"{tree} & " + " & ".join(cells) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    Path(a.out).write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
