"""Default-reproduction check of round v13 (2026-09-29; already-used seeds, not a result).

The form-variant options added for v13 (distance_utility, distance_scale, min_dwell_steps in PriorityWeights) must
leave every policy unchanged at their defaults. This check re-runs the first episodes of every agent of the frozen
Part G-fit test -- the four G-fit fits, the six earlier fits, the adopted trees and the designed styles with and
without their route channel, on all nine maps and three scenarios, with the G-fit test seed base -- through the frozen
run_fitting_g.stage_test_g, and compares them with the stored rows of repro_outputs/v11_fit/test_rows.csv in every
shared column. It complements check_policy_defaults.py --defaults (before/after the change) and the reproduction
check of the G-fit protocol (run_fitting_g.py --stage check).
Usage: python experiments/check_v13_defaults.py --out ../repro_outputs/_check_v13_defaults/v11_test --jobs 4
"""
from __future__ import annotations

import argparse
import csv
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_fitting_g as rfg  # noqa: E402

rf, rfc = rfg.rf, rfg.rfc
V11 = rfg.ROOT / "repro_outputs" / "v11_fit"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    p.add_argument("--jobs", type=int, default=4)
    p.add_argument("--episodes", type=int, default=2)
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=False)
    rf.SEED_BASES.update(rfg.SEED_BASES)
    rfc.EPISODES["test"] = a.episodes
    shutil.copy(V11 / "fitted.json", out / "fitted.json")
    rfg.stage_test_g(out, a.jobs)

    def key(r: dict) -> tuple:
        return r["agent"], r["map"], r["scenario"], r["episode"]

    with (out / "test_rows.csv").open() as fh:
        new = {key(r): r for r in csv.DictReader(fh)}
    with (V11 / "test_rows.csv").open() as fh:
        old = {key(r): r for r in csv.DictReader(fh) if int(r["episode"]) < a.episodes}
    by_agent: dict = {}
    for k, o in old.items():
        n = new.get(k)
        rec = by_agent.setdefault(k[0], {"n": 0, "same": 0, "missing": 0, "diffs": {}})
        rec["n"] += 1
        if n is None:
            rec["missing"] += 1
            continue
        bad = [c for c in o if c in n and o[c] != n[c]]
        rec["same"] += not bad
        for c in bad:
            rec["diffs"][c] = rec["diffs"].get(c, 0) + 1
    ok = bool(by_agent) and all(r["same"] == r["n"] for r in by_agent.values()) and len(new) == len(old)
    lines = [f"# v13 default-reproduction check against the stored Part G-fit test rows (episodes 0-{a.episodes - 1}, "
             f"test seed base {rfg.SEED_BASES['c_test']})", "",
             f"stored rows compared: {len(old)}; re-run rows: {len(new)}"]
    for ag, r in sorted(by_agent.items()):
        lines.append(f"- {ag}: {r['same']}/{r['n']} episodes identical in every shared column"
                     + (f"; missing {r['missing']}" if r["missing"] else "")
                     + (f"; differing columns {r['diffs']}" if r["diffs"] else ""))
    lines.append("V13 DEFAULTS CHECK " + ("PASSED" if ok else "FAILED"))
    (out / "check.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
