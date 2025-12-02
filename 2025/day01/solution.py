"""
Advent of Code 2025 - Day 1
"""

import sys

sys.path.insert(0, str(__file__).split("2025")[0])
from libraries.aoc_runner import run


def parse(lines: list[str]) -> list[tuple[str, int]]:
    """Parse lines into list of (direction, amount) tuples."""
    rotations = []
    for line in lines:
        if line.strip():
            direction = line[0]
            amount = int(line[1:])
            rotations.append((direction, amount))
    return rotations


def part1(rotations: list[tuple[str, int]]) -> int:
    dial = 50

    count = 0

    for rotation in rotations:
        if rotation[0] == "R":
            dial += rotation[1]
        else:
            dial -= rotation[1]

        dial %= 100

        if dial == 0:
            count += 1

    return count


def part2(rotations: list[tuple[str, int]]) -> int:
    dial = 50
    count = 0

    for rotation in rotations:
        start_pos = dial
        movement = rotation[1]

        full_rotations = movement // 100

        count += full_rotations

        movement %= 100

        if rotation[0] == "R":
            dial += movement
        else:
            dial -= movement

        if dial <= 0:
            count += 1 if not start_pos == 0 else 0
        if dial >= 100:
            count += 1

        dial %= 100

    return count


if __name__ == "__main__":
    run(part1, part2, parser=parse)
