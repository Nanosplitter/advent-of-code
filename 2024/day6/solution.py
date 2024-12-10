from tqdm import tqdm

class Guard:
    def __init__(self, row, col):
        self.start_position = (row, col)
        self.reset_position()

    def reset_position(self):
        self.direction = 0
        self.position = self.start_position
        self.visited = [(self.position[0], self.position[1], self.direction)]
        self.visited_set = set(self.visited)

    def get_path(self, board):
        self.reset_position()
        board_rows = len(board)
        board_cols = len(board[0])

        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # UP, RIGHT, DOWN, LEFT

        while True:
            delta_row, delta_col = directions[self.direction]
            check_row = self.position[0] + delta_row
            check_col = self.position[1] + delta_col

            if (check_row, check_col, self.direction) in self.visited_set:
                return list(self.visited_set), "LOOP"

            if check_row < 0 or check_row >= board_rows or check_col < 0 or check_col >= board_cols:
                return list(self.visited_set), "OUT OF BOUNDS"

            if board[check_row][check_col] == "#":
                self.direction = (self.direction + 1) % 4
                continue

            self.visited_set.add((check_row, check_col, self.direction))
            self.position = (check_row, check_col)
    

def part1(board) -> int:
    for i, row in enumerate(board):
        if "^" in row:
            guard = Guard(i, row.index("^"))
            break
            
    path, _ = guard.get_path(board)
    
    unique_locations = set([(x, y) for x, y, _ in path])
    
    return len(unique_locations)

def part2(board) -> int:
    for i, row in enumerate(board):
        if "^" in row:
            guard = Guard(i, row.index("^"))
            break
    
    loop_spots = []
    
    total_checks = sum(row.count('.') for row in board)
    
    with tqdm(total=total_checks, desc="Progress") as pbar:
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == ".":
                    board[row][col] = "#"
                    _, status = guard.get_path(board)
                    if status == "LOOP":
                        loop_spots.append((row, col))
                    board[row][col] = "."
                    
                    pbar.update(1)
                
    print()
    return len(set(loop_spots))
    
    
with open("input.txt") as f:
    board = [list(row.strip()) for row in f.readlines()]
    
    print(part1(board))
    print(part2(board))