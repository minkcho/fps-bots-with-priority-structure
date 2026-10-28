# Statistical summary (n = 30 episodes per condition)

Consistency checks (CRN): navigation-ablation full = main; commitment 0.45 = main MC; lambda x1 = main; lambda x0 = distance-only. **passed**

## Main experiment

| Scenario | Style | ObjCommit | AllyDist | EngRedirect | ResSeek | Kills | Deaths | Control |
|---|---|---|---|---|---|---|---|---|
| Mission | Mission–Cooperation | 0.95 ± 0.03 | 1.56 ± 0.30 | 0.01 ± 0.02 | 0.00 ± 0.00 | 3.2 ± 1.7 | 3.1 ± 1.8 |  |
| Mission | Persistent Objective | 0.82 ± 0.12 | 2.84 ± 1.43 | 0.00 ± 0.00 | 0.00 ± 0.01 | 1.9 ± 1.0 | 1.8 ± 1.1 |  |
| Mission | Aggressive | 0.16 ± 0.11 | 3.20 ± 0.80 | 0.59 ± 0.17 | 0.00 ± 0.00 | 4.8 ± 1.5 | 4.8 ± 1.5 |  |
| Mission | Survival-Aware | 0.08 ± 0.08 | 4.36 ± 0.87 | 0.29 ± 0.08 | 0.33 ± 0.09 | 3.6 ± 0.9 | 2.7 ± 0.7 |  |
| Deathmatch | Mission–Cooperation | 0.00 ± 0.00 | 2.08 ± 0.25 | 0.20 ± 0.11 | 0.21 ± 0.36 | 6.9 ± 1.8 | 5.6 ± 1.5 |  |
| Deathmatch | Persistent Objective | 0.00 ± 0.00 | 4.59 ± 0.71 | 0.05 ± 0.03 | 0.00 ± 0.00 | 7.6 ± 0.9 | 4.0 ± 0.8 |  |
| Deathmatch | Aggressive | 0.00 ± 0.00 | 4.43 ± 0.82 | 1.01 ± 0.15 | 0.00 ± 0.00 | 8.5 ± 1.5 | 8.4 ± 1.3 |  |
| Deathmatch | Survival-Aware | 0.00 ± 0.00 | 4.83 ± 0.91 | 0.38 ± 0.11 | 0.45 ± 0.12 | 4.1 ± 1.0 | 3.3 ± 0.8 |  |
| Control | Mission–Cooperation | 0.96 ± 0.02 | 1.49 ± 0.26 | 0.00 ± 0.00 | 0.00 ± 0.00 | 1.5 ± 1.1 | 1.4 ± 1.1 | 120.00 ± 0.00; wins 30/30; stalls 0; med. steps 143.0 |
| Control | Persistent Objective | 0.88 ± 0.08 | 2.57 ± 0.85 | 0.00 ± 0.01 | 0.00 ± 0.00 | 1.5 ± 0.7 | 1.5 ± 0.8 | 119.03 ± 1.98; wins 29/30; stalls 0; med. steps 143.0 |
| Control | Aggressive | 0.16 ± 0.09 | 4.33 ± 0.98 | 0.73 ± 0.16 | 0.00 ± 0.00 | 4.9 ± 1.6 | 4.9 ± 1.4 | 36.10 ± 20.33; wins 8/30; stalls 2; med. steps 252.0 |
| Control | Survival-Aware | 0.04 ± 0.05 | 4.98 ± 1.20 | 0.31 ± 0.11 | 0.36 ± 0.10 | 3.5 ± 0.9 | 2.6 ± 0.8 | 14.10 ± 13.55; wins 2/30; stalls 3; med. steps 340.0 |

## Style contrasts (Mann–Whitney U, rank-biserial r > 0: first style higher; Holm within family)

| Scenario | Metric | Style A | Style B | r | p | p (Holm) |
|---|---|---|---|---|---|---|
| Mission | ObjCommit | Mission–Cooperation | Persistent Objective | +0.15 | 0.277 | 0.353 |
| Mission | ObjCommit | Mission–Cooperation | Aggressive | +0.90 | <0.001 | <0.001 |
| Mission | ObjCommit | Mission–Cooperation | Survival-Aware | +0.98 | <0.001 | <0.001 |
| Mission | ObjCommit | Persistent Objective | Aggressive | +0.78 | <0.001 | <0.001 |
| Mission | ObjCommit | Persistent Objective | Survival-Aware | +0.87 | <0.001 | <0.001 |
| Mission | ObjCommit | Aggressive | Survival-Aware | +0.18 | 0.176 | 0.353 |
| Mission | AllyDist | Mission–Cooperation | Persistent Objective | -0.12 | 0.440 | 0.440 |
| Mission | AllyDist | Mission–Cooperation | Aggressive | -0.62 | <0.001 | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Survival-Aware | -0.83 | <0.001 | <0.001 |
| Mission | AllyDist | Persistent Objective | Aggressive | -0.43 | 0.005 | 0.014 |
| Mission | AllyDist | Persistent Objective | Survival-Aware | -0.59 | <0.001 | <0.001 |
| Mission | AllyDist | Aggressive | Survival-Aware | -0.34 | 0.024 | 0.048 |
| Deathmatch | EngRedirect | Mission–Cooperation | Persistent Objective | +0.36 | 0.009 | 0.011 |
| Deathmatch | EngRedirect | Mission–Cooperation | Aggressive | -0.89 | <0.001 | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Survival-Aware | -0.41 | 0.006 | 0.011 |
| Deathmatch | EngRedirect | Persistent Objective | Aggressive | -1.00 | <0.001 | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Survival-Aware | -0.73 | <0.001 | <0.001 |
| Deathmatch | EngRedirect | Aggressive | Survival-Aware | +0.78 | <0.001 | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Persistent Objective | +0.27 | 0.003 | 0.008 |
| Deathmatch | ResSeek | Mission–Cooperation | Aggressive | +0.27 | 0.003 | 0.008 |
| Deathmatch | ResSeek | Mission–Cooperation | Survival-Aware | -0.68 | <0.001 | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Aggressive | +0.00 | 1.000 | 1.000 |
| Deathmatch | ResSeek | Persistent Objective | Survival-Aware | -0.83 | <0.001 | <0.001 |
| Deathmatch | ResSeek | Aggressive | Survival-Aware | -0.83 | <0.001 | <0.001 |
| Deathmatch | AllyDist | Mission–Cooperation | Persistent Objective | -0.84 | <0.001 | <0.001 |
| Deathmatch | AllyDist | Mission–Cooperation | Aggressive | -0.71 | <0.001 | <0.001 |
| Deathmatch | AllyDist | Mission–Cooperation | Survival-Aware | -0.70 | <0.001 | <0.001 |
| Deathmatch | AllyDist | Persistent Objective | Aggressive | +0.03 | 0.853 | 1.000 |
| Deathmatch | AllyDist | Persistent Objective | Survival-Aware | -0.08 | 0.620 | 1.000 |
| Deathmatch | AllyDist | Aggressive | Survival-Aware | -0.11 | 0.455 | 1.000 |
| Control | CtrlScore | Mission–Cooperation | Persistent Objective | +0.03 | 0.334 | 0.334 |
| Control | CtrlScore | Mission–Cooperation | Aggressive | +0.73 | <0.001 | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Survival-Aware | +0.93 | <0.001 | <0.001 |
| Control | CtrlScore | Persistent Objective | Aggressive | +0.72 | <0.001 | <0.001 |
| Control | CtrlScore | Persistent Objective | Survival-Aware | +0.93 | <0.001 | <0.001 |
| Control | CtrlScore | Aggressive | Survival-Aware | +0.17 | 0.164 | 0.328 |
| Control | ObjCommit | Mission–Cooperation | Persistent Objective | +0.23 | 0.112 | 0.112 |
| Control | ObjCommit | Mission–Cooperation | Aggressive | +1.00 | <0.001 | <0.001 |
| Control | ObjCommit | Mission–Cooperation | Survival-Aware | +1.00 | <0.001 | <0.001 |
| Control | ObjCommit | Persistent Objective | Aggressive | +0.94 | <0.001 | <0.001 |
| Control | ObjCommit | Persistent Objective | Survival-Aware | +0.99 | <0.001 | <0.001 |
| Control | ObjCommit | Aggressive | Survival-Aware | +0.34 | 0.009 | 0.019 |
| Control | AllyDist | Mission–Cooperation | Persistent Objective | -0.22 | 0.147 | 0.294 |
| Control | AllyDist | Mission–Cooperation | Aggressive | -0.77 | <0.001 | <0.001 |
| Control | AllyDist | Mission–Cooperation | Survival-Aware | -0.84 | <0.001 | <0.001 |
| Control | AllyDist | Persistent Objective | Aggressive | -0.48 | 0.002 | 0.005 |
| Control | AllyDist | Persistent Objective | Survival-Aware | -0.55 | <0.001 | <0.001 |
| Control | AllyDist | Aggressive | Survival-Aware | -0.12 | 0.446 | 0.446 |

## Commitment sensitivity (Mission–Cooperation base)

| w_commit | Mission ObjCommit | Control score | Control wins | stalls |
|---|---|---|---|---|
| 0.00 | 0.89 ± 0.08 | 111.47 ± 10.75 | 27/30 | 1 |
| 0.20 | 0.97 ± 0.02 | 119.37 ± 1.30 | 29/30 | 0 |
| 0.45 | 0.95 ± 0.03 | 120.00 ± 0.00 | 30/30 | 0 |
| 0.65 | 0.96 ± 0.03 | 118.00 ± 3.29 | 28/30 | 0 |
| 0.85 | 0.96 ± 0.02 | 120.00 ± 0.00 | 30/30 | 0 |
| 1.05 | 0.96 ± 0.03 | 120.00 ± 0.00 | 30/30 | 0 |
| 1.25 | 0.96 ± 0.03 | 120.00 ± 0.00 | 30/30 | 0 |

Paired Wilcoxon, w=0.45 vs w=0 (Mission, ObjCommit): r = +0.56, p = 0.007

Paired Wilcoxon, w=0.45 vs w=0 (Control, CtrlScore): r = +1.00, p = 0.250

## Navigation ablation (full vs distance-only; paired Wilcoxon, r > 0: full higher)

| Condition | Metric | Full | Distance-only | r | p |
|---|---|---|---|---|---|
| Mission/Mission–Cooperation | AllyDist | 1.56 ± 0.30 | 1.47 ± 0.30 | +0.23 | 0.313 |
| Mission/Mission–Cooperation | ObjCommit | 0.95 ± 0.03 | 0.97 ± 0.02 | -0.46 | 0.176 |
| Mission/Mission–Cooperation | EngRedirect | 0.01 ± 0.02 | 0.00 ± 0.00 | +1.00 | 0.500 |
| Mission/Mission–Cooperation | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Mission/Mission–Cooperation | Kills | 3.17 ± 1.73 | 3.07 ± 1.70 | +0.10 | 0.774 |
| Mission/Mission–Cooperation | Deaths | 3.07 ± 1.77 | 2.77 ± 1.56 | +0.12 | 0.746 |
| Deathmatch/Survival-Aware | AllyDist | 4.83 ± 0.91 | 4.23 ± 0.69 | +0.23 | 0.280 |
| Deathmatch/Survival-Aware | ObjCommit | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Deathmatch/Survival-Aware | EngRedirect | 0.38 ± 0.11 | 0.67 ± 0.17 | -0.54 | 0.009 |
| Deathmatch/Survival-Aware | ResSeek | 0.45 ± 0.12 | 0.79 ± 0.15 | -0.69 | <0.001 |
| Deathmatch/Survival-Aware | Kills | 4.13 ± 1.00 | 7.50 ± 1.27 | -0.85 | <0.001 |
| Deathmatch/Survival-Aware | Deaths | 3.33 ± 0.83 | 6.20 ± 1.07 | -0.80 | <0.001 |

## Combat-mode ablation (full vs weights-only; paired Wilcoxon, r > 0: full higher)

| Scenario | Style | Metric | Full | Weights-only | r | p |
|---|---|---|---|---|---|---|
| Mission | Mission–Cooperation | ObjCommit | 0.95 ± 0.03 | 0.96 ± 0.03 | -0.21 | 0.569 |
| Mission | Mission–Cooperation | AllyDist | 1.56 ± 0.30 | 1.65 ± 0.40 | -0.12 | 0.715 |
| Mission | Mission–Cooperation | EngRedirect | 0.01 ± 0.02 | 0.01 ± 0.01 | +0.20 | 0.875 |
| Mission | Mission–Cooperation | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Mission | Persistent Objective | ObjCommit | 0.82 ± 0.12 | 0.82 ± 0.12 | +0.00 | 1.000 |
| Mission | Persistent Objective | AllyDist | 2.84 ± 1.43 | 2.84 ± 1.43 | +0.00 | 1.000 |
| Mission | Persistent Objective | EngRedirect | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Mission | Persistent Objective | ResSeek | 0.00 ± 0.01 | 0.00 ± 0.01 | +0.00 | 1.000 |
| Mission | Aggressive | ObjCommit | 0.16 ± 0.11 | 0.25 ± 0.13 | -0.47 | 0.105 |
| Mission | Aggressive | AllyDist | 3.20 ± 0.80 | 3.56 ± 0.79 | -0.17 | 0.452 |
| Mission | Aggressive | EngRedirect | 0.59 ± 0.17 | 0.31 ± 0.10 | +0.69 | 0.002 |
| Mission | Aggressive | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.01 | -1.00 | 1.000 |
| Mission | Survival-Aware | ObjCommit | 0.08 ± 0.08 | 0.05 ± 0.06 | +0.21 | 0.569 |
| Mission | Survival-Aware | AllyDist | 4.36 ± 0.87 | 4.69 ± 0.88 | -0.15 | 0.495 |
| Mission | Survival-Aware | EngRedirect | 0.29 ± 0.08 | 0.22 ± 0.05 | +0.17 | 0.425 |
| Mission | Survival-Aware | ResSeek | 0.33 ± 0.09 | 0.02 ± 0.02 | +0.99 | <0.001 |
| Deathmatch | Mission–Cooperation | EngRedirect | 0.20 ± 0.11 | 0.26 ± 0.09 | -0.31 | 0.141 |
| Deathmatch | Mission–Cooperation | ResSeek | 0.21 ± 0.36 | 0.10 ± 0.05 | -0.20 | 0.444 |
| Deathmatch | Mission–Cooperation | AllyDist | 2.08 ± 0.25 | 2.31 ± 0.21 | -0.20 | 0.349 |
| Deathmatch | Persistent Objective | EngRedirect | 0.05 ± 0.03 | 0.05 ± 0.03 | +0.00 | 1.000 |
| Deathmatch | Persistent Objective | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Deathmatch | Persistent Objective | AllyDist | 4.59 ± 0.71 | 4.59 ± 0.71 | +0.00 | 1.000 |
| Deathmatch | Aggressive | EngRedirect | 1.01 ± 0.15 | 0.52 ± 0.10 | +0.81 | <0.001 |
| Deathmatch | Aggressive | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Deathmatch | Aggressive | AllyDist | 4.43 ± 0.82 | 4.72 ± 0.81 | -0.12 | 0.579 |
| Deathmatch | Survival-Aware | EngRedirect | 0.38 ± 0.11 | 0.33 ± 0.07 | +0.11 | 0.612 |
| Deathmatch | Survival-Aware | ResSeek | 0.45 ± 0.12 | 0.04 ± 0.03 | +0.98 | <0.001 |
| Deathmatch | Survival-Aware | AllyDist | 4.83 ± 0.91 | 5.60 ± 0.88 | -0.23 | 0.289 |
| Control | Mission–Cooperation | CtrlScore | 120.00 ± 0.00 | 120.00 ± 0.00 | +0.00 | 1.000 |
| Control | Mission–Cooperation | ObjCommit | 0.96 ± 0.02 | 0.96 ± 0.02 | +0.06 | 0.945 |
| Control | Mission–Cooperation | EngRedirect | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Control | Mission–Cooperation | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Control | Persistent Objective | CtrlScore | 119.03 ± 1.98 | 119.03 ± 1.98 | +0.00 | 1.000 |
| Control | Persistent Objective | ObjCommit | 0.88 ± 0.08 | 0.88 ± 0.08 | +0.00 | 1.000 |
| Control | Persistent Objective | EngRedirect | 0.00 ± 0.01 | 0.00 ± 0.01 | +0.00 | 1.000 |
| Control | Persistent Objective | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Control | Aggressive | CtrlScore | 36.10 ± 20.33 | 29.90 ± 18.68 | +0.27 | 0.446 |
| Control | Aggressive | ObjCommit | 0.16 ± 0.09 | 0.14 ± 0.08 | +0.16 | 0.546 |
| Control | Aggressive | EngRedirect | 0.73 ± 0.16 | 0.47 ± 0.14 | +0.51 | 0.020 |
| Control | Aggressive | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Control | Survival-Aware | CtrlScore | 14.10 ± 13.55 | 8.80 ± 11.36 | +0.16 | 0.707 |
| Control | Survival-Aware | ObjCommit | 0.04 ± 0.05 | 0.01 ± 0.02 | +0.20 | 0.652 |
| Control | Survival-Aware | EngRedirect | 0.31 ± 0.11 | 0.21 ± 0.07 | +0.26 | 0.239 |
| Control | Survival-Aware | ResSeek | 0.36 ± 0.10 | 0.02 ± 0.02 | +0.99 | <0.001 |

Weights-only Control outcomes: Mission–Cooperation: 30/30 wins; Persistent Objective: 29/30 wins; Aggressive: 6/30 wins; Survival-Aware: 2/30 wins

## Style interpolation (mode fixed to keep moving; Spearman rho between alpha and metric)


### Deathmatch: Aggressive -> Survival-Aware

| alpha | EngRedirect | ResSeek | AllyDist | Kills | Deaths |
|---|---|---|---|---|---|
| 0.00 | 0.52 ± 0.10 | 0.00 ± 0.00 | 4.72 ± 0.81 | 6.67 ± 1.36 | 6.00 ± 1.22 |
| 0.25 | 0.49 ± 0.09 | 0.00 ± 0.01 | 5.47 ± 0.84 | 6.40 ± 1.04 | 5.53 ± 1.05 |
| 0.50 | 0.41 ± 0.09 | 0.01 ± 0.01 | 5.74 ± 0.81 | 6.10 ± 1.05 | 5.57 ± 0.96 |
| 0.75 | 0.35 ± 0.08 | 0.03 ± 0.02 | 6.53 ± 0.99 | 5.73 ± 1.19 | 4.73 ± 0.91 |
| 1.00 | 0.33 ± 0.07 | 0.04 ± 0.03 | 5.60 ± 0.88 | 5.63 ± 1.10 | 4.47 ± 0.80 |

- Spearman rho(alpha, EngRedirect) = -0.27, p = 0.001
- Spearman rho(alpha, ResSeek) = +0.36, p = <0.001
- Spearman rho(alpha, AllyDist) = +0.17, p = 0.038
- Spearman rho(alpha, Kills) = -0.12, p = 0.141
- Spearman rho(alpha, Deaths) = -0.19, p = 0.022

### Mission: Mission–Cooperation -> Persistent Objective

| alpha | ObjCommit | AllyDist | EngRedirect | Kills | Deaths |
|---|---|---|---|---|---|
| 0.00 | 0.96 ± 0.03 | 1.65 ± 0.40 | 0.01 ± 0.01 | 3.10 ± 1.76 | 2.90 ± 1.81 |
| 0.25 | 0.96 ± 0.02 | 1.60 ± 0.42 | 0.00 ± 0.01 | 2.17 ± 1.33 | 2.10 ± 1.38 |
| 0.50 | 0.96 ± 0.02 | 1.60 ± 0.39 | 0.00 ± 0.00 | 2.20 ± 1.25 | 2.17 ± 1.37 |
| 0.75 | 0.95 ± 0.03 | 1.74 ± 0.47 | 0.00 ± 0.00 | 2.33 ± 1.33 | 2.27 ± 1.40 |
| 1.00 | 0.82 ± 0.12 | 2.84 ± 1.43 | 0.00 ± 0.00 | 1.93 ± 0.98 | 1.77 ± 1.09 |

- Spearman rho(alpha, ObjCommit) = -0.11, p = 0.181
- Spearman rho(alpha, AllyDist) = +0.09, p = 0.288
- Spearman rho(alpha, EngRedirect) = -0.17, p = 0.039
- Spearman rho(alpha, Kills) = +0.01, p = 0.947
- Spearman rho(alpha, Deaths) = -0.01, p = 0.859

## Navigation-weight scale (lambda x k; Spearman rho between k and metric)


### Mission / Mission–Cooperation

| scale | AllyDist | ObjCommit | EngRedirect | ResSeek | Kills | Deaths |
|---|---|---|---|---|---|---|
| x0 | 1.47 ± 0.30 | 0.97 ± 0.02 | 0.00 ± 0.00 | 0.00 ± 0.00 | 3.07 ± 1.70 | 2.77 ± 1.56 |
| x0.25 | 1.46 ± 0.25 | 0.97 ± 0.02 | 0.00 ± 0.01 | 0.00 ± 0.00 | 3.43 ± 1.85 | 2.73 ± 1.44 |
| x0.5 | 1.70 ± 0.41 | 0.94 ± 0.05 | 0.01 ± 0.02 | 0.00 ± 0.00 | 3.53 ± 1.95 | 3.07 ± 1.64 |
| x1 | 1.56 ± 0.30 | 0.95 ± 0.03 | 0.01 ± 0.02 | 0.00 ± 0.00 | 3.17 ± 1.73 | 3.07 ± 1.77 |
| x2 | 1.53 ± 0.28 | 0.96 ± 0.02 | 0.01 ± 0.02 | 0.00 ± 0.00 | 2.83 ± 1.55 | 2.83 ± 1.62 |

- Spearman rho(scale, AllyDist) = -0.01, p = 0.937
- Spearman rho(scale, ObjCommit) = -0.03, p = 0.751
- Spearman rho(scale, EngRedirect) = +0.11, p = 0.166
- Spearman rho(scale, Kills) = -0.01, p = 0.886
- Spearman rho(scale, Deaths) = -0.01, p = 0.939

### Deathmatch / Survival-Aware

| scale | AllyDist | ObjCommit | EngRedirect | ResSeek | Kills | Deaths |
|---|---|---|---|---|---|---|
| x0 | 4.23 ± 0.69 | 0.00 ± 0.00 | 0.67 ± 0.17 | 0.79 ± 0.15 | 7.50 ± 1.27 | 6.20 ± 1.07 |
| x0.25 | 4.23 ± 0.82 | 0.00 ± 0.00 | 0.57 ± 0.17 | 0.52 ± 0.12 | 5.37 ± 1.18 | 4.03 ± 0.93 |
| x0.5 | 3.95 ± 0.65 | 0.00 ± 0.00 | 0.45 ± 0.15 | 0.42 ± 0.13 | 3.93 ± 1.10 | 3.13 ± 0.92 |
| x1 | 4.83 ± 0.91 | 0.00 ± 0.00 | 0.38 ± 0.11 | 0.45 ± 0.12 | 4.13 ± 1.00 | 3.33 ± 0.83 |
| x2 | 4.66 ± 0.80 | 0.00 ± 0.00 | 0.41 ± 0.13 | 0.40 ± 0.10 | 3.80 ± 0.92 | 2.97 ± 0.76 |

- Spearman rho(scale, AllyDist) = +0.10, p = 0.234
- Spearman rho(scale, EngRedirect) = -0.24, p = 0.003
- Spearman rho(scale, ResSeek) = -0.33, p = <0.001
- Spearman rho(scale, Kills) = -0.36, p = <0.001
- Spearman rho(scale, Deaths) = -0.36, p = <0.001

## Additional experiment: designer risk budgets, relative budget (Deathmatch)


### Survival-Aware (fixed-weight reference: main experiment)

| beta | Adherence | ExposureRatio | LengthOverhead | lambda_E | EngRedirect | ResSeek | AllyDist | Kills | Deaths |
|---|---|---|---|---|---|---|---|---|---|
| fixed | – | – | – | 20.00 | 0.38 ± 0.11 | 0.45 ± 0.12 | 4.83 ± 0.91 | 4.13 ± 1.00 | 3.33 ± 0.83 |
| 1.00 | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 2.35 ± 2.89 | 0.77 ± 0.16 | 3.58 ± 0.65 | 7.53 ± 1.37 | 6.23 ± 0.96 |
| 0.75 | 0.913 ± 0.029 | 0.587 ± 0.041 | 1.122 ± 0.033 | 5.063 ± 1.528 | 0.49 ± 0.16 | 0.49 ± 0.13 | 4.46 ± 0.80 | 4.70 ± 1.10 | 3.70 ± 0.97 |
| 0.50 | 0.867 ± 0.043 | 0.559 ± 0.052 | 1.165 ± 0.035 | 7.184 ± 2.168 | 0.54 ± 0.13 | 0.50 ± 0.12 | 4.08 ± 0.65 | 5.17 ± 1.18 | 3.63 ± 0.96 |
| 0.25 | 0.828 ± 0.045 | 0.538 ± 0.064 | 1.159 ± 0.036 | 9.087 ± 2.287 | 0.48 ± 0.14 | 0.46 ± 0.11 | 4.60 ± 0.72 | 4.57 ± 1.04 | 3.27 ± 0.73 |

- Spearman rho(beta, budget_adherence) = +0.72, p = <0.001
- Spearman rho(beta, exposure_ratio) = +0.66, p = <0.001
- Spearman rho(beta, length_overhead) = -0.66, p = <0.001
- Spearman rho(beta, mean_lambda) = -0.72, p = <0.001
- Spearman rho(beta, engagement_redirection_rate_per_100) = +0.26, p = 0.005
- Spearman rho(beta, resource_seeking_rate_per_100) = +0.25, p = 0.006
- Spearman rho(beta, avg_ally_proximity) = -0.17, p = 0.057
- Spearman rho(beta, kills) = +0.26, p = 0.005
- Spearman rho(beta, deaths) = +0.35, p = <0.001

- Paired Wilcoxon beta=0.25 vs 1 (budget_adherence): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (exposure_ratio): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (length_overhead): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (mean_lambda): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (engagement_redirection_rate_per_100): r = -0.64, p = 0.001
- Paired Wilcoxon beta=0.25 vs 1 (resource_seeking_rate_per_100): r = -0.62, p = 0.004
- Paired Wilcoxon beta=0.25 vs 1 (avg_ally_proximity): r = +0.45, p = 0.033
- Paired Wilcoxon beta=0.25 vs 1 (kills): r = -0.64, p = 0.004
- Paired Wilcoxon beta=0.25 vs 1 (deaths): r = -0.78, p = <0.001

### Aggressive (fixed-weight reference: main experiment)

| beta | Adherence | ExposureRatio | LengthOverhead | lambda_E | EngRedirect | ResSeek | AllyDist | Kills | Deaths |
|---|---|---|---|---|---|---|---|---|---|
| fixed | – | – | – | 3.64 | 1.01 ± 0.15 | 0.00 ± 0.00 | 4.43 ± 0.82 | 8.53 ± 1.46 | 8.37 ± 1.34 |
| 1.00 | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 1.28 ± 0.18 | 0.00 ± 0.00 | 4.00 ± 0.81 | 10.13 ± 1.29 | 9.87 ± 1.34 |
| 0.75 | 0.854 ± 0.034 | 0.815 ± 0.022 | 1.388 ± 0.137 | 8.351 ± 1.688 | 0.83 ± 0.14 | 0.00 ± 0.00 | 6.17 ± 1.14 | 6.10 ± 1.21 | 6.77 ± 1.39 |
| 0.50 | 0.740 ± 0.071 | 0.770 ± 0.062 | 1.366 ± 0.090 | 13.245 ± 3.575 | 0.81 ± 0.14 | 0.00 ± 0.00 | 5.43 ± 1.02 | 6.63 ± 1.24 | 7.10 ± 1.34 |
| 0.25 | 0.737 ± 0.082 | 0.762 ± 0.058 | 1.377 ± 0.109 | 13.230 ± 4.121 | 0.74 ± 0.12 | 0.00 ± 0.00 | 5.73 ± 1.10 | 5.63 ± 0.97 | 6.40 ± 1.03 |

- Spearman rho(beta, budget_adherence) = +0.69, p = <0.001
- Spearman rho(beta, exposure_ratio) = +0.67, p = <0.001
- Spearman rho(beta, length_overhead) = -0.58, p = <0.001
- Spearman rho(beta, mean_lambda) = -0.66, p = <0.001
- Spearman rho(beta, engagement_redirection_rate_per_100) = +0.37, p = <0.001
- Spearman rho(beta, avg_ally_proximity) = -0.20, p = 0.026
- Spearman rho(beta, kills) = +0.39, p = <0.001
- Spearman rho(beta, deaths) = +0.29, p = 0.001

- Paired Wilcoxon beta=0.25 vs 1 (budget_adherence): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (exposure_ratio): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (length_overhead): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (mean_lambda): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (engagement_redirection_rate_per_100): r = -0.75, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (resource_seeking_rate_per_100): r = +0.00, p = 1.000
- Paired Wilcoxon beta=0.25 vs 1 (avg_ally_proximity): r = +0.47, p = 0.023
- Paired Wilcoxon beta=0.25 vs 1 (kills): r = -0.87, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (deaths): r = -0.69, p = 0.001

## Additional experiment: designer risk budgets, normalised budget (Deathmatch)


### Survival-Aware (fixed-weight reference: main experiment)

| beta | Adherence | ExposureRatio | LengthOverhead | lambda_E | BudgetPosition | EngRedirect | ResSeek | AllyDist | Kills | Deaths |
|---|---|---|---|---|---|---|---|---|---|---|
| fixed | – | – | – | 20.00 | – | 0.38 ± 0.11 | 0.45 ± 0.12 | 4.83 ± 0.91 | 4.13 ± 1.00 | 3.33 ± 0.83 |
| 1.00 | 1.000 ± 0.000 | 0.999 ± 0.001 | 1.000 ± 0.000 | 0.001 ± 0.001 | 0.997 ± 0.002 | 2.37 ± 2.89 | 0.78 ± 0.15 | 3.66 ± 0.65 | 7.90 ± 1.36 | 6.30 ± 0.92 |
| 0.75 | 1.000 ± 0.000 | 0.637 ± 0.046 | 1.192 ± 0.175 | 1.453 ± 1.130 | 0.174 ± 0.038 | 0.54 ± 0.18 | 0.56 ± 0.16 | 3.90 ± 0.68 | 5.30 ± 1.10 | 4.37 ± 1.16 |
| 0.50 | 1.000 ± 0.000 | 0.571 ± 0.047 | 1.218 ± 0.173 | 1.510 ± 1.109 | 0.081 ± 0.013 | 0.56 ± 0.18 | 0.59 ± 0.16 | 4.63 ± 0.82 | 5.23 ± 1.08 | 4.57 ± 1.09 |
| 0.25 | 1.000 ± 0.000 | 0.515 ± 0.065 | 1.156 ± 0.031 | 1.524 ± 0.504 | 0.028 ± 0.011 | 0.50 ± 0.13 | 0.45 ± 0.12 | 4.18 ± 0.69 | 4.77 ± 1.06 | 3.20 ± 0.75 |
| 0.00 | 1.000 ± 0.000 | 0.461 ± 0.059 | 1.142 ± 0.037 | 1.403 ± 0.384 | 0.000 ± 0.000 | 0.39 ± 0.12 | 0.39 ± 0.11 | 4.05 ± 0.65 | 4.10 ± 1.04 | 2.83 ± 0.79 |

- Spearman rho(beta, exposure_ratio) = +0.73, p = <0.001
- Spearman rho(beta, length_overhead) = -0.56, p = <0.001
- Spearman rho(beta, mean_lambda) = -0.59, p = <0.001
- Spearman rho(beta, budget_position) = +0.95, p = <0.001
- Spearman rho(beta, engagement_redirection_rate_per_100) = +0.32, p = <0.001
- Spearman rho(beta, resource_seeking_rate_per_100) = +0.31, p = <0.001
- Spearman rho(beta, avg_ally_proximity) = -0.11, p = 0.178
- Spearman rho(beta, kills) = +0.33, p = <0.001
- Spearman rho(beta, deaths) = +0.41, p = <0.001

- Paired Wilcoxon beta=0.00 vs 1 (budget_adherence): r = +0.00, p = 1.000
- Paired Wilcoxon beta=0.00 vs 1 (exposure_ratio): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (length_overhead): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (mean_lambda): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (budget_position): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (engagement_redirection_rate_per_100): r = -0.85, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (resource_seeking_rate_per_100): r = -0.75, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (avg_ally_proximity): r = +0.26, p = 0.213
- Paired Wilcoxon beta=0.00 vs 1 (kills): r = -0.78, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (deaths): r = -0.86, p = <0.001

### Aggressive (fixed-weight reference: main experiment)

| beta | Adherence | ExposureRatio | LengthOverhead | lambda_E | BudgetPosition | EngRedirect | ResSeek | AllyDist | Kills | Deaths |
|---|---|---|---|---|---|---|---|---|---|---|
| fixed | – | – | – | 3.64 | – | 1.01 ± 0.15 | 0.00 ± 0.00 | 4.43 ± 0.82 | 8.53 ± 1.46 | 8.37 ± 1.34 |
| 1.00 | 1.000 ± 0.000 | 1.000 ± 0.001 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.999 ± 0.002 | 1.29 ± 0.19 | 0.00 ± 0.00 | 4.05 ± 0.82 | 10.23 ± 1.31 | 9.97 ± 1.37 |
| 0.75 | 1.000 ± 0.000 | 0.820 ± 0.037 | 1.274 ± 0.081 | 1.530 ± 0.539 | 0.221 ± 0.038 | 0.98 ± 0.17 | 0.00 ± 0.00 | 4.79 ± 0.81 | 7.50 ± 1.35 | 7.63 ± 1.28 |
| 0.50 | 1.000 ± 0.000 | 0.788 ± 0.060 | 1.284 ± 0.084 | 1.385 ± 0.453 | 0.093 ± 0.016 | 0.79 ± 0.12 | 0.00 ± 0.00 | 4.98 ± 0.79 | 6.50 ± 1.21 | 6.57 ± 1.14 |
| 0.25 | 1.000 ± 0.000 | 0.801 ± 0.032 | 1.322 ± 0.072 | 1.618 ± 0.391 | 0.031 ± 0.005 | 0.84 ± 0.14 | 0.00 ± 0.00 | 5.51 ± 0.96 | 6.67 ± 1.37 | 6.73 ± 1.10 |
| 0.00 | 1.000 ± 0.000 | 0.769 ± 0.056 | 1.405 ± 0.107 | 2.951 ± 1.448 | 0.000 ± 0.000 | 0.73 ± 0.12 | 0.00 ± 0.00 | 6.35 ± 1.28 | 5.77 ± 0.98 | 6.30 ± 1.13 |

- Spearman rho(beta, exposure_ratio) = +0.62, p = <0.001
- Spearman rho(beta, length_overhead) = -0.60, p = <0.001
- Spearman rho(beta, mean_lambda) = -0.59, p = <0.001
- Spearman rho(beta, budget_position) = +0.96, p = <0.001
- Spearman rho(beta, engagement_redirection_rate_per_100) = +0.37, p = <0.001
- Spearman rho(beta, avg_ally_proximity) = -0.28, p = <0.001
- Spearman rho(beta, kills) = +0.37, p = <0.001
- Spearman rho(beta, deaths) = +0.31, p = <0.001

- Paired Wilcoxon beta=0.00 vs 1 (budget_adherence): r = +0.00, p = 1.000
- Paired Wilcoxon beta=0.00 vs 1 (exposure_ratio): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (length_overhead): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (mean_lambda): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (budget_position): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (engagement_redirection_rate_per_100): r = -0.82, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (resource_seeking_rate_per_100): r = +0.00, p = 1.000
- Paired Wilcoxon beta=0.00 vs 1 (avg_ally_proximity): r = +0.54, p = 0.009
- Paired Wilcoxon beta=0.00 vs 1 (kills): r = -0.87, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (deaths): r = -0.74, p = <0.001
