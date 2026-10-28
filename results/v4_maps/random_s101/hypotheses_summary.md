# Hypothesis tests and effect sizes (random_s101 map)

## Primary tests (Holm-adjusted across all primary tests of this map)

| Hypothesis | Test | Statistic | Effect size | p | p (Holm) |
|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 286.7 | eps2 = 0.72 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 120.5 | eps2 = 0.30 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 338.9 | eps2 = 0.85 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 214.3 | eps2 = 0.53 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 264.1 | eps2 = 0.66 | <0.001 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.77 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Style classification, Deathmatch | accuracy = 0.96 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Style classification, Control | accuracy = 0.79 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.51 [+0.40, +0.61] | r = +0.97 | <0.001 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +1.39 [+1.26, +1.49] | r = +1.00 | <0.001 | <0.001 |
| H2 | Mission GoalSwitches, w_commit 0.45 - 0 | median diff = -21.66 [-26.11, -15.95] | r = -1.00 | <0.001 | <0.001 |
| H2 | Control GoalSwitches, w_commit 0.45 - 0 | median diff = -23.73 [-26.57, -19.94] | r = -1.00 | <0.001 | <0.001 |
| H3 | Deathmatch Mission–Cooperation WalkedHits, lambda_E configured - 0 | median diff = -0.0120 [-0.0160, -0.0057] | r = -0.57 | <0.001 | <0.001 |
| H3 | Deathmatch Persistent Objective WalkedHits, lambda_E configured - 0 | median diff = -0.0221 [-0.0259, -0.0165] | r = -0.92 | <0.001 | <0.001 |
| H3 | Deathmatch Aggressive WalkedHits, lambda_E configured - 0 | median diff = -0.0110 [-0.0174, -0.0075] | r = -0.64 | <0.001 | <0.001 |
| H3 | Deathmatch Survival-Aware WalkedHits, lambda_E configured - 0 | median diff = -0.0083 [-0.0113, -0.0029] | r = -0.38 | <0.001 | 0.002 |
| H3 | Sign test, WalkedHits lower with the exposure term (all scenarios x styles) | 12/12 conditions lower | one-sided binomial | <0.001 | 0.001 |
| H3b | Deathmatch Mission–Cooperation AllyDist, lambda_T 10 - 0 | median diff = -0.24 [-0.31, -0.11] | r = -0.31 | 0.007 | 0.007 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.20 | n = 500 | <0.001 | <0.001 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.64 | n = 500 | <0.001 | <0.001 |

## Earlier formulations of the hypotheses (unadjusted; not in the Holm family)

| Hypothesis | Test | Statistic | Effect size | p |
|---|---|---|---|---|
| H2 (earlier formulation) | Mission ObjCommit, w_commit 0.45 - 0 | median diff = +0.10 [+0.07, +0.13] | r = +0.88 | <0.001 |
| H2 (earlier formulation) | Control CtrlScore, w_commit 0.45 - 0 | median diff = +0.00 [+0.00, +0.00] | r = +0.82 | <0.001 |

## Secondary pairwise style contrasts (Mann-Whitney; delta = Cliff's delta = rank-biserial r; HL = Hodges-Lehmann shift A - B with bootstrap 95% CI; unadjusted)

| Scenario | Metric | A | B | delta | HL [95% CI] | p |
|---|---|---|---|---|---|---|
| Mission | ObjCommit | Mission–Cooperation | Persistent Objective | +0.05 | +0.00 [-0.01, +0.03] | 0.526 |
| Mission | ObjCommit | Mission–Cooperation | Aggressive | +0.88 | +0.64 [+0.56, +0.70] | <0.001 |
| Mission | ObjCommit | Mission–Cooperation | Survival-Aware | +0.99 | +0.88 [+0.86, +0.90] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Aggressive | +0.81 | +0.59 [+0.49, +0.67] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Survival-Aware | +0.99 | +0.88 [+0.85, +0.90] | <0.001 |
| Mission | ObjCommit | Aggressive | Survival-Aware | +0.78 | +0.22 [+0.18, +0.30] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Persistent Objective | -0.24 | -0.63 [-1.16, -0.08] | 0.003 |
| Mission | AllyDist | Mission–Cooperation | Aggressive | -0.63 | -1.88 [-2.33, -1.46] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Survival-Aware | -0.78 | -3.35 [-4.30, -2.63] | <0.001 |
| Mission | AllyDist | Persistent Objective | Aggressive | -0.32 | -1.11 [-1.64, -0.59] | <0.001 |
| Mission | AllyDist | Persistent Objective | Survival-Aware | -0.57 | -2.67 [-3.51, -1.99] | <0.001 |
| Mission | AllyDist | Aggressive | Survival-Aware | -0.36 | -1.70 [-2.62, -0.90] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Persistent Objective | +0.78 | +0.33 [+0.28, +0.41] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Aggressive | -1.00 | -2.29 [-2.43, -2.16] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Survival-Aware | +0.93 | +0.41 [+0.34, +0.50] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Aggressive | -1.00 | -2.63 [-2.76, -2.50] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Survival-Aware | +0.46 | +0.00 [+0.00, +0.10] | <0.001 |
| Deathmatch | EngRedirect | Aggressive | Survival-Aware | +1.00 | +2.69 [+2.60, +2.85] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Persistent Objective | +0.74 | +0.13 [+0.12, +0.22] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Aggressive | -0.34 | -0.12 [-0.14, -0.04] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Survival-Aware | -0.63 | -0.39 [-0.48, -0.29] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Aggressive | -0.91 | -0.25 [-0.35, -0.24] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Survival-Aware | -0.90 | -0.58 [-0.68, -0.50] | <0.001 |
| Deathmatch | ResSeek | Aggressive | Survival-Aware | -0.49 | -0.27 [-0.37, -0.18] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Persistent Objective | -0.06 | +0.00 [+0.00, +0.00] | 0.084 |
| Control | CtrlScore | Mission–Cooperation | Aggressive | +0.59 | +47.00 [+11.00, +77.00] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Survival-Aware | +0.95 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Aggressive | +0.62 | +47.00 [+14.00, +80.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Survival-Aware | +0.94 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Aggressive | Survival-Aware | +0.57 | +56.00 [+34.00, +83.00] | <0.001 |
