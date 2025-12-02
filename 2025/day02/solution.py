"""
Advent of Code 2025 - Day 2
"""

import sys
from functools import cache

sys.path.insert(0, str(__file__).split("2025")[0])
from libraries.aoc_runner import run


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
                    invalid_ids.append(int(half + half))
            if half == "":
                half = "0"
            check = int(str(int(half) + 1) + str(int(half) + 1))

    return sum(invalid_ids)


@cache
def check_invalid(fruit: str, range_start: int, range_end: int) -> list[int]:
    invalid_ids = []

    for seed in generate_seeds(fruit):
        check = int(seed)

        while check <= range_end:
            if check >= range_start:
                invalid_ids.append(check)

            check = int(str(check) + seed)
    return invalid_ids


@cache
def generate_seeds(fruit: str) -> list[str]:
    seeds = []

    for i in range(len(fruit)):
        seeds.append(fruit[: i + 1])

    return seeds


def part2(data) -> int:
    invalid_ids = []

    for low, high in data:
        low_str = str(low)
        high_str = str(high)
        low_half = low_str[: (len(low_str) // 2)]
        if low_half == "":
            low_half = 1
        high_half = high_str[: (len(high_str) // 2) + (len(high_str) % 2 != 0)]

        range_invalid = []

        for fruit in range(int(low_half), int(high_half) + 1):
            invalid = list(set(check_invalid(str(fruit), low, high)))

            range_invalid += invalid

        range_invalid = list(set(range_invalid))
        invalid_ids += range_invalid

    return sum(invalid_ids)


if __name__ == "__main__":
    run(part1, part2, parser=parse)
