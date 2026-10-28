"""Descriptive summary of the round v13 development pilot (2026-09-29; development seeds 5801 / 5901, not a result).

Reads the rows of run_form_variants.py (parts a, b, calib) and run_weight_adaptation.py (parts step, closed) and
writes the tables that the draft protocol (FAMILY_ADAPT_PLAN_V13_DRAFT.md) uses to fix its grids, thresholds and
predictions: means per condition, the style classification accuracy of each distance transform (cross-validated
logistic regression of analyze_hypotheses.classify, few permutations), the dwell time matching each style's main-model
switching rate, the open-loop time courses per 25-step bin and the closed-loop outcomes on the steps a rule is active.
Usage: python experiments/summarize_v13_pilot.py --fv ../repro_outputs/dev_v13/fv --wa ../repro_outputs/dev_v13/wa \
           --out ../repro_outputs/dev_v13/pilot_summary.md
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_hypotheses import classify  # noqa: E402

STYLES = ["MC", "PO", "Agg", "SA"]
SCEN = ["Mission", "Deathmatch", "Control"]
MEASURES = {   # column: (label, scenarios in which it is read)
    "objective_commitment_ratio": ("objective", ["Mission", "Control"]),
    "far_objective_share": ("far obj.", ["Mission", "Control"]),
    "goal_switch_rate_per_100": ("switches", SCEN),
    "engagement_redirection_rate_per_100": ("redirect.", SCEN),
    "retreat_share": ("retreat", SCEN),
    "resource_goal_share_good": ("item ctrl", SCEN),
    "idle_item_chain_rate_per_100": ("chains", SCEN),
    "share_teammate": ("teammate", SCEN),
    "far_pursuit_share": ("far pursuit", ["Deathmatch"]),
    "kill_rate_per_100": ("kills", ["Deathmatch"]),
    "death_rate_per_100": ("deaths", ["Deathmatch"]),
    "control_score": ("ctrl score", ["Control"]),
}


def num(df: pd.DataFrame) -> pd.DataFrame:
    for c in df.columns:
        if c not in ("part", "style", "variant", "map", "scenario", "condition", "schedule"):
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def table(df: pd.DataFrame, by: list, cols: list, fmt: str = "{:.3f}") -> list:
    g = df.groupby(by, sort=False)[cols].mean()
    lines = ["| " + " | ".join(by + cols) + " |", "|" + "---|" * (len(by) + len(cols))]
    for k, r in g.iterrows():
        k = k if isinstance(k, tuple) else (k,)
        lines.append("| " + " | ".join(map(str, k)) + " | " + " | ".join(
            "" if pd.isna(r[c]) else fmt.format(r[c]) for c in cols) + " |")
    return lines


def fv_sections(fv: Path) -> list:
    md = []
    if (fv / "rows_a.csv").exists():
        a = num(pd.read_csv(fv / "rows_a.csv"))
        md += ["## FV-a distance transform (means over the two maps)", ""]
        for sc in SCEN:
            cols = [c for c, (_, scs) in MEASURES.items() if sc in scs]
            md += [f"### {sc}", ""] + table(a[a["scenario"] == sc], ["style", "variant"], cols) + [""]
        md += ["### Style classification accuracy (5-fold logistic regression; 4 styles, chance 0.25)", "",
               "| variant | map | " + " | ".join(SCEN) + " |", "|---|---|" + "---|" * len(SCEN)]
        for v in a["variant"].unique():
            for m in a["map"].unique():
                d = a[(a["variant"] == v) & (a["map"] == m)]
                enough = d.groupby(["scenario", "style"]).size().min() >= 5      # 5-fold cross-validation
                acc = [classify(d, sc, n_perm=20)["accuracy"] if enough else np.nan for sc in SCEN]
                md.append(f"| {v} | {m} | " + " | ".join(f"{x:.2f}" for x in acc) + " |")
        md.append("")
    if (fv / "rows_b.csv").exists():
        b = num(pd.read_csv(fv / "rows_b.csv"))
        b["win"] = np.where(b["scenario"] == "Control", (b["control_score"] >= 120).astype(float), np.nan)
        md += ["## FV-b Mission-Cooperation: penalty grid and dwell times (means over the two maps)", ""]
        for sc in SCEN:
            cols = [c for c, (_, scs) in MEASURES.items() if sc in scs] + (["win"] if sc == "Control" else [])
            md += [f"### {sc}", ""] + table(b[b["scenario"] == sc], ["variant"], cols) + [""]
    if (fv / "rows_calib.csv").exists():
        c = num(pd.read_csv(fv / "rows_calib.csv"))
        md += ["## Calibration: goal switches per 100 steps with dwell time N (w_commitment = 0) vs the main model", ""]
        rate = c.groupby(["style", "variant"])["goal_switch_rate_per_100"].mean()
        per_sc = c.groupby(["style", "variant", "scenario"])["goal_switch_rate_per_100"].mean()
        md += ["| style | main | " + " | ".join(v for v in c["variant"].unique() if v != "main") + " | matched N |",
               "|---|---|" + "---|" * (c["variant"].nunique())]
        for s in STYLES:
            if s not in rate.index.get_level_values(0):
                continue
            main = rate[(s, "main")]
            others = {v: rate[(s, v)] for v in c["variant"].unique() if v != "main"}
            best = min(others, key=lambda v: abs(others[v] - main))
            md.append(f"| {s} | {main:.2f} | " + " | ".join(f"{x:.2f}" for x in others.values()) + f" | {best} |")
        md += ["", "Per scenario (main / matched):", ""]
        for s in STYLES:
            if s not in rate.index.get_level_values(0):
                continue
            others = {v: rate[(s, v)] for v in c["variant"].unique() if v != "main"}
            best = min(others, key=lambda v: abs(others[v] - rate[(s, "main")]))
            md.append(f"- {s} ({best}): " + ", ".join(
                f"{sc} {per_sc[(s, 'main', sc)]:.2f} / {per_sc[(s, best, sc)]:.2f}" for sc in SCEN))
        md += ["", "### Other measures, main vs dwell times", ""]
        for sc in SCEN:
            cols = [col for col, (_, scs) in MEASURES.items() if sc in scs]
            md += [f"#### {sc}", ""] + table(c[c["scenario"] == sc], ["style", "variant"], cols) + [""]
    return md


def rates(g: pd.DataFrame) -> pd.Series:
    s = g.sum(numeric_only=True)
    alive = s["alive"] or np.nan
    return pd.Series({"objective": s["obj"] / alive, "resource": s["res"] / alive, "teammate": s["tm"] / alive,
                      "enemy": s["enemy"] / alive, "switches/100": 100 * s["switches"] / alive,
                      "exp. hits": s["exp_hits"] / alive, "los": s["los"] / alive,
                      "ally dist": s["ally_sum"] / s["ally_n"] if s["ally_n"] else np.nan,
                      "kills/100": 100 * s["kills"] / alive, "deaths/100": 100 * s["deaths"] / alive,
                      "pts own": s["pts_own"] / len(g), "pts opp": s["pts_opp"] / len(g)})


WINDOWS = {"pre 101-200": range(4, 8), "201-225": [8], "226-250": [9], "251-300": range(10, 12),
           "301-350": range(12, 14), "late 351-550": range(14, 22)}


def wa_sections(wa: Path) -> list:
    md = []
    if (wa / "bins_step.csv").exists():
        b = num(pd.read_csv(wa / "bins_step.csv"))
        md += ["## WA-1 open loop (change at step 200; rates over team 0's alive agent-steps, pooled over maps)", ""]
        for cond in b["condition"].unique():
            d = b[b["condition"] == cond]
            md += [f"### {cond} ({d['style'].iloc[0]}, {d['scenario'].iloc[0]})", "",
                   "| schedule | window | " + " | ".join(rates(d.head(1)).index) + " |",
                   "|---|---|" + "---|" * len(rates(d.head(1)))]
            for sch in ("none", "abrupt", "gradual"):
                for wname, bins in WINDOWS.items():
                    r = rates(d[(d["schedule"] == sch) & (d["bin"].isin(list(bins)))])
                    md.append(f"| {sch} | {wname} | " + " | ".join(f"{x:.3f}" for x in r) + " |")
            md.append("")
            w = d[d["schedule"] != "none"].groupby(["schedule", "bin"])[
                ["w_objective", "w_engage", "w_resource", "w_team", "w_commitment", "w_exposure"]].mean()
            md += ["Applied weights at bins 7-12 (steps 176-325):", "", "```", w.loc[(slice(None), slice(7, 12)), :]
                   .round(3).to_string(), "```", ""]
    if (wa / "episodes_closed.csv").exists():
        e = num(pd.read_csv(wa / "episodes_closed.csv"))
        md += ["## WA-2 closed loop (fixed = shadow triggers; per rule: share of steps active and the outcome on the "
               "active steps, pooled over maps and episodes)", ""]
        md += ["| style | scenario | schedule | R1 act. | R1 pts own-opp /step | R2 act. | R2 ally dist | R3 act. | "
               "R3 exp. hits | R4 act. | R4 los | switches/100 | kills/100 | deaths/100 | pts own-opp |",
               "|---|---|---|" + "---|" * 12]
        for (s, sc, sch), g in e.groupby(["style", "scenario", "schedule"], sort=False):
            t = g.sum(numeric_only=True)
            act = {r: t[f"{r}_active_steps"] / t["steps"] for r in ("R1", "R2", "R3", "R4")}

            def ratio(a, b):
                return t[a] / t[b] if t[b] else np.nan
            vals = [act["R1"], ratio("R1_pts_own", "R1_active_steps") - ratio("R1_pts_opp", "R1_active_steps"),
                    act["R2"], ratio("R2_ally_sum", "R2_ally_n"), act["R3"], ratio("R3_exp_hits", "R3_alive"),
                    act["R4"], ratio("R4_los", "R4_alive"), 100 * ratio("switches", "alive"),
                    100 * ratio("kills", "alive"), 100 * ratio("deaths", "alive"),
                    (t["pts_own"] - t["pts_opp"]) / len(g)]
            md.append(f"| {s} | {sc} | {sch} | " + " | ".join("" if pd.isna(v) else f"{v:.3f}" for v in vals) + " |")
        md.append("")
    return md


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--fv", default="../repro_outputs/dev_v13/fv")
    p.add_argument("--wa", default="../repro_outputs/dev_v13/wa")
    p.add_argument("--out", default="../repro_outputs/dev_v13/pilot_summary.md")
    a = p.parse_args()
    md = ["# Round v13 development pilot (development seeds; not a result)", ""]
    md += fv_sections(Path(a.fv)) + wa_sections(Path(a.wa))
    Path(a.out).write_text("\n".join(md) + "\n")
    print(f"written: {a.out}")


if __name__ == "__main__":
    main()
