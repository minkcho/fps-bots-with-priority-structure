"""External baselines (paper: "External baselines").

Four behaviour trees implement the reconstructed pseudocode of the four case-study games
(paper Fig. 2) as fixed decision logic, and one utility AI scores the candidate goals with
multiplicative response curves. All baselines use distance-only A* (no route shaping), no
goal-persistence device, and the same perception, movement, and shooting rules as the
priority-structure policy, so the behavioural metrics are computed identically.

  CSO-BT  enemy visible -> attack and hold position; otherwise the lowest-id living team
          member leads toward the objective and the other follows it (follows while more
          than one cell away, otherwise heads for the objective). Without an objective:
          last-seen enemy, else roam. No item logic (pickups only when walked over).
  OW-BT   enemy visible -> attack while moving (movement goal unchanged); health low ->
          nearest health item; teammate within 2 cells -> objective; teammate within view
          radius -> regroup; otherwise objective. Without an objective the objective
          branches fall back to the last-seen enemy, else roam.
  AC-BT   (revised 2026-09-25 from the AssaultCube bot source, refs/game_sources/assaultcube: CBot::MainAI,
          FindEnemy, CheckHunt, DoCombatNav, CACBot::SearchForEnts) a fixed priority chain: enemy visible ->
          attack and chase it (in combat, an ammunition item within 3 cells only when ammunition is critical);
          otherwise hunt the nearest opponent within the hunting range (10 cells; AC: 250 units, following its
          recent positions); otherwise the best item the bot is missing (score on need, distance and visibility);
          otherwise roam.
  XO-BT   (revised 2026-09-25 from the Xonotic havocbot source, refs/game_sources/xonotic: havocbot_role_generic,
          havocbot_goalrating_items / _enemyplayers, navigation_routerating, healtharmor/ammo_pickupevalfunc,
          havocbot_ai) one rating scale: every item the bot is missing is rated by need (value x min(2, item
          amount / own amount); health 5000, ammunition 1500), every living opponent by relative strength (2500 x
          clamp(1 + (own health - its health) / 150, 0, 3)), each discounted by route length (12 / (12 + d); rangebias
          2000 units); the bot moves to the best-rated goal and shoots while moving. Since 2026-09-27 (user decision)
          the goal is kept until the strategy timer expires, as in the source (bot_ai_strategyinterval 7 s, 5.5 s for
          an opponent; xonotic-server.cfg): 15 and 12 steps at the scale of the rangebias conversion (2000 units = 12
          cells, movement 360 units/s = one cell per step, so a step is about 0.46 s); a goal that is gone forces a
          re-rating. The tree of fitting Parts D-F re-rated every step: BaselineStyle("XO-BT", "XO-BT") with the
          dataclass defaults (code tags v6- to v8-protocol-frozen).
  AC-BT-v1, XO-BT-v1  the earlier reconstructions (paper drafts up to 2026-09-25; Part B and Part C of the fitting):
          AC-BT-v1: status poor -> nearest needed item; registered enemy -> pursue it; otherwise the nearest living
          opponent. XO-BT-v1: status poor -> safest item if an enemy is visible, else nearest needed item;
          otherwise the nearest living opponent.
  Utility AI  argmax of: engage = visibility x max(0, 1 - (d/15)^2) x logistic((h-35)/10)
          (remembered enemy x 0.5); objective = 0.8 x (0.5 + 0.5 max(0, 1 - d/40));
          item = need^2 / (1 + d/6) with need = max(1 - h/100, 1 - a/30);
          regroup = 0.6 x min(1, d/r_view)^2; roam = 0.05.
As in the reconstructed logic, AC-BT-v1 and XO-BT-v1 head for the nearest opponent even when it is out of sight;
the revised AC-BT does so within its hunting range and the revised XO-BT rates every living opponent (as the
games' bots do).
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, replace
from typing import Dict, List, Optional, Tuple

from .astar import astar_search
from .config import AgentConfig, WeaponConfig
from .entities import Agent, Item
from .policy import (PolicyOutput, _blocked_cell, _nearest, _needed_resource, _safe_item, _status_bad,
                     _visible_enemies)
from .world import BlockedView, GridWorld, Vec2, euclidean, manhattan

KINDS = ("CSO-BT", "OW-BT", "AC-BT", "XO-BT", "UtilityAI")
LEGACY_KINDS = ("AC-BT-v1", "XO-BT-v1")    # earlier reconstructions, kept for reproducibility (not in default_baselines)

# Revised AssaultCube and Xonotic trees (2026-09-25): constants from the games' bot sources (see the module docstring)
AC_HUNT_RANGE = 10.0          # cells (AssaultCube hunts opponents within 250 units)
AC_COMBAT_ITEM_RANGE = 3.0    # cells (in combat, items within 25 units, only with critical ammunition)
XO_RANGE_BIAS = 12.0          # cells (rating discount rangebias / (rangebias + route cost), rangebias 2000 units)
XO_ENEMY_RATING = 2500.0      # BOT_RATING_ENEMY
XO_HEALTH_VALUE = 5000.0      # Health m_botvalue
XO_AMMO_VALUE = 1500.0        # Bullets / Rockets m_botvalue
XO_STRATEGY_STEPS = 15        # bot_ai_strategyinterval 7 s at 0.46 s per step (2026-09-27)
XO_STRATEGY_STEPS_MOVING = 12  # bot_ai_strategyinterval_movingtarget 5.5 s
# (2026-09-27, user decision after the tree review) early re-rating of the havocbot timer, in cells and steps at the same
# scale (167 units per cell, 0.46 s per step): a goal farther than 1.5 x sv_maxspeed = 540 units is re-rated in the last
# 2 s (static) / 3 s (moving goal) before the timer expires (navigation_goalrating_timeout_can_be_anticipated, checked at
# every waypoint the bot touches; on the grid at every step, an upper bound), and an opponent within MAX_CHASE_DISTANCE
# 700 units is re-rated at once when the straight walk to it fails (tracewalk every 0.25 s; on the grid: line of sight)
XO_ANTICIPATE_CELLS = 3.24
XO_ANTICIPATE_STEPS = 4
XO_ANTICIPATE_STEPS_MOVING = 6
XO_CHASE_CELLS = 4.2
# (2026-09-27, user decision) one length scale for the AssaultCube tree, anchored at the hunting range (250 units = 10
# cells, 25 units per cell); with the bot's maxspeed 22 units/s (bot.cpp) one step is about 1.14 s. Hunting follows
# CheckHunt / HuntEnemy: a new hunt is searched at most every 2nd step (1.5 s), its location is updated every 2nd step
# (1.25 s), and a failed hunt blocks hunting for 3 steps (3.5 s). The length of the players' position history is not in
# the sources we hold; 3 steps is an assumption.
AC_UNITS_PER_CELL = 25.0
AC_HUNT_HISTORY = 3
AC_HUNT_SEARCH_STEPS = 2
AC_HUNT_UPDATE_STEPS = 2
AC_HUNT_PAUSE_STEPS = 4


@dataclass(frozen=True)
class BaselineStyle:
    name: str
    kind: str  # one of KINDS
    # (2026-09-27) optional settings of the Xonotic tree for the conversion sensitivity check; the defaults reproduce
    # the revised tree exactly (rangebias 12 cells, goals re-rated every step, skill term 0 = the default skill 8).
    # xo_interval / xo_interval_moving: steps for which the chosen goal is kept before it is re-rated, for an item and
    #   for an opponent (havocbot strategy timer: bot_ai_strategyinterval 7 s, _movingtarget 5.5 s); a goal that is
    #   gone (item taken, opponent dead) or a respawn forces an immediate re-rating (navigation_goalrating_timeout_force)
    # xo_skill_bonus: 0.05 * max(0, 8 - skill), added to an opponent's strength factor (havocbot_goalrating_enemyplayers)
    xo_range_bias: float = XO_RANGE_BIAS
    xo_interval: int = 1
    xo_interval_moving: int = 1
    xo_skill_bonus: float = 0.0
    xo_early_rerating: bool = False
    # (2026-09-27) optional settings of the AssaultCube tree; the defaults reproduce the tree of 2026-09-25 (hunting range
    # 10 cells, in-combat items within 3 cells, item distance term 4 x cells; hunting the current position of the nearest
    # opponent within range). ac_units_per_cell > 0: one length scale for all three constants; ac_hunt_history > 0:
    # CheckHunt / HuntEnemy with that many steps of position history.
    ac_units_per_cell: float = 0.0
    ac_hunt_history: int = 0


def default_baselines() -> Dict[str, BaselineStyle]:
    out = {k: BaselineStyle(name=k, kind=k) for k in KINDS}
    # (2026-09-27) the Xonotic tree keeps its goal for the source's strategy interval (user decision)
    out["XO-BT"] = replace(out["XO-BT"], xo_interval=XO_STRATEGY_STEPS, xo_interval_moving=XO_STRATEGY_STEPS_MOVING,
                           xo_early_rerating=True)
    # (2026-09-27) the AssaultCube tree at one length scale, hunting as in the source (user decision)
    out["AC-BT"] = replace(out["AC-BT"], ac_units_per_cell=AC_UNITS_PER_CELL, ac_hunt_history=AC_HUNT_HISTORY)
    return out


class BaselinePolicy:
    def __init__(self, style: BaselineStyle, agent_cfg: AgentConfig, weapon_cfg: WeaponConfig,
                 rng: random.Random):
        assert style.kind in KINDS + LEGACY_KINDS, style.kind
        self.style = style
        self.agent_cfg = agent_cfg
        self.weapon_cfg = weapon_cfg
        self.rng = rng
        self.roam_target: Optional[Vec2] = None
        self.plan_log: List[Dict[str, float]] = []  # interface parity with PriorityPolicy
        self._step = 0
        self._xo_goal: Optional[Tuple[str, object, int]] = None   # strategy timer: (goal type, item or opponent id, expiry)
        self._xo_last_step = -10
        # AssaultCube hunting state (CheckHunt / HuntEnemy): position histories, hunt target and location, timers
        self._hist: Dict[int, List[Vec2]] = {}
        self._prev_enemy: Optional[int] = None
        self._hunt_target: Optional[int] = None
        self._hunt_loc: Optional[Vec2] = None
        self._prev_hunt_loc: Optional[Vec2] = None
        self._hunt_prev_dist = 0.0
        self._hunt_blocked_until = -1
        self._hunt_next_update = -1

    # ------------------------------------------------------------------ helpers
    def _roam(self, world: GridWorld, agent: Agent) -> Tuple[str, Vec2]:
        if self.roam_target is None or self.roam_target == agent.pos:
            self.roam_target = world.random_empty_cell(self.rng)
        return "roam", self.roam_target

    def _hunt_or_roam(self, world: GridWorld, agent: Agent) -> Tuple[str, Vec2]:
        if agent.memory.last_seen_enemy_pos is not None:
            return "enemy", agent.memory.last_seen_enemy_pos
        return self._roam(world, agent)

    def _needed_item(self, agent: Agent, items: List[Item]) -> Optional[Vec2]:
        active = [it for it in items if it.active]
        if not active:
            return None
        kind = _needed_resource(agent, self.agent_cfg)
        pos = [it.pos for it in active if it.kind == kind] or [it.pos for it in active]
        nearest = _nearest(agent.pos, pos)
        return nearest[0] if nearest else None

    def _nearest_opponent(self, agent: Agent, agents: Dict[int, Agent]) -> Optional[Vec2]:
        opp = [a.pos for a in agents.values() if a.alive and a.team != agent.team]
        nearest = _nearest(agent.pos, opp)
        return nearest[0] if nearest else None

    # --------------------------------------------------------------- decisions
    def _choose(self, world, agent, agents, items, objective, vis_ids, nearest_enemy_id,
                status_bad) -> Tuple[str, Optional[Vec2], bool]:
        kind = self.style.kind
        enemy_visible = nearest_enemy_id is not None
        teammates = [a for a in agents.values() if a.alive and a.team == agent.team and a.agent_id != agent.agent_id]
        tm_near = _nearest(agent.pos, [a.pos for a in teammates]) if teammates else None

        if kind == "CSO-BT":
            if enemy_visible:
                return "enemy", agents[nearest_enemy_id].pos, False           # attack + hold
            team = sorted([agent] + teammates, key=lambda a: a.agent_id)
            leader = team[0]
            if leader.agent_id != agent.agent_id and euclidean(agent.pos, leader.pos) > 1.0:
                return "teammate", leader.pos, True                            # follow the leader
            if objective is not None:
                return "objective", objective, True
            g, p = self._hunt_or_roam(world, agent)
            return g, p, True

        if kind == "OW-BT":
            if agent.health <= self.agent_cfg.low_health_threshold:
                health = [it.pos for it in items if it.active and it.kind == "health"]
                nearest = _nearest(agent.pos, health)
                if nearest:
                    return "resource", nearest[0], True
            if tm_near is not None and tm_near[1] <= 2.0:
                if objective is not None:
                    return "objective", objective, True
                g, p = self._hunt_or_roam(world, agent)
                return g, p, True
            if tm_near is not None and tm_near[1] <= self.agent_cfg.view_radius:
                return "teammate", tm_near[0], True
            if objective is not None:
                return "objective", objective, True
            g, p = self._hunt_or_roam(world, agent)
            return g, p, True

        if kind == "AC-BT":
            if self.style.ac_units_per_cell > 0 or self.style.ac_hunt_history > 0:
                return self._choose_ac_source(world, agent, agents, items, nearest_enemy_id)
            return self._choose_ac(world, agent, agents, items, nearest_enemy_id)

        if kind == "XO-BT":
            if self.style.xo_interval > 1 or self.style.xo_interval_moving > 1:
                return self._choose_xo_timed(world, agent, agents, items)
            return self._choose_xo(world, agent, agents, items)

        if kind == "AC-BT-v1":
            if status_bad:
                item = self._needed_item(agent, items)
                if item is not None:
                    return "resource", item, True
            if agent.memory.last_seen_enemy_pos is not None:
                return "enemy", agent.memory.last_seen_enemy_pos, True
            opp = self._nearest_opponent(agent, agents)
            if opp is not None:
                return "enemy", opp, True
            g, p = self._roam(world, agent)
            return g, p, True

        if kind == "XO-BT-v1":
            if status_bad:
                if enemy_visible:
                    enemy_pos = [agents[i].pos for i in vis_ids]
                    safe = _safe_item(world, agent, [it for it in items if it.active], enemy_pos)
                    if safe is not None:
                        return "resource", safe, True
                item = self._needed_item(agent, items)
                if item is not None:
                    return "resource", item, True
            opp = self._nearest_opponent(agent, agents)
            if opp is not None:
                return "enemy", opp, True
            g, p = self._roam(world, agent)
            return g, p, True

        # Utility AI: multiplicative considerations, argmax every step, no persistence
        cands: List[Tuple[str, Vec2, float]] = []
        health_curve = 1.0 / (1.0 + math.exp(-(agent.health - 35.0) / 10.0))
        if enemy_visible:
            epos = agents[nearest_enemy_id].pos
            d = euclidean(agent.pos, epos)
            cands.append(("enemy", epos, max(0.0, 1.0 - (d / 15.0) ** 2) * health_curve))
        elif agent.memory.last_seen_enemy_pos is not None:
            epos = agent.memory.last_seen_enemy_pos
            d = euclidean(agent.pos, epos)
            cands.append(("enemy", epos, 0.5 * max(0.0, 1.0 - (d / 15.0) ** 2) * health_curve))
        if objective is not None:
            d = manhattan(agent.pos, objective)
            cands.append(("objective", objective, 0.8 * (0.5 + 0.5 * max(0.0, 1.0 - d / 40.0))))
        item = self._needed_item(agent, items)
        if item is not None:
            need = max(1.0 - agent.health / self.agent_cfg.max_health, 1.0 - agent.ammo / self.weapon_cfg.max_ammo)
            cands.append(("resource", item, need ** 2 / (1.0 + euclidean(agent.pos, item) / 6.0)))
        if tm_near is not None:
            cands.append(("teammate", tm_near[0], 0.6 * min(1.0, tm_near[1] / self.agent_cfg.view_radius) ** 2))
        g, p = self._roam(world, agent)
        cands.append((g, p, 0.05))
        best = max(cands, key=lambda c: c[2])
        return best[0], best[1], True

    def _choose_ac(self, world, agent, agents, items, nearest_enemy_id) -> Tuple[str, Optional[Vec2], bool]:
        """Revised AssaultCube tree: fight > hunt a nearby opponent > missing items > roam (CBot::MainAI)."""
        if nearest_enemy_id is not None:
            if agent.ammo <= self.agent_cfg.low_ammo_threshold:      # DoCombatNav: items only with critical ammo
                near = [it.pos for it in items if it.active and it.kind == "ammo"
                        and euclidean(agent.pos, it.pos) <= AC_COMBAT_ITEM_RANGE and world.los_clear(agent.pos, it.pos)]
                nn = _nearest(agent.pos, near)
                if nn is not None:
                    return "resource", nn[0], True
            return "enemy", agents[nearest_enemy_id].pos, True
        opp = [a.pos for a in agents.values() if a.alive and a.team != agent.team
               and euclidean(agent.pos, a.pos) <= AC_HUNT_RANGE]
        nn = _nearest(agent.pos, opp)
        if nn is not None:                                            # CheckHunt / HuntEnemy
            return "enemy", nn[0], True
        best, best_score = None, -1.0                                 # CheckItems / SearchForEnts
        for it in items:
            if not it.active:
                continue
            have, top = ((agent.health, self.agent_cfg.max_health) if it.kind == "health"
                         else (agent.ammo, self.weapon_cfg.max_ammo))
            if have >= top:
                continue
            d = euclidean(agent.pos, it.pos)
            score = ((100.0 - 100.0 * have / top) / 2.0 + (100.0 - min(4.0 * d, 100.0)) / 2.0
                     + (30.0 if world.los_clear(agent.pos, it.pos) else 15.0))
            if score > best_score:
                best, best_score = it.pos, score
        if best is not None:
            return "resource", best, True
        g, p = self._roam(world, agent)
        return g, p, True

    def _ac_item_score(self, world, agent, it, units_per_cell: float) -> Optional[float]:
        """SearchForEnts score of an item the bot lacks: need + distance (saturating at 100 units) + 30 if visible
        (15 via a waypoint); None if the bot does not lack it."""
        have, top = ((agent.health, self.agent_cfg.max_health) if it.kind == "health"
                     else (agent.ammo, self.weapon_cfg.max_ammo))
        if have >= top:
            return None
        d = euclidean(agent.pos, it.pos)
        return ((100.0 - 100.0 * have / top) / 2.0 + (100.0 - min(units_per_cell * d, 100.0)) / 2.0
                + (30.0 if world.los_clear(agent.pos, it.pos) else 15.0))

    def _choose_ac_source(self, world, agent, agents, items, nearest_enemy_id) -> Tuple[str, Optional[Vec2], bool]:
        """AssaultCube tree at one length scale with source-like hunting (2026-09-27, user decision; CBot::MainAI):
        fight a visible enemy (in combat, with critical ammunition, the best item the bot lacks within 25 units,
        DoCombatNav / SearchForEnts(false, 25)); otherwise hunt (CheckHunt / HuntEnemy, _ac_hunt); otherwise the best
        item the bot lacks (SearchForEnts); otherwise roam."""
        u = self.style.ac_units_per_cell if self.style.ac_units_per_cell > 0 else AC_UNITS_PER_CELL
        if nearest_enemy_id is not None:
            self._prev_enemy = nearest_enemy_id
            if agent.ammo <= self.agent_cfg.low_ammo_threshold:
                best, best_score = None, -1.0
                for it in items:
                    if not it.active or euclidean(agent.pos, it.pos) > 25.0 / u:
                        continue
                    sc = self._ac_item_score(world, agent, it, u)
                    if sc is not None and sc > best_score:
                        best, best_score = it.pos, sc
                if best is not None:
                    return "resource", best, True
            return "enemy", agents[nearest_enemy_id].pos, True
        if self.style.ac_hunt_history > 0:
            loc = self._ac_hunt(world, agent, agents, 250.0 / u)
            if loc is not None:
                return "enemy", loc, True
        else:
            opp = [a.pos for a in agents.values() if a.alive and a.team != agent.team
                   and euclidean(agent.pos, a.pos) <= 250.0 / u]
            nn = _nearest(agent.pos, opp)
            if nn is not None:
                return "enemy", nn[0], True
        best, best_score = None, -1.0
        for it in items:
            if not it.active:
                continue
            sc = self._ac_item_score(world, agent, it, u)
            if sc is not None and sc > best_score:
                best, best_score = it.pos, sc
        if best is not None:
            return "resource", best, True
        g, p = self._roam(world, agent)
        return g, p, True

    def _ac_hunt(self, world, agent, agents, rng_cells: float) -> Optional[Vec2]:
        """CheckHunt / HuntEnemy on the grid. A hunt location is a recent position of the target (position history of
        ac_hunt_history steps) that the bot can see (IsReachable starts with IsVisible; line of sight here), or a recent
        position of the bot itself from which the target is visible; the hunt ends when the location is reached or the
        bot moves away from it without a new one, and then hunting is blocked for AC_HUNT_PAUSE_STEPS steps."""
        step = self._step
        seen = lambda p: world.los_clear(agent.pos, p)  # noqa: E731
        if self._hunt_target is not None:                                      # CheckHunt: keep an ongoing hunt
            t = agents.get(self._hunt_target)
            if t is None or t.team == agent.team:
                self._hunt_target = None
            elif not (t.alive and self._hunt_loc is not None and seen(self._hunt_loc)):
                if step < self._hunt_blocked_until:
                    return None
                self._hunt_target = None
        if self._hunt_target is None:
            if step < self._hunt_blocked_until:
                return None
            if self._hunt_loc is not None:
                self._prev_hunt_loc = self._hunt_loc
            self._hunt_loc = None
            self._hunt_blocked_until = step + AC_HUNT_SEARCH_STEPS
            best_val, choice, nearest = 0, None, float("inf")
            for d in sorted(agents.values(), key=lambda a: a.agent_id):
                if d.team == agent.team or not d.alive:
                    continue
                dist = euclidean(agent.pos, d.pos)
                if dist > rng_cells:
                    continue
                val = 1
                if dist < nearest:
                    val += 2
                    nearest = dist
                if d.agent_id == self._prev_enemy:
                    val += 2
                if val < best_val:
                    continue
                own = [v for v in self._hist.get(d.agent_id, []) if v != self._prev_hunt_loc and seen(v)]
                mine = [v for v in self._hist.get(agent.agent_id, []) if v != self._prev_hunt_loc
                        and world.los_clear(d.pos, v) and seen(v)]
                if own:
                    choice, best_val = (d.agent_id, min(own, key=lambda v: euclidean(d.pos, v))), val
                elif mine:
                    choice, best_val = (d.agent_id, min(mine, key=lambda v: euclidean(agent.pos, v))), val
            if choice is None:
                return None
            self._hunt_target, self._hunt_loc = choice
            self._hunt_prev_dist = 0.0
            self._hunt_next_update = step + AC_HUNT_UPDATE_STEPS
            return self._hunt_loc
        t = agents[self._hunt_target]                                            # HuntEnemy
        dist = euclidean(agent.pos, self._hunt_loc)
        done = dist <= 3.0 / AC_UNITS_PER_CELL or (self._hunt_prev_dist > 0.0 and dist > self._hunt_prev_dist)
        self._hunt_prev_dist = dist
        new = False
        if step >= self._hunt_next_update or done:
            self._hunt_next_update = step + AC_HUNT_UPDATE_STEPS
            cand = [v for v in self._hist.get(t.agent_id, [])
                    if not (done and v == self._hunt_loc) and euclidean(agent.pos, v) <= rng_cells and seen(v)]
            mine = [v for v in self._hist.get(agent.agent_id, [])
                    if not (done and v == self._hunt_loc) and euclidean(agent.pos, v) <= 25.0 / AC_UNITS_PER_CELL
                    and world.los_clear(t.pos, v) and seen(v)]
            if cand:
                self._prev_hunt_loc, self._hunt_loc, new = self._hunt_loc, cand[0], True
                self._hunt_prev_dist = 0.0
            elif mine:
                self._prev_hunt_loc, self._hunt_loc, new = self._hunt_loc, mine[0], True
                self._hunt_prev_dist = 0.0
        if not new and (done or not seen(self._hunt_loc)):
            self._hunt_target = None
            self._prev_hunt_loc, self._hunt_loc = self._hunt_loc, None
            self._hunt_prev_dist = 0.0
            self._hunt_blocked_until = step + AC_HUNT_PAUSE_STEPS
            return None
        return self._hunt_loc

    @staticmethod
    def _route_lengths(world: GridWorld, start: Vec2) -> Dict[Vec2, int]:
        dist, frontier = {start: 0}, [start]
        while frontier:
            nxt = []
            for p in frontier:
                for q in world.neighbors4(p):
                    if q not in dist and world.passable(q):
                        dist[q] = dist[p] + 1
                        nxt.append(q)
            frontier = nxt
        return dist

    def _choose_xo(self, world, agent, agents, items) -> Tuple[str, Optional[Vec2], bool]:
        """Revised Xonotic tree: items and opponents on one rating scale (havocbot_role_generic)."""
        dist = self._route_lengths(world, agent.pos)
        rb = self.style.xo_range_bias
        cands: List[Tuple[str, Vec2, float]] = []
        for it in items:
            if not it.active or it.pos not in dist:
                continue
            if it.kind == "health":
                if agent.health >= self.agent_cfg.max_health:
                    continue
                rating = XO_HEALTH_VALUE * min(2.0, 50.0 / max(1.0, agent.health))
            else:
                if agent.ammo >= self.weapon_cfg.max_ammo:
                    continue
                rating = XO_AMMO_VALUE * min(2.0, 15.0 / max(0.5, agent.ammo))
            cands.append(("resource", it.pos, rating * rb / (rb + dist[it.pos])))
        for e in agents.values():
            if not e.alive or e.team == agent.team or e.pos not in dist:
                continue
            t = min(3.0, max(0.0, 1.0 + (agent.health - e.health) / 150.0)) + self.style.xo_skill_bonus
            cands.append(("enemy", e.pos, XO_ENEMY_RATING * t * rb / (rb + dist[e.pos])))
        if cands:
            g = max(cands, key=lambda c: c[2])
            return g[0], g[1], True
        g, p = self._roam(world, agent)
        return g, p, True

    def _choose_xo_timed(self, world, agent, agents, items) -> Tuple[str, Optional[Vec2], bool]:
        """Xonotic tree with the strategy timer (havocbot: navigation_goalrating_timeout / _set / _force; 2026-09-27,
        optional): the goal rated by _choose_xo is kept for xo_interval steps (an item) or xo_interval_moving steps (an
        opponent, whose current position is followed) and then re-rated; it is re-rated at once when the goal item is
        gone, the goal opponent is dead, or the bot has been dead since its last decision."""
        step, g = self._step, self._xo_goal
        early = self.style.xo_early_rerating
        if g is not None and step == self._xo_last_step + 1 and step < g[2]:
            if g[0] == "resource" and g[1].active:
                if not (early and euclidean(agent.pos, g[1].pos) > XO_ANTICIPATE_CELLS
                        and g[2] - step <= XO_ANTICIPATE_STEPS):
                    self._xo_last_step = step
                    return "resource", g[1].pos, True
            elif g[0] == "enemy" and agents[g[1]].alive:
                e = agents[g[1]]
                d = euclidean(agent.pos, e.pos)
                if not (early and ((d > XO_ANTICIPATE_CELLS and g[2] - step <= XO_ANTICIPATE_STEPS_MOVING)
                                   or (d <= XO_CHASE_CELLS and not world.los_clear(agent.pos, e.pos)))):
                    self._xo_last_step = step
                    return "enemy", e.pos, True
        goal = self._choose_xo(world, agent, agents, items)
        self._xo_goal = None
        if goal[0] == "resource":
            ref = next((it for it in items if it.active and it.pos == goal[1]), None)
            if ref is not None:
                self._xo_goal = ("resource", ref, step + self.style.xo_interval)
        elif goal[0] == "enemy":
            ref = next((a.agent_id for a in agents.values()
                        if a.alive and a.team != agent.team and a.pos == goal[1]), None)
            if ref is not None:
                self._xo_goal = ("enemy", ref, step + self.style.xo_interval_moving)
        self._xo_last_step = step
        return goal

    def decide(self, world: GridWorld, agent: Agent, agents: Dict[int, Agent], items: List[Item],
               objective: Optional[Vec2], step: int) -> PolicyOutput:
        vis_ids = _visible_enemies(world, agent, agents, self.agent_cfg)
        nearest_enemy_id = None
        if vis_ids:
            nearest_enemy_id = min(vis_ids, key=lambda eid: euclidean(agent.pos, agents[eid].pos))
            agent.memory.last_seen_enemy_pos = agents[nearest_enemy_id].pos
        elif (self.agent_cfg.forget_reached_memory and agent.memory.last_seen_enemy_pos is not None
              and euclidean(agent.pos, agent.memory.last_seen_enemy_pos) <= 1.5):
            agent.memory.last_seen_enemy_pos = None   # reached, nobody there: drop the stale memory
        status_bad = _status_bad(agent, self.agent_cfg)

        self._step = step
        if self.style.ac_hunt_history > 0:                 # position histories for AssaultCube hunting (newest first)
            for a in agents.values():
                if a.alive:
                    h = self._hist.setdefault(a.agent_id, [])
                    h.insert(0, a.pos)
                    del h[self.style.ac_hunt_history:]
        chosen_type, chosen_pos, allow_move = self._choose(world, agent, agents, items, objective,
                                                           vis_ids, nearest_enemy_id, status_bad)

        # Path following (distance-only A*), identical replanning rules to PriorityPolicy
        move_to: Optional[Vec2] = None
        blocked = _blocked_cell(agent, agents) if self.agent_cfg.local_avoidance else None
        if allow_move and chosen_pos is not None:
            mem = agent.memory
            need_replan = (mem.current_goal_pos != chosen_pos or mem.current_goal_type != chosen_type
                           or not mem.planned_path
                           or not world.passable(mem.planned_path[0])
                           or manhattan(mem.planned_path[0], agent.pos) != 1
                           or blocked is not None)
            if need_replan:
                res = None
                if blocked is not None and blocked != chosen_pos:   # no detour to a held goal cell
                    res = astar_search(BlockedView(world, {blocked}), agent.pos, chosen_pos, step_cost=lambda u, v: 1.0)
                if res is None:
                    res = astar_search(world, agent.pos, chosen_pos, step_cost=lambda u, v: 1.0)
                mem.planned_path = res.path[1:] if res is not None else []
            if mem.planned_path:
                move_to = mem.planned_path.pop(0)

        shoot_target: Optional[int] = None
        if nearest_enemy_id is not None:
            d = euclidean(agent.pos, agents[nearest_enemy_id].pos)
            if d <= self.weapon_cfg.range_cells and agent.ammo >= self.weapon_cfg.ammo_per_shot:
                shoot_target = nearest_enemy_id

        agent.memory.current_goal_type = chosen_type
        agent.memory.current_goal_pos = chosen_pos
        agent.memory.last_visible_enemies = vis_ids
        agent.memory.last_move_to = move_to
        return PolicyOutput(goal_type=chosen_type, goal_pos=chosen_pos, move_to=move_to,
                            allow_move=allow_move, shoot_target=shoot_target)
