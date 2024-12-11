class Antenna:
    def __init__(self, row, col, symbol):
        self.row = row
        self.col = col
        self.symbol = symbol
    
def is_in_bounds(row, col, instructions) -> bool:
    return 0 <= row < len(instructions) and 0 <= col < len(instructions[0])

def part1(instructions) -> int:
    antennas = []
    for row, line in enumerate(instructions):
        for col, symbol in enumerate(line):
            if symbol != ".":
                antennas.append(Antenna(row, col, symbol))
    
    antinodes = []
    for antenna1 in antennas:
        for antenna2 in [antenna for antenna in antennas if antenna.symbol == antenna1.symbol and antenna != antenna1]:
            check_row = antenna1.row + (antenna1.row - antenna2.row)
            check_col = antenna1.col + (antenna1.col - antenna2.col)
            if is_in_bounds(check_row, check_col, instructions):
                antinodes.append((check_row, check_col))
    
    return len(set(antinodes))

def part2(instructions) -> int:
    antennas = []
    for row, line in enumerate(instructions):
        for col, symbol in enumerate(line):
            if symbol != ".":
                antennas.append(Antenna(row, col, symbol))
    
    antinodes = []
    for antenna1 in antennas:
        for antenna2 in [antenna for antenna in antennas if antenna.symbol == antenna1.symbol and antenna != antenna1]:
            check_row = antenna1.row
            check_col = antenna1.col
            while is_in_bounds(check_row, check_col, instructions):
                antinodes.append((check_row, check_col))
                check_row += (antenna1.row - antenna2.row)
                check_col += (antenna1.col - antenna2.col)
    
    return len(set(antinodes))

with open("input.txt") as f:
    instructions = [line.strip() for line in f.readlines()]

    print(part1(instructions))
    print(part2(instructions))
