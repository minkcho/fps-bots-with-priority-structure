# Commitment sweep, all four designed styles (exploratory)

Goal switches per 100 alive steps (mean [95% CI]), objective commitment, Control wins of 100; n = 100 episodes per cell; seed 2026; final testbed (five rule flags on).


## random map


### Mission

| w_commit | MC switches | PO switches | Agg switches | SA switches | MC obj. commit | PO obj. commit | Agg obj. commit | SA obj. commit |
|---|---|---|---|---|---|---|---|---|
| 0.00 | 25.36 [21.10, 29.62] | 32.41 [26.52, 38.30] | 34.79 [29.32, 40.27] | 23.68 [20.02, 27.33] | 0.80 | 0.79 | 0.53 | 0.11 |
| 0.20 | 3.23 [1.86, 4.60] | 2.16 [1.67, 2.65] | 2.88 [2.52, 3.24] | 3.71 [3.27, 4.14] | 0.93 | 0.94 | 0.37 | 0.05 |
| 0.25 | 1.92 [1.64, 2.20] | 1.55 [1.29, 1.81] | 2.88 [2.52, 3.24]* | 3.71 [3.27, 4.14]* | 0.93 | 0.94 | 0.37 | 0.05 |
| 0.45 | 1.13 [0.93, 1.32]* | 1.14 [0.92, 1.36] | 2.88 [2.52, 3.24] | 3.71 [3.27, 4.14] | 0.94 | 0.92 | 0.37 | 0.05 |
| 0.65 | 0.77 [0.66, 0.89] | 0.83 [0.70, 0.95] | 2.88 [2.52, 3.24] | 3.71 [3.27, 4.14] | 0.92 | 0.92 | 0.37 | 0.05 |
| 0.85 | 0.58 [0.51, 0.66] | 0.54 [0.48, 0.60]* | 2.88 [2.52, 3.24] | 3.71 [3.27, 4.14] | 0.93 | 0.91 | 0.37 | 0.05 |
| 1.05 | 0.51 [0.46, 0.57] | 0.54 [0.48, 0.60] | 2.88 [2.52, 3.24] | 3.71 [3.27, 4.14] | 0.92 | 0.91 | 0.37 | 0.05 |
| 1.25 | 0.51 [0.46, 0.57] | 0.54 [0.48, 0.60] | 2.88 [2.52, 3.24] | 3.71 [3.27, 4.14] | 0.92 | 0.91 | 0.37 | 0.05 |

* = the style's configured value (the main experiment).

- MC: Spearman rho(w, switches) = -0.65 (p = 2.0e-96); switches at w = 0 25.36 -> at w = 1.25 0.51 (-98%)
- PO: Spearman rho(w, switches) = -0.61 (p = 1.6e-82); switches at w = 0 32.41 -> at w = 1.25 0.54 (-98%)
- Agg: Spearman rho(w, switches) = -0.32 (p = 2.6e-20); switches at w = 0 34.79 -> at w = 1.25 2.88 (-92%)
- SA: Spearman rho(w, switches) = -0.25 (p = 3.3e-13); switches at w = 0 23.68 -> at w = 1.25 3.71 (-84%)

### Control

| w_commit | MC switches | PO switches | Agg switches | SA switches | MC obj. commit | PO obj. commit | Agg obj. commit | SA obj. commit | MC wins | PO wins | Agg wins | SA wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.00 | 26.08 [23.51, 28.64] | 27.32 [23.98, 30.67] | 34.96 [31.00, 38.91] | 22.66 [19.72, 25.59] | 0.80 | 0.80 | 0.46 | 0.07 | 73 | 70 | 60 | 10 |
| 0.20 | 2.91 [2.65, 3.18] | 2.90 [2.52, 3.28] | 3.47 [3.18, 3.77] | 4.76 [4.31, 5.20] | 0.94 | 0.93 | 0.32 | 0.03 | 96 | 93 | 47 | 7 |
| 0.25 | 3.02 [2.45, 3.59] | 2.05 [1.79, 2.31] | 3.47 [3.18, 3.77]* | 4.76 [4.31, 5.20]* | 0.93 | 0.93 | 0.32 | 0.03 | 95 | 92 | 47 | 7 |
| 0.45 | 1.16 [1.02, 1.30]* | 1.34 [1.18, 1.49] | 3.47 [3.18, 3.77] | 4.75 [4.31, 5.19] | 0.94 | 0.92 | 0.32 | 0.03 | 95 | 95 | 47 | 7 |
| 0.65 | 1.09 [0.97, 1.20] | 1.16 [1.05, 1.28] | 3.47 [3.18, 3.77] | 4.75 [4.31, 5.19] | 0.94 | 0.92 | 0.32 | 0.03 | 96 | 95 | 47 | 7 |
| 0.85 | 0.95 [0.88, 1.03] | 0.99 [0.92, 1.06]* | 3.47 [3.18, 3.77] | 4.75 [4.31, 5.19] | 0.94 | 0.90 | 0.32 | 0.03 | 97 | 91 | 47 | 7 |
| 1.05 | 0.89 [0.84, 0.94] | 0.99 [0.92, 1.06] | 3.47 [3.18, 3.77] | 4.75 [4.31, 5.19] | 0.94 | 0.90 | 0.32 | 0.03 | 96 | 91 | 47 | 7 |
| 1.25 | 0.89 [0.84, 0.94] | 0.99 [0.92, 1.06] | 3.47 [3.18, 3.77] | 4.75 [4.31, 5.19] | 0.94 | 0.90 | 0.32 | 0.03 | 96 | 91 | 47 | 7 |

* = the style's configured value (the main experiment).

- MC: Spearman rho(w, switches) = -0.76 (p = 7.0e-153); switches at w = 0 26.08 -> at w = 1.25 0.89 (-97%)
- PO: Spearman rho(w, switches) = -0.68 (p = 4.1e-109); switches at w = 0 27.32 -> at w = 1.25 0.99 (-96%)
- Agg: Spearman rho(w, switches) = -0.33 (p = 7.1e-22); switches at w = 0 34.96 -> at w = 1.25 3.47 (-90%)
- SA: Spearman rho(w, switches) = -0.28 (p = 1.0e-15); switches at w = 0 22.66 -> at w = 1.25 4.75 (-79%)

## urban map


### Mission

| w_commit | MC switches | PO switches | Agg switches | SA switches | MC obj. commit | PO obj. commit | Agg obj. commit | SA obj. commit |
|---|---|---|---|---|---|---|---|---|
| 0.00 | 21.88 [17.78, 25.98] | 27.99 [23.10, 32.89] | 39.31 [34.24, 44.37] | 26.66 [22.95, 30.37] | 0.81 | 0.82 | 0.41 | 0.07 |
| 0.20 | 4.01 [1.93, 6.09] | 2.29 [1.47, 3.11] | 3.26 [2.89, 3.63] | 4.22 [3.74, 4.70] | 0.92 | 0.94 | 0.32 | 0.04 |
| 0.25 | 2.79 [1.66, 3.91] | 2.67 [1.46, 3.87] | 3.26 [2.89, 3.63]* | 4.23 [3.74, 4.71]* | 0.93 | 0.93 | 0.32 | 0.04 |
| 0.45 | 1.11 [0.90, 1.33]* | 1.02 [0.84, 1.19] | 3.26 [2.89, 3.63] | 4.26 [3.78, 4.75] | 0.94 | 0.93 | 0.32 | 0.04 |
| 0.65 | 0.99 [0.81, 1.16] | 0.78 [0.66, 0.89] | 3.26 [2.89, 3.63] | 4.26 [3.78, 4.75] | 0.93 | 0.92 | 0.32 | 0.04 |
| 0.85 | 0.65 [0.54, 0.77] | 0.55 [0.47, 0.62]* | 3.26 [2.89, 3.63] | 4.26 [3.78, 4.75] | 0.93 | 0.87 | 0.32 | 0.04 |
| 1.05 | 0.52 [0.44, 0.59] | 0.55 [0.47, 0.62] | 3.26 [2.89, 3.63] | 4.26 [3.78, 4.75] | 0.93 | 0.87 | 0.32 | 0.04 |
| 1.25 | 0.52 [0.44, 0.59] | 0.55 [0.47, 0.62] | 3.26 [2.89, 3.63] | 4.26 [3.78, 4.75] | 0.93 | 0.87 | 0.32 | 0.04 |

* = the style's configured value (the main experiment).

- MC: Spearman rho(w, switches) = -0.52 (p = 1.9e-56); switches at w = 0 21.88 -> at w = 1.25 0.52 (-98%)
- PO: Spearman rho(w, switches) = -0.56 (p = 1.1e-66); switches at w = 0 27.99 -> at w = 1.25 0.55 (-98%)
- Agg: Spearman rho(w, switches) = -0.32 (p = 1.6e-20); switches at w = 0 39.31 -> at w = 1.25 3.26 (-92%)
- SA: Spearman rho(w, switches) = -0.26 (p = 5.6e-14); switches at w = 0 26.66 -> at w = 1.25 4.26 (-84%)

### Control

| w_commit | MC switches | PO switches | Agg switches | SA switches | MC obj. commit | PO obj. commit | Agg obj. commit | SA obj. commit | MC wins | PO wins | Agg wins | SA wins |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.00 | 29.47 [25.70, 33.24] | 34.79 [30.56, 39.03] | 40.86 [36.14, 45.57] | 22.54 [19.12, 25.95] | 0.79 | 0.77 | 0.39 | 0.06 | 70 | 73 | 51 | 6 |
| 0.20 | 2.85 [2.07, 3.64] | 2.61 [1.90, 3.32] | 4.02 [3.72, 4.32] | 5.01 [4.56, 5.46] | 0.94 | 0.94 | 0.29 | 0.02 | 89 | 93 | 48 | 4 |
| 0.25 | 2.35 [1.81, 2.89] | 2.29 [1.83, 2.75] | 4.01 [3.71, 4.31]* | 5.01 [4.56, 5.46]* | 0.94 | 0.93 | 0.29 | 0.02 | 88 | 97 | 48 | 4 |
| 0.45 | 1.26 [1.08, 1.44]* | 1.27 [1.09, 1.45] | 4.01 [3.71, 4.31] | 5.01 [4.56, 5.46] | 0.95 | 0.93 | 0.29 | 0.02 | 94 | 94 | 48 | 4 |
| 0.65 | 1.15 [1.00, 1.30] | 1.08 [0.97, 1.20] | 4.01 [3.71, 4.31] | 5.01 [4.56, 5.46] | 0.94 | 0.93 | 0.29 | 0.02 | 94 | 97 | 48 | 4 |
| 0.85 | 1.03 [0.92, 1.14] | 0.90 [0.84, 0.96]* | 4.01 [3.71, 4.31] | 5.01 [4.56, 5.46] | 0.94 | 0.91 | 0.29 | 0.02 | 90 | 96 | 48 | 4 |
| 1.05 | 0.89 [0.82, 0.95] | 0.90 [0.84, 0.96] | 4.01 [3.71, 4.31] | 5.01 [4.56, 5.46] | 0.94 | 0.91 | 0.29 | 0.02 | 95 | 96 | 48 | 4 |
| 1.25 | 0.89 [0.82, 0.95] | 0.90 [0.84, 0.96] | 4.01 [3.71, 4.31] | 5.01 [4.56, 5.46] | 0.94 | 0.91 | 0.29 | 0.02 | 95 | 96 | 48 | 4 |

* = the style's configured value (the main experiment).

- MC: Spearman rho(w, switches) = -0.46 (p = 5.4e-43); switches at w = 0 29.47 -> at w = 1.25 0.89 (-97%)
- PO: Spearman rho(w, switches) = -0.63 (p = 8.4e-91); switches at w = 0 34.79 -> at w = 1.25 0.90 (-97%)
- Agg: Spearman rho(w, switches) = -0.33 (p = 2.8e-21); switches at w = 0 40.86 -> at w = 1.25 4.01 (-90%)
- SA: Spearman rho(w, switches) = -0.27 (p = 6.8e-15); switches at w = 0 22.54 -> at w = 1.25 5.01 (-78%)

## Reproduction checks

- random, MC, Mission, w = 0.45 vs main experiment: identical (100 episodes)
- random, MC, Mission: all shared values vs the original sweep checked (differences listed above, if any)
- random, MC, Control, w = 0.45 vs main experiment: identical (100 episodes)
- random, MC, Control: all shared values vs the original sweep checked (differences listed above, if any)
- random, PO, Mission, w = 0.85 vs main experiment: identical (100 episodes)
- random, PO, Control, w = 0.85 vs main experiment: identical (100 episodes)
- random, Agg, Mission, w = 0.25 vs main experiment: identical (100 episodes)
- random, Agg, Control, w = 0.25 vs main experiment: identical (100 episodes)
- random, SA, Mission, w = 0.25 vs main experiment: identical (100 episodes)
- random, SA, Control, w = 0.25 vs main experiment: identical (100 episodes)
- urban, MC, Mission, w = 0.45 vs main experiment: identical (100 episodes)
- urban, MC, Mission: all shared values vs the original sweep checked (differences listed above, if any)
- urban, MC, Control, w = 0.45 vs main experiment: identical (100 episodes)
- urban, MC, Control: all shared values vs the original sweep checked (differences listed above, if any)
- urban, PO, Mission, w = 0.85 vs main experiment: identical (100 episodes)
- urban, PO, Control, w = 0.85 vs main experiment: identical (100 episodes)
- urban, Agg, Mission, w = 0.25 vs main experiment: identical (100 episodes)
- urban, Agg, Control, w = 0.25 vs main experiment: identical (100 episodes)
- urban, SA, Mission, w = 0.25 vs main experiment: identical (100 episodes)
- urban, SA, Control, w = 0.25 vs main experiment: identical (100 episodes)
