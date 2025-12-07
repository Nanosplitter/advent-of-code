"""
Advent of Code 2025 - Day 7
"""

import sys

sys.path.insert(0, str(__file__).split("2025")[0])
from libraries.aoc_runner import run


def parse(lines: list[str]):
    return lines


def part1(data) -> int:
    width = len(data[0])
    start_line = data[0]
    beams = [0] * width
    beams[start_line.index("S")] = 1
    splits = 0

    for line in data[1:]:
        for index in range(width):
            if beams[index]:
                if line[index] == "^":
                    splits += 1
                    beams[index] = 0
                    beams[index - 1] = 1
                    beams[index + 1] = 1

    return splits


def part2(data) -> int:
    width = len(data[0])
    start_line = data[0]
    beams = [0] * width
    beams[start_line.index("S")] = 1

    for line in data[1:]:
        for index in range(width):
            if beams[index]:
                if line[index] == "^":
                    beams[index - 1] += beams[index]
                    beams[index + 1] += beams[index]
                    beams[index] = 0

    return sum(beams)


if __name__ == "__main__":
    run(part1, part2, parser=parse)
