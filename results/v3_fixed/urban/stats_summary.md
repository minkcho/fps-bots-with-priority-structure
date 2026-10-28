# Statistical summary (n = 100 episodes per condition)

Consistency checks (CRN): navigation-ablation full = main; commitment 0.45 = main MC; lambda x1 = main; lambda x0 = distance-only. **passed**

## Main experiment

| Scenario | Style | ObjCommit | AllyDist | EngRedirect | ResSeek | Kills | Deaths | Control |
|---|---|---|---|---|---|---|---|---|
| Mission | Mission–Cooperation | 0.94 ± 0.01 | 1.77 ± 0.18 | 0.02 ± 0.01 | 0.00 ± 0.00 | 5.0 ± 0.9 | 4.2 ± 0.9 |  |
| Mission | Persistent Objective | 0.87 ± 0.04 | 3.00 ± 0.41 | 0.00 ± 0.00 | 0.00 ± 0.00 | 5.2 ± 0.9 | 5.2 ± 1.0 |  |
| Mission | Aggressive | 0.32 ± 0.06 | 4.48 ± 0.41 | 1.69 ± 0.20 | 0.17 ± 0.04 | 7.2 ± 0.9 | 7.3 ± 0.9 |  |
| Mission | Survival-Aware | 0.04 ± 0.03 | 6.89 ± 0.71 | 0.00 ± 0.00 | 0.38 ± 0.06 | 3.3 ± 0.4 | 2.9 ± 0.5 |  |
| Deathmatch | Mission–Cooperation | 0.00 ± 0.00 | 2.69 ± 0.09 | 0.46 ± 0.05 | 0.24 ± 0.05 | 10.2 ± 0.6 | 9.1 ± 0.6 |  |
| Deathmatch | Persistent Objective | 0.00 ± 0.00 | 5.61 ± 0.26 | 0.09 ± 0.02 | 0.02 ± 0.01 | 7.8 ± 0.5 | 5.7 ± 0.4 |  |
| Deathmatch | Aggressive | 0.00 ± 0.00 | 4.73 ± 0.20 | 2.86 ± 0.13 | 0.35 ± 0.04 | 11.8 ± 0.5 | 11.4 ± 0.5 |  |
| Deathmatch | Survival-Aware | 0.00 ± 0.00 | 7.42 ± 0.57 | 0.00 ± 0.00 | 0.61 ± 0.06 | 4.7 ± 0.5 | 4.7 ± 0.5 |  |
| Control | Mission–Cooperation | 0.95 ± 0.01 | 1.84 ± 0.24 | 0.00 ± 0.01 | 0.00 ± 0.00 | 2.2 ± 0.5 | 1.8 ± 0.5 | 117.30 ± 2.64; wins 94/100; stalls 0; med. steps 143.0 |
| Control | Persistent Objective | 0.91 ± 0.03 | 2.79 ± 0.54 | 0.01 ± 0.01 | 0.00 ± 0.00 | 2.0 ± 0.4 | 1.5 ± 0.5 | 116.86 ± 3.49; wins 96/100; stalls 0; med. steps 143.0 |
| Control | Aggressive | 0.29 ± 0.05 | 4.69 ± 0.36 | 2.00 ± 0.18 | 0.18 ± 0.04 | 6.1 ± 0.8 | 6.1 ± 0.8 | 73.61 ± 10.43; wins 48/100; stalls 2; med. steps 304.0 |
| Control | Survival-Aware | 0.02 ± 0.02 | 6.71 ± 0.67 | 0.00 ± 0.00 | 0.43 ± 0.06 | 2.9 ± 0.4 | 2.6 ± 0.4 | 7.94 ± 5.10; wins 4/100; stalls 7; med. steps 263.0 |

## Style contrasts (Mann–Whitney U, rank-biserial r > 0: first style higher; Holm within family)

| Scenario | Metric | Style A | Style B | r | p | p (Holm) |
|---|---|---|---|---|---|---|
| Mission | ObjCommit | Mission–Cooperation | Persistent Objective | +0.22 | 0.006 | 0.006 |
| Mission | ObjCommit | Mission–Cooperation | Aggressive | +0.90 | <0.001 | <0.001 |
| Mission | ObjCommit | Mission–Cooperation | Survival-Aware | +0.99 | <0.001 | <0.001 |
| Mission | ObjCommit | Persistent Objective | Aggressive | +0.83 | <0.001 | <0.001 |
| Mission | ObjCommit | Persistent Objective | Survival-Aware | +0.97 | <0.001 | <0.001 |
| Mission | ObjCommit | Aggressive | Survival-Aware | +0.76 | <0.001 | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Persistent Objective | -0.32 | <0.001 | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Aggressive | -0.78 | <0.001 | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Survival-Aware | -0.92 | <0.001 | <0.001 |
| Mission | AllyDist | Persistent Objective | Aggressive | -0.42 | <0.001 | <0.001 |
| Mission | AllyDist | Persistent Objective | Survival-Aware | -0.70 | <0.001 | <0.001 |
| Mission | AllyDist | Aggressive | Survival-Aware | -0.44 | <0.001 | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Persistent Objective | +0.84 | <0.001 | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Aggressive | -1.00 | <0.001 | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Survival-Aware | +0.96 | <0.001 | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Aggressive | -1.00 | <0.001 | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Survival-Aware | +0.55 | <0.001 | <0.001 |
| Deathmatch | EngRedirect | Aggressive | Survival-Aware | +1.00 | <0.001 | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Persistent Objective | +0.70 | <0.001 | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Aggressive | -0.37 | <0.001 | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Survival-Aware | -0.66 | <0.001 | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Aggressive | -0.93 | <0.001 | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Survival-Aware | -0.93 | <0.001 | <0.001 |
| Deathmatch | ResSeek | Aggressive | Survival-Aware | -0.52 | <0.001 | <0.001 |
| Deathmatch | AllyDist | Mission–Cooperation | Persistent Objective | -0.95 | <0.001 | <0.001 |
| Deathmatch | AllyDist | Mission–Cooperation | Aggressive | -0.94 | <0.001 | <0.001 |
| Deathmatch | AllyDist | Mission–Cooperation | Survival-Aware | -0.86 | <0.001 | <0.001 |
| Deathmatch | AllyDist | Persistent Objective | Aggressive | +0.43 | <0.001 | <0.001 |
| Deathmatch | AllyDist | Persistent Objective | Survival-Aware | -0.45 | <0.001 | <0.001 |
| Deathmatch | AllyDist | Aggressive | Survival-Aware | -0.68 | <0.001 | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Persistent Objective | -0.02 | 0.545 | 0.545 |
| Control | CtrlScore | Mission–Cooperation | Aggressive | +0.48 | <0.001 | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Survival-Aware | +0.96 | <0.001 | <0.001 |
| Control | CtrlScore | Persistent Objective | Aggressive | +0.48 | <0.001 | <0.001 |
| Control | CtrlScore | Persistent Objective | Survival-Aware | +0.94 | <0.001 | <0.001 |
| Control | CtrlScore | Aggressive | Survival-Aware | +0.65 | <0.001 | <0.001 |
| Control | ObjCommit | Mission–Cooperation | Persistent Objective | +0.14 | 0.089 | 0.089 |
| Control | ObjCommit | Mission–Cooperation | Aggressive | +0.96 | <0.001 | <0.001 |
| Control | ObjCommit | Mission–Cooperation | Survival-Aware | +1.00 | <0.001 | <0.001 |
| Control | ObjCommit | Persistent Objective | Aggressive | +0.92 | <0.001 | <0.001 |
| Control | ObjCommit | Persistent Objective | Survival-Aware | +0.99 | <0.001 | <0.001 |
| Control | ObjCommit | Aggressive | Survival-Aware | +0.79 | <0.001 | <0.001 |
| Control | AllyDist | Mission–Cooperation | Persistent Objective | -0.18 | 0.024 | 0.024 |
| Control | AllyDist | Mission–Cooperation | Aggressive | -0.84 | <0.001 | <0.001 |
| Control | AllyDist | Mission–Cooperation | Survival-Aware | -0.86 | <0.001 | <0.001 |
| Control | AllyDist | Persistent Objective | Aggressive | -0.60 | <0.001 | <0.001 |
| Control | AllyDist | Persistent Objective | Survival-Aware | -0.70 | <0.001 | <0.001 |
| Control | AllyDist | Aggressive | Survival-Aware | -0.38 | <0.001 | <0.001 |

## Commitment sensitivity (Mission–Cooperation base)

| w_commit | Mission ObjCommit | Control score | Control wins | stalls |
|---|---|---|---|---|
| 0.00 | 0.81 ± 0.04 | 93.12 ± 9.11 | 70/100 | 6 |
| 0.20 | 0.92 ± 0.02 | 114.34 ± 4.21 | 89/100 | 0 |
| 0.45 | 0.94 ± 0.01 | 117.30 ± 2.64 | 94/100 | 0 |
| 0.65 | 0.93 ± 0.01 | 115.68 ± 3.81 | 94/100 | 0 |
| 0.85 | 0.93 ± 0.01 | 115.01 ± 3.59 | 90/100 | 0 |
| 1.05 | 0.93 ± 0.02 | 117.44 ± 2.90 | 95/100 | 0 |
| 1.25 | 0.93 ± 0.02 | 117.44 ± 2.90 | 95/100 | 0 |

Paired Wilcoxon, w=0.45 vs w=0 (Mission, ObjCommit): r = +0.83, p = <0.001

Paired Wilcoxon, w=0.45 vs w=0 (Control, CtrlScore): r = +0.96, p = <0.001

## Navigation ablation (full vs distance-only; paired Wilcoxon, r > 0: full higher)

| Condition | Metric | Full | Distance-only | r | p |
|---|---|---|---|---|---|
| Mission/Mission–Cooperation | AllyDist | 1.77 ± 0.18 | 1.89 ± 0.22 | -0.10 | 0.416 |
| Mission/Mission–Cooperation | ObjCommit | 0.94 ± 0.01 | 0.94 ± 0.01 | -0.06 | 0.650 |
| Mission/Mission–Cooperation | EngRedirect | 0.02 ± 0.01 | 0.02 ± 0.01 | +0.03 | 0.913 |
| Mission/Mission–Cooperation | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | -1.00 | 1.000 |
| Mission/Mission–Cooperation | Kills | 5.03 ± 0.94 | 5.65 ± 1.07 | -0.32 | 0.033 |
| Mission/Mission–Cooperation | Deaths | 4.22 ± 0.89 | 4.80 ± 1.02 | -0.28 | 0.050 |
| Deathmatch/Survival-Aware | AllyDist | 7.42 ± 0.57 | 6.67 ± 0.69 | +0.25 | 0.032 |
| Deathmatch/Survival-Aware | ObjCommit | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Deathmatch/Survival-Aware | EngRedirect | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Deathmatch/Survival-Aware | ResSeek | 0.61 ± 0.06 | 0.66 ± 0.07 | -0.11 | 0.366 |
| Deathmatch/Survival-Aware | Kills | 4.70 ± 0.46 | 5.46 ± 0.52 | -0.31 | 0.012 |
| Deathmatch/Survival-Aware | Deaths | 4.72 ± 0.50 | 5.40 ± 0.52 | -0.22 | 0.074 |

## Combat-mode ablation (full vs weights-only; paired Wilcoxon, r > 0: full higher)

| Scenario | Style | Metric | Full | Weights-only | r | p |
|---|---|---|---|---|---|---|
| Mission | Mission–Cooperation | ObjCommit | 0.94 ± 0.01 | 0.95 ± 0.01 | -0.05 | 0.718 |
| Mission | Mission–Cooperation | AllyDist | 1.77 ± 0.18 | 1.71 ± 0.15 | -0.05 | 0.747 |
| Mission | Mission–Cooperation | EngRedirect | 0.02 ± 0.01 | 0.02 ± 0.01 | -0.19 | 0.472 |
| Mission | Mission–Cooperation | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | -1.00 | 1.000 |
| Mission | Persistent Objective | ObjCommit | 0.87 ± 0.04 | 0.87 ± 0.04 | +0.00 | 1.000 |
| Mission | Persistent Objective | AllyDist | 3.00 ± 0.41 | 3.00 ± 0.41 | +0.00 | 1.000 |
| Mission | Persistent Objective | EngRedirect | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Mission | Persistent Objective | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Mission | Aggressive | ObjCommit | 0.32 ± 0.06 | 0.33 ± 0.07 | -0.08 | 0.519 |
| Mission | Aggressive | AllyDist | 4.48 ± 0.41 | 4.28 ± 0.40 | +0.10 | 0.408 |
| Mission | Aggressive | EngRedirect | 1.69 ± 0.20 | 0.79 ± 0.12 | +0.85 | <0.001 |
| Mission | Aggressive | ResSeek | 0.17 ± 0.04 | 0.07 ± 0.02 | +0.63 | <0.001 |
| Mission | Survival-Aware | ObjCommit | 0.04 ± 0.03 | 0.02 ± 0.01 | +0.29 | 0.102 |
| Mission | Survival-Aware | AllyDist | 6.89 ± 0.71 | 5.06 ± 0.33 | +0.49 | <0.001 |
| Mission | Survival-Aware | EngRedirect | 0.00 ± 0.00 | 0.33 ± 0.05 | -1.00 | <0.001 |
| Mission | Survival-Aware | ResSeek | 0.38 ± 0.06 | 0.05 ± 0.02 | +0.93 | <0.001 |
| Deathmatch | Mission–Cooperation | EngRedirect | 0.46 ± 0.05 | 0.70 ± 0.08 | -0.59 | <0.001 |
| Deathmatch | Mission–Cooperation | ResSeek | 0.24 ± 0.05 | 0.33 ± 0.07 | -0.23 | 0.049 |
| Deathmatch | Mission–Cooperation | AllyDist | 2.69 ± 0.09 | 2.92 ± 0.09 | -0.37 | 0.001 |
| Deathmatch | Persistent Objective | EngRedirect | 0.09 ± 0.02 | 0.09 ± 0.02 | +0.00 | 1.000 |
| Deathmatch | Persistent Objective | ResSeek | 0.02 ± 0.01 | 0.02 ± 0.01 | +0.00 | 1.000 |
| Deathmatch | Persistent Objective | AllyDist | 5.61 ± 0.26 | 5.61 ± 0.26 | +0.00 | 1.000 |
| Deathmatch | Aggressive | EngRedirect | 2.86 ± 0.13 | 1.48 ± 0.09 | +1.00 | <0.001 |
| Deathmatch | Aggressive | ResSeek | 0.35 ± 0.04 | 0.21 ± 0.03 | +0.60 | <0.001 |
| Deathmatch | Aggressive | AllyDist | 4.73 ± 0.20 | 4.81 ± 0.24 | -0.03 | 0.762 |
| Deathmatch | Survival-Aware | EngRedirect | 0.00 ± 0.00 | 0.51 ± 0.05 | -1.00 | <0.001 |
| Deathmatch | Survival-Aware | ResSeek | 0.61 ± 0.06 | 0.10 ± 0.02 | +0.97 | <0.001 |
| Deathmatch | Survival-Aware | AllyDist | 7.42 ± 0.57 | 5.85 ± 0.26 | +0.53 | <0.001 |
| Control | Mission–Cooperation | CtrlScore | 117.30 ± 2.64 | 115.35 ± 3.43 | +0.32 | 0.331 |
| Control | Mission–Cooperation | ObjCommit | 0.95 ± 0.01 | 0.95 ± 0.01 | -0.19 | 0.291 |
| Control | Mission–Cooperation | EngRedirect | 0.00 ± 0.01 | 0.02 ± 0.02 | -0.60 | 0.312 |
| Control | Mission–Cooperation | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.01 | -1.00 | 0.500 |
| Control | Persistent Objective | CtrlScore | 116.86 ± 3.49 | 116.86 ± 3.49 | +0.00 | 1.000 |
| Control | Persistent Objective | ObjCommit | 0.91 ± 0.03 | 0.91 ± 0.03 | +0.00 | 1.000 |
| Control | Persistent Objective | EngRedirect | 0.01 ± 0.01 | 0.01 ± 0.01 | +0.00 | 1.000 |
| Control | Persistent Objective | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Control | Aggressive | CtrlScore | 73.61 ± 10.43 | 59.40 ± 11.03 | +0.28 | 0.043 |
| Control | Aggressive | ObjCommit | 0.29 ± 0.05 | 0.28 ± 0.06 | +0.05 | 0.699 |
| Control | Aggressive | EngRedirect | 2.00 ± 0.18 | 0.87 ± 0.10 | +0.96 | <0.001 |
| Control | Aggressive | ResSeek | 0.18 ± 0.04 | 0.08 ± 0.02 | +0.58 | <0.001 |
| Control | Survival-Aware | CtrlScore | 7.94 ± 5.10 | 11.49 ± 6.21 | -0.18 | 0.345 |
| Control | Survival-Aware | ObjCommit | 0.02 ± 0.02 | 0.04 ± 0.02 | -0.21 | 0.261 |
| Control | Survival-Aware | EngRedirect | 0.00 ± 0.00 | 0.41 ± 0.06 | -1.00 | <0.001 |
| Control | Survival-Aware | ResSeek | 0.43 ± 0.06 | 0.05 ± 0.02 | +0.97 | <0.001 |

Weights-only Control outcomes: Mission–Cooperation: 90/100 wins; Persistent Objective: 96/100 wins; Aggressive: 38/100 wins; Survival-Aware: 6/100 wins

## Style interpolation (mode fixed to keep moving; Spearman rho between alpha and metric)


### Deathmatch: Aggressive -> Survival-Aware

| alpha | EngRedirect | ResSeek | AllyDist | Kills | Deaths |
|---|---|---|---|---|---|
| 0.00 | 1.48 ± 0.09 | 0.21 ± 0.03 | 4.81 ± 0.24 | 9.95 ± 0.57 | 8.53 ± 0.53 |
| 0.25 | 0.96 ± 0.08 | 0.13 ± 0.02 | 5.45 ± 0.26 | 8.31 ± 0.49 | 6.65 ± 0.52 |
| 0.50 | 0.80 ± 0.06 | 0.10 ± 0.02 | 5.61 ± 0.27 | 7.89 ± 0.48 | 6.46 ± 0.42 |
| 0.75 | 0.60 ± 0.05 | 0.08 ± 0.02 | 5.78 ± 0.28 | 7.60 ± 0.46 | 5.93 ± 0.41 |
| 1.00 | 0.51 ± 0.05 | 0.10 ± 0.02 | 5.85 ± 0.26 | 7.63 ± 0.48 | 5.95 ± 0.48 |

- Spearman rho(alpha, EngRedirect) = -0.67, p = <0.001
- Spearman rho(alpha, ResSeek) = -0.30, p = <0.001
- Spearman rho(alpha, AllyDist) = +0.25, p = <0.001
- Spearman rho(alpha, Kills) = -0.28, p = <0.001
- Spearman rho(alpha, Deaths) = -0.31, p = <0.001

### Mission: Mission–Cooperation -> Persistent Objective

| alpha | ObjCommit | AllyDist | EngRedirect | Kills | Deaths |
|---|---|---|---|---|---|
| 0.00 | 0.95 ± 0.01 | 1.71 ± 0.15 | 0.02 ± 0.01 | 4.89 ± 0.89 | 4.15 ± 0.86 |
| 0.25 | 0.94 ± 0.01 | 1.89 ± 0.19 | 0.02 ± 0.01 | 5.01 ± 0.88 | 4.58 ± 0.91 |
| 0.50 | 0.93 ± 0.01 | 2.03 ± 0.21 | 0.01 ± 0.01 | 5.03 ± 0.87 | 4.76 ± 0.92 |
| 0.75 | 0.92 ± 0.02 | 2.23 ± 0.26 | 0.01 ± 0.01 | 5.15 ± 0.91 | 4.91 ± 0.98 |
| 1.00 | 0.87 ± 0.04 | 3.00 ± 0.41 | 0.00 ± 0.00 | 5.23 ± 0.89 | 5.19 ± 0.98 |

- Spearman rho(alpha, ObjCommit) = -0.14, p = 0.001
- Spearman rho(alpha, AllyDist) = +0.20, p = <0.001
- Spearman rho(alpha, EngRedirect) = -0.11, p = 0.013
- Spearman rho(alpha, Kills) = +0.03, p = 0.496
- Spearman rho(alpha, Deaths) = +0.06, p = 0.188

## Navigation-weight scale (lambda x k; Spearman rho between k and metric)


### Mission / Mission–Cooperation

| scale | AllyDist | ObjCommit | EngRedirect | ResSeek | Kills | Deaths |
|---|---|---|---|---|---|---|
| x0 | 1.89 ± 0.22 | 0.94 ± 0.01 | 0.02 ± 0.01 | 0.00 ± 0.00 | 5.65 ± 1.07 | 4.80 ± 1.02 |
| x0.25 | 1.91 ± 0.20 | 0.94 ± 0.01 | 0.02 ± 0.02 | 0.00 ± 0.00 | 5.43 ± 1.00 | 5.04 ± 1.04 |
| x0.5 | 1.83 ± 0.18 | 0.94 ± 0.01 | 0.01 ± 0.01 | 0.00 ± 0.00 | 5.15 ± 0.95 | 4.81 ± 1.00 |
| x1 | 1.77 ± 0.18 | 0.94 ± 0.01 | 0.02 ± 0.01 | 0.00 ± 0.00 | 5.03 ± 0.94 | 4.22 ± 0.89 |
| x2 | 1.97 ± 0.21 | 0.93 ± 0.02 | 0.02 ± 0.01 | 0.00 ± 0.00 | 4.99 ± 0.88 | 4.79 ± 0.99 |

- Spearman rho(scale, AllyDist) = +0.04, p = 0.422
- Spearman rho(scale, ObjCommit) = -0.05, p = 0.306
- Spearman rho(scale, EngRedirect) = +0.04, p = 0.421
- Spearman rho(scale, ResSeek) = -0.02, p = 0.679
- Spearman rho(scale, Kills) = -0.05, p = 0.289
- Spearman rho(scale, Deaths) = -0.02, p = 0.646

### Deathmatch / Survival-Aware

| scale | AllyDist | ObjCommit | EngRedirect | ResSeek | Kills | Deaths |
|---|---|---|---|---|---|---|
| x0 | 6.67 ± 0.69 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.66 ± 0.07 | 5.46 ± 0.52 | 5.40 ± 0.52 |
| x0.25 | 7.57 ± 0.64 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.57 ± 0.06 | 4.95 ± 0.46 | 4.38 ± 0.48 |
| x0.5 | 7.31 ± 0.52 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.61 ± 0.06 | 4.65 ± 0.42 | 4.69 ± 0.46 |
| x1 | 7.42 ± 0.57 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.61 ± 0.06 | 4.70 ± 0.46 | 4.72 ± 0.50 |
| x2 | 7.25 ± 0.63 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.61 ± 0.07 | 4.49 ± 0.48 | 4.69 ± 0.55 |

- Spearman rho(scale, AllyDist) = +0.06, p = 0.177
- Spearman rho(scale, ResSeek) = -0.03, p = 0.468
- Spearman rho(scale, Kills) = -0.13, p = 0.003
- Spearman rho(scale, Deaths) = -0.07, p = 0.136

## Additional experiment: designer risk budgets, relative budget (Deathmatch)


### Survival-Aware (fixed-weight reference: main experiment)

| beta | Adherence | ExposureRatio | LengthOverhead | lambda_E | EngRedirect | ResSeek | AllyDist | Kills | Deaths |
|---|---|---|---|---|---|---|---|---|---|
| fixed | – | – | – | 20.00 | 0.00 ± 0.00 | 0.61 ± 0.06 | 7.42 ± 0.57 | 4.70 ± 0.46 | 4.72 ± 0.50 |
| 1.00 | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.00 ± 0.00 | 0.66 ± 0.07 | 7.23 ± 0.65 | 5.79 ± 0.51 | 5.43 ± 0.54 |
| 0.75 | 0.956 ± 0.005 | 0.554 ± 0.020 | 1.054 ± 0.006 | 2.629 ± 0.259 | 0.00 ± 0.00 | 0.60 ± 0.06 | 7.28 ± 0.66 | 5.01 ± 0.48 | 4.76 ± 0.48 |
| 0.50 | 0.943 ± 0.006 | 0.497 ± 0.023 | 1.072 ± 0.008 | 3.321 ± 0.351 | 0.00 ± 0.00 | 0.62 ± 0.06 | 7.45 ± 0.59 | 4.95 ± 0.46 | 4.91 ± 0.44 |
| 0.25 | 0.932 ± 0.007 | 0.457 ± 0.023 | 1.079 ± 0.009 | 3.836 ± 0.402 | 0.00 ± 0.00 | 0.57 ± 0.06 | 7.32 ± 0.63 | 4.94 ± 0.46 | 4.51 ± 0.46 |

- Spearman rho(beta, budget_adherence) = +0.71, p = <0.001
- Spearman rho(beta, exposure_ratio) = +0.73, p = <0.001
- Spearman rho(beta, length_overhead) = -0.68, p = <0.001
- Spearman rho(beta, mean_lambda) = -0.69, p = <0.001
- Spearman rho(beta, resource_seeking_rate_per_100) = +0.08, p = 0.095
- Spearman rho(beta, avg_ally_proximity) = -0.05, p = 0.285
- Spearman rho(beta, kills) = +0.11, p = 0.023
- Spearman rho(beta, deaths) = +0.10, p = 0.037

- Paired Wilcoxon beta=0.25 vs 1 (budget_adherence): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (exposure_ratio): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (length_overhead): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (mean_lambda): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (engagement_redirection_rate_per_100): r = +0.00, p = 1.000
- Paired Wilcoxon beta=0.25 vs 1 (resource_seeking_rate_per_100): r = -0.26, p = 0.026
- Paired Wilcoxon beta=0.25 vs 1 (avg_ally_proximity): r = +0.09, p = 0.443
- Paired Wilcoxon beta=0.25 vs 1 (kills): r = -0.34, p = 0.004
- Paired Wilcoxon beta=0.25 vs 1 (deaths): r = -0.30, p = 0.012

### Aggressive (fixed-weight reference: main experiment)

| beta | Adherence | ExposureRatio | LengthOverhead | lambda_E | EngRedirect | ResSeek | AllyDist | Kills | Deaths |
|---|---|---|---|---|---|---|---|---|---|
| fixed | – | – | – | 3.64 | 2.86 ± 0.13 | 0.35 ± 0.04 | 4.73 ± 0.20 | 11.76 ± 0.50 | 11.41 ± 0.53 |
| 1.00 | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 3.24 ± 0.12 | 0.40 ± 0.04 | 4.60 ± 0.24 | 13.61 ± 0.52 | 12.49 ± 0.52 |
| 0.75 | 0.607 ± 0.011 | 0.802 ± 0.007 | 1.337 ± 0.020 | 21.982 ± 0.574 | 2.45 ± 0.09 | 0.24 ± 0.03 | 5.71 ± 0.24 | 9.83 ± 0.50 | 10.58 ± 0.46 |
| 0.50 | 0.469 ± 0.015 | 0.783 ± 0.009 | 1.371 ± 0.020 | 27.227 ± 0.778 | 2.25 ± 0.08 | 0.20 ± 0.03 | 5.79 ± 0.27 | 8.96 ± 0.47 | 10.41 ± 0.45 |
| 0.25 | 0.447 ± 0.019 | 0.780 ± 0.009 | 1.364 ± 0.022 | 27.989 ± 0.946 | 2.23 ± 0.09 | 0.21 ± 0.03 | 5.78 ± 0.28 | 9.18 ± 0.50 | 9.93 ± 0.51 |

- Spearman rho(beta, budget_adherence) = +0.86, p = <0.001
- Spearman rho(beta, exposure_ratio) = +0.67, p = <0.001
- Spearman rho(beta, length_overhead) = -0.63, p = <0.001
- Spearman rho(beta, mean_lambda) = -0.82, p = <0.001
- Spearman rho(beta, engagement_redirection_rate_per_100) = +0.55, p = <0.001
- Spearman rho(beta, resource_seeking_rate_per_100) = +0.35, p = <0.001
- Spearman rho(beta, avg_ally_proximity) = -0.30, p = <0.001
- Spearman rho(beta, kills) = +0.50, p = <0.001
- Spearman rho(beta, deaths) = +0.32, p = <0.001

- Paired Wilcoxon beta=0.25 vs 1 (budget_adherence): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (exposure_ratio): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (length_overhead): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (mean_lambda): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (engagement_redirection_rate_per_100): r = -0.97, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (resource_seeking_rate_per_100): r = -0.72, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (avg_ally_proximity): r = +0.70, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (kills): r = -0.97, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (deaths): r = -0.78, p = <0.001

## Additional experiment: designer risk budgets, normalised budget (Deathmatch)


### Survival-Aware (fixed-weight reference: main experiment)

| beta | Adherence | ExposureRatio | LengthOverhead | lambda_E | BudgetPosition | EngRedirect | ResSeek | AllyDist | Kills | Deaths |
|---|---|---|---|---|---|---|---|---|---|---|
| fixed | – | – | – | 20.00 | – | 0.00 ± 0.00 | 0.61 ± 0.06 | 7.42 ± 0.57 | 4.70 ± 0.46 | 4.72 ± 0.50 |
| 1.00 | 1.000 ± 0.000 | 0.999 ± 0.001 | 1.000 ± 0.000 | 0.001 ± 0.001 | 0.998 ± 0.001 | 0.00 ± 0.00 | 0.67 ± 0.07 | 7.13 ± 0.65 | 5.82 ± 0.51 | 5.54 ± 0.53 |
| 0.75 | 1.000 ± 0.000 | 0.558 ± 0.019 | 1.053 ± 0.007 | 0.474 ± 0.064 | 0.162 ± 0.009 | 0.00 ± 0.00 | 0.65 ± 0.07 | 7.56 ± 0.64 | 5.22 ± 0.48 | 4.93 ± 0.51 |
| 0.50 | 1.000 ± 0.000 | 0.513 ± 0.023 | 1.061 ± 0.007 | 0.566 ± 0.075 | 0.095 ± 0.007 | 0.00 ± 0.00 | 0.63 ± 0.07 | 6.74 ± 0.54 | 4.95 ± 0.45 | 4.87 ± 0.51 |
| 0.25 | 1.000 ± 0.000 | 0.445 ± 0.021 | 1.077 ± 0.009 | 0.779 ± 0.094 | 0.033 ± 0.003 | 0.00 ± 0.00 | 0.61 ± 0.06 | 7.09 ± 0.57 | 4.99 ± 0.46 | 4.67 ± 0.48 |
| 0.00 | 1.000 ± 0.000 | 0.442 ± 0.025 | 1.089 ± 0.012 | 1.044 ± 0.161 | 0.000 ± 0.000 | 0.00 ± 0.00 | 0.58 ± 0.06 | 7.80 ± 0.68 | 4.91 ± 0.42 | 4.51 ± 0.42 |

- Spearman rho(beta, exposure_ratio) = +0.70, p = <0.001
- Spearman rho(beta, length_overhead) = -0.63, p = <0.001
- Spearman rho(beta, mean_lambda) = -0.67, p = <0.001
- Spearman rho(beta, budget_position) = +0.97, p = <0.001
- Spearman rho(beta, resource_seeking_rate_per_100) = +0.10, p = 0.027
- Spearman rho(beta, avg_ally_proximity) = -0.06, p = 0.159
- Spearman rho(beta, kills) = +0.12, p = 0.006
- Spearman rho(beta, deaths) = +0.13, p = 0.004

- Paired Wilcoxon beta=0.00 vs 1 (budget_adherence): r = +0.00, p = 1.000
- Paired Wilcoxon beta=0.00 vs 1 (exposure_ratio): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (length_overhead): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (mean_lambda): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (budget_position): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (engagement_redirection_rate_per_100): r = +0.00, p = 1.000
- Paired Wilcoxon beta=0.00 vs 1 (resource_seeking_rate_per_100): r = -0.25, p = 0.030
- Paired Wilcoxon beta=0.00 vs 1 (avg_ally_proximity): r = +0.22, p = 0.052
- Paired Wilcoxon beta=0.00 vs 1 (kills): r = -0.40, p = 0.001
- Paired Wilcoxon beta=0.00 vs 1 (deaths): r = -0.35, p = 0.003

### Aggressive (fixed-weight reference: main experiment)

| beta | Adherence | ExposureRatio | LengthOverhead | lambda_E | BudgetPosition | EngRedirect | ResSeek | AllyDist | Kills | Deaths |
|---|---|---|---|---|---|---|---|---|---|---|
| fixed | – | – | – | 3.64 | – | 2.86 ± 0.13 | 0.35 ± 0.04 | 4.73 ± 0.20 | 11.76 ± 0.50 | 11.41 ± 0.53 |
| 1.00 | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.999 ± 0.000 | 3.24 ± 0.12 | 0.40 ± 0.04 | 4.61 ± 0.24 | 13.58 ± 0.51 | 12.51 ± 0.53 |
| 0.75 | 1.000 ± 0.000 | 0.836 ± 0.007 | 1.227 ± 0.014 | 2.552 ± 0.131 | 0.200 ± 0.010 | 2.59 ± 0.11 | 0.26 ± 0.04 | 5.15 ± 0.23 | 10.25 ± 0.51 | 11.04 ± 0.55 |
| 0.50 | 1.000 ± 0.000 | 0.804 ± 0.009 | 1.313 ± 0.034 | 3.485 ± 0.317 | 0.100 ± 0.006 | 2.38 ± 0.12 | 0.23 ± 0.04 | 5.51 ± 0.27 | 9.29 ± 0.57 | 10.44 ± 0.58 |
| 0.25 | 1.000 ± 0.000 | 0.789 ± 0.007 | 1.350 ± 0.022 | 4.165 ± 0.422 | 0.029 ± 0.002 | 2.37 ± 0.09 | 0.24 ± 0.03 | 5.75 ± 0.26 | 9.31 ± 0.51 | 10.23 ± 0.44 |
| 0.00 | 1.000 ± 0.000 | 0.770 ± 0.011 | 1.382 ± 0.021 | 5.064 ± 0.254 | 0.000 ± 0.000 | 2.20 ± 0.08 | 0.20 ± 0.03 | 5.78 ± 0.28 | 9.06 ± 0.44 | 9.92 ± 0.51 |

- Spearman rho(beta, exposure_ratio) = +0.75, p = <0.001
- Spearman rho(beta, length_overhead) = -0.77, p = <0.001
- Spearman rho(beta, mean_lambda) = -0.85, p = <0.001
- Spearman rho(beta, budget_position) = +0.98, p = <0.001
- Spearman rho(beta, engagement_redirection_rate_per_100) = +0.52, p = <0.001
- Spearman rho(beta, resource_seeking_rate_per_100) = +0.30, p = <0.001
- Spearman rho(beta, avg_ally_proximity) = -0.31, p = <0.001
- Spearman rho(beta, kills) = +0.47, p = <0.001
- Spearman rho(beta, deaths) = +0.31, p = <0.001

- Paired Wilcoxon beta=0.00 vs 1 (budget_adherence): r = +0.00, p = 1.000
- Paired Wilcoxon beta=0.00 vs 1 (exposure_ratio): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (length_overhead): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (mean_lambda): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (budget_position): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (engagement_redirection_rate_per_100): r = -0.99, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (resource_seeking_rate_per_100): r = -0.71, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (avg_ally_proximity): r = +0.71, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (kills): r = -0.96, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (deaths): r = -0.79, p = <0.001
