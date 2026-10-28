"""Earlier testbed vs testbed with the movement and perception fixes (2026-09-25).

The same main model and seeds are run on the testbed of the paper's final run (--a) and on the testbed with the
optional rules of 2026-09-25 switched on (--b: teammate swap, local avoidance, forgetting a reached enemy memory,
symmetric line of sight; see testbed_flags.txt in each directory). Writes testbed_comparison.md/.json into --out:

  1. primary hypothesis tests (H1-H4) row by row: effect and Holm-adjusted p on both testbeds
  2. main-experiment metrics per scenario and style (episodes paired by seed; paired Wilcoxon b vs a, Holm within
     each condition) and Control wins
  3. the H3 outcomes of the cost-term ablation (configured lambda_E vs 0; walked expected hits and hits taken per
     alive step; Deathmatch per style, Holm over the four styles; sign test over the 12 conditions)
  4. movement stalls (share of episodes in which an agent of either team stands >= 50 steps although its goal is
     elsewhere; analyze_stalls.py), when the stall files are given

Usage:
  python experiments/compare_testbeds.py --a ../repro_outputs/v3 --a-results ../repro_outputs/v3_hits \
      --b ../repro_outputs/v3_fixed --stalls-a stalls_{map}.csv --stalls-b stalls_{map}_allfixes.csv \
      --stalls-dir ../repro_outputs/v3/analysis --out ../repro_outputs/v3_fixed
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_stats import METRICS, SCENARIOS, STYLES, control_outcomes, fmt, fmt_p, holm, load, mean_ci, wilcoxon_paired  # noqa: E402

KEY = {"Mission": ["objective_commitment_ratio", "avg_ally_proximity", "engagement_redirection_rate_per_100", "kills", "deaths"],
       "Deathmatch": ["engagement_redirection_rate_per_100", "resource_seeking_rate_per_100", "avg_ally_proximity",
                      "kills", "deaths"],
       "Control": ["control_score", "objective_commitment_ratio", "avg_ally_proximity", "kills", "deaths"]}
EXTRA = {"walked_hits_per_step": "WalkedHits", "hits_taken_per_step": "HitsTaken", "goal_switch_rate_per_100": "Switches"}


def label(c: str) -> str:
    return METRICS.get(c, EXTRA.get(c, c))


def flags(d: Path) -> str:
    f = d / "testbed_flags.txt"
    return f.read_text().strip() if f.exists() else "(no testbed_flags.txt: the final run, all rules off)"


def h3_outcomes(ct: pd.DataFrame, col: str) -> dict:
    out, dm_p, lower = {}, [], 0
    for sc in SCENARIOS:
        for st in STYLES:
            f = ct[(ct.scenario == sc) & (ct["style"] == st) & (ct.variant == "full")].sort_values("episode")
            z = ct[(ct.scenario == sc) & (ct["style"] == st) & (ct.variant == "no_exposure")].sort_values("episode")
            t = wilcoxon_paired(f[col].values, z[col].values)
            mf, mz = float(f[col].mean()), float(z[col].mean())
            lower += int(mf < mz)
            out[f"{sc}|{st}"] = {"full": mf, "no_exposure": mz, "change": (mf - mz) / mz if mz else float("nan"),
                                 "r": t["r"], "p": t["p"]}
            if sc == "Deathmatch":
                dm_p.append((st, t["p"]))
    for (st, _), ph in zip(dm_p, holm([p for _, p in dm_p])):
        out[f"Deathmatch|{st}"]["p_holm"] = ph
    out["sign"] = {"lower": lower, "p": float(stats.binomtest(lower, 12, 0.5, alternative="greater").pvalue)}
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--a", required=True, help="earlier-testbed output directory (random map; urban in <a>/urban)")
    p.add_argument("--a-results", default=None,
                   help="directory with results.csv / cost_term_ablation.csv of the earlier testbed incl. hits taken "
                        "(e.g. the hits-taken rerun; default --a)")
    p.add_argument("--b", required=True, help="fixed-testbed output directory")
    p.add_argument("--stalls-dir", default=None)
    p.add_argument("--stalls-a", default="stalls_{map}.csv")
    p.add_argument("--stalls-b", default="stalls_{map}_allfixes.csv")
    p.add_argument("--out", default=None)
    a = p.parse_args()
    S: dict = {"testbed_a": flags(Path(a.a)), "testbed_b": flags(Path(a.b))}
    md = ["# Earlier testbed vs testbed with the movement and perception fixes (same model, same seeds)", "",
          f"- a (earlier): `{a.a}` — rules: {S['testbed_a']}", f"- b (fixed): `{a.b}` — rules: {S['testbed_b']}", ""]
    for m, sub in (("random", ""), ("urban", "urban")):
        da, db = Path(a.a) / sub, Path(a.b) / sub
        dra = Path(a.a_results or a.a) / sub
        S[m] = {}
        # 1) primary tests, row by row
        ha = json.loads((da / "hypotheses_summary.json").read_text(encoding="utf-8"))["primary"]
        hb = json.loads((db / "hypotheses_summary.json").read_text(encoding="utf-8"))["primary"]
        hbk = {(t["hypothesis"], t["test"]): t for t in hb}
        md += [f"## {m} map", "", "### Primary tests (Holm across each testbed's primary tests)", "",
               "| Hyp. | Test | a: statistic; effect | a: p_Holm | b: statistic; effect | b: p_Holm | at 0.05 |", "|---|---|---|---|---|---|---|"]
        rows = []
        for t in ha:
            u = hbk.get((t["hypothesis"], t["test"]))
            if u is None:
                continue
            sa, sb = t["p_holm"] < 0.05, u["p_holm"] < 0.05
            change = "same" if sa == sb else ("lost" if sa else "gained")
            rows.append({"hypothesis": t["hypothesis"], "test": t["test"], "a": t, "b": u, "change": change})
            md.append(f"| {t['hypothesis']} | {t['test']} | {t['statistic']}; {t['effect']} | {fmt_p(t['p_holm'])} | "
                      f"{u['statistic']}; {u['effect']} | {fmt_p(u['p_holm'])} | {change} |")
        S[m]["primary"] = rows
        # 2) main experiment
        ra, rb = load(dra / "results.csv"), load(db / "results.csv")
        md += ["", "### Main experiment (means; paired Wilcoxon b vs a by episode seed, Holm within condition)", "",
               "| Scenario | Style | Metric | a | b | r | p_Holm |", "|---|---|---|---|---|---|---|"]
        S[m]["main"] = {}
        for sc in SCENARIOS:
            for st in STYLES:
                x = ra[(ra["scenario"] == sc) & (ra["style"] == st)].sort_values("episode")
                y = rb[(rb["scenario"] == sc) & (rb["style"] == st)].sort_values("episode")
                common = sorted(set(x["episode"]) & set(y["episode"]))
                x, y = x[x["episode"].isin(common)], y[y["episode"].isin(common)]
                cols = KEY[sc] + [c for c in ("walked_hits_per_step", "hits_taken_per_step") if c in x and c in y]
                tests = [wilcoxon_paired(y[c].values, x[c].values) for c in cols]
                for c, t, ph in zip(cols, tests, holm([t["p"] for t in tests])):
                    t.update({"p_holm": ph, "a": mean_ci(x[c]), "b": mean_ci(y[c])})
                    S[m]["main"][f"{sc}|{st}|{label(c)}"] = t
                    md.append(f"| {sc} | {st} | {label(c)} | {fmt(t['a'])} | {fmt(t['b'])} | {t['r']:+.2f} | {fmt_p(ph)} |")
                if sc == "Control":
                    S[m]["main"][f"Control|{st}|wins"] = {"a": control_outcomes(x)["wins"], "b": control_outcomes(y)["wins"]}
        md.append("")
        md.append("Control wins (a -> b): " + "; ".join(
            f"{st}: {S[m]['main'][f'Control|{st}|wins']['a']} -> {S[m]['main'][f'Control|{st}|wins']['b']}" for st in STYLES))
        # 3) H3 outcomes of the cost-term ablation
        cta, ctb = load(dra / "cost_term_ablation.csv"), load(db / "cost_term_ablation.csv")
        S[m]["h3"] = {}
        for col in ("walked_hits_per_step", "hits_taken_per_step"):
            if col not in cta or col not in ctb:
                continue
            oa, ob = h3_outcomes(cta, col), h3_outcomes(ctb, col)
            S[m]["h3"][col] = {"a": oa, "b": ob}
            md += ["", f"### H3, {label(col)} per alive step: configured lambda_E vs 0 (change; Deathmatch p_Holm over 4 styles)", "",
                   "| Scenario | Style | a: change | a: p | b: change | b: p |", "|---|---|---|---|---|---|"]
            for sc in SCENARIOS:
                for st in STYLES:
                    u, v = oa[f"{sc}|{st}"], ob[f"{sc}|{st}"]
                    pa_, pb_ = (u.get("p_holm", u["p"]), v.get("p_holm", v["p"]))
                    md.append(f"| {sc} | {st} | {100 * u['change']:+.0f}% | {fmt_p(pa_)} | {100 * v['change']:+.0f}% | {fmt_p(pb_)} |")
            md.append(f"\nSign test (lower with the exposure term): a {oa['sign']['lower']}/12 (p {fmt_p(oa['sign']['p'])}), "
                      f"b {ob['sign']['lower']}/12 (p {fmt_p(ob['sign']['p'])})")
        # 4) stalls
        if a.stalls_dir:
            fa = Path(a.stalls_dir) / a.stalls_a.format(map=m)
            fb = Path(a.stalls_dir) / a.stalls_b.format(map=m)
            if fa.exists() and fb.exists():
                sa_, sb_ = pd.read_csv(fa).fillna(""), pd.read_csv(fb).fillna("")
                md += ["", "### Movement stalls >= 50 steps (share of episodes, either team)", "",
                       "| Scenario | Style | a | b |", "|---|---|---|---|"]
                S[m]["stalls"] = {}
                for sc in SCENARIOS:
                    for st in STYLES:
                        def share(d):
                            d = d[(d.scenario == sc) & (d["style"] == st)]
                            return float(((d.team0_stall_kind != "") | (d.team1_stall_kind != "")).mean())
                        S[m]["stalls"][f"{sc}|{st}"] = {"a": share(sa_), "b": share(sb_)}
                        md.append(f"| {sc} | {st} | {100 * share(sa_):.0f}% | {100 * share(sb_):.0f}% |")
                tot = lambda d: float(((d.team0_stall_kind != "") | (d.team1_stall_kind != "")).mean())
                md.append(f"\nAll conditions: a {100 * tot(sa_):.1f}%, b {100 * tot(sb_):.1f}%")
        md.append("")
    out = Path(a.out or a.b)
    (out / "testbed_comparison.json").write_text(json.dumps(S, indent=2, ensure_ascii=False, default=float), encoding="utf-8")
    (out / "testbed_comparison.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Saved: {(out / 'testbed_comparison.md').resolve()}")


if __name__ == "__main__":
    main()
