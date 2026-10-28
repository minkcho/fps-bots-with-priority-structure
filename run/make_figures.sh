#!/bin/bash
# Regenerate the seven figures of the paper from results/ into figures/out/ (see figures/README.md).
# Usage: bash run/make_figures.sh
set -e
source "$(dirname "$0")/_common.sh"
PYTHON="$PYTHON" bash "$ROOT/figures/make_all.sh"
