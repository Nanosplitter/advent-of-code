from collections import defaultdict
import os
import sys
import time
from termcolor import colored

cache = {'': 1}

def color_towel(towel):
    res = ""
    for color in towel:
        if color == "w":
            res += colored("   ", 'black', 'on_white')
        elif color == "r":
            res += colored("   ", 'white', 'on_red')
        elif color == "b":
            res += colored("   ", 'white', 'on_black')
        elif color == "g":
            res += colored("   ", 'white', 'on_green')
        elif color == "u":
            res += colored("   ", 'white', 'on_blue')
    return res

def num_ways_to_make(design, towels):
    if not design:
        return 1, []
    
    if design not in cache:
        total, example = 0, []
        for towel in towels:
            if design.startswith(towel):
                ways, sol = num_ways_to_make(design[len(towel):], towels)
                total += ways
                if not example and sol is not None:
                    example = [towel] + sol
        cache[design] = (total, example)
    
    return cache[design]

def part1(towels, designs, visualize=False) -> str:
    
    matches_found = 0
        
    for design in designs:
        
        ways_to_make = num_ways_to_make(design, towels)
        matches_found += 1 if ways_to_make[0] > 0 else 0
        
        if visualize:
            os.system('cls||clear')
            print("="*300)
            print(f"Design:                {color_towel(design)}")
            time.sleep(0.5)
            if ways_to_make[0] == 0:
                os.system('cls||clear')
                print("="*300)
                print(f"No solution possible!: {color_towel(design)}")
            else:
                os.system('cls||clear')
                print("="*300)
                print(f"Solution:              {"|".join([color_towel(towel) for towel in ways_to_make[1]])}")
            time.sleep(1)
    
    return matches_found


def part2(designs, visualize=False) -> int:
    return sum(cache[design][0] for design in designs)

input_file = sys.argv[1]

with open(input_file) as f:
    lines = f.readlines()
    
    towels = tuple([line.strip() for line in lines[0].split(', ')])
    
    designs = [line.strip() for line in lines[2:]]
    
    print(part1(towels, designs, visualize=False))
    print(part2(designs, visualize=False))

