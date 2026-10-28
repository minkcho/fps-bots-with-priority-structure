# Figures of the paper

`make_all.sh` regenerates the seven figures of the paper from the result files in `results/` (copied from
`repro_outputs/` of the full artifact, same relative paths) into `out/`. Run from the repository root:

```bash
bash figures/make_all.sh            # uses python3; set PYTHON=/path/to/python to choose an interpreter
```

Requirements: Python 3.10+ with `numpy`, `pandas`, `matplotlib` (`requirements.txt`). The scripts import
`experiments/make_ec_figures.py` (confidence intervals) and `fps_priority_ai/` (map registry) through `--code .`.
Text is set in TeX Gyre Pagella when `kpsewhich` finds the font (TeX Live); otherwise matplotlib's default serif font.

| Figure (paper) | Script | Inputs under `results/` | Options used in the paper |
|---|---|---|---|
| Fig. 2 The maps of the study | `make_map_gallery.py` | `maps/testbed_fixed/descriptors.csv`; maps from `fps_priority_ai` | default |
| Fig. 3 Behavioral fingerprints | `make_fingerprint_heatmap.py` | `v3_fixed/results.csv` | `--width-cm 18.46 --height-cm 8.5` (full page width) |
| Fig. 4 Combat-movement mode ablation | `make_mode_ablation.py` | `v3_fixed/results.csv`, `v3_fixed/mode_ablation.csv` | default |
| Fig. 5 Commitment sweep of the four styles | `make_commit_sweep_styles.py` | `commit_sweep_styles/{random,urban}/sensitivity_commitment[_PO\|_Agg\|_SA].csv` | default |
| Fig. 6 Primary H3 tests | `make_h3_primary.py` | `v3_fixed/cost_term_ablation.csv`, `v3_fixed/urban/cost_term_ablation.csv` | `--hpad 2.0 --height 3.5` |
| Fig. 7 Style blending (H4) | `make_blending_trend.py` | `v3_fixed/interpolation.csv`, `v3_fixed/urban/interpolation.csv`, `blend_agg_mc/*/…Mission.csv`, `blend_po_sa/*/…Control.csv`, `v3_fixed/*/results.csv` | `--width-cm 18.46` |
| Fig. 8 Confirmation forest plots | `make_confirmation_forest.py` | `v4_maps/confirmation_summary.json` | default |

Figure 1 (the reconstructed pseudocode of the four bots) is typeset in LaTeX and has no script. The tables of the
paper are produced by the analysis scripts of each run (`experiments/analyze_*.py`, `make_*_tables.py`); their
Markdown and LaTeX outputs are kept under `results/`.

The CSV files under `results/` are the complete per-episode outputs of the runs that the figures use (about 5 MB); the Markdown, JSON and LaTeX files next to them are the analysis summaries and generated tables of the same runs. The complete result files of the
study (about 250 MB) and the pre-registered protocols with their hash lists are available from the authors on request.
