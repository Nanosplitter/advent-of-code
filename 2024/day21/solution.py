from functools import cache, lru_cache
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

@lru_cache
def bfs(pad_type, start, target, visited=(), path=()):
    if start == target:
        #print("Found target", target)
        return path
    if start in visited:
        return None
    
    check_paths = []
    for next, dir in PADS[pad_type][start]:
        check_paths.append(bfs(pad_type, next, target, visited + (start,), path + (dir,)))
    if any(check_paths):
        valid_paths = [cp for cp in check_paths if cp]
        return min(valid_paths, key=lambda p: sum(1 for i in range(1, len(p)) if p[i] != p[i-1])) if valid_paths else None

    return None

# def get_path(code, robot_num):
    


def get_keypad_path(code, num_robots):
    counter = 0
    print("Code", code)
    code = "A" + code
    for robot_num in range(num_robots):
        print(f"Robot {robot_num}")
        code_path = []
        for num in range(len(code) - 1):
            
            print(f"Finding path from {code[num]} to {code[num + 1]}")
            path = bfs(robot_num, code[num], code[num + 1])
            print("got path")
            #print("Path", path)
            code_path.extend(path)
            code_path.append("A")
        
        #print(code_path)
        code = ["A"] + code_path[:]
    return code_path
        
    
def part1(instructions):
    codes = [code.strip() for code in instructions]
    total_complexity = 0
    
    for code in codes:
        path = get_keypad_path(code, 3)
        print(f"Path length for code {code} is {len(path)}")
        total_complexity += len(path) * int(code[:-1])
        
    return total_complexity
    

def part2(instructions):
    codes = [code.strip() for code in instructions]
    total_complexity = 0
    
    for code in codes:
        path = get_keypad_path(code, 25)
        print(f"Path length for code {code} is {len(path)}")
        total_complexity += len(path) * int(code[:-1])
        
    return total_complexity

if len(sys.argv) < 2:
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    instructions = f.readlines()

    print(part1(instructions))
    #print(part2(instructions))