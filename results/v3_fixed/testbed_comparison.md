# Earlier testbed vs testbed with the movement and perception fixes (same model, same seeds)

- a (earlier): `../repro_outputs/v3` — rules: (no testbed_flags.txt: the final run, all rules off)
- b (fixed): `../repro_outputs/v3_fixed` — rules: {'teammate_swap': True, 'local_avoidance': True, 'forget_reached_memory': True, 'symmetric_los': True, 'reachable_placement': True}

## random map

### Primary tests (Holm across each testbed's primary tests)

| Hyp. | Test | a: statistic; effect | a: p_Holm | b: statistic; effect | b: p_Holm | at 0.05 |
|---|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 278.5; eps2 = 0.70 | <0.001 | H = 281.7; eps2 = 0.70 | <0.001 | same |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 123.4; eps2 = 0.30 | <0.001 | H = 160.1; eps2 = 0.40 | <0.001 | same |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 300.6; eps2 = 0.75 | <0.001 | H = 343.6; eps2 = 0.86 | <0.001 | same |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 205.4; eps2 = 0.51 | <0.001 | H = 211.8; eps2 = 0.53 | <0.001 | same |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 219.5; eps2 = 0.55 | <0.001 | H = 234.7; eps2 = 0.59 | <0.001 | same |
| H1 | Style classification, Mission | accuracy = 0.77 (chance 0.25); 5-fold CV, 1000 permutations | 0.007 | accuracy = 0.75 (chance 0.25); 5-fold CV, 1000 permutations | 0.005 | same |
| H1 | Style classification, Deathmatch | accuracy = 0.90 (chance 0.25); 5-fold CV, 1000 permutations | 0.007 | accuracy = 0.98 (chance 0.25); 5-fold CV, 1000 permutations | 0.005 | same |
| H1 | Style classification, Control | accuracy = 0.73 (chance 0.25); 5-fold CV, 1000 permutations | 0.007 | accuracy = 0.74 (chance 0.25); 5-fold CV, 1000 permutations | 0.005 | same |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.19 [+0.18, +0.29]; r = +0.94 | <0.001 | median diff = +0.51 [+0.39, +0.61]; r = +0.95 | <0.001 | same |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +0.60 [+0.48, +0.73]; r = +0.86 | <0.001 | median diff = +1.43 [+1.28, +1.54]; r = +1.00 | <0.001 | same |
| H2 | Mission GoalSwitches, w_commit 0.45 - 0 | median diff = -4.91 [-7.32, -4.00]; r = -0.98 | <0.001 | median diff = -20.39 [-24.15, -13.52]; r = -1.00 | <0.001 | same |
| H2 | Control GoalSwitches, w_commit 0.45 - 0 | median diff = -14.38 [-15.83, -12.20]; r = -1.00 | <0.001 | median diff = -21.39 [-24.78, -20.06]; r = -1.00 | <0.001 | same |
| H3 | Deathmatch Mission–Cooperation WalkedHits, lambda_E configured - 0 | median diff = -0.0081 [-0.0220, +0.0024]; r = -0.32 | 0.020 | median diff = -0.0097 [-0.0136, -0.0017]; r = -0.39 | 0.004 | same |
| H3 | Deathmatch Persistent Objective WalkedHits, lambda_E configured - 0 | median diff = -0.0256 [-0.0314, -0.0202]; r = -0.89 | <0.001 | median diff = -0.0214 [-0.0267, -0.0154]; r = -0.96 | <0.001 | same |
| H3 | Deathmatch Aggressive WalkedHits, lambda_E configured - 0 | median diff = -0.0167 [-0.0235, -0.0136]; r = -0.55 | <0.001 | median diff = -0.0150 [-0.0185, -0.0125]; r = -0.77 | <0.001 | same |
| H3 | Deathmatch Survival-Aware WalkedHits, lambda_E configured - 0 | median diff = -0.0014 [-0.0072, +0.0008]; r = -0.24 | 0.039 | median diff = -0.0026 [-0.0072, +0.0015]; r = -0.15 | 0.179 | lost |
| H3 | Sign test, WalkedHits lower with the exposure term (all scenarios x styles) | 11/12 conditions lower; one-sided binomial | 0.013 | 12/12 conditions lower; one-sided binomial | 0.002 | same |
| H3b | Deathmatch Mission–Cooperation AllyDist, lambda_T 10 - 0 | median diff = -0.33 [-0.71, -0.03]; r = -0.39 | 0.005 | median diff = -0.31 [-0.49, -0.11]; r = -0.53 | <0.001 | same |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.11; n = 500 | 0.024 | rho = +0.15; n = 500 | 0.005 | same |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.53; n = 500 | <0.001 | rho = -0.70; n = 500 | <0.001 | same |

### Main experiment (means; paired Wilcoxon b vs a by episode seed, Holm within condition)

| Scenario | Style | Metric | a | b | r | p_Holm |
|---|---|---|---|---|---|---|
| Mission | Mission–Cooperation | ObjCommit | 0.95 ± 0.02 | 0.94 ± 0.01 | -0.44 | 0.003 |
| Mission | Mission–Cooperation | AllyDist | 1.66 ± 0.17 | 2.08 ± 0.18 | +0.59 | <0.001 |
| Mission | Mission–Cooperation | EngRedirect | 0.00 ± 0.00 | 0.01 ± 0.01 | +0.69 | 0.086 |
| Mission | Mission–Cooperation | Kills | 3.87 ± 0.80 | 6.25 ± 0.94 | +0.69 | <0.001 |
| Mission | Mission–Cooperation | Deaths | 2.95 ± 0.63 | 5.06 ± 0.82 | +0.80 | <0.001 |
| Mission | Mission–Cooperation | WalkedHits | 0.03 ± 0.01 | 0.04 ± 0.01 | +0.65 | <0.001 |
| Mission | Mission–Cooperation | HitsTaken | 0.01 ± 0.00 | 0.02 ± 0.00 | +0.77 | <0.001 |
| Mission | Persistent Objective | ObjCommit | 0.92 ± 0.02 | 0.91 ± 0.02 | -0.28 | 0.079 |
| Mission | Persistent Objective | AllyDist | 2.29 ± 0.28 | 2.82 ± 0.38 | +0.43 | 0.001 |
| Mission | Persistent Objective | EngRedirect | 0.00 ± 0.00 | 0.01 ± 0.01 | +0.62 | 0.090 |
| Mission | Persistent Objective | Kills | 5.09 ± 0.92 | 6.42 ± 0.93 | +0.42 | 0.012 |
| Mission | Persistent Objective | Deaths | 4.20 ± 0.82 | 5.16 ± 0.83 | +0.42 | 0.013 |
| Mission | Persistent Objective | WalkedHits | 0.03 ± 0.01 | 0.04 ± 0.01 | +0.46 | 0.002 |
| Mission | Persistent Objective | HitsTaken | 0.02 ± 0.00 | 0.03 ± 0.00 | +0.39 | 0.013 |
| Mission | Aggressive | ObjCommit | 0.28 ± 0.07 | 0.37 ± 0.06 | +0.36 | 0.020 |
| Mission | Aggressive | AllyDist | 3.64 ± 0.43 | 4.42 ± 0.36 | +0.39 | 0.004 |
| Mission | Aggressive | EngRedirect | 0.72 ± 0.11 | 1.45 ± 0.20 | +0.72 | <0.001 |
| Mission | Aggressive | Kills | 5.32 ± 0.80 | 6.43 ± 0.85 | +0.31 | 0.038 |
| Mission | Aggressive | Deaths | 5.59 ± 0.84 | 6.24 ± 0.84 | +0.17 | 0.175 |
| Mission | Aggressive | WalkedHits | 0.03 ± 0.01 | 0.04 ± 0.01 | +0.32 | 0.032 |
| Mission | Aggressive | HitsTaken | 0.03 ± 0.00 | 0.03 ± 0.00 | +0.30 | 0.038 |
| Mission | Survival-Aware | ObjCommit | 0.05 ± 0.03 | 0.05 ± 0.03 | +0.10 | 1.000 |
| Mission | Survival-Aware | AllyDist | 5.63 ± 0.87 | 6.80 ± 0.84 | +0.27 | 0.143 |
| Mission | Survival-Aware | EngRedirect | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Mission | Survival-Aware | Kills | 3.16 ± 0.48 | 3.01 ± 0.44 | -0.03 | 1.000 |
| Mission | Survival-Aware | Deaths | 2.63 ± 0.46 | 2.93 ± 0.45 | +0.12 | 1.000 |
| Mission | Survival-Aware | WalkedHits | 0.02 ± 0.00 | 0.02 ± 0.00 | +0.05 | 1.000 |
| Mission | Survival-Aware | HitsTaken | 0.01 ± 0.00 | 0.02 ± 0.00 | +0.08 | 1.000 |
| Deathmatch | Mission–Cooperation | EngRedirect | 0.31 ± 0.08 | 0.47 ± 0.06 | +0.48 | <0.001 |
| Deathmatch | Mission–Cooperation | ResSeek | 0.06 ± 0.02 | 0.25 ± 0.05 | +0.83 | <0.001 |
| Deathmatch | Mission–Cooperation | AllyDist | 2.40 ± 0.23 | 2.86 ± 0.11 | +0.56 | <0.001 |
| Deathmatch | Mission–Cooperation | Kills | 7.13 ± 0.84 | 10.14 ± 0.53 | +0.63 | <0.001 |
| Deathmatch | Mission–Cooperation | Deaths | 5.46 ± 0.67 | 9.27 ± 0.53 | +0.82 | <0.001 |
| Deathmatch | Mission–Cooperation | WalkedHits | 0.05 ± 0.01 | 0.07 ± 0.00 | +0.69 | <0.001 |
| Deathmatch | Mission–Cooperation | HitsTaken | 0.03 ± 0.00 | 0.05 ± 0.00 | +0.87 | <0.001 |
| Deathmatch | Persistent Objective | EngRedirect | 0.05 ± 0.01 | 0.08 ± 0.02 | +0.37 | 0.011 |
| Deathmatch | Persistent Objective | ResSeek | 0.01 ± 0.00 | 0.03 ± 0.01 | +0.76 | 0.002 |
| Deathmatch | Persistent Objective | AllyDist | 5.40 ± 0.35 | 5.81 ± 0.29 | +0.18 | 0.114 |
| Deathmatch | Persistent Objective | Kills | 8.06 ± 0.55 | 9.04 ± 0.44 | +0.35 | 0.011 |
| Deathmatch | Persistent Objective | Deaths | 4.67 ± 0.41 | 5.86 ± 0.42 | +0.48 | <0.001 |
| Deathmatch | Persistent Objective | WalkedHits | 0.04 ± 0.00 | 0.06 ± 0.00 | +0.69 | <0.001 |
| Deathmatch | Persistent Objective | HitsTaken | 0.03 ± 0.00 | 0.04 ± 0.00 | +0.62 | <0.001 |
| Deathmatch | Aggressive | EngRedirect | 1.37 ± 0.10 | 2.84 ± 0.10 | +1.00 | <0.001 |
| Deathmatch | Aggressive | ResSeek | 0.00 ± 0.00 | 0.33 ± 0.04 | +1.00 | <0.001 |
| Deathmatch | Aggressive | AllyDist | 4.50 ± 0.46 | 5.11 ± 0.23 | +0.39 | 0.001 |
| Deathmatch | Aggressive | Kills | 10.10 ± 0.73 | 11.86 ± 0.51 | +0.42 | 0.001 |
| Deathmatch | Aggressive | Deaths | 10.29 ± 0.74 | 12.22 ± 0.49 | +0.51 | <0.001 |
| Deathmatch | Aggressive | WalkedHits | 0.07 ± 0.01 | 0.09 ± 0.00 | +0.80 | <0.001 |
| Deathmatch | Aggressive | HitsTaken | 0.05 ± 0.00 | 0.07 ± 0.00 | +0.78 | <0.001 |
| Deathmatch | Survival-Aware | EngRedirect | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Deathmatch | Survival-Aware | ResSeek | 0.29 ± 0.05 | 0.57 ± 0.06 | +0.69 | <0.001 |
| Deathmatch | Survival-Aware | AllyDist | 5.76 ± 0.82 | 7.20 ± 0.79 | +0.27 | 0.041 |
| Deathmatch | Survival-Aware | Kills | 3.15 ± 0.45 | 4.86 ± 0.43 | +0.61 | <0.001 |
| Deathmatch | Survival-Aware | Deaths | 2.32 ± 0.39 | 4.65 ± 0.50 | +0.75 | <0.001 |
| Deathmatch | Survival-Aware | WalkedHits | 0.02 ± 0.00 | 0.03 ± 0.00 | +0.71 | <0.001 |
| Deathmatch | Survival-Aware | HitsTaken | 0.01 ± 0.00 | 0.02 ± 0.00 | +0.68 | <0.001 |
| Control | Mission–Cooperation | CtrlScore | 110.56 ± 5.82 | 117.58 ± 2.45 | +0.68 | 0.119 |
| Control | Mission–Cooperation | ObjCommit | 0.95 ± 0.01 | 0.94 ± 0.01 | -0.10 | 0.890 |
| Control | Mission–Cooperation | AllyDist | 1.88 ± 0.22 | 2.22 ± 0.21 | +0.45 | <0.001 |
| Control | Mission–Cooperation | Kills | 2.11 ± 0.44 | 2.29 ± 0.40 | +0.17 | 0.890 |
| Control | Mission–Cooperation | Deaths | 1.35 ± 0.37 | 1.52 ± 0.39 | +0.15 | 0.890 |
| Control | Mission–Cooperation | WalkedHits | 0.03 ± 0.01 | 0.04 ± 0.01 | +0.25 | 0.342 |
| Control | Mission–Cooperation | HitsTaken | 0.02 ± 0.00 | 0.02 ± 0.00 | +0.24 | 0.342 |
| Control | Persistent Objective | CtrlScore | 117.08 ± 3.09 | 114.95 ± 3.93 | -0.26 | 0.850 |
| Control | Persistent Objective | ObjCommit | 0.91 ± 0.03 | 0.90 ± 0.03 | -0.29 | 0.193 |
| Control | Persistent Objective | AllyDist | 2.33 ± 0.38 | 3.05 ± 0.41 | +0.52 | <0.001 |
| Control | Persistent Objective | Kills | 2.38 ± 0.42 | 2.43 ± 0.41 | +0.03 | 0.872 |
| Control | Persistent Objective | Deaths | 1.53 ± 0.39 | 1.94 ± 0.47 | +0.30 | 0.193 |
| Control | Persistent Objective | WalkedHits | 0.04 ± 0.01 | 0.04 ± 0.01 | +0.24 | 0.220 |
| Control | Persistent Objective | HitsTaken | 0.02 ± 0.00 | 0.03 ± 0.00 | +0.32 | 0.106 |
| Control | Aggressive | CtrlScore | 43.60 ± 11.17 | 70.06 ± 10.78 | +0.55 | 0.001 |
| Control | Aggressive | ObjCommit | 0.19 ± 0.06 | 0.32 ± 0.06 | +0.65 | <0.001 |
| Control | Aggressive | AllyDist | 4.28 ± 0.41 | 4.35 ± 0.35 | +0.06 | 0.601 |
| Control | Aggressive | Kills | 6.31 ± 0.83 | 5.02 ± 0.81 | -0.35 | 0.024 |
| Control | Aggressive | Deaths | 6.28 ± 0.84 | 4.93 ± 0.78 | -0.36 | 0.024 |
| Control | Aggressive | WalkedHits | 0.05 ± 0.00 | 0.06 ± 0.01 | +0.19 | 0.317 |
| Control | Aggressive | HitsTaken | 0.04 ± 0.00 | 0.04 ± 0.01 | +0.16 | 0.339 |
| Control | Survival-Aware | CtrlScore | 15.53 ± 7.48 | 13.59 ± 6.58 | -0.09 | 1.000 |
| Control | Survival-Aware | ObjCommit | 0.04 ± 0.03 | 0.03 ± 0.02 | -0.01 | 1.000 |
| Control | Survival-Aware | AllyDist | 5.35 ± 0.84 | 6.05 ± 0.63 | +0.20 | 0.444 |
| Control | Survival-Aware | Kills | 2.17 ± 0.36 | 2.32 ± 0.42 | +0.01 | 1.000 |
| Control | Survival-Aware | Deaths | 1.80 ± 0.37 | 2.21 ± 0.42 | +0.17 | 0.693 |
| Control | Survival-Aware | WalkedHits | 0.02 ± 0.00 | 0.02 ± 0.00 | +0.38 | 0.007 |
| Control | Survival-Aware | HitsTaken | 0.01 ± 0.00 | 0.02 ± 0.00 | +0.37 | 0.008 |

Control wins (a -> b): Mission–Cooperation: 88 -> 95; Persistent Objective: 96 -> 91; Aggressive: 31 -> 47; Survival-Aware: 11 -> 7

### H3, WalkedHits per alive step: configured lambda_E vs 0 (change; Deathmatch p_Holm over 4 styles)

| Scenario | Style | a: change | a: p | b: change | b: p |
|---|---|---|---|---|---|
| Mission | Mission–Cooperation | -31% | <0.001 | -6% | 0.018 |
| Mission | Persistent Objective | -21% | <0.001 | -11% | 0.002 |
| Mission | Aggressive | -21% | 0.023 | -13% | 0.003 |
| Mission | Survival-Aware | +3% | 0.799 | -23% | <0.001 |
| Deathmatch | Mission–Cooperation | -17% | 0.013 | -9% | 0.001 |
| Deathmatch | Persistent Objective | -36% | <0.001 | -29% | <0.001 |
| Deathmatch | Aggressive | -19% | <0.001 | -14% | <0.001 |
| Deathmatch | Survival-Aware | -24% | 0.039 | -8% | 0.179 |
| Control | Mission–Cooperation | -17% | <0.001 | -4% | 0.239 |
| Control | Persistent Objective | -10% | <0.001 | -3% | 0.108 |
| Control | Aggressive | -12% | 0.022 | -4% | 0.206 |
| Control | Survival-Aware | -26% | 0.005 | -23% | <0.001 |

Sign test (lower with the exposure term): a 11/12 (p 0.003), b 12/12 (p <0.001)

### H3, HitsTaken per alive step: configured lambda_E vs 0 (change; Deathmatch p_Holm over 4 styles)

| Scenario | Style | a: change | a: p | b: change | b: p |
|---|---|---|---|---|---|
| Mission | Mission–Cooperation | -32% | <0.001 | -5% | 0.177 |
| Mission | Persistent Objective | -17% | 0.003 | -9% | 0.057 |
| Mission | Aggressive | -18% | 0.046 | -13% | 0.017 |
| Mission | Survival-Aware | +9% | 0.481 | -18% | 0.008 |
| Deathmatch | Mission–Cooperation | -20% | 0.041 | -5% | 0.115 |
| Deathmatch | Persistent Objective | -33% | <0.001 | -26% | <0.001 |
| Deathmatch | Aggressive | -14% | 0.003 | -10% | <0.001 |
| Deathmatch | Survival-Aware | -19% | 0.182 | -5% | 0.274 |
| Control | Mission–Cooperation | -19% | 0.001 | -7% | 0.083 |
| Control | Persistent Objective | -10% | 0.030 | -0% | 0.709 |
| Control | Aggressive | -9% | 0.192 | -2% | 0.245 |
| Control | Survival-Aware | -16% | 0.098 | -17% | 0.008 |

Sign test (lower with the exposure term): a 11/12 (p 0.003), b 12/12 (p <0.001)

### Movement stalls >= 50 steps (share of episodes, either team)

| Scenario | Style | a | b |
|---|---|---|---|
| Mission | Mission–Cooperation | 26% | 0% |
| Mission | Persistent Objective | 17% | 0% |
| Mission | Aggressive | 36% | 0% |
| Mission | Survival-Aware | 31% | 0% |
| Deathmatch | Mission–Cooperation | 40% | 0% |
| Deathmatch | Persistent Objective | 11% | 0% |
| Deathmatch | Aggressive | 14% | 0% |
| Deathmatch | Survival-Aware | 30% | 1% |
| Control | Mission–Cooperation | 9% | 0% |
| Control | Persistent Objective | 3% | 0% |
| Control | Aggressive | 13% | 0% |
| Control | Survival-Aware | 34% | 0% |

All conditions: a 22.0%, b 0.1%

## urban map

### Primary tests (Holm across each testbed's primary tests)

| Hyp. | Test | a: statistic; effect | a: p_Holm | b: statistic; effect | b: p_Holm | at 0.05 |
|---|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | H = 294.6; eps2 = 0.74 | <0.001 | H = 291.0; eps2 = 0.73 | <0.001 | same |
| H1 | Kruskal-Wallis, Mission AllyDist | H = 161.4; eps2 = 0.40 | <0.001 | H = 178.3; eps2 = 0.44 | <0.001 | same |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | H = 309.0; eps2 = 0.77 | <0.001 | H = 347.4; eps2 = 0.87 | <0.001 | same |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | H = 237.7; eps2 = 0.59 | <0.001 | H = 223.8; eps2 = 0.56 | <0.001 | same |
| H1 | Kruskal-Wallis, Control CtrlScore | H = 270.0; eps2 = 0.67 | <0.001 | H = 262.4; eps2 = 0.65 | <0.001 | same |
| H1 | Style classification, Mission | accuracy = 0.76 (chance 0.25); 5-fold CV, 1000 permutations | 0.006 | accuracy = 0.79 (chance 0.25); 5-fold CV, 1000 permutations | 0.006 | same |
| H1 | Style classification, Deathmatch | accuracy = 0.89 (chance 0.25); 5-fold CV, 1000 permutations | 0.006 | accuracy = 0.98 (chance 0.25); 5-fold CV, 1000 permutations | 0.006 | same |
| H1 | Style classification, Control | accuracy = 0.76 (chance 0.25); 5-fold CV, 1000 permutations | 0.006 | accuracy = 0.79 (chance 0.25); 5-fold CV, 1000 permutations | 0.006 | same |
| H1 | Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | median diff = +0.30 [+0.28, +0.40]; r = +1.00 | <0.001 | median diff = +0.50 [+0.43, +0.60]; r = +0.97 | <0.001 | same |
| H1 | Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | median diff = +0.51 [+0.33, +0.70]; r = +0.79 | <0.001 | median diff = +1.30 [+1.19, +1.41]; r = +1.00 | <0.001 | same |
| H2 | Mission GoalSwitches, w_commit 0.45 - 0 | median diff = -7.51 [-9.28, -4.36]; r = -1.00 | <0.001 | median diff = -14.82 [-18.32, -9.53]; r = -1.00 | <0.001 | same |
| H2 | Control GoalSwitches, w_commit 0.45 - 0 | median diff = -14.60 [-16.87, -13.12]; r = -1.00 | <0.001 | median diff = -22.99 [-27.63, -20.35]; r = -1.00 | <0.001 | same |
| H3 | Deathmatch Mission–Cooperation WalkedHits, lambda_E configured - 0 | median diff = -0.0113 [-0.0178, -0.0047]; r = -0.29 | 0.043 | median diff = -0.0081 [-0.0124, -0.0025]; r = -0.36 | 0.006 | same |
| H3 | Deathmatch Persistent Objective WalkedHits, lambda_E configured - 0 | median diff = -0.0307 [-0.0347, -0.0241]; r = -0.93 | <0.001 | median diff = -0.0267 [-0.0318, -0.0219]; r = -0.97 | <0.001 | same |
| H3 | Deathmatch Aggressive WalkedHits, lambda_E configured - 0 | median diff = -0.0173 [-0.0265, -0.0035]; r = -0.46 | <0.001 | median diff = -0.0173 [-0.0205, -0.0125]; r = -0.79 | <0.001 | same |
| H3 | Deathmatch Survival-Aware WalkedHits, lambda_E configured - 0 | median diff = -0.0048 [-0.0084, +0.0008]; r = -0.22 | 0.061 | median diff = -0.0054 [-0.0112, +0.0013]; r = -0.31 | 0.010 | gained |
| H3 | Sign test, WalkedHits lower with the exposure term (all scenarios x styles) | 12/12 conditions lower; one-sided binomial | 0.002 | 12/12 conditions lower; one-sided binomial | 0.002 | same |
| H3b | Deathmatch Mission–Cooperation AllyDist, lambda_T 10 - 0 | median diff = -0.34 [-0.60, -0.16]; r = -0.47 | <0.001 | median diff = -0.20 [-0.35, -0.02]; r = -0.32 | 0.010 | same |
| H4 | Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | rho = +0.11; n = 500 | 0.043 | rho = +0.20; n = 500 | <0.001 | same |
| H4 | Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | rho = -0.39; n = 500 | <0.001 | rho = -0.67; n = 500 | <0.001 | same |

### Main experiment (means; paired Wilcoxon b vs a by episode seed, Holm within condition)

| Scenario | Style | Metric | a | b | r | p_Holm |
|---|---|---|---|---|---|---|
| Mission | Mission–Cooperation | ObjCommit | 0.95 ± 0.02 | 0.94 ± 0.01 | -0.42 | 0.009 |
| Mission | Mission–Cooperation | AllyDist | 1.51 ± 0.16 | 1.77 ± 0.18 | +0.53 | <0.001 |
| Mission | Mission–Cooperation | EngRedirect | 0.00 ± 0.00 | 0.02 ± 0.01 | +0.69 | 0.026 |
| Mission | Mission–Cooperation | Kills | 2.64 ± 0.76 | 5.03 ± 0.94 | +0.76 | <0.001 |
| Mission | Mission–Cooperation | Deaths | 2.27 ± 0.72 | 4.22 ± 0.89 | +0.68 | <0.001 |
| Mission | Mission–Cooperation | WalkedHits | 0.02 ± 0.01 | 0.03 ± 0.01 | +0.64 | <0.001 |
| Mission | Mission–Cooperation | HitsTaken | 0.01 ± 0.00 | 0.02 ± 0.00 | +0.68 | <0.001 |
| Mission | Persistent Objective | ObjCommit | 0.92 ± 0.03 | 0.87 ± 0.04 | -0.50 | <0.001 |
| Mission | Persistent Objective | AllyDist | 2.27 ± 0.50 | 3.00 ± 0.41 | +0.57 | <0.001 |
| Mission | Persistent Objective | EngRedirect | 0.01 ± 0.01 | 0.00 ± 0.00 | -0.90 | 0.062 |
| Mission | Persistent Objective | Kills | 2.66 ± 0.76 | 5.23 ± 0.89 | +0.80 | <0.001 |
| Mission | Persistent Objective | Deaths | 2.43 ± 0.77 | 5.19 ± 0.98 | +0.89 | <0.001 |
| Mission | Persistent Objective | WalkedHits | 0.02 ± 0.01 | 0.04 ± 0.01 | +0.88 | <0.001 |
| Mission | Persistent Objective | HitsTaken | 0.01 ± 0.00 | 0.03 ± 0.01 | +0.83 | <0.001 |
| Mission | Aggressive | ObjCommit | 0.19 ± 0.06 | 0.32 ± 0.06 | +0.49 | <0.001 |
| Mission | Aggressive | AllyDist | 3.95 ± 0.47 | 4.48 ± 0.41 | +0.24 | 0.043 |
| Mission | Aggressive | EngRedirect | 0.73 ± 0.10 | 1.69 ± 0.20 | +0.79 | <0.001 |
| Mission | Aggressive | Kills | 5.74 ± 0.82 | 7.25 ± 0.89 | +0.32 | 0.031 |
| Mission | Aggressive | Deaths | 6.13 ± 0.83 | 7.29 ± 0.88 | +0.30 | 0.033 |
| Mission | Aggressive | WalkedHits | 0.04 ± 0.01 | 0.05 ± 0.01 | +0.45 | <0.001 |
| Mission | Aggressive | HitsTaken | 0.03 ± 0.00 | 0.04 ± 0.01 | +0.43 | 0.001 |
| Mission | Survival-Aware | ObjCommit | 0.05 ± 0.03 | 0.04 ± 0.03 | +0.06 | 1.000 |
| Mission | Survival-Aware | AllyDist | 6.39 ± 1.02 | 6.89 ± 0.71 | +0.24 | 0.272 |
| Mission | Survival-Aware | EngRedirect | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Mission | Survival-Aware | Kills | 2.97 ± 0.44 | 3.29 ± 0.42 | +0.14 | 1.000 |
| Mission | Survival-Aware | Deaths | 2.49 ± 0.42 | 2.89 ± 0.46 | +0.15 | 1.000 |
| Mission | Survival-Aware | WalkedHits | 0.02 ± 0.00 | 0.02 ± 0.00 | +0.19 | 0.571 |
| Mission | Survival-Aware | HitsTaken | 0.01 ± 0.00 | 0.02 ± 0.00 | +0.12 | 1.000 |
| Deathmatch | Mission–Cooperation | EngRedirect | 0.35 ± 0.08 | 0.46 ± 0.05 | +0.45 | <0.001 |
| Deathmatch | Mission–Cooperation | ResSeek | 0.08 ± 0.03 | 0.24 ± 0.05 | +0.69 | <0.001 |
| Deathmatch | Mission–Cooperation | AllyDist | 2.32 ± 0.14 | 2.69 ± 0.09 | +0.54 | <0.001 |
| Deathmatch | Mission–Cooperation | Kills | 7.33 ± 0.79 | 10.15 ± 0.60 | +0.56 | <0.001 |
| Deathmatch | Mission–Cooperation | Deaths | 6.38 ± 0.73 | 9.12 ± 0.62 | +0.63 | <0.001 |
| Deathmatch | Mission–Cooperation | WalkedHits | 0.05 ± 0.01 | 0.07 ± 0.00 | +0.72 | <0.001 |
| Deathmatch | Mission–Cooperation | HitsTaken | 0.03 ± 0.00 | 0.05 ± 0.00 | +0.73 | <0.001 |
| Deathmatch | Persistent Objective | EngRedirect | 0.05 ± 0.02 | 0.09 ± 0.02 | +0.59 | <0.001 |
| Deathmatch | Persistent Objective | ResSeek | 0.01 ± 0.01 | 0.02 ± 0.01 | +0.38 | 0.196 |
| Deathmatch | Persistent Objective | AllyDist | 5.48 ± 0.34 | 5.61 ± 0.26 | +0.09 | 0.445 |
| Deathmatch | Persistent Objective | Kills | 7.33 ± 0.51 | 7.84 ± 0.45 | +0.18 | 0.303 |
| Deathmatch | Persistent Objective | Deaths | 4.09 ± 0.38 | 5.69 ± 0.45 | +0.61 | <0.001 |
| Deathmatch | Persistent Objective | WalkedHits | 0.04 ± 0.00 | 0.05 ± 0.00 | +0.68 | <0.001 |
| Deathmatch | Persistent Objective | HitsTaken | 0.03 ± 0.00 | 0.04 ± 0.00 | +0.70 | <0.001 |
| Deathmatch | Aggressive | EngRedirect | 1.14 ± 0.10 | 2.86 ± 0.13 | +1.00 | <0.001 |
| Deathmatch | Aggressive | ResSeek | 0.00 ± 0.00 | 0.35 ± 0.04 | +1.00 | <0.001 |
| Deathmatch | Aggressive | AllyDist | 4.50 ± 0.46 | 4.73 ± 0.20 | +0.19 | 0.100 |
| Deathmatch | Aggressive | Kills | 9.18 ± 0.74 | 11.76 ± 0.50 | +0.67 | <0.001 |
| Deathmatch | Aggressive | Deaths | 9.16 ± 0.71 | 11.41 ± 0.53 | +0.53 | <0.001 |
| Deathmatch | Aggressive | WalkedHits | 0.06 ± 0.00 | 0.09 ± 0.00 | +0.85 | <0.001 |
| Deathmatch | Aggressive | HitsTaken | 0.05 ± 0.00 | 0.07 ± 0.00 | +0.83 | <0.001 |
| Deathmatch | Survival-Aware | EngRedirect | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Deathmatch | Survival-Aware | ResSeek | 0.40 ± 0.06 | 0.61 ± 0.06 | +0.56 | <0.001 |
| Deathmatch | Survival-Aware | AllyDist | 5.96 ± 0.69 | 7.42 ± 0.57 | +0.42 | <0.001 |
| Deathmatch | Survival-Aware | Kills | 3.80 ± 0.47 | 4.70 ± 0.46 | +0.33 | 0.014 |
| Deathmatch | Survival-Aware | Deaths | 3.18 ± 0.47 | 4.72 ± 0.50 | +0.53 | <0.001 |
| Deathmatch | Survival-Aware | WalkedHits | 0.02 ± 0.00 | 0.03 ± 0.00 | +0.61 | <0.001 |
| Deathmatch | Survival-Aware | HitsTaken | 0.02 ± 0.00 | 0.03 ± 0.00 | +0.54 | <0.001 |
| Control | Mission–Cooperation | CtrlScore | 113.03 ± 4.73 | 117.30 ± 2.64 | +0.43 | 0.508 |
| Control | Mission–Cooperation | ObjCommit | 0.94 ± 0.02 | 0.95 ± 0.01 | +0.07 | 1.000 |
| Control | Mission–Cooperation | AllyDist | 1.88 ± 0.31 | 1.84 ± 0.24 | -0.02 | 1.000 |
| Control | Mission–Cooperation | Kills | 1.56 ± 0.50 | 2.23 ± 0.53 | +0.48 | 0.011 |
| Control | Mission–Cooperation | Deaths | 1.45 ± 0.51 | 1.75 ± 0.53 | +0.26 | 0.508 |
| Control | Mission–Cooperation | WalkedHits | 0.02 ± 0.01 | 0.03 ± 0.01 | +0.56 | 0.001 |
| Control | Mission–Cooperation | HitsTaken | 0.01 ± 0.00 | 0.02 ± 0.01 | +0.51 | 0.004 |
| Control | Persistent Objective | CtrlScore | 118.80 ± 2.38 | 116.86 ± 3.49 | -0.80 | 0.750 |
| Control | Persistent Objective | ObjCommit | 0.91 ± 0.03 | 0.91 ± 0.03 | -0.14 | 0.913 |
| Control | Persistent Objective | AllyDist | 2.74 ± 0.57 | 2.79 ± 0.54 | +0.09 | 0.913 |
| Control | Persistent Objective | Kills | 1.58 ± 0.43 | 2.03 ± 0.43 | +0.44 | 0.030 |
| Control | Persistent Objective | Deaths | 1.25 ± 0.41 | 1.54 ± 0.46 | +0.27 | 0.579 |
| Control | Persistent Objective | WalkedHits | 0.03 ± 0.01 | 0.03 ± 0.01 | +0.55 | 0.001 |
| Control | Persistent Objective | HitsTaken | 0.02 ± 0.00 | 0.02 ± 0.01 | +0.42 | 0.026 |
| Control | Aggressive | CtrlScore | 26.39 ± 9.21 | 73.61 ± 10.43 | +0.75 | <0.001 |
| Control | Aggressive | ObjCommit | 0.13 ± 0.04 | 0.29 ± 0.05 | +0.75 | <0.001 |
| Control | Aggressive | AllyDist | 3.95 ± 0.48 | 4.69 ± 0.36 | +0.36 | 0.005 |
| Control | Aggressive | Kills | 5.86 ± 0.79 | 6.11 ± 0.82 | +0.08 | 0.865 |
| Control | Aggressive | Deaths | 5.72 ± 0.79 | 6.14 ± 0.80 | +0.10 | 0.865 |
| Control | Aggressive | WalkedHits | 0.04 ± 0.01 | 0.06 ± 0.01 | +0.61 | <0.001 |
| Control | Aggressive | HitsTaken | 0.03 ± 0.00 | 0.05 ± 0.00 | +0.63 | <0.001 |
| Control | Survival-Aware | CtrlScore | 13.61 ± 7.10 | 7.94 ± 5.10 | -0.32 | 0.349 |
| Control | Survival-Aware | ObjCommit | 0.04 ± 0.03 | 0.02 ± 0.02 | -0.29 | 0.443 |
| Control | Survival-Aware | AllyDist | 6.19 ± 0.87 | 6.71 ± 0.67 | +0.14 | 0.703 |
| Control | Survival-Aware | Kills | 2.97 ± 0.48 | 2.86 ± 0.45 | -0.05 | 1.000 |
| Control | Survival-Aware | Deaths | 2.57 ± 0.45 | 2.59 ± 0.40 | +0.01 | 1.000 |
| Control | Survival-Aware | WalkedHits | 0.02 ± 0.00 | 0.02 ± 0.00 | +0.32 | 0.041 |
| Control | Survival-Aware | HitsTaken | 0.02 ± 0.00 | 0.02 ± 0.00 | +0.27 | 0.129 |

Control wins (a -> b): Mission–Cooperation: 90 -> 94; Persistent Objective: 99 -> 96; Aggressive: 17 -> 48; Survival-Aware: 9 -> 4

### H3, WalkedHits per alive step: configured lambda_E vs 0 (change; Deathmatch p_Holm over 4 styles)

| Scenario | Style | a: change | a: p | b: change | b: p |
|---|---|---|---|---|---|
| Mission | Mission–Cooperation | -12% | 0.245 | -14% | 0.007 |
| Mission | Persistent Objective | -27% | 0.011 | -10% | 0.039 |
| Mission | Aggressive | -25% | 0.003 | -18% | <0.001 |
| Mission | Survival-Aware | -10% | 0.381 | -25% | <0.001 |
| Deathmatch | Mission–Cooperation | -14% | 0.029 | -9% | 0.003 |
| Deathmatch | Persistent Objective | -41% | <0.001 | -35% | <0.001 |
| Deathmatch | Aggressive | -19% | <0.001 | -15% | <0.001 |
| Deathmatch | Survival-Aware | -14% | 0.061 | -14% | 0.007 |
| Control | Mission–Cooperation | -19% | 0.020 | -11% | 0.009 |
| Control | Persistent Objective | -14% | 0.008 | -13% | 0.003 |
| Control | Aggressive | -22% | <0.001 | -5% | 0.149 |
| Control | Survival-Aware | -17% | 0.050 | -23% | <0.001 |

Sign test (lower with the exposure term): a 12/12 (p <0.001), b 12/12 (p <0.001)

### H3, HitsTaken per alive step: configured lambda_E vs 0 (change; Deathmatch p_Holm over 4 styles)

| Scenario | Style | a: change | a: p | b: change | b: p |
|---|---|---|---|---|---|
| Mission | Mission–Cooperation | -8% | 0.621 | -16% | 0.005 |
| Mission | Persistent Objective | -21% | 0.121 | -12% | 0.067 |
| Mission | Aggressive | -20% | 0.009 | -12% | 0.016 |
| Mission | Survival-Aware | +0% | 0.709 | -21% | 0.012 |
| Deathmatch | Mission–Cooperation | -12% | 0.137 | -6% | 0.175 |
| Deathmatch | Persistent Objective | -40% | <0.001 | -32% | <0.001 |
| Deathmatch | Aggressive | -18% | 0.002 | -11% | <0.001 |
| Deathmatch | Survival-Aware | -6% | 0.364 | -12% | 0.175 |
| Control | Mission–Cooperation | -24% | 0.008 | -10% | 0.069 |
| Control | Persistent Objective | -15% | 0.020 | -8% | 0.139 |
| Control | Aggressive | -23% | <0.001 | -2% | 0.747 |
| Control | Survival-Aware | -10% | 0.373 | -23% | <0.001 |

Sign test (lower with the exposure term): a 11/12 (p 0.003), b 12/12 (p <0.001)

### Movement stalls >= 50 steps (share of episodes, either team)

| Scenario | Style | a | b |
|---|---|---|---|
| Mission | Mission–Cooperation | 50% | 0% |
| Mission | Persistent Objective | 48% | 0% |
| Mission | Aggressive | 25% | 0% |
| Mission | Survival-Aware | 24% | 0% |
| Deathmatch | Mission–Cooperation | 35% | 0% |
| Deathmatch | Persistent Objective | 14% | 0% |
| Deathmatch | Aggressive | 16% | 0% |
| Deathmatch | Survival-Aware | 33% | 0% |
| Control | Mission–Cooperation | 24% | 0% |
| Control | Persistent Objective | 18% | 0% |
| Control | Aggressive | 30% | 0% |
| Control | Survival-Aware | 27% | 0% |

All conditions: a 28.7%, b 0.0%

