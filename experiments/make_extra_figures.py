"""Generate the additional paper figures that are not covered by make_ec_figures.py.

Produces:
  - fig_maps.pdf                    (simulator initialisation; the three scenario
                                     panels intentionally share one obstacle layout,
                                     map seed 7, with one seeded item placement)
  - fig_performance_sanity.pdf      (kills/deaths per style and scenario, from results.csv)
  - fig_fingerprint_heatmap.pdf     (normalised behaviour fingerprints, from results.csv)
  - fig_sensitivity_commitment.pdf  (from sensitivity_commitment.csv,
                                     produced by run_sensitivity_commitment.py)
  - fig_ablation_navigation.pdf     (from ablation_navigation.csv,
                                     produced by run_ablation_navigation.py)
  - fig_mode_ablation.pdf           (full vs weights-only combat modes, from
                                     results.csv + mode_ablation.csv)
  - fig_interpolation.pdf           (style interpolation, from interpolation.csv)
  - fig_lambda_scale.pdf            (navigation-weight scale sweep, from lambda_scale.csv)
  - fig_risk_budget_<mode>.pdf      (optional additional experiment, from risk_budget_<mode>.csv)
  - fig_cover_model.pdf             (optional additional experiment, from cover_model.csv)
  - fig_cost_terms.pdf              (optional additional experiment, from cost_term_ablation.csv)
  - fig_baselines.pdf               (optional additional experiment, from baselines.csv + results.csv)
  - fig_argument_chain.pdf          (static schematic of the paper's deductive
                                     chain: observations -> requirements ->
                                     formal elements -> tests; used by main_v2)

Usage:
  python experiments/make_extra_figures.py \
      --csv ../paper/results.csv \
      --sensitivity-csv ../paper/sensitivity_commitment.csv \
      --ablation-csv ../paper/ablation_navigation.csv \
      --mode-csv ../paper/mode_ablation.csv \
      --interp-csv ../paper/interpolation.csv \
      --lambda-csv ../paper/lambda_scale.csv \
      --out ../repro_outputs/figures
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Patch

# Ensure project root and this directory are on sys.path when executed as a script
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from make_ec_figures import mean_ci  # noqa: E402  (shared CI helper)
from fps_priority_ai.runner import default_styles, default_scenarios  # noqa: E402
from fps_priority_ai.config import MapConfig, AgentConfig, WeaponConfig  # noqa: E402
from fps_priority_ai.env import FPSEnv  # noqa: E402
from fps_priority_ai.experiment import MAPS  # noqa: E402

STYLES_ORDER = ["Mission-Cooperation", "Persistent Objective", "Aggressive", "Survival-Aware"]
SCENARIOS_ORDER = ["Mission", "Deathmatch", "Control"]

METRIC_COLS = [
    ("objective_commitment_ratio", "Objective\ncommitment"),
    ("engagement_redirection_rate_per_100", "Engagement\nredirection"),
    ("resource_seeking_rate_per_100", "Resource\nseeking"),
    ("avg_ally_proximity", "Cohesion\n(inv. ally distance)"),
]


def _normalise_style_col(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['style'] = df['style'].astype(str).str.replace('–', '-', regex=False)
    return df


def grouped_bars_with_ci(ax, group_labels, series, title, ylabel, show_points: bool = True):
    """series: list of (name, means, cis, raws) tuples, one bar group per label.

    show_points=False draws the bars and confidence intervals only (2026-09-29, journal version: the per-episode
    points hid the bars and the intervals). The default keeps the report's figures unchanged.
    """
    x = np.arange(len(group_labels))
    n = len(series)
    width = 0.8 / n
    for i, (name, means, cis, raws) in enumerate(series):
        offs = (i - (n - 1) / 2) * width
        ax.bar(x + offs, means, width=width * 0.92, yerr=cis, capsize=3, label=name)
        if not show_points:
            continue
        for xi, vals in zip(x + offs, raws):
            vals = np.asarray(vals, dtype=float)
            vals = vals[~np.isnan(vals)]
            if len(vals) == 0:
                continue
            dot_offs = np.linspace(-width * 0.3, width * 0.3, len(vals))
            ax.scatter(xi + dot_offs, vals, s=8, color='black', alpha=0.55, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(group_labels, rotation=20, ha='right')
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(True, axis='y', linewidth=0.3, alpha=0.4)
    ax.legend(fontsize=8)


def make_argument_chain(out_path: Path, o4_verified: bool = False) -> None:
    """Schematic of the paper's deductive chain (no data input; test texts updated to the final testbed and the
    nine-map confirmation 2026-09-25; section numbers follow the Test environments chapter inserted as Section 6).

    Columns: observations -> requirements -> formal elements -> tests.
    The contact-mode row's final arrow is dashed unless `o4_verified` (combat-mode ablation).
    """
    fig, ax = plt.subplots(figsize=(11.5, 4.7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    def box(x, y, w, h, text, fc, fs=6.8):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                    boxstyle="round,pad=0.006",
                                    fc=fc, ec='0.35', lw=0.8))
        ax.text(x, y, text, ha='center', va='center', fontsize=fs)

    def arrow(x0, x1, y, dashed=False):
        ax.annotate('', xy=(x1, y), xytext=(x0, y),
                    arrowprops=dict(arrowstyle='->', lw=0.9, color='0.25',
                                    linestyle='--' if dashed else '-'))

    CX = {'obs': 0.115, 'req': 0.395, 'form': 0.645, 'test': 0.885}
    W = {'obs': 0.21, 'req': 0.225, 'form': 0.185, 'test': 0.205}
    FC = {'obs': '#e8f0fb', 'req': '#fdf1de', 'form': '#e9f7ec', 'test': '#f4ecfa'}

    # Premises banner and column headers
    box(0.255, 0.935, 0.49, 0.075,
        "Premises (Secs. 2, 4.2):  P1 interpretability  ·  P2 real-time  ·  P3 no training",
        fc='#f2f2f2', fs=7.2)
    box(0.765, 0.935, 0.43, 0.075,
        "All primary tests confirmed on nine new maps (Sec. 8.8)",
        fc=FC['test'], fs=7.2)
    ax.annotate('', xy=(CX['req'], 0.83), xytext=(CX['req'], 0.895),
                arrowprops=dict(arrowstyle='->', lw=0.9, color='0.25'))
    for key, label in (('obs', 'Observations (Sec. 3.4)'),
                       ('req', 'Requirements (Sec. 4)'),
                       ('form', 'Form (Sec. 5)'),
                       ('test', 'Tests (Sec. 8)')):
        ax.text(CX[key], 0.80, label, ha='center', va='center',
                fontsize=8, fontweight='bold')

    rows = [
        ("O0 common pool of\nobservable features",
         "state $s_t$ +\nstyle separation (4.1)",
         "observation model\n(Sec. 5.1)",
         "grounded in the\npseudocode (Sec. 3)", False),
        ("O1 concern-importance\ndifferences (+ status-gated\nresources, regrouping)",
         "R1–R4$'$ utilities,\ngates, regroup direction",
         "$U_g$ and\n$\\arg\\max_g w_g U_g$",
         "H1 separated\nfingerprints (8.1)", False),
        ("O2 interruption-rule\ndifferences",
         "R5 persistence\ndevice",
         "$w_{\\mathrm{commit}}$ penalty\n(Eq. 5)",
         "H2 switching rate falls\nwith $w_{\\mathrm{commit}}$ (8.2)", False),
        ("O3 route-preference\ndifferences",
         "R7 goal-invariant\nroute costs",
         "risk-aware A*, exponential\nstep cost (Eqs. 6–9)",
         "H3 walked exposure and\nhits taken lower;\nH3b teammate term (8.3)", False),
        ("O4 contact\nmicro-behaviours",
         "R6 discrete\ndominance modes",
         "hold / keep moving /\nchase / evade",
         ("chase / evade / hold:\nweights-only ablation (8.4)" if o4_verified
          else "partial: structural\nzeros only (8.1)"), not o4_verified),
    ]
    ys = [0.685, 0.545, 0.405, 0.265, 0.115]
    H = 0.115
    for (obs, req, form, test, dashed), y in zip(rows, ys):
        box(CX['obs'], y, W['obs'], H, obs, FC['obs'])
        box(CX['req'], y, W['req'], H, req, FC['req'])
        box(CX['form'], y, W['form'], H, form, FC['form'])
        box(CX['test'], y, W['test'], H, test, FC['test'])
        arrow(CX['obs'] + W['obs'] / 2 + 0.004, CX['req'] - W['req'] / 2 - 0.004, y)
        arrow(CX['req'] + W['req'] / 2 + 0.004, CX['form'] - W['form'] / 2 - 0.004, y)
        arrow(CX['form'] + W['form'] / 2 + 0.004, CX['test'] - W['test'] / 2 - 0.004, y,
              dashed=dashed)

    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def make_maps(out_path: Path, map_name: str = "random") -> None:
    styles = default_styles()
    map_cfg = MAPS[map_name]
    agent_cfg, weapon_cfg = AgentConfig(), WeaponConfig()

    fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.6))
    for ax, sc in zip(axes, default_scenarios()):
        env = FPSEnv(
            map_cfg=map_cfg, agent_cfg=agent_cfg, weapon_cfg=weapon_cfg,
            scenario=sc, styles=styles, rng=random.Random(2026),
        )
        world = env.world
        ax.set_title(f"{sc.name}")
        ax.set_xlim(-0.5, world.width - 0.5)
        ax.set_ylim(-0.5, world.height - 0.5)
        ax.set_aspect('equal')
        ax.invert_yaxis()

        if world.obstacles:
            xs = [p[0] for p in world.obstacles]
            ys = [p[1] for p in world.obstacles]
            ax.scatter(xs, ys, marker='s', s=14, color='0.35', alpha=0.6, label='Obstacle')

        for kind, marker, label in (("health", 'o', 'Health item'), ("ammo", '^', 'Ammo item')):
            pts = [it.pos for it in env.items if it.kind == kind]
            if pts:
                ax.scatter([p[0] for p in pts], [p[1] for p in pts],
                           marker=marker, s=30, label=label)

        # (2026-09-24) both spawn cells of each team (the second agent spawns spawn_separation cells inward)
        spawns_a = sorted({env._spawn_pos(0, i) for i in range(2)})
        spawns_b = sorted({env._spawn_pos(1, i) for i in range(2)})
        ax.scatter([p[0] for p in spawns_a], [p[1] for p in spawns_a], marker='P', s=90, label='Spawn team 0')
        ax.scatter([p[0] for p in spawns_b], [p[1] for p in spawns_b], marker='X', s=90, label='Spawn team 1')

        obj = env.objective_pos()
        if obj is not None:
            ax.scatter([obj[0]], [obj[1]], marker='*', s=160,
                       label='Objective' if sc.mode == 'mission' else 'Control point')

        ax.grid(True, linewidth=0.3, alpha=0.4)

    axes[0].legend(loc='lower left', fontsize=7, framealpha=0.9)
    title = ("Testbed maps (shared obstacle layout, map seed 7; one seeded item placement)" if map_name == "random"
             else f"Testbed maps ({map_name} layout, map seed {map_cfg.seed}; one seeded item placement)")
    fig.suptitle(title, fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(out_path, dpi=200)
    plt.close(fig)


def make_performance_sanity(df: pd.DataFrame, out_path: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(12.6, 3.9))
    for ax, sc_name in zip(axes, SCENARIOS_ORDER):
        sub = df[df['scenario'] == sc_name]
        series = []
        for col, label in (("kills", "Kills"), ("deaths", "Deaths")):
            means, cis, raws = [], [], []
            for s in STYLES_ORDER:
                vals = sub[sub['style'] == s][col].astype(float).values
                m, c = mean_ci(vals)
                means.append(m); cis.append(c); raws.append(vals)
            series.append((label, means, cis, raws))
        grouped_bars_with_ci(ax, STYLES_ORDER, series,
                             title=f"{sc_name}: combat outcomes",
                             ylabel="Count per episode")
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def make_fingerprint_heatmap(df: pd.DataFrame, out_path: Path) -> None:
    # Mean of each metric per (scenario, style) condition
    rows, row_labels = [], []
    for sc_name in SCENARIOS_ORDER:
        for s in STYLES_ORDER:
            sub = df[(df['scenario'] == sc_name) & (df['style'] == s)]
            rows.append([float(sub[col].astype(float).mean()) for col, _ in METRIC_COLS])
            row_labels.append(f"{sc_name} / {s}")
    data = np.asarray(rows, dtype=float)

    # Min-max normalise each metric across the 12 conditions; invert ally
    # distance so the last column reads as cohesion (higher = closer).
    norm = np.zeros_like(data)
    for j in range(data.shape[1]):
        col = data[:, j]
        rng_ = col.max() - col.min()
        norm[:, j] = 0.0 if rng_ == 0 else (col - col.min()) / rng_
    norm[:, 3] = 1.0 - norm[:, 3]

    fig, ax = plt.subplots(figsize=(7.4, 6.4))
    im = ax.imshow(norm, aspect='auto', vmin=0.0, vmax=1.0)
    ax.set_xticks(np.arange(len(METRIC_COLS)))
    ax.set_xticklabels([label for _, label in METRIC_COLS], fontsize=9)
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_yticklabels(row_labels, fontsize=8)
    for i in range(norm.shape[0]):
        for j in range(norm.shape[1]):
            ax.text(j, i, f"{norm[i, j]:.2f}", ha='center', va='center',
                    fontsize=7, color='white' if norm[i, j] < 0.5 else 'black')
    ax.set_title("Normalised behaviour fingerprints (per-metric min-max over 12 conditions)")
    fig.colorbar(im, ax=ax, shrink=0.85)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def make_sensitivity(df: pd.DataFrame, out_path: Path) -> None:
    values = sorted(df['w_commitment'].astype(float).unique())
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.9))

    # Left: Mission objective commitment
    sub = df[df['scenario'] == 'Mission']
    means, cis = [], []
    for w in values:
        vals = sub[sub['w_commitment'].astype(float) == w]['objective_commitment_ratio'].astype(float).values
        m, c = mean_ci(vals)
        means.append(m); cis.append(c)
        axes[0].scatter([w + o for o in np.linspace(-0.02, 0.02, len(vals))], vals,
                        s=9, color='black', alpha=0.5, zorder=3)
    axes[0].errorbar(values, means, yerr=cis, marker='o', capsize=3)
    axes[0].set_xlabel(r"$w_{\mathrm{commit}}$")
    axes[0].set_ylabel("Objective commitment ratio")
    axes[0].set_title("Mission: objective commitment")
    axes[0].grid(True, linewidth=0.3, alpha=0.4)

    # Right: Control score, with wins annotated
    sub = df[df['scenario'] == 'Control']
    means, cis, wins, counts = [], [], [], []
    for w in values:
        vals = sub[sub['w_commitment'].astype(float) == w]['control_score'].astype(float).values
        m, c = mean_ci(vals)
        means.append(m); cis.append(c)
        wins.append(int((vals >= 120).sum())); counts.append(len(vals))
        axes[1].scatter([w + o for o in np.linspace(-0.02, 0.02, len(vals))], vals,
                        s=9, color='black', alpha=0.5, zorder=3)
    axes[1].errorbar(values, means, yerr=cis, marker='o', capsize=3)
    axes[1].axhline(120, linestyle='--', linewidth=0.8, color='0.4')
    for w, k, n in zip(values, wins, counts):
        axes[1].text(w, 128, f"{k}/{n}", ha='center', fontsize=7)
    axes[1].set_ylim(-8, 140)
    axes[1].set_xlabel(r"$w_{\mathrm{commit}}$")
    axes[1].set_ylabel("Control score (win threshold 120)")
    axes[1].set_title("Control: score and wins")
    axes[1].grid(True, linewidth=0.3, alpha=0.4)

    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def make_ablation(df: pd.DataFrame, out_path: Path) -> None:
    conditions = [("Mission", "Mission-Cooperation"), ("Deathmatch", "Survival-Aware")]
    cond_labels = [f"{sc} /\n{st}" for sc, st in conditions]

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.9))
    panels = [
        ("avg_ally_proximity", "Avg. nearest-ally distance", "Teammate cohesion"),
        ("deaths", "Deaths per episode", "Deaths"),
    ]
    for ax, (col, ylabel, title) in zip(axes, panels):
        series = []
        for variant, label in (("full", "Factor-shaped A*"), ("distance_only", "Distance-only A*")):
            means, cis, raws = [], [], []
            for sc_name, st in conditions:
                vals = df[(df['scenario'] == sc_name) & (df['style'] == st)
                          & (df['variant'] == variant)][col].astype(float).values
                m, c = mean_ci(vals)
                means.append(m); cis.append(c); raws.append(vals)
            series.append((label, means, cis, raws))
        grouped_bars_with_ci(ax, cond_labels, series, title=title, ylabel=ylabel)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def make_mode_ablation(df: pd.DataFrame, mode_df: pd.DataFrame, out_path: Path, show_points: bool = True,
                       shared_legend: bool = False) -> None:
    """Full (pinned combat mode) vs weights-only (keep moving) for the key metrics.

    show_points=False: bars and confidence intervals only; shared_legend=True: one legend above the row instead of
    one per panel, so that no legend covers a bar (both for the journal version, 2026-09-29; the defaults keep the
    report's figure unchanged).
    """
    panels = [
        ("Mission", "objective_commitment_ratio", "Objective commitment ratio", "Mission: objective commitment"),
        ("Deathmatch", "engagement_redirection_rate_per_100", "Switches per 100 agent-steps", "Deathmatch: engagement redirection"),
        ("Deathmatch", "resource_seeking_rate_per_100", "Switches per 100 agent-steps", "Deathmatch: resource seeking"),
        ("Control", "control_score", "Control score", "Control: score"),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(15.0, 3.9))
    for ax, (sc_name, col, ylabel, title) in zip(axes, panels):
        series = []
        for label, src in (("Full (pinned mode)", df), ("Weights-only (keep moving)", mode_df)):
            means, cis, raws = [], [], []
            for s in STYLES_ORDER:
                vals = src[(src['scenario'] == sc_name) & (src['style'] == s)][col].astype(float).values
                m, c = mean_ci(vals)
                means.append(m); cis.append(c); raws.append(vals)
            series.append((label, means, cis, raws))
        grouped_bars_with_ci(ax, STYLES_ORDER, series, title=title, ylabel=ylabel, show_points=show_points)
    if shared_legend:
        handles, labels = axes[0].get_legend_handles_labels()
        for ax in axes:
            leg = ax.get_legend()
            if leg is not None:
                leg.remove()
        fig.legend(handles, labels, loc='upper center', ncol=2, fontsize=9, frameon=False)
        fig.tight_layout(rect=(0, 0, 1, 0.93))
    else:
        fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def make_interpolation(df: pd.DataFrame, out_path: Path) -> None:
    """Metric trends along the interpolation parameter alpha (mode fixed to keep moving)."""
    panels = [
        ("Deathmatch", "engagement_redirection_rate_per_100", "Engagement redirection"),
        ("Deathmatch", "resource_seeking_rate_per_100", "Resource seeking"),
        ("Mission", "objective_commitment_ratio", "Objective commitment"),
        ("Mission", "avg_ally_proximity", "Avg. nearest-ally distance"),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(15.0, 3.7))
    for ax, (sc_name, col, ylabel) in zip(axes, panels):
        sub = df[df['scenario'] == sc_name]
        pair = sub['pair'].iloc[0].replace('–', '-')
        alphas = sorted(sub['alpha'].astype(float).unique())
        means, cis = [], []
        for a in alphas:
            vals = sub[sub['alpha'].astype(float) == a][col].astype(float).dropna().values
            m, c = mean_ci(vals)
            means.append(m); cis.append(c)
            ax.scatter(a + np.linspace(-0.02, 0.02, len(vals)), vals, s=6, color='black', alpha=0.35, zorder=3)
        ax.errorbar(alphas, means, yerr=cis, marker='o', capsize=3)
        a_name, b_name = pair.split(' -> ')
        ax.set_xlabel(f"alpha  ({a_name} → {b_name})", fontsize=8)
        ax.set_ylabel(ylabel)
        ax.set_title(f"{sc_name}: {ylabel.lower()}", fontsize=9)
        ax.set_xticks(alphas)
        ax.grid(True, linewidth=0.3, alpha=0.4)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def make_lambda_scale(df: pd.DataFrame, out_path: Path) -> None:
    """Dose-response of the route channel: metrics vs navigation-weight scale k."""
    df = _normalise_style_col(df)
    # (2026-09-24) Survival-Aware's engagement redirection is zero by design under the evade mode, so the
    # route-level readouts (walked expected hits, LOS fraction) replace it.
    panels = [
        ("Mission", "Mission-Cooperation", "avg_ally_proximity", "Avg. nearest-ally distance"),
        ("Deathmatch", "Survival-Aware", "walked_hits_per_step", "Walked expected hits per step"),
        ("Deathmatch", "Survival-Aware", "los_frac", "LOS fraction"),
        ("Deathmatch", "Survival-Aware", "deaths", "Deaths per episode"),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(15.0, 3.7))
    for ax, (sc_name, st, col, ylabel) in zip(axes, panels):
        sub = df[(df['scenario'] == sc_name) & (df['style'] == st)]
        scales = sorted(sub['lambda_scale'].unique())
        pos = np.arange(len(scales))
        means, cis = [], []
        for x, k in zip(pos, scales):
            vals = sub[sub['lambda_scale'] == k][col].astype(float).dropna().values
            m, c = mean_ci(vals)
            means.append(m); cis.append(c)
            ax.scatter(x + np.linspace(-0.08, 0.08, len(vals)), vals, s=6, color='black', alpha=0.35, zorder=3)
        ax.errorbar(pos, means, yerr=cis, marker='o', capsize=3)
        ax.set_xticks(pos)
        ax.set_xticklabels([f"x{k:g}" for k in scales])
        ax.set_xlabel("navigation-weight scale $k$ (x0 = distance-only)", fontsize=8)
        ax.set_ylabel(ylabel)
        ax.set_title(f"{sc_name} / {st}", fontsize=9)
        ax.grid(True, linewidth=0.3, alpha=0.4)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def make_risk_budget(df: pd.DataFrame, main_df: pd.DataFrame, out_path: Path, mode: str) -> None:
    """Risk budget beta: planner-level control and behavioural effect (Deathmatch)."""
    df = _normalise_style_col(df)
    first = (("budget_position", "Budget position $(R-R_{\\min})/(R_0-R_{\\min})$") if mode == "normalised"
             else ("exposure_ratio", "Realised exposure ratio $R(P)/R(P_0)$"))
    panels = [
        first,
        ("length_overhead", "Length overhead $|P|/|P_0|$"),
        ("walked_hits_per_step", "Walked expected hits per step"),
        ("deaths", "Deaths per episode"),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(15.0, 3.7))
    for ax, (col, ylabel) in zip(axes, panels):
        for i, st in enumerate(["Survival-Aware", "Aggressive"]):
            sub = df[df['style'] == st]
            betas = sorted(sub['beta'].astype(float).unique())
            means, cis = [], []
            for b in betas:
                vals = sub[sub['beta'].astype(float) == b][col].astype(float).dropna().values
                m, c = mean_ci(vals)
                means.append(m); cis.append(c)
            line = ax.errorbar(np.array(betas) + (i - 0.5) * 0.012, means, yerr=cis, marker='o', capsize=3, label=st)
            if col in ("engagement_redirection_rate_per_100", "walked_hits_per_step", "deaths"):
                ref = main_df[(main_df['scenario'] == 'Deathmatch') & (main_df['style'] == st)][col].astype(float)
                ax.axhline(ref.mean(), linestyle=':', linewidth=1.0, color=line[0].get_color())
        if col in ("exposure_ratio", "budget_position"):
            lo = 0.0 if mode == "normalised" else 0.25
            ax.plot([lo, 1.0], [lo, 1.0], linestyle='--', linewidth=0.8, color='0.5', label='budget $\\beta$')
        ax.set_xlabel(("normalised" if mode == "normalised" else "relative") + r" risk budget $\beta$")
        ax.set_ylabel(ylabel)
        ax.set_xticks(sorted(df['beta'].astype(float).unique()))
        ax.grid(True, linewidth=0.3, alpha=0.4)
    axes[0].legend(fontsize=7)
    axes[2].set_title("dotted: fixed configured $\\lambda_E$", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def make_cover_model(df: pd.DataFrame, out_path: Path) -> None:
    """Route-cost decomposition: distance-only vs adjacency/threat cover, cover-only and full."""
    df = _normalise_style_col(df)
    variants = [("distance_only", "distance-only"), ("adjacency_cover_only", "adjacency cover only"),
                ("threat_cover_only", "threat cover only"), ("adjacency_full", "adjacency, full"),
                ("threat_full", "threat, full")]
    panels = [
        ("Deathmatch", "Survival-Aware", "walked_hits_per_step", "Walked expected hits per step"),
        ("Deathmatch", "Survival-Aware", "deaths", "Deaths per episode"),
        ("Deathmatch", "Aggressive", "deaths", "Deaths per episode"),
        ("Mission", "Mission-Cooperation", "avg_ally_proximity", "Avg. nearest-ally distance"),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(15.0, 3.9))
    for ax, (sc_name, st, col, ylabel) in zip(axes, panels):
        sub = df[(df['scenario'] == sc_name) & (df['style'] == st)]
        means, cis, raws = [], [], []
        for v, _ in variants:
            vals = sub[sub['variant'] == v][col].astype(float).dropna().values
            m, c = mean_ci(vals)
            means.append(m); cis.append(c); raws.append(vals)
        x = np.arange(len(variants))
        ax.bar(x, means, yerr=cis, capsize=3, color=['0.6', '#e69f00', '#0072b2', '#f0c987', '#7fb8da'])
        for xi, vals in zip(x, raws):
            ax.scatter(xi + np.linspace(-0.25, 0.25, len(vals)), vals, s=6, color='black', alpha=0.4, zorder=3)
        ax.set_xticks(x)
        ax.set_xticklabels([lab for _, lab in variants], rotation=30, ha='right', fontsize=7)
        ax.set_ylabel(ylabel)
        ax.set_title(f"{sc_name} / {st}", fontsize=9)
        ax.grid(True, axis='y', linewidth=0.3, alpha=0.4)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def make_cost_terms(df: pd.DataFrame, out_path: Path) -> None:
    """Leave-one-out ablation of the route-cost terms."""
    df = _normalise_style_col(df)
    variants = [("full", "full"), ("no_exposure", "no exposure"), ("no_cover", "no cover"),
                ("no_separation", "no separation")]
    # (2026-09-24) with lambda_T = 0 in the main model the no-separation variant equals the full configuration
    # episode by episode; it is then left out of the figure.
    key, cols = ['scenario', 'style', 'episode'], ["walked_hits_per_step", "deaths", "avg_ally_proximity",
                                                  "objective_commitment_ratio"]
    full_rows = df[df['variant'] == 'full'].sort_values(key)[cols].astype(float).values
    sep_rows = df[df['variant'] == 'no_separation'].sort_values(key)[cols].astype(float).values
    if full_rows.shape == sep_rows.shape and np.allclose(full_rows, sep_rows, equal_nan=True):
        variants = variants[:3]
    panels = [
        ("Deathmatch", "Survival-Aware", "walked_hits_per_step", "Walked expected hits per step"),
        ("Deathmatch", "Persistent Objective", "walked_hits_per_step", "Walked expected hits per step"),
        ("Deathmatch", "Survival-Aware", "deaths", "Deaths per episode"),
        ("Mission", "Mission-Cooperation", "avg_ally_proximity", "Avg. nearest-ally distance"),
        ("Control", "Aggressive", "objective_commitment_ratio", "Objective commitment"),
    ]
    fig, axes = plt.subplots(1, 5, figsize=(15.0, 3.9))
    for ax, (sc_name, st, col, ylabel) in zip(axes, panels):
        sub = df[(df['scenario'] == sc_name) & (df['style'] == st)]
        means, cis, raws = [], [], []
        for v, _ in variants:
            vals = sub[sub['variant'] == v][col].astype(float).dropna().values
            m, c = mean_ci(vals)
            means.append(m); cis.append(c); raws.append(vals)
        x = np.arange(len(variants))
        ax.bar(x, means, yerr=cis, capsize=3, color=['0.45', '#e69f00', '#56b4e9', '#009e73'][:len(variants)])
        for xi, vals in zip(x, raws):
            ax.scatter(xi + np.linspace(-0.25, 0.25, len(vals)), vals, s=6, color='black', alpha=0.4, zorder=3)
        ax.set_xticks(x)
        ax.set_xticklabels([lab for _, lab in variants], rotation=25, ha='right', fontsize=8)
        ax.set_ylabel(ylabel)
        ax.set_title(f"{sc_name} / {st}", fontsize=9)
        ax.grid(True, axis='y', linewidth=0.3, alpha=0.4)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def make_baselines(bl: pd.DataFrame, main_df: pd.DataFrame, out_path: Path) -> None:
    """Priority-structure styles next to the behaviour tree of the corresponding game, plus utility AI."""
    agents = [("Mission-Cooperation", "MC"), ("CSO-BT", "CSO-BT"), ("Persistent Objective", "PO"), ("OW-BT", "OW-BT"),
              ("Aggressive", "Agg"), ("AC-BT", "AC-BT"), ("Survival-Aware", "SA"), ("XO-BT", "XO-BT"),
              ("UtilityAI", "Utility")]
    colors = ['#0072b2', '#e69f00'] * 4 + ['0.5']
    panels = [
        ("Mission", "objective_commitment_ratio", "Objective commitment"),
        ("Mission", "avg_ally_proximity", "Avg. nearest-ally distance"),
        ("Deathmatch", "engagement_redirection_rate_per_100", "Engagement redirection"),
        ("Deathmatch", "resource_seeking_rate_per_100", "Resource seeking"),
        ("Control", "control_score", "Control score"),
    ]
    fig, axes = plt.subplots(1, 5, figsize=(15.0, 3.9))
    for ax, (sc_name, col, ylabel) in zip(axes, panels):
        means, cis = [], []
        for name, _ in agents:
            src = bl[(bl['scenario'] == sc_name) & (bl['baseline'] == name)] if name in bl['baseline'].unique() else \
                main_df[(main_df['scenario'] == sc_name) & (main_df['style'] == name)]
            m, c = mean_ci(src[col].astype(float).dropna().values)
            means.append(m); cis.append(c)
        x = np.arange(len(agents))
        ax.bar(x, means, yerr=cis, capsize=2, color=colors)
        ax.set_xticks(x)
        ax.set_xticklabels([lab for _, lab in agents], rotation=45, ha='right', fontsize=8)
        ax.set_ylabel(ylabel)
        ax.set_title(sc_name, fontsize=9)
        ax.grid(True, axis='y', linewidth=0.3, alpha=0.4)
    handles = [Patch(facecolor='#0072b2', label='priority structure'), Patch(facecolor='#e69f00', label='behaviour tree'),
               Patch(facecolor='0.5', label='utility AI')]
    axes[1].legend(handles=handles, fontsize=7, loc='upper left')
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


ROUTE_VARIANTS = [("additive", "A additive"), ("centred", "B zero-centred"), ("exp", "C exponential"),
                  ("exp_geo", "D exponential, walking-distance threat"), ("exp_geo_replan", "E = D + replanning"),
                  ("additive_replan", "A + replanning")]


def make_route_metric(df: pd.DataFrame, out_path: Path) -> None:
    """Route-metric experiment: dose-response of route diagnostics and behaviour per variant."""
    df = _normalise_style_col(df).copy()
    df['detour_rate'] = 100.0 * df['n_detour'] / df['n_plans'].where(df['n_plans'] > 0)
    df['exposure_ratio'] = df['sum_exp'] / df['sum_exp0'].where(df['sum_exp0'] > 0)
    panels = [
        ("Deathmatch", "Survival-Aware", "detour_rate", "Plans longer than shortest (%)"),
        ("Deathmatch", "Survival-Aware", "exposure_ratio", "Exposure: planned / shortest path"),
        ("Deathmatch", "Survival-Aware", "engagement_redirection_rate_per_100", "Engagement redirection"),
        ("Deathmatch", "Survival-Aware", "deaths", "Deaths per episode"),
        ("Mission", "Mission-Cooperation", "avg_ally_proximity", "Avg. nearest-ally distance"),
    ]
    scales = sorted(df['lambda_scale'].unique())
    colors = ['0.25', '#e69f00', '#0072b2', '#009e73', '#cc79a7', '0.6']
    markers = ['o', 's', '^', 'D', 'v', 'x']
    fig, axes = plt.subplots(1, 5, figsize=(15.0, 4.3))
    for ax, (sc_name, st, col, ylabel) in zip(axes, panels):
        for i, ((v, lab), colr, mk) in enumerate(zip(ROUTE_VARIANTS, colors, markers)):
            sub = df[(df['scenario'] == sc_name) & (df['style'] == st) & (df['variant'] == v)]
            means, cis = [], []
            for k in scales:
                m, c = mean_ci(sub[sub['lambda_scale'] == k][col].astype(float).dropna().values)
                means.append(m); cis.append(c)
            x = np.arange(len(scales)) + (i - 2.5) * 0.07
            ax.errorbar(x, means, yerr=cis, color=colr, marker=mk, ms=4, lw=1.2, capsize=2, label=lab)
        ax.set_xticks(np.arange(len(scales)))
        ax.set_xticklabels([f"x{k:g}" for k in scales])
        ax.set_xlabel("navigation-weight scale $k$", fontsize=8)
        ax.set_ylabel(ylabel)
        ax.set_title(f"{sc_name} / {st}", fontsize=9)
        ax.grid(True, axis='y', linewidth=0.3, alpha=0.4)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', ncol=6, fontsize=8, frameon=False)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig(out_path)
    plt.close(fig)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--csv", type=str, required=True, help="Path to results.csv")
    p.add_argument("--sensitivity-csv", type=str, required=True,
                   help="Path to sensitivity_commitment.csv")
    p.add_argument("--ablation-csv", type=str, required=True,
                   help="Path to ablation_navigation.csv")
    p.add_argument("--mode-csv", type=str, required=True, help="Path to mode_ablation.csv")
    p.add_argument("--interp-csv", type=str, required=True, help="Path to interpolation.csv")
    p.add_argument("--lambda-csv", type=str, required=True, help="Path to lambda_scale.csv")
    p.add_argument("--budget-relative-csv", type=str, default=None,
                   help="Optional path to risk_budget_relative.csv (additional experiment)")
    p.add_argument("--budget-normalised-csv", type=str, default=None,
                   help="Optional path to risk_budget_normalised.csv (additional experiment)")
    p.add_argument("--map", type=str, default="random", help="Map layout drawn in fig_maps.pdf")
    p.add_argument("--cover-csv", type=str, default=None,
                   help="Optional path to cover_model.csv (additional experiment)")
    p.add_argument("--cost-csv", type=str, default=None,
                   help="Optional path to cost_term_ablation.csv (additional experiment)")
    p.add_argument("--baselines-csv", type=str, default=None,
                   help="Optional path to baselines.csv (additional experiment)")
    p.add_argument("--route-csv", type=str, default=None,
                   help="Optional path to route_metric.csv (additional experiment)")
    p.add_argument("--o4-verified", action="store_true",
                   help="Draw the contact-mode row of the argument chain as verified (solid arrow)")
    p.add_argument("--out", type=str, required=True, help="Output directory for figures")
    args = p.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    df = _normalise_style_col(pd.read_csv(args.csv))
    sens_df = pd.read_csv(args.sensitivity_csv)
    abl_df = _normalise_style_col(pd.read_csv(args.ablation_csv))
    mode_df = _normalise_style_col(pd.read_csv(args.mode_csv))
    interp_df = pd.read_csv(args.interp_csv)
    lambda_df = pd.read_csv(args.lambda_csv)

    make_argument_chain(out_dir / 'fig_argument_chain.pdf', o4_verified=args.o4_verified)
    make_maps(out_dir / 'fig_maps.pdf', args.map)
    make_performance_sanity(df, out_dir / 'fig_performance_sanity.pdf')
    make_fingerprint_heatmap(df, out_dir / 'fig_fingerprint_heatmap.pdf')
    make_sensitivity(sens_df, out_dir / 'fig_sensitivity_commitment.pdf')
    make_ablation(abl_df, out_dir / 'fig_ablation_navigation.pdf')
    make_mode_ablation(df, mode_df, out_dir / 'fig_mode_ablation.pdf')
    make_interpolation(interp_df, out_dir / 'fig_interpolation.pdf')
    make_lambda_scale(lambda_df, out_dir / 'fig_lambda_scale.pdf')
    if args.cover_csv:
        make_cover_model(pd.read_csv(args.cover_csv), out_dir / 'fig_cover_model.pdf')
    if args.cost_csv:
        make_cost_terms(pd.read_csv(args.cost_csv), out_dir / 'fig_cost_terms.pdf')
    if args.baselines_csv:
        make_baselines(pd.read_csv(args.baselines_csv), df, out_dir / 'fig_baselines.pdf')
    if args.route_csv:
        make_route_metric(pd.read_csv(args.route_csv), out_dir / 'fig_route_metric.pdf')
    for mode, path in (("relative", args.budget_relative_csv), ("normalised", args.budget_normalised_csv)):
        if path:
            make_risk_budget(pd.read_csv(path), df, out_dir / f'fig_risk_budget_{mode}.pdf', mode)

    print(f"Saved figures to: {out_dir.resolve()}")


if __name__ == '__main__':
    main()
