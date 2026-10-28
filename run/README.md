# Running the code

Scripts for a first look at the testbed and the policy. All of them are run from anywhere; they locate the repository
root themselves, put it on `PYTHONPATH`, and switch on the five testbed rules used by every reported run
(`FPS_TEAMMATE_SWAP`, `FPS_LOCAL_AVOIDANCE`, `FPS_FORGET_MEMORY`, `FPS_SYMMETRIC_LOS`, `FPS_REACHABLE_PLACEMENT`).
They use `.venv/bin/python` at the repository root when it exists, otherwise `python3`; set `PYTHON=/path/to/python`
to choose another interpreter.

| Script | What it does | Time |
|---|---|---|
| `setup.sh` | Creates `.venv`, installs `requirements.txt` (and scikit-learn for the classifier tests), runs the two simulator tests | about 1 min |
| `quick_demo.sh [EPISODES] [OUT]` | Four designed styles in the three scenarios on the default map; prints mean intent metrics, writes `results.csv` and trajectory images to `outputs/quick_demo/` | 5 episodes: about 1 min |
| `main_experiment.sh [EPISODES] [MAP] [OUT]` | The development-map experiments of Sections 6.1–6.4 on one map (main experiment, commitment sweep, combat-mode ablation, route-term ablation, teammate term, style blends) and the H1–H4 hypothesis tests of that map | 100 episodes: about 70 min on one core; 10 episodes: about 7 min (the tests need at least 5 episodes) |
| `make_figures.sh` | Rebuilds the seven figures of the paper from `results/` (see `figures/README.md`) | seconds |

The full pre-registered rounds of the paper (development maps, nine confirmation maps, the fits to the four reconstructed
behavior trees) were run with frozen protocols and hash-verified drivers; those drivers, the protocols and the complete
result files are available from the authors on request. The individual experiment commands are listed in the top-level
`README.md`.

Example:

```bash
bash run/setup.sh
bash run/quick_demo.sh 5
bash run/main_experiment.sh 10 urban
```
