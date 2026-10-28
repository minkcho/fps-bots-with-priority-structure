# Hypothesis tests and effect sizes (urban_s102 map)

## Primary tests (Holm-adjusted across all primary tests of this map)

| Hypothesis | Test | Statistic | Effect size | p | p (Holm) |
|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 289.8 | eps2 = 0.72 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 128.6 | eps2 = 0.32 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 331.7 | eps2 = 0.83 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 208.8 | eps2 = 0.52 | <0.001 | <0.001 |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 205.5 | eps2 = 0.51 | <0.001 | <0.001 |
| H1 | Style classification, Mission | accuracy = 0.77 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | <0.001 |
| H1 | Style classification, Deathmatch | accuracy = 0.96 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | <0.001 |
| H1 | Style classification, Control | accuracy = 0.78 (chance 0.25) | 5-fold CV, 5000 permutations | <0.001 | <0.001 |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.50 [+0.39, +0.57] | r = +0.99 | <0.001 | <0.001 |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +1.44 [+1.33, +1.57] | r = +0.99 | <0.001 | <0.001 |
| H2 | Mission GoalSwitches, w_commit 0.45 - 0 | median diff = -22.74 [-27.01, -19.26] | r = -1.00 | <0.001 | <0.001 |
| H2 | Control GoalSwitches, w_commit 0.45 - 0 | median diff = -27.05 [-31.72, -23.16] | r = -1.00 | <0.001 | <0.001 |
| H3 | Deathmatch Mission–Cooperation WalkedHits, lambda_E configured - 0 | median diff = -0.0105 [-0.0147, -0.0051] | r = -0.57 | <0.001 | <0.001 |
| H3 | Deathmatch Persistent Objective WalkedHits, lambda_E configured - 0 | median diff = -0.0262 [-0.0292, -0.0231] | r = -0.98 | <0.001 | <0.001 |
| H3 | Deathmatch Aggressive WalkedHits, lambda_E configured - 0 | median diff = -0.0130 [-0.0207, -0.0078] | r = -0.72 | <0.001 | <0.001 |
| H3 | Deathmatch Survival-Aware WalkedHits, lambda_E configured - 0 | median diff = -0.0079 [-0.0166, -0.0045] | r = -0.59 | <0.001 | <0.001 |
| H3 | Sign test, WalkedHits lower with the exposure term (all scenarios x styles) | 12/12 conditions lower | one-sided binomial | <0.001 | <0.001 |
| H3b | Deathmatch Mission–Cooperation AllyDist, lambda_T 10 - 0 | median diff = -0.24 [-0.34, -0.16] | r = -0.39 | <0.001 | <0.001 |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.23 | n = 500 | <0.001 | <0.001 |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.64 | n = 500 | <0.001 | <0.001 |

## Earlier formulations of the hypotheses (unadjusted; not in the Holm family)

| Hypothesis | Test | Statistic | Effect size | p |
|---|---|---|---|---|
| H2 (earlier formulation) | Mission ObjCommit, w_commit 0.45 - 0 | median diff = +0.08 [+0.06, +0.12] | r = +0.90 | <0.001 |
| H2 (earlier formulation) | Control CtrlScore, w_commit 0.45 - 0 | median diff = +0.00 [+0.00, +0.00] | r = +0.43 | 0.021 |

## Secondary pairwise style contrasts (Mann-Whitney; delta = Cliff's delta = rank-biserial r; HL = Hodges-Lehmann shift A - B with bootstrap 95% CI; unadjusted)

| Scenario | Metric | A | B | delta | HL [95% CI] | p |
|---|---|---|---|---|---|---|
| Mission | ObjCommit | Mission–Cooperation | Persistent Objective | +0.07 | +0.00 [-0.01, +0.04] | 0.408 |
| Mission | ObjCommit | Mission–Cooperation | Aggressive | +0.89 | +0.60 [+0.53, +0.67] | <0.001 |
| Mission | ObjCommit | Mission–Cooperation | Survival-Aware | +0.99 | +0.88 [+0.85, +0.91] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Aggressive | +0.83 | +0.57 [+0.50, +0.64] | <0.001 |
| Mission | ObjCommit | Persistent Objective | Survival-Aware | +0.98 | +0.87 [+0.85, +0.90] | <0.001 |
| Mission | ObjCommit | Aggressive | Survival-Aware | +0.80 | +0.26 [+0.20, +0.34] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Persistent Objective | -0.25 | -0.68 [-1.25, -0.12] | 0.002 |
| Mission | AllyDist | Mission–Cooperation | Aggressive | -0.69 | -2.11 [-2.52, -1.67] | <0.001 |
| Mission | AllyDist | Mission–Cooperation | Survival-Aware | -0.79 | -3.53 [-4.32, -2.96] | <0.001 |
| Mission | AllyDist | Persistent Objective | Aggressive | -0.36 | -1.31 [-1.84, -0.70] | <0.001 |
| Mission | AllyDist | Persistent Objective | Survival-Aware | -0.57 | -2.87 [-3.62, -2.02] | <0.001 |
| Mission | AllyDist | Aggressive | Survival-Aware | -0.35 | -1.52 [-2.36, -0.78] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Persistent Objective | +0.74 | +0.26 [+0.22, +0.34] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Aggressive | -1.00 | -2.39 [-2.57, -2.21] | <0.001 |
| Deathmatch | EngRedirect | Mission–Cooperation | Survival-Aware | +0.87 | +0.35 [+0.27, +0.41] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Aggressive | -1.00 | -2.70 [-2.87, -2.46] | <0.001 |
| Deathmatch | EngRedirect | Persistent Objective | Survival-Aware | +0.39 | +0.00 [+0.00, +0.00] | <0.001 |
| Deathmatch | EngRedirect | Aggressive | Survival-Aware | +1.00 | +2.78 [+2.53, +2.93] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Persistent Objective | +0.68 | +0.12 [+0.11, +0.22] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Aggressive | -0.29 | -0.11 [-0.14, -0.03] | <0.001 |
| Deathmatch | ResSeek | Mission–Cooperation | Survival-Aware | -0.56 | -0.30 [-0.39, -0.26] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Aggressive | -0.89 | -0.28 [-0.34, -0.24] | <0.001 |
| Deathmatch | ResSeek | Persistent Objective | Survival-Aware | -0.96 | -0.51 [-0.60, -0.49] | <0.001 |
| Deathmatch | ResSeek | Aggressive | Survival-Aware | -0.47 | -0.23 [-0.29, -0.16] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Persistent Objective | +0.02 | +0.00 [+0.00, +0.00] | 0.723 |
| Control | CtrlScore | Mission–Cooperation | Aggressive | +0.41 | +6.00 [+0.00, +60.00] | <0.001 |
| Control | CtrlScore | Mission–Cooperation | Survival-Aware | +0.89 | +120.00 [+120.00, +120.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Aggressive | +0.41 | +6.00 [+0.00, +57.00] | <0.001 |
| Control | CtrlScore | Persistent Objective | Survival-Aware | +0.91 | +120.00 [+119.00, +120.00] | <0.001 |
| Control | CtrlScore | Aggressive | Survival-Aware | +0.54 | +60.00 [+21.98, +108.00] | <0.001 |
