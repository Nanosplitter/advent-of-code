from collections import defaultdict
from itertools import groupby
import sys
import time

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

DIRS_MAP = {
    "^": UP,
    "v": DOWN,
    "<": LEFT,
    ">": RIGHT
}

class Node:
    def __init__(self, symbol, position, is_moveable):
        self.symbol = symbol
        self.position = position
        self.is_moveable = is_moveable
        self.partner = None
    
    def __str__(self):
        return f"Node({self.symbol} | {self.position} | {self.is_moveable})"
    
    def __repr__(self):
        return self.__str__()
    
    def __hash__(self):
        return hash(self.position)
    
    def add_partner(self, partner):
        self.partner = partner
        
    def can_move_freely(self, direction, board):
        check_position = (self.position[0] + direction[0], self.position[1] + direction[1])
        check_node = board.nodes[check_position]
        
        if check_node is None:
            return True
        
        return False
    
    def attempt_move(self, direction, board, moving_nodes, called_from_partner=False):
        if not self.is_moveable:
            moving_nodes.clear()
            return False
        
        
        check_position = (self.position[0] + direction[0], self.position[1] + direction[1])
        check_node = board.nodes[check_position]
        
        partner_can_move = True
        
        if direction in [UP, DOWN] and self.partner is not None:
            if not called_from_partner:
                partner_can_move = self.partner.attempt_move(direction, board, moving_nodes, True)
                
                if not partner_can_move:
                    moving_nodes.clear()
                    return False
        
        if check_node is None:
            moving_nodes.append((self, check_position))
            return True
        
        if check_node is not None and not check_node.is_moveable:
            moving_nodes.clear()
            return False

        if not partner_can_move:
            moving_nodes.clear()
            return False
        
        moving_nodes.append((self, check_position))
        return check_node.attempt_move(direction, board, moving_nodes, False) and partner_can_move
    
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.nodes = defaultdict(lambda: None)
        self.robot = None
    
    def add_node(self, node, is_robot=False):
        self.nodes[node.position] = node
        
        if is_robot:
            self.robot = node

    def update_node(self, position, node):
        self.nodes[position] = node
    
    def attempt_move(self, direction):
        moving_nodes = [(self.robot, (self.robot.position[0] + direction[0], self.robot.position[1] + direction[1]))]
        self.robot.attempt_move(direction, self, moving_nodes, False)
        
        for node_instructions in moving_nodes[::-1]:
            new_position = node_instructions[1]
            node = node_instructions[0]
            self.update_node(node.position, None)
            node.position = new_position
            self.update_node(new_position, node)
        
    def __str__(self):
        res = ""
        for row in range(self.height):
            for col in range(self.width):
                node = self.nodes[(row, col)]
                if node is not None:
                    if node.symbol == "@":
                        res += "\033[92m@\033[0m"  # Red
                    elif node.symbol == "O":
                        res += "\033[92mO\033[0m"  # Green
                    elif node.symbol == "#":
                        res += "#"  # Yellow
                    elif node.symbol == "[":
                        res += "\033[93m[\033[0m"  # Blue
                    elif node.symbol == "]":
                        res += "\033[93m]\033[0m"  # Magenta
                    else:
                        res += node.symbol
                else:
                    res += " "
            res += "\n"
        return res
    
    def __repr__(self):
        return self.__str__()
    
def part1(instructions) -> int:
    instructions = [list(group) for k, group in groupby(instructions, lambda x: x.strip() == "") if not k]
    
    moves_lines = instructions[1]
    
    board = Board(len(instructions[0][0].strip()), len(instructions[0]))
    
    for row, line in enumerate(instructions[0]):
        if line.strip() == "":
            break
        
        for col, symbol in enumerate(line.strip()):
            robot = False
            can_move = False
            
            if symbol in ["@", "O"]:
                can_move = True
                robot = symbol == "@"
            
            if symbol != ".":
                board.add_node(Node(symbol, (row, col), can_move), robot)
    
    moves = []
    
    for line in moves_lines:
        moves.extend(line.strip())

    for i in range(len(moves)):
        move = moves[i]
        direction = DIRS_MAP[move]
        board.attempt_move(direction)
    
    gps_total = 0
    
    for node in board.nodes.values():
        if node is not None and node.symbol == "O":
            gps_total += (100 * node.position[0]) + node.position[1]
    
    return gps_total

def part2(instructions) -> int:
    instructions = [list(group) for k, group in groupby(instructions, lambda x: x.strip() == "") if not k]
    
    moves_lines = instructions[1]
    
    board = Board(len(instructions[0][0].strip()) * 2, len(instructions[0]))
    
    for row, line in enumerate(instructions[0]):
        if line.strip() == "":
            break
        
        line = line.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
        
        for col, symbol in enumerate(line.strip()):
            robot = False
            can_move = False
            
            if symbol in ["@", "[",]:
                can_move = True
                robot = symbol == "@"
            
            if symbol not in [".", "]"]:
                node = Node(symbol, (row, col), can_move)
                if symbol == "[":
                    partner_node = Node("]", (row, col + 1), can_move)
                    node.add_partner(partner_node)
                    partner_node.add_partner(node)
                    board.add_node(partner_node, robot)
                    
                board.add_node(node, robot)
    
    moves = []
    
    for line in moves_lines:
        moves.extend(line.strip())
    
    for i in range(len(moves)):
        move = moves[i]
        direction = DIRS_MAP[move]
        board.attempt_move(direction)
        
        print(board)
        time.sleep(0.01)

    gps_total = 0
    
    for node in board.nodes.values():
        if node is not None and node.symbol == "[":
            gps_total += (100 * node.position[0]) + node.position[1]
    
    return gps_total

if len(sys.argv) < 2:
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    instructions = f.readlines()

    print(part1(instructions))
    print(part2(instructions))