"""Movement invariants of the simulator (standard library only; no matplotlib).

  1. Every move is to a 4-adjacent cell (no multi-cell jumps after blocked moves).
  2. Episodes are deterministic given a seed.

Usage (from code/):  python tests/test_movement.py
"""

from __future__ import annotations

import random
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fps_priority_ai.config import AgentConfig, ScenarioConfig, WeaponConfig
from fps_priority_ai.runner import default_styles
from fps_priority_ai.env import FPSEnv
from fps_priority_ai.baselines import default_baselines
from fps_priority_ai.experiment import MAPS, episode_seed
from fps_priority_ai.world import manhattan

# Main model (exponential route metric, calibrated weights), the v2 additive styles under renamed
# keys, and route-metric variants with amplified weights (alternative route costs, walking-distance
# fields, clipping, and periodic replanning).
STYLES = default_styles()
ADDITIVE = {f"{n} [additive]": replace(s, name=f"{n} [additive]") for n, s in default_styles("additive").items()}
ROUTE_VARIANTS = {}
for _s in default_styles("additive").values():
    for _tag, _k, _kw in [("exp_geo_replan", 3, dict(route_cost="exp", threat_field="geodesic", replan_interval=5)),
                          ("centred", 10, dict(route_cost="centred"))]:
        _name = f"{_s.name} [{_tag} x{_k}]"
        ROUTE_VARIANTS[_name] = replace(_s, name=_name, w_exposure=_k * _s.w_exposure, w_cover=_k * _s.w_cover,
                                        w_teammate_sep=_k * _s.w_teammate_sep, route_diagnostics=True, **_kw)

SCENARIOS = [
    ScenarioConfig(name="Mission", mode="mission", max_steps=550),
    ScenarioConfig(name="Deathmatch", mode="deathmatch", max_steps=550),
    ScenarioConfig(name="Control", mode="control", max_steps=550, score_to_win=120),
]


def run(scenario: ScenarioConfig, style: str, seed: int, map_name: str = "random"):
    env = FPSEnv(map_cfg=MAPS[map_name], agent_cfg=AgentConfig(), weapon_cfg=WeaponConfig(),
                 scenario=scenario, styles={**STYLES, **ADDITIVE, **ROUTE_VARIANTS, **default_baselines()},
                 rng=random.Random(seed))
    return env.run_episode(evaluated_style=style).logs


def non_adjacent_moves(logs) -> int:
    last, bad = {}, 0
    for r in logs:
        prev = last.get(r.agent_id)
        # Consecutive logged steps only (dead agents are not logged; respawns are excluded).
        if prev is not None and prev[0] == r.step - 1 and manhattan(prev[1], r.pos) > 1:
            bad += 1
        last[r.agent_id] = (r.step, r.pos)
    return bad


def main() -> None:
    total_bad, n = 0, 0
    for map_name in ("random", "urban"):   # (2026-09-25) base maps only; new maps: tests/test_maps.py
        for sc in SCENARIOS:
            for style in list(STYLES) + list(ADDITIVE) + list(ROUTE_VARIANTS) + list(default_baselines()):
                for ep in range(2):
                    total_bad += non_adjacent_moves(run(sc, style, episode_seed(2026, sc.name, ep), map_name))
                    n += 1
    assert total_bad == 0, f"{total_bad} non-adjacent moves found"
    print("[OK] no non-adjacent moves in", n, "episodes on maps", ["random", "urban"])

    seed = episode_seed(2026, "Control", 0)
    a = [(r.step, r.agent_id, r.pos, r.goal_type) for r in run(SCENARIOS[2], "Mission–Cooperation", seed)]
    b = [(r.step, r.agent_id, r.pos, r.goal_type) for r in run(SCENARIOS[2], "Mission–Cooperation", seed)]
    assert a == b, "episodes are not deterministic for a fixed seed"
    name = "Survival-Aware [exp_geo_replan x3]"
    a = [(r.step, r.agent_id, r.pos, r.goal_type) for r in run(SCENARIOS[1], name, seed)]
    b = [(r.step, r.agent_id, r.pos, r.goal_type) for r in run(SCENARIOS[1], name, seed)]
    assert a == b, "route-metric episodes are not deterministic for a fixed seed"
    print("[OK] deterministic given a seed")


if __name__ == "__main__":
    main()
