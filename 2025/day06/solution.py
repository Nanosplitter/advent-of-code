"""
Advent of Code 2025 - Day 6
"""

import sys

sys.path.insert(0, str(__file__).split("2025")[0])
from libraries.aoc_runner import run


def parse(lines: list[str]):
    data = []
    operators = lines[-1].split()

    for line in lines[:-1]:
        if line.strip():
            data.append(list(map(int, line.strip().split())))

    return (data, operators)


def parse_pt2(lines: list[str]):
    data = []
    operators = lines[-1].split()

    for line in lines[:-1]:
        data.append(line)

    return (data, operators)


def part1(data) -> int:
    numbers = data[0]
    operators = data[1]

    totals = [0] * len(operators)

    for i, operator in enumerate(operators):
        for number_line in numbers:
            if operator == "*":
                if totals[i] == 0:
                    totals[i] = 1
                totals[i] *= number_line[i]
            elif operator == "+":
                totals[i] += number_line[i]

    print(totals)
    return sum(totals)


def part2(data) -> int:
    operators = data[1][::-1]
    rotated = list(zip(*data[0][::-1]))
    rotated = list(zip(*rotated[::-1]))
    rotated = zip(*rotated[::-1])

    problems = []

    problem = []
    for row in rotated:
        line = "".join(row).strip()
        if line:
            problem.append(int(line))
        else:
            problems.append(problem)
            problem = []
    problems.append(problem)

    totals = [0] * len(operators)
    for i, problem in enumerate(problems):
        operator = operators[i]
        for number in problem:
            if operator == "*":
                if totals[i] == 0:
                    totals[i] = 1
                totals[i] *= number
            elif operator == "+":
                totals[i] += number

    return sum(totals)


if __name__ == "__main__":
    run(part1, parser=parse)
    run(part2, parser=parse_pt2)
