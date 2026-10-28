#!/bin/bash
# The development-map experiments of the paper (Sections 6.1-6.4) on one map, then the hypothesis tests H1-H4 of that map:
#   main experiment (3 scenarios x 4 styles vs. the Aggressive opponent), commitment sweep (H2), combat-mode ablation (H1),
#   route-term ablation (H3), teammate term (H3b), style blends (H4), and analyze_hypotheses.py (effect sizes, Holm-adjusted p).
# All runs share the common-random-numbers design, so every variant sees the same initial states episode by episode.
# Usage: bash run/main_experiment.sh [EPISODES] [MAP] [OUT_DIR]
#   defaults: 100 episodes (as in the paper; about 70 minutes on one core), map "random", output outputs/main_<MAP>
#   a first look: bash run/main_experiment.sh 10          (about 7 minutes; the tests need at least 5 episodes)
set -e
source "$(dirname "$0")/_common.sh"
EPISODES="${1:-100}"; MAP="${2:-random}"; OUT="${3:-$ROOT/outputs/main_$MAP}"
cd "$CODE"
run() { echo "== $1"; shift; "$PYTHON" "$@"; }
run "main experiment (H1)"        experiments/run_ec_experiments.py       --out "$OUT" --episodes "$EPISODES" --seed 2026 --map "$MAP"
run "commitment sweep (H2)"       experiments/run_sensitivity_commitment.py --out "$OUT" --episodes "$EPISODES" --seed 2026 --map "$MAP"
run "combat-mode ablation (H1)"   experiments/run_mode_ablation.py        --out "$OUT" --episodes "$EPISODES" --seed 2026 --map "$MAP"
run "route-term ablation (H3)"    experiments/run_cost_term_ablation.py   --out "$OUT" --episodes "$EPISODES" --seed 2026 --map "$MAP"
run "teammate term (H3b)"         experiments/run_teammate_term.py        --out "$OUT" --episodes "$EPISODES" --seed 2026 --map "$MAP" --exact-out
run "style blends (H4)"           experiments/run_interpolation.py        --out "$OUT" --episodes "$EPISODES" --seed 2026 --map "$MAP"
if [ "$EPISODES" -ge 5 ]; then
  run "hypothesis tests"          experiments/analyze_hypotheses.py       --dir "$OUT" --map-name "$MAP"
else
  echo "== hypothesis tests skipped: the style classifier uses 5-fold cross-validation, so run at least 5 episodes"
fi
"$PYTHON" "$RUN_DIR/summarize_results.py" "$OUT/results.csv"
echo "results, hypotheses_summary.md and hypotheses_summary.json: $OUT/"
