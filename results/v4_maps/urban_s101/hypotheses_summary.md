# Hypothesis tests and effect sizes (urban_s101 map)

## Primary tests (Holm-adjusted across all primary tests of this map)

| Hypothesis | Test | Statistic | Effect size | p | p (Holm) |
|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 298.5 | eps2 = 0.75 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 121.1 | eps2 = 0.30 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 346.7 | eps2 = 0.87 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 238.4 | eps2 = 0.59 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 247.6 | eps2 = 0.62 | <0.001 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.80 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Style classification, Deathmatch | accuracy = 0.98 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Style classification, Control | accuracy = 0.84 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | 0.001 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.50 [+0.47, +0.61] | r = +0.99 | <0.001 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +1.32 [+1.15, +1.43] | r = +1.00 | <0.001 | <0.001 |
| H2 | Mission GoalSwitches, w_commit 0.45 - 0 | median diff = -22.20 [-27.04, -18.97] | r = -1.00 | <0.001 | <0.001 |
| H2 | Control GoalSwitches, w_commit 0.45 - 0 | median diff = -27.55 [-30.06, -25.75] | r = -1.00 | <0.001 | <0.001 |
| H3 | Deathmatch Mission–Cooperation WalkedHits, lambda_E configured - 0 | median diff = -0.0084 [-0.0120, -0.0054] | r = -0.49 | <0.001 | <0.001 |
| H3 | Deathmatch Persistent Objective WalkedHits, lambda_E configured - 0 | median diff = -0.0224 [-0.0264, -0.0191] | r = -0.90 | <0.001 | <0.001 |
| H3 | Deathmatch Aggressive WalkedHits, lambda_E configured - 0 | median diff = -0.0085 [-0.0160, -0.0043] | r = -0.55 | <0.001 | <0.001 |
| H3 | Deathmatch Survival-Aware WalkedHits, lambda_E configured - 0 | median diff = -0.0074 [-0.0127, -0.0013] | r = -0.43 | <0.001 | 0.001 |
| H3 | Sign test, WalkedHits lower with the exposure term (all scenarios x styles) | 10/12 conditions lower | one-sided binomial | 0.019 | 0.019 |
| H3b | Deathmatch Mission–Cooperation AllyDist, lambda_T 10 - 0 | median diff = -0.35 [-0.52, -0.21] | r = -0.61 | <0.001 | <0.001 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.17 | n = 500 | <0.001 | 0.001 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.65 | n = 500 | <0.001 | <0.001 |

## Earlier formulations of the hypotheses (unadjusted; not in the Holm family)

| Hypothesis | Test | Statistic | Effect size | p |
|---|---|---|---|---|
| H2 (earlier formulation) | Mission ObjCommit, w_commit 0.45 - 0 | median diff = +0.08 [+0.05, +0.11] | r = +0.88 | <0.001 |
| H2 (earlier formulation) | Control CtrlScore, w_commit 0.45 - 0 | median diff = +0.00 [+0.00, +0.00] | r = +0.80 | <0.001 |

## Secondary pairwise style contrasts (Mann-Whitney; delta = Cliff's delta = rank-biserial r; HL = Hodges-Lehmann shift A - B with bootstrap 95% CI; unadjusted)

| Scenario | Metric | A | B | delta | HL [95% CI] | p |
|---|---|---|---|---|---|---|
| Mission | ObjCommit | Mission–Cooperation | Persistent Objective | +0.01 | +0.00 [-0.02, +0.03] | 0.919 |
| Mission | ObjCommit | Mission–Cooperation | Aggressive | +0.89 | +0.64 [+0.56, +0.71] | <0.001 |
| Mission | ObjCommit | Mission–Cooperation | Survival-Aware | +1.00 | +0.88 [+0.87, +0.90] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Aggressive | +0.85 | +0.62 [+0.53, +0.69] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Survival-Aware | +1.00 | +0.88 [+0.86, +0.91] | <0.001 |
| Mission | ObjCommit | Aggressive | Survival-Aware | +0.81 | +0.23 [+0.16, +0.31] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Persistent Objective | -0.20 | -0.61 [-1.21, -0.06] | 0.013 |
| Mission | AllyDist | Mission–Cooperation | Aggressive | -0.64 | -2.08 [-2.49, -1.58] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Survival-Aware | -0.80 | -3.40 [-4.07, -2.80] | <0.001 |
| Mission | AllyDist | Persistent Objective | Aggressive | -0.32 | -1.23 [-1.78, -0.62] | <0.001 |
| Mission | AllyDist | Persistent Objective | Survival-Aware | -0.56 | -2.67 [-3.28, -2.04] | <0.001 |
| Mission | AllyDist | Aggressive | Survival-Aware | -0.35 | -1.49 [-2.19, -0.84] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Persistent Objective | +0.85 | +0.32 [+0.24, +0.35] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Aggressive | -1.00 | -2.43 [-2.56, -2.29] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Survival-Aware | +0.94 | +0.35 [+0.32, +0.42] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Aggressive | -1.00 | -2.77 [-2.89, -2.58] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Survival-Aware | +0.40 | +0.00 [+0.00, +0.05] | <0.001 |
| Deathmatch | EngRedirect | Aggressive | Survival-Aware | +1.00 | +2.82 [+2.60, +2.97] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Persistent Objective | +0.78 | +0.22 [+0.12, +0.25] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Aggressive | -0.18 | -0.03 [-0.12, +0.00] | 0.032 |
| Deathmatch | ResSeek | Mission–Cooperation | Survival-Aware | -0.64 | -0.36 [-0.40, -0.28] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Aggressive | -0.92 | -0.25 [-0.32, -0.23] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Survival-Aware | -0.98 | -0.60 [-0.63, -0.50] | <0.001 |
| Deathmatch | ResSeek | Aggressive | Survival-Aware | -0.63 | -0.28 [-0.37, -0.24] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Persistent Objective | +0.03 | +0.00 [+0.00, +0.00] | 0.532 |
| Control | CtrlScore | Mission–Cooperation | Aggressive | +0.60 | +60.00 [+17.00, +80.00] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Survival-Aware | +0.94 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Aggressive | +0.58 | +57.00 [+12.00, +80.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Survival-Aware | +0.94 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Aggressive | Survival-Aware | +0.54 | +46.00 [+14.00, +71.00] | <0.001 |
