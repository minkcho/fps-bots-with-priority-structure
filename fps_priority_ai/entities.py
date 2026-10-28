from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import math

Vec2 = Tuple[int, int]


@dataclass
class Item:
    kind: str  # 'health' or 'ammo'
    pos: Vec2
    active: bool = True
    respawn_timer: int = 0


@dataclass
class AgentMemory:
    current_goal_type: str = "none"  # objective | enemy | resource | teammate | roam | none
    current_goal_pos: Optional[Vec2] = None
    planned_path: List[Vec2] = field(default_factory=list)
    last_seen_enemy_pos: Optional[Vec2] = None
    last_visible_enemies: List[int] = field(default_factory=list)
    evade_active: bool = False   # evade hysteresis state (see AgentConfig.evade_release_radius)
    last_move_to: Optional[Vec2] = None   # cell of the last attempted move (local avoidance, 2026-09-25)


@dataclass
class Agent:
    agent_id: int
    team: int  # 0 or 1
    pos: Vec2
    health: int
    ammo: int
    alive: bool = True
    respawn_timer: int = 0
    memory: AgentMemory = field(default_factory=AgentMemory)

    # Stats
    kills: int = 0
    deaths: int = 0
    hits_taken: int = 0   # (2026-09-24) hits received; bookkeeping only, no effect on behaviour


@dataclass
class StepLog:
    step: int
    agent_id: int
    team: int
    pos: Vec2

    goal_type: str
    goal_pos: Optional[Vec2]

    enemy_visible: bool
    status_bad: bool
    switched_goal: bool
    switch_reason: str  # 'enemy', 'resource', 'teammate', 'objective', 'roam', 'none'

    moved: bool
    shot: bool
    hit: bool
    killed_enemy: bool
