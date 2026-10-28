from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import math
import random

from .astar import astar_search
from .config import AgentConfig, PriorityWeights, WeaponConfig
from .entities import Agent, Item
from .world import BlockedView, GridWorld, Vec2, bresenham_line, euclidean, manhattan


def _nearest(pos: Vec2, targets: List[Vec2]) -> Optional[Tuple[Vec2, float]]:
    if not targets:
        return None
    best = None
    best_d = 1e9
    for t in targets:
        d = euclidean(pos, t)
        if d < best_d:
            best_d = d
            best = t
    return (best, best_d) if best is not None else None


def _visible_enemies(world: GridWorld, agent: Agent, agents: Dict[int, Agent], cfg: AgentConfig) -> List[int]:
    visible: List[int] = []
    for other_id, other in agents.items():
        if not other.alive or other.team == agent.team:
            continue
        if euclidean(agent.pos, other.pos) <= cfg.view_radius and world.los_clear(agent.pos, other.pos):
            visible.append(other_id)
    return visible


def _status_bad(agent: Agent, cfg: AgentConfig) -> bool:
    return (agent.health <= cfg.low_health_threshold) or (agent.ammo <= cfg.low_ammo_threshold)


def _needed_resource(agent: Agent, cfg: AgentConfig) -> str:
    # If both are bad, prioritize health.
    if agent.health <= cfg.low_health_threshold:
        return "health"
    if agent.ammo <= cfg.low_ammo_threshold:
        return "ammo"
    # Default
    return "health"


def _safe_item(
    world: GridWorld,
    agent: Agent,
    items: List[Item],
    enemy_positions: List[Vec2],
) -> Optional[Vec2]:
    """Pick an active item that is 'safe' relative to enemies."""
    candidates = [it for it in items if it.active]
    if not candidates:
        return None
    best_pos = None
    best_score = -1e9
    for it in candidates:
        # Safety: far from enemies, and ideally not in LOS.
        score = 0.0
        for ep in enemy_positions:
            d = euclidean(it.pos, ep)
            score += d
            if world.los_clear(it.pos, ep):
                score -= 3.0  # visible from enemy -> less safe
        if score > best_score:
            best_score = score
            best_pos = it.pos
    return best_pos


def _blocked_cell(agent: Agent, agents: Dict[int, Agent]) -> Optional[Vec2]:
    """Cell of the agent's last attempted move if that move was rejected because another agent holds the cell
    (local avoidance, AgentConfig.local_avoidance)."""
    last = agent.memory.last_move_to
    if last is None or last == agent.pos or manhattan(last, agent.pos) != 1:
        return None
    if any(a.alive and a.pos == last and a.agent_id != agent.agent_id for a in agents.values()):
        return last
    return None


def infer_combat_mode(style: PriorityWeights, enemy_visible: bool, status_bad: bool) -> int:
    """
    Return the style's pinned combat-movement mode:
    0: hold, 1: keep moving, 2: chase, 3: evade.

    Modes only take effect while an enemy is visible (see `decide`). A style
    without a pinned mode defaults to keep moving, i.e. pure weighted selection.
    """
    if style.combat_mode_override is not None:
        return style.combat_mode_override
    return 1


@dataclass
class PolicyOutput:
    goal_type: str
    goal_pos: Optional[Vec2]
    move_to: Optional[Vec2]
    allow_move: bool
    shoot_target: Optional[int]


# Floor of the zero-centred ("centred") route cost; keeps step costs positive.
CENTRED_EPS = 0.1


class PriorityPolicy:
    """
    Priority-structure + risk-aware A* navigation policy.

    The policy is intentionally lightweight and interpretable:
    - high-level goal selection via weighted utilities + commitment penalty
    - path planning via A* with step cost augmented by risk/team terms
    - optionally, a risk budget converted into w_exposure per plan
    """

    # Risk-budget conversion (Lagrangian bisection over w_exposure)
    LAMBDA_MAX = 50.0
    BISECTION_STEPS = 8

    def __init__(
        self,
        style: PriorityWeights,
        agent_cfg: AgentConfig,
        weapon_cfg: WeaponConfig,
        rng: random.Random,
    ):
        self.style = style
        self.agent_cfg = agent_cfg
        self.weapon_cfg = weapon_cfg
        self.rng = rng
        # One entry per plan when a risk budget is active (read by the budget experiment).
        self.plan_log: List[Dict[str, float]] = []
        # One entry per plan when style.route_diagnostics is set (route-metric experiment):
        # (planned length, shortest length, differs from the shortest path, exposure along the
        # planned path, exposure along the shortest path)
        self.route_log: List[Tuple[int, int, int, float, float]] = []
        self._last_plan_step = -10**9
        # Steps spent on the current goal type, the current step included (read by min_dwell_steps).
        self._goal_age = 0

    def decide(
        self,
        world: GridWorld,
        agent: Agent,
        agents: Dict[int, Agent],
        items: List[Item],
        objective: Optional[Vec2],
        step: int,
    ) -> PolicyOutput:
        # 1) Perception
        vis_enemy_ids = _visible_enemies(world, agent, agents, self.agent_cfg)
        enemy_visible = len(vis_enemy_ids) > 0
        status_bad = _status_bad(agent, self.agent_cfg)

        enemy_positions = [agents[eid].pos for eid in vis_enemy_ids if agents[eid].alive]
        if enemy_visible:
            # Track nearest visible enemy
            nearest_enemy_id = min(vis_enemy_ids, key=lambda eid: euclidean(agent.pos, agents[eid].pos))
            agent.memory.last_seen_enemy_pos = agents[nearest_enemy_id].pos
        elif (self.agent_cfg.forget_reached_memory and agent.memory.last_seen_enemy_pos is not None
              and not agent.memory.evade_active
              and euclidean(agent.pos, agent.memory.last_seen_enemy_pos) <= 1.5):
            agent.memory.last_seen_enemy_pos = None   # reached, nobody there: drop the stale memory
        nearest_enemy_id = None
        if enemy_visible:
            nearest_enemy_id = min(vis_enemy_ids, key=lambda eid: euclidean(agent.pos, agents[eid].pos))

        # 2) Combat movement mode
        combat_mode = infer_combat_mode(self.style, enemy_visible=enemy_visible, status_bad=status_bad)

        # 3) Candidate goals
        candidates: List[Tuple[str, Vec2, float]] = []

        # Utility helpers (bounded [0,1] roughly)
        # (2026-09-29) distance discount of the form variants (distance_utility, distance_scale); the defaults
        # ("inverse", 1) give exactly the main model's 1 / (1 + d)
        tau = self.style.distance_scale
        if self.style.distance_utility == "inverse":
            def inv_dist_utility(d: float) -> float:
                return 1.0 / (1.0 + d / tau)
        elif self.style.distance_utility == "exp":
            def inv_dist_utility(d: float) -> float:
                return math.exp(-d / tau)
        else:
            raise ValueError(f"unknown distance_utility: {self.style.distance_utility!r}")

        # Objective goal
        if objective is not None:
            d_obj = manhattan(agent.pos, objective)
            candidates.append(("objective", objective, inv_dist_utility(d_obj)))

        # Resource goal
        active_items = [it for it in items if it.active]
        if active_items:
            kind = _needed_resource(agent, self.agent_cfg)
            needed = [it.pos for it in active_items if it.kind == kind]
            if not needed:
                needed = [it.pos for it in active_items]
            nearest = _nearest(agent.pos, needed)
            if nearest is not None:
                it_pos, d_it = nearest
                severity = 1.0
                if agent.health <= self.agent_cfg.low_health_threshold:
                    severity = min(1.0, (self.agent_cfg.low_health_threshold - agent.health) / self.agent_cfg.low_health_threshold + 0.3)
                if agent.ammo <= self.agent_cfg.low_ammo_threshold:
                    severity = max(severity, min(1.0, (self.agent_cfg.low_ammo_threshold - agent.ammo) / (self.agent_cfg.low_ammo_threshold + 1) + 0.3))
                # If not bad, down-weight the utility.
                # (2026-09-25) distance scale and idle factor are style parameters; the defaults (1, 0.25) give
                # exactly the main model's 1 / (1 + d) and soft gate
                base_u = inv_dist_utility(d_it / self.style.resource_distance_scale) * (
                    1.0 if status_bad else self.style.resource_idle_factor)
                candidates.append(("resource", it_pos, base_u * severity))

        # Teammate goal (regroup incentive). With goal termination, a teammate within one cell means the
        # goal is achieved: no candidate, and no switching penalty when leaving it.
        teammate_positions = [a.pos for a in agents.values() if a.alive and a.team == agent.team and a.agent_id != agent.agent_id]
        regrouped = False
        if teammate_positions:
            nearest_tm = _nearest(agent.pos, teammate_positions)
            if nearest_tm is not None:
                tm_pos, d_tm = nearest_tm
                regrouped = self.style.teammate_goal_terminates and d_tm <= 1.5
                if not regrouped:
                    # High utility when far apart
                    u_tm = min(1.0, d_tm / max(1.0, self.agent_cfg.view_radius))
                    candidates.append(("teammate", tm_pos, u_tm))

        # Enemy goal (only if visible or remembered)
        if enemy_visible and nearest_enemy_id is not None:
            epos = agents[nearest_enemy_id].pos
            d_e = manhattan(agent.pos, epos)
            candidates.append(("enemy", epos, inv_dist_utility(d_e)))
        elif agent.memory.last_seen_enemy_pos is not None:
            epos = agent.memory.last_seen_enemy_pos
            d_e = manhattan(agent.pos, epos)
            candidates.append(("enemy", epos, inv_dist_utility(d_e) * 0.4))  # stale info
        # (2026-09-25) optional perception of unseen opponents (hunt_unseen > 0; off in the main model)
        if self.style.hunt_unseen > 0 and not enemy_visible:
            opp = _nearest(agent.pos, [a.pos for a in agents.values() if a.alive and a.team != agent.team])
            if opp is not None:
                candidates.append(("enemy", opp[0], self.style.hunt_unseen * inv_dist_utility(manhattan(agent.pos, opp[0]))))

        # Roam goal (fallback)
        if not candidates:
            # Random nearby point
            roam = world.random_empty_cell(self.rng)
            candidates.append(("roam", roam, 0.1))

        # 4) Override goal selection based on combat mode
        forced_goal: Optional[Tuple[str, Vec2]] = None
        # Evade hysteresis: the evade mode switches on when an enemy is visible and stays on, driven by
        # the remembered enemy position, until that position is at least evade_release_radius away.
        threat_pos: Optional[Vec2] = agents[nearest_enemy_id].pos if (enemy_visible and nearest_enemy_id is not None) else None
        evading = False
        if combat_mode == 3:
            if enemy_visible:
                agent.memory.evade_active = True
            elif agent.memory.evade_active:
                mem = agent.memory.last_seen_enemy_pos
                if mem is not None and euclidean(agent.pos, mem) < self.agent_cfg.evade_release_radius:
                    threat_pos = mem
                else:
                    agent.memory.evade_active = False
            evading = agent.memory.evade_active and threat_pos is not None
        if enemy_visible or evading:
            if combat_mode == 2 and nearest_enemy_id is not None:
                forced_goal = ("enemy", agents[nearest_enemy_id].pos)
            elif combat_mode == 3 and evading:
                # If bad status, prefer a safe resource; else flee away from nearest enemy.
                if active_items and status_bad:
                    safe = _safe_item(world, agent, active_items, enemy_positions if enemy_positions else [threat_pos])
                    if safe is not None:
                        forced_goal = ("resource", safe)
                if forced_goal is None and threat_pos is not None:
                    # Flee target: take a point opposite enemy direction.
                    ax, ay = agent.pos
                    ex, ey = threat_pos
                    dx = ax - ex
                    dy = ay - ey
                    # Normalize to step of view radius
                    scale = max(1, self.agent_cfg.view_radius // 2)
                    fx = max(0, min(world.width - 1, ax + int(math.copysign(scale, dx)) if dx != 0 else ax))
                    fy = max(0, min(world.height - 1, ay + int(math.copysign(scale, dy)) if dy != 0 else ay))
                    flee = (fx, fy)
                    if not world.passable(flee):
                        # Blocked flee cell (2026-09-23 fix): take the nearest passable cell to it that is
                        # farther from the threat than the agent, instead of falling back to the weighted
                        # selection (which alternated with the flee goal step by step).
                        d_now = euclidean(agent.pos, threat_pos)
                        best = None
                        for rr in range(1, scale + 1):
                            ring = [(flee[0] + ix, flee[1] + iy) for ix in range(-rr, rr + 1) for iy in range(-rr, rr + 1)
                                    if max(abs(ix), abs(iy)) == rr]
                            ok = [c for c in ring if world.passable(c) and euclidean(c, threat_pos) > d_now]
                            if ok:
                                best = min(ok, key=lambda c: (euclidean(c, flee), -euclidean(c, threat_pos)))
                                break
                        flee = best
                    if flee is not None:
                        forced_goal = ("roam", flee)

        # 5) Score candidates
        def weight_for(goal_type: str) -> float:
            if goal_type == "objective":
                return self.style.w_objective
            if goal_type == "enemy":
                return self.style.w_engage
            if goal_type == "resource":
                return self.style.w_resource
            if goal_type == "teammate":
                return self.style.w_team
            return 0.1

        chosen_type = None
        chosen_pos = None
        best_score = -1e9

        incumbent = agent.memory.current_goal_type
        if regrouped and incumbent == "teammate":
            incumbent = "none"          # the regroup goal has been reached: commitment resets
        if not candidates:
            candidates.append(("roam", world.random_empty_cell(self.rng), 0.1))

        if forced_goal is not None:
            chosen_type, chosen_pos = forced_goal
        else:
            pool = candidates
            # (2026-09-29) optional minimum dwell time (min_dwell_steps; 0 = main model): the incumbent type is kept
            # while it has been held for fewer than N steps and is still a candidate
            if incumbent != "none" and self._goal_age < self.style.min_dwell_steps:
                pool = [c for c in candidates if c[0] == incumbent] or candidates
            for gtype, gpos, util in pool:
                score = weight_for(gtype) * util
                # commitment penalty for switching away from current goal type
                if incumbent != "none" and gtype != incumbent:
                    penalty = self.style.w_commitment
                    # (2026-09-26) optional relief for an urgent switch to an item (urgent_switch_relief; 0 = main model)
                    if status_bad and gtype == "resource":
                        penalty *= 1.0 - self.style.urgent_switch_relief
                    score -= penalty
                if score > best_score:
                    best_score = score
                    chosen_type, chosen_pos = gtype, gpos

        assert chosen_type is not None
        # Hold mode: keep the goal but block movement while shooting
        allow_move = True
        if enemy_visible and combat_mode == 0:
            allow_move = False

        # 6) Path planning (risk-aware A*)
        move_to: Optional[Vec2] = None
        blocked = _blocked_cell(agent, agents) if self.agent_cfg.local_avoidance else None
        if allow_move and chosen_pos is not None:
            need_replan = blocked is not None
            if agent.memory.current_goal_pos != chosen_pos or agent.memory.current_goal_type != chosen_type:
                need_replan = True
            if not agent.memory.planned_path:
                need_replan = True
            # If next step blocked, replan
            if agent.memory.planned_path and (not world.passable(agent.memory.planned_path[0])):
                need_replan = True
            # If the previous move was rejected (cell occupied), the popped path no longer
            # starts next to the agent; replan so that every move stays 4-adjacent.
            if agent.memory.planned_path and manhattan(agent.memory.planned_path[0], agent.pos) != 1:
                need_replan = True
            # Optional periodic replanning, so that route costs follow moving opponents.
            if self.style.replan_interval > 0 and step - self._last_plan_step >= self.style.replan_interval:
                need_replan = True

            if need_replan:
                # (a detour is pointless when the held cell is the goal itself: the goal would be unreachable)
                path = (self._plan(BlockedView(world, {blocked}), agent, agents, chosen_pos)
                        if blocked is not None and blocked != chosen_pos else None)
                if not path:
                    path = self._plan(world, agent, agents, chosen_pos)
                agent.memory.planned_path = path[1:] if path else []  # drop current cell
                self._last_plan_step = step
            # Pop next move
            if agent.memory.planned_path:
                move_to = agent.memory.planned_path.pop(0)

        # 7) Shooting: shoot nearest visible enemy if in range and ammo.
        shoot_target: Optional[int] = None
        if enemy_visible and nearest_enemy_id is not None:
            d = euclidean(agent.pos, agents[nearest_enemy_id].pos)
            if d <= self.weapon_cfg.range_cells and agent.ammo >= self.weapon_cfg.ammo_per_shot:
                shoot_target = nearest_enemy_id

        # Update memory goal
        self._goal_age = self._goal_age + 1 if chosen_type == agent.memory.current_goal_type else 1
        agent.memory.current_goal_type = chosen_type
        agent.memory.current_goal_pos = chosen_pos
        agent.memory.last_visible_enemies = vis_enemy_ids
        agent.memory.last_move_to = move_to

        return PolicyOutput(
            goal_type=chosen_type,
            goal_pos=chosen_pos,
            move_to=move_to,
            allow_move=allow_move,
            shoot_target=shoot_target,
        )

    def _plan(self, world: GridWorld, agent: Agent, agents: Dict[int, Agent], goal: Vec2) -> Optional[List[Vec2]]:
        # Context for costs
        if self.style.threat_knowledge == "memory":
            enemy_positions = [agents[eid].pos for eid in _visible_enemies(world, agent, agents, self.agent_cfg)]
            mem = agent.memory.last_seen_enemy_pos
            if mem is not None and mem not in enemy_positions:
                enemy_positions.append(mem)
        else:
            enemy_positions = [a.pos for a in agents.values() if a.alive and a.team != agent.team]
        teammate_positions = [a.pos for a in agents.values() if a.alive and a.team == agent.team and a.agent_id != agent.agent_id]

        # Per-cell cost terms; positions are fixed during one planning call, so cache them.
        cache: Dict[Vec2, Tuple[float, float, float]] = {}

        def terms(v: Vec2) -> Tuple[float, float, float]:
            t = cache.get(v)
            if t is None:
                # Exposure risk: prefer cells not in LOS of enemies, and far away.
                exposure = 0.0
                if self.style.exposure_model == "hits":
                    rng_cells = float(self.weapon_cfg.range_cells)
                    for ep in enemy_positions:
                        d = euclidean(v, ep)
                        if d <= rng_cells and world.los_clear(v, ep):
                            exposure += self.weapon_cfg.base_accuracy * max(0.05, 1.0 - 0.7 * d / rng_cells)
                elif self.style.exposure_model == "anticipatory":
                    rng_cells = float(self.weapon_cfg.range_cells)
                    t_arrive = float(manhattan(agent.pos, v))
                    for ep in enemy_positions:
                        dw = self._walking_distances(world, ep)
                        if v not in dw:
                            continue
                        eff = max(0.0, float(dw[v]) - t_arrive)
                        if eff <= rng_cells:
                            exposure += self.weapon_cfg.base_accuracy * max(0.05, 1.0 - 0.7 * eff / rng_cells)
                else:
                    for ep in enemy_positions:
                        d = euclidean(v, ep)
                        if d < 0.5:
                            d = 0.5
                        if world.los_clear(v, ep):
                            exposure += 1.0 / d
                        else:
                            exposure += 0.2 / d
                # Environmental risk: lack of cover
                if self.style.cover_model == "threat":
                    open_area = 1.0 - self._threat_cover(world, v, enemy_positions)
                else:
                    open_area = 1.0 - world.cover_score(v)
                # Teammate separation penalty (encourages cohesion)
                sep = 0.0
                if teammate_positions:
                    d_tm = min(euclidean(v, tp) for tp in teammate_positions)
                    sep = d_tm / max(1.0, float(self.agent_cfg.view_radius))
                t = (exposure, open_area, sep)
                cache[v] = t
            return t

        if self.style.route_cost == "additive":
            def search(w_exposure: float) -> Optional[List[Vec2]]:
                def step_cost(u: Vec2, v: Vec2) -> float:
                    exposure, open_area, sep = terms(v)
                    return 1.0 + w_exposure * exposure + self.style.w_cover * open_area + self.style.w_teammate_sep * sep

                res = astar_search(world, agent.pos, goal, step_cost=step_cost)
                return res.path if res is not None else None
        else:
            search = self._alt_search(world, agent, goal, terms, enemy_positions, teammate_positions)

        if self.style.risk_budget is None:
            path = search(self.style.w_exposure)
        else:
            path = self._plan_with_budget(search, lambda path: sum(terms(v)[0] for v in path[1:]))
        if self.style.route_diagnostics and path:
            res0 = astar_search(world, agent.pos, goal, step_cost=lambda u, v: 1.0)
            path0 = res0.path if res0 is not None else path
            self.route_log.append((len(path) - 1, len(path0) - 1, int(path != path0),
                                   sum(terms(v)[0] for v in path[1:]), sum(terms(v)[0] for v in path0[1:])))
        return path

    def _alt_search(self, world: GridWorld, agent: Agent, goal: Vec2, terms, enemy_positions: List[Vec2],
                    teammate_positions: List[Vec2]):
        """Search function for the alternative route costs (style.route_cost != "additive").

        "centred": max(eps, 1 + lambda_E E - lambda_C Cover + lambda_T Sep); the heuristic is
        scaled by the smallest possible step cost so that A* stays optimal.
        "exp": exp(lambda_E Phi_E - lambda_C Cover - lambda_A Phi_A) with lambda_A = w_teammate_sep:
        opponents stretch space (factor > 1), cover and teammates contract it (0 < factor < 1);
        the step cost is positive for any weights, and the heuristic is scaled by its lower bound.
        """
        s = self.style
        if s.route_cost == "centred":
            h_scale = max(CENTRED_EPS, 1.0 - s.w_cover)

            def search(w_exposure: float) -> Optional[List[Vec2]]:
                def step_cost(u: Vec2, v: Vec2) -> float:
                    exposure, open_area, sep = terms(v)
                    return max(CENTRED_EPS, 1.0 + w_exposure * exposure - s.w_cover * (1.0 - open_area)
                               + s.w_teammate_sep * sep)

                res = astar_search(world, agent.pos, goal, step_cost=step_cost,
                                   heuristic=lambda a, b: h_scale * manhattan(a, b))
                return res.path if res is not None else None
            return search

        if s.route_cost == "exp":
            fields = [self._walking_distances(world, ep) for ep in enemy_positions] \
                if s.threat_field == "geodesic" else None
            cache: Dict[Vec2, Tuple[float, float, float]] = {}

            def potentials(v: Vec2) -> Tuple[float, float, float]:
                t = cache.get(v)
                if t is None:
                    exposure, open_area, _ = terms(v)
                    phi_e = exposure if fields is None else sum(1.0 / max(f[v], 0.5) for f in fields if v in f)
                    phi_a = sum(1.0 / max(euclidean(v, tp), 1.0) for tp in teammate_positions)
                    t = (phi_e, 1.0 - open_area, phi_a)
                    cache[v] = t
                return t

            g_min = math.exp(-s.w_cover - s.w_teammate_sep * len(teammate_positions))

            if s.risk_budget is not None:
                # Risk budget: exposure enters as a linear price mu * E(v) on top of the exponential
                # metric of the remaining terms, so the budget-to-weight conversion stays a
                # Lagrangian relaxation (path exposure is non-increasing in mu).
                def search(mu: float) -> Optional[List[Vec2]]:
                    def step_cost(u: Vec2, v: Vec2) -> float:
                        _, cover, phi_a = potentials(v)
                        return math.exp(-s.w_cover * cover - s.w_teammate_sep * phi_a) + mu * terms(v)[0]

                    res = astar_search(world, agent.pos, goal, step_cost=step_cost,
                                       heuristic=lambda a, b: g_min * manhattan(a, b))
                    return res.path if res is not None else None
                return search

            def search(w_exposure: float) -> Optional[List[Vec2]]:
                def step_cost(u: Vec2, v: Vec2) -> float:
                    phi_e, cover, phi_a = potentials(v)
                    return math.exp(w_exposure * phi_e - s.w_cover * cover - s.w_teammate_sep * phi_a)

                res = astar_search(world, agent.pos, goal, step_cost=step_cost,
                                   heuristic=lambda a, b: g_min * manhattan(a, b))
                return res.path if res is not None else None
            return search

        if s.route_cost == "square":
            def search(w_exposure: float) -> Optional[List[Vec2]]:
                def step_cost(u: Vec2, v: Vec2) -> float:
                    exposure, open_area, sep = terms(v)
                    return 1.0 + w_exposure * exposure * exposure + s.w_cover * open_area + s.w_teammate_sep * sep

                res = astar_search(world, agent.pos, goal, step_cost=step_cost)
                return res.path if res is not None else None
            return search

        raise ValueError(f"unknown route_cost: {s.route_cost!r}")

    @staticmethod
    def _walking_distances(world: GridWorld, src: Vec2) -> Dict[Vec2, int]:
        """4-neighbour walking distances from src over passable cells (cached per world)."""
        cache = world.__dict__.setdefault("_walking_distance_cache", {})
        dist = cache.get(src)
        if dist is None:
            dist = {src: 0}
            frontier = [src]
            while frontier:
                nxt = []
                for p in frontier:
                    for q in world.neighbors4(p):
                        if q not in dist:
                            dist[q] = dist[p] + 1
                            nxt.append(q)
                frontier = nxt
            cache[src] = dist
        return dist

    @staticmethod
    def _threat_cover(world: GridWorld, v: Vec2, enemy_positions: List[Vec2]) -> float:
        """Threat-relative cover in [0, 1]: proximity-weighted share of living opponents for
        which the next cell from v toward the opponent is an obstacle (1 if no opponents)."""
        num = den = 0.0
        for ep in enemy_positions:
            wgt = 1.0 / max(euclidean(v, ep), 0.5)
            toward = bresenham_line(v, ep)[1:-1][:1]      # first cell toward the opponent
            num += wgt * float(any(c in world.obstacles for c in toward))
            den += wgt
        return num / den if den > 0 else 1.0

    def _plan_with_budget(self, search, risk) -> Optional[List[Vec2]]:
        """Smallest w_exposure whose path exposure meets the style's risk budget.

        relative:   budget = beta * R(P0)
        normalised: budget = R_min + beta * (R(P0) - R_min), R_min = exposure of the
                    w_exposure = LAMBDA_MAX path (always attainable within the family)
        """
        p0 = search(0.0)
        if p0 is None:
            return None
        r0 = risk(p0)
        beta = self.style.risk_budget
        p_hi = None
        r_min = float("nan")
        if self.style.risk_budget_mode == "normalised":
            p_hi = search(self.LAMBDA_MAX)
            r_min = min(risk(p_hi), r0) if p_hi is not None else r0
            budget = r_min + beta * (r0 - r_min)
        else:
            budget = beta * r0
        if r0 <= budget:                # exposure-blind path already within budget (e.g. beta = 1)
            best, lam = p0, 0.0
        else:
            if p_hi is None:
                p_hi = search(self.LAMBDA_MAX)
            if p_hi is None or risk(p_hi) > budget:
                best, lam = (p_hi or p0), self.LAMBDA_MAX   # infeasible within the weighted-sum family
            else:
                lo, hi, best = 0.0, self.LAMBDA_MAX, p_hi
                for _ in range(self.BISECTION_STEPS):
                    mid = 0.5 * (lo + hi)
                    p = search(mid)
                    if p is not None and risk(p) <= budget:
                        hi, best = mid, p
                    else:
                        lo = mid
                lam = hi
        r = risk(best)
        self.plan_log.append({"r0": r0, "r_min": r_min, "budget": budget, "r": r, "len0": len(p0) - 1,
                              "len": len(best) - 1, "lam": lam, "ok": float(r <= budget + 1e-9)})
        return best
