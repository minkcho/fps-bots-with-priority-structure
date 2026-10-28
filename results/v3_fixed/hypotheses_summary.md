# Hypothesis tests and effect sizes (random map)

## Primary tests (Holm-adjusted across all primary tests of this map)

| Hypothesis | Test | Statistic | Effect size | p | p (Holm) |
|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 281.7 | eps2 = 0.70 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 160.1 | eps2 = 0.40 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 343.6 | eps2 = 0.86 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 211.8 | eps2 = 0.53 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 234.7 | eps2 = 0.59 | <0.001 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.75 (chance 0.25) | 5-fold CV, 1000 permutations | <0.001 | 0.005 |
| H1 | Style classification, Deathmatch | accuracy = 0.98 (chance 0.25) | 5-fold CV, 1000 permutations | <0.001 | 0.005 |
| H1 | Style classification, Control | accuracy = 0.74 (chance 0.25) | 5-fold CV, 1000 permutations | <0.001 | 0.005 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.51 [+0.39, +0.61] | r = +0.95 | <0.001 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +1.43 [+1.28, +1.54] | r = +1.00 | <0.001 | <0.001 |
| H2 | Mission GoalSwitches, w_commit 0.45 - 0 | median diff = -20.39 [-24.15, -13.52] | r = -1.00 | <0.001 | <0.001 |
| H2 | Control GoalSwitches, w_commit 0.45 - 0 | median diff = -21.39 [-24.78, -20.06] | r = -1.00 | <0.001 | <0.001 |
| H3 | Deathmatch Mission–Cooperation WalkedHits, lambda_E configured - 0 | median diff = -0.0097 [-0.0136, -0.0017] | r = -0.39 | <0.001 | 0.004 |
| H3 | Deathmatch Persistent Objective WalkedHits, lambda_E configured - 0 | median diff = -0.0214 [-0.0267, -0.0154] | r = -0.96 | <0.001 | <0.001 |
| H3 | Deathmatch Aggressive WalkedHits, lambda_E configured - 0 | median diff = -0.0150 [-0.0185, -0.0125] | r = -0.77 | <0.001 | <0.001 |
| H3 | Deathmatch Survival-Aware WalkedHits, lambda_E configured - 0 | median diff = -0.0026 [-0.0072, +0.0015] | r = -0.15 | 0.179 | 0.179 |
| H3 | Sign test, WalkedHits lower with the exposure term (all scenarios x styles) | 12/12 conditions lower | one-sided binomial | <0.001 | 0.002 |
| H3b | Deathmatch Mission–Cooperation AllyDist, lambda_T 10 - 0 | median diff = -0.31 [-0.49, -0.11] | r = -0.53 | <0.001 | <0.001 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.15 | n = 500 | <0.001 | 0.005 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.70 | n = 500 | <0.001 | <0.001 |

## Earlier formulations of the hypotheses (unadjusted; not in the Holm family)

| Hypothesis | Test | Statistic | Effect size | p |
|---|---|---|---|---|
| H2 (earlier formulation) | Mission ObjCommit, w_commit 0.45 - 0 | median diff = +0.10 [+0.07, +0.14] | r = +0.94 | <0.001 |
| H2 (earlier formulation) | Control CtrlScore, w_commit 0.45 - 0 | median diff = +0.00 [+0.00, +0.00] | r = +0.90 | <0.001 |
| H3 (earlier formulation: Survival-Aware lambda scale) | Deathmatch Survival-Aware WalkedHits, lambda x1 - x0 | median diff = -0.004 [-0.009, +0.002] | r = -0.13 | 0.270 |
| H3 (earlier formulation: Survival-Aware lambda scale) | Deathmatch Survival-Aware LOSFraction, lambda x1 - x0 | median diff = -0.006 [-0.019, +0.011] | r = -0.08 | 0.507 |
| H3 (earlier formulation: Survival-Aware lambda scale) | Deathmatch Survival-Aware Deaths, lambda x1 - x0 | median diff = +0.000 [-1.000, +0.000] | r = -0.09 | 0.471 |
| H3 (earlier formulation: Survival-Aware lambda scale) | Deathmatch Survival-Aware EngRedirect, lambda x1 - x0 | median diff = +0.000 [+0.000, +0.000] | r = +0.00 | 1.000 |
| H3 (earlier formulation: Survival-Aware lambda scale) | Mission Mission–Cooperation AllyDist, lambda x1 - x0 | median diff = +0.000 [+0.000, +0.000] | r = +0.05 | 0.737 |

## Secondary pairwise style contrasts (Mann-Whitney; delta = Cliff's delta = rank-biserial r; HL = Hodges-Lehmann shift A - B with bootstrap 95% CI; unadjusted)

| Scenario | Metric | A | B | delta | HL [95% CI] | p |
|---|---|---|---|---|---|---|
| Mission | ObjCommit | Mission–Cooperation | Persistent Objective | +0.14 | +0.01 [+0.00, +0.03] | 0.081 |
| Mission | ObjCommit | Mission–Cooperation | Aggressive | +0.85 | +0.61 [+0.54, +0.68] | <0.001 |
| Mission | ObjCommit | Mission–Cooperation | Survival-Aware | +1.00 | +0.92 [+0.90, +0.93] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Aggressive | +0.82 | +0.59 [+0.51, +0.66] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Survival-Aware | +1.00 | +0.90 [+0.88, +0.92] | <0.001 |
| Mission | ObjCommit | Aggressive | Survival-Aware | +0.68 | +0.29 [+0.20, +0.35] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Persistent Objective | -0.23 | -0.43 [-0.85, -0.01] | 0.004 |
| Mission | AllyDist | Mission–Cooperation | Aggressive | -0.71 | -2.50 [-2.92, -1.94] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Survival-Aware | -0.85 | -3.81 [-4.54, -3.04] | <0.001 |
| Mission | AllyDist | Persistent Objective | Aggressive | -0.52 | -1.81 [-2.34, -1.34] | <0.001 |
| Mission | AllyDist | Persistent Objective | Survival-Aware | -0.70 | -3.17 [-3.99, -2.47] | <0.001 |
| Mission | AllyDist | Aggressive | Survival-Aware | -0.33 | -1.52 [-2.27, -0.77] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Persistent Objective | +0.83 | +0.36 [+0.31, +0.43] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Aggressive | -1.00 | -2.42 [-2.54, -2.29] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Survival-Aware | +0.93 | +0.45 [+0.36, +0.51] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Aggressive | -1.00 | -2.80 [-2.93, -2.66] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Survival-Aware | +0.57 | +0.10 [+0.00, +0.10] | <0.001 |
| Deathmatch | EngRedirect | Aggressive | Survival-Aware | +1.00 | +2.89 [+2.71, +3.03] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Persistent Objective | +0.76 | +0.13 [+0.12, +0.23] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Aggressive | -0.30 | -0.11 [-0.14, -0.02] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Survival-Aware | -0.55 | -0.30 [-0.40, -0.25] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Aggressive | -0.94 | -0.26 [-0.33, -0.25] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Survival-Aware | -0.91 | -0.52 [-0.61, -0.41] | <0.001 |
| Deathmatch | ResSeek | Aggressive | Survival-Aware | -0.46 | -0.25 [-0.33, -0.15] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Persistent Objective | +0.04 | +0.00 [+0.00, +0.00] | 0.259 |
| Control | CtrlScore | Mission–Cooperation | Aggressive | +0.50 | +12.00 [+0.00, +66.00] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Survival-Aware | +0.92 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Aggressive | +0.46 | +9.00 [+0.00, +60.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Survival-Aware | +0.91 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Aggressive | Survival-Aware | +0.52 | +62.00 [+30.00, +108.00] | <0.001 |
