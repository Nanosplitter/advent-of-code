"""
Advent of Code 2025 - Day 8
"""

import sys
import numpy as np

sys.path.insert(0, str(__file__).split("2025")[0])
from libraries.aoc_runner import run


def parse(lines: list[str]):
    return [np.array(list(map(int, line.split(",")))) for line in lines]


def distance(p1, p2):
    d = p1 - p2
    return np.sqrt(d[0] * d[0] + d[1] * d[1] + d[2] * d[2])


def junction_key(junction):
    return tuple(int(v) for v in junction)


def junction_to_key(junction):
    if isinstance(junction, np.ndarray):
        return junction_key(junction)
    return tuple(int(v) for v in junction)


distances_flat = []
distances_map = {}


def build_distance_structures(junctions: list[np.ndarray]):
    distances_map.clear()
    distances_flat.clear()

    for idx1, junction1 in enumerate(junctions):
        key1 = junction_key(junction1)
        distances_map.setdefault(key1, {})

        for idx2 in range(idx1 + 1, len(junctions)):
            junction2 = junctions[idx2]
            key2 = junction_key(junction2)

            dist = float(distance(junction1, junction2))

            distances_map[key1][key2] = dist
            distances_map.setdefault(key2, {})[key1] = dist
            distances_flat.append((key1, key2, dist))

    distances_flat.sort(key=lambda entry: entry[2])


def combine_grids(idx1, idx2, grids, grid_keys):
    if idx1 == idx2:
        return

    if idx1 > idx2:
        idx1, idx2 = idx2, idx1

    if idx1 < 0 or idx2 >= len(grids):
        return

    grid1 = grids[idx1]
    grid2 = grids[idx2]
    keys1 = grid_keys[idx1]
    keys2 = grid_keys[idx2]

    for junction in grid2:
        key = junction_to_key(junction)
        if key not in keys1:
            grid1.append(junction)
            keys1.add(key)

    keys1.update(keys2)

    del grids[idx2]
    del grid_keys[idx2]


def rebuild_key_to_grid(grid_keys):
    mapping = {}
    for idx, keys in enumerate(grid_keys):
        for key in keys:
            mapping[key] = idx
    return mapping


def part1(data):
    build_distance_structures(data)

    grids = []
    grid_keys = []

    for junction in data:
        grids.append([junction])
        grid_keys.append({junction_to_key(junction)})

    key_to_grid = rebuild_key_to_grid(grid_keys)

    for junction1, junction2, dist in distances_flat[:1000]:
        grid1 = key_to_grid.get(junction1, -1)
        grid2 = key_to_grid.get(junction2, -1)

        if grid1 >= 0 and grid2 >= 0 and grid1 != grid2:
            combine_grids(grid1, grid2, grids, grid_keys)
            key_to_grid = rebuild_key_to_grid(grid_keys)

    grids = sorted(grids, key=len, reverse=True)
    total = 1
    for grid in grids[:3]:
        total *= len(grid)
    return total


def part2(data) -> int:
    build_distance_structures(data)

    grids = []
    grid_keys = []

    for junction in data:
        grids.append([junction])
        grid_keys.append({junction_to_key(junction)})

    key_to_grid = rebuild_key_to_grid(grid_keys)

    for junction1, junction2, dist in distances_flat:
        grid1 = key_to_grid.get(junction1, -1)
        grid2 = key_to_grid.get(junction2, -1)

        if grid1 >= 0 and grid2 >= 0 and grid1 != grid2:
            combine_grids(grid1, grid2, grids, grid_keys)
            key_to_grid = rebuild_key_to_grid(grid_keys)

        if len(grids) == 1:
            return junction1[0] * junction2[0]


if __name__ == "__main__":
    run(part1, part2, parser=parse)
