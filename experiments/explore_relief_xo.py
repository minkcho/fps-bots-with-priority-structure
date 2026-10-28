"""Exploratory (2026-09-27; not part of any frozen protocol): what the relief rho does to the Part F Xonotic fit.

The Part F fit of the Xonotic tree (hold mode, rho 0.653) is run with rho in {0, 0.25, 0.5, fitted, 0.75, 1} and all
other parameters as fitted, next to the four trees and the designed styles (with and without route terms), on
development seeds (base 5301, never used for a result; 20 episodes per agent x map x scenario on the four
game-inspired and the five held-out maps), so that the test seeds of Part F stay untouched. Reported per rho: the
objective J against the Part F stage-0 target of the Xonotic tree (game maps), D2 to the four trees with the nearest
one, the gap closure G (game maps), the nearest tree and G on each held-out map, and the retreat and far-pursuit shares.
Distances, scales and G as in the frozen analysis (analyze_fitting.py) on the Part E fingerprint.
Usage: python experiments/explore_relief_xo.py --fit ../repro_outputs/v8_fit --out ../repro_outputs/dev_relief/rho_xo --jobs 12
"""
from __future__ import annotations

import argparse
import json
import sys
from multiprocessing import Pool
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting_f as rff  # noqa: E402  (patches rf.FP to the Part E fingerprint and rfc.params to eight parameters)

rf, rfc = rff.rf, rff.rfc
import analyze_fitting as af  # noqa: E402  (after the patch: af.FP is the Part E fingerprint)

rf.SEED_BASES["dev_rho"] = 5301
EPISODES = 20


def label(rho: float) -> str:
    return f"fit[XO-BT] rho={rho:.3f}"


def policy(spec: tuple):
    if spec[0] == "xo":                      # ("xo", rho, mode, *x): the Part F Xonotic fit with rho replaced
        x = list(spec[3:])
        x[7] = spec[1]
        return rfc.fitted_style_c(label(spec[1]), spec[2], x)
    return rfc.make_policy_c(spec)


def run(task: tuple) -> list[dict]:
    spec, map_name, scenario = task
    styles = rf.default_styles("exp")
    sc = next(s for s in rf.default_scenarios() if s.name == scenario)
    pol = policy(spec)
    name = label(spec[1]) if spec[0] == "xo" else rfc.label_c(spec)
    return [{"agent": name, "map": map_name, "scenario": scenario, "seed_kind": "dev_rho", "episode": ep,
             **rf.run_episode(sc, pol, styles, rf.fit_seed("dev_rho", map_name, scenario, ep), rf.MAPS[map_name])}
            for ep in range(EPISODES)]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--fit", default="../repro_outputs/v8_fit")
    p.add_argument("--out", default="../repro_outputs/dev_relief/rho_xo")
    p.add_argument("--jobs", type=int, default=12)
    a = p.parse_args()
    fit, out = Path(a.fit), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    f = json.loads((fit / "fitted.json").read_text())["XO-BT"]
    rhos = sorted([0.0, 0.25, 0.5, 0.75, 1.0, float(f["x"][7])])   # the fitted value exactly
    specs = ([("xo", r, f["combat_mode"], *f["x"]) for r in rhos] + [("tree", g) for g in rfc.GAMES]
             + [("style", s) for s in rf.STYLE_NAMES] + [("style_off", s) for s in rf.STYLE_NAMES])
    tasks = [(sp, m, sc) for sp in specs for m in rf.TRAIN_MAPS + rf.HELDOUT_MAPS for sc in rf.SCENARIOS]
    with Pool(a.jobs) as pool:
        blocks = pool.map(run, tasks, chunksize=1)
    rows = [r for b in blocks for r in b]
    rf.write_rows(out / "rows.csv", rows)
    df = pd.read_csv(out / "rows.csv")
    stage0 = json.loads((fit / "stage0.json").read_text())
    cells = af.Cells(df, af.FP)
    sc_game = af.scales_for(df, stage0, af.TRAIN_MAPS)
    styles = [s for s in df.agent.unique() if s in af.HAND.values() or s.endswith("[route off]")]
    game = df[df["map"].isin(af.TRAIN_MAPS)]
    held = df[df["map"].isin(af.HELDOUT_MAPS)]
    res, md = {}, ["# Exploratory: the relief rho in the Part F Xonotic fit (development seeds 5301, 20 episodes per "
                   "cell; other parameters as fitted; not a result)", "",
                   "| rho | J (game) | D2 XO-BT | D2 AC-BT | nearest (game) | G (game) | held-out: own tree nearest | "
                   "held-out G | retreat game / held-out | far pursuit game / held-out |",
                   "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rhos:
        ag = label(r)
        own = [row for t, b in zip(tasks, blocks) if t[0][0] == "xo" and t[0][1] == r and t[1] in rf.TRAIN_MAPS
               for row in b]
        j = rf.objective_value(rf.summarise(own), stage0["targets"]["XO-BT"], stage0["scales"])
        d = {t: af.d2(cells, ag, t, sc_game) for t in af.TREES}
        g = af.gap(cells, ag, "XO-BT", styles, sc_game)
        ho = {}
        for m in af.HELDOUT_MAPS:
            sm = af.scales_for(df, stage0, [m])
            dm = {t: af.d2(cells, ag, t, sm) for t in af.TREES}
            ho[m] = {"nearest": min(dm, key=dm.get), "G": af.gap(cells, ag, "XO-BT", styles, sm)}
        ret = (game[game.agent == ag].retreat_share.mean(), held[held.agent == ag].retreat_share.mean())
        far = (game[game.agent == ag].far_pursuit_share.mean(), held[held.agent == ag].far_pursuit_share.mean())
        res[str(r)] = {"J": j, "D2": d, "G": g, "heldout": ho, "retreat": ret, "far_pursuit": far}
        md.append(f"| {r:.3f} | {j:.2f} | {d['XO-BT']:.2f} | {d['AC-BT']:.2f} | {min(d, key=d.get)} | {g:.2f} | "
                  f"{sum(v['nearest'] == 'XO-BT' for v in ho.values())}/5 | "
                  + ", ".join(f"{v['G']:.2f}" for v in ho.values())
                  + f" | {ret[0]:.2f} / {ret[1]:.2f} | {far[0]:.2f} / {far[1]:.2f} |")
    for t in ("XO-BT", "AC-BT"):
        md.append(f"| {t} tree | | | | | | | | {game[game.agent == t].retreat_share.mean():.2f} / "
                  f"{held[held.agent == t].retreat_share.mean():.2f} | {game[game.agent == t].far_pursuit_share.mean():.2f} / "
                  f"{held[held.agent == t].far_pursuit_share.mean():.2f} |")
    (out / "summary.json").write_text(json.dumps(res, indent=1, default=float))
    (out / "summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
