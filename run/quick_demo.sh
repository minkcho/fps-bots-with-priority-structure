#!/bin/bash
# Quick demonstration: the four designed styles in the three scenarios on the default random map, a few episodes each.
# Prints the mean intent metrics per (scenario, style) and writes results.csv plus map and trajectory images.
# Usage: bash run/quick_demo.sh [EPISODES] [OUT_DIR]      (default 5 episodes, about one minute; output outputs/quick_demo)
set -e
source "$(dirname "$0")/_common.sh"
EPISODES="${1:-5}"; OUT="${2:-$ROOT/outputs/quick_demo}"
"$PYTHON" "$CODE/experiments/run_experiments.py" --out "$OUT" --episodes "$EPISODES" --seed 2026
"$PYTHON" "$RUN_DIR/summarize_results.py" "$OUT/results.csv"
echo "trajectory and map images: $OUT/figures/"
