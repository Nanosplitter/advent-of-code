UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
UP_LEFT = (-1, -1)
UP_RIGHT = (-1, 1)
DOWN_LEFT = (1, -1)
DOWN_RIGHT = (1, 1)

MANHATTAN_DIRS = [UP, DOWN, LEFT, RIGHT]
ALL_DIRS = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
CORNER_DIRS = [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]

class Node:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.friends = {
            UP: None,
            DOWN: None,
            LEFT: None,
            RIGHT: None,
            UP_LEFT: None,
            UP_RIGHT: None,
            DOWN_LEFT: None,
            DOWN_RIGHT: None
        }
    
    def add_friend(self, friend, dir):
        self.friends[dir] = friend
    
    def get_num_friends(self):
        friends = 0
        for dir in MANHATTAN_DIRS:
            if self.friends[dir] is not None:
                friends += 1
        return friends
    
    def get_num_corners(self):
        # no friends means 4 corners
        
        corners = 0
        
        if self.get_num_friends() == 0:
            return 4
        
        if (self.friends[UP] and self.friends[DOWN]) and (self.friends[LEFT] is None and self.friends[RIGHT] is None):
            return 0
        
        if self.friends[LEFT] and self.friends[RIGHT] and (self.friends[UP] is None and self.friends[DOWN] is None):
            return 0
        
        if self.friends[UP] and self.friends[LEFT]:
            corners += self.friends[UP_LEFT] is None
        
        if self.friends[UP] and self.friends[RIGHT]:
            corners += self.friends[UP_RIGHT] is None
            
        if self.friends[DOWN] and self.friends[LEFT]:
            corners += self.friends[DOWN_LEFT] is None
            
        if self.friends[DOWN] and self.friends[RIGHT]:
            corners += self.friends[DOWN_RIGHT] is None
            
        return corners
        
        
        
        
        
    
    def __str__(self):
        return f"Node({self.row}, {self.col}, {self.value})"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col and self.value == other.value
    
    def __hash__(self):
        return hash((self.row, self.col, self.value))

class Region:
    def __init__(self):
        self.nodes = set()
    
    def __str__(self):
        return f"Region({self.nodes}, {self.get_area()}, {self.get_perimeter()}, {self.get_price()})"
    
    def __repr__(self):
        return self.__str__()

    def get_perimeter(self):
        perimeter = 0
        for node in self.nodes:
            perimeter += 4 - node.get_num_friends()
        
        return perimeter
    
    def get_area(self):
        return len(self.nodes)
    
    def get_price(self):
        return self.get_perimeter() * self.get_area()
    
    def get_corners(self):
        corners = 0
        for node in self.nodes:
            corners += node.get_num_corners()
        return corners


def get_region(row, col, grid, region):
    #print(f"Checking {row}, {col} | current perimeter: {region.perimeter} | current area: {region.area}")
    
    node = Node(row, col, grid[row][col])
    
    if node in region.nodes:
        #print(f"Already checked {node}")
        return region
    
    region.nodes.add(node)
    
    for direction in ALL_DIRS:
        check_row = row + direction[0]
        check_col = col + direction[1]
        if 0 <= check_row < len(grid) and 0 <= check_col < len(grid[0]):
            if grid[check_row][check_col] == grid[row][col] and (check_row, check_col) not in region.nodes:
                node.add_friend(Node(check_row, check_col, grid[check_row][check_col]), direction)
                get_region(check_row, check_col, grid, region)
    return region


def part1(grid) -> int:
    #print(get_region(0, 0, grid))
    
    all_nodes = []
    regions = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if Node(row, col, grid[row][col]) not in all_nodes:
                region = Region()
                get_region(row, col, grid, region)
                regions.append(region)
                all_nodes += list(region.nodes)
                
    
    total_price = 0
    for region in regions:
        total_price += region.get_price()
    
    return total_price

def part2(grid) -> int:
    all_nodes = []
    regions = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if Node(row, col, grid[row][col]) not in all_nodes:
                region = Region()
                get_region(row, col, grid, region)
                regions.append(region)
                all_nodes += list(region.nodes)
    
    for region in regions:
        print(region, "| corners:", region.get_corners())
    return 0

with open("2024/day12/simple_input.txt") as f:
    instructions = [line.strip() for line in f.readlines()]

    #print(part1(instructions))
    print(part2(instructions))
