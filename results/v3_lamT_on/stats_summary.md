# Statistical summary (n = 30 episodes per condition)

Consistency checks (CRN): navigation-ablation full = main; commitment 0.45 = main MC; lambda x1 = main; lambda x0 = distance-only. **passed**

## Main experiment

| Scenario | Style | ObjCommit | AllyDist | EngRedirect | ResSeek | Kills | Deaths | Control |
|---|---|---|---|---|---|---|---|---|
| Mission | Mission–Cooperation | 0.95 ± 0.02 | 1.91 ± 0.32 | 0.00 ± 0.00 | 0.00 ± 0.00 | 5.4 ± 1.6 | 4.2 ± 1.4 |  |
| Mission | Persistent Objective | 0.90 ± 0.04 | 2.50 ± 0.51 | 0.00 ± 0.01 | 0.00 ± 0.00 | 6.1 ± 1.9 | 4.9 ± 1.6 |  |
| Mission | Aggressive | 0.20 ± 0.11 | 3.84 ± 0.78 | 0.86 ± 0.19 | 0.00 ± 0.00 | 6.7 ± 1.5 | 6.8 ± 1.5 |  |
| Mission | Survival-Aware | 0.02 ± 0.02 | 4.52 ± 1.01 | 0.52 ± 0.18 | 0.43 ± 0.11 | 4.4 ± 1.0 | 3.3 ± 0.7 |  |
| Deathmatch | Mission–Cooperation | 0.00 ± 0.00 | 2.09 ± 0.34 | 0.19 ± 0.10 | 0.06 ± 0.03 | 5.7 ± 1.5 | 4.5 ± 1.1 |  |
| Deathmatch | Persistent Objective | 0.00 ± 0.00 | 5.29 ± 0.69 | 0.06 ± 0.04 | 0.00 ± 0.01 | 8.7 ± 0.9 | 4.8 ± 0.8 |  |
| Deathmatch | Aggressive | 0.00 ± 0.00 | 4.15 ± 0.62 | 1.33 ± 0.19 | 0.00 ± 0.00 | 10.1 ± 1.4 | 10.0 ± 1.4 |  |
| Deathmatch | Survival-Aware | 0.00 ± 0.00 | 3.43 ± 0.50 | 0.69 ± 0.21 | 0.41 ± 0.10 | 4.2 ± 1.1 | 3.5 ± 0.8 |  |
| Control | Mission–Cooperation | 0.96 ± 0.01 | 1.69 ± 0.32 | 0.00 ± 0.00 | 0.00 ± 0.00 | 1.9 ± 0.7 | 1.1 ± 0.5 | 114.23 ± 8.83; wins 28/30; stalls 0; med. steps 143.0 |
| Control | Persistent Objective | 0.90 ± 0.07 | 2.77 ± 1.04 | 0.00 ± 0.00 | 0.00 ± 0.00 | 2.4 ± 0.9 | 1.5 ± 0.7 | 118.23 ± 3.61; wins 29/30; stalls 0; med. steps 143.0 |
| Control | Aggressive | 0.17 ± 0.09 | 3.87 ± 0.59 | 1.00 ± 0.19 | 0.00 ± 0.00 | 6.5 ± 1.7 | 6.4 ± 1.6 | 39.70 ± 20.16; wins 8/30; stalls 1; med. steps 313.0 |
| Control | Survival-Aware | 0.03 ± 0.03 | 4.38 ± 1.13 | 0.90 ± 0.84 | 0.31 ± 0.11 | 3.5 ± 0.9 | 2.3 ± 0.9 | 16.43 ± 14.74; wins 3/30; stalls 3; med. steps 255.0 |

## Style contrasts (Mann–Whitney U, rank-biserial r > 0: first style higher; Holm within family)

| Scenario | Metric | Style A | Style B | r | p | p (Holm) |
|---|---|---|---|---|---|---|
| Mission | ObjCommit | Mission–Cooperation | Persistent Objective | +0.24 | 0.109 | 0.109 |
| Mission | ObjCommit | Mission–Cooperation | Aggressive | +0.94 | <0.001 | <0.001 |
| Mission | ObjCommit | Mission–Cooperation | Survival-Aware | +1.00 | <0.001 | <0.001 |
| Mission | ObjCommit | Persistent Objective | Aggressive | +0.91 | <0.001 | <0.001 |
| Mission | ObjCommit | Persistent Objective | Survival-Aware | +1.00 | <0.001 | <0.001 |
| Mission | ObjCommit | Aggressive | Survival-Aware | +0.37 | 0.007 | 0.015 |
| Mission | AllyDist | Mission–Cooperation | Persistent Objective | -0.20 | 0.180 | 0.360 |
| Mission | AllyDist | Mission–Cooperation | Aggressive | -0.59 | <0.001 | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Survival-Aware | -0.66 | <0.001 | <0.001 |
| Mission | AllyDist | Persistent Objective | Aggressive | -0.40 | 0.008 | 0.024 |
| Mission | AllyDist | Persistent Objective | Survival-Aware | -0.48 | 0.002 | 0.006 |
| Mission | AllyDist | Aggressive | Survival-Aware | -0.12 | 0.420 | 0.420 |
| Deathmatch | EngRedirect | Mission–Cooperation | Persistent Objective | +0.39 | 0.006 | 0.006 |
| Deathmatch | EngRedirect | Mission–Cooperation | Aggressive | -0.94 | <0.001 | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Survival-Aware | -0.60 | <0.001 | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Aggressive | -0.99 | <0.001 | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Survival-Aware | -0.79 | <0.001 | <0.001 |
| Deathmatch | EngRedirect | Aggressive | Survival-Aware | +0.64 | <0.001 | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Persistent Objective | +0.37 | <0.001 | 0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Aggressive | +0.40 | <0.001 | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Survival-Aware | -0.76 | <0.001 | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Aggressive | +0.03 | 0.334 | 0.334 |
| Deathmatch | ResSeek | Persistent Objective | Survival-Aware | -0.92 | <0.001 | <0.001 |
| Deathmatch | ResSeek | Aggressive | Survival-Aware | -0.93 | <0.001 | <0.001 |
| Deathmatch | AllyDist | Mission–Cooperation | Persistent Objective | -0.89 | <0.001 | <0.001 |
| Deathmatch | AllyDist | Mission–Cooperation | Aggressive | -0.73 | <0.001 | <0.001 |
| Deathmatch | AllyDist | Mission–Cooperation | Survival-Aware | -0.59 | <0.001 | <0.001 |
| Deathmatch | AllyDist | Persistent Objective | Aggressive | +0.34 | 0.026 | 0.052 |
| Deathmatch | AllyDist | Persistent Objective | Survival-Aware | +0.55 | <0.001 | <0.001 |
| Deathmatch | AllyDist | Aggressive | Survival-Aware | +0.25 | 0.096 | 0.096 |
| Control | CtrlScore | Mission–Cooperation | Persistent Objective | -0.03 | 0.557 | 0.557 |
| Control | CtrlScore | Mission–Cooperation | Aggressive | +0.68 | <0.001 | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Survival-Aware | +0.85 | <0.001 | <0.001 |
| Control | CtrlScore | Persistent Objective | Aggressive | +0.72 | <0.001 | <0.001 |
| Control | CtrlScore | Persistent Objective | Survival-Aware | +0.89 | <0.001 | <0.001 |
| Control | CtrlScore | Aggressive | Survival-Aware | +0.19 | 0.146 | 0.293 |
| Control | ObjCommit | Mission–Cooperation | Persistent Objective | +0.16 | 0.268 | 0.268 |
| Control | ObjCommit | Mission–Cooperation | Aggressive | +0.95 | <0.001 | <0.001 |
| Control | ObjCommit | Mission–Cooperation | Survival-Aware | +1.00 | <0.001 | <0.001 |
| Control | ObjCommit | Persistent Objective | Aggressive | +0.91 | <0.001 | <0.001 |
| Control | ObjCommit | Persistent Objective | Survival-Aware | +0.99 | <0.001 | <0.001 |
| Control | ObjCommit | Aggressive | Survival-Aware | +0.42 | 0.002 | 0.003 |
| Control | AllyDist | Mission–Cooperation | Persistent Objective | -0.18 | 0.230 | 0.460 |
| Control | AllyDist | Mission–Cooperation | Aggressive | -0.73 | <0.001 | <0.001 |
| Control | AllyDist | Mission–Cooperation | Survival-Aware | -0.62 | <0.001 | <0.001 |
| Control | AllyDist | Persistent Objective | Aggressive | -0.49 | 0.001 | 0.004 |
| Control | AllyDist | Persistent Objective | Survival-Aware | -0.42 | 0.006 | 0.017 |
| Control | AllyDist | Aggressive | Survival-Aware | -0.02 | 0.888 | 0.888 |

## Commitment sensitivity (Mission–Cooperation base)

| w_commit | Mission ObjCommit | Control score | Control wins | stalls |
|---|---|---|---|---|
| 0.00 | 0.87 ± 0.07 | 106.20 ± 12.87 | 25/30 | 1 |
| 0.20 | 0.94 ± 0.03 | 114.23 ± 8.83 | 28/30 | 0 |
| 0.45 | 0.95 ± 0.02 | 114.23 ± 8.83 | 28/30 | 0 |
| 0.65 | 0.94 ± 0.02 | 114.23 ± 8.83 | 28/30 | 0 |
| 0.85 | 0.93 ± 0.03 | 111.30 ± 9.67 | 26/30 | 0 |
| 1.05 | 0.94 ± 0.02 | 108.17 ± 11.26 | 25/30 | 0 |
| 1.25 | 0.94 ± 0.02 | 108.17 ± 11.26 | 25/30 | 0 |

Paired Wilcoxon, w=0.45 vs w=0 (Mission, ObjCommit): r = +0.54, p = 0.010

Paired Wilcoxon, w=0.45 vs w=0 (Control, CtrlScore): r = +0.52, p = 0.281

## Navigation ablation (full vs distance-only; paired Wilcoxon, r > 0: full higher)

| Condition | Metric | Full | Distance-only | r | p |
|---|---|---|---|---|---|
| Mission/Mission–Cooperation | AllyDist | 1.91 ± 0.32 | 2.04 ± 0.35 | -0.14 | 0.596 |
| Mission/Mission–Cooperation | ObjCommit | 0.95 ± 0.02 | 0.94 ± 0.02 | +0.15 | 0.609 |
| Mission/Mission–Cooperation | EngRedirect | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Mission/Mission–Cooperation | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Mission/Mission–Cooperation | Kills | 5.37 ± 1.64 | 6.80 ± 2.04 | -0.77 | 0.009 |
| Mission/Mission–Cooperation | Deaths | 4.20 ± 1.40 | 4.80 ± 1.49 | -0.34 | 0.294 |
| Deathmatch/Survival-Aware | AllyDist | 3.43 ± 0.50 | 3.42 ± 0.63 | -0.05 | 0.824 |
| Deathmatch/Survival-Aware | ObjCommit | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Deathmatch/Survival-Aware | EngRedirect | 0.69 ± 0.21 | 1.71 ± 0.60 | -0.68 | <0.001 |
| Deathmatch/Survival-Aware | ResSeek | 0.41 ± 0.10 | 0.85 ± 0.15 | -0.74 | <0.001 |
| Deathmatch/Survival-Aware | Kills | 4.23 ± 1.09 | 8.17 ± 1.34 | -0.72 | <0.001 |
| Deathmatch/Survival-Aware | Deaths | 3.50 ± 0.77 | 6.97 ± 1.10 | -0.75 | <0.001 |

## Combat-mode ablation (full vs weights-only; paired Wilcoxon, r > 0: full higher)

| Scenario | Style | Metric | Full | Weights-only | r | p |
|---|---|---|---|---|---|---|
| Mission | Mission–Cooperation | ObjCommit | 0.95 ± 0.02 | 0.93 ± 0.02 | +0.46 | 0.076 |
| Mission | Mission–Cooperation | AllyDist | 1.91 ± 0.32 | 2.11 ± 0.39 | -0.27 | 0.312 |
| Mission | Mission–Cooperation | EngRedirect | 0.00 ± 0.00 | 0.01 ± 0.01 | -1.00 | 0.500 |
| Mission | Mission–Cooperation | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Mission | Persistent Objective | ObjCommit | 0.90 ± 0.04 | 0.90 ± 0.04 | +0.00 | 1.000 |
| Mission | Persistent Objective | AllyDist | 2.50 ± 0.51 | 2.50 ± 0.51 | +0.00 | 1.000 |
| Mission | Persistent Objective | EngRedirect | 0.00 ± 0.01 | 0.00 ± 0.01 | +0.00 | 1.000 |
| Mission | Persistent Objective | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Mission | Aggressive | ObjCommit | 0.20 ± 0.11 | 0.31 ± 0.12 | -0.57 | 0.015 |
| Mission | Aggressive | AllyDist | 3.84 ± 0.78 | 3.71 ± 0.89 | +0.01 | 0.966 |
| Mission | Aggressive | EngRedirect | 0.86 ± 0.19 | 0.49 ± 0.13 | +0.63 | 0.003 |
| Mission | Aggressive | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Mission | Survival-Aware | ObjCommit | 0.02 ± 0.02 | 0.03 ± 0.03 | +0.15 | 0.677 |
| Mission | Survival-Aware | AllyDist | 4.52 ± 1.01 | 5.22 ± 0.66 | -0.29 | 0.171 |
| Mission | Survival-Aware | EngRedirect | 0.52 ± 0.18 | 0.28 ± 0.08 | +0.46 | 0.028 |
| Mission | Survival-Aware | ResSeek | 0.43 ± 0.11 | 0.02 ± 0.02 | +1.00 | <0.001 |
| Deathmatch | Mission–Cooperation | EngRedirect | 0.19 ± 0.10 | 0.42 ± 0.14 | -0.58 | 0.007 |
| Deathmatch | Mission–Cooperation | ResSeek | 0.06 ± 0.03 | 0.12 ± 0.06 | -0.51 | 0.046 |
| Deathmatch | Mission–Cooperation | AllyDist | 2.09 ± 0.34 | 2.35 ± 0.27 | -0.34 | 0.109 |
| Deathmatch | Persistent Objective | EngRedirect | 0.06 ± 0.04 | 0.06 ± 0.04 | +0.00 | 1.000 |
| Deathmatch | Persistent Objective | ResSeek | 0.00 ± 0.01 | 0.00 ± 0.01 | +0.00 | 1.000 |
| Deathmatch | Persistent Objective | AllyDist | 5.29 ± 0.69 | 5.29 ± 0.69 | +0.00 | 1.000 |
| Deathmatch | Aggressive | EngRedirect | 1.33 ± 0.19 | 0.77 ± 0.14 | +0.93 | <0.001 |
| Deathmatch | Aggressive | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Deathmatch | Aggressive | AllyDist | 4.15 ± 0.62 | 4.68 ± 0.70 | -0.28 | 0.184 |
| Deathmatch | Survival-Aware | EngRedirect | 0.69 ± 0.21 | 0.28 ± 0.06 | +0.74 | <0.001 |
| Deathmatch | Survival-Aware | ResSeek | 0.41 ± 0.10 | 0.04 ± 0.02 | +0.97 | <0.001 |
| Deathmatch | Survival-Aware | AllyDist | 3.43 ± 0.50 | 6.62 ± 0.66 | -0.96 | <0.001 |
| Control | Mission–Cooperation | CtrlScore | 114.23 ± 8.83 | 119.70 ± 0.61 | -0.67 | 0.500 |
| Control | Mission–Cooperation | ObjCommit | 0.96 ± 0.01 | 0.95 ± 0.03 | +0.12 | 0.720 |
| Control | Mission–Cooperation | EngRedirect | 0.00 ± 0.00 | 0.02 ± 0.04 | -1.00 | 1.000 |
| Control | Mission–Cooperation | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Control | Persistent Objective | CtrlScore | 118.23 ± 3.61 | 118.23 ± 3.61 | +0.00 | 1.000 |
| Control | Persistent Objective | ObjCommit | 0.90 ± 0.07 | 0.90 ± 0.07 | +0.00 | 1.000 |
| Control | Persistent Objective | EngRedirect | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Control | Persistent Objective | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Control | Aggressive | CtrlScore | 39.70 ± 20.16 | 51.23 ± 21.67 | -0.25 | 0.328 |
| Control | Aggressive | ObjCommit | 0.17 ± 0.09 | 0.26 ± 0.11 | -0.42 | 0.092 |
| Control | Aggressive | EngRedirect | 1.00 ± 0.19 | 0.57 ± 0.10 | +0.81 | <0.001 |
| Control | Aggressive | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Control | Survival-Aware | CtrlScore | 16.43 ± 14.74 | 14.87 ± 14.00 | -0.11 | 0.706 |
| Control | Survival-Aware | ObjCommit | 0.03 ± 0.03 | 0.04 ± 0.03 | -0.07 | 0.910 |
| Control | Survival-Aware | EngRedirect | 0.90 ± 0.84 | 0.23 ± 0.07 | +0.50 | 0.020 |
| Control | Survival-Aware | ResSeek | 0.31 ± 0.11 | 0.02 ± 0.02 | +0.99 | <0.001 |

Weights-only Control outcomes: Mission–Cooperation: 29/30 wins; Persistent Objective: 29/30 wins; Aggressive: 12/30 wins; Survival-Aware: 3/30 wins

## Style interpolation (mode fixed to keep moving; Spearman rho between alpha and metric)


### Deathmatch: Aggressive -> Survival-Aware

| alpha | EngRedirect | ResSeek | AllyDist | Kills | Deaths |
|---|---|---|---|---|---|
| 0.00 | 0.77 ± 0.14 | 0.00 ± 0.00 | 4.68 ± 0.70 | 8.60 ± 1.31 | 7.70 ± 1.25 |
| 0.25 | 0.61 ± 0.11 | 0.01 ± 0.01 | 5.57 ± 0.65 | 8.33 ± 1.24 | 7.13 ± 1.30 |
| 0.50 | 0.44 ± 0.09 | 0.00 ± 0.01 | 5.22 ± 0.65 | 7.50 ± 1.29 | 5.77 ± 0.94 |
| 0.75 | 0.40 ± 0.08 | 0.04 ± 0.03 | 6.06 ± 0.72 | 7.87 ± 1.05 | 5.60 ± 0.90 |
| 1.00 | 0.28 ± 0.06 | 0.04 ± 0.02 | 6.62 ± 0.66 | 7.70 ± 0.86 | 4.97 ± 0.59 |

- Spearman rho(alpha, EngRedirect) = -0.51, p = <0.001
- Spearman rho(alpha, ResSeek) = +0.32, p = <0.001
- Spearman rho(alpha, AllyDist) = +0.33, p = <0.001
- Spearman rho(alpha, Kills) = -0.14, p = 0.078
- Spearman rho(alpha, Deaths) = -0.35, p = <0.001

### Mission: Mission–Cooperation -> Persistent Objective

| alpha | ObjCommit | AllyDist | EngRedirect | Kills | Deaths |
|---|---|---|---|---|---|
| 0.00 | 0.93 ± 0.02 | 2.11 ± 0.39 | 0.01 ± 0.01 | 6.80 ± 2.08 | 5.47 ± 1.73 |
| 0.25 | 0.93 ± 0.02 | 2.07 ± 0.32 | 0.01 ± 0.01 | 6.13 ± 1.85 | 5.13 ± 1.54 |
| 0.50 | 0.93 ± 0.02 | 2.13 ± 0.33 | 0.01 ± 0.01 | 6.20 ± 1.85 | 5.20 ± 1.57 |
| 0.75 | 0.91 ± 0.03 | 2.52 ± 0.50 | 0.00 ± 0.00 | 6.60 ± 1.93 | 5.67 ± 1.80 |
| 1.00 | 0.90 ± 0.04 | 2.50 ± 0.51 | 0.00 ± 0.01 | 6.10 ± 1.90 | 4.87 ± 1.58 |

- Spearman rho(alpha, ObjCommit) = -0.11, p = 0.198
- Spearman rho(alpha, AllyDist) = +0.12, p = 0.149
- Spearman rho(alpha, EngRedirect) = -0.09, p = 0.282
- Spearman rho(alpha, Kills) = -0.01, p = 0.875
- Spearman rho(alpha, Deaths) = -0.02, p = 0.838

## Navigation-weight scale (lambda x k; Spearman rho between k and metric)


### Mission / Mission–Cooperation

| scale | AllyDist | ObjCommit | EngRedirect | ResSeek | Kills | Deaths |
|---|---|---|---|---|---|---|
| x0 | 2.04 ± 0.35 | 0.94 ± 0.02 | 0.00 ± 0.00 | 0.00 ± 0.00 | 6.80 ± 2.04 | 4.80 ± 1.49 |
| x0.25 | 1.95 ± 0.30 | 0.94 ± 0.02 | 0.00 ± 0.01 | 0.00 ± 0.00 | 5.53 ± 1.63 | 4.47 ± 1.37 |
| x0.5 | 1.94 ± 0.30 | 0.95 ± 0.02 | 0.01 ± 0.01 | 0.00 ± 0.00 | 6.03 ± 1.81 | 4.47 ± 1.39 |
| x1 | 1.91 ± 0.32 | 0.95 ± 0.02 | 0.00 ± 0.00 | 0.00 ± 0.00 | 5.37 ± 1.64 | 4.20 ± 1.40 |
| x2 | 1.89 ± 0.31 | 0.95 ± 0.02 | 0.00 ± 0.00 | 0.00 ± 0.00 | 5.27 ± 1.62 | 3.97 ± 1.28 |

- Spearman rho(scale, AllyDist) = -0.04, p = 0.651
- Spearman rho(scale, ObjCommit) = +0.05, p = 0.574
- Spearman rho(scale, EngRedirect) = -0.03, p = 0.685
- Spearman rho(scale, Kills) = -0.10, p = 0.223
- Spearman rho(scale, Deaths) = -0.08, p = 0.350

### Deathmatch / Survival-Aware

| scale | AllyDist | ObjCommit | EngRedirect | ResSeek | Kills | Deaths |
|---|---|---|---|---|---|---|
| x0 | 3.42 ± 0.63 | 0.00 ± 0.00 | 1.71 ± 0.60 | 0.85 ± 0.15 | 8.17 ± 1.34 | 6.97 ± 1.10 |
| x0.25 | 4.07 ± 0.61 | 0.00 ± 0.00 | 1.39 ± 0.74 | 0.59 ± 0.10 | 6.33 ± 1.17 | 4.60 ± 0.94 |
| x0.5 | 3.87 ± 0.53 | 0.00 ± 0.00 | 0.79 ± 0.18 | 0.58 ± 0.11 | 5.33 ± 0.88 | 4.07 ± 0.73 |
| x1 | 3.43 ± 0.50 | 0.00 ± 0.00 | 0.69 ± 0.21 | 0.41 ± 0.10 | 4.23 ± 1.09 | 3.50 ± 0.77 |
| x2 | 4.09 ± 0.64 | 0.00 ± 0.00 | 0.58 ± 0.16 | 0.51 ± 0.13 | 5.00 ± 1.27 | 3.87 ± 0.95 |

- Spearman rho(scale, AllyDist) = +0.09, p = 0.298
- Spearman rho(scale, EngRedirect) = -0.35, p = <0.001
- Spearman rho(scale, ResSeek) = -0.33, p = <0.001
- Spearman rho(scale, Kills) = -0.34, p = <0.001
- Spearman rho(scale, Deaths) = -0.36, p = <0.001

## Additional experiment: designer risk budgets, relative budget (Deathmatch)


### Survival-Aware (fixed-weight reference: main experiment)

| beta | Adherence | ExposureRatio | LengthOverhead | lambda_E | EngRedirect | ResSeek | AllyDist | Kills | Deaths |
|---|---|---|---|---|---|---|---|---|---|
| fixed | – | – | – | 20.00 | 0.69 ± 0.21 | 0.41 ± 0.10 | 3.43 ± 0.50 | 4.23 ± 1.09 | 3.50 ± 0.77 |
| 1.00 | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 1.73 ± 1.45 | 0.75 ± 0.18 | 2.88 ± 0.48 | 6.73 ± 1.39 | 5.93 ± 1.33 |
| 0.75 | 0.889 ± 0.019 | 0.628 ± 0.035 | 1.199 ± 0.081 | 6.530 ± 1.022 | 0.73 ± 0.15 | 0.68 ± 0.12 | 4.29 ± 0.61 | 6.47 ± 0.92 | 5.23 ± 0.79 |
| 0.50 | 0.837 ± 0.051 | 0.600 ± 0.040 | 1.166 ± 0.030 | 8.871 ± 2.622 | 0.81 ± 0.21 | 0.59 ± 0.11 | 4.09 ± 0.79 | 6.20 ± 1.24 | 4.77 ± 0.78 |
| 0.25 | 0.798 ± 0.060 | 0.570 ± 0.065 | 1.175 ± 0.042 | 10.541 ± 3.029 | 0.70 ± 0.23 | 0.50 ± 0.13 | 3.89 ± 0.64 | 5.20 ± 1.18 | 4.23 ± 1.07 |

- Spearman rho(beta, budget_adherence) = +0.70, p = <0.001
- Spearman rho(beta, exposure_ratio) = +0.69, p = <0.001
- Spearman rho(beta, length_overhead) = -0.59, p = <0.001
- Spearman rho(beta, mean_lambda) = -0.68, p = <0.001
- Spearman rho(beta, engagement_redirection_rate_per_100) = +0.18, p = 0.048
- Spearman rho(beta, resource_seeking_rate_per_100) = +0.22, p = 0.015
- Spearman rho(beta, avg_ally_proximity) = -0.17, p = 0.063
- Spearman rho(beta, kills) = +0.16, p = 0.073
- Spearman rho(beta, deaths) = +0.20, p = 0.028

- Paired Wilcoxon beta=0.25 vs 1 (budget_adherence): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (exposure_ratio): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (length_overhead): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (mean_lambda): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (engagement_redirection_rate_per_100): r = -0.53, p = 0.011
- Paired Wilcoxon beta=0.25 vs 1 (resource_seeking_rate_per_100): r = -0.48, p = 0.026
- Paired Wilcoxon beta=0.25 vs 1 (avg_ally_proximity): r = +0.57, p = 0.006
- Paired Wilcoxon beta=0.25 vs 1 (kills): r = -0.44, p = 0.042
- Paired Wilcoxon beta=0.25 vs 1 (deaths): r = -0.51, p = 0.037

### Aggressive (fixed-weight reference: main experiment)

| beta | Adherence | ExposureRatio | LengthOverhead | lambda_E | EngRedirect | ResSeek | AllyDist | Kills | Deaths |
|---|---|---|---|---|---|---|---|---|---|
| fixed | – | – | – | 3.64 | 1.33 ± 0.19 | 0.00 ± 0.00 | 4.15 ± 0.62 | 10.10 ± 1.38 | 10.03 ± 1.38 |
| 1.00 | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 1.51 ± 0.22 | 0.00 ± 0.00 | 4.00 ± 0.59 | 11.43 ± 1.27 | 11.13 ± 1.55 |
| 0.75 | 0.830 ± 0.034 | 0.789 ± 0.026 | 1.317 ± 0.086 | 10.016 ± 1.900 | 1.13 ± 0.17 | 0.00 ± 0.00 | 4.35 ± 0.61 | 8.57 ± 1.40 | 8.57 ± 1.24 |
| 0.50 | 0.719 ± 0.046 | 0.766 ± 0.025 | 1.431 ± 0.084 | 14.463 ± 2.369 | 1.10 ± 0.15 | 0.00 ± 0.00 | 5.87 ± 0.91 | 8.30 ± 1.12 | 8.50 ± 1.19 |
| 0.25 | 0.715 ± 0.054 | 0.756 ± 0.036 | 1.448 ± 0.120 | 14.493 ± 2.701 | 0.99 ± 0.13 | 0.00 ± 0.00 | 5.86 ± 0.95 | 7.73 ± 1.10 | 7.67 ± 1.02 |

- Spearman rho(beta, budget_adherence) = +0.73, p = <0.001
- Spearman rho(beta, exposure_ratio) = +0.68, p = <0.001
- Spearman rho(beta, length_overhead) = -0.70, p = <0.001
- Spearman rho(beta, mean_lambda) = -0.69, p = <0.001
- Spearman rho(beta, engagement_redirection_rate_per_100) = +0.36, p = <0.001
- Spearman rho(beta, avg_ally_proximity) = -0.35, p = <0.001
- Spearman rho(beta, kills) = +0.40, p = <0.001
- Spearman rho(beta, deaths) = +0.35, p = <0.001

- Paired Wilcoxon beta=0.25 vs 1 (budget_adherence): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (exposure_ratio): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (length_overhead): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (mean_lambda): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (engagement_redirection_rate_per_100): r = -0.81, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (resource_seeking_rate_per_100): r = +0.00, p = 1.000
- Paired Wilcoxon beta=0.25 vs 1 (avg_ally_proximity): r = +0.63, p = 0.002
- Paired Wilcoxon beta=0.25 vs 1 (kills): r = -0.81, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (deaths): r = -0.74, p = <0.001

## Additional experiment: designer risk budgets, normalised budget (Deathmatch)


### Survival-Aware (fixed-weight reference: main experiment)

| beta | Adherence | ExposureRatio | LengthOverhead | lambda_E | BudgetPosition | EngRedirect | ResSeek | AllyDist | Kills | Deaths |
|---|---|---|---|---|---|---|---|---|---|---|
| fixed | – | – | – | 20.00 | – | 0.69 ± 0.21 | 0.41 ± 0.10 | 3.43 ± 0.50 | 4.23 ± 1.09 | 3.50 ± 0.77 |
| 1.00 | 1.000 ± 0.000 | 0.998 ± 0.002 | 1.001 ± 0.001 | 0.005 ± 0.004 | 0.996 ± 0.003 | 1.72 ± 1.45 | 0.72 ± 0.18 | 2.91 ± 0.49 | 6.60 ± 1.32 | 5.70 ± 1.34 |
| 0.75 | 1.000 ± 0.000 | 0.647 ± 0.042 | 1.115 ± 0.023 | 0.957 ± 0.170 | 0.198 ± 0.031 | 1.28 ± 0.80 | 0.73 ± 0.13 | 3.70 ± 0.59 | 6.67 ± 1.04 | 5.63 ± 0.97 |
| 0.50 | 1.000 ± 0.000 | 0.569 ± 0.037 | 1.171 ± 0.034 | 1.352 ± 0.292 | 0.110 ± 0.015 | 0.78 ± 0.17 | 0.68 ± 0.14 | 3.82 ± 0.60 | 6.40 ± 1.07 | 5.13 ± 1.05 |
| 0.25 | 1.000 ± 0.000 | 0.559 ± 0.048 | 1.242 ± 0.109 | 1.700 ± 0.395 | 0.032 ± 0.007 | 0.73 ± 0.20 | 0.58 ± 0.10 | 3.91 ± 0.62 | 5.97 ± 1.09 | 4.40 ± 0.90 |
| 0.00 | 1.000 ± 0.000 | 0.568 ± 0.063 | 1.182 ± 0.053 | 1.652 ± 0.453 | 0.000 ± 0.000 | 0.61 ± 0.17 | 0.51 ± 0.12 | 4.28 ± 0.91 | 5.17 ± 1.12 | 4.13 ± 0.96 |

- Spearman rho(beta, exposure_ratio) = +0.64, p = <0.001
- Spearman rho(beta, length_overhead) = -0.60, p = <0.001
- Spearman rho(beta, mean_lambda) = -0.61, p = <0.001
- Spearman rho(beta, budget_position) = +0.97, p = <0.001
- Spearman rho(beta, engagement_redirection_rate_per_100) = +0.21, p = 0.010
- Spearman rho(beta, resource_seeking_rate_per_100) = +0.18, p = 0.026
- Spearman rho(beta, avg_ally_proximity) = -0.18, p = 0.024
- Spearman rho(beta, kills) = +0.15, p = 0.062
- Spearman rho(beta, deaths) = +0.19, p = 0.021

- Paired Wilcoxon beta=0.00 vs 1 (budget_adherence): r = +0.00, p = 1.000
- Paired Wilcoxon beta=0.00 vs 1 (exposure_ratio): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (length_overhead): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (mean_lambda): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (budget_position): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (engagement_redirection_rate_per_100): r = -0.49, p = 0.017
- Paired Wilcoxon beta=0.00 vs 1 (resource_seeking_rate_per_100): r = -0.45, p = 0.038
- Paired Wilcoxon beta=0.00 vs 1 (avg_ally_proximity): r = +0.57, p = 0.006
- Paired Wilcoxon beta=0.00 vs 1 (kills): r = -0.41, p = 0.062
- Paired Wilcoxon beta=0.00 vs 1 (deaths): r = -0.42, p = 0.065

### Aggressive (fixed-weight reference: main experiment)

| beta | Adherence | ExposureRatio | LengthOverhead | lambda_E | BudgetPosition | EngRedirect | ResSeek | AllyDist | Kills | Deaths |
|---|---|---|---|---|---|---|---|---|---|---|
| fixed | – | – | – | 3.64 | – | 1.33 ± 0.19 | 0.00 ± 0.00 | 4.15 ± 0.62 | 10.10 ± 1.38 | 10.03 ± 1.38 |
| 1.00 | 1.000 ± 0.000 | 1.000 ± 0.001 | 1.000 ± 0.000 | 0.001 ± 0.001 | 0.999 ± 0.001 | 1.52 ± 0.22 | 0.00 ± 0.00 | 4.00 ± 0.59 | 11.43 ± 1.27 | 11.20 ± 1.57 |
| 0.75 | 1.000 ± 0.000 | 0.853 ± 0.018 | 1.137 ± 0.040 | 0.812 ± 0.178 | 0.226 ± 0.030 | 1.10 ± 0.19 | 0.00 ± 0.00 | 3.58 ± 0.62 | 8.63 ± 1.34 | 8.33 ± 1.32 |
| 0.50 | 1.000 ± 0.000 | 0.790 ± 0.028 | 1.283 ± 0.070 | 1.601 ± 0.354 | 0.101 ± 0.011 | 1.23 ± 0.16 | 0.00 ± 0.00 | 5.06 ± 0.79 | 9.10 ± 1.01 | 9.43 ± 1.07 |
| 0.25 | 1.000 ± 0.000 | 0.758 ± 0.028 | 1.395 ± 0.098 | 2.409 ± 0.537 | 0.036 ± 0.008 | 1.16 ± 0.17 | 0.00 ± 0.00 | 5.92 ± 1.26 | 8.53 ± 1.21 | 8.77 ± 1.13 |
| 0.00 | 1.000 ± 0.000 | 0.738 ± 0.040 | 1.421 ± 0.115 | 2.788 ± 0.687 | 0.000 ± 0.000 | 1.04 ± 0.13 | 0.00 ± 0.00 | 5.40 ± 0.79 | 7.87 ± 0.99 | 8.13 ± 1.03 |

- Spearman rho(beta, exposure_ratio) = +0.77, p = <0.001
- Spearman rho(beta, length_overhead) = -0.78, p = <0.001
- Spearman rho(beta, mean_lambda) = -0.77, p = <0.001
- Spearman rho(beta, budget_position) = +0.97, p = <0.001
- Spearman rho(beta, engagement_redirection_rate_per_100) = +0.24, p = 0.003
- Spearman rho(beta, avg_ally_proximity) = -0.31, p = <0.001
- Spearman rho(beta, kills) = +0.35, p = <0.001
- Spearman rho(beta, deaths) = +0.25, p = 0.002

- Paired Wilcoxon beta=0.00 vs 1 (budget_adherence): r = +0.00, p = 1.000
- Paired Wilcoxon beta=0.00 vs 1 (exposure_ratio): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (length_overhead): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (mean_lambda): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (budget_position): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (engagement_redirection_rate_per_100): r = -0.76, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (resource_seeking_rate_per_100): r = +0.00, p = 1.000
- Paired Wilcoxon beta=0.00 vs 1 (avg_ally_proximity): r = +0.62, p = 0.002
- Paired Wilcoxon beta=0.00 vs 1 (kills): r = -0.81, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (deaths): r = -0.69, p = 0.002
