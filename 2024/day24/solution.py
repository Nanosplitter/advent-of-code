from collections import defaultdict
import sys
import graphviz
    
def part1(wires, rules) -> int:
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
        
    return z_decimal

def part2(wires, rules) -> int:
    dot = graphviz.Digraph(comment='Wires', format='png')
    
    wires = sorted(wires.keys())
    rules = sorted(rules)

    for wire in wires:
        dot.node(wire)

    for rule in rules:
        if rule[1] == "AND":
            gate_label = f"{rule[0]} AND {rule[2]}"
            color = "red"
        elif rule[1] == "OR":
            gate_label = f"{rule[0]} OR {rule[2]}"
            color = "green"
        elif rule[1] == "XOR":
            gate_label = f"{rule[0]} XOR {rule[2]}"
            color = "blue"

        dot.node(gate_label, rule[1], color=color)

        dot.edge(rule[0], gate_label)
        dot.edge(rule[2], gate_label)
        dot.edge(gate_label, rule[3])

    # dot.render('diagram.gv', view=False)

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

    print(part1(wires, rules))
    print(part2(wires, rules))