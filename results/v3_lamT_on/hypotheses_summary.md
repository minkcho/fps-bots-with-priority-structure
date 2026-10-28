# Hypothesis tests and effect sizes (random map)

## Primary tests (Holm-adjusted across all primary tests of this map)

| Hypothesis | Test | Statistic | Effect size | p | p (Holm) |
|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 87.6 | eps2 = 0.73 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 27.5 | eps2 = 0.21 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 75.5 | eps2 = 0.63 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 80.1 | eps2 = 0.66 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 72.6 | eps2 = 0.60 | <0.001 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.73 (chance 0.25) | 5-fold CV, 1000 permutations | <0.001 | 0.007 |
| H1 | Style classification, Deathmatch | accuracy = 0.87 (chance 0.25) | 5-fold CV, 1000 permutations | <0.001 | 0.007 |
| H1 | Style classification, Control | accuracy = 0.71 (chance 0.25) | 5-fold CV, 1000 permutations | <0.001 | 0.007 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.39 [+0.24, +0.50] | r = +0.97 | <0.001 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +0.55 [+0.33, +0.81] | r = +0.93 | <0.001 | <0.001 |
| H2 | Mission ObjCommit, w_commit 0.45 - 0 | median diff = +0.02 [+0.01, +0.06] | r = +0.54 | 0.010 | 0.042 |
| H2 | Control CtrlScore, w_commit 0.45 - 0 | median diff = +0.00 [+0.00, +0.00] | r = +0.52 | 0.281 | 0.562 |
| H3 | Deathmatch Survival-Aware EngRedirect, lambda x1 - x0 | median diff = -0.70 [-1.33, -0.39] | r = -0.68 | <0.001 | 0.005 |
| H3 | Mission Mission–Cooperation AllyDist, lambda x1 - x0 | median diff = +0.00 [-0.01, +0.01] | r = -0.14 | 0.596 | 0.596 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.12 | n = 150 | 0.149 | 0.446 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.51 | n = 150 | <0.001 | <0.001 |

## Secondary pairwise style contrasts (Mann-Whitney; delta = Cliff's delta = rank-biserial r; HL = Hodges-Lehmann shift A - B with bootstrap 95% CI; unadjusted)

| Scenario | Metric | A | B | delta | HL [95% CI] | p |
|---|---|---|---|---|---|---|
| Mission | ObjCommit | Mission–Cooperation | Persistent Objective | +0.24 | +0.03 [+0.00, +0.07] | 0.109 |
| Mission | ObjCommit | Mission–Cooperation | Aggressive | +0.94 | +0.89 [+0.75, +0.94] | <0.001 |
| Mission | ObjCommit | Mission–Cooperation | Survival-Aware | +1.00 | +0.94 [+0.91, +0.95] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Aggressive | +0.91 | +0.83 [+0.69, +0.90] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Survival-Aware | +1.00 | +0.92 [+0.86, +0.95] | <0.001 |
| Mission | ObjCommit | Aggressive | Survival-Aware | +0.37 | +0.01 [+0.00, +0.19] | 0.007 |
| Mission | AllyDist | Mission–Cooperation | Persistent Objective | -0.20 | -0.39 [-1.21, +0.02] | 0.180 |
| Mission | AllyDist | Mission–Cooperation | Aggressive | -0.59 | -1.81 [-2.61, -0.94] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Survival-Aware | -0.66 | -2.10 [-3.20, -1.09] | <0.001 |
| Mission | AllyDist | Persistent Objective | Aggressive | -0.40 | -1.23 [-2.14, -0.29] | 0.008 |
| Mission | AllyDist | Persistent Objective | Survival-Aware | -0.48 | -1.60 [-2.87, -0.54] | 0.002 |
| Mission | AllyDist | Aggressive | Survival-Aware | -0.12 | -0.49 [-1.65, +0.64] | 0.420 |
| Deathmatch | EngRedirect | Mission–Cooperation | Persistent Objective | +0.39 | +0.10 [+0.00, +0.11] | 0.006 |
| Deathmatch | EngRedirect | Mission–Cooperation | Aggressive | -0.94 | -1.24 [-1.46, -0.99] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Survival-Aware | -0.60 | -0.46 [-0.71, -0.20] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Aggressive | -0.99 | -1.40 [-1.59, -1.10] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Survival-Aware | -0.79 | -0.55 [-0.84, -0.29] | <0.001 |
| Deathmatch | EngRedirect | Aggressive | Survival-Aware | +0.64 | +0.70 [+0.41, +0.97] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Persistent Objective | +0.37 | +0.00 [+0.00, +0.10] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Aggressive | +0.40 | +0.00 [+0.00, +0.10] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Survival-Aware | -0.76 | -0.38 [-0.50, -0.19] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Aggressive | +0.03 | +0.00 [+0.00, +0.00] | 0.334 |
| Deathmatch | ResSeek | Persistent Objective | Survival-Aware | -0.92 | -0.39 [-0.51, -0.29] | <0.001 |
| Deathmatch | ResSeek | Aggressive | Survival-Aware | -0.93 | -0.39 [-0.51, -0.29] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Persistent Objective | -0.03 | +0.00 [+0.00, +0.00] | 0.557 |
| Control | CtrlScore | Mission–Cooperation | Aggressive | +0.68 | +120.00 [+50.00, +120.00] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Survival-Aware | +0.85 | +120.00 [+118.00, +120.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Aggressive | +0.72 | +120.00 [+50.00, +120.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Survival-Aware | +0.89 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Aggressive | Survival-Aware | +0.19 | +0.00 [+0.00, +19.00] | 0.146 |
