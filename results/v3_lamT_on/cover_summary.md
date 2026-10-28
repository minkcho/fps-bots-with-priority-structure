# Threat-relative cover: statistical summary (random map)

Consistency checks (CRN): adjacency_full = main; distance_only = navigation ablation. **passed**

## Route-cost decomposition (paired Wilcoxon; r > 0: first variant higher)


### Deathmatch / Survival-Aware

| Variant | EngRedirect | ResSeek | AllyDist | ObjCommit | Kills | Deaths |
|---|---|---|---|---|---|---|
| distance_only | 1.71 ± 0.60 | 0.85 ± 0.15 | 3.42 ± 0.63 | 0.00 ± 0.00 | 8.17 ± 1.34 | 6.97 ± 1.10 |
| adjacency_cover_only | 1.73 ± 1.45 | 0.75 ± 0.18 | 2.88 ± 0.48 | 0.00 ± 0.00 | 6.73 ± 1.39 | 5.93 ± 1.33 |
| threat_cover_only | 1.36 ± 0.37 | 0.80 ± 0.18 | 3.10 ± 0.44 | 0.00 ± 0.00 | 8.10 ± 1.43 | 6.10 ± 1.20 |
| adjacency_full | 0.69 ± 0.21 | 0.41 ± 0.10 | 3.43 ± 0.50 | 0.00 ± 0.00 | 4.23 ± 1.09 | 3.50 ± 0.77 |
| threat_full | 0.69 ± 0.21 | 0.49 ± 0.12 | 4.19 ± 0.81 | 0.00 ± 0.00 | 4.67 ± 1.15 | 3.73 ± 0.77 |

- adjacency_cover_only vs distance_only: EngRedirect r=-0.23, p=0.289; Deaths r=-0.29, p=0.194; AllyDist r=-0.34, p=0.109
- threat_cover_only vs distance_only: EngRedirect r=-0.14, p=0.516; Deaths r=-0.26, p=0.234; AllyDist r=-0.09, p=0.670
- threat_cover_only vs adjacency_cover_only: EngRedirect r=+0.19, p=0.382; Deaths r=+0.09, p=0.657; AllyDist r=+0.19, p=0.382
- threat_full vs adjacency_full: EngRedirect r=+0.04, p=0.848; Deaths r=+0.11, p=0.646; AllyDist r=+0.33, p=0.119

### Deathmatch / Aggressive

| Variant | EngRedirect | ResSeek | AllyDist | ObjCommit | Kills | Deaths |
|---|---|---|---|---|---|---|
| distance_only | 1.55 ± 0.16 | 0.00 ± 0.00 | 4.56 ± 0.55 | 0.00 ± 0.00 | 11.53 ± 0.98 | 11.47 ± 1.03 |
| adjacency_cover_only | 1.51 ± 0.22 | 0.00 ± 0.00 | 4.00 ± 0.59 | 0.00 ± 0.00 | 11.43 ± 1.27 | 11.13 ± 1.55 |
| threat_cover_only | 1.60 ± 0.22 | 0.00 ± 0.00 | 4.21 ± 0.64 | 0.00 ± 0.00 | 11.77 ± 1.23 | 11.70 ± 1.36 |
| adjacency_full | 1.33 ± 0.19 | 0.00 ± 0.00 | 4.15 ± 0.62 | 0.00 ± 0.00 | 10.10 ± 1.38 | 10.03 ± 1.38 |
| threat_full | 1.24 ± 0.23 | 0.00 ± 0.00 | 4.06 ± 0.61 | 0.00 ± 0.00 | 9.63 ± 1.60 | 9.17 ± 1.59 |

- adjacency_cover_only vs distance_only: EngRedirect r=-0.03, p=0.887; Deaths r=-0.07, p=0.744; AllyDist r=-0.31, p=0.146
- threat_cover_only vs distance_only: EngRedirect r=+0.08, p=0.730; Deaths r=+0.08, p=0.704; AllyDist r=-0.19, p=0.371
- threat_cover_only vs adjacency_cover_only: EngRedirect r=+0.14, p=0.529; Deaths r=+0.11, p=0.618; AllyDist r=+0.09, p=0.670
- threat_full vs adjacency_full: EngRedirect r=-0.16, p=0.468; Deaths r=-0.21, p=0.346; AllyDist r=-0.05, p=0.808

### Mission / Mission–Cooperation

| Variant | EngRedirect | ResSeek | AllyDist | ObjCommit | Kills | Deaths |
|---|---|---|---|---|---|---|
| distance_only | 0.00 ± 0.00 | 0.00 ± 0.00 | 2.04 ± 0.35 | 0.94 ± 0.02 | 6.80 ± 2.04 | 4.80 ± 1.49 |
| adjacency_cover_only | 0.00 ± 0.00 | 0.00 ± 0.00 | 2.04 ± 0.35 | 0.94 ± 0.02 | 6.80 ± 2.04 | 4.80 ± 1.49 |
| threat_cover_only | 0.00 ± 0.01 | 0.00 ± 0.00 | 1.86 ± 0.27 | 0.95 ± 0.02 | 6.53 ± 1.97 | 4.90 ± 1.57 |
| adjacency_full | 0.00 ± 0.00 | 0.00 ± 0.00 | 1.91 ± 0.32 | 0.95 ± 0.02 | 5.37 ± 1.64 | 4.20 ± 1.40 |
| threat_full | 0.01 ± 0.01 | 0.00 ± 0.00 | 2.10 ± 0.38 | 0.94 ± 0.02 | 5.77 ± 1.76 | 4.17 ± 1.32 |

- adjacency_cover_only vs distance_only: EngRedirect r=+0.00, p=1.000; Deaths r=+0.00, p=1.000; AllyDist r=+0.00, p=1.000
- threat_cover_only vs distance_only: EngRedirect r=+1.00, p=1.000; Deaths r=+0.13, p=0.659; AllyDist r=-0.30, p=0.243
- threat_cover_only vs adjacency_cover_only: EngRedirect r=+1.00, p=1.000; Deaths r=+0.13, p=0.659; AllyDist r=-0.30, p=0.243
- threat_full vs adjacency_full: EngRedirect r=+1.00, p=1.000; Deaths r=-0.03, p=0.959; AllyDist r=+0.26, p=0.320

## Main experiment: threat cover vs adjacency cover (evaluated team; paired Wilcoxon)

| Scenario | Style | Metric | Adjacency | Threat | r | p |
|---|---|---|---|---|---|---|
| Mission | Mission–Cooperation | ObjCommit | 0.95 ± 0.02 | 0.94 ± 0.02 | -0.29 | 0.277 |
| Mission | Mission–Cooperation | AllyDist | 1.91 ± 0.32 | 2.10 ± 0.38 | +0.26 | 0.320 |
| Mission | Mission–Cooperation | Deaths | 4.20 ± 1.40 | 4.17 ± 1.32 | -0.03 | 0.959 |
| Mission | Persistent Objective | ObjCommit | 0.90 ± 0.04 | 0.92 ± 0.04 | +0.49 | 0.050 |
| Mission | Persistent Objective | AllyDist | 2.50 ± 0.51 | 2.18 ± 0.40 | -0.39 | 0.113 |
| Mission | Persistent Objective | Deaths | 4.87 ± 1.58 | 3.93 ± 1.30 | -0.55 | 0.059 |
| Mission | Aggressive | ObjCommit | 0.20 ± 0.11 | 0.28 ± 0.13 | +0.33 | 0.191 |
| Mission | Aggressive | AllyDist | 3.84 ± 0.78 | 3.75 ± 0.76 | -0.12 | 0.598 |
| Mission | Aggressive | Deaths | 6.83 ± 1.49 | 6.67 ± 1.55 | +0.00 | 1.000 |
| Mission | Survival-Aware | ObjCommit | 0.02 ± 0.02 | 0.06 ± 0.07 | +0.22 | 0.489 |
| Mission | Survival-Aware | AllyDist | 4.52 ± 1.01 | 3.91 ± 0.89 | -0.29 | 0.177 |
| Mission | Survival-Aware | Deaths | 3.27 ± 0.73 | 3.47 ± 0.94 | +0.11 | 0.624 |
| Deathmatch | Mission–Cooperation | EngRedirect | 0.19 ± 0.10 | 0.22 ± 0.08 | +0.27 | 0.273 |
| Deathmatch | Mission–Cooperation | ResSeek | 0.06 ± 0.03 | 0.07 ± 0.04 | +0.22 | 0.438 |
| Deathmatch | Mission–Cooperation | Deaths | 4.53 ± 1.10 | 5.17 ± 1.36 | +0.19 | 0.414 |
| Deathmatch | Persistent Objective | EngRedirect | 0.06 ± 0.04 | 0.05 ± 0.03 | -0.12 | 0.660 |
| Deathmatch | Persistent Objective | ResSeek | 0.00 ± 0.01 | 0.00 ± 0.00 | -1.00 | 1.000 |
| Deathmatch | Persistent Objective | Deaths | 4.77 ± 0.81 | 4.67 ± 1.08 | -0.08 | 0.714 |
| Deathmatch | Aggressive | EngRedirect | 1.33 ± 0.19 | 1.24 ± 0.23 | -0.16 | 0.468 |
| Deathmatch | Aggressive | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Deathmatch | Aggressive | Deaths | 10.03 ± 1.38 | 9.17 ± 1.59 | -0.21 | 0.346 |
| Deathmatch | Survival-Aware | EngRedirect | 0.69 ± 0.21 | 0.69 ± 0.21 | +0.04 | 0.848 |
| Deathmatch | Survival-Aware | ResSeek | 0.41 ± 0.10 | 0.49 ± 0.12 | +0.25 | 0.259 |
| Deathmatch | Survival-Aware | Deaths | 3.50 ± 0.77 | 3.73 ± 0.77 | +0.11 | 0.646 |
| Control | Mission–Cooperation | CtrlScore | 114.23 ± 8.83 | 116.00 ± 8.18 | +1.00 | 1.000 |
| Control | Mission–Cooperation | ObjCommit | 0.96 ± 0.01 | 0.96 ± 0.01 | +0.24 | 0.570 |
| Control | Mission–Cooperation | Deaths | 1.07 ± 0.47 | 1.13 ± 0.54 | +0.33 | 0.750 |
| Control | Persistent Objective | CtrlScore | 118.23 ± 3.61 | 120.00 ± 0.00 | +1.00 | 1.000 |
| Control | Persistent Objective | ObjCommit | 0.90 ± 0.07 | 0.92 ± 0.05 | +0.33 | 0.426 |
| Control | Persistent Objective | Deaths | 1.53 ± 0.66 | 1.53 ± 0.65 | +0.00 | 1.000 |
| Control | Aggressive | CtrlScore | 39.70 ± 20.16 | 45.40 ± 21.21 | +0.18 | 0.633 |
| Control | Aggressive | ObjCommit | 0.17 ± 0.09 | 0.17 ± 0.09 | -0.06 | 0.860 |
| Control | Aggressive | Deaths | 6.43 ± 1.60 | 5.67 ± 1.45 | -0.26 | 0.266 |
| Control | Survival-Aware | CtrlScore | 16.43 ± 14.74 | 28.90 ± 17.17 | +0.45 | 0.093 |
| Control | Survival-Aware | ObjCommit | 0.03 ± 0.03 | 0.05 ± 0.03 | +0.40 | 0.188 |
| Control | Survival-Aware | Deaths | 2.27 ± 0.85 | 2.67 ± 0.61 | +0.20 | 0.421 |

Control wins (adjacency -> threat): Mission–Cooperation: 28 -> 29; Persistent Objective: 29 -> 30; Aggressive: 8 -> 9; Survival-Aware: 3 -> 5

## Navigation-weight scale with threat cover (Spearman rho between k and metric)


### Mission / Mission–Cooperation

| scale | AllyDist | EngRedirect | ResSeek | Kills | Deaths |
|---|---|---|---|---|---|
| x0 | 2.04 ± 0.35 | 0.00 ± 0.00 | 0.00 ± 0.00 | 6.80 ± 2.04 | 4.80 ± 1.49 |
| x0.25 | 2.09 ± 0.46 | 0.01 ± 0.01 | 0.00 ± 0.00 | 5.63 ± 1.76 | 4.73 ± 1.51 |
| x0.5 | 2.00 ± 0.37 | 0.01 ± 0.01 | 0.00 ± 0.00 | 6.63 ± 1.84 | 4.90 ± 1.41 |
| x1 | 2.10 ± 0.38 | 0.01 ± 0.01 | 0.00 ± 0.00 | 5.77 ± 1.76 | 4.17 ± 1.32 |
| x2 | 1.94 ± 0.28 | 0.01 ± 0.02 | 0.00 ± 0.00 | 5.63 ± 1.67 | 4.23 ± 1.40 |
- Spearman rho(scale, AllyDist) = -0.01, p = 0.931
- Spearman rho(scale, EngRedirect) = +0.07, p = 0.391
- Spearman rho(scale, Deaths) = -0.07, p = 0.425
- Paired Wilcoxon x1 vs x0 (AllyDist): r = +0.06, p = 0.824
- Paired Wilcoxon x1 vs x0 (EngRedirect): r = +1.00, p = 1.000
- Paired Wilcoxon x1 vs x0 (Deaths): r = -0.33, p = 0.233

### Deathmatch / Survival-Aware

| scale | AllyDist | EngRedirect | ResSeek | Kills | Deaths |
|---|---|---|---|---|---|
| x0 | 3.42 ± 0.63 | 1.71 ± 0.60 | 0.85 ± 0.15 | 8.17 ± 1.34 | 6.97 ± 1.10 |
| x0.25 | 3.42 ± 0.57 | 1.86 ± 1.29 | 0.68 ± 0.14 | 6.40 ± 1.21 | 5.57 ± 1.07 |
| x0.5 | 4.15 ± 1.00 | 0.76 ± 0.21 | 0.46 ± 0.12 | 4.77 ± 1.18 | 3.43 ± 0.93 |
| x1 | 4.19 ± 0.81 | 0.69 ± 0.21 | 0.49 ± 0.12 | 4.67 ± 1.15 | 3.73 ± 0.77 |
| x2 | 4.05 ± 0.65 | 0.85 ± 0.48 | 0.49 ± 0.12 | 4.93 ± 0.94 | 3.70 ± 0.90 |
- Spearman rho(scale, AllyDist) = +0.17, p = 0.035
- Spearman rho(scale, EngRedirect) = -0.32, p = <0.001
- Spearman rho(scale, Deaths) = -0.40, p = <0.001
- Paired Wilcoxon x1 vs x0 (AllyDist): r = +0.36, p = 0.084
- Paired Wilcoxon x1 vs x0 (EngRedirect): r = -0.65, p = 0.001
- Paired Wilcoxon x1 vs x0 (Deaths): r = -0.73, p = <0.001
