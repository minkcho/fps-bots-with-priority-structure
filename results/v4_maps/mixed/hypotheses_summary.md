# Hypothesis tests and effect sizes (mixed map)

## Primary tests (Holm-adjusted across all primary tests of this map)

| Hypothesis | Test | Statistic | Effect size | p | p (Holm) |
|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 286.6 | eps2 = 0.72 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 141.9 | eps2 = 0.35 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 334.6 | eps2 = 0.84 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 246.5 | eps2 = 0.62 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 234.7 | eps2 = 0.59 | <0.001 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.81 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | <0.001 |
| H1 | Style classification, Deathmatch | accuracy = 0.98 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | <0.001 |
| H1 | Style classification, Control | accuracy = 0.75 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | <0.001 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.46 [+0.40, +0.51] | r = +1.00 | <0.001 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +1.02 [+0.85, +1.14] | r = +0.99 | <0.001 | <0.001 |
| H2 | Mission GoalSwitches, w_commit 0.45 - 0 | median diff = -20.31 [-24.73, -15.63] | r = -1.00 | <0.001 | <0.001 |
| H2 | Control GoalSwitches, w_commit 0.45 - 0 | median diff = -22.37 [-24.92, -20.81] | r = -1.00 | <0.001 | <0.001 |
| H3 | Deathmatch Mission–Cooperation WalkedHits, lambda_E configured - 0 | median diff = -0.0081 [-0.0145, -0.0026] | r = -0.47 | <0.001 | <0.001 |
| H3 | Deathmatch Persistent Objective WalkedHits, lambda_E configured - 0 | median diff = -0.0189 [-0.0251, -0.0165] | r = -0.91 | <0.001 | <0.001 |
| H3 | Deathmatch Aggressive WalkedHits, lambda_E configured - 0 | median diff = -0.0148 [-0.0188, -0.0101] | r = -0.72 | <0.001 | <0.001 |
| H3 | Deathmatch Survival-Aware WalkedHits, lambda_E configured - 0 | median diff = -0.0095 [-0.0147, -0.0033] | r = -0.50 | <0.001 | <0.001 |
| H3 | Sign test, WalkedHits lower with the exposure term (all scenarios x styles) | 12/12 conditions lower | one-sided binomial | <0.001 | <0.001 |
| H3b | Deathmatch Mission–Cooperation AllyDist, lambda_T 10 - 0 | median diff = -0.25 [-0.36, -0.17] | r = -0.55 | <0.001 | <0.001 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.19 | n = 500 | <0.001 | <0.001 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.65 | n = 500 | <0.001 | <0.001 |

## Earlier formulations of the hypotheses (unadjusted; not in the Holm family)

| Hypothesis | Test | Statistic | Effect size | p |
|---|---|---|---|---|
| H2 (earlier formulation) | Mission ObjCommit, w_commit 0.45 - 0 | median diff = +0.07 [+0.05, +0.10] | r = +0.96 | <0.001 |
| H2 (earlier formulation) | Control CtrlScore, w_commit 0.45 - 0 | median diff = +0.00 [+0.00, +0.00] | r = +0.65 | 0.005 |

## Secondary pairwise style contrasts (Mann-Whitney; delta = Cliff's delta = rank-biserial r; HL = Hodges-Lehmann shift A - B with bootstrap 95% CI; unadjusted)

| Scenario | Metric | A | B | delta | HL [95% CI] | p |
|---|---|---|---|---|---|---|
| Mission | ObjCommit | Mission–Cooperation | Persistent Objective | +0.16 | +0.02 [+0.00, +0.06] | 0.055 |
| Mission | ObjCommit | Mission–Cooperation | Aggressive | +0.85 | +0.60 [+0.51, +0.67] | <0.001 |
| Mission | ObjCommit | Mission–Cooperation | Survival-Aware | +1.00 | +0.90 [+0.87, +0.92] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Aggressive | +0.75 | +0.53 [+0.43, +0.62] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Survival-Aware | +1.00 | +0.87 [+0.84, +0.89] | <0.001 |
| Mission | ObjCommit | Aggressive | Survival-Aware | +0.82 | +0.30 [+0.19, +0.39] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Persistent Objective | -0.28 | -0.85 [-1.51, -0.22] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Aggressive | -0.65 | -2.12 [-2.56, -1.65] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Survival-Aware | -0.89 | -3.89 [-4.40, -3.30] | <0.001 |
| Mission | AllyDist | Persistent Objective | Aggressive | -0.27 | -1.10 [-1.69, -0.43] | <0.001 |
| Mission | AllyDist | Persistent Objective | Survival-Aware | -0.59 | -2.79 [-3.66, -2.19] | <0.001 |
| Mission | AllyDist | Aggressive | Survival-Aware | -0.43 | -1.80 [-2.42, -1.15] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Persistent Objective | +0.73 | +0.21 [+0.19, +0.22] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Aggressive | -1.00 | -2.13 [-2.25, -2.01] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Survival-Aware | +0.91 | +0.22 [+0.21, +0.28] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Aggressive | -1.00 | -2.36 [-2.49, -2.21] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Survival-Aware | +0.35 | +0.00 [+0.00, +0.00] | <0.001 |
| Deathmatch | EngRedirect | Aggressive | Survival-Aware | +1.00 | +2.41 [+2.26, +2.54] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Persistent Objective | +0.74 | +0.12 [+0.11, +0.21] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Aggressive | -0.27 | -0.10 [-0.13, -0.01] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Survival-Aware | -0.73 | -0.39 [-0.41, -0.30] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Aggressive | -0.87 | -0.24 [-0.33, -0.23] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Survival-Aware | -0.99 | -0.51 [-0.61, -0.50] | <0.001 |
| Deathmatch | ResSeek | Aggressive | Survival-Aware | -0.67 | -0.29 [-0.38, -0.25] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Persistent Objective | +0.09 | +0.00 [+0.00, +0.00] | 0.046 |
| Control | CtrlScore | Mission–Cooperation | Aggressive | +0.46 | +0.00 [+0.00, +42.00] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Survival-Aware | +0.94 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Aggressive | +0.39 | +0.00 [+0.00, +38.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Survival-Aware | +0.93 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Aggressive | Survival-Aware | +0.58 | +83.00 [+39.00, +120.00] | <0.001 |
