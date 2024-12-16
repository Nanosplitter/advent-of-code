from collections import defaultdict
from itertools import groupby
import sys
import time
import os

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

DIR_NAMES = {UP: "UP", DOWN: "DOWN", LEFT: "LEFT", RIGHT: "RIGHT"}


class Node:
    def __init__(self, position, symbol):
        self.position = position
        self.symbol = symbol
        
    def find_neighbors(self, board):
        neighbors = {UP: None, DOWN: None, LEFT: None, RIGHT: None}
        
        for direction in [UP, DOWN, LEFT, RIGHT]:
            check_position = (self.position[0] + direction[0], self.position[1] + direction[1])
            check_node = board.nodes[check_position]
            
            if check_node is not None and check_node.symbol != "#":
                neighbors[direction] = check_node
        
        return neighbors
        
    
    def __str__(self):
        return f"Node({self.symbol}, {self.position})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.position == other.position
    
    def __hash__(self):
        return hash(self.position)
    
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.start_position = None
        self.end_position = None
        self.nodes = defaultdict(lambda: None)
    
    def set_node(self, node):
        self.nodes[node.position] = node
    
    def set_start_position(self, position):
        self.start_position = position
    
    def set_end_position(self, position):
        self.end_position = position
    
    def find_shortest_path(self):
        cost_up, path_up = find_shortest_path(self, self.start_position, self.end_position, UP)
        cost_right, path_right = find_shortest_path(self, self.start_position, self.end_position, RIGHT)
        
        print(f"Cost up: {cost_up}, path: {path_up}")
        print(f"Cost right: {cost_right}, path: {path_right}")
        
        if cost_up < cost_right:
            cost = cost_up
            path = path_up
        else:
            cost = cost_right
            path = path_right
        
        for position in path:
            node = self.nodes[position]
            node.symbol = "*"
        print(self)
        return cost
        
    def __str__(self):
        res = ""
        for row in range(self.height):
            for col in range(self.width):
                node = self.nodes[(row, col)]
                if node is not None:
                    if node.symbol == "E":
                        res += "\033[91mE\033[0m"  # Red
                    elif node.symbol == "#":
                        res += "#"  # Yellow
                    elif node.symbol == "S":
                        res += "\033[92mS\033[0m"
                    elif node.symbol == "[":
                        res += "\033[93m[\033[0m"  # Blue
                    elif node.symbol == "]":
                        res += "\033[93m]\033[0m"  # Magenta
                    elif node.symbol == "*":
                        res += "\033[95m*\033[0m"
                    elif node.symbol == ".":
                        res += " "
                    else:
                        res += node.symbol
                else:
                    res += " "
            res += "\n"
        return res
    
    def __repr__(self):
        return self.__str__()

def find_shortest_path(board, start_position, end_position, curr_direction, visited=None):
    if visited is None:
        visited = set()
    if start_position in visited:
        return 1000000000, []
    if start_position == end_position:
        return 0, [start_position]
    visited.add(start_position)
    curr_node = board.nodes[start_position]
    neighbors = curr_node.find_neighbors(board)
    best_cost = 1000000000
    best_path = []
    for dir in neighbors:
        neighbor = neighbors[dir]
        if neighbor is None:
            continue
        cost = 1 if dir == curr_direction else 1001
        total_cost, path = find_shortest_path(
            board, neighbor.position, end_position, dir, visited.copy()
        )
        total_cost += cost
        if total_cost < best_cost:
            best_cost = total_cost
            best_path = [start_position] + path
    return best_cost, best_path
        
    
def part1(instructions) -> int:
    board = Board(len(instructions[0]), len(instructions))
    
    for row in range(len(instructions)):
        for col in range(len(instructions[row])):
            board.set_node(Node((row, col), instructions[row][col]))
            
            if instructions[row][col] == "S":
                board.set_start_position((row, col))
            elif instructions[row][col] == "E":
                board.set_end_position((row, col))
    
    print(board)
    return board.find_shortest_path()
    

def part2(instructions) -> int:
    return 0
    

if len(sys.argv) < 2:
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    instructions = [line.strip() for line in f.readlines()]

    print(part1(instructions))
    #print(part2(instructions))