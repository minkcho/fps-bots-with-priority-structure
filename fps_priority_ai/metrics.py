from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from collections import defaultdict

from .entities import StepLog
from .world import euclidean


@dataclass
class Metrics:
    objective_commitment_ratio: float
    engagement_redirection_rate_per_100: float
    resource_seeking_rate_per_100: float
    avg_ally_proximity: Optional[float]

    kills: int
    deaths: int
    control_score: Optional[int] = None
    # Goal switches of any kind per 100 alive agent-steps (consecutive logged steps only, so a
    # respawn does not count as a switch). Added 2026-09-23 for the redefined H2.
    goal_switch_rate_per_100: float = 0.0

    def as_dict(self) -> Dict[str, float]:
        d: Dict[str, float] = {
            "objective_commitment_ratio": self.objective_commitment_ratio,
            "engagement_redirection_rate_per_100": self.engagement_redirection_rate_per_100,
            "resource_seeking_rate_per_100": self.resource_seeking_rate_per_100,
            "kills": float(self.kills),
            "deaths": float(self.deaths),
            "goal_switch_rate_per_100": self.goal_switch_rate_per_100,
        }
        if self.avg_ally_proximity is not None:
            d["avg_ally_proximity"] = float(self.avg_ally_proximity)
        if self.control_score is not None:
            d["control_score"] = float(self.control_score)
        return d


def compute_metrics(
    logs: List[StepLog],
    team_id: int = 0,
    kills: int = 0,
    deaths: int = 0,
    control_score: Optional[int] = None,
) -> Metrics:
    """
    Compute lightweight behavioural metrics from per-step logs.

    Notes:
    - Metrics are computed only for the selected team (default: blue team 0).
    - Switching is reconstructed from successive goal_type changes per agent.
    """
    # Organize logs by agent and by step
    by_agent = defaultdict(list)
    by_step = defaultdict(list)
    for row in logs:
        by_step[row.step].append(row)
        if row.team == team_id:
            by_agent[row.agent_id].append(row)

    # Sort per-agent time series
    for aid in list(by_agent.keys()):
        by_agent[aid].sort(key=lambda r: r.step)

    total_steps = sum(len(ts) for ts in by_agent.values())
    if total_steps == 0:
        return Metrics(0.0, 0.0, 0.0, None, kills=kills, deaths=deaths, control_score=control_score)

    # Objective commitment ratio
    obj_steps = 0
    for ts in by_agent.values():
        obj_steps += sum(1 for r in ts if r.goal_type == "objective")
    objective_commitment_ratio = obj_steps / total_steps

    # Engagement redirection: switches to enemy while enemy is visible
    enemy_switches = 0
    resource_switches = 0
    all_switches = 0

    for ts in by_agent.values():
        prev_goal = None
        prev_step = None
        for r in ts:
            if prev_goal is not None and r.goal_type != prev_goal:
                if r.goal_type == "enemy" and r.enemy_visible:
                    enemy_switches += 1
                if r.goal_type == "resource" and r.status_bad:
                    resource_switches += 1
                if prev_step is not None and r.step == prev_step + 1:
                    all_switches += 1
            prev_goal = r.goal_type
            prev_step = r.step

    engagement_redirection_rate_per_100 = enemy_switches / total_steps * 100.0
    goal_switch_rate_per_100 = all_switches / total_steps * 100.0
    resource_seeking_rate_per_100 = resource_switches / total_steps * 100.0

    # Average ally proximity
    avg_ally_proximity: Optional[float] = None
    agent_ids = list(by_agent.keys())
    if len(agent_ids) >= 2:
        dists: List[float] = []
        for step, rows in by_step.items():
            team_rows = [r for r in rows if r.team == team_id]
            if len(team_rows) < 2:
                continue
            for r in team_rows:
                others = [o for o in team_rows if o.agent_id != r.agent_id]
                d = min(euclidean(r.pos, o.pos) for o in others)
                dists.append(d)
        if dists:
            avg_ally_proximity = sum(dists) / len(dists)

    return Metrics(
        objective_commitment_ratio=objective_commitment_ratio,
        engagement_redirection_rate_per_100=engagement_redirection_rate_per_100,
        resource_seeking_rate_per_100=resource_seeking_rate_per_100,
        avg_ally_proximity=avg_ally_proximity,
        kills=kills,
        deaths=deaths,
        control_score=control_score,
        goal_switch_rate_per_100=goal_switch_rate_per_100,
    )
