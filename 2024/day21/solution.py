from collections import defaultdict
from functools import cache, lru_cache
from itertools import product
import os
import sys
import time

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

# VISUALIZATION

@cache
def get_keypad_path(code, num_robots, robot_type=0):
    if num_robots == 0:
        return code
    
    complete_path = []
    for pair in zip(('A',) + code, code):
        if robot_type == 0:
            paths = num_paths_cache[pair]
        else:
            paths = key_paths_cache[pair]

        complete_path += min([get_keypad_path(path + ('A',), num_robots - 1, 1) for path in paths], key=len)
    
    return complete_path



class Keypad:
    def __init__(self, key_type, name):
        self.name = name
        self.key_type = key_type
        if key_type == 0:
            self.keys = [
                ['7', '8', '9'],
                ['4', '5', '6'],
                ['1', '2', '3'],
                [' ', '0', 'A']
            ]
        else:
            self.keys = [
                [' ', '^', 'A'],
                ['<', 'v', '>'],
                [' ', ' ', ' '],
                [' ', ' ', ' '],
            ]
        self.pointer = 'A'
        self.pressed = False
    
    def process_input(self, instruction):
        if instruction == ' ':
            self.pressed = False
        
        if instruction == 'A':
            self.pressed = True
        
        pad = N_PAD if self.key_type == 0 else D_PAD
        
        for next, dir in pad[self.pointer]:
            if instruction == dir:
                self.pointer = next
                break

    def __str__(self):
        border = "             "
        lines = []
        for row in self.keys:
            lines.append(border)
            line = ""
            for key in row:
                if key == self.pointer:
                    if self.pressed:
                        line += f" \033[42m {key} \033[0m "
                    else:
                        line += f" \033[93m {key} \033[0m "
                else:
                    line += f"  {key}  "  # Adjusted spacing for alignment
            line += " "
            lines.append(line)
        lines.append(border)
        return self.name + "   \n" + "\n".join(lines) + "\n"

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
    #print(part1(codes))
    #print(part2(codes))
    
    num_robots = 3
    
    presses = ["".join(get_keypad_path(tuple(list(codes[0])), robot + 1)) for robot in range(num_robots)[::-1]]
    
    for robot in range(1, num_robots):
        new_presses = ""
        for press in presses[robot - 1]:
            if press == "A":
                new_presses += presses[robot][0]
                presses[robot] = presses[robot][1:]
            else:
                new_presses += " "
        presses[robot] = new_presses
    
    for press in presses:
        print(press)
    
    keypads = [Keypad(1, f"Robot {i + 1} Keypad") for i in range(num_robots - 1)]
    keypads.append(Keypad(0, "Final Robot Numpad"))
    
    human_keypad = Keypad(1, "Human keypad")
    
    output = ""
    for press_index in range(len(presses[0])):
        instructions_str = ""
        for i, press in enumerate(presses[0]):
            if i % 36 == 0:
                instructions_str += "\n"
            if i == press_index:
                instructions_str += f"\033[93m{press}\033[0m "
            else:
                instructions_str += f"{press} "
        instructions_str += "\n"
        
        # Update Human Keypad
        human_keypad.pointer = presses[0][press_index]
        human_keypad.pressed = True
        os.system('cls||clear')
        
        # Update all keypads with their respective presses
        for i, pad in enumerate(keypads):
            pad.process_input(presses[i][press_index])
        
        human_str = str(human_keypad).split('\n')
        keypad_strs = [str(pad).split('\n') for pad in keypads]
        
        combined = "\n".join(
            "  ".join(pads[i] for pads in [human_str] + keypad_strs)
            for i in range(len(human_str))
        )
        print(f"Instructions:\n{instructions_str}")
        print(combined)
        print(f"Output: {output}")
        
        time.sleep(0.5)

        if keypads[-1].pressed:
            output += keypads[-1].pointer
        
        os.system('cls||clear')
        human_keypad.pressed = False
        
        for key in keypads:
            key.pressed = False
        
        combined = "\n".join(
            "  ".join(pads[i] for pads in [str(human_keypad).split('\n')] + [str(pad).split('\n') for pad in keypads])
            for i in range(len(str(human_keypad).split('\n')))
        )
        print(f"Instructions:\n{instructions_str}")
        print(combined)
        print(f"Output: {output}")
        time.sleep(0.2)



