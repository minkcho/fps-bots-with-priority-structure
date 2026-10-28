"""Summarise probe_cost_scale.py output (per map, scale k, style; and per goal class).

Usage:
  python experiments/analyze_cost_scale.py --dir ../repro_outputs/probe_cost_scale
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

STYLES = ["Mission–Cooperation", "Persistent Objective", "Aggressive", "Survival-Aware"]


def summarise(g: pd.DataFrame) -> dict:
    g = g[g["L"] > 0]
    x = g["XE"] + g["XC"] + g["XT"]
    det = g[g["L"] > g["L0"]]
    return {
        "plans": len(g),
        "len": g["L"].mean(),
        "extra_share": (x / (g["L"] + x)).mean(),                 # share of the extra cost in total path cost
        "E_step": g["XE"].sum() / g["L"].sum(),                   # lambda_E * E per step
        "C_step": g["XC"].sum() / g["L"].sum(),                   # lambda_C * (1 - Cover) per step
        "T_step": g["XT"].sum() / g["L"].sum(),                   # lambda_T * Sep per step
        "differs": g["differs"].mean(),                           # P != P0 (any cell)
        "detour": (g["L"] > g["L0"]).mean(),                      # P longer than the shortest path
        "detour_steps": (det["L"] - det["L0"]).mean() if len(det) else 0.0,
        "len_ratio": g["L"].sum() / g["L0"].sum(),
        "exp_ratio": g["E_P"].sum() / g["E_P0"].sum() if g["E_P0"].sum() > 0 else float("nan"),
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", type=str, required=True)
    args = p.parse_args()
    d = Path(args.dir)
    df = pd.concat([pd.read_csv(f) for f in sorted(d.glob("plans_*.csv.gz"))], ignore_index=True)
    md = ["# Route cost vs distance: probe summary\n",
          "extra_share: mean share of lambda-weighted extra cost in the total path cost; E/C/T_step: extra cost per step "
          "(unit distance cost = 1); differs: planned path differs from the distance-only path; detour: planned path is "
          "longer than the shortest path; len_ratio: total planned / shortest length; exp_ratio: exposure along planned / "
          "along shortest paths.\n"]
    cols = ["plans", "len", "extra_share", "E_step", "C_step", "T_step", "differs", "detour", "detour_steps", "len_ratio", "exp_ratio"]
    for m in sorted(df["map"].unique()):
        md.append(f"\n## {m} map (pooled over scenarios)\n")
        md.append("| k | style | " + " | ".join(cols) + " |")
        md.append("|---|---|" + "---|" * len(cols))
        for k in sorted(df["k"].unique()):
            for st in STYLES:
                s = summarise(df[(df["map"] == m) & (df["k"] == k) & (df["style"] == st)])
                md.append(f"| x{k} | {st} | " + " | ".join(
                    f"{s[c]:.0f}" if c == "plans" else f"{s[c]:.3f}" for c in cols) + " |")
        md.append(f"\n### {m} map, k = 1, by goal class (all styles)\n")
        md.append("| goal | share of plans | " + " | ".join(cols) + " |")
        md.append("|---|---|" + "---|" * len(cols))
        g1 = df[(df["map"] == m) & (df["k"] == 1)]
        for gc, g in g1.groupby("goal"):
            s = summarise(g)
            md.append(f"| {gc} | {len(g) / len(g1):.2f} | " + " | ".join(
                f"{s[c]:.0f}" if c == "plans" else f"{s[c]:.3f}" for c in cols) + " |")
        md.append(f"\n### {m} map, k = 1, Survival-Aware by goal class\n")
        md.append("| goal | share of plans | " + " | ".join(cols) + " |")
        md.append("|---|---|" + "---|" * len(cols))
        gs = g1[g1["style"] == "Survival-Aware"]
        for gc, g in gs.groupby("goal"):
            s = summarise(g)
            md.append(f"| {gc} | {len(g) / len(gs):.2f} | " + " | ".join(
                f"{s[c]:.0f}" if c == "plans" else f"{s[c]:.3f}" for c in cols) + " |")
    (d / "cost_scale_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print((d / "cost_scale_summary.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
