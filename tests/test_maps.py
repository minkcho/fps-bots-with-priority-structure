"""Map registry checks (2026-09-25): reachability of every registered map, the seed-selection rule of the
map sample, and the unchanged base maps (obstacle counts of the maps used in the paper's final run)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fps_priority_ai import maps  # noqa: E402  (importing runs check_map on every registered map)
from fps_priority_ai.env import build_world  # noqa: E402


def main() -> None:
    for name, cfg in maps.MAPS.items():
        assert maps.map_ok(cfg), name
    for kind in ("random", "urban"):
        assert tuple(maps.first_valid_seeds(maps.BASE_MAPS[kind])) == maps.SAMPLE_SEEDS[kind], kind
    assert len(build_world(maps.MAPS["random"]).obstacles) == 108
    assert len(build_world(maps.MAPS["urban"]).obstacles) == 158
    assert set(maps.CONFIRMATION_MAPS) <= set(maps.MAPS)
    print("[OK]", len(maps.MAPS), "maps reachable; sample seeds", maps.SAMPLE_SEEDS, "; base maps unchanged")


if __name__ == "__main__":
    main()
