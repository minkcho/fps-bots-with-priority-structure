# Cross-map confirmation (Level 2) over 2 maps: random, urban

| Hyp. | Test | p (Level 2) | p_Holm | Effect across maps | maps in predicted direction | SESOI | Verdict |
|---|---|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | 2.1e-61 | 4e-60 | eps2 median 0.74 (min 0.71) | 2/2 | yes | confirmed |
| H1 | Kruskal-Wallis, Mission AllyDist | 2.9e-31 | 4.6e-30 | eps2 median 0.40 (min 0.36) | 2/2 | yes | confirmed |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | 1.7e-73 | 3.5e-72 | eps2 median 0.86 (min 0.85) | 2/2 | yes | confirmed |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | 1.8e-46 | 3e-45 | eps2 median 0.56 (min 0.54) | 2/2 | yes | confirmed |
| H1 | Kruskal-Wallis, Control CtrlScore | 9.6e-48 | 1.7e-46 | eps2 median 0.57 (min 0.55) | 2/2 | yes | confirmed |
| H1 | Style classification, Mission | 0.0002 | 0.0022 | accuracy median 0.79 (min 0.78) | 2/2 | yes | confirmed |
| H1 | Style classification, Deathmatch | 0.0002 | 0.0022 | accuracy median 0.97 (min 0.97) | 2/2 | yes | confirmed |
| H1 | Style classification, Control | 0.0002 | 0.0022 | accuracy median 0.75 (min 0.72) | 2/2 | yes | confirmed |
| H1 | Mode ablation, Deathmatch Survival-Aware (full > weights-only) | 2.8e-17 | 3.4e-16 | r median +0.98 | 2/2 | yes | confirmed |
| H1 | Mode ablation, Deathmatch Aggressive (full > weights-only) | 6.7e-18 | 8.7e-17 | r median +0.99 | 2/2 | yes | confirmed |
| H2 | Mission goal switches, w_commit 0.45 < 0 | 1.9e-18 | 2.9e-17 | r median -1.00 | 2/2 | yes | confirmed |
| H2 | Control goal switches, w_commit 0.45 < 0 | 1.9e-18 | 2.9e-17 | r median -1.00 | 2/2 | yes | confirmed |
| H3 | Deathmatch Mission–Cooperation walked expected hits lower (lambda_E configured vs 0) | 0.096 | 0.29 | pooled r -0.51 [-2.50, +1.49], PI [-3.74, +2.73]; mean change -13% | 2/2 | yes | not confirmed |
| H3 | Deathmatch Persistent Objective walked expected hits lower (lambda_E configured vs 0) | 0.0081 | 0.033 | pooled r -0.96 [-1.28, -0.65], PI [-1.44, -0.49]; mean change -28% | 2/2 | yes | confirmed |
| H3 | Deathmatch Aggressive walked expected hits lower (lambda_E configured vs 0) | 0.0015 | 0.012 | pooled r -0.68 [-0.72, -0.64], PI [-0.73, -0.63]; mean change -14% | 2/2 | yes | confirmed |
| H3 | Deathmatch Survival-Aware walked expected hits lower (lambda_E configured vs 0) | 0.0033 | 0.02 | pooled r -0.21 [-0.24, -0.18], PI [-0.25, -0.17]; mean change -12% | 2/2 | yes | confirmed |
| H3 | Sign test: share of the 12 conditions with lower walked expected hits > 0.5 | 0 | 0 | mean share 1.00 (min 1.00) | 2/2 | yes | confirmed |
| H3 | Hits taken, Deathmatch, four styles pooled (lambda_E configured vs 0) | 0.0025 | 0.017 | pooled r -0.44 [-0.48, -0.40]; mean change -14% | 2/2 | yes | confirmed |
| H3b | Deathmatch Mission–Cooperation ally distance, lambda_T 10 < 0 | 0.13 | 0.29 | pooled r -0.43 [-2.68, +1.83]; mean difference -0.26 cells | 2/2 | yes | not confirmed |
| H4 | Deathmatch engagement redirection decreases along alpha (Aggressive -> Survival-Aware) | 0.0035 | 0.02 | pooled rho -0.67 [-0.72, -0.60] | 2/2 | yes | confirmed |
| H4 | Mission ally distance increases along alpha (Mission–Cooperation -> Persistent Objective) | 0.12 | 0.29 | pooled rho +0.14 [-0.50, +0.68]; mean change over alpha 0 -> 1 +0.93 cells | 2/2 | yes | not confirmed |

Per hypothesis: H1 confirmed; H2 confirmed; H3 partly confirmed; H3b not confirmed; H4 partly confirmed

## Level 1 (per map, Holm within map; descriptive)

| Test | random | urban |
|---|---|---|
| Kruskal-Wallis, Mission ObjCommit | eps2 = 0.71; 3.8e-60 | eps2 = 0.77; 4.5e-65 |
| Kruskal-Wallis, Mission AllyDist | eps2 = 0.36; 4.3e-30 | eps2 = 0.45; 1.2e-37 |
| Kruskal-Wallis, Deathmatch EngRedirect | eps2 = 0.85; 3.5e-72 | eps2 = 0.87; 2.4e-73 |
| Kruskal-Wallis, Deathmatch ResSeek | eps2 = 0.54; 2.9e-45 | eps2 = 0.58; 9.8e-49 |
| Kruskal-Wallis, Control CtrlScore | eps2 = 0.58; 7e-49 | eps2 = 0.55; 1.5e-46 |
| Style classification, Mission | 5-fold CV, 5000 permutations; 0.0012 | 5-fold CV, 5000 permutations; 0.0014 |
| Style classification, Deathmatch | 5-fold CV, 5000 permutations; 0.0012 | 5-fold CV, 5000 permutations; 0.0014 |
| Style classification, Control | 5-fold CV, 5000 permutations; 0.0012 | 5-fold CV, 5000 permutations; 0.0014 |
| Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | r = +0.98; 5.7e-16 | r = +0.98; 2.6e-16 |
| Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | r = +0.98; 1.6e-16 | r = +1.00; 5.5e-17 |
| Mission GoalSwitches, w_commit 0.45 - 0 | r = -1.00; 5.5e-17 | r = -1.00; 5.5e-17 |
| Control GoalSwitches, w_commit 0.45 - 0 | r = -1.00; 5.5e-17 | r = -1.00; 5.5e-17 |
| Deathmatch Mission–Cooperation WalkedHits, lambda_E configured - 0 | r = -0.66; 1.1e-07 | r = -0.34; 0.0093 |
| Deathmatch Persistent Objective WalkedHits, lambda_E configured - 0 | r = -0.98; 1.7e-16 | r = -0.93; 6.5e-15 |
| Deathmatch Aggressive WalkedHits, lambda_E configured - 0 | r = -0.68; 2.9e-08 | r = -0.68; 4.1e-08 |
| Deathmatch Survival-Aware WalkedHits, lambda_E configured - 0 | r = -0.21; 0.074 | r = -0.21; 0.11 |
| Sign test, WalkedHits lower with the exposure term (all scenarios x styles) | one-sided binomial; 0.0012 | one-sided binomial; 0.0014 |
| Deathmatch Mission–Cooperation AllyDist, lambda_T 10 - 0 | r = -0.24; 0.074 | r = -0.59; 1.9e-06 |
| Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | n = 500; 0.00012 | n = 500; 0.11 |
| Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | n = 500; 3.1e-65 | n = 500; 9.7e-63 |
