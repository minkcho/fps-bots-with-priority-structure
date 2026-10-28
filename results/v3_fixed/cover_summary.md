# Threat-relative cover: statistical summary (random map)

Consistency checks (CRN): adjacency_full = main; distance_only = navigation ablation. **passed**

## Route-cost decomposition (paired Wilcoxon; r > 0: first variant higher)


### Deathmatch / Survival-Aware

| Variant | EngRedirect | ResSeek | AllyDist | ObjCommit | Kills | Deaths |
|---|---|---|---|---|---|---|
| distance_only | 0.00 ± 0.00 | 0.60 ± 0.07 | 5.68 ± 0.56 | 0.00 ± 0.00 | 4.93 ± 0.43 | 4.93 ± 0.49 |
| adjacency_cover_only | 0.00 ± 0.00 | 0.60 ± 0.06 | 5.82 ± 0.63 | 0.00 ± 0.00 | 4.99 ± 0.47 | 5.02 ± 0.52 |
| threat_cover_only | 0.00 ± 0.00 | 0.57 ± 0.08 | 6.18 ± 0.72 | 0.00 ± 0.00 | 4.69 ± 0.47 | 4.60 ± 0.61 |
| adjacency_full | 0.00 ± 0.00 | 0.57 ± 0.06 | 7.20 ± 0.79 | 0.00 ± 0.00 | 4.86 ± 0.43 | 4.65 ± 0.50 |
| threat_full | 0.00 ± 0.00 | 0.55 ± 0.06 | 7.09 ± 0.66 | 0.00 ± 0.00 | 4.26 ± 0.44 | 4.50 ± 0.50 |

- adjacency_cover_only vs distance_only: EngRedirect r=+0.00, p=1.000; Deaths r=+0.07, p=0.533; AllyDist r=+0.01, p=0.904
- threat_cover_only vs distance_only: EngRedirect r=+0.00, p=1.000; Deaths r=-0.08, p=0.517; AllyDist r=+0.09, p=0.437
- threat_cover_only vs adjacency_cover_only: EngRedirect r=+0.00, p=1.000; Deaths r=-0.11, p=0.380; AllyDist r=+0.07, p=0.527
- threat_full vs adjacency_full: EngRedirect r=+0.00, p=1.000; Deaths r=-0.08, p=0.545; AllyDist r=+0.03, p=0.770

### Deathmatch / Aggressive

| Variant | EngRedirect | ResSeek | AllyDist | ObjCommit | Kills | Deaths |
|---|---|---|---|---|---|---|
| distance_only | 3.02 ± 0.13 | 0.35 ± 0.04 | 4.53 ± 0.23 | 0.00 ± 0.00 | 12.87 ± 0.51 | 12.28 ± 0.56 |
| adjacency_cover_only | 3.19 ± 0.12 | 0.37 ± 0.04 | 4.82 ± 0.26 | 0.00 ± 0.00 | 13.22 ± 0.55 | 13.04 ± 0.51 |
| threat_cover_only | 3.03 ± 0.12 | 0.36 ± 0.04 | 4.58 ± 0.21 | 0.00 ± 0.00 | 12.37 ± 0.54 | 12.81 ± 0.53 |
| adjacency_full | 2.84 ± 0.10 | 0.33 ± 0.04 | 5.11 ± 0.23 | 0.00 ± 0.00 | 11.86 ± 0.51 | 12.22 ± 0.49 |
| threat_full | 2.71 ± 0.13 | 0.32 ± 0.04 | 4.97 ± 0.25 | 0.00 ± 0.00 | 11.53 ± 0.58 | 11.63 ± 0.63 |

- adjacency_cover_only vs distance_only: EngRedirect r=+0.30, p=0.010; Deaths r=+0.30, p=0.014; AllyDist r=+0.28, p=0.015
- threat_cover_only vs distance_only: EngRedirect r=-0.01, p=0.900; Deaths r=+0.17, p=0.158; AllyDist r=+0.04, p=0.731
- threat_cover_only vs adjacency_cover_only: EngRedirect r=-0.29, p=0.013; Deaths r=-0.07, p=0.564; AllyDist r=-0.11, p=0.320
- threat_full vs adjacency_full: EngRedirect r=-0.13, p=0.265; Deaths r=-0.14, p=0.264; AllyDist r=-0.15, p=0.179

### Mission / Mission–Cooperation

| Variant | EngRedirect | ResSeek | AllyDist | ObjCommit | Kills | Deaths |
|---|---|---|---|---|---|---|
| distance_only | 0.01 ± 0.02 | 0.00 ± 0.00 | 2.09 ± 0.20 | 0.94 ± 0.01 | 6.55 ± 0.97 | 5.26 ± 0.85 |
| adjacency_cover_only | 0.01 ± 0.01 | 0.00 ± 0.00 | 2.09 ± 0.21 | 0.94 ± 0.01 | 6.55 ± 0.97 | 5.30 ± 0.86 |
| threat_cover_only | 0.00 ± 0.00 | 0.00 ± 0.00 | 1.96 ± 0.18 | 0.95 ± 0.01 | 6.47 ± 0.97 | 5.03 ± 0.84 |
| adjacency_full | 0.01 ± 0.01 | 0.00 ± 0.00 | 2.08 ± 0.18 | 0.94 ± 0.01 | 6.25 ± 0.94 | 5.06 ± 0.82 |
| threat_full | 0.01 ± 0.01 | 0.00 ± 0.00 | 2.17 ± 0.24 | 0.93 ± 0.01 | 6.29 ± 0.94 | 4.80 ± 0.80 |

- adjacency_cover_only vs distance_only: EngRedirect r=-1.00, p=0.500; Deaths r=+0.16, p=0.711; AllyDist r=-0.11, p=0.634
- threat_cover_only vs distance_only: EngRedirect r=-0.67, p=0.188; Deaths r=-0.17, p=0.291; AllyDist r=-0.33, p=0.018
- threat_cover_only vs adjacency_cover_only: EngRedirect r=-0.67, p=0.250; Deaths r=-0.24, p=0.151; AllyDist r=-0.34, p=0.013
- threat_full vs adjacency_full: EngRedirect r=+0.20, p=0.625; Deaths r=-0.31, p=0.067; AllyDist r=+0.02, p=0.864

## Main experiment: threat cover vs adjacency cover (evaluated team; paired Wilcoxon)

| Scenario | Style | Metric | Adjacency | Threat | r | p |
|---|---|---|---|---|---|---|
| Mission | Mission–Cooperation | ObjCommit | 0.94 ± 0.01 | 0.93 ± 0.01 | -0.17 | 0.271 |
| Mission | Mission–Cooperation | AllyDist | 2.08 ± 0.18 | 2.17 ± 0.24 | +0.02 | 0.864 |
| Mission | Mission–Cooperation | Deaths | 5.06 ± 0.82 | 4.80 ± 0.80 | -0.31 | 0.067 |
| Mission | Persistent Objective | ObjCommit | 0.91 ± 0.02 | 0.91 ± 0.02 | -0.17 | 0.267 |
| Mission | Persistent Objective | AllyDist | 2.82 ± 0.38 | 2.88 ± 0.35 | +0.11 | 0.403 |
| Mission | Persistent Objective | Deaths | 5.16 ± 0.83 | 5.34 ± 0.83 | +0.19 | 0.282 |
| Mission | Aggressive | ObjCommit | 0.37 ± 0.06 | 0.40 ± 0.06 | +0.13 | 0.297 |
| Mission | Aggressive | AllyDist | 4.42 ± 0.36 | 4.38 ± 0.37 | +0.01 | 0.924 |
| Mission | Aggressive | Deaths | 6.24 ± 0.84 | 6.76 ± 0.80 | +0.15 | 0.224 |
| Mission | Survival-Aware | ObjCommit | 0.05 ± 0.03 | 0.02 ± 0.01 | -0.30 | 0.050 |
| Mission | Survival-Aware | AllyDist | 6.80 ± 0.84 | 6.94 ± 0.86 | +0.03 | 0.762 |
| Mission | Survival-Aware | Deaths | 2.93 ± 0.45 | 2.64 ± 0.41 | -0.17 | 0.161 |
| Deathmatch | Mission–Cooperation | EngRedirect | 0.47 ± 0.06 | 0.47 ± 0.06 | +0.01 | 0.910 |
| Deathmatch | Mission–Cooperation | ResSeek | 0.25 ± 0.05 | 0.28 ± 0.06 | +0.04 | 0.720 |
| Deathmatch | Mission–Cooperation | Deaths | 9.27 ± 0.53 | 8.49 ± 0.60 | -0.29 | 0.020 |
| Deathmatch | Persistent Objective | EngRedirect | 0.08 ± 0.02 | 0.11 ± 0.02 | +0.20 | 0.116 |
| Deathmatch | Persistent Objective | ResSeek | 0.03 ± 0.01 | 0.03 ± 0.01 | +0.06 | 0.731 |
| Deathmatch | Persistent Objective | Deaths | 5.86 ± 0.42 | 6.60 ± 0.44 | +0.30 | 0.014 |
| Deathmatch | Aggressive | EngRedirect | 2.84 ± 0.10 | 2.71 ± 0.13 | -0.13 | 0.265 |
| Deathmatch | Aggressive | ResSeek | 0.33 ± 0.04 | 0.32 ± 0.04 | +0.03 | 0.815 |
| Deathmatch | Aggressive | Deaths | 12.22 ± 0.49 | 11.63 ± 0.63 | -0.14 | 0.264 |
| Deathmatch | Survival-Aware | EngRedirect | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Deathmatch | Survival-Aware | ResSeek | 0.57 ± 0.06 | 0.55 ± 0.06 | -0.07 | 0.532 |
| Deathmatch | Survival-Aware | Deaths | 4.65 ± 0.50 | 4.50 ± 0.50 | -0.08 | 0.545 |
| Control | Mission–Cooperation | CtrlScore | 117.58 ± 2.45 | 118.41 ± 1.59 | +0.33 | 0.625 |
| Control | Mission–Cooperation | ObjCommit | 0.94 ± 0.01 | 0.94 ± 0.01 | -0.12 | 0.615 |
| Control | Mission–Cooperation | Deaths | 1.52 ± 0.39 | 1.65 ± 0.42 | +0.46 | 0.127 |
| Control | Persistent Objective | CtrlScore | 114.95 ± 3.93 | 116.80 ± 3.44 | +0.44 | 0.312 |
| Control | Persistent Objective | ObjCommit | 0.90 ± 0.03 | 0.90 ± 0.03 | +0.16 | 0.499 |
| Control | Persistent Objective | Deaths | 1.94 ± 0.47 | 1.77 ± 0.44 | -0.43 | 0.130 |
| Control | Aggressive | CtrlScore | 70.06 ± 10.78 | 74.13 ± 10.85 | +0.11 | 0.507 |
| Control | Aggressive | ObjCommit | 0.32 ± 0.06 | 0.33 ± 0.06 | +0.06 | 0.664 |
| Control | Aggressive | Deaths | 4.93 ± 0.78 | 4.16 ± 0.63 | -0.26 | 0.052 |
| Control | Survival-Aware | CtrlScore | 13.59 ± 6.58 | 17.96 ± 7.29 | +0.18 | 0.279 |
| Control | Survival-Aware | ObjCommit | 0.03 ± 0.02 | 0.04 ± 0.02 | +0.23 | 0.196 |
| Control | Survival-Aware | Deaths | 2.21 ± 0.42 | 2.32 ± 0.37 | +0.14 | 0.320 |

Control wins (adjacency -> threat): Mission–Cooperation: 95 -> 95; Persistent Objective: 91 -> 94; Aggressive: 47 -> 53; Survival-Aware: 7 -> 9

## Navigation-weight scale with threat cover (Spearman rho between k and metric)


### Mission / Mission–Cooperation

| scale | AllyDist | EngRedirect | ResSeek | Kills | Deaths |
|---|---|---|---|---|---|
| x0 | 2.09 ± 0.20 | 0.01 ± 0.02 | 0.00 ± 0.00 | 6.55 ± 0.97 | 5.26 ± 0.85 |
| x0.25 | 1.96 ± 0.16 | 0.01 ± 0.01 | 0.00 ± 0.00 | 6.25 ± 0.94 | 5.04 ± 0.86 |
| x0.5 | 2.13 ± 0.22 | 0.01 ± 0.01 | 0.00 ± 0.00 | 6.41 ± 0.95 | 4.92 ± 0.83 |
| x1 | 2.17 ± 0.24 | 0.01 ± 0.01 | 0.00 ± 0.00 | 6.29 ± 0.94 | 4.80 ± 0.80 |
| x2 | 2.10 ± 0.19 | 0.01 ± 0.01 | 0.00 ± 0.00 | 6.44 ± 0.94 | 5.12 ± 0.81 |
- Spearman rho(scale, AllyDist) = -0.02, p = 0.626
- Spearman rho(scale, EngRedirect) = +0.01, p = 0.828
- Spearman rho(scale, Deaths) = -0.02, p = 0.709
- Paired Wilcoxon x1 vs x0 (AllyDist): r = +0.09, p = 0.525
- Paired Wilcoxon x1 vs x0 (EngRedirect): r = +0.16, p = 0.635
- Paired Wilcoxon x1 vs x0 (Deaths): r = -0.53, p = 0.001

### Deathmatch / Survival-Aware

| scale | AllyDist | EngRedirect | ResSeek | Kills | Deaths |
|---|---|---|---|---|---|
| x0 | 5.68 ± 0.56 | 0.00 ± 0.00 | 0.60 ± 0.07 | 4.93 ± 0.43 | 4.93 ± 0.49 |
| x0.25 | 6.40 ± 0.69 | 0.00 ± 0.00 | 0.54 ± 0.06 | 4.36 ± 0.44 | 4.54 ± 0.50 |
| x0.5 | 7.36 ± 0.74 | 0.00 ± 0.00 | 0.57 ± 0.06 | 4.83 ± 0.46 | 4.46 ± 0.50 |
| x1 | 7.09 ± 0.66 | 0.00 ± 0.00 | 0.55 ± 0.06 | 4.26 ± 0.44 | 4.50 ± 0.50 |
| x2 | 7.41 ± 0.71 | 0.00 ± 0.00 | 0.59 ± 0.07 | 4.65 ± 0.44 | 4.70 ± 0.52 |
- Spearman rho(scale, AllyDist) = +0.19, p = <0.001
- Spearman rho(scale, Deaths) = -0.02, p = 0.696
- Paired Wilcoxon x1 vs x0 (AllyDist): r = +0.35, p = 0.002
- Paired Wilcoxon x1 vs x0 (EngRedirect): r = +0.00, p = 1.000
- Paired Wilcoxon x1 vs x0 (Deaths): r = -0.18, p = 0.118
