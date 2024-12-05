ending_cards = [1] * 214

for id, wins in enumerate([len(set(line[10:40].split()) & set(line[41:].split())) for line in open("input.txt").readlines()]):
    for i in range(id + 1, id + wins + 1):
        ending_cards[i] += ending_cards[id]

print(sum(ending_cards))