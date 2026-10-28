#!/bin/bash
# Create a virtual environment at the repository root, install the dependencies, and run the simulator tests.
# Usage: bash run/setup.sh          (about one minute; needs Python 3.10+ and network access for pip)
set -e
source "$(dirname "$0")/_common.sh"
VENV="${VENV_DIR:-$ROOT/.venv}"
python3 -m venv "$VENV"
"$VENV/bin/pip" install -q -r "$CODE/requirements.txt" scikit-learn
echo "dependencies installed in $VENV"
PYTHON="$VENV/bin/python"
(cd "$CODE" && "$PYTHON" tests/test_movement.py && "$PYTHON" tests/test_maps.py)
echo "tests passed. Next: bash run/quick_demo.sh"
