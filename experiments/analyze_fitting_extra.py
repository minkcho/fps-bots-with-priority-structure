"""Exploratory additions to the fitting analysis (2026-09-25; protocol part B, "also reported").

From the saved outputs of run_fitting.py (no new episodes):
  residuals   standardised residual z_d = (mean fit - mean tree) / s_d of every fingerprint dimension on the game maps
              (test seeds; s_d = stage-0 scale), summarised per metric and scenario, with the largest ones listed
  finalists   the eight candidates of stage 3 with their training and validation objective, and the range of the
              weights among the near-optimal ones (validation J at most 1.2 times the best); the training objective
              of the search (2 or 4 episodes per cell) is noisy, which the comparison with validation shows
Output: <dir>/fitting_extra.md
Usage: python experiments/analyze_fitting_extra.py --dir ../repro_outputs/v4_fit
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_fitting import FP, GAMES, SCENARIOS, TRAIN_MAPS, dims, simplex  # noqa: E402

SHORT = {"objective_commitment_ratio": "commitment", "engagement_redirection_rate_per_100": "engagement",
         "resource_seeking_rate_per_100": "resource", "avg_ally_proximity": "ally distance"}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="../repro_outputs/v4_fit")
    a = p.parse_args()
    d = Path(a.dir)
    df = pd.read_csv(d / "test_rows.csv")
    scales = json.loads((d / "stage0.json").read_text())["scales"]
    fitted = json.loads((d / "fitted.json").read_text())
    g = df[df["map"].isin(TRAIN_MAPS)].groupby(["agent", "map", "scenario"])[FP].mean()
    md = ["# Fitting: exploratory additions (game maps, test seeds)", ""]
    for game in GAMES:
        fit = f"fit[{game}]"
        z = {}
        for mp, sc, m in dims(TRAIN_MAPS):
            key = f"{mp}|{sc}|{m}"
            if key not in scales:
                continue
            z[(mp, sc, m)] = (g.loc[(fit, mp, sc), m] - g.loc[(game, mp, sc), m]) / scales[key]
        md += [f"## {game}", "", "Mean |z| by metric and scenario (over the four game maps):", "",
               "| metric | " + " | ".join(SCENARIOS) + " |", "|---|" + "---|" * len(SCENARIOS)]
        for m in FP:
            cells = []
            for sc in SCENARIOS:
                v = [abs(z[k]) for k in z if k[1] == sc and k[2] == m]
                cells.append(f"{np.mean(v):.2f}" if v else "--")
            md.append(f"| {SHORT[m]} | " + " | ".join(cells) + " |")
        tot = sum(v ** 2 for v in z.values())
        md += ["", "Share of the squared residuals by metric: " + ", ".join(
            f"{SHORT[m]} {100 * sum(v ** 2 for k, v in z.items() if k[2] == m) / tot:.0f}%" for m in FP)
            + "; by map: " + ", ".join(f"{mp} {100 * sum(v ** 2 for k, v in z.items() if k[0] == mp) / tot:.0f}%"
                                       for mp in TRAIN_MAPS)]
        top = sorted(z.items(), key=lambda kv: -abs(kv[1]))[:6]
        md += ["", "Largest residuals: " + "; ".join(f"{mp} {sc} {SHORT[m]} {v:+.1f}" for (mp, sc, m), v in top),
               f"Mean |z| over all {len(z)} dimensions: {np.mean([abs(v) for v in z.values()]):.2f}", ""]
        fin = fitted[game]["finalists"]
        best = min(f["validation_J"] for f in fin)
        near = [f for f in fin if f["validation_J"] <= 1.2 * best]
        md += ["Stage-3 finalists (training J -> validation J): "
               + ", ".join(f"{f['train_J']:.2f} -> {f['validation_J']:.2f}" for f in sorted(fin, key=lambda f: f["validation_J"])), ""]
        ws = np.array([simplex(*f["x"][:3]) + [f["x"][3]] for f in near])
        names = ["w_objective", "w_engage", "w_resource", "w_team", "w_commitment"]
        md += [f"Near-optimal finalists (validation J <= 1.2 x {best:.2f}): {len(near)}; weight ranges: "
               + ", ".join(f"{n} {ws[:, i].min():.2f}-{ws[:, i].max():.2f}" for i, n in enumerate(names)), ""]
    (d / "fitting_extra.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
