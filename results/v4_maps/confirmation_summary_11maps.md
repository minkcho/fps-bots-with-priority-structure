# Cross-map confirmation (Level 2) over 11 maps: random, urban, random_s101, random_s102, random_s103, urban_s101, urban_s102, urban_s103, blocks, walls, mixed

| Hyp. | Test | p (Level 2) | p_Holm | Effect across maps | maps in predicted direction | SESOI | Verdict |
|---|---|---|---|---|---|---|---|
| H1 | Kruskal-Wallis, Mission ObjCommit | 1.4e-58 | 2.9e-57 | eps2 median 0.73 (min 0.68) | 11/11 | yes | confirmed |
| H1 | Kruskal-Wallis, Mission AllyDist | 5.6e-20 | 9.5e-19 | eps2 median 0.36 (min 0.23) | 11/11 | yes | confirmed |
| H1 | Kruskal-Wallis, Deathmatch EngRedirect | 7.8e-64 | 1.6e-62 | eps2 median 0.85 (min 0.74) | 11/11 | yes | confirmed |
| H1 | Kruskal-Wallis, Deathmatch ResSeek | 5.2e-45 | 9.8e-44 | eps2 median 0.54 (min 0.52) | 11/11 | yes | confirmed |
| H1 | Kruskal-Wallis, Control CtrlScore | 2.7e-44 | 4.9e-43 | eps2 median 0.58 (min 0.51) | 11/11 | yes | confirmed |
| H1 | Style classification, Mission | 0.0002 | 0.0006 | accuracy median 0.80 (min 0.73) | 11/11 | yes | confirmed |
| H1 | Style classification, Deathmatch | 0.0002 | 0.0006 | accuracy median 0.97 (min 0.95) | 11/11 | yes | confirmed |
| H1 | Style classification, Control | 0.0002 | 0.0006 | accuracy median 0.77 (min 0.71) | 11/11 | yes | confirmed |
| H1 | Mode ablation, Deathmatch Survival-Aware (full > weights-only) | 7.4e-17 | 9.6e-16 | r median +0.98 | 11/11 | yes | confirmed |
| H1 | Mode ablation, Deathmatch Aggressive (full > weights-only) | 5.2e-17 | 7.3e-16 | r median +0.99 | 11/11 | yes | confirmed |
| H2 | Mission goal switches, w_commit 0.45 < 0 | 4e-18 | 6e-17 | r median -1.00 | 11/11 | yes | confirmed |
| H2 | Control goal switches, w_commit 0.45 < 0 | 1.9e-18 | 3.1e-17 | r median -1.00 | 11/11 | yes | confirmed |
| H3 | Deathmatch Mission–Cooperation walked expected hits lower (lambda_E configured vs 0) | 1.3e-09 | 9e-09 | pooled r -0.54 [-0.60, -0.48], PI [-0.60, -0.48]; mean change -14% | 11/11 | yes | confirmed |
| H3 | Deathmatch Persistent Objective walked expected hits lower (lambda_E configured vs 0) | 1e-16 | 1.2e-15 | pooled r -0.95 [-0.97, -0.93], PI [-1.01, -0.90]; mean change -31% | 11/11 | yes | confirmed |
| H3 | Deathmatch Aggressive walked expected hits lower (lambda_E configured vs 0) | 2.8e-12 | 2.8e-11 | pooled r -0.71 [-0.76, -0.67], PI [-0.76, -0.67]; mean change -15% | 11/11 | yes | confirmed |
| H3 | Deathmatch Survival-Aware walked expected hits lower (lambda_E configured vs 0) | 8.9e-07 | 4.4e-06 | pooled r -0.45 [-0.55, -0.35], PI [-0.73, -0.17]; mean change -19% | 11/11 | yes | confirmed |
| H3 | Sign test: share of the 12 conditions with lower walked expected hits > 0.5 | 1e-11 | 8.8e-11 | mean share 0.98 (min 0.83) | 11/11 | yes | confirmed |
| H3 | Hits taken, Deathmatch, four styles pooled (lambda_E configured vs 0) | 9.7e-12 | 8.8e-11 | pooled r -0.53 [-0.56, -0.49]; mean change -17% | 11/11 | yes | confirmed |
| H3b | Deathmatch Mission–Cooperation ally distance, lambda_T 10 < 0 | 1.4e-06 | 5.5e-06 | pooled r -0.41 [-0.50, -0.31]; mean difference -0.20 cells | 11/11 | yes | confirmed |
| H4 | Deathmatch engagement redirection decreases along alpha (Aggressive -> Survival-Aware) | 2.3e-15 | 2.5e-14 | pooled rho -0.64 [-0.66, -0.63] | 11/11 | yes | confirmed |
| H4 | Mission ally distance increases along alpha (Mission–Cooperation -> Persistent Objective) | 6.2e-07 | 3.7e-06 | pooled rho +0.18 [+0.14, +0.22]; mean change over alpha 0 -> 1 +1.08 cells | 11/11 | yes | confirmed |

Per hypothesis: H1 confirmed; H2 confirmed; H3 confirmed; H3b confirmed; H4 confirmed

## Level 1 (per map, Holm within map; descriptive)

| Test | random | urban | random_s101 | random_s102 | random_s103 | urban_s101 | urban_s102 | urban_s103 | blocks | walls | mixed |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Kruskal-Wallis, Mission ObjCommit | eps2 = 0.71; 3.8e-60 | eps2 = 0.77; 4.5e-65 | eps2 = 0.72; 1.4e-60 | eps2 = 0.75; 3e-63 | eps2 = 0.73; 1.2e-61 | eps2 = 0.75; 4e-63 | eps2 = 0.72; 3.1e-61 | eps2 = 0.73; 7.1e-62 | eps2 = 0.75; 2.6e-63 | eps2 = 0.68; 2.7e-57 | eps2 = 0.72; 1.5e-60 |
| Kruskal-Wallis, Mission AllyDist | eps2 = 0.36; 4.3e-30 | eps2 = 0.45; 1.2e-37 | eps2 = 0.30; 9.2e-25 | eps2 = 0.41; 1.5e-34 | eps2 = 0.23; 8.4e-19 | eps2 = 0.30; 6.9e-25 | eps2 = 0.32; 1.6e-26 | eps2 = 0.43; 3.5e-36 | eps2 = 0.41; 2.2e-34 | eps2 = 0.44; 4.8e-37 | eps2 = 0.35; 2.2e-29 |
| Kruskal-Wallis, Deathmatch EngRedirect | eps2 = 0.85; 3.5e-72 | eps2 = 0.87; 2.4e-73 | eps2 = 0.85; 7.4e-72 | eps2 = 0.74; 1.4e-62 | eps2 = 0.83; 1.8e-70 | eps2 = 0.87; 1.5e-73 | eps2 = 0.83; 2.7e-70 | eps2 = 0.85; 3.9e-72 | eps2 = 0.86; 4.5e-73 | eps2 = 0.81; 3.1e-68 | eps2 = 0.84; 6.4e-71 |
| Kruskal-Wallis, Deathmatch ResSeek | eps2 = 0.54; 2.9e-45 | eps2 = 0.58; 9.8e-49 | eps2 = 0.53; 5.4e-45 | eps2 = 0.54; 1.8e-45 | eps2 = 0.58; 2.8e-49 | eps2 = 0.59; 3.3e-50 | eps2 = 0.52; 8.8e-44 | eps2 = 0.56; 2e-47 | eps2 = 0.53; 1.7e-44 | eps2 = 0.52; 3.6e-44 | eps2 = 0.62; 6.2e-52 |
| Kruskal-Wallis, Control CtrlScore | eps2 = 0.58; 7e-49 | eps2 = 0.55; 1.5e-46 | eps2 = 0.66; 9.8e-56 | eps2 = 0.68; 1.3e-57 | eps2 = 0.56; 1.7e-47 | eps2 = 0.62; 3.7e-52 | eps2 = 0.51; 4.4e-43 | eps2 = 0.59; 1.6e-49 | eps2 = 0.57; 1.2e-47 | eps2 = 0.56; 2.5e-47 | eps2 = 0.59; 2.1e-49 |
| Style classification, Mission | 5-fold CV, 5000 permutations; 0.0012 | 5-fold CV, 5000 permutations; 0.0014 | 5-fold CV, 5000 permutations; 0.0012 | 5-fold CV, 5000 permutations; 0.0012 | 5-fold CV, 5000 permutations; 0.0012 | 5-fold CV, 5000 permutations; 0.0012 | 5-fold CV, 5000 permutations; 0.001 | 5-fold CV, 5000 permutations; 0.0014 | 5-fold CV, 5000 permutations; 0.001 | 5-fold CV, 5000 permutations; 0.001 | 5-fold CV, 5000 permutations; 0.0008 |
| Style classification, Deathmatch | 5-fold CV, 5000 permutations; 0.0012 | 5-fold CV, 5000 permutations; 0.0014 | 5-fold CV, 5000 permutations; 0.0012 | 5-fold CV, 5000 permutations; 0.0012 | 5-fold CV, 5000 permutations; 0.0012 | 5-fold CV, 5000 permutations; 0.0012 | 5-fold CV, 5000 permutations; 0.001 | 5-fold CV, 5000 permutations; 0.0014 | 5-fold CV, 5000 permutations; 0.001 | 5-fold CV, 5000 permutations; 0.001 | 5-fold CV, 5000 permutations; 0.0008 |
| Style classification, Control | 5-fold CV, 5000 permutations; 0.0012 | 5-fold CV, 5000 permutations; 0.0014 | 5-fold CV, 5000 permutations; 0.0012 | 5-fold CV, 5000 permutations; 0.0012 | 5-fold CV, 5000 permutations; 0.0012 | 5-fold CV, 5000 permutations; 0.0012 | 5-fold CV, 5000 permutations; 0.001 | 5-fold CV, 5000 permutations; 0.0014 | 5-fold CV, 5000 permutations; 0.001 | 5-fold CV, 5000 permutations; 0.001 | 5-fold CV, 5000 permutations; 0.0008 |
| Mode ablation, Deathmatch Survival-Aware ResSeek (full - weights-only) | r = +0.98; 5.7e-16 | r = +0.98; 2.6e-16 | r = +0.97; 1.6e-15 | r = +0.98; 3.9e-16 | r = +0.99; 1.7e-16 | r = +0.99; 9.9e-17 | r = +0.99; 1.7e-16 | r = +0.99; 1.1e-16 | r = +0.98; 2.2e-16 | r = +0.98; 3.6e-16 | r = +1.00; 7.5e-17 |
| Mode ablation, Deathmatch Aggressive EngRedirect (full - weights-only) | r = +0.98; 1.6e-16 | r = +1.00; 5.5e-17 | r = +1.00; 5.5e-17 | r = +0.99; 1.3e-16 | r = +1.00; 6.1e-17 | r = +1.00; 6.8e-17 | r = +0.99; 9.3e-17 | r = +0.97; 3.6e-16 | r = +0.98; 1.8e-16 | r = +0.96; 1.1e-15 | r = +0.99; 8.1e-17 |
| Mission GoalSwitches, w_commit 0.45 - 0 | r = -1.00; 5.5e-17 | r = -1.00; 5.5e-17 | r = -1.00; 5.5e-17 | r = -1.00; 5.5e-17 | r = -1.00; 5.5e-17 | r = -1.00; 5.5e-17 | r = -1.00; 6.8e-17 | r = -0.99; 1e-16 | r = -1.00; 5.4e-17 | r = -1.00; 5.5e-17 | r = -1.00; 5.4e-17 |
| Control GoalSwitches, w_commit 0.45 - 0 | r = -1.00; 5.5e-17 | r = -1.00; 5.5e-17 | r = -1.00; 5.5e-17 | r = -1.00; 5.5e-17 | r = -1.00; 5.5e-17 | r = -1.00; 5.5e-17 | r = -1.00; 5.5e-17 | r = -1.00; 5.5e-17 | r = -1.00; 5.4e-17 | r = -1.00; 5.5e-17 | r = -1.00; 5.4e-17 |
| Deathmatch Mission–Cooperation WalkedHits, lambda_E configured - 0 | r = -0.66; 1.1e-07 | r = -0.34; 0.0093 | r = -0.57; 6.8e-06 | r = -0.51; 8e-05 | r = -0.65; 1.3e-07 | r = -0.49; 0.00014 | r = -0.57; 4.2e-06 | r = -0.41; 0.0014 | r = -0.55; 1.5e-05 | r = -0.56; 1.3e-05 | r = -0.47; 0.00023 |
| Deathmatch Persistent Objective WalkedHits, lambda_E configured - 0 | r = -0.98; 1.7e-16 | r = -0.93; 6.5e-15 | r = -0.92; 2.3e-14 | r = -0.97; 3.2e-16 | r = -0.94; 2.4e-15 | r = -0.90; 5.5e-14 | r = -0.98; 1.5e-16 | r = -0.92; 1.7e-14 | r = -0.94; 4.7e-15 | r = -0.93; 9.3e-15 | r = -0.91; 2.9e-14 |
| Deathmatch Aggressive WalkedHits, lambda_E configured - 0 | r = -0.68; 2.9e-08 | r = -0.68; 4.1e-08 | r = -0.64; 2e-07 | r = -0.67; 6.6e-08 | r = -0.76; 3e-10 | r = -0.55; 1.5e-05 | r = -0.72; 3.4e-09 | r = -0.75; 5.1e-10 | r = -0.71; 6.3e-09 | r = -0.80; 3.5e-11 | r = -0.72; 3.5e-09 |
| Deathmatch Survival-Aware WalkedHits, lambda_E configured - 0 | r = -0.21; 0.074 | r = -0.21; 0.11 | r = -0.38; 0.0018 | r = -0.29; 0.021 | r = -0.42; 0.0012 | r = -0.43; 0.0012 | r = -0.59; 2.3e-06 | r = -0.61; 7.9e-07 | r = -0.63; 4e-07 | r = -0.55; 1.5e-05 | r = -0.50; 0.0001 |
| Sign test, WalkedHits lower with the exposure term (all scenarios x styles) | one-sided binomial; 0.0012 | one-sided binomial; 0.0014 | one-sided binomial; 0.0012 | one-sided binomial; 0.0012 | one-sided binomial; 0.0012 | one-sided binomial; 0.019 | one-sided binomial; 0.001 | one-sided binomial; 0.0014 | one-sided binomial; 0.001 | one-sided binomial; 0.001 | one-sided binomial; 0.0008 |
| Deathmatch Mission–Cooperation AllyDist, lambda_T 10 - 0 | r = -0.24; 0.074 | r = -0.59; 1.9e-06 | r = -0.31; 0.0072 | r = -0.21; 0.068 | r = -0.33; 0.0043 | r = -0.61; 8.7e-07 | r = -0.39; 0.001 | r = -0.35; 0.0043 | r = -0.30; 0.01 | r = -0.45; 0.00063 | r = -0.55; 1.3e-05 |
| Mission AllyDist along alpha (Mission–Cooperation -> Persistent Objective) | n = 500; 0.00012 | n = 500; 0.11 | n = 500; 5.3e-05 | n = 500; 5.8e-07 | n = 500; 3.6e-08 | n = 500; 0.0012 | n = 500; 1.9e-06 | n = 500; 0.028 | n = 500; 6.2e-05 | n = 500; 0.0076 | n = 500; 0.00018 |
| Deathmatch EngRedirect along alpha (Aggressive -> Survival-Aware) | n = 500; 3.1e-65 | n = 500; 9.7e-63 | n = 500; 2.1e-58 | n = 500; 8.7e-63 | n = 500; 6.1e-55 | n = 500; 5.8e-61 | n = 500; 1.3e-56 | n = 500; 2.7e-53 | n = 500; 2.3e-49 | n = 500; 1.4e-56 | n = 500; 2.4e-59 |
