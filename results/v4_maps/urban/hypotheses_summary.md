# Hypothesis tests and effect sizes (urban map)

## Primary tests (Holm-adjusted across all primary tests of this map)

| Hypothesis | Test | Statistic | Effect size | p | p (Holm) |
|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 307.5 | eps2 = 0.77 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 180.1 | eps2 = 0.45 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 345.8 | eps2 = 0.87 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 231.8 | eps2 = 0.58 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 221.5 | eps2 = 0.55 | <0.001 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.78 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Style classification, Deathmatch | accuracy = 0.97 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Style classification, Control | accuracy = 0.78 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.50 [+0.41, +0.59] | r = +0.98 | <0.001 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +1.37 [+1.27, +1.55] | r = +1.00 | <0.001 | <0.001 |
| H2 | Mission GoalSwitches, w_commit 0.45 - 0 | median diff = -15.21 [-17.22, -11.47] | r = -1.00 | <0.001 | <0.001 |
| H2 | Control GoalSwitches, w_commit 0.45 - 0 | median diff = -24.14 [-27.12, -21.13] | r = -1.00 | <0.001 | <0.001 |
| H3 | Deathmatch Mission–Cooperation WalkedHits, lambda_E configured - 0 | median diff = -0.0059 [-0.0099, -0.0009] | r = -0.34 | 0.003 | 0.009 |
| H3 | Deathmatch Persistent Objective WalkedHits, lambda_E configured - 0 | median diff = -0.0234 [-0.0258, -0.0198] | r = -0.93 | <0.001 | <0.001 |
| H3 | Deathmatch Aggressive WalkedHits, lambda_E configured - 0 | median diff = -0.0156 [-0.0195, -0.0111] | r = -0.68 | <0.001 | <0.001 |
| H3 | Deathmatch Survival-Aware WalkedHits, lambda_E configured - 0 | median diff = -0.0049 [-0.0090, +0.0024] | r = -0.21 | 0.062 | 0.110 |
| H3 | Sign test, WalkedHits lower with the exposure term (all scenarios x styles) | 12/12 conditions lower | one-sided binomial | <0.001 | 0.001 |
| H3b | Deathmatch Mission–Cooperation AllyDist, lambda_T 10 - 0 | median diff = -0.33 [-0.46, -0.15] | r = -0.59 | <0.001 | <0.001 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.09 | n = 500 | 0.055 | 0.110 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.66 | n = 500 | <0.001 | <0.001 |

## Earlier formulations of the hypotheses (unadjusted; not in the Holm family)

| Hypothesis | Test | Statistic | Effect size | p |
|---|---|---|---|---|
| H2 (earlier formulation) | Mission ObjCommit, w_commit 0.45 - 0 | median diff = +0.09 [+0.05, +0.12] | r = +0.90 | <0.001 |
| H2 (earlier formulation) | Control CtrlScore, w_commit 0.45 - 0 | median diff = +0.00 [+0.00, +0.00] | r = +0.64 | 0.003 |

## Secondary pairwise style contrasts (Mann-Whitney; delta = Cliff's delta = rank-biserial r; HL = Hodges-Lehmann shift A - B with bootstrap 95% CI; unadjusted)

| Scenario | Metric | A | B | delta | HL [95% CI] | p |
|---|---|---|---|---|---|---|
| Mission | ObjCommit | Mission–Cooperation | Persistent Objective | +0.08 | +0.00 [+0.00, +0.00] | 0.309 |
| Mission | ObjCommit | Mission–Cooperation | Aggressive | +0.94 | +0.75 [+0.69, +0.81] | <0.001 |
| Mission | ObjCommit | Mission–Cooperation | Survival-Aware | +1.00 | +0.96 [+0.94, +0.98] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Aggressive | +0.89 | +0.71 [+0.61, +0.76] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Survival-Aware | +1.00 | +0.95 [+0.90, +0.99] | <0.001 |
| Mission | ObjCommit | Aggressive | Survival-Aware | +0.73 | +0.17 [+0.13, +0.24] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Persistent Objective | -0.11 | -0.04 [-0.30, +0.00] | 0.189 |
| Mission | AllyDist | Mission–Cooperation | Aggressive | -0.82 | -2.81 [-3.26, -2.42] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Survival-Aware | -0.91 | -4.35 [-5.29, -3.70] | <0.001 |
| Mission | AllyDist | Persistent Objective | Aggressive | -0.54 | -2.31 [-2.79, -1.62] | <0.001 |
| Mission | AllyDist | Persistent Objective | Survival-Aware | -0.72 | -3.89 [-4.65, -2.99] | <0.001 |
| Mission | AllyDist | Aggressive | Survival-Aware | -0.39 | -1.91 [-2.88, -1.05] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Persistent Objective | +0.82 | +0.34 [+0.26, +0.39] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Aggressive | -1.00 | -2.36 [-2.46, -2.24] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Survival-Aware | +0.96 | +0.43 [+0.36, +0.47] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Aggressive | -1.00 | -2.69 [-2.79, -2.61] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Survival-Aware | +0.59 | +0.10 [+0.00, +0.11] | <0.001 |
| Deathmatch | EngRedirect | Aggressive | Survival-Aware | +1.00 | +2.79 [+2.72, +2.91] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Persistent Objective | +0.69 | +0.21 [+0.12, +0.23] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Aggressive | -0.32 | -0.12 [-0.14, -0.03] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Survival-Aware | -0.66 | -0.39 [-0.48, -0.29] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Aggressive | -0.95 | -0.27 [-0.34, -0.24] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Survival-Aware | -0.95 | -0.60 [-0.63, -0.51] | <0.001 |
| Deathmatch | ResSeek | Aggressive | Survival-Aware | -0.59 | -0.28 [-0.37, -0.23] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Persistent Objective | +0.04 | +0.00 [+0.00, +0.00] | 0.345 |
| Control | CtrlScore | Mission–Cooperation | Aggressive | +0.47 | +12.00 [+0.00, +48.00] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Survival-Aware | +0.91 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Aggressive | +0.43 | +8.00 [+0.00, +42.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Survival-Aware | +0.89 | +120.00 [+119.00, +120.00] | <0.001 |
| Control | CtrlScore | Aggressive | Survival-Aware | +0.60 | +74.00 [+38.00, +100.00] | <0.001 |
