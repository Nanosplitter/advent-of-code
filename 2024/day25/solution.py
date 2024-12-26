import sys

def fits(key, lock):
    for i in range(5):
        if key[i] + lock[i] > 5:
            return False
    return True
    
def part1(keys, locks) -> int:
    working_pairs = 0
    for key in keys:
        for lock in locks:
            if fits(key, lock):
                working_pairs += 1
    return working_pairs

def part2(instructions) -> int:
    return 0

if len(sys.argv) < 2:
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    instructions = f.readlines()
    
    schematics = []
    
    schematic = []
    for line in instructions:
        if line == '\n':
            schematics.append(schematic)
            schematic = []
        else:
            schematic.append(line.strip())
    schematics.append(schematic)
    
    key_schematics = []
    lock_schematics = []
    
    for schematic in schematics:
        if schematic[0] == "#####":
            lock_schematics.append(schematic)
        else:
            key_schematics.append(schematic)
    
    keys = []
    for key_schematic in key_schematics:
        columns = zip(*key_schematic)
        hash_counts = [col.count('#') - 1 for col in columns]
        keys.append(hash_counts)
    
    locks = []
    for lock_schematic in lock_schematics:
        columns = zip(*lock_schematic)
        hash_counts = [col.count('#') - 1 for col in columns]
        locks.append(hash_counts)

    print(part1(keys, locks))
    #print(part2(instructions))