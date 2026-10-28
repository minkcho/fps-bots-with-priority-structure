"""Cross-map confirmation analysis (2026-09-25; protocol: CONFIRMATION_PLAN, part A, Level 2 and verdicts).

Reads, for every map directory under --root, the per-map primary tests of analyze_hypotheses.py
(hypotheses_summary.json, Level 1) and the raw CSVs, and computes one cross-map p-value per test over the
confirmatory maps (the nine new maps; --maps overrides), Holm-adjusted across the 21 Level-2 tests:

  H1 (10 tests), H2 (2)  intersection-union test: p = the largest per-map p (one-sided in the predicted direction
                         for the paired tests; the Kruskal-Wallis and classification p are used as they are)
  H3 per style (4), H3b, H4 (2), hits taken (pooled Deathmatch test over the four styles)
                         random-effects meta-analysis of the per-map effects (matched-pairs r, or Fisher z of
                         Spearman rho; bootstrap standard errors), REML, Hartung-Knapp, k - 1 df, one-sided
  H3 sign test           per map the share of the 12 scenario x style conditions with lower walked expected hits;
                         one-sided one-sample t-test of the mean share > 0.5

Smallest effects of interest (standardised, set before the confirmation run and independently of the development
values): Kruskal-Wallis eps^2 >= 0.10; classification accuracy >= 0.40; mode ablation r >= 0.5 and H2 r <= -0.5
(median over maps); H3 per style, hits taken and H3b pooled r <= -0.2; H3 sign test mean share >= 0.75; H4
engagement pooled rho <= -0.3; H4 cohesion pooled rho >= 0.1 (the endpoints of that blend differ by about one
cell). Raw-unit effects (percent change, cells) are reported alongside.

Verdicts per test: confirmed = Level-2 Holm p < 0.05, predicted direction on >= 8 of 9 maps, pooled effect at
least the SESOI; partly confirmed = Level-2 significant but not the rest; not confirmed = otherwise. Per
hypothesis: confirmed if all its tests are, partly if at least half are and none is significant in the opposite
direction, otherwise not confirmed; H3 with only Survival-Aware failing = partly confirmed. Counts of per-map
significant tests are descriptive.

Usage: python experiments/analyze_map_confirmation.py --root ../repro_outputs/v4_maps [--maps ...] [--boot 1000]
"""
from __future__ import annotations

import argparse
import json
import sys
import zlib
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import optimize, stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analyze_stats import STYLES, holm, load, wilcoxon_paired  # noqa: E402
from fps_priority_ai.maps import CONFIRMATION_MAPS  # noqa: E402

DEVELOPMENT = ("random", "urban")
CONFIRMATORY = tuple(m for m in CONFIRMATION_MAPS if m not in DEVELOPMENT)
SCENARIOS = ["Mission", "Deathmatch", "Control"]
# smallest effect sizes of interest (pre-registered); applied to the pooled (meta-analysis) or median per-map effects
SESOI = {"kw_eps2": 0.10, "accuracy": 0.40, "mode_r": 0.50, "h2_r": -0.50, "h3_r": -0.20, "sign_share": 0.75,
         "hits_r": -0.20, "h3b_r": -0.20, "h4_eng_rho": -0.30, "h4_coh_rho": 0.10}


# ------------------------------------------------------------------------------------------ statistics
def one_sided(p_two: float, effect: float, sign: int) -> float:
    """One-sided p in the direction sign (+1: effect > 0 predicted, -1: effect < 0 predicted)."""
    return p_two / 2 if np.sign(effect) == sign and effect != 0 else 1 - p_two / 2


def boot_se(fn, n: int, rng, boot: int, strata=None) -> float:
    vals = []
    for _ in range(boot):
        if strata is None:
            idx = rng.integers(0, n, n)
        else:
            idx = np.concatenate([rng.choice(s, len(s)) for s in strata])
        v = fn(idx)
        if np.isfinite(v):
            vals.append(v)
    return float(np.std(vals, ddof=1)) if len(vals) > 1 else float("nan")


def reml_hk(y, v, sign: int) -> dict:
    """Random-effects meta-analysis: REML tau^2, Hartung-Knapp SE, t with k - 1 df, one-sided p (sign)."""
    y, v = np.asarray(y, float), np.asarray(v, float)
    k = len(y)

    def nll(t2):
        w = 1 / (v + t2)
        mu = np.sum(w * y) / np.sum(w)
        return 0.5 * (np.sum(np.log(v + t2)) + np.log(np.sum(w)) + np.sum(w * (y - mu) ** 2))
    hi = max(10 * np.var(y, ddof=1), 1e-8) if k > 1 else 1e-8
    t2 = float(optimize.minimize_scalar(nll, bounds=(0.0, hi), method="bounded").x)
    w = 1 / (v + t2)
    mu = float(np.sum(w * y) / np.sum(w))
    q = float(np.sum(w * (y - mu) ** 2) / (k - 1))
    se = float(np.sqrt(q / np.sum(w)))
    t = mu / se if se > 0 else np.inf * np.sign(mu)
    p = float(stats.t.sf(sign * t, k - 1))
    tq = stats.t.ppf(0.975, k - 1)
    pi = stats.t.ppf(0.975, max(k - 2, 1)) * np.sqrt(t2 + se ** 2)
    return {"mu": mu, "se": se, "tau2": t2, "p": p, "ci": [mu - tq * se, mu + tq * se], "pi": [mu - pi, mu + pi], "k": k}


def paired(a: pd.DataFrame, b: pd.DataFrame, col: str) -> tuple[np.ndarray, np.ndarray]:
    m = a[["episode", col]].merge(b[["episode", col]], on="episode", suffixes=("_a", "_b")).dropna()
    return m[col + "_a"].to_numpy(float), m[col + "_b"].to_numpy(float)


def rb_r(x, y) -> float:
    """Matched-pairs rank-biserial r of x - y (the r of analyze_stats.wilcoxon_paired, without its p-value, which
    scipy may compute by permutation for small samples; used inside the bootstrap)."""
    d = np.asarray(x, float) - np.asarray(y, float)
    d = d[~np.isnan(d)]
    nz = d[d != 0]
    if len(nz) == 0:
        return 0.0
    ranks = stats.rankdata(np.abs(nz))
    return float((ranks[nz > 0].sum() - ranks[nz < 0].sum()) / ranks.sum())


def r_effect(x, y, rng, boot) -> dict:
    w = wilcoxon_paired(x, y)
    se = boot_se(lambda i: rb_r(x[i], y[i]), len(x), rng, boot)
    rel = float((np.mean(x) - np.mean(y)) / np.mean(y)) if np.mean(y) else float("nan")
    return {"r": w["r"], "p_two": w["p"], "se": se, "diff": float(np.mean(x - y)), "rel": rel}


# ------------------------------------------------------------------------------------------ per map
def per_map(d: Path, rng, boot: int) -> dict:
    hs = json.loads((d / "hypotheses_summary.json").read_text())["primary"]
    lvl1 = {(t["hypothesis"], t["test"]): t for t in hs}
    main, sens = load(d / "results.csv"), load(d / "sensitivity_commitment.csv")
    mode, interp = load(d / "mode_ablation.csv"), load(d / "interpolation.csv")
    ct, tt = load(d / "cost_term_ablation.csv"), load(d / "teammate_term.csv")
    out = {"level1": lvl1}
    # H1 mode ablation (full > weights-only)
    for st, col in (("Survival-Aware", "resource_seeking_rate_per_100"), ("Aggressive", "engagement_redirection_rate_per_100")):
        x, y = paired(main[(main.scenario == "Deathmatch") & (main["style"] == st)],
                      mode[(mode.scenario == "Deathmatch") & (mode["style"] == st)], col)
        out[f"mode|{st}"] = r_effect(x, y, rng, 0)
    # H2 (fewer switches with w_commit 0.45)
    for sc in ("Mission", "Control"):
        g = sens[sens.scenario == sc]
        x, y = paired(g[g.w_commitment.round(2) == 0.45], g[g.w_commitment == 0.0], "goal_switch_rate_per_100")
        out[f"h2|{sc}"] = r_effect(x, y, rng, 0)
    # H3 per style (Deathmatch) and the sign-test share
    lower = 0
    for sc in SCENARIOS:
        for st in STYLES:
            g = ct[(ct.scenario == sc) & (ct["style"] == st)]
            x, y = paired(g[g.variant == "full"], g[g.variant == "no_exposure"], "walked_hits_per_step")
            lower += int(np.mean(x) < np.mean(y))
            if sc == "Deathmatch":
                out[f"h3|{st}"] = r_effect(x, y, rng, boot)
    out["h3_share"] = lower / 12
    # hits taken, Deathmatch, four styles pooled (resampling within style)
    xs, ys, strata, start = [], [], [], 0
    for st in STYLES:
        g = ct[(ct.scenario == "Deathmatch") & (ct["style"] == st)]
        x, y = paired(g[g.variant == "full"], g[g.variant == "no_exposure"], "hits_taken_per_step")
        xs.append(x); ys.append(y); strata.append(np.arange(start, start + len(x))); start += len(x)
    X, Y = np.concatenate(xs), np.concatenate(ys)
    w = wilcoxon_paired(X, Y)
    out["hits"] = {"r": w["r"], "p_two": w["p"], "rel": float((X.mean() - Y.mean()) / Y.mean()),
                   "se": boot_se(lambda i: rb_r(X[i], Y[i]), len(X), rng, boot, strata)}
    # H3b
    g = tt[(tt.scenario == "Deathmatch") & (tt["style"] == "Mission–Cooperation")]
    x, y = paired(g[g.lambda_T == 10], g[g.lambda_T == 0], "avg_ally_proximity")
    out["h3b"] = r_effect(x, y, rng, boot)
    # H4 engagement (Spearman rho along alpha, Fisher z) and cohesion (OLS change over alpha 0 -> 1)
    g = interp[interp.scenario == "Deathmatch"][["alpha", "engagement_redirection_rate_per_100"]].dropna()
    a, e = g.alpha.to_numpy(float), g.engagement_redirection_rate_per_100.to_numpy(float)
    rho = stats.spearmanr(a, e).statistic
    z_se = boot_se(lambda i: np.arctanh(np.clip(stats.spearmanr(a[i], e[i]).statistic, -0.999, 0.999)), len(a), rng, boot)
    out["h4_eng"] = {"rho": float(rho), "z": float(np.arctanh(np.clip(rho, -0.999, 0.999))), "se": z_se,
                     "p_two": float(stats.spearmanr(a, e).pvalue)}
    g = interp[interp.scenario == "Mission"][["alpha", "avg_ally_proximity"]].dropna()
    a, c = g.alpha.to_numpy(float), g.avg_ally_proximity.to_numpy(float)
    rho = stats.spearmanr(a, c).statistic
    z_se = boot_se(lambda i: np.arctanh(np.clip(stats.spearmanr(a[i], c[i]).statistic, -0.999, 0.999)), len(a), rng, boot)
    out["h4_coh"] = {"rho": float(rho), "z": float(np.arctanh(np.clip(rho, -0.999, 0.999))), "se": z_se,
                     "change_cells": float(stats.linregress(a, c).slope)}
    return out


def per_map_seeded(d: Path, name: str, boot: int) -> dict:
    """per_map with a bootstrap stream fixed by the map name (maps are analysed in parallel)."""
    return per_map(d, np.random.default_rng([2028, zlib.crc32(name.encode())]), boot)


# ------------------------------------------------------------------------------------------ main
def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="../repro_outputs/v4_maps")
    p.add_argument("--maps", default=",".join(CONFIRMATORY), help="maps of the confirmatory analysis")
    p.add_argument("--boot", type=int, default=1000)
    p.add_argument("--tag", default="", help="suffix of the output files (e.g. 11maps)")
    p.add_argument("--jobs", type=int, default=11, help="maps analysed in parallel")
    a = p.parse_args()
    root, maps = Path(a.root), a.maps.split(",")
    with Pool(min(len(maps), a.jobs)) as pool:
        M = dict(zip(maps, pool.starmap(per_map_seeded, [(root / m, m, a.boot) for m in maps])))
    k = len(maps)
    tests = []   # (key, hypothesis, label, p_level2, effect summary, n maps in predicted direction, meets SESOI)

    def lv1(m, h, prefix):
        return next(t for (hh, lab), t in M[m]["level1"].items() if hh == h and lab.startswith(prefix))
    # H1 Kruskal-Wallis and classification: IUT on the Level-1 p
    for prefix in ("Kruskal-Wallis, Mission ObjCommit", "Kruskal-Wallis, Mission AllyDist", "Kruskal-Wallis, Deathmatch EngRedirect",
                   "Kruskal-Wallis, Deathmatch ResSeek", "Kruskal-Wallis, Control CtrlScore"):
        ts = [lv1(m, "H1", prefix) for m in maps]
        eps = [t["raw"]["eps2"] for t in ts]
        tests.append(("H1", prefix, max(t["p"] for t in ts), f"eps2 median {np.median(eps):.2f} (min {min(eps):.2f})",
                      sum(e >= SESOI["kw_eps2"] for e in eps), bool(np.median(eps) >= SESOI["kw_eps2"])))
    for sc in SCENARIOS:
        ts = [lv1(m, "H1", f"Style classification, {sc}") for m in maps]
        acc = [t["raw"]["accuracy"] for t in ts]
        tests.append(("H1", f"Style classification, {sc}", max(t["p"] for t in ts),
                      f"accuracy median {np.median(acc):.2f} (min {min(acc):.2f})",
                      sum(x > 0.25 for x in acc), bool(np.median(acc) >= SESOI["accuracy"])))
    for st in ("Survival-Aware", "Aggressive"):
        es = [M[m][f"mode|{st}"] for m in maps]
        tests.append(("H1", f"Mode ablation, Deathmatch {st} (full > weights-only)",
                      max(one_sided(e["p_two"], e["r"], +1) for e in es), f"r median {np.median([e['r'] for e in es]):+.2f}",
                      sum(e["r"] > 0 for e in es), bool(np.median([e["r"] for e in es]) >= SESOI["mode_r"])))
    for sc in ("Mission", "Control"):
        es = [M[m][f"h2|{sc}"] for m in maps]
        tests.append(("H2", f"{sc} goal switches, w_commit 0.45 < 0", max(one_sided(e["p_two"], e["r"], -1) for e in es),
                      f"r median {np.median([e['r'] for e in es]):+.2f}", sum(e["r"] < 0 for e in es),
                      bool(np.median([e["r"] for e in es]) <= SESOI["h2_r"])))
    # meta-analysed tests
    meta = {}
    for st in STYLES:
        es = [M[m][f"h3|{st}"] for m in maps]
        ma = reml_hk([e["r"] for e in es], [e["se"] ** 2 for e in es], -1)
        rel = float(np.mean([e["rel"] for e in es]))
        meta[f"h3|{st}"] = ma
        tests.append(("H3", f"Deathmatch {st} walked expected hits lower (lambda_E configured vs 0)", ma["p"],
                      f"pooled r {ma['mu']:+.2f} [{ma['ci'][0]:+.2f}, {ma['ci'][1]:+.2f}], PI [{ma['pi'][0]:+.2f}, {ma['pi'][1]:+.2f}]; "
                      f"mean change {100 * rel:+.0f}%", sum(e["r"] < 0 for e in es), bool(ma["mu"] <= SESOI["h3_r"])))
    shares = np.array([M[m]["h3_share"] for m in maps])
    tt = stats.ttest_1samp(shares, 0.5, alternative="greater") if shares.std() > 0 else None
    p_share = float(tt.pvalue) if tt is not None else (0.0 if shares.mean() > 0.5 else 1.0)
    tests.append(("H3", "Sign test: share of the 12 conditions with lower walked expected hits > 0.5", p_share,
                  f"mean share {shares.mean():.2f} (min {shares.min():.2f})", int(sum(shares > 0.5)),
                  bool(shares.mean() >= SESOI["sign_share"])))
    es = [M[m]["hits"] for m in maps]
    ma = reml_hk([e["r"] for e in es], [e["se"] ** 2 for e in es], -1)
    rel = float(np.mean([e["rel"] for e in es]))
    meta["hits"] = ma
    tests.append(("H3", "Hits taken, Deathmatch, four styles pooled (lambda_E configured vs 0)", ma["p"],
                  f"pooled r {ma['mu']:+.2f} [{ma['ci'][0]:+.2f}, {ma['ci'][1]:+.2f}]; mean change {100 * rel:+.0f}%",
                  sum(e["r"] < 0 for e in es), bool(ma["mu"] <= SESOI["hits_r"])))
    es = [M[m]["h3b"] for m in maps]
    ma = reml_hk([e["r"] for e in es], [e["se"] ** 2 for e in es], -1)
    diff = float(np.mean([e["diff"] for e in es]))
    meta["h3b"] = ma
    tests.append(("H3b", "Deathmatch Mission–Cooperation ally distance, lambda_T 10 < 0", ma["p"],
                  f"pooled r {ma['mu']:+.2f} [{ma['ci'][0]:+.2f}, {ma['ci'][1]:+.2f}]; mean difference {diff:+.2f} cells",
                  sum(e["r"] < 0 for e in es), bool(ma["mu"] <= SESOI["h3b_r"])))
    es = [M[m]["h4_eng"] for m in maps]
    ma = reml_hk([e["z"] for e in es], [e["se"] ** 2 for e in es], -1)
    meta["h4_eng"] = ma
    tests.append(("H4", "Deathmatch engagement redirection decreases along alpha (Aggressive -> Survival-Aware)", ma["p"],
                  f"pooled rho {np.tanh(ma['mu']):+.2f} [{np.tanh(ma['ci'][0]):+.2f}, {np.tanh(ma['ci'][1]):+.2f}]",
                  sum(e["rho"] < 0 for e in es), bool(np.tanh(ma["mu"]) <= SESOI["h4_eng_rho"])))
    es = [M[m]["h4_coh"] for m in maps]
    ma = reml_hk([e["z"] for e in es], [e["se"] ** 2 for e in es], +1)
    meta["h4_coh"] = ma
    change = float(np.mean([e["change_cells"] for e in es]))
    tests.append(("H4", "Mission ally distance increases along alpha (Mission–Cooperation -> Persistent Objective)", ma["p"],
                  f"pooled rho {np.tanh(ma['mu']):+.2f} [{np.tanh(ma['ci'][0]):+.2f}, {np.tanh(ma['ci'][1]):+.2f}]; "
                  f"mean change over alpha 0 -> 1 {change:+.2f} cells", sum(e["rho"] > 0 for e in es),
                  bool(np.tanh(ma["mu"]) >= SESOI["h4_coh_rho"])))
    # Holm across the Level-2 family and verdicts
    adj = holm([t[2] for t in tests])
    rows = []
    for (h, lab, pv, eff, n_dir, sesoi), pa in zip(tests, adj):
        if pa < 0.05 and n_dir >= min(8, k - 1) and sesoi:
            v = "confirmed"
        elif pa < 0.05:
            v = "partly confirmed"
        else:
            v = "not confirmed"
        rows.append({"hypothesis": h, "test": lab, "p_level2": pv, "p_holm": pa, "effect": eff,
                     "maps_in_direction": n_dir, "meets_sesoi": sesoi, "verdict": v})
    hyp = {}
    for h in ("H1", "H2", "H3", "H3b", "H4"):
        vs = [r["verdict"] for r in rows if r["hypothesis"] == h]
        ok = [v.startswith("confirmed") for v in vs]
        if all(ok):
            hyp[h] = "confirmed"
        elif h == "H3" and all(o or ("Survival-Aware" in r["test"]) for o, r in zip(ok, [r for r in rows if r["hypothesis"] == h])):
            hyp[h] = "partly confirmed (only Survival-Aware fails)"
        elif sum(ok) >= len(ok) / 2:
            hyp[h] = "partly confirmed"
        else:
            hyp[h] = "not confirmed"
    md = [f"# Cross-map confirmation (Level 2) over {k} maps: {', '.join(maps)}", "",
          "| Hyp. | Test | p (Level 2) | p_Holm | Effect across maps | maps in predicted direction | SESOI | Verdict |",
          "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['hypothesis']} | {r['test']} | {r['p_level2']:.2g} | {r['p_holm']:.2g} | {r['effect']} | "
                  f"{r['maps_in_direction']}/{k} | {'yes' if r['meets_sesoi'] else 'no'} | {r['verdict']} |")
    md += ["", "Per hypothesis: " + "; ".join(f"{h} {v}" for h, v in hyp.items()), "",
           "## Level 1 (per map, Holm within map; descriptive)", "",
           "| Test | " + " | ".join(maps) + " |", "|---|" + "---|" * k]
    labels = [lab for (h, lab) in M[maps[0]]["level1"]]
    for lab in labels:
        cells = []
        for m in maps:
            t = next(v for (hh, ll), v in M[m]["level1"].items() if ll == lab)
            cells.append(f"{t['effect']}; {t['p_holm']:.2g}")
        md.append(f"| {lab} | " + " | ".join(cells) + " |")
    tag = f"_{a.tag}" if a.tag else ""
    (root / f"confirmation_summary{tag}.md").write_text("\n".join(md) + "\n")
    (root / f"confirmation_summary{tag}.json").write_text(json.dumps(
        {"maps": maps, "tests": rows, "hypotheses": hyp, "meta": meta,
         "per_map": {m: {k_: v for k_, v in M[m].items() if k_ != "level1"} for m in maps}}, indent=1, default=float))
    print("\n".join(md[:len(rows) + 5]))


if __name__ == "__main__":
    main()
