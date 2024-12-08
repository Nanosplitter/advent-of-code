dirs = ["UP", "RIGHT", "DOWN", "LEFT"]

class Guard:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.direction = 0
        self.visited = [(row, col, 0)]
    
    def __repr__(self):
        return f"({self.row}, {self.col})"

    def get_path(self, board):
        while True:
            check_row = self.row
            check_col = self.col
            
            if dirs[self.direction] == "UP":
                check_row -= 1
            elif dirs[self.direction] == "DOWN":
                check_row += 1
            elif dirs[self.direction] == "LEFT":
                check_col -= 1
            elif dirs[self.direction] == "RIGHT":
                check_col += 1
                
            if (check_row, check_col, self.direction) in self.visited:
                return self.visited, "LOOP"
        
            if check_row < 0 or check_row >= len(board) or check_col < 0 or check_col >= len(board[0]):
                return self.visited, "OUT OF BOUNDS"
            
            if board[check_row][check_col] == "#":
                self.direction = (self.direction + 1) % 4
                continue
            
            self.visited.append((check_row, check_col, self.direction))
            self.row = check_row
            self.col = check_col
            
    


def part1(board) -> int:
    for row in board:
        if "^" in row:
            guard = Guard(board.index(row), row.index("^"))
            break
            
    path, _ = guard.get_path(board)
    
    unique_locations = set([(x, y) for x, y, _ in path])
    
    return len(unique_locations)

def part2(board) -> int:
    for row in board:
        if "^" in row:
            guard = Guard(board.index(row), row.index("^"))
            break
    
    for 
    
    return 0
    
    
    
with open("input.txt") as f:
    board = f.readlines()
    
    board = [list(row.strip()) for row in board]
    
    print(part1(board))
    #print(part2(board))