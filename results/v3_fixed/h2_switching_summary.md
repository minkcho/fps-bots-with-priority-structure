# Redefined H2: commitment weight vs goal switching (v3_fixed directory)


## Control

| w_commit | goal switches / 100 steps | objective commitment | engagement redirection | deaths |
|---|---|---|---|---|
| 0 | 26.08 ± 2.56 | 0.80 | 0.48 | 1.88 |
| 0.2 | 2.91 ± 0.26 | 0.94 | 0.01 | 1.64 |
| 0.45 | 1.16 ± 0.14 | 0.94 | 0.01 | 1.52 |
| 0.65 | 1.09 ± 0.12 | 0.94 | 0.00 | 1.49 |
| 0.85 | 0.95 ± 0.07 | 0.94 | 0.00 | 1.51 |
| 1.05 | 0.89 ± 0.05 | 0.94 | 0.00 | 1.53 |
| 1.25 | 0.89 ± 0.05 | 0.94 | 0.00 | 1.53 |

Spearman rho(w_commit, goal switches) = -0.67, p = 7.56e-94 (n = 700)
Paired Wilcoxon, goal switches, w_commit 0.45 vs 0: median diff -21.39, r = -1.00, p = 3.9e-18
Paired Wilcoxon, goal switches, w_commit 1.25 vs 0: median diff -22.09, r = -1.00, p = 3.9e-18

## Mission

| w_commit | goal switches / 100 steps | objective commitment | engagement redirection | deaths |
|---|---|---|---|---|
| 0 | 25.36 ± 4.26 | 0.80 | 0.51 | 3.85 |
| 0.2 | 3.23 ± 1.37 | 0.93 | 0.01 | 4.85 |
| 0.45 | 1.13 ± 0.20 | 0.94 | 0.01 | 5.06 |
| 0.65 | 0.77 ± 0.11 | 0.92 | 0.01 | 5.07 |
| 0.85 | 0.58 ± 0.07 | 0.93 | 0.01 | 5.01 |
| 1.05 | 0.51 ± 0.05 | 0.92 | 0.01 | 5.16 |
| 1.25 | 0.51 ± 0.05 | 0.92 | 0.01 | 5.16 |

Spearman rho(w_commit, goal switches) = -0.62, p = 8.79e-76 (n = 700)
Paired Wilcoxon, goal switches, w_commit 0.45 vs 0: median diff -20.39, r = -1.00, p = 3.89e-18
Paired Wilcoxon, goal switches, w_commit 1.25 vs 0: median diff -21.49, r = -1.00, p = 3.89e-18

## Main experiment: goal switches per 100 steps by style

| Scenario | Mission–Cooperation | Persistent Objective | Aggressive | Survival-Aware |
|---|---|---|---|---|
| Mission | 1.13 | 0.54 | 2.88 | 3.71 |
| Deathmatch | 6.38 | 0.79 | 5.10 | 4.96 |
| Control | 1.16 | 0.99 | 3.47 | 4.76 |
