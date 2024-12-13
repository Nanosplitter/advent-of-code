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
        corners = 0

        if self.get_num_friends() == 0:
            return 4

        if (self.friends[UP] and self.friends[DOWN]) and (self.friends[LEFT] is None and self.friends[RIGHT] is None):
            return 0

        if self.friends[LEFT] and self.friends[RIGHT] and (self.friends[UP] is None and self.friends[DOWN] is None):
            return 0

        if self.friends[UP_LEFT] is None:
            if (self.friends[UP] is None and self.friends[LEFT] is None) or (self.friends[UP] is not None and self.friends[LEFT] is not None):
                corners += 1

        if self.friends[UP_RIGHT] is None:
            if (self.friends[UP] is None and self.friends[RIGHT] is None) or (self.friends[UP] is not None and self.friends[RIGHT] is not None):
                corners += 1

        if self.friends[DOWN_LEFT] is None:
            if (self.friends[DOWN] is None and self.friends[LEFT] is None) or (self.friends[DOWN] is not None and self.friends[LEFT] is not None):
                corners += 1

        if self.friends[DOWN_RIGHT] is None:
            if (self.friends[DOWN] is None and self.friends[RIGHT] is None) or (self.friends[DOWN] is not None and self.friends[RIGHT] is not None):
                corners += 1
        
        if self.friends[UP_LEFT]:
            if self.friends[UP] is None and self.friends[LEFT] is None:
                corners += 1
        
        if self.friends[UP_RIGHT]:
            if self.friends[UP] is None and self.friends[RIGHT] is None:
                corners += 1
                
        if self.friends[DOWN_LEFT]:
            if self.friends[DOWN] is None and self.friends[LEFT] is None:
                corners += 1
                
        if self.friends[DOWN_RIGHT]:
            if self.friends[DOWN] is None and self.friends[RIGHT] is None:
                corners += 1

        return corners
    
    def __eq__(self, other):
        if other is None:
            return False
        return self.row == other.row and self.col == other.col and self.value == other.value
    
    def __hash__(self):
        return hash((self.row, self.col, self.value))

class Region:
    def __init__(self):
        self.nodes = set()

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
    
    def get_bulk_price(self):
        return self.get_area() * self.get_corners()


def get_region(row, col, grid, region):
    node = Node(row, col, grid[row][col])
    
    if node in region.nodes:
        return region
    
    region.nodes.add(node)
    
    for direction in ALL_DIRS:
        check_row = row + direction[0]
        check_col = col + direction[1]
        if 0 <= check_row < len(grid) and 0 <= check_col < len(grid[0]):
            if grid[check_row][check_col] == grid[row][col] and (check_row, check_col) not in region.nodes:
                node.add_friend(Node(check_row, check_col, grid[check_row][check_col]), direction)
                if direction in MANHATTAN_DIRS:
                    get_region(check_row, check_col, grid, region)
    return region

def get_price(grid, bulk):
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
        if bulk:
            total_price += region.get_bulk_price()
        else:
            total_price += region.get_price()
    
    return total_price

def part1(grid) -> int:
    return get_price(grid, bulk=False)

def part2(grid) -> int:
    return get_price(grid, bulk=True)

with open("2024/day12/ex_input.txt") as f:
    instructions = [line.strip() for line in f.readlines()]

    print(part1(instructions))
    print(part2(instructions))
