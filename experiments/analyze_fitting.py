"""Analysis of the fitting experiment (2026-09-25; protocol: CONFIRMATION_PLAN, part B).

Reads the test stage of run_fitting.py (test_rows.csv; seed base TEST, 50 episodes per agent x map x scenario) and
stage0.json, and reports per behaviour tree:

  (a) nearest tree: standardised distances of the fitted policy to the four trees (4 x 4 table), with the share of
      bootstrap resamples in which its own tree is the nearest (resampling episode indices, which keeps the common
      random numbers of the agents paired); "correct" if its own tree is nearest in >= 95% of the resamples
  (b) gap closure G = sqrt(D2(fit, tree) / min over hand styles D2(style, tree)), the hand styles including their
      route-off versions; D2 is the bias-corrected squared standardised distance (below); bootstrap 95% CI
  (c) noise floor: D(fit[S1], tree[S2]) against D(tree[S1], tree[S2]) over 1000 random splits S1/S2 of the
      episode indices; "within the noise floor" if the mean of the former is at most the 95th percentile of the latter
  (d) classifier two-sample test: logistic regression (5-fold cross-validation, out-of-fold AUC with a bootstrap CI,
      permutation p with 2000 label permutations) on the fingerprint metrics, and separately on label-free metrics
      (ally distance, share of steps in enemy line of sight, walked expected hits, hits taken per step)
  (e) untargeted outcomes (kills, deaths, Control wins, hits taken per step): Cohen's d of fit vs tree

Distances. For a map set M, the dimensions are scenario x metric on each map of M (objective commitment,
engagement redirection, resource seeking, ally distance; Deathmatch objective commitment and dimensions on which
the eight reference agents do not vary are left out). Scale s_d: stage-0 scale on the game maps; on a held-out
map, the pooled within-condition SD of the eight reference agents on that map (test seeds), floored at 5% of the
range of their means.
  D2(A, B) = mean_d [(xbar_A - xbar_B)^2 - v_A / n_A - v_B / n_B] / s_d^2   (unbiased for the squared distance)
  D(A, B)  = sqrt(mean_d (xbar_A - xbar_B)^2 / s_d^2)                      (plain, for the noise-floor comparison)

Verdict per tree (pre-registered):
  success       (a) correct on the game maps, upper CI of G < 0.5, and on >= 4 of the 5 held-out maps the own
                tree is nearest with G < 0.5
  equivalence   success and within the noise floor, AUC upper CI <= 0.65 and all |d| < 0.2 on the game maps
  partial       upper CI of G < 1 on the game maps (closer than every hand style)
  failure       otherwise
The headline claim ("the unified policy reproduces the game logics") needs success on at least 3 of the 4 trees.

Usage: python experiments/analyze_fitting.py --dir ../repro_outputs/v4_fit [--boot 1000 --perm 2000]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_fitting import FP, GAMES, HAND, HELDOUT_MAPS, SCENARIOS, TRAIN_MAPS  # noqa: E402

LABEL_FREE = ["avg_ally_proximity", "los_frac", "walked_hits_per_step", "hits_taken_per_step"]
UNTARGETED = ["kills", "deaths", "win", "hits_taken_per_step"]
TREES = list(GAMES)
REFERENCE = TREES + list(HAND.values())


def dims_for(maps) -> list[tuple]:
    return [(m, sc, f) for m in maps for sc in SCENARIOS for f in FP
            if not (sc == "Deathmatch" and f == "objective_commitment_ratio")]


def scales_for(df: pd.DataFrame, stage0: dict, maps) -> dict:
    s = {}
    for d in dims_for(maps):
        key = "|".join(d)
        if d[0] in TRAIN_MAPS:
            if key in stage0["scales"]:
                s[d] = stage0["scales"][key]
            continue
        g = df[(df["map"] == d[0]) & (df.scenario == d[1]) & (df.agent.isin(REFERENCE))]
        by = g.groupby("agent")[d[2]]
        means, var = by.mean(), by.var(ddof=1)
        sd = float(np.sqrt(var.mean())) if len(var) else 0.0
        val = max(sd, 0.05 * float(means.max() - means.min())) if len(means) else 0.0
        if val > 0:
            s[d] = val
    return s


class Cells:
    """Episode values per (agent, map, scenario, metric) as arrays indexed by episode."""

    def __init__(self, df: pd.DataFrame, cols):
        self.v = {}
        for (a, m, sc), g in df.groupby(["agent", "map", "scenario"]):
            g = g.sort_values("episode")
            for c in cols:
                self.v[(a, m, sc, c)] = g[c].to_numpy(dtype=float)
        self.n_ep = max(len(x) for x in self.v.values())

    def stats(self, a, d, idx=None):
        x = self.v[(a, d[0], d[1], d[2])]
        if idx is not None:
            x = x[idx]
        x = x[~np.isnan(x)]
        return (x.mean(), x.var(ddof=1) if len(x) > 1 else 0.0, len(x)) if len(x) else (np.nan, np.nan, 0)


def d2(cells: Cells, a, b, scales, idx=None) -> float:
    t = []
    for d, s in scales.items():
        ma, va, na = cells.stats(a, d, idx)
        mb, vb, nb = cells.stats(b, d, idx)
        if na and nb:
            t.append(((ma - mb) ** 2 - va / na - vb / nb) / s ** 2)
    return float(np.mean(t))


def dplain(cells: Cells, a, b, scales, ia=None, ib=None) -> float:
    t = []
    for d, s in scales.items():
        ma = cells.stats(a, d, ia)[0]
        mb = cells.stats(b, d, ib)[0]
        if not (np.isnan(ma) or np.isnan(mb)):
            t.append((ma - mb) ** 2 / s ** 2)
    return float(np.sqrt(np.mean(t)))


def gap(cells, fit, tree, styles, scales, idx=None):
    num = max(d2(cells, fit, tree, scales, idx), 0.0)
    den = min(max(d2(cells, s, tree, scales, idx), 1e-12) for s in styles)
    return float(np.sqrt(num / den))


def classifier(df: pd.DataFrame, fit: str, tree: str, maps, cols, rng, perm: int, boot: int) -> dict:
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import StratifiedKFold
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    g = df[df["map"].isin(maps) & df.agent.isin([fit, tree])].copy()
    X = pd.get_dummies(g[cols + ["scenario", "map"]], columns=["scenario", "map"], dtype=float).fillna(0.0).to_numpy()
    y = (g.agent == fit).to_numpy(dtype=int)

    def oof(labels):
        p = np.zeros(len(labels))
        for tr, te in StratifiedKFold(5, shuffle=True, random_state=0).split(X, labels):
            m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)).fit(X[tr], labels[tr])
            p[te] = m.predict_proba(X[te])[:, 1]
        return p
    p = oof(y)
    auc = roc_auc_score(y, p)
    bs = []
    for _ in range(boot):
        i = rng.integers(0, len(y), len(y))
        if len(set(y[i])) == 2:
            bs.append(roc_auc_score(y[i], p[i]))
    null = [roc_auc_score(yp, oof(yp)) for yp in (rng.permutation(y) for _ in range(perm))]
    return {"auc": float(auc), "ci": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
            "p_perm": float((1 + sum(a >= auc for a in null)) / (1 + len(null)))}


def cohens_d(a, b) -> float:
    a, b = np.asarray(a, float), np.asarray(b, float)
    a, b = a[~np.isnan(a)], b[~np.isnan(b)]
    s = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    return float((a.mean() - b.mean()) / s) if s > 0 else 0.0


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dir", default="../repro_outputs/v4_fit")
    p.add_argument("--boot", type=int, default=1000)
    p.add_argument("--perm", type=int, default=2000)
    p.add_argument("--splits", type=int, default=1000)
    a = p.parse_args()
    d = Path(a.dir)
    df = pd.read_csv(d / "test_rows.csv")
    df["win"] = ((df.scenario == "Control") & (pd.to_numeric(df.control_score, errors="coerce") >= 120)).astype(float)
    df.loc[df.scenario != "Control", "win"] = np.nan
    stage0 = json.loads((d / "stage0.json").read_text())
    fitted = json.loads((d / "fitted.json").read_text())
    rng = np.random.default_rng(2030)
    cells = Cells(df, FP + LABEL_FREE + UNTARGETED)
    heldout = [m for m in HELDOUT_MAPS if m in set(df["map"])]
    out, md = {"verdicts": {}}, ["# Fitting: test stage (seed base TEST, 50 episodes per agent x map x scenario)", ""]
    sc_game = scales_for(df, stage0, TRAIN_MAPS)
    for game in TREES:
        fit = f"fit[{game}]"
        if fit not in set(df.agent):
            continue
        styles = [s for s in df.agent.unique() if s in HAND.values() or s.endswith("[route off]")]
        res = {"weights": fitted[game]["weights"], "mode": fitted[game]["combat_mode"]}
        # (a) + (b) on the game maps
        dist = {t: d2(cells, fit, t, sc_game) for t in TREES}
        own_nearest, gs = 0, []
        for _ in range(a.boot):
            idx = rng.integers(0, cells.n_ep, cells.n_ep)
            dd = {t: d2(cells, fit, t, sc_game, idx) for t in TREES}
            own_nearest += min(dd, key=dd.get) == game
            gs.append(gap(cells, fit, game, styles, sc_game, idx))
        G = gap(cells, fit, game, styles, sc_game)
        res["game_maps"] = {"D2": dist, "own_nearest_share": own_nearest / a.boot,
                            "correct": own_nearest / a.boot >= 0.95, "G": G,
                            "G_ci": [float(np.percentile(gs, 2.5)), float(np.percentile(gs, 97.5))],
                            "best_style": min(styles, key=lambda s: d2(cells, s, game, sc_game))}
        # (c) noise floor on the game maps
        fl, fs = [], []
        for _ in range(a.splits):
            perm = rng.permutation(cells.n_ep)
            s1, s2 = perm[: cells.n_ep // 2], perm[cells.n_ep // 2:]
            fl.append(dplain(cells, game, game, sc_game, s1, s2))
            fs.append(dplain(cells, fit, game, sc_game, s1, s2))
        res["noise_floor"] = {"fit_mean": float(np.mean(fs)), "tree_p95": float(np.percentile(fl, 95)),
                              "within": float(np.mean(fs)) <= float(np.percentile(fl, 95))}
        # (d) classifier two-sample tests on the game maps
        res["classifier"] = {"fingerprint": classifier(df, fit, game, TRAIN_MAPS, FP, rng, a.perm, a.boot),
                             "label_free": classifier(df, fit, game, TRAIN_MAPS, LABEL_FREE, rng, a.perm, a.boot)}
        # (e) untargeted outcomes (game maps, per scenario)
        eff = {}
        for sc in SCENARIOS:
            for c in UNTARGETED:
                if c == "win" and sc != "Control":
                    continue
                x = df[(df.agent == fit) & (df.scenario == sc) & df["map"].isin(TRAIN_MAPS)][c]
                y = df[(df.agent == game) & (df.scenario == sc) & df["map"].isin(TRAIN_MAPS)][c]
                eff[f"{sc}|{c}"] = cohens_d(x, y)
        res["untargeted_d"] = eff
        # held-out maps
        ho = {}
        for m in heldout:
            sc_m = scales_for(df, stage0, [m])
            dm = {t: d2(cells, fit, t, sc_m) for t in TREES}
            ho[m] = {"nearest": min(dm, key=dm.get), "G": gap(cells, fit, game, styles, sc_m), "D2": dm}
        res["heldout"] = ho
        n_ok = sum(1 for m in ho.values() if m["nearest"] == game and m["G"] < 0.5)
        success = res["game_maps"]["correct"] and res["game_maps"]["G_ci"][1] < 0.5 and n_ok >= 4
        equivalent = (success and res["noise_floor"]["within"]
                      and res["classifier"]["fingerprint"]["ci"][1] <= 0.65
                      and all(abs(v) < 0.2 for v in eff.values()))
        verdict = ("equivalence" if equivalent else "success" if success
                   else "partial" if res["game_maps"]["G_ci"][1] < 1 else "failure")
        res["verdict"] = verdict
        out[game] = res
        out["verdicts"][game] = verdict
        gm = res["game_maps"]
        md += [f"## {game} (mode {res['mode']}; weights " + ", ".join(f"{k} {v:.2f}" for k, v in res["weights"].items()) + ")", "",
               "- (a) D2 to the trees (game maps): " + ", ".join(f"{t} {v:.3f}" for t, v in dist.items())
               + f"; own tree nearest in {100 * gm['own_nearest_share']:.0f}% of resamples",
               f"- (b) G = {gm['G']:.2f} (95% CI {gm['G_ci'][0]:.2f}-{gm['G_ci'][1]:.2f}); closest hand style {gm['best_style']}",
               f"- (c) noise floor: fit {res['noise_floor']['fit_mean']:.3f} vs tree 95th percentile {res['noise_floor']['tree_p95']:.3f}",
               f"- (d) AUC fingerprint {res['classifier']['fingerprint']['auc']:.2f} (CI {res['classifier']['fingerprint']['ci'][0]:.2f}-"
               f"{res['classifier']['fingerprint']['ci'][1]:.2f}, p {res['classifier']['fingerprint']['p_perm']:.4f}); label-free "
               f"{res['classifier']['label_free']['auc']:.2f} (p {res['classifier']['label_free']['p_perm']:.4f})",
               "- (e) Cohen's d (fit - tree): " + ", ".join(f"{k} {v:+.2f}" for k, v in eff.items()),
               "- held-out maps: " + "; ".join(f"{m}: nearest {v['nearest']}, G {v['G']:.2f}" for m, v in ho.items()),
               f"- **verdict: {verdict}**", ""]
    n_success = sum(v in ("success", "equivalence") for v in out["verdicts"].values())
    md.append(f"Headline criterion (success on >= 3 of 4 trees): {n_success}/4 -> {'met' if n_success >= 3 else 'not met'}")
    (d / "fitting_summary.json").write_text(json.dumps(out, indent=1, default=float))
    (d / "fitting_summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
