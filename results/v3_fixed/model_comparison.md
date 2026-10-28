# v2 (additive route cost) vs v3 main model (exp route metric over the expected-hits field, lambda_E x36.36, lambda_T = 0, goal termination, separated spawns, evade hysteresis)


## random map: primary hypothesis tests (Holm across the primary tests of each model)


### additive (v2)

| Hyp. | Test | Statistic; effect | p_Holm |
|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 82.4; eps2 = 0.68 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 22.8; eps2 = 0.17 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 72.0; eps2 = 0.59 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 107.7; eps2 = 0.90 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 61.0; eps2 = 0.50 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.80 (chance 0.25); 5-fold CV, 1000 permutations | 0.008 |
| H1 | Style classification, Deathmatch | accuracy = 0.83 (chance 0.25); 5-fold CV, 1000 permutations | 0.008 |
| H1 | Style classification, Control | accuracy = 0.72 (chance 0.25); 5-fold CV, 1000 permutations | 0.008 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.39 [+0.29, +0.63]; r = +1.00 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +0.56 [+0.03, +0.91]; r = +0.60 | 0.021 |
| H2 | Mission ObjCommit, w_commit 0.45 - 0 | median diff = +0.28 [+0.21, +1.00]; r = +1.00 | <0.001 |
| H2 | Control CtrlScore, w_commit 0.45 - 0 | median diff = +120.00 [+104.00, +120.00]; r = +1.00 | <0.001 |
| H3 | Deathmatch Survival-Aware EngRedirect, lambda x1 - x0 | median diff = -0.09 [-0.37, +0.00]; r = -0.44 | 0.093 |
| H3 | Mission Mission–Cooperation AllyDist, lambda x1 - x0 | median diff = +0.00 [+0.00, +0.00]; r = -0.20 | 0.625 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.23; n = 150 | 0.021 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.22; n = 150 | 0.023 |

### exp (v3)

| Hyp. | Test | Statistic; effect | p_Holm |
|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 281.7; eps2 = 0.70 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 160.1; eps2 = 0.40 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 343.6; eps2 = 0.86 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 211.8; eps2 = 0.53 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 234.7; eps2 = 0.59 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.75 (chance 0.25); 5-fold CV, 1000 permutations | 0.005 |
| H1 | Style classification, Deathmatch | accuracy = 0.98 (chance 0.25); 5-fold CV, 1000 permutations | 0.005 |
| H1 | Style classification, Control | accuracy = 0.74 (chance 0.25); 5-fold CV, 1000 permutations | 0.005 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.51 [+0.39, +0.61]; r = +0.95 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +1.43 [+1.28, +1.54]; r = +1.00 | <0.001 |
| H2 | Mission GoalSwitches, w_commit 0.45 - 0 | median diff = -20.39 [-24.15, -13.52]; r = -1.00 | <0.001 |
| H2 | Control GoalSwitches, w_commit 0.45 - 0 | median diff = -21.39 [-24.78, -20.06]; r = -1.00 | <0.001 |
| H3 | Deathmatch Mission–Cooperation WalkedHits, lambda_E configured - 0 | median diff = -0.0097 [-0.0136, -0.0017]; r = -0.39 | 0.004 |
| H3 | Deathmatch Persistent Objective WalkedHits, lambda_E configured - 0 | median diff = -0.0214 [-0.0267, -0.0154]; r = -0.96 | <0.001 |
| H3 | Deathmatch Aggressive WalkedHits, lambda_E configured - 0 | median diff = -0.0150 [-0.0185, -0.0125]; r = -0.77 | <0.001 |
| H3 | Deathmatch Survival-Aware WalkedHits, lambda_E configured - 0 | median diff = -0.0026 [-0.0072, +0.0015]; r = -0.15 | 0.179 |
| H3 | Sign test, WalkedHits lower with the exposure term (all scenarios x styles) | 12/12 conditions lower; one-sided binomial | 0.002 |
| H3b | Deathmatch Mission–Cooperation AllyDist, lambda_T 10 - 0 | median diff = -0.31 [-0.49, -0.11]; r = -0.53 | <0.001 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.15; n = 500 | 0.005 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.70; n = 500 | <0.001 |

## random map: main experiment, exp vs additive (paired by seed on the 30 common episodes; Holm within condition)

| Scenario | Style | Metric | additive | exp | r | p_Holm |
|---|---|---|---|---|---|---|
| Mission | Mission–Cooperation | ObjCommit | 0.56 ± 0.16 | 0.93 ± 0.02 | +0.55 | 0.017 |
| Mission | Mission–Cooperation | AllyDist | 1.19 ± 0.08 | 2.32 ± 0.37 | +0.96 | <0.001 |
| Mission | Mission–Cooperation | EngRedirect | 0.02 ± 0.03 | 0.00 ± 0.01 | -0.33 | 1.000 |
| Mission | Mission–Cooperation | Deaths | 1.90 ± 0.87 | 5.60 ± 1.51 | +0.97 | <0.001 |
| Mission | Persistent Objective | ObjCommit | 0.74 ± 0.08 | 0.90 ± 0.03 | +0.66 | 0.006 |
| Mission | Persistent Objective | AllyDist | 2.54 ± 0.67 | 3.10 ± 0.75 | +0.29 | 0.495 |
| Mission | Persistent Objective | EngRedirect | 0.01 ± 0.01 | 0.01 ± 0.01 | +0.00 | 1.000 |
| Mission | Persistent Objective | Deaths | 6.30 ± 2.36 | 5.47 ± 1.63 | -0.26 | 0.606 |
| Mission | Aggressive | ObjCommit | 0.11 ± 0.08 | 0.32 ± 0.10 | +0.85 | <0.001 |
| Mission | Aggressive | AllyDist | 2.29 ± 0.45 | 5.04 ± 0.63 | +0.95 | <0.001 |
| Mission | Aggressive | EngRedirect | 0.68 ± 0.23 | 1.57 ± 0.33 | +0.78 | <0.001 |
| Mission | Aggressive | Deaths | 5.37 ± 1.76 | 7.00 ± 1.44 | +0.50 | 0.021 |
| Mission | Survival-Aware | ObjCommit | 0.00 ± 0.00 | 0.02 ± 0.01 | +0.70 | 0.041 |
| Mission | Survival-Aware | AllyDist | 2.53 ± 0.75 | 6.98 ± 1.57 | +0.85 | <0.001 |
| Mission | Survival-Aware | EngRedirect | 0.52 ± 0.27 | 0.00 ± 0.00 | -1.00 | <0.001 |
| Mission | Survival-Aware | Deaths | 3.93 ± 1.52 | 3.07 ± 0.96 | -0.13 | 0.547 |
| Deathmatch | Mission–Cooperation | EngRedirect | 0.12 ± 0.08 | 0.44 ± 0.12 | +0.93 | <0.001 |
| Deathmatch | Mission–Cooperation | ResSeek | 0.00 ± 0.00 | 0.22 ± 0.08 | +1.00 | <0.001 |
| Deathmatch | Mission–Cooperation | AllyDist | 1.26 ± 0.10 | 2.95 ± 0.16 | +1.00 | <0.001 |
| Deathmatch | Mission–Cooperation | Kills | 4.50 ± 1.48 | 10.30 ± 0.95 | +0.90 | <0.001 |
| Deathmatch | Mission–Cooperation | Deaths | 3.73 ± 1.13 | 9.27 ± 0.80 | +0.96 | <0.001 |
| Deathmatch | Persistent Objective | EngRedirect | 0.12 ± 0.07 | 0.07 ± 0.03 | -0.23 | 0.660 |
| Deathmatch | Persistent Objective | ResSeek | 0.00 ± 0.01 | 0.02 ± 0.02 | +0.90 | 0.250 |
| Deathmatch | Persistent Objective | AllyDist | 2.30 ± 0.48 | 5.84 ± 0.65 | +0.99 | <0.001 |
| Deathmatch | Persistent Objective | Kills | 7.80 ± 1.97 | 9.53 ± 0.85 | +0.39 | 0.250 |
| Deathmatch | Persistent Objective | Deaths | 5.50 ± 1.48 | 5.33 ± 0.82 | +0.02 | 0.939 |
| Deathmatch | Aggressive | EngRedirect | 1.45 ± 0.28 | 2.86 ± 0.21 | +0.98 | <0.001 |
| Deathmatch | Aggressive | ResSeek | 0.00 ± 0.00 | 0.27 ± 0.06 | +1.00 | <0.001 |
| Deathmatch | Aggressive | AllyDist | 3.11 ± 0.60 | 5.37 ± 0.48 | +0.94 | <0.001 |
| Deathmatch | Aggressive | Kills | 10.90 ± 1.91 | 11.37 ± 0.95 | +0.13 | 0.553 |
| Deathmatch | Aggressive | Deaths | 10.50 ± 1.78 | 12.37 ± 1.08 | +0.38 | 0.154 |
| Deathmatch | Survival-Aware | EngRedirect | 0.65 ± 0.24 | 0.00 ± 0.00 | -1.00 | <0.001 |
| Deathmatch | Survival-Aware | ResSeek | 0.54 ± 0.17 | 0.52 ± 0.12 | +0.03 | 1.000 |
| Deathmatch | Survival-Aware | AllyDist | 2.20 ± 0.75 | 7.17 ± 1.33 | +0.91 | <0.001 |
| Deathmatch | Survival-Aware | Kills | 5.20 ± 1.64 | 4.53 ± 0.91 | -0.03 | 1.000 |
| Deathmatch | Survival-Aware | Deaths | 4.47 ± 1.24 | 4.17 ± 0.94 | -0.01 | 1.000 |
| Control | Mission–Cooperation | CtrlScore | 94.43 ± 15.99 | 117.43 ± 5.25 | +0.82 | 0.041 |
| Control | Mission–Cooperation | ObjCommit | 0.73 ± 0.13 | 0.96 ± 0.02 | +0.58 | 0.022 |
| Control | Mission–Cooperation | AllyDist | 1.73 ± 0.31 | 1.95 ± 0.32 | +0.29 | 0.214 |
| Control | Mission–Cooperation | Deaths | 1.33 ± 0.56 | 0.90 ± 0.51 | -0.41 | 0.214 |
| Control | Persistent Objective | CtrlScore | 109.57 ± 12.18 | 113.80 ± 8.61 | +0.33 | 1.000 |
| Control | Persistent Objective | ObjCommit | 0.77 ± 0.11 | 0.89 ± 0.07 | +0.57 | 0.023 |
| Control | Persistent Objective | AllyDist | 2.83 ± 0.65 | 2.88 ± 0.82 | +0.07 | 1.000 |
| Control | Persistent Objective | Deaths | 3.00 ± 1.41 | 1.47 ± 0.82 | -0.72 | 0.025 |
| Control | Aggressive | CtrlScore | 44.73 ± 20.55 | 75.67 ± 21.01 | +0.41 | 0.203 |
| Control | Aggressive | ObjCommit | 0.16 ± 0.10 | 0.35 ± 0.12 | +0.64 | 0.007 |
| Control | Aggressive | AllyDist | 2.52 ± 0.62 | 4.22 ± 0.68 | +0.66 | 0.004 |
| Control | Aggressive | Deaths | 6.00 ± 1.98 | 4.43 ± 1.57 | -0.28 | 0.203 |
| Control | Survival-Aware | CtrlScore | 6.37 ± 8.60 | 17.27 ± 14.14 | +0.33 | 0.542 |
| Control | Survival-Aware | ObjCommit | 0.02 ± 0.04 | 0.03 ± 0.03 | +0.27 | 0.542 |
| Control | Survival-Aware | AllyDist | 2.44 ± 0.69 | 6.53 ± 1.06 | +0.94 | <0.001 |
| Control | Survival-Aware | Deaths | 4.17 ± 0.88 | 2.93 ± 0.92 | -0.44 | 0.108 |

Control wins (additive -> exp): Mission–Cooperation: 20 -> 29; Persistent Objective: 27 -> 27; Aggressive: 9 -> 17; Survival-Aware: 1 -> 3

## random map: exp-model lambda-scale sweep (k relative to the new defaults; x1 = defaults)


### Mission / Mission–Cooperation

| k | AllyDist | EngRedirect | Deaths | Kills |
|---|---|---|---|---|
| x0 | 2.09 ± 0.20 | 0.01 ± 0.02 | 5.26 ± 0.85 | 6.55 ± 0.97 |
| x0.25 | 2.13 ± 0.21 | 0.01 ± 0.01 | 5.17 ± 0.85 | 6.70 ± 1.01 |
| x0.5 | 2.12 ± 0.20 | 0.01 ± 0.01 | 4.96 ± 0.82 | 6.40 ± 0.96 |
| x1 | 2.08 ± 0.18 | 0.01 ± 0.01 | 5.06 ± 0.82 | 6.25 ± 0.94 |
| x2 | 2.09 ± 0.19 | 0.01 ± 0.01 | 5.12 ± 0.84 | 6.36 ± 0.94 |
- Spearman rho(k, AllyDist) = +0.01, p = 0.860
- Spearman rho(k, EngRedirect) = +0.01, p = 0.901
- Spearman rho(k, Deaths) = -0.01, p = 0.775
- Spearman rho(k, Kills) = -0.04, p = 0.410

### Deathmatch / Survival-Aware

| k | AllyDist | EngRedirect | Deaths | Kills |
|---|---|---|---|---|
| x0 | 5.68 ± 0.56 | 0.00 ± 0.00 | 4.93 ± 0.49 | 4.93 ± 0.43 |
| x0.25 | 6.82 ± 0.64 | 0.00 ± 0.00 | 4.60 ± 0.48 | 4.94 ± 0.44 |
| x0.5 | 7.08 ± 0.78 | 0.00 ± 0.00 | 4.90 ± 0.49 | 4.53 ± 0.43 |
| x1 | 7.20 ± 0.79 | 0.00 ± 0.00 | 4.65 ± 0.50 | 4.86 ± 0.43 |
| x2 | 6.81 ± 0.70 | 0.00 ± 0.00 | 4.45 ± 0.50 | 4.82 ± 0.44 |
- Spearman rho(k, AllyDist) = +0.11, p = 0.010
- Spearman rho(k, Deaths) = -0.04, p = 0.351
- Spearman rho(k, Kills) = -0.02, p = 0.644

## urban map: primary hypothesis tests (Holm across the primary tests of each model)


### additive (v2)

| Hyp. | Test | Statistic; effect | p_Holm |
|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 78.0; eps2 = 0.65 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 21.2; eps2 = 0.16 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 59.9; eps2 = 0.49 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 100.2; eps2 = 0.84 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 81.0; eps2 = 0.67 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.80 (chance 0.25); 5-fold CV, 1000 permutations | 0.008 |
| H1 | Style classification, Deathmatch | accuracy = 0.87 (chance 0.25); 5-fold CV, 1000 permutations | 0.008 |
| H1 | Style classification, Control | accuracy = 0.72 (chance 0.25); 5-fold CV, 1000 permutations | 0.008 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.45 [+0.29, +0.83]; r = +0.98 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +0.18 [-0.00, +0.60]; r = +0.35 | 0.233 |
| H2 | Mission ObjCommit, w_commit 0.45 - 0 | median diff = +0.84 [+0.29, +0.98]; r = +1.00 | <0.001 |
| H2 | Control CtrlScore, w_commit 0.45 - 0 | median diff = +120.00 [+120.00, +120.00]; r = +1.00 | <0.001 |
| H3 | Deathmatch Survival-Aware EngRedirect, lambda x1 - x0 | median diff = +0.09 [+0.00, +0.51]; r = +0.50 | 0.089 |
| H3 | Mission Mission–Cooperation AllyDist, lambda x1 - x0 | median diff = +0.01 [+0.01, +0.03]; r = +0.59 | 0.022 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.20; n = 150 | 0.053 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.11; n = 150 | 0.233 |

### exp (v3)

| Hyp. | Test | Statistic; effect | p_Holm |
|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 291.0; eps2 = 0.73 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 178.3; eps2 = 0.44 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 347.4; eps2 = 0.87 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 223.8; eps2 = 0.56 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 262.4; eps2 = 0.65 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.79 (chance 0.25); 5-fold CV, 1000 permutations | 0.006 |
| H1 | Style classification, Deathmatch | accuracy = 0.98 (chance 0.25); 5-fold CV, 1000 permutations | 0.006 |
| H1 | Style classification, Control | accuracy = 0.79 (chance 0.25); 5-fold CV, 1000 permutations | 0.006 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.50 [+0.43, +0.60]; r = +0.97 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +1.30 [+1.19, +1.41]; r = +1.00 | <0.001 |
| H2 | Mission GoalSwitches, w_commit 0.45 - 0 | median diff = -14.82 [-18.32, -9.53]; r = -1.00 | <0.001 |
| H2 | Control GoalSwitches, w_commit 0.45 - 0 | median diff = -22.99 [-27.63, -20.35]; r = -1.00 | <0.001 |
| H3 | Deathmatch Mission–Cooperation WalkedHits, lambda_E configured - 0 | median diff = -0.0081 [-0.0124, -0.0025]; r = -0.36 | 0.006 |
| H3 | Deathmatch Persistent Objective WalkedHits, lambda_E configured - 0 | median diff = -0.0267 [-0.0318, -0.0219]; r = -0.97 | <0.001 |
| H3 | Deathmatch Aggressive WalkedHits, lambda_E configured - 0 | median diff = -0.0173 [-0.0205, -0.0125]; r = -0.79 | <0.001 |
| H3 | Deathmatch Survival-Aware WalkedHits, lambda_E configured - 0 | median diff = -0.0054 [-0.0112, +0.0013]; r = -0.31 | 0.010 |
| H3 | Sign test, WalkedHits lower with the exposure term (all scenarios x styles) | 12/12 conditions lower; one-sided binomial | 0.002 |
| H3b | Deathmatch Mission–Cooperation AllyDist, lambda_T 10 - 0 | median diff = -0.20 [-0.35, -0.02]; r = -0.32 | 0.010 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.20; n = 500 | <0.001 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.67; n = 500 | <0.001 |

## urban map: main experiment, exp vs additive (paired by seed on the 30 common episodes; Holm within condition)

| Scenario | Style | Metric | additive | exp | r | p_Holm |
|---|---|---|---|---|---|---|
| Mission | Mission–Cooperation | ObjCommit | 0.61 ± 0.15 | 0.95 ± 0.02 | +0.66 | 0.006 |
| Mission | Mission–Cooperation | AllyDist | 1.38 ± 0.23 | 1.64 ± 0.34 | +0.09 | 1.000 |
| Mission | Mission–Cooperation | EngRedirect | 0.00 ± 0.01 | 0.02 ± 0.02 | +0.67 | 1.000 |
| Mission | Mission–Cooperation | Deaths | 2.57 ± 1.03 | 3.50 ± 1.74 | +0.13 | 1.000 |
| Mission | Persistent Objective | ObjCommit | 0.60 ± 0.11 | 0.84 ± 0.09 | +0.75 | 0.002 |
| Mission | Persistent Objective | AllyDist | 2.19 ± 0.50 | 3.35 ± 0.95 | +0.38 | 0.216 |
| Mission | Persistent Objective | EngRedirect | 0.00 ± 0.01 | 0.00 ± 0.00 | -1.00 | 1.000 |
| Mission | Persistent Objective | Deaths | 5.70 ± 2.14 | 4.50 ± 1.79 | -0.36 | 0.285 |
| Mission | Aggressive | ObjCommit | 0.07 ± 0.05 | 0.36 ± 0.11 | +0.91 | <0.001 |
| Mission | Aggressive | AllyDist | 2.31 ± 0.51 | 4.56 ± 0.89 | +0.79 | <0.001 |
| Mission | Aggressive | EngRedirect | 0.72 ± 0.25 | 1.50 ± 0.39 | +0.59 | 0.007 |
| Mission | Aggressive | Deaths | 5.83 ± 1.83 | 6.77 ± 1.70 | +0.18 | 0.405 |
| Mission | Survival-Aware | ObjCommit | 0.00 ± 0.00 | 0.03 ± 0.03 | +0.93 | 0.062 |
| Mission | Survival-Aware | AllyDist | 2.29 ± 0.56 | 6.49 ± 1.31 | +0.96 | <0.001 |
| Mission | Survival-Aware | EngRedirect | 0.30 ± 0.11 | 0.00 ± 0.00 | -1.00 | <0.001 |
| Mission | Survival-Aware | Deaths | 3.97 ± 1.42 | 2.83 ± 0.98 | -0.22 | 0.345 |
| Deathmatch | Mission–Cooperation | EngRedirect | 0.21 ± 0.09 | 0.46 ± 0.11 | +0.77 | <0.001 |
| Deathmatch | Mission–Cooperation | ResSeek | 0.00 ± 0.00 | 0.17 ± 0.05 | +1.00 | <0.001 |
| Deathmatch | Mission–Cooperation | AllyDist | 1.22 ± 0.11 | 2.74 ± 0.19 | +1.00 | <0.001 |
| Deathmatch | Mission–Cooperation | Kills | 6.10 ± 2.03 | 10.13 ± 1.46 | +0.73 | 0.002 |
| Deathmatch | Mission–Cooperation | Deaths | 5.43 ± 1.55 | 9.13 ± 1.47 | +0.70 | 0.002 |
| Deathmatch | Persistent Objective | EngRedirect | 0.06 ± 0.04 | 0.12 ± 0.05 | +0.39 | 0.324 |
| Deathmatch | Persistent Objective | ResSeek | 0.01 ± 0.01 | 0.02 ± 0.02 | +0.36 | 0.906 |
| Deathmatch | Persistent Objective | AllyDist | 2.56 ± 0.48 | 5.58 ± 0.51 | +0.96 | <0.001 |
| Deathmatch | Persistent Objective | Kills | 7.90 ± 1.77 | 8.10 ± 0.78 | +0.02 | 0.926 |
| Deathmatch | Persistent Objective | Deaths | 4.87 ± 1.13 | 6.40 ± 0.92 | +0.42 | 0.184 |
| Deathmatch | Aggressive | EngRedirect | 1.28 ± 0.29 | 3.02 ± 0.25 | +1.00 | <0.001 |
| Deathmatch | Aggressive | ResSeek | 0.00 ± 0.00 | 0.36 ± 0.07 | +1.00 | <0.001 |
| Deathmatch | Aggressive | AllyDist | 2.64 ± 0.55 | 4.76 ± 0.40 | +0.92 | <0.001 |
| Deathmatch | Aggressive | Kills | 9.60 ± 2.03 | 12.13 ± 1.16 | +0.37 | 0.085 |
| Deathmatch | Aggressive | Deaths | 9.53 ± 1.84 | 12.07 ± 1.10 | +0.47 | 0.062 |
| Deathmatch | Survival-Aware | EngRedirect | 0.61 ± 0.23 | 0.00 ± 0.00 | -1.00 | <0.001 |
| Deathmatch | Survival-Aware | ResSeek | 0.64 ± 0.19 | 0.58 ± 0.11 | -0.05 | 0.831 |
| Deathmatch | Survival-Aware | AllyDist | 2.65 ± 0.58 | 8.11 ± 1.25 | +1.00 | <0.001 |
| Deathmatch | Survival-Aware | Kills | 6.33 ± 1.78 | 4.93 ± 0.84 | -0.34 | 0.393 |
| Deathmatch | Survival-Aware | Deaths | 5.43 ± 1.44 | 4.47 ± 0.91 | -0.19 | 0.728 |
| Control | Mission–Cooperation | CtrlScore | 99.37 ± 15.06 | 117.57 ± 3.47 | +0.89 | 0.076 |
| Control | Mission–Cooperation | ObjCommit | 0.80 ± 0.12 | 0.94 ± 0.03 | +0.15 | 0.476 |
| Control | Mission–Cooperation | AllyDist | 1.58 ± 0.26 | 2.07 ± 0.54 | +0.36 | 0.172 |
| Control | Mission–Cooperation | Deaths | 1.10 ± 0.51 | 2.03 ± 1.09 | +0.74 | 0.076 |
| Control | Persistent Objective | CtrlScore | 112.00 ± 11.37 | 116.00 ± 8.18 | +0.33 | 1.000 |
| Control | Persistent Objective | ObjCommit | 0.77 ± 0.11 | 0.87 ± 0.08 | +0.46 | 0.087 |
| Control | Persistent Objective | AllyDist | 2.38 ± 0.65 | 3.38 ± 1.25 | +0.48 | 0.087 |
| Control | Persistent Objective | Deaths | 2.27 ± 0.98 | 1.63 ± 0.81 | -0.33 | 0.536 |
| Control | Aggressive | CtrlScore | 24.23 ± 17.60 | 89.13 ± 17.43 | +0.87 | <0.001 |
| Control | Aggressive | ObjCommit | 0.09 ± 0.08 | 0.32 ± 0.08 | +0.78 | <0.001 |
| Control | Aggressive | AllyDist | 2.42 ± 0.53 | 4.68 ± 0.71 | +1.00 | <0.001 |
| Control | Aggressive | Deaths | 5.63 ± 1.98 | 5.37 ± 1.50 | -0.08 | 0.727 |
| Control | Survival-Aware | CtrlScore | 0.03 ± 0.07 | 6.43 ± 9.28 | +1.00 | 0.188 |
| Control | Survival-Aware | ObjCommit | 0.00 ± 0.00 | 0.02 ± 0.03 | +1.00 | 0.250 |
| Control | Survival-Aware | AllyDist | 2.62 ± 0.88 | 6.31 ± 1.22 | +0.80 | <0.001 |
| Control | Survival-Aware | Deaths | 3.37 ± 1.22 | 2.47 ± 0.85 | -0.33 | 0.250 |

Control wins (additive -> exp): Mission–Cooperation: 23 -> 27; Persistent Objective: 28 -> 29; Aggressive: 5 -> 18; Survival-Aware: 0 -> 1

## urban map: exp-model lambda-scale sweep (k relative to the new defaults; x1 = defaults)


### Mission / Mission–Cooperation

| k | AllyDist | EngRedirect | Deaths | Kills |
|---|---|---|---|---|
| x0 | 1.89 ± 0.22 | 0.02 ± 0.01 | 4.80 ± 1.02 | 5.65 ± 1.07 |
| x0.25 | 1.91 ± 0.20 | 0.02 ± 0.02 | 5.04 ± 1.04 | 5.43 ± 1.00 |
| x0.5 | 1.83 ± 0.18 | 0.01 ± 0.01 | 4.81 ± 1.00 | 5.15 ± 0.95 |
| x1 | 1.77 ± 0.18 | 0.02 ± 0.01 | 4.22 ± 0.89 | 5.03 ± 0.94 |
| x2 | 1.97 ± 0.21 | 0.02 ± 0.01 | 4.79 ± 0.99 | 4.99 ± 0.88 |
- Spearman rho(k, AllyDist) = +0.04, p = 0.422
- Spearman rho(k, EngRedirect) = +0.04, p = 0.421
- Spearman rho(k, Deaths) = -0.02, p = 0.646
- Spearman rho(k, Kills) = -0.05, p = 0.289

### Deathmatch / Survival-Aware

| k | AllyDist | EngRedirect | Deaths | Kills |
|---|---|---|---|---|
| x0 | 6.67 ± 0.69 | 0.00 ± 0.00 | 5.40 ± 0.52 | 5.46 ± 0.52 |
| x0.25 | 7.57 ± 0.64 | 0.00 ± 0.00 | 4.38 ± 0.48 | 4.95 ± 0.46 |
| x0.5 | 7.31 ± 0.52 | 0.00 ± 0.00 | 4.69 ± 0.46 | 4.65 ± 0.42 |
| x1 | 7.42 ± 0.57 | 0.00 ± 0.00 | 4.72 ± 0.50 | 4.70 ± 0.46 |
| x2 | 7.25 ± 0.63 | 0.00 ± 0.00 | 4.69 ± 0.55 | 4.49 ± 0.48 |
- Spearman rho(k, AllyDist) = +0.06, p = 0.177
- Spearman rho(k, Deaths) = -0.07, p = 0.136
- Spearman rho(k, Kills) = -0.13, p = 0.003
