# Hypothesis tests and effect sizes (random_s102 map)

## Primary tests (Holm-adjusted across all primary tests of this map)

| Hypothesis | Test | Statistic | Effect size | p | p (Holm) |
|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 299.2 | eps2 = 0.75 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 165.9 | eps2 = 0.41 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 295.9 | eps2 = 0.74 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 216.5 | eps2 = 0.54 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 272.7 | eps2 = 0.68 | <0.001 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.80 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Style classification, Deathmatch | accuracy = 0.95 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Style classification, Control | accuracy = 0.77 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.49 [+0.40, +0.59] | r = +0.98 | <0.001 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +1.50 [+1.42, +1.74] | r = +0.99 | <0.001 | <0.001 |
| H2 | Mission GoalSwitches, w_commit 0.45 - 0 | median diff = -13.16 [-18.28, -9.98] | r = -1.00 | <0.001 | <0.001 |
| H2 | Control GoalSwitches, w_commit 0.45 - 0 | median diff = -21.40 [-23.22, -18.94] | r = -1.00 | <0.001 | <0.001 |
| H3 | Deathmatch Mission–Cooperation WalkedHits, lambda_E configured - 0 | median diff = -0.0085 [-0.0155, -0.0054] | r = -0.51 | <0.001 | <0.001 |
| H3 | Deathmatch Persistent Objective WalkedHits, lambda_E configured - 0 | median diff = -0.0261 [-0.0305, -0.0221] | r = -0.97 | <0.001 | <0.001 |
| H3 | Deathmatch Aggressive WalkedHits, lambda_E configured - 0 | median diff = -0.0156 [-0.0231, -0.0100] | r = -0.67 | <0.001 | <0.001 |
| H3 | Deathmatch Survival-Aware WalkedHits, lambda_E configured - 0 | median diff = -0.0057 [-0.0106, -0.0025] | r = -0.29 | 0.011 | 0.021 |
| H3 | Sign test, WalkedHits lower with the exposure term (all scenarios x styles) | 12/12 conditions lower | one-sided binomial | <0.001 | 0.001 |
| H3b | Deathmatch Mission–Cooperation AllyDist, lambda_T 10 - 0 | median diff = -0.17 [-0.31, -0.01] | r = -0.21 | 0.068 | 0.068 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.24 | n = 500 | <0.001 | <0.001 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.66 | n = 500 | <0.001 | <0.001 |

## Earlier formulations of the hypotheses (unadjusted; not in the Holm family)

| Hypothesis | Test | Statistic | Effect size | p |
|---|---|---|---|---|
| H2 (earlier formulation) | Mission ObjCommit, w_commit 0.45 - 0 | median diff = +0.07 [+0.03, +0.11] | r = +0.81 | <0.001 |
| H2 (earlier formulation) | Control CtrlScore, w_commit 0.45 - 0 | median diff = +0.00 [+0.00, +0.00] | r = +0.55 | 0.008 |

## Secondary pairwise style contrasts (Mann-Whitney; delta = Cliff's delta = rank-biserial r; HL = Hodges-Lehmann shift A - B with bootstrap 95% CI; unadjusted)

| Scenario | Metric | A | B | delta | HL [95% CI] | p |
|---|---|---|---|---|---|---|
| Mission | ObjCommit | Mission–Cooperation | Persistent Objective | +0.21 | +0.03 [+0.00, +0.05] | 0.010 |
| Mission | ObjCommit | Mission–Cooperation | Aggressive | +0.91 | +0.65 [+0.59, +0.72] | <0.001 |
| Mission | ObjCommit | Mission–Cooperation | Survival-Aware | +1.00 | +0.90 [+0.89, +0.92] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Aggressive | +0.84 | +0.60 [+0.53, +0.67] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Survival-Aware | +1.00 | +0.87 [+0.84, +0.89] | <0.001 |
| Mission | ObjCommit | Aggressive | Survival-Aware | +0.81 | +0.25 [+0.17, +0.31] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Persistent Objective | -0.34 | -1.02 [-1.39, -0.51] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Aggressive | -0.72 | -2.26 [-2.61, -1.90] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Survival-Aware | -0.87 | -4.08 [-4.52, -3.61] | <0.001 |
| Mission | AllyDist | Persistent Objective | Aggressive | -0.38 | -1.17 [-1.69, -0.74] | <0.001 |
| Mission | AllyDist | Persistent Objective | Survival-Aware | -0.68 | -3.07 [-3.79, -2.48] | <0.001 |
| Mission | AllyDist | Aggressive | Survival-Aware | -0.50 | -1.86 [-2.49, -1.28] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Persistent Objective | +0.74 | +0.37 [+0.31, +0.47] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Aggressive | -0.97 | -2.46 [-2.58, -2.32] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Survival-Aware | +0.79 | +0.44 [+0.32, +0.52] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Aggressive | -0.99 | -2.84 [-2.98, -2.71] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Survival-Aware | +0.30 | +0.00 [+0.00, +0.10] | <0.001 |
| Deathmatch | EngRedirect | Aggressive | Survival-Aware | +0.99 | +2.88 [+2.73, +3.03] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Persistent Objective | +0.70 | +0.13 [+0.12, +0.21] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Aggressive | -0.42 | -0.14 [-0.18, -0.10] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Survival-Aware | -0.66 | -0.38 [-0.45, -0.29] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Aggressive | -0.90 | -0.29 [-0.37, -0.26] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Survival-Aware | -0.90 | -0.52 [-0.61, -0.50] | <0.001 |
| Deathmatch | ResSeek | Aggressive | Survival-Aware | -0.48 | -0.24 [-0.31, -0.16] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Persistent Objective | -0.06 | +0.00 [+0.00, +0.00] | 0.047 |
| Control | CtrlScore | Mission–Cooperation | Aggressive | +0.45 | +10.00 [+0.00, +37.00] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Survival-Aware | +0.95 | +120.00 [+119.00, +120.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Aggressive | +0.52 | +13.00 [+0.00, +45.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Survival-Aware | +0.99 | +120.00 [+119.00, +120.00] | <0.001 |
| Control | CtrlScore | Aggressive | Survival-Aware | +0.72 | +89.00 [+72.00, +113.00] | <0.001 |
