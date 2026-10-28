"""Development checks for fitting Part F (2026-09-26; not results).

--defaults      the optional commitment relief (urgent_switch_relief) at its default 0 must leave the policy unchanged:
                a fixed set of episodes -- the four designed styles (main model) and the four Part E fits (their
                modes and parameters) on random, urban and blocks, three scenarios, two episodes each -- written as
                metric rows; run it before and after the change and compare the two files (all columns)
--trees         (2026-09-27) the same for the five baselines (four trees and the utility AI): run before and after a
                change of baselines.py and compare the two files. --tree-variant: default = default_baselines();
                legacy = BaselineStyle(k, k) with the dataclass defaults (the trees of 2026-09-25: per-step Xonotic tree,
                mixed-scale AssaultCube tree); timer = default_baselines() with the Xonotic early re-rating off and the
                AssaultCube tree of 2026-09-25 (the state of 2026-09-27 11:13)
--relief-check  the Part E fits of the Overwatch and Xonotic trees with relief 0 and 1, and the two trees, on the
                game-inspired maps (10 episodes per cell): mean behaviour measures per agent and scenario, to confirm
                that the relief lets a weakened agent under fire switch to an item
Seeds: development base 5201 (never used for a result).
Usage: python experiments/check_policy_defaults.py --defaults --out ../repro_outputs/dev_relief/defaults_before.csv
       python experiments/check_policy_defaults.py --relief-check --out ../repro_outputs/dev_relief/check.txt
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import replace
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting as rf  # noqa: E402
import run_fitting_c as rfc  # noqa: E402

rf.SEED_BASES["dev"] = 5201
PART_E = Path(__file__).resolve().parents[2] / "repro_outputs" / "v7_fit" / "fitted.json"
MEASURES = ["retreat_share", "far_pursuit_share", "resource_goal_share_good", "kill_rate_per_100",
            "death_rate_per_100", "engagement_redirection_rate_per_100", "objective_commitment_ratio"]


def policy(spec: tuple):
    if spec[0] == "treevar":                     # ("treevar", variant, kind)
        from fps_priority_ai.baselines import BaselineStyle, default_baselines
        if spec[1] == "legacy":
            return BaselineStyle(name=spec[2], kind=spec[2])
        b = default_baselines()[spec[2]]
        return replace(b, xo_early_rerating=False, ac_units_per_cell=0.0, ac_hunt_history=0)
    if spec[0] == "fitE":                        # ("fitE", game, relief or None)
        f = json.loads(PART_E.read_text())[spec[1]]
        s = rfc.fitted_style_c(f"fitE[{spec[1]}]", f["combat_mode"], f["x"])
        return s if spec[2] is None else replace(s, name=f"{s.name} relief {spec[2]:g}", urgent_switch_relief=spec[2])
    return rf.make_policy(spec)


def run(task: tuple) -> list[dict]:
    spec, map_name, scenario, n = task
    styles = rf.default_styles("exp")
    sc = next(s for s in rf.default_scenarios() if s.name == scenario)
    pol = policy(spec)
    return [{"agent": pol.name, "map": map_name, "scenario": scenario, "episode": ep,
             **rf.run_episode(sc, pol, styles, rf.fit_seed("dev", map_name, scenario, ep), rf.MAPS[map_name])}
            for ep in range(n)]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--defaults", action="store_true")
    p.add_argument("--relief-check", action="store_true")
    p.add_argument("--trees", action="store_true")
    p.add_argument("--tree-variant", default="default", choices=["default", "legacy", "timer"])
    p.add_argument("--out", required=True)
    p.add_argument("--jobs", type=int, default=4)
    a = p.parse_args()
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if a.defaults or a.trees:
        specs = ([("tree", k) for k in ("CSO-BT", "OW-BT", "AC-BT", "XO-BT", "UtilityAI")] if a.trees else
                 [("style", s) for s in rf.STYLE_NAMES] + [("fitE", g, None) for g in rf.GAMES])
        if a.trees and a.tree_variant != "default":
            specs = [("treevar", a.tree_variant, k) for k in ("CSO-BT", "OW-BT", "AC-BT", "XO-BT", "UtilityAI")]
        tasks = [(sp, m, sc, 2) for sp in specs for m in ("random", "urban", "blocks") for sc in rf.SCENARIOS]
        with Pool(a.jobs) as pool:
            rows = [r for block in pool.map(run, tasks) for r in block]
        rows.sort(key=lambda r: (r["agent"], r["map"], r["scenario"], r["episode"]))
        with out.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(f"{len(rows)} rows -> {out}")
    if a.relief_check:
        import pandas as pd
        specs = [("tree", "OW-BT"), ("fitE", "OW-BT", 0.0), ("fitE", "OW-BT", 1.0),
                 ("tree", "XO-BT"), ("fitE", "XO-BT", 0.0), ("fitE", "XO-BT", 1.0)]
        tasks = [(sp, m, sc, 10) for sp in specs for m in rf.TRAIN_MAPS for sc in rf.SCENARIOS]
        with Pool(a.jobs) as pool:
            rows = [r for block in pool.map(run, tasks) for r in block]
        df = pd.DataFrame(rows)
        for c in MEASURES:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        g = df.groupby(["agent", "scenario"], sort=False)[MEASURES].mean()
        lines = ["# Development check of the commitment relief (seeds 5201, game-inspired maps, 10 episodes per cell;"
                 " not a result)", "", "| agent | scenario | " + " | ".join(MEASURES) + " |",
                 "|---|---|" + "---|" * len(MEASURES)]
        for (ag, sc), r in g.iterrows():
            lines.append(f"| {ag} | {sc} | " + " | ".join(f"{r[c]:.3f}" for c in MEASURES) + " |")
        out.write_text("\n".join(lines) + "\n")
        print("\n".join(lines))


if __name__ == "__main__":
    main()
