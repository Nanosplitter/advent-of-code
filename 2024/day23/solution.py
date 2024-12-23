from collections import defaultdict
from itertools import product
from networkx.algorithms.clique import find_cliques as maximal_cliques
import networkx as nx
import sys

connections = defaultdict(list)

def is_interconnected(pair, node):
    return pair[0] in connections[node] and pair[1] in connections[node] and pair[0] in connections[pair[1]]

def get_interconnected_groups(group_size):
    groups = set()
    for connection in connections:
        
        pairs = list(product(connections[connection], repeat=group_size - 1))
        
        for pair in pairs:        
            if is_interconnected(pair, connection):
                groups.add(tuple(sorted(pair + (connection,))))

    return list(groups)

def part1() -> int:
    return sum([1 for clique in get_interconnected_groups(3) if any([node.startswith("t") for node in clique])])

def part2() -> tuple[int, set]:
    graph = nx.Graph(dict(connections))

    all_cliques = sorted((clique for clique in maximal_cliques(graph)), key=len, reverse=True)
    
    return ",".join(sorted(all_cliques[0]))

if len(sys.argv) < 2:
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    instructions = f.readlines()
    
    for connection in instructions:
        connection = connection.strip().split("-")
        connections[connection[0]].append(connection[1])
        connections[connection[1]].append(connection[0])
    
    
    print(part1())
    print(part2())