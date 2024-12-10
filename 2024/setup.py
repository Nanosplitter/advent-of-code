import os

template_code = '''import numpy as np

def part1(instructions) -> int:
    return 0

def part2(instructions) -> int:
    return 0

with open("input.txt") as f:
    board = f.readlines()

    print(part1(board))
    print(part2(board))
'''

for day in range(7, 26):
    folder_name = f'day{day}'
    os.makedirs(folder_name, exist_ok=True)
    files = ['ex_input.txt', 'input.txt', 'simple_input.txt']
    for file_name in files:
        open(os.path.join(folder_name, file_name), 'w').close()
    with open(os.path.join(folder_name, 'solution.py'), 'w') as f:
        f.write(template_code)