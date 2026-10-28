from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt

from .entities import Agent, Item, StepLog
from .world import GridWorld, Vec2


def save_map_figure(
    world: GridWorld,
    items: List[Item],
    agents: Dict[int, Agent],
    objective: Optional[Vec2],
    out_path: str,
    title: str = "",
) -> None:
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_title(title)
    ax.set_xlim(-0.5, world.width - 0.5)
    ax.set_ylim(-0.5, world.height - 0.5)
    ax.set_aspect("equal")
    ax.invert_yaxis()

    # Obstacles
    if world.obstacles:
        xs = [p[0] for p in world.obstacles]
        ys = [p[1] for p in world.obstacles]
        ax.scatter(xs, ys, marker="s", s=20, alpha=0.6)

    # Items
    for it in items:
        if not it.active:
            continue
        if it.kind == "health":
            ax.scatter([it.pos[0]], [it.pos[1]], marker="o", s=35)
        else:
            ax.scatter([it.pos[0]], [it.pos[1]], marker="^", s=35)

    # Objective
    if objective is not None:
        ax.scatter([objective[0]], [objective[1]], marker="*", s=120)

    # Agents
    for a in agents.values():
        if not a.alive:
            continue
        ax.scatter([a.pos[0]], [a.pos[1]], marker="X", s=60)

    ax.grid(True, linewidth=0.3, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def save_trajectory_figure(
    world: GridWorld,
    logs: List[StepLog],
    team_id: int,
    out_path: str,
    title: str = "",
) -> None:
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_title(title)
    ax.set_xlim(-0.5, world.width - 0.5)
    ax.set_ylim(-0.5, world.height - 0.5)
    ax.set_aspect("equal")
    ax.invert_yaxis()

    # Obstacles
    if world.obstacles:
        xs = [p[0] for p in world.obstacles]
        ys = [p[1] for p in world.obstacles]
        ax.scatter(xs, ys, marker="s", s=20, alpha=0.3)

    # Trajectories per agent
    by_agent: Dict[int, List[Tuple[int, int]]] = {}
    for r in logs:
        if r.team != team_id:
            continue
        by_agent.setdefault(r.agent_id, []).append(r.pos)

    for aid, pts in by_agent.items():
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        ax.plot(xs, ys, linewidth=1.5, label=f"agent{aid}")

    ax.grid(True, linewidth=0.3, alpha=0.3)
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
