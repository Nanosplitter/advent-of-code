def read_input():
    with open("input.txt") as f:
        return f.readlines()


inputs = []

for i in read_input():
    inputs.append(i.replace("\n", ""))


def sum_complete_part_numbers(lines):
    non_symbols = set([".", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"])
    total_sum = 0

    def is_adjacent_to_symbol(column, line):
        surrounding_symbols = []

        # check upper left
        if column > 0 and line > 0 and lines[line - 1][column - 1] not in non_symbols:
            surrounding_symbols.append(
                (True, column - 1, line - 1, lines[line - 1][column - 1])
            )

        # check up
        if line > 0 and lines[line - 1][column] not in non_symbols:
            surrounding_symbols.append(
                (True, column, line - 1, lines[line - 1][column])
            )

        # check upper right
        if (
            column < len(lines[line]) - 1
            and line > 0
            and lines[line - 1][column + 1] not in non_symbols
        ):
            surrounding_symbols.append(
                (True, column + 1, line - 1, lines[line - 1][column + 1])
            )

        # check left
        if column > 0 and lines[line][column - 1] not in non_symbols:
            surrounding_symbols.append(
                (True, column - 1, line, lines[line][column - 1])
            )

        # check right
        if column < len(lines[line]) - 1 and lines[line][column + 1] not in non_symbols:
            surrounding_symbols.append(
                (True, column + 1, line, lines[line][column + 1])
            )

        # check lower left
        if (
            column > 0
            and line < len(lines) - 1
            and lines[line + 1][column - 1] not in non_symbols
        ):
            surrounding_symbols.append(
                (True, column - 1, line + 1, lines[line + 1][column - 1])
            )

        # check down
        if line < len(lines) - 1 and lines[line + 1][column] not in non_symbols:
            surrounding_symbols.append(
                (True, column, line + 1, lines[line + 1][column])
            )

        # check lower right
        if (
            column < len(lines[line]) - 1
            and line < len(lines) - 1
            and lines[line + 1][column + 1] not in non_symbols
        ):
            surrounding_symbols.append(
                (True, column + 1, line + 1, lines[line + 1][column + 1])
            )

        surrounding_symbols.append((False, -1, -1, ""))
        return surrounding_symbols

    surrounded_nums = []
    valid_nums = []
    for line in range(len(lines)):
        column = 0
        while column < len(lines[line]):
            if lines[line][column].isdigit():
                number_str = ""
                while column < len(lines[line]) and lines[line][column].isdigit():
                    number_str += lines[line][column]
                    column += 1

                    for i in range(column - len(number_str), column):
                        adj_value = is_adjacent_to_symbol(i, line)
                        if any(i[0] for i in adj_value):
                            for i in adj_value:
                                if i[0]:
                                    surrounded_nums.append(
                                        [number_str, i[1], i[2], i[3]]
                                    )

                if any(
                    any(i[0] for i in is_adjacent_to_symbol(column, line))
                    for column in range(column - len(number_str), column)
                ):
                    valid_nums.append(number_str)
                    total_sum += int(number_str)
            else:
                column += 1

    surrounded_nums = list(
        filter(lambda x: x[3] == "*" and x[0] in valid_nums, surrounded_nums)
    )

    gear_sum = 0
    gear_groups = dict()
    for num in surrounded_nums:
        if str(num[1]) + "," + str(num[2]) in gear_groups:
            gear_groups[str(num[1]) + "," + str(num[2])].append(num[0])
        else:
            gear_groups[str(num[1]) + "," + str(num[2])] = [num[0]]

    multiplied_numbers = []

    for cell in gear_groups:
        if len(gear_groups[cell]) == 2:
            multiplied_numbers.append(int(gear_groups[cell][0]))
            multiplied_numbers.append(int(gear_groups[cell][1]))
            gear_sum += int(gear_groups[cell][0]) * int(gear_groups[cell][1])

    for i in sorted(multiplied_numbers):
        print(i)

    return total_sum, gear_sum


print(sum_complete_part_numbers(inputs))
