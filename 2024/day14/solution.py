import sys
from functools import reduce
from operator import mul

class Robot:
    def __init__(self, position, velocity, board_width, board_height):
        self.position = position
        self.velocity = velocity
        self.board_width = board_width
        self.board_height = board_height
        
    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        if self.position[0] < 0 or self.position[0] >= self.board_width:
            self.position[0] = self.position[0] % self.board_width
        if self.position[1] < 0 or self.position[1] >= self.board_height:
            self.position[1] = self.position[1] % self.board_height

class Board:
    def __init__(self, width, height, robots=[]):
        self.width = width
        self.height = height
        self.robots = robots
    
    def move(self):
        for robot in self.robots:
            robot.move()
            
    def add_robot(self, position, velocity):
        self.robots.append(Robot(position, velocity, self.width, self.height))
        
    def get_robots_in_all_quadrants(self):
        quadrants = [[], [], [], []]
        for robot in self.robots:
            if robot.position[0] == self.width // 2 or robot.position[1] == self.height // 2:
                continue
            
            if robot.position[0] < self.width / 2 and robot.position[1] < self.height / 2:
                quadrants[0].append(robot)
            elif robot.position[0] >= self.width / 2 and robot.position[1] < self.height / 2:
                quadrants[1].append(robot)
            elif robot.position[0] < self.width / 2 and robot.position[1] >= self.height / 2:
                quadrants[2].append(robot)
            else:
                quadrants[3].append(robot)
                
        return quadrants
        
    def print_quadrants(self):
        quadrants = self.get_robots_in_all_quadrants()
        board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for i, quadrant in enumerate(quadrants):
            for robot in quadrant:
                board[robot.position[1]][robot.position[0]] += 1
        
        for row in range(self.height):
            for col in range(self.width):
                if row == self.height // 2 or col == self.width // 2:
                    board[row][col] = " "
        
        return "\n".join(["".join([str(cell) if cell != 0 else "." for cell in row]) for row in board])
        
    
    def __str__(self):
        board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for robot in self.robots:
            board[robot.position[1]][robot.position[0]] = "#"
                
            
        return "\n".join(["".join([str(cell) if cell != 0 else "." for cell in row]) for row in board])
    
    def __repr__(self):
        return self.__str__()

    

def part1(board) -> int:
    for _ in range(100):
        board.move()
    quadrants = [len(q) for q in board.get_robots_in_all_quadrants()]
    
    return reduce(mul, quadrants, 1)

def part2(board) -> int:
    with open(f"board.txt", "w") as f:
        for i in range(10):
            board.move()
            f.write("state " + str(i) + "\n")
            f.write(str(board))
            f.write("\n")

if len(sys.argv) < 2:
    print("Usage: python solution.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    instructions = f.readlines()
    board_width, board_height = [int(x) for x in instructions[0].split(",")]
    board = Board(board_width, board_height)
    
    for line in instructions[1:]:
        position = [int(x) for x in line.split("p=")[1].split(" ")[0].split(",")]
        velocity = [int(x) for x in line.split("v=")[1].split(" ")[0].split(",")]
        
        board.add_robot(position, velocity)

    print(part1(board))
    print(part2(board))
