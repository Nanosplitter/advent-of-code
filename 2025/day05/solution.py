"""
Advent of Code 2025 - Day 5
"""

import sys

sys.path.insert(0, str(__file__).split("2025")[0])
from libraries.aoc_runner import run


def parse(lines: list[str]):
    ranges = []
    ingredients = []
    for line in lines:
        if line.strip() == "":
            continue
        if "-" in line:
            ranges.append(list(map(int, line.strip().split("-"))))
        else:
            ingredients.append(int(line.strip()))

    return (ranges, ingredients)


def part1(data) -> int:
    valid_ids = set()

    ranges = data[0]
    ingredients = data[1]

    for ingredient in ingredients:
        for r in ranges:
            if r[0] <= ingredient <= r[1]:
                valid_ids.add(ingredient)
                break
    return len(valid_ids)


def part2(data) -> int:
    combined_ranges = []
    ranges = data[0]

    for r in sorted(ranges):
        if not combined_ranges or combined_ranges[-1][1] < r[0] - 1:
            combined_ranges.append(r)
        else:
            combined_ranges[-1][1] = max(combined_ranges[-1][1], r[1])
    total_nums = 0
    for r in combined_ranges:
        total_nums += r[1] - r[0] + 1

    return total_nums


if __name__ == "__main__":
    run(part1, part2, parser=parse)
