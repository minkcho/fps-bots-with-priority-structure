from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

Vec2 = Tuple[int, int]


@dataclass(frozen=True)
class MapConfig:
    """Grid-world map configuration."""
    width: int = 25
    height: int = 25
    obstacle_density: float = 0.18
    seed: int = 0

    # Item spawns
    num_health: int = 6
    num_ammo: int = 6
    item_respawn_steps: int = 40

    # Spawns / objective
    spawn_a: Vec2 = (2, 2)
    spawn_b: Vec2 = (22, 22)
    objective: Vec2 = (22, 2)  # used in mission/control scenarios
    # Distance (cells, along x toward the map interior) between the spawn cells of the two agents of
    # a team; 0 stacks both agents on one cell (v2). Adopted 2026-09-23: 2, so that the cohesion
    # metrics and the separation term are not pinned at their floor by a shared spawn cell.
    spawn_separation: int = 2

    # Layout: "random" (scattered obstacle cells, obstacle_density), "buildings"
    # (rectangular buildings separated by streets, building_density; more cover), or "custom"
    # (explicit obstacle cells in `obstacles`; added 2026-09-25 for the map sample and the game maps).
    layout: str = "random"
    building_density: float = 0.25
    obstacles: Tuple[Vec2, ...] = ()
    # Explicit spawn cells, one tuple per team indexed by the agent's index within the team (added
    # 2026-09-25 for the game-inspired maps, whose spawn cells are placed symmetrically by design);
    # empty: spawn_a / spawn_b and the spawn_separation rule.
    spawn_cells: Tuple[Tuple[Vec2, ...], ...] = ()
    # Fixed item cells, ((kind, cell), ...) with kind "health" or "ammo" (game-inspired maps: pickups at
    # fixed places, as in the games; num_health / num_ammo are then unused); empty: num_health health and
    # num_ammo ammunition items at random free cells, drawn once per episode.
    item_cells: Tuple[Tuple[str, Vec2], ...] = ()


@dataclass(frozen=True)
class WeaponConfig:
    range_cells: int = 7
    base_accuracy: float = 0.55  # hit probability at distance 0
    damage: int = 25
    ammo_per_shot: int = 1
    max_ammo: int = 30


@dataclass(frozen=True)
class AgentConfig:
    """Agent dynamics and thresholds (shared across styles)."""
    max_health: int = 100
    respawn_steps: int = 25

    # "Bad status" thresholds (used by the policy)
    low_health_threshold: int = 45
    low_ammo_threshold: int = 5

    # Perception
    view_radius: int = 9
    # Evade hysteresis (2026-09-23): once the evade mode is triggered by a visible enemy, it stays
    # active until the last-seen enemy position is at least this far away (or the agent respawns).
    # Setting it to view_radius reproduces the earlier behaviour (evade only while an enemy is
    # visible), which chattered at the edge of the view radius.
    evade_release_radius: float = 11.0
    # Movement rule (2026-09-25): when two teammates each want the other's cell, they exchange cells instead of
    # both moves being rejected (without it, such a pair can stay in place for the rest of an episode; see
    # experiments/analyze_stalls.py). Off by default, which reproduces the paper's final run; the environment
    # variable FPS_TEAMMATE_SWAP=1 switches it on for every run of a process (used by the pipeline scripts).
    teammate_swap: bool = field(default_factory=lambda: os.environ.get("FPS_TEAMMATE_SWAP", "0") == "1")
    # Local avoidance (2026-09-25): after a move was rejected because another agent holds the cell, the next plan
    # routes around that cell when such a route exists (otherwise the agent waits as before). Environment
    # variable FPS_LOCAL_AVOIDANCE=1.
    local_avoidance: bool = field(default_factory=lambda: os.environ.get("FPS_LOCAL_AVOIDANCE", "0") == "1")
    # Forget a reached enemy memory (2026-09-25): when no enemy is visible and the agent is within one cell of
    # the remembered last-seen enemy position (and not evading), the memory is dropped. Without it the stale
    # enemy goal keeps its highest utility at distance 0 and the agent can wait there for the rest of the
    # episode. Environment variable FPS_FORGET_MEMORY=1.
    forget_reached_memory: bool = field(default_factory=lambda: os.environ.get("FPS_FORGET_MEMORY", "0") == "1")


@dataclass(frozen=True)
class PriorityWeights:
    """
    Style/configuration parameters that encode the 'priority structure' and
    risk-sensitive navigation preferences.

    Higher is 'more important' for rewards/utility, higher cost weights mean
    'avoid more'.
    """
    name: str

    # High-level goal selection priorities
    w_objective: float
    w_engage: float
    w_resource: float
    w_team: float
    w_commitment: float  # penalty for switching goals

    # Navigation (risk-aware A*) weights
    w_exposure: float
    w_cover: float
    w_teammate_sep: float

    # Per-style pinned combat-movement mode, active while an enemy is visible:
    # 0: hold, 1: keep moving, 2: chase, 3: evade.
    # None defaults to keep moving (pure weighted goal selection).
    combat_mode_override: Optional[int] = None

    # Optional risk budget beta in [0, 1] (additional experiment). When set, w_exposure is
    # replaced per plan by the smallest value whose path exposure meets the budget
    # (Lagrangian bisection; see PriorityPolicy._plan_with_budget and risk_budget_mode).
    risk_budget: Optional[float] = None
    # "relative":   budget = beta * R(P0)                       (P0: exposure-blind path)
    # "normalised": budget = R_min + beta * (R(P0) - R_min)     (R_min: safest path in the family)
    risk_budget_mode: str = "relative"

    # Cover term of the route cost (lambda_C * (1 - Cover(v))):
    # "adjacency": fraction of blocked 4-neighbours (default; independent of threats)
    # "threat":    threat-relative cover, i.e. the proximity-weighted fraction of living
    #              opponents whose line of sight from v is blocked by the next cell toward them
    cover_model: str = "adjacency"

    # Form of the route cost (additional experiment "route metric"):
    # "additive": 1 + lambda_E * E + lambda_C * (1 - Cover) + lambda_T * Sep         (default)
    # "centred":  max(eps, 1 + lambda_E * E - lambda_C * Cover + lambda_T * Sep)     (zero-centred cover)
    # "exp":      exp(lambda_E * Phi_E - lambda_C * Cover - lambda_A * Phi_A)         (exponential metric;
    #             lambda_A = w_teammate_sep, Phi_A = sum over teammates of 1 / max(d, 1))
    # "square":   1 + lambda_E * E^2 + lambda_C * (1 - Cover) + lambda_T * Sep       (H3 probe, 2026-09-22)
    route_cost: str = "additive"
    # Opponent potential Phi_E of the "exp" route cost: "los" = the exposure E(v) of the
    # additive cost; "geodesic" = sum over opponents of 1 / max(walking distance, 0.5)
    threat_field: str = "los"
    # 0: replan only on events (goal change, blocked or exhausted path); N > 0: also every N steps
    replan_interval: int = 0
    # Record per-plan route diagnostics in PriorityPolicy.route_log (route-metric experiment)
    route_diagnostics: bool = False
    # Exposure term E(v) of the route cost (H3 diagnosis, 2026-09-22):
    # "distance": sum over living opponents of kappa / max(d, 0.5), kappa = 1 in LOS else 0.2   (paper v2)
    # "hits":     expected hits per step, sum over opponents in LOS and within weapon range of the
    #             testbed hit probability base_accuracy * max(0.05, 1 - 0.7 d / range); zero out of LOS/range
    # "anticipatory": time-to-contact field: for each opponent the hit probability at the effective
    #             distance max(0, d_walk(e, v) - t(v)), where d_walk is the walking distance around
    #             obstacles and t(v) the Manhattan distance from the planning agent to v (arrival-time
    #             proxy, opponent closing in at one cell per step); zero beyond the weapon range; no LOS gate
    exposure_model: str = "distance"
    # Goal termination (2026-09-23, adopted after the regroup-stall diagnosis): when the nearest
    # teammate is within one cell (8-neighbourhood), the Teammate goal counts as achieved: it is
    # dropped from the candidates for that step and, if it is the incumbent, the switching penalty
    # is waived (reaching a goal resets commitment, like a respawn). False reproduces v2, in which
    # a regrouped pair could stay on the Teammate goal indefinitely.
    teammate_goal_terminates: bool = True
    # Opponents that enter the exposure term:
    # "all":    every living opponent (omniscient planner, paper v2)
    # "memory": opponents visible now plus the remembered last-seen position (partial observability)
    threat_knowledge: str = "all"
    # Goal-utility shape parameters (2026-09-25, parameter-regression extension of the fitting experiment; the
    # defaults reproduce the main model exactly).
    # resource_idle_factor: multiplier of the Resource utility while the status is fine (the soft status gate of R4);
    #   0 makes the gate hard, so that items compete for the goal only in low status.
    resource_idle_factor: float = 0.25
    # resource_distance_scale: tau in U_Res = severity / (1 + d / tau); tau = 1 is the main model's 1 / (1 + d). A large
    #   tau makes the utility almost independent of distance, so that a large w_resource puts items first in low
    #   status whatever their distance (a condition-first rule).
    resource_distance_scale: float = 1.0
    # hunt_unseen: eta >= 0. While no enemy is visible, an Enemy candidate at the nearest living opponent's true
    #   position with utility eta / (1 + d) (Manhattan), i.e. perception of unseen opponents as in the reconstructed
    #   AssaultCube and Xonotic logics. 0 = the main model (Enemy candidates only for visible or remembered enemies).
    hunt_unseen: float = 0.0
    # urgent_switch_relief: rho in [0, 1] (2026-09-26, fitting Part F). While the status is poor, the commitment
    #   penalty for switching to the Resource goal is multiplied by (1 - rho), so that a weakened agent can leave a
    #   fight for an item however large the penalty that keeps its other goals stable. 0 = the main model.
    urgent_switch_relief: float = 0.0
    # Form variants (2026-09-29, round v13; the defaults reproduce the main model exactly).
    # distance_utility, distance_scale: the distance discount U(d) of the Objective, Enemy and Resource utilities,
    #   "inverse" 1 / (1 + d / tau) or "exp" exp(-d / tau) with tau = distance_scale (for the Resource utility d is
    #   d / resource_distance_scale); ("inverse", 1) is the main model's 1 / (1 + d). The Teammate utility
    #   min(1, d / view radius) is not a discount and keeps its form.
    distance_utility: str = "inverse"
    distance_scale: float = 1.0
    # min_dwell_steps: N >= 0, a minimum dwell time as persistence device. After the goal type changes, the weighted
    #   selection keeps that type for N steps (the step of the change included) while it is still a candidate; forced
    #   goals of the chase and evade modes take precedence, and a reached regroup goal or a respawn ends the dwell as it
    #   ends the incumbent. Used with w_commitment = 0 in place of the switching penalty. 0 = the main model.
    min_dwell_steps: int = 0


@dataclass(frozen=True)
class ScenarioConfig:
    """Defines what the environment asks agents to do."""
    name: str
    mode: str  # 'deathmatch', 'mission', 'team_deathmatch', 'control'
    max_steps: int = 600
    num_agents_per_team: int = 2
    score_to_win: int = 120  # used in control mode (seconds/steps on point)

    # Whether the blue team is evaluated and the red team acts as a fixed opponent style.
    opponent_style: str = "Aggressive"
    # If True, both teams use the same style (not recommended for behaviour comparisons).
    symmetric_styles: bool = False


@dataclass(frozen=True)
class ExperimentConfig:
    map_cfg: MapConfig
    agent_cfg: AgentConfig
    weapon_cfg: WeaponConfig
    scenarios: List[ScenarioConfig]
    styles: List[PriorityWeights]
    episodes: int = 20
    seed: int = 123
    out_dir: str = "outputs"
