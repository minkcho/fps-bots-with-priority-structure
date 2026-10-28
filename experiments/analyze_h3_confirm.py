"""Paired tests for the H3 confirmation simulation (needs scipy; run on mypc).

For each scenario/map/style set, compares every exp condition (field, knowledge, lambda_E) with
the distance-only planner and with the configured additive model (v2) on walked hits per step,
deaths and the scenario outcome, with Wilcoxon signed-rank tests paired by episode (common
random numbers), matched-pairs rank-biserial r, and Holm adjustment across the 12 conditions
within each (set, reference, metric) family.
Usage: python experiments/analyze_h3_confirm.py --dir ../repro_outputs/h3_confirm > ../repro_outputs/h3_confirm/tests.md
"""
from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy import stats


def holm(ps):
    idx = sorted(range(len(ps)), key=lambda i: ps[i])
    adj = [0.0] * len(ps); m = len(ps); running = 0.0
    for rank, i in enumerate(idx):
        val = min(1.0, (m - rank) * ps[i]); running = max(running, val); adj[i] = running
    return adj


def paired(a, b):
    d = np.array(b) - np.array(a)
    nz = d[d != 0]
    if len(nz) == 0:
        return 1.0, 0.0
    p = stats.wilcoxon(nz).pvalue
    ranks = stats.rankdata(np.abs(nz)); wp = ranks[nz > 0].sum(); wn = ranks[nz < 0].sum()
    r = (wp - wn) / (wp + wn)
    return float(p), float(r)


def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument("--dir", default="../repro_outputs/h3_confirm"); ap.add_argument("--metrics", default=None); args = ap.parse_args()
    rows = []
    for f in sorted(Path(args.dir).glob("*.csv")):
        rows += list(csv.DictReader(f.open(encoding="utf-8")))
    sets = defaultdict(lambda: defaultdict(dict))
    for r in rows:
        sets[(r["scenario"], r["map"], r["style"])][(r["field"], r["knowledge"], f"{float(r['lam']):g}")][int(r["episode"])] = r
    for key in sorted(sets, key=lambda k: (["transit", "deathmatch", "control"].index(k[0]), k[1], k[2])):
        conds = sets[key]
        outcome = "arrived" if key[0] == "transit" else ("win" if key[0] == "control" else "kills")
        print(f"\n## {key[0]} / {key[1]} / {key[2]}")
        for ref_name, ref_key in (("distance-only", ("none", "none", "0")), ("v2 configured", ("v2", "all", "0.55"))):
            ref = conds[ref_key]
            for metric in (args.metrics.split(",") if args.metrics else ("walked_hits_per_step", "deaths", outcome)):
                labels, ps, rs, diffs = [], [], [], []
                for c in sorted(k for k in conds if k[0] not in ("none", "v2")):
                    cur = conds[c]; eps = sorted(set(ref) & set(cur))
                    a = [float(ref[e][metric]) for e in eps]; b = [float(cur[e][metric]) for e in eps]
                    p, r = paired(a, b); labels.append(c); ps.append(p); rs.append(r); diffs.append(float(np.mean(b) - np.mean(a)))
                adj = holm(ps)
                print(f"vs {ref_name}, {metric}: " + "; ".join(f"{c[0]}/{c[1]}/l{c[2]} d={d:+.4f} r={r:+.2f} p={p:.3f} pH={ph:.3f}" for c, d, r, p, ph in zip(labels, diffs, rs, ps, adj)))


if __name__ == "__main__":
    main()
