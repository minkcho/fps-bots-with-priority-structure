# Redefined H2: commitment weight vs goal switching (v3 directory)


## Control

| w_commit | goal switches / 100 steps | objective commitment | engagement redirection | deaths |
|---|---|---|---|---|
| 0 | 15.98 ± 2.41 | 0.87 | 0.23 | 1.40 |
| 0.2 | 1.28 ± 0.45 | 0.97 | 0.00 | 1.17 |
| 0.45 | 0.98 ± 0.17 | 0.96 | 0.00 | 1.07 |
| 0.65 | 1.00 ± 0.22 | 0.95 | 0.00 | 1.30 |
| 0.85 | 0.78 ± 0.08 | 0.96 | 0.00 | 1.10 |
| 1.05 | 0.74 ± 0.08 | 0.96 | 0.00 | 1.13 |
| 1.25 | 0.74 ± 0.08 | 0.96 | 0.00 | 1.13 |

Spearman rho(w_commit, goal switches) = -0.50, p = 9.52e-15 (n = 210)
Paired Wilcoxon, goal switches, w_commit 0.45 vs 0: median diff -12.97, r = -1.00, p = 1.73e-06
Paired Wilcoxon, goal switches, w_commit 1.25 vs 0: median diff -12.97, r = -1.00, p = 1.73e-06

## Mission

| w_commit | goal switches / 100 steps | objective commitment | engagement redirection | deaths |
|---|---|---|---|---|
| 0 | 10.09 ± 3.63 | 0.87 | 0.73 | 2.13 |
| 0.2 | 2.43 ± 2.06 | 0.94 | 0.02 | 4.13 |
| 0.45 | 0.85 ± 0.29 | 0.95 | 0.00 | 4.20 |
| 0.65 | 0.82 ± 0.27 | 0.94 | 0.00 | 4.20 |
| 0.85 | 0.69 ± 0.22 | 0.93 | 0.00 | 4.80 |
| 1.05 | 0.45 ± 0.09 | 0.94 | 0.00 | 4.13 |
| 1.25 | 0.45 ± 0.09 | 0.94 | 0.00 | 4.13 |

Spearman rho(w_commit, goal switches) = -0.51, p = 2.89e-15 (n = 210)
Paired Wilcoxon, goal switches, w_commit 0.45 vs 0: median diff -4.97, r = -1.00, p = 1.73e-06
Paired Wilcoxon, goal switches, w_commit 1.25 vs 0: median diff -5.59, r = -1.00, p = 1.73e-06

## Main experiment: goal switches per 100 steps by style

| Scenario | Mission–Cooperation | Persistent Objective | Aggressive | Survival-Aware |
|---|---|---|---|---|
| Mission | 0.85 | 0.53 | 1.34 | 10.25 |
| Deathmatch | 2.69 | 0.54 | 1.97 | 13.37 |
| Control | 0.98 | 0.80 | 1.59 | 17.03 |
