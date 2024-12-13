def find_min_tokens(aX, aY, bX, bY, targetX, targetY) -> int:
    valid_solutions = []
    
    for check_a in range(100):
        for check_b in range(100):
            if aX * check_a + bX * check_b == targetX and aY * check_a + bY * check_b == targetY:
                valid_solutions.append((check_a, check_b))
    
    if len(valid_solutions) == 0:
        return 0
        
    return min([(a * 3) + b for a, b in valid_solutions])

def part1(machines) -> int:
    return sum(find_min_tokens(aX, aY, bX, bY, targetX, targetY) for aX, aY, bX, bY, targetX, targetY in machines)
    

def part2(instructions) -> int:
    return 0

with open("2024/day13/ex_input.txt") as f:
    instructions = [line.strip() for line in f.readlines() if line.strip() != ""]
    instructions = [instructions[i:i+3] for i in range(0, len(instructions), 3)]

    machines = []

    for group in instructions:
        #print(group)
        aGroup = group[0].split(":")
        bGroup = group[1].split(":")
        targetGroup = group[2].split(":")
        
        aX = int(aGroup[1].split(",")[0].split("+")[1])
        aY = int(aGroup[1].split(",")[1].split("+")[1])
        
        bX = int(bGroup[1].split(",")[0].split("+")[1])
        bY = int(bGroup[1].split(",")[1].split("+")[1])
        
        targetX = int(targetGroup[1].split(",")[0].split("=")[1])
        targetY = int(targetGroup[1].split(",")[1].split("=")[1])
        
        machines.append((aX, aY, bX, bY, targetX, targetY))

    print(part1(machines))

    # print(part1(instructions))
    # print(part2(instructions))

