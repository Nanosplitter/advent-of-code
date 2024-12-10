def can_reach_target(target, total, values, conc_allowed) -> bool:
    if len(values) == 0:
        return target == total
    
    multiply_path, add_path, conc_path = False, False, False
    
    if total * values[0] <= target:
        if total == 0:
            total = 1
        multiply_path = can_reach_target(target, total * values[0], values[1:], conc_allowed)
    
    if target >= values[0]:
        add_path = can_reach_target(target, total + values[0], values[1:], conc_allowed)
    
    if target >= int(str(total) + str(values[0])) and conc_allowed:
        conc_path = can_reach_target(target, int(str(total) + str(values[0])), values[1:], conc_allowed)
    
    return multiply_path or add_path or conc_path
         
def get_total_passing(instructions, conc_allowed=False):
    total = 0
    for instruction in instructions:
        target, values = instruction.split(":")
        target = int(target)
        values = list(map(int, values.split()))
        
        if can_reach_target(target, 1, values, conc_allowed):
            total += target
    
    return total

def part1(instructions) -> int:
    return get_total_passing(instructions)

def part2(instructions) -> int:
    return get_total_passing(instructions, conc_allowed=True)

with open("input.txt") as f:
    instructions = f.readlines()

    print(part1(instructions))
    print(part2(instructions))
