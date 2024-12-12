from collections import defaultdict

def get_next_stone(stone):
    new_stones = []
    if stone == '0':
        new_stones.append('1')
    elif len(stone) % 2 == 0:
        new_stones.append(str(int(stone[:len(stone)//2])))
        new_stones.append(str(int(stone[len(stone)//2:])))
    else:
        new_stones.append(str(int(stone) * 2024))
    
    return new_stones


def find_num_stones(instructions, blinks):
    stones_list = instructions[0].split()
    stones = defaultdict(int)
    for stone in stones_list:
        stones[stone] += 1
    
    for i in range(blinks):
        new_stones = defaultdict(int)
        
        for stone, count in stones.items():
            for new_stone in get_next_stone(stone):
                new_stones[new_stone] += count
        stones = new_stones

    num_stones = 0
    for stone, count in stones.items():
        num_stones += count
        
    return num_stones


def part1(instructions) -> int:   
    return find_num_stones(instructions, 25)

def part2(instructions) -> int:
    return find_num_stones(instructions, 75)

with open("2024/day11/input.txt") as f:
    instructions = [line.strip() for line in f.readlines()]

    print(part1(instructions))
    print(part2(instructions))
