"""Exploratory (2026-09-28; development seeds, not a result). User: "조금더 큰 맵에서 진행하면 좋을듯. 사이즈를 50x50으로
2배씩 늘리면 어떤 일이 벌어지지? 계산이 더 많이 요구되나? 기존의 map의 방해물의 크기는 유지하고 위치만 간격을 맵 크기 커진거를
기반으로 이동만 시키면 좋을듯." -- what happens on 50x50 versions of the two development maps, and what they cost.

Variants of each development map (random seed 7, urban seed 11):
  base25    the 25x25 map of the main experiment
  spread50  50x50: every obstacle component (4-connected) keeps its shape and size and is moved so that its top-left
            cell doubles its coordinates (the user's proposal; the obstacle density falls to about a quarter)
  zoom50    50x50: every cell becomes a 2x2 block (same layout and density; obstacles and streets twice as wide)
  regen50   50x50 from the same generator with the same density and seed (same local statistics, more obstacles)
Key cells of the 50x50 variants: spawn cells (4,4) and (44,44), objective (44,4) (the 25x25 cells doubled); the second
agent of a team spawns two cells further in, as on 25x25; a 3x3 zone around every key cell is kept free.
Everything else as in the main experiment: view radius 9, weapon range 7, 550 steps, 6 + 6 items, Control threshold
120, respawn 25, the Aggressive opponent, the five movement and perception rules (set by the launcher).
Per variant: map descriptors (obstacle density, reachable free cells, shortest path from spawn_a to the objective,
visibility = mean number of free cells within 9 cells in line of sight of a free cell, 300 sampled cells), and the four
styles x three scenarios x N episodes (development seed base 5701): seconds per episode and behaviour means.
Output: repro_outputs/dev_map50/{rows.csv, maps.json, summary.md}.
Usage: python experiments/explore_map50.py --episodes 8 --jobs 4 --out ../repro_outputs/dev_map50
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics as st
import sys
import time
from collections import deque
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dataclasses import replace  # noqa: E402

from fps_priority_ai.config import MapConfig  # noqa: E402
from fps_priority_ai.env import build_world  # noqa: E402
from fps_priority_ai.experiment import episode_seed, run_episode, testbed_flags  # noqa: E402
from fps_priority_ai.maps import MAPS, component, key_cells, map_ok  # noqa: E402
from fps_priority_ai.runner import default_scenarios, default_styles  # noqa: E402

SEED_BASE = 5701
KEY50 = {"spawn_a": (4, 4), "spawn_b": (44, 44), "objective": (44, 4)}
METRICS = ["objective_commitment_ratio", "engagement_redirection_rate_per_100", "resource_seeking_rate_per_100",
           "avg_ally_proximity", "kills", "deaths", "control_score", "goal_switch_rate_per_100", "walked_hits_per_step",
           "los_frac", "hits_taken_per_step", "far_pursuit_share"]


def obstacle_components(obstacles: set) -> list:
    seen, comps = set(), []
    for c in sorted(obstacles):
        if c in seen:
            continue
        comp, queue = [], deque([c])
        seen.add(c)
        while queue:
            x, y = queue.popleft()
            comp.append((x, y))
            for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if n in obstacles and n not in seen:
                    seen.add(n)
                    queue.append(n)
        comps.append(comp)
    return comps


def clear_zones(cells: set, cfg: MapConfig) -> set:
    keys = [cfg.spawn_a, cfg.spawn_b, cfg.objective, (cfg.spawn_a[0] + cfg.spawn_separation, cfg.spawn_a[1]),
            (cfg.spawn_b[0] - cfg.spawn_separation, cfg.spawn_b[1])]
    zone = {(x + dx, y + dy) for x, y in keys for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    return cells - zone


def variants() -> dict:
    out = {}
    for name in ("random", "urban"):
        base = MAPS[name]
        out[f"{name}/base25"] = base
        obst = set(build_world(base).obstacles)
        c50 = MapConfig(width=50, height=50, seed=base.seed, layout="custom", **KEY50)
        spread = set()
        for comp in obstacle_components(obst):
            mx, my = min(x for x, _ in comp), min(y for _, y in comp)
            spread |= {(x + mx, y + my) for x, y in comp}           # top-left cell (mx, my) -> (2 mx, 2 my)
        spread = {c for c in spread if 0 <= c[0] < 50 and 0 <= c[1] < 50}
        out[f"{name}/spread50"] = replace(c50, obstacles=tuple(sorted(clear_zones(spread, c50))))
        zoom = {(2 * x + dx, 2 * y + dy) for x, y in obst for dx in (0, 1) for dy in (0, 1)}
        out[f"{name}/zoom50"] = replace(c50, obstacles=tuple(sorted(clear_zones(zoom, c50))))
        regen = replace(base, width=50, height=50, **KEY50)
        seed = base.seed
        while not map_ok(replace(regen, seed=seed)):
            seed += 1
        out[f"{name}/regen50"] = replace(regen, seed=seed)
    return out


def descriptors(cfg: MapConfig) -> dict:
    world = build_world(cfg)
    free = component(world, cfg.spawn_a)
    dist, queue = {cfg.spawn_a: 0}, deque([cfg.spawn_a])
    while queue:
        x, y = queue.popleft()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if n not in dist and world.passable(n):
                dist[n] = dist[(x, y)] + 1
                queue.append(n)
    rng = random.Random(0)
    sample = rng.sample(sorted(free), min(300, len(free)))
    vis = []
    for a in sample:
        n = 0
        for b in free:
            if b != a and (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 <= 81 and world.los_clear(a, b):
                n += 1
        vis.append(n)
    return {"width": cfg.width, "density": round(len(world.obstacles) / (cfg.width * cfg.height), 3),
            "reachable": len(free), "path_to_objective": dist.get(cfg.objective), "visibility": round(st.mean(vis), 1),
            "ok": map_ok(cfg), "seed": cfg.seed, "layout": cfg.layout}


def run_task(task: tuple) -> dict:
    vname, cfg, style_name, scen_name, ep = task
    styles = default_styles("exp")
    sc = next(s for s in default_scenarios() if s.name == scen_name)
    t = time.perf_counter()
    row = run_episode(sc, styles[style_name], styles, episode_seed(SEED_BASE, scen_name, ep), cfg)
    return {"variant": vname, "style": style_name, "scenario": scen_name, "episode": ep,
            "seconds": round(time.perf_counter() - t, 4), **{m: row.get(m, "") for m in METRICS}}


def mean(rows, m):
    v = [float(r[m]) for r in rows if r.get(m) not in ("", None)]
    return st.mean(v) if v else float("nan")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--episodes", type=int, default=8)
    p.add_argument("--jobs", type=int, default=4)
    p.add_argument("--out", default="../repro_outputs/dev_map50")
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=False)
    vs = variants()
    desc = {k: descriptors(v) for k, v in vs.items()}
    (out / "maps.json").write_text(json.dumps({"descriptors": desc, "testbed": testbed_flags(),
                                               "configs": {k: {"width": v.width, "layout": v.layout, "seed": v.seed,
                                                               "obstacles": len(v.obstacles)} for k, v in vs.items()}},
                                              indent=1))
    styles = list(default_styles("exp"))
    tasks = [(k, v, s, sc.name, ep) for k, v in vs.items() for s in styles for sc in default_scenarios()
             for ep in range(a.episodes)]
    t0 = time.time()
    with Pool(a.jobs) as pool:
        rows = list(pool.imap_unordered(run_task, tasks, chunksize=1))
    with (out / "rows.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    md = [f"# 50x50 variants of the development maps (exploratory; seed base {SEED_BASE}, {a.episodes} episodes per "
          f"condition; {len(rows)} episodes in {time.time() - t0:.0f} s with {a.jobs} jobs)", "",
          "## Maps", "", "| variant | density | reachable | path to objective | visibility | ok |", "|---|---|---|---|---|---|"]
    for k, d in desc.items():
        md.append(f"| {k} | {d['density']} | {d['reachable']} | {d['path_to_objective']} | {d['visibility']} | {d['ok']} |")
    md += ["", "## Seconds per episode (mean over styles and scenarios; relative to base25 of the same map)", ""]
    for name in ("random", "urban"):
        base = mean([r for r in rows if r["variant"] == f"{name}/base25"], "seconds")
        for k in vs:
            if k.startswith(name):
                s = mean([r for r in rows if r["variant"] == k], "seconds")
                md.append(f"- {k}: {s:.2f} s ({s / base:.1f}x)")
    md += ["", "## Behaviour (means)", "",
           "| variant | style | Mission commit. | Mission switches | DM redirect. | DM kills | DM deaths | DM los | "
           "DM walked hits | DM ally dist | Control score | Control wins |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k in vs:
        for s in styles:
            rm = [r for r in rows if r["variant"] == k and r["style"] == s and r["scenario"] == "Mission"]
            rd = [r for r in rows if r["variant"] == k and r["style"] == s and r["scenario"] == "Deathmatch"]
            rc = [r for r in rows if r["variant"] == k and r["style"] == s and r["scenario"] == "Control"]
            wins = sum(1 for r in rc if r["control_score"] not in ("", None) and float(r["control_score"]) >= 120)
            md.append(f"| {k} | {s} | {mean(rm, 'objective_commitment_ratio'):.2f} | {mean(rm, 'goal_switch_rate_per_100'):.2f} | "
                      f"{mean(rd, 'engagement_redirection_rate_per_100'):.2f} | {mean(rd, 'kills'):.1f} | "
                      f"{mean(rd, 'deaths'):.1f} | {mean(rd, 'los_frac'):.3f} | {mean(rd, 'walked_hits_per_step'):.3f} | "
                      f"{mean(rd, 'avg_ally_proximity'):.1f} | {mean(rc, 'control_score'):.0f} | {wins}/{len(rc)} |")
    (out / "summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
