def read_input():
    with open("input.txt") as f:
        return f.readlines()


lines = []

for i in read_input():
    lines.append(i.replace("\n", ""))


class PartNumber:
    def __init__(self, id):
        self.id = id
        self.number = ""
        self.number_cells = []
        self.surronding_cells = []

    def add_number_cell(self, value, row, column):
        self.number_cells.append([value, row, column])
        self.number += value

    def add_surronding_cell(self, cell):
        self.surronding_cells.append(cell)

    def remove_surronding_cell(self, cell):
        self.surronding_cells.remove(cell)

    def __repr__(self):
        return f"PartNumber(id={self.id}, number={self.number})"


def get_surrounding_cells(row, column):
    surrounding_cells = []

    # check upper left
    if column > 0 and row > 0:
        surrounding_cells.append((row - 1, column - 1))

    # check up
    if row > 0:
        surrounding_cells.append((row - 1, column))

    # check upper right
    if column < len(lines[row]) - 1 and row > 0:
        surrounding_cells.append((row - 1, column + 1))

    # check left
    if column > 0:
        surrounding_cells.append((row, column - 1))

    # check right
    if column < len(lines[row]) - 1:
        surrounding_cells.append((row, column + 1))

    # check lower left
    if column > 0 and row < len(lines) - 1:
        surrounding_cells.append((row + 1, column - 1))

    # check down
    if row < len(lines) - 1:
        surrounding_cells.append((row + 1, column))

    # check lower right
    if column < len(lines[row]) - 1 and row < len(lines) - 1:
        surrounding_cells.append((row + 1, column + 1))

    return surrounding_cells


num_parts = 0
part_numbers = []
for row in range(len(lines)):
    column = 0
    while column < len(lines[row]):
        if lines[row][column].isdigit():
            number_str = ""
            part_number = PartNumber(num_parts)
            while column < len(lines[row]) and lines[row][column].isdigit():
                part_number.add_number_cell(lines[row][column], row, column)
                part_number.surronding_cells += get_surrounding_cells(row, column)
                column += 1
            num_parts += 1
            part_numbers.append(part_number)
        else:
            column += 1

total = 0

for row in range(len(lines)):
    for column in range(len(lines[row])):
        if lines[row][column] == "*":
            part_neighbors = []
            for part_number in part_numbers:
                if (row, column) in part_number.surronding_cells:
                    part_neighbors.append(part_number)
            if len(part_neighbors) == 2:
                total += int(part_neighbors[0].number) * int(part_neighbors[1].number)

print(total)
