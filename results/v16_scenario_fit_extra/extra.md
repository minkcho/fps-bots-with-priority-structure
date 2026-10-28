# Round I (v16), exploratory supplement: denominators, noise floor, classifier, outcomes (stored test episodes; not part of the frozen protocol)

## CSO-BT in Mission

- D2(fit, tree) 0.65; nearest designed style Aggressive [route off] at D2 5.46 (G 0.35); all styles: Aggressive [route off] 5.46, Aggressive 7.30, Mission–Cooperation 21.99, Persistent Objective [route off] 22.25, Persistent Objective 22.25, Mission–Cooperation [route off] 22.35, Survival-Aware [route off] 53.09, Survival-Aware 55.82
- noise floor: fit 0.857 vs tree 95th percentile 0.419 -> outside
- classifier AUC 0.967 (CI 0.948-0.983, permutation p 0.0010)
- Cohen's d (fit - tree): kills +0.24, deaths +0.44, hits_taken_per_step +0.56; means fit / tree: kills 15.385 / 14.755, deaths 15.245 / 14.020, hits_taken_per_step 0.087 / 0.076

## CSO-BT in Control

- D2(fit, tree) 0.59; nearest designed style Aggressive [route off] at D2 4.40 (G 0.37); all styles: Aggressive [route off] 4.40, Aggressive 5.60, Mission–Cooperation 13.00, Persistent Objective 13.24, Mission–Cooperation [route off] 13.34, Persistent Objective [route off] 13.39, Survival-Aware [route off] 35.08, Survival-Aware 38.38
- noise floor: fit 0.812 vs tree 95th percentile 0.376 -> outside
- classifier AUC 0.947 (CI 0.921-0.969, permutation p 0.0010)
- Cohen's d (fit - tree): kills +0.05, deaths +0.19, hits_taken_per_step +0.52, win +0.23; means fit / tree: kills 9.585 / 9.450, deaths 9.420 / 8.695, hits_taken_per_step 0.085 / 0.074, win 0.745 / 0.640

## OW-BT in Mission

- D2(fit, tree) 1.31; nearest designed style Mission–Cooperation [route off] at D2 12.40 (G 0.32); all styles: Mission–Cooperation [route off] 12.40, Mission–Cooperation 12.58, Persistent Objective [route off] 12.62, Persistent Objective 12.75, Aggressive [route off] 32.20, Aggressive 33.07, Survival-Aware [route off] 51.27, Survival-Aware 53.35
- noise floor: fit 1.177 vs tree 95th percentile 0.391 -> outside
- classifier AUC 0.971 (CI 0.955-0.985, permutation p 0.0010)
- Cohen's d (fit - tree): kills -0.06, deaths +0.08, hits_taken_per_step +0.15; means fit / tree: kills 16.410 / 16.580, deaths 12.195 / 11.930, hits_taken_per_step 0.077 / 0.074

## OW-BT in Control

- D2(fit, tree) 0.57; nearest designed style Mission–Cooperation [route off] at D2 10.04 (G 0.24); all styles: Mission–Cooperation [route off] 10.04, Mission–Cooperation 10.12, Persistent Objective [route off] 10.15, Persistent Objective 10.22, Aggressive [route off] 24.72, Aggressive 25.89, Survival-Aware [route off] 33.66, Survival-Aware 37.37
- noise floor: fit 0.811 vs tree 95th percentile 0.387 -> outside
- classifier AUC 0.869 (CI 0.834-0.901, permutation p 0.0010)
- Cohen's d (fit - tree): kills -0.11, deaths +0.13, hits_taken_per_step +0.28, win +0.00; means fit / tree: kills 6.835 / 7.055, deaths 4.685 / 4.340, hits_taken_per_step 0.073 / 0.066, win 0.935 / 0.935

## AC-BT in Deathmatch

- D2(fit, tree) 5.63; nearest designed style Aggressive at D2 6.42 (G 0.94); all styles: Aggressive 6.42, Aggressive [route off] 7.86, Mission–Cooperation 13.12, Mission–Cooperation [route off] 14.92, Survival-Aware [route off] 16.81, Survival-Aware 18.04, Persistent Objective [route off] 19.32, Persistent Objective 20.44
- noise floor: fit 2.388 vs tree 95th percentile 0.312 -> outside
- classifier AUC 1.000 (CI 1.000-1.000, permutation p 0.0010)
- Cohen's d (fit - tree): kills +0.48, deaths -0.21, hits_taken_per_step -0.11; means fit / tree: kills 13.920 / 12.380, deaths 14.515 / 15.210, hits_taken_per_step 0.091 / 0.094
- active weights (Deathmatch has no objective candidate): w_engage 0.428, w_resource 0.407, w_team 0.165, w_commitment 0.335, sum_of_active_weights 0.922

## XO-BT in Deathmatch

- D2(fit, tree) 1.86; nearest designed style Aggressive at D2 24.51 (G 0.28); all styles: Aggressive 24.51, Mission–Cooperation 25.54, Aggressive [route off] 26.38, Mission–Cooperation [route off] 27.64, Survival-Aware [route off] 29.88, Survival-Aware 30.83, Persistent Objective 32.16, Persistent Objective [route off] 32.36
- noise floor: fit 1.409 vs tree 95th percentile 0.441 -> outside
- classifier AUC 0.987 (CI 0.977-0.994, permutation p 0.0010)
- Cohen's d (fit - tree): kills -0.30, deaths +0.60, hits_taken_per_step +0.15; means fit / tree: kills 15.395 / 16.280, deaths 17.095 / 15.075, hits_taken_per_step 0.112 / 0.108
- active weights (Deathmatch has no objective candidate): w_engage 0.932, w_resource 0.067, w_team 0.001, w_commitment 0.045, sum_of_active_weights 0.478

