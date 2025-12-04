"""
Advent of Code 2025 - Day 3
"""

import sys

sys.path.insert(0, str(__file__).split("2025")[0])
from libraries.aoc_runner import run


def parse(lines: list[str]):
    return lines


def part1(data) -> int:
    best_nums = []
    for bank in data:
        largest_index, largest_battery = max(list(enumerate(bank)), key=lambda x: x[1])

        best_num = 0

        if largest_index != len(bank) - 1:
            second_number = max(bank[largest_index + 1 :])
            best_num = int(str(largest_battery) + str(second_number))
        else:
            first_number = max(bank[:largest_index])
            best_num = int(str(first_number) + str(largest_battery))

        best_nums.append(best_num)
    return sum(best_nums)


def part2(data) -> int:
    best_nums = []
    for bank in data:
        best_index = -1
        best_num = ""
        for i in range(1, 13):
            prev_best = best_index
            remaining_index = 12 - i
            if remaining_index == 0:
                bank_section = bank[best_index + 1 :]
            else:
                bank_section = bank[best_index + 1 : -(12 - i)]
            best_index, best_digit = max(
                list(enumerate(bank_section)), key=lambda x: x[1]
            )
            best_index += prev_best + 1
            best_num += best_digit
        best_nums.append(int(best_num))

    return sum(best_nums)


if __name__ == "__main__":
    run(part1, part2, parser=parse)
