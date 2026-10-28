"""Exploratory (2026-09-27): D2 of the Part F AssaultCube and Xonotic fits to every tree variant of
repro_outputs/dev_tree_revision/rows.csv on the game-inspired maps (Part F stage-0 scales), read from the existing
rows (no new episodes). Same definitions as explore_tree_revision.py.
Usage: python experiments/extra_tree_revision_d2.py > ../repro_outputs/dev_tree_revision_extra/fit_d2.md"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting_f  # noqa: E402,F401  (patches the Part E fingerprint into analyze_fitting)
import analyze_fitting as af  # noqa: E402

ROOT = Path(__file__).resolve().parents[2] / "repro_outputs"
df = pd.read_csv(ROOT / "dev_tree_revision" / "rows.csv")
df.loc[df.agent == "AC 2026-09-25", "agent"] = "AC-BT"
df.loc[df.agent == "XO per-step", "agent"] = "XO-BT"
stage0 = json.loads((ROOT / "v8_fit" / "stage0.json").read_text())
cells = af.Cells(df, af.FP)
sc = af.scales_for(df, stage0, af.TRAIN_MAPS)
trees = ["CSO-BT", "OW-BT", "AC-BT", "AC 25u hunt h3", "XO-BT", "XO timer", "XO timer+early"]
print("# D2 of the Part F fits to the tree variants (development seeds 5601, game-inspired maps, Part F stage-0 scales)")
print("AC-BT = AC 2026-09-25 (Parts D-F), XO-BT = XO per-step (Parts D-F); new defaults: AC 25u hunt h3, XO timer+early\n")
print("| fit | " + " | ".join(trees) + " |")
print("|---|" + "---|" * len(trees))
for fit in ("fit[AC-BT]", "fit[XO-BT]"):
    print(f"| {fit} | " + " | ".join(f"{af.d2(cells, fit, t, sc):.2f}" for t in trees) + " |")
