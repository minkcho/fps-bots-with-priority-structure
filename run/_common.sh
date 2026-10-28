# Shared settings for the scripts in run/ (sourced, not executed).
# Repository root, interpreter, and the five testbed rules that every reported run used.
RUN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$RUN_DIR/.." && pwd)"
CODE="$ROOT"
if [ -z "${PYTHON:-}" ]; then
  if [ -x "$ROOT/.venv/bin/python" ]; then PYTHON="$ROOT/.venv/bin/python"; else PYTHON=python3; fi
fi
export PYTHONPATH="$CODE${PYTHONPATH:+:$PYTHONPATH}"
export FPS_TEAMMATE_SWAP=1 FPS_LOCAL_AVOIDANCE=1 FPS_FORGET_MEMORY=1 FPS_SYMMETRIC_LOS=1 FPS_REACHABLE_PLACEMENT=1
export PYTHONHASHSEED=0 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
