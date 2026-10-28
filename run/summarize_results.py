#!/usr/bin/env python3
"""Print the mean intent metrics per (scenario, style) of a results.csv written by the experiment runner.
Usage: python run/summarize_results.py <results.csv>"""
import sys
import pandas as pd

COLS = [("objective_commitment_ratio", "objective commitment"), ("engagement_redirection_rate_per_100", "engagement redirection /100"),
        ("resource_seeking_rate_per_100", "resource seeking /100"), ("avg_ally_proximity", "nearest-ally distance"),
        ("kills", "kills"), ("deaths", "deaths"), ("control_score", "control score")]

def main() -> None:
    df = pd.read_csv(sys.argv[1])
    cols = [c for c, _ in COLS if c in df.columns]
    table = df.groupby(["scenario", "style"], sort=False)[cols].mean().round(2)
    table.columns = [dict(COLS)[c] for c in cols]
    n = df.groupby(["scenario", "style"]).size().iloc[0]
    pd.set_option("display.width", 200); pd.set_option("display.max_columns", 20)
    print(f"\nmean over {n} episodes per (scenario, style):\n")
    print(table.to_string())
    print()

if __name__ == "__main__":
    main()
