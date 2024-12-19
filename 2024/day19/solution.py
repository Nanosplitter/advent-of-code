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
    
    if design not in cache:
        cache[design] = sum(num_ways_to_make(design[len(towel):], towels) for towel in towels if design.startswith(towel))

    return cache[design]

def part1(towels, designs, visualize=False) -> str:
    
    matches_found = 0
        
    for design in designs:
        if visualize:
            os.system('cls||clear')
            print(f"Towels:")
            for towel in towels:
                print(color_towel(towel))
            print(f"Design: {color_towel(design)}")
            time.sleep(0.5)
        ways_to_make = num_ways_to_make(design, towels)
        matches_found += 1 if ways_to_make > 0 else 0
    
    return matches_found


def part2(designs, visualize=False) -> int:
    return sum(cache[design] for design in designs)

input_file = sys.argv[1]

with open(input_file) as f:
    lines = f.readlines()
    
    towels = tuple([line.strip() for line in lines[0].split(', ')])
    
    designs = [line.strip() for line in lines[2:]]
    
    print(part1(towels, designs, visualize=False))
    print(part2(designs, visualize=False))

