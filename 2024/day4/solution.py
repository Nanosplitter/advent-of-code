import numpy as np

def part1(board) -> int:
    size = len(board)
    xmas_count = 0
    
    xmas_count += sum([row.count("XMAS") + row.count("SAMX") for row in board])

    board = np.array([list(i.replace("\n", "")) for i in board])
    
    diags = [board[::-1,:].diagonal(i) for i in range(-size,size)]
    diags.extend(board.diagonal(i) for i in range(size,-size,-1))
    diags = ["".join(diag) for diag in [n.tolist() for n in diags]]
    xmas_count += sum([diag.count("XMAS") + diag.count("SAMX") for diag in diags])
        
    board = ["".join(row) for row in np.rot90(board)]
    xmas_count += sum([row.count("XMAS") + row.count("SAMX") for row in board])
    
    return xmas_count

def part2(board) -> int:
    size = len(board)
    xmas_count = 0
    
    for row in range(1, size - 1):
        for col in range(1, size - 1):
            if board[row][col] == "A":
                up_left = board[row - 1][col - 1]
                up_right = board[row - 1][col + 1]
                down_left = board[row + 1][col - 1]
                down_right = board[row + 1][col + 1]
                if sorted([up_left, up_right, down_left, down_right]) == ["M", "M", "S", "S"] and up_left != down_right:
                    xmas_count += 1
    return xmas_count
    
with open("input.txt") as f:
    board = f.readlines()
    print(part1(board))
    print(part2(board))