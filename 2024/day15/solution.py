from collections import defaultdict
from itertools import groupby
import sys

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
    
    def add_partner(self, partner):
        self.partner = partner
        
    def can_move_freely(self, direction, board):
        check_position = (self.position[0] + direction[0], self.position[1] + direction[1])
        check_node = board.nodes[check_position]
        
        if check_node is None:
            return True
        
        return False
    
    def attempt_move(self, direction, board, called_from_partner=False):
        if not self.is_moveable:
            return False
        
        check_position = (self.position[0] + direction[0], self.position[1] + direction[1])
        check_node = board.nodes[check_position]
        
        print("------------------------------")
        print(f"Checking {self.symbol} at {self.position} moving to {check_position}...")
        print(f"Check node: {check_node}")
        print(f"Called from partner: {called_from_partner}")
        
        if check_node is not None and not check_node.is_moveable:
            #print("Node is not moveable")
            return False
        
        if direction in [UP, DOWN] and self.partner is not None and not called_from_partner:
            if (check_node is None or board.nodes[check_position].attempt_move(direction, board)) and self.partner.attempt_move(direction, board, called_from_partner=True):
                board.update_node(self.position, None)
                board.update_node(check_position, self)
                self.position = check_position
                return True
            else:
                return False
        
       
        if check_node is None or board.nodes[check_position].attempt_move(direction, board):
            board.update_node(self.position, None)
            board.update_node(check_position, self)
            self.position = check_position
            return True
                
            
        
        return False
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
        self.robot.attempt_move(direction, self)
        
    def __str__(self):
        res = ""
        for row in range(self.height):
            for col in range(self.width):
                node = self.nodes[(row, col)]
                res += node.symbol if node is not None else "."
            res += "\n"
            
        return res
    
    def __repr__(self):
        return self.__str__()
    
def part1(instructions) -> int:
    #print(instructions)
    instructions = [list(group) for k, group in groupby(instructions, lambda x: x.strip() == "") if not k]
    
    moves_lines = instructions[1]
    
    board = Board(len(instructions[0][0].strip()), len(instructions[0]))
    
    
    
    for row, line in enumerate(instructions[0]):
        #print(line.strip())
        if line.strip() == "":
            break
        
        for col, symbol in enumerate(line.strip()):
            #print(row, col, symbol)
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
    
    print(board)
    #print(board.nodes)
        
    #print("Initial board:")
    #print(board)
    for i in range(len(moves)):
        move = moves[i]
        direction = DIRS_MAP[move]
        board.attempt_move(direction)
        #print(f"Board after move {i + 1}:")
        #print(board)
    
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
    
    #print(board)
                
    
    moves = []
    
    for line in moves_lines:
        moves.extend(line.strip())
    
    for i in range(len(moves)):
        move = moves[i]
        direction = DIRS_MAP[move]
        board.attempt_move(direction)
        print(f"Board after move {i + 1}:")
        with open("board_output.txt", "a") as f:
            f.write(f"Board after move {i + 1} {move}:\n")
            f.write(str(board))
            f.write("\n")
        print(board)
    
    print(board)
    gps_total = 0
    
    for node in board.nodes.values():
        if node is not None and node.symbol == "[":
            gps_total += (100 * node.position[0]) + node.position[1]
    
    return gps_total

if len(sys.argv) < 2:
    print("Usage: python solution.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    instructions = f.readlines()

    print(part1(instructions))
    print(part2(instructions))