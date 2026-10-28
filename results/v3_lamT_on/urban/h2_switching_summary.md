# Redefined H2: commitment weight vs goal switching (urban directory)


## Control

| w_commit | goal switches / 100 steps | objective commitment | engagement redirection | deaths |
|---|---|---|---|---|
| 0 | 15.98 ± 2.47 | 0.83 | 0.28 | 1.77 |
| 0.2 | 1.49 ± 0.40 | 0.97 | 0.01 | 0.87 |
| 0.45 | 1.04 ± 0.23 | 0.96 | 0.00 | 1.40 |
| 0.65 | 1.10 ± 0.27 | 0.95 | 0.00 | 1.87 |
| 0.85 | 0.87 ± 0.12 | 0.96 | 0.00 | 1.00 |
| 1.05 | 0.78 ± 0.06 | 0.95 | 0.01 | 1.03 |
| 1.25 | 0.78 ± 0.06 | 0.95 | 0.01 | 1.03 |

Spearman rho(w_commit, goal switches) = -0.48, p = 1.09e-13 (n = 210)
Paired Wilcoxon, goal switches, w_commit 0.45 vs 0: median diff -13.68, r = -1.00, p = 1.73e-06
Paired Wilcoxon, goal switches, w_commit 1.25 vs 0: median diff -13.87, r = -1.00, p = 1.73e-06

## Mission

| w_commit | goal switches / 100 steps | objective commitment | engagement redirection | deaths |
|---|---|---|---|---|
| 0 | 8.07 ± 2.74 | 0.89 | 0.21 | 1.77 |
| 0.2 | 0.97 ± 0.47 | 0.97 | 0.02 | 2.37 |
| 0.45 | 0.75 ± 0.35 | 0.95 | 0.01 | 3.07 |
| 0.65 | 0.50 ± 0.21 | 0.96 | 0.01 | 2.87 |
| 0.85 | 0.39 ± 0.13 | 0.96 | 0.00 | 2.70 |
| 1.05 | 0.35 ± 0.09 | 0.96 | 0.00 | 2.63 |
| 1.25 | 0.35 ± 0.09 | 0.96 | 0.00 | 2.63 |

Spearman rho(w_commit, goal switches) = -0.50, p = 6.94e-15 (n = 210)
Paired Wilcoxon, goal switches, w_commit 0.45 vs 0: median diff -4.64, r = -1.00, p = 1.73e-06
Paired Wilcoxon, goal switches, w_commit 1.25 vs 0: median diff -4.64, r = -1.00, p = 1.73e-06

## Main experiment: goal switches per 100 steps by style

| Scenario | Mission–Cooperation | Persistent Objective | Aggressive | Survival-Aware |
|---|---|---|---|---|
| Mission | 0.75 | 0.28 | 0.97 | 6.33 |
| Deathmatch | 3.93 | 0.49 | 1.51 | 9.74 |
| Control | 1.04 | 0.86 | 1.28 | 6.68 |
