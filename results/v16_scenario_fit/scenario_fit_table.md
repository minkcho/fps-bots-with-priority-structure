## Per case: fitted setting and grade

| Case | w_Obj | w_Eng | w_Res | w_Team | w_commit | g0 | tau | eta | rho | Mode | Nearest | G [95% CI] | Held-out | Tier |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CSO-BT : Mission | 0.77 | 0.01 | 0.03 | 0.18 | 0.08 | 0.12 | 20 | 0.43 | 0.95 | chase | CSO-BT | 0.35 [0.32, 0.39] | 5/5 (2) | improved |
| CSO-BT : Control | 0.66 | 0.21 | 0.01 | 0.12 | 0.03 | 0.39 | 39 | 0.21 | 0.56 | chase | CSO-BT | 0.37 [0.33, 0.43] | 5/5 (3) | improved |
| OW-BT : Mission | 0.29 | 0.04 | 0.62 | 0.05 | 0.03 | 0.03 | 86 | 0.05 | 0.35 | keep moving | OW-BT | 0.32 [0.29, 0.37] | 5/5 (4) | close |
| OW-BT : Control | 0.29 | 0.04 | 0.62 | 0.05 | 0.03 | 0.03 | 86 | 0.05 | 0.35 | keep moving | OW-BT | 0.24 [0.21, 0.28] | 5/5 (4) | close |
| AC-BT : Deathmatch | 0.08 | 0.39 | 0.38 | 0.15 | 0.31 | 0.01 | 42 | 0.20 | 0.80 | chase | AC-BT | 0.94 [0.91, 0.96] | 5/5 (0) | improved |
| XO-BT : Deathmatch | 0.52 | 0.45 | 0.03 | 0.00 | 0.02 | 0.15 | 44 | 0.92 | 0.57 | chase | XO-BT | 0.28 [0.26, 0.30] | 5/5 (5) | close |

Columns: goal weights (sum 1), w_commit = kappa (relative to the goal-weight sum), the four optional parameters, mode; nearest tree of the family; G with the 95% CI; held-out maps with the own tree nearest (and G < 0.5); tier.
