# Hypothesis tests and effect sizes (urban map)

## Primary tests (Holm-adjusted across all primary tests of this map)

| Hypothesis | Test | Statistic | Effect size | p | p (Holm) |
|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 291.0 | eps2 = 0.73 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 178.3 | eps2 = 0.44 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 347.4 | eps2 = 0.87 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 223.8 | eps2 = 0.56 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 262.4 | eps2 = 0.65 | <0.001 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.79 (chance 0.25) | 5-fold CV, 1000 permutations | <0.001 | 0.006 |
| H1 | Style classification, Deathmatch | accuracy = 0.98 (chance 0.25) | 5-fold CV, 1000 permutations | <0.001 | 0.006 |
| H1 | Style classification, Control | accuracy = 0.79 (chance 0.25) | 5-fold CV, 1000 permutations | <0.001 | 0.006 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.50 [+0.43, +0.60] | r = +0.97 | <0.001 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +1.30 [+1.19, +1.41] | r = +1.00 | <0.001 | <0.001 |
| H2 | Mission GoalSwitches, w_commit 0.45 - 0 | median diff = -14.82 [-18.32, -9.53] | r = -1.00 | <0.001 | <0.001 |
| H2 | Control GoalSwitches, w_commit 0.45 - 0 | median diff = -22.99 [-27.63, -20.35] | r = -1.00 | <0.001 | <0.001 |
| H3 | Deathmatch Mission–Cooperation WalkedHits, lambda_E configured - 0 | median diff = -0.0081 [-0.0124, -0.0025] | r = -0.36 | 0.002 | 0.006 |
| H3 | Deathmatch Persistent Objective WalkedHits, lambda_E configured - 0 | median diff = -0.0267 [-0.0318, -0.0219] | r = -0.97 | <0.001 | <0.001 |
| H3 | Deathmatch Aggressive WalkedHits, lambda_E configured - 0 | median diff = -0.0173 [-0.0205, -0.0125] | r = -0.79 | <0.001 | <0.001 |
| H3 | Deathmatch Survival-Aware WalkedHits, lambda_E configured - 0 | median diff = -0.0054 [-0.0112, +0.0013] | r = -0.31 | 0.007 | 0.010 |
| H3 | Sign test, WalkedHits lower with the exposure term (all scenarios x styles) | 12/12 conditions lower | one-sided binomial | <0.001 | 0.002 |
| H3b | Deathmatch Mission–Cooperation AllyDist, lambda_T 10 - 0 | median diff = -0.20 [-0.35, -0.02] | r = -0.32 | 0.005 | 0.010 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.20 | n = 500 | <0.001 | <0.001 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.67 | n = 500 | <0.001 | <0.001 |

## Earlier formulations of the hypotheses (unadjusted; not in the Holm family)

| Hypothesis | Test | Statistic | Effect size | p |
|---|---|---|---|---|
| H2 (earlier formulation) | Mission ObjCommit, w_commit 0.45 - 0 | median diff = +0.08 [+0.05, +0.11] | r = +0.83 | <0.001 |
| H2 (earlier formulation) | Control CtrlScore, w_commit 0.45 - 0 | median diff = +0.00 [+0.00, +0.00] | r = +0.96 | <0.001 |
| H3 (earlier formulation: Survival-Aware lambda scale) | Deathmatch Survival-Aware WalkedHits, lambda x1 - x0 | median diff = -0.002 [-0.007, +0.002] | r = -0.21 | 0.066 |
| H3 (earlier formulation: Survival-Aware lambda scale) | Deathmatch Survival-Aware LOSFraction, lambda x1 - x0 | median diff = -0.003 [-0.015, +0.009] | r = -0.10 | 0.385 |
| H3 (earlier formulation: Survival-Aware lambda scale) | Deathmatch Survival-Aware Deaths, lambda x1 - x0 | median diff = -1.000 [-1.000, +0.000] | r = -0.22 | 0.074 |
| H3 (earlier formulation: Survival-Aware lambda scale) | Deathmatch Survival-Aware EngRedirect, lambda x1 - x0 | median diff = +0.000 [+0.000, +0.000] | r = +0.00 | 1.000 |
| H3 (earlier formulation: Survival-Aware lambda scale) | Mission Mission–Cooperation AllyDist, lambda x1 - x0 | median diff = +0.000 [-0.001, +0.002] | r = -0.10 | 0.416 |

## Secondary pairwise style contrasts (Mann-Whitney; delta = Cliff's delta = rank-biserial r; HL = Hodges-Lehmann shift A - B with bootstrap 95% CI; unadjusted)

| Scenario | Metric | A | B | delta | HL [95% CI] | p |
|---|---|---|---|---|---|---|
| Mission | ObjCommit | Mission–Cooperation | Persistent Objective | +0.22 | +0.02 [+0.00, +0.06] | 0.006 |
| Mission | ObjCommit | Mission–Cooperation | Aggressive | +0.90 | +0.68 [+0.62, +0.75] | <0.001 |
| Mission | ObjCommit | Mission–Cooperation | Survival-Aware | +0.99 | +0.94 [+0.91, +0.96] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Aggressive | +0.83 | +0.63 [+0.56, +0.69] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Survival-Aware | +0.97 | +0.89 [+0.87, +0.91] | <0.001 |
| Mission | ObjCommit | Aggressive | Survival-Aware | +0.76 | +0.22 [+0.17, +0.30] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Persistent Objective | -0.32 | -0.78 [-1.32, -0.07] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Aggressive | -0.78 | -2.65 [-3.15, -2.21] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Survival-Aware | -0.92 | -4.65 [-5.36, -3.93] | <0.001 |
| Mission | AllyDist | Persistent Objective | Aggressive | -0.42 | -1.63 [-2.25, -1.02] | <0.001 |
| Mission | AllyDist | Persistent Objective | Survival-Aware | -0.70 | -3.68 [-4.37, -2.95] | <0.001 |
| Mission | AllyDist | Aggressive | Survival-Aware | -0.44 | -2.07 [-2.80, -1.34] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Persistent Objective | +0.84 | +0.35 [+0.31, +0.43] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Aggressive | -1.00 | -2.40 [-2.55, -2.26] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Survival-Aware | +0.96 | +0.46 [+0.35, +0.52] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Aggressive | -1.00 | -2.78 [-2.91, -2.63] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Survival-Aware | +0.55 | +0.10 [+0.00, +0.10] | <0.001 |
| Deathmatch | EngRedirect | Aggressive | Survival-Aware | +1.00 | +2.87 [+2.68, +3.01] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Persistent Objective | +0.70 | +0.15 [+0.12, +0.23] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Aggressive | -0.37 | -0.13 [-0.17, -0.08] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Survival-Aware | -0.66 | -0.39 [-0.48, -0.30] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Aggressive | -0.93 | -0.28 [-0.36, -0.25] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Survival-Aware | -0.93 | -0.60 [-0.63, -0.52] | <0.001 |
| Deathmatch | ResSeek | Aggressive | Survival-Aware | -0.52 | -0.27 [-0.36, -0.19] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Persistent Objective | -0.02 | +0.00 [+0.00, +0.00] | 0.545 |
| Control | CtrlScore | Mission–Cooperation | Aggressive | +0.48 | +12.00 [+0.00, +48.00] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Survival-Aware | +0.96 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Aggressive | +0.48 | +4.00 [+0.00, +47.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Survival-Aware | +0.94 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Aggressive | Survival-Aware | +0.65 | +90.00 [+58.00, +116.00] | <0.001 |
