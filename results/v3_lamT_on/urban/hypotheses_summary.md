# Hypothesis tests and effect sizes (urban map)

## Primary tests (Holm-adjusted across all primary tests of this map)

| Hypothesis | Test | Statistic | Effect size | p | p (Holm) |
|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 75.8 | eps2 = 0.63 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 38.4 | eps2 = 0.31 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 72.1 | eps2 = 0.60 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 71.8 | eps2 = 0.59 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 82.1 | eps2 = 0.68 | <0.001 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.72 (chance 0.25) | 5-fold CV, 1000 permutations | <0.001 | 0.009 |
| H1 | Style classification, Deathmatch | accuracy = 0.80 (chance 0.25) | 5-fold CV, 1000 permutations | <0.001 | 0.009 |
| H1 | Style classification, Control | accuracy = 0.77 (chance 0.25) | 5-fold CV, 1000 permutations | <0.001 | 0.009 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.34 [+0.23, +0.60] | r = +0.98 | <0.001 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +0.60 [+0.25, +0.74] | r = +0.81 | <0.001 | <0.001 |
| H2 | Mission ObjCommit, w_commit 0.45 - 0 | median diff = +0.02 [+0.01, +0.02] | r = +0.56 | 0.007 | 0.036 |
| H2 | Control CtrlScore, w_commit 0.45 - 0 | median diff = +0.00 [+0.00, +0.00] | r = +1.00 | 0.250 | 0.750 |
| H3 | Deathmatch Survival-Aware EngRedirect, lambda x1 - x0 | median diff = -0.19 [-0.45, -0.06] | r = -0.54 | 0.009 | 0.037 |
| H3 | Mission Mission–Cooperation AllyDist, lambda x1 - x0 | median diff = +0.00 [-0.00, +0.01] | r = +0.23 | 0.313 | 0.750 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.09 | n = 150 | 0.288 | 0.750 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.27 | n = 150 | 0.001 | 0.009 |

## Secondary pairwise style contrasts (Mann-Whitney; delta = Cliff's delta = rank-biserial r; HL = Hodges-Lehmann shift A - B with bootstrap 95% CI; unadjusted)

| Scenario | Metric | A | B | delta | HL [95% CI] | p |
|---|---|---|---|---|---|---|
| Mission | ObjCommit | Mission–Cooperation | Persistent Objective | +0.15 | +0.00 [+0.00, +0.08] | 0.277 |
| Mission | ObjCommit | Mission–Cooperation | Aggressive | +0.90 | +0.92 [+0.79, +0.98] | <0.001 |
| Mission | ObjCommit | Mission–Cooperation | Survival-Aware | +0.98 | +0.97 [+0.92, +1.00] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Aggressive | +0.78 | +0.86 [+0.65, +0.97] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Survival-Aware | +0.87 | +0.92 [+0.83, +1.00] | <0.001 |
| Mission | ObjCommit | Aggressive | Survival-Aware | +0.18 | +0.00 [+0.00, +0.05] | 0.176 |
| Mission | AllyDist | Mission–Cooperation | Persistent Objective | -0.12 | -0.00 [-0.61, +0.01] | 0.440 |
| Mission | AllyDist | Mission–Cooperation | Aggressive | -0.62 | -0.93 [-1.70, -0.53] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Survival-Aware | -0.83 | -2.39 [-3.51, -1.65] | <0.001 |
| Mission | AllyDist | Persistent Objective | Aggressive | -0.43 | -0.84 [-1.44, -0.34] | 0.005 |
| Mission | AllyDist | Persistent Objective | Survival-Aware | -0.59 | -1.99 [-2.99, -1.14] | <0.001 |
| Mission | AllyDist | Aggressive | Survival-Aware | -0.34 | -1.20 [-2.18, -0.22] | 0.024 |
| Deathmatch | EngRedirect | Mission–Cooperation | Persistent Objective | +0.36 | +0.10 [+0.00, +0.13] | 0.009 |
| Deathmatch | EngRedirect | Mission–Cooperation | Aggressive | -0.89 | -0.86 [-1.02, -0.63] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Survival-Aware | -0.41 | -0.19 [-0.36, -0.06] | 0.006 |
| Deathmatch | EngRedirect | Persistent Objective | Aggressive | -1.00 | -0.99 [-1.13, -0.82] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Survival-Aware | -0.73 | -0.30 [-0.45, -0.17] | <0.001 |
| Deathmatch | EngRedirect | Aggressive | Survival-Aware | +0.78 | +0.63 [+0.44, +0.86] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Persistent Objective | +0.27 | +0.00 [+0.00, +0.00] | 0.003 |
| Deathmatch | ResSeek | Mission–Cooperation | Aggressive | +0.27 | +0.00 [+0.00, +0.00] | 0.003 |
| Deathmatch | ResSeek | Mission–Cooperation | Survival-Aware | -0.68 | -0.38 [-0.58, -0.19] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Aggressive | +0.00 | +0.00 [+0.00, +0.00] | 1.000 |
| Deathmatch | ResSeek | Persistent Objective | Survival-Aware | -0.83 | -0.44 [-0.60, -0.29] | <0.001 |
| Deathmatch | ResSeek | Aggressive | Survival-Aware | -0.83 | -0.44 [-0.60, -0.29] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Persistent Objective | +0.03 | +0.00 [+0.00, +0.00] | 0.334 |
| Control | CtrlScore | Mission–Cooperation | Aggressive | +0.73 | +120.00 [+106.50, +120.00] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Survival-Aware | +0.93 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Aggressive | +0.72 | +120.00 [+94.00, +120.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Survival-Aware | +0.93 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Aggressive | Survival-Aware | +0.17 | +0.00 [+0.00, +1.00] | 0.164 |
