import sys
    
def part1(instructions) -> int:
    return 0

def part2(instructions) -> int:
    return 0

if len(sys.argv) < 2:
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    instructions = f.readlines()

    print(part1(instructions))
    print(part2(instructions))