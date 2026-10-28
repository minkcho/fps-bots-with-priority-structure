# Statistical summary (n = 100 episodes per condition)

Consistency checks (CRN): navigation-ablation full = main; commitment 0.45 = main MC; lambda x1 = main; lambda x0 = distance-only. **passed**

## Main experiment

| Scenario | Style | ObjCommit | AllyDist | EngRedirect | ResSeek | Kills | Deaths | Control |
|---|---|---|---|---|---|---|---|---|
| Mission | Mission–Cooperation | 0.94 ± 0.01 | 2.08 ± 0.18 | 0.01 ± 0.01 | 0.00 ± 0.00 | 6.2 ± 0.9 | 5.1 ± 0.8 |  |
| Mission | Persistent Objective | 0.91 ± 0.02 | 2.82 ± 0.38 | 0.01 ± 0.01 | 0.00 ± 0.00 | 6.4 ± 0.9 | 5.2 ± 0.8 |  |
| Mission | Aggressive | 0.37 ± 0.06 | 4.42 ± 0.36 | 1.45 ± 0.20 | 0.14 ± 0.03 | 6.4 ± 0.8 | 6.2 ± 0.8 |  |
| Mission | Survival-Aware | 0.05 ± 0.03 | 6.80 ± 0.84 | 0.00 ± 0.00 | 0.35 ± 0.05 | 3.0 ± 0.4 | 2.9 ± 0.4 |  |
| Deathmatch | Mission–Cooperation | 0.00 ± 0.00 | 2.86 ± 0.11 | 0.47 ± 0.06 | 0.25 ± 0.05 | 10.1 ± 0.5 | 9.3 ± 0.5 |  |
| Deathmatch | Persistent Objective | 0.00 ± 0.00 | 5.81 ± 0.29 | 0.08 ± 0.02 | 0.03 ± 0.01 | 9.0 ± 0.4 | 5.9 ± 0.4 |  |
| Deathmatch | Aggressive | 0.00 ± 0.00 | 5.11 ± 0.23 | 2.84 ± 0.10 | 0.33 ± 0.04 | 11.9 ± 0.5 | 12.2 ± 0.5 |  |
| Deathmatch | Survival-Aware | 0.00 ± 0.00 | 7.20 ± 0.79 | 0.00 ± 0.00 | 0.57 ± 0.06 | 4.9 ± 0.4 | 4.7 ± 0.5 |  |
| Control | Mission–Cooperation | 0.94 ± 0.01 | 2.22 ± 0.21 | 0.01 ± 0.01 | 0.00 ± 0.00 | 2.3 ± 0.4 | 1.5 ± 0.4 | 117.58 ± 2.45; wins 95/100; stalls 0; med. steps 143.0 |
| Control | Persistent Objective | 0.90 ± 0.03 | 3.05 ± 0.41 | 0.01 ± 0.01 | 0.00 ± 0.00 | 2.4 ± 0.4 | 1.9 ± 0.5 | 114.95 ± 3.93; wins 91/100; stalls 0; med. steps 143.0 |
| Control | Aggressive | 0.32 ± 0.06 | 4.35 ± 0.35 | 1.74 ± 0.18 | 0.19 ± 0.04 | 5.0 ± 0.8 | 4.9 ± 0.8 | 70.06 ± 10.78; wins 47/100; stalls 0; med. steps 270.0 |
| Control | Survival-Aware | 0.03 ± 0.02 | 6.05 ± 0.63 | 0.00 ± 0.00 | 0.42 ± 0.06 | 2.3 ± 0.4 | 2.2 ± 0.4 | 13.59 ± 6.58; wins 7/100; stalls 8; med. steps 298.0 |

## Style contrasts (Mann–Whitney U, rank-biserial r > 0: first style higher; Holm within family)

| Scenario | Metric | Style A | Style B | r | p | p (Holm) |
|---|---|---|---|---|---|---|
| Mission | ObjCommit | Mission–Cooperation | Persistent Objective | +0.14 | 0.081 | 0.081 |
| Mission | ObjCommit | Mission–Cooperation | Aggressive | +0.85 | <0.001 | <0.001 |
| Mission | ObjCommit | Mission–Cooperation | Survival-Aware | +1.00 | <0.001 | <0.001 |
| Mission | ObjCommit | Persistent Objective | Aggressive | +0.82 | <0.001 | <0.001 |
| Mission | ObjCommit | Persistent Objective | Survival-Aware | +1.00 | <0.001 | <0.001 |
| Mission | ObjCommit | Aggressive | Survival-Aware | +0.68 | <0.001 | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Persistent Objective | -0.23 | 0.004 | 0.004 |
| Mission | AllyDist | Mission–Cooperation | Aggressive | -0.71 | <0.001 | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Survival-Aware | -0.85 | <0.001 | <0.001 |
| Mission | AllyDist | Persistent Objective | Aggressive | -0.52 | <0.001 | <0.001 |
| Mission | AllyDist | Persistent Objective | Survival-Aware | -0.70 | <0.001 | <0.001 |
| Mission | AllyDist | Aggressive | Survival-Aware | -0.33 | <0.001 | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Persistent Objective | +0.83 | <0.001 | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Aggressive | -1.00 | <0.001 | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Survival-Aware | +0.93 | <0.001 | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Aggressive | -1.00 | <0.001 | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Survival-Aware | +0.57 | <0.001 | <0.001 |
| Deathmatch | EngRedirect | Aggressive | Survival-Aware | +1.00 | <0.001 | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Persistent Objective | +0.76 | <0.001 | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Aggressive | -0.30 | <0.001 | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Survival-Aware | -0.55 | <0.001 | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Aggressive | -0.94 | <0.001 | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Survival-Aware | -0.91 | <0.001 | <0.001 |
| Deathmatch | ResSeek | Aggressive | Survival-Aware | -0.46 | <0.001 | <0.001 |
| Deathmatch | AllyDist | Mission–Cooperation | Persistent Objective | -0.94 | <0.001 | <0.001 |
| Deathmatch | AllyDist | Mission–Cooperation | Aggressive | -0.93 | <0.001 | <0.001 |
| Deathmatch | AllyDist | Mission–Cooperation | Survival-Aware | -0.73 | <0.001 | <0.001 |
| Deathmatch | AllyDist | Persistent Objective | Aggressive | +0.31 | <0.001 | <0.001 |
| Deathmatch | AllyDist | Persistent Objective | Survival-Aware | -0.23 | 0.005 | 0.005 |
| Deathmatch | AllyDist | Aggressive | Survival-Aware | -0.37 | <0.001 | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Persistent Objective | +0.04 | 0.259 | 0.259 |
| Control | CtrlScore | Mission–Cooperation | Aggressive | +0.50 | <0.001 | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Survival-Aware | +0.92 | <0.001 | <0.001 |
| Control | CtrlScore | Persistent Objective | Aggressive | +0.46 | <0.001 | <0.001 |
| Control | CtrlScore | Persistent Objective | Survival-Aware | +0.91 | <0.001 | <0.001 |
| Control | CtrlScore | Aggressive | Survival-Aware | +0.52 | <0.001 | <0.001 |
| Control | ObjCommit | Mission–Cooperation | Persistent Objective | +0.18 | 0.024 | 0.024 |
| Control | ObjCommit | Mission–Cooperation | Aggressive | +0.88 | <0.001 | <0.001 |
| Control | ObjCommit | Mission–Cooperation | Survival-Aware | +1.00 | <0.001 | <0.001 |
| Control | ObjCommit | Persistent Objective | Aggressive | +0.83 | <0.001 | <0.001 |
| Control | ObjCommit | Persistent Objective | Survival-Aware | +0.99 | <0.001 | <0.001 |
| Control | ObjCommit | Aggressive | Survival-Aware | +0.73 | <0.001 | <0.001 |
| Control | AllyDist | Mission–Cooperation | Persistent Objective | -0.16 | 0.048 | 0.048 |
| Control | AllyDist | Mission–Cooperation | Aggressive | -0.69 | <0.001 | <0.001 |
| Control | AllyDist | Mission–Cooperation | Survival-Aware | -0.76 | <0.001 | <0.001 |
| Control | AllyDist | Persistent Objective | Aggressive | -0.43 | <0.001 | <0.001 |
| Control | AllyDist | Persistent Objective | Survival-Aware | -0.58 | <0.001 | <0.001 |
| Control | AllyDist | Aggressive | Survival-Aware | -0.30 | <0.001 | <0.001 |

## Commitment sensitivity (Mission–Cooperation base)

| w_commit | Mission ObjCommit | Control score | Control wins | stalls |
|---|---|---|---|---|
| 0.00 | 0.80 ± 0.03 | 101.41 ± 7.37 | 73/100 | 4 |
| 0.20 | 0.93 ± 0.01 | 118.85 ± 1.44 | 96/100 | 0 |
| 0.45 | 0.94 ± 0.01 | 117.58 ± 2.45 | 95/100 | 0 |
| 0.65 | 0.92 ± 0.01 | 117.38 ± 2.57 | 96/100 | 0 |
| 0.85 | 0.93 ± 0.01 | 118.83 ± 1.54 | 97/100 | 0 |
| 1.05 | 0.92 ± 0.01 | 119.00 ± 1.35 | 96/100 | 0 |
| 1.25 | 0.92 ± 0.01 | 119.00 ± 1.35 | 96/100 | 0 |

Paired Wilcoxon, w=0.45 vs w=0 (Mission, ObjCommit): r = +0.94, p = <0.001

Paired Wilcoxon, w=0.45 vs w=0 (Control, CtrlScore): r = +0.90, p = <0.001

## Navigation ablation (full vs distance-only; paired Wilcoxon, r > 0: full higher)

| Condition | Metric | Full | Distance-only | r | p |
|---|---|---|---|---|---|
| Mission/Mission–Cooperation | AllyDist | 2.08 ± 0.18 | 2.09 ± 0.20 | +0.05 | 0.737 |
| Mission/Mission–Cooperation | ObjCommit | 0.94 ± 0.01 | 0.94 ± 0.01 | -0.31 | 0.038 |
| Mission/Mission–Cooperation | EngRedirect | 0.01 ± 0.01 | 0.01 ± 0.02 | -0.02 | 0.991 |
| Mission/Mission–Cooperation | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Mission/Mission–Cooperation | Kills | 6.25 ± 0.94 | 6.55 ± 0.97 | -0.33 | 0.056 |
| Mission/Mission–Cooperation | Deaths | 5.06 ± 0.82 | 5.26 ± 0.85 | -0.16 | 0.356 |
| Deathmatch/Survival-Aware | AllyDist | 7.20 ± 0.79 | 5.68 ± 0.56 | +0.34 | 0.004 |
| Deathmatch/Survival-Aware | ObjCommit | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Deathmatch/Survival-Aware | EngRedirect | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Deathmatch/Survival-Aware | ResSeek | 0.57 ± 0.06 | 0.60 ± 0.07 | -0.09 | 0.438 |
| Deathmatch/Survival-Aware | Kills | 4.86 ± 0.43 | 4.93 ± 0.43 | -0.05 | 0.675 |
| Deathmatch/Survival-Aware | Deaths | 4.65 ± 0.50 | 4.93 ± 0.49 | -0.09 | 0.471 |

## Combat-mode ablation (full vs weights-only; paired Wilcoxon, r > 0: full higher)

| Scenario | Style | Metric | Full | Weights-only | r | p |
|---|---|---|---|---|---|---|
| Mission | Mission–Cooperation | ObjCommit | 0.94 ± 0.01 | 0.94 ± 0.01 | -0.13 | 0.369 |
| Mission | Mission–Cooperation | AllyDist | 2.08 ± 0.18 | 2.04 ± 0.17 | +0.09 | 0.521 |
| Mission | Mission–Cooperation | EngRedirect | 0.01 ± 0.01 | 0.01 ± 0.01 | +0.01 | 0.975 |
| Mission | Mission–Cooperation | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | -1.00 | 1.000 |
| Mission | Persistent Objective | ObjCommit | 0.91 ± 0.02 | 0.91 ± 0.02 | +0.00 | 1.000 |
| Mission | Persistent Objective | AllyDist | 2.82 ± 0.38 | 2.82 ± 0.38 | +0.00 | 1.000 |
| Mission | Persistent Objective | EngRedirect | 0.01 ± 0.01 | 0.01 ± 0.01 | +0.00 | 1.000 |
| Mission | Persistent Objective | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Mission | Aggressive | ObjCommit | 0.37 ± 0.06 | 0.40 ± 0.07 | -0.15 | 0.237 |
| Mission | Aggressive | AllyDist | 4.42 ± 0.36 | 3.85 ± 0.32 | +0.43 | <0.001 |
| Mission | Aggressive | EngRedirect | 1.45 ± 0.20 | 0.87 ± 0.12 | +0.80 | <0.001 |
| Mission | Aggressive | ResSeek | 0.14 ± 0.03 | 0.09 ± 0.02 | +0.44 | <0.001 |
| Mission | Survival-Aware | ObjCommit | 0.05 ± 0.03 | 0.03 ± 0.02 | +0.26 | 0.116 |
| Mission | Survival-Aware | AllyDist | 6.80 ± 0.84 | 5.29 ± 0.30 | +0.28 | 0.018 |
| Mission | Survival-Aware | EngRedirect | 0.00 ± 0.00 | 0.32 ± 0.05 | -1.00 | <0.001 |
| Mission | Survival-Aware | ResSeek | 0.35 ± 0.05 | 0.05 ± 0.01 | +0.93 | <0.001 |
| Deathmatch | Mission–Cooperation | EngRedirect | 0.47 ± 0.06 | 0.73 ± 0.09 | -0.54 | <0.001 |
| Deathmatch | Mission–Cooperation | ResSeek | 0.25 ± 0.05 | 0.26 ± 0.05 | +0.01 | 0.913 |
| Deathmatch | Mission–Cooperation | AllyDist | 2.86 ± 0.11 | 2.90 ± 0.10 | -0.08 | 0.505 |
| Deathmatch | Persistent Objective | EngRedirect | 0.08 ± 0.02 | 0.08 ± 0.02 | +0.00 | 1.000 |
| Deathmatch | Persistent Objective | ResSeek | 0.03 ± 0.01 | 0.03 ± 0.01 | +0.00 | 1.000 |
| Deathmatch | Persistent Objective | AllyDist | 5.81 ± 0.29 | 5.81 ± 0.29 | +0.00 | 1.000 |
| Deathmatch | Aggressive | EngRedirect | 2.84 ± 0.10 | 1.46 ± 0.08 | +1.00 | <0.001 |
| Deathmatch | Aggressive | ResSeek | 0.33 ± 0.04 | 0.20 ± 0.03 | +0.55 | <0.001 |
| Deathmatch | Aggressive | AllyDist | 5.11 ± 0.23 | 4.73 ± 0.23 | +0.31 | 0.007 |
| Deathmatch | Survival-Aware | EngRedirect | 0.00 ± 0.00 | 0.51 ± 0.04 | -1.00 | <0.001 |
| Deathmatch | Survival-Aware | ResSeek | 0.57 ± 0.06 | 0.08 ± 0.02 | +0.95 | <0.001 |
| Deathmatch | Survival-Aware | AllyDist | 7.20 ± 0.79 | 6.06 ± 0.31 | +0.27 | 0.018 |
| Control | Mission–Cooperation | CtrlScore | 117.58 ± 2.45 | 117.82 ± 2.35 | -0.02 | 1.000 |
| Control | Mission–Cooperation | ObjCommit | 0.94 ± 0.01 | 0.94 ± 0.01 | +0.16 | 0.312 |
| Control | Mission–Cooperation | EngRedirect | 0.01 ± 0.01 | 0.02 ± 0.02 | -0.39 | 0.383 |
| Control | Mission–Cooperation | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Control | Persistent Objective | CtrlScore | 114.95 ± 3.93 | 114.95 ± 3.93 | +0.00 | 1.000 |
| Control | Persistent Objective | ObjCommit | 0.90 ± 0.03 | 0.90 ± 0.03 | +0.00 | 1.000 |
| Control | Persistent Objective | EngRedirect | 0.01 ± 0.01 | 0.01 ± 0.01 | +0.00 | 1.000 |
| Control | Persistent Objective | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Control | Aggressive | CtrlScore | 70.06 ± 10.78 | 76.38 ± 10.83 | -0.15 | 0.350 |
| Control | Aggressive | ObjCommit | 0.32 ± 0.06 | 0.38 ± 0.07 | -0.29 | 0.020 |
| Control | Aggressive | EngRedirect | 1.74 ± 0.18 | 0.97 ± 0.12 | +0.84 | <0.001 |
| Control | Aggressive | ResSeek | 0.19 ± 0.04 | 0.08 ± 0.03 | +0.57 | <0.001 |
| Control | Survival-Aware | CtrlScore | 13.59 ± 6.58 | 7.71 ± 5.24 | +0.10 | 0.520 |
| Control | Survival-Aware | ObjCommit | 0.03 ± 0.02 | 0.02 ± 0.01 | +0.25 | 0.195 |
| Control | Survival-Aware | EngRedirect | 0.00 ± 0.00 | 0.34 ± 0.05 | -1.00 | <0.001 |
| Control | Survival-Aware | ResSeek | 0.42 ± 0.06 | 0.07 ± 0.02 | +0.96 | <0.001 |

Weights-only Control outcomes: Mission–Cooperation: 95/100 wins; Persistent Objective: 91/100 wins; Aggressive: 56/100 wins; Survival-Aware: 3/100 wins

## Style interpolation (mode fixed to keep moving; Spearman rho between alpha and metric)


### Deathmatch: Aggressive -> Survival-Aware

| alpha | EngRedirect | ResSeek | AllyDist | Kills | Deaths |
|---|---|---|---|---|---|
| 0.00 | 1.46 ± 0.08 | 0.20 ± 0.03 | 4.73 ± 0.23 | 10.58 ± 0.47 | 8.81 ± 0.49 |
| 0.25 | 0.98 ± 0.07 | 0.14 ± 0.02 | 5.42 ± 0.26 | 9.03 ± 0.54 | 7.51 ± 0.49 |
| 0.50 | 0.79 ± 0.06 | 0.12 ± 0.02 | 5.48 ± 0.31 | 8.81 ± 0.45 | 6.72 ± 0.50 |
| 0.75 | 0.62 ± 0.06 | 0.09 ± 0.02 | 5.83 ± 0.27 | 8.78 ± 0.48 | 6.82 ± 0.44 |
| 1.00 | 0.51 ± 0.04 | 0.08 ± 0.02 | 6.06 ± 0.31 | 8.79 ± 0.36 | 6.44 ± 0.44 |

- Spearman rho(alpha, EngRedirect) = -0.70, p = <0.001
- Spearman rho(alpha, ResSeek) = -0.36, p = <0.001
- Spearman rho(alpha, AllyDist) = +0.30, p = <0.001
- Spearman rho(alpha, Kills) = -0.21, p = <0.001
- Spearman rho(alpha, Deaths) = -0.30, p = <0.001

### Mission: Mission–Cooperation -> Persistent Objective

| alpha | ObjCommit | AllyDist | EngRedirect | Kills | Deaths |
|---|---|---|---|---|---|
| 0.00 | 0.94 ± 0.01 | 2.04 ± 0.17 | 0.01 ± 0.01 | 6.36 ± 0.94 | 4.72 ± 0.78 |
| 0.25 | 0.92 ± 0.01 | 2.17 ± 0.20 | 0.01 ± 0.01 | 6.46 ± 0.96 | 4.93 ± 0.79 |
| 0.50 | 0.93 ± 0.01 | 2.21 ± 0.20 | 0.01 ± 0.01 | 6.60 ± 0.96 | 4.92 ± 0.78 |
| 0.75 | 0.92 ± 0.01 | 2.32 ± 0.21 | 0.01 ± 0.01 | 6.41 ± 0.95 | 4.94 ± 0.79 |
| 1.00 | 0.91 ± 0.02 | 2.82 ± 0.38 | 0.01 ± 0.01 | 6.42 ± 0.93 | 5.16 ± 0.83 |

- Spearman rho(alpha, ObjCommit) = -0.08, p = 0.064
- Spearman rho(alpha, AllyDist) = +0.15, p = <0.001
- Spearman rho(alpha, EngRedirect) = -0.01, p = 0.796
- Spearman rho(alpha, Kills) = -0.00, p = 0.935
- Spearman rho(alpha, Deaths) = +0.03, p = 0.503

## Navigation-weight scale (lambda x k; Spearman rho between k and metric)


### Mission / Mission–Cooperation

| scale | AllyDist | ObjCommit | EngRedirect | ResSeek | Kills | Deaths |
|---|---|---|---|---|---|---|
| x0 | 2.09 ± 0.20 | 0.94 ± 0.01 | 0.01 ± 0.02 | 0.00 ± 0.00 | 6.55 ± 0.97 | 5.26 ± 0.85 |
| x0.25 | 2.13 ± 0.21 | 0.94 ± 0.01 | 0.01 ± 0.01 | 0.00 ± 0.00 | 6.70 ± 1.01 | 5.17 ± 0.85 |
| x0.5 | 2.12 ± 0.20 | 0.94 ± 0.01 | 0.01 ± 0.01 | 0.00 ± 0.00 | 6.40 ± 0.96 | 4.96 ± 0.82 |
| x1 | 2.08 ± 0.18 | 0.94 ± 0.01 | 0.01 ± 0.01 | 0.00 ± 0.00 | 6.25 ± 0.94 | 5.06 ± 0.82 |
| x2 | 2.09 ± 0.19 | 0.93 ± 0.01 | 0.01 ± 0.01 | 0.00 ± 0.00 | 6.36 ± 0.94 | 5.12 ± 0.84 |

- Spearman rho(scale, AllyDist) = +0.01, p = 0.860
- Spearman rho(scale, ObjCommit) = -0.04, p = 0.349
- Spearman rho(scale, EngRedirect) = +0.01, p = 0.901
- Spearman rho(scale, ResSeek) = -0.03, p = 0.480
- Spearman rho(scale, Kills) = -0.04, p = 0.410
- Spearman rho(scale, Deaths) = -0.01, p = 0.775

### Deathmatch / Survival-Aware

| scale | AllyDist | ObjCommit | EngRedirect | ResSeek | Kills | Deaths |
|---|---|---|---|---|---|---|
| x0 | 5.68 ± 0.56 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.60 ± 0.07 | 4.93 ± 0.43 | 4.93 ± 0.49 |
| x0.25 | 6.82 ± 0.64 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.58 ± 0.06 | 4.94 ± 0.44 | 4.60 ± 0.48 |
| x0.5 | 7.08 ± 0.78 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.59 ± 0.06 | 4.53 ± 0.43 | 4.90 ± 0.49 |
| x1 | 7.20 ± 0.79 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.57 ± 0.06 | 4.86 ± 0.43 | 4.65 ± 0.50 |
| x2 | 6.81 ± 0.70 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.55 ± 0.06 | 4.82 ± 0.44 | 4.45 ± 0.50 |

- Spearman rho(scale, AllyDist) = +0.11, p = 0.010
- Spearman rho(scale, ResSeek) = -0.04, p = 0.331
- Spearman rho(scale, Kills) = -0.02, p = 0.644
- Spearman rho(scale, Deaths) = -0.04, p = 0.351

## Additional experiment: designer risk budgets, relative budget (Deathmatch)


### Survival-Aware (fixed-weight reference: main experiment)

| beta | Adherence | ExposureRatio | LengthOverhead | lambda_E | EngRedirect | ResSeek | AllyDist | Kills | Deaths |
|---|---|---|---|---|---|---|---|---|---|
| fixed | – | – | – | 20.00 | 0.00 ± 0.00 | 0.57 ± 0.06 | 7.20 ± 0.79 | 4.86 ± 0.43 | 4.65 ± 0.50 |
| 1.00 | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.00 ± 0.00 | 0.60 ± 0.06 | 5.82 ± 0.63 | 4.99 ± 0.47 | 5.02 ± 0.52 |
| 0.75 | 0.948 ± 0.006 | 0.611 ± 0.015 | 1.060 ± 0.008 | 3.059 ± 0.359 | 0.00 ± 0.00 | 0.57 ± 0.06 | 6.82 ± 0.67 | 4.76 ± 0.45 | 4.72 ± 0.47 |
| 0.50 | 0.923 ± 0.009 | 0.559 ± 0.018 | 1.076 ± 0.009 | 4.361 ± 0.481 | 0.00 ± 0.00 | 0.59 ± 0.06 | 6.42 ± 0.72 | 5.01 ± 0.44 | 4.86 ± 0.49 |
| 0.25 | 0.912 ± 0.010 | 0.515 ± 0.021 | 1.085 ± 0.009 | 4.807 ± 0.554 | 0.00 ± 0.00 | 0.55 ± 0.06 | 6.91 ± 0.78 | 4.52 ± 0.42 | 4.61 ± 0.47 |

- Spearman rho(beta, budget_adherence) = +0.72, p = <0.001
- Spearman rho(beta, exposure_ratio) = +0.74, p = <0.001
- Spearman rho(beta, length_overhead) = -0.69, p = <0.001
- Spearman rho(beta, mean_lambda) = -0.71, p = <0.001
- Spearman rho(beta, resource_seeking_rate_per_100) = +0.04, p = 0.380
- Spearman rho(beta, avg_ally_proximity) = -0.08, p = 0.128
- Spearman rho(beta, kills) = +0.06, p = 0.207
- Spearman rho(beta, deaths) = +0.06, p = 0.259

- Paired Wilcoxon beta=0.25 vs 1 (budget_adherence): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (exposure_ratio): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (length_overhead): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (mean_lambda): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (engagement_redirection_rate_per_100): r = +0.00, p = 1.000
- Paired Wilcoxon beta=0.25 vs 1 (resource_seeking_rate_per_100): r = -0.15, p = 0.205
- Paired Wilcoxon beta=0.25 vs 1 (avg_ally_proximity): r = +0.24, p = 0.038
- Paired Wilcoxon beta=0.25 vs 1 (kills): r = -0.19, p = 0.116
- Paired Wilcoxon beta=0.25 vs 1 (deaths): r = -0.17, p = 0.180

### Aggressive (fixed-weight reference: main experiment)

| beta | Adherence | ExposureRatio | LengthOverhead | lambda_E | EngRedirect | ResSeek | AllyDist | Kills | Deaths |
|---|---|---|---|---|---|---|---|---|---|
| fixed | – | – | – | 3.64 | 2.84 ± 0.10 | 0.33 ± 0.04 | 5.11 ± 0.23 | 11.86 ± 0.51 | 12.22 ± 0.49 |
| 1.00 | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 3.19 ± 0.12 | 0.37 ± 0.04 | 4.82 ± 0.26 | 13.22 ± 0.55 | 13.04 ± 0.51 |
| 0.75 | 0.632 ± 0.014 | 0.797 ± 0.008 | 1.315 ± 0.041 | 20.758 ± 0.589 | 2.51 ± 0.12 | 0.26 ± 0.03 | 5.26 ± 0.24 | 10.01 ± 0.52 | 11.43 ± 0.53 |
| 0.50 | 0.475 ± 0.012 | 0.760 ± 0.007 | 1.380 ± 0.019 | 27.095 ± 0.620 | 2.35 ± 0.08 | 0.23 ± 0.03 | 5.68 ± 0.25 | 9.74 ± 0.45 | 10.87 ± 0.44 |
| 0.25 | 0.431 ± 0.015 | 0.757 ± 0.009 | 1.393 ± 0.031 | 28.742 ± 0.763 | 2.26 ± 0.08 | 0.22 ± 0.03 | 5.54 ± 0.22 | 9.66 ± 0.45 | 10.50 ± 0.48 |

- Spearman rho(beta, budget_adherence) = +0.90, p = <0.001
- Spearman rho(beta, exposure_ratio) = +0.73, p = <0.001
- Spearman rho(beta, length_overhead) = -0.73, p = <0.001
- Spearman rho(beta, mean_lambda) = -0.87, p = <0.001
- Spearman rho(beta, engagement_redirection_rate_per_100) = +0.54, p = <0.001
- Spearman rho(beta, resource_seeking_rate_per_100) = +0.29, p = <0.001
- Spearman rho(beta, avg_ally_proximity) = -0.22, p = <0.001
- Spearman rho(beta, kills) = +0.41, p = <0.001
- Spearman rho(beta, deaths) = +0.36, p = <0.001

- Paired Wilcoxon beta=0.25 vs 1 (budget_adherence): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (exposure_ratio): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (length_overhead): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (mean_lambda): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (engagement_redirection_rate_per_100): r = -0.98, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (resource_seeking_rate_per_100): r = -0.56, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (avg_ally_proximity): r = +0.51, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (kills): r = -0.95, p = <0.001
- Paired Wilcoxon beta=0.25 vs 1 (deaths): r = -0.79, p = <0.001

## Additional experiment: designer risk budgets, normalised budget (Deathmatch)


### Survival-Aware (fixed-weight reference: main experiment)

| beta | Adherence | ExposureRatio | LengthOverhead | lambda_E | BudgetPosition | EngRedirect | ResSeek | AllyDist | Kills | Deaths |
|---|---|---|---|---|---|---|---|---|---|---|
| fixed | – | – | – | 20.00 | – | 0.00 ± 0.00 | 0.57 ± 0.06 | 7.20 ± 0.79 | 4.86 ± 0.43 | 4.65 ± 0.50 |
| 1.00 | 1.000 ± 0.000 | 0.998 ± 0.001 | 1.000 ± 0.000 | 0.001 ± 0.001 | 0.995 ± 0.002 | 0.00 ± 0.00 | 0.60 ± 0.07 | 5.81 ± 0.63 | 5.01 ± 0.47 | 5.06 ± 0.54 |
| 0.75 | 1.000 ± 0.000 | 0.622 ± 0.015 | 1.050 ± 0.007 | 0.427 ± 0.061 | 0.200 ± 0.013 | 0.00 ± 0.00 | 0.53 ± 0.06 | 6.45 ± 0.70 | 4.54 ± 0.46 | 4.21 ± 0.47 |
| 0.50 | 1.000 ± 0.000 | 0.581 ± 0.016 | 1.064 ± 0.008 | 0.589 ± 0.081 | 0.108 ± 0.008 | 0.00 ± 0.00 | 0.55 ± 0.06 | 6.64 ± 0.70 | 4.74 ± 0.44 | 4.67 ± 0.49 |
| 0.25 | 1.000 ± 0.000 | 0.521 ± 0.019 | 1.079 ± 0.008 | 0.779 ± 0.093 | 0.036 ± 0.003 | 0.00 ± 0.00 | 0.56 ± 0.06 | 7.03 ± 0.66 | 4.79 ± 0.45 | 4.66 ± 0.47 |
| 0.00 | 1.000 ± 0.000 | 0.516 ± 0.021 | 1.084 ± 0.009 | 1.008 ± 0.146 | 0.000 ± 0.000 | 0.00 ± 0.00 | 0.52 ± 0.06 | 6.86 ± 0.80 | 4.56 ± 0.43 | 4.23 ± 0.45 |

- Spearman rho(beta, exposure_ratio) = +0.70, p = <0.001
- Spearman rho(beta, length_overhead) = -0.65, p = <0.001
- Spearman rho(beta, mean_lambda) = -0.68, p = <0.001
- Spearman rho(beta, budget_position) = +0.97, p = <0.001
- Spearman rho(beta, resource_seeking_rate_per_100) = +0.06, p = 0.207
- Spearman rho(beta, avg_ally_proximity) = -0.10, p = 0.023
- Spearman rho(beta, kills) = +0.04, p = 0.359
- Spearman rho(beta, deaths) = +0.07, p = 0.111

- Paired Wilcoxon beta=0.00 vs 1 (budget_adherence): r = +0.00, p = 1.000
- Paired Wilcoxon beta=0.00 vs 1 (exposure_ratio): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (length_overhead): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (mean_lambda): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (budget_position): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (engagement_redirection_rate_per_100): r = +0.00, p = 1.000
- Paired Wilcoxon beta=0.00 vs 1 (resource_seeking_rate_per_100): r = -0.25, p = 0.035
- Paired Wilcoxon beta=0.00 vs 1 (avg_ally_proximity): r = +0.22, p = 0.056
- Paired Wilcoxon beta=0.00 vs 1 (kills): r = -0.18, p = 0.149
- Paired Wilcoxon beta=0.00 vs 1 (deaths): r = -0.31, p = 0.012

### Aggressive (fixed-weight reference: main experiment)

| beta | Adherence | ExposureRatio | LengthOverhead | lambda_E | BudgetPosition | EngRedirect | ResSeek | AllyDist | Kills | Deaths |
|---|---|---|---|---|---|---|---|---|---|---|
| fixed | – | – | – | 3.64 | – | 2.84 ± 0.10 | 0.33 ± 0.04 | 5.11 ± 0.23 | 11.86 ± 0.51 | 12.22 ± 0.49 |
| 1.00 | 1.000 ± 0.000 | 1.000 ± 0.000 | 1.000 ± 0.000 | 0.000 ± 0.000 | 0.999 ± 0.001 | 3.18 ± 0.12 | 0.37 ± 0.04 | 4.79 ± 0.26 | 13.22 ± 0.55 | 13.00 ± 0.52 |
| 0.75 | 1.000 ± 0.000 | 0.839 ± 0.006 | 1.171 ± 0.017 | 2.028 ± 0.154 | 0.213 ± 0.007 | 2.75 ± 0.12 | 0.32 ± 0.04 | 4.93 ± 0.21 | 11.61 ± 0.51 | 11.72 ± 0.53 |
| 0.50 | 1.000 ± 0.000 | 0.808 ± 0.007 | 1.246 ± 0.014 | 2.829 ± 0.142 | 0.116 ± 0.005 | 2.57 ± 0.09 | 0.29 ± 0.04 | 5.23 ± 0.21 | 10.97 ± 0.41 | 11.61 ± 0.41 |
| 0.25 | 1.000 ± 0.000 | 0.773 ± 0.008 | 1.333 ± 0.017 | 4.029 ± 0.202 | 0.038 ± 0.002 | 2.49 ± 0.09 | 0.25 ± 0.03 | 5.41 ± 0.24 | 10.08 ± 0.45 | 11.30 ± 0.43 |
| 0.00 | 1.000 ± 0.000 | 0.752 ± 0.010 | 1.404 ± 0.032 | 5.434 ± 0.352 | 0.000 ± 0.000 | 2.27 ± 0.08 | 0.22 ± 0.03 | 5.69 ± 0.23 | 9.51 ± 0.41 | 10.83 ± 0.47 |

- Spearman rho(beta, exposure_ratio) = +0.83, p = <0.001
- Spearman rho(beta, length_overhead) = -0.86, p = <0.001
- Spearman rho(beta, mean_lambda) = -0.90, p = <0.001
- Spearman rho(beta, budget_position) = +0.98, p = <0.001
- Spearman rho(beta, engagement_redirection_rate_per_100) = +0.50, p = <0.001
- Spearman rho(beta, resource_seeking_rate_per_100) = +0.29, p = <0.001
- Spearman rho(beta, avg_ally_proximity) = -0.27, p = <0.001
- Spearman rho(beta, kills) = +0.46, p = <0.001
- Spearman rho(beta, deaths) = +0.28, p = <0.001

- Paired Wilcoxon beta=0.00 vs 1 (budget_adherence): r = +0.00, p = 1.000
- Paired Wilcoxon beta=0.00 vs 1 (exposure_ratio): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (length_overhead): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (mean_lambda): r = +1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (budget_position): r = -1.00, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (engagement_redirection_rate_per_100): r = -0.97, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (resource_seeking_rate_per_100): r = -0.61, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (avg_ally_proximity): r = +0.61, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (kills): r = -0.95, p = <0.001
- Paired Wilcoxon beta=0.00 vs 1 (deaths): r = -0.73, p = <0.001
