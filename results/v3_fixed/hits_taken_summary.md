# Hits taken: independent outcome for H3 (rerun with the hits-taken counter, n = 100)

## random map

- Reproduction check, main experiment: 1200 of 1200 rows matched; all shared columns identical
- Reproduction check, cost-term ablation: 4800 of 4800 rows matched; all shared columns identical

### Main experiment: hits taken per alive step (mean) and agreement with walked expected hits

| Scenario | Style | hits taken / step | walked expected hits / step | Spearman rho (episodes) |
|---|---|---|---|---|
| Mission | Mission–Cooperation | 0.0239 | 0.0393 | +0.97 |
| Mission | Persistent Objective | 0.0251 | 0.0394 | +0.97 |
| Mission | Aggressive | 0.0340 | 0.0430 | +0.96 |
| Mission | Survival-Aware | 0.0154 | 0.0191 | +0.95 |
| Deathmatch | Mission–Cooperation | 0.0533 | 0.0714 | +0.85 |
| Deathmatch | Persistent Objective | 0.0445 | 0.0568 | +0.89 |
| Deathmatch | Aggressive | 0.0735 | 0.0922 | +0.87 |
| Deathmatch | Survival-Aware | 0.0246 | 0.0311 | +0.94 |
| Control | Mission–Cooperation | 0.0213 | 0.0378 | +0.96 |
| Control | Persistent Objective | 0.0265 | 0.0418 | +0.94 |
| Control | Aggressive | 0.0438 | 0.0553 | +0.94 |
| Control | Survival-Aware | 0.0197 | 0.0241 | +0.89 |

Pooled over all 1200 episodes: Spearman rho = +0.95

### H3 with hits taken (cost-term ablation, configured lambda_E vs 0)

| Scenario | Style | full | no exposure | change | r | p | p_Holm (DM, 4 styles) |
|---|---|---|---|---|---|---|---|
| Mission | Mission–Cooperation | 0.0239 | 0.0252 | -5% | -0.20 | 0.177 |  |
| Mission | Persistent Objective | 0.0251 | 0.0275 | -9% | -0.28 | 0.057 |  |
| Mission | Aggressive | 0.0340 | 0.0389 | -13% | -0.29 | 0.017 |  |
| Mission | Survival-Aware | 0.0154 | 0.0187 | -18% | -0.32 | 0.008 |  |
| Deathmatch | Mission–Cooperation | 0.0533 | 0.0564 | -5% | -0.22 | 0.058 | 0.115 |
| Deathmatch | Persistent Objective | 0.0445 | 0.0598 | -26% | -0.82 | <0.001 | <0.001 |
| Deathmatch | Aggressive | 0.0735 | 0.0815 | -10% | -0.49 | <0.001 | <0.001 |
| Deathmatch | Survival-Aware | 0.0246 | 0.0260 | -5% | -0.13 | 0.274 | 0.274 |
| Control | Mission–Cooperation | 0.0213 | 0.0230 | -7% | -0.36 | 0.083 |  |
| Control | Persistent Objective | 0.0265 | 0.0266 | -0% | +0.07 | 0.709 |  |
| Control | Aggressive | 0.0438 | 0.0448 | -2% | -0.14 | 0.245 |  |
| Control | Survival-Aware | 0.0197 | 0.0239 | -17% | -0.31 | 0.008 |  |

Sign test: hits taken lower with the exposure term in 12 of 12 conditions (one-sided binomial p = <0.001)

## urban map

- Reproduction check, main experiment: 1200 of 1200 rows matched; all shared columns identical
- Reproduction check, cost-term ablation: 4800 of 4800 rows matched; all shared columns identical

### Main experiment: hits taken per alive step (mean) and agreement with walked expected hits

| Scenario | Style | hits taken / step | walked expected hits / step | Spearman rho (episodes) |
|---|---|---|---|---|
| Mission | Mission–Cooperation | 0.0210 | 0.0309 | +0.99 |
| Mission | Persistent Objective | 0.0263 | 0.0369 | +0.99 |
| Mission | Aggressive | 0.0404 | 0.0512 | +0.97 |
| Mission | Survival-Aware | 0.0160 | 0.0205 | +0.95 |
| Deathmatch | Mission–Cooperation | 0.0530 | 0.0742 | +0.88 |
| Deathmatch | Persistent Objective | 0.0416 | 0.0527 | +0.87 |
| Deathmatch | Aggressive | 0.0699 | 0.0884 | +0.89 |
| Deathmatch | Survival-Aware | 0.0256 | 0.0321 | +0.91 |
| Control | Mission–Cooperation | 0.0210 | 0.0331 | +0.98 |
| Control | Persistent Objective | 0.0227 | 0.0350 | +0.98 |
| Control | Aggressive | 0.0485 | 0.0621 | +0.94 |
| Control | Survival-Aware | 0.0195 | 0.0244 | +0.87 |

Pooled over all 1200 episodes: Spearman rho = +0.97

### H3 with hits taken (cost-term ablation, configured lambda_E vs 0)

| Scenario | Style | full | no exposure | change | r | p | p_Holm (DM, 4 styles) |
|---|---|---|---|---|---|---|---|
| Mission | Mission–Cooperation | 0.0210 | 0.0251 | -16% | -0.44 | 0.005 |  |
| Mission | Persistent Objective | 0.0263 | 0.0299 | -12% | -0.26 | 0.067 |  |
| Mission | Aggressive | 0.0404 | 0.0459 | -12% | -0.29 | 0.016 |  |
| Mission | Survival-Aware | 0.0160 | 0.0201 | -21% | -0.29 | 0.012 |  |
| Deathmatch | Mission–Cooperation | 0.0530 | 0.0564 | -6% | -0.20 | 0.087 | 0.175 |
| Deathmatch | Persistent Objective | 0.0416 | 0.0616 | -32% | -0.93 | <0.001 | <0.001 |
| Deathmatch | Aggressive | 0.0699 | 0.0788 | -11% | -0.47 | <0.001 | <0.001 |
| Deathmatch | Survival-Aware | 0.0256 | 0.0290 | -12% | -0.20 | 0.093 | 0.175 |
| Control | Mission–Cooperation | 0.0210 | 0.0232 | -10% | -0.38 | 0.069 |  |
| Control | Persistent Objective | 0.0227 | 0.0247 | -8% | -0.30 | 0.139 |  |
| Control | Aggressive | 0.0485 | 0.0494 | -2% | -0.04 | 0.747 |  |
| Control | Survival-Aware | 0.0195 | 0.0252 | -23% | -0.44 | <0.001 |  |

Sign test: hits taken lower with the exposure term in 12 of 12 conditions (one-sided binomial p = <0.001)

