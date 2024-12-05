import re

def part1(instructions: str) -> int:
    matches = [match.replace("mul(", "").replace(")", "") for match in re.findall(r"mul\([0-9]*,[0-9]*\)", instructions)]
    str_nums = [match.split(",") for match in matches]
    nums = [(int(nums[0]), int(nums[1])) for nums in str_nums]
    
    return sum([mul[0] * mul[1] for mul in nums])

def part2(instructions: str) -> int:
    instructions = f"do(){instructions}"
    
    dont_split = re.split(r"don't\(\)", instructions)
    everything_removed_before_do = [re.sub(r'^.*?do\(\)', 'do()', section) if "do()" in section else "" for section in dont_split]
    valid_instructions = "".join(everything_removed_before_do)
    
    return part1(valid_instructions)
    
with open("input.txt") as f:
    instructions = f.read().replace("\n", "")
    print(part1(instructions))
    print(part2(instructions))