# Hypothesis tests and effect sizes (random_s103 map)

## Primary tests (Holm-adjusted across all primary tests of this map)

| Hypothesis | Test | Statistic | Effect size | p | p (Holm) |
|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 291.7 | eps2 = 0.73 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 92.8 | eps2 = 0.23 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 332.5 | eps2 = 0.83 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 234.3 | eps2 = 0.58 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 225.9 | eps2 = 0.56 | <0.001 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.82 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Style classification, Deathmatch | accuracy = 0.97 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Style classification, Control | accuracy = 0.76 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.52 [+0.45, +0.62] | r = +0.99 | <0.001 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +1.52 [+1.29, +1.60] | r = +1.00 | <0.001 | <0.001 |
| H2 | Mission GoalSwitches, w_commit 0.45 - 0 | median diff = -29.45 [-38.94, -25.39] | r = -1.00 | <0.001 | <0.001 |
| H2 | Control GoalSwitches, w_commit 0.45 - 0 | median diff = -31.99 [-40.83, -28.55] | r = -1.00 | <0.001 | <0.001 |
| H3 | Deathmatch Mission–Cooperation WalkedHits, lambda_E configured - 0 | median diff = -0.0105 [-0.0179, -0.0080] | r = -0.65 | <0.001 | <0.001 |
| H3 | Deathmatch Persistent Objective WalkedHits, lambda_E configured - 0 | median diff = -0.0237 [-0.0278, -0.0205] | r = -0.94 | <0.001 | <0.001 |
| H3 | Deathmatch Aggressive WalkedHits, lambda_E configured - 0 | median diff = -0.0186 [-0.0253, -0.0130] | r = -0.76 | <0.001 | <0.001 |
| H3 | Deathmatch Survival-Aware WalkedHits, lambda_E configured - 0 | median diff = -0.0084 [-0.0126, -0.0048] | r = -0.42 | <0.001 | 0.001 |
| H3 | Sign test, WalkedHits lower with the exposure term (all scenarios x styles) | 12/12 conditions lower | one-sided binomial | <0.001 | 0.001 |
| H3b | Deathmatch Mission–Cooperation AllyDist, lambda_T 10 - 0 | median diff = -0.13 [-0.29, -0.02] | r = -0.33 | 0.004 | 0.004 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.26 | n = 500 | <0.001 | <0.001 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.63 | n = 500 | <0.001 | <0.001 |

## Earlier formulations of the hypotheses (unadjusted; not in the Holm family)

| Hypothesis | Test | Statistic | Effect size | p |
|---|---|---|---|---|
| H2 (earlier formulation) | Mission ObjCommit, w_commit 0.45 - 0 | median diff = +0.15 [+0.13, +0.18] | r = +0.98 | <0.001 |
| H2 (earlier formulation) | Control CtrlScore, w_commit 0.45 - 0 | median diff = +3.50 [+0.00, +43.00] | r = +0.92 | <0.001 |

## Secondary pairwise style contrasts (Mann-Whitney; delta = Cliff's delta = rank-biserial r; HL = Hodges-Lehmann shift A - B with bootstrap 95% CI; unadjusted)

| Scenario | Metric | A | B | delta | HL [95% CI] | p |
|---|---|---|---|---|---|---|
| Mission | ObjCommit | Mission–Cooperation | Persistent Objective | +0.17 | +0.03 [+0.00, +0.05] | 0.040 |
| Mission | ObjCommit | Mission–Cooperation | Aggressive | +0.87 | +0.63 [+0.56, +0.69] | <0.001 |
| Mission | ObjCommit | Mission–Cooperation | Survival-Aware | +1.00 | +0.87 [+0.86, +0.89] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Aggressive | +0.82 | +0.57 [+0.51, +0.64] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Survival-Aware | +1.00 | +0.86 [+0.83, +0.87] | <0.001 |
| Mission | ObjCommit | Aggressive | Survival-Aware | +0.77 | +0.26 [+0.19, +0.32] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Persistent Objective | -0.30 | -0.95 [-1.52, -0.42] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Aggressive | -0.60 | -1.78 [-2.22, -1.34] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Survival-Aware | -0.68 | -3.49 [-4.57, -2.64] | <0.001 |
| Mission | AllyDist | Persistent Objective | Aggressive | -0.20 | -0.75 [-1.30, -0.13] | 0.016 |
| Mission | AllyDist | Persistent Objective | Survival-Aware | -0.45 | -2.52 [-3.62, -1.52] | <0.001 |
| Mission | AllyDist | Aggressive | Survival-Aware | -0.33 | -1.84 [-2.96, -0.91] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Persistent Objective | +0.74 | +0.33 [+0.25, +0.39] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Aggressive | -1.00 | -2.38 [-2.49, -2.27] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Survival-Aware | +0.92 | +0.44 [+0.37, +0.50] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Aggressive | -1.00 | -2.71 [-2.80, -2.61] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Survival-Aware | +0.60 | +0.10 [+0.10, +0.11] | <0.001 |
| Deathmatch | EngRedirect | Aggressive | Survival-Aware | +1.00 | +2.79 [+2.71, +2.92] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Persistent Objective | +0.79 | +0.22 [+0.12, +0.24] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Aggressive | -0.31 | -0.12 [-0.14, -0.03] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Survival-Aware | -0.64 | -0.37 [-0.41, -0.28] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Aggressive | -0.93 | -0.30 [-0.36, -0.25] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Survival-Aware | -0.97 | -0.60 [-0.68, -0.50] | <0.001 |
| Deathmatch | ResSeek | Aggressive | Survival-Aware | -0.50 | -0.26 [-0.33, -0.17] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Persistent Objective | +0.00 | +0.00 [+0.00, +0.00] | 0.995 |
| Control | CtrlScore | Mission–Cooperation | Aggressive | +0.45 | +16.00 [+0.00, +44.00] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Survival-Aware | +0.93 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Aggressive | +0.44 | +12.00 [+0.00, +44.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Survival-Aware | +0.90 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Aggressive | Survival-Aware | +0.60 | +77.00 [+43.00, +98.00] | <0.001 |
