"""Figure of the primary H3 test under the main model (2026-09-24).

Reads the cost-term ablation of both maps (run_cost_term_ablation.py) and draws
  (a), (b) Deathmatch: expected hits per walked step for each style with the configured exposure weight
           ("full") and without the exposure term ("no exposure"), random and urban map;
  (c)      the relative change of the mean walked exposure, full vs no exposure, for every
           scenario x style condition on both maps (the conditions of the sign test).

Usage:
  python experiments/make_h3_primary_figure.py --random-dir ../repro_outputs/v3 \
      --urban-dir ../repro_outputs/v3/urban --out ../new_paper/figures/fig_h3_primary.pdf
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_ec_figures import mean_ci  # noqa: E402  (shared CI helper)
from make_extra_figures import grouped_bars_with_ci, _normalise_style_col, STYLES_ORDER, SCENARIOS_ORDER  # noqa: E402

SHORT = {"Mission-Cooperation": "MC", "Persistent Objective": "PO", "Aggressive": "Agg", "Survival-Aware": "SA"}
MARKERS = {"Mission-Cooperation": "o", "Persistent Objective": "s", "Aggressive": "^", "Survival-Aware": "D"}
COL = "walked_hits_per_step"


def load(d: Path) -> pd.DataFrame:
    return _normalise_style_col(pd.read_csv(d / "cost_term_ablation.csv"))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--random-dir", required=True)
    p.add_argument("--urban-dir", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--no-points", action="store_true",
                   help="bars and confidence intervals only, without the per-episode points (journal version)")
    p.add_argument("--panel-labels", action="store_true", help="prefix the panel titles with (a), (b), (c) (journal version)")
    args = p.parse_args()
    maps = [("random", load(Path(args.random_dir))), ("urban", load(Path(args.urban_dir)))]
    lab = ["(a) ", "(b) ", "(c) "] if args.panel_labels else ["", "", ""]

    fig, axes = plt.subplots(1, 3, figsize=(15.0, 4.0), gridspec_kw={"width_ratios": [1, 1, 1.15]})
    for (ax, (name, df)), plab in zip(zip(axes[:2], maps), lab[:2]):
        sub = df[df["scenario"] == "Deathmatch"]
        series = []
        for variant, label in (("full", "configured $\\lambda_E$"), ("no_exposure", "$\\lambda_E=0$")):
            means, cis, raws = [], [], []
            for st in STYLES_ORDER:
                vals = sub[(sub["style"] == st) & (sub["variant"] == variant)][COL].astype(float).values
                m, c = mean_ci(vals)
                means.append(m); cis.append(c); raws.append(vals)
            series.append((label, means, cis, raws))
        grouped_bars_with_ci(ax, [SHORT[s] for s in STYLES_ORDER], series,
                             title=f"{plab}Deathmatch, {name} map", ylabel="Walked expected hits per step",
                             show_points=not args.no_points)

    ax = axes[2]
    for mi, (name, df) in enumerate(maps):
        for si, sc in enumerate(SCENARIOS_ORDER):
            for ti, st in enumerate(STYLES_ORDER):
                cond = df[(df["scenario"] == sc) & (df["style"] == st)]
                full = cond[cond["variant"] == "full"][COL].astype(float).mean()
                base = cond[cond["variant"] == "no_exposure"][COL].astype(float).mean()
                rel = 100.0 * (full - base) / base
                x = si + (mi - 0.5) * 0.36 + (ti - 1.5) * 0.06
                ax.scatter([x], [rel], marker=MARKERS[st], s=34,
                           color="#0072b2" if name == "random" else "#e69f00",
                           edgecolor="black", linewidth=0.4, zorder=3,
                           label=(f"{SHORT[st]}, {name}" if si == 0 else None))
    ax.axhline(0.0, color="0.3", linewidth=0.8)
    ax.set_xticks(np.arange(len(SCENARIOS_ORDER)))
    ax.set_xticklabels(SCENARIOS_ORDER)
    ax.set_ylabel("Change of walked exposure (%)\nconfigured vs $\\lambda_E=0$")
    ax.set_title(lab[2] + "All scenario $\\times$ style conditions")
    ax.grid(True, axis="y", linewidth=0.3, alpha=0.4)
    ax.legend(fontsize=6.5, ncol=1, loc="center left", bbox_to_anchor=(1.01, 0.5))
    fig.tight_layout()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    plt.close(fig)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
