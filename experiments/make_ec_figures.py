"""Generate paper figures from a results.csv produced by run_ec_experiments.py.

Usage:
  MPLBACKEND=Agg python experiments/make_ec_figures.py --csv outputs_ec/results.csv --out outputs_ec/figures

The script produces:
  - fig_priority_map.pdf
  - fig_metrics_mission_deathmatch.pdf
  - fig_metrics_control.pdf
  - fig_traj_mission.pdf
"""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Ensure project root is on sys.path when executed as a script
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fps_priority_ai.runner import DEFAULT_MODEL, STYLE_MODELS, default_styles
from fps_priority_ai.config import MapConfig, AgentConfig, WeaponConfig, ScenarioConfig
from fps_priority_ai.env import FPSEnv


def t_crit_95(df: int) -> float:
    table = {
        1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447,
        7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179,
        13: 2.160, 14: 2.145, 15: 2.131, 16: 2.120, 17: 2.110, 18: 2.101,
        19: 2.093, 20: 2.086,
    }
    return table.get(df, 1.96)


def mean_ci(vals: np.ndarray):
    vals = np.asarray(vals, dtype=float)
    vals = vals[~np.isnan(vals)]
    n = len(vals)
    if n == 0:
        return np.nan, np.nan
    m = float(vals.mean())
    if n == 1:
        return m, 0.0
    s = float(vals.std(ddof=1))
    se = s / math.sqrt(n)
    t = t_crit_95(n - 1)
    return m, t * se


def bar_with_ci(ax, labels, means, cis, title, ylabel, raw=None):
    x = np.arange(len(labels))
    ax.bar(x, means, yerr=cis, capsize=3)
    if raw is not None:
        # Per-episode dots at deterministic offsets (no random jitter, so the
        # rendered PDF is reproducible).
        for xi, vals in zip(x, raw):
            vals = np.asarray(vals, dtype=float)
            vals = vals[~np.isnan(vals)]
            if len(vals) == 0:
                continue
            offs = np.linspace(-0.18, 0.18, len(vals))
            ax.scatter(xi + offs, vals, s=9, color='black', alpha=0.55, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=20, ha='right')
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(True, axis='y', linewidth=0.3, alpha=0.4)


def make_priority_map(out_path: Path):
    # Hand-crafted coordinates based on the taxonomy.
    games = [
        ("CSO (bomb)", 0.85, 0.90),
        ("Overwatch (payload)", 0.95, 0.70),
        ("AssaultCube (DM)", 0.10, 0.15),
        ("Xonotic (DM)", 0.10, 0.10),
    ]

    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel("Objective pressure (battle → mission)")
    ax.set_ylabel("Cooperation pressure (individual → team)")
    ax.set_title("Priority-structure map of FPS game modes")

    ax.scatter([g[1] for g in games], [g[2] for g in games])
    for name, x, y in games:
        ax.text(x + 0.02, y + 0.02, name, fontsize=9)

    ax.grid(True, linewidth=0.3, alpha=0.4)
    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def make_traj_mission(out_path: Path, map_cfg=None, model: str = DEFAULT_MODEL):
    styles = default_styles(model)

    sc = ScenarioConfig(
        name='Mission',
        mode='mission',
        max_steps=550,
        num_agents_per_team=2,
        opponent_style='Aggressive'
    )
    if map_cfg is None:
        map_cfg = MapConfig(width=25, height=25, obstacle_density=0.18, seed=7)
    agent_cfg = AgentConfig()
    weapon_cfg = WeaponConfig()

    base_rng = random.Random(424242)

    def plot_trajectory(ax, env: FPSEnv, logs, team_id: int, title: str):
        world = env.world
        ax.set_title(title)
        ax.set_xlim(-0.5, world.width - 0.5)
        ax.set_ylim(-0.5, world.height - 0.5)
        ax.set_aspect('equal')
        ax.invert_yaxis()

        if world.obstacles:
            xs = [p[0] for p in world.obstacles]
            ys = [p[1] for p in world.obstacles]
            ax.scatter(xs, ys, marker='s', s=12, alpha=0.25)

        obj = env.objective_pos()
        if obj is not None:
            ax.scatter([obj[0]], [obj[1]], marker='*', s=100)

        by_agent = {}
        for r in logs:
            if r.team != team_id:
                continue
            by_agent.setdefault(r.agent_id, []).append(r.pos)

        for aid, pts in by_agent.items():
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            ax.plot(xs, ys, linewidth=1.2, label=f"agent{aid}")

        ax.grid(True, linewidth=0.3, alpha=0.4)

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 5.2))
    for ax, style_name in zip(axes, ['Mission–Cooperation', 'Persistent Objective']):
        local_rng = random.Random(base_rng.randrange(10**9))
        env = FPSEnv(
            map_cfg=map_cfg,
            agent_cfg=agent_cfg,
            weapon_cfg=weapon_cfg,
            scenario=sc,
            styles=styles,
            rng=local_rng,
        )
        res = env.run_episode(evaluated_style=style_name)
        plot_trajectory(ax, env, res.logs, team_id=0, title=style_name.replace('–','-'))

    axes[0].legend(loc='best', fontsize=8)
    axes[1].legend(loc='best', fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--csv", type=str, required=True, help="Path to results.csv")
    p.add_argument("--out", type=str, required=True, help="Output directory for figures")
    p.add_argument("--map", type=str, default="random", help="Map layout for the trajectory figure")
    p.add_argument("--model", type=str, default=DEFAULT_MODEL, choices=list(STYLE_MODELS),
                   help="Style set of the re-simulated trajectory figure")
    args = p.parse_args()

    csv_path = Path(args.csv)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path)
    df['style'] = df['style'].astype(str).str.replace('–', '-', regex=False)

    styles_order = ["Mission-Cooperation", "Persistent Objective", "Aggressive", "Survival-Aware"]

    make_priority_map(out_dir / 'fig_priority_map.pdf')

    # Mission + Deathmatch (4 panels)
    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.2))

    sub = df[df['scenario'] == 'Mission']
    means, cis, raws = [], [], []
    for s in styles_order:
        vals = sub[sub['style'] == s]['objective_commitment_ratio'].values
        m, c = mean_ci(vals)
        means.append(m); cis.append(c); raws.append(vals)
    bar_with_ci(axes[0, 0], styles_order, means, cis,
                title='Mission: Objective commitment',
                ylabel='Ratio of steps (goal=objective)', raw=raws)

    means, cis, raws = [], [], []
    for s in styles_order:
        vals = sub[sub['style'] == s]['avg_ally_proximity'].values
        m, c = mean_ci(vals)
        means.append(m); cis.append(c); raws.append(vals)
    bar_with_ci(axes[0, 1], styles_order, means, cis,
                title='Mission: Teammate cohesion',
                ylabel='Avg. nearest-ally distance', raw=raws)

    sub = df[df['scenario'] == 'Deathmatch']
    means, cis, raws = [], [], []
    for s in styles_order:
        vals = sub[sub['style'] == s]['engagement_redirection_rate_per_100'].values
        m, c = mean_ci(vals)
        means.append(m); cis.append(c); raws.append(vals)
    bar_with_ci(axes[1, 0], styles_order, means, cis,
                title='Deathmatch: Engagement redirection',
                ylabel='Switches to enemy goal / 100 steps', raw=raws)

    means, cis, raws = [], [], []
    for s in styles_order:
        vals = sub[sub['style'] == s]['resource_seeking_rate_per_100'].values
        m, c = mean_ci(vals)
        means.append(m); cis.append(c); raws.append(vals)
    bar_with_ci(axes[1, 1], styles_order, means, cis,
                title='Deathmatch: Resource seeking',
                ylabel='Switches to resource goal / 100 steps', raw=raws)

    fig.tight_layout()
    fig.savefig(out_dir / 'fig_metrics_mission_deathmatch.pdf')
    plt.close(fig)

    # Control (2 panels)
    sub = df[df['scenario'] == 'Control']
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.8))

    means, cis, raws = [], [], []
    for s in styles_order:
        vals = sub[sub['style'] == s]['control_score'].dropna().astype(float).values
        m, c = mean_ci(vals)
        means.append(m); cis.append(c); raws.append(vals)
    bar_with_ci(axes[0], styles_order, means, cis,
                title='Control: Objective scoring',
                ylabel='Team score (higher is better)', raw=raws)

    means, cis, raws = [], [], []
    for s in styles_order:
        vals = sub[sub['style'] == s]['avg_ally_proximity'].values
        m, c = mean_ci(vals)
        means.append(m); cis.append(c); raws.append(vals)
    bar_with_ci(axes[1], styles_order, means, cis,
                title='Control: Teammate cohesion',
                ylabel='Avg. nearest-ally distance', raw=raws)

    fig.tight_layout()
    fig.savefig(out_dir / 'fig_metrics_control.pdf')
    plt.close(fig)

    from fps_priority_ai.experiment import MAPS
    make_traj_mission(out_dir / 'fig_traj_mission.pdf', MAPS[args.map], args.model)

    print(f"Saved figures to: {out_dir.resolve()}")


if __name__ == '__main__':
    main()
