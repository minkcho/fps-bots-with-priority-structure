"""Shared experiment utilities: common-random-number seeding and episode execution.

Every experiment script evaluates (scenario, style) conditions episode by episode.
Seeds follow a common-random-numbers design: the seed of an episode depends only on
(base seed, scenario, episode index), never on the style or variant being evaluated.
Conditions evaluated on the same scenario therefore start from identical initial
states episode by episode, which allows paired comparisons and makes the "full"
condition of every ablation identical to the corresponding main-experiment episode.
"""

from __future__ import annotations

import csv
import random
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

from .config import AgentConfig, MapConfig, PriorityWeights, ScenarioConfig, WeaponConfig
from .env import FPSEnv
from .metrics import compute_metrics

# Map layouts: the registry in maps.py (2026-09-25). "random" is the scattered-obstacle map of the main
# experiments and "urban" has rectangular buildings separated by streets; the registry adds the map sample of
# the confirmation run and the game-inspired maps. Every map is checked for reachability on import.
from .maps import MAPS  # noqa: E402
MAP_CFG = MAPS["random"]

METRIC_COLUMNS = [
    "objective_commitment_ratio",
    "engagement_redirection_rate_per_100",
    "resource_seeking_rate_per_100",
    "avg_ally_proximity",
    "kills", "deaths",
    "control_score",
    "steps",
    "goal_switch_rate_per_100",
    "walked_hits_per_step",
    "los_frac",
    "hits_taken",            # (2026-09-24) hits actually received by the evaluated team
    "hits_taken_per_step",   # per alive agent-step, the same denominator as walked_hits_per_step
    "kill_rate_per_100",     # (2026-09-25) kills per 100 alive agent-steps
    "death_rate_per_100",    # (2026-09-25) deaths per 100 alive agent-steps
    "resource_goal_share_good",  # (2026-09-25) share of good-status alive steps on the Resource goal (item control)
    "retreat_share",         # (2026-09-26) share of low-status steps with an enemy visible spent on the Resource goal
    "far_pursuit_share",     # (2026-09-26) share of steps with no opponent within 10 cells spent on the Enemy goal
    "contact_distance",      # (2026-09-26) mean distance to the nearest opponent over steps with an enemy visible
    "resource_trip_distance",  # (2026-09-26) mean distance to the goal cell over steps on the Resource goal
]


def testbed_flags() -> Dict[str, bool]:
    """Optional testbed rules of 2026-09-25 (movement and perception fixes; all off in the paper's final run),
    as set by the environment variables FPS_TEAMMATE_SWAP, FPS_LOCAL_AVOIDANCE, FPS_FORGET_MEMORY,
    FPS_SYMMETRIC_LOS and FPS_REACHABLE_PLACEMENT."""
    from . import world
    a = AgentConfig()
    return {"teammate_swap": a.teammate_swap, "local_avoidance": a.local_avoidance,
            "forget_reached_memory": a.forget_reached_memory, "symmetric_los": world.SYMMETRIC_LOS,
            "reachable_placement": world.REACHABLE_PLACEMENT}


def episode_seed(base_seed: int, scenario_name: str, episode: int) -> int:
    """Seed for one episode; independent of the style or variant (common random numbers)."""
    return random.Random(f"{base_seed}|{scenario_name}|{episode}").randrange(10**9)


def walked_exposure(env: FPSEnv, logs, team_id: int = 0) -> Tuple[float, float]:
    """Route-level readouts (added 2026-09-23 for H3): over the team's alive steps, the expected
    hits per step from living opponents in line of sight within weapon range (the expected-hits
    field of the route cost, evaluated along the walked path) and the fraction of steps with such
    an opponent."""
    from collections import defaultdict
    wc = env.weapon_cfg
    by_step = defaultdict(lambda: {0: [], 1: []})
    for l in logs:
        by_step[l.step][0 if l.team == team_id else 1].append(l)
    alive = los = 0
    hits = 0.0
    for d in by_step.values():
        enemies = [l.pos for l in d[1]]
        for l in d[0]:
            alive += 1
            h = 0.0
            for e in enemies:
                dist = ((l.pos[0] - e[0]) ** 2 + (l.pos[1] - e[1]) ** 2) ** 0.5
                if dist <= wc.range_cells and env.world.los_clear(l.pos, e):
                    h += wc.base_accuracy * max(0.05, 1.0 - 0.7 * dist / max(1.0, float(wc.range_cells)))
            hits += h
            los += int(h > 0)
    return (hits / alive, los / alive) if alive else (0.0, 0.0)


def run_episode(
    scenario: ScenarioConfig,
    style: PriorityWeights,
    styles: Dict[str, PriorityWeights],
    seed: int,
    map_cfg: MapConfig = MAP_CFG,
) -> Dict[str, object]:
    """Run one episode of `style` (team 0) against the scenario's fixed opponent style."""
    return run_episode_env(scenario, style, styles, seed, map_cfg)[0]


def run_episode_env(
    scenario: ScenarioConfig,
    style: PriorityWeights,
    styles: Dict[str, PriorityWeights],
    seed: int,
    map_cfg: MapConfig = MAP_CFG,
) -> Tuple[Dict[str, object], FPSEnv]:
    """Like run_episode, but also returns the finished environment (e.g. for policy logs)."""
    # The environment must keep the four stock style names (FPSEnv._init_agents and the
    # opponent style reference them), so variants are added alongside them.
    styles_for_env = {**styles, style.name: style}
    env = FPSEnv(
        map_cfg=map_cfg,
        agent_cfg=AgentConfig(),
        weapon_cfg=WeaponConfig(),
        scenario=scenario,
        styles=styles_for_env,
        rng=random.Random(seed),
    )
    res = env.run_episode(evaluated_style=style.name)

    kills = sum(a.kills for a in env.agents.values() if a.team == 0)
    deaths = sum(a.deaths for a in env.agents.values() if a.team == 0)
    control_score = res.team_scores.get(0) if scenario.mode == "control" else None
    m = compute_metrics(logs=res.logs, team_id=0, kills=kills, deaths=deaths, control_score=control_score)

    row = {
        "objective_commitment_ratio": f"{m.objective_commitment_ratio:.6f}",
        "engagement_redirection_rate_per_100": f"{m.engagement_redirection_rate_per_100:.6f}",
        "resource_seeking_rate_per_100": f"{m.resource_seeking_rate_per_100:.6f}",
        "avg_ally_proximity": f"{m.avg_ally_proximity:.6f}" if m.avg_ally_proximity is not None else "",
        "kills": kills,
        "deaths": deaths,
        "control_score": control_score if control_score is not None else "",
        "steps": res.steps,
        "goal_switch_rate_per_100": f"{m.goal_switch_rate_per_100:.6f}",
    }
    wh, lf = walked_exposure(env, res.logs)
    row["walked_hits_per_step"] = f"{wh:.6f}"
    row["los_frac"] = f"{lf:.6f}"
    taken = sum(a.hits_taken for a in env.agents.values() if a.team == 0)
    alive_steps = sum(1 for l in res.logs if l.team == 0)
    row["hits_taken"] = taken
    row["hits_taken_per_step"] = f"{(taken / alive_steps) if alive_steps else 0.0:.6f}"
    # (2026-09-25) behavioural measures for the fitting fingerprint (additive columns; nothing above changes):
    # kills and deaths per 100 alive agent-steps of team 0, and item control, the share of team 0's good-status
    # alive steps (health and ammunition above the low thresholds) spent on the Resource goal
    row["kill_rate_per_100"] = f"{(100.0 * kills / alive_steps) if alive_steps else 0.0:.6f}"
    row["death_rate_per_100"] = f"{(100.0 * deaths / alive_steps) if alive_steps else 0.0:.6f}"
    good = [l for l in res.logs if l.team == 0 and not l.status_bad]
    row["resource_goal_share_good"] = f"{(sum(l.goal_type == 'resource' for l in good) / len(good)) if good else 0.0:.6f}"
    # (2026-09-26) measures that separate the source-based AssaultCube and Xonotic logics (additive columns; the
    # 10-cell radius is AssaultCube's hunting range); empty where the situation never occurs
    from .world import euclidean
    by_step: Dict[int, list] = {}
    for l in res.logs:
        by_step.setdefault(l.step, []).append(l)
    retreat = [0, 0]
    far = [0, 0]
    contact: List[float] = []
    trip: List[float] = []
    for ls in by_step.values():
        opp = [l.pos for l in ls if l.team != 0]
        for l in ls:
            if l.team != 0:
                continue
            dmin = min((euclidean(l.pos, o) for o in opp), default=None)
            if l.status_bad and l.enemy_visible:
                retreat[1] += 1
                retreat[0] += l.goal_type == "resource"
            if dmin is None or dmin > 10.0:
                far[1] += 1
                far[0] += l.goal_type == "enemy"
            if l.enemy_visible and dmin is not None:
                contact.append(dmin)
            if l.goal_type == "resource" and l.goal_pos is not None:
                trip.append(euclidean(l.pos, l.goal_pos))
    row["retreat_share"] = f"{retreat[0] / retreat[1]:.6f}" if retreat[1] else ""
    row["far_pursuit_share"] = f"{far[0] / far[1]:.6f}" if far[1] else ""
    row["contact_distance"] = f"{sum(contact) / len(contact):.6f}" if contact else ""
    row["resource_trip_distance"] = f"{sum(trip) / len(trip):.6f}" if trip else ""
    return row, env


def run_condition(
    scenario: ScenarioConfig,
    style: PriorityWeights,
    styles: Dict[str, PriorityWeights],
    episodes: int,
    base_seed: int,
    keys: Dict[str, object],
    map_cfg: MapConfig = MAP_CFG,
) -> List[Dict[str, object]]:
    """Run `episodes` episodes of one condition; `keys` are prepended to every row."""
    rows = []
    for ep in range(episodes):
        row = dict(keys)
        row["episode"] = ep
        row.update(run_episode(scenario, style, styles, episode_seed(base_seed, scenario.name, ep), map_cfg))
        rows.append(row)
    return rows


def write_csv(path: Path, key_columns: Sequence[str], rows: Iterable[Dict[str, object]],
              extra_columns: Sequence[str] = ()) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(key_columns) + ["episode"] + METRIC_COLUMNS + list(extra_columns))
        w.writeheader()
        for row in rows:
            w.writerow(row)
    return path
