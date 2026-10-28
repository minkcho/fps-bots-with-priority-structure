# Cost-term ablation and external baselines (urban map)

Consistency check (CRN): cost-term full = main. **passed**

## Leave-one-out cost-term ablation (paired Wilcoxon vs full; r > 0: variant higher; Holm per condition)


### Mission / Mission–Cooperation

| Variant | ObjCommit | AllyDist | EngRedirect | Deaths |
|---|---|---|---|---|
| full | 0.94 ± 0.01 | 1.77 ± 0.18 | 0.02 ± 0.01 | 4.22 ± 0.89 |
| no_exposure | 0.95 ± 0.01 | 1.92 ± 0.23 | 0.01 ± 0.01 | 4.93 ± 1.05 |
| no_cover | 0.95 ± 0.01 | 1.67 ± 0.16 | 0.02 ± 0.01 | 3.93 ± 0.88 |
| no_separation | 0.94 ± 0.01 | 1.77 ± 0.18 | 0.02 ± 0.01 | 4.22 ± 0.89 |

- nominally significant: no_exposure Deaths: r=+0.43, p=0.007, p_Holm=0.088; no_cover ObjCommit: r=+0.30, p=0.037, p_Holm=0.412

### Mission / Persistent Objective

| Variant | ObjCommit | AllyDist | EngRedirect | Deaths |
|---|---|---|---|---|
| full | 0.87 ± 0.04 | 3.00 ± 0.41 | 0.00 ± 0.00 | 5.19 ± 0.98 |
| no_exposure | 0.87 ± 0.04 | 2.75 ± 0.42 | 0.01 ± 0.01 | 5.73 ± 1.06 |
| no_cover | 0.86 ± 0.04 | 3.27 ± 0.60 | 0.00 ± 0.01 | 4.91 ± 0.96 |
| no_separation | 0.87 ± 0.04 | 3.00 ± 0.41 | 0.00 ± 0.00 | 5.19 ± 0.98 |

- nominally significant: no_exposure AllyDist: r=-0.30, p=0.033, p_Holm=0.398; no_exposure EngRedirect: r=+0.83, p=0.039, p_Holm=0.430

### Mission / Aggressive

| Variant | ObjCommit | AllyDist | EngRedirect | Deaths |
|---|---|---|---|---|
| full | 0.32 ± 0.06 | 4.48 ± 0.41 | 1.69 ± 0.20 | 7.29 ± 0.88 |
| no_exposure | 0.33 ± 0.05 | 4.24 ± 0.33 | 1.89 ± 0.20 | 8.07 ± 0.91 |
| no_cover | 0.29 ± 0.05 | 4.44 ± 0.36 | 1.72 ± 0.19 | 7.84 ± 0.84 |
| no_separation | 0.32 ± 0.06 | 4.48 ± 0.41 | 1.69 ± 0.20 | 7.29 ± 0.88 |

- nominally significant: no_exposure EngRedirect: r=+0.31, p=0.009, p_Holm=0.106

### Mission / Survival-Aware

| Variant | ObjCommit | AllyDist | EngRedirect | Deaths |
|---|---|---|---|---|
| full | 0.04 ± 0.03 | 6.89 ± 0.71 | 0.00 ± 0.00 | 2.89 ± 0.46 |
| no_exposure | 0.03 ± 0.02 | 6.58 ± 0.72 | 0.00 ± 0.00 | 3.65 ± 0.52 |
| no_cover | 0.02 ± 0.02 | 7.43 ± 0.75 | 0.00 ± 0.00 | 3.08 ± 0.42 |
| no_separation | 0.04 ± 0.03 | 6.89 ± 0.71 | 0.00 ± 0.00 | 2.89 ± 0.46 |

- nominally significant: no_exposure Deaths: r=+0.30, p=0.017, p_Holm=0.185; no_cover ObjCommit: r=-0.43, p=0.015, p_Holm=0.183

### Deathmatch / Mission–Cooperation

| Variant | EngRedirect | ResSeek | AllyDist | Deaths |
|---|---|---|---|---|
| full | 0.46 ± 0.05 | 0.24 ± 0.05 | 2.69 ± 0.09 | 9.12 ± 0.62 |
| no_exposure | 0.41 ± 0.05 | 0.30 ± 0.06 | 2.66 ± 0.11 | 9.31 ± 0.64 |
| no_cover | 0.42 ± 0.06 | 0.19 ± 0.05 | 2.63 ± 0.09 | 8.54 ± 0.61 |
| no_separation | 0.46 ± 0.05 | 0.24 ± 0.05 | 2.69 ± 0.09 | 9.12 ± 0.62 |

- nominally significant: none

### Deathmatch / Persistent Objective

| Variant | EngRedirect | ResSeek | AllyDist | Deaths |
|---|---|---|---|---|
| full | 0.09 ± 0.02 | 0.02 ± 0.01 | 5.61 ± 0.26 | 5.69 ± 0.45 |
| no_exposure | 0.20 ± 0.03 | 0.05 ± 0.01 | 4.57 ± 0.24 | 8.59 ± 0.56 |
| no_cover | 0.10 ± 0.02 | 0.02 ± 0.01 | 5.53 ± 0.30 | 5.72 ± 0.40 |
| no_separation | 0.09 ± 0.02 | 0.02 ± 0.01 | 5.61 ± 0.26 | 5.69 ± 0.45 |

- nominally significant: no_exposure EngRedirect: r=+0.69, p=<0.001, p_Holm=<0.001; no_exposure ResSeek: r=+0.50, p=0.002, p_Holm=0.018; no_exposure AllyDist: r=-0.63, p=<0.001, p_Holm=<0.001; no_exposure Deaths: r=+0.82, p=<0.001, p_Holm=<0.001

### Deathmatch / Aggressive

| Variant | EngRedirect | ResSeek | AllyDist | Deaths |
|---|---|---|---|---|
| full | 2.86 ± 0.13 | 0.35 ± 0.04 | 4.73 ± 0.20 | 11.41 ± 0.53 |
| no_exposure | 3.24 ± 0.12 | 0.40 ± 0.04 | 4.60 ± 0.24 | 12.49 ± 0.52 |
| no_cover | 2.83 ± 0.11 | 0.31 ± 0.04 | 4.72 ± 0.22 | 11.34 ± 0.47 |
| no_separation | 2.86 ± 0.13 | 0.35 ± 0.04 | 4.73 ± 0.20 | 11.41 ± 0.53 |

- nominally significant: no_exposure EngRedirect: r=+0.65, p=<0.001, p_Holm=<0.001; no_exposure Deaths: r=+0.38, p=0.002, p_Holm=0.017

### Deathmatch / Survival-Aware

| Variant | EngRedirect | ResSeek | AllyDist | Deaths |
|---|---|---|---|---|
| full | 0.00 ± 0.00 | 0.61 ± 0.06 | 7.42 ± 0.57 | 4.72 ± 0.50 |
| no_exposure | 0.00 ± 0.00 | 0.66 ± 0.07 | 7.23 ± 0.65 | 5.43 ± 0.54 |
| no_cover | 0.00 ± 0.00 | 0.65 ± 0.06 | 6.93 ± 0.57 | 5.08 ± 0.48 |
| no_separation | 0.00 ± 0.00 | 0.61 ± 0.06 | 7.42 ± 0.57 | 4.72 ± 0.50 |

- nominally significant: none

### Control / Mission–Cooperation

| Variant | CtrlScore | ObjCommit | AllyDist | Deaths |
|---|---|---|---|---|
| full | 117.30 ± 2.64 | 0.95 ± 0.01 | 1.84 ± 0.24 | 1.75 ± 0.53 |
| no_exposure | 117.77 ± 2.42 | 0.95 ± 0.01 | 1.91 ± 0.26 | 1.83 ± 0.59 |
| no_cover | 113.35 ± 4.55 | 0.94 ± 0.02 | 1.88 ± 0.24 | 2.03 ± 0.66 |
| no_separation | 117.30 ± 2.64 | 0.95 ± 0.01 | 1.84 ± 0.24 | 1.75 ± 0.53 |

- nominally significant: none

### Control / Persistent Objective

| Variant | CtrlScore | ObjCommit | AllyDist | Deaths |
|---|---|---|---|---|
| full | 116.86 ± 3.49 | 0.91 ± 0.03 | 2.79 ± 0.54 | 1.54 ± 0.46 |
| no_exposure | 120.00 ± 0.00 | 0.93 ± 0.02 | 2.33 ± 0.39 | 1.57 ± 0.45 |
| no_cover | 117.87 ± 2.69 | 0.91 ± 0.03 | 2.67 ± 0.54 | 1.55 ± 0.48 |
| no_separation | 116.86 ± 3.49 | 0.91 ± 0.03 | 2.79 ± 0.54 | 1.54 ± 0.46 |

- nominally significant: no_exposure ObjCommit: r=+0.75, p=<0.001, p_Holm=<0.001; no_exposure AllyDist: r=-0.74, p=<0.001, p_Holm=<0.001; no_cover AllyDist: r=-0.28, p=0.034, p_Holm=0.344

### Control / Aggressive

| Variant | CtrlScore | ObjCommit | AllyDist | Deaths |
|---|---|---|---|---|
| full | 73.61 ± 10.43 | 0.29 ± 0.05 | 4.69 ± 0.36 | 6.14 ± 0.80 |
| no_exposure | 73.01 ± 10.35 | 0.31 ± 0.05 | 4.52 ± 0.36 | 5.67 ± 0.76 |
| no_cover | 64.28 ± 10.90 | 0.28 ± 0.06 | 5.06 ± 0.53 | 5.17 ± 0.72 |
| no_separation | 73.61 ± 10.43 | 0.29 ± 0.05 | 4.69 ± 0.36 | 6.14 ± 0.80 |

- nominally significant: no_cover Deaths: r=-0.27, p=0.029, p_Holm=0.344

### Control / Survival-Aware

| Variant | CtrlScore | ObjCommit | AllyDist | Deaths |
|---|---|---|---|---|
| full | 7.94 ± 5.10 | 0.02 ± 0.02 | 6.71 ± 0.67 | 2.59 ± 0.40 |
| no_exposure | 7.59 ± 5.02 | 0.02 ± 0.01 | 6.51 ± 0.66 | 3.48 ± 0.51 |
| no_cover | 12.03 ± 6.65 | 0.04 ± 0.03 | 6.28 ± 0.62 | 2.65 ± 0.43 |
| no_separation | 7.94 ± 5.10 | 0.02 ± 0.02 | 6.71 ± 0.67 | 2.59 ± 0.40 |

- nominally significant: no_exposure Deaths: r=+0.34, p=0.007, p_Holm=0.079

## External baselines (vs fixed Aggressive opponent)

| Scenario | Agent | ObjCommit | AllyDist | EngRedirect | ResSeek | Kills | Deaths | Control |
|---|---|---|---|---|---|---|---|---|
| Mission | CSO-BT | 0.54 ± 0.06 | 1.80 ± 0.19 | 5.67 ± 1.09 | 0.00 ± 0.00 | 5.7 ± 1.0 | 5.1 ± 1.1 |  |
| Mission | OW-BT | 0.95 ± 0.01 | 1.88 ± 0.23 | 0.00 ± 0.00 | 0.67 ± 0.14 | 6.2 ± 1.1 | 4.6 ± 0.9 |  |
| Mission | AC-BT | 0.00 ± 0.00 | 7.10 ± 0.30 | 0.28 ± 0.05 | 2.43 ± 0.14 | 14.8 ± 0.8 | 14.5 ± 0.8 |  |
| Mission | XO-BT | 0.00 ± 0.00 | 7.06 ± 0.31 | 0.24 ± 0.05 | 2.47 ± 0.14 | 14.6 ± 0.7 | 15.1 ± 0.8 |  |
| Mission | UtilityAI | 0.95 ± 0.01 | 2.19 ± 0.26 | 1.44 ± 0.25 | 0.00 ± 0.00 | 6.3 ± 1.1 | 6.0 ± 1.1 |  |
| Mission | Mission–Cooperation | 0.94 ± 0.01 | 1.77 ± 0.18 | 0.02 ± 0.01 | 0.00 ± 0.00 | 5.0 ± 0.9 | 4.2 ± 0.9 |  |
| Mission | Persistent Objective | 0.87 ± 0.04 | 3.00 ± 0.41 | 0.00 ± 0.00 | 0.00 ± 0.00 | 5.2 ± 0.9 | 5.2 ± 1.0 |  |
| Mission | Aggressive | 0.32 ± 0.06 | 4.48 ± 0.41 | 1.69 ± 0.20 | 0.17 ± 0.04 | 7.2 ± 0.9 | 7.3 ± 0.9 |  |
| Mission | Survival-Aware | 0.04 ± 0.03 | 6.89 ± 0.71 | 0.00 ± 0.00 | 0.38 ± 0.06 | 3.3 ± 0.4 | 2.9 ± 0.5 |  |
| Deathmatch | CSO-BT | 0.00 ± 0.00 | 3.50 ± 0.19 | 3.35 ± 0.15 | 0.00 ± 0.00 | 10.9 ± 0.5 | 11.6 ± 0.5 |  |
| Deathmatch | OW-BT | 0.00 ± 0.00 | 3.25 ± 0.24 | 3.57 ± 0.73 | 1.16 ± 0.14 | 8.9 ± 0.9 | 7.8 ± 0.9 |  |
| Deathmatch | AC-BT | 0.00 ± 0.00 | 6.86 ± 0.27 | 0.35 ± 0.06 | 2.82 ± 0.11 | 15.6 ± 0.5 | 16.7 ± 0.5 |  |
| Deathmatch | XO-BT | 0.00 ± 0.00 | 6.73 ± 0.25 | 0.29 ± 0.05 | 2.76 ± 0.09 | 15.7 ± 0.5 | 16.4 ± 0.4 |  |
| Deathmatch | UtilityAI | 0.00 ± 0.00 | 2.96 ± 0.10 | 2.09 ± 0.22 | 0.85 ± 0.12 | 9.6 ± 1.0 | 8.0 ± 0.9 |  |
| Deathmatch | Mission–Cooperation | 0.00 ± 0.00 | 2.69 ± 0.09 | 0.46 ± 0.05 | 0.24 ± 0.05 | 10.2 ± 0.6 | 9.1 ± 0.6 |  |
| Deathmatch | Persistent Objective | 0.00 ± 0.00 | 5.61 ± 0.26 | 0.09 ± 0.02 | 0.02 ± 0.01 | 7.8 ± 0.5 | 5.7 ± 0.4 |  |
| Deathmatch | Aggressive | 0.00 ± 0.00 | 4.73 ± 0.20 | 2.86 ± 0.13 | 0.35 ± 0.04 | 11.8 ± 0.5 | 11.4 ± 0.5 |  |
| Deathmatch | Survival-Aware | 0.00 ± 0.00 | 7.42 ± 0.57 | 0.00 ± 0.00 | 0.61 ± 0.06 | 4.7 ± 0.5 | 4.7 ± 0.5 |  |
| Control | CSO-BT | 0.71 ± 0.04 | 1.77 ± 0.20 | 4.42 ± 0.94 | 0.00 ± 0.00 | 2.6 ± 0.6 | 2.0 ± 0.6 | 119.32 ± 1.35; wins 99/100 |
| Control | OW-BT | 0.96 ± 0.01 | 1.75 ± 0.17 | 0.00 ± 0.00 | 0.54 ± 0.14 | 2.3 ± 0.5 | 1.6 ± 0.5 | 118.79 ± 1.71; wins 97/100 |
| Control | AC-BT | 0.00 ± 0.00 | 6.98 ± 0.30 | 0.27 ± 0.05 | 2.47 ± 0.14 | 14.7 ± 0.8 | 14.7 ± 0.8 | 0.04 ± 0.04; wins 0/100 |
| Control | XO-BT | 0.00 ± 0.00 | 6.89 ± 0.30 | 0.21 ± 0.05 | 2.46 ± 0.13 | 14.8 ± 0.7 | 15.0 ± 0.7 | 0.05 ± 0.07; wins 0/100 |
| Control | UtilityAI | 0.95 ± 0.01 | 2.00 ± 0.25 | 1.30 ± 0.26 | 0.00 ± 0.00 | 2.5 ± 0.5 | 2.3 ± 0.6 | 119.43 ± 0.62; wins 96/100 |
| Control | Mission–Cooperation | 0.95 ± 0.01 | 1.84 ± 0.24 | 0.00 ± 0.01 | 0.00 ± 0.00 | 2.2 ± 0.5 | 1.8 ± 0.5 | 117.30 ± 2.64; wins 94/100 |
| Control | Persistent Objective | 0.91 ± 0.03 | 2.79 ± 0.54 | 0.01 ± 0.01 | 0.00 ± 0.00 | 2.0 ± 0.4 | 1.5 ± 0.5 | 116.86 ± 3.49; wins 96/100 |
| Control | Aggressive | 0.29 ± 0.05 | 4.69 ± 0.36 | 2.00 ± 0.18 | 0.18 ± 0.04 | 6.1 ± 0.8 | 6.1 ± 0.8 | 73.61 ± 10.43; wins 48/100 |
| Control | Survival-Aware | 0.02 ± 0.02 | 6.71 ± 0.67 | 0.00 ± 0.00 | 0.43 ± 0.06 | 2.9 ± 0.4 | 2.6 ± 0.4 | 7.94 ± 5.10; wins 4/100 |

## Behaviour trees vs corresponding priority-structure styles (Mann-Whitney; r > 0: BT higher)

| Scenario | Pair | Metric | BT | Style | r | p |
|---|---|---|---|---|---|---|
| Mission | CSO-BT / Mission–Cooperation | ObjCommit | 0.54 ± 0.06 | 0.94 ± 0.01 | -0.79 | <0.001 |
| Mission | CSO-BT / Mission–Cooperation | AllyDist | 1.80 ± 0.19 | 1.77 ± 0.18 | -0.10 | 0.228 |
| Mission | CSO-BT / Mission–Cooperation | EngRedirect | 5.67 ± 1.09 | 0.02 ± 0.01 | +0.81 | <0.001 |
| Mission | CSO-BT / Mission–Cooperation | Deaths | 5.07 ± 1.07 | 4.22 ± 0.89 | +0.06 | 0.469 |
| Mission | OW-BT / Persistent Objective | ObjCommit | 0.95 ± 0.01 | 0.87 ± 0.04 | +0.36 | <0.001 |
| Mission | OW-BT / Persistent Objective | AllyDist | 1.88 ± 0.23 | 3.00 ± 0.41 | -0.31 | <0.001 |
| Mission | OW-BT / Persistent Objective | EngRedirect | 0.00 ± 0.00 | 0.00 ± 0.00 | -0.01 | 0.322 |
| Mission | OW-BT / Persistent Objective | Deaths | 4.57 ± 0.92 | 5.19 ± 0.98 | -0.06 | 0.438 |
| Mission | AC-BT / Aggressive | ObjCommit | 0.00 ± 0.00 | 0.32 ± 0.06 | -0.91 | <0.001 |
| Mission | AC-BT / Aggressive | AllyDist | 7.10 ± 0.30 | 4.48 ± 0.41 | +0.68 | <0.001 |
| Mission | AC-BT / Aggressive | EngRedirect | 0.28 ± 0.05 | 1.69 ± 0.20 | -0.78 | <0.001 |
| Mission | AC-BT / Aggressive | Deaths | 14.53 ± 0.79 | 7.29 ± 0.88 | +0.80 | <0.001 |
| Mission | XO-BT / Survival-Aware | ObjCommit | 0.00 ± 0.00 | 0.04 ± 0.03 | -0.31 | <0.001 |
| Mission | XO-BT / Survival-Aware | AllyDist | 7.06 ± 0.31 | 6.89 ± 0.71 | +0.15 | 0.062 |
| Mission | XO-BT / Survival-Aware | EngRedirect | 0.24 ± 0.05 | 0.00 ± 0.00 | +0.70 | <0.001 |
| Mission | XO-BT / Survival-Aware | Deaths | 15.08 ± 0.81 | 2.89 ± 0.46 | +0.93 | <0.001 |
| Deathmatch | CSO-BT / Mission–Cooperation | EngRedirect | 3.35 ± 0.15 | 0.46 ± 0.05 | +1.00 | <0.001 |
| Deathmatch | CSO-BT / Mission–Cooperation | ResSeek | 0.00 ± 0.00 | 0.24 ± 0.05 | -0.77 | <0.001 |
| Deathmatch | CSO-BT / Mission–Cooperation | AllyDist | 3.50 ± 0.19 | 2.69 ± 0.09 | +0.54 | <0.001 |
| Deathmatch | CSO-BT / Mission–Cooperation | Deaths | 11.60 ± 0.50 | 9.12 ± 0.62 | +0.46 | <0.001 |
| Deathmatch | OW-BT / Persistent Objective | EngRedirect | 3.57 ± 0.73 | 0.09 ± 0.02 | +0.83 | <0.001 |
| Deathmatch | OW-BT / Persistent Objective | ResSeek | 1.16 ± 0.14 | 0.02 ± 0.01 | +0.83 | <0.001 |
| Deathmatch | OW-BT / Persistent Objective | AllyDist | 3.25 ± 0.24 | 5.61 ± 0.26 | -0.80 | <0.001 |
| Deathmatch | OW-BT / Persistent Objective | Deaths | 7.75 ± 0.89 | 5.69 ± 0.45 | +0.33 | <0.001 |
| Deathmatch | AC-BT / Aggressive | EngRedirect | 0.35 ± 0.06 | 2.86 ± 0.13 | -1.00 | <0.001 |
| Deathmatch | AC-BT / Aggressive | ResSeek | 2.82 ± 0.11 | 0.35 ± 0.04 | +1.00 | <0.001 |
| Deathmatch | AC-BT / Aggressive | AllyDist | 6.86 ± 0.27 | 4.73 ± 0.20 | +0.81 | <0.001 |
| Deathmatch | AC-BT / Aggressive | Deaths | 16.68 ± 0.47 | 11.41 ± 0.53 | +0.86 | <0.001 |
| Deathmatch | XO-BT / Survival-Aware | EngRedirect | 0.29 ± 0.05 | 0.00 ± 0.00 | +0.76 | <0.001 |
| Deathmatch | XO-BT / Survival-Aware | ResSeek | 2.76 ± 0.09 | 0.61 ± 0.06 | +1.00 | <0.001 |
| Deathmatch | XO-BT / Survival-Aware | AllyDist | 6.73 ± 0.25 | 7.42 ± 0.57 | -0.15 | 0.061 |
| Deathmatch | XO-BT / Survival-Aware | Deaths | 16.35 ± 0.44 | 4.72 ± 0.50 | +1.00 | <0.001 |
| Control | CSO-BT / Mission–Cooperation | CtrlScore | 119.32 ± 1.35 | 117.30 ± 2.64 | +0.05 | 0.058 |
| Control | CSO-BT / Mission–Cooperation | ObjCommit | 0.71 ± 0.04 | 0.95 ± 0.01 | -0.76 | <0.001 |
| Control | CSO-BT / Mission–Cooperation | AllyDist | 1.77 ± 0.20 | 1.84 ± 0.24 | -0.25 | 0.003 |
| Control | CSO-BT / Mission–Cooperation | Deaths | 2.04 ± 0.64 | 1.75 ± 0.53 | +0.04 | 0.588 |
| Control | OW-BT / Persistent Objective | CtrlScore | 118.79 ± 1.71 | 116.86 ± 3.49 | +0.01 | 0.687 |
| Control | OW-BT / Persistent Objective | ObjCommit | 0.96 ± 0.01 | 0.91 ± 0.03 | +0.41 | <0.001 |
| Control | OW-BT / Persistent Objective | AllyDist | 1.75 ± 0.17 | 2.79 ± 0.54 | -0.17 | 0.041 |
| Control | OW-BT / Persistent Objective | Deaths | 1.55 ± 0.46 | 1.54 ± 0.46 | +0.02 | 0.779 |
| Control | AC-BT / Aggressive | CtrlScore | 0.04 ± 0.04 | 73.61 ± 10.43 | -0.76 | <0.001 |
| Control | AC-BT / Aggressive | ObjCommit | 0.00 ± 0.00 | 0.29 ± 0.05 | -0.89 | <0.001 |
| Control | AC-BT / Aggressive | AllyDist | 6.98 ± 0.30 | 4.69 ± 0.36 | +0.70 | <0.001 |
| Control | AC-BT / Aggressive | Deaths | 14.74 ± 0.78 | 6.14 ± 0.80 | +0.85 | <0.001 |
| Control | XO-BT / Survival-Aware | CtrlScore | 0.05 ± 0.07 | 7.94 ± 5.10 | -0.22 | <0.001 |
| Control | XO-BT / Survival-Aware | ObjCommit | 0.00 ± 0.00 | 0.02 ± 0.02 | -0.22 | <0.001 |
| Control | XO-BT / Survival-Aware | AllyDist | 6.89 ± 0.30 | 6.71 ± 0.67 | +0.11 | 0.171 |
| Control | XO-BT / Survival-Aware | Deaths | 15.00 ± 0.73 | 2.59 ± 0.40 | +0.96 | <0.001 |

## Fingerprint matching (nearest priority-structure style, normalised 4-metric space)

| Baseline | Mission | Deathmatch | Control | pooled (12-D) |
|---|---|---|---|---|
| CSO-BT | Aggressive (0.88) | Aggressive (0.26) | Aggressive (0.80) | Aggressive (1.22) |
| OW-BT | Mission–Cooperation (0.24) | Aggressive (0.41) | Mission–Cooperation (0.19) | Mission–Cooperation (0.72) |
| AC-BT | Survival-Aware (0.73) | Survival-Aware (0.79) | Survival-Aware (0.73) | Survival-Aware (1.30) |
| XO-BT | Survival-Aware (0.75) | Survival-Aware (0.78) | Survival-Aware (0.72) | Survival-Aware (1.30) |
| UtilityAI | Mission–Cooperation (0.26) | Mission–Cooperation (0.36) | Mission–Cooperation (0.23) | Mission–Cooperation (0.50) |
