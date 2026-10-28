"""Commitment sweep for all four designed styles (exploratory, 2026-10-12).

Reads, for each map directory under --root (random, urban), the outputs of run_sensitivity_commitment.py
--style {MC,PO,Agg,SA}: sensitivity_commitment.csv (Mission–Cooperation) and sensitivity_commitment_<abbr>.csv.
Writes <root>/summary.md with, per style, scenario and w_commitment, the goal switches per 100 alive steps (mean and
95% t-interval), objective commitment, and Control wins (score at the 120-point threshold); Spearman's rho between
w_commitment and the switch rate per episode; and two reproduction checks: (1) the Mission–Cooperation rows equal
those of the original sweep (<v3dir>/sensitivity_commitment.csv) at every shared value, and (2) each style at its
configured value equals its main-experiment rows (<v3dir>/results.csv). Draws <root>/fig_commit_sweep_styles.pdf.

Usage (artifact virtual environment):
  python experiments/analyze_commit_sweep_styles.py --root ../repro_outputs/commit_sweep_styles \
      --v3 ../repro_outputs/v3_fixed
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_ec_figures import mean_ci  # noqa: E402  (the shared 95% t-interval helper)

STYLES = [("Mission–Cooperation", "MC", "sensitivity_commitment.csv", 0.45),
          ("Persistent Objective", "PO", "sensitivity_commitment_PO.csv", 0.85),
          ("Aggressive", "Agg", "sensitivity_commitment_Agg.csv", 0.25),
          ("Survival-Aware", "SA", "sensitivity_commitment_SA.csv", 0.25)]
MAPS = [("random", ""), ("urban", "urban")]
SCENARIOS = ["Mission", "Control"]
SW = "goal_switch_rate_per_100"
COMPARE = [SW, "objective_commitment_ratio", "engagement_redirection_rate_per_100", "resource_seeking_rate_per_100",
           "avg_ally_proximity", "kills", "deaths", "control_score"]


def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["w"] = df["w_commitment"].astype(float).round(2)
    return df


def same(a: pd.DataFrame, b: pd.DataFrame) -> tuple[bool, int]:
    a = a.sort_values("episode").reset_index(drop=True)
    b = b.sort_values("episode").reset_index(drop=True)
    if len(a) != len(b) or len(a) == 0:
        return False, 0
    ok = True
    for c in COMPARE:
        x = pd.to_numeric(a[c], errors="coerce").fillna(-1).to_numpy()
        y = pd.to_numeric(b[c], errors="coerce").fillna(-1).to_numpy()
        ok &= bool(np.allclose(x, y, atol=1e-9))
    return ok, len(a)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--v3", required=True, help="the final development-map results (v3_fixed)")
    ap.add_argument("--no-figure", action="store_true")
    a = ap.parse_args()
    root, v3 = Path(a.root), Path(a.v3)
    out = ["# Commitment sweep, all four designed styles (exploratory)\n",
           "Goal switches per 100 alive steps (mean [95% CI]), objective commitment, Control wins of 100; "
           "n = 100 episodes per cell; seed 2026; final testbed (five rule flags on).\n"]
    data = {}
    checks = []
    for mname, sub in MAPS:
        d = root / mname
        v3d = v3 / sub if sub else v3
        main_res = pd.read_csv(v3d / "results.csv")
        main_res["style"] = main_res["style"].astype(str)
        orig_mc = load(v3d / "sensitivity_commitment.csv")
        for full, abbr, fname, wconf in STYLES:
            df = load(d / fname)
            data[(mname, abbr)] = df
            for sc in SCENARIOS:
                # check 2: configured value equals the main experiment
                got = df[(df["scenario"] == sc) & (df["w"] == wconf)]
                ref = main_res[(main_res["scenario"] == sc) & (main_res["style"] == full)]
                ok, n = same(got, ref)
                checks.append(f"- {mname}, {abbr}, {sc}, w = {wconf:.2f} vs main experiment: {'identical' if ok else 'DIFFERENT'} ({n} episodes)")
                if abbr == "MC":
                    for w in sorted(set(orig_mc["w"]) & set(df["w"])):
                        ok2, n2 = same(df[(df["scenario"] == sc) & (df["w"] == w)], orig_mc[(orig_mc["scenario"] == sc) & (orig_mc["w"] == w)])
                        if not ok2:
                            checks.append(f"- {mname}, MC, {sc}, w = {w:.2f} vs original sweep: DIFFERENT ({n2})")
                    checks.append(f"- {mname}, MC, {sc}: all shared values vs the original sweep checked (differences listed above, if any)")
    for mname, _ in MAPS:
        out.append(f"\n## {mname} map\n")
        for sc in SCENARIOS:
            out.append(f"\n### {sc}\n")
            ws = sorted(set(data[(mname, 'MC')]["w"]))
            hdr = "| w_commit | " + " | ".join(f"{abbr} switches" for _, abbr, _, _ in STYLES) + " | " + \
                  " | ".join(f"{abbr} obj. commit" for _, abbr, _, _ in STYLES) + (" | " + " | ".join(f"{abbr} wins" for _, abbr, _, _ in STYLES) if sc == "Control" else "") + " |"
            out.append(hdr)
            out.append("|" + "---|" * (hdr.count("|") - 1))
            for w in ws:
                cells_sw, cells_oc, cells_win = [], [], []
                for full, abbr, _, wconf in STYLES:
                    g = data[(mname, abbr)]
                    g = g[(g["scenario"] == sc) & (g["w"] == w)]
                    m, c = mean_ci(g[SW].astype(float).values)
                    star = "*" if abs(w - wconf) < 1e-9 else ""
                    cells_sw.append(f"{m:.2f} [{m - c:.2f}, {m + c:.2f}]{star}")
                    cells_oc.append(f"{g['objective_commitment_ratio'].astype(float).mean():.2f}")
                    if sc == "Control":
                        cells_win.append(str(int((g["control_score"].astype(float) >= 120).sum())))
                out.append(f"| {w:.2f} | " + " | ".join(cells_sw) + " | " + " | ".join(cells_oc) + (" | " + " | ".join(cells_win) if sc == "Control" else "") + " |")
            out.append("\n* = the style's configured value (the main experiment).\n")
            for full, abbr, _, _ in STYLES:
                g = data[(mname, abbr)]
                g = g[g["scenario"] == sc]
                rho, p = stats.spearmanr(g["w"], g[SW].astype(float))
                m0 = g[g["w"] == 0.0][SW].astype(float).mean()
                m1 = g[g["w"] == 1.25][SW].astype(float).mean()
                out.append(f"- {abbr}: Spearman rho(w, switches) = {rho:.2f} (p = {p:.1e}); switches at w = 0 {m0:.2f} -> at w = 1.25 {m1:.2f} ({100 * (m1 - m0) / m0:+.0f}%)")
    out.append("\n## Reproduction checks\n")
    out += checks
    (root / "summary.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))
    if not a.no_figure:
        draw(data, root / "fig_commit_sweep_styles.pdf")


def draw(data, out: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    try:
        path = subprocess.run(["kpsewhich", "texgyrepagella-regular.otf"], capture_output=True, text=True).stdout.strip()
        if path:
            font_manager.fontManager.addfont(path)
            matplotlib.rcParams["font.family"] = "serif"
            matplotlib.rcParams["font.serif"] = ["TeX Gyre Pagella"]
    except OSError:
        pass
    fs = 7.5
    names = {"MC": "Mission-Cooperation (hold)", "PO": "Persistent Objective (keep moving)", "Agg": "Aggressive (chase)", "SA": "Survival-Aware (evade)"}
    fig, axes = plt.subplots(2, 2, figsize=(7.27, 4.4), sharex=True)
    for i, (mname, _) in enumerate(MAPS):
        for j, sc in enumerate(SCENARIOS):
            ax = axes[i, j]
            for (full, abbr, _, wconf), color in zip(STYLES, ["tab:blue", "tab:orange", "tab:red", "tab:green"]):
                g = data[(mname, abbr)]
                g = g[g["scenario"] == sc]
                ws = sorted(set(g["w"]))
                ms, cs = [], []
                for w in ws:
                    m, c = mean_ci(g[g["w"] == w][SW].astype(float).values)
                    ms.append(m); cs.append(c)
                ms, cs = np.array(ms), np.array(cs)
                ax.plot(ws, ms, marker="o", ms=2.5, lw=1.0, color=color, label=names[abbr])
                ax.fill_between(ws, ms - cs, ms + cs, color=color, alpha=0.15, lw=0)
                k = ws.index(wconf)
                ax.plot([wconf], [ms[k]], marker="o", ms=6, mfc="none", mec=color, mew=1.0)
            ax.set_yscale("log")
            ax.set_title(f"{sc}, {mname} map", fontsize=fs)
            ax.tick_params(labelsize=fs, length=2)
            ax.grid(True, which="both", axis="y", linewidth=0.3, alpha=0.4)
            if j == 0:
                ax.set_ylabel("Goal switches per 100 alive steps", fontsize=fs)
            if i == 1:
                ax.set_xlabel("$w_{\\mathrm{commit}}$", fontsize=fs)
    h, l = axes[0, 0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=4, fontsize=fs, frameon=False)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(out)
    fig.savefig(out.with_suffix(".png"), dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    main()
