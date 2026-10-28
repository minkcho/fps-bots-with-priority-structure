# Hypothesis tests and effect sizes (blocks map)

## Primary tests (Holm-adjusted across all primary tests of this map)

| Hypothesis | Test | Statistic | Effect size | p | p (Holm) |
|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 299.3 | eps2 = 0.75 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 165.0 | eps2 = 0.41 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 344.5 | eps2 = 0.86 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 212.0 | eps2 = 0.53 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 226.8 | eps2 = 0.57 | <0.001 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.81 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | <0.001 |
| H1 | Style classification, Deathmatch | accuracy = 0.96 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | <0.001 |
| H1 | Style classification, Control | accuracy = 0.78 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | <0.001 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.49 [+0.40, +0.54] | r = +0.98 | <0.001 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +1.06 [+0.90, +1.24] | r = +0.98 | <0.001 | <0.001 |
| H2 | Mission GoalSwitches, w_commit 0.45 - 0 | median diff = -18.38 [-21.93, -13.61] | r = -1.00 | <0.001 | <0.001 |
| H2 | Control GoalSwitches, w_commit 0.45 - 0 | median diff = -19.06 [-21.82, -16.67] | r = -1.00 | <0.001 | <0.001 |
| H3 | Deathmatch Mission–Cooperation WalkedHits, lambda_E configured - 0 | median diff = -0.0113 [-0.0147, -0.0087] | r = -0.55 | <0.001 | <0.001 |
| H3 | Deathmatch Persistent Objective WalkedHits, lambda_E configured - 0 | median diff = -0.0259 [-0.0290, -0.0204] | r = -0.94 | <0.001 | <0.001 |
| H3 | Deathmatch Aggressive WalkedHits, lambda_E configured - 0 | median diff = -0.0145 [-0.0197, -0.0081] | r = -0.71 | <0.001 | <0.001 |
| H3 | Deathmatch Survival-Aware WalkedHits, lambda_E configured - 0 | median diff = -0.0090 [-0.0152, -0.0050] | r = -0.63 | <0.001 | <0.001 |
| H3 | Sign test, WalkedHits lower with the exposure term (all scenarios x styles) | 12/12 conditions lower | one-sided binomial | <0.001 | <0.001 |
| H3b | Deathmatch Mission–Cooperation AllyDist, lambda_T 10 - 0 | median diff = -0.13 [-0.26, -0.02] | r = -0.30 | 0.010 | 0.010 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.20 | n = 500 | <0.001 | <0.001 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.60 | n = 500 | <0.001 | <0.001 |

## Earlier formulations of the hypotheses (unadjusted; not in the Holm family)

| Hypothesis | Test | Statistic | Effect size | p |
|---|---|---|---|---|
| H2 (earlier formulation) | Mission ObjCommit, w_commit 0.45 - 0 | median diff = +0.08 [+0.06, +0.11] | r = +0.92 | <0.001 |
| H2 (earlier formulation) | Control CtrlScore, w_commit 0.45 - 0 | median diff = +0.00 [+0.00, +0.00] | r = +0.50 | 0.039 |

## Secondary pairwise style contrasts (Mann-Whitney; delta = Cliff's delta = rank-biserial r; HL = Hodges-Lehmann shift A - B with bootstrap 95% CI; unadjusted)

| Scenario | Metric | A | B | delta | HL [95% CI] | p |
|---|---|---|---|---|---|---|
| Mission | ObjCommit | Mission–Cooperation | Persistent Objective | +0.19 | +0.03 [+0.00, +0.05] | 0.020 |
| Mission | ObjCommit | Mission–Cooperation | Aggressive | +0.89 | +0.68 [+0.62, +0.73] | <0.001 |
| Mission | ObjCommit | Mission–Cooperation | Survival-Aware | +1.00 | +0.92 [+0.90, +0.94] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Aggressive | +0.84 | +0.63 [+0.56, +0.69] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Survival-Aware | +0.99 | +0.90 [+0.87, +0.92] | <0.001 |
| Mission | ObjCommit | Aggressive | Survival-Aware | +0.85 | +0.23 [+0.17, +0.28] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Persistent Objective | -0.33 | -0.78 [-1.23, -0.34] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Aggressive | -0.79 | -2.51 [-2.93, -2.13] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Survival-Aware | -0.89 | -3.97 [-4.53, -3.41] | <0.001 |
| Mission | AllyDist | Persistent Objective | Aggressive | -0.43 | -1.57 [-2.13, -1.08] | <0.001 |
| Mission | AllyDist | Persistent Objective | Survival-Aware | -0.63 | -3.00 [-3.65, -2.30] | <0.001 |
| Mission | AllyDist | Aggressive | Survival-Aware | -0.36 | -1.48 [-2.19, -0.85] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Persistent Objective | +0.82 | +0.29 [+0.23, +0.33] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Aggressive | -1.00 | -2.13 [-2.28, -2.00] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Survival-Aware | +0.95 | +0.35 [+0.32, +0.42] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Aggressive | -1.00 | -2.43 [-2.57, -2.27] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Survival-Aware | +0.55 | +0.10 [+0.00, +0.10] | <0.001 |
| Deathmatch | EngRedirect | Aggressive | Survival-Aware | +1.00 | +2.51 [+2.35, +2.65] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Persistent Objective | +0.51 | +0.11 [+0.01, +0.12] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Aggressive | -0.29 | -0.11 [-0.13, -0.02] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Survival-Aware | -0.73 | -0.40 [-0.50, -0.33] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Aggressive | -0.77 | -0.23 [-0.25, -0.15] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Survival-Aware | -0.96 | -0.58 [-0.61, -0.50] | <0.001 |
| Deathmatch | ResSeek | Aggressive | Survival-Aware | -0.66 | -0.33 [-0.39, -0.26] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Persistent Objective | +0.04 | +0.00 [+0.00, +0.00] | 0.428 |
| Control | CtrlScore | Mission–Cooperation | Aggressive | +0.51 | +26.00 [+0.00, +76.00] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Survival-Aware | +0.93 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Aggressive | +0.47 | +22.00 [+0.00, +72.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Survival-Aware | +0.90 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Aggressive | Survival-Aware | +0.55 | +47.00 [+30.00, +96.00] | <0.001 |
