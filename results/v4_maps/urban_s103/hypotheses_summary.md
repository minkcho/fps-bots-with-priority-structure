# Hypothesis tests and effect sizes (urban_s103 map)

## Primary tests (Holm-adjusted across all primary tests of this map)

| Hypothesis | Test | Statistic | Effect size | p | p (Holm) |
|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 292.7 | eps2 = 0.73 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 173.4 | eps2 = 0.43 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 340.2 | eps2 = 0.85 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 225.5 | eps2 = 0.56 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 235.4 | eps2 = 0.59 | <0.001 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.74 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Style classification, Deathmatch | accuracy = 0.98 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Style classification, Control | accuracy = 0.75 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.48 [+0.39, +0.53] | r = +0.99 | <0.001 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +1.32 [+1.16, +1.41] | r = +0.97 | <0.001 | <0.001 |
| H2 | Mission GoalSwitches, w_commit 0.45 - 0 | median diff = -9.44 [-12.23, -7.45] | r = -0.99 | <0.001 | <0.001 |
| H2 | Control GoalSwitches, w_commit 0.45 - 0 | median diff = -19.85 [-21.98, -17.16] | r = -1.00 | <0.001 | <0.001 |
| H3 | Deathmatch Mission–Cooperation WalkedHits, lambda_E configured - 0 | median diff = -0.0085 [-0.0129, -0.0014] | r = -0.41 | <0.001 | 0.001 |
| H3 | Deathmatch Persistent Objective WalkedHits, lambda_E configured - 0 | median diff = -0.0217 [-0.0260, -0.0156] | r = -0.92 | <0.001 | <0.001 |
| H3 | Deathmatch Aggressive WalkedHits, lambda_E configured - 0 | median diff = -0.0134 [-0.0176, -0.0093] | r = -0.75 | <0.001 | <0.001 |
| H3 | Deathmatch Survival-Aware WalkedHits, lambda_E configured - 0 | median diff = -0.0119 [-0.0159, -0.0072] | r = -0.61 | <0.001 | <0.001 |
| H3 | Sign test, WalkedHits lower with the exposure term (all scenarios x styles) | 12/12 conditions lower | one-sided binomial | <0.001 | 0.001 |
| H3b | Deathmatch Mission–Cooperation AllyDist, lambda_T 10 - 0 | median diff = -0.21 [-0.33, -0.10] | r = -0.35 | 0.002 | 0.004 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.10 | n = 500 | 0.028 | 0.028 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.62 | n = 500 | <0.001 | <0.001 |

## Earlier formulations of the hypotheses (unadjusted; not in the Holm family)

| Hypothesis | Test | Statistic | Effect size | p |
|---|---|---|---|---|
| H2 (earlier formulation) | Mission ObjCommit, w_commit 0.45 - 0 | median diff = +0.04 [+0.03, +0.07] | r = +0.83 | <0.001 |
| H2 (earlier formulation) | Control CtrlScore, w_commit 0.45 - 0 | median diff = +0.00 [+0.00, +0.00] | r = +0.09 | 0.737 |

## Secondary pairwise style contrasts (Mann-Whitney; delta = Cliff's delta = rank-biserial r; HL = Hodges-Lehmann shift A - B with bootstrap 95% CI; unadjusted)

| Scenario | Metric | A | B | delta | HL [95% CI] | p |
|---|---|---|---|---|---|---|
| Mission | ObjCommit | Mission–Cooperation | Persistent Objective | +0.07 | +0.00 [+0.00, +0.02] | 0.352 |
| Mission | ObjCommit | Mission–Cooperation | Aggressive | +0.89 | +0.66 [+0.59, +0.72] | <0.001 |
| Mission | ObjCommit | Mission–Cooperation | Survival-Aware | +0.99 | +0.96 [+0.92, +0.98] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Aggressive | +0.85 | +0.62 [+0.54, +0.70] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Survival-Aware | +0.98 | +0.93 [+0.88, +0.97] | <0.001 |
| Mission | ObjCommit | Aggressive | Survival-Aware | +0.77 | +0.25 [+0.19, +0.31] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Persistent Objective | -0.13 | -0.01 [-0.70, +0.00] | 0.112 |
| Mission | AllyDist | Mission–Cooperation | Aggressive | -0.79 | -2.74 [-3.25, -2.17] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Survival-Aware | -0.90 | -4.14 [-4.57, -3.64] | <0.001 |
| Mission | AllyDist | Persistent Objective | Aggressive | -0.54 | -2.06 [-2.71, -1.54] | <0.001 |
| Mission | AllyDist | Persistent Objective | Survival-Aware | -0.70 | -3.61 [-4.16, -2.76] | <0.001 |
| Mission | AllyDist | Aggressive | Survival-Aware | -0.35 | -1.43 [-2.11, -0.77] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Persistent Objective | +0.82 | +0.32 [+0.24, +0.36] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Aggressive | -0.98 | -2.31 [-2.42, -2.20] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Survival-Aware | +0.93 | +0.36 [+0.34, +0.44] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Aggressive | -1.00 | -2.63 [-2.75, -2.53] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Survival-Aware | +0.50 | +0.05 [+0.00, +0.10] | <0.001 |
| Deathmatch | EngRedirect | Aggressive | Survival-Aware | +1.00 | +2.72 [+2.60, +2.81] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Persistent Objective | +0.62 | +0.12 [+0.11, +0.21] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Aggressive | -0.31 | -0.11 [-0.14, -0.03] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Survival-Aware | -0.68 | -0.38 [-0.42, -0.29] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Aggressive | -0.88 | -0.25 [-0.32, -0.24] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Survival-Aware | -0.96 | -0.51 [-0.61, -0.49] | <0.001 |
| Deathmatch | ResSeek | Aggressive | Survival-Aware | -0.62 | -0.27 [-0.36, -0.21] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Persistent Objective | -0.02 | +0.00 [+0.00, +0.00] | 0.686 |
| Control | CtrlScore | Mission–Cooperation | Aggressive | +0.48 | +22.00 [+0.00, +55.02] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Survival-Aware | +0.94 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Aggressive | +0.47 | +14.00 [+0.00, +57.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Survival-Aware | +0.91 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Aggressive | Survival-Aware | +0.58 | +73.00 [+35.00, +105.00] | <0.001 |
