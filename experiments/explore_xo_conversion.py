"""Exploratory (2026-09-27; not part of any frozen protocol): how the Xonotic tree depends on the conversions made when
it was reconstructed from the havocbot source (user request after the Part F report).

The source rates goals with rangebias 2000 units and re-rates them only when the strategy timer expires
(bot_ai_strategyinterval 7 s, 5.5 s for a moving target; xonotic-server.cfg, refs/game_sources/xonotic/cfg_*); the
default bot skill is 8, which makes the skill term 0.05 * max(0, 8 - skill) zero. The revised tree (baselines.py) uses
12 cells for 2000 units and re-rates every step. One scale -- units per cell -- sets both conversions: with the
movement speed 360 units/s (physicsX.cfg) and one cell per step, rangebias 6 / 12 / 24 cells correspond to strategy
intervals of 8/6, 15/12 and 30/24 steps (static / moving goal). Variants of XO-BT (BaselineStyle options):
  rangebias 6, 12, 24 cells, each re-rated every step and with the source timer at the same scale;
  rangebias 12 with intervals 5 and 10 steps; skill 4 (bonus 0.2) with and without the timer.
Run next to the current trees, the designed styles (for the held-out scales) and the Part F Xonotic fit, on
development seeds (base 5401, never used for a result; 20 episodes per agent x map x scenario, game and held-out maps).
Reported per variant: behaviour means, D2 to the current XO-BT and to AC-BT (game maps, Part F stage-0 scales), and for
the Part F Xonotic fit the D2 to the variant against AC-BT and the held-out maps on which the variant is its nearest tree.
Usage: python experiments/explore_xo_conversion.py --out ../repro_outputs/dev_xo_conversion --jobs 12
"""
from __future__ import annotations

import argparse
import json
import sys
from multiprocessing import Pool
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting_f as rff  # noqa: E402  (Part E fingerprint and the eight-parameter mapping of Part F)

rf, rfc = rff.rf, rff.rfc
import analyze_fitting as af  # noqa: E402  (after the patch: af.FP is the Part E fingerprint)
from fps_priority_ai.baselines import BaselineStyle  # noqa: E402

rf.SEED_BASES["dev_xo"] = 5401
EPISODES = 20
VARIANTS = [  # label, rangebias (cells), interval static, interval moving, skill bonus
    ("XO rb6 step", 6.0, 1, 1, 0.0),
    ("XO rb12 step", 12.0, 1, 1, 0.0),          # = the current tree (identity check against XO-BT)
    ("XO rb24 step", 24.0, 1, 1, 0.0),
    ("XO rb6 timer 8/6", 6.0, 8, 6, 0.0),
    ("XO rb12 timer 15/12", 12.0, 15, 12, 0.0),
    ("XO rb24 timer 30/24", 24.0, 30, 24, 0.0),
    ("XO rb12 interval 5", 12.0, 5, 5, 0.0),
    ("XO rb12 interval 10", 12.0, 10, 10, 0.0),
    ("XO rb12 step skill4", 12.0, 1, 1, 0.2),
    ("XO rb12 timer 15/12 skill4", 12.0, 15, 12, 0.2),
]
MEASURES = ["retreat_share", "far_pursuit_share", "resource_goal_share_good", "kill_rate_per_100", "death_rate_per_100",
            "goal_switch_rate_per_100", "engagement_redirection_rate_per_100", "avg_ally_proximity",
            "contact_distance"]
SHORT = ["retreat", "far pursuit", "item control", "kills/100", "deaths/100", "switches/100", "redirection/100",
         "ally dist", "contact dist"]
FIT = Path(__file__).resolve().parents[2] / "repro_outputs" / "v8_fit"


def policy(spec: tuple):
    if spec[0] == "xo":                      # ("xo", label, rangebias, interval, interval moving, skill bonus)
        return BaselineStyle(name=spec[1], kind="XO-BT", xo_range_bias=spec[2], xo_interval=spec[3],
                             xo_interval_moving=spec[4], xo_skill_bonus=spec[5])
    if spec[0] == "fitF":                    # ("fitF", mode, *x): the Part F Xonotic fit
        return rfc.fitted_style_c("fit[XO-BT]", spec[1], spec[2:])
    if spec[0] == "tree" and spec[1] in ("XO-BT", "AC-BT"):
        # (2026-09-27, after the tree review) the trees as they were when this check ran: per-step Xonotic tree and the
        # AssaultCube tree of 2026-09-25 (dataclass defaults); default_baselines() now differs
        return BaselineStyle(name=spec[1], kind=spec[1])
    return rfc.make_policy_c(spec)


def run(task: tuple) -> list[dict]:
    spec, map_name, scenario = task
    styles = rf.default_styles("exp")
    sc = next(s for s in rf.default_scenarios() if s.name == scenario)
    pol = policy(spec)
    return [{"agent": pol.name, "map": map_name, "scenario": scenario, "seed_kind": "dev_xo", "episode": ep,
             **rf.run_episode(sc, pol, styles, rf.fit_seed("dev_xo", map_name, scenario, ep), rf.MAPS[map_name])}
            for ep in range(EPISODES)]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="../repro_outputs/dev_xo_conversion")
    p.add_argument("--jobs", type=int, default=12)
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    f = json.loads((FIT / "fitted.json").read_text())["XO-BT"]
    specs = ([("xo", *v) for v in VARIANTS] + [("tree", g) for g in rfc.GAMES]
             + [("style", s) for s in rf.STYLE_NAMES] + [("fitF", f["combat_mode"], *f["x"])])
    tasks = [(sp, m, sc) for sp in specs for m in rf.TRAIN_MAPS + rf.HELDOUT_MAPS for sc in rf.SCENARIOS]
    with Pool(a.jobs) as pool:
        rows = [r for b in pool.map(run, tasks, chunksize=1) for r in b]
    rf.write_rows(out / "rows.csv", rows)
    df = pd.read_csv(out / "rows.csv")
    stage0 = json.loads((FIT / "stage0.json").read_text())
    cells = af.Cells(df, af.FP)
    sc_game = af.scales_for(df, stage0, af.TRAIN_MAPS)
    cols = [c for c in df.columns if c not in ("agent", "map", "scenario", "seed_kind", "episode")]
    a_ = df[df.agent == "XO rb12 step"].sort_values(["map", "scenario", "episode"])[cols].astype(str).to_numpy()
    b_ = df[df.agent == "XO-BT"].sort_values(["map", "scenario", "episode"])[cols].astype(str).to_numpy()
    same = int((a_ == b_).all(axis=1).sum())
    md = ["# Exploratory: the Xonotic tree under the conversions from the havocbot source (development seeds 5401, "
          "20 episodes per cell; not a result)", "",
          f"Identity check: 'XO rb12 step' equals XO-BT in {same}/{len(a_)} episodes (all {len(cols)} metric columns).", ""]
    res = {"identity": [same, len(a_)], "variants": {}}
    agents = [v[0] for v in VARIANTS] + ["AC-BT", "OW-BT", "fit[XO-BT]"]
    for label, maps in (("game maps", af.TRAIN_MAPS), ("held-out maps", af.HELDOUT_MAPS)):
        sub = df[df["map"].isin(maps)]
        g = sub.groupby("agent")[MEASURES].mean()
        md += [f"## Behaviour, {label} (means over maps, scenarios and episodes)", "",
               "| agent | " + " | ".join(SHORT) + " |", "|---|" + "---|" * len(SHORT)]
        for ag in agents:
            md.append(f"| {ag} | " + " | ".join(f"{g.loc[ag, c]:.2f}" for c in MEASURES) + " |")
        md.append("")
        res[f"means {label}"] = {ag: g.loc[ag].to_dict() for ag in agents}
    fit = "fit[XO-BT]"
    d_fit_ac = af.d2(cells, fit, "AC-BT", sc_game)
    md += ["## Distances (game maps: Part F stage-0 scales; held-out maps: nearest tree to the Part F Xonotic fit when the "
           "variant replaces XO-BT)", "",
           "| variant | D2 to current XO-BT | D2 to AC-BT | fit: D2 to variant | fit: D2 to AC-BT | held-out maps with the "
           "variant nearest to the fit |", "|---|---|---|---|---|---|"]
    for v in VARIANTS:
        lab = v[0]
        ho = 0
        for m in af.HELDOUT_MAPS:
            sm = af.scales_for(df, stage0, [m])
            dm = {t: af.d2(cells, fit, t, sm) for t in ("CSO-BT", "OW-BT", "AC-BT", lab)}
            ho += min(dm, key=dm.get) == lab
        r = {"D2_to_XO": af.d2(cells, lab, "XO-BT", sc_game), "D2_to_AC": af.d2(cells, lab, "AC-BT", sc_game),
             "fit_D2_to_variant": af.d2(cells, fit, lab, sc_game), "fit_D2_to_AC": d_fit_ac, "heldout_nearest": ho}
        res["variants"][lab] = r
        md.append(f"| {lab} | {r['D2_to_XO']:.2f} | {r['D2_to_AC']:.2f} | {r['fit_D2_to_variant']:.2f} | "
                  f"{r['fit_D2_to_AC']:.2f} | {ho}/5 |")
    (out / "summary.json").write_text(json.dumps(res, indent=1, default=float))
    (out / "summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
