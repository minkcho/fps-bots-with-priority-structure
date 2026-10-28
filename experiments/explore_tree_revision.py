"""Exploratory (2026-09-27; not part of any frozen protocol): what the tree revisions decided after the tree review
change (REVIEW_trees_2026-09-27.md; user decisions: Xonotic early re-rating, one AssaultCube length scale, source-like
AssaultCube hunting).

Variants (BaselineStyle options; development seeds 5601, never used for a result; 20 episodes per agent x map x
scenario on the four game-inspired and the five held-out maps):
  Xonotic      per-step (Parts D-F), timer 15/12 without early re-rating, timer with early re-rating (new default)
  AssaultCube  2026-09-25 tree (mixed scales, current-position hunting; Parts D-F), 25 units per cell with the old
               hunting, 25 units per cell with source-like hunting (new default; history 3 steps), the same with a
               history of 1 and of 5 steps, and 12 units per cell with source-like hunting (another length scale)
next to the CSO and Overwatch trees and the designed styles (for the held-out scales) and the Part F fits of the
AssaultCube and Xonotic trees. Reported: behaviour means; D2 of each variant to its earlier tree and between the new
AssaultCube and Xonotic trees (game maps, Part F stage-0 scales); for the Part F fits, D2 to the variants of their
tree and the held-out maps on which that variant is the nearest tree. Note: far_pursuit_share uses a 10-cell radius,
equal to the AssaultCube hunting range at 25 units per cell.
Usage: python experiments/explore_tree_revision.py --out ../repro_outputs/dev_tree_revision --jobs 12
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import replace
from multiprocessing import Pool
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting_f as rff  # noqa: E402  (Part E fingerprint and the eight-parameter mapping of Part F)

rf, rfc = rff.rf, rff.rfc
import analyze_fitting as af  # noqa: E402  (after the patch: af.FP is the Part E fingerprint)
from fps_priority_ai.baselines import BaselineStyle, default_baselines  # noqa: E402

rf.SEED_BASES["dev_rev"] = 5601
EPISODES = 20
FIT = Path(__file__).resolve().parents[2] / "repro_outputs" / "v8_fit"
XO_NEW = default_baselines()["XO-BT"]
AC_NEW = default_baselines()["AC-BT"]
VARIANTS = {  # label -> style
    "XO per-step": BaselineStyle("XO per-step", "XO-BT"),
    "XO timer": replace(XO_NEW, name="XO timer", xo_early_rerating=False),
    "XO timer+early": replace(XO_NEW, name="XO timer+early"),
    "AC 2026-09-25": BaselineStyle("AC 2026-09-25", "AC-BT"),
    "AC 25u old hunt": replace(AC_NEW, name="AC 25u old hunt", ac_hunt_history=0),
    "AC 25u hunt h3": replace(AC_NEW, name="AC 25u hunt h3"),
    "AC 25u hunt h1": replace(AC_NEW, name="AC 25u hunt h1", ac_hunt_history=1),
    "AC 25u hunt h5": replace(AC_NEW, name="AC 25u hunt h5", ac_hunt_history=5),
    "AC 12u hunt h3": replace(AC_NEW, name="AC 12u hunt h3", ac_units_per_cell=12.0),
}
MEASURES = ["retreat_share", "far_pursuit_share", "resource_goal_share_good", "kill_rate_per_100", "death_rate_per_100",
            "goal_switch_rate_per_100", "engagement_redirection_rate_per_100", "avg_ally_proximity",
            "contact_distance", "los_frac"]
SHORT = ["retreat", "far pursuit", "item control", "kills/100", "deaths/100", "switches/100", "redirection/100",
         "ally dist", "contact dist", "contact share"]


def policy(spec: tuple):
    if spec[0] == "var":
        return VARIANTS[spec[1]]
    if spec[0] == "fitF":                    # ("fitF", game, mode, *x): a Part F fit
        return rfc.fitted_style_c(f"fit[{spec[1]}]", spec[2], spec[3:])
    return rfc.make_policy_c(spec)


def run(task: tuple) -> list[dict]:
    spec, map_name, scenario = task
    styles = rf.default_styles("exp")
    sc = next(s for s in rf.default_scenarios() if s.name == scenario)
    pol = policy(spec)
    return [{"agent": pol.name, "map": map_name, "scenario": scenario, "seed_kind": "dev_rev", "episode": ep,
             **rf.run_episode(sc, pol, styles, rf.fit_seed("dev_rev", map_name, scenario, ep), rf.MAPS[map_name])}
            for ep in range(EPISODES)]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="../repro_outputs/dev_tree_revision")
    p.add_argument("--jobs", type=int, default=12)
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    fitted = json.loads((FIT / "fitted.json").read_text())
    specs = ([("var", k) for k in VARIANTS] + [("tree", "CSO-BT"), ("tree", "OW-BT")]
             + [("style", s) for s in rf.STYLE_NAMES]
             + [("fitF", g, fitted[g]["combat_mode"], *fitted[g]["x"]) for g in ("AC-BT", "XO-BT")])
    tasks = [(sp, m, sc) for sp in specs for m in rf.TRAIN_MAPS + rf.HELDOUT_MAPS for sc in rf.SCENARIOS]
    with Pool(a.jobs) as pool:
        rows = [r for b in pool.map(run, tasks, chunksize=1) for r in b]
    rf.write_rows(out / "rows.csv", rows)
    df = pd.read_csv(out / "rows.csv")
    # the frozen analysis names the trees CSO-BT, OW-BT, AC-BT, XO-BT; the earlier AC and XO trees play those roles
    # for the held-out scales (reference agents), the variants are compared by name
    df.loc[df.agent == "AC 2026-09-25", "agent"] = "AC-BT"
    df.loc[df.agent == "XO per-step", "agent"] = "XO-BT"
    stage0 = json.loads((FIT / "stage0.json").read_text())
    cells = af.Cells(df, af.FP)
    sc_game = af.scales_for(df, stage0, af.TRAIN_MAPS)
    names = {"XO per-step": "XO-BT", "AC 2026-09-25": "AC-BT"}
    lab = lambda k: names.get(k, k)  # noqa: E731
    md = ["# Exploratory: the revised AssaultCube and Xonotic trees (development seeds 5601, 20 episodes per cell; "
          "not a result)", "", "Earlier trees: 'XO per-step' (= XO-BT of Parts D-F) and 'AC 2026-09-25' (= AC-BT of "
          "Parts D-F). New defaults: 'XO timer+early' and 'AC 25u hunt h3'.", ""]
    res = {"means": {}, "distances": {}}
    agents = [lab(k) for k in VARIANTS] + ["fit[AC-BT]", "fit[XO-BT]"]
    for title, maps in (("game maps", af.TRAIN_MAPS), ("held-out maps", af.HELDOUT_MAPS)):
        g = df[df["map"].isin(maps)].groupby("agent")[MEASURES].mean()
        md += [f"## Behaviour, {title} (means over maps, scenarios and episodes)", "",
               "| agent | " + " | ".join(SHORT) + " |", "|---|" + "---|" * len(SHORT)]
        for ag in agents:
            md.append(f"| {ag} | " + " | ".join(f"{g.loc[ag, c]:.2f}" for c in MEASURES) + " |")
        md.append("")
        res["means"][title] = {ag: g.loc[ag].to_dict() for ag in agents}
    md += ["## Distances (game maps, Part F stage-0 scales)", "",
           "| variant | D2 to its earlier tree | D2 to the other game's new tree | Part F fit of its game: D2 to the variant "
           "| held-out maps on which the variant is the fit's nearest tree |", "|---|---|---|---|---|"]
    for k in VARIANTS:
        game = "XO-BT" if k.startswith("XO") else "AC-BT"
        other = "AC 25u hunt h3" if game == "XO-BT" else "XO timer+early"
        fit = f"fit[{game}]"
        ho = 0
        for m in af.HELDOUT_MAPS:
            sm = af.scales_for(df, stage0, [m])
            rivals = ["CSO-BT", "OW-BT", other, lab(k)]
            dm = {t: af.d2(cells, fit, t, sm) for t in rivals}
            ho += min(dm, key=dm.get) == lab(k)
        r = {"to_earlier": af.d2(cells, lab(k), game, sc_game), "to_other_new": af.d2(cells, lab(k), other, sc_game),
             "fit_to_variant": af.d2(cells, fit, lab(k), sc_game), "heldout_nearest": ho}
        res["distances"][k] = r
        md.append(f"| {k} | {r['to_earlier']:.2f} | {r['to_other_new']:.2f} | {r['fit_to_variant']:.2f} | {ho}/5 |")
    (out / "summary.json").write_text(json.dumps(res, indent=1, default=float))
    (out / "summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
