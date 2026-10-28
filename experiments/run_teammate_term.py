"""H3b (pre-specified 2026-09-23, before any run of this script): the route-level teammate term.

The main model has lambda_T = 0. This experiment switches the term on for the evaluated team
(exp form: attraction exp(-lambda_T * sum_teammates 1/max(d,1))) with lambda_T in {0, 1, 3, 10},
all other weights as in the main model, for every style and scenario.
Primary test (pre-specified): Deathmatch, Mission--Cooperation, nearest-ally distance,
lambda_T = 10 vs 0, paired Wilcoxon by episode (common random numbers); H3b predicts a smaller
distance. Everything else is secondary.
Usage: python experiments/run_teammate_term.py --out ../repro_outputs/v3 --map random
"""
from __future__ import annotations

import argparse
from dataclasses import replace
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fps_priority_ai.experiment import MAPS, run_condition, write_csv  # noqa: E402
from fps_priority_ai.runner import default_scenarios, default_styles  # noqa: E402

LAMS_T = [0.0, 1.0, 3.0, 10.0]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True); p.add_argument("--map", default="random", choices=sorted(MAPS))
    p.add_argument("--episodes", type=int, default=30); p.add_argument("--seed", type=int, default=2026)
    # (2026-09-25) filters for the confirmation run (only the pre-specified primary test is needed) and an
    # exact output directory (the default keeps the old layout: random -> <out>, other maps -> <out>/urban)
    p.add_argument("--scenario", default=None); p.add_argument("--style", default=None)
    p.add_argument("--lambdas", default=None, help="comma-separated lambda_T values (default 0,1,3,10)")
    p.add_argument("--exact-out", action="store_true", help="write <out>/teammate_term.csv for any map")
    a = p.parse_args()
    styles = default_styles("exp")
    lams = [float(x) for x in a.lambdas.split(",")] if a.lambdas else LAMS_T
    rows = []
    for sc in default_scenarios():
        if a.scenario and sc.name != a.scenario:
            continue
        for st in styles.values():
            if a.style and st.name != a.style:
                continue
            for lt in lams:
                ev = st if lt == 0 else replace(st, name=f"{st.name} [lambda_T {lt:g}]", w_teammate_sep=lt)
                rows += run_condition(sc, ev, styles, a.episodes, a.seed,
                                      {"scenario": sc.name, "style": st.name, "lambda_T": lt}, MAPS[a.map])
    out = Path(a.out) / ("teammate_term.csv" if (a.exact_out or a.map == "random") else "urban/teammate_term.csv")
    print("Saved:", write_csv(out, ["scenario", "style", "lambda_T"], rows))


if __name__ == "__main__":
    main()
