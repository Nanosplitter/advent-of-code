"""
Advent of Code 2025 - Day 2
"""

import sys

sys.path.insert(0, str(__file__).split("2025")[0])
from libraries.aoc_runner import run, get_input


def parse(lines: list[str]):
    """Parse the input lines into your desired format."""

    ranges = lines[0].strip().split(",")

    res = []

    for range in ranges:
        bounds = range.split("-")
        res.append(tuple(map(int, bounds)))

    return res


def part1(data) -> int:
    invalid_ids = []

    for range in data:
        check = range[0]
        while check <= range[1]:
            check_str = str(check)
            half = check_str[: len(check_str) // 2]

            if len(check_str) % 2 == 0:
                if range[0] <= int(half + half) <= range[1]:
                    print("Adding invalid ID:", half + half)
                    invalid_ids.append(int(half + half))
            if half == "":
                half = "0"
            check = int(str(int(half) + 1) + str(int(half) + 1))

    return sum(invalid_ids)


def part2(data) -> int:
    """Solve part 2."""
    return 0


if __name__ == "__main__":
    run(part1, part2, parser=parse)
