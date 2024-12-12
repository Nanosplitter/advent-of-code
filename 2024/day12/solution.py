UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


class Node:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.friends = {
            UP: None,
            DOWN: None,
            LEFT: None,
            RIGHT: None
        }
    
    def add_friend(self, friend, dir):
        self.friends[dir] = friend
    
    def get_num_friends(self):
        return len([friend for friend in self.friends.values() if friend is not None])
    
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


def get_region(row, col, grid, region):
    #print(f"Checking {row}, {col} | current perimeter: {region.perimeter} | current area: {region.area}")
    
    directions = [UP, DOWN, LEFT, RIGHT]
    node = Node(row, col, grid[row][col])
    
    if node in region.nodes:
        #print(f"Already checked {node}")
        return region
    
    region.nodes.add(node)
    
    for direction in directions:
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

def part2(instructions) -> int:
    return 0

with open("ex_input.txt") as f:
    instructions = [line.strip() for line in f.readlines()]

    print(part1(instructions))
    print(part2(instructions))
