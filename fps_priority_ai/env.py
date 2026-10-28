from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import random

from .config import AgentConfig, MapConfig, ScenarioConfig, WeaponConfig, PriorityWeights
from .entities import Agent, Item, StepLog
from .policy import PriorityPolicy
from .baselines import BaselinePolicy, BaselineStyle
from . import world as world_rules
from .world import GridWorld, Vec2, euclidean, manhattan


@dataclass
class EpisodeResult:
    logs: List[StepLog]
    team_scores: Dict[int, int]
    steps: int


def build_world(map_cfg: MapConfig) -> GridWorld:
    """World of a map configuration (factored out of FPSEnv.__init__ on 2026-09-25; the random and
    buildings layouts are generated exactly as before). With the reachable-placement rule, the world also records
    the free cells reachable from team 0's spawn cell."""
    world = _layout_world(map_cfg)
    if world_rules.REACHABLE_PLACEMENT:
        world.reachable = world.component(map_cfg.spawn_a)
    return world


def _layout_world(map_cfg: MapConfig) -> GridWorld:
    protected = {map_cfg.spawn_a, map_cfg.spawn_b, map_cfg.objective}
    if map_cfg.layout == "buildings":
        return GridWorld.building_world(
            width=map_cfg.width,
            height=map_cfg.height,
            seed=map_cfg.seed,
            target_density=map_cfg.building_density,
            protected=protected,
        )
    if map_cfg.layout == "random":
        return GridWorld.random_world(
            width=map_cfg.width,
            height=map_cfg.height,
            obstacle_density=map_cfg.obstacle_density,
            seed=map_cfg.seed,
            protected=protected,
        )
    if map_cfg.layout == "custom":
        return GridWorld(width=map_cfg.width, height=map_cfg.height, obstacles=set(map_cfg.obstacles) - protected)
    raise ValueError(f"unknown map layout: {map_cfg.layout!r}")


def spawn_position(map_cfg: MapConfig, world: GridWorld, team: int, index: int = 0) -> Vec2:
    """Spawn cell of the index-th agent of a team: the team's spawn cell for index 0, and cells
    spawn_separation * index further along x toward the map interior for the others (falling
    back to the nearest passable neighbour, then to the spawn cell itself). Maps with explicit
    spawn cells (MapConfig.spawn_cells) use those."""
    if map_cfg.spawn_cells and index < len(map_cfg.spawn_cells[team]):
        return map_cfg.spawn_cells[team][index]
    base = map_cfg.spawn_a if team == 0 else map_cfg.spawn_b
    sep = map_cfg.spawn_separation * index
    if sep == 0:
        return base
    sign = 1 if team == 0 else -1
    for cand in ((base[0] + sign * sep, base[1]), (base[0], base[1] + sign * sep),
                 (base[0] + sign * sep, base[1] + sign * sep), (base[0] + sign, base[1]), (base[0], base[1] + sign)):
        if world.passable(cand):
            return cand
    return base


class FPSEnv:
    """
    A lightweight FPS-like grid simulation for controlled behavioural experiments.

    Design philosophy:
    - Minimal mechanics to keep behaviour interpretable
    - Deterministic/reproducible with explicit random seeds
    - Sufficient richness to trigger: objective pursuit, engagement redirection,
      resource seeking, and team cohesion.
    """

    def __init__(
        self,
        map_cfg: MapConfig,
        agent_cfg: AgentConfig,
        weapon_cfg: WeaponConfig,
        scenario: ScenarioConfig,
        styles: Dict[str, PriorityWeights],
        rng: random.Random,
    ):
        self.map_cfg = map_cfg
        self.agent_cfg = agent_cfg
        self.weapon_cfg = weapon_cfg
        self.scenario = scenario
        self.styles = styles
        self.rng = rng

        self.world = build_world(map_cfg)

        # Create items
        self.items: List[Item] = []
        self._init_items()

        # Create agents
        self.agents: Dict[int, Agent] = {}
        self.policies: Dict[int, PriorityPolicy] = {}
        self._init_agents()

        # Scores (for control mode)
        self.team_scores: Dict[int, int] = {0: 0, 1: 0}

        self.step_idx = 0

    def _init_items(self) -> None:
        if self.map_cfg.item_cells:  # fixed item cells (game-inspired maps); consumes no randomness
            self.items = [Item(kind=kind, pos=pos) for kind, pos in self.map_cfg.item_cells]
            return
        protected = {self.map_cfg.spawn_a, self.map_cfg.spawn_b, self.map_cfg.objective}
        for team in (0, 1):
            for idx in range(1, self.scenario.num_agents_per_team):
                protected.add(self._spawn_pos(team, idx))
        # Health
        for _ in range(self.map_cfg.num_health):
            p = self.world.random_empty_cell(self.rng, protected=protected)
            protected.add(p)
            self.items.append(Item(kind="health", pos=p))
        # Ammo
        for _ in range(self.map_cfg.num_ammo):
            p = self.world.random_empty_cell(self.rng, protected=protected)
            protected.add(p)
            self.items.append(Item(kind="ammo", pos=p))

    def _spawn_pos(self, team: int, index: int = 0) -> Vec2:
        return spawn_position(self.map_cfg, self.world, team, index)

    def _init_agents(self) -> None:
        aid = 0
        for team in (0, 1):
            for idx in range(self.scenario.num_agents_per_team):
                pos = self._spawn_pos(team, idx)
                agent = Agent(
                    agent_id=aid,
                    team=team,
                    pos=pos,
                    health=self.agent_cfg.max_health,
                    ammo=self.weapon_cfg.max_ammo,
                    alive=True,
                )
                self.agents[aid] = agent
                aid += 1

        # Build policies (blue team uses evaluated style; red team uses opponent style unless symmetric)
        # This is set/reset per episode by `set_team_styles`.
        self.set_team_styles(evaluated_style="Mission–Cooperation")

    def set_team_styles(self, evaluated_style: str) -> None:
        opponent_style = self.scenario.opponent_style
        for agent in self.agents.values():
            if self.scenario.symmetric_styles:
                style_name = evaluated_style
            else:
                style_name = evaluated_style if agent.team == 0 else opponent_style
            style = self.styles[style_name]
            # Make a distinct RNG per agent for tie-breaking
            local_rng = random.Random(self.rng.randrange(10**9))
            policy_cls = BaselinePolicy if isinstance(style, BaselineStyle) else PriorityPolicy
            self.policies[agent.agent_id] = policy_cls(
                style=style,
                agent_cfg=self.agent_cfg,
                weapon_cfg=self.weapon_cfg,
                rng=local_rng,
            )

    def objective_pos(self) -> Optional[Vec2]:
        if self.scenario.mode in ("mission", "control"):
            return self.map_cfg.objective
        return None

    def _item_at(self, pos: Vec2) -> Optional[Item]:
        for it in self.items:
            if it.active and it.pos == pos:
                return it
        return None

    def _apply_item_pickups(self) -> None:
        for agent in self.agents.values():
            if not agent.alive:
                continue
            it = self._item_at(agent.pos)
            if it is None:
                continue
            if it.kind == "health":
                agent.health = min(self.agent_cfg.max_health, agent.health + 50)
            elif it.kind == "ammo":
                agent.ammo = min(self.weapon_cfg.max_ammo, agent.ammo + 15)
            it.active = False
            it.respawn_timer = self.map_cfg.item_respawn_steps

    def _update_items(self) -> None:
        for it in self.items:
            if it.active:
                continue
            it.respawn_timer -= 1
            if it.respawn_timer <= 0:
                it.active = True
                it.respawn_timer = 0

    def _update_respawns(self) -> None:
        for agent in self.agents.values():
            if agent.alive:
                continue
            agent.respawn_timer -= 1
            if agent.respawn_timer <= 0:
                agent.alive = True
                agent.health = self.agent_cfg.max_health
                agent.ammo = self.weapon_cfg.max_ammo
                agent.pos = self._spawn_pos(agent.team, agent.agent_id % self.scenario.num_agents_per_team)
                agent.respawn_timer = 0
                # Clear memory
                agent.memory.planned_path.clear()
                agent.memory.current_goal_pos = None
                agent.memory.current_goal_type = "none"
                agent.memory.evade_active = False
                agent.memory.last_seen_enemy_pos = None
                agent.memory.last_visible_enemies = []
                agent.memory.last_move_to = None

    def _apply_control_scoring(self) -> None:
        if self.scenario.mode != "control":
            return
        obj = self.map_cfg.objective
        occ = {0: 0, 1: 0}
        for a in self.agents.values():
            if a.alive and a.pos == obj:
                occ[a.team] += 1
        if occ[0] > occ[1]:
            self.team_scores[0] += 1
        elif occ[1] > occ[0]:
            self.team_scores[1] += 1

    def step(self) -> List[StepLog]:
        self.step_idx += 1
        obj = self.objective_pos()

        # Decide for each agent
        decisions: Dict[int, Tuple[str, Optional[Vec2], Optional[Vec2], bool, Optional[int], bool, bool]] = {}
        # stored: (goal_type, goal_pos, move_to, allow_move, shoot_target, enemy_visible, status_bad)
        for aid, agent in self.agents.items():
            if not agent.alive:
                continue
            policy = self.policies[aid]
            prev_goal = agent.memory.current_goal_type
            prev_enemy_visible = len(agent.memory.last_visible_enemies) > 0

            out = policy.decide(
                world=self.world,
                agent=agent,
                agents=self.agents,
                items=self.items,
                objective=obj,
                step=self.step_idx,
            )
            enemy_visible = out.shoot_target is not None or (len(agent.memory.last_visible_enemies) > 0)
            status_bad = (agent.health <= self.agent_cfg.low_health_threshold) or (agent.ammo <= self.agent_cfg.low_ammo_threshold)
            decisions[aid] = (out.goal_type, out.goal_pos, out.move_to, out.allow_move, out.shoot_target, enemy_visible, status_bad)

        # Apply movement (random order to reduce bias)
        order = [aid for aid, a in self.agents.items() if a.alive]
        self.rng.shuffle(order)
        occupied = {a.pos: a.agent_id for a in self.agents.values() if a.alive}

        moved_flags: Dict[int, bool] = {aid: False for aid in order}
        for aid in order:
            if moved_flags[aid]:
                continue  # already moved by a teammate swap this step
            agent = self.agents[aid]
            goal_type, goal_pos, move_to, allow_move, shoot_target, enemy_visible, status_bad = decisions[aid]
            if not allow_move or move_to is None:
                continue
            if not self.world.passable(move_to):
                continue
            if manhattan(agent.pos, move_to) != 1:
                continue  # invariant guard: agents move one 4-neighbour cell per step
            if move_to in occupied:
                other_id = occupied[move_to]
                other = self.agents[other_id]
                if (self.agent_cfg.teammate_swap and other.team == agent.team and other_id in decisions
                        and not moved_flags.get(other_id, False)
                        and decisions[other_id][3] and decisions[other_id][2] == agent.pos):
                    # teammate swap (optional movement rule): the two agents exchange cells
                    occupied[agent.pos], occupied[move_to] = other_id, aid
                    other.pos, agent.pos = agent.pos, move_to
                    moved_flags[aid] = moved_flags[other_id] = True
                continue
            # move
            occupied.pop(agent.pos, None)
            agent.pos = move_to
            occupied[agent.pos] = aid
            moved_flags[aid] = True

        # Apply shooting
        shot_flags: Dict[int, bool] = {aid: False for aid in order}
        hit_flags: Dict[int, bool] = {aid: False for aid in order}
        killed_flags: Dict[int, bool] = {aid: False for aid in order}

        for aid in order:
            agent = self.agents[aid]
            goal_type, goal_pos, move_to, allow_move, shoot_target, enemy_visible, status_bad = decisions[aid]
            if shoot_target is None:
                continue
            target = self.agents.get(shoot_target)
            if target is None or (not target.alive):
                continue
            d = euclidean(agent.pos, target.pos)
            if d > self.weapon_cfg.range_cells:
                continue
            # Consume ammo
            if agent.ammo < self.weapon_cfg.ammo_per_shot:
                continue
            agent.ammo -= self.weapon_cfg.ammo_per_shot
            shot_flags[aid] = True

            # Hit probability decreases with distance
            p = self.weapon_cfg.base_accuracy * max(0.05, 1.0 - 0.7 * (d / max(1.0, float(self.weapon_cfg.range_cells))))
            if self.rng.random() < p:
                hit_flags[aid] = True
                target.hits_taken += 1   # (2026-09-24) independent outcome for H3; consumes no randomness
                target.health -= self.weapon_cfg.damage
                if target.health <= 0 and target.alive:
                    target.alive = False
                    target.deaths += 1
                    target.respawn_timer = self.agent_cfg.respawn_steps
                    agent.kills += 1
                    killed_flags[aid] = True

        # Apply item pickups & updates
        self._apply_item_pickups()
        self._update_items()
        self._apply_control_scoring()
        self._update_respawns()

        # Build logs
        logs: List[StepLog] = []
        for aid in order:
            agent = self.agents[aid]
            goal_type, goal_pos, move_to, allow_move, shoot_target, enemy_visible, status_bad = decisions[aid]
            prev_goal_type = agent.memory.current_goal_type  # already updated by policy
            # We can detect switch by checking whether at this step the chosen goal differs from previous stored before policy,
            # but we didn't store it per agent. Approximate via planned_path reset: if goal changed, planned_path likely recomputed.
            # To make this explicit, we log based on comparing the policy output vs last step's goal stored in memory *before* policy,
            # which is not preserved. For robustness, we track switch via internal field in memory? Not available.
            # Here we compute switch by comparing to the current_goal_type at end of decide against what it was in the previous log.
            # This will be handled in metrics by reconstructing per-agent time series.
            switched = False
            reason = goal_type
            # We store enough to reconstruct switching offline.
            logs.append(
                StepLog(
                    step=self.step_idx,
                    agent_id=aid,
                    team=agent.team,
                    pos=agent.pos,
                    goal_type=goal_type,
                    goal_pos=goal_pos,
                    enemy_visible=enemy_visible,
                    status_bad=status_bad,
                    switched_goal=switched,
                    switch_reason=reason,
                    moved=moved_flags.get(aid, False),
                    shot=shot_flags.get(aid, False),
                    hit=hit_flags.get(aid, False),
                    killed_enemy=killed_flags.get(aid, False),
                )
            )
        return logs

    def run_episode(self, evaluated_style: str) -> EpisodeResult:
        # Reset env state for a fresh episode
        self.__init__(
            map_cfg=self.map_cfg,
            agent_cfg=self.agent_cfg,
            weapon_cfg=self.weapon_cfg,
            scenario=self.scenario,
            styles=self.styles,
            rng=self.rng,
        )
        self.set_team_styles(evaluated_style=evaluated_style)
        logs: List[StepLog] = []
        for _ in range(self.scenario.max_steps):
            logs.extend(self.step())
            # Early stop for control mode
            if self.scenario.mode == "control":
                if max(self.team_scores.values()) >= self.scenario.score_to_win:
                    break
        return EpisodeResult(logs=logs, team_scores=dict(self.team_scores), steps=self.step_idx)
