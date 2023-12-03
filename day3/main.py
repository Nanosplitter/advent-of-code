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
        # check upper left
        if column > 0 and line > 0 and lines[line - 1][column - 1] not in non_symbols:
            return (True, column - 1, line - 1, lines[line - 1][column - 1])

        # check up
        if line > 0 and lines[line - 1][column] not in non_symbols:
            return (True, column, line - 1, lines[line - 1][column])

        # check upper right
        if (
            column < len(lines[line]) - 1
            and line > 0
            and lines[line - 1][column + 1] not in non_symbols
        ):
            return (True, column + 1, line - 1, lines[line - 1][column + 1])

        # check left
        if column > 0 and lines[line][column - 1] not in non_symbols:
            return (True, column - 1, line, lines[line][column - 1])

        # check right
        if column < len(lines[line]) - 1 and lines[line][column + 1] not in non_symbols:
            return (True, column + 1, line, lines[line][column + 1])

        # check lower left
        if (
            column > 0
            and line < len(lines) - 1
            and lines[line + 1][column - 1] not in non_symbols
        ):
            return (True, column - 1, line + 1, lines[line + 1][column - 1])

        # check down
        if line < len(lines) - 1 and lines[line + 1][column] not in non_symbols:
            return (True, column, line + 1, lines[line + 1][column])

        # check lower right
        if (
            column < len(lines[line]) - 1
            and line < len(lines) - 1
            and lines[line + 1][column + 1] not in non_symbols
        ):
            return (True, column + 1, line + 1, lines[line + 1][column + 1])

        return (False, -1, -1, "")

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

                    found_gear_for_number = False
                    for i in range(column - len(number_str), column):
                        adj_value = is_adjacent_to_symbol(i, line)
                        if adj_value[0] and not found_gear_for_number:
                            surrounded_nums.append(
                                [number_str, adj_value[1], adj_value[2], adj_value[3]]
                            )
                            found_gear_for_number = True

                if any(
                    is_adjacent_to_symbol(column, line)[0]
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

    for cell in gear_groups:
        if len(gear_groups[cell]) == 2:
            gear_sum += int(gear_groups[cell][0]) * int(gear_groups[cell][1])

    return total_sum, gear_sum


print(sum_complete_part_numbers(inputs))
