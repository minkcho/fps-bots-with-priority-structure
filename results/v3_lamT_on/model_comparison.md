# Additive (v2) vs exponential route metric (v3: route_cost = exp, navigation weights x36.36363636363636)


## random map: primary hypothesis tests (Holm across the primary tests of each model)

| Hyp. | Test | additive: effect | additive: p_Holm | exp: effect | exp: p_Holm |
|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 82.4; eps2 = 0.68 | <0.001 | H = 87.6; eps2 = 0.73 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 22.8; eps2 = 0.17 | <0.001 | H = 27.5; eps2 = 0.21 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 72.0; eps2 = 0.59 | <0.001 | H = 75.5; eps2 = 0.63 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 107.7; eps2 = 0.90 | <0.001 | H = 80.1; eps2 = 0.66 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 61.0; eps2 = 0.50 | <0.001 | H = 72.6; eps2 = 0.60 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.80 (chance 0.25); 5-fold CV, 1000 permutations | 0.008 | accuracy = 0.73 (chance 0.25); 5-fold CV, 1000 permutations | 0.007 |
| H1 | Style classification, Deathmatch | accuracy = 0.83 (chance 0.25); 5-fold CV, 1000 permutations | 0.008 | accuracy = 0.87 (chance 0.25); 5-fold CV, 1000 permutations | 0.007 |
| H1 | Style classification, Control | accuracy = 0.72 (chance 0.25); 5-fold CV, 1000 permutations | 0.008 | accuracy = 0.71 (chance 0.25); 5-fold CV, 1000 permutations | 0.007 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.39 [+0.29, +0.63]; r = +1.00 | <0.001 | median diff = +0.39 [+0.24, +0.50]; r = +0.97 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +0.56 [+0.03, +0.91]; r = +0.60 | 0.021 | median diff = +0.55 [+0.33, +0.81]; r = +0.93 | <0.001 |
| H2 | Mission ObjCommit, w_commit 0.45 - 0 | median diff = +0.28 [+0.21, +1.00]; r = +1.00 | <0.001 | median diff = +0.02 [+0.01, +0.06]; r = +0.54 | 0.042 |
| H2 | Control CtrlScore, w_commit 0.45 - 0 | median diff = +120.00 [+104.00, +120.00]; r = +1.00 | <0.001 | median diff = +0.00 [+0.00, +0.00]; r = +0.52 | 0.562 |
| H3 | Deathmatch Survival-Aware EngRedirect, lambda x1 - x0 | median diff = -0.09 [-0.37, +0.00]; r = -0.44 | 0.093 | median diff = -0.70 [-1.33, -0.39]; r = -0.68 | 0.005 |
| H3 | Mission Mission–Cooperation AllyDist, lambda x1 - x0 | median diff = +0.00 [+0.00, +0.00]; r = -0.20 | 0.625 | median diff = +0.00 [-0.01, +0.01]; r = -0.14 | 0.596 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.23; n = 150 | 0.021 | rho = +0.12; n = 150 | 0.446 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.22; n = 150 | 0.023 | rho = -0.51; n = 150 | <0.001 |

## random map: main experiment, exp vs additive (paired by seed; Holm within condition)

| Scenario | Style | Metric | additive | exp | r | p_Holm |
|---|---|---|---|---|---|---|
| Mission | Mission–Cooperation | ObjCommit | 0.56 ± 0.16 | 0.95 ± 0.02 | +0.59 | 0.010 |
| Mission | Mission–Cooperation | AllyDist | 1.19 ± 0.08 | 1.91 ± 0.32 | +0.81 | <0.001 |
| Mission | Mission–Cooperation | EngRedirect | 0.02 ± 0.03 | 0.00 ± 0.00 | -1.00 | 1.000 |
| Mission | Mission–Cooperation | Deaths | 1.90 ± 0.87 | 4.20 ± 1.40 | +0.75 | 0.005 |
| Mission | Persistent Objective | ObjCommit | 0.74 ± 0.08 | 0.90 ± 0.04 | +0.69 | 0.004 |
| Mission | Persistent Objective | AllyDist | 2.54 ± 0.67 | 2.50 ± 0.51 | +0.06 | 1.000 |
| Mission | Persistent Objective | EngRedirect | 0.01 ± 0.01 | 0.00 ± 0.01 | -0.33 | 1.000 |
| Mission | Persistent Objective | Deaths | 6.30 ± 2.36 | 4.87 ± 1.58 | -0.32 | 0.525 |
| Mission | Aggressive | ObjCommit | 0.11 ± 0.08 | 0.20 ± 0.11 | +0.64 | 0.032 |
| Mission | Aggressive | AllyDist | 2.29 ± 0.45 | 3.84 ± 0.78 | +0.70 | 0.002 |
| Mission | Aggressive | EngRedirect | 0.68 ± 0.23 | 0.86 ± 0.19 | +0.34 | 0.221 |
| Mission | Aggressive | Deaths | 5.37 ± 1.76 | 6.83 ± 1.49 | +0.35 | 0.221 |
| Mission | Survival-Aware | ObjCommit | 0.00 ± 0.00 | 0.02 ± 0.02 | +0.72 | 0.081 |
| Mission | Survival-Aware | AllyDist | 2.53 ± 0.75 | 4.52 ± 1.01 | +0.61 | 0.011 |
| Mission | Survival-Aware | EngRedirect | 0.52 ± 0.27 | 0.52 ± 0.18 | +0.04 | 1.000 |
| Mission | Survival-Aware | Deaths | 3.93 ± 1.52 | 3.27 ± 0.73 | -0.11 | 1.000 |
| Deathmatch | Mission–Cooperation | EngRedirect | 0.12 ± 0.08 | 0.19 ± 0.10 | +0.25 | 0.706 |
| Deathmatch | Mission–Cooperation | ResSeek | 0.00 ± 0.00 | 0.06 ± 0.03 | +1.00 | 0.002 |
| Deathmatch | Mission–Cooperation | AllyDist | 1.26 ± 0.10 | 2.09 ± 0.34 | +0.82 | <0.001 |
| Deathmatch | Mission–Cooperation | Kills | 4.50 ± 1.48 | 5.73 ± 1.54 | +0.26 | 0.706 |
| Deathmatch | Mission–Cooperation | Deaths | 3.73 ± 1.13 | 4.53 ± 1.10 | +0.24 | 0.706 |
| Deathmatch | Persistent Objective | EngRedirect | 0.12 ± 0.07 | 0.06 ± 0.04 | -0.43 | 0.575 |
| Deathmatch | Persistent Objective | ResSeek | 0.00 ± 0.01 | 0.00 ± 0.01 | -0.33 | 1.000 |
| Deathmatch | Persistent Objective | AllyDist | 2.30 ± 0.48 | 5.29 ± 0.69 | +0.95 | <0.001 |
| Deathmatch | Persistent Objective | Kills | 7.80 ± 1.97 | 8.70 ± 0.91 | +0.28 | 0.575 |
| Deathmatch | Persistent Objective | Deaths | 5.50 ± 1.48 | 4.77 ± 0.81 | -0.19 | 0.828 |
| Deathmatch | Aggressive | EngRedirect | 1.45 ± 0.28 | 1.33 ± 0.19 | -0.16 | 1.000 |
| Deathmatch | Aggressive | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Deathmatch | Aggressive | AllyDist | 3.11 ± 0.60 | 4.15 ± 0.62 | +0.55 | 0.038 |
| Deathmatch | Aggressive | Kills | 10.90 ± 1.91 | 10.10 ± 1.38 | -0.16 | 1.000 |
| Deathmatch | Aggressive | Deaths | 10.50 ± 1.78 | 10.03 ± 1.38 | -0.03 | 1.000 |
| Deathmatch | Survival-Aware | EngRedirect | 0.65 ± 0.24 | 0.69 ± 0.21 | +0.14 | 1.000 |
| Deathmatch | Survival-Aware | ResSeek | 0.54 ± 0.17 | 0.41 ± 0.10 | -0.16 | 1.000 |
| Deathmatch | Survival-Aware | AllyDist | 2.20 ± 0.75 | 3.43 ± 0.50 | +0.68 | 0.003 |
| Deathmatch | Survival-Aware | Kills | 5.20 ± 1.64 | 4.23 ± 1.09 | -0.12 | 1.000 |
| Deathmatch | Survival-Aware | Deaths | 4.47 ± 1.24 | 3.50 ± 0.77 | -0.24 | 1.000 |
| Control | Mission–Cooperation | CtrlScore | 94.43 ± 15.99 | 114.23 ± 8.83 | +0.56 | 0.275 |
| Control | Mission–Cooperation | ObjCommit | 0.73 ± 0.13 | 0.96 ± 0.01 | +0.57 | 0.027 |
| Control | Mission–Cooperation | AllyDist | 1.73 ± 0.31 | 1.69 ± 0.32 | -0.04 | 0.858 |
| Control | Mission–Cooperation | Deaths | 1.33 ± 0.56 | 1.07 ± 0.47 | -0.22 | 0.830 |
| Control | Persistent Objective | CtrlScore | 109.57 ± 12.18 | 118.23 ± 3.61 | +0.80 | 0.500 |
| Control | Persistent Objective | ObjCommit | 0.77 ± 0.11 | 0.90 ± 0.07 | +0.53 | 0.043 |
| Control | Persistent Objective | AllyDist | 2.83 ± 0.65 | 2.77 ± 1.04 | -0.21 | 0.500 |
| Control | Persistent Objective | Deaths | 3.00 ± 1.41 | 1.53 ± 0.66 | -0.56 | 0.096 |
| Control | Aggressive | CtrlScore | 44.73 ± 20.55 | 39.70 ± 20.16 | -0.07 | 1.000 |
| Control | Aggressive | ObjCommit | 0.16 ± 0.10 | 0.17 ± 0.09 | +0.09 | 1.000 |
| Control | Aggressive | AllyDist | 2.52 ± 0.62 | 3.87 ± 0.59 | +0.61 | 0.013 |
| Control | Aggressive | Deaths | 6.00 ± 1.98 | 6.43 ± 1.60 | +0.09 | 1.000 |
| Control | Survival-Aware | CtrlScore | 6.37 ± 8.60 | 16.43 ± 14.74 | +0.56 | 0.215 |
| Control | Survival-Aware | ObjCommit | 0.02 ± 0.04 | 0.03 ± 0.03 | +0.16 | 0.734 |
| Control | Survival-Aware | AllyDist | 2.44 ± 0.69 | 4.38 ± 1.13 | +0.57 | 0.023 |
| Control | Survival-Aware | Deaths | 4.17 ± 0.88 | 2.27 ± 0.85 | -0.63 | 0.023 |

Control wins (additive -> exp): Mission–Cooperation: 20 -> 28; Persistent Objective: 27 -> 29; Aggressive: 9 -> 8; Survival-Aware: 1 -> 3

## random map: exp-model lambda-scale sweep (k relative to the new defaults; x1 = defaults)


### Mission / Mission–Cooperation

| k | AllyDist | EngRedirect | Deaths | Kills |
|---|---|---|---|---|
| x0 | 2.04 ± 0.35 | 0.00 ± 0.00 | 4.80 ± 1.49 | 6.80 ± 2.04 |
| x0.25 | 1.95 ± 0.30 | 0.00 ± 0.01 | 4.47 ± 1.37 | 5.53 ± 1.63 |
| x0.5 | 1.94 ± 0.30 | 0.01 ± 0.01 | 4.47 ± 1.39 | 6.03 ± 1.81 |
| x1 | 1.91 ± 0.32 | 0.00 ± 0.00 | 4.20 ± 1.40 | 5.37 ± 1.64 |
| x2 | 1.89 ± 0.31 | 0.00 ± 0.00 | 3.97 ± 1.28 | 5.27 ± 1.62 |
- Spearman rho(k, AllyDist) = -0.04, p = 0.651
- Spearman rho(k, EngRedirect) = -0.03, p = 0.685
- Spearman rho(k, Deaths) = -0.08, p = 0.350
- Spearman rho(k, Kills) = -0.10, p = 0.223

### Deathmatch / Survival-Aware

| k | AllyDist | EngRedirect | Deaths | Kills |
|---|---|---|---|---|
| x0 | 3.42 ± 0.63 | 1.71 ± 0.60 | 6.97 ± 1.10 | 8.17 ± 1.34 |
| x0.25 | 4.07 ± 0.61 | 1.39 ± 0.74 | 4.60 ± 0.94 | 6.33 ± 1.17 |
| x0.5 | 3.87 ± 0.53 | 0.79 ± 0.18 | 4.07 ± 0.73 | 5.33 ± 0.88 |
| x1 | 3.43 ± 0.50 | 0.69 ± 0.21 | 3.50 ± 0.77 | 4.23 ± 1.09 |
| x2 | 4.09 ± 0.64 | 0.58 ± 0.16 | 3.87 ± 0.95 | 5.00 ± 1.27 |
- Spearman rho(k, AllyDist) = +0.09, p = 0.298
- Spearman rho(k, EngRedirect) = -0.35, p = <0.001
- Spearman rho(k, Deaths) = -0.36, p = <0.001
- Spearman rho(k, Kills) = -0.34, p = <0.001

## urban map: primary hypothesis tests (Holm across the primary tests of each model)

| Hyp. | Test | additive: effect | additive: p_Holm | exp: effect | exp: p_Holm |
|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 78.0; eps2 = 0.65 | <0.001 | H = 75.8; eps2 = 0.63 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 21.2; eps2 = 0.16 | <0.001 | H = 38.4; eps2 = 0.31 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 59.9; eps2 = 0.49 | <0.001 | H = 72.1; eps2 = 0.60 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 100.2; eps2 = 0.84 | <0.001 | H = 71.8; eps2 = 0.59 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 81.0; eps2 = 0.67 | <0.001 | H = 82.1; eps2 = 0.68 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.80 (chance 0.25); 5-fold CV, 1000 permutations | 0.008 | accuracy = 0.72 (chance 0.25); 5-fold CV, 1000 permutations | 0.009 |
| H1 | Style classification, Deathmatch | accuracy = 0.87 (chance 0.25); 5-fold CV, 1000 permutations | 0.008 | accuracy = 0.80 (chance 0.25); 5-fold CV, 1000 permutations | 0.009 |
| H1 | Style classification, Control | accuracy = 0.72 (chance 0.25); 5-fold CV, 1000 permutations | 0.008 | accuracy = 0.77 (chance 0.25); 5-fold CV, 1000 permutations | 0.009 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.45 [+0.29, +0.83]; r = +0.98 | <0.001 | median diff = +0.34 [+0.23, +0.60]; r = +0.98 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +0.18 [-0.00, +0.60]; r = +0.35 | 0.233 | median diff = +0.60 [+0.25, +0.74]; r = +0.81 | <0.001 |
| H2 | Mission ObjCommit, w_commit 0.45 - 0 | median diff = +0.84 [+0.29, +0.98]; r = +1.00 | <0.001 | median diff = +0.02 [+0.01, +0.02]; r = +0.56 | 0.036 |
| H2 | Control CtrlScore, w_commit 0.45 - 0 | median diff = +120.00 [+120.00, +120.00]; r = +1.00 | <0.001 | median diff = +0.00 [+0.00, +0.00]; r = +1.00 | 0.750 |
| H3 | Deathmatch Survival-Aware EngRedirect, lambda x1 - x0 | median diff = +0.09 [+0.00, +0.51]; r = +0.50 | 0.089 | median diff = -0.19 [-0.45, -0.06]; r = -0.54 | 0.037 |
| H3 | Mission Mission–Cooperation AllyDist, lambda x1 - x0 | median diff = +0.01 [+0.01, +0.03]; r = +0.59 | 0.022 | median diff = +0.00 [-0.00, +0.01]; r = +0.23 | 0.750 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.20; n = 150 | 0.053 | rho = +0.09; n = 150 | 0.750 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.11; n = 150 | 0.233 | rho = -0.27; n = 150 | 0.009 |

## urban map: main experiment, exp vs additive (paired by seed; Holm within condition)

| Scenario | Style | Metric | additive | exp | r | p_Holm |
|---|---|---|---|---|---|---|
| Mission | Mission–Cooperation | ObjCommit | 0.61 ± 0.15 | 0.95 ± 0.03 | +0.62 | 0.012 |
| Mission | Mission–Cooperation | AllyDist | 1.38 ± 0.23 | 1.56 ± 0.30 | -0.08 | 1.000 |
| Mission | Mission–Cooperation | EngRedirect | 0.00 ± 0.01 | 0.01 ± 0.02 | +0.67 | 1.000 |
| Mission | Mission–Cooperation | Deaths | 2.57 ± 1.03 | 3.07 ± 1.77 | -0.02 | 1.000 |
| Mission | Persistent Objective | ObjCommit | 0.60 ± 0.11 | 0.82 ± 0.12 | +0.65 | 0.011 |
| Mission | Persistent Objective | AllyDist | 2.19 ± 0.50 | 2.84 ± 1.43 | -0.05 | 1.000 |
| Mission | Persistent Objective | EngRedirect | 0.00 ± 0.01 | 0.00 ± 0.00 | -1.00 | 1.000 |
| Mission | Persistent Objective | Deaths | 5.70 ± 2.14 | 1.77 ± 1.09 | -0.69 | 0.011 |
| Mission | Aggressive | ObjCommit | 0.07 ± 0.05 | 0.16 ± 0.11 | +0.50 | 0.250 |
| Mission | Aggressive | AllyDist | 2.31 ± 0.51 | 3.20 ± 0.80 | +0.48 | 0.083 |
| Mission | Aggressive | EngRedirect | 0.72 ± 0.25 | 0.59 ± 0.17 | -0.29 | 0.250 |
| Mission | Aggressive | Deaths | 5.83 ± 1.83 | 4.80 ± 1.50 | -0.37 | 0.250 |
| Mission | Survival-Aware | ObjCommit | 0.00 ± 0.00 | 0.08 ± 0.08 | +0.96 | 0.012 |
| Mission | Survival-Aware | AllyDist | 2.29 ± 0.56 | 4.36 ± 0.87 | +0.82 | <0.001 |
| Mission | Survival-Aware | EngRedirect | 0.30 ± 0.11 | 0.29 ± 0.08 | +0.03 | 0.902 |
| Mission | Survival-Aware | Deaths | 3.97 ± 1.42 | 2.70 ± 0.69 | -0.34 | 0.265 |
| Deathmatch | Mission–Cooperation | EngRedirect | 0.21 ± 0.09 | 0.20 ± 0.11 | -0.14 | 1.000 |
| Deathmatch | Mission–Cooperation | ResSeek | 0.00 ± 0.00 | 0.21 ± 0.36 | +1.00 | 0.031 |
| Deathmatch | Mission–Cooperation | AllyDist | 1.22 ± 0.11 | 2.08 ± 0.25 | +0.86 | <0.001 |
| Deathmatch | Mission–Cooperation | Kills | 6.10 ± 2.03 | 6.90 ± 1.77 | +0.16 | 1.000 |
| Deathmatch | Mission–Cooperation | Deaths | 5.43 ± 1.55 | 5.63 ± 1.50 | +0.05 | 1.000 |
| Deathmatch | Persistent Objective | EngRedirect | 0.06 ± 0.04 | 0.05 ± 0.03 | -0.22 | 1.000 |
| Deathmatch | Persistent Objective | ResSeek | 0.01 ± 0.01 | 0.00 ± 0.00 | -1.00 | 1.000 |
| Deathmatch | Persistent Objective | AllyDist | 2.56 ± 0.48 | 4.59 ± 0.71 | +0.84 | <0.001 |
| Deathmatch | Persistent Objective | Kills | 7.90 ± 1.77 | 7.60 ± 0.90 | -0.07 | 1.000 |
| Deathmatch | Persistent Objective | Deaths | 4.87 ± 1.13 | 4.00 ± 0.81 | -0.26 | 0.854 |
| Deathmatch | Aggressive | EngRedirect | 1.28 ± 0.29 | 1.01 ± 0.15 | -0.39 | 0.254 |
| Deathmatch | Aggressive | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Deathmatch | Aggressive | AllyDist | 2.64 ± 0.55 | 4.43 ± 0.82 | +0.75 | <0.001 |
| Deathmatch | Aggressive | Kills | 9.60 ± 2.03 | 8.53 ± 1.46 | -0.19 | 0.760 |
| Deathmatch | Aggressive | Deaths | 9.53 ± 1.84 | 8.37 ± 1.34 | -0.30 | 0.437 |
| Deathmatch | Survival-Aware | EngRedirect | 0.61 ± 0.23 | 0.38 ± 0.11 | -0.29 | 0.275 |
| Deathmatch | Survival-Aware | ResSeek | 0.64 ± 0.19 | 0.45 ± 0.12 | -0.32 | 0.275 |
| Deathmatch | Survival-Aware | AllyDist | 2.65 ± 0.58 | 4.83 ± 0.91 | +0.74 | <0.001 |
| Deathmatch | Survival-Aware | Kills | 6.33 ± 1.78 | 4.13 ± 1.00 | -0.42 | 0.189 |
| Deathmatch | Survival-Aware | Deaths | 5.43 ± 1.44 | 3.33 ± 0.83 | -0.48 | 0.100 |
| Control | Mission–Cooperation | CtrlScore | 99.37 ± 15.06 | 120.00 ± 0.00 | +1.00 | 0.062 |
| Control | Mission–Cooperation | ObjCommit | 0.80 ± 0.12 | 0.96 ± 0.02 | +0.32 | 0.387 |
| Control | Mission–Cooperation | AllyDist | 1.58 ± 0.26 | 1.49 ± 0.26 | -0.16 | 0.952 |
| Control | Mission–Cooperation | Deaths | 1.10 ± 0.51 | 1.40 ± 1.08 | +0.02 | 0.965 |
| Control | Persistent Objective | CtrlScore | 112.00 ± 11.37 | 119.03 ± 1.98 | +0.67 | 1.000 |
| Control | Persistent Objective | ObjCommit | 0.77 ± 0.11 | 0.88 ± 0.08 | +0.44 | 0.139 |
| Control | Persistent Objective | AllyDist | 2.38 ± 0.65 | 2.57 ± 0.85 | +0.11 | 1.000 |
| Control | Persistent Objective | Deaths | 2.27 ± 0.98 | 1.50 ± 0.78 | -0.51 | 0.206 |
| Control | Aggressive | CtrlScore | 24.23 ± 17.60 | 36.10 ± 20.33 | +0.35 | 0.605 |
| Control | Aggressive | ObjCommit | 0.09 ± 0.08 | 0.16 ± 0.09 | +0.38 | 0.502 |
| Control | Aggressive | AllyDist | 2.42 ± 0.53 | 4.33 ± 0.98 | +0.74 | <0.001 |
| Control | Aggressive | Deaths | 5.63 ± 1.98 | 4.87 ± 1.35 | -0.07 | 0.770 |
| Control | Survival-Aware | CtrlScore | 0.03 ± 0.07 | 14.10 ± 13.55 | +0.94 | 0.047 |
| Control | Survival-Aware | ObjCommit | 0.00 ± 0.00 | 0.04 ± 0.05 | +1.00 | 0.047 |
| Control | Survival-Aware | AllyDist | 2.62 ± 0.88 | 4.98 ± 1.20 | +0.66 | 0.004 |
| Control | Survival-Aware | Deaths | 3.37 ± 1.22 | 2.60 ± 0.81 | -0.21 | 0.334 |

Control wins (additive -> exp): Mission–Cooperation: 23 -> 30; Persistent Objective: 28 -> 29; Aggressive: 5 -> 8; Survival-Aware: 0 -> 2

## urban map: exp-model lambda-scale sweep (k relative to the new defaults; x1 = defaults)


### Mission / Mission–Cooperation

| k | AllyDist | EngRedirect | Deaths | Kills |
|---|---|---|---|---|
| x0 | 1.47 ± 0.30 | 0.00 ± 0.00 | 2.77 ± 1.56 | 3.07 ± 1.70 |
| x0.25 | 1.46 ± 0.25 | 0.00 ± 0.01 | 2.73 ± 1.44 | 3.43 ± 1.85 |
| x0.5 | 1.70 ± 0.41 | 0.01 ± 0.02 | 3.07 ± 1.64 | 3.53 ± 1.95 |
| x1 | 1.56 ± 0.30 | 0.01 ± 0.02 | 3.07 ± 1.77 | 3.17 ± 1.73 |
| x2 | 1.53 ± 0.28 | 0.01 ± 0.02 | 2.83 ± 1.62 | 2.83 ± 1.55 |
- Spearman rho(k, AllyDist) = -0.01, p = 0.937
- Spearman rho(k, EngRedirect) = +0.11, p = 0.166
- Spearman rho(k, Deaths) = -0.01, p = 0.939
- Spearman rho(k, Kills) = -0.01, p = 0.886

### Deathmatch / Survival-Aware

| k | AllyDist | EngRedirect | Deaths | Kills |
|---|---|---|---|---|
| x0 | 4.23 ± 0.69 | 0.67 ± 0.17 | 6.20 ± 1.07 | 7.50 ± 1.27 |
| x0.25 | 4.23 ± 0.82 | 0.57 ± 0.17 | 4.03 ± 0.93 | 5.37 ± 1.18 |
| x0.5 | 3.95 ± 0.65 | 0.45 ± 0.15 | 3.13 ± 0.92 | 3.93 ± 1.10 |
| x1 | 4.83 ± 0.91 | 0.38 ± 0.11 | 3.33 ± 0.83 | 4.13 ± 1.00 |
| x2 | 4.66 ± 0.80 | 0.41 ± 0.13 | 2.97 ± 0.76 | 3.80 ± 0.92 |
- Spearman rho(k, AllyDist) = +0.10, p = 0.234
- Spearman rho(k, EngRedirect) = -0.24, p = 0.003
- Spearman rho(k, Deaths) = -0.36, p = <0.001
- Spearman rho(k, Kills) = -0.36, p = <0.001
