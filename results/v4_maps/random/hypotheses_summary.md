# Hypothesis tests and effect sizes (random map)

## Primary tests (Holm-adjusted across all primary tests of this map)

| Hypothesis | Test | Statistic | Effect size | p | p (Holm) |
|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 284.6 | eps2 = 0.71 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 145.2 | eps2 = 0.36 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 340.4 | eps2 = 0.85 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 215.6 | eps2 = 0.54 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 232.4 | eps2 = 0.58 | <0.001 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.80 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Style classification, Deathmatch | accuracy = 0.97 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Style classification, Control | accuracy = 0.72 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.51 [+0.42, +0.57] | r = +0.98 | <0.001 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +1.32 [+1.15, +1.54] | r = +0.98 | <0.001 | <0.001 |
| H2 | Mission GoalSwitches, w_commit 0.45 - 0 | median diff = -20.15 [-23.82, -16.34] | r = -1.00 | <0.001 | <0.001 |
| H2 | Control GoalSwitches, w_commit 0.45 - 0 | median diff = -22.44 [-27.02, -19.40] | r = -1.00 | <0.001 | <0.001 |
| H3 | Deathmatch Mission–Cooperation WalkedHits, lambda_E configured - 0 | median diff = -0.0119 [-0.0168, -0.0093] | r = -0.66 | <0.001 | <0.001 |
| H3 | Deathmatch Persistent Objective WalkedHits, lambda_E configured - 0 | median diff = -0.0210 [-0.0269, -0.0171] | r = -0.98 | <0.001 | <0.001 |
| H3 | Deathmatch Aggressive WalkedHits, lambda_E configured - 0 | median diff = -0.0130 [-0.0177, -0.0089] | r = -0.68 | <0.001 | <0.001 |
| H3 | Deathmatch Survival-Aware WalkedHits, lambda_E configured - 0 | median diff = -0.0034 [-0.0102, +0.0020] | r = -0.21 | 0.068 | 0.074 |
| H3 | Sign test, WalkedHits lower with the exposure term (all scenarios x styles) | 12/12 conditions lower | one-sided binomial | <0.001 | 0.001 |
| H3b | Deathmatch Mission–Cooperation AllyDist, lambda_T 10 - 0 | median diff = -0.25 [-0.36, -0.05] | r = -0.24 | 0.037 | 0.074 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.19 | n = 500 | <0.001 | <0.001 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.67 | n = 500 | <0.001 | <0.001 |

## Earlier formulations of the hypotheses (unadjusted; not in the Holm family)

| Hypothesis | Test | Statistic | Effect size | p |
|---|---|---|---|---|
| H2 (earlier formulation) | Mission ObjCommit, w_commit 0.45 - 0 | median diff = +0.09 [+0.07, +0.11] | r = +0.97 | <0.001 |
| H2 (earlier formulation) | Control CtrlScore, w_commit 0.45 - 0 | median diff = +0.00 [+0.00, +0.00] | r = +0.85 | <0.001 |

## Secondary pairwise style contrasts (Mann-Whitney; delta = Cliff's delta = rank-biserial r; HL = Hodges-Lehmann shift A - B with bootstrap 95% CI; unadjusted)

| Scenario | Metric | A | B | delta | HL [95% CI] | p |
|---|---|---|---|---|---|---|
| Mission | ObjCommit | Mission–Cooperation | Persistent Objective | +0.22 | +0.02 [+0.00, +0.05] | 0.006 |
| Mission | ObjCommit | Mission–Cooperation | Aggressive | +0.85 | +0.59 [+0.54, +0.64] | <0.001 |
| Mission | ObjCommit | Mission–Cooperation | Survival-Aware | +0.99 | +0.91 [+0.90, +0.93] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Aggressive | +0.79 | +0.55 [+0.49, +0.61] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Survival-Aware | +0.99 | +0.88 [+0.87, +0.90] | <0.001 |
| Mission | ObjCommit | Aggressive | Survival-Aware | +0.79 | +0.32 [+0.25, +0.37] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Persistent Objective | -0.28 | -0.61 [-1.06, -0.20] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Aggressive | -0.66 | -2.13 [-2.57, -1.68] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Survival-Aware | -0.81 | -4.65 [-5.54, -3.69] | <0.001 |
| Mission | AllyDist | Persistent Objective | Aggressive | -0.41 | -1.39 [-1.89, -0.89] | <0.001 |
| Mission | AllyDist | Persistent Objective | Survival-Aware | -0.66 | -3.89 [-4.89, -2.91] | <0.001 |
| Mission | AllyDist | Aggressive | Survival-Aware | -0.47 | -2.62 [-3.61, -1.73] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Persistent Objective | +0.78 | +0.32 [+0.24, +0.36] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Aggressive | -0.99 | -2.39 [-2.51, -2.24] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Survival-Aware | +0.94 | +0.41 [+0.34, +0.45] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Aggressive | -1.00 | -2.73 [-2.86, -2.56] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Survival-Aware | +0.56 | +0.10 [+0.00, +0.10] | <0.001 |
| Deathmatch | EngRedirect | Aggressive | Survival-Aware | +1.00 | +2.83 [+2.65, +2.91] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Persistent Objective | +0.68 | +0.12 [+0.11, +0.14] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Aggressive | -0.35 | -0.12 [-0.14, -0.02] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Survival-Aware | -0.67 | -0.40 [-0.49, -0.36] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Aggressive | -0.88 | -0.24 [-0.27, -0.17] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Survival-Aware | -0.91 | -0.60 [-0.62, -0.51] | <0.001 |
| Deathmatch | ResSeek | Aggressive | Survival-Aware | -0.57 | -0.29 [-0.38, -0.25] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Persistent Objective | +0.02 | +0.00 [+0.00, +0.00] | 0.518 |
| Control | CtrlScore | Mission–Cooperation | Aggressive | +0.36 | +0.00 [+0.00, +0.00] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Survival-Aware | +0.91 | +120.00 [+119.00, +120.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Aggressive | +0.34 | +0.00 [+0.00, +0.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Survival-Aware | +0.89 | +120.00 [+119.00, +120.00] | <0.001 |
| Control | CtrlScore | Aggressive | Survival-Aware | +0.61 | +107.00 [+75.00, +118.00] | <0.001 |
