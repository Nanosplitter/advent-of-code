def get_trail_score(head_row, head_col, map):
    if map[head_row][head_col] == '9':
        return {(head_row, head_col)}
    else:
        reachable_nines = set()
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for direction in directions:
            check_row = head_row + direction[0]
            check_col = head_col + direction[1]
            if 0 <= check_row < len(map) and 0 <= check_col < len(map[0]):
                next_value = str(int(map[head_row][head_col]) + 1)
                if map[check_row][check_col] == next_value:
                    reachable_nines.update(get_trail_score(check_row, check_col, map))
        return reachable_nines
        
def get_trail_rating(head_row, head_col, map):
    if map[head_row][head_col] == '9':
        return 1
    else:
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        dir_ratings = 0
        for direction in directions:
            check_row = head_row + direction[0]
            check_col = head_col + direction[1]
            if 0 <= check_row < len(map) and 0 <= check_col < len(map[0]):
                next_value = str(int(map[head_row][head_col]) + 1)
                if map[check_row][check_col] == next_value:
                    dir_ratings += get_trail_rating(check_row, check_col, map)
        return dir_ratings

def part1(instructions) -> int:
    total_score = 0
    for row_index, row in enumerate(instructions):
        for col_index, col in enumerate(row):
            if col == '0':
                score = len(get_trail_score(row_index, col_index, instructions))
                total_score += score
    return total_score

def part2(instructions) -> int:
    total_rating = 0
    for row_index, row in enumerate(instructions):
        for col_index, col in enumerate(row):
            if col == '0':
                rating = get_trail_rating(row_index, col_index, instructions)
                total_rating += rating
    return total_rating

with open("2024/day10/input.txt") as f:
    instructions = [line.strip() for line in f.readlines()]
    
    print(part1(instructions))
    print(part2(instructions))
