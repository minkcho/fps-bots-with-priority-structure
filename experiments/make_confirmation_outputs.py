"""Paper tables and figure of the pre-registered confirmation across maps (2026-09-25; presentation only).

Reads the outputs of analyze_map_confirmation.py (not part of the frozen analysis; it only formats them):
  <root>/confirmation_summary.json                 nine confirmatory maps (Level 2, verdicts, per-map effects)
  <root>/confirmation_summary_11maps.json          sensitivity analysis with the development maps (optional)
  <root>/confirmation_summary_development_maps.json the development maps with the new seeds (optional)
  <root>/<map>/hypotheses_summary.json             Level 1 (the 20 primary tests per map, Holm within the map)
Writes to --tables / --figures:
  confirmation_level2.tex   one row per Level-2 test: effect across the nine maps, p_Holm, maps in the predicted
                            direction, SESOI met, verdict (and the verdict of the 11-map analysis)
  confirmation_level1.tex   tests x maps: per-map effect, marked with a dagger where p_Holm >= 0.05 within the map
  fig_confirmation_forest.pdf  per-map effects (95% CI from the bootstrap SE) of the meta-analysed tests, the pooled
                            estimate with its CI and prediction interval, and the smallest effect of interest
  confirmation_moderators.md   (with --descriptors; exploratory) Spearman rho over the maps between the per-map
                            route-channel effects (H3 per style, hits taken, H3b) and each map descriptor
Usage: python experiments/make_confirmation_outputs.py --root ../repro_outputs/v4_maps \
           --tables ../repro_outputs/v4_maps/paper --figures ../repro_outputs/v4_maps/paper
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np

STYLE_SHORT = {"Mission–Cooperation": "MC", "Persistent Objective": "PO", "Aggressive": "Agg", "Survival-Aware": "SA"}
MAP_TEX = {"random": "random", "urban": "urban", "random_s101": "random 101", "random_s102": "random 102",
           "random_s103": "random 103", "urban_s101": "urban 101", "urban_s102": "urban 102", "urban_s103": "urban 103",
           "blocks": "blocks", "walls": "walls", "mixed": "mixed"}
SESOI = {"h3": -0.20, "hits": -0.20, "h3b": -0.20, "h4_eng": -0.30, "h4_coh": 0.10}


def short_style(s: str) -> str:
    for a, b in STYLE_SHORT.items():
        s = s.replace(a, b)
    return s


def test_label(lab: str) -> str:
    """LaTeX label of a Level-2 test."""
    rules = [
        (r"^Kruskal-Wallis, (\w+) ObjCommit$", r"Kruskal--Wallis, \1 objective commitment"),
        (r"^Kruskal-Wallis, (\w+) AllyDist$", r"Kruskal--Wallis, \1 ally distance"),
        (r"^Kruskal-Wallis, (\w+) EngRedirect$", r"Kruskal--Wallis, \1 engagement redirection"),
        (r"^Kruskal-Wallis, (\w+) ResSeek$", r"Kruskal--Wallis, \1 resource seeking"),
        (r"^Kruskal-Wallis, (\w+) CtrlScore$", r"Kruskal--Wallis, \1 score"),
        (r"^Style classification, (\w+)$", r"Style classification, \1"),
        (r"^Mode ablation, Deathmatch (.+) \(full > weights-only\)$", r"Mode ablation, Deathmatch \1"),
        (r"^(\w+) goal switches, w_commit 0\.45 < 0$", r"\1 goal switches, $w_{\\mathrm{commit}}$ 0.45 vs.\\ 0"),
        (r"^Deathmatch (.+) walked expected hits lower \(lambda_E configured vs 0\)$", r"Deathmatch \1 walked exposure"),
        (r"^Sign test: .*$", r"Sign test, share of the 12 conditions"),
        (r"^Hits taken, Deathmatch, four styles pooled .*$", r"Hits taken, Deathmatch, four styles"),
        (r"^Deathmatch (.+) ally distance, lambda_T 10 < 0$", r"Deathmatch \1 ally distance, $\\lambda_T$ 10 vs.\\ 0"),
        (r"^Deathmatch engagement redirection decreases along alpha .*$", r"Deathmatch engagement along $\\alpha$ (Agg $\\to$ SA)"),
        (r"^Mission ally distance increases along alpha .*$", r"Mission ally distance along $\\alpha$ (MC $\\to$ PO)"),
    ]
    lab = short_style(lab)
    for pat, rep in rules:
        if re.match(pat, lab):
            return re.sub(pat, rep, lab)
    return lab


def tex_effect(s: str) -> str:
    """Effect string of analyze_map_confirmation.py in LaTeX (signed numbers in math mode)."""
    s = s.replace("%", "\\%").replace("eps2", "$\\varepsilon^2$").replace("rho", "$\\rho$")
    s = re.sub(r"\br\b", "$r$", s)
    s = re.sub(r"(?<![\w.$])([+-]\d+(?:\.\d+)?)", r"$\1$", s)
    s = s.replace("alpha 0 -> 1", "$\\alpha$ 0 to 1").replace("->", "$\\to$")
    return s


def fmt_p(p: float) -> str:
    return "$<0.001$" if p < 0.001 else f"{p:.3f}"


def level2_table(summary: dict, summary11: dict | None) -> str:
    k = len(summary["maps"])
    v11 = {r["test"]: r["verdict"] for r in summary11["tests"]} if summary11 else {}
    cols = "llp{0.34\\textwidth}cccl" + ("l" if summary11 else "")
    head = ["Hyp.", "Test", f"Effect across the {k} maps", "$p_{\\mathrm{Holm}}$", "Direction", "SESOI", "Verdict"]
    if summary11:
        head.append(f"{len(summary11['maps'])} maps")
    lines = [f"\\begin{{tabular}}{{{cols}}}", "\\toprule", " & ".join(head) + " \\\\", "\\midrule"]
    prev = None
    for r in summary["tests"]:
        if prev is not None and r["hypothesis"] != prev:
            lines.append("\\midrule")
        prev = r["hypothesis"]
        cells = [r["hypothesis"], test_label(r["test"]), tex_effect(r["effect"]), fmt_p(r["p_holm"]),
                 f"{r['maps_in_direction']}/{k}", "yes" if r["meets_sesoi"] else "no", r["verdict"]]
        if summary11:
            cells.append(v11.get(r["test"], "--"))
        lines.append(" & ".join(cells) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


def level1_effect(t: dict) -> str:
    stat, eff = t.get("statistic", ""), t.get("effect", "")
    if eff.startswith("eps2"):
        v = eff.split("=")[1].strip()
    elif stat.startswith("accuracy"):
        v = stat.split("=")[1].split("(")[0].strip()
    elif stat.startswith("median diff"):
        v = re.search(r"r = ([+-]?[\d.]+)", eff).group(1)
    elif stat.startswith("rho"):
        v = stat.split("=")[1].split(";")[0].strip()
    elif "conditions lower" in stat:
        v = stat.split(" conditions")[0]
    else:
        v = stat
    v = f"${v}$" if re.match(r"^[+-]?\d", v) and "/" not in v else v
    return v if t["p_holm"] < 0.05 else v + "$^{\\dagger}$"


def level1_table(root: Path, maps: list[str]) -> str:
    per = {m: json.loads((root / m / "hypotheses_summary.json").read_text())["primary"] for m in maps}
    lines = ["\\begin{tabular}{ll" + "c" * len(maps) + "}", "\\toprule",
             "Hyp. & Test & " + " & ".join(MAP_TEX.get(m, m) for m in maps) + " \\\\", "\\midrule"]
    first = per[maps[0]]
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from make_paper_tables import pretty   # the labels of the paper's hypothesis tables
    for i, t in enumerate(first):
        lab = pretty(t["test"]).replace("Sign test, WalkedHits lower with the exposure term (all scenarios x styles)",
                                        "Sign test, walked exposure lower with the term (12 conditions)")
        cells = [level1_effect(per[m][i]) for m in maps]
        lines.append(f"{t['hypothesis']} & {lab} & " + " & ".join(cells) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    return "\n".join(lines)


def forest(summary: dict, summary11: dict | None, out: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    maps9 = summary["maps"]
    per = dict(summary["per_map"])
    dev = []
    if summary11:
        for m, v in summary11["per_map"].items():
            if m not in per:
                per[m] = v
                dev.append(m)
    panels = [(f"h3|{s}", f"H3 walked exposure, {STYLE_SHORT[s]}", "r", SESOI["h3"]) for s in STYLE_SHORT] + [
        ("hits", "Hits taken (four styles)", "r", SESOI["hits"]), ("h3b", "H3b ally distance", "r", SESOI["h3b"]),
        ("h4_eng", "H4 engagement along $\\alpha$", "rho", SESOI["h4_eng"]),
        ("h4_coh", "H4 ally distance along $\\alpha$", "rho", SESOI["h4_coh"])]
    rows = maps9 + dev
    fig, axes = plt.subplots(2, 4, figsize=(13, 6.4), sharey=True)
    for ax, (key, title, kind, sesoi) in zip(axes.ravel(), panels):
        for j, m in enumerate(rows):
            e = per[m][key]
            if kind == "r":
                est, lo, hi = e["r"], e["r"] - 1.96 * e["se"], e["r"] + 1.96 * e["se"]
            else:
                est, lo, hi = e["rho"], np.tanh(e["z"] - 1.96 * e["se"]), np.tanh(e["z"] + 1.96 * e["se"])
            y = len(rows) - j + (0 if m in maps9 else -0.5)
            ax.plot([lo, hi], [y, y], color="0.3", lw=1)
            ax.plot(est, y, "o", ms=4, color="k" if m in maps9 else "white", mec="k")
        ma = summary["meta"][key]
        f = (lambda x: x) if kind == "r" else np.tanh
        mu, (c0, c1), (p0, p1) = f(ma["mu"]), [f(c) for c in ma["ci"]], [f(p) for p in ma["pi"]]
        yp = -1.0
        ax.plot([p0, p1], [yp, yp], color="tab:blue", lw=1, alpha=0.6)
        ax.fill([c0, mu, c1, mu], [yp, yp + 0.4, yp, yp - 0.4], color="tab:blue")
        ax.axvline(0, color="0.6", lw=0.8)
        ax.axvline(sesoi, color="tab:red", lw=0.8, ls="--")
        ax.set_title(title, fontsize=9)
        ax.set_xlabel("$r$" if kind == "r" else "$\\rho$", fontsize=8)
        ax.tick_params(labelsize=7)
    ticks = [len(rows) - j + (0 if m in maps9 else -0.5) for j, m in enumerate(rows)] + [-1.0]
    labels = [MAP_TEX.get(m, m) + ("" if m in maps9 else " (dev.)") for m in rows] + ["pooled (9 maps)"]
    for ax in axes[:, 0]:
        ax.set_yticks(ticks)
        ax.set_yticklabels(labels, fontsize=7)
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    fig.savefig(out.with_suffix(".png"), dpi=150)


def moderators(summary: dict, summary11: dict | None, descriptors: Path) -> str:
    """Exploratory: Spearman rho over the maps between per-map route-channel effects and the map descriptors."""
    import csv
    from scipy import stats
    per = dict(summary11["per_map"]) if summary11 else dict(summary["per_map"])
    desc = {r["map"]: r for r in csv.DictReader(descriptors.open())}
    names = ["density", "area", "visibility", "cover", "diversity", "cut", "headroom"]
    keys = [(f"h3|{s}", f"H3 {STYLE_SHORT[s]}") for s in STYLE_SHORT] + [("hits", "hits taken"), ("h3b", "H3b")]
    maps = [m for m in per if m in desc]
    out = [f"# Exploratory: per-map effects vs map descriptors (Spearman rho over {len(maps)} maps: {', '.join(maps)})", "",
           "| effect | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
    for key, lab in keys:
        eff = [per[m][key]["r"] for m in maps]
        cells = []
        for n in names:
            x = [float(desc[m][n]) for m in maps]
            r = stats.spearmanr(x, eff)
            cells.append(f"{r.statistic:+.2f} (p {r.pvalue:.2f})")
        out.append(f"| {lab} | " + " | ".join(cells) + " |")
    out += ["", "Per-map effects (matched-pairs r):", "",
            "| map | " + " | ".join(lab for _, lab in keys) + " | headroom |", "|---|" + "---|" * (len(keys) + 1)]
    for m in maps:
        out.append(f"| {m} | " + " | ".join(f"{per[m][k]['r']:+.2f}" for k, _ in keys) + f" | {float(desc[m]['headroom']):.3f} |")
    return "\n".join(out) + "\n"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="../repro_outputs/v4_maps")
    p.add_argument("--tables", required=True)
    p.add_argument("--figures", required=True)
    p.add_argument("--descriptors", default="", help="descriptors.csv of analyze_map_descriptors.py (moderators)")
    a = p.parse_args()
    root = Path(a.root)
    summary = json.loads((root / "confirmation_summary.json").read_text())
    f11 = root / "confirmation_summary_11maps.json"
    summary11 = json.loads(f11.read_text()) if f11.exists() else None
    tables, figures = Path(a.tables), Path(a.figures)
    tables.mkdir(parents=True, exist_ok=True)
    (tables / "confirmation_level2.tex").write_text(level2_table(summary, summary11) + "\n")
    maps = list(summary["maps"]) + ([m for m in summary11["maps"] if m not in summary["maps"]] if summary11 else [])
    (tables / "confirmation_level1.tex").write_text(level1_table(root, maps) + "\n")
    forest(summary, summary11, figures / "fig_confirmation_forest.pdf")
    if a.descriptors:
        (tables / "confirmation_moderators.md").write_text(moderators(summary, summary11, Path(a.descriptors)))
    print(f"written: {tables}/confirmation_level2.tex, confirmation_level1.tex; {figures}/fig_confirmation_forest.pdf")


if __name__ == "__main__":
    main()
