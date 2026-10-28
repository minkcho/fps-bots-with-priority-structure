# Cost-term ablation and external baselines (random map)

Consistency check (CRN): cost-term full = main. **passed**

## Leave-one-out cost-term ablation (paired Wilcoxon vs full; r > 0: variant higher; Holm per condition)


### Mission / Mission–Cooperation

| Variant | ObjCommit | AllyDist | EngRedirect | Deaths |
|---|---|---|---|---|
| full | 0.95 ± 0.02 | 1.91 ± 0.32 | 0.00 ± 0.00 | 4.20 ± 1.40 |
| no_exposure | 0.94 ± 0.02 | 2.04 ± 0.35 | 0.00 ± 0.00 | 4.80 ± 1.49 |
| no_cover | 0.93 ± 0.03 | 2.05 ± 0.39 | 0.01 ± 0.02 | 4.47 ± 1.50 |
| no_separation | 0.92 ± 0.05 | 1.90 ± 0.34 | 0.01 ± 0.01 | 3.50 ± 1.22 |

- nominally significant: none

### Mission / Persistent Objective

| Variant | ObjCommit | AllyDist | EngRedirect | Deaths |
|---|---|---|---|---|
| full | 0.90 ± 0.04 | 2.50 ± 0.51 | 0.00 ± 0.01 | 4.87 ± 1.58 |
| no_exposure | 0.91 ± 0.03 | 2.47 ± 0.46 | 0.00 ± 0.01 | 5.87 ± 1.84 |
| no_cover | 0.91 ± 0.04 | 2.25 ± 0.42 | 0.00 ± 0.00 | 4.13 ± 1.30 |
| no_separation | 0.90 ± 0.04 | 2.65 ± 0.60 | 0.00 ± 0.00 | 4.73 ± 1.62 |

- nominally significant: none

### Mission / Aggressive

| Variant | ObjCommit | AllyDist | EngRedirect | Deaths |
|---|---|---|---|---|
| full | 0.20 ± 0.11 | 3.84 ± 0.78 | 0.86 ± 0.19 | 6.83 ± 1.49 |
| no_exposure | 0.30 ± 0.13 | 3.09 ± 0.76 | 0.78 ± 0.18 | 6.37 ± 1.43 |
| no_cover | 0.21 ± 0.11 | 3.00 ± 0.47 | 0.86 ± 0.21 | 6.67 ± 1.53 |
| no_separation | 0.24 ± 0.12 | 3.88 ± 0.84 | 0.68 ± 0.19 | 5.43 ± 1.51 |

- nominally significant: no_exposure AllyDist: r=-0.45, p=0.035, p_Holm=0.380; no_cover AllyDist: r=-0.48, p=0.025, p_Holm=0.297

### Mission / Survival-Aware

| Variant | ObjCommit | AllyDist | EngRedirect | Deaths |
|---|---|---|---|---|
| full | 0.02 ± 0.02 | 4.52 ± 1.01 | 0.52 ± 0.18 | 3.27 ± 0.73 |
| no_exposure | 0.08 ± 0.07 | 2.96 ± 0.56 | 0.99 ± 0.46 | 4.23 ± 1.18 |
| no_cover | 0.11 ± 0.09 | 3.57 ± 0.60 | 0.54 ± 0.15 | 3.17 ± 0.98 |
| no_separation | 0.03 ± 0.03 | 3.40 ± 0.80 | 0.49 ± 0.15 | 2.57 ± 0.88 |

- nominally significant: no_exposure AllyDist: r=-0.67, p=<0.001, p_Holm=0.012

### Deathmatch / Mission–Cooperation

| Variant | EngRedirect | ResSeek | AllyDist | Deaths |
|---|---|---|---|---|
| full | 0.19 ± 0.10 | 0.06 ± 0.03 | 2.09 ± 0.34 | 4.53 ± 1.10 |
| no_exposure | 0.18 ± 0.09 | 0.05 ± 0.05 | 1.98 ± 0.21 | 5.73 ± 1.58 |
| no_cover | 0.28 ± 0.25 | 0.04 ± 0.03 | 2.01 ± 0.23 | 4.60 ± 1.21 |
| no_separation | 0.37 ± 0.38 | 0.29 ± 0.45 | 2.20 ± 0.30 | 4.43 ± 1.24 |

- nominally significant: none

### Deathmatch / Persistent Objective

| Variant | EngRedirect | ResSeek | AllyDist | Deaths |
|---|---|---|---|---|
| full | 0.06 ± 0.04 | 0.00 ± 0.01 | 5.29 ± 0.69 | 4.77 ± 0.81 |
| no_exposure | 0.14 ± 0.05 | 0.00 ± 0.01 | 4.40 ± 0.61 | 7.13 ± 0.96 |
| no_cover | 0.05 ± 0.03 | 0.00 ± 0.01 | 5.06 ± 0.64 | 5.10 ± 0.94 |
| no_separation | 0.08 ± 0.03 | 0.01 ± 0.01 | 5.71 ± 0.62 | 4.73 ± 0.84 |

- nominally significant: no_exposure EngRedirect: r=+0.51, p=0.025, p_Holm=0.280; no_exposure AllyDist: r=-0.42, p=0.043, p_Holm=0.427; no_exposure Deaths: r=+0.85, p=<0.001, p_Holm=0.002

### Deathmatch / Aggressive

| Variant | EngRedirect | ResSeek | AllyDist | Deaths |
|---|---|---|---|---|
| full | 1.33 ± 0.19 | 0.00 ± 0.00 | 4.15 ± 0.62 | 10.03 ± 1.38 |
| no_exposure | 1.51 ± 0.22 | 0.00 ± 0.00 | 4.00 ± 0.59 | 11.13 ± 1.55 |
| no_cover | 1.31 ± 0.19 | 0.00 ± 0.00 | 3.93 ± 0.48 | 9.73 ± 1.34 |
| no_separation | 1.35 ± 0.16 | 0.00 ± 0.00 | 4.14 ± 0.59 | 10.47 ± 1.15 |

- nominally significant: none

### Deathmatch / Survival-Aware

| Variant | EngRedirect | ResSeek | AllyDist | Deaths |
|---|---|---|---|---|
| full | 0.69 ± 0.21 | 0.41 ± 0.10 | 3.43 ± 0.50 | 3.50 ± 0.77 |
| no_exposure | 1.73 ± 1.45 | 0.75 ± 0.18 | 2.88 ± 0.48 | 5.93 ± 1.33 |
| no_cover | 0.57 ± 0.22 | 0.42 ± 0.09 | 3.21 ± 0.51 | 3.43 ± 0.77 |
| no_separation | 0.58 ± 0.17 | 0.41 ± 0.10 | 4.40 ± 0.76 | 3.13 ± 0.85 |

- nominally significant: no_exposure EngRedirect: r=+0.50, p=0.017, p_Holm=0.168; no_exposure ResSeek: r=+0.67, p=0.001, p_Holm=0.013; no_exposure Deaths: r=+0.70, p=0.001, p_Holm=0.015

### Control / Mission–Cooperation

| Variant | CtrlScore | ObjCommit | AllyDist | Deaths |
|---|---|---|---|---|
| full | 114.23 ± 8.83 | 0.96 ± 0.01 | 1.69 ± 0.32 | 1.07 ± 0.47 |
| no_exposure | 120.00 ± 0.00 | 0.95 ± 0.02 | 1.88 ± 0.35 | 1.33 ± 0.64 |
| no_cover | 114.23 ± 8.83 | 0.96 ± 0.01 | 1.67 ± 0.31 | 1.07 ± 0.47 |
| no_separation | 114.23 ± 8.83 | 0.95 ± 0.03 | 1.76 ± 0.33 | 1.27 ± 0.66 |

- nominally significant: no_cover ObjCommit: r=+0.86, p=0.047, p_Holm=0.516; no_cover AllyDist: r=-0.82, p=0.014, p_Holm=0.164

### Control / Persistent Objective

| Variant | CtrlScore | ObjCommit | AllyDist | Deaths |
|---|---|---|---|---|
| full | 118.23 ± 3.61 | 0.90 ± 0.07 | 2.77 ± 1.04 | 1.53 ± 0.66 |
| no_exposure | 112.00 ± 11.37 | 0.87 ± 0.10 | 2.34 ± 0.94 | 1.63 ± 0.79 |
| no_cover | 120.00 ± 0.00 | 0.91 ± 0.06 | 2.29 ± 0.77 | 1.47 ± 0.61 |
| no_separation | 116.00 ± 8.18 | 0.89 ± 0.08 | 2.40 ± 0.82 | 1.60 ± 0.69 |

- nominally significant: no_separation AllyDist: r=-0.78, p=0.027, p_Holm=0.328

### Control / Aggressive

| Variant | CtrlScore | ObjCommit | AllyDist | Deaths |
|---|---|---|---|---|
| full | 39.70 ± 20.16 | 0.17 ± 0.09 | 3.87 ± 0.59 | 6.43 ± 1.60 |
| no_exposure | 57.10 ± 22.42 | 0.26 ± 0.11 | 3.25 ± 0.62 | 4.57 ± 1.36 |
| no_cover | 36.93 ± 20.18 | 0.13 ± 0.09 | 4.75 ± 0.84 | 6.17 ± 1.71 |
| no_separation | 42.50 ± 20.56 | 0.16 ± 0.09 | 3.71 ± 0.63 | 5.87 ± 1.51 |

- nominally significant: no_exposure Deaths: r=-0.52, p=0.022, p_Holm=0.262

### Control / Survival-Aware

| Variant | CtrlScore | ObjCommit | AllyDist | Deaths |
|---|---|---|---|---|
| full | 16.43 ± 14.74 | 0.03 ± 0.03 | 4.38 ± 1.13 | 2.27 ± 0.85 |
| no_exposure | 17.90 ± 14.39 | 0.04 ± 0.04 | 3.69 ± 0.77 | 4.77 ± 1.36 |
| no_cover | 30.13 ± 17.54 | 0.08 ± 0.05 | 4.04 ± 0.81 | 3.23 ± 0.92 |
| no_separation | 12.83 ± 12.77 | 0.04 ± 0.04 | 3.99 ± 0.88 | 3.13 ± 0.97 |

- nominally significant: no_exposure Deaths: r=+0.70, p=0.001, p_Holm=0.018; no_cover ObjCommit: r=+0.60, p=0.041, p_Holm=0.454

## External baselines (vs fixed Aggressive opponent)

| Scenario | Agent | ObjCommit | AllyDist | EngRedirect | ResSeek | Kills | Deaths | Control |
|---|---|---|---|---|---|---|---|---|
| Mission | CSO-BT | 0.80 ± 0.08 | 2.12 ± 0.42 | 2.47 ± 0.82 | 0.00 ± 0.00 | 6.5 ± 2.1 | 4.9 ± 1.7 |  |
| Mission | OW-BT | 0.94 ± 0.02 | 2.09 ± 0.36 | 0.00 ± 0.00 | 0.70 ± 0.25 | 7.1 ± 2.2 | 5.0 ± 1.7 |  |
| Mission | AC-BT | 0.00 ± 0.00 | 6.57 ± 1.44 | 0.05 ± 0.03 | 1.44 ± 0.30 | 11.0 ± 1.9 | 9.8 ± 1.8 |  |
| Mission | XO-BT | 0.00 ± 0.00 | 7.46 ± 0.60 | 0.12 ± 0.05 | 2.46 ± 0.16 | 17.0 ± 0.7 | 15.6 ± 0.8 |  |
| Mission | UtilityAI | 0.93 ± 0.02 | 2.61 ± 0.64 | 1.87 ± 0.64 | 0.01 ± 0.02 | 7.1 ± 2.2 | 6.2 ± 2.1 |  |
| Mission | Mission–Cooperation | 0.95 ± 0.02 | 1.91 ± 0.32 | 0.00 ± 0.00 | 0.00 ± 0.00 | 5.4 ± 1.6 | 4.2 ± 1.4 |  |
| Mission | Persistent Objective | 0.90 ± 0.04 | 2.50 ± 0.51 | 0.00 ± 0.01 | 0.00 ± 0.00 | 6.1 ± 1.9 | 4.9 ± 1.6 |  |
| Mission | Aggressive | 0.20 ± 0.11 | 3.84 ± 0.78 | 0.86 ± 0.19 | 0.00 ± 0.00 | 6.7 ± 1.5 | 6.8 ± 1.5 |  |
| Mission | Survival-Aware | 0.02 ± 0.02 | 4.52 ± 1.01 | 0.52 ± 0.18 | 0.43 ± 0.11 | 4.4 ± 1.0 | 3.3 ± 0.7 |  |
| Deathmatch | CSO-BT | 0.00 ± 0.00 | 2.30 ± 0.39 | 1.74 ± 0.32 | 0.00 ± 0.00 | 8.8 ± 1.6 | 7.7 ± 1.6 |  |
| Deathmatch | OW-BT | 0.00 ± 0.00 | 2.44 ± 0.33 | 1.32 ± 0.49 | 0.81 ± 0.28 | 6.9 ± 2.2 | 5.7 ± 2.0 |  |
| Deathmatch | AC-BT | 0.00 ± 0.00 | 6.02 ± 1.24 | 0.12 ± 0.07 | 1.93 ± 0.22 | 13.9 ± 1.1 | 12.9 ± 1.2 |  |
| Deathmatch | XO-BT | 0.00 ± 0.00 | 7.72 ± 0.62 | 0.18 ± 0.07 | 2.50 ± 0.11 | 17.4 ± 0.7 | 15.3 ± 0.8 |  |
| Deathmatch | UtilityAI | 0.00 ± 0.00 | 2.68 ± 0.28 | 1.01 ± 0.32 | 1.21 ± 0.68 | 7.5 ± 2.2 | 6.8 ± 2.0 |  |
| Deathmatch | Mission–Cooperation | 0.00 ± 0.00 | 2.09 ± 0.34 | 0.19 ± 0.10 | 0.06 ± 0.03 | 5.7 ± 1.5 | 4.5 ± 1.1 |  |
| Deathmatch | Persistent Objective | 0.00 ± 0.00 | 5.29 ± 0.69 | 0.06 ± 0.04 | 0.00 ± 0.01 | 8.7 ± 0.9 | 4.8 ± 0.8 |  |
| Deathmatch | Aggressive | 0.00 ± 0.00 | 4.15 ± 0.62 | 1.33 ± 0.19 | 0.00 ± 0.00 | 10.1 ± 1.4 | 10.0 ± 1.4 |  |
| Deathmatch | Survival-Aware | 0.00 ± 0.00 | 3.43 ± 0.50 | 0.69 ± 0.21 | 0.41 ± 0.10 | 4.2 ± 1.1 | 3.5 ± 0.8 |  |
| Control | CSO-BT | 0.80 ± 0.06 | 1.63 ± 0.32 | 3.00 ± 1.13 | 0.00 ± 0.00 | 2.8 ± 1.1 | 1.9 ± 0.9 | 116.03 ± 8.11; wins 29/30 |
| Control | OW-BT | 0.97 ± 0.02 | 1.68 ± 0.38 | 0.00 ± 0.00 | 0.44 ± 0.22 | 2.2 ± 0.9 | 1.5 ± 0.8 | 120.00 ± 0.00; wins 30/30 |
| Control | AC-BT | 0.00 ± 0.00 | 6.44 ± 1.26 | 0.09 ± 0.04 | 1.61 ± 0.26 | 12.0 ± 1.9 | 10.2 ± 1.8 | 1.07 ± 0.95; wins 0/30 |
| Control | XO-BT | 0.00 ± 0.00 | 7.24 ± 0.73 | 0.11 ± 0.06 | 2.43 ± 0.18 | 16.5 ± 1.1 | 15.1 ± 1.1 | 0.00 ± 0.00; wins 0/30 |
| Control | UtilityAI | 0.95 ± 0.02 | 2.10 ± 0.56 | 1.38 ± 0.51 | 0.00 ± 0.00 | 2.2 ± 0.9 | 1.4 ± 0.7 | 120.00 ± 0.00; wins 30/30 |
| Control | Mission–Cooperation | 0.96 ± 0.01 | 1.69 ± 0.32 | 0.00 ± 0.00 | 0.00 ± 0.00 | 1.9 ± 0.7 | 1.1 ± 0.5 | 114.23 ± 8.83; wins 28/30 |
| Control | Persistent Objective | 0.90 ± 0.07 | 2.77 ± 1.04 | 0.00 ± 0.00 | 0.00 ± 0.00 | 2.4 ± 0.9 | 1.5 ± 0.7 | 118.23 ± 3.61; wins 29/30 |
| Control | Aggressive | 0.17 ± 0.09 | 3.87 ± 0.59 | 1.00 ± 0.19 | 0.00 ± 0.00 | 6.5 ± 1.7 | 6.4 ± 1.6 | 39.70 ± 20.16; wins 8/30 |
| Control | Survival-Aware | 0.03 ± 0.03 | 4.38 ± 1.13 | 0.90 ± 0.84 | 0.31 ± 0.11 | 3.5 ± 0.9 | 2.3 ± 0.9 | 16.43 ± 14.74; wins 3/30 |

## Behaviour trees vs corresponding priority-structure styles (Mann-Whitney; r > 0: BT higher)

| Scenario | Pair | Metric | BT | Style | r | p |
|---|---|---|---|---|---|---|
| Mission | CSO-BT / Mission–Cooperation | ObjCommit | 0.80 ± 0.08 | 0.95 ± 0.02 | -0.51 | <0.001 |
| Mission | CSO-BT / Mission–Cooperation | AllyDist | 2.12 ± 0.42 | 1.91 ± 0.32 | +0.01 | 0.953 |
| Mission | CSO-BT / Mission–Cooperation | EngRedirect | 2.47 ± 0.82 | 0.00 ± 0.00 | +0.73 | <0.001 |
| Mission | CSO-BT / Mission–Cooperation | Deaths | 4.87 ± 1.71 | 4.20 ± 1.40 | +0.06 | 0.674 |
| Mission | OW-BT / Persistent Objective | ObjCommit | 0.94 ± 0.02 | 0.90 ± 0.04 | +0.21 | 0.166 |
| Mission | OW-BT / Persistent Objective | AllyDist | 2.09 ± 0.36 | 2.50 ± 0.51 | -0.14 | 0.347 |
| Mission | OW-BT / Persistent Objective | EngRedirect | 0.00 ± 0.00 | 0.00 ± 0.01 | -0.03 | 0.334 |
| Mission | OW-BT / Persistent Objective | Deaths | 5.03 ± 1.73 | 4.87 ± 1.58 | +0.02 | 0.886 |
| Mission | AC-BT / Aggressive | ObjCommit | 0.00 ± 0.00 | 0.20 ± 0.11 | -0.60 | <0.001 |
| Mission | AC-BT / Aggressive | AllyDist | 6.57 ± 1.44 | 3.84 ± 0.78 | +0.46 | 0.002 |
| Mission | AC-BT / Aggressive | EngRedirect | 0.05 ± 0.03 | 0.86 ± 0.19 | -0.92 | <0.001 |
| Mission | AC-BT / Aggressive | Deaths | 9.83 ± 1.85 | 6.83 ± 1.49 | +0.40 | 0.008 |
| Mission | XO-BT / Survival-Aware | ObjCommit | 0.00 ± 0.00 | 0.02 ± 0.02 | -0.30 | 0.001 |
| Mission | XO-BT / Survival-Aware | AllyDist | 7.46 ± 0.60 | 4.52 ± 1.01 | +0.65 | <0.001 |
| Mission | XO-BT / Survival-Aware | EngRedirect | 0.12 ± 0.05 | 0.52 ± 0.18 | -0.56 | <0.001 |
| Mission | XO-BT / Survival-Aware | Deaths | 15.63 ± 0.76 | 3.27 ± 0.73 | +1.00 | <0.001 |
| Deathmatch | CSO-BT / Mission–Cooperation | EngRedirect | 1.74 ± 0.32 | 0.19 ± 0.10 | +0.95 | <0.001 |
| Deathmatch | CSO-BT / Mission–Cooperation | ResSeek | 0.00 ± 0.00 | 0.06 ± 0.03 | -0.40 | <0.001 |
| Deathmatch | CSO-BT / Mission–Cooperation | AllyDist | 2.30 ± 0.39 | 2.09 ± 0.34 | +0.13 | 0.379 |
| Deathmatch | CSO-BT / Mission–Cooperation | Deaths | 7.70 ± 1.63 | 4.53 ± 1.10 | +0.43 | 0.004 |
| Deathmatch | OW-BT / Persistent Objective | EngRedirect | 1.32 ± 0.49 | 0.06 ± 0.04 | +0.58 | <0.001 |
| Deathmatch | OW-BT / Persistent Objective | ResSeek | 0.81 ± 0.28 | 0.00 ± 0.01 | +0.69 | <0.001 |
| Deathmatch | OW-BT / Persistent Objective | AllyDist | 2.44 ± 0.33 | 5.29 ± 0.69 | -0.83 | <0.001 |
| Deathmatch | OW-BT / Persistent Objective | Deaths | 5.73 ± 1.97 | 4.77 ± 0.81 | +0.05 | 0.743 |
| Deathmatch | AC-BT / Aggressive | EngRedirect | 0.12 ± 0.07 | 1.33 ± 0.19 | -0.98 | <0.001 |
| Deathmatch | AC-BT / Aggressive | ResSeek | 1.93 ± 0.22 | 0.00 ± 0.00 | +1.00 | <0.001 |
| Deathmatch | AC-BT / Aggressive | AllyDist | 6.02 ± 1.24 | 4.15 ± 0.62 | +0.43 | 0.004 |
| Deathmatch | AC-BT / Aggressive | Deaths | 12.90 ± 1.17 | 10.03 ± 1.38 | +0.43 | 0.005 |
| Deathmatch | XO-BT / Survival-Aware | EngRedirect | 0.18 ± 0.07 | 0.69 ± 0.21 | -0.64 | <0.001 |
| Deathmatch | XO-BT / Survival-Aware | ResSeek | 2.50 ± 0.11 | 0.41 ± 0.10 | +1.00 | <0.001 |
| Deathmatch | XO-BT / Survival-Aware | AllyDist | 7.72 ± 0.62 | 3.43 ± 0.50 | +0.98 | <0.001 |
| Deathmatch | XO-BT / Survival-Aware | Deaths | 15.27 ± 0.77 | 3.50 ± 0.77 | +1.00 | <0.001 |
| Control | CSO-BT / Mission–Cooperation | CtrlScore | 116.03 ± 8.11 | 114.23 ± 8.83 | +0.03 | 0.570 |
| Control | CSO-BT / Mission–Cooperation | ObjCommit | 0.80 ± 0.06 | 0.96 ± 0.01 | -0.79 | <0.001 |
| Control | CSO-BT / Mission–Cooperation | AllyDist | 1.63 ± 0.32 | 1.69 ± 0.32 | -0.17 | 0.272 |
| Control | CSO-BT / Mission–Cooperation | Deaths | 1.93 ± 0.88 | 1.07 ± 0.47 | +0.14 | 0.335 |
| Control | OW-BT / Persistent Objective | CtrlScore | 120.00 ± 0.00 | 118.23 ± 3.61 | +0.03 | 0.334 |
| Control | OW-BT / Persistent Objective | ObjCommit | 0.97 ± 0.02 | 0.90 ± 0.07 | +0.47 | 0.002 |
| Control | OW-BT / Persistent Objective | AllyDist | 1.68 ± 0.38 | 2.77 ± 1.04 | -0.17 | 0.246 |
| Control | OW-BT / Persistent Objective | Deaths | 1.47 ± 0.75 | 1.53 ± 0.66 | -0.06 | 0.692 |
| Control | AC-BT / Aggressive | CtrlScore | 1.07 ± 0.95 | 39.70 ± 20.16 | -0.33 | 0.007 |
| Control | AC-BT / Aggressive | ObjCommit | 0.00 ± 0.00 | 0.17 ± 0.09 | -0.60 | <0.001 |
| Control | AC-BT / Aggressive | AllyDist | 6.44 ± 1.26 | 3.87 ± 0.59 | +0.45 | 0.003 |
| Control | AC-BT / Aggressive | Deaths | 10.20 ± 1.82 | 6.43 ± 1.60 | +0.46 | 0.002 |
| Control | XO-BT / Survival-Aware | CtrlScore | 0.00 ± 0.00 | 16.43 ± 14.74 | -0.30 | 0.001 |
| Control | XO-BT / Survival-Aware | ObjCommit | 0.00 ± 0.00 | 0.03 ± 0.03 | -0.20 | 0.011 |
| Control | XO-BT / Survival-Aware | AllyDist | 7.24 ± 0.73 | 4.38 ± 1.13 | +0.63 | <0.001 |
| Control | XO-BT / Survival-Aware | Deaths | 15.07 ± 1.14 | 2.27 ± 0.85 | +0.98 | <0.001 |

## Fingerprint matching (nearest priority-structure style, normalised 4-metric space)

| Baseline | Mission | Deathmatch | Control | pooled (12-D) |
|---|---|---|---|---|
| CSO-BT | Persistent Objective (0.83) | Aggressive (0.33) | Aggressive (1.00) | Aggressive (1.36) |
| OW-BT | Mission–Cooperation (0.28) | Survival-Aware (0.31) | Mission–Cooperation (0.18) | Mission–Cooperation (0.59) |
| AC-BT | Survival-Aware (0.55) | Survival-Aware (0.76) | Survival-Aware (0.68) | Survival-Aware (1.16) |
| XO-BT | Survival-Aware (0.95) | Persistent Objective (1.08) | Survival-Aware (1.01) | Survival-Aware (1.77) |
| UtilityAI | Persistent Objective (0.62) | Survival-Aware (0.36) | Mission–Cooperation (0.47) | Mission–Cooperation (0.96) |
