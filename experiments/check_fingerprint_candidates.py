"""Development check of fingerprint measures that separate the AssaultCube and Xonotic trees (2026-09-26; not a result).

Runs the trees, the designed styles and the Part D fitted policies on the four game-inspired maps and the five held-out
maps (three scenarios each) with development seeds (base 5101, never used for a result), and reports, for every
candidate measure and every Part D fingerprint metric, the standardised separation between AC-BT and XO-BT
(|mean difference| / pooled within-condition SD, averaged over scenarios) per map family, and where the Part D fits of
the two trees lie between them (position 1 = at AC-BT, 0 = at XO-BT).
Usage: python experiments/check_fingerprint_candidates.py --fit ../repro_outputs/v6_fit --episodes 20 --jobs 12
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting as rf  # noqa: E402
import run_fitting_c as rfc  # noqa: E402

rf.SEED_BASES["dev_fp"] = 5101
TREES = ["CSO-BT", "OW-BT", "AC-BT", "XO-BT"]
MEASURES = ["objective_commitment_ratio", "engagement_redirection_rate_per_100", "resource_seeking_rate_per_100",
            "avg_ally_proximity", "kill_rate_per_100", "death_rate_per_100", "los_frac", "resource_goal_share_good",
            "retreat_share", "far_pursuit_share", "contact_distance", "resource_trip_distance"]


def run(task):
    spec, mp, sc_name, ep = task
    styles = rf.default_styles("exp")
    sc = next(s for s in rf.default_scenarios() if s.name == sc_name)
    policy = rfc.make_policy_c(spec)
    row = rf.run_episode(sc, policy, styles, rf.fit_seed("dev_fp", mp, sc_name, ep), rf.MAPS[mp])
    return {"agent": rfc.label_c(spec), "map": mp, "scenario": sc_name, **row}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--fit", default="../repro_outputs/v6_fit")
    p.add_argument("--episodes", type=int, default=20)
    p.add_argument("--jobs", type=int, default=12)
    a = p.parse_args()
    fitted = json.loads((Path(a.fit) / "fitted.json").read_text())
    specs = ([("tree", g) for g in TREES] + [("style", s) for s in rf.STYLE_NAMES]
             + [("fitc", f"fitD[{g}]", fitted[g]["combat_mode"], *fitted[g]["x"]) for g in TREES])
    maps = rf.TRAIN_MAPS + rf.HELDOUT_MAPS
    tasks = [(sp, mp, sc, ep) for sp in specs for mp in maps for sc in rf.SCENARIOS for ep in range(a.episodes)]
    with Pool(a.jobs) as pool:
        rows = pool.map(run, tasks, chunksize=6)
    vals = {}
    for r in rows:
        for m in MEASURES:
            v = r.get(m)
            if v in ("", None):
                continue
            v = float(v)
            if not math.isnan(v):
                vals.setdefault((r["agent"], r["map"], r["scenario"], m), []).append(v)
    print("measure | family | separation AC-BT vs XO-BT (|diff| / pooled SD, mean over maps x scenarios) | "
          "position of fitD[AC-BT] | position of fitD[XO-BT]  (1 = at AC-BT, 0 = at XO-BT)")
    for m in MEASURES:
        for fam, fmaps in (("game", rf.TRAIN_MAPS), ("held-out", rf.HELDOUT_MAPS)):
            seps, pa, px = [], [], []
            for mp in fmaps:
                for sc in rf.SCENARIOS:
                    ac, xo = vals.get(("AC-BT", mp, sc, m)), vals.get(("XO-BT", mp, sc, m))
                    if not ac or not xo or len(ac) < 2 or len(xo) < 2:
                        continue
                    sd = math.sqrt((np.var(ac, ddof=1) + np.var(xo, ddof=1)) / 2)
                    diff = np.mean(ac) - np.mean(xo)
                    if sd > 0:
                        seps.append(abs(diff) / sd)
                    if abs(diff) > 1e-9:
                        fa, fx = vals.get(("fitD[AC-BT]", mp, sc, m)), vals.get(("fitD[XO-BT]", mp, sc, m))
                        if fa:
                            pa.append((np.mean(fa) - np.mean(xo)) / diff)
                        if fx:
                            px.append((np.mean(fx) - np.mean(xo)) / diff)
            f = lambda x: f"{np.median(x):+.2f}" if x else "--"
            print(f"{m:36s} | {fam:8s} | {np.mean(seps) if seps else float('nan'):.2f} | {f(pa)} | {f(px)}")


if __name__ == "__main__":
    main()
