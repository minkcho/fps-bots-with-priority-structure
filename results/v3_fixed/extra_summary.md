# Cost-term ablation and external baselines (random map)

Consistency check (CRN): cost-term full = main. **passed**

## Leave-one-out cost-term ablation (paired Wilcoxon vs full; r > 0: variant higher; Holm per condition)


### Mission / Mission–Cooperation

| Variant | ObjCommit | AllyDist | EngRedirect | Deaths |
|---|---|---|---|---|
| full | 0.94 ± 0.01 | 2.08 ± 0.18 | 0.01 ± 0.01 | 5.06 ± 0.82 |
| no_exposure | 0.94 ± 0.01 | 2.09 ± 0.21 | 0.01 ± 0.01 | 5.30 ± 0.86 |
| no_cover | 0.93 ± 0.01 | 2.19 ± 0.22 | 0.01 ± 0.01 | 5.17 ± 0.85 |
| no_separation | 0.94 ± 0.01 | 2.08 ± 0.18 | 0.01 ± 0.01 | 5.06 ± 0.82 |

- nominally significant: no_exposure ObjCommit: r=+0.34, p=0.025, p_Holm=0.294; no_cover ObjCommit: r=-0.37, p=0.040, p_Holm=0.444

### Mission / Persistent Objective

| Variant | ObjCommit | AllyDist | EngRedirect | Deaths |
|---|---|---|---|---|
| full | 0.91 ± 0.02 | 2.82 ± 0.38 | 0.01 ± 0.01 | 5.16 ± 0.83 |
| no_exposure | 0.92 ± 0.02 | 2.49 ± 0.31 | 0.01 ± 0.01 | 5.60 ± 0.89 |
| no_cover | 0.91 ± 0.02 | 2.90 ± 0.35 | 0.01 ± 0.01 | 5.42 ± 0.84 |
| no_separation | 0.91 ± 0.02 | 2.82 ± 0.38 | 0.01 ± 0.01 | 5.16 ± 0.83 |

- nominally significant: no_exposure AllyDist: r=-0.46, p=0.001, p_Holm=0.013

### Mission / Aggressive

| Variant | ObjCommit | AllyDist | EngRedirect | Deaths |
|---|---|---|---|---|
| full | 0.37 ± 0.06 | 4.42 ± 0.36 | 1.45 ± 0.20 | 6.24 ± 0.84 |
| no_exposure | 0.44 ± 0.06 | 4.24 ± 0.34 | 1.61 ± 0.21 | 7.07 ± 0.87 |
| no_cover | 0.37 ± 0.06 | 4.36 ± 0.35 | 1.40 ± 0.19 | 6.46 ± 0.84 |
| no_separation | 0.37 ± 0.06 | 4.42 ± 0.36 | 1.45 ± 0.20 | 6.24 ± 0.84 |

- nominally significant: no_exposure ObjCommit: r=+0.25, p=0.041, p_Holm=0.413; no_exposure EngRedirect: r=+0.26, p=0.033, p_Holm=0.394; no_exposure Deaths: r=+0.27, p=0.034, p_Holm=0.394

### Mission / Survival-Aware

| Variant | ObjCommit | AllyDist | EngRedirect | Deaths |
|---|---|---|---|---|
| full | 0.05 ± 0.03 | 6.80 ± 0.84 | 0.00 ± 0.00 | 2.93 ± 0.45 |
| no_exposure | 0.03 ± 0.01 | 6.02 ± 0.73 | 0.00 ± 0.00 | 3.51 ± 0.48 |
| no_cover | 0.03 ± 0.02 | 6.90 ± 0.93 | 0.00 ± 0.00 | 2.78 ± 0.42 |
| no_separation | 0.05 ± 0.03 | 6.80 ± 0.84 | 0.00 ± 0.00 | 2.93 ± 0.45 |

- nominally significant: no_exposure Deaths: r=+0.29, p=0.025, p_Holm=0.279; no_cover ObjCommit: r=-0.38, p=0.016, p_Holm=0.197

### Deathmatch / Mission–Cooperation

| Variant | EngRedirect | ResSeek | AllyDist | Deaths |
|---|---|---|---|---|
| full | 0.47 ± 0.06 | 0.25 ± 0.05 | 2.86 ± 0.11 | 9.27 ± 0.53 |
| no_exposure | 0.38 ± 0.06 | 0.23 ± 0.05 | 2.61 ± 0.09 | 9.48 ± 0.60 |
| no_cover | 0.44 ± 0.06 | 0.28 ± 0.05 | 2.78 ± 0.10 | 8.86 ± 0.59 |
| no_separation | 0.47 ± 0.06 | 0.25 ± 0.05 | 2.86 ± 0.11 | 9.27 ± 0.53 |

- nominally significant: no_exposure EngRedirect: r=-0.29, p=0.014, p_Holm=0.150; no_exposure AllyDist: r=-0.45, p=<0.001, p_Holm=0.001

### Deathmatch / Persistent Objective

| Variant | EngRedirect | ResSeek | AllyDist | Deaths |
|---|---|---|---|---|
| full | 0.08 ± 0.02 | 0.03 ± 0.01 | 5.81 ± 0.29 | 5.86 ± 0.42 |
| no_exposure | 0.15 ± 0.03 | 0.04 ± 0.01 | 4.60 ± 0.26 | 8.24 ± 0.53 |
| no_cover | 0.09 ± 0.02 | 0.02 ± 0.01 | 5.65 ± 0.30 | 6.27 ± 0.47 |
| no_separation | 0.08 ± 0.02 | 0.03 ± 0.01 | 5.81 ± 0.29 | 5.86 ± 0.42 |

- nominally significant: no_exposure EngRedirect: r=+0.57, p=<0.001, p_Holm=<0.001; no_exposure ResSeek: r=+0.42, p=0.013, p_Holm=0.120; no_exposure AllyDist: r=-0.66, p=<0.001, p_Holm=<0.001; no_exposure Deaths: r=+0.76, p=<0.001, p_Holm=<0.001

### Deathmatch / Aggressive

| Variant | EngRedirect | ResSeek | AllyDist | Deaths |
|---|---|---|---|---|
| full | 2.84 ± 0.10 | 0.33 ± 0.04 | 5.11 ± 0.23 | 12.22 ± 0.49 |
| no_exposure | 3.19 ± 0.12 | 0.37 ± 0.04 | 4.82 ± 0.26 | 13.04 ± 0.51 |
| no_cover | 2.79 ± 0.11 | 0.33 ± 0.04 | 4.91 ± 0.25 | 11.80 ± 0.48 |
| no_separation | 2.84 ± 0.10 | 0.33 ± 0.04 | 5.11 ± 0.23 | 12.22 ± 0.49 |

- nominally significant: no_exposure EngRedirect: r=+0.64, p=<0.001, p_Holm=<0.001; no_exposure Deaths: r=+0.31, p=0.012, p_Holm=0.135

### Deathmatch / Survival-Aware

| Variant | EngRedirect | ResSeek | AllyDist | Deaths |
|---|---|---|---|---|
| full | 0.00 ± 0.00 | 0.57 ± 0.06 | 7.20 ± 0.79 | 4.65 ± 0.50 |
| no_exposure | 0.00 ± 0.00 | 0.60 ± 0.06 | 5.82 ± 0.63 | 5.02 ± 0.52 |
| no_cover | 0.00 ± 0.00 | 0.53 ± 0.06 | 6.49 ± 0.64 | 4.41 ± 0.46 |
| no_separation | 0.00 ± 0.00 | 0.57 ± 0.06 | 7.20 ± 0.79 | 4.65 ± 0.50 |

- nominally significant: no_exposure AllyDist: r=-0.33, p=0.005, p_Holm=0.057

### Control / Mission–Cooperation

| Variant | CtrlScore | ObjCommit | AllyDist | Deaths |
|---|---|---|---|---|
| full | 117.58 ± 2.45 | 0.94 ± 0.01 | 2.22 ± 0.21 | 1.52 ± 0.39 |
| no_exposure | 119.17 ± 1.65 | 0.95 ± 0.01 | 2.21 ± 0.20 | 1.68 ± 0.46 |
| no_cover | 118.01 ± 2.01 | 0.94 ± 0.01 | 2.21 ± 0.21 | 1.51 ± 0.38 |
| no_separation | 117.58 ± 2.45 | 0.94 ± 0.01 | 2.22 ± 0.21 | 1.52 ± 0.39 |

- nominally significant: none

### Control / Persistent Objective

| Variant | CtrlScore | ObjCommit | AllyDist | Deaths |
|---|---|---|---|---|
| full | 114.95 ± 3.93 | 0.90 ± 0.03 | 3.05 ± 0.41 | 1.94 ± 0.47 |
| no_exposure | 119.77 ± 0.46 | 0.91 ± 0.02 | 2.82 ± 0.37 | 1.70 ± 0.42 |
| no_cover | 114.67 ± 4.20 | 0.90 ± 0.03 | 2.99 ± 0.39 | 1.88 ± 0.46 |
| no_separation | 114.95 ± 3.93 | 0.90 ± 0.03 | 3.05 ± 0.41 | 1.94 ± 0.47 |

- nominally significant: no_exposure CtrlScore: r=+0.89, p=0.010, p_Holm=0.107; no_exposure ObjCommit: r=+0.41, p=0.027, p_Holm=0.274; no_exposure AllyDist: r=-0.51, p=0.005, p_Holm=0.062; no_exposure Deaths: r=-0.44, p=0.029, p_Holm=0.274

### Control / Aggressive

| Variant | CtrlScore | ObjCommit | AllyDist | Deaths |
|---|---|---|---|---|
| full | 70.06 ± 10.78 | 0.32 ± 0.06 | 4.35 ± 0.35 | 4.93 ± 0.78 |
| no_exposure | 80.83 ± 10.20 | 0.37 ± 0.06 | 4.39 ± 0.39 | 4.81 ± 0.74 |
| no_cover | 69.99 ± 11.10 | 0.31 ± 0.06 | 4.37 ± 0.35 | 4.34 ± 0.69 |
| no_separation | 70.06 ± 10.78 | 0.32 ± 0.06 | 4.35 ± 0.35 | 4.93 ± 0.78 |

- nominally significant: no_exposure ObjCommit: r=+0.26, p=0.037, p_Holm=0.443

### Control / Survival-Aware

| Variant | CtrlScore | ObjCommit | AllyDist | Deaths |
|---|---|---|---|---|
| full | 13.59 ± 6.58 | 0.03 ± 0.02 | 6.05 ± 0.63 | 2.21 ± 0.42 |
| no_exposure | 15.53 ± 7.21 | 0.04 ± 0.02 | 5.29 ± 0.52 | 2.95 ± 0.46 |
| no_cover | 6.05 ± 3.83 | 0.01 ± 0.01 | 6.44 ± 0.70 | 2.40 ± 0.43 |
| no_separation | 13.59 ± 6.58 | 0.03 ± 0.02 | 6.05 ± 0.63 | 2.21 ± 0.42 |

- nominally significant: no_exposure Deaths: r=+0.32, p=0.013, p_Holm=0.151

## External baselines (vs fixed Aggressive opponent)

| Scenario | Agent | ObjCommit | AllyDist | EngRedirect | ResSeek | Kills | Deaths | Control |
|---|---|---|---|---|---|---|---|---|
| Mission | CSO-BT | 0.81 ± 0.03 | 1.94 ± 0.16 | 2.55 ± 0.41 | 0.00 ± 0.00 | 6.6 ± 1.0 | 5.2 ± 0.8 |  |
| Mission | OW-BT | 0.94 ± 0.01 | 2.01 ± 0.18 | 0.00 ± 0.00 | 0.68 ± 0.12 | 6.9 ± 1.0 | 4.5 ± 0.8 |  |
| Mission | AC-BT | 0.00 ± 0.00 | 7.05 ± 0.28 | 0.16 ± 0.03 | 2.71 ± 0.09 | 15.0 ± 0.5 | 16.2 ± 0.5 |  |
| Mission | XO-BT | 0.00 ± 0.00 | 7.00 ± 0.26 | 0.12 ± 0.03 | 2.74 ± 0.09 | 15.2 ± 0.4 | 16.5 ± 0.5 |  |
| Mission | UtilityAI | 0.95 ± 0.01 | 2.28 ± 0.25 | 1.52 ± 0.25 | 0.00 ± 0.00 | 6.4 ± 0.9 | 5.6 ± 0.9 |  |
| Mission | Mission–Cooperation | 0.94 ± 0.01 | 2.08 ± 0.18 | 0.01 ± 0.01 | 0.00 ± 0.00 | 6.2 ± 0.9 | 5.1 ± 0.8 |  |
| Mission | Persistent Objective | 0.91 ± 0.02 | 2.82 ± 0.38 | 0.01 ± 0.01 | 0.00 ± 0.00 | 6.4 ± 0.9 | 5.2 ± 0.8 |  |
| Mission | Aggressive | 0.37 ± 0.06 | 4.42 ± 0.36 | 1.45 ± 0.20 | 0.14 ± 0.03 | 6.4 ± 0.8 | 6.2 ± 0.8 |  |
| Mission | Survival-Aware | 0.05 ± 0.03 | 6.80 ± 0.84 | 0.00 ± 0.00 | 0.35 ± 0.05 | 3.0 ± 0.4 | 2.9 ± 0.4 |  |
| Deathmatch | CSO-BT | 0.00 ± 0.00 | 3.49 ± 0.21 | 3.97 ± 0.25 | 0.00 ± 0.00 | 10.8 ± 0.6 | 11.4 ± 0.8 |  |
| Deathmatch | OW-BT | 0.00 ± 0.00 | 3.32 ± 0.25 | 4.72 ± 1.24 | 1.41 ± 0.17 | 9.9 ± 1.0 | 9.2 ± 1.1 |  |
| Deathmatch | AC-BT | 0.00 ± 0.00 | 7.11 ± 0.27 | 0.23 ± 0.04 | 2.82 ± 0.08 | 15.4 ± 0.5 | 16.6 ± 0.4 |  |
| Deathmatch | XO-BT | 0.00 ± 0.00 | 6.98 ± 0.27 | 0.18 ± 0.05 | 2.83 ± 0.07 | 15.4 ± 0.6 | 16.9 ± 0.4 |  |
| Deathmatch | UtilityAI | 0.00 ± 0.00 | 3.13 ± 0.11 | 2.47 ± 0.24 | 1.06 ± 0.13 | 11.3 ± 1.0 | 9.1 ± 0.9 |  |
| Deathmatch | Mission–Cooperation | 0.00 ± 0.00 | 2.86 ± 0.11 | 0.47 ± 0.06 | 0.25 ± 0.05 | 10.1 ± 0.5 | 9.3 ± 0.5 |  |
| Deathmatch | Persistent Objective | 0.00 ± 0.00 | 5.81 ± 0.29 | 0.08 ± 0.02 | 0.03 ± 0.01 | 9.0 ± 0.4 | 5.9 ± 0.4 |  |
| Deathmatch | Aggressive | 0.00 ± 0.00 | 5.11 ± 0.23 | 2.84 ± 0.10 | 0.33 ± 0.04 | 11.9 ± 0.5 | 12.2 ± 0.5 |  |
| Deathmatch | Survival-Aware | 0.00 ± 0.00 | 7.20 ± 0.79 | 0.00 ± 0.00 | 0.57 ± 0.06 | 4.9 ± 0.4 | 4.7 ± 0.5 |  |
| Control | CSO-BT | 0.77 ± 0.02 | 2.16 ± 0.20 | 2.75 ± 0.45 | 0.00 ± 0.00 | 2.9 ± 0.6 | 2.0 ± 0.5 | 119.73 ± 0.38; wins 97/100 |
| Control | OW-BT | 0.95 ± 0.01 | 1.97 ± 0.20 | 0.00 ± 0.00 | 0.53 ± 0.11 | 2.6 ± 0.5 | 1.4 ± 0.4 | 120.00 ± 0.00; wins 100/100 |
| Control | AC-BT | 0.00 ± 0.00 | 7.15 ± 0.25 | 0.19 ± 0.04 | 2.78 ± 0.08 | 15.7 ± 0.5 | 16.2 ± 0.4 | 0.41 ± 0.19; wins 0/100 |
| Control | XO-BT | 0.00 ± 0.00 | 6.81 ± 0.27 | 0.11 ± 0.03 | 2.63 ± 0.09 | 15.4 ± 0.5 | 15.8 ± 0.5 | 0.35 ± 0.17; wins 0/100 |
| Control | UtilityAI | 0.94 ± 0.01 | 2.50 ± 0.34 | 1.69 ± 0.30 | 0.00 ± 0.00 | 2.5 ± 0.4 | 1.9 ± 0.5 | 120.00 ± 0.00; wins 100/100 |
| Control | Mission–Cooperation | 0.94 ± 0.01 | 2.22 ± 0.21 | 0.01 ± 0.01 | 0.00 ± 0.00 | 2.3 ± 0.4 | 1.5 ± 0.4 | 117.58 ± 2.45; wins 95/100 |
| Control | Persistent Objective | 0.90 ± 0.03 | 3.05 ± 0.41 | 0.01 ± 0.01 | 0.00 ± 0.00 | 2.4 ± 0.4 | 1.9 ± 0.5 | 114.95 ± 3.93; wins 91/100 |
| Control | Aggressive | 0.32 ± 0.06 | 4.35 ± 0.35 | 1.74 ± 0.18 | 0.19 ± 0.04 | 5.0 ± 0.8 | 4.9 ± 0.8 | 70.06 ± 10.78; wins 47/100 |
| Control | Survival-Aware | 0.03 ± 0.02 | 6.05 ± 0.63 | 0.00 ± 0.00 | 0.42 ± 0.06 | 2.3 ± 0.4 | 2.2 ± 0.4 | 13.59 ± 6.58; wins 7/100 |

## Behaviour trees vs corresponding priority-structure styles (Mann-Whitney; r > 0: BT higher)

| Scenario | Pair | Metric | BT | Style | r | p |
|---|---|---|---|---|---|---|
| Mission | CSO-BT / Mission–Cooperation | ObjCommit | 0.81 ± 0.03 | 0.94 ± 0.01 | -0.55 | <0.001 |
| Mission | CSO-BT / Mission–Cooperation | AllyDist | 1.94 ± 0.16 | 2.08 ± 0.18 | -0.12 | 0.130 |
| Mission | CSO-BT / Mission–Cooperation | EngRedirect | 2.55 ± 0.41 | 0.01 ± 0.01 | +0.74 | <0.001 |
| Mission | CSO-BT / Mission–Cooperation | Deaths | 5.15 ± 0.83 | 5.06 ± 0.82 | +0.01 | 0.929 |
| Mission | OW-BT / Persistent Objective | ObjCommit | 0.94 ± 0.01 | 0.91 ± 0.02 | +0.19 | 0.018 |
| Mission | OW-BT / Persistent Objective | AllyDist | 2.01 ± 0.18 | 2.82 ± 0.38 | -0.34 | <0.001 |
| Mission | OW-BT / Persistent Objective | EngRedirect | 0.00 ± 0.00 | 0.01 ± 0.01 | -0.08 | 0.004 |
| Mission | OW-BT / Persistent Objective | Deaths | 4.55 ± 0.78 | 5.16 ± 0.83 | -0.08 | 0.295 |
| Mission | AC-BT / Aggressive | ObjCommit | 0.00 ± 0.00 | 0.37 ± 0.06 | -0.85 | <0.001 |
| Mission | AC-BT / Aggressive | AllyDist | 7.05 ± 0.28 | 4.42 ± 0.36 | +0.76 | <0.001 |
| Mission | AC-BT / Aggressive | EngRedirect | 0.16 ± 0.03 | 1.45 ± 0.20 | -0.77 | <0.001 |
| Mission | AC-BT / Aggressive | Deaths | 16.17 ± 0.45 | 6.24 ± 0.84 | +0.97 | <0.001 |
| Mission | XO-BT / Survival-Aware | ObjCommit | 0.00 ± 0.00 | 0.05 ± 0.03 | -0.38 | <0.001 |
| Mission | XO-BT / Survival-Aware | AllyDist | 7.00 ± 0.26 | 6.80 ± 0.84 | +0.24 | 0.004 |
| Mission | XO-BT / Survival-Aware | EngRedirect | 0.12 ± 0.03 | 0.00 ± 0.00 | +0.48 | <0.001 |
| Mission | XO-BT / Survival-Aware | Deaths | 16.51 ± 0.46 | 2.93 ± 0.45 | +1.00 | <0.001 |
| Deathmatch | CSO-BT / Mission–Cooperation | EngRedirect | 3.97 ± 0.25 | 0.47 ± 0.06 | +0.95 | <0.001 |
| Deathmatch | CSO-BT / Mission–Cooperation | ResSeek | 0.00 ± 0.00 | 0.25 ± 0.05 | -0.83 | <0.001 |
| Deathmatch | CSO-BT / Mission–Cooperation | AllyDist | 3.49 ± 0.21 | 2.86 ± 0.11 | +0.43 | <0.001 |
| Deathmatch | CSO-BT / Mission–Cooperation | Deaths | 11.44 ± 0.76 | 9.27 ± 0.53 | +0.43 | <0.001 |
| Deathmatch | OW-BT / Persistent Objective | EngRedirect | 4.72 ± 1.24 | 0.08 ± 0.02 | +0.83 | <0.001 |
| Deathmatch | OW-BT / Persistent Objective | ResSeek | 1.41 ± 0.17 | 0.03 ± 0.01 | +0.85 | <0.001 |
| Deathmatch | OW-BT / Persistent Objective | AllyDist | 3.32 ± 0.25 | 5.81 ± 0.29 | -0.80 | <0.001 |
| Deathmatch | OW-BT / Persistent Objective | Deaths | 9.22 ± 1.07 | 5.86 ± 0.42 | +0.45 | <0.001 |
| Deathmatch | AC-BT / Aggressive | EngRedirect | 0.23 ± 0.04 | 2.84 ± 0.10 | -1.00 | <0.001 |
| Deathmatch | AC-BT / Aggressive | ResSeek | 2.82 ± 0.08 | 0.33 ± 0.04 | +1.00 | <0.001 |
| Deathmatch | AC-BT / Aggressive | AllyDist | 7.11 ± 0.27 | 5.11 ± 0.23 | +0.73 | <0.001 |
| Deathmatch | AC-BT / Aggressive | Deaths | 16.60 ± 0.42 | 12.22 ± 0.49 | +0.81 | <0.001 |
| Deathmatch | XO-BT / Survival-Aware | EngRedirect | 0.18 ± 0.05 | 0.00 ± 0.00 | +0.58 | <0.001 |
| Deathmatch | XO-BT / Survival-Aware | ResSeek | 2.83 ± 0.07 | 0.57 ± 0.06 | +1.00 | <0.001 |
| Deathmatch | XO-BT / Survival-Aware | AllyDist | 6.98 ± 0.27 | 7.20 ± 0.79 | +0.02 | 0.844 |
| Deathmatch | XO-BT / Survival-Aware | Deaths | 16.87 ± 0.40 | 4.65 ± 0.50 | +1.00 | <0.001 |
| Control | CSO-BT / Mission–Cooperation | CtrlScore | 119.73 ± 0.38 | 117.58 ± 2.45 | +0.02 | 0.452 |
| Control | CSO-BT / Mission–Cooperation | ObjCommit | 0.77 ± 0.02 | 0.94 ± 0.01 | -0.80 | <0.001 |
| Control | CSO-BT / Mission–Cooperation | AllyDist | 2.16 ± 0.20 | 2.22 ± 0.21 | -0.08 | 0.300 |
| Control | CSO-BT / Mission–Cooperation | Deaths | 2.01 ± 0.55 | 1.52 ± 0.39 | +0.04 | 0.653 |
| Control | OW-BT / Persistent Objective | CtrlScore | 120.00 ± 0.00 | 114.95 ± 3.93 | +0.09 | 0.002 |
| Control | OW-BT / Persistent Objective | ObjCommit | 0.95 ± 0.01 | 0.90 ± 0.03 | +0.27 | <0.001 |
| Control | OW-BT / Persistent Objective | AllyDist | 1.97 ± 0.20 | 3.05 ± 0.41 | -0.45 | <0.001 |
| Control | OW-BT / Persistent Objective | Deaths | 1.35 ± 0.36 | 1.94 ± 0.47 | -0.11 | 0.162 |
| Control | AC-BT / Aggressive | CtrlScore | 0.41 ± 0.19 | 70.06 ± 10.78 | -0.64 | <0.001 |
| Control | AC-BT / Aggressive | ObjCommit | 0.00 ± 0.00 | 0.32 ± 0.06 | -0.85 | <0.001 |
| Control | AC-BT / Aggressive | AllyDist | 7.15 ± 0.25 | 4.35 ± 0.35 | +0.80 | <0.001 |
| Control | AC-BT / Aggressive | Deaths | 16.16 ± 0.40 | 4.93 ± 0.78 | +0.98 | <0.001 |
| Control | XO-BT / Survival-Aware | CtrlScore | 0.35 ± 0.17 | 13.59 ± 6.58 | -0.17 | 0.008 |
| Control | XO-BT / Survival-Aware | ObjCommit | 0.00 ± 0.00 | 0.03 ± 0.02 | -0.25 | <0.001 |
| Control | XO-BT / Survival-Aware | AllyDist | 6.81 ± 0.27 | 6.05 ± 0.63 | +0.23 | 0.005 |
| Control | XO-BT / Survival-Aware | Deaths | 15.84 ± 0.51 | 2.21 ± 0.42 | +0.99 | <0.001 |

## Fingerprint matching (nearest priority-structure style, normalised 4-metric space)

| Baseline | Mission | Deathmatch | Control | pooled (12-D) |
|---|---|---|---|---|
| CSO-BT | Mission–Cooperation (0.56) | Aggressive (0.41) | Mission–Cooperation (0.61) | Aggressive (1.05) |
| OW-BT | Mission–Cooperation (0.24) | Aggressive (0.65) | Mission–Cooperation (0.19) | Mission–Cooperation (1.04) |
| AC-BT | Survival-Aware (0.84) | Survival-Aware (0.80) | Survival-Aware (0.86) | Survival-Aware (1.45) |
| XO-BT | Survival-Aware (0.85) | Survival-Aware (0.80) | Survival-Aware (0.80) | Survival-Aware (1.41) |
| UtilityAI | Mission–Cooperation (0.32) | Aggressive (0.46) | Mission–Cooperation (0.36) | Mission–Cooperation (0.71) |
