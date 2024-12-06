def part1(rules, updates):
    return sum([int(update[len(update)//2]) for update in updates if not any([rule[0] in update and rule[1] in update and update.index(rule[0]) > update.index(rule[1]) for rule in rules])])

def follows_rules(rules, update):
    return not any([rule[0] in update and rule[1] in update and update.index(rule[0]) > update.index(rule[1]) for rule in rules])

def part2(rules, updates):
    total = 0
    for update in updates:
        if follows_rules(rules, update):
            continue
        
        while not follows_rules(rules, update):
            for rule in rules:
                if rule[0] in update and rule[1] in update and update.index(rule[0]) > update.index(rule[1]):
                    r0i, r1i = update.index(rule[0]), update.index(rule[1])
                    update[r0i], update[r1i] = update[r1i], update[r0i]
            
        total += int(update[len(update)//2])
    
    return total

with open("input.txt") as f:
    instructions = f.readlines()
    
    parsing_rules = True
    rules = []
    updates = []
    
    for line in instructions:
        line = line.replace("\n", "")
        if len(line) == 0:
            parsing_rules = False
            continue
        
        if parsing_rules:
            rules.append(line.split("|"))
        else:
            updates.append(line.split(","))
            
    
    
    print(part1(rules, updates))
    print(part2(rules, updates))