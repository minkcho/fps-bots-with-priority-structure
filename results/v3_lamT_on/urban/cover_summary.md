# Threat-relative cover: statistical summary (urban map)

Consistency checks (CRN): adjacency_full = main; distance_only = navigation ablation. **passed**

## Route-cost decomposition (paired Wilcoxon; r > 0: first variant higher)


### Deathmatch / Survival-Aware

| Variant | EngRedirect | ResSeek | AllyDist | ObjCommit | Kills | Deaths |
|---|---|---|---|---|---|---|
| distance_only | 0.67 ± 0.17 | 0.79 ± 0.15 | 4.23 ± 0.69 | 0.00 ± 0.00 | 7.50 ± 1.27 | 6.20 ± 1.07 |
| adjacency_cover_only | 2.35 ± 2.89 | 0.77 ± 0.16 | 3.58 ± 0.65 | 0.00 ± 0.00 | 7.53 ± 1.37 | 6.23 ± 0.96 |
| threat_cover_only | 0.97 ± 0.26 | 0.80 ± 0.13 | 5.00 ± 0.85 | 0.00 ± 0.00 | 8.60 ± 1.20 | 6.30 ± 1.04 |
| adjacency_full | 0.38 ± 0.11 | 0.45 ± 0.12 | 4.83 ± 0.91 | 0.00 ± 0.00 | 4.13 ± 1.00 | 3.33 ± 0.83 |
| threat_full | 0.51 ± 0.16 | 0.46 ± 0.11 | 4.46 ± 0.79 | 0.00 ± 0.00 | 4.00 ± 0.90 | 4.00 ± 0.99 |

- adjacency_cover_only vs distance_only: EngRedirect r=+0.52, p=0.011; Deaths r=-0.02, p=0.936; AllyDist r=-0.34, p=0.105
- threat_cover_only vs distance_only: EngRedirect r=+0.33, p=0.114; Deaths r=+0.02, p=0.909; AllyDist r=+0.40, p=0.058
- threat_cover_only vs adjacency_cover_only: EngRedirect r=-0.08, p=0.700; Deaths r=+0.06, p=0.778; AllyDist r=+0.51, p=0.014
- threat_full vs adjacency_full: EngRedirect r=+0.19, p=0.399; Deaths r=+0.23, p=0.292; AllyDist r=-0.07, p=0.761

### Deathmatch / Aggressive

| Variant | EngRedirect | ResSeek | AllyDist | ObjCommit | Kills | Deaths |
|---|---|---|---|---|---|---|
| distance_only | 1.24 ± 0.22 | 0.00 ± 0.00 | 4.24 ± 0.89 | 0.00 ± 0.00 | 10.13 ± 1.48 | 10.20 ± 1.55 |
| adjacency_cover_only | 1.28 ± 0.18 | 0.00 ± 0.00 | 4.00 ± 0.81 | 0.00 ± 0.00 | 10.13 ± 1.29 | 9.87 ± 1.34 |
| threat_cover_only | 1.42 ± 0.24 | 0.00 ± 0.00 | 4.31 ± 0.75 | 0.00 ± 0.00 | 10.10 ± 1.48 | 10.73 ± 1.69 |
| adjacency_full | 1.01 ± 0.15 | 0.00 ± 0.00 | 4.43 ± 0.82 | 0.00 ± 0.00 | 8.53 ± 1.46 | 8.37 ± 1.34 |
| threat_full | 1.03 ± 0.14 | 0.00 ± 0.00 | 4.55 ± 0.68 | 0.00 ± 0.00 | 9.17 ± 1.37 | 8.40 ± 1.11 |

- adjacency_cover_only vs distance_only: EngRedirect r=+0.06, p=0.792; Deaths r=-0.16, p=0.457; AllyDist r=-0.02, p=0.919
- threat_cover_only vs distance_only: EngRedirect r=+0.21, p=0.325; Deaths r=+0.06, p=0.779; AllyDist r=+0.03, p=0.887
- threat_cover_only vs adjacency_cover_only: EngRedirect r=+0.18, p=0.393; Deaths r=+0.19, p=0.379; AllyDist r=+0.13, p=0.543
- threat_full vs adjacency_full: EngRedirect r=+0.05, p=0.824; Deaths r=+0.02, p=0.927; AllyDist r=+0.11, p=0.598

### Mission / Mission–Cooperation

| Variant | EngRedirect | ResSeek | AllyDist | ObjCommit | Kills | Deaths |
|---|---|---|---|---|---|---|
| distance_only | 0.00 ± 0.00 | 0.00 ± 0.00 | 1.47 ± 0.30 | 0.97 ± 0.02 | 3.07 ± 1.70 | 2.77 ± 1.56 |
| adjacency_cover_only | 0.00 ± 0.01 | 0.00 ± 0.00 | 1.37 ± 0.22 | 0.97 ± 0.02 | 3.27 ± 1.93 | 2.60 ± 1.47 |
| threat_cover_only | 0.00 ± 0.01 | 0.00 ± 0.00 | 1.54 ± 0.28 | 0.97 ± 0.02 | 3.87 ± 2.11 | 3.20 ± 1.76 |
| adjacency_full | 0.01 ± 0.02 | 0.00 ± 0.00 | 1.56 ± 0.30 | 0.95 ± 0.03 | 3.17 ± 1.73 | 3.07 ± 1.77 |
| threat_full | 0.00 ± 0.01 | 0.00 ± 0.00 | 1.50 ± 0.25 | 0.97 ± 0.02 | 2.60 ± 1.47 | 2.17 ± 1.23 |

- adjacency_cover_only vs distance_only: EngRedirect r=+1.00, p=1.000; Deaths r=+0.05, p=0.951; AllyDist r=-0.09, p=0.696
- threat_cover_only vs distance_only: EngRedirect r=+1.00, p=1.000; Deaths r=+0.50, p=0.281; AllyDist r=-0.25, p=0.247
- threat_cover_only vs adjacency_cover_only: EngRedirect r=-0.33, p=1.000; Deaths r=+0.39, p=0.267; AllyDist r=+0.01, p=0.976
- threat_full vs adjacency_full: EngRedirect r=-0.67, p=0.500; Deaths r=-0.53, p=0.158; AllyDist r=-0.36, p=0.136

## Main experiment: threat cover vs adjacency cover (evaluated team; paired Wilcoxon)

| Scenario | Style | Metric | Adjacency | Threat | r | p |
|---|---|---|---|---|---|---|
| Mission | Mission–Cooperation | ObjCommit | 0.95 ± 0.03 | 0.97 ± 0.02 | +0.43 | 0.191 |
| Mission | Mission–Cooperation | AllyDist | 1.56 ± 0.30 | 1.50 ± 0.25 | -0.36 | 0.136 |
| Mission | Mission–Cooperation | Deaths | 3.07 ± 1.77 | 2.17 ± 1.23 | -0.53 | 0.158 |
| Mission | Persistent Objective | ObjCommit | 0.82 ± 0.12 | 0.86 ± 0.09 | +0.26 | 0.426 |
| Mission | Persistent Objective | AllyDist | 2.84 ± 1.43 | 2.91 ± 1.29 | -0.09 | 0.692 |
| Mission | Persistent Objective | Deaths | 1.77 ± 1.09 | 2.47 ± 1.33 | +0.28 | 0.360 |
| Mission | Aggressive | ObjCommit | 0.16 ± 0.11 | 0.22 ± 0.13 | +0.40 | 0.175 |
| Mission | Aggressive | AllyDist | 3.20 ± 0.80 | 3.94 ± 0.90 | +0.31 | 0.146 |
| Mission | Aggressive | Deaths | 4.80 ± 1.50 | 5.47 ± 1.34 | +0.11 | 0.619 |
| Mission | Survival-Aware | ObjCommit | 0.08 ± 0.08 | 0.02 ± 0.02 | -0.52 | 0.147 |
| Mission | Survival-Aware | AllyDist | 4.36 ± 0.87 | 4.39 ± 0.86 | +0.02 | 0.952 |
| Mission | Survival-Aware | Deaths | 2.70 ± 0.69 | 2.23 ± 0.60 | -0.26 | 0.238 |
| Deathmatch | Mission–Cooperation | EngRedirect | 0.20 ± 0.11 | 0.23 ± 0.08 | +0.18 | 0.420 |
| Deathmatch | Mission–Cooperation | ResSeek | 0.21 ± 0.36 | 0.32 ± 0.52 | +0.24 | 0.410 |
| Deathmatch | Mission–Cooperation | Deaths | 5.63 ± 1.50 | 6.30 ± 1.27 | +0.18 | 0.434 |
| Deathmatch | Persistent Objective | EngRedirect | 0.05 ± 0.03 | 0.06 ± 0.03 | +0.31 | 0.277 |
| Deathmatch | Persistent Objective | ResSeek | 0.00 ± 0.00 | 0.01 ± 0.01 | +1.00 | 0.500 |
| Deathmatch | Persistent Objective | Deaths | 4.00 ± 0.81 | 3.83 ± 0.64 | -0.01 | 0.977 |
| Deathmatch | Aggressive | EngRedirect | 1.01 ± 0.15 | 1.03 ± 0.14 | +0.05 | 0.824 |
| Deathmatch | Aggressive | ResSeek | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Deathmatch | Aggressive | Deaths | 8.37 ± 1.34 | 8.40 ± 1.11 | +0.02 | 0.927 |
| Deathmatch | Survival-Aware | EngRedirect | 0.38 ± 0.11 | 0.51 ± 0.16 | +0.19 | 0.399 |
| Deathmatch | Survival-Aware | ResSeek | 0.45 ± 0.12 | 0.46 ± 0.11 | +0.02 | 0.914 |
| Deathmatch | Survival-Aware | Deaths | 3.33 ± 0.83 | 4.00 ± 0.99 | +0.23 | 0.292 |
| Control | Mission–Cooperation | CtrlScore | 120.00 ± 0.00 | 113.13 ± 7.96 | -1.00 | 0.250 |
| Control | Mission–Cooperation | ObjCommit | 0.96 ± 0.02 | 0.93 ± 0.04 | -0.58 | 0.068 |
| Control | Mission–Cooperation | Deaths | 1.40 ± 1.08 | 1.53 ± 0.94 | +0.23 | 0.527 |
| Control | Persistent Objective | CtrlScore | 119.03 ± 1.98 | 120.00 ± 0.00 | +1.00 | 1.000 |
| Control | Persistent Objective | ObjCommit | 0.88 ± 0.08 | 0.89 ± 0.06 | -0.08 | 0.839 |
| Control | Persistent Objective | Deaths | 1.50 ± 0.78 | 1.57 ± 0.78 | +0.11 | 0.844 |
| Control | Aggressive | CtrlScore | 36.10 ± 20.33 | 35.20 ± 19.41 | -0.05 | 0.915 |
| Control | Aggressive | ObjCommit | 0.16 ± 0.09 | 0.14 ± 0.09 | -0.11 | 0.709 |
| Control | Aggressive | Deaths | 4.87 ± 1.35 | 5.30 ± 1.36 | +0.13 | 0.555 |
| Control | Survival-Aware | CtrlScore | 14.10 ± 13.55 | 18.93 ± 15.23 | +0.30 | 0.412 |
| Control | Survival-Aware | ObjCommit | 0.04 ± 0.05 | 0.06 ± 0.06 | +0.35 | 0.375 |
| Control | Survival-Aware | Deaths | 2.60 ± 0.81 | 3.10 ± 0.70 | +0.27 | 0.259 |

Control wins (adjacency -> threat): Mission–Cooperation: 30 -> 27; Persistent Objective: 29 -> 30; Aggressive: 8 -> 7; Survival-Aware: 2 -> 3

## Navigation-weight scale with threat cover (Spearman rho between k and metric)


### Mission / Mission–Cooperation

| scale | AllyDist | EngRedirect | ResSeek | Kills | Deaths |
|---|---|---|---|---|---|
| x0 | 1.47 ± 0.30 | 0.00 ± 0.00 | 0.00 ± 0.00 | 3.07 ± 1.70 | 2.77 ± 1.56 |
| x0.25 | 1.51 ± 0.27 | 0.00 ± 0.01 | 0.00 ± 0.00 | 3.80 ± 2.06 | 3.17 ± 1.76 |
| x0.5 | 1.46 ± 0.24 | 0.00 ± 0.00 | 0.00 ± 0.00 | 3.20 ± 1.84 | 2.37 ± 1.28 |
| x1 | 1.50 ± 0.25 | 0.00 ± 0.01 | 0.00 ± 0.00 | 2.60 ± 1.47 | 2.17 ± 1.23 |
| x2 | 1.54 ± 0.26 | 0.00 ± 0.01 | 0.00 ± 0.00 | 2.63 ± 1.48 | 2.17 ± 1.21 |
- Spearman rho(scale, AllyDist) = -0.07, p = 0.418
- Spearman rho(scale, EngRedirect) = +0.07, p = 0.421
- Spearman rho(scale, Deaths) = -0.03, p = 0.691
- Paired Wilcoxon x1 vs x0 (AllyDist): r = -0.20, p = 0.373
- Paired Wilcoxon x1 vs x0 (EngRedirect): r = +1.00, p = 1.000
- Paired Wilcoxon x1 vs x0 (Deaths): r = -0.33, p = 0.349

### Deathmatch / Survival-Aware

| scale | AllyDist | EngRedirect | ResSeek | Kills | Deaths |
|---|---|---|---|---|---|
| x0 | 4.23 ± 0.69 | 0.67 ± 0.17 | 0.79 ± 0.15 | 7.50 ± 1.27 | 6.20 ± 1.07 |
| x0.25 | 4.68 ± 0.86 | 1.48 ± 1.62 | 0.52 ± 0.14 | 5.13 ± 1.25 | 3.93 ± 1.01 |
| x0.5 | 4.22 ± 0.89 | 0.53 ± 0.13 | 0.50 ± 0.13 | 4.50 ± 1.06 | 3.90 ± 0.92 |
| x1 | 4.46 ± 0.79 | 0.51 ± 0.16 | 0.46 ± 0.11 | 4.00 ± 0.90 | 4.00 ± 0.99 |
| x2 | 4.46 ± 1.22 | 0.36 ± 0.14 | 0.34 ± 0.11 | 3.40 ± 1.03 | 3.00 ± 1.01 |
- Spearman rho(scale, AllyDist) = -0.06, p = 0.469
- Spearman rho(scale, EngRedirect) = -0.27, p = <0.001
- Spearman rho(scale, Deaths) = -0.31, p = <0.001
- Paired Wilcoxon x1 vs x0 (AllyDist): r = +0.23, p = 0.289
- Paired Wilcoxon x1 vs x0 (EngRedirect): r = -0.33, p = 0.114
- Paired Wilcoxon x1 vs x0 (Deaths): r = -0.58, p = 0.006
