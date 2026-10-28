# fps-bots-with-priority-structure — a steerable, rule-based decision layer for FPS bots

Code, result data and figure scripts for the paper *Steering First-Person Shooter Bots with a Compact Priority Structure
and Risk-Aware Pathfinding* (Yongwoo Ju, Minkyoung Cho).

The repository provides a reproducible, controlled FPS-like simulation (a 2D grid world) to evaluate bot behaviors
driven by a **priority structure**: four goal weights (objective, enemy, resource, teammate), a commitment weight that
penalizes goal switching, a **risk-aware A\*** route cost that prices expected enemy fire, cover and teammate proximity
in extra movement steps, and four discrete combat-movement modes (hold, keep moving, chase, evade). Together these
parameters form a compact **style vector** that steers a fixed decision core without any training.

## Layout

| Path | Contents |
|---|---|
| `fps_priority_ai/` | The grid-world testbed and the unified priority policy: `policy.py` (goal selection with commitment, combat-movement modes, risk-aware A\*), `config.py` (constants), `experiment.py` (episodes, metrics), `runner.py` (styles, scenarios, the default experiment), map registry |
| `experiments/` | Experiment runners (`run_*.py`), analyses (`analyze_*.py`), table and figure generators (`make_*.py`), the behavior-tree baselines and the fitting rounds |
| `tests/` | Simulator invariants (`test_movement.py`: 4-adjacent moves, determinism given a seed; `test_maps.py`) |
| `run/` | Scripts for a first look: setup, a quick demo, the development-map experiments with their hypothesis tests, the figures (see `run/README.md`) |
| `results/` | Result data, analysis summaries and generated tables of the runs the paper reports (development maps, nine confirmation maps, commitment sweep, style blends, teammate term, the six behavior-tree fits, map descriptors) |
| `figures/` | The scripts that draw the seven figures of the paper from `results/`, `make_all.sh`, and the figures themselves in `figures/out/` (see `figures/README.md`) |

## Quick start

```bash
bash run/setup.sh            # virtual environment, dependencies, simulator tests (about a minute)
bash run/quick_demo.sh 5     # four styles x three scenarios, 5 episodes each; prints the intent metrics (about a minute)
bash run/make_figures.sh     # the seven figures of the paper from results/ into figures/out/
bash run/main_experiment.sh 10   # the development-map experiments and the H1-H4 tests on the random map (about 7 minutes)
```

Requirements: Python 3.10+ with `numpy`, `pandas`, `matplotlib`, `scipy` (`requirements.txt`) and `scikit-learn` for the
style classifier in the hypothesis tests. The run scripts use `.venv/bin/python` when `run/setup.sh` has created it,
otherwise `python3`; set `PYTHON=/path/to/python` to choose another interpreter.

## Testbed settings used by every reported run

All results in the paper were produced with the five movement and perception rules of the final testbed switched on
and with single-threaded, hash-stable Python. The run scripts set these; when calling a runner directly, export them first:

```bash
export FPS_TEAMMATE_SWAP=1 FPS_LOCAL_AVOIDANCE=1 FPS_FORGET_MEMORY=1 FPS_SYMMETRIC_LOS=1 FPS_REACHABLE_PLACEMENT=1
export PYTHONHASHSEED=0 OMP_NUM_THREADS=1
```

## Running experiments directly

The default experiment (four styles, three scenarios, the default random map) is the module entry point:

```bash
python -m fps_priority_ai.runner --out outputs/default --episodes 20 --seed 123
```

The runners of the paper's experiments live in `experiments/` and take `--out`, `--episodes`, `--seed` and `--map`
(`random`, `urban`, the nine confirmation maps and the four game-inspired maps of the registry). From the repository root:

```bash
python experiments/run_ec_experiments.py        --out outputs/dev --episodes 100 --seed 2026 --map random  # main experiment (H1)
python experiments/run_sensitivity_commitment.py --out outputs/dev --episodes 100 --seed 2026 --map random  # commitment sweep (H2)
python experiments/run_mode_ablation.py         --out outputs/dev --episodes 100 --seed 2026 --map random  # combat-mode ablation (H1)
python experiments/run_cost_term_ablation.py    --out outputs/dev --episodes 100 --seed 2026 --map random  # route terms, leave-one-out (H3)
python experiments/run_teammate_term.py         --out outputs/dev --episodes 100 --seed 2026 --map random --exact-out  # teammate term (H3b)
python experiments/run_interpolation.py         --out outputs/dev --episodes 100 --seed 2026 --map random  # style blends (H4)
python experiments/analyze_hypotheses.py        --dir outputs/dev --map-name random                        # H1-H4 tests, effect sizes
python experiments/run_baselines.py             --out outputs/dev --map random                             # behavior-tree baselines
```

`run/main_experiment.sh` runs exactly this sequence. Every runner follows the common-random-numbers design of
`fps_priority_ai.experiment`: each style or variant is evaluated on the same initial states episode by episode.

Outputs of a run:

- `results.csv`: one row per (scenario, style, episode) with the intent metrics and the outcome measures;
- `figures/`: map images and trajectory plots of the default runner;
- `hypotheses_summary.md` / `.json`: the tests of `analyze_hypotheses.py`.

## Interpreting the key metrics

Computed for the evaluated team over the steps in which an agent is alive:

- `objective_commitment_ratio`: fraction of decision steps in which the selected goal is the objective.
- `engagement_redirection_rate_per_100`: switches to the enemy goal while an opponent is visible, per 100 alive agent-steps.
- `resource_seeking_rate_per_100`: switches to the resource goal in a low-status state, per 100 alive agent-steps.
- `avg_ally_proximity`: mean distance to the nearest living teammate (lower means tighter cohesion). The column keeps its
  historical name; the paper reports it as the nearest-ally distance.
- `kills`, `deaths`, `control_score`: outcome measures; the control score is the points on the control cell in *Control*.

## Reproducing the figures of the paper

`figures/make_all.sh` draws the seven figures from the files in `results/` (about 5 MB of per-episode data and the
confirmation summary); `figures/README.md` maps every figure to its script, its inputs and the options used in the paper.
Figure 1 (the reconstructed pseudocode of the four bots) is typeset in LaTeX and has no script.

## Extending the environment

- Add route-cost terms to the A\* step cost in `fps_priority_ai/policy.py`.
- Add scenarios (for example escort or payload) in `fps_priority_ai/runner.py`.
- Replace the grid with a navigation mesh while keeping the same policy interface; the risk-aware cost applies to
  traversal costs of mesh polygons in the same way.

## License

Code (including the figure scripts) and result data: MIT (`LICENSE`).
