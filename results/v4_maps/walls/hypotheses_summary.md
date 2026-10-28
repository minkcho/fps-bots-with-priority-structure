# Hypothesis tests and effect sizes (walls map)

## Primary tests (Holm-adjusted across all primary tests of this map)

| Hypothesis | Test | Statistic | Effect size | p | p (Holm) |
|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 271.5 | eps2 = 0.68 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 177.4 | eps2 = 0.44 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 322.2 | eps2 = 0.81 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 210.5 | eps2 = 0.52 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 225.2 | eps2 = 0.56 | <0.001 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.73 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | <0.001 |
| H1 | Style classification, Deathmatch | accuracy = 0.96 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | <0.001 |
| H1 | Style classification, Control | accuracy = 0.71 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | <0.001 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.48 [+0.39, +0.51] | r = +0.98 | <0.001 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +1.03 [+0.84, +1.18] | r = +0.96 | <0.001 | <0.001 |
| H2 | Mission GoalSwitches, w_commit 0.45 - 0 | median diff = -16.11 [-21.95, -12.86] | r = -1.00 | <0.001 | <0.001 |
| H2 | Control GoalSwitches, w_commit 0.45 - 0 | median diff = -23.86 [-27.41, -20.60] | r = -1.00 | <0.001 | <0.001 |
| H3 | Deathmatch Mission–Cooperation WalkedHits, lambda_E configured - 0 | median diff = -0.0100 [-0.0145, -0.0049] | r = -0.56 | <0.001 | <0.001 |
| H3 | Deathmatch Persistent Objective WalkedHits, lambda_E configured - 0 | median diff = -0.0227 [-0.0277, -0.0177] | r = -0.93 | <0.001 | <0.001 |
| H3 | Deathmatch Aggressive WalkedHits, lambda_E configured - 0 | median diff = -0.0162 [-0.0183, -0.0120] | r = -0.80 | <0.001 | <0.001 |
| H3 | Deathmatch Survival-Aware WalkedHits, lambda_E configured - 0 | median diff = -0.0078 [-0.0120, -0.0013] | r = -0.55 | <0.001 | <0.001 |
| H3 | Sign test, WalkedHits lower with the exposure term (all scenarios x styles) | 12/12 conditions lower | one-sided binomial | <0.001 | <0.001 |
| H3b | Deathmatch Mission–Cooperation AllyDist, lambda_T 10 - 0 | median diff = -0.28 [-0.35, -0.08] | r = -0.45 | <0.001 | <0.001 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.12 | n = 500 | 0.008 | 0.008 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.64 | n = 500 | <0.001 | <0.001 |

## Earlier formulations of the hypotheses (unadjusted; not in the Holm family)

| Hypothesis | Test | Statistic | Effect size | p |
|---|---|---|---|---|
| H2 (earlier formulation) | Mission ObjCommit, w_commit 0.45 - 0 | median diff = +0.06 [+0.04, +0.09] | r = +0.99 | <0.001 |
| H2 (earlier formulation) | Control CtrlScore, w_commit 0.45 - 0 | median diff = +0.00 [+0.00, +0.00] | r = +0.96 | <0.001 |

## Secondary pairwise style contrasts (Mann-Whitney; delta = Cliff's delta = rank-biserial r; HL = Hodges-Lehmann shift A - B with bootstrap 95% CI; unadjusted)

| Scenario | Metric | A | B | delta | HL [95% CI] | p |
|---|---|---|---|---|---|---|
| Mission | ObjCommit | Mission–Cooperation | Persistent Objective | +0.14 | +0.01 [+0.00, +0.04] | 0.072 |
| Mission | ObjCommit | Mission–Cooperation | Aggressive | +0.83 | +0.54 [+0.44, +0.65] | <0.001 |
| Mission | ObjCommit | Mission–Cooperation | Survival-Aware | +0.99 | +0.94 [+0.91, +0.96] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Aggressive | +0.75 | +0.50 [+0.40, +0.60] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Survival-Aware | +0.97 | +0.92 [+0.89, +0.94] | <0.001 |
| Mission | ObjCommit | Aggressive | Survival-Aware | +0.75 | +0.36 [+0.26, +0.47] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Persistent Objective | -0.19 | -0.29 [-0.63, -0.00] | 0.020 |
| Mission | AllyDist | Mission–Cooperation | Aggressive | -0.66 | -2.17 [-2.66, -1.77] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Survival-Aware | -0.91 | -4.75 [-5.23, -4.10] | <0.001 |
| Mission | AllyDist | Persistent Objective | Aggressive | -0.45 | -1.64 [-2.20, -1.06] | <0.001 |
| Mission | AllyDist | Persistent Objective | Survival-Aware | -0.77 | -4.16 [-4.87, -3.46] | <0.001 |
| Mission | AllyDist | Aggressive | Survival-Aware | -0.55 | -2.54 [-3.25, -1.85] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Persistent Objective | +0.67 | +0.23 [+0.21, +0.32] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Aggressive | -0.99 | -2.02 [-2.14, -1.90] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Survival-Aware | +0.82 | +0.32 [+0.23, +0.34] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Aggressive | -1.00 | -2.26 [-2.37, -2.19] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Survival-Aware | +0.43 | +0.00 [+0.00, +0.10] | <0.001 |
| Deathmatch | EngRedirect | Aggressive | Survival-Aware | +1.00 | +2.33 [+2.21, +2.46] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Persistent Objective | +0.76 | +0.20 [+0.12, +0.24] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Aggressive | -0.10 | -0.01 [-0.09, +0.01] | 0.241 |
| Deathmatch | ResSeek | Mission–Cooperation | Survival-Aware | -0.58 | -0.29 [-0.38, -0.25] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Aggressive | -0.81 | -0.23 [-0.29, -0.13] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Survival-Aware | -0.95 | -0.51 [-0.59, -0.48] | <0.001 |
| Deathmatch | ResSeek | Aggressive | Survival-Aware | -0.59 | -0.28 [-0.37, -0.20] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Persistent Objective | +0.08 | +0.00 [+0.00, +0.00] | 0.032 |
| Control | CtrlScore | Mission–Cooperation | Aggressive | +0.46 | +0.00 [+0.00, +65.00] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Survival-Aware | +0.92 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Aggressive | +0.39 | +0.00 [+0.00, +58.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Survival-Aware | +0.87 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Aggressive | Survival-Aware | +0.54 | +62.00 [+29.96, +118.05] | <0.001 |
