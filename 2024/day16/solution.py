from collections import defaultdict
import sys
import heapq

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
        cost, path, num_straights, num_turns = find_shortest_path(self)
        return cost, path, num_straights, num_turns
        
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


def find_shortest_paths(board):
    end = board.end_position
    queue = []
    heapq.heappush(queue, (0, board.start_position, RIGHT))
    visited = {}
    parent_nodes = defaultdict(set)
    min_cost_per_node = defaultdict(lambda: float('inf'))
    min_cost = None

    while queue:
        cost, position, curr_direction = heapq.heappop(queue)

        if min_cost is not None and cost > min_cost:
            break

        if position == end:
            if min_cost is None:
                min_cost = cost
            continue

        if (position, curr_direction) in visited and visited[(position, curr_direction)] <= cost:
            continue

        visited[(position, curr_direction)] = cost

        curr_node = board.nodes[position]
        neighbors = curr_node.find_neighbors(board)

        for dir, neighbor in neighbors.items():
            if neighbor is None:
                continue

            turn_cost = 1 if curr_direction == dir else 1001
            new_cost = cost + turn_cost

            neighbor_pos = neighbor.position
            neighbor_dir = dir

            if new_cost < min_cost_per_node[(neighbor_pos, neighbor_dir)]:
                parent_nodes[(neighbor_pos, neighbor_dir)] = {(position, curr_direction)}
                min_cost_per_node[(neighbor_pos, neighbor_dir)] = new_cost
                heapq.heappush(queue, (new_cost, neighbor_pos, neighbor_dir))
                
            elif new_cost == min_cost_per_node[(neighbor_pos, neighbor_dir)]:
                parent_nodes[(neighbor_pos, neighbor_dir)].add((position, curr_direction))
                heapq.heappush(queue, (new_cost, neighbor_pos, neighbor_dir))

    end_directions = [
        (end, dir) for dir in [UP, DOWN, LEFT, RIGHT]
        if min_cost_per_node[(end, dir)] == min_cost
    ]

    if not end_directions:
        return float('inf'), set()

    nodes_in_best_paths = set()
    processed = set()
    stack = end_directions.copy()

    while stack:
        current_pos, current_dir = stack.pop()
        if (current_pos, current_dir) in processed:
            continue
        processed.add((current_pos, current_dir))
        nodes_in_best_paths.add(current_pos)
        for parent_pos, parent_dir in parent_nodes[(current_pos, current_dir)]:
            stack.append((parent_pos, parent_dir))

    return min_cost, nodes_in_best_paths
    

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
                
    min_cost, nodes_in_best_paths = find_shortest_paths(board)
    
    for row in range(board.height):
        for col in range(board.width):
            if (row, col) in nodes_in_best_paths:
                node = board.nodes[(row, col)]
                if node.symbol == ".":
                    node.symbol = "*"
    print(board)
    print(f"Minimum Cost: {min_cost}")
    print(f"Number of nodes in best paths: {len(nodes_in_best_paths)}")