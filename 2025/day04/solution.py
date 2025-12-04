"""
Advent of Code 2025 - Day 4
"""

import sys

sys.path.insert(0, str(__file__).split("2025")[0])
from libraries.aoc_runner import run
from libraries.grid import Grid


def parse(lines: list[str]) -> Grid:
    return Grid([list(x) for x in lines])


def is_liftable(row: int, col: int, grid: Grid) -> bool:
    if grid.get(row, col) == ".":
        return False
    neighbors = grid.neighbors(row, col)
    rolls = [n for n in neighbors if n[0] == "@"]

    return len(rolls) < 4


def part1(grid: Grid) -> int:
    total_lifted = 0
    for r in range(grid.height):
        for c in range(grid.width):
            if is_liftable(r, c, grid):
                total_lifted += 1

    return total_lifted


def part2(grid) -> int:
    total_lifted = 0
    while True:
        liftable_spots = []
        for r in range(grid.height):
            for c in range(grid.width):
                if is_liftable(r, c, grid):
                    liftable_spots.append((r, c))

        for spot in liftable_spots:
            total_lifted += 1
            grid.set(spot[0], spot[1], ".")
        if liftable_spots == []:
            break

    return total_lifted


if __name__ == "__main__":
    run(part1, part2, parser=parse)
