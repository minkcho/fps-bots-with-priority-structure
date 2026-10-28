"""Aggregate the H3 factorial CSVs into performance tables (standard library only).

Usage: python experiments/analyze_h3_factorial.py --dir ../repro_outputs/h3_factorial [--md out.md]
"""
from __future__ import annotations

import argparse
import csv
import statistics as st
from collections import defaultdict
from pathlib import Path

KEY = ["scenario", "map", "style", "field", "knowledge", "form", "replan", "lam"]
COLS = ["walked_hits_per_step", "los_frac", "plan_detour", "plan_len_ratio", "plan_exp_ratio", "deaths", "kills",
        "arrived", "arrival_step", "win", "control_score", "engagement_redirection", "objective_commitment", "ally_distance"]


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="../repro_outputs/h3_factorial")
    p.add_argument("--md", default=None)
    p.add_argument("--compact", action="store_true")
    p.add_argument("--levels", default="5,20")
    args = p.parse_args()
    rows = []
    for f in sorted(Path(args.dir).glob("*.csv")):
        rows += list(csv.DictReader(f.open(encoding="utf-8")))
    groups = defaultdict(list)
    for r in rows:
        groups[tuple(r[k] for k in KEY)].append(r)
    out = []
    by_table = defaultdict(list)
    for key, rs in sorted(groups.items(), key=lambda kv: (kv[0][:3], kv[0][3], kv[0][4], kv[0][5], int(kv[0][6]), float(kv[0][7]))):
        agg = {"n": len(rs)}
        for c in COLS:
            vals = [fnum(r.get(c)) for r in rs]
            vals = [v for v in vals if v is not None and v == v]
            agg[c] = st.mean(vals) if vals else None
        by_table[key[:3]].append((key[3:], agg))
    for tab, items in by_table.items():
        cols = [c for c in COLS if any(a[c] is not None for _, a in items)]
        out.append(f"\n## {tab[0]} / {tab[1]} / {tab[2]}\n")
        out.append("| field | knowledge | form | replan | lam | n | " + " | ".join(cols) + " |")
        out.append("|" + "---|" * (6 + len(cols)))
        for (field, knowledge, form, replan, lam), a in items:
            cells = [f"{a[c]:.4f}" if isinstance(a[c], float) else "" for c in cols]
            out.append(f"| {field} | {knowledge} | {form} | {replan} | {float(lam):g} | {a['n']} | " + " | ".join(cells) + " |")
    text = "\n".join(out)
    if args.md:
        Path(args.md).write_text(text + "\n", encoding="utf-8")
    if not args.compact:
        print(text)
        return
    # Compact view: one row per (field, knowledge, form, replan) with the baseline (lam 0) and two lam levels.
    lam_levels = [float(x) for x in args.levels.split(",")]
    for tab, items in by_table.items():
        d = {k: a for k, a in items}
        outcome = "arrived" if any(a.get("arrived") is not None for _, a in items) else ("win" if any(a.get("win") is not None for _, a in items) else "deaths")
        print(f"\n## {tab[0]} / {tab[1]} / {tab[2]}  (cells: hits/step | LOS frac | detour | deaths | {outcome}; columns lam = 0, {', '.join(f'{l:g}' for l in lam_levels)})")
        print("| field | knowledge | form | replan | " + " | ".join(["lam 0"] + [f"lam {l:g}" for l in lam_levels]) + " |")
        print("|---|---|---|---|" + "---|" * (1 + len(lam_levels)))
        def cell(a):
            if a is None:
                return "-"
            f = lambda k, fmt: (fmt % a[k]) if a.get(k) is not None else "-"
            return f"{f('walked_hits_per_step', '%.4f')} / {f('los_frac', '%.3f')} / {f('plan_detour', '%.3f')} / {f('deaths', '%.2f')} / {f(outcome, '%.2f')}"
        seen = set()
        for (field, knowledge, form, replan, lam), a in items:
            if field == "none" or (field, knowledge, form, replan) in seen:
                continue
            seen.add((field, knowledge, form, replan))
            base = d.get(("none", "none", "additive", replan, "0.0")) or d.get(("none", "none", "additive", replan, "0"))
            cells = [cell(base)] + [cell(d.get((field, knowledge, form, replan, f"{l}")) or d.get((field, knowledge, form, replan, f"{l:g}"))) for l in lam_levels]
            print(f"| {field} | {knowledge} | {form} | {replan} | " + " | ".join(cells) + " |")


if __name__ == "__main__":
    main()
