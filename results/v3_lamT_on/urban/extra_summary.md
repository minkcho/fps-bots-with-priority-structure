# Cost-term ablation and external baselines (urban map)

Consistency check (CRN): cost-term full = main. **passed**

## Leave-one-out cost-term ablation (paired Wilcoxon vs full; r > 0: variant higher; Holm per condition)


### Mission / Mission–Cooperation

| Variant | ObjCommit | AllyDist | EngRedirect | Deaths |
|---|---|---|---|---|
| full | 0.95 ± 0.03 | 1.56 ± 0.30 | 0.01 ± 0.02 | 3.07 ± 1.77 |
| no_exposure | 0.97 ± 0.02 | 1.37 ± 0.22 | 0.00 ± 0.01 | 2.60 ± 1.47 |
| no_cover | 0.97 ± 0.02 | 1.46 ± 0.27 | 0.01 ± 0.01 | 1.93 ± 1.18 |
| no_separation | 0.97 ± 0.02 | 1.42 ± 0.25 | 0.02 ± 0.02 | 2.13 ± 1.40 |

- nominally significant: no_separation Deaths: r=-0.82, p=0.031, p_Holm=0.375

### Mission / Persistent Objective

| Variant | ObjCommit | AllyDist | EngRedirect | Deaths |
|---|---|---|---|---|
| full | 0.82 ± 0.12 | 2.84 ± 1.43 | 0.00 ± 0.00 | 1.77 ± 1.09 |
| no_exposure | 0.87 ± 0.10 | 2.26 ± 0.77 | 0.00 ± 0.00 | 2.77 ± 1.48 |
| no_cover | 0.87 ± 0.10 | 2.92 ± 1.55 | 0.00 ± 0.00 | 1.93 ± 1.12 |
| no_separation | 0.86 ± 0.09 | 3.16 ± 1.44 | 0.00 ± 0.00 | 2.63 ± 1.37 |

- nominally significant: no_exposure Deaths: r=+0.88, p=0.007, p_Holm=0.082; no_cover ObjCommit: r=+0.69, p=0.034, p_Holm=0.342; no_separation AllyDist: r=+0.55, p=0.014, p_Holm=0.156

### Mission / Aggressive

| Variant | ObjCommit | AllyDist | EngRedirect | Deaths |
|---|---|---|---|---|
| full | 0.16 ± 0.11 | 3.20 ± 0.80 | 0.59 ± 0.17 | 4.80 ± 1.50 |
| no_exposure | 0.17 ± 0.12 | 3.87 ± 0.92 | 0.74 ± 0.19 | 6.30 ± 1.61 |
| no_cover | 0.15 ± 0.11 | 3.61 ± 0.90 | 0.73 ± 0.21 | 5.63 ± 1.73 |
| no_separation | 0.21 ± 0.13 | 3.70 ± 0.89 | 0.60 ± 0.19 | 5.17 ± 1.64 |

- nominally significant: none

### Mission / Survival-Aware

| Variant | ObjCommit | AllyDist | EngRedirect | Deaths |
|---|---|---|---|---|
| full | 0.08 ± 0.08 | 4.36 ± 0.87 | 0.29 ± 0.08 | 2.70 ± 0.69 |
| no_exposure | 0.06 ± 0.07 | 3.76 ± 0.72 | 0.87 ± 0.38 | 4.93 ± 1.20 |
| no_cover | 0.09 ± 0.10 | 3.59 ± 0.76 | 0.37 ± 0.16 | 2.17 ± 0.82 |
| no_separation | 0.08 ± 0.08 | 4.57 ± 0.83 | 0.29 ± 0.07 | 2.57 ± 0.79 |

- nominally significant: no_exposure EngRedirect: r=+0.70, p=0.001, p_Holm=0.015; no_exposure Deaths: r=+0.71, p=0.002, p_Holm=0.024

### Deathmatch / Mission–Cooperation

| Variant | EngRedirect | ResSeek | AllyDist | Deaths |
|---|---|---|---|---|
| full | 0.20 ± 0.11 | 0.21 ± 0.36 | 2.08 ± 0.25 | 5.63 ± 1.50 |
| no_exposure | 0.21 ± 0.09 | 0.07 ± 0.06 | 2.07 ± 0.28 | 6.77 ± 1.70 |
| no_cover | 0.17 ± 0.06 | 0.08 ± 0.07 | 1.94 ± 0.24 | 5.17 ± 1.59 |
| no_separation | 0.15 ± 0.07 | 0.02 ± 0.02 | 2.11 ± 0.28 | 4.70 ± 1.64 |

- nominally significant: none

### Deathmatch / Persistent Objective

| Variant | EngRedirect | ResSeek | AllyDist | Deaths |
|---|---|---|---|---|
| full | 0.05 ± 0.03 | 0.00 ± 0.00 | 4.59 ± 0.71 | 4.00 ± 0.81 |
| no_exposure | 0.12 ± 0.05 | 0.00 ± 0.00 | 4.04 ± 0.53 | 7.07 ± 0.99 |
| no_cover | 0.06 ± 0.03 | 0.00 ± 0.01 | 3.97 ± 0.54 | 3.80 ± 0.93 |
| no_separation | 0.06 ± 0.04 | 0.01 ± 0.01 | 5.43 ± 0.59 | 4.10 ± 0.82 |

- nominally significant: no_exposure EngRedirect: r=+0.65, p=0.007, p_Holm=0.081; no_exposure Deaths: r=+0.83, p=<0.001, p_Holm=0.001; no_separation AllyDist: r=+0.45, p=0.033, p_Holm=0.327

### Deathmatch / Aggressive

| Variant | EngRedirect | ResSeek | AllyDist | Deaths |
|---|---|---|---|---|
| full | 1.01 ± 0.15 | 0.00 ± 0.00 | 4.43 ± 0.82 | 8.37 ± 1.34 |
| no_exposure | 1.28 ± 0.18 | 0.00 ± 0.00 | 4.00 ± 0.81 | 9.87 ± 1.34 |
| no_cover | 1.03 ± 0.22 | 0.00 ± 0.00 | 3.89 ± 0.73 | 8.27 ± 1.63 |
| no_separation | 1.13 ± 0.22 | 0.00 ± 0.00 | 4.59 ± 0.87 | 8.77 ± 1.58 |

- nominally significant: no_exposure EngRedirect: r=+0.45, p=0.029, p_Holm=0.352

### Deathmatch / Survival-Aware

| Variant | EngRedirect | ResSeek | AllyDist | Deaths |
|---|---|---|---|---|
| full | 0.38 ± 0.11 | 0.45 ± 0.12 | 4.83 ± 0.91 | 3.33 ± 0.83 |
| no_exposure | 2.35 ± 2.89 | 0.77 ± 0.16 | 3.58 ± 0.65 | 6.23 ± 0.96 |
| no_cover | 0.42 ± 0.10 | 0.47 ± 0.10 | 4.67 ± 0.76 | 3.80 ± 0.80 |
| no_separation | 0.37 ± 0.12 | 0.43 ± 0.12 | 4.45 ± 0.79 | 3.37 ± 0.79 |

- nominally significant: no_exposure EngRedirect: r=+0.84, p=<0.001, p_Holm=<0.001; no_exposure ResSeek: r=+0.66, p=<0.001, p_Holm=0.010; no_exposure AllyDist: r=-0.45, p=0.031, p_Holm=0.279; no_exposure Deaths: r=+0.84, p=<0.001, p_Holm=0.001

### Control / Mission–Cooperation

| Variant | CtrlScore | ObjCommit | AllyDist | Deaths |
|---|---|---|---|---|
| full | 120.00 ± 0.00 | 0.96 ± 0.02 | 1.49 ± 0.26 | 1.40 ± 1.08 |
| no_exposure | 117.83 ± 4.43 | 0.96 ± 0.05 | 1.38 ± 0.25 | 0.63 ± 0.48 |
| no_cover | 120.00 ± 0.00 | 0.93 ± 0.04 | 1.94 ± 0.45 | 2.07 ± 1.16 |
| no_separation | 116.40 ± 5.48 | 0.97 ± 0.02 | 1.48 ± 0.27 | 1.30 ± 1.09 |

- nominally significant: none

### Control / Persistent Objective

| Variant | CtrlScore | ObjCommit | AllyDist | Deaths |
|---|---|---|---|---|
| full | 119.03 ± 1.98 | 0.88 ± 0.08 | 2.57 ± 0.85 | 1.50 ± 0.78 |
| no_exposure | 120.00 ± 0.00 | 0.91 ± 0.04 | 2.21 ± 0.56 | 2.00 ± 1.11 |
| no_cover | 120.00 ± 0.00 | 0.88 ± 0.06 | 3.02 ± 1.01 | 1.63 ± 0.82 |
| no_separation | 115.73 ± 7.68 | 0.88 ± 0.07 | 3.03 ± 1.08 | 1.53 ± 0.84 |

- nominally significant: no_separation AllyDist: r=+0.59, p=0.011, p_Holm=0.132

### Control / Aggressive

| Variant | CtrlScore | ObjCommit | AllyDist | Deaths |
|---|---|---|---|---|
| full | 36.10 ± 20.33 | 0.16 ± 0.09 | 4.33 ± 0.98 | 4.87 ± 1.35 |
| no_exposure | 39.70 ± 20.16 | 0.18 ± 0.09 | 3.71 ± 0.80 | 6.87 ± 1.51 |
| no_cover | 42.03 ± 20.18 | 0.15 ± 0.07 | 4.32 ± 0.94 | 5.80 ± 1.35 |
| no_separation | 30.43 ± 18.73 | 0.13 ± 0.07 | 3.76 ± 0.75 | 6.00 ± 1.64 |

- nominally significant: no_exposure Deaths: r=+0.48, p=0.031, p_Holm=0.377

### Control / Survival-Aware

| Variant | CtrlScore | ObjCommit | AllyDist | Deaths |
|---|---|---|---|---|
| full | 14.10 ± 13.55 | 0.04 ± 0.05 | 4.98 ± 1.20 | 2.60 ± 0.81 |
| no_exposure | 9.17 ± 9.84 | 0.01 ± 0.01 | 4.25 ± 0.73 | 4.30 ± 1.26 |
| no_cover | 12.13 ± 12.38 | 0.03 ± 0.03 | 4.32 ± 0.85 | 2.67 ± 0.77 |
| no_separation | 7.93 ± 10.89 | 0.01 ± 0.02 | 4.88 ± 0.77 | 3.53 ± 1.02 |

- nominally significant: no_exposure Deaths: r=+0.56, p=0.011, p_Holm=0.131

## External baselines (vs fixed Aggressive opponent)

| Scenario | Agent | ObjCommit | AllyDist | EngRedirect | ResSeek | Kills | Deaths | Control |
|---|---|---|---|---|---|---|---|---|
| Mission | CSO-BT | 0.57 ± 0.13 | 1.38 ± 0.28 | 3.38 ± 2.37 | 0.00 ± 0.00 | 3.5 ± 2.1 | 2.7 ± 1.5 |  |
| Mission | OW-BT | 0.95 ± 0.04 | 1.35 ± 0.22 | 0.00 ± 0.00 | 0.30 ± 0.19 | 2.9 ± 1.7 | 2.3 ± 1.4 |  |
| Mission | AC-BT | 0.00 ± 0.00 | 6.92 ± 1.61 | 0.11 ± 0.05 | 1.23 ± 0.26 | 9.7 ± 1.6 | 8.8 ± 1.8 |  |
| Mission | XO-BT | 0.00 ± 0.00 | 7.05 ± 0.63 | 0.14 ± 0.06 | 2.41 ± 0.17 | 16.5 ± 0.7 | 15.1 ± 0.9 |  |
| Mission | UtilityAI | 0.97 ± 0.02 | 1.80 ± 0.56 | 0.74 ± 0.41 | 0.00 ± 0.00 | 3.5 ± 1.9 | 3.4 ± 1.8 |  |
| Mission | Mission–Cooperation | 0.95 ± 0.03 | 1.56 ± 0.30 | 0.01 ± 0.02 | 0.00 ± 0.00 | 3.2 ± 1.7 | 3.1 ± 1.8 |  |
| Mission | Persistent Objective | 0.82 ± 0.12 | 2.84 ± 1.43 | 0.00 ± 0.00 | 0.00 ± 0.01 | 1.9 ± 1.0 | 1.8 ± 1.1 |  |
| Mission | Aggressive | 0.16 ± 0.11 | 3.20 ± 0.80 | 0.59 ± 0.17 | 0.00 ± 0.00 | 4.8 ± 1.5 | 4.8 ± 1.5 |  |
| Mission | Survival-Aware | 0.08 ± 0.08 | 4.36 ± 0.87 | 0.29 ± 0.08 | 0.33 ± 0.09 | 3.6 ± 0.9 | 2.7 ± 0.7 |  |
| Deathmatch | CSO-BT | 0.00 ± 0.00 | 2.01 ± 0.38 | 1.55 ± 0.49 | 0.00 ± 0.00 | 7.8 ± 1.8 | 7.1 ± 1.6 |  |
| Deathmatch | OW-BT | 0.00 ± 0.00 | 2.29 ± 0.19 | 1.63 ± 0.56 | 0.88 ± 0.22 | 8.2 ± 1.9 | 5.7 ± 1.3 |  |
| Deathmatch | AC-BT | 0.00 ± 0.00 | 5.20 ± 0.76 | 0.13 ± 0.05 | 1.73 ± 0.19 | 13.3 ± 1.3 | 11.6 ± 1.1 |  |
| Deathmatch | XO-BT | 0.00 ± 0.00 | 7.26 ± 0.53 | 0.17 ± 0.08 | 2.43 ± 0.16 | 17.1 ± 0.8 | 14.7 ± 0.8 |  |
| Deathmatch | UtilityAI | 0.00 ± 0.00 | 2.68 ± 0.19 | 0.90 ± 0.24 | 0.80 ± 0.29 | 7.9 ± 1.9 | 6.9 ± 1.6 |  |
| Deathmatch | Mission–Cooperation | 0.00 ± 0.00 | 2.08 ± 0.25 | 0.20 ± 0.11 | 0.21 ± 0.36 | 6.9 ± 1.8 | 5.6 ± 1.5 |  |
| Deathmatch | Persistent Objective | 0.00 ± 0.00 | 4.59 ± 0.71 | 0.05 ± 0.03 | 0.00 ± 0.00 | 7.6 ± 0.9 | 4.0 ± 0.8 |  |
| Deathmatch | Aggressive | 0.00 ± 0.00 | 4.43 ± 0.82 | 1.01 ± 0.15 | 0.00 ± 0.00 | 8.5 ± 1.5 | 8.4 ± 1.3 |  |
| Deathmatch | Survival-Aware | 0.00 ± 0.00 | 4.83 ± 0.91 | 0.38 ± 0.11 | 0.45 ± 0.12 | 4.1 ± 1.0 | 3.3 ± 0.8 |  |
| Control | CSO-BT | 0.66 ± 0.09 | 1.32 ± 0.15 | 3.14 ± 1.69 | 0.00 ± 0.00 | 1.5 ± 0.9 | 1.0 ± 0.6 | 115.37 ± 8.24; wins 28/30 |
| Control | OW-BT | 0.97 ± 0.02 | 1.67 ± 0.33 | 0.00 ± 0.00 | 0.44 ± 0.27 | 1.7 ± 1.1 | 1.4 ± 0.9 | 120.00 ± 0.00; wins 30/30 |
| Control | AC-BT | 0.00 ± 0.00 | 5.46 ± 1.16 | 0.12 ± 0.05 | 1.46 ± 0.29 | 10.5 ± 2.0 | 9.6 ± 2.1 | 0.00 ± 0.00; wins 0/30 |
| Control | XO-BT | 0.00 ± 0.00 | 7.08 ± 0.66 | 0.11 ± 0.05 | 2.41 ± 0.17 | 16.4 ± 0.7 | 15.2 ± 1.1 | 0.00 ± 0.00; wins 0/30 |
| Control | UtilityAI | 0.96 ± 0.02 | 1.92 ± 0.49 | 0.77 ± 0.44 | 0.00 ± 0.00 | 2.2 ± 1.4 | 1.8 ± 1.3 | 120.00 ± 0.00; wins 30/30 |
| Control | Mission–Cooperation | 0.96 ± 0.02 | 1.49 ± 0.26 | 0.00 ± 0.00 | 0.00 ± 0.00 | 1.5 ± 1.1 | 1.4 ± 1.1 | 120.00 ± 0.00; wins 30/30 |
| Control | Persistent Objective | 0.88 ± 0.08 | 2.57 ± 0.85 | 0.00 ± 0.01 | 0.00 ± 0.00 | 1.5 ± 0.7 | 1.5 ± 0.8 | 119.03 ± 1.98; wins 29/30 |
| Control | Aggressive | 0.16 ± 0.09 | 4.33 ± 0.98 | 0.73 ± 0.16 | 0.00 ± 0.00 | 4.9 ± 1.6 | 4.9 ± 1.4 | 36.10 ± 20.33; wins 8/30 |
| Control | Survival-Aware | 0.04 ± 0.05 | 4.98 ± 1.20 | 0.31 ± 0.11 | 0.36 ± 0.10 | 3.5 ± 0.9 | 2.6 ± 0.8 | 14.10 ± 13.55; wins 2/30 |

## Behaviour trees vs corresponding priority-structure styles (Mann-Whitney; r > 0: BT higher)

| Scenario | Pair | Metric | BT | Style | r | p |
|---|---|---|---|---|---|---|
| Mission | CSO-BT / Mission–Cooperation | ObjCommit | 0.57 ± 0.13 | 0.95 ± 0.03 | -0.75 | <0.001 |
| Mission | CSO-BT / Mission–Cooperation | AllyDist | 1.38 ± 0.28 | 1.56 ± 0.30 | -0.20 | 0.196 |
| Mission | CSO-BT / Mission–Cooperation | EngRedirect | 3.38 ± 2.37 | 0.01 ± 0.02 | +0.74 | <0.001 |
| Mission | CSO-BT / Mission–Cooperation | Deaths | 2.70 ± 1.54 | 3.07 ± 1.77 | -0.02 | 0.907 |
| Mission | OW-BT / Persistent Objective | ObjCommit | 0.95 ± 0.04 | 0.82 ± 0.12 | +0.49 | <0.001 |
| Mission | OW-BT / Persistent Objective | AllyDist | 1.35 ± 0.22 | 2.84 ± 1.43 | -0.17 | 0.254 |
| Mission | OW-BT / Persistent Objective | EngRedirect | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 1.000 |
| Mission | OW-BT / Persistent Objective | Deaths | 2.30 ± 1.44 | 1.77 ± 1.09 | +0.01 | 0.960 |
| Mission | AC-BT / Aggressive | ObjCommit | 0.00 ± 0.00 | 0.16 ± 0.11 | -0.43 | <0.001 |
| Mission | AC-BT / Aggressive | AllyDist | 6.92 ± 1.61 | 3.20 ± 0.80 | +0.48 | 0.001 |
| Mission | AC-BT / Aggressive | EngRedirect | 0.11 ± 0.05 | 0.59 ± 0.17 | -0.70 | <0.001 |
| Mission | AC-BT / Aggressive | Deaths | 8.77 ± 1.82 | 4.80 ± 1.50 | +0.47 | 0.002 |
| Mission | XO-BT / Survival-Aware | ObjCommit | 0.00 ± 0.00 | 0.08 ± 0.08 | -0.30 | 0.001 |
| Mission | XO-BT / Survival-Aware | AllyDist | 7.05 ± 0.63 | 4.36 ± 0.87 | +0.65 | <0.001 |
| Mission | XO-BT / Survival-Aware | EngRedirect | 0.14 ± 0.06 | 0.29 ± 0.08 | -0.40 | 0.007 |
| Mission | XO-BT / Survival-Aware | Deaths | 15.07 ± 0.89 | 2.70 ± 0.69 | +1.00 | <0.001 |
| Deathmatch | CSO-BT / Mission–Cooperation | EngRedirect | 1.55 ± 0.49 | 0.20 ± 0.11 | +0.82 | <0.001 |
| Deathmatch | CSO-BT / Mission–Cooperation | ResSeek | 0.00 ± 0.00 | 0.21 ± 0.36 | -0.27 | 0.003 |
| Deathmatch | CSO-BT / Mission–Cooperation | AllyDist | 2.01 ± 0.38 | 2.08 ± 0.25 | -0.16 | 0.277 |
| Deathmatch | CSO-BT / Mission–Cooperation | Deaths | 7.10 ± 1.65 | 5.63 ± 1.50 | +0.20 | 0.181 |
| Deathmatch | OW-BT / Persistent Objective | EngRedirect | 1.63 ± 0.56 | 0.05 ± 0.03 | +0.82 | <0.001 |
| Deathmatch | OW-BT / Persistent Objective | ResSeek | 0.88 ± 0.22 | 0.00 ± 0.00 | +0.87 | <0.001 |
| Deathmatch | OW-BT / Persistent Objective | AllyDist | 2.29 ± 0.19 | 4.59 ± 0.71 | -0.82 | <0.001 |
| Deathmatch | OW-BT / Persistent Objective | Deaths | 5.70 ± 1.35 | 4.00 ± 0.81 | +0.31 | 0.039 |
| Deathmatch | AC-BT / Aggressive | EngRedirect | 0.13 ± 0.05 | 1.01 ± 0.15 | -0.98 | <0.001 |
| Deathmatch | AC-BT / Aggressive | ResSeek | 1.73 ± 0.19 | 0.00 ± 0.00 | +1.00 | <0.001 |
| Deathmatch | AC-BT / Aggressive | AllyDist | 5.20 ± 0.76 | 4.43 ± 0.82 | +0.24 | 0.109 |
| Deathmatch | AC-BT / Aggressive | Deaths | 11.63 ± 1.09 | 8.37 ± 1.34 | +0.57 | <0.001 |
| Deathmatch | XO-BT / Survival-Aware | EngRedirect | 0.17 ± 0.08 | 0.38 ± 0.11 | -0.43 | 0.004 |
| Deathmatch | XO-BT / Survival-Aware | ResSeek | 2.43 ± 0.16 | 0.45 ± 0.12 | +1.00 | <0.001 |
| Deathmatch | XO-BT / Survival-Aware | AllyDist | 7.26 ± 0.53 | 4.83 ± 0.91 | +0.65 | <0.001 |
| Deathmatch | XO-BT / Survival-Aware | Deaths | 14.73 ± 0.80 | 3.33 ± 0.83 | +1.00 | <0.001 |
| Control | CSO-BT / Mission–Cooperation | CtrlScore | 115.37 ± 8.24 | 120.00 ± 0.00 | -0.07 | 0.161 |
| Control | CSO-BT / Mission–Cooperation | ObjCommit | 0.66 ± 0.09 | 0.96 ± 0.02 | -0.85 | <0.001 |
| Control | CSO-BT / Mission–Cooperation | AllyDist | 1.32 ± 0.15 | 1.49 ± 0.26 | -0.21 | 0.171 |
| Control | CSO-BT / Mission–Cooperation | Deaths | 1.03 ± 0.61 | 1.40 ± 1.08 | +0.06 | 0.654 |
| Control | OW-BT / Persistent Objective | CtrlScore | 120.00 ± 0.00 | 119.03 ± 1.98 | +0.03 | 0.334 |
| Control | OW-BT / Persistent Objective | ObjCommit | 0.97 ± 0.02 | 0.88 ± 0.08 | +0.52 | <0.001 |
| Control | OW-BT / Persistent Objective | AllyDist | 1.67 ± 0.33 | 2.57 ± 0.85 | -0.05 | 0.747 |
| Control | OW-BT / Persistent Objective | Deaths | 1.43 ± 0.92 | 1.50 ± 0.78 | -0.05 | 0.719 |
| Control | AC-BT / Aggressive | CtrlScore | 0.00 ± 0.00 | 36.10 ± 20.33 | -0.37 | <0.001 |
| Control | AC-BT / Aggressive | ObjCommit | 0.00 ± 0.00 | 0.16 ± 0.09 | -0.53 | <0.001 |
| Control | AC-BT / Aggressive | AllyDist | 5.46 ± 1.16 | 4.33 ± 0.98 | +0.20 | 0.181 |
| Control | AC-BT / Aggressive | Deaths | 9.60 ± 2.05 | 4.87 ± 1.35 | +0.49 | 0.001 |
| Control | XO-BT / Survival-Aware | CtrlScore | 0.00 ± 0.00 | 14.10 ± 13.55 | -0.23 | 0.006 |
| Control | XO-BT / Survival-Aware | ObjCommit | 0.00 ± 0.00 | 0.04 ± 0.05 | -0.23 | 0.006 |
| Control | XO-BT / Survival-Aware | AllyDist | 7.08 ± 0.66 | 4.98 ± 1.20 | +0.50 | <0.001 |
| Control | XO-BT / Survival-Aware | Deaths | 15.23 ± 1.12 | 2.60 ± 0.81 | +1.00 | <0.001 |

## Fingerprint matching (nearest priority-structure style, normalised 4-metric space)

| Baseline | Mission | Deathmatch | Control | pooled (12-D) |
|---|---|---|---|---|
| CSO-BT | Aggressive (0.97) | Mission–Cooperation (0.41) | Persistent Objective (0.98) | Aggressive (1.47) |
| OW-BT | Mission–Cooperation (0.13) | Mission–Cooperation (0.51) | Mission–Cooperation (0.18) | Mission–Cooperation (0.55) |
| AC-BT | Survival-Aware (0.58) | Survival-Aware (0.54) | Survival-Aware (0.47) | Survival-Aware (0.92) |
| XO-BT | Survival-Aware (0.97) | Survival-Aware (0.92) | Survival-Aware (0.92) | Survival-Aware (1.62) |
| UtilityAI | Mission–Cooperation (0.22) | Mission–Cooperation (0.33) | Mission–Cooperation (0.24) | Mission–Cooperation (0.47) |
