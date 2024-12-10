from collections import Counter

def part1(lines):
    left = []
    right = []

    for line in lines:
        left_num, right_num = [int(i) for i in line.split()]
        left.append(left_num)
        right.append(right_num)

    left = sorted(left)
    right = sorted(right)

    dist = sum([abs(left[i] - right[i]) for i in range(len(left))])

    return dist

def part2(lines):
    left = []
    right = []

    for line in lines:
        left_num, right_num = [int(i) for i in line.split()]
        left.append(left_num)
        right.append(right_num)

    counter = Counter(right)

    score = 0
    for num in left:
        score += num * counter[num]

    return score
    


with open("input.txt") as f:
    board = f.readlines()
    
    print(part1(board))
    print(part2(board))