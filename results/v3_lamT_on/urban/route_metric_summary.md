# Route metric: statistical summary (urban map)

Consistency checks (CRN): exp x36.36363636363636 = main experiment; at x0 the additive, centred, exp, and exp_geo variants coincide (distance-only) and equal the lambda-scale sweep; exp_geo_replan x0 = additive_replan x0. **passed**


## Route diagnostics, all styles (pooled over plans; detour = planned path longer than the shortest)

| variant | k | plans | detour | differs | len_ratio | exp_ratio |
|---|---|---|---|---|---|---|
| additive | x0 | 183679 | 0.00% | 0.0% | 1.000 | 1.000 |
| additive | x1 | 183113 | 0.02% | 18.1% | 1.000 | 0.929 |
| additive | x3 | 183470 | 0.08% | 18.4% | 1.001 | 0.926 |
| additive | x10 | 182463 | 0.20% | 18.5% | 1.002 | 0.920 |
| centred | x0 | 183679 | 0.00% | 0.0% | 1.000 | 1.000 |
| centred | x1 | 182908 | 0.05% | 18.1% | 1.000 | 0.927 |
| centred | x3 | 182131 | 0.31% | 18.7% | 1.003 | 0.920 |
| centred | x10 | 181012 | 2.32% | 17.8% | 1.026 | 0.903 |
| exp | x0 | 183679 | 0.00% | 0.0% | 1.000 | 1.000 |
| exp | x1 | 184202 | 0.07% | 17.7% | 1.001 | 0.917 |
| exp | x3 | 185925 | 0.53% | 17.7% | 1.006 | 0.897 |
| exp | x10 | 180054 | 4.78% | 19.1% | 1.089 | 0.873 |
| exp_geo | x0 | 183679 | 0.00% | 0.0% | 1.000 | 1.000 |
| exp_geo | x1 | 185566 | 0.06% | 16.3% | 1.000 | 0.925 |
| exp_geo | x3 | 183125 | 0.71% | 17.2% | 1.008 | 0.914 |
| exp_geo | x10 | 181013 | 3.92% | 19.5% | 1.048 | 0.909 |
| exp_geo_replan | x0 | 195009 | 0.00% | 0.0% | 1.000 | 1.000 |
| exp_geo_replan | x1 | 199303 | 0.06% | 17.6% | 1.000 | 0.925 |
| exp_geo_replan | x3 | 197466 | 0.46% | 18.2% | 1.004 | 0.909 |
| exp_geo_replan | x10 | 195367 | 4.01% | 21.5% | 1.043 | 0.894 |
| additive_replan | x0 | 195009 | 0.00% | 0.0% | 1.000 | 1.000 |
| additive_replan | x1 | 195799 | 0.02% | 17.9% | 1.000 | 0.924 |
| additive_replan | x3 | 195701 | 0.09% | 18.3% | 1.001 | 0.918 |
| additive_replan | x10 | 194724 | 0.21% | 18.8% | 1.002 | 0.911 |

## Route diagnostics, Survival-Aware (pooled over plans; detour = planned path longer than the shortest)

| variant | k | plans | detour | differs | len_ratio | exp_ratio |
|---|---|---|---|---|---|---|
| additive | x0 | 54514 | 0.00% | 0.0% | 1.000 | 1.000 |
| additive | x1 | 55602 | 0.05% | 27.5% | 1.000 | 0.885 |
| additive | x3 | 56151 | 0.19% | 28.6% | 1.001 | 0.882 |
| additive | x10 | 56345 | 0.42% | 29.1% | 1.003 | 0.874 |
| centred | x0 | 54514 | 0.00% | 0.0% | 1.000 | 1.000 |
| centred | x1 | 55524 | 0.13% | 27.5% | 1.001 | 0.881 |
| centred | x3 | 56622 | 0.81% | 29.0% | 1.005 | 0.880 |
| centred | x10 | 54465 | 6.91% | 26.0% | 1.057 | 0.828 |
| exp | x0 | 54514 | 0.00% | 0.0% | 1.000 | 1.000 |
| exp | x1 | 57935 | 0.19% | 26.0% | 1.001 | 0.881 |
| exp | x3 | 59861 | 1.13% | 24.2% | 1.010 | 0.845 |
| exp | x10 | 55614 | 10.19% | 28.1% | 1.120 | 0.829 |
| exp_geo | x0 | 54514 | 0.00% | 0.0% | 1.000 | 1.000 |
| exp_geo | x1 | 58199 | 0.16% | 23.6% | 1.001 | 0.896 |
| exp_geo | x3 | 58153 | 1.78% | 27.9% | 1.015 | 0.864 |
| exp_geo | x10 | 53743 | 8.17% | 28.1% | 1.083 | 0.871 |
| exp_geo_replan | x0 | 58198 | 0.00% | 0.0% | 1.000 | 1.000 |
| exp_geo_replan | x1 | 62091 | 0.18% | 24.6% | 1.001 | 0.884 |
| exp_geo_replan | x3 | 60503 | 1.04% | 26.9% | 1.008 | 0.864 |
| exp_geo_replan | x10 | 59098 | 8.43% | 31.9% | 1.079 | 0.860 |
| additive_replan | x0 | 58198 | 0.00% | 0.0% | 1.000 | 1.000 |
| additive_replan | x1 | 59082 | 0.05% | 27.6% | 1.000 | 0.891 |
| additive_replan | x3 | 59361 | 0.21% | 28.4% | 1.001 | 0.880 |
| additive_replan | x10 | 59549 | 0.43% | 29.7% | 1.003 | 0.874 |

## Route diagnostics, Mission–Cooperation (pooled over plans; detour = planned path longer than the shortest)

| variant | k | plans | detour | differs | len_ratio | exp_ratio |
|---|---|---|---|---|---|---|
| additive | x0 | 32503 | 0.00% | 0.0% | 1.000 | 1.000 |
| additive | x1 | 33468 | 0.00% | 13.6% | 1.000 | 0.919 |
| additive | x3 | 33568 | 0.04% | 13.6% | 1.000 | 0.912 |
| additive | x10 | 32935 | 0.06% | 13.5% | 1.001 | 0.912 |
| centred | x0 | 32503 | 0.00% | 0.0% | 1.000 | 1.000 |
| centred | x1 | 33405 | 0.02% | 13.6% | 1.000 | 0.914 |
| centred | x3 | 32661 | 0.06% | 14.0% | 1.001 | 0.903 |
| centred | x10 | 32012 | 0.39% | 14.9% | 1.005 | 0.892 |
| exp | x0 | 32503 | 0.00% | 0.0% | 1.000 | 1.000 |
| exp | x1 | 30723 | 0.02% | 11.4% | 1.000 | 0.872 |
| exp | x3 | 30962 | 0.19% | 11.7% | 1.003 | 0.886 |
| exp | x10 | 31706 | 4.62% | 13.2% | 1.206 | 0.823 |
| exp_geo | x0 | 32503 | 0.00% | 0.0% | 1.000 | 1.000 |
| exp_geo | x1 | 31496 | 0.01% | 10.0% | 1.000 | 0.828 |
| exp_geo | x3 | 30871 | 0.12% | 8.0% | 1.002 | 0.909 |
| exp_geo | x10 | 31258 | 3.52% | 15.9% | 1.033 | 0.900 |
| exp_geo_replan | x0 | 33585 | 0.00% | 0.0% | 1.000 | 1.000 |
| exp_geo_replan | x1 | 33888 | 0.01% | 11.7% | 1.000 | 0.895 |
| exp_geo_replan | x3 | 34258 | 0.15% | 10.1% | 1.002 | 0.858 |
| exp_geo_replan | x10 | 32536 | 2.30% | 16.8% | 1.023 | 0.889 |
| additive_replan | x0 | 33585 | 0.00% | 0.0% | 1.000 | 1.000 |
| additive_replan | x1 | 34118 | 0.01% | 11.3% | 1.000 | 0.871 |
| additive_replan | x3 | 34186 | 0.05% | 11.8% | 1.000 | 0.865 |
| additive_replan | x10 | 33768 | 0.08% | 11.8% | 1.001 | 0.860 |

## Dose-response: Deathmatch / Survival-Aware

| variant | k | EngRedirect | Deaths | AllyDist | ResSeek | Kills | detour rate | exposure ratio |
|---|---|---|---|---|---|---|---|---|
| additive | x0 | 0.67 ± 0.17 | 6.20 ± 1.07 | 4.23 ± 0.69 | 0.79 ± 0.15 | 7.50 ± 1.27 | 0.000 ± 0.000 | 1.000 ± 0.000 |
| additive | x1 | 1.11 ± 0.27 | 7.27 ± 1.25 | 4.26 ± 0.54 | 0.94 ± 0.16 | 8.63 ± 1.25 | 0.001 ± 0.000 | 0.891 ± 0.022 |
| additive | x3 | 1.33 ± 0.56 | 6.23 ± 1.09 | 3.88 ± 0.49 | 0.80 ± 0.14 | 7.90 ± 1.26 | 0.002 ± 0.001 | 0.891 ± 0.022 |
| additive | x10 | 0.92 ± 0.23 | 5.93 ± 1.04 | 4.00 ± 0.54 | 0.74 ± 0.14 | 7.47 ± 1.19 | 0.005 ± 0.001 | 0.883 ± 0.023 |

- **additive**: EngRedirect: rho=+0.11 (p=0.243); vs x0: x1 r=+0.56 pH=0.022, x3 r=+0.54 pH=0.022, x10 r=+0.32 pH=0.137 | Deaths: rho=-0.07 (p=0.421); vs x0: x1 r=+0.28 pH=0.612, x3 r=+0.00 pH=1.000, x10 r=-0.11 pH=1.000 | AllyDist: rho=-0.06 (p=0.496); vs x0: x1 r=+0.02 pH=1.000, x3 r=-0.12 pH=1.000, x10 r=-0.04 pH=1.000 | ResSeek: rho=-0.07 (p=0.422); vs x0: x1 r=+0.23 pH=0.840, x3 r=+0.01 pH=0.980, x10 r=-0.15 pH=0.980 | Kills: rho=-0.03 (p=0.708); vs x0: x1 r=+0.30 pH=0.559, x3 r=+0.08 pH=1.000, x10 r=-0.04 pH=1.000 | detour_rate: rho=+0.69 (p=<0.001); vs x0: x1 r=+1.00 pH=0.016, x3 r=+1.00 pH=<0.001, x10 r=+1.00 pH=<0.001 | exposure_ratio: rho=-0.61 (p=<0.001); vs x0: x1 r=-1.00 pH=<0.001, x3 r=-1.00 pH=<0.001, x10 r=-1.00 pH=<0.001

| centred | x0 | 0.67 ± 0.17 | 6.20 ± 1.07 | 4.23 ± 0.69 | 0.79 ± 0.15 | 7.50 ± 1.27 | 0.000 ± 0.000 | 1.000 ± 0.000 |
| centred | x1 | 1.38 ± 0.56 | 6.73 ± 1.15 | 4.15 ± 0.59 | 0.85 ± 0.16 | 8.20 ± 1.31 | 0.002 ± 0.001 | 0.890 ± 0.023 |
| centred | x3 | 1.04 ± 0.22 | 6.23 ± 0.98 | 3.99 ± 0.50 | 0.83 ± 0.15 | 8.33 ± 1.31 | 0.013 ± 0.004 | 0.871 ± 0.017 |
| centred | x10 | 0.75 ± 0.17 | 5.40 ± 0.78 | 4.27 ± 0.53 | 0.73 ± 0.12 | 7.70 ± 1.05 | 0.089 ± 0.019 | 0.812 ± 0.024 |

- **centred**: EngRedirect: rho=+0.05 (p=0.622); vs x0: x1 r=+0.61 pH=0.010, x3 r=+0.54 pH=0.018, x10 r=+0.22 pH=0.299 | Deaths: rho=-0.12 (p=0.176); vs x0: x1 r=+0.10 pH=1.000, x3 r=+0.00 pH=1.000, x10 r=-0.27 pH=0.645 | AllyDist: rho=-0.00 (p=0.962); vs x0: x1 r=-0.01 pH=1.000, x3 r=-0.11 pH=1.000, x10 r=+0.00 pH=1.000 | ResSeek: rho=-0.07 (p=0.468); vs x0: x1 r=+0.05 pH=1.000, x3 r=+0.08 pH=1.000, x10 r=-0.16 pH=1.000 | Kills: rho=+0.02 (p=0.792); vs x0: x1 r=+0.17 pH=1.000, x3 r=+0.19 pH=1.000, x10 r=+0.08 pH=1.000 | detour_rate: rho=+0.93 (p=<0.001); vs x0: x1 r=+1.00 pH=<0.001, x3 r=+1.00 pH=<0.001, x10 r=+1.00 pH=<0.001 | exposure_ratio: rho=-0.80 (p=<0.001); vs x0: x1 r=-1.00 pH=<0.001, x3 r=-1.00 pH=<0.001, x10 r=-1.00 pH=<0.001

| exp | x0 | 0.67 ± 0.17 | 6.20 ± 1.07 | 4.23 ± 0.69 | 0.79 ± 0.15 | 7.50 ± 1.27 | 0.000 ± 0.000 | 1.000 ± 0.000 |
| exp | x1 | 1.14 ± 0.30 | 6.40 ± 1.09 | 4.25 ± 0.60 | 0.83 ± 0.15 | 8.20 ± 1.27 | 0.003 ± 0.001 | 0.881 ± 0.024 |
| exp | x3 | 0.87 ± 0.19 | 5.43 ± 1.28 | 3.76 ± 0.61 | 0.69 ± 0.16 | 7.00 ± 1.37 | 0.014 ± 0.003 | 0.833 ± 0.036 |
| exp | x10 | 0.51 ± 0.17 | 3.63 ± 1.02 | 4.26 ± 0.75 | 0.49 ± 0.13 | 4.97 ± 1.16 | 0.115 ± 0.034 | 0.824 ± 0.030 |

- **exp**: EngRedirect: rho=-0.13 (p=0.143); vs x0: x1 r=+0.50 pH=0.050, x3 r=+0.32 pH=0.275, x10 r=-0.30 pH=0.275 | Deaths: rho=-0.31 (p=<0.001); vs x0: x1 r=-0.01 pH=0.971, x3 r=-0.20 pH=0.690, x10 r=-0.69 pH=0.004 | AllyDist: rho=-0.05 (p=0.607); vs x0: x1 r=-0.02 pH=1.000, x3 r=-0.20 pH=1.000, x10 r=-0.00 pH=1.000 | ResSeek: rho=-0.29 (p=0.001); vs x0: x1 r=+0.04 pH=0.855, x3 r=-0.24 pH=0.490, x10 r=-0.58 pH=0.017 | Kills: rho=-0.28 (p=0.002); vs x0: x1 r=+0.06 pH=1.000, x3 r=-0.15 pH=1.000, x10 r=-0.53 pH=0.039 | detour_rate: rho=+0.92 (p=<0.001); vs x0: x1 r=+1.00 pH=<0.001, x3 r=+1.00 pH=<0.001, x10 r=+1.00 pH=<0.001 | exposure_ratio: rho=-0.72 (p=<0.001); vs x0: x1 r=-1.00 pH=<0.001, x3 r=-1.00 pH=<0.001, x10 r=-1.00 pH=<0.001

| exp_geo | x0 | 0.67 ± 0.17 | 6.20 ± 1.07 | 4.23 ± 0.69 | 0.79 ± 0.15 | 7.50 ± 1.27 | 0.000 ± 0.000 | 1.000 ± 0.000 |
| exp_geo | x1 | 0.85 ± 0.22 | 6.47 ± 1.13 | 4.01 ± 0.64 | 0.81 ± 0.16 | 7.93 ± 1.17 | 0.002 ± 0.001 | 0.926 ± 0.017 |
| exp_geo | x3 | 0.89 ± 0.30 | 5.93 ± 1.15 | 4.13 ± 0.76 | 0.75 ± 0.16 | 6.80 ± 1.36 | 0.013 ± 0.004 | 0.889 ± 0.030 |
| exp_geo | x10 | 0.72 ± 0.20 | 4.83 ± 1.00 | 3.81 ± 0.56 | 0.65 ± 0.13 | 6.57 ± 1.04 | 0.083 ± 0.015 | 0.876 ± 0.025 |

- **exp_geo**: EngRedirect: rho=+0.00 (p=0.992); vs x0: x1 r=+0.31 pH=0.421, x3 r=+0.19 pH=0.764, x10 r=+0.04 pH=0.855 | Deaths: rho=-0.17 (p=0.057); vs x0: x1 r=+0.04 pH=1.000, x3 r=-0.05 pH=1.000, x10 r=-0.44 pH=0.180 | AllyDist: rho=-0.06 (p=0.545); vs x0: x1 r=-0.14 pH=1.000, x3 r=-0.07 pH=1.000, x10 r=-0.23 pH=0.840 | ResSeek: rho=-0.15 (p=0.103); vs x0: x1 r=+0.07 pH=1.000, x3 r=-0.10 pH=1.000, x10 r=-0.39 pH=0.221 | Kills: rho=-0.18 (p=0.051); vs x0: x1 r=+0.18 pH=0.825, x3 r=-0.16 pH=0.825, x10 r=-0.39 pH=0.278 | detour_rate: rho=+0.91 (p=<0.001); vs x0: x1 r=+1.00 pH=<0.001, x3 r=+1.00 pH=<0.001, x10 r=+1.00 pH=<0.001 | exposure_ratio: rho=-0.67 (p=<0.001); vs x0: x1 r=-0.97 pH=<0.001, x3 r=-0.87 pH=<0.001, x10 r=-1.00 pH=<0.001

| exp_geo_replan | x0 | 0.67 ± 0.17 | 6.20 ± 1.07 | 4.23 ± 0.69 | 0.79 ± 0.15 | 7.50 ± 1.27 | 0.000 ± 0.000 | 1.000 ± 0.000 |
| exp_geo_replan | x1 | 0.90 ± 0.24 | 6.30 ± 1.04 | 3.95 ± 0.51 | 0.78 ± 0.14 | 7.57 ± 1.22 | 0.002 ± 0.001 | 0.908 ± 0.024 |
| exp_geo_replan | x3 | 0.89 ± 0.31 | 6.27 ± 1.27 | 4.08 ± 0.69 | 0.78 ± 0.17 | 6.57 ± 1.29 | 0.014 ± 0.004 | 0.867 ± 0.036 |
| exp_geo_replan | x10 | 0.73 ± 0.21 | 4.20 ± 0.86 | 3.85 ± 0.53 | 0.57 ± 0.11 | 6.00 ± 1.06 | 0.091 ± 0.020 | 0.877 ± 0.044 |

- **exp_geo_replan**: EngRedirect: rho=-0.00 (p=0.964); vs x0: x1 r=+0.36 pH=0.252, x3 r=+0.16 pH=0.904, x10 r=+0.02 pH=0.952 | Deaths: rho=-0.24 (p=0.009); vs x0: x1 r=+0.03 pH=1.000, x3 r=+0.00 pH=1.000, x10 r=-0.57 pH=0.027 | AllyDist: rho=-0.05 (p=0.561); vs x0: x1 r=-0.11 pH=1.000, x3 r=-0.08 pH=1.000, x10 r=-0.17 pH=1.000 | ResSeek: rho=-0.19 (p=0.035); vs x0: x1 r=+0.04 pH=1.000, x3 r=-0.04 pH=1.000, x10 r=-0.47 pH=0.078 | Kills: rho=-0.20 (p=0.033); vs x0: x1 r=+0.10 pH=0.656, x3 r=-0.22 pH=0.647, x10 r=-0.39 pH=0.260 | detour_rate: rho=+0.92 (p=<0.001); vs x0: x1 r=+1.00 pH=<0.001, x3 r=+1.00 pH=<0.001, x10 r=+1.00 pH=<0.001 | exposure_ratio: rho=-0.56 (p=<0.001); vs x0: x1 r=-0.98 pH=<0.001, x3 r=-0.89 pH=<0.001, x10 r=-0.98 pH=<0.001

| additive_replan | x0 | 0.67 ± 0.17 | 6.20 ± 1.07 | 4.23 ± 0.69 | 0.79 ± 0.15 | 7.50 ± 1.27 | 0.000 ± 0.000 | 1.000 ± 0.000 |
| additive_replan | x1 | 1.00 ± 0.25 | 7.47 ± 1.23 | 4.36 ± 0.57 | 0.94 ± 0.16 | 8.57 ± 1.15 | 0.001 ± 0.000 | 0.900 ± 0.019 |
| additive_replan | x3 | 0.93 ± 0.24 | 7.07 ± 1.16 | 4.20 ± 0.60 | 0.87 ± 0.17 | 7.97 ± 1.18 | 0.003 ± 0.001 | 0.893 ± 0.020 |
| additive_replan | x10 | 0.90 ± 0.24 | 6.67 ± 1.15 | 4.05 ± 0.60 | 0.82 ± 0.16 | 7.70 ± 1.28 | 0.005 ± 0.002 | 0.879 ± 0.022 |

- **additive_replan**: EngRedirect: rho=+0.10 (p=0.269); vs x0: x1 r=+0.48 pH=0.069, x3 r=+0.46 pH=0.069, x10 r=+0.37 pH=0.080 | Deaths: rho=+0.03 (p=0.727); vs x0: x1 r=+0.32 pH=0.409, x3 r=+0.20 pH=0.721, x10 r=+0.11 pH=0.721 | AllyDist: rho=-0.04 (p=0.666); vs x0: x1 r=+0.10 pH=1.000, x3 r=+0.03 pH=1.000, x10 r=-0.04 pH=1.000 | ResSeek: rho=+0.01 (p=0.872); vs x0: x1 r=+0.18 pH=1.000, x3 r=+0.07 pH=1.000, x10 r=-0.01 pH=1.000 | Kills: rho=-0.00 (p=0.958); vs x0: x1 r=+0.26 pH=0.698, x3 r=+0.09 pH=1.000, x10 r=+0.03 pH=1.000 | detour_rate: rho=+0.70 (p=<0.001); vs x0: x1 r=+1.00 pH=0.004, x3 r=+1.00 pH=<0.001, x10 r=+1.00 pH=<0.001 | exposure_ratio: rho=-0.66 (p=<0.001); vs x0: x1 r=-1.00 pH=<0.001, x3 r=-1.00 pH=<0.001, x10 r=-1.00 pH=<0.001


## Dose-response: Mission / Mission–Cooperation

| variant | k | AllyDist | ObjCommit | Deaths | detour rate | exposure ratio |
|---|---|---|---|---|---|---|
| additive | x0 | 1.47 ± 0.30 | 0.97 ± 0.02 | 2.77 ± 1.56 | 0.000 ± 0.000 | 1.000 ± 0.000 |
| additive | x1 | 1.51 ± 0.31 | 0.97 ± 0.02 | 3.10 ± 1.72 | 0.000 ± 0.000 | 0.923 ± 0.048 |
| additive | x3 | 1.51 ± 0.31 | 0.97 ± 0.02 | 3.10 ± 1.72 | 0.000 ± 0.000 | 0.923 ± 0.048 |
| additive | x10 | 1.51 ± 0.31 | 0.97 ± 0.02 | 3.10 ± 1.72 | 0.000 ± 0.000 | 0.923 ± 0.048 |

- **additive**: AllyDist: rho=-0.00 (p=0.978); vs x0: x1 r=-0.04 pH=1.000, x3 r=-0.04 pH=1.000, x10 r=-0.04 pH=1.000 | ObjCommit: rho=-0.02 (p=0.841); vs x0: x1 r=-0.06 pH=1.000, x3 r=-0.06 pH=1.000, x10 r=-0.06 pH=1.000 | Deaths: rho=+0.01 (p=0.901); vs x0: x1 r=+0.38 pH=1.000, x3 r=+0.38 pH=1.000, x10 r=+0.38 pH=1.000 | detour_rate: constant; vs x0: x1 r=+0.00 pH=1.000, x3 r=+0.00 pH=1.000, x10 r=+0.00 pH=1.000 | exposure_ratio: rho=-0.51 (p=<0.001); vs x0: x1 r=-0.85 pH=<0.001, x3 r=-0.85 pH=<0.001, x10 r=-0.85 pH=<0.001

| centred | x0 | 1.47 ± 0.30 | 0.97 ± 0.02 | 2.77 ± 1.56 | 0.000 ± 0.000 | 1.000 ± 0.000 |
| centred | x1 | 1.51 ± 0.31 | 0.97 ± 0.02 | 3.10 ± 1.72 | 0.000 ± 0.000 | 0.923 ± 0.048 |
| centred | x3 | 1.51 ± 0.31 | 0.97 ± 0.02 | 3.10 ± 1.72 | 0.000 ± 0.000 | 0.923 ± 0.048 |
| centred | x10 | 1.63 ± 0.42 | 0.96 ± 0.02 | 3.27 ± 1.82 | 0.001 ± 0.001 | 0.922 ± 0.049 |

- **centred**: AllyDist: rho=+0.00 (p=0.958); vs x0: x1 r=-0.04 pH=1.000, x3 r=-0.04 pH=1.000, x10 r=+0.15 pH=1.000 | ObjCommit: rho=-0.02 (p=0.786); vs x0: x1 r=-0.06 pH=1.000, x3 r=-0.06 pH=1.000, x10 r=-0.33 pH=1.000 | Deaths: rho=+0.02 (p=0.834); vs x0: x1 r=+0.38 pH=0.680, x3 r=+0.38 pH=0.680, x10 r=+0.53 pH=0.504 | detour_rate: rho=+0.28 (p=0.002); vs x0: x1 r=+0.00 pH=1.000, x3 r=+0.00 pH=1.000, x10 r=+1.00 pH=0.188 | exposure_ratio: rho=-0.51 (p=<0.001); vs x0: x1 r=-0.85 pH=<0.001, x3 r=-0.85 pH=<0.001, x10 r=-0.85 pH=<0.001

| exp | x0 | 1.47 ± 0.30 | 0.97 ± 0.02 | 2.77 ± 1.56 | 0.000 ± 0.000 | 1.000 ± 0.000 |
| exp | x1 | 1.39 ± 0.20 | 0.97 ± 0.01 | 2.80 ± 1.62 | 0.000 ± 0.000 | 0.936 ± 0.048 |
| exp | x3 | 1.34 ± 0.15 | 0.98 ± 0.01 | 2.70 ± 1.54 | 0.000 ± 0.000 | 0.935 ± 0.043 |
| exp | x10 | 1.37 ± 0.20 | 0.97 ± 0.02 | 2.33 ± 1.43 | 0.033 ± 0.061 | 0.941 ± 0.035 |

- **exp**: AllyDist: rho=+0.04 (p=0.679); vs x0: x1 r=+0.18 pH=1.000, x3 r=+0.06 pH=1.000, x10 r=+0.13 pH=1.000 | ObjCommit: rho=+0.02 (p=0.838); vs x0: x1 r=+0.15 pH=1.000, x3 r=+0.38 pH=0.798, x10 r=+0.06 pH=1.000 | Deaths: rho=-0.02 (p=0.852); vs x0: x1 r=+0.11 pH=1.000, x3 r=+0.09 pH=1.000, x10 r=-0.18 pH=1.000 | detour_rate: rho=+0.36 (p=<0.001); vs x0: x1 r=+0.00 pH=1.000, x3 r=+1.00 pH=1.000, x10 r=+1.00 pH=0.023 | exposure_ratio: rho=-0.37 (p=<0.001); vs x0: x1 r=-0.35 pH=0.100, x3 r=-0.42 pH=0.085, x10 r=-0.87 pH=<0.001

| exp_geo | x0 | 1.47 ± 0.30 | 0.97 ± 0.02 | 2.77 ± 1.56 | 0.000 ± 0.000 | 1.000 ± 0.000 |
| exp_geo | x1 | 1.42 ± 0.24 | 0.97 ± 0.02 | 2.70 ± 1.54 | 0.000 ± 0.000 | 0.932 ± 0.039 |
| exp_geo | x3 | 1.52 ± 0.30 | 0.97 ± 0.02 | 3.03 ± 1.70 | 0.000 ± 0.000 | 0.927 ± 0.042 |
| exp_geo | x10 | 1.36 ± 0.22 | 0.98 ± 0.01 | 2.20 ± 1.47 | 0.003 ± 0.003 | 0.948 ± 0.032 |

- **exp_geo**: AllyDist: rho=+0.05 (p=0.576); vs x0: x1 r=+0.18 pH=0.879, x3 r=+0.32 pH=0.508, x10 r=+0.03 pH=0.886 | ObjCommit: rho=+0.02 (p=0.826); vs x0: x1 r=+0.05 pH=1.000, x3 r=-0.14 pH=1.000, x10 r=+0.31 pH=1.000 | Deaths: rho=-0.02 (p=0.838); vs x0: x1 r=+0.02 pH=1.000, x3 r=+0.21 pH=1.000, x10 r=-0.29 pH=1.000 | detour_rate: rho=+0.33 (p=<0.001); vs x0: x1 r=+0.00 pH=1.000, x3 r=+1.00 pH=1.000, x10 r=+1.00 pH=0.047 | exposure_ratio: rho=-0.51 (p=<0.001); vs x0: x1 r=-0.95 pH=<0.001, x3 r=-0.95 pH=<0.001, x10 r=-0.87 pH=<0.001

| exp_geo_replan | x0 | 1.47 ± 0.30 | 0.97 ± 0.02 | 2.77 ± 1.56 | 0.000 ± 0.000 | 1.000 ± 0.000 |
| exp_geo_replan | x1 | 1.50 ± 0.29 | 0.97 ± 0.02 | 2.90 ± 1.61 | 0.000 ± 0.000 | 0.937 ± 0.036 |
| exp_geo_replan | x3 | 1.51 ± 0.30 | 0.97 ± 0.02 | 3.17 ± 1.70 | 0.000 ± 0.000 | 0.934 ± 0.038 |
| exp_geo_replan | x10 | 1.31 ± 0.16 | 0.98 ± 0.01 | 2.13 ± 1.36 | 0.008 ± 0.008 | 0.944 ± 0.035 |

- **exp_geo_replan**: AllyDist: rho=+0.07 (p=0.438); vs x0: x1 r=+0.32 pH=0.276, x3 r=+0.41 pH=0.166, x10 r=+0.15 pH=0.494 | ObjCommit: rho=+0.00 (p=0.960); vs x0: x1 r=-0.08 pH=1.000, x3 r=-0.20 pH=1.000, x10 r=+0.39 pH=0.650 | Deaths: rho=+0.00 (p=0.980); vs x0: x1 r=+0.13 pH=0.940, x3 r=+0.30 pH=0.940, x10 r=-0.25 pH=0.940 | detour_rate: rho=+0.33 (p=<0.001); vs x0: x1 r=+0.00 pH=1.000, x3 r=+1.00 pH=1.000, x10 r=+1.00 pH=0.047 | exposure_ratio: rho=-0.51 (p=<0.001); vs x0: x1 r=-0.95 pH=<0.001, x3 r=-0.95 pH=<0.001, x10 r=-0.88 pH=<0.001

| additive_replan | x0 | 1.47 ± 0.30 | 0.97 ± 0.02 | 2.77 ± 1.56 | 0.000 ± 0.000 | 1.000 ± 0.000 |
| additive_replan | x1 | 1.43 ± 0.25 | 0.97 ± 0.01 | 2.60 ± 1.45 | 0.000 ± 0.000 | 0.925 ± 0.043 |
| additive_replan | x3 | 1.43 ± 0.25 | 0.97 ± 0.01 | 2.60 ± 1.45 | 0.000 ± 0.000 | 0.925 ± 0.043 |
| additive_replan | x10 | 1.43 ± 0.25 | 0.97 ± 0.01 | 2.60 ± 1.45 | 0.000 ± 0.000 | 0.925 ± 0.043 |

- **additive_replan**: AllyDist: rho=-0.01 (p=0.888); vs x0: x1 r=-0.06 pH=1.000, x3 r=-0.06 pH=1.000, x10 r=-0.06 pH=1.000 | ObjCommit: rho=-0.01 (p=0.951); vs x0: x1 r=-0.03 pH=1.000, x3 r=-0.03 pH=1.000, x10 r=-0.03 pH=1.000 | Deaths: rho=-0.01 (p=0.901); vs x0: x1 r=-0.02 pH=1.000, x3 r=-0.02 pH=1.000, x10 r=-0.02 pH=1.000 | detour_rate: constant; vs x0: x1 r=+0.00 pH=1.000, x3 r=+0.00 pH=1.000, x10 r=+0.00 pH=1.000 | exposure_ratio: rho=-0.51 (p=<0.001); vs x0: x1 r=-0.84 pH=<0.001, x3 r=-0.84 pH=<0.001, x10 r=-0.84 pH=<0.001


## Variants vs additive at the same k (paired Wilcoxon; Holm within condition x variant x k; listed if p_Holm < 0.05)


### k = 1

- **centred**: no adjusted-significant difference
- **exp**: Control/Mission–Cooperation ObjCommit 0.96 ± 0.02 -> 0.98 ± 0.01 (r=+0.85, pH=0.039)
- **exp_geo**: Control/Mission–Cooperation AllyDist 1.76 ± 0.35 -> 1.73 ± 0.30 (r=+0.59, pH=0.034)
- **exp_geo_replan**: Control/Persistent Objective AllyDist 2.43 ± 0.68 -> 2.23 ± 0.58 (r=+0.58, pH=0.039)
- **additive_replan**: no adjusted-significant difference

### k = 3

- **centred**: no adjusted-significant difference
- **exp**: Mission/Mission–Cooperation ObjCommit 0.97 ± 0.02 -> 0.98 ± 0.01 (r=+0.79, pH=0.049)
- **exp_geo**: Mission/Persistent Objective ObjCommit 0.87 ± 0.10 -> 0.90 ± 0.08 (r=+0.79, pH=0.037)
- **exp_geo_replan**: no adjusted-significant difference
- **additive_replan**: Mission/Aggressive EngRedirect 0.92 ± 0.21 -> 0.82 ± 0.20 (r=-0.79, pH=0.039); Mission/Aggressive Deaths 7.30 ± 1.61 -> 6.60 ± 1.56 (r=-0.91, pH=0.039)

### k = 10

- **centred**: no adjusted-significant difference
- **exp**: Mission/Aggressive EngRedirect 0.86 ± 0.21 -> 0.63 ± 0.17 (r=-0.58, pH=0.041); Mission/Aggressive Deaths 6.83 ± 1.61 -> 5.13 ± 1.43 (r=-0.63, pH=0.036); Deathmatch/Survival-Aware EngRedirect 0.92 ± 0.23 -> 0.51 ± 0.17 (r=-0.53, pH=0.029); Deathmatch/Survival-Aware ResSeek 0.74 ± 0.14 -> 0.49 ± 0.13 (r=-0.56, pH=0.029); Deathmatch/Survival-Aware Deaths 5.93 ± 1.04 -> 3.63 ± 1.02 (r=-0.70, pH=0.007)
- **exp_geo**: Deathmatch/Persistent Objective EngRedirect 0.10 ± 0.04 -> 0.04 ± 0.03 (r=-0.65, pH=0.026); Deathmatch/Persistent Objective Deaths 7.07 ± 0.88 -> 5.33 ± 0.65 (r=-0.71, pH=0.007); Control/Mission–Cooperation AllyDist 1.66 ± 0.31 -> 1.67 ± 0.28 (r=+0.60, pH=0.034); Control/Persistent Objective AllyDist 2.39 ± 0.65 -> 2.62 ± 0.67 (r=+0.63, pH=0.020); Control/Survival-Aware AllyDist 3.28 ± 0.60 -> 4.62 ± 0.82 (r=+0.52, pH=0.048)
- **exp_geo_replan**: Deathmatch/Persistent Objective Deaths 7.07 ± 0.88 -> 5.10 ± 0.93 (r=-0.69, pH=0.007); Control/Survival-Aware AllyDist 3.28 ± 0.60 -> 4.92 ± 0.93 (r=+0.62, pH=0.009)
- **additive_replan**: no adjusted-significant difference

## Style signatures per variant (Kruskal-Wallis epsilon^2 across the four styles; Control wins)

| variant | k | Mission ObjCommit | Mission AllyDist | Deathmatch EngRedirect | Deathmatch ResSeek | Control CtrlScore | Control wins (MC/PO/Agg/SA) |
|---|---|---|---|---|---|---|---|
| additive | x0 | 0.68 | 0.31 | 0.55 | 0.81 | 0.72 | 28/27/8/0 |
| additive | x1 | 0.66 | 0.36 | 0.64 | 0.75 | 0.67 | 30/30/11/2 |
| additive | x3 | 0.68 | 0.35 | 0.64 | 0.75 | 0.70 | 30/30/11/1 |
| additive | x10 | 0.67 | 0.32 | 0.62 | 0.76 | 0.69 | 30/30/11/1 |
| centred | x0 | 0.68 | 0.31 | 0.55 | 0.81 | 0.72 | 28/27/8/0 |
| centred | x1 | 0.66 | 0.35 | 0.62 | 0.75 | 0.69 | 30/30/11/1 |
| centred | x3 | 0.66 | 0.33 | 0.64 | 0.72 | 0.66 | 30/30/11/2 |
| centred | x10 | 0.67 | 0.33 | 0.63 | 0.79 | 0.71 | 30/30/11/1 |
| exp | x0 | 0.68 | 0.31 | 0.55 | 0.81 | 0.72 | 28/27/8/0 |
| exp | x1 | 0.69 | 0.37 | 0.62 | 0.72 | 0.69 | 30/30/10/2 |
| exp | x3 | 0.70 | 0.33 | 0.64 | 0.73 | 0.72 | 30/30/8/2 |
| exp | x10 | 0.67 | 0.36 | 0.58 | 0.69 | 0.67 | 30/28/9/1 |
| exp_geo | x0 | 0.68 | 0.31 | 0.55 | 0.81 | 0.72 | 28/27/8/0 |
| exp_geo | x1 | 0.71 | 0.34 | 0.63 | 0.85 | 0.72 | 30/30/11/0 |
| exp_geo | x3 | 0.69 | 0.30 | 0.60 | 0.75 | 0.73 | 30/29/10/0 |
| exp_geo | x10 | 0.65 | 0.38 | 0.68 | 0.78 | 0.63 | 30/28/9/3 |
| exp_geo_replan | x0 | 0.68 | 0.31 | 0.52 | 0.76 | 0.72 | 28/27/8/0 |
| exp_geo_replan | x1 | 0.69 | 0.32 | 0.62 | 0.82 | 0.69 | 30/30/11/1 |
| exp_geo_replan | x3 | 0.66 | 0.32 | 0.58 | 0.77 | 0.70 | 30/29/10/1 |
| exp_geo_replan | x10 | 0.64 | 0.39 | 0.66 | 0.77 | 0.63 | 30/26/9/2 |
| additive_replan | x0 | 0.68 | 0.31 | 0.52 | 0.76 | 0.72 | 28/27/8/0 |
| additive_replan | x1 | 0.69 | 0.34 | 0.66 | 0.78 | 0.67 | 29/30/9/2 |
| additive_replan | x3 | 0.68 | 0.33 | 0.65 | 0.76 | 0.67 | 29/30/9/2 |
| additive_replan | x10 | 0.68 | 0.32 | 0.65 | 0.75 | 0.70 | 29/30/9/1 |
