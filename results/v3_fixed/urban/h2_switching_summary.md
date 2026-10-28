# Redefined H2: commitment weight vs goal switching (urban directory)


## Control

| w_commit | goal switches / 100 steps | objective commitment | engagement redirection | deaths |
|---|---|---|---|---|
| 0 | 29.47 ± 3.77 | 0.79 | 0.77 | 1.74 |
| 0.2 | 2.85 ± 0.78 | 0.94 | 0.04 | 1.75 |
| 0.45 | 1.26 ± 0.18 | 0.95 | 0.00 | 1.75 |
| 0.65 | 1.15 ± 0.15 | 0.94 | 0.01 | 1.83 |
| 0.85 | 1.03 ± 0.11 | 0.94 | 0.01 | 1.94 |
| 1.05 | 0.89 ± 0.06 | 0.94 | 0.01 | 2.10 |
| 1.25 | 0.89 ± 0.06 | 0.94 | 0.01 | 2.10 |

Spearman rho(w_commit, goal switches) = -0.47, p = 3.06e-40 (n = 700)
Paired Wilcoxon, goal switches, w_commit 0.45 vs 0: median diff -22.99, r = -1.00, p = 3.9e-18
Paired Wilcoxon, goal switches, w_commit 1.25 vs 0: median diff -23.77, r = -1.00, p = 3.9e-18

## Mission

| w_commit | goal switches / 100 steps | objective commitment | engagement redirection | deaths |
|---|---|---|---|---|
| 0 | 21.88 ± 4.10 | 0.81 | 0.64 | 3.16 |
| 0.2 | 4.01 ± 2.08 | 0.92 | 0.05 | 4.18 |
| 0.45 | 1.11 ± 0.22 | 0.94 | 0.02 | 4.22 |
| 0.65 | 0.99 ± 0.18 | 0.93 | 0.03 | 4.98 |
| 0.85 | 0.65 ± 0.11 | 0.93 | 0.02 | 4.79 |
| 1.05 | 0.52 ± 0.08 | 0.93 | 0.02 | 4.82 |
| 1.25 | 0.52 ± 0.08 | 0.93 | 0.02 | 4.82 |

Spearman rho(w_commit, goal switches) = -0.53, p = 2.61e-51 (n = 700)
Paired Wilcoxon, goal switches, w_commit 0.45 vs 0: median diff -14.82, r = -1.00, p = 3.9e-18
Paired Wilcoxon, goal switches, w_commit 1.25 vs 0: median diff -14.84, r = -1.00, p = 3.9e-18

## Main experiment: goal switches per 100 steps by style

| Scenario | Mission–Cooperation | Persistent Objective | Aggressive | Survival-Aware |
|---|---|---|---|---|
| Mission | 1.11 | 0.55 | 3.26 | 4.23 |
| Deathmatch | 6.63 | 0.82 | 5.52 | 6.04 |
| Control | 1.26 | 0.90 | 4.01 | 5.01 |
