from collections import defaultdict
import sys
    
def part1(wires, rules) -> int:
    
    x_wires = sorted([wire for wire in wires if wire.startswith("x")], reverse=True)
    y_wires = sorted([wire for wire in wires if wire.startswith("y")], reverse=True)
        
    
    
    x_binary = "".join([str(int(wires[wire])) for wire in x_wires])
    x_decimal = int(x_binary, 2)
    
    y_binary = "".join([str(int(wires[wire])) for wire in y_wires])
    y_decimal = int(y_binary, 2)
    
    print(f"x: {x_decimal}, y: {y_decimal}")
    
    for i in range(1000):
        for rule in rules:
            if rule[1] == "AND":
                wires[rule[3]] = wires[rule[0]] and wires[rule[2]]
            elif rule[1] == "OR":
                wires[rule[3]] = wires[rule[0]] or wires[rule[2]]
            elif rule[1] == "XOR":
                wires[rule[3]] = wires[rule[0]] != wires[rule[2]]
    
    
    z_wires = sorted([wire for wire in wires if wire.startswith("z")], reverse=True)
    
    z_binary = "".join([str(int(wires[wire])) for wire in z_wires])
    
    z_decimal = int(z_binary, 2)
    
    
    
    print(f"x: {x_decimal}, y: {y_decimal}, z: {z_decimal}")
        
    return wires

def part2(instructions) -> int:
    return 0

if len(sys.argv) < 2:
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    instructions = f.readlines()
    
    parsing_wires = True
    wires = defaultdict(bool)
    rules = []
    
    for line in instructions:
        line = line.strip()
        if len(line) == 0:
            parsing_wires = False
            continue
        
        if parsing_wires:
            wire = line.split(": ")
            wires[wire[0]] = wire[1] == "1"
        else:
            rule = line.split(" ")
            rule.remove("->")
            rules.append(rule)
            
    #print(wires)
    #print(rules)

    print(part1(wires, rules))
    #print(part2(instructions))