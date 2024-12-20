from collections import defaultdict, Counter
import os
import sys
import time

from termcolor import colored

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

def print_board(board, nodes_to_highlight={}):
    res = ""
    for row in range(board.height):
        print(res)
        res = ""
        for col in range(board.width):
            node = board.nodes[(row, col)]
            if node is not None: 
                if node.symbol == "S":
                    res += colored("S ", 'white', 'on_green')
                elif node.symbol == "E":
                    res += colored("E ", 'white', 'on_red')
                elif node in nodes_to_highlight:
                    res += colored("  ", 'white', nodes_to_highlight[node])
                elif node.symbol == "#":
                    res += colored("  ", 'white', 'on_black')
                else:
                    res += "  "                
    print(res)

class Node:
    def __init__(self, position, symbol):
        self.position = position
        self.symbol = symbol
        self.dist_from_start = None
        self.neighbors = []
        
    def find_neighbors(self, board):
        if len(self.neighbors) > 0:
            return self.neighbors
        
        neighbors = {UP: None, DOWN: None, LEFT: None, RIGHT: None}
        
        for direction in [UP, DOWN, LEFT, RIGHT]:
            check_position = (self.position[0] + direction[0], self.position[1] + direction[1])
            if check_position in board.nodes:
                check_node = board.nodes[check_position]
                if check_node is not None and check_node.symbol != "#":
                    neighbors[direction] = check_node
        
        self.neighbors = neighbors
        return neighbors
    
    def __str__(self):
        return f"Node({self.symbol}, {self.position})"
    
    def __repr__(self):
        return self.__str__()
    
    
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.start_position = None
        self.end_position = None
        self.nodes = defaultdict(None)
    
    def set_node(self, node):
        self.nodes[node.position] = node
    
    def set_start_position(self, position):
        self.start_position = position
        self.nodes[position].symbol = "S"
    
    def set_end_position(self, position):
        self.end_position = position
        self.nodes[position].symbol = "E"
    
    def find_path(self):
        path = []
        current_node = self.nodes[self.start_position]
        while current_node.position != self.end_position:
            current_node.dist_from_start = len(path)
            path.append(current_node)
            for _, neighbor in current_node.find_neighbors(self).items():
                if neighbor is not None and neighbor.dist_from_start is None:
                    current_node = neighbor
                    break
                
        current_node.dist_from_start = len(path)
        path.append(current_node)
        return path

def get_all_shortcuts(path, max_shortcut_length):
    shortcuts = []
    
    
    
    for node in path:
        best_shortcut = 0
        nodes_to_highlight = defaultdict(str)
        nodes_to_highlight[node] = 'on_blue'
        for target_node in path:
            distance = abs(node.position[0] - target_node.position[0]) + abs(node.position[1] - target_node.position[1])
            if distance <= max_shortcut_length and target_node.dist_from_start > node.dist_from_start + distance:
                nodes_to_highlight[target_node] = 'on_white'
                
                cost_save = target_node.dist_from_start - node.dist_from_start - distance
                best_shortcut = max(best_shortcut, cost_save)
                shortcuts.append(cost_save)
        os.system('cls||clear')
        print_board(board, nodes_to_highlight)
        print(f"Best shortcut saves {best_shortcut} steps.")
        time.sleep(0.5)
    
    return sum([shortcut[1] for shortcut in Counter(shortcuts).items() if shortcut[0] >= 100])

def part1(path):
    return get_all_shortcuts(path, 2)

def part2(path):
    return get_all_shortcuts(path, 20)
    
if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            sys.exit(1)

        input_file = sys.argv[1]

        with open(input_file) as f:
            instructions = [line.strip() for line in f.readlines()]

            board = Board(len(instructions[0]), len(instructions))
            for row in range(len(instructions)):
                for col in range(len(instructions[row])):
                    board.set_node(Node((row, col), instructions[row][col]))
                    if instructions[row][col] == "S":
                        board.set_start_position((row, col))
                    elif instructions[row][col] == "E":
                        board.set_end_position((row, col))
            
            
            path = board.find_path()
            
            print_board(board)
            
            #print(part1(path))
            print(part2(path))
    except KeyboardInterrupt:
        print("Execution interrupted by user.")
        sys.exit(1)