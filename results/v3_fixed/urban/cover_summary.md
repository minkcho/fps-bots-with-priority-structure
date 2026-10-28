# Threat-relative cover: statistical summary (urban map)

Consistency checks (CRN): adjacency_full = main; distance_only = navigation ablation. **passed**

## Route-cost decomposition (paired Wilcoxon; r > 0: first variant higher)


### Deathmatch / Survival-Aware

| Variant | EngRedirect | ResSeek | AllyDist | ObjCommit | Kills | Deaths |
|---|---|---|---|---|---|---|
| distance_only | 0.00 ± 0.00 | 0.66 ± 0.07 | 6.67 ± 0.69 | 0.00 ± 0.00 | 5.46 ± 0.52 | 5.40 ± 0.52 |
| adjacency_cover_only | 0.00 ± 0.00 | 0.66 ± 0.07 | 7.23 ± 0.65 | 0.00 ± 0.00 | 5.79 ± 0.51 | 5.43 ± 0.54 |
| threat_cover_only | 0.00 ± 0.00 | 0.72 ± 0.07 | 6.74 ± 0.62 | 0.00 ± 0.00 | 5.95 ± 0.49 | 5.69 ± 0.53 |
| adjacency_full | 0.00 ± 0.00 | 0.61 ± 0.06 | 7.42 ± 0.57 | 0.00 ± 0.00 | 4.70 ± 0.46 | 4.72 ± 0.50 |
| threat_full | 0.00 ± 0.00 | 0.64 ± 0.06 | 7.58 ± 0.52 | 0.00 ± 0.00 | 5.46 ± 0.45 | 4.98 ± 0.47 |

- adjacency_cover_only vs distance_only: EngRedirect r=+0.00, p=1.000; Deaths r=+0.01, p=0.912; AllyDist r=+0.14, p=0.216
- threat_cover_only vs distance_only: EngRedirect r=+0.00, p=1.000; Deaths r=+0.11, p=0.341; AllyDist r=+0.04, p=0.726
- threat_cover_only vs adjacency_cover_only: EngRedirect r=+0.00, p=1.000; Deaths r=+0.09, p=0.454; AllyDist r=-0.15, p=0.186
- threat_full vs adjacency_full: EngRedirect r=+0.00, p=1.000; Deaths r=+0.09, p=0.467; AllyDist r=+0.07, p=0.536

### Deathmatch / Aggressive

| Variant | EngRedirect | ResSeek | AllyDist | ObjCommit | Kills | Deaths |
|---|---|---|---|---|---|---|
| distance_only | 3.02 ± 0.12 | 0.38 ± 0.05 | 4.34 ± 0.23 | 0.00 ± 0.00 | 12.58 ± 0.58 | 12.36 ± 0.52 |
| adjacency_cover_only | 3.24 ± 0.12 | 0.40 ± 0.04 | 4.60 ± 0.24 | 0.00 ± 0.00 | 13.61 ± 0.52 | 12.49 ± 0.52 |
| threat_cover_only | 3.17 ± 0.10 | 0.40 ± 0.05 | 4.77 ± 0.26 | 0.00 ± 0.00 | 12.99 ± 0.57 | 12.91 ± 0.54 |
| adjacency_full | 2.86 ± 0.13 | 0.35 ± 0.04 | 4.73 ± 0.20 | 0.00 ± 0.00 | 11.76 ± 0.50 | 11.41 ± 0.53 |
| threat_full | 2.73 ± 0.12 | 0.30 ± 0.04 | 4.81 ± 0.25 | 0.00 ± 0.00 | 11.31 ± 0.58 | 11.37 ± 0.62 |

- adjacency_cover_only vs distance_only: EngRedirect r=+0.33, p=0.004; Deaths r=-0.01, p=0.963; AllyDist r=+0.18, p=0.123
- threat_cover_only vs distance_only: EngRedirect r=+0.29, p=0.013; Deaths r=+0.19, p=0.121; AllyDist r=+0.35, p=0.002
- threat_cover_only vs adjacency_cover_only: EngRedirect r=-0.14, p=0.240; Deaths r=+0.18, p=0.146; AllyDist r=+0.17, p=0.152
- threat_full vs adjacency_full: EngRedirect r=-0.16, p=0.162; Deaths r=+0.05, p=0.710; AllyDist r=+0.10, p=0.409

### Mission / Mission–Cooperation

| Variant | EngRedirect | ResSeek | AllyDist | ObjCommit | Kills | Deaths |
|---|---|---|---|---|---|---|
| distance_only | 0.02 ± 0.01 | 0.00 ± 0.00 | 1.89 ± 0.22 | 0.94 ± 0.01 | 5.65 ± 1.07 | 4.80 ± 1.02 |
| adjacency_cover_only | 0.01 ± 0.01 | 0.00 ± 0.00 | 1.92 ± 0.23 | 0.95 ± 0.01 | 5.36 ± 1.01 | 4.93 ± 1.05 |
| threat_cover_only | 0.01 ± 0.01 | 0.00 ± 0.00 | 1.86 ± 0.21 | 0.95 ± 0.01 | 5.72 ± 1.05 | 4.84 ± 1.01 |
| adjacency_full | 0.02 ± 0.01 | 0.00 ± 0.00 | 1.77 ± 0.18 | 0.94 ± 0.01 | 5.03 ± 0.94 | 4.22 ± 0.89 |
| threat_full | 0.01 ± 0.01 | 0.00 ± 0.00 | 1.68 ± 0.18 | 0.95 ± 0.01 | 4.59 ± 0.89 | 4.10 ± 0.89 |

- adjacency_cover_only vs distance_only: EngRedirect r=-0.13, p=0.733; Deaths r=+0.03, p=0.859; AllyDist r=+0.13, p=0.324
- threat_cover_only vs distance_only: EngRedirect r=-0.39, p=0.383; Deaths r=+0.11, p=0.634; AllyDist r=-0.17, p=0.299
- threat_cover_only vs adjacency_cover_only: EngRedirect r=-0.05, p=0.915; Deaths r=-0.03, p=0.858; AllyDist r=-0.13, p=0.304
- threat_full vs adjacency_full: EngRedirect r=-0.17, p=0.570; Deaths r=-0.03, p=0.819; AllyDist r=-0.20, p=0.114

## Main experiment: threat cover vs adjacency cover (evaluated team; paired Wilcoxon)

| Scenario | Style | Metric | Adjacency | Threat | r | p |
|---|---|---|---|---|---|---|
| Mission | Mission–Cooperation | ObjCommit | 0.94 ± 0.01 | 0.95 ± 0.01 | +0.20 | 0.167 |
| Mission | Mission–Cooperation | AllyDist | 1.77 ± 0.18 | 1.68 ± 0.18 | -0.20 | 0.114 |
| Mission | Mission–Cooperation | Deaths | 4.22 ± 0.89 | 4.10 ± 0.89 | -0.03 | 0.819 |
| Mission | Persistent Objective | ObjCommit | 0.87 ± 0.04 | 0.88 ± 0.03 | +0.01 | 0.940 |
| Mission | Persistent Objective | AllyDist | 3.00 ± 0.41 | 2.85 ± 0.41 | -0.16 | 0.196 |
| Mission | Persistent Objective | Deaths | 5.19 ± 0.98 | 4.59 ± 0.85 | -0.20 | 0.156 |
| Mission | Aggressive | ObjCommit | 0.32 ± 0.06 | 0.31 ± 0.06 | -0.03 | 0.814 |
| Mission | Aggressive | AllyDist | 4.48 ± 0.41 | 4.38 ± 0.34 | -0.04 | 0.723 |
| Mission | Aggressive | Deaths | 7.29 ± 0.88 | 7.74 ± 0.77 | +0.20 | 0.124 |
| Mission | Survival-Aware | ObjCommit | 0.04 ± 0.03 | 0.02 ± 0.02 | -0.44 | 0.012 |
| Mission | Survival-Aware | AllyDist | 6.89 ± 0.71 | 7.29 ± 0.76 | +0.05 | 0.690 |
| Mission | Survival-Aware | Deaths | 2.89 ± 0.46 | 2.92 ± 0.41 | +0.06 | 0.650 |
| Deathmatch | Mission–Cooperation | EngRedirect | 0.46 ± 0.05 | 0.48 ± 0.06 | +0.04 | 0.740 |
| Deathmatch | Mission–Cooperation | ResSeek | 0.24 ± 0.05 | 0.27 ± 0.06 | +0.02 | 0.899 |
| Deathmatch | Mission–Cooperation | Deaths | 9.12 ± 0.62 | 9.32 ± 0.59 | +0.06 | 0.627 |
| Deathmatch | Persistent Objective | EngRedirect | 0.09 ± 0.02 | 0.11 ± 0.02 | +0.14 | 0.264 |
| Deathmatch | Persistent Objective | ResSeek | 0.02 ± 0.01 | 0.02 ± 0.01 | -0.03 | 0.856 |
| Deathmatch | Persistent Objective | Deaths | 5.69 ± 0.45 | 5.49 ± 0.43 | -0.09 | 0.469 |
| Deathmatch | Aggressive | EngRedirect | 2.86 ± 0.13 | 2.73 ± 0.12 | -0.16 | 0.162 |
| Deathmatch | Aggressive | ResSeek | 0.35 ± 0.04 | 0.30 ± 0.04 | -0.21 | 0.075 |
| Deathmatch | Aggressive | Deaths | 11.41 ± 0.53 | 11.37 ± 0.62 | +0.05 | 0.710 |
| Deathmatch | Survival-Aware | EngRedirect | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Deathmatch | Survival-Aware | ResSeek | 0.61 ± 0.06 | 0.64 ± 0.06 | +0.08 | 0.517 |
| Deathmatch | Survival-Aware | Deaths | 4.72 ± 0.50 | 4.98 ± 0.47 | +0.09 | 0.467 |
| Control | Mission–Cooperation | CtrlScore | 117.30 ± 2.64 | 115.80 ± 3.27 | -0.21 | 0.530 |
| Control | Mission–Cooperation | ObjCommit | 0.95 ± 0.01 | 0.94 ± 0.01 | -0.17 | 0.293 |
| Control | Mission–Cooperation | Deaths | 1.75 ± 0.53 | 1.92 ± 0.59 | +0.13 | 0.494 |
| Control | Persistent Objective | CtrlScore | 116.86 ± 3.49 | 116.48 ± 3.57 | -0.33 | 0.438 |
| Control | Persistent Objective | ObjCommit | 0.91 ± 0.03 | 0.91 ± 0.03 | +0.01 | 0.954 |
| Control | Persistent Objective | Deaths | 1.54 ± 0.46 | 1.42 ± 0.44 | -0.05 | 0.802 |
| Control | Aggressive | CtrlScore | 73.61 ± 10.43 | 69.13 ± 10.53 | -0.11 | 0.441 |
| Control | Aggressive | ObjCommit | 0.29 ± 0.05 | 0.27 ± 0.05 | -0.04 | 0.713 |
| Control | Aggressive | Deaths | 6.14 ± 0.80 | 5.77 ± 0.78 | -0.14 | 0.284 |
| Control | Survival-Aware | CtrlScore | 7.94 ± 5.10 | 12.39 ± 6.05 | +0.26 | 0.115 |
| Control | Survival-Aware | ObjCommit | 0.02 ± 0.02 | 0.02 ± 0.01 | +0.25 | 0.144 |
| Control | Survival-Aware | Deaths | 2.59 ± 0.40 | 3.16 ± 0.42 | +0.27 | 0.026 |

Control wins (adjacency -> threat): Mission–Cooperation: 94 -> 90; Persistent Objective: 96 -> 93; Aggressive: 48 -> 42; Survival-Aware: 4 -> 5

## Navigation-weight scale with threat cover (Spearman rho between k and metric)


### Mission / Mission–Cooperation

| scale | AllyDist | EngRedirect | ResSeek | Kills | Deaths |
|---|---|---|---|---|---|
| x0 | 1.89 ± 0.22 | 0.02 ± 0.01 | 0.00 ± 0.00 | 5.65 ± 1.07 | 4.80 ± 1.02 |
| x0.25 | 1.83 ± 0.21 | 0.01 ± 0.01 | 0.00 ± 0.00 | 5.33 ± 1.00 | 4.67 ± 1.03 |
| x0.5 | 1.69 ± 0.17 | 0.01 ± 0.01 | 0.00 ± 0.00 | 4.48 ± 0.87 | 4.01 ± 0.88 |
| x1 | 1.68 ± 0.18 | 0.01 ± 0.01 | 0.00 ± 0.00 | 4.59 ± 0.89 | 4.10 ± 0.89 |
| x2 | 1.63 ± 0.16 | 0.01 ± 0.01 | 0.00 ± 0.00 | 4.39 ± 0.84 | 3.91 ± 0.83 |
- Spearman rho(scale, AllyDist) = -0.05, p = 0.227
- Spearman rho(scale, EngRedirect) = -0.06, p = 0.198
- Spearman rho(scale, Deaths) = -0.05, p = 0.299
- Paired Wilcoxon x1 vs x0 (AllyDist): r = -0.35, p = 0.023
- Paired Wilcoxon x1 vs x0 (EngRedirect): r = -0.15, p = 0.662
- Paired Wilcoxon x1 vs x0 (Deaths): r = -0.43, p = 0.012

### Deathmatch / Survival-Aware

| scale | AllyDist | EngRedirect | ResSeek | Kills | Deaths |
|---|---|---|---|---|---|
| x0 | 6.67 ± 0.69 | 0.00 ± 0.00 | 0.66 ± 0.07 | 5.46 ± 0.52 | 5.40 ± 0.52 |
| x0.25 | 6.95 ± 0.61 | 0.00 ± 0.00 | 0.68 ± 0.06 | 5.38 ± 0.49 | 5.23 ± 0.51 |
| x0.5 | 7.43 ± 0.57 | 0.00 ± 0.00 | 0.67 ± 0.06 | 5.33 ± 0.46 | 5.07 ± 0.44 |
| x1 | 7.58 ± 0.52 | 0.00 ± 0.00 | 0.64 ± 0.06 | 5.46 ± 0.45 | 4.98 ± 0.47 |
| x2 | 7.39 ± 0.46 | 0.00 ± 0.00 | 0.67 ± 0.06 | 5.21 ± 0.44 | 5.24 ± 0.45 |
- Spearman rho(scale, AllyDist) = +0.15, p = <0.001
- Spearman rho(scale, Deaths) = -0.05, p = 0.291
- Paired Wilcoxon x1 vs x0 (AllyDist): r = +0.27, p = 0.018
- Paired Wilcoxon x1 vs x0 (EngRedirect): r = +0.00, p = 1.000
- Paired Wilcoxon x1 vs x0 (Deaths): r = -0.16, p = 0.190
