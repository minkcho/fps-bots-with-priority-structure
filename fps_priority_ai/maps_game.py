"""Game-inspired maps (2026-09-25; approved by the user in the design review and frozen: no layout change after this
point; SHA-256 of this file in STATE.md and in the confirmation protocol).

One 25 x 25 map per reconstructed game. Each map abstracts structural features that are typical of the
game's maps and modes; none reproduces a specific map.

  cso  bomb-defusal lanes: the objective (bomb site) sits in a walled site with box cover; each team reaches
       it by its own long lane along the map edge (2-cell doors) or through a shared mid area (1-cell side
       entrances); a narrow back tunnel links the two spawns. No pickups (bomb-defusal maps have none;
       equipment is bought at the start of a round).
  ow   control point: the point sits in a central room with four 2-cell entrances and pillar cover; a walled,
       turning main road leads from each spawn to the room, and two flanks with sight-blocking walls lead to
       the side entrances. Health packs in the flanks near the side entrances; ammunition in the spawn zones
       (Overwatch has no ammunition pickups).
  ac   small close-quarters arena (19 x 19 playable cells): an outer corridor, a ring corridor and a central
       courtyard joined by narrow doors, giving many loops and short sightlines; crates break the corridor
       sightlines. Pickups spread over corridors and courtyard.
  xo   open arena: few pillars and short walls, a central platform with exposed health, pickups spread over
       the whole map.

The maps are symmetric so that both teams face the same geometry: `cso` under reflection about the
anti-diagonal ((x, y) -> (24 - y, 24 - x)), the others under point reflection through the centre
((x, y) -> (24 - x, 24 - y)). The loader checks the symmetry of the obstacles, spawn cells, item cells and
objective, which makes the two teams' paths to the objective equal by construction.

Legend: '#' obstacle, '.' free, 'A' spawn cell of team 0 (reading order = agent index), 'B' spawn cell of
team 1, 'O' objective / control point, '+' health item cell, '=' ammunition item cell.
"""
from __future__ import annotations

from typing import Callable, Dict, List, Tuple

from .config import MapConfig, Vec2

SIZE = 25

LAYOUTS: Dict[str, Tuple[str, Tuple[str, ...]]] = {
    "cso": ("anti", (
        "................#........",
        ".........................",
        "..A.A.............#..#...",
        "........#########.#...#..",
        "........#########...O....",
        "........#########........",
        "..####..........#....##..",
        "..####...................",
        "..####....#.......####..#",
        "..####.............###...",
        "..####.......##....###...",
        ".............##....###...",
        "...................###...",
        "..#########........###...",
        "..##########....#..###...",
        "..##########.......###...",
        "..##########.......###...",
        "..##########.............",
        "..##########.............",
        "..##########..#####......",
        "..##########..#####...B..",
        "..##########..#####......",
        "..##########..#####...B..",
        ".........................",
        ".........................",
    )),
    "ow": ("rot", (
        "==.......................",
        "=......................+.",
        "..A.A...#########........",
        "........#########..##....",
        "........#########..##....",
        "..####......#####..##....",
        "..####......#####..##.+..",
        "..####......#####..##....",
        "..####..##..#####........",
        "..#######.......#.....###",
        "..#######.#...#..........",
        "..#######........+.......",
        "........#...O...#........",
        ".......+........#######..",
        "..........#...#.#######..",
        "###.....#.......#######..",
        "........#####..##..####..",
        "....##..#####......####..",
        "..+.##..#####......####..",
        "....##..#####......####..",
        "....##..#########........",
        "....##..#########........",
        "........#########...B.B..",
        ".+......................=",
        ".......................==",
    )),
    "ac": ("rot", (
        "#########################",
        "#########################",
        "#########################",
        "###.....+...#........=###",
        "###.A.A.....#.......#.###",
        "###...................###",
        "###...###..######.#...###",
        "###...#......#.+..#...###",
        "###...#=..........#...###",
        "###=..#..###.###......###",
        "###...#..#.....#......###",
        "###...##.#.+...#..#...###",
        "#####.#.....O.....#.#####",
        "###...#..#...+.#.##...###",
        "###......#.....#..#...###",
        "###......###.###..#..=###",
        "###...#..........=#...###",
        "###...#..+.#......#...###",
        "###...#.######..###...###",
        "###...................###",
        "###.#.......#.....B.B.###",
        "###=........#...+.....###",
        "#########################",
        "#########################",
        "#########################",
    )),
    "xo": ("rot", (
        "............+.........=..",
        ".........................",
        "..A.A....................",
        "...........###...........",
        ".........................",
        "...................+.....",
        "......##.........##......",
        "......##.........##......",
        ".........................",
        ".........=...............",
        "..........#.+.#..........",
        "...#.................#...",
        "=..#........O........#..=",
        "...#.................#...",
        "..........#.+.#..........",
        "...............=.........",
        ".........................",
        "......##.........##......",
        "......##.........##......",
        ".....+...................",
        ".........................",
        "...........###...........",
        "....................B.B..",
        ".........................",
        "..=.........+............",
    )),
}

SYMMETRIES: Dict[str, Callable[[Vec2], Vec2]] = {
    "anti": lambda p: (SIZE - 1 - p[1], SIZE - 1 - p[0]),
    "rot": lambda p: (SIZE - 1 - p[0], SIZE - 1 - p[1]),
}
ITEM_KINDS = {"+": "health", "=": "ammo"}


def parse_layout(name: str, symmetry: str, rows: Tuple[str, ...]) -> MapConfig:
    assert len(rows) == SIZE and all(len(r) == SIZE for r in rows), name
    cells: Dict[str, List[Vec2]] = {}
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            assert ch in "#.ABO+=", (name, x, y, ch)
            cells.setdefault(ch, []).append((x, y))
    mirror = SYMMETRIES[symmetry]
    obstacles = set(cells.get("#", []))
    spawns_a = cells["A"]                                    # reading order = agent index
    spawns_b = [mirror(p) for p in spawns_a]                 # the mirror images, in the same order
    (objective,) = cells["O"]
    items = [(ITEM_KINDS[ch], p) for ch in "+=" for p in cells.get(ch, [])]
    # symmetry checks (equal geometry for both teams)
    assert {mirror(p) for p in obstacles} == obstacles, (name, "obstacles not symmetric")
    assert sorted(spawns_b) == sorted(cells["B"]), (name, "spawn cells not symmetric")
    assert mirror(objective) == objective, (name, "objective not on the symmetry axis")
    assert {(k, mirror(p)) for k, p in items} == set(items), (name, "item cells not symmetric")
    return MapConfig(width=SIZE, height=SIZE, layout="custom", obstacles=tuple(sorted(obstacles)),
                     spawn_a=spawns_a[0], spawn_b=spawns_b[0], spawn_cells=(tuple(spawns_a), tuple(spawns_b)),
                     objective=objective, item_cells=tuple(items),
                     num_health=sum(k == "health" for k, _ in items), num_ammo=sum(k == "ammo" for k, _ in items))


GAME_MAPS: Dict[str, MapConfig] = {name: parse_layout(name, sym, rows) for name, (sym, rows) in LAYOUTS.items()}
