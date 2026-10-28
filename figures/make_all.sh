#!/bin/bash
# Regenerate the seven figures of the paper from results/ into figures/out/.
# Run from the repository root:  bash figures/make_all.sh   (python3 with numpy, pandas, matplotlib; TeX Gyre Pagella via kpsewhich if available)
set -e
cd "$(dirname "$0")/.."
PY=${PYTHON:-python3}; S=figures/scripts; D=results; O=figures/out; mkdir -p "$O"
$PY $S/make_map_gallery.py          --code . --descriptors $D/maps/testbed_fixed/descriptors.csv --out $O/fig_map_gallery.pdf
$PY $S/make_fingerprint_heatmap.py  --csv $D/v3_fixed/results.csv --width-cm 18.46 --height-cm 8.5 --out $O/fig_fingerprint_heatmap.pdf
$PY $S/make_mode_ablation.py        --csv $D/v3_fixed/results.csv --mode-csv $D/v3_fixed/mode_ablation.csv --code . --out $O/fig_mode_ablation.pdf
$PY $S/make_commit_sweep_styles.py  --root $D/commit_sweep_styles --code . --out $O/fig_commit_sweep_styles.pdf
$PY $S/make_h3_primary.py           --random-dir $D/v3_fixed --urban-dir $D/v3_fixed/urban --code . --hpad 2.0 --height 3.5 --out $O/fig_h3_primary.pdf
$PY $S/make_blending_trend.py       --random-dir $D/v3_fixed --urban-dir $D/v3_fixed/urban --outputs-root $D --code . --width-cm 18.46 --out $O/fig_blending_trend.pdf
$PY $S/make_confirmation_forest.py  --root $D/v4_maps --out $O/fig_confirmation_forest.pdf
echo "figures written to $O/"
