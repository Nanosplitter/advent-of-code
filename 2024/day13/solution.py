def find_min_tokens(aX, aY, bX, bY, targetX, targetY) -> int:
    D = (aX * bY) - (aY * bX)
    
    a = ((targetX * bY) - (targetY * bX)) / D
    b = ((-targetX * aY) + (targetY * aX)) / D

    if a.is_integer() and b.is_integer():
        return int((a * 3) + b)
    
    return 0

def part1(machines) -> int:
    return sum(find_min_tokens(aX, aY, bX, bY, targetX, targetY) for aX, aY, bX, bY, targetX, targetY in machines)
    

def part2(instructions) -> int:
    return sum(find_min_tokens(aX, aY, bX, bY, targetX + 10000000000000, targetY + 10000000000000) for aX, aY, bX, bY, targetX, targetY in machines)

with open("2024/day13/input.txt") as f:
    instructions = [line.strip() for line in f.readlines() if line.strip() != ""]
    instructions = [instructions[i:i+3] for i in range(0, len(instructions), 3)]

    machines = []

    for group in instructions:
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
    print(part2(machines))

