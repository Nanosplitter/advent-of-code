from collections import defaultdict, Counter
from math import inf
import sys

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

DIR_NAMES = {UP: "UP", DOWN: "DOWN", LEFT: "LEFT", RIGHT: "RIGHT"}

def node_default():
    return None

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
        return f"Node({self.symbol}, {self.position}, {self.dist_from_start})"
    
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
        self.nodes = defaultdict(node_default)
    
    def set_node(self, node):
        self.nodes[node.position] = node
    
    def set_start_position(self, position):
        self.start_position = position
        self.nodes[position].symbol = "S"
    
    def set_end_position(self, position):
        self.end_position = position
        self.nodes[position].symbol = "E"
        
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
                        res += "\033[93m*\033[0m"
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
    
    def find_path(self):
        path = []
        current_node = self.nodes[self.start_position]
        while current_node.position != self.end_position:
            current_node.dist_from_start = len(path)
            path.append(current_node)
            for direction, neighbor in current_node.find_neighbors(self).items():
                if neighbor is not None and neighbor.dist_from_start is None:
                    current_node = neighbor
                    break
                
        current_node.dist_from_start = len(path)
        path.append(current_node)
        return path

def part1(board):
    
    path = board.find_path()
    
    base_cost = board.nodes[board.end_position].dist_from_start
    
    shortcuts = []
    
    counter = 0
    
    for node in path:
        counter += 1
        print(f"[{counter}/{len(path)}] {node.position}")
        for direction1 in [UP, DOWN, LEFT, RIGHT]:
            for direction2 in [UP, DOWN, LEFT, RIGHT]:
                next_pos = (
                    node.position[0] + direction1[0] + direction2[0],
                    node.position[1] + direction1[1] + direction2[1]
                )
                if next_pos in board.nodes and board.nodes[next_pos] in path and board.nodes[next_pos].dist_from_start > node.dist_from_start + 2:
                    shortcuts.append(board.nodes[next_pos].dist_from_start - node.dist_from_start - 2)
    
    shortcuts = sorted(shortcuts, reverse=True)
    
    shortcut_counter = Counter(shortcuts)
    
    shortcut_counter = sorted(shortcut_counter.items(), key=lambda x: x[0], reverse=True)
    
    return sum([shortcut[1] for shortcut in shortcut_counter if shortcut[0] >= 100])
    
                
    #print(board)
    
    return 0

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            sys.exit(1)

        input_file = sys.argv[1]

        with open(input_file) as f:
            instructions = [line.strip() for line in f.readlines()]

            sys.setrecursionlimit(1000000)

            board = Board(len(instructions[0]), len(instructions))
            for row in range(len(instructions)):
                for col in range(len(instructions[row])):
                    board.set_node(Node((row, col), instructions[row][col]))
                    if instructions[row][col] == "S":
                        board.set_start_position((row, col))
                    elif instructions[row][col] == "E":
                        board.set_end_position((row, col))
            
            print(part1(board))
    except KeyboardInterrupt:
        print("Execution interrupted by user.")
        sys.exit(1)