from collections import defaultdict
from functools import cache, lru_cache
from itertools import product
import sys

N_PAD = {
    "0": [("2", "^"), ("A", ">")],
    "1": [("2", ">"), ("4", "^")],
    "2": [("0", "v"), ("1", "<"), ("3", ">"), ("5", "^")],
    "3": [("2", "<"), ("6", "^"), ("A", "v")],
    "4": [("1", "v"), ("5", ">"), ("7", "^")],
    "5": [("2", "v"), ("4", "<"), ("6", ">"), ("8", "^")],
    "6": [("3", "v"), ("5", "<"), ("9", "^")],
    "7": [("4", "v"), ("8", ">")],
    "8": [("5", "v"), ("7", "<"), ("9", ">")],
    "9": [("6", "v"), ("8", "<")],
    "A": [("0", "<"), ("3", "^")],
}
D_PAD = {
    "^": [("A", ">"), ("v", "v")],
    "<": [("v", ">")],
    "v": [("<", "<"), ("^", "^"), (">", ">")],
    ">": [("v", "<"), ("A", "^")],
    "A": [("^", "<"), (">", "v")],
}
PADS = [N_PAD] + [D_PAD] * 24

num_paths_cache = defaultdict(None)
key_paths_cache = defaultdict(None)

@cache
def bfs(pad_type, start, target, visited=(), path=()):
    if start == target:
        return [path]
    if start in visited:
        return []
    
    all_paths = []
    for next, dir in PADS[pad_type][start]:
        new_paths = bfs(pad_type, next, target, visited + (start,), path + (dir,))
        if new_paths:
            all_paths.extend(new_paths)
    
    if all_paths:
        min_turns = min(sum(1 for i in range(1, len(p)) if p[i] != p[i-1]) for p in all_paths)
        min_turn_paths = [p for p in all_paths if sum(1 for i in range(1, len(p)) if p[i] != p[i-1]) == min_turns]
        return min_turn_paths

    return []

@cache
def get_path(code, robot_type):
    code_path = []
    for pair in zip(code, code[1:]):
        if robot_type == 0:
            path = num_paths_cache[pair]
        else:
            path = key_paths_cache[pair]

        code_path.extend(path)
        code_path.append("A")
    return code_path

@cache
def get_keypad_len(code, num_robots, robot_type=0):
    if num_robots == 0:
        return len(code)
    
    total_moves = 0
    for pair in zip(('A',) + code, code):
        if robot_type == 0:
            paths = num_paths_cache[pair]
        else:
            paths = key_paths_cache[pair]

        total_moves += min(get_keypad_len(path + ('A',), num_robots - 1, 1) for path in paths)
    
    return total_moves

def get_complexity(codes, num_robots):
    return sum(get_keypad_len(tuple(list(code)), num_robots + 1) * int(code[:-1]) for code in codes)

def part1(codes):
    return get_complexity(codes, 2)
    
def part2(codes):
    return get_complexity(codes, 25)

if len(sys.argv) < 2:
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    instructions = f.readlines()
    
    num_pad_combos = product("0123456789A", repeat=2)
    for combo in num_pad_combos:
        num_paths_cache[combo] = bfs(0, combo[0], combo[1])
        
    key_pad_combos = product("<^>vA", repeat=2)
    for combo in key_pad_combos:
        key_paths_cache[combo] = bfs(1, combo[0], combo[1])

    codes = [code.strip() for code in instructions]
    print(part1(codes))
    print(part2(codes))