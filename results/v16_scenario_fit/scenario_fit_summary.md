# Round I (v16): per-scenario fits, graded per game-scenario case (test seeds; native scenarios only)

## CSO-BT in Mission (41 dimensions on the game maps; trees of the family: CSO-BT, OW-BT): improved

- setting: w_Obj 0.770, w_Eng 0.014, w_Res 0.031, w_Team 0.185, w_commit 0.085, g0 0.124, tau 19.546, eta 0.425, rho 0.954, mode 2 (chase)
- D2 (game maps): CSO-BT 0.65, OW-BT 31.94; nearest CSO-BT; own tree nearest in 100% of resamples; G 0.35 [0.32, 0.39]
- held-out maps: own tree nearest on 5/5 (with G < 0.5 on 2/5): random CSO-BT (G 0.21); urban CSO-BT (G 0.90); random_s101 CSO-BT (G 0.59); urban_s101 CSO-BT (G 0.70); blocks CSO-BT (G 0.45)
- contributions to D2(fit, own tree): contact_distance 0.29, engagement_redirection_rate_per_100 0.13, objective_commitment_ratio 0.09, death_rate_per_100 0.04, kill_rate_per_100 0.03, avg_ally_proximity 0.03, los_frac 0.03, resource_seeking_rate_per_100 0.02, far_pursuit_share 0.00, resource_goal_share_good 0.00, retreat_share 0.00
- search: stage-1b selection J by mode 2 (chase) 0.76, 0 (hold) 4.35, 1 (keep moving) 7.71, 3 (evade) 42.69; searched [2, 0]; fitted mode 2 (chase), first-ranked: yes; validation J 0.572 (train 0.465; best per searched mode 2 0.572, 0 3.547)

## CSO-BT in Control (41 dimensions on the game maps; trees of the family: CSO-BT, OW-BT): improved

- setting: w_Obj 0.661, w_Eng 0.210, w_Res 0.007, w_Team 0.122, w_commit 0.034, g0 0.391, tau 39.049, eta 0.208, rho 0.563, mode 2 (chase)
- D2 (game maps): CSO-BT 0.59, OW-BT 21.18; nearest CSO-BT; own tree nearest in 100% of resamples; G 0.37 [0.33, 0.43]
- held-out maps: own tree nearest on 5/5 (with G < 0.5 on 3/5): random CSO-BT (G 0.34); urban CSO-BT (G 0.69); random_s101 CSO-BT (G 0.26); urban_s101 CSO-BT (G 0.50); blocks CSO-BT (G 0.55)
- contributions to D2(fit, own tree): objective_commitment_ratio 0.21, contact_distance 0.15, engagement_redirection_rate_per_100 0.13, los_frac 0.03, death_rate_per_100 0.03, avg_ally_proximity 0.02, kill_rate_per_100 0.02, far_pursuit_share 0.00, resource_seeking_rate_per_100 0.00, resource_goal_share_good 0.00, retreat_share 0.00
- search: stage-1b selection J by mode 2 (chase) 0.35, 0 (hold) 2.47, 1 (keep moving) 3.85, 3 (evade) 27.11; searched [2, 0]; fitted mode 2 (chase), first-ranked: yes; validation J 0.445 (train 0.303; best per searched mode 2 0.445, 0 1.961)

## OW-BT in Mission (41 dimensions on the game maps; trees of the family: CSO-BT, OW-BT): close

- setting: w_Obj 0.290, w_Eng 0.038, w_Res 0.617, w_Team 0.054, w_commit 0.025, g0 0.025, tau 85.682, eta 0.052, rho 0.353, mode 1 (keep moving)
- D2 (game maps): CSO-BT 39.22, OW-BT 1.31; nearest OW-BT; own tree nearest in 100% of resamples; G 0.32 [0.29, 0.37]
- held-out maps: own tree nearest on 5/5 (with G < 0.5 on 4/5): random OW-BT (G 0.22); urban OW-BT (G 0.43); random_s101 OW-BT (G 0.49); urban_s101 OW-BT (G 0.59); blocks OW-BT (G 0.39)
- contributions to D2(fit, own tree): retreat_share 0.86, objective_commitment_ratio 0.36, resource_goal_share_good 0.04, avg_ally_proximity 0.03, resource_seeking_rate_per_100 0.02, contact_distance 0.01, death_rate_per_100 0.00, engagement_redirection_rate_per_100 0.00, far_pursuit_share 0.00, kill_rate_per_100 -0.00, los_frac -0.00
- search: stage-1b selection J by mode 1 (keep moving) 1.04, 0 (hold) 1.78, 2 (chase) 22.61, 3 (evade) 33.26; searched [1, 0]; fitted mode 1 (keep moving), first-ranked: yes; validation J 0.856 (train 1.425; best per searched mode 1 0.856, 0 1.708)

## OW-BT in Control (41 dimensions on the game maps; trees of the family: CSO-BT, OW-BT): close

- setting: w_Obj 0.290, w_Eng 0.038, w_Res 0.617, w_Team 0.054, w_commit 0.025, g0 0.025, tau 85.682, eta 0.052, rho 0.353, mode 1 (keep moving)
- D2 (game maps): CSO-BT 25.42, OW-BT 0.57; nearest OW-BT; own tree nearest in 100% of resamples; G 0.24 [0.21, 0.28]
- held-out maps: own tree nearest on 5/5 (with G < 0.5 on 4/5): random OW-BT (G 0.17); urban OW-BT (G 0.38); random_s101 OW-BT (G 0.39); urban_s101 OW-BT (G 0.69); blocks OW-BT (G 0.23)
- contributions to D2(fit, own tree): objective_commitment_ratio 0.28, retreat_share 0.17, resource_goal_share_good 0.06, avg_ally_proximity 0.03, resource_seeking_rate_per_100 0.02, death_rate_per_100 0.01, contact_distance 0.00, engagement_redirection_rate_per_100 0.00, far_pursuit_share 0.00, kill_rate_per_100 -0.00, los_frac -0.00
- search: stage-1b selection J by mode 1 (keep moving) 0.51, 0 (hold) 0.70, 2 (chase) 16.10, 3 (evade) 17.99; searched [1, 0]; fitted mode 1 (keep moving), first-ranked: yes; validation J 0.535 (train 0.224; best per searched mode 1 0.535, 0 0.649)

## AC-BT in Deathmatch (37 dimensions on the game maps; trees of the family: AC-BT, XO-BT): improved

- setting: w_Obj 0.078, w_Eng 0.394, w_Res 0.375, w_Team 0.152, w_commit 0.309, g0 0.010, tau 41.580, eta 0.203, rho 0.799, mode 2 (chase)
- D2 (game maps): AC-BT 5.63, XO-BT 8.94; nearest AC-BT; own tree nearest in 100% of resamples; G 0.94 [0.91, 0.96]
- held-out maps: own tree nearest on 5/5 (with G < 0.5 on 0/5): random AC-BT (G 1.03); urban AC-BT (G 0.89); random_s101 AC-BT (G 0.93); urban_s101 AC-BT (G 0.86); blocks AC-BT (G 0.78)
- contributions to D2(fit, own tree): far_pursuit_share 3.44, avg_ally_proximity 1.14, resource_goal_share_good 0.69, engagement_redirection_rate_per_100 0.18, los_frac 0.06, kill_rate_per_100 0.06, death_rate_per_100 0.05, contact_distance 0.01, resource_seeking_rate_per_100 0.00, retreat_share 0.00
- search: stage-1b selection J by mode 2 (chase) 6.29, 1 (keep moving) 7.32, 0 (hold) 7.51, 3 (evade) 14.47; searched [2, 1]; fitted mode 2 (chase), first-ranked: yes; validation J 5.298 (train 5.639; best per searched mode 2 5.298, 1 6.825)

## XO-BT in Deathmatch (37 dimensions on the game maps; trees of the family: AC-BT, XO-BT): close

- setting: w_Obj 0.522, w_Eng 0.446, w_Res 0.032, w_Team 0.000, w_commit 0.022, g0 0.150, tau 43.598, eta 0.918, rho 0.572, mode 2 (chase)
- D2 (game maps): AC-BT 17.75, XO-BT 1.86; nearest XO-BT; own tree nearest in 100% of resamples; G 0.28 [0.26, 0.30]
- held-out maps: own tree nearest on 5/5 (with G < 0.5 on 5/5): random XO-BT (G 0.27); urban XO-BT (G 0.30); random_s101 XO-BT (G 0.27); urban_s101 XO-BT (G 0.27); blocks XO-BT (G 0.31)
- contributions to D2(fit, own tree): retreat_share 1.00, death_rate_per_100 0.20, avg_ally_proximity 0.19, far_pursuit_share 0.17, resource_seeking_rate_per_100 0.16, resource_goal_share_good 0.06, los_frac 0.04, engagement_redirection_rate_per_100 0.02, contact_distance 0.01, kill_rate_per_100 0.01
- search: stage-1b selection J by mode 0 (hold) 1.32, 2 (chase) 1.54, 1 (keep moving) 2.35, 3 (evade) 20.47; searched [0, 2]; fitted mode 2 (chase), first-ranked: no; validation J 1.373 (train 1.220; best per searched mode 0 1.418, 2 1.373)

## Behaviour (means over the game maps and episodes, per scenario)

| agent | scenario | retreat_share | far_pursuit_share | resource_goal_share_good | contact_distance |
|---|---|---|---|---|---|
| CSO-BT | Mission | 0.00 | 0.00 | 0.00 | 3.28 |
| CSO-BT | Control | 0.00 | 0.00 | 0.00 | 3.25 |
| OW-BT | Mission | 0.53 | 0.00 | 0.00 | 3.14 |
| OW-BT | Control | 0.64 | 0.00 | 0.00 | 3.21 |
| AC-BT | Deathmatch | 0.00 | 0.01 | 0.14 | 3.03 |
| XO-BT | Deathmatch | 0.31 | 0.56 | 0.18 | 3.14 |
| fitsc[CSO-BT:Mission] | Mission | 0.00 | 0.00 | 0.00 | 2.75 |
| fitsc[CSO-BT:Control] | Control | 0.00 | 0.00 | 0.00 | 2.86 |
| fitsc[OW-BT:Mission] | Mission | 0.75 | 0.00 | 0.02 | 3.03 |
| fitsc[OW-BT:Control] | Control | 0.75 | 0.00 | 0.02 | 3.06 |
| fitsc[AC-BT:Deathmatch] | Deathmatch | 0.00 | 0.23 | 0.29 | 3.10 |
| fitsc[XO-BT:Deathmatch] | Deathmatch | 0.00 | 0.54 | 0.17 | 3.01 |

## Headline

- case fits at least 'improved': 6/6; 'close': 3/6
- tiers: CSO-BT|Mission improved, CSO-BT|Control improved, OW-BT|Mission close, OW-BT|Control close, AC-BT|Deathmatch improved, XO-BT|Deathmatch close
- G: CSO-BT|Mission 0.35 [0.32, 0.39], CSO-BT|Control 0.37 [0.33, 0.43], OW-BT|Mission 0.32 [0.29, 0.37], OW-BT|Control 0.24 [0.21, 0.28], AC-BT|Deathmatch 0.94 [0.91, 0.96], XO-BT|Deathmatch 0.28 [0.26, 0.30]
- fitted mode first-ranked in stage 1b: CSO-BT|Mission yes, CSO-BT|Control yes, OW-BT|Mission yes, OW-BT|Control yes, AC-BT|Deathmatch yes, XO-BT|Deathmatch no

## Predictions of the plan

- P1: every case fit identifies its own tree (own tree nearest in >= 95% of resamples and on >= 4 of 5 held-out maps): met
- H-I1: case fits at least 'improved' in >= 4 of the 6 cases: met
- H-I2: case fits 'close' in >= 3 of the 6 cases: met

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

